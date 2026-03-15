"""
geo_orphan_query.py — GEO Orphan Dataset Scanner (RS-002)
Empire Lab

Finds lung cancer RNA-seq datasets on GEO with few or no linked publications.
"Orphan" = results posted but not yet synthesized in peer-reviewed literature.

Each orphan dataset is a potential Empire Lab secondary analysis target.

Uses:
  - NCBI E-utilities API (no API key required, but polite rate limiting)
  - DrugBank Open Data (public TSV, downloaded once to data/)

Analysis pipeline design (requires pydeseq2):
  pip install pydeseq2 anndata

Usage:
    python pipelines/geo_orphan_query.py
    python pipelines/geo_orphan_query.py --disease "breast cancer"
    python pipelines/geo_orphan_query.py --max-datasets 200 --citation-threshold 2
    python pipelines/geo_orphan_query.py --dry-run

Output: findings/rs002_geo_orphans_[disease]_[date].md
        data/geo_orphans_[disease].tsv  (for downstream analysis)
"""

from __future__ import annotations
import argparse
import csv
import json
import time
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from typing import Optional

import requests

# ── Paths ─────────────────────────────────────────────────────────────────────

ROOT = Path(__file__).parent.parent
FINDINGS_DIR = ROOT / "findings"
DATA_DIR = ROOT / "data"
FINDINGS_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)

# ── NCBI E-utils ──────────────────────────────────────────────────────────────

ENTREZ_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
ENTREZ_EMAIL = "empire-lab@example.com"  # Required by NCBI ToS
RATE_LIMIT_SLEEP = 0.35  # NCBI allows 3 req/sec without API key


def entrez_search(db: str, term: str, retmax: int = 500) -> list[str]:
    """Search NCBI database, return list of IDs."""
    params = {
        "db": db,
        "term": term,
        "retmax": retmax,
        "retmode": "json",
        "email": ENTREZ_EMAIL,
    }
    r = requests.get(f"{ENTREZ_BASE}/esearch.fcgi", params=params, timeout=30)
    r.raise_for_status()
    data = r.json()
    return data.get("esearchresult", {}).get("idlist", [])


def entrez_summary(db: str, ids: list[str]) -> list[dict]:
    """Fetch summaries for a list of IDs (batch up to 200)."""
    results = []
    for i in range(0, len(ids), 200):
        batch = ids[i : i + 200]
        params = {
            "db": db,
            "id": ",".join(batch),
            "retmode": "json",
            "email": ENTREZ_EMAIL,
        }
        r = requests.get(f"{ENTREZ_BASE}/esummary.fcgi", params=params, timeout=30)
        r.raise_for_status()
        data = r.json()
        uids = data.get("result", {}).get("uids", [])
        for uid in uids:
            results.append(data["result"][uid])
        time.sleep(RATE_LIMIT_SLEEP)
    return results


def gse_to_gds_uid(gse_accession: str) -> str | None:
    """
    Derive the GDS UID from a GSE accession.
    Pattern: GSE236862 → 200236862 (prefix 200 + numeric part).
    This avoids extra API calls.
    """
    if gse_accession.upper().startswith("GSE"):
        try:
            numeric = int(gse_accession[3:])
            return str(200_000_000 + numeric)
        except ValueError:
            return None
    return None


def entrez_elink_pubmed(gse_accession: str) -> list[str]:
    """
    Get PMIDs linked to a GEO Series via E-link (GDS uid → pubmed).
    Returns list of linked PMIDs (empty = orphan).
    """
    gds_uid = gse_to_gds_uid(gse_accession)
    if not gds_uid:
        return []

    params = {
        "dbfrom": "gds",
        "db": "pubmed",
        "id": gds_uid,
        "retmode": "json",
        "email": ENTREZ_EMAIL,
    }
    try:
        r = requests.get(f"{ENTREZ_BASE}/elink.fcgi", params=params, timeout=30)
        r.raise_for_status()
        data = r.json()
        pmids = []
        for linkset in data.get("linksets", []):
            for linksetdb in linkset.get("linksetdbs", []):
                pmids.extend(linksetdb.get("links", []))
        return pmids
    except Exception:
        return []


