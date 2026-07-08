# Experiment B/D Fireworks Harness

This directory contains the reproducible harness for the ISC Experiment B/D
Fireworks runs.

The experiment compares:

- **QSR**: query-time semantic reconstruction from noisy retrieved context.
- **ISC**: answering from an ingest-time compiled substrate row whose corpus
  state, deletion status, and provenance have already been resolved.

## Credentials

The runner resolves Fireworks credentials in this order:

1. `FIREWORKS_API_KEY`
2. `LLM_GATEWAY_DEFAULT_FIREWORKS_API_KEY`
3. Optional: `op read <value passed via --op-ref>`

If you use 1Password, pass your own secret reference with `--op-ref`. No
repository-specific 1Password item is required.

## Re-run Key Results

From the repository root:

```bash
uv run python experiments/exp_BD_fireworks/run.py \
  --config experiments/exp_BD_fireworks/configs/adversarial_flash.json
```

```bash
uv run python experiments/exp_BD_fireworks/run.py \
  --config experiments/exp_BD_fireworks/configs/adversarial_heavy_qsr.json
```

```bash
uv run python experiments/exp_BD_fireworks/run.py \
  --config experiments/exp_BD_fireworks/configs/cost_flash_qsr_isc.json
```

## Result Snapshots

- `results/2026-07-08-adversarial-flash/`
  - Flash fails adversarial QSR exact answer+source+revision, but succeeds with ISC.
- `results/2026-07-08-adversarial-heavy-qsr-sample/`
  - GLM 5.2 succeeds on adversarial QSR sample; Kimi K2.7 Code does not in this run.
- `results/2026-07-08-cost-sweep/`
  - Flash QSR and Flash ISC both answer simple revision tasks, but QSR pays a large token/cost tax.

## Notes

This is a synthetic governance/revision harness. It is appropriate for isolating
failure modes and cost mechanics, not for claiming external validity on real
corpora. The next step is to run the same protocol on a real revision stream with
equivalent governance rules.
