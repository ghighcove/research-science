# RS-002 — GEO Orphan Dataset Analysis: Lung Cancer
*Date: 2026-03-15 | Citation threshold: ≤2 linked PMIDs | Date range: 2019–2023*

---

## Executive Summary

**36% of lung cancer RNA-seq datasets on GEO have zero linked publications.**

Of 100 completed lung cancer RNA-seq datasets deposited to GEO between 2019 and 2023:
- **36 datasets (36%)** have no linked publications — true orphans
- **61 datasets** have exactly 1 linked PMID (typically the depositor's paper only)
- Only **0 datasets** have been independently reanalyzed (>2 PMIDs)

These are the datasets that exist — data collected, patients enrolled, samples processed —
but whose findings have never been independently synthesized. Each is a candidate for
Empire Lab secondary analysis.

---

## Cohort Overview

| Citation tier | Count | % | Total samples |
|--------------|-------|---|---------------|
| 0 PMIDs — true orphans | 36 | 36% | 333 |
| 1 PMID — depositor paper only | 61 | 61% | 1,868 |
| 2 PMIDs — minimal reanalysis | 3 | 3% | 129 |
| >2 PMIDs — published | 0 | 0% | 0 |
| **Total** | **100** | 100% | **2,330** |

---

## Top Orphan Datasets (ranked by Drug Target Relevance)

Datasets with druggable lung cancer target genes (EGFR, KRAS, ALK, etc.) in their
title or abstract receive higher Drug Target Relevance (DTR) scores.

| Accession | Title | Samples | DTR Score | Linked PMIDs | Year | Key Targets |
|-----------|-------|---------|-----------|-------------|------|-------------|
| [GSE217646](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE217646) | RB1 expression and targeting by CDK4/6 inhibitors in sm… | 5 | 6 | 1 | 2022 | TP53, RB1, CDK4 |
| [GSE232569](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE232569) | Association of Antifolate Response Signature Status and… | 95 | 5 | 1 | 2023 | MET, RET |
| [GSE232890](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE232890) | Relation between TP53 GOF mutation and Osimertinib trea… | 8 | 5 | 0 | 2023 | TP53, EGFR |
| [GSE190704](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE190704) | The role of S100A9 in brain metastesis in EGFR-mutant l… | 18 | 4 | 0 | 2023 | MET, EGFR |
| [GSE226712](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE226712) | Fast proliferating and slowly migrating non-small cell … | 18 | 4 | 1 | 2023 | MET, RET |
| [GSE231938](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE231938) | Metabolic Reprogramming Driven by IGF2BP3 Promotes Acqu… | 10 | 4 | 1 | 2023 | MET, EGFR |
| [GSE244376](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE244376) | Isovalerylspiramycin I suppresses small cell lung cance… | 6 | 4 | 0 | 2023 | MET, MYC |
| [GSE156054](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE156054) | Next Generation Sequencing of EGFR-mutant non-small cel… | 6 | 4 | 1 | 2023 | MET, EGFR |
| [GSE202864](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE202864) | Mammalian SWI/SNF chromatin remodeling complexes promot… | 90 | 3 | 1 | 2023 | EGFR |
| [GSE227999](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE227999) | Mammalian SWI/SNF chromatin remodeling complexes promot… | 82 | 3 | 1 | 2023 | EGFR |
| [GSE202859](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE202859) | Mammalian SWI/SNF chromatin remodeling complexes promot… | 52 | 3 | 1 | 2023 | EGFR |
| [GSE211215](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE211215) | Warburg effect enhanced by AKR1B10 promotes acquired re… | 6 | 3 | 1 | 2023 | MET |
| [GSE223372](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE223372) | Lurbinectedin is an effective therapeutic target for de… | 61 | 2 | 2 | 2023 | MET |
| [GSE239514](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE239514) | Molecular and immune changes in tumor draining lymph no… | 25 | 2 | 1 | 2023 | RET |
| [GSE228217](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE228217) | Optimised linear amplification method for whole transcr… | 21 | 2 | 0 | 2023 | MET |
| [GSE173761](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE173761) | METTL1/WDR4 mediated tRNA N7-methylguanosine (m7G) modi… | 14 | 2 | 0 | 2022 | MET |
| [GSE226285](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE226285) | By controlling glutathione metabolism, NR0B1 prevents l… | 12 | 2 | 1 | 2023 | MET |
| [GSE192475](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE192475) | MUC1-C IS A MASTER REGULATOR OF SMALL CELL LUNG CANCER … | 12 | 2 | 1 | 2023 | MYC |
| [GSE159801](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE159801) | MUC1-C IS A MASTER REGULATOR OF SMALL CELL LUNG CANCER … | 12 | 2 | 1 | 2023 | MYC |
| [GSE210560](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE210560) | Effect of theta toxin secreted by live S. typhimurium i… | 12 | 2 | 1 | 2022 | RET |
| [GSE219030](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE219030) | A TIAM1-TRIM28 complex mediates epigenetic silencing of… | 10 | 2 | 1 | 2023 | MET |
| [GSE232904](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE232904) | Identification of exosomal microRNA panel as diagnostic… | 10 | 2 | 1 | 2023 | MET |
| [GSE237319](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE237319) | CD44+ Lung Cancer Stem Cell-derived Vascular Pericytes … | 10 | 2 | 0 | 2023 | MET |
| [GSE239495](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE239495) | Canagliflozin mediates tumor suppression alone and in c… | 9 | 2 | 1 | 2023 | MYC |
| [GSE161218](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE161218) | Drug repurposing unveils new combinatorial treatments t… | 9 | 2 | 1 | 2023 | KRAS |
| [GSE178738](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE178738) | Neuronal mimicry mechanisms promote the growth of small… | 9 | 2 | 0 | 2023 | MET |
| [GSE114563](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE114563) | CBX5 loss drives EGFR inhibitor resistance and results … | 9 | 2 | 1 | 2023 | EGFR |
| [GSE234816](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE234816) | LCMR1 Promotes Large-cell Lung Cancer Proliferation and… | 8 | 2 | 1 | 2023 | MET |
| [GSE173750](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE173750) | METTL1/WDR4 mediated tRNA N7-methylguanosine (m7G) modi… | 8 | 2 | 0 | 2022 | MET |
| [GSE202342](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE202342) | AXL and error-prone DNA replication confer drug resista… | 7 | 2 | 1 | 2022 | EGFR |
| [GSE248935](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE248935) | CD146 as a potent target for anti-vascular therapies in… | 6 | 2 | 1 | 2023 | MET |
| [GSE198099](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE198099) | Immune suppressive landscape in the human non-small cel… | 6 | 2 | 0 | 2023 | MET |
| [GSE218949](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE218949) | The molecular mechanism of microtubule-binding protein … | 6 | 2 | 1 | 2023 | MET |
| [GSE178736](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE178736) | Neuronal mimicry mechanisms promote the growth of small… | 6 | 2 | 0 | 2023 | MET |
| [GSE237317](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE237317) | CD44+ Lung Cancer Stem Cell-derived Vascular Pericytes … | 6 | 2 | 0 | 2023 | MET |
| [GSE222023](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE222023) | A self-propagating c-Met-SOX2 axis drives cancer-derive… | 6 | 2 | 0 | 2023 | MET |
| [GSE217991](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE217991) | Chimeric RNA RRM2-C2orf48 plays an oncogenic role in th… | 6 | 2 | 1 | 2022 | MET |
| [GSE227000](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE227000) | Long-read transcriptome profiling of human lung cancer … | 5 | 2 | 1 | 2023 | MET |
| [GSE237316](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE237316) | CD44+ Lung Cancer Stem Cell-derived Vascular Pericytes … | 4 | 2 | 0 | 2023 | MET |
| [GSE216297](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE216297) | Blood platelet RNA profiles do not enable for nivolumab… | 286 | 1 | 1 | 2023 | — |

---

## Drug Target Landscape

Gene hits across all orphan datasets (mentions in title/abstract):

| Gene | Orphan Dataset Mentions | Approved Drugs |
|------|------------------------|----------------|
| MET | 26 | crizotinib, capmatinib, tepotinib |
| EGFR | 9 | erlotinib, gefitinib, osimertinib |
| RET | 4 | selpercatinib, pralsetinib |
| MYC | 4 | — |
| TP53 | 2 | — |
| KRAS | 1 | adagrasib, sotorasib |
| RB1 | 1 | — |
| CDK4 | 1 | — |

---

## Analysis Pipeline

The following pipeline design is ready for execution once `pydeseq2` is installed.
Install: `pip install pydeseq2 anndata`


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
counts = pd.read_csv("data/geo/GSE[ACCESSION]_counts.tsv", sep="\t", index_col=0)
metadata = pd.read_csv("data/geo/GSE[ACCESSION]_metadata.tsv", sep="\t", index_col=0)

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
actionable.to_csv(f"findings/GSE[ACCESSION]_actionable_degs.tsv", sep="\t")
```

### Interpretation
- Significant DEGs that are druggable targets = highest-priority hits
- Compare to FAERS signals (RS-001): overlap between DEGs and SSRI-adjacent pathways?
- Novel finding = target is up/downregulated + approved drug available + not in major papers


---

## Priority Candidates for Empire Lab Analysis

Top 5 orphan datasets with highest Drug Target Relevance:

### 1. [GSE217646](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE217646) — DTR 6
**Title**: RB1 expression and targeting by CDK4/6 inhibitors in small cell lung cancer
**Samples**: 5 | **Linked publications**: 1
**Target genes mentioned**: TP53, RB1, CDK4
**Drugs mentioned**: see target genes
**Summary excerpt**: The canonical model of small cell lung cancer (SCLC) depicts tumors arising from dual inactivation of TP53 and RB1. However, many genomic studies have persistently identified tumors with no RB1 mutati

### 2. [GSE232569](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE232569) — DTR 5
**Title**: Association of Antifolate Response Signature Status and Clinical Activity of Pemetrexed-Platinum Chemotherapy in Non-Small Cell Lung Cancer - The Piedmont Study
**Samples**: 95 | **Linked publications**: 1
**Target genes mentioned**: MET, RET
**Drugs mentioned**: pemetrexed
**Summary excerpt**: The Piedmont study is a prospectively designed retrospective evaluation of a new 48-gene antifolate response signature (AF-PRS) in patients with locally advanced/metastatic NS-NSCLC treated with pemet

### 3. [GSE232890](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE232890) — DTR 5
**Title**: Relation between TP53 GOF mutation and Osimertinib treatment in EGFR mutant lung cancer
**Samples**: 8 | **Linked publications**: 0
**Target genes mentioned**: TP53, EGFR
**Drugs mentioned**: osimertinib
**Summary excerpt**: Background: Although TP53 gain-of-function (GOF) mutations promote cancer survival, its effect on EGFR-TKI efficacy remains unclear. We established EGFR-mutant lung cancer cell lines expressing variou

### 4. [GSE190704](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE190704) — DTR 4
**Title**: The role of S100A9 in brain metastesis in EGFR-mutant lung cancer
**Samples**: 18 | **Linked publications**: 0
**Target genes mentioned**: MET, EGFR
**Drugs mentioned**: see target genes
**Summary excerpt**: Metastatic relapse from treatment failure has been a formidable challenge to finding a cure for EGFR-mutant lung cancer. Metastasis to the brain is a severe complication for 45% of patients with EGFR-

### 5. [GSE226712](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE226712) — DTR 4
**Title**: Fast proliferating and slowly migrating non-small cell lung cancer cells are vulnerable to decitabine and retinoic acid combinatorial treatment
**Samples**: 18 | **Linked publications**: 1
**Target genes mentioned**: MET, RET
**Drugs mentioned**: see target genes
**Summary excerpt**: Non-small cell lung cancer (NSCLC) patients are often elderly or unfit and thus cannot tolerate standard aggressive therapy regimes. In this study, we test the efficacy of the DNA-hypomethylating agen

---

## Next Steps

- [ ] Download count matrices for top 3 DTR-scored orphan datasets
- [ ] Run DESeq2 pipeline (see Analysis Pipeline section above)
- [ ] Cross-reference DEGs with FAERS signals from RS-001
- [ ] Check if any significant findings are already in ClinicalTrials.gov trials (RS-003 pipeline)
- [ ] Draft RS-002b findings summary for highest-signal dataset

*Generated: 2026-03-15 06:01 | RS-002 pipeline*