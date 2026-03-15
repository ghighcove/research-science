"""
prepub_check.py — Pre-publication check agent (RS-013)
Empire Lab

Automated scan before any article or finding goes public. Catches credibility errors,
attribution gaps, platform violations, and missing caveats.

MUST run before every publish. Triggered manually before Substack/Medium publish.

Usage:
    python pipelines/prepub_check.py findings/rs001b_knowledge_gap_analysis.md
    python pipelines/prepub_check.py articles/substack_draft_faers_delta_2026-03.md
    python pipelines/prepub_check.py --scan-all     # scan all articles/ and findings/

Exit codes:
    0 = PASS (may have warnings)
    1 = FAIL (blocking issues found — do not publish)
"""

from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path
from dataclasses import dataclass, field

ROOT = Path(__file__).parent.parent


# ── Check definitions ─────────────────────────────────────────────────────────

@dataclass
class CheckResult:
    name: str
    level: str  # BLOCK | WARN | INFO
    message: str
    line_ref: str = ""


def check_small_denominator_prr(text: str) -> list[CheckResult]:
    """Flag PRR statements that lack chi-squared or sample size context."""
    results = []
    # Match patterns like "PRR=XX" or "PRR of XX" without nearby "chi" or "n="
    prr_matches = list(re.finditer(r'PRR\s*[=≈]\s*[\d.]+', text, re.IGNORECASE))
    for m in prr_matches:
        context_window = text[max(0, m.start()-150):m.end()+150]
        has_chi = bool(re.search(r'chi|χ|chi2|chi-sq', context_window, re.IGNORECASE))
        has_n = bool(re.search(r'\bn\s*[=≈]\s*\d|count|reports|n=\d{1,6}', context_window, re.IGNORECASE))
        if not has_chi and not has_n:
            results.append(CheckResult(
                name="small_denominator_prr",
                level="WARN",
                message=f"PRR mentioned without chi² or n context near: '{text[m.start():m.end()+20]}'",
                line_ref=f"char {m.start()}",
            ))
    return results[:3]  # cap at 3 warnings (avoid noise flood)


def check_novel_in_prescribing_labels(text: str) -> list[CheckResult]:
    """Warn if 'novel' signals are declared without a caveat about label supplementary data."""
    results = []
    novel_count = len(re.findall(r'\bnovel\b', text, re.IGNORECASE))
    has_caveat = bool(re.search(
        r'labeling|prescribing information|package insert|supplementary|investigator.?s brochure|label',
        text, re.IGNORECASE
    ))
    if novel_count >= 3 and not has_caveat:
        results.append(CheckResult(
            name="novel_signal_caveat",
            level="WARN",
            message=(
                f"'{novel_count}' uses of 'novel' without caveat that signals may appear in "
                "prescribing labels/supplementary data not captured in trial profiles. Add: "
                "'Note: novel relative to published trial AE profile summaries — may appear in labeling.'"
            ),
        ))
    return results


def check_causation_language(text: str) -> list[CheckResult]:
    """Flag causal language in pharmacovigilance/observational content."""
    results = []
    causal_patterns = [
        (r'\b(causes?|caused|causing)\b(?!.*caveat|.*note|.*correlation)',
         "Direct causation claim"),
        (r'\b(proves?|proven|proof)\b',
         "Proof language"),
        (r'\b(definitively shows?|conclusively)\b',
         "Overly conclusive language"),
    ]
    for pattern, label in causal_patterns:
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            context = text[max(0, m.start()-50):m.end()+50].replace('\n', ' ')
            results.append(CheckResult(
                name="causation_language",
                level="BLOCK",
                message=f"{label}: '...{context}...' — pharmacovigilance signals are not causal proof.",
                line_ref=f"char {m.start()}",
            ))
    return results


