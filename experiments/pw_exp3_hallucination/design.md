# Prompt Whisperers — Experiment 3 Design: Hallucination Characterization
*Empire Lab | Research note RS-004 | Designed: 2026-03-15*

---

## Hypothesis

**Different model architectures and sizes hallucinate different *categories* of information.**

Specifically: a smaller model (3B params) does not simply "hallucinate more" than a larger model
(7B, 14B). It hallucinates in *structurally different ways* — some categories worse, some better.
If this is true, task routing by hallucination type (not just model capability rank) can extract
better total performance from a fleet than routing by raw quality score alone.

This is the Empire Lab practical question: when routing tasks across Emperor/Willy fleet, which
model is *least wrong* for each task category — not just "which is best overall."

---

## Research Context

### What Exp 1 + 2 established

**Exp 1 (LLM Judge Stability)**: Judge rankings are highly unstable (mean Spearman ρ=0.22).
All 26 judge-variant pairs were UNSTABLE. This means LLM-as-judge evaluation is unreliable
as a measurement tool for subtle quality differences.

**Exp 2 (Model Substitution ROI)**: INCONCLUSIVE — optimized prompts for a weak model
(qwen2.5:3b) showed minimal measurable advantage over basic prompts on the strong model
(llama3.1). Confounded by the Exp 1 finding: judges can't reliably rank the outputs.

**Implication for Exp 3**: Cannot use LLM-as-judge for hallucination scoring. Must use
*ground-truth verifiable* questions where correctness is objectively assessable.

### Why hallucination characterization, not more quality scoring

Quality scoring is subjective → corrupted by judge instability (Exp 1).
Factual accuracy scoring is objective → countable correct/incorrect against a known answer set.
This is the right measurement tool for this fleet-routing question.

---

## Design

### Models Under Test

| ID | Model | Size | Typical role |
|----|-------|------|--------------|
| M1 | qwen2.5:3b | ~2GB | Fast/cheap — Billy crons |
| M2 | phi4-mini | ~2.5GB | Billy extraction, RSS |
| M3 | qwen2.5:7b | ~4.5GB | Billy quality ops, lesson scraper |

*(When Willy arrives: add mistral-nemo:12b and gemma3:12b as M4/M5)*

### Hallucination Categories (7 types)

| Category | Code | Example | Why it matters |
|----------|------|---------|----------------|
| Factual-static | FS | "What year was X founded?" | Knowledge base accuracy |
| Factual-temporal | FT | "What was the last result of Y?" | Training cutoff awareness |
| Attribution | AT | "Who wrote/said Z?" | Source reliability |
| Numerical | NM | "What is the population of W?" | Quantitative reasoning |
| Procedural | PR | "What are the steps for V?" | Instruction following |
| Causal | CA | "Why does X cause Y?" | Reasoning/confabulation |
| Self-knowledge | SK | "What can you do / what's your training cutoff?" | Meta-accuracy |

### Question Battery

- **N = 20 questions per category** = 140 total questions
- **Scoring**: Binary (correct/incorrect) + optionally partial credit for near-misses
- **Answer key**: Pre-verified against authoritative sources (Wikipedia, NCBI, official docs)
- **Format**: Short-answer (5-15 words max expected output) to enable consistent scoring

### Conditions

Each question is presented to each model under 3 prompting conditions:
1. **Bare**: Just the question, no context or framing
2. **Calibrated**: "Answer only if you are confident. Say 'I don't know' if uncertain."
3. **Chain-of-thought**: "Think step by step before answering."

Total runs = 140 questions × 3 models × 3 conditions = **1,260 inference calls**
At ~0.5s per inference on qwen2.5:3b → ~10 minutes total on existing hardware.

### Scoring

```python
# Binary scoring per response
correct = 1.0
near_miss = 0.5    # semantically correct but phrasing differs
incorrect = 0.0
refused = None     # "I don't know" — not penalized, tracked separately

# Per model, per category:
accuracy_rate = sum(scores) / len(valid_scores)  # excludes refused

# Key secondary metric: Calibration Rate
# How often does the model refuse ("I don't know") when it would have been wrong?
# High calibration = model knows what it doesn't know
calibration_rate = correct_refusals / total_refusals_for_wrong_questions
```

### Key Metrics

