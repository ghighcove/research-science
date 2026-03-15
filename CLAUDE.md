# research_science — Project Rules

## Purpose
Empire Lab: cottage science at machine scale. Computational discovery using public datasets.
No wet lab. Rigorous methodology. Transparent publication.

## Key Constraints
- All findings must be statistically valid and methodology-transparent (Level 1+2 validation minimum)
- Never claim a finding is "proven" — use "signal", "association", "suggests", "consistent with"
- Never fabricate statistics or data points — every number must trace to a real source
- All data sources must be legally public (see data sources table in docs/empire_lab_vision.md)

## Pipeline Pattern (when building)
- FAERS: download → PRR/ROR → cross-ref trial data → flag → enrich → publish
- GEO: query API → DESeq2 → cross-ref DrugBank/OpenTargets → flag → brief
- ClinicalTrials: download XML → parse → gap analysis → synthesis

## Python Environment
- Python 3.8 32-bit (default, wardriving/analysis scripts)
- Python 3.14 64-bit (publishing tools)
- Emperor (arriving ~Apr 7) will be primary compute for weekly runs

## File Conventions
- Findings: `findings/YYYY-MM-DD_[field]_[slug].md`
- Pipelines: `pipelines/[field]/[script].py`
- Data: `data/[source]/` (raw data never committed to git — add to .gitignore)
- Discovery log: `findings/discovery_log.md` (append-only, one line per finding)

## Publication Venues (by type)
- General audience: Medium + Substack (existing pipeline)
- Preprints: bioRxiv (bio), arXiv cs.LG/cs.AI (AI/ML), SSRN (social science)
- Peer review targets: PLOS ONE (broad), BMJ Open (clinical), Environmental Health Perspectives (env)
