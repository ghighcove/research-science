# Empire Lab — Multi-Outcome Asset Strategy

**Last updated**: 2026-03-14
**Author**: Glenn Highcove / Empire Lab

---

## The Core Premise

Empire Lab is a one-person research operation that uses AI assistance, public regulatory data,
and structured experimental pipelines to produce findings that matter. The asset being built
is not any single study — it's the **infrastructure and track record** that makes every
subsequent study faster, more credible, and more monetizable.

The strategic goal: build an asset where multiple independent paths lead to positive outcomes.
Lose one path entirely, and two others still pay.

---

## The Multi-Outcome Architecture

### Win Path 1 — Career Capital (Lowest Risk, Nearly Guaranteed)

**What it is**: A published, reproducible, methodology-sound pharmacovigilance analysis with
real data and clear findings. This is a portfolio piece demonstrating the intersection of
data science, domain knowledge, and independent research.

**Why it's nearly guaranteed**: The RS-001 findings are real. The methodology is standard
(Evans et al., used by EMA/WHO). The code is open and reproducible. The data is public (FDA).
This is a legitimate research output regardless of whether anyone pays for it.

**How to maximize it**:
- GitHub repo: code fully open, methodology documented, contributions welcome
- LinkedIn: "Built a pharmacovigilance pipeline on 20M FDA adverse event reports"
- Substack/Medium: narrative explanation of findings (free tier)
- CV line: "Empire Lab, Principal Investigator — FAERS Signal Detection (RS-001)"

**Timeline to value**: Immediate (article draft, GitHub push) → 30 days (published, indexed)

---

### Win Path 2 — Substack Revenue (Medium Risk, Moderate Reward)

**What it is**: A paid research newsletter. Free tier = methodology + narrative summaries.
Paid tier = full signal tables, monthly delta reports, dataset access.

**The content engine**:
```
Monthly: FAERS delta run (automated, ~15 min)
         → diff vs prior month
         → new signals flagged
         → Emperor writes clinical interpretation paragraph
         → Claude reviews
         → Substack post published within 24h
```

**The product tiers**:
| Tier | Price | What You Get |
|------|-------|-------------|
| Free | $0 | Methodology articles, top 10 signals summary, all charts |
| Researcher | $12/mo | Full signal tables (all 230+), CSV exports, monthly delta |
| Professional | $49/mo | Same + custom queries ("show me all rhabdomyolysis signals") |
| Expert | $200+/case | Litigation support letter, expert documentation |

**Monetization path**: 100 paid subscribers at $12/mo = $1,200/mo. Not life-changing.
But the delta reports require essentially no ongoing labor once automated. The marginal
cost per subscriber approaches $0.

**Timeline to value**: 60-90 days (build subscriber base, publish 3-4 articles first)

---

### Win Path 3 — Litigation Support (Higher Variance, Highest Per-Unit Revenue)

**What it is**: Plaintiff attorneys in pharmaceutical cases need independent documentation
of FAERS signals. Our output — methodology documented, code open, findings reproducible —
is exactly what an expert support package looks like.

**Why this works**: FAERS data is public. Our analysis is independently reproducible. The
methodology cites peer-reviewed literature. This is not consulting — it's evidence production.

**What we can produce**:
- Signal documentation letter: PRR, chi², count, Evans criteria compliance, methodology description
- Temporal signal emergence report (once backfill is done): "This signal first appeared in Q3 2011"
- Comparative drug analysis: "How does drug X compare to class comparators?"
- Custom query against historical database

**Pricing**: $500–$2,500 per case, depending on complexity. Volume is low but margins are very high.

**Critical constraint**: Must remain demonstrably independent. No pharmaceutical company clients,
ever. This is what makes the litigation support credible.

**Timeline to value**: 6-12 months (requires established publication track record first)

---

### Win Path 4 — Academic Collaboration (Long Runway, High Ceiling)

**What it is**: Once RS-001 is published and visible, academic researchers will find it.
Epidemiologists, pharmacists, clinical pharmacologists routinely mine FAERS but rarely have
the software infrastructure to do it at this scale efficiently. Collaboration opportunities
arise naturally.

**Forms it could take**:
- Co-authorship on a journal paper using our pipeline as the data source
- A university lab licensing or forking our pipeline (with attribution)
- Grant co-applicant position (NIH R21, PCORI funding for pharmacovigilance methods)

**Why this is a real path**: The gap in the market is not talent — academics have that. The
gap is engineering infrastructure. We have the pipeline. They have the institutional affiliation
and publication channels.

**Timeline to value**: 12-24 months

---

### Win Path 5 — Data Asset / Licensing (Long Runway, Scalable)

