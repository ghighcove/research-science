"""
faers_delta_monitor.py — Monthly FAERS delta monitor (RS-001d)
Empire Lab

Runs the FAERS PRR pipeline, diffs vs prior month's snapshot in SQLite,
identifies new signals crossing Evans criteria, and auto-drafts a Substack
post for any noteworthy new findings.

Usage:
    python pipelines/faers_delta_monitor.py               # run delta, draft post if new signals
    python pipelines/faers_delta_monitor.py --dry-run     # show what would run
    python pipelines/faers_delta_monitor.py --force       # re-run even if already ran this month

Wire into Billy cron: 1st of month, 2 AM.
Output: findings/faers_delta_YYYY-MM.md + articles/substack_draft_YYYY-MM.md (if new signals)
"""

from __future__ import annotations
import argparse
import json
import math
import os
import sqlite3
import sys
import time
from datetime import date, datetime
from pathlib import Path

import requests

# ── Paths ─────────────────────────────────────────────────────────────────────

ROOT = Path(__file__).parent.parent
FINDINGS_DIR = ROOT / "findings"
ARTICLES_DIR = ROOT / "articles"
DATA_DIR = ROOT / "data"
DB_PATH = DATA_DIR / "faers_signals.db"

FINDINGS_DIR.mkdir(exist_ok=True)
ARTICLES_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)

# ── Config (matches faers_prr.py) ─────────────────────────────────────────────

BASE_URL = "https://api.fda.gov/drug/event.json"
RATE_LIMIT_SLEEP = 1.5

SSRIS = {
    "fluoxetine":    "Fluoxetine (Prozac)",
    "sertraline":    "Sertraline (Zoloft)",
    "escitalopram":  "Escitalopram (Lexapro)",
    "paroxetine":    "Paroxetine (Paxil)",
    "citalopram":    "Citalopram (Celexa)",
    "fluvoxamine":   "Fluvoxamine (Luvox)",
}

KNOWN_SSRI_AES = {
    "nausea", "insomnia", "headache", "diarrhoea", "diarrhea",
    "dry mouth", "somnolence", "dizziness", "fatigue", "anxiety",
    "ejaculation disorder", "decreased libido", "hyperhidrosis",
    "tremor", "constipation", "vomiting", "weight decreased",
    "drug withdrawal syndrome", "suicidal ideation",
}

PRR_THRESHOLD = 2.0
COUNT_THRESHOLD = 3
CHI2_THRESHOLD = 4.0


# ── Database ──────────────────────────────────────────────────────────────────

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS signals (
            run_date TEXT,
            drug TEXT,
            event TEXT,
            count INTEGER,
            prr REAL,
            chi2 REAL,
            novel INTEGER,
            PRIMARY KEY (run_date, drug, event)
        )
    """)
    conn.commit()
    return conn


def save_signals(conn, run_date: str, drug: str, signals: list[dict]):
    for s in signals:
        conn.execute("""
            INSERT OR REPLACE INTO signals (run_date, drug, event, count, prr, chi2, novel)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (run_date, drug, s["event"], s["count"], s["prr"], s["chi2"],
               1 if s.get("novel") else 0))
    conn.commit()


def load_prior_signals(conn, drug: str, exclude_run_date: str) -> set[str]:
    """Return set of event strings seen for this drug in any prior run."""
    rows = conn.execute(
        "SELECT DISTINCT event FROM signals WHERE drug=? AND run_date != ?",
        (drug, exclude_run_date)
    ).fetchall()
    return {r[0] for r in rows}


def has_run_this_month(conn) -> bool:
    ym = date.today().strftime("%Y-%m")
    rows = conn.execute(
        "SELECT COUNT(*) FROM signals WHERE run_date LIKE ?", (f"{ym}%",)
    ).fetchone()
    return rows[0] > 0


# ── API helpers (mirrors faers_prr.py logic) ──────────────────────────────────

def get_total_reports() -> int:
    r = requests.get(BASE_URL, params={"limit": 1}, timeout=30)
    return r.json()["meta"]["results"]["total"]


def get_drug_event_counts(drug: str, top_n: int = 50) -> list[dict]:
    """Get top N adverse events for a drug by report count."""
    params = {
        "search": f'patient.drug.medicinalproduct:"{drug}"',
        "count": "patient.reaction.reactionmeddrapt.exact",
        "limit": top_n,
    }
    try:
        r = requests.get(BASE_URL, params=params, timeout=30)
        r.raise_for_status()
        return r.json().get("results", [])
    except Exception:
        return []


def get_event_background(event: str) -> int:
    """Total FAERS reports mentioning this event (any drug)."""
    params = {
        "search": f'patient.reaction.reactionmeddrapt:"{event}"',
        "limit": 1,
    }
    try:
        r = requests.get(BASE_URL, params=params, timeout=30)
        r.raise_for_status()
        return r.json()["meta"]["results"]["total"]
    except Exception:
        return 0


