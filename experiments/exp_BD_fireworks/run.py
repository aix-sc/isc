"""
ISC Experiment B/D Fireworks runner.

Delegates a small set of QSR-style questions to OSS models hosted on Fireworks:

- DeepSeek V4 Pro: accounts/fireworks/models/deepseek-v4-pro
- DeepSeek V4 Flash: accounts/fireworks/models/deepseek-v4-flash
- GLM 5.2: accounts/fireworks/models/glm-5p2
- Kimi K2.7 Code: accounts/fireworks/models/kimi-k2p7-code

The runner uses the same synthetic revision corpus as synthetic_revision.py.
Each model receives a shuffled retrieved context with current facts, stale
revisions, deletion tombstones, and distractors. The model must reconstruct the
current answer and cite the supporting source.

Secrets are resolved from FIREWORKS_API_KEY.

Example:
  uv run python experiments/exp_BD_fireworks/run.py --limit 6
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import random
import subprocess
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from synthetic_revision import (
    SEED,
    FactDoc,
    apply_corrections_and_deletions,
    make_corpus,
    retrieve_context,
)


OUT_DIR = Path(__file__).resolve().parent
FIREWORKS_CHAT_URL = "https://api.fireworks.ai/inference/v1/chat/completions"
MODELS = {
    "deepseek-v4-flash": "accounts/fireworks/models/deepseek-v4-flash",
    "deepseek-v4-pro": "accounts/fireworks/models/deepseek-v4-pro",
    "glm-5p2": "accounts/fireworks/models/glm-5p2",
    "kimi-k2p7-code": "accounts/fireworks/models/kimi-k2p7-code",
}

PRICES_PER_MILLION = {
    "accounts/fireworks/models/deepseek-v4-flash": {"input": 0.14, "output": 0.28},
    "accounts/fireworks/models/deepseek-v4-pro": {"input": 1.74, "output": 3.48},
    "accounts/fireworks/models/glm-5p2": {"input": 1.40, "output": 4.40},
    "accounts/fireworks/models/kimi-k2p7-code": {"input": 0.95, "output": 4.00},
}


@dataclass(frozen=True)
class Question:
    question_id: str
    entity: str
    slot: str
    expected_value: str
    expected_source: str
    expected_revision: int
    expected_deleted: bool
    category: str
    context: list[FactDoc]
    qsr_context_text: str | None = None


def resolve_fireworks_api_key() -> str:
    key = os.environ.get("FIREWORKS_API_KEY", "").strip()
    if not key:
        raise RuntimeError("Set FIREWORKS_API_KEY.")
    return key


def fact_category(doc: FactDoc) -> str:
    if doc.deleted:
        return "deleted"
    if "_corrected_" in doc.value:
        return "corrected"
    return "ordinary"


def make_questions(
    limit: int,
    context_docs: int,
    seed: int,
    include_gold: bool,
    balanced_categories: bool,
) -> list[Question]:
    docs, gold = make_corpus()
    updated_docs, updated_gold, _, _ = apply_corrections_and_deletions(docs, gold)
    keys = sorted(updated_gold)
    rng = random.Random(seed)
    if balanced_categories:
        grouped: dict[str, list[tuple[str, str]]] = {"corrected": [], "deleted": [], "ordinary": []}
        for key in keys:
            grouped[fact_category(updated_gold[key])].append(key)
        for group in grouped.values():
            rng.shuffle(group)
        keys = []
        while len(keys) < limit and any(grouped.values()):
            for category in ("corrected", "deleted", "ordinary"):
                if grouped[category] and len(keys) < limit:
                    keys.append(grouped[category].pop())
    else:
        rng.shuffle(keys)

    questions: list[Question] = []
    for key in keys[:limit]:
        entity, slot = key
        expected = updated_gold[key]
        context = retrieve_context(updated_docs, entity, slot, context_docs, rng)
        if include_gold and all(doc.source != expected.source for doc in context):
            if len(context) >= context_docs:
                context[-1] = expected
            else:
                context.append(expected)
            rng.shuffle(context)
        questions.append(
            Question(
                question_id=f"{entity}:{slot}",
                entity=entity,
                slot=slot,
                expected_value="UNKNOWN" if expected.deleted else expected.value,
                expected_source=expected.source,
                expected_revision=expected.revision,
                expected_deleted=expected.deleted,
                category=fact_category(expected),
                context=context,
            )
        )
    return questions


def make_hard_questions(limit: int, context_docs: int, seed: int) -> list[Question]:
    rng = random.Random(seed)
    questions: list[Question] = []
    regions = [
        "apac-south-3",
        "emea-north-2",
        "latam-east-1",
        "na-central-4",
        "japan-west-2",
        "india-west-1",
    ]
    slots = ["launch_region", "risk_owner", "capital_plan"]

    rules = """Resolution rules:
