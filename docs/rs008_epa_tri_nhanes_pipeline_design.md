# RS-008 — EPA TRI × NHANES Correlation Pipeline Design
*Empire Lab | Designed: 2026-03-15 | Execution: Emperor (Apr 2026+)*

---

## Research Question

**Do communities with higher toxic chemical releases (EPA TRI) show measurable differences in
health outcomes (NHANES) beyond what is explained by demographic and socioeconomic controls?**

And more specifically: which chemicals and which health outcomes form the strongest correlations,
and can we identify novel signal — associations not yet documented in the peer-reviewed literature?

---

## Data Sources

### 1. EPA Toxics Release Inventory (TRI)

- **URL**: https://www.epa.gov/toxics-release-inventory-tri-program/tri-data-and-tools
- **Coverage**: Industrial facilities reporting annual releases of 650+ toxic chemicals, 1987–present
- **Geography**: County-level aggregation (latitude/longitude per facility → aggregate to FIPS county code)
- **Download**: Bulk CSV download at `https://www.epa.gov/toxics-release-inventory-tri-program/tri-basic-data-files-calendar-years-1987-present`
- **Key fields**: FIPS code, chemical name, release medium (air/water/land), total release (lbs/year), year

### 2. NHANES (National Health and Nutrition Examination Survey)

- **URL**: https://www.cdc.gov/nchs/nhanes/
- **Coverage**: Representative sample of ~10,000 US adults per 2-year cycle, 1999–present
- **Download**: SAS XPT files per cycle, per module (demographics, blood tests, diet, questionnaire)
- **Key fields**: SEQN (participant ID), RIDSTATR (exam status), RIDRETH3 (ethnicity), INDFMPIR (poverty-income ratio),
  BMXBMI (BMI), blood chemistry panels, urine metals, interview questionnaire outcomes
- **Geography**: Masked — PSU (primary sampling unit) not county. Cross-reference via masked region codes or published county linkage studies

### 3. Geography Linkage

**Challenge**: NHANES masks participant geography for privacy. Solutions:

**Option A (Academic linkage)**: The NHANES-linked Mortality Public Use file links participants
to county FIPS via CDC-restricted data. Available under DUA (Data Use Agreement). 4-6 week turnaround.

**Option B (Ecological analysis)**: Aggregate NHANES to census region or state level →
join TRI at same level. Ecological correlation only — cannot establish individual-level association.
Sufficient for hypothesis generation; publishable with appropriate caveats.

**Option C (Synthetic linkage)**: Use BRFSS (Behavioral Risk Factor Surveillance System) instead
of NHANES — BRFSS includes county FIPS codes and is fully public. ~450,000 respondents/year.
Lower clinical depth than NHANES but direct geographic linkage.

**Recommended approach**: **Option B + C** in parallel. Ecological analysis (NHANES × TRI by region)
for depth; BRFSS × TRI (county-level) for geographic granularity.

---

## Pipeline Architecture

```
Data Ingest
├── download_tri.py          → data/tri/tri_[year].csv for 2010–2023
├── download_nhanes.py       → data/nhanes/[cycle]_[module].xpt
└── download_brfss.py        → data/brfss/[year].zip

Transform
├── tri_aggregate.py         → county × chemical × year aggregates (lbs_released, n_facilities)
├── nhanes_clean.py          → participant-level cleaned + survey weights
├── brfss_clean.py           → respondent-level cleaned + FIPS code
└── geo_join.py              → TRI county metrics → NHANES region crosswalk → BRFSS county join

Analysis
├── ecological_analysis.py   → Spearman/Pearson TRI chemical × NHANES outcome, by region
├── brfss_analysis.py        → OLS/logistic regression, TRI exposure → BRFSS outcomes, county-level
├── confounder_control.py    → Demographics, SES (poverty index), urbanicity, race/ethnicity controls
└── signal_novelty_check.py  → Cross-reference significant associations vs. PubMed literature

Output
├── findings/rs008_tri_nhanes_signals_[date].md  → ranked signal table + novel finding flags
└── data/rs008_results.json                      → machine-readable output for downstream analysis
```

---

## Chemical Priority List

Focus on chemicals with: (1) high total release volume, (2) known health endpoint linkage,
(3) high Empire Lab novelty potential. Starting panel:

| Chemical | TRI Volume | Known health targets | Novelty potential |
|----------|-----------|---------------------|-------------------|
| Lead compounds | High | Neurodevelopment, CVD, kidney | Moderate (well-studied) |
| Formaldehyde | High | Respiratory, carcinogen | Moderate |
| Toluene | High | Neurotoxicity, reproductive | High (modern cohort) |
| Benzene | Medium | Leukemia, hematologic | Moderate |
| Arsenic compounds | Medium | CVD, diabetes, kidney | High (NHANES biomarker data available) |
| Chromium compounds | Medium | Respiratory, kidney | High |
| Mercury compounds | Medium | Neurodevelopment, CVD | High (NHANES blood mercury) |
| PFAS (Perfluorooctanoic acid) | Low-Medium | Thyroid, lipids, immune | **Very high** (NHANES PFAS panel 2013+) |
| Styrene | Medium | CNS, reproductive | High |
| Vinyl chloride | Medium | Hepatic, carcinogen | High |

