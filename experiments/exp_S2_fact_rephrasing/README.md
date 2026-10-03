# Experiment S2 Fact Rephrasing

This experiment measures the S2 fact-rephrasing step from the ingest-time fact
compilation pipeline on real passage sets.

It records:

- source passages snapshotted from public Wikipedia pages or public Federal
  Reserve press-conference transcripts
- atomic facts produced by the S2 rephrasing prompt
- token compression from source passage to generated facts
- model-judged source fidelity for generated facts

By default the script calls the exe.dev `fireworks` integration
(`https://fireworks.int.exe.xyz/inference/v1`), which injects the key, so no
key is needed on the VM. Off exe.dev, set
`FIREWORKS_BASE_URL=https://api.fireworks.ai/inference/v1` and provide
`FIREWORKS_API_KEY` (or `LLM_GATEWAY_DEFAULT_FIREWORKS_API_KEY`, or `--op-ref`).

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