| Metric | Definition |
|--------|------------|
| Category accuracy | % correct per model per category |
| Calibration rate | % of "I don't know" responses that would have been wrong |
| Hallucination gap | (M3_accuracy - M1_accuracy) per category — is the gap uniform? |
| Best-model-by-category | Which model wins each category? |
| Prompted calibration lift | Delta in refusal rate: bare → calibrated condition |

---

## Expected Findings

**Hypothesis A (routing-relevant)**: The hallucination gap is NOT uniform across categories.
Smaller models may match larger models on procedural or self-knowledge tasks while showing
large gaps on factual-temporal or attribution tasks.

**Hypothesis B (calibration)**: The "I don't know" instruction significantly increases
calibration on smaller models. If true: routing + calibration prompts can compensate for
model size on some categories.

**Hypothesis C (category blind spots)**: Each model has a category where it hallucinates
at rates higher than its overall mean. This is actionable for fleet routing.

---

## Output Files

```
experiments/pw_exp3_hallucination/
  design.md                          ← this file (RS-004 design)
  config.py                          ← question battery, models, scoring functions
  questions/
    fs_factual_static.json           ← 20 questions + answer keys
    ft_factual_temporal.json
    at_attribution.json
    nm_numerical.json
    pr_procedural.json
    ca_causal.json
    sk_self_knowledge.json
  01_run_battery.py                  ← send all 1260 queries to Ollama
  02_score_responses.py              ← binary scoring against answer keys
  03_analyze_results.py              ← accuracy by model × category, charts
  data/
    responses.json                   ← all model outputs
    scores.json                      ← binary scores
    results.json                     ← accuracy matrices
    report.md                        ← findings + routing recommendations
  findings/
    rs004_hallucination_characterization_[date].md  ← Empire Lab findings doc
```

---

## Execution Plan

### Phase 1: Question Battery Construction (1-2h, Empire Lab session)
1. Write 20 questions per category with verified answer keys
2. Include answer variants (e.g., "1776" and "seventeen seventy-six" both correct)
3. Include `difficulty: [easy/medium/hard]` per question for stratified analysis

### Phase 2: Run Battery (automated, Willy-native when available)
1. Verify all 3 models are loaded in Ollama
2. Run `01_run_battery.py` — ~10-15 min wall time
3. Human spot-check 10 random responses for scoring calibration

### Phase 3: Score + Analyze (automated)
1. Run `02_score_responses.py` with answer keys
2. Run `03_analyze_results.py` — produces accuracy matrix + routing recommendations

---

## Routing Application (Output Format)

The final deliverable is a **routing recommendation table** for the Empire fleet:

```
For this task type → use this model
  Factual-static: M3 (qwen2.5:7b) with calibrated prompt
  Numerical: M2 (phi4-mini) — comparable to M3, faster
  Procedural: M1 (qwen2.5:3b) + CoT — matches M3 accuracy
  ...
```

This feeds directly into the Emperor/Willy routing protocol
(`G:/ai/automation/tasks/willy_routing_protocol.md`).

---

## Publication Potential

Combined with Exp 1 (judge instability) and Exp 2 (substitution ROI), Exp 3 completes a
3-experiment arc on **local LLM fleet optimization**:

> *"We show that: (1) LLM-as-judge rankings are unreliable, (2) prompt engineering cannot
> fully compensate for model size, but (3) routing by hallucination type — rather than
> overall quality rank — extracts significantly better total fleet performance."*

Target: arXiv preprint → Machine Learning for Systems workshop at NeurIPS or ICLR.
Practical contribution: fleet routing algorithm + open question battery as benchmark.

---

## Dependencies

- Ollama running with qwen2.5:3b, phi4-mini, qwen2.5:7b loaded
- Python 3.8+, requests (no ML libraries required)
- ~30 min compute time on existing hardware
- Willy optional (speeds up batch inference when available)

---

## Status

- [x] Design complete (RS-004, 2026-03-15)
- [ ] Question battery: 140 questions × 7 categories (Phase 1 — ~1h)
- [ ] Runner script: 01_run_battery.py
- [ ] Scoring script: 02_score_responses.py
- [ ] Analysis script: 03_analyze_results.py
- [ ] Execution (after question battery complete — Willy-native preferred)

*Next action: write question battery (fs_factual_static.json first — easiest to verify)*
