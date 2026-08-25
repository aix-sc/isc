# ISC Data-Freeze Report, 2026-07-16

This report covers the two July 16 data-freeze asks for the ICAST-ES ISC
fact-compilation manuscript: S2 fact-rephrasing measurement and B/D multi-seed
reruns.

## 1. S2 Fact Rephrasing

Artifact directories:

```text
experiments/exp_S2_fact_rephrasing/results/2026-07-16-s2-real-passages/
experiments/exp_S2_fact_rephrasing/results/2026-07-16-s2-dialogue-passages-valid/
```

Dense-prose setup:

- Passage set: 30 public Wikipedia passages, snapshotted in `passages.jsonl`
- Model: `accounts/fireworks/models/deepseek-v4-flash`
- Token counter: `tiktoken:cl100k_base`
- Outputs: `passages.jsonl`, `answers.jsonl`, `scores.csv`, `summary.json`, `summary.md`

Dense-prose results:

| Metric | Value |
| :-- | --: |
| Original passage tokens | 3,748 |
| S2 fact tokens | 3,854 |
| Token ratio | 1.0283x |
| Generated facts | 223 |
| Source-entailed fact rate | 100.0% |
| QA-fidelity pass rate | 96.7% |
| Missing major claims | 0 |

Dialogue/transcript setup:

- Passage set: 25 valid Federal Reserve press-conference Q&A excerpts from 30
  attempted passages; 5 malformed model completions were excluded
- Model: `accounts/fireworks/models/deepseek-v4-flash`
- Token counter: `tiktoken:cl100k_base`

Dialogue/transcript results:

| Metric | Value |
| :-- | --: |
| Original passage tokens | 6,789 |
| S2 fact tokens | 3,310 |
| Token ratio | 0.4876x |
| Generated facts | 165 |
| Source-entailed fact rate | 97.6% |
| QA-fidelity pass rate | 92.0% |
| Missing major claims | 1 |

Interpretation:

S2 preserved source fidelity on the dense Wikipedia set, but did not compress
that source because the prose was already concise. On verbose dialogue with
pronouns, filler, and back-references, S2 reduced token count by 51.2% while
retaining high judged fidelity. A safe wording is:

> On 25 Federal Reserve press-conference dialogue excerpts, S2 reduced token
> count to 0.49x of the original passage text using `tiktoken:cl100k_base`, with
> 97.6% of generated facts judged source-entailed and 92.0% passage-level QA-fidelity
> pass rate.

## 2. B/D Multi-Seed Reruns

Artifact directory:

```text
experiments/exp_BD_fireworks/results/2026-07-16-multiseed/
```

Seeds:

```text
20260709 20260710 20260711 20260712 20260713
```

Results are reported as min / mean / max across seeds.

| Condition | Exact Rate | Cost/q ($) | Tokens/q |
| :-- | --: | --: | --: |
| Adversarial Flash + QSR | 0.0000 / 0.0333 / 0.1667 | 0.00130657 / 0.00130785 / 0.00130916 | 8308.7 / 8318.3 / 8327.2 |
| Adversarial Flash + ISC | 1.0000 / 1.0000 / 1.0000 | 0.00009387 / 0.00010145 / 0.00010843 | 436.2 / 463.2 / 488.2 |
| Adversarial Kimi QSR | 0.0000 / 0.0667 / 0.3333 | 0.01074502 / 0.01086006 / 0.01090465 | 8135.3 / 8166.5 / 8191.0 |
| Adversarial GLM QSR | 0.6667 / 0.7333 / 1.0000 | 0.01368167 / 0.01388991 / 0.01437340 | 8108.3 / 8162.9 / 8266.0 |
| Cost Flash QSR, 128 rows | 1.0000 / 1.0000 / 1.0000 | 0.00140958 / 0.00142094 / 0.00143428 | 9737.8 / 9777.2 / 9822.3 |
| Cost Flash ISC | 1.0000 / 1.0000 / 1.0000 | 0.00009490 / 0.00009998 / 0.00010561 | 434.9 / 453.3 / 473.4 |
| Cost Pro QSR, 128 rows | 1.0000 / 1.0000 / 1.0000 | 0.01821693 / 0.01850612 / 0.01891206 | 9935.5 / 10018.3 / 10134.0 |

Mean-cost ratios:

- Adversarial Flash QSR / Flash ISC: 12.89x
- Cost Flash QSR 128 / Flash ISC: 14.21x
- Cost Pro QSR 128 / Flash ISC: 185.10x

Interpretation:

The main failure-asymmetry claim is robust: Flash QSR remains unreliable on
adversarial governance reconstruction, while Flash ISC is exact on every seed.
On simple revision tasks, all compared paths remain exact, but QSR pays a large
recurring cost and token premium. The heavier-model claim should be softened:
GLM QSR ranged from 2/3 to 3/3 exact across seeds, not uniformly 3/3.

## Manuscript Edits Implied

- Replace the S2 "roughly 30% token compression" claim with the measured
  dialogue result above, and qualify that compression depends on source style.
- Add min/max ranges for B/D tables or mention the five-seed rerun in the
  limitations/results text.
- Change the GLM language from "solved the QSR condition" to "partially to fully
  solved the QSR sample across seeds."