def compute_prr(a: int, b: int, c: int, d: int) -> tuple[float, float]:
    """PRR and chi-squared. a=drug+event, b=drug-event, c=bg+event, d=bg-event."""
    if b == 0 or c == 0:
        return 0.0, 0.0
    prr = (a / (a + b)) / (c / (c + d))
    # Chi-squared (simplified 2x2)
    n = a + b + c + d
    expected = (a + b) * (a + c) / n
    if expected == 0:
        return prr, 0.0
    chi2 = (a - expected) ** 2 / expected
    return prr, chi2


def run_pipeline(dry_run: bool = False) -> dict[str, list[dict]]:
    """Run full PRR pipeline, return signals per drug."""
    print(f"[delta_monitor] Fetching total FAERS reports...")
    total_reports = get_total_reports()
    print(f"[delta_monitor] Total reports: {total_reports:,}")

    results = {}
    for drug_key, drug_label in SSRIS.items():
        if dry_run:
            print(f"  [DRY RUN] Would fetch {drug_key}")
            results[drug_key] = []
            continue

        print(f"  Fetching {drug_label}...")
        events = get_drug_event_counts(drug_key, top_n=100)
        time.sleep(RATE_LIMIT_SLEEP)

        drug_total = sum(e["count"] for e in events)
        signals = []

        for event_rec in events:
            event = event_rec["term"]
            a = event_rec["count"]  # drug + event
            b = drug_total - a       # drug - event

            time.sleep(RATE_LIMIT_SLEEP * 0.5)
            bg_count = get_event_background(event)
            c = max(0, bg_count - a)
            d = max(0, total_reports - drug_total - c)

            prr, chi2 = compute_prr(a, b, c, d)

            if prr >= PRR_THRESHOLD and a >= COUNT_THRESHOLD and chi2 >= CHI2_THRESHOLD:
                signals.append({
                    "event": event,
                    "count": a,
                    "prr": round(prr, 2),
                    "chi2": round(chi2, 1),
                    "novel": event.lower() not in KNOWN_SSRI_AES,
                })

        results[drug_key] = sorted(signals, key=lambda x: x["prr"], reverse=True)
        print(f"    → {len(signals)} signals")

    return results


# ── Delta analysis ────────────────────────────────────────────────────────────

def compute_delta(conn, run_date: str, current: dict[str, list[dict]]) -> dict:
    """Compare current signals to prior snapshots. Return new/lost/unchanged."""
    new_signals = {}
    lost_signals = {}

    for drug, signals in current.items():
        prior_events = load_prior_signals(conn, drug, run_date)
        current_events = {s["event"] for s in signals}

        new_for_drug = [s for s in signals if s["event"] not in prior_events]
        lost_for_drug = [e for e in prior_events if e not in current_events]

        if new_for_drug:
            new_signals[drug] = new_for_drug
        if lost_for_drug:
            lost_signals[drug] = lost_for_drug

    return {"new": new_signals, "lost": lost_signals}


# ── Report writer ─────────────────────────────────────────────────────────────

def write_delta_report(run_date: str, current: dict, delta: dict) -> Path:
    ym = run_date[:7]
    out = FINDINGS_DIR / f"faers_delta_{ym}.md"

    total_new = sum(len(v) for v in delta["new"].values())
    total_lost = sum(len(v) for v in delta["lost"].values())
    total_signals = sum(len(v) for v in current.values())

    lines = [
        f"# FAERS SSRI Delta Report — {ym}",
        f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')} | RS-001d monthly monitor*",
        "",
        "---",
        "",
        f"## Summary",
        "",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| Total active signals | {total_signals} |",
        f"| New signals this month | {total_new} |",
        f"| Resolved signals | {total_lost} |",
        "",
    ]

    if total_new > 0:
        lines += ["## New Signals (crossed Evans threshold this month)", ""]
        for drug, sigs in delta["new"].items():
            label = SSRIS.get(drug, drug)
            lines.append(f"### {label}")
            lines.append("| Event | Count | PRR | Chi² | Novel? |")
            lines.append("|-------|-------|-----|------|--------|")
            for s in sigs:
                novel = "**novel**" if s["novel"] else "known"
                lines.append(f"| {s['event']} | {s['count']:,} | {s['prr']} | {s['chi2']} | {novel} |")
            lines.append("")
    else:
        lines += ["## New Signals", "", "*None this month — signal profile stable.*", ""]

    if total_lost > 0:
        lines += ["## Resolved Signals (no longer meeting Evans criteria)", ""]
        for drug, events in delta["lost"].items():
            label = SSRIS.get(drug, drug)
            lines.append(f"**{label}**: {', '.join(events)}")
        lines.append("")

    lines += [
        "## Current Signal Counts by Drug",
        "",
        "| Drug | Signals | Novel |",
        "|------|---------|-------|",
    ]
    for drug, sigs in current.items():
        label = SSRIS.get(drug, drug)
        novel_count = sum(1 for s in sigs if s.get("novel"))
        lines.append(f"| {label} | {len(sigs)} | {novel_count} |")

    lines += ["", f"*Next run: {ym}-01 +1 month auto via Billy cron*"]

    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"[delta_monitor] Delta report: {out}")
    return out


