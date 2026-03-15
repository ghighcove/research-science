"""
RS-001: FAERS Pharmacovigilance — SSRI Adverse Event Signal Detection
Empire Lab, 2026-03-14

Uses openFDA drug/event API to compute Proportional Reporting Ratios (PRR)
and Reporting Odds Ratios (ROR) for SSRIs vs. the full FAERS background.

Signal criteria (Evans et al., standard pharmacovigilance):
  PRR >= 2.0  AND  count >= 3  AND  chi-squared >= 4

Output: findings/YYYY-MM-DD_faers_ssri_signals.md
"""

import requests
import json
import math
import time
import csv
import os
from datetime import date
from collections import defaultdict

# ── Configuration ──────────────────────────────────────────────────────────────

BASE_URL = "https://api.fda.gov/drug/event.json"
RATE_LIMIT_SLEEP = 1.5  # seconds between requests (no API key = 40/min)

SSRIS = {
    "fluoxetine":    "Fluoxetine (Prozac)",
    "sertraline":    "Sertraline (Zoloft)",
    "escitalopram":  "Escitalopram (Lexapro)",
    "paroxetine":    "Paroxetine (Paxil)",
    "citalopram":    "Citalopram (Celexa)",
    "fluvoxamine":   "Fluvoxamine (Luvox)",
}

# Events known from published SSRI trial data (for comparison)
KNOWN_SSRI_AES = {
    "nausea", "insomnia", "headache", "diarrhoea", "diarrhea",
    "dry mouth", "somnolence", "dizziness", "fatigue", "anxiety",
    "ejaculation disorder", "decreased libido", "hyperhidrosis",
    "tremor", "constipation", "vomiting", "weight decreased",
    "drug withdrawal syndrome",  # discontinuation syndrome
    "suicidal ideation",         # black box warning
}

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "findings")

# ── API helpers ────────────────────────────────────────────────────────────────

def api_get(params, retries=3):
    """Single openFDA API call with retry."""
    for attempt in range(retries):
        try:
            r = requests.get(BASE_URL, params=params, timeout=15)
            if r.status_code == 200:
                return r.json()
            elif r.status_code == 404:
                return None  # zero results
            else:
                print(f"    HTTP {r.status_code}, retrying...")
                time.sleep(3)
        except Exception as e:
            print(f"    Error: {e}, retrying...")
            time.sleep(3)
    return None

def get_total_reports():
    """Total reports in FAERS."""
    data = api_get({"limit": 1})
    if data:
        return data["meta"]["results"]["total"]
    return None

def get_drug_total(drug_name):
    """Total reports mentioning drug X (any indication/role)."""
    time.sleep(RATE_LIMIT_SLEEP)
    data = api_get({
        "search": f'patient.drug.medicinalproduct:"{drug_name.upper()}"',
        "limit": 1
    })
    if data:
        return data["meta"]["results"]["total"]
    return 0

def get_drug_events(drug_name, limit=200):
    """Top events for drug X, with counts."""
    time.sleep(RATE_LIMIT_SLEEP)
    data = api_get({
        "search": f'patient.drug.medicinalproduct:"{drug_name.upper()}"',
        "count": "patient.reaction.reactionmeddrapt.exact",
        "limit": limit
    })
    if data and "results" in data:
        return {r["term"].lower(): r["count"] for r in data["results"]}
    return {}

def get_event_total(event_term):
    """Total reports for event Y across all drugs."""
    time.sleep(RATE_LIMIT_SLEEP)
    escaped = event_term.replace('"', '\\"')
    data = api_get({
        "search": f'patient.reaction.reactionmeddrapt:"{escaped}"',
        "limit": 1
    })
    if data:
        return data["meta"]["results"]["total"]
    return 0

# ── Signal calculation ─────────────────────────────────────────────────────────

def compute_prr(a, n_drug, n_event, n_total):
    """
    PRR = [a / n_drug] / [n_event / n_total]
    a        = count(drug AND event)
    n_drug   = total reports for drug
    n_event  = total reports for event (all drugs)
    n_total  = total reports in DB
    """
    if n_drug == 0 or n_event == 0 or n_total == 0:
        return None, None
    prr = (a / n_drug) / (n_event / n_total)
    # Chi-squared approximation
    b = n_drug - a
    c = n_event - a
    d = n_total - n_drug - c
    if b <= 0 or c <= 0 or d <= 0:
        return prr, 0
    ror = (a * d) / (b * c) if (b * c) > 0 else None
    # Chi-squared (Yates corrected)
    expected = (n_drug * n_event) / n_total
    if expected > 0:
        chi2 = (abs(a - expected) - 0.5) ** 2 / expected
    else:
        chi2 = 0
    return prr, chi2

def is_signal(count, prr, chi2):
    """Evans criteria: count>=3, PRR>=2, chi2>=4."""
    return count >= 3 and prr is not None and prr >= 2.0 and chi2 is not None and chi2 >= 4.0

# ── Main pipeline ──────────────────────────────────────────────────────────────