def check_indication_bias_caveat(text: str) -> list[CheckResult]:
    """Check that suicide/self-harm signals have indication confounding caveat."""
    results = []
    has_suicide_signal = bool(re.search(
        r'suicide|self.?harm|self-injur|suicidal', text, re.IGNORECASE
    ))
    has_indication_caveat = bool(re.search(
        r'indication.?bias|indication.?confound|underlying.?disease|depression.*itself|confound',
        text, re.IGNORECASE
    ))
    if has_suicide_signal and not has_indication_caveat:
        results.append(CheckResult(
            name="indication_bias_caveat",
            level="BLOCK",
            message=(
                "Suicide/self-harm signals present without indication confounding caveat. "
                "Must add: 'Patients on SSRIs have depression; suicide signals may reflect the "
                "underlying disease, not solely the drug.'"
            ),
        ))
    return results


def check_mental_health_resource(text: str) -> list[CheckResult]:
    """Require mental health resource line in articles discussing suicide signals."""
    results = []
    has_suicide = bool(re.search(r'suicide|self.?harm|suicidal', text, re.IGNORECASE))
    has_resource = bool(re.search(
        r'988|crisis|hotline|mental.?health.?resource|lifeline|if you.?re struggling',
        text, re.IGNORECASE
    ))
    if has_suicide and not has_resource:
        results.append(CheckResult(
            name="mental_health_resource",
            level="BLOCK",
            message=(
                "Article discusses suicide signals but has no mental health resource line. "
                "Add before publishing: 'If you or someone you know is struggling, "
                "contact the 988 Suicide & Crisis Lifeline by calling or texting 988.'"
            ),
        ))
    return results


def check_local_file_paths(text: str) -> list[CheckResult]:
    """Block publication if local file paths are embedded in the text."""
    results = []
    path_patterns = [
        r'[A-Z]:[/\\][^\s<>"]{5,}',   # Windows: G:/ai/...
        r'/Users/[^\s<>"]{3,}',         # macOS home
        r'/home/[^\s<>"]{3,}',          # Linux home
        r'C:\\Users\\[^\s<>"]{3,}',     # Windows home
    ]
    for pattern in path_patterns:
        m = re.search(pattern, text)
        if m:
            results.append(CheckResult(
                name="local_file_path",
                level="BLOCK",
                message=f"Local file path found: '{m.group()}' — must be removed before publishing.",
                line_ref=f"char {m.start()}",
            ))
    return results


def check_first_person_in_body(text: str) -> list[CheckResult]:
    """Warn if first-person voice appears in the article body (not in designated intro/quote sections)."""
    results = []
    # Exclude lines that look like intro/attribution sections
    body_lines = []
    in_attribution = False
    for line in text.split('\n'):
        if re.search(r'^#|attribution|intro|note:|author|bio', line, re.IGNORECASE):
            in_attribution = True
        if re.search(r'^---', line):
            in_attribution = False
        if not in_attribution:
            body_lines.append(line)

    body = '\n'.join(body_lines)
    first_person = re.findall(r'\b(I |I\'m |I\'ve |my |I think|in my experience)\b', body)
    if len(first_person) > 2:
        results.append(CheckResult(
            name="first_person_voice",
            level="WARN",
            message=(
                f"First-person voice ({len(first_person)} instances) in article body. "
                "Analytical content should be objective/third-person per article-attribution rules."
            ),
        ))
    return results


def check_table_in_medium_article(text: str, filepath: Path) -> list[CheckResult]:
    """Block HTML tables in Medium articles (Medium strips them)."""
    results = []
    if "medium" in filepath.name.lower() or "medium" in str(filepath).lower():
        has_html_table = bool(re.search(r'<table|<tr |<td ', text, re.IGNORECASE))
        if has_html_table:
            results.append(CheckResult(
                name="html_table_medium",
                level="BLOCK",
                message="HTML <table> found in Medium article. Medium strips tables — must convert to PNG image.",
            ))
    return results


