"""
clinicaltrials_pub_gap.py — ClinicalTrials.gov publication gap scanner (RS-003)
Empire Lab

Finds depression trials (2015-2020) with posted results but no linked peer-reviewed
publication. Ranks by enrollment size and sponsor type.

Uses ClinicalTrials.gov v2 API (api.clinicaltrials.gov).

Usage:
    python pipelines/clinicaltrials_pub_gap.py
    python pipelines/clinicaltrials_pub_gap.py --dry-run
    python pipelines/clinicaltrials_pub_gap.py --condition "bipolar disorder"
    python pipelines/clinicaltrials_pub_gap.py --start-year 2010 --end-year 2022

Output: findings/rs003_pub_gap_[condition]_[year-range].md
"""

from __future__ import annotations
import argparse
import json
import time
from datetime import datetime
from pathlib import Path

import requests

# ── Paths ─────────────────────────────────────────────────────────────────────

ROOT = Path(__file__).parent.parent
FINDINGS_DIR = ROOT / "findings"
FINDINGS_DIR.mkdir(exist_ok=True)

# ── Config ────────────────────────────────────────────────────────────────────

CT_API = "https://clinicaltrials.gov/api/v2/studies"
RATE_LIMIT_SLEEP = 0.5  # seconds between requests

SPONSOR_CATEGORIES = {
    "industry": ["pharma", "inc", "ltd", "llc", "corp", "bioscience", "pharmaceutical",
                 "therapeutics", "biotech", "ag", "gmbh", "sa", "plc"],
    "academic":  ["university", "univ", "college", "institute", "hospital", "medical center",
                  "clinic", "school of medicine"],
    "nih":       ["national institute", "nih", "nimh", "nida", "niaaa", "niaid"],
    "other_gov": ["department of", "veterans", "va ", "army", "navy", "air force", "cdc", "fda"],
}


def categorize_sponsor(sponsor_name: str) -> str:
    name = (sponsor_name or "").lower()
    for category, keywords in SPONSOR_CATEGORIES.items():
        if any(kw in name for kw in keywords):
            return category
    return "other"


# ── API ───────────────────────────────────────────────────────────────────────

def fetch_trials_page(
    condition: str,
    start_year: int,
    end_year: int,
    page_token: str | None = None,
    page_size: int = 100,
) -> dict:
    """Fetch one page of trial results from ClinicalTrials.gov v2 API."""
    params = {
        "query.cond": condition,
        "filter.advanced": (
            f"AREA[StartDate]RANGE[{start_year}-01-01,{end_year}-12-31]"
            " AND AREA[OverallStatus]COMPLETED"
            " AND AREA[ResultsFirstPostDate]RANGE[2000-01-01,2030-01-01]"
        ),
        "fields": ",".join([
            "NCTId", "BriefTitle", "OverallStatus", "EnrollmentCount",
            "LeadSponsorName", "LeadSponsorClass",
            "StartDate", "PrimaryCompletionDate", "ResultsFirstPostDate",
            "ReferencePMID", "ReferenceCitation",
        ]),
        "pageSize": page_size,
        "format": "json",
    }
    if page_token:
        params["pageToken"] = page_token

    r = requests.get(CT_API, params=params, timeout=30)
    r.raise_for_status()
    return r.json()


def has_publication(study: dict) -> tuple[bool, str]:
    """
    Check if study has a linked peer-reviewed publication.
    Returns (has_pub, reason).
    """
    # Check for PMIDs linked to the study
    refs = study.get("protocolSection", {}).get("referencesModule", {})

    # v2 API nested structure
    references = refs.get("references", [])
    for ref in references:
        ref_type = ref.get("type", "")
        pmid = ref.get("pmid", "")
        if pmid and ref_type in ("RESULT", "DERIVED", "BACKGROUND"):
            return True, f"PMID:{pmid}"
        if pmid:
            return True, f"PMID:{pmid}"
        # Check citation text for journal markers
        citation = ref.get("citation", "")
        if citation and any(marker in citation.lower() for marker in
                            [". doi:", "pubmed", "pmid", "j med", "lancet", "jama", "nejm",
                             "annals", "bmj", "plos", "nature", "science"]):
            return True, "citation link"

    return False, "no publication found"


