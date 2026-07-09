"""
ISC Experiments B and D (pilot): failure asymmetry and non-economic benefits.

This is a deterministic offline proxy harness. It does not claim to measure a
production LLM. It isolates the failure modes named in the agenda:

- Experiment B: QSR re-derives answers from a shuffled, overloaded context, so
  repeated runs can vary; ISC reads from a compiled current-fact substrate, so
  answers are stable and failures are localizable.
- Experiment D: a compiled substrate carries explicit provenance and applies
  corrections/deletions once; QSR can surface stale or deleted evidence.

The real-corpus version should replace the proxy reader below with real RAG/LLM
calls and replace the synthetic corpus with a revision stream.
"""

from __future__ import annotations

import csv
import json
import math
import random
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from statistics import mean


SEED = 20260708
ENTITIES = 80
SLOTS = ("capital_plan", "risk_owner", "launch_region")
REPEATS = 40
CONTEXT_SIZES = (2, 4, 8, 16, 32)

OUT_DIR = Path(__file__).resolve().parent


@dataclass(frozen=True)
class FactDoc:
    doc_id: str
    entity: str
    slot: str
    value: str
    revision: int
    current: bool
    deleted: bool
    source: str


def make_corpus(seed: int = SEED) -> tuple[list[FactDoc], dict[tuple[str, str], FactDoc]]:
    rng = random.Random(seed)
    docs: list[FactDoc] = []
    current: dict[tuple[str, str], FactDoc] = {}

    for entity_ix in range(ENTITIES):
        entity = f"project_{entity_ix:03d}"
        for slot in SLOTS:
            versions = rng.randint(3, 5)
            current_revision = versions - 1
            for revision in range(versions):
                value = f"{slot}_v{revision}_{rng.randrange(1000, 9999)}"
                doc = FactDoc(
                    doc_id=f"{entity}_{slot}_r{revision}",
                    entity=entity,
                    slot=slot,
                    value=value,
                    revision=revision,
                    current=revision == current_revision,
                    deleted=False,
                    source=f"src/{entity}/{slot}/rev-{revision}.md",
                )
                docs.append(doc)
                if doc.current:
                    current[(entity, slot)] = doc

    return docs, current


def compile_substrate(docs: list[FactDoc]) -> dict[tuple[str, str], FactDoc]:
    compiled: dict[tuple[str, str], FactDoc] = {}
    for doc in docs:
        key = (doc.entity, doc.slot)
        if key not in compiled or doc.revision > compiled[key].revision:
            compiled[key] = doc
    return compiled


