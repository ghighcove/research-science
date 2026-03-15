# Empire Lab — Vision & Strategic Framework
## Cottage Science at Machine Scale

**Version**: 1.0
**Date**: 2026-03-14
**Author**: Glenn Highcove + Claude Sonnet 4.6
**Status**: Founding document

---

## Genesis

In early 2026, a small number of people began demonstrating that meaningful scientific discovery no longer required an institution. A researcher made a custom cancer vaccine for a dying pet — not at a university, not with a grant — using open-source bioinformatics pipelines, publicly available genomic databases, and the mRNA synthesis protocols democratized after COVID. The tumor responded. The story circulated quietly.

This wasn't an anomaly. It was a signal.

The same year, AI systems began outperforming specialist human researchers in specific domains: protein structure prediction (AlphaFold), mathematical proof generation (DeepMind AlphaProof), drug-target interaction modeling, literature synthesis at scale. The tools existed. What was missing was the *operational infrastructure* to run a small, recursive, AI-augmented science team systematically and continuously — not as a one-off experiment, but as a weekly practice.

This document is the founding charter for the Empire Lab: a cottage science operation built on the thesis that a small recursive team of AI agents and one human can, over time, produce genuine scientific findings. Not Nobel Prize work. Something more interesting: *systematic discovery at a cadence no individual researcher can match, in fields where cross-domain synthesis is the primary bottleneck.*

---

## The Structural Argument: Why This Should Work

### The Replication Crisis Is a Standing Invitation

In 2005, John Ioannidis published "Why Most Published Research Findings Are False" — one of the most-cited papers in the history of science. He showed mathematically that under typical conditions (low prior probability, small samples, flexible methodology, publication bias), most statistically significant findings in the literature are false positives. The Open Science Collaboration's 2015 replication project confirmed it empirically: only 36% of 100 psychology studies replicated.

This is not a scandal that will be fixed. The incentive structure of academic science (publish or perish, positive result bias, grants for novelty not replication) makes this a *permanent feature* of the landscape. Every field has it. Psychology, nutrition science, cancer biomarker research, social science — all have documented non-replication rates above 50%.

What this means for cottage science: there is a permanent, renewable supply of findings worth re-examining. The data to re-examine them is often public. The analysis tools are free. The only missing ingredient has been a systematic operation to do it at scale. That's what the Empire Lab supplies.

### Public Data Is Massively Underanalyzed

The following datasets are publicly available, free to access, and systematically underanalyzed relative to their potential:

**Biomedical:**
- **NCBI Gene Expression Omnibus (GEO)**: 215,000+ gene expression datasets deposited as publication requirements. A meaningful fraction have fewer than 3 downstream citations — deposited and never independently analyzed. Each contains 20,000+ genes of differential expression data from specific disease/treatment conditions.
- **FDA FAERS (Adverse Event Reporting System)**: 20+ million adverse event reports, updated quarterly. The FDA's own disproportionality analysis has documented blind spots for rare drug combinations, long-latency events, and events underreported because the causal connection isn't obvious.
- **ClinicalTrials.gov**: 500,000+ registered trials. ~100,000 completed with no associated publication — the "file drawer problem" at industrial scale. These trials consumed billions in funding. Their results are unknown because negative and null results don't get published.
- **NCBI dbGaP**: Genome-wide association study (GWAS) data for hundreds of diseases. Many datasets have been analyzed for the primary phenotype; cross-phenotype and cross-dataset analysis is sparse.

**Environmental/Population:**
- **EPA Toxic Release Inventory (TRI)**: 30 years of industrial chemical release data by facility, by zip code. Cross-referenced against health outcomes data, this is a pollution-health correlation database that environmental lawyers have been piecing together manually for decades.
- **CDC NHANES (National Health and Nutrition Examination Survey)**: Comprehensive nutrition, health marker, and disease outcome data going back to 1971. Most analyses use a single wave; multi-wave longitudinal synthesis is rare.
- **NOAA Climate Data**: 150 years of station-level temperature, precipitation, and extreme weather data. Synthesis with agricultural yield data, health outcome data, and economic data is sparse.

