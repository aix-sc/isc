"""
Run and aggregate multi-seed B/D Fireworks experiments.

This wrapper executes the existing run.py harness for a list of configs and
seeds, writes one artifact set per config/seed, and produces min/mean/max
summaries by model/mode.
"""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from statistics import mean
from typing import Any


DEFAULT_CONFIGS = [
    "experiments/exp_BD_fireworks/configs/adversarial_flash.json",
    "experiments/exp_BD_fireworks/configs/adversarial_heavy_qsr.json",
    "experiments/exp_BD_fireworks/configs/cost_flash_qsr_isc.json",
    "experiments/exp_BD_fireworks/configs/cost_flash_qsr_context128.json",
    "experiments/exp_BD_fireworks/configs/cost_pro_qsr_context128_sample.json",
]

DEFAULT_SEEDS = [20260709, 20260710, 20260711, 20260712, 20260713]


def slug_for_config(config_path: Path) -> str:
    return config_path.stem


def run_one(
    root: Path,
    config_path: Path,
    seed: int,
    out_dir: Path,
    dry_run: bool,
) -> None:
    slug = slug_for_config(config_path)
    prefix = out_dir / f"{slug}_seed_{seed}"
    cmd = [
        sys.executable,
        "experiments/exp_BD_fireworks/run.py",
        "--config",
        str(config_path),
        "--seed",
        str(seed),
        "--csv-out",
        str(prefix.with_name(prefix.name + "_scores.csv")),
        "--jsonl-out",
        str(prefix.with_name(prefix.name + "_answers.jsonl")),
        "--summary-out",
        str(prefix.with_name(prefix.name + "_summary.json")),
    ]
    if dry_run:
        print(" ".join(cmd))
        return
    subprocess.run(cmd, cwd=root, check=True)


def read_scores(path: Path) -> list[dict[str, Any]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def exact(row: dict[str, Any]) -> bool:
    return (
        str(row.get("answer_correct")).lower() == "true"
        and str(row.get("source_correct")).lower() == "true"
        and str(row.get("revision_correct")).lower() == "true"
    )


def summarize_scores(out_dir: Path) -> dict[str, Any]:
    cells: dict[tuple[str, str, str], list[dict[str, Any]]] = {}
    for path in sorted(out_dir.glob("*_scores.csv")):
        stem = path.name.removesuffix("_scores.csv")
        if "_seed_" not in stem:
            continue
        config_slug, seed_text = stem.rsplit("_seed_", 1)
        seed = int(seed_text)
        for row in read_scores(path):
            key = (config_slug, str(row["model_name"]), str(row["mode"]))
            cells.setdefault(key, []).append({**row, "seed": seed})

    summary_cells: dict[str, dict[str, Any]] = {}
    for (config_slug, model_name, mode), rows in cells.items():
        by_seed: dict[int, list[dict[str, Any]]] = {}
        for row in rows:
            by_seed.setdefault(int(row["seed"]), []).append(row)

        seed_metrics = []
        for seed, seed_rows in sorted(by_seed.items()):
            questions = len(seed_rows)
            exact_count = sum(1 for row in seed_rows if exact(row))
            cost = sum(float(row.get("estimated_cost_usd") or 0.0) for row in seed_rows)
            tokens = sum(int(float(row.get("total_tokens") or 0)) for row in seed_rows)
            latency = mean(float(row.get("latency_ms") or 0.0) for row in seed_rows)
            seed_metrics.append(
                {
                    "seed": seed,
                    "questions": questions,
                    "exact_count": exact_count,
                    "exact_rate": exact_count / questions if questions else 0.0,
                    "cost_per_question": cost / questions if questions else 0.0,
                    "tokens_per_question": tokens / questions if questions else 0.0,
                    "latency_ms": latency,
                }
            )

        def stat(field: str) -> dict[str, float]:
            values = [float(metric[field]) for metric in seed_metrics]
            return {
                "min": round(min(values), 8),
                "mean": round(mean(values), 8),
                "max": round(max(values), 8),
            }

        cell_key = f"{config_slug}/{model_name}/{mode}"
        summary_cells[cell_key] = {
            "seeds": [metric["seed"] for metric in seed_metrics],
            "per_seed": seed_metrics,
            "exact_rate": stat("exact_rate"),
            "cost_per_question": stat("cost_per_question"),
            "tokens_per_question": stat("tokens_per_question"),
            "latency_ms": stat("latency_ms"),
        }

    return {
        "date": datetime.now(UTC).date().isoformat(),
        "cells": summary_cells,
    }


def write_markdown(summary: dict[str, Any], path: Path) -> None:
    lines = [
        "# B/D Multi-Seed Summary",
        "",
        "| Config / model / mode | Seeds | Exact rate min-mean-max | Cost/q min-mean-max | Tokens/q min-mean-max | Latency ms min-mean-max |",
        "| :-- | --: | --: | --: | --: | --: |",
    ]
    for key, cell in summary["cells"].items():
        exact_rate = cell["exact_rate"]
        cost = cell["cost_per_question"]
        tokens = cell["tokens_per_question"]
        latency = cell["latency_ms"]
        lines.append(
            "| "
            + " | ".join(
                [
                    key,
                    str(len(cell["seeds"])),
                    f"{exact_rate['min']:.4f}-{exact_rate['mean']:.4f}-{exact_rate['max']:.4f}",
                    f"{cost['min']:.8f}-{cost['mean']:.8f}-{cost['max']:.8f}",
                    f"{tokens['min']:.1f}-{tokens['mean']:.1f}-{tokens['max']:.1f}",
                    f"{latency['min']:.1f}-{latency['mean']:.1f}-{latency['max']:.1f}",
                ]
            )
            + " |"
        )
    path.write_text("\n".join(lines) + "\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run B/D configs across multiple seeds.")
    parser.add_argument("--seeds", nargs="+", type=int, default=DEFAULT_SEEDS)
    parser.add_argument("--configs", nargs="+", type=Path, default=[Path(p) for p in DEFAULT_CONFIGS])
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("experiments/exp_BD_fireworks/results/2026-07-16-multiseed"),
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--aggregate-only", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path.cwd()
    args.out_dir.mkdir(parents=True, exist_ok=True)

    if not args.aggregate_only:
        for config_path in args.configs:
            for seed in args.seeds:
                print(f"running {config_path} seed={seed}", flush=True)
                run_one(root, config_path, seed, args.out_dir, args.dry_run)

    if args.dry_run:
        return 0

    summary = summarize_scores(args.out_dir)
    (args.out_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    write_markdown(summary, args.out_dir / "summary.md")
    manifest = {
        "experiment": "B/D Fireworks multi-seed rerun",
        "command": " ".join(sys.argv),
        "configs": [str(path) for path in args.configs],
        "seeds": args.seeds,
        "outputs": ["*_scores.csv", "*_answers.jsonl", "*_summary.json", "summary.json", "summary.md"],
    }
    (args.out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