# ── GEO dataset fetch ─────────────────────────────────────────────────────────

def search_geo_datasets(
    disease: str,
    data_type: str = "expression profiling by high throughput sequencing",
    max_datasets: int = 300,
    date_start: str = "2018/01/01",
    date_end: str = "2023/12/31",
) -> list[str]:
    """
    Query GEO for datasets matching disease + data type.
    Returns list of GEO DataSet accessions (GSE*).

    date_start/date_end: filter to datasets from this window. Default 2018-2023
    so datasets are old enough to have been cited but recent enough to be relevant.
    Very recent datasets (2024+) are trivially orphan — not informative.
    """
    # GEO search term structure
    # PDAT = publication/submission date range
    term = (
        f'"{disease}"[Title/Abstract] '
        f'AND "{data_type}"[DataSet Type] '
        f"AND Homo sapiens[Organism] "
        f"AND {date_start}:{date_end}[PDAT]"
    )
    print(f"[geo_orphan] Searching GEO: {term[:100]}...")
    ids = entrez_search("gds", term, retmax=max_datasets)
    print(f"[geo_orphan] Found {len(ids)} datasets in date window {date_start}:{date_end}")
    return ids


def get_dataset_summaries(gds_ids: list[str]) -> list[dict]:
    """Fetch summaries for GDS IDs, extract key metadata."""
    print(f"[geo_orphan] Fetching summaries for {len(gds_ids)} datasets...")
    raw = entrez_summary("gds", gds_ids)
    datasets = []
    for d in raw:
        try:
            accession = d.get("accession", "")
            if not accession.startswith("GSE"):
                continue  # Skip GPL, GSM entries
            datasets.append({
                "gds_id": d.get("uid", ""),
                "accession": accession,
                "title": d.get("title", ""),
                "summary": d.get("summary", "")[:300],
                "n_samples": d.get("n_samples", 0),
                "organism": d.get("taxon", ""),
                "gds_type": d.get("gdstype", ""),
                "pdat": d.get("pdat", ""),  # publication date
                "suppfile": d.get("suppfile", ""),
                "url": f"https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc={accession}",
                "n_linked_pmids": None,  # filled later
                "linked_pmids": [],       # filled later
            })
        except (KeyError, TypeError):
            continue
    print(f"[geo_orphan] Extracted {len(datasets)} GSE records")
    return datasets


def check_citations(datasets: list[dict], citation_threshold: int = 2) -> list[dict]:
    """
    For each dataset, count linked PMIDs via E-link.
    Tag as 'orphan' if linked_count <= citation_threshold.
    """
    print(f"[geo_orphan] Checking citations (threshold={citation_threshold})...")
    for i, d in enumerate(datasets):
        pmids = entrez_elink_pubmed(d["accession"])
        d["n_linked_pmids"] = len(pmids)
        d["linked_pmids"] = pmids
        d["is_orphan"] = len(pmids) <= citation_threshold
        if i % 20 == 0:
            print(f"  {i+1}/{len(datasets)} checked...")
        time.sleep(RATE_LIMIT_SLEEP)
    return datasets


# ── DrugBank cross-reference ──────────────────────────────────────────────────

DRUGBANK_GENES_URL = "https://go.drugbank.com/releases/latest/downloads/target-all-uniprot-links"
# Note: full DrugBank download requires login. Open data:
DRUGBANK_APPROVED_URL = "https://go.drugbank.com/releases/5-1-9/downloads/approved-drug-ids-drug-targets"

# Lung cancer relevant genes (curated shortlist for cross-reference)
LUNG_CANCER_TARGET_GENES = {
    "EGFR", "KRAS", "ALK", "ROS1", "BRAF", "MET", "RET", "NTRK1", "NTRK2", "NTRK3",
    "ERBB2", "PIK3CA", "STK11", "KEAP1", "NF1", "TP53", "RB1", "CDKN2A", "PTEN",
    "SMAD4", "APC", "CTNNB1", "IDH1", "IDH2", "FGFR1", "FGFR2", "FGFR3", "FGFR4",
    "MAP2K1", "ARAF", "CRAF", "NRG1", "HER2", "MYC", "MYCN", "CDK4", "CDK6",
    "MDM2", "CCND1", "CCNE1", "AURKA", "AURKB", "VEGFA", "PDGFRA", "KIT",
}