def write_substack_draft(run_date: str, delta: dict) -> Path | None:
    """Draft a Substack post if there are noteworthy new signals."""
    total_new = sum(len(v) for v in delta["new"].values())
    if total_new == 0:
        return None

    ym = run_date[:7]
    out = ARTICLES_DIR / f"substack_draft_faers_delta_{ym}.md"

    # Find the most notable new signal
    top_drug = None
    top_signal = None
    top_prr = 0
    for drug, sigs in delta["new"].items():
        for s in sigs:
            if s["prr"] > top_prr:
                top_prr = s["prr"]
                top_signal = s
                top_drug = drug

    drug_label = SSRIS.get(top_drug, top_drug) if top_drug else "SSRI"

    lines = [
        f"# FAERS Watch: {total_new} New Adverse Event Signal{'s' if total_new > 1 else ''} — {ym}",
        "",
        "*[Empire Lab FAERS Monthly Monitor — auto-draft. Review and humanize before publishing.]*",
        "",
        "---",
        "",
        "Each month, I re-run the Empire Lab FAERS signal detection pipeline against the latest",
        "FDA adverse event database. This month's scan across 6 SSRIs and 20M+ reports identified",
        f"**{total_new} new signal{'s' if total_new > 1 else ''}** crossing the Evans pharmacovigilance threshold.",
        "",
    ]

    if top_signal:
        lines += [
            f"## Lead Finding: {top_signal['event']} × {drug_label}",
            "",
            f"A new signal emerged for **{drug_label}** this month: **{top_signal['event']}**",
            f"(PRR={top_signal['prr']}, n={top_signal['count']:,}, χ²={top_signal['chi2']}).",
            "",
            "PRR measures how much more likely this adverse event is in patients on this drug",
            "compared to the overall FAERS background. A PRR ≥ 2 with sufficient sample size",
            "and statistical significance triggers pharmacovigilance follow-up.",
            "",
        ]

    lines += [
        "## All New Signals This Month",
        "",
        "| Drug | Event | Count | PRR | Novel? |",
        "|------|-------|-------|-----|--------|",
    ]
    for drug, sigs in delta["new"].items():
        label = SSRIS.get(drug, drug)
        for s in sigs:
            novel = "Yes" if s["novel"] else "Known"
            lines.append(f"| {label} | {s['event']} | {s['count']:,} | {s['prr']} | {novel} |")

    lines += [
        "",
        "---",
        "",
        "## Methodology",
        "",
        "Proportional Reporting Ratio (PRR) via openFDA API. Evans criteria: PRR ≥ 2.0, n ≥ 3, χ² ≥ 4.0.",
        "Signals marked 'novel' are absent from published SSRI trial adverse event profiles.",
        "This is pharmacovigilance signal detection, not causation proof.",
        "",
        "**Data**: FDA FAERS public database | **Code**: github.com/ghighcove/research-science",
        "",
        "---",
        "*Empire Lab — independent signal detection. All methods open-source.*",
        "",
        f"*[TODO: add clinical interpretation of top signal before publishing]*",
        f"*[TODO: verify signal not artifact — check FAERS report quality for {top_signal['event'] if top_signal else 'top signal'}]*",
    ]

    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"[delta_monitor] Substack draft: {out}")
    return out


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="FAERS monthly delta monitor")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force", action="store_true", help="Re-run even if already ran this month")
    args = parser.parse_args()

    conn = init_db()
    run_date = date.today().isoformat()

    if not args.force and not args.dry_run:
        if has_run_this_month(conn):
            print(f"[delta_monitor] Already ran this month. Use --force to re-run.")
            conn.close()
            return

    if args.dry_run:
        print(f"[delta_monitor] DRY RUN — would fetch FAERS signals for: {list(SSRIS.keys())}")
        print(f"[delta_monitor] DB: {DB_PATH}")
        print(f"[delta_monitor] Output: findings/faers_delta_{date.today().strftime('%Y-%m')}.md")
        conn.close()
        return

    # Run pipeline
    current = run_pipeline()

    # Save to DB
    for drug, signals in current.items():
        save_signals(conn, run_date, drug, signals)

    # Delta vs prior months
    delta = compute_delta(conn, run_date, current)
    conn.close()

    # Write reports
    write_delta_report(run_date, current, delta)
    write_substack_draft(run_date, delta)

    total_new = sum(len(v) for v in delta["new"].values())
    print(f"[delta_monitor] Done. New signals: {total_new}. DB: {DB_PATH}")


if __name__ == "__main__":
    main()
