# ICAST Camera-Ready Evidence, 2026-08-20

This note closes the three camera-ready evidence/release tasks tracked in
issues #7–#9. Reproduce the numeric results with:

## Final submission receipt (reported 2026-08-29)

Yusuke confirmed that the iCAST-ES camera-ready is **submitted and final**:
PDF eXpress approved it, and EDAS now contains the final file. The work was
finished two days before the September 1 deadline.

- The abstract again says: “open source, MIT-licensed implementation and
  experimental artifacts.”
- The authoritative LaTeX source and submitted PDF are in
  [`paper/icast2026-camera-ready/`](../paper/icast2026-camera-ready/). Tables
  and Fig. 1 were retypeset to sit at column tops, and one malformed quote
  character was corrected across the references.
- No reported numerical result changed.
- Yusuke plans to post the accepted version, with the IEEE copyright notice,
  to arXiv under `cs.AI` in the next day or two. This is planned, not yet
  recorded as uploaded.

After Kyle returns from Burning Man, the remaining conference preparation is
presenter registration and slides. Prior iCAST programs suggest a working
format of a 10-minute talk plus 5 minutes for Q&A; confirm the assigned format
when the conference provides it.


```sh
uv run --with tiktoken python experiments/camera_ready_analysis.py
```

## Issue #7: S2 ingest cost per fact

The committed S2 runner did not persist the Fireworks API `usage` object. The
costs below are therefore reconstructed from the exact frozen prompt content
and exact frozen completion content using the tokenizer named in the frozen
study (`tiktoken:cl100k_base`). The calculation includes only the rephrasing
call, not the separate fidelity-judge call, because the requested quantity is
S2 ingest/rephrasing cost.

The frozen price schedule for `deepseek-v4-flash` is USD 0.14 per million input
tokens and USD 0.28 per million output tokens, as recorded in
[`exp_BD_fireworks/run.py`](exp_BD_fireworks/run.py) and corroborated by the
[Fireworks model listing](https://fireworks.ai/models/fireworks/deepseek-v4-flash).

| Passage set | Passages | Facts | Prompt-content tokens | Completion tokens | Total reconstructed cost | Cost/fact | Manuscript value (5 decimals) |
| :-- | --: | --: | --: | --: | --: | --: | --: |
| Dialogue | 25 | 165 | 12,514 | 9,653 | USD 0.00445480 | USD 0.0000269988 | **USD 0.00003/fact** |
| Prose | 30 | 223 | 8,491 | 4,197 | USD 0.00236390 | USD 0.0000106004 | **USD 0.00001/fact** |

Chat-template wrapper tokens were not retained by the frozen runner and are
not included. At the requested five-decimal precision, the small wrapper
overhead cannot change either reported value.

Manuscript-ready sentence:

> At the frozen DeepSeek V4 Flash price schedule, reconstructed S2 rephrasing
> cost was USD 0.00003 per fact for dialogue and USD 0.00001 per fact for
> prose.

## Issue #8: adversarial QSR failure breakdown

The frozen five-seed DeepSeek V4 Flash run contains 30 adversarial QSR rows:
one exact success and 29 failures. Inspecting the saved result fields gives:

| Reviewer-requested category | Count |
| :-- | --: |
| Correct value, but wrong source and/or revision | **0** |
| Value not found at all | **29** |

All 29 failed rows have `model_value`, `model_source`, and `model_revision` set
to null because the model never produced a parseable final answer before the
completion limit. Five deletion questions have `answer_correct: true` in the
legacy rows because `score()` treats a null value in its parse-error sentinel
as a valid deleted/unknown answer. That mechanical flag must not be interpreted
as a produced correct value: the raw result contains no value or citation, so
all five belong in “value not found at all.”

The source artifacts are the five
[`adversarial_flash_seed_*_answers.jsonl`](exp_BD_fireworks/results/2026-07-16-multiseed/)
files.

## Issue #9: public-release audit

The repository was verified public on 2026-08-20. Before confirming the
release gate:

- Gitleaks v8.30.1 scanned the complete Git history: 30 commits and about
  3.07 MB, with **no leaks found**.
- The only tracked environment file is
  [`packages/web/.env.example`](../packages/web/.env.example), containing
  placeholder Firebase values. Real `.env`, `.firebaserc`, and local settings
  are ignored.
- The B/D fixtures and result snapshots are deterministically generated
  synthetic `project_*`, `hard_project_*`, and `adversarial_project_*` records.
- S2 prose passages are public Wikipedia excerpts; S2 dialogue passages are
  public Federal Reserve press-conference excerpts. No client/customer dataset
  is present in the tracked snapshots.
- The release tag `data-freeze-2026-07-16` identifies freeze commit `9cca7ef`.

Result: no history rewrite or artifact removal is required before public use.
