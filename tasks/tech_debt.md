# research_science — Tech Debt / Task Queue

| ID | Description | Risk | Est | Bucket | Status | Notes |
|----|-------------|------|-----|--------|--------|-------|
| RS-001 | Build FAERS demo pipeline — Q4 2025 data, PRR analysis on SSRIs, compare to trial AE profiles | LOW | 3h | auto_sprint | done | Completed 2026-03-14. 230 signals, 199 novel. Charts + findings committed. |
| RS-001b | FAERS knowledge gap meta-analysis — what % of FAERS post-market signal is invisible in registration trial profiles? Cross-drug comparison | LOW | 3h | auto_sprint | open | Added: 2026-03-14. P1. Builds on RS-001 findings. |
| RS-001c | FAERS historical backfill — download 2004-present quarterly XML files, build 20-year signal emergence database | MEDIUM | 8h | auto_sprint | open | Added: 2026-03-14. P1. Highest strategic leverage — creates the data moat. ~20GB download. |
| RS-001d | Monthly FAERS delta monitor — cron job that diffs current signals vs prior month, auto-drafts Substack post | LOW | 3h | auto_sprint | open | Added: 2026-03-14. P1. Turns RS-001 into a standing monitor. Core content engine. |
| RS-001e | Fluvoxamine deep-dive paper — CYP1A2 inhibition + rhabdomyolysis cluster, literature review, write standalone findings doc | LOW | 4h | auto_sprint | open | Added: 2026-03-14. P2. Most defensible novel finding from RS-001. |
| RS-001f | Write RS-001 Substack article — "What 20M FDA reports say about SSRIs" — narrative, methodology, charts, gated tables | LOW | 2h | manual | open | Added: 2026-03-14. P1. Data is in hand. Requires Glenn review before publish. |
| RS-002 | GEO orphan query — lung cancer datasets <3 citations, DESeq2, cross-ref DrugBank | LOW | 4h | auto_sprint | open | Requires R/Bioconductor or Python rpy2. Added: 2026-03-14. P1. |
| RS-003 | ClinicalTrials.gov publication gap scan — depression trials 2015-2020, by sponsor type | LOW | 2h | auto_sprint | open | Pure Python + XML parsing. Added: 2026-03-14. P1. |
| RS-004 | Prompt Whisperer Experiment 2 design — hallucination characterization across 3 local models | LOW | 2h | auto_sprint | open | Uses existing Ollama fleet. Added: 2026-03-14. P2. |
| RS-005 | NHANES diet reanalysis — red meat + CVD claim, modern confounders, vs. published result | MEDIUM | 5h | auto_sprint | open | Requires NHANES data download + survey regression. Added: 2026-03-14. P2. |
| RS-006 | Set up GitHub remote for research_science repo | LOW | 15m | auto_sprint | done | Completed 2026-03-14. ghighcove/research-science (private initially). |
| RS-007 | Write .gitignore for data/ directory (large raw files should never be committed) | LOW | 5m | auto_sprint | done | Completed 2026-03-14 (in initial commit). |
| RS-008 | EPA TRI × NHANES correlation pipeline design doc | LOW | 2h | auto_sprint | open | Design only — Emperor runs it. Added: 2026-03-14. P2. Gated on Emperor. |
| RS-009 | Patent landscape tool — USPTO bulk download + NLP classification for one domain | MEDIUM | 6h | auto_sprint | open | Added: 2026-03-14. P3. |
| RS-010 | Set up GitHub Pages for findings/index.html — enable Pages on research-science repo | LOW | 10m | auto_sprint | open | Added: 2026-03-14. P1. Requires repo to be public or Pages enabled on private repo. |
| RS-011 | Substack publication setup — create Empire Lab Research publication, configure paid tiers | USER | 30m | manual | open | Added: 2026-03-14. P1. Requires Glenn to create publication (Substack web UI). |
| RS-012 | WHO VigiBase expansion design — 35M international reports, Uppsala Monitoring Centre API | LOW | 2h | auto_sprint | open | Added: 2026-03-14. P3. Gated on Emperor (compute). |
| RS-TDU-001 | Select first preprint target: FAERS signal or GEO finding — Glenn decides after RS-001/RS-002 | USER | 30m | manual | open | Cannot proceed without Glenn's choice. Added: 2026-03-14. |
| RS-TDU-002 | Decide: make research-science GitHub repo public? Enables GitHub Pages, discoverability, career capital. Risk: methodology visible before publication. | USER | 15m | manual | open | Added: 2026-03-14. Recommend: public after first Substack article is live. |
