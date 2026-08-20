#!/usr/bin/env python3
"""Reproduce the ICAST camera-ready S2 cost and QSR failure counts."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

import tiktoken


ROOT = Path(__file__).resolve().parent
S2_ROOT = ROOT / "exp_S2_fact_rephrasing"
MULTISEED_ROOT = ROOT / "exp_BD_fireworks" / "results" / "2026-07-16-multiseed"
INPUT_PRICE_PER_MILLION = 0.14
OUTPUT_PRICE_PER_MILLION = 0.28


def load_s2_runner() -> Any:
    path = S2_ROOT / "run.py"
    spec = importlib.util.spec_from_file_location("camera_ready_s2_runner", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text().splitlines() if line]


def s2_costs() -> list[dict[str, Any]]:
    runner = load_s2_runner()
    encoding = tiktoken.get_encoding("cl100k_base")
    sets = (
        (
            "dialogue",
            "fed_dialogue",
            S2_ROOT / "results" / "2026-07-16-s2-dialogue-passages-valid",
        ),
        (
            "prose",
            "wikipedia",
            S2_ROOT / "results" / "2026-07-16-s2-real-passages",
        ),
    )
    results: list[dict[str, Any]] = []
    for label, source_set, directory in sets:
        passages = {
            row["passage_id"]: runner.Passage(**row)
            for row in read_jsonl(directory / "passages.jsonl")
        }
        rows = read_jsonl(directory / "answers.jsonl")
        prompt_tokens = 0
        completion_tokens = 0
        facts = 0
        for row in rows:
            messages = runner.rephrase_messages(passages[row["passage_id"]], source_set)
            prompt_tokens += sum(
                len(encoding.encode(message["content"])) for message in messages
            )
            completion_tokens += len(encoding.encode(row["rephrase_raw_content"]))
            facts += int(row["fact_count"])
        total_cost = (
            prompt_tokens * INPUT_PRICE_PER_MILLION
            + completion_tokens * OUTPUT_PRICE_PER_MILLION
        ) / 1_000_000
        results.append(
            {
                "set": label,
                "passages": len(rows),
                "facts": facts,
                "prompt_content_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": prompt_tokens + completion_tokens,
                "total_cost_usd": round(total_cost, 8),
                "cost_per_fact_usd": round(total_cost / facts, 10),
                "manuscript_cost_per_fact_usd": f"{total_cost / facts:.5f}",
            }
        )
    return results


def qsr_failures() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for path in sorted(MULTISEED_ROOT.glob("adversarial_flash_seed_*_answers.jsonl")):
        rows.extend(row for row in read_jsonl(path) if row["mode"] == "qsr")
    failed = [
        row
        for row in rows
        if not (
            row["answer_correct"]
            and row["source_correct"]
            and row["revision_correct"]
        )
    ]
    citation_only = [
        row
        for row in failed
        if row.get("model_value") is not None
        and str(row["model_value"]).strip().upper()
        == str(row["expected_value"]).strip().upper()
        and not (row["source_correct"] and row["revision_correct"])
    ]
    value_not_found = [row for row in failed if row.get("model_value") is None]
    return {
        "qsr_rows": len(rows),
        "exact_successes": len(rows) - len(failed),
        "failed_rows": len(failed),
        "correct_value_wrong_source_or_revision": len(citation_only),
        "value_not_found": len(value_not_found),
        "other_failure": len(failed) - len(citation_only) - len(value_not_found),
    }


def main() -> None:
    print(json.dumps({"s2_costs": s2_costs(), "qsr_failures": qsr_failures()}, indent=2))


if __name__ == "__main__":
    main()
