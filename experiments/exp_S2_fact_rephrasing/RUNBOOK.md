# S2 / Multi-Seed Runbook

## S2 measurement

From the repo root:

```bash
uv run --with tiktoken python experiments/exp_S2_fact_rephrasing/run.py \
  --source-set wikipedia \
  --limit 30 \
  --out-dir experiments/exp_S2_fact_rephrasing/results/2026-07-16-s2-real-passages
```

For dialogue/transcript passages, use the Federal Reserve press-conference
source set:

```bash
uv run --with pypdf --with tiktoken python experiments/exp_S2_fact_rephrasing/run.py \
  --source-set fed_dialogue \
  --limit 30 \
  --out-dir experiments/exp_S2_fact_rephrasing/results/2026-07-16-s2-dialogue-passages
```

Expected outputs:

- `passages.jsonl`
- `answers.jsonl`
- `scores.csv`
- `summary.json`
- `summary.md`
- `manifest.json`

The manuscript-ready sentence is written at the bottom of `summary.md`.

## B/D multi-seed rerun

From the repo root:

```bash
python3 experiments/exp_BD_fireworks/run_multiseed.py \
  --out-dir experiments/exp_BD_fireworks/results/2026-07-16-multiseed
```

By default this runs five seeds:

```text
20260709 20260710 20260711 20260712 20260713
```

Across these configs:

```text
adversarial_flash.json
adversarial_heavy_qsr.json
cost_flash_qsr_isc.json
cost_flash_qsr_context128.json
cost_pro_qsr_context128_sample.json
```

The aggregate min/mean/max table is written to `summary.md`.
