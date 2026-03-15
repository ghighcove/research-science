---
title: "What 20 Million FDA Reports Say About SSRIs"
seo:
  substack:
    meta_description: "Statistical analysis of 20M FDA reports uncovers 199 novel SSRI adverse drug reactions via proportional reporting ratio methodology."
    tags: ["pharmacovigilance", "drug safety", "SSRI", "FDA", "data science"]
---
# What 20 Million FDA Reports Say About SSRIs

**A pharmacovigilance analysis of 6 antidepressants reveals 230 adverse event signals — 199 of which don't appear in standard clinical trial profiles.**

*This article's content and analytical perspective were crafted by Claude Sonnet 4.6. The project genesis and direction came from Glenn Highcove. For more information and feedback, connect with Glenn on [LinkedIn](https://www.linkedin.com/in/glennhighcove/).*

---

The number that started this project was 826.

That's the Proportional Reporting Ratio — a standard pharmacovigilance metric — for one specific combination: fluvoxamine (Luvox) and myoglobin in the urine. A PRR of 826 means this adverse event is reported 826 times more often for fluvoxamine than across the full FDA adverse event database, after controlling for overall reporting volume. The chi-squared statistic on that signal: 51,114.

That number isn't in any clinical trial profile for fluvoxamine. It emerged from 20 million patient reports.

This article explains where it came from, what it means, what it doesn't mean, and what the full analysis found.

---

## What FAERS Is — And What It Isn't

The FDA Adverse Event Reporting System (FAERS) is a database of voluntary adverse event reports submitted by patients, healthcare providers, and pharmaceutical manufacturers. As of the most recent quarterly update, it contains approximately 20 million reports covering decades of post-market drug surveillance.

It is not a controlled clinical trial. It cannot establish causation. The reports are voluntary, so they're subject to notoriety bias (widely-publicized effects are over-reported), Weber effect distortion (new drugs accumulate reports rapidly in the first two years), and confounding by co-medications (patients taking one SSRI typically take several other drugs).

What FAERS *can* detect is disproportionate reporting: the statistical signature that a particular drug-event combination is showing up more often than expected given background rates across the full database. When that signal is strong enough and consistent enough, it warrants clinical investigation. This is how regulators at the EMA and WHO use the data. It is also how this analysis used it.

The signal detection method used here is the Proportional Reporting Ratio (PRR), with signal criteria established by Evans et al.: PRR ≥ 2.0, event count ≥ 3, and chi-squared ≥ 4.0. This is a published, peer-reviewed standard used in regulatory pharmacovigilance worldwide. The code implementing this pipeline is open-source and available on GitHub.

---

## The Pipeline

The analysis queried the openFDA API across six SSRI antidepressants:

- **Fluoxetine** (Prozac): 84,185 FAERS reports
- **Sertraline** (Zoloft): 139,223 reports
- **Escitalopram** (Lexapro): 74,216 reports
- **Paroxetine** (Paxil): 51,761 reports
- **Citalopram** (Celexa): 111,530 reports
- **Fluvoxamine** (Luvox): 6,175 reports

For each drug, the pipeline tested 100 adverse event terms drawn from the MedDRA system against the Evans criteria. The total dataset analyzed: **20,006,989 FAERS reports**.

**[CHART: known_vs_novel.png — Stacked bar by drug showing ~85% novel signals vs. ~15% known across all 6 drugs]**

230 drug-event combinations met signal criteria. Of those, 199 — **86%** — are not among the commonly listed adverse events in published SSRI trial AE profiles.

That figure requires interpretation. "Novel" in this context means not appearing in standard SSRI clinical trial adverse event summaries. It does not mean unknown to medicine, unknown to clinicians who prescribe these drugs, or necessarily indicative of harm. Some signals reflect known pharmacology that simply wasn't labeled. Some reflect polypharmacy effects invisible in single-drug trials. Some may be artifacts of who reports what to FAERS. All require clinical judgment to interpret.

With that framing established, here are the four most significant patterns from the analysis.

---

## Finding 1: The Validation Signal

Before discussing novel findings, it's worth starting with a known one.

Citalopram's cardiac QT interval prolongation was the subject of an FDA Drug Safety Communication in 2011 — a high-profile regulatory action that resulted in dose restrictions and black box warnings. This is one of the most well-documented adverse effects in all of psychopharmacology.

In this analysis: **citalopram × QT prolongation: PRR = 9.15, chi² = 12,689, n = 1,750.**

Escitalopram (the mirror-image enantiomer of citalopram, sharing its mechanism): **PRR = 8.87, chi² = 7,873, n = 1,129.**