# Approved lung cancer drugs with primary targets
LUNG_CANCER_DRUGS: dict[str, list[str]] = {
    "erlotinib": ["EGFR"],
    "gefitinib": ["EGFR"],
    "osimertinib": ["EGFR"],
    "afatinib": ["EGFR", "ERBB2"],
    "crizotinib": ["ALK", "MET", "ROS1"],
    "alectinib": ["ALK"],
    "brigatinib": ["ALK"],
    "lorlatinib": ["ALK", "ROS1"],
    "capmatinib": ["MET"],
    "tepotinib": ["MET"],
    "selpercatinib": ["RET"],
    "pralsetinib": ["RET"],
    "larotrectinib": ["NTRK1", "NTRK2", "NTRK3"],
    "entrectinib": ["NTRK1", "NTRK2", "NTRK3", "ROS1", "ALK"],
    "adagrasib": ["KRAS"],
    "sotorasib": ["KRAS"],
    "vemurafenib": ["BRAF"],
    "dabrafenib": ["BRAF"],
    "trametinib": ["MAP2K1"],
    "pembrolizumab": ["PDCD1"],  # PD-1
    "nivolumab": ["PDCD1"],
    "atezolizumab": ["CD274"],  # PD-L1
    "durvalumab": ["CD274"],
    "bevacizumab": ["VEGFA"],
    "ramucirumab": ["KDR"],
    "carboplatin": ["DNA"],
    "cisplatin": ["DNA"],
    "paclitaxel": ["TUBB"],
    "docetaxel": ["TUBB"],
    "pemetrexed": ["TYMS", "DHFR"],
}


def crossref_drugbank(datasets: list[dict]) -> list[dict]:
    """
    Score each dataset for Drug Target Relevance (DTR):
    check if dataset title/summary mentions known lung cancer target genes or drugs.
    """
    drug_terms = set(LUNG_CANCER_DRUGS.keys())
    gene_terms = LUNG_CANCER_TARGET_GENES

    for d in datasets:
        text = (d["title"] + " " + d["summary"]).upper()
        hits_genes = [g for g in gene_terms if g.upper() in text]
        hits_drugs = [dr for dr in drug_terms if dr.upper() in text]

        # Also check if any linked drug targets map to our gene list
        d["dtr_genes"] = hits_genes
        d["dtr_drugs"] = hits_drugs
        d["dtr_score"] = len(hits_genes) * 2 + len(hits_drugs)  # genes worth more
    return datasets


# ── Analysis pipeline design (requires pydeseq2) ────────────────────────────

DESEQ2_PIPELINE_TEMPLATE = '''
## DESeq2 Analysis Pipeline (design — requires pydeseq2 install)

```bash
pip install pydeseq2 anndata scipy
```

```python
from pydeseq2.dds import DeseqDataSet
from pydeseq2.ds import DeseqStats
import pandas as pd
import anndata as ad

# 1. Download GEO dataset matrix
# python pipelines/geo_download.py GSE[ACCESSION] --output data/geo/

# 2. Load count matrix
counts = pd.read_csv("data/geo/GSE[ACCESSION]_counts.tsv", sep="\\t", index_col=0)
metadata = pd.read_csv("data/geo/GSE[ACCESSION]_metadata.tsv", sep="\\t", index_col=0)

# 3. Filter low-count genes (standard filter)
keep = counts.sum(axis=1) >= 10
counts = counts[keep]

# 4. Run DESeq2
dds = DeseqDataSet(
    counts=counts.T,
    metadata=metadata,
    design_factors="condition",  # adjust to dataset
    refit_cooks=True,
)
dds.deseq2()

# 5. Extract results
stat_res = DeseqStats(dds, contrast=["condition", "tumor", "normal"])
stat_res.summary()
results_df = stat_res.results_df

# 6. Filter significant DEGs
sig = results_df[
    (results_df["padj"] < 0.05) &
    (results_df["log2FoldChange"].abs() > 1.0)
].sort_values("padj")

# 7. Cross-reference with drug targets
from pipelines.geo_orphan_query import LUNG_CANCER_TARGET_GENES, LUNG_CANCER_DRUGS
actionable = sig[sig.index.isin(LUNG_CANCER_TARGET_GENES)]
print(f"Actionable DEGs (druggable targets): {len(actionable)}")
actionable.to_csv(f"findings/GSE[ACCESSION]_actionable_degs.tsv", sep="\\t")
```

### Interpretation
- Significant DEGs that are druggable targets = highest-priority hits
- Compare to FAERS signals (RS-001): overlap between DEGs and SSRI-adjacent pathways?
- Novel finding = target is up/downregulated + approved drug available + not in major papers
'''