def run():
    print("=" * 60)
    print("RS-001: FAERS SSRI Signal Detection")
    print("Empire Lab | openFDA API")
    print("=" * 60)

    print("\n[1] Getting total report count...")
    n_total = get_total_reports()
    print(f"    Total FAERS reports: {n_total:,}")

    results = {}  # drug -> list of (event, count, prr, chi2, is_known)

    for drug_key, drug_label in SSRIS.items():
        print(f"\n[2] Analyzing {drug_label}...")

        n_drug = get_drug_total(drug_key)
        print(f"    Reports mentioning {drug_key}: {n_drug:,}")
        if n_drug == 0:
            print("    No reports found — skipping.")
            continue

        events = get_drug_events(drug_key, limit=150)
        print(f"    Top events returned: {len(events)}")

        signals = []
        # Get event totals for top events (rate-limit aware)
        print(f"    Computing PRR for each event...")
        for i, (event, count) in enumerate(
            sorted(events.items(), key=lambda x: -x[1])[:100]
        ):
            n_event = get_event_total(event)
            if n_event == 0:
                continue
            prr, chi2 = compute_prr(count, n_drug, n_event, n_total)
            known = any(k in event.lower() for k in KNOWN_SSRI_AES)
            if count >= 3:  # store all with min count; filter later
                signals.append({
                    "event": event,
                    "count": count,
                    "n_drug": n_drug,
                    "n_event": n_event,
                    "prr": prr,
                    "chi2": chi2,
                    "is_signal": is_signal(count, prr, chi2),
                    "is_known": known,
                })
            if (i + 1) % 10 == 0:
                print(f"      ... {i+1} events processed")

        results[drug_key] = {
            "label": drug_label,
            "n_drug": n_drug,
            "signals": signals,
        }
        print(f"    Signals detected (Evans criteria): "
              f"{sum(1 for s in signals if s['is_signal'])}")

    return results, n_total

def write_report(results, n_total):
    today = date.today().strftime("%Y-%m-%d")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    outpath = os.path.join(OUTPUT_DIR, f"{today}_faers_ssri_signals.md")

    lines = [
        f"# FAERS Watch — SSRI Adverse Event Signals",
        f"**Date**: {today}",
        f"**Method**: Proportional Reporting Ratio (PRR) via openFDA API",
        f"**Signal criteria**: PRR ≥ 2.0, count ≥ 3, chi² ≥ 4.0 (Evans et al.)",
        f"**Total FAERS reports analyzed**: {n_total:,}",
        f"**Drugs analyzed**: {', '.join(SSRIS.keys())}",
        f"",
        f"---",
        f"",
        f"## Summary",
        f"",
    ]

    all_novel_signals = []

    for drug_key, data in results.items():
        sigs = [s for s in data["signals"] if s["is_signal"]]
        novel = [s for s in sigs if not s["is_known"]]
        all_novel_signals.extend([(drug_key, data["label"], s) for s in novel])
        lines.append(f"- **{data['label']}**: {data['n_drug']:,} reports, "
                     f"{len(sigs)} signals ({len(novel)} novel / not in trial AE profile)")

    lines += [
        f"",
        f"---",
        f"",
        f"## Novel Signals (Not in Published Trial Adverse Event Profiles)",
        f"",
        f"These signals meet Evans criteria AND are not among the commonly reported",
        f"SSRl adverse events from published trial data. Requires clinical interpretation.",
        f"",
        f"| Drug | Event | Count | PRR | Chi² | Notes |",
        f"|------|-------|-------|-----|------|-------|",
    ]

    for drug_key, drug_label, s in sorted(
        all_novel_signals, key=lambda x: -(x[2]["prr"] or 0)
    )[:50]:
        prr_str = f"{s['prr']:.1f}" if s["prr"] else "?"
        chi2_str = f"{s['chi2']:.1f}" if s["chi2"] else "?"
        lines.append(
            f"| {drug_label} | {s['event'].title()} | {s['count']:,} | "
            f"{prr_str} | {chi2_str} | |"
        )

    lines += [
        f"",
        f"---",
        f"",
        f"## Full Signal Tables by Drug",
        f"",
    ]

    for drug_key, data in results.items():
        sigs = sorted(
            [s for s in data["signals"] if s["is_signal"]],
            key=lambda x: -(x["prr"] or 0),
        )
        lines += [
            f"### {data['label']}",
            f"Total reports: {data['n_drug']:,} | Signals: {len(sigs)}",
            f"",
            f"| Event | Count | PRR | Chi² | Known AE? |",
            f"|-------|-------|-----|------|-----------|",
        ]
        for s in sigs[:40]:
            prr_str = f"{s['prr']:.2f}" if s["prr"] else "?"
            chi2_str = f"{s['chi2']:.1f}" if s["chi2"] else "?"
            known_str = "✓" if s["is_known"] else "**novel**"
            lines.append(
                f"| {s['event'].title()} | {s['count']:,} | "
                f"{prr_str} | {chi2_str} | {known_str} |"
            )
        lines.append("")

    lines += [
        f"---",
        f"",
        f"## Methodology Notes",
        f"",
        f"**Data source**: FDA FAERS via openFDA API (opendata.fda.gov). "
        f"Covers voluntary adverse event reports submitted by patients, providers, and manufacturers.",
        f"",
        f"**PRR formula**: `(a / N_drug) / (N_event / N_total)` where a = reports with both "
        f"drug and event, N_drug = total drug reports, N_event = total event reports, "
        f"N_total = total FAERS reports.",
        f"",
        f"**Limitations**:",
        f"- FAERS captures reports, not causation. High PRR = disproportionate reporting, not proven harm.",
        f"- Notoriety bias: widely-publicized effects are over-reported.",
        f"- Weber effect: new drugs accumulate reports rapidly in first 2 years.",
        f"- Drug name matching is approximate (brand/generic variation in reports).",
        f"- Co-medication confounding: patients taking SSRIs typically take other drugs.",
        f"",
        f"**Novel signal interpretation**: Signals not in known SSRI AE profiles warrant "
        f"clinical pharmacologist review. They may reflect: (1) real under-labeled effects, "
        f"(2) confounding by co-medications, (3) indication bias, or (4) reporting artifacts.",
        f"",
        f"*Generated by Empire Lab RS-001. Methodology open for independent verification.*",
    ]

    with open(outpath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"\nReport written: {outpath}")
    return outpath

if __name__ == "__main__":
    results, n_total = run()
    outpath = write_report(results, n_total)
    print(f"\nDone. Open: {outpath}")