def fetch_all_trials(
    condition: str,
    start_year: int,
    end_year: int,
    max_trials: int = 500,
) -> list[dict]:
    """Fetch all matching trials (up to max_trials)."""
    all_trials = []
    page_token = None

    while len(all_trials) < max_trials:
        data = fetch_trials_page(condition, start_year, end_year, page_token)
        studies = data.get("studies", [])
        all_trials.extend(studies)

        page_token = data.get("nextPageToken")
        if not page_token or not studies:
            break
        time.sleep(RATE_LIMIT_SLEEP)

    return all_trials[:max_trials]


def extract_study_fields(study: dict) -> dict:
    """Extract flat fields from nested v2 study object."""
    protocol = study.get("protocolSection", {})
    id_module = protocol.get("identificationModule", {})
    status_module = protocol.get("statusModule", {})
    design_module = protocol.get("designModule", {})
    sponsor_module = protocol.get("sponsorCollaboratorsModule", {})

    nct_id = id_module.get("nctId", "")
    title = id_module.get("briefTitle", "")
    enrollment = design_module.get("enrollmentInfo", {}).get("count", 0) or 0
    lead_sponsor = sponsor_module.get("leadSponsor", {})
    sponsor_name = lead_sponsor.get("name", "")
    sponsor_class = lead_sponsor.get("class", "")
    results_first_post = status_module.get("resultsFirstPostDateStruct", {}).get("date", "")
    primary_completion = status_module.get("primaryCompletionDateStruct", {}).get("date", "")
    start_date = status_module.get("startDateStruct", {}).get("date", "")

    has_pub, pub_evidence = has_publication(study)

    return {
        "nct_id": nct_id,
        "title": title,
        "enrollment": int(enrollment) if str(enrollment).isdigit() else 0,
        "sponsor": sponsor_name,
        "sponsor_category": categorize_sponsor(sponsor_name),
        "sponsor_class": sponsor_class,
        "start_date": start_date,
        "primary_completion": primary_completion,
        "results_posted": results_first_post,
        "has_publication": has_pub,
        "pub_evidence": pub_evidence,
        "url": f"https://clinicaltrials.gov/study/{nct_id}",
    }


# ── Report ────────────────────────────────────────────────────────────────────