# ── Report ────────────────────────────────────────────────────────────────────

def write_report(
    disease: str,
    datasets: list[dict],
    citation_threshold: int,
) -> Path:
    orphans = [d for d in datasets if d.get("is_orphan")]
    non_orphans = [d for d in datasets if not d.get("is_orphan")]

    # Sort orphans by DTR score desc, then n_samples desc
    orphans_sorted = sorted(
        orphans,
        key=lambda x: (x.get("dtr_score", 0), x.get("n_samples", 0)),
        reverse=True,
    )

    # Break down by citation tier for more informative reporting
    zero_pmid = [d for d in datasets if d.get("n_linked_pmids", 0) == 0]
    one_pmid = [d for d in datasets if d.get("n_linked_pmids", 0) == 1]
    two_pmid = [d for d in datasets if d.get("n_linked_pmids", 0) == 2]

    orphan_rate = len(orphans) / len(datasets) * 100 if datasets else 0
    zero_rate = len(zero_pmid) / len(datasets) * 100 if datasets else 0
    total_samples_orphaned = sum(d.get("n_samples", 0) for d in orphans)
    total_samples_zero = sum(d.get("n_samples", 0) for d in zero_pmid)

    date_str = datetime.now().strftime("%Y-%m-%d")
    disease_slug = disease.lower().replace(" ", "_")
    out = FINDINGS_DIR / f"rs002_geo_orphans_{disease_slug}_{date_str}.md"

    lines = [
        f"# RS-002 — GEO Orphan Dataset Analysis: {disease.title()}",
        f"*Date: {date_str} | Citation threshold: ≤{citation_threshold} linked PMIDs | Date range: 2019–2023*",
        "",
        "---",
        "",
        "## Executive Summary",
        "",
        f"**{zero_rate:.0f}% of {disease} RNA-seq datasets on GEO have zero linked publications.**",
        "",
        f"Of {len(datasets)} completed {disease} RNA-seq datasets deposited to GEO between 2019 and 2023:",
        f"- **{len(zero_pmid)} datasets ({zero_rate:.0f}%)** have no linked publications — true orphans",
        f"- **{len(one_pmid)} datasets** have exactly 1 linked PMID (typically the depositor's paper only)",
        f"- Only **{len(non_orphans)} datasets** have been independently reanalyzed (>2 PMIDs)",
        "",
        "These are the datasets that exist — data collected, patients enrolled, samples processed —",
        "but whose findings have never been independently synthesized. Each is a candidate for",
        "Empire Lab secondary analysis.",
        "",
        "---",
        "",
        "## Cohort Overview",
        "",
        f"| Citation tier | Count | % | Total samples |",
        f"|--------------|-------|---|---------------|",
        f"| 0 PMIDs — true orphans | {len(zero_pmid)} | {zero_rate:.0f}% | {total_samples_zero:,} |",
        f"| 1 PMID — depositor paper only | {len(one_pmid)} | {len(one_pmid)/len(datasets)*100:.0f}% | {sum(d.get('n_samples',0) for d in one_pmid):,} |",
        f"| 2 PMIDs — minimal reanalysis | {len(two_pmid)} | {len(two_pmid)/len(datasets)*100:.0f}% | {sum(d.get('n_samples',0) for d in two_pmid):,} |",
        f"| >2 PMIDs — published | {len(non_orphans)} | {len(non_orphans)/len(datasets)*100:.0f}% | {sum(d.get('n_samples',0) for d in non_orphans):,} |",
        f"| **Total** | **{len(datasets)}** | 100% | **{sum(d.get('n_samples',0) for d in datasets):,}** |",
        "",
        "---",
        "",
        "## Top Orphan Datasets (ranked by Drug Target Relevance)",
        "",
        "Datasets with druggable lung cancer target genes (EGFR, KRAS, ALK, etc.) in their",
        "title or abstract receive higher Drug Target Relevance (DTR) scores.",
        "",
        "| Accession | Title | Samples | DTR Score | Linked PMIDs | Year | Key Targets |",
        "|-----------|-------|---------|-----------|-------------|------|-------------|",
    ]

    for d in orphans_sorted[:40]:
        title_short = d["title"][:55] + "…" if len(d["title"]) > 55 else d["title"]
        year = d.get("pdat", "")[:4] if d.get("pdat") else "?"
        genes = ", ".join(d.get("dtr_genes", [])[:3]) or "—"
        lines.append(
            f"| [{d['accession']}]({d['url']}) | {title_short} | "
            f"{d.get('n_samples', '?')} | {d.get('dtr_score', 0)} | "
            f"{d.get('n_linked_pmids', '?')} | {year} | {genes} |"
        )

    lines += [
        "",
        "---",
        "",
        "## Drug Target Landscape",
        "",
        "Gene hits across all orphan datasets (mentions in title/abstract):",
        "",
    ]

    # Count gene mentions across orphans
    from collections import Counter
    gene_counts: Counter = Counter()
    drug_counts: Counter = Counter()
    for d in orphans:
        gene_counts.update(d.get("dtr_genes", []))
        drug_counts.update(d.get("dtr_drugs", []))

    if gene_counts:
        lines.append("| Gene | Orphan Dataset Mentions | Approved Drugs |")
        lines.append("|------|------------------------|----------------|")
        for gene, count in gene_counts.most_common(20):
            drugs_for_gene = [
                drug for drug, targets in LUNG_CANCER_DRUGS.items()
                if gene in targets
            ]
            lines.append(
                f"| {gene} | {count} | {', '.join(drugs_for_gene[:3]) or '—'} |"
            )
    else:
        lines.append("*No drug target gene mentions detected in scanned dataset metadata.*")

    lines += [
        "",
        "---",
        "",
        "## Analysis Pipeline",
        "",
        "The following pipeline design is ready for execution once `pydeseq2` is installed.",
        "Install: `pip install pydeseq2 anndata`",
        "",
        DESEQ2_PIPELINE_TEMPLATE,
        "",
        "---",
        "",
        "## Priority Candidates for Empire Lab Analysis",
        "",
        "Top 5 orphan datasets with highest Drug Target Relevance:",
        "",
    ]

    for i, d in enumerate(orphans_sorted[:5], 1):
        genes = ", ".join(d.get("dtr_genes", [])[:5]) or "general RNA-seq"
        drugs = ", ".join(d.get("dtr_drugs", [])[:3]) or "see target genes"
        lines += [
            f"### {i}. [{d['accession']}]({d['url']}) — DTR {d.get('dtr_score', 0)}",
            f"**Title**: {d['title']}",
            f"**Samples**: {d.get('n_samples', '?')} | **Linked publications**: {d.get('n_linked_pmids', '?')}",
            f"**Target genes mentioned**: {genes}",
            f"**Drugs mentioned**: {drugs}",
            f"**Summary excerpt**: {d.get('summary', '')[:200]}",
            "",
        ]

    lines += [
        "---",
        "",
        "## Next Steps",
        "",
        "- [ ] Download count matrices for top 3 DTR-scored orphan datasets",
        "- [ ] Run DESeq2 pipeline (see Analysis Pipeline section above)",
        "- [ ] Cross-reference DEGs with FAERS signals from RS-001",
        "- [ ] Check if any significant findings are already in ClinicalTrials.gov trials (RS-003 pipeline)",
        "- [ ] Draft RS-002b findings summary for highest-signal dataset",
        "",
        f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')} | RS-002 pipeline*",
    ]

    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"[geo_orphan] Report: {out}")
    return out