**Economic/Social:**
- **USPTO Patent Database**: Full text of every US patent since 1976. Technology trajectory analysis, emerging domain detection, competitor landscape — largely manual today.
- **SEC EDGAR**: Every public company filing since 1996. Natural language analysis of risk factors, MD&A sections, and earnings call transcripts reveals patterns invisible to quarterly earnings analysis.
- **OpenAlex**: 250+ million academic papers with citation graphs, author networks, and institutional affiliations. The meta-science layer — studying how science itself works — is thin despite this data existing.

**The core observation**: Each of these datasets was collected at enormous public expense. Each contains more signal than has been extracted. Each requires *breadth* (reading across domains), *patience* (running analyses that take days), and *synthesis* (connecting findings across datasets) — all Empire strengths.

### AI Has Permanent Structural Advantages in Specific Scientific Bottlenecks

AI does not beat human scientists in creativity, intuition, or the kind of generative insight that produces paradigm shifts. But AI has *permanent structural advantages* in three specific bottlenecks that have historically limited discovery:

**Bottleneck 1 — Volume synthesis**
A human researcher can deeply read approximately 200-500 papers per year in their specialty. PubMed adds 1.5 million new papers per year. The gap between what any individual can read and what is published grows every year. For questions that require synthesis across thousands of papers — "what does the entire literature on drug X say about outcome Y?" — human researchers cannot do this comprehensively. AI can.

**Bottleneck 2 — Cross-domain integration**
Most significant discoveries in the past 50 years came from applying methods from one field to problems in another: information theory to biology (genomics), physics methods to finance (quant trading), network theory to epidemiology, statistical mechanics to social science. These cross-domain transfers happen slowly because researchers specialize. An AI system that reads across all domains simultaneously has no specialization penalty.

**Bottleneck 3 — Hypothesis generation at scale**
Traditional hypothesis generation is rate-limited by a researcher's reading and their intuition. A system that can generate 1,000 hypotheses per week, score them by prior probability and testability, and route the top 10 to deeper analysis is operating at a fundamentally different throughput than any individual scientist. Most of the 1,000 will be wrong. That's fine. The question is whether 5-10 per year are right — and whether those justify the infrastructure cost.

---

## The Fields

### Tier 1 — Build Now (High tractability, clear value, Empire-ready)

---

#### 1. Pharmacovigilance — FDA FAERS Signal Detection

**What it is**: The FDA Adverse Event Reporting System is the world's largest database of drug safety signals. Healthcare providers, patients, and manufacturers are required (or encouraged) to report adverse events — unexpected or serious side effects that occur while taking a drug. The FDA runs automated disproportionality analysis (Proportional Reporting Ratio, Reporting Odds Ratio, Information Component) to flag signals.

**Why the FDA misses things**: FAERS has known structural limitations:
- Reports are voluntary outside of manufacturer reporting requirements — systematic underreporting for events that don't look "drug-related"
- Long-latency adverse events (effects appearing months or years after drug use) are rarely connected by the reporter
- Drug combination effects (patient on 5 medications — which one caused the event?) are analytically hard
- Rare events in rare populations: if 1 in 100,000 patients on drug X develops a specific liver injury, FAERS might have 15 reports — enough for a signal, but below the FDA's automated detection threshold
- Events that are common in the general population (myocardial infarction, depression) require elevated rates vs. baseline to be flagged — the baseline modeling is imperfect

**What has slipped through**: Vioxx (rofecoxib) — 55,000 estimated excess cardiac deaths before withdrawal in 2004. Post-hoc FAERS analysis showed the signal was detectable 18 months earlier. Avandia (rosiglitazone) — same pattern. Fluoroquinolone-associated disability (FQAD) — still inadequately labeled despite thousands of FAERS reports.