def write_gap_report(
    condition: str,
    start_year: int,
    end_year: int,
    trials: list[dict],
) -> Path:
    """Write the publication gap findings report."""
    unpublished = [t for t in trials if not t["has_publication"]]
    published = [t for t in trials if t["has_publication"]]

    # Sort unpublished by enrollment desc
    unpublished_sorted = sorted(unpublished, key=lambda x: x["enrollment"], reverse=True)

    # Sponsor type breakdown
    sponsor_counts: dict[str, dict] = {}
    for t in trials:
        cat = t["sponsor_category"]
        if cat not in sponsor_counts:
            sponsor_counts[cat] = {"total": 0, "unpublished": 0, "enrollment": 0}
        sponsor_counts[cat]["total"] += 1
        sponsor_counts[cat]["enrollment"] += t["enrollment"]
        if not t["has_publication"]:
            sponsor_counts[cat]["unpublished"] += 1

    gap_rate = len(unpublished) / len(trials) * 100 if trials else 0
    total_unpublished_enrollment = sum(t["enrollment"] for t in unpublished)

    cond_slug = condition.lower().replace(" ", "_")
    out = FINDINGS_DIR / f"rs003_pub_gap_{cond_slug}_{start_year}-{end_year}.md"

    lines = [
        f"# RS-003 — ClinicalTrials.gov Publication Gap: {condition.title()}",
        f"*Date: {datetime.now().strftime('%Y-%m-%d')} | Years: {start_year}–{end_year}*",
        "",
        "---",
        "",
        "## Summary",
        "",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| Trials with posted results | {len(trials)} |",
        f"| Unpublished (no linked publication) | {len(unpublished)} ({gap_rate:.1f}%) |",
        f"| Published | {len(published)} ({100-gap_rate:.1f}%) |",
        f"| Participants in unpublished trials | {total_unpublished_enrollment:,} |",
        "",
        "## Publication Gap by Sponsor Type",
        "",
        "| Sponsor Type | Trials | Unpublished | Gap Rate | Total Enrollment |",
        "|-------------|--------|-------------|----------|-----------------|",
    ]

    for cat, counts in sorted(sponsor_counts.items(), key=lambda x: x[1]["total"], reverse=True):
        gap_pct = counts["unpublished"] / counts["total"] * 100 if counts["total"] else 0
        lines.append(
            f"| {cat.title()} | {counts['total']} | {counts['unpublished']} | "
            f"{gap_pct:.1f}% | {counts['enrollment']:,} |"
        )

    lines += [
        "",
        "## Top Unpublished Trials (by enrollment, descending)",
        "",
        "These trials have posted results on ClinicalTrials.gov but no linked peer-reviewed publication.",
        "",
        "| NCT ID | Enrollment | Sponsor | Type | Results Posted | Title |",
        "|--------|-----------|---------|------|---------------|-------|",
    ]

    for t in unpublished_sorted[:50]:
        title_short = t["title"][:60] + "…" if len(t["title"]) > 60 else t["title"]
        lines.append(
            f"| [{t['nct_id']}]({t['url']}) | {t['enrollment']:,} | "
            f"{t['sponsor'][:30]} | {t['sponsor_category']} | "
            f"{t['results_posted'][:10]} | {title_short} |"
        )

    lines += [
        "",
        "---",
        "",
        "## Interpretation",
        "",
        f"**{gap_rate:.0f}% of completed {condition} trials with posted results have no linked publication.**",
        "",
        "This represents **publication bias at the registration level**: trials complete, results",
        "are posted to ClinicalTrials.gov (required by FDAAA 2007 for many trials), but the",
        "peer-reviewed synthesis — the form that reaches clinicians and informs guidelines — is absent.",
        "",
        "**Participant burden**: {total_unpublished_enrollment:,} participants contributed data to trials".replace(
            "{total_unpublished_enrollment:,}", f"{total_unpublished_enrollment:,}"
        ) +
        " whose findings remain inaccessible in the clinical literature.",
        "",
        "**For Empire Lab**: Each unpublished trial is a potential RS research target. If the",
        "posted results show signal (significant outcomes, unexpected adverse events), an",
        "Empire Lab secondary analysis can surface findings that would otherwise stay buried.",
        "",
        "## Next Steps",
        "",
        "- [ ] Flag the top 10 unpublished trials for manual review of posted results",
        "- [ ] Check if any unpublished trials have significant primary outcome results",
        "- [ ] Cross-reference with FAERS: do any trial drugs appear in RS-001 signals?",
        "",
        f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')} | RS-003 pipeline*",
    ]

    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"[ct_pub_gap] Report: {out}")
    return out


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="ClinicalTrials.gov publication gap scanner")
    parser.add_argument("--condition", default="depression",
                        help="Medical condition to search (default: depression)")
    parser.add_argument("--start-year", type=int, default=2015)
    parser.add_argument("--end-year", type=int, default=2020)
    parser.add_argument("--max-trials", type=int, default=500)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if args.dry_run:
        print(f"[ct_pub_gap] DRY RUN")
        print(f"  Condition: {args.condition}")
        print(f"  Years: {args.start_year}–{args.end_year}")
        print(f"  Max trials: {args.max_trials}")
        print(f"  API: {CT_API}")
        out = FINDINGS_DIR / f"rs003_pub_gap_{args.condition.lower().replace(' ', '_')}_{args.start_year}-{args.end_year}.md"
        print(f"  Output: {out}")
        return

    print(f"[ct_pub_gap] Fetching {args.condition} trials {args.start_year}–{args.end_year}...")
    raw_trials = fetch_all_trials(
        args.condition, args.start_year, args.end_year, args.max_trials
    )
    print(f"[ct_pub_gap] Fetched {len(raw_trials)} trials with posted results")

    print("[ct_pub_gap] Extracting fields and checking publications...")
    trials = [extract_study_fields(s) for s in raw_trials]

    unpublished = [t for t in trials if not t["has_publication"]]
    print(f"[ct_pub_gap] Unpublished: {len(unpublished)} / {len(trials)} ({len(unpublished)/len(trials)*100:.1f}%)")

    write_gap_report(args.condition, args.start_year, args.end_year, trials)


if __name__ == "__main__":
    main()