A pipeline that correctly identifies the most well-validated signal in SSRI pharmacology — and does so with high statistical confidence — has demonstrated its methodology works on known ground before making claims about unknown territory. This is a prerequisite for any responsible pharmacovigilance analysis, and the data delivers it.

---

## Finding 2: The Headline Signal

**[CHART: novel_signals_prr.png — Top 20 novel signals by PRR, dark theme, fluvoxamine dominates]**

The signal that generated PRR=826 is: fluvoxamine × myoglobin in the urine (myoglobinuria). This is a laboratory marker for rhabdomyolysis — the breakdown of muscle tissue that releases myoglobin into the bloodstream. When myoglobin reaches the kidneys, it can cause acute kidney injury and, in severe cases, renal failure.

The supporting signals make the mechanism legible. Alongside myoglobinuria, fluvoxamine shows elevated signals for:
- Blood creatine phosphokinase increased (PRR=17.4, n=154) — the primary rhabdomyolysis marker
- Blood lactate dehydrogenase increased (PRR=17.6, n=84) — muscle injury marker
- Antipsychotic drug level increased (PRR=71.9, n=60) — the probable mechanism
- Rhabdomyolysis (direct term): PRR=7.8, n=96

Fluvoxamine is among the most potent inhibitors of the CYP1A2 enzyme in the cytochrome P450 system. CYP1A2 metabolizes several atypical antipsychotics (olanzapine, clozapine, haloperidol) and statins. When fluvoxamine inhibits CYP1A2, co-administered drugs that depend on that pathway cannot be cleared normally. Their plasma levels rise. At elevated concentrations, some of these agents — particularly antipsychotics — can directly cause rhabdomyolysis.

This is a known pharmacological interaction. It is not in fluvoxamine's standard adverse event profile because it doesn't arise from fluvoxamine alone. It arises from polypharmacy — the exact condition that clinical trials are designed to exclude and that real-world FAERS reporting captures by default.

The signal doesn't require a new mechanism. It requires acknowledging that drug interactions invisible in controlled trials become visible in 20 million voluntary reports from actual patients.

**A note on the extreme PRR value**: Fluvoxamine has the smallest report base of the six drugs analyzed — 6,175 total reports versus 139,223 for sertraline. Smaller denominators make extreme PRR values mathematically more likely. Two factors confirm this isn't a small-sample artifact: (1) the chi-squared of 51,114 is calculated against the full 20-million-report database and accounts for sample size; (2) the cluster of supporting signals — CPK elevated, LDH elevated, myoglobinuria, and rhabdomyolysis as a direct FAERS term — all independently exceed Evans criteria. The signal is replicated across four independent terms, not just one extreme number.

---

## Finding 3: Serotonin Syndrome Across All Six Drugs

Serotonin syndrome is not a new concern for SSRIs — it appears in SSRI prescribing labels as a drug interaction warning. Its classification as "novel" in this analysis requires explanation: the comparison baseline here is clinical trial adverse event tables, not prescribing label warnings. Serotonin syndrome is absent from trial AE tables because those trials were designed as single-drug studies that excluded the polypharmacy conditions under which SS occurs. "Novel to trial profiles" is not the same as "novel to medicine." What the data contributes is not discovery but quantification: the magnitude and consistency of this signal at scale, across all six drugs simultaneously, in real-world polypharmacy populations that trials cannot capture.

| Drug | Serotonin Syndrome PRR | n |
|------|----------------------|---|
| Fluvoxamine | 40.7 | 229 |
| Paroxetine | 27.7 | 1,308 |
| Fluoxetine | 28.8 | 2,209 |
| Escitalopram | 22.1 | 1,497 |
| Sertraline | 17.2 | 2,186 |
| Citalopram | 15.0 | 1,523 |

*Note: Tables in the published version are rendered as images per platform requirements.*

Serotonin syndrome arises from excessive serotonergic activity — typically from combining drugs that increase serotonin through different mechanisms. An SSRI combined with a triptan (for migraines), MAO inhibitor, tramadol, or even some over-the-counter supplements creates risk. The condition ranges from mild (shivering, diarrhea) to severe (hyperthermia, seizures, death).

Fluvoxamine's highest PRR here is partly explained by its dual mechanism: it's both a serotonin reuptake inhibitor and a potent CYP1A2 inhibitor, meaning it can elevate serotonin-active drug levels *while simultaneously* increasing serotonin reuptake inhibition. This pharmacological stacking is not captured in single-drug trial profiles.

The consistent signal across all six drugs at these magnitudes is a pattern the data insists on and the pharmacology fully explains. It warrants being treated as a class-level finding, not individual drug findings that happen to cluster.

