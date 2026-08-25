# Experiment B/D Fireworks Cost Superiority Summary

This sweep compares query-time semantic reconstruction (QSR) against ingest-time
semantic compilation (ISC) on the same synthetic revision corpus. The questions
are balanced across corrected facts, deletion tombstones, and ordinary current
facts.

## Strongest result so far

DeepSeek V4 Flash in ISC mode and DeepSeek V4 Pro in QSR mode both answered the
sampled questions correctly, but the expensive QSR path was much more costly.

| Condition | Questions | Accuracy | Cost / question | Tokens / question | Mean latency |
| --- | ---: | ---: | ---: | ---: | ---: |
| DeepSeek V4 Flash + ISC | 9 | 9/9 | $0.00009848 | 448.1 | 4.78 s |
| DeepSeek V4 Flash + QSR, 128 context docs | 9 | 9/9 | $0.00141454 | 9,754.2 | 7.36 s |
| DeepSeek V4 Pro + QSR, 128 context docs | 2 | 2/2 | $0.01850403 | 10,014.5 | 33.87 s |

Relative to Flash + ISC, Flash + QSR at 128 context docs cost 14.36x more per
question and used 21.77x more tokens. DeepSeek V4 Pro + QSR cost 187.89x more
per question and was 7.09x slower on the sampled overloaded prompts.

## Interpretation

This does not yet show an accuracy advantage for ISC on these simple revision
rules. It shows a cost and latency advantage: when the current state and
provenance are compiled once, a cheap model can perform the answer/citation task
with a small prompt. QSR can also solve the task, but it repeatedly pays to scan
large noisy contexts and becomes much more expensive as context grows.

The next harder test should increase reconstruction difficulty rather than just
context size: multi-hop updates, conflicting current flags, source trust rules,
and access-control/deletion policies.