1. Consider only rows matching the requested entity and slot.
2. Ignore rows where env is not production.
3. Ignore rows where state is draft, proposal, rejected, or superseded.
4. If the highest-version matching production row is a tombstone, answer UNKNOWN.
5. Otherwise choose the highest-version matching production row with state approved.
6. The source and revision must come from the chosen row, not from a nearby draft or sandbox row.
"""

    for i in range(limit):
        entity = f"hard_project_{i:03d}"
        slot = slots[i % len(slots)]
        answer = regions[i % len(regions)] if slot == "launch_region" else f"{slot}_approved_{i:03d}"
        revision = 7 + (i % 3)
        source = f"src/{entity}/{slot}/approved-r{revision}.md"
        deleted = i % 5 == 3
        expected_value = "UNKNOWN" if deleted else answer
        expected_source = f"src/{entity}/{slot}/delete-r{revision + 1}.md" if deleted else source
        expected_revision = revision + 1 if deleted else revision

        rows: list[dict[str, object]] = [
            {
                "doc_id": f"{entity}_{slot}_r{revision - 5}_approved_old",
                "entity": entity,
                "slot": slot,
                "value": f"{slot}_old_{i:03d}",
                "version": revision - 5,
                "env": "production",
                "state": "approved",
                "source": f"src/{entity}/{slot}/approved-r{revision - 5}.md",
            },
            {
                "doc_id": f"{entity}_{slot}_r{revision - 1}_sandbox",
                "entity": entity,
                "slot": slot,
                "value": f"{slot}_sandbox_{i:03d}",
                "version": revision - 1,
                "env": "sandbox",
                "state": "approved",
                "source": f"src/{entity}/{slot}/sandbox-r{revision - 1}.md",
            },
            {
                "doc_id": f"{entity}_{slot}_r{revision}_approved",
                "entity": entity,
                "slot": slot,
                "value": answer,
                "version": revision,
                "env": "production",
                "state": "approved",
                "source": source,
            },
            {
                "doc_id": f"{entity}_{slot}_r{revision + 2}_draft",
                "entity": entity,
                "slot": slot,
                "value": f"{slot}_tempting_draft_{i:03d}",
                "version": revision + 2,
                "env": "production",
                "state": "draft",
                "source": f"src/{entity}/{slot}/draft-r{revision + 2}.md",
            },
            {
                "doc_id": f"{entity}_{slot}_r{revision + 3}_proposal",
                "entity": entity,
                "slot": slot,
                "value": f"{slot}_tempting_proposal_{i:03d}",
                "version": revision + 3,
                "env": "production",
                "state": "proposal",
                "source": f"src/{entity}/{slot}/proposal-r{revision + 3}.md",
            },
        ]
        if deleted:
            rows.append(
                {
                    "doc_id": f"{entity}_{slot}_r{revision + 1}_delete",
                    "entity": entity,
                    "slot": slot,
                    "value": "DELETED",
                    "version": revision + 1,
                    "env": "production",
                    "state": "tombstone",
                    "source": expected_source,
                }
            )

        for j in range(max(0, context_docs - len(rows))):
            distract_entity = f"hard_project_{rng.randrange(0, max(limit, 20)):03d}"
            distract_slot = rng.choice(slots)
            rows.append(
                {
                    "doc_id": f"{distract_entity}_{distract_slot}_distractor_{j}",
                    "entity": distract_entity,
                    "slot": distract_slot,
                    "value": f"{distract_slot}_distractor_{rng.randrange(1000, 9999)}",
                    "version": rng.randrange(1, 14),
                    "env": rng.choice(["production", "sandbox"]),
                    "state": rng.choice(["approved", "draft", "proposal", "superseded", "rejected"]),
                    "source": f"src/{distract_entity}/{distract_slot}/distractor-{j}.md",
                }
            )
        rng.shuffle(rows)
        rendered_rows = []
        for idx, row in enumerate(rows[:context_docs], start=1):
            rendered_rows.append(
                "\n".join(
                    [
                        f"[{idx}] doc_id: {row['doc_id']}",
                        f"entity: {row['entity']}",
                        f"slot: {row['slot']}",
                        f"value: {row['value']}",
                        f"version: {row['version']}",
                        f"env: {row['env']}",
                        f"state: {row['state']}",
                        f"source: {row['source']}",
                    ]
                )
            )

        questions.append(
            Question(
                question_id=f"{entity}:{slot}",
                entity=entity,
                slot=slot,
                expected_value=expected_value,
                expected_source=expected_source,
                expected_revision=expected_revision,
                expected_deleted=deleted,
                category="hard_deleted" if deleted else "hard_policy",
                context=[],
                qsr_context_text=rules + "\nRetrieved policy rows:\n" + "\n\n".join(rendered_rows),
            )
        )

    return questions


def make_adversarial_questions(limit: int, context_docs: int, seed: int) -> list[Question]:
    rng = random.Random(seed)
    questions: list[Question] = []
    slots = ["launch_region", "risk_owner", "capital_plan"]
    rules = """Resolution rules for today = 2026-07-08:
