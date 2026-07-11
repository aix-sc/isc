# Experiment S2 Fact Rephrasing

This experiment measures the S2 fact-rephrasing step from the ingest-time fact
compilation pipeline on real passage sets.

It records:

- source passages snapshotted from public Wikipedia pages or public Federal
  Reserve press-conference transcripts
- atomic facts produced by the S2 rephrasing prompt
- token compression from source passage to generated facts
- model-judged source fidelity for generated facts

The script reads Fireworks credentials from `FIREWORKS_API_KEY`.

Example:

```bash
uv run --with tiktoken python experiments/exp_S2_fact_rephrasing/run.py \
  --source-set wikipedia \
  --limit 30 \
  --out-dir experiments/exp_S2_fact_rephrasing/results/2026-07-16-s2-real-passages
```

Dialogue/transcript corpus:

```bash
uv run --with pypdf --with tiktoken python experiments/exp_S2_fact_rephrasing/run.py \
  --source-set fed_dialogue \
  --limit 30 \
  --out-dir experiments/exp_S2_fact_rephrasing/results/2026-07-16-s2-dialogue-passages
```
