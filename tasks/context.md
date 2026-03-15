# research_science — Session Context

## Last Updated: 2026-03-14

## Current State
- Project created 2026-03-14 as Empire Lab genesis
- Vision document: `docs/empire_lab_vision.md` — the founding document
- No pipelines built yet. All work is design/planning phase.

## Active Work
- Vision document written (fractaltime + ideaamplifier synthesis)
- Priority targets identified: FAERS, GEO orphaned datasets, ClinicalTrials.gov gaps, EPA TRI + NHANES, math/AI science

## Key Design Decisions
- **Lab philosophy**: Cottage science — rigorous methodology, public data, no wet lab required
- **Discovery type**: Computational, cross-domain synthesis, orphaned data analysis, replication scanning
- **Productization priority**: FAERS pharmacovigilance first (recurring pipeline, clear buyers)
- **Not chasing Nobel Prizes**: Discovery = finding not easily synthesized before, statistically valid, useful to identified audience
- **Empire role**: Patient + systematic + cross-domain → permanent structural advantage over individual researchers

## Blockers / Open Questions
- FAERS pipeline not yet built — first action item
- GEO API access not yet tested
- No publication venue selected yet (bioRxiv, PLOS ONE, SSRN)

## Next Steps
1. Build FAERS demo pipeline — pull last quarterly data, run PRR analysis on one drug class
2. Query GEO API for orphaned datasets in cancer/neurological disease
3. Design ClinicalTrials.gov gap analysis pipeline
4. Select first preprint target and venue

## Environment
- G:/ai/research_science/ (this project)
- Python 3.8 (32-bit) at E:/Python/Python38-32/python.exe
- Emperor (arriving ~Apr 7) will be primary compute for weekly runs

## Quick Reference
- Vision doc: `docs/empire_lab_vision.md`
- Pipelines: `pipelines/` (not yet built)
- Findings: `findings/` (not yet populated)
- Git: local only (no remote yet)
- Working directory: G:/ai/research_science