1. Consider only rows matching the requested entity and slot.
2. Candidate rows must have type=value, env=production, state=approved.
3. Candidate valid_from must be on or before today.
4. Candidate valid_until must be NONE or after today.
5. Ignore any candidate whose doc_id is named by a matching type=revocation row.
6. Ignore any candidate whose source_trust is imported if an eligible owner or regulatory candidate exists.
7. If an eligible type=tombstone row exists with effective_on on or before today, answer UNKNOWN.
8. Otherwise choose the eligible value row with highest version. Source/revision must come from that row.
"""
    for i in range(limit):
        entity = f"adversarial_project_{i:03d}"
        slot = slots[i % len(slots)]
        answer = f"{slot}_governed_{i:03d}"
        correct_version = 5 + (i % 4)
        correct_doc = f"{entity}_{slot}_approved_{correct_version}"
        correct_source = f"src/{entity}/{slot}/owner-approved-r{correct_version}.md"
        deleted = i % 4 == 2
        expected_value = "UNKNOWN" if deleted else answer
        expected_revision = correct_version + 7 if deleted else correct_version
        expected_source = (
            f"src/{entity}/{slot}/regulatory-delete-r{expected_revision}.md"
            if deleted
            else correct_source
        )

        wrong_high = f"{entity}_{slot}_approved_high_revoked"
        wrong_imported = f"{entity}_{slot}_approved_imported"
        wrong_future = f"{entity}_{slot}_approved_future"
        rows: list[dict[str, object]] = [
            {
                "doc_id": wrong_high,
                "type": "value",
                "entity": entity,
                "slot": slot,
                "value": f"{slot}_wrong_revoked_{i:03d}",
                "version": correct_version + 6,
                "env": "production",
                "state": "approved",
                "source_trust": "owner",
                "valid_from": "2026-01-01",
                "valid_until": "NONE",
                "source": f"src/{entity}/{slot}/owner-approved-r{correct_version + 6}.md",
            },
            {
                "doc_id": f"{entity}_{slot}_revokes_high",
                "type": "revocation",
                "entity": entity,
                "slot": slot,
                "revokes": wrong_high,
                "version": correct_version + 8,
                "env": "production",
                "state": "approved",
                "source_trust": "regulatory",
                "effective_on": "2026-05-01",
                "source": f"src/{entity}/{slot}/revocation-r{correct_version + 8}.md",
            },
            {
                "doc_id": wrong_imported,
                "type": "value",
                "entity": entity,
                "slot": slot,
                "value": f"{slot}_wrong_imported_{i:03d}",
                "version": correct_version + 5,
                "env": "production",
                "state": "approved",
                "source_trust": "imported",
                "valid_from": "2026-01-01",
                "valid_until": "NONE",
                "source": f"src/{entity}/{slot}/imported-r{correct_version + 5}.md",
            },
            {
                "doc_id": wrong_future,
                "type": "value",
                "entity": entity,
                "slot": slot,
                "value": f"{slot}_wrong_future_{i:03d}",
                "version": correct_version + 4,
                "env": "production",
                "state": "approved",
                "source_trust": "regulatory",
                "valid_from": "2026-12-01",
                "valid_until": "NONE",
                "source": f"src/{entity}/{slot}/future-r{correct_version + 4}.md",
            },
            {
                "doc_id": correct_doc,
                "type": "value",
                "entity": entity,
                "slot": slot,
                "value": answer,
                "version": correct_version,
                "env": "production",
                "state": "approved",
                "source_trust": "owner",
                "valid_from": "2026-01-01",
                "valid_until": "NONE",
                "source": correct_source,
            },
            {
                "doc_id": f"{entity}_{slot}_draft_latest",
                "type": "value",
                "entity": entity,
                "slot": slot,
                "value": f"{slot}_wrong_draft_{i:03d}",
                "version": correct_version + 9,
                "env": "production",
                "state": "draft",
                "source_trust": "owner",
                "valid_from": "2026-01-01",
                "valid_until": "NONE",
                "source": f"src/{entity}/{slot}/draft-r{correct_version + 9}.md",
            },
        ]
        if deleted:
            rows.append(
                {
                    "doc_id": f"{entity}_{slot}_tombstone",
                    "type": "tombstone",
                    "entity": entity,
                    "slot": slot,
                    "value": "DELETED",
                    "version": expected_revision,
                    "env": "production",
                    "state": "approved",
                    "source_trust": "regulatory",
                    "effective_on": "2026-06-15",
                    "source": expected_source,
                }
            )

        for j in range(max(0, context_docs - len(rows))):
            de = f"adversarial_project_{rng.randrange(0, max(limit, 24)):03d}"
            ds = rng.choice(slots)
            rows.append(
                {
                    "doc_id": f"{de}_{ds}_distractor_{j}",
                    "type": rng.choice(["value", "revocation", "note"]),
                    "entity": de,
                    "slot": ds,
                    "value": f"{ds}_distractor_{rng.randrange(1000, 9999)}",
                    "version": rng.randrange(1, 20),
                    "env": rng.choice(["production", "sandbox"]),
                    "state": rng.choice(["approved", "draft", "proposal", "rejected"]),
                    "source_trust": rng.choice(["imported", "owner", "regulatory"]),
                    "valid_from": rng.choice(["2025-01-01", "2026-02-01", "2026-11-01"]),
                    "valid_until": rng.choice(["NONE", "2026-06-01", "2027-01-01"]),
                    "source": f"src/{de}/{ds}/distractor-{j}.md",
                }
            )
        rng.shuffle(rows)
        rendered_rows = []
        for idx, row in enumerate(rows[:context_docs], start=1):
            rendered_rows.append(
                "\n".join(f"{key}: {value}" for key, value in [("row", idx), *row.items()])
            )
        questions.append(
            Question(
                question_id=f"{entity}:{slot}",
                entity=entity,
                slot=slot,
                expected_value=expected_value,
                expected_source=expected_source,
                expected_revision=expected_revision,
                expected_deleted=deleted,
                category="adversarial_deleted" if deleted else "adversarial_policy",
                context=[],
                qsr_context_text=rules + "\nRetrieved governance rows:\n" + "\n\n".join(rendered_rows),
            )
        )
    return questions


def context_to_text(context: list[FactDoc]) -> str:
    rows = []
    for i, doc in enumerate(context, start=1):
        rows.append(
            "\n".join(
                [
                    f"[{i}] doc_id: {doc.doc_id}",
                    f"entity: {doc.entity}",
                    f"slot: {doc.slot}",
                    f"value: {doc.value}",
                    f"revision: {doc.revision}",
                    f"current_flag: {str(doc.current).lower()}",
                    f"deleted: {str(doc.deleted).lower()}",
                    f"source: {doc.source}",
                ]
            )
        )
    return "\n\n".join(rows)


def build_messages(question: Question, mode: str) -> list[dict[str, str]]:
    if mode == "qsr":
        system = (
            "You are evaluating a query-time semantic reconstruction baseline. "
            "Use only the provided context. Pick the current answer for the requested "
            "entity and slot. Higher revision wins. A deletion tombstone means the "
            "answer is UNKNOWN. Return only strict JSON with keys: value, source, "
            "revision, rationale."
        )
        context = question.qsr_context_text or context_to_text(question.context)
        user = f"""Question: What is the current value of slot {question.slot!r} for entity {question.entity!r}?