def check_faers_reporting_bias_caveat(text: str) -> list[CheckResult]:
    """Require FAERS reporting bias caveat in any FAERS analysis article."""
    results = []
    has_faers = bool(re.search(r'FAERS|adverse event|pharmacovigilance', text, re.IGNORECASE))
    has_caveat = bool(re.search(
        r'reporting.?bias|under.?report|PRR.*(not|does not|doesn.t).*(incidence|rate)',
        text, re.IGNORECASE
    ))
    # Only require in articles (not raw findings files)
    is_article = bool(re.search(r'substack|medium|article', str(text[:500]).lower()))
    if has_faers and not has_caveat and is_article:
        results.append(CheckResult(
            name="faers_reporting_bias",
            level="WARN",
            message=(
                "FAERS analysis without reporting bias caveat. "
                "Add: 'FAERS is a voluntary reporting system — PRR does not equal incidence rate.'"
            ),
        ))
    return results


# ── Runner ────────────────────────────────────────────────────────────────────

ALL_CHECKS = [
    check_small_denominator_prr,
    check_novel_in_prescribing_labels,
    check_causation_language,
    check_indication_bias_caveat,
    check_mental_health_resource,
    check_local_file_paths,
    check_first_person_in_body,
    check_faers_reporting_bias_caveat,
]


def run_checks(filepath: Path) -> list[CheckResult]:
    text = filepath.read_text(encoding="utf-8", errors="replace")
    results = []
    for check_fn in ALL_CHECKS:
        try:
            if check_fn.__name__ == "check_table_in_medium_article":
                results.extend(check_fn(text, filepath))
            else:
                results.extend(check_fn(text))
        except Exception as e:
            results.append(CheckResult(
                name=check_fn.__name__,
                level="INFO",
                message=f"Check error: {e}",
            ))
    return results


def format_report(filepath: Path, results: list[CheckResult]) -> str:
    blocks = results
    warnings = [r for r in results if r.level == "WARN"]
    infos = [r for r in results if r.level == "INFO"]

    blocks_list = [r for r in results if r.level == "BLOCK"]
    pass_fail = "FAIL -- DO NOT PUBLISH" if blocks_list else "PASS"

    lines = [
        f"## Pre-publication check: {filepath.name}",
        f"**Result**: {pass_fail}",
        f"**Blocking issues**: {len(blocks_list)} | **Warnings**: {len(warnings)}",
        "",
    ]

    if blocks_list:
        lines.append("### [BLOCK] Blocking Issues (must fix before publishing)")
        for r in blocks_list:
            lines.append(f"- {r.name}: {r.message}")
            if r.line_ref:
                lines.append(f"  (at {r.line_ref})")
        lines.append("")

    if warnings:
        lines.append("### [WARN] Warnings (review before publishing)")
        for r in warnings:
            lines.append(f"- {r.name}: {r.message}")
        lines.append("")

    if not blocks_list and not warnings:
        lines.append("*No issues found.*")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Pre-publication check agent")
    parser.add_argument("files", nargs="*", help="Files to check")
    parser.add_argument("--scan-all", action="store_true",
                        help="Scan all articles/ and findings/*.md files")
    args = parser.parse_args()

    targets = []
    if args.scan_all:
        targets.extend((ROOT / "articles").glob("*.md"))
        targets.extend((ROOT / "findings").glob("*.md"))
    else:
        for f in args.files:
            p = Path(f)
            if not p.is_absolute():
                p = ROOT / f
            targets.append(p)

    if not targets:
        print("Usage: python pipelines/prepub_check.py <file> [file2 ...] [--scan-all]")
        sys.exit(1)

    overall_fail = False
    for target in targets:
        if not target.exists():
            print(f"[prepub] Not found: {target}")
            continue
        results = run_checks(target)
        report = format_report(target, results)
        print(report)
        print()
        if any(r.level == "BLOCK" for r in results):
            overall_fail = True

    sys.exit(1 if overall_fail else 0)


if __name__ == "__main__":
    main()