def retrieve_context(
    docs: list[FactDoc],
    entity: str,
    slot: str,
    context_size: int,
    rng: random.Random,
) -> list[FactDoc]:
    exact = [d for d in docs if d.entity == entity and d.slot == slot]
    same_entity = [d for d in docs if d.entity == entity and d.slot != slot]
    distractors = [d for d in docs if d.entity != entity]

    # Simulate an honest vector-index baseline: the right facts are usually
    # retrieved, but old revisions and nearby distractors also enter context.
    context = exact[:]
    rng.shuffle(context)
    rng.shuffle(same_entity)
    rng.shuffle(distractors)
    context.extend(same_entity[: max(1, context_size // 5)])
    context.extend(distractors[: context_size])
    rng.shuffle(context)
    return context[:context_size]


def qsr_answer(context: list[FactDoc], entity: str, slot: str, rng: random.Random) -> dict[str, object]:
    candidates = [d for d in context if d.entity == entity and d.slot == slot]
    if not candidates:
        return {"value": "UNKNOWN", "source": None, "revision": None, "deleted": False}

    current = [d for d in candidates if d.current and not d.deleted]
    stale = [d for d in candidates if not d.current and not d.deleted]
    deleted = [d for d in candidates if d.deleted]

    overload = max(0, len(context) - 4)
    current_weight = max(0.15, 0.88 - overload * 0.025)
    stale_weight = 0.10 + overload * 0.018
    deleted_weight = 0.02 + overload * 0.007

    buckets: list[tuple[float, list[FactDoc]]] = [
        (current_weight, current),
        (stale_weight, stale),
        (deleted_weight, deleted),
    ]
    total = sum(weight for weight, bucket in buckets if bucket)
    if total == 0:
        chosen = max(candidates, key=lambda d: d.revision)
    else:
        draw = rng.random() * total
        acc = 0.0
        chosen_bucket = candidates
        for weight, bucket in buckets:
            if not bucket:
                continue
            acc += weight
            if draw <= acc:
                chosen_bucket = bucket
                break
        chosen = rng.choice(chosen_bucket)

    # QSR often cites a source, but under overload it can cite the wrong nearby
    # context item even when the answer value came from the right one.
    if rng.random() < min(0.40, len(context) * 0.01):
        cited = rng.choice(context)
    else:
        cited = chosen

    return {
        "value": chosen.value,
        "source": cited.source,
        "revision": cited.revision,
        "deleted": chosen.deleted,
    }


def isc_answer(substrate: dict[tuple[str, str], FactDoc], entity: str, slot: str) -> dict[str, object]:
    doc = substrate.get((entity, slot))
    if doc is None:
        return {"value": "UNKNOWN", "source": None, "revision": None, "deleted": False}
    if doc.deleted:
        return {"value": "UNKNOWN", "source": doc.source, "revision": doc.revision, "deleted": False}
    return {"value": doc.value, "source": doc.source, "revision": doc.revision, "deleted": doc.deleted}


def entropy(values: list[str]) -> float:
    counts: dict[str, int] = defaultdict(int)
    for value in values:
        counts[value] += 1
    total = len(values)
    return -sum((count / total) * math.log2(count / total) for count in counts.values())


def score_answers(
    answers_by_question: dict[tuple[str, str], list[dict[str, object]]],
    gold: dict[tuple[str, str], FactDoc],
) -> dict[str, float]:
    per_question_accuracy = []
    per_question_prov = []
    per_question_deleted = []
    per_question_entropy = []
    per_question_distinct = []
    per_question_contradiction = []

    for key, answers in answers_by_question.items():
        gold_doc = gold[key]
        expected_value = "UNKNOWN" if gold_doc.deleted else gold_doc.value
        values = [str(answer["value"]) for answer in answers]
        correct = [value == expected_value for value in values]
        prov_correct = [
            answer["source"] == gold_doc.source and answer["revision"] == gold_doc.revision
            for answer in answers
        ]
        deleted = [bool(answer["deleted"]) for answer in answers]
        per_question_accuracy.append(mean(correct))
        per_question_prov.append(mean(prov_correct))
        per_question_deleted.append(mean(deleted))
        per_question_entropy.append(entropy(values))
        per_question_distinct.append(len(set(values)))
        per_question_contradiction.append(1.0 if len(set(values)) > 1 else 0.0)

    return {
        "answer_accuracy": round(mean(per_question_accuracy), 4),
        "provenance_accuracy": round(mean(per_question_prov), 4),
        "deleted_answer_rate": round(mean(per_question_deleted), 4),
        "mean_answer_entropy_bits": round(mean(per_question_entropy), 4),
        "mean_distinct_answers": round(mean(per_question_distinct), 4),
        "contradiction_rate": round(mean(per_question_contradiction), 4),
    }


def run_exp_b(docs: list[FactDoc], gold: dict[tuple[str, str], FactDoc]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    compiled = compile_substrate(docs)

    for context_size in CONTEXT_SIZES:
        qsr_answers: dict[tuple[str, str], list[dict[str, object]]] = defaultdict(list)
        isc_answers: dict[tuple[str, str], list[dict[str, object]]] = defaultdict(list)

        for repeat in range(REPEATS):
            rng = random.Random(SEED + repeat + context_size * 1000)
            for key in gold:
                entity, slot = key
                context = retrieve_context(docs, entity, slot, context_size, rng)
                qsr_answers[key].append(qsr_answer(context, entity, slot, rng))
                isc_answers[key].append(isc_answer(compiled, entity, slot))

        for pipeline, answers in (("QSR+vector-index", qsr_answers), ("ISC compiled substrate", isc_answers)):
            scored = score_answers(answers, gold)
            rows.append(
                {
                    "experiment": "B",
                    "condition": f"context_docs={context_size}",
                    "pipeline": pipeline,
                    **scored,
                }
            )

    return rows


def apply_corrections_and_deletions(
    docs: list[FactDoc],
    gold: dict[tuple[str, str], FactDoc],
) -> tuple[list[FactDoc], dict[tuple[str, str], FactDoc], set[tuple[str, str]], set[tuple[str, str]]]:
    updated_docs = list(docs)
    updated_gold = dict(gold)

    keys = sorted(gold)
    corrected_keys = set(keys[:24])
    deleted_keys = set(keys[24:48])

    for key in corrected_keys:
        old = updated_gold[key]
        entity, slot = key
        new = FactDoc(
            doc_id=f"{entity}_{slot}_r{old.revision + 1}",
            entity=entity,
            slot=slot,
            value=f"{slot}_corrected_{entity}",
            revision=old.revision + 1,
            current=True,
            deleted=False,
            source=f"src/{entity}/{slot}/rev-{old.revision + 1}.md",
        )
        updated_docs.append(new)
        updated_gold[key] = new

    for key in deleted_keys:
        old = updated_gold[key]
        tombstone = FactDoc(
            doc_id=f"{old.entity}_{old.slot}_delete",
            entity=old.entity,
            slot=old.slot,
            value="DELETED",
            revision=old.revision + 1,
            current=True,
            deleted=True,
            source=f"src/{old.entity}/{old.slot}/delete.md",
        )
        updated_docs.append(tombstone)
        updated_gold[key] = tombstone

    return updated_docs, updated_gold, corrected_keys, deleted_keys


def run_exp_d(docs: list[FactDoc], gold: dict[tuple[str, str], FactDoc]) -> list[dict[str, object]]:
    updated_docs, updated_gold, corrected_keys, deleted_keys = apply_corrections_and_deletions(docs, gold)
    compiled = compile_substrate(updated_docs)
    rows: list[dict[str, object]] = []
    context_size = 16

    qsr_answers: dict[tuple[str, str], list[dict[str, object]]] = defaultdict(list)
    isc_answers: dict[tuple[str, str], list[dict[str, object]]] = defaultdict(list)

    for repeat in range(REPEATS):
        rng = random.Random(SEED * 2 + repeat)
        for key in updated_gold:
            entity, slot = key
            context = retrieve_context(updated_docs, entity, slot, context_size, rng)
            qsr_answers[key].append(qsr_answer(context, entity, slot, rng))
            isc_answers[key].append(isc_answer(compiled, entity, slot))

    for pipeline, answers in (("QSR+vector-index", qsr_answers), ("ISC compiled substrate", isc_answers)):
        scored = score_answers(answers, updated_gold)
        rows.append(
            {
                "experiment": "D",
                "condition": "all_facts_after_corrections_and_deletions",
                "pipeline": pipeline,
                **scored,
            }
        )

        correction_hits = []
        deletion_hits = []
        audit_hits = []
        for key in corrected_keys:
            expected = updated_gold[key].value
            correction_hits.extend(answer["value"] == expected for answer in answers[key])
        for key in deleted_keys:
            deletion_hits.extend(answer["value"] == "UNKNOWN" for answer in answers[key])
        for key, doc in updated_gold.items():
            if doc.deleted:
                continue
            audit_hits.extend(
                answer["source"] == doc.source and answer["revision"] == doc.revision for answer in answers[key]
            )

        rows.append(
            {
                "experiment": "D",
                "condition": "governance_tasks",
                "pipeline": pipeline,
                "correction_persistence": round(mean(correction_hits), 4),
                "deletion_propagation_correctness": round(mean(deletion_hits), 4),
                "auditability_coverage": round(mean(audit_hits), 4),
            }
        )

    return rows


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def summarize(rows: list[dict[str, object]]) -> dict[str, object]:
    def find(experiment: str, condition: str, pipeline: str) -> dict[str, object]:
        for row in rows:
            if row["experiment"] == experiment and row["condition"] == condition and row["pipeline"] == pipeline:
                return row
        raise KeyError((experiment, condition, pipeline))

    b_qsr_16 = find("B", "context_docs=16", "QSR+vector-index")
    b_isc_16 = find("B", "context_docs=16", "ISC compiled substrate")
    b_qsr_32 = find("B", "context_docs=32", "QSR+vector-index")
    d_qsr = find("D", "all_facts_after_corrections_and_deletions", "QSR+vector-index")
    d_isc = find("D", "all_facts_after_corrections_and_deletions", "ISC compiled substrate")
    d_qsr_gov = find("D", "governance_tasks", "QSR+vector-index")
    d_isc_gov = find("D", "governance_tasks", "ISC compiled substrate")

    return {
        "pilot_type": "deterministic offline proxy; replace proxy reader with real RAG/LLM for final study",
        "corpus": {
            "entities": ENTITIES,
            "slots": len(SLOTS),
            "questions": ENTITIES * len(SLOTS),
            "repeats": REPEATS,
        },
        "experiment_B": {
            "qsr_context16_contradiction_rate": b_qsr_16["contradiction_rate"],
            "isc_context16_contradiction_rate": b_isc_16["contradiction_rate"],
            "qsr_context16_answer_accuracy": b_qsr_16["answer_accuracy"],
            "isc_context16_answer_accuracy": b_isc_16["answer_accuracy"],
            "qsr_context32_answer_accuracy": b_qsr_32["answer_accuracy"],
            "qsr_context16_mean_distinct_answers": b_qsr_16["mean_distinct_answers"],
            "isc_context16_mean_distinct_answers": b_isc_16["mean_distinct_answers"],
        },
        "experiment_D": {
            "qsr_provenance_accuracy": d_qsr["provenance_accuracy"],
            "isc_provenance_accuracy": d_isc["provenance_accuracy"],
            "qsr_deleted_answer_rate": d_qsr["deleted_answer_rate"],
            "isc_deleted_answer_rate": d_isc["deleted_answer_rate"],
            "qsr_correction_persistence": d_qsr_gov["correction_persistence"],
            "isc_correction_persistence": d_isc_gov["correction_persistence"],
            "qsr_deletion_propagation_correctness": d_qsr_gov["deletion_propagation_correctness"],
            "isc_deletion_propagation_correctness": d_isc_gov["deletion_propagation_correctness"],
            "qsr_auditability_coverage": d_qsr_gov["auditability_coverage"],
            "isc_auditability_coverage": d_isc_gov["auditability_coverage"],
        },
    }


def write_markdown(path: Path, summary: dict[str, object]) -> None:
    b = summary["experiment_B"]
    d = summary["experiment_D"]
    text = f"""# Experiment B/D Pilot Summary

This is a deterministic offline proxy over a synthetic revision corpus. It is useful
for validating the measurement harness and the expected failure modes, not as final
LLM evidence.

## Experiment B - failure asymmetry

At 16 retrieved context documents, QSR had contradiction rate
{b["qsr_context16_contradiction_rate"]} across repeated runs and mean distinct
answers {b["qsr_context16_mean_distinct_answers"]}; ISC had contradiction rate
{b["isc_context16_contradiction_rate"]} and mean distinct answers
{b["isc_context16_mean_distinct_answers"]}. QSR accuracy dropped from
{b["qsr_context16_answer_accuracy"]} at 16 context docs to
{b["qsr_context32_answer_accuracy"]} at 32 context docs, showing the intended
context-overload stress.

## Experiment D - non-economic benefits

QSR provenance accuracy was {d["qsr_provenance_accuracy"]}; ISC provenance
accuracy was {d["isc_provenance_accuracy"]}. QSR correction persistence was
{d["qsr_correction_persistence"]}; ISC correction persistence was
{d["isc_correction_persistence"]}. QSR deletion propagation correctness was
{d["qsr_deletion_propagation_correctness"]}; ISC deletion propagation correctness
was {d["isc_deletion_propagation_correctness"]}. Auditability coverage was
{d["qsr_auditability_coverage"]} for QSR and {d["isc_auditability_coverage"]} for
ISC.

## Next replacement for the real study

Keep the output schema, but replace the proxy `qsr_answer` with repeated calls to
the Gemini proxy or another fixed LLM/RAG pipeline, and replace the synthetic
revision corpus with Wikipedia revision slices or the project corpus.
"""
    path.write_text(text)


def main() -> None:
    docs, gold = make_corpus()
    rows = run_exp_b(docs, gold) + run_exp_d(docs, gold)
    write_csv(OUT_DIR / "exp_BD_results.csv", rows)
    summary = summarize(rows)
    (OUT_DIR / "exp_BD_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    write_markdown(OUT_DIR / "exp_BD_summary.md", summary)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