---

## Finding 4: The Suicide Signals

This finding requires the most careful framing, because the data is real and the interpretation is genuinely complex.

Every drug in this analysis shows disproportionate FAERS reporting for suicide-related events: completed suicide, suicide attempt, intentional self-injury, and intentional overdose. PRRs range from roughly 5 to 15 across drugs and event types. These numbers are not small.

The critical question is what these signals mean. SSRIs are prescribed almost exclusively to patients with depression, anxiety disorders, and other conditions that independently elevate suicide risk. This is called **indication bias**: the patients who receive the drug are a high-risk population regardless of drug effects. A PRR does not — and cannot — disentangle whether the drug causes the outcome or whether the population receiving it was already at elevated risk before the first dose.

The FDA added a black box warning to SSRI labels in 2004 for increased suicidality in pediatric and young adult patients. That warning reflects clinical trial data with comparator arms that can partially control for indication bias. The FAERS signal — with no comparator, no baseline, no age breakdown — cannot replicate that controlled finding. It can only report that these events appear disproportionately in the database.

What the signal shows: patients on SSRIs who experience adverse events and file FAERS reports are disproportionately reporting suicide-related events. Whether that reflects indication bias, a true drug effect, or both is a clinical question, not a statistical one.

The data is reported here as-is, with that caveat explicit. Removing it because it's uncomfortable would be a methodological failure.

*If you or someone you know is in crisis, contact the 988 Suicide and Crisis Lifeline by calling or texting 988 (US), or visit the [International Association for Suicide Prevention](https://www.iasp.info/resources/Crisis_Centres/) for resources outside the US.*

---

## What "86% Novel" Actually Means

The finding that 199 of 230 signals are "novel" — not in standard SSRI trial AE profiles — is the one number most likely to be misread.

It does not mean 199 previously unknown harms. It means 199 signals that meet Evans criteria in FAERS data but are not commonly listed in published clinical trial adverse event summaries for SSRIs.

Clinical trials are conducted under controlled conditions, in carefully selected patient populations, over defined time periods, with exclusion criteria that remove patients with co-medications or co-morbidities. FAERS captures real patients, with real polypharmacy, over decades of actual use.

The gap between those two populations *is* the gap this analysis is measuring. Some of what fills that gap reflects genuine post-market pharmacovigilance: drug interactions, population-level effects in elderly patients, effects that only appear at scale. Some reflects the reporting noise inherent in a voluntary system.

Distinguishing which is which is the work that comes next — not from a database scan, but from clinical pharmacology and targeted investigation of the highest-signal findings.

---

## What This Analysis Is and Is Not

This is an independent, unfunded, reproducible pharmacovigilance analysis using public FDA data and published methodology. The code is open-source. The findings are documented. Any researcher can run the pipeline and obtain the same results.

This is not a clinical trial. It is not a regulatory filing. It does not establish causation. It does not recommend clinical action. It is a hypothesis-generating tool — the first step in a pipeline that ends, if signals survive scrutiny, with peer review and publication.

Empire Lab operates under three structural rules:
1. Code is always open. Reproducibility is the credibility.
2. Independence is non-negotiable. No pharmaceutical company clients, ever.
3. Methodology first. Every finding is bounded by what the data can and cannot show.

---

## What Comes Next

The full signal database — all 199 novel signals, all 230 signals total, with PRR values, chi-squared statistics, event counts, and confidence intervals — is available to paid subscribers.

The pipeline runs monthly. Each run will diff new signals against the prior month, flag emerging patterns, and produce a delta report. Subscribers receive those reports as they publish.

The code and methodology are on GitHub: [github.com/ghighcove/research-science](https://github.com/ghighcove/research-science)

The next analysis in this series: what percentage of post-market FAERS signals across all drug classes are invisible in registration trial profiles? The SSRI analysis suggests the answer is around 85%. Whether that holds across oncology, cardiovascular, and neurological drug classes is the meta-question worth building toward.

---

*Empire Lab is an independent, one-person research operation. Methodology is peer-reviewed standard (Evans et al.). Code is open for independent verification. This analysis does not constitute medical advice. Signal detection in pharmacovigilance is a hypothesis-generating tool, not a causal determination.*

---

**Access the full signal database:**

🔬 **Researcher tier ($12/mo)**: All 230 signals, full PRR tables, CSV export, monthly delta reports
💼 **Professional tier ($49/mo)**: Same + custom queries (filter by event type, drug, PRR threshold)
📋 **Expert tier (custom)**: Signal documentation for litigation or research use

[Subscribe to Empire Lab Research →]