**The Empire pipeline**:
1. Download quarterly FAERS data (free, public, ~500MB per quarter)
2. Parse into drug-event pairs with patient demographics
3. Compute PRR and ROR for all drug-event pairs meeting minimum count threshold (≥3 reports)
4. Cross-reference against published clinical trial adverse event profiles (from ClinicalTrials.gov result summaries)
5. Flag: any drug-event pair where FAERS rate >> trial-reported rate by meaningful factor
6. Enrich flagged signals: mechanism analysis (does the drug's pharmacology plausibly explain the signal?), literature search for corroborating case reports
7. Publish as "FAERS Watch" — weekly signal report with methodology transparent

**What discovery looks like here**: A signal that says "drug X appears to have a meaningful association with condition Y that isn't in the label, isn't in the published trial data, and has a plausible mechanism." That's not proof. It's a hypothesis with statistical support. It deserves attention. If it holds up on closer analysis, it's worth publishing to bioRxiv and notifying the relevant medical community.

**Who buys this**:
- Medical journalists covering drug safety (The BMJ, STAT News, ProPublica have all run FAERS-based investigations)
- Patient advocacy organizations for specific conditions
- Plaintiffs' attorneys in pharmaceutical litigation (they pay $10,000-$50,000 for this kind of analysis)
- Clinical pharmacologists at academic medical centers
- Subscription newsletter readers interested in evidence-based medicine

**Realistic output**: 2-5 signal reports per quarter, of which 1 might be significant enough to publish. Over 3 years, that's 3-15 published signals. If even one leads to a label change or physician behavior change, the social value exceeds the infrastructure cost by several orders of magnitude.

---

#### 2. Orphaned Genomic Data Mining — NCBI GEO

**What it is**: Gene Expression Omnibus is a public repository where researchers deposit genomic data as a publication requirement. The data is raw and re-analyzable by anyone. The problem: most depositors analyze for their specific hypothesis (is gene X differentially expressed in disease condition vs. control?) and publish one paper. The remaining 19,999 genes of expression data sit untouched.

**The opportunity**: Every deposited GEO dataset is a mini-experiment that answered one question and ignored thousands of others. Cross-dataset analysis — applying findings from one study's conditions to questions raised by another — is the methodology that produced the Connectivity Map (Broad Institute), one of the most influential drug repurposing resources in biomedical research. They ran existing gene expression data against drug perturbation profiles and found new uses for existing drugs. Some have reached clinical trials.

**The Empire pipeline**:
1. Weekly: query GEO API for datasets in target disease area (oncology, neurodegeneration, rare disease) with <3 downstream citations and RNA-seq or microarray data
2. Normalize and run differential expression analysis (DESeq2 or limma via Bioconductor, callable from Python)
3. Cross-reference gene lists against:
   - DisGeNET: gene-disease associations
   - DrugBank: drug-target interactions
   - OpenTargets: therapeutic target evidence
   - MSigDB: gene set enrichment (pathways, hallmarks)
4. Flag: any gene signature that matches a known drug's mechanism of action (repurposing candidate), a known disease gene set in an unexpected context, or a pathway activation pattern not described in the original paper
5. Route flagged findings to synthesis: generate a hypothesis brief, draft a short preprint

**What discovery looks like here**: "Dataset GSE12345 examined lung cancer cell lines treated with compound X. Standard DEA found 47 differentially expressed genes. Cross-referencing against drug perturbation profiles reveals significant overlap with the mechanism of action of drug Y (used for condition Z) — suggesting potential repurposing relevance that was not the original study's focus."

This is publishable to bioRxiv. Other researchers will see it, run their own validation if they have the lab capability, and cite you if it holds up. Citation-based credibility builds over time.

**What makes this tractable**: Unlike wet lab experiments, you cannot get a false negative from pipette contamination. The data is fixed. Your analysis either finds something or it doesn't. The only failure mode is a false positive — a statistical artifact. But you publish the methodology transparently, which means other researchers can check your math.

---

#### 3. Clinical Trial Registry Mining — ClinicalTrials.gov

**What it is**: Every clinical trial conducted in the US (and most internationally) must be registered at ClinicalTrials.gov before it begins, and results must be posted within 12 months of completion. The reality: many results are never posted, many summaries are incomplete, and cross-trial synthesis almost never happens.

**The publication gap**: A 2020 study in the New England Journal of Medicine found that 40% of trials registered on ClinicalTrials.gov between 2008 and 2017 never had results publicly reported. That's hundreds of thousands of trials. The data to know why is also on ClinicalTrials.gov: outcome type, sponsor, drug class, disease area. The pattern of what gets published and what doesn't is itself a finding.

**The Empire pipeline**:
1. Download ClinicalTrials.gov full dataset (free XML download, ~4GB)
2. Parse: completion date, results posted flag, primary sponsor type (industry, NIH, academic), condition, intervention
3. Identify unpublished completed trials in disease areas of interest
4. For those with posted results but no PubMed-linked publication: extract the result summaries
5. Synthesize: what did unpublished trials in condition X find? Is there a pattern (negative results, industry trials for failed drugs, inconvenient safety findings)?
6. Publish the synthesis, methodology transparent

**What discovery looks like here**: "Of 847 completed trials for condition X registered between 2010 and 2020, 41% have no associated publication. Industry-sponsored trials were 3x less likely to report results than NIH-sponsored trials. Of the 156 trials with posted result summaries but no publication, 62% reported null or negative primary outcomes. The aggregate effect size across these unpublished trials for outcome Y was..." — that's a NEJM-quality finding produced entirely from public data with no original data collection.

---

### Tier 2 — Build on Emperor (Computationally heavier, still tractable)

---

#### 4. Environmental Exposure + Health Outcome Correlation — EPA TRI × CDC NHANES

**What it is**: The EPA Toxic Release Inventory documents every industrial chemical release above reporting thresholds since 1987, by facility and location. NHANES documents health markers, disease prevalence, and biomarkers for a nationally representative population sample going back to 1971. Cross-referencing them — "do people who live near facilities releasing chemical X have higher rates of condition Y?" — is the core of environmental epidemiology.

**Why this is underexplored**: Environmental epidemiology requires matching individual-level health data with facility-level exposure data by geography. This is computationally intensive and requires data engineering that most academic researchers don't have time for. The EPA and NIH do it for specific chemicals of highest concern. The comprehensive cross-reference — all facilities, all chemicals, all conditions — hasn't been done.

**Why this matters**: PFAS ("forever chemicals") became a national crisis 30 years after the exposure began. Lead in water was measured but not acted on for decades. The pattern: exposure accumulates, health effects emerge, the connection is made too late. A systematic cross-reference running continuously might catch the next PFAS earlier.

**What discovery looks like here**: Statistical correlations between facility-type releases and specific biomarkers in NHANES. Some will be known. Some will be noise. Some might be novel. The methodology is publishable to Environmental Health Perspectives or Environmental Science & Technology regardless of whether specific findings are novel — systematic cross-reference at this scale hasn't been published.

---

#### 5. Nutritional Epidemiology Reanalysis — NHANES + UK Biobank

**What it is**: Nutrition science has the highest known false positive rate of any health science field. The reasons are structural: food frequency questionnaires are inaccurate by design; the "healthy user" bias is enormous (people who eat vegetables also exercise, sleep better, and have lower stress); the number of dietary variables is vast (enabling p-hacking even unintentionally); industry funding is pervasive.

The result: a 50-year literature full of contradictions. Eggs cause heart disease / eggs are fine. Coffee causes cancer / coffee prevents cancer. Fat is bad / sugar is bad / fat is fine. Nearly every major dietary recommendation has been reversed at least once.

**The Empire angle**: NHANES is public. UK Biobank (with application) is publicly available. The raw data that underlies most nutritional epidemiology findings can be re-analyzed. An Empire pipeline that:
1. Downloads NHANES continuous survey data
2. Re-runs the regression analysis for major dietary claims from published papers
3. Applies modern causal inference methods (propensity matching, instrumental variables where available)
4. Flags where the new analysis disagrees with the published conclusion

...is doing genuine replication science. Published findings that don't survive re-analysis with better methods are a real contribution to the field.

---

#### 6. Patent Landscape Intelligence — USPTO + Google Patents

**What it is**: Every patent application in the US is public after 18 months. The full text, claims, and citation network is available. Patent landscapes — "what is being invented in domain X, by whom, and what does it suggest about the next 5 years?" — are today produced by large consulting firms charging hundreds of thousands of dollars for reports that are often shallow.

**The Empire angle**: Natural language analysis of patent claims, automated classification, citation network analysis, and temporal trend detection can be automated. The output — "here is what's being patented in domain X, here are the acceleration trends, here are the white spaces" — is valuable to:
- Venture capital investors
- R&D departments doing competitive intelligence
- Entrepreneurs looking for gaps
- Academic researchers who want to know where industry is heading before it's published

**What makes this tractable**: Patent text is structured (claims, abstract, description, references). The USPTO and Google provide free bulk downloads. Temporal analysis (application filing date vs. grant date) allows trend detection. No original science is needed — the synthesis is the product.

---

### Tier 3 — Math and Emerging AI Science

This tier is different from Tiers 1-2. It's not about analyzing existing data. It's about contributing to the frontier of mathematical and computational knowledge — the hardest category, but also potentially the most transformative.

---

#### 7. AI-Assisted Mathematics — The New Frontier

**The moment**: In 2024, DeepMind's AlphaProof system proved four of six problems at the International Mathematical Olympiad at silver medal level. In the same year, multiple groups used LLMs to identify errors in published mathematical proofs, generate new proof strategies, and formalize existing informal proofs into machine-checkable form. The barrier between "AI as math assistant" and "AI as math co-discoverer" is collapsing.

**What cottage math looks like**:

*Conjecture verification*: Many mathematical conjectures (Collatz, Goldbach, Riemann Hypothesis) have been verified computationally for all numbers up to some bound. The Empire can contribute verification runs, extending known bounds, which is a citable contribution even if the full proof doesn't follow.

*Combinatorics and graph theory*: These fields have a large number of open problems that are tractable with computational search. The Ramsey number R(5,5) is unknown. Large-scale computational search combined with structural reasoning is how progress happens. Empire can run these searches. Results have been published in combinatorics journals from purely computational contributions.

*Automated formal verification*: Lean 4 and Coq are proof assistants where you write machine-checkable proofs. There's an active project (Mathlib) to formalize all of mathematics in Lean. Contributing formalizations of existing proofs — or finding gaps where informal proofs fail to formalize — is a real academic contribution. LLMs have been shown to be surprisingly good at this.

*Sequence and pattern discovery*: The OEIS (Online Encyclopedia of Integer Sequences) is a database of 370,000+ integer sequences. Contributing a new sequence — a pattern noticed in the output of a computational process that hasn't been catalogued — is a citable contribution. It's a low bar but it's real.

**The deeper question**: Can the Empire identify new conjectures? Not just verify known ones, but notice patterns in mathematical output that suggest new relationships? This is where recursive AI analysis gets interesting. A system that generates examples of a mathematical object, notices a pattern across thousands of examples, and formulates a conjecture — that's the machine equivalent of mathematical intuition. It has happened in small ways (Ramanujan machine). It's an open research frontier.

---

#### 8. AI Science — The Meta-Layer

**What it is**: "AI science" here means two things: (a) empirical study of how AI systems behave, and (b) theoretical contributions to understanding why AI works. Both are tractable for the Empire and both have publication venues.

**Empirical AI behavioral science**:

This is almost exactly what the Prompt Whisperer project already is. You're doing empirical science about AI system behavior: you have a hypothesis (prompting strategy X produces different outputs than strategy Y), you design an experiment, you collect data, you analyze it, you report findings. The Prompt Whisperer is citizen science about AI.

This can be extended significantly:
- Systematic mapping of "failure modes by model size" — what can a 7B model do that a 3B model can't? Where is the capability cliff?
- Prompt injection attack patterns — documenting attack vectors and their effectiveness across models (already a published research area; Empire can contribute empirical data)
- Hallucination characterization — under what conditions does a specific model hallucinate? Can you predict it? This is an open empirical question with real safety implications
- Fine-tuning behavior — how does fine-tuning on domain data change model behavior in other domains? (Catastrophic forgetting, capability generalization)
- Emergent behavior at scale — the "emergent capabilities" debate in AI involves claims about behaviors that appear discontinuously at certain model sizes; rigorous empirical testing of these claims is genuinely valuable

**Theoretical AI contributions**:

This is harder. The mathematical theory of deep learning is one of the most active and incomplete fields in science. What's tractable for Empire:
- Reproducing and extending known theoretical results in simplified settings
- Computational verification of theoretical bounds
- Empirical testing of theoretical predictions against model behavior
- Survey and synthesis papers — "here is the state of theory on phenomenon X" — which are highly cited and don't require original theoretical results

The arxiv cs.LG and cs.AI preprint servers see 200+ new papers per day. Many are incremental. A synthesis paper that says "here are the 20 most important papers on interpretability from 2024-2025 and here is what they collectively say" is a contribution that many researchers want but nobody has time to write.

---

#### 9. Computational Linguistics and Language Model Science

**What it is**: The science of how language models represent, process, and generate language is surprisingly young. Many fundamental questions are open:
- What do the attention heads "see"? (Mechanistic interpretability)
- How do models represent factual knowledge, and how can it be edited?
- What is the computational geometry of semantic space in embedding models?
- Can we predict which tokens a model will hallucinate before it generates them?

**Why this is tractable**: All of these questions can be investigated empirically using open-source models (Llama, Mistral, Phi, Qwen) with Ollama running locally. The Empire has 6 models running. Emperor will run 70B. The computational infrastructure for empirical interpretability research is already in place.

**What discovery looks like here**: "Across 5 open-source models of different sizes, we find that [factual claim type X] is consistently encoded in [layer range Y], while [factual claim type Z] shows no consistent encoding location, which correlates with higher hallucination rates for type Z claims." This is a real finding. It would be of interest to the interpretability community. It's publishable to arxiv and potentially to conferences (ICML, NeurIPS, ICLR all have interpretation tracks).

---

#### 10. Computational Social Science and Collective Behavior

**What it is**: The study of how collective human behavior emerges from individual decisions, using large-scale behavioral data. This field was transformed by the availability of social media data, but the big platforms have been steadily closing their APIs. The remaining open data sources are:
- Reddit (Pushshift archive through 2023 — 3+ billion posts and comments)
- Wikipedia edit history (every edit ever made, public)
- GitHub commit history (code evolution as social behavior)
- ArXiv submission and citation patterns (science as social behavior)
- FEC political donation data (political behavior by geography and occupation)

**Why this is Empire-tractable**: These are large structured datasets that require computational analysis. The questions are interesting (how does misinformation spread? how does consensus form? what predicts scientific citation?) and the publication venues (ICWSM, EPJ Data Science, Nature Human Behaviour) are active and receptive to computational work.

---

## The Discovery Pipeline: Operational Design

The above fields share a common workflow structure. The Empire Lab runs one recurring pipeline:

### Weekly Science Cycle (Post-Emperor)

```
Monday AM — Emperor runs:
  1. FAERS signal detection (new quarterly data if available)
  2. GEO orphaned dataset query + top 3 datasets analyzed
  3. ClinicalTrials.gov gap scan (newly completed trials, no results posted)
  4. Target field: patent landscape / NHANES / EPA TRI (rotating weekly)

  Output: EMPEROR_OUTBOX/SCIENCE_BRIEF_YYYY-MM-DD.md
  Format: [field] | [finding] | [confidence 0-1] | [publishability: preprint|article|note] | [next step]

Tuesday AM — Claude reviews brief:
  Any finding above confidence 0.7 → route to synthesis session
  Any finding above confidence 0.85 → draft preprint abstract
  Kill: anything below 0.4 confidence, or finding already in literature

Wednesday (optional) — Synthesis session:
  Claude writes up flagged finding as structured analysis
  Routes to: bioRxiv draft | article draft | idea pipeline
```

This is approximately 3-5 hours of Emperor compute per week. At Emperor's expected throughput (~273 GB/s bandwidth, 70B capable), this is well within capacity. The human time required is 30-60 minutes: reviewing the brief and deciding what to route.

---

## The Validation Philosophy

A permanent tension in cottage science: how do you know if a finding is real?

The honest answer: *you often don't, at first.* That's not a disqualifier — it's how all science works. The validation ladder is:

**Level 1 — Statistical validity**: Is the analysis mathematically sound? Does it survive basic checks (multiple testing correction, confounders accounted for, sample size adequate)? Empire can do this internally.

**Level 2 — Methodological transparency**: Is the methodology published clearly enough that someone else could reproduce it? If yes, the finding can be scrutinized. Empire publishes all methodology.

**Level 3 — Independent replication**: Does another group, running the same analysis on the same data, get the same result? This is the true standard. We can't control whether others will replicate. We can make it easy by publishing data and code.

**Level 4 — Experimental validation**: Does a wet lab / clinical / field study confirm what the computational analysis predicted? This is beyond Empire's direct capability — but Empire can design findings to be *easily validatable* by others who do have labs.

The goal: produce Level 1 and Level 2 findings consistently, aim for Level 3 when possible, and design findings so that others are motivated to reach Level 4.

---

## The Productization Stack

Scientific discovery has multiple downstream product types, ordered by time-to-revenue and effort:

**Tier A — Immediate, existing infrastructure (weeks)**
- Articles on Medium/Substack: same Empire publishing pipeline already built
- Target: "What FAERS data says about [drug class]" — general audience, uses existing subscriber base

**Tier B — Credibility building (months)**
- bioRxiv/arXiv preprints: no peer review, permanent DOI, real credibility signal
- Target: first preprint within 90 days of pipeline launch

**Tier C — Recurring intelligence product (6-12 months)**
- Weekly/monthly newsletter: "FAERS Watch", "GEO Discovery Report", "Clinical Trial Transparency Digest"
- Subscription model: $5-15/month consumer, $50-200/month professional
- Target: 500 subscribers = self-sustaining; 5,000 = significant revenue

**Tier D — High-value analysis on demand (12+ months)**
- Litigation support: pharmaceutical adverse event analysis for plaintiffs' attorneys
- Investment intelligence: patent landscape and clinical pipeline analysis for biotech investors
- Regulatory consulting: drug safety signal analysis for policy organizations
- Target: 1 engagement per quarter at $5,000-25,000 = meaningful revenue with minimal volume

---

## On the Pet Cancer Vaccine, and What It Means

The story that launched this project: a person, using open-source tools, mRNA synthesis protocols democratized by COVID vaccine manufacturing, and publicly available genomic databases, made a custom cancer vaccine for a dying pet. The tumor responded.

Whether the specific result holds up under scrutiny matters less than what the story represents. It says: the tools of sophisticated science are now available to people who aren't inside institutions. The institutional wrapper — the university, the grant, the regulatory approval — was never the knowledge. It was the access management layer. Access is being democratized.

The Empire Lab isn't trying to replace institutions. Institutions do things we can't: run controlled clinical trials, maintain biobanks, operate particle accelerators, recruit patient populations. There are entire categories of important science that require institutional resources and always will.

But the class of science that requires *synthesis, computation, and patient systematic analysis of existing data* — that class is now available to anyone with the tools, the discipline, and the recursive infrastructure to do it consistently.

The question isn't "are we smart enough?" We have access to the same models that are passing medical licensing exams, solving olympiad mathematics, and predicting protein structures that stumped human researchers for 50 years. The question is: *what do we do with that, systematically, over time?*

This document is the first answer.

---

## First Experiments (Ordered by Tractability)

1. **FAERS demo run** — Pull Q4 2025 FAERS data, run PRR analysis on SSRIs (well-understood class, good for methodology validation), compare against published trial adverse event profiles, write up as a methodology demonstration article
2. **GEO orphan query** — Query GEO API for lung cancer datasets with <3 citations, download the top candidate, run DESeq2, cross-reference against DrugBank/OpenTargets, write up findings
3. **ClinicalTrials.gov publication gap scan** — Query all completed trials in depression (high file-drawer problem documented) from 2015-2020, calculate publication rate by sponsor type, write up as a journalism-style analysis piece
4. **Prompt Whisperer extension** — Design Experiment 2 in the AI behavioral science track: systematic hallucination characterization across 3 local models
5. **NHANES diet-health reanalysis** — Pick one well-known dietary claim (red meat + cardiovascular), re-run NHANES regression with modern confounders, compare against published result

---

## Appendix: Key Data Sources and Access

| Dataset | URL | Access | Size | Update Frequency |
|---------|-----|--------|------|-----------------|
| FDA FAERS | opendata.fda.gov/drug/event | Free download | ~2GB/quarter | Quarterly |
| NCBI GEO | ncbi.nlm.nih.gov/geo | Free, API available | Variable | Daily |
| ClinicalTrials.gov | clinicaltrials.gov/api | Free REST API | ~4GB full dump | Daily |
| EPA TRI | epa.gov/toxics-release-inventory-tri-program | Free download | ~500MB/year | Annual |
| CDC NHANES | cdc.gov/nchs/nhanes | Free download | ~10GB total | Biennial |
| USPTO Patents | patentsview.org/download | Free bulk download | ~50GB | Annual |
| OpenAlex | openalex.org | Free API + bulk | ~250GB | Weekly |
| Reddit (Pushshift) | pushshift.io / academic torrent | Academic access | ~1TB | Archived |
| arXiv | arxiv.org/help/bulk_data | Free S3 access | ~1TB | Daily |
| GBIF | gbif.org/developer/occurrence | Free API | ~70GB | Weekly |
| dbSNP / dbGaP | ncbi.nlm.nih.gov | Free / application | Variable | Ongoing |
| UK Biobank | ukbiobank.ac.uk | Application required | ~10TB | Ongoing |

---

*This document will be updated as the lab produces findings. Each experiment will generate a findings file in `/findings/`. The pipeline code will live in `/pipelines/`. Discovery log maintained in `/findings/discovery_log.md`.*

*Empire Lab. Cottage science at machine scale.*