**Priority target**: PFAS × NHANES lipid panel × TRI county exposure.
PFAS county-level TRI data exists; NHANES has blood serum PFAS measurements (2013–2018 cycles);
lipid/thyroid/immune endpoints all measured. This is the highest-signal, most novel sub-analysis.

---

## Analysis Methodology

### Step 1: Ecological Correlation (NHANES × TRI by Census Division)

```python
# Census divisions: 9 regions
# For each chemical × health outcome:
# - TRI: sum lbs_released per division per year
# - NHANES: weighted mean of health outcome per division per 2-year cycle
# - Pearson correlation + 95% CI
# - Confounder adjustment: partial correlation controlling for poverty index, urbanicity
```

### Step 2: County-Level Regression (BRFSS × TRI)

```python
# For each chemical × health outcome:
import statsmodels.formula.api as smf

model = smf.ols(
    'health_outcome ~ log1p(tri_release) + poverty_rate + pct_urban + pct_black + pct_hispanic',
    data=county_joined
).fit()

# Multiple testing correction: Benjamini-Hochberg FDR
# Threshold: q < 0.05 after correction
```

### Step 3: Signal Novelty Classification

For each significant (q < 0.05) chemical × outcome association:
1. Query PubMed for `[chemical] AND [outcome] AND epidemiology`
2. Count papers in last 10 years
3. Classify:
   - 0-2 papers → **NOVEL** (Empire Lab primary target)
   - 3-10 papers → **UNDER-CHARACTERIZED** (replication/extension value)
   - 10+ papers → **ESTABLISHED** (confirm or challenge existing literature)

---

## Output: Signal Ranking Table

The pipeline produces a ranked table of chemical × outcome associations:

| Rank | Chemical | Outcome | Beta (95% CI) | q-value | Novelty | Papers | Empire Priority |
|------|---------|---------|--------------|---------|---------|--------|----------------|
| 1 | PFAS | HDL cholesterol | -0.8 (-1.1, -0.5) | 0.003 | NOVEL | 2 | P1 |
| 2 | Arsenic | HbA1c | +0.12 (0.06, 0.18) | 0.008 | UNDER | 5 | P2 |
| ... | | | | | | | |

---

## Compute Requirements

| Step | CPU | RAM | Time | Machine |
|------|-----|-----|------|---------|
| TRI download (13 years) | Low | 4GB | 15 min | Any |
| NHANES download (5 cycles) | Low | 4GB | 20 min | Any |
| BRFSS download (10 years) | Low | 4GB | 30 min | Any |
| Transform + join | Medium | 16GB | 30 min | Emperor preferred |
| Regression analysis | High | 32GB | 1-2h | **Emperor required** |
| Novel signal PubMed query | Low | 4GB | 30 min | Any |

**Total compute: ~3h on Emperor (64GB M4 Pro)**. Fits comfortably in a single overnight Emperor run.

---

## Caveats for Publication

1. **Ecological fallacy**: Region-level correlations cannot establish individual-level associations
2. **Healthy worker effect**: Populations near industrial facilities differ from general population in
   multiple ways beyond chemical exposure
3. **TRI completeness**: TRI captures facility-reported releases, not ambient environmental exposure.
   Actual human exposure requires air/water modeling or biomonitoring
4. **Confounding**: Even with demographic controls, residual confounding is unavoidable in observational data
5. **Multiple testing**: With 650+ chemicals × 30+ health outcomes = 19,500+ tests → FDR correction essential

*Standard pharmaeopidemiology disclaimer: correlations are hypothesis-generating, not causal.*

---

## Empire Lab Value

This pipeline delivers three types of value:

1. **Content**: "What toxic chemicals near you are linked to which health problems? We analyzed
   EPA and CDC data to find out." → Substack/Medium article with interactive county map.

2. **Research**: Novel PFAS or industrial chemical × health outcome associations → preprint target.

3. **Data asset**: The TRI × NHANES/BRFSS joined database is reusable for dozens of sub-analyses.
   Built once, queried repeatedly.

---

## Next Steps

- [ ] Download TRI data for 2015-2023 (start there, not 1987)
- [ ] Identify NHANES cycles with most relevant biomarkers (2013-2018 for PFAS)
- [ ] Implement geo_join.py (BRFSS + TRI county join — the highest-priority technical piece)
- [ ] Run PFAS sub-analysis first (highest novelty potential, data already available)
- [ ] Full pipeline: Emperor session, Apr 2026+

*RS-008 design complete. Execution gated on Emperor arrival (~Apr 7, 2026).*
