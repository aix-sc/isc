# Experiment B/D Fireworks Adversarial Superiority Summary

This run adds an adversarial governance-reconstruction question set. The same
underlying information is present in the QSR context, but it is noisy and must be
resolved at query time:

- ignore drafts, proposals, rejected rows, sandbox rows, and future-dated rows
- apply cross-row revocations
- prefer owner/regulatory sources over imported rows
- apply effective tombstones
- cite the exact value/tombstone source and revision

ISC mode receives the compiled substrate row after those rules have already been
applied.

## Flash gap

| Condition | Questions | Exact answer+source+revision | Cost / question | Mean latency |
| --- | ---: | ---: | ---: | ---: |
| DeepSeek V4 Flash + QSR | 6 | 0/6 | $0.00130755 | 11.07 s |
| DeepSeek V4 Flash + ISC | 6 | 6/6 | $0.00009877 | 3.29 s |

On these adversarial governance questions, Flash could not reliably perform QSR,
but it could answer from the compiled ISC substrate. ISC was also 13.24x cheaper
per question and 3.36x faster.

## Heavier-model QSR spot check

| Condition | Questions | Exact answer+source+revision | Cost / question | Mean latency |
| --- | ---: | ---: | ---: | ---: |
| Kimi K2.7 Code + QSR | 3 | 0/3 | $0.01087203 | 9.13 s |
| GLM 5.2 + QSR | 3 | 3/3 | $0.01358027 | 10.50 s |

GLM 5.2 handled the adversarial QSR sample; Kimi K2.7 Code did not on this run.
Relative to Flash + ISC, GLM 5.2 + QSR cost 137.49x more per question.

## Claim supported

The supported claim is narrow and defensible: for governance-heavy corpus state
reconstruction, a cheap model can answer accurately from ISC's compiled substrate
but fails when asked to reconstruct the same state from noisy QSR context. A
heavier model (GLM 5.2) can solve the QSR version, but at much higher cost.

This is still a synthetic harness. The next step is to reproduce the same pattern
on a real revision stream with equivalent governance rules.