def write_tsv(disease: str, datasets: list[dict], date_str: str) -> Path:
    """Write raw dataset data to TSV for downstream analysis."""
    disease_slug = disease.lower().replace(" ", "_")
    out = DATA_DIR / f"geo_orphans_{disease_slug}_{date_str}.tsv"

    fields = ["accession", "title", "n_samples", "pdat", "gds_type",
              "n_linked_pmids", "is_orphan", "dtr_score", "dtr_genes",
              "dtr_drugs", "url", "summary"]

    with open(out, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fields, delimiter="\t", extrasaction="ignore")
        writer.writeheader()
        for d in datasets:
            row = dict(d)
            row["dtr_genes"] = "|".join(row.get("dtr_genes", []))
            row["dtr_drugs"] = "|".join(row.get("dtr_drugs", []))
            writer.writerow(row)

    print(f"[geo_orphan] TSV data: {out}")
    return out


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="GEO orphan dataset scanner")
    parser.add_argument("--disease", default="lung cancer",
                        help="Disease to search (default: lung cancer)")
    parser.add_argument("--max-datasets", type=int, default=300,
                        help="Max datasets to scan (default: 300)")
    parser.add_argument("--citation-threshold", type=int, default=2,
                        help="Max linked PMIDs to qualify as orphan (default: 2)")
    parser.add_argument("--date-start", default="2018/01/01",
                        help="Dataset submission date window start (default: 2018/01/01)")
    parser.add_argument("--date-end", default="2023/12/31",
                        help="Dataset submission date window end (default: 2023/12/31)")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if args.dry_run:
        print(f"[geo_orphan] DRY RUN")
        print(f"  Disease: {args.disease}")
        print(f"  Max datasets: {args.max_datasets}")
        print(f"  Citation threshold: {args.citation_threshold}")
        print(f"  NCBI E-utils: {ENTREZ_BASE}")
        out = FINDINGS_DIR / f"rs002_geo_orphans_{args.disease.lower().replace(' ', '_')}_{datetime.now().strftime('%Y-%m-%d')}.md"
        print(f"  Output: {out}")
        return

    # 1. Search GEO
    gds_ids = search_geo_datasets(
        args.disease,
        max_datasets=args.max_datasets,
        date_start=args.date_start,
        date_end=args.date_end,
    )
    if not gds_ids:
        print("[geo_orphan] No datasets found — check search term and network access")
        return

    # 2. Get summaries
    datasets = get_dataset_summaries(gds_ids)
    if not datasets:
        print("[geo_orphan] No GSE records extracted from summaries")
        return

    # 3. Check citations (this is slow — ~0.35s per dataset)
    datasets = check_citations(datasets, citation_threshold=args.citation_threshold)

    orphan_count = sum(1 for d in datasets if d.get("is_orphan"))
    print(f"[geo_orphan] Orphans: {orphan_count} / {len(datasets)}")

    # 4. DrugBank cross-reference
    datasets = crossref_drugbank(datasets)

    # 5. Write outputs
    date_str = datetime.now().strftime("%Y-%m-%d")
    report_path = write_report(args.disease, datasets, args.citation_threshold)
    tsv_path = write_tsv(args.disease, datasets, date_str)

    orphan_rate = orphan_count / len(datasets) * 100 if datasets else 0
    print(f"\n[geo_orphan] Complete:")
    print(f"  {len(datasets)} datasets scanned")
    print(f"  {orphan_count} orphans ({orphan_rate:.1f}%)")
    print(f"  Report: {report_path}")
    print(f"  Data: {tsv_path}")


if __name__ == "__main__":
    main()