**What it is**: Once we have the 20-year FAERS backfill (all quarterly downloads, 2004-present),
we have a processed, analyzed, signal-detected database that took significant compute and
methodology to produce. That's a data asset.

**Forms of value**:
- API access to the historical signal database ($X/month for institutions)
- Custom cohort analysis for research organizations
- Licensing the signal database to pharmacovigilance firms

**Prerequisites**: Need the historical backfill first (RS-001c) and needs the track record
from Win Paths 1-2 to establish credibility.

**Timeline to value**: 18-36 months

---

## The Asset Stack (What We're Building)

```
Layer 1 — Infrastructure (build once, reuse forever)
├── faers_prr.py              # signal detection pipeline
├── faers_visualize.py        # chart generation
├── faers_delta.py            # [TO BUILD] monthly diff monitor
├── faers_historical.py       # [TO BUILD] quarterly download + ingest
└── faers_query.py            # [TO BUILD] natural language query layer

Layer 2 — Data (the moat)
├── findings/YYYY-MM-DD_*.md  # monthly signal snapshots (accumulates over time)
├── historical_signals.db     # [TO BUILD] 20-year signal database
└── signal_emergence.csv      # [TO BUILD] first-appearance timeline per drug×event

Layer 3 — Publication (the distribution)
├── findings/index.html       # browsable findings page (GitHub Pages)
├── Substack                  # narrative articles + paid delta reports
└── Medium                    # cross-posts for discovery

Layer 4 — Credibility Layer (compounds over time)
├── GitHub repo (open code)   # reproducibility
├── methodology docs          # peer-citation target
└── track record (n studies)  # academic credibility
```

---

## The Expansion Roadmap

### Phase 1: Foundation (Now → 60 days)
- [x] RS-001: FAERS SSRI signal detection (DONE)
- [ ] RS-001c: FAERS historical backfill (2004-present)
- [ ] RS-001d: Monthly delta monitor (automated)
- [ ] RS-002: GEO orphaned dataset pipeline
- [ ] RS-003: ClinicalTrials.gov publication gap scan
- [ ] GitHub public repo + GitHub Pages findings page
- [ ] First Substack article: "What 20M FDA reports say about SSRIs"

### Phase 2: Diversification (60-180 days)
- [ ] RS-004: Prompt Whisperer Experiment 2 (in-Empire AI science)
- [ ] RS-005: NHANES diet reanalysis pipeline
- [ ] RS-008: EPA TRI × NHANES correlation
- [ ] 3+ Substack articles published, paid tier launched
- [ ] 50+ paid subscribers

### Phase 3: Data Asset (180-365 days)
- [ ] Historical FAERS database complete (2004-present)
- [ ] Signal emergence timelines for top 100 drugs
- [ ] First academic collaboration initiated
- [ ] Litigation support first case

### Phase 4: Platform (Year 2+)
- [ ] WHO VigiBase international expansion (35M reports)
- [ ] API access tier for institutional subscribers
- [ ] RS-001 or RS-002 findings cited in academic literature

---

## The 3 Mandatory Structural Rules

**Rule 1: Code is always open.**
Open code = reproducibility = credibility = career capital. Revenue comes from data and
interpretation, not from hiding the method. Always.

**Rule 2: Independence is non-negotiable.**
No pharmaceutical company clients, no industry funding, no promotional content.
The value of every finding depends entirely on the source being independent.

**Rule 3: Methodology first, findings second.**
Every publication leads with the method, its limitations, and what the findings don't mean
before stating what they do mean. This is what distinguishes us from irresponsible
science communication and what makes litigation support defensible.

---

## How to Measure Progress

Monthly check-in metrics:
| Metric | Now | 90-day target | 1-year target |
|--------|-----|---------------|---------------|
| Studies completed | 1 | 4 | 10 |
| Substack subscribers | 0 | 200 | 1,000 |
| Paid subscribers | 0 | 20 | 150 |
| Monthly revenue | $0 | $240 | $1,800 |
| GitHub stars (research_science) | 0 | 25 | 200 |
| Academic citations | 0 | 0 | 2 |
| Data coverage (FAERS years) | 1 | 5 | 20 |

---

## The Minimum Viable Version of Success

If every ambitious path fails, this is still net-positive:

- One published article (Substack, free) demonstrating methodologically sound pharmacovigilance
- One GitHub repo with reproducible code used by at least a handful of researchers
- One CV line that's defensible in any data science or health analytics interview
- One data infrastructure that took 3 sessions to build and can be rerun indefinitely for free

That minimum case requires nothing from anyone else. It's already done.
Everything above it is upside.