Retrieved context:
{context}

Return JSON only. The `source` must be the exact source path supporting the answer.
"""
    elif mode == "isc":
        system = (
            "You are answering from an ingest-time semantic compilation substrate. "
            "The substrate has already resolved revision conflicts, corrections, "
            "deletions, and provenance. Use only the compiled record. Return only "
            "strict JSON with keys: value, source, revision, rationale. If the "
            'compiled record says deleted: true, set value exactly to "UNKNOWN" '
            "and keep the deletion source and revision."
        )
        user = f"""Question: What is the current value of slot {question.slot!r} for entity {question.entity!r}?

Compiled substrate record:
entity: {question.entity}
slot: {question.slot}
value: {question.expected_value}
revision: {question.expected_revision}
deleted: {str(question.expected_deleted).lower()}
source: {question.expected_source}

Return JSON only. The `source` must be the exact source path from the compiled record.
"""
    else:
        raise ValueError(f"unknown mode {mode!r}")
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


def post_chat_completion(
    api_key: str,
    model: str,
    messages: list[dict[str, str]],
    max_tokens: int,
    temperature: float,
    timeout: float,
) -> dict[str, Any]:
    body = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "response_format": {"type": "json_object"},
    }
    req = urllib.request.Request(
        FIREWORKS_CHAT_URL,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as res:
            return json.loads(res.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Fireworks HTTP {exc.code} for model {model}: {detail}") from exc


def parse_model_json(content: str) -> dict[str, Any]:
    try:
        parsed = json.loads(content)
    except json.JSONDecodeError:
        start = content.find("{")
        end = content.rfind("}")
        if start == -1 or end == -1 or end <= start:
            return {"value": None, "source": None, "revision": None, "parse_error": content}
        try:
            parsed = json.loads(content[start : end + 1])
        except json.JSONDecodeError:
            return {"value": None, "source": None, "revision": None, "parse_error": content}

    if not isinstance(parsed, dict):
        return {"value": None, "source": None, "revision": None, "parse_error": content}
    return parsed


def score(question: Question, parsed: dict[str, Any]) -> dict[str, Any]:
    has_value_key = "value" in parsed
    raw_value = parsed.get("value")
    value = "" if raw_value is None else str(raw_value).strip()
    source = str(parsed.get("source", "")).strip()
    revision_raw = parsed.get("revision")
    try:
        revision = int(revision_raw)
    except (TypeError, ValueError):
        revision = None

    if question.expected_deleted:
        answer_correct = has_value_key and value.upper() in {"", "UNKNOWN", "NULL", "NONE", "DELETED"}
    else:
        answer_correct = value == question.expected_value

    return {
        "answer_correct": answer_correct,
        "source_correct": source == question.expected_source,
        "revision_correct": revision == question.expected_revision,
    }


def estimate_cost_usd(model_id: str, prompt_tokens: Any, completion_tokens: Any) -> float | None:
    prices = PRICES_PER_MILLION.get(model_id)
    if prices is None or prompt_tokens is None or completion_tokens is None:
        return None
    return round(
        (int(prompt_tokens) * prices["input"] + int(completion_tokens) * prices["output"]) / 1_000_000,
        8,
    )


def run(args: argparse.Namespace) -> list[dict[str, Any]]:
    if args.question_set == "revision":
        questions = make_questions(
            args.limit,
            args.context_docs,
            args.seed,
            include_gold=not args.allow_missing_gold,
            balanced_categories=not args.random_questions,
        )
    elif args.question_set == "hard":
        questions = make_hard_questions(args.limit, args.context_docs, args.seed)
    else:
        questions = make_adversarial_questions(args.limit, args.context_docs, args.seed)
    selected_models = [(name, MODELS[name]) for name in args.models]

    if args.dry_run:
        for question in questions:
            for mode in args.modes:
                print(f"\n# {mode} {question.question_id} ({question.category})")
                print(build_messages(question, mode)[1]["content"])
        return []

    api_key = resolve_fireworks_api_key()
    rows: list[dict[str, Any]] = []

    for q_ix, question in enumerate(questions, start=1):
        for mode in args.modes:
            for model_name, model_id in selected_models:
                started = time.perf_counter()
                messages = build_messages(question, mode)
                print(
                    f"{q_ix}/{len(questions)} calling {model_name} {mode} for "
                    f"{question.question_id} ({question.category})...",
                    flush=True,
                )
                response = post_chat_completion(
                    api_key=api_key,
                    model=model_id,
                    messages=messages,
                    max_tokens=args.max_tokens,
                    temperature=args.temperature,
                    timeout=args.timeout,
                )
                elapsed_ms = round((time.perf_counter() - started) * 1000, 1)
                choice = response.get("choices", [{}])[0]
                content = choice.get("message", {}).get("content", "")
                parsed = parse_model_json(content)
                scored = score(question, parsed)
                usage = response.get("usage", {})
                prompt_tokens = usage.get("prompt_tokens")
                completion_tokens = usage.get("completion_tokens")
                row = {
                    "question_index": q_ix,
                    "question_id": question.question_id,
                    "category": question.category,
                    "mode": mode,
                    "entity": question.entity,
                    "slot": question.slot,
                    "model_name": model_name,
                    "model_id": model_id,
                    "expected_value": question.expected_value,
                    "expected_source": question.expected_source,
                    "expected_revision": question.expected_revision,
                    "expected_deleted": question.expected_deleted,
                    "model_value": parsed.get("value"),
                    "model_source": parsed.get("source"),
                    "model_revision": parsed.get("revision"),
                    "model_rationale": parsed.get("rationale"),
                    "answer_correct": scored["answer_correct"],
                    "source_correct": scored["source_correct"],
                    "revision_correct": scored["revision_correct"],
                    "latency_ms": elapsed_ms,
                    "prompt_tokens": prompt_tokens,
                    "completion_tokens": completion_tokens,
                    "total_tokens": usage.get("total_tokens"),
                    "estimated_cost_usd": estimate_cost_usd(model_id, prompt_tokens, completion_tokens),
                    "raw_content": content,
                }
                rows.append(row)
                status = "ok" if row["answer_correct"] and row["source_correct"] else "miss"
                print(
                    f"{q_ix}/{len(questions)} {model_name} {mode} {question.question_id}: "
                    f"{status} ({elapsed_ms} ms)"
                )

    return rows


def write_outputs(rows: list[dict[str, Any]], csv_path: Path, jsonl_path: Path, summary_path: Path) -> None:
    if not rows:
        return

    csv_path.parent.mkdir(parents=True, exist_ok=True)
    jsonl_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.parent.mkdir(parents=True, exist_ok=True)

    with jsonl_path.open("w") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    fields = [key for key in rows[0].keys() if key != "raw_content"] + ["raw_content"]
    with csv_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    by_model_mode: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for row in rows:
        by_model_mode.setdefault((str(row["model_name"]), str(row["mode"])), []).append(row)

    summary = {
        "rows": len(rows),
        "model_modes": {
            f"{model}/{mode}": {
                "questions": len(model_rows),
                "answer_accuracy": round(sum(bool(r["answer_correct"]) for r in model_rows) / len(model_rows), 4),
                "source_accuracy": round(sum(bool(r["source_correct"]) for r in model_rows) / len(model_rows), 4),
                "revision_accuracy": round(sum(bool(r["revision_correct"]) for r in model_rows) / len(model_rows), 4),
                "mean_latency_ms": round(sum(float(r["latency_ms"]) for r in model_rows) / len(model_rows), 1),
                "total_tokens": sum(int(r["total_tokens"] or 0) for r in model_rows),
                "estimated_cost_usd": round(
                    sum(float(r["estimated_cost_usd"] or 0.0) for r in model_rows),
                    8,
                ),
            }
            for (model, mode), model_rows in by_model_mode.items()
        },
    }
    summary_path.write_text(json.dumps(summary, indent=2) + "\n")


def parse_args() -> argparse.Namespace:
    pre_parser = argparse.ArgumentParser(add_help=False)
    pre_parser.add_argument("--config", type=Path, help="JSON config file with argument defaults.")
    pre_args, _ = pre_parser.parse_known_args()
    config_defaults: dict[str, Any] = {}
    if pre_args.config:
        config_defaults = json.loads(pre_args.config.read_text())

    parser = argparse.ArgumentParser(description="Run B/D QSR questions against Fireworks OSS models.")
    parser.add_argument("--config", type=Path, help="JSON config file with argument defaults.")
    parser.add_argument("--limit", type=int, default=6, help="Number of corpus questions to ask.")
    parser.add_argument("--context-docs", type=int, default=16, help="Retrieved context documents per question.")
    parser.add_argument("--seed", type=int, default=SEED + 99, help="Question/context sampling seed.")
    parser.add_argument("--models", nargs="+", choices=sorted(MODELS), default=sorted(MODELS))
    parser.add_argument("--modes", nargs="+", choices=("qsr", "isc"), default=("qsr", "isc"))
    parser.add_argument("--question-set", choices=("revision", "hard", "adversarial"), default="revision")
    parser.add_argument("--max-tokens", type=int, default=1024)
    parser.add_argument("--temperature", type=float, default=0.1)
    parser.add_argument("--timeout", type=float, default=90.0)
    parser.add_argument("--csv-out", type=Path, default=OUT_DIR / "exp_BD_fireworks_answers.csv")
    parser.add_argument("--jsonl-out", type=Path, default=OUT_DIR / "exp_BD_fireworks_answers.jsonl")
    parser.add_argument("--summary-out", type=Path, default=OUT_DIR / "exp_BD_fireworks_summary.json")
    parser.add_argument("--dry-run", action="store_true", help="Print prompts without calling Fireworks.")
    parser.add_argument(
        "--allow-missing-gold",
        action="store_true",
        help="Do not force the current/gold fact into retrieved context; measures retrieval failure too.",
    )
    parser.add_argument("--random-questions", action="store_true", help="Sample questions uniformly at random.")
    parser.set_defaults(**config_defaults)
    args = parser.parse_args()
    for field in ("csv_out", "jsonl_out", "summary_out", "config"):
        value = getattr(args, field, None)
        if field.endswith("_out") or field == "config":
            if isinstance(value, str):
                setattr(args, field, Path(value))
    return args


def main() -> int:
    args = parse_args()
    try:
        rows = run(args)
        write_outputs(rows, args.csv_out, args.jsonl_out, args.summary_out)
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
