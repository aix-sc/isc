# Data Freeze Summary, 2026-07-16

This file summarizes the July 2026 data-freeze artifacts for the ICAST-ES ISC
fact-compilation paper.

## S2 Fact Rephrasing

Artifact directory:

```text
experiments/exp_S2_fact_rephrasing/results/2026-07-16-s2-real-passages/
```

Passage set: 30 public Wikipedia passages snapshotted in `passages.jsonl`.

Model: `accounts/fireworks/models/deepseek-v4-flash`.

Token counter: `tiktoken:cl100k_base`.

Key result:

- Original tokens: 3,748
- S2 fact tokens: 3,854
- Overall token ratio: 1.0283x
- Generated facts: 223
- Source-entailed fact rate: 100.0%
- Passage-level QA-fidelity pass rate: 96.7%
- Missing major claims: 0

Manuscript-safe wording:

> On 30 public Wikipedia passages, S2 fact rephrasing produced 1.03x as many
> tokens as the original passage text using `tiktoken:cl100k_base`, with 100.0%
> of generated facts judged source-entailed and 96.7% passage-level QA-fidelity
> pass rate.

Interpretation: this run supports S2 fidelity, but it does not support the
draft's "roughly 30% token compression" design-value claim on this real passage
set. The paper should either remove the compression claim or frame compression
as future optimization.

## B/D Multi-Seed Rerun

Artifact directory:

```text
experiments/exp_BD_fireworks/results/2026-07-16-multiseed/
```

Seeds:

```text
20260709 20260710 20260711 20260712 20260713
```

Key min/mean/max results:

| Condition | Exact rate | Cost/q ($) | Tokens/q |
| :-- | --: | --: | --: |
| Adversarial Flash + QSR | 0.0000 / 0.0333 / 0.1667 | 0.00130657 / 0.00130785 / 0.00130916 | 8308.7 / 8318.3 / 8327.2 |
| Adversarial Flash + ISC | 1.0000 / 1.0000 / 1.0000 | 0.00009387 / 0.00010145 / 0.00010843 | 436.2 / 463.2 / 488.2 |
| Adversarial Kimi QSR | 0.0000 / 0.0667 / 0.3333 | 0.01074502 / 0.01086006 / 0.01090465 | 8135.3 / 8166.5 / 8191.0 |
| Adversarial GLM QSR | 0.6667 / 0.7333 / 1.0000 | 0.01368167 / 0.01388991 / 0.01437340 | 8108.3 / 8162.9 / 8266.0 |
| Cost Flash QSR, 128 rows | 1.0000 / 1.0000 / 1.0000 | 0.00140958 / 0.00142094 / 0.00143428 | 9737.8 / 9777.2 / 9822.3 |
| Cost Flash ISC | 1.0000 / 1.0000 / 1.0000 | 0.00009490 / 0.00009998 / 0.00010561 | 434.9 / 453.3 / 473.4 |
| Cost Pro QSR, 128 rows | 1.0000 / 1.0000 / 1.0000 | 0.01821693 / 0.01850612 / 0.01891206 | 9935.5 / 10018.3 / 10134.0 |

Derived ratios from mean cost:

- Adversarial Flash QSR / Flash ISC: 12.89x
- Cost Flash QSR 128 / Flash ISC: 14.21x
- Cost Pro QSR 128 / Flash ISC: 185.10x

Manuscript-safe wording:

> Across five seeds, DeepSeek V4 Flash under QSR achieved 0.0%-16.7% exact
> answer+source+revision accuracy on adversarial governance questions, while the
> same model reading the compiled ISC row achieved 100% on every seed. On simple
> revision tasks, Flash QSR, Flash ISC, and Pro QSR all remained exact across all
> seeds, but mean per-question cost was 14.21x higher for Flash QSR at 128
> context rows and 185.10x higher for Pro QSR than for Flash ISC.

Interpretation: the main failure-asymmetry claim is robust for Flash QSR vs.
Flash ISC. The heavier-model spot check should be softened: GLM QSR ranged from
2/3 to 3/3 exact across seeds, not uniformly 3/3.
