"""
Measure S2 fact rephrasing compression and fidelity on real passages.

Supported passage sources are public Wikipedia paragraphs and public Federal
Reserve press-conference transcript excerpts. The measurement is deliberately
narrow: S2 rewrites each passage into self-contained, pronoun-free atomic facts;
a judge then checks whether the fact set is supported by the original passage
and sufficient for factual QA over the passage.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


FIREWORKS_CHAT_URL = "https://api.fireworks.ai/inference/v1/chat/completions"
DEFAULT_MODEL = "accounts/fireworks/models/deepseek-v4-flash"

WIKIPEDIA_TITLES = [
    "Materialized_view",
    "Inverted_index",
    "Vector_space_model",
    "Latent_semantic_analysis",
    "Retrieval-augmented_generation",
    "Knowledge_graph",
    "Database_transaction",
    "Data_lineage",
    "Version_control",
    "Slowly_changing_dimension",
    "Record_linkage",
    "Information_retrieval",
    "Question_answering",
    "Data_governance",
    "Change_data_capture",
]

FED_TRANSCRIPTS = [
    (
        "FOMC press conference, April 29 2026",
        "20260429",
        "https://www.federalreserve.gov/mediacenter/files/FOMCpresconf20260429.pdf",
    ),
    (
        "FOMC press conference, March 18 2026",
        "20260318",
        "https://www.federalreserve.gov/mediacenter/files/FOMCpresconf20260318.pdf",
    ),
    (
        "FOMC press conference, January 28 2026",
        "20260128",
        "https://www.federalreserve.gov/mediacenter/files/FOMCpresconf20260128.pdf",
    ),
    (
        "FOMC press conference, July 30 2025",
        "20250730",
        "https://www.federalreserve.gov/mediacenter/files/FOMCpresconf20250730.pdf",
    ),
    (
        "FOMC press conference, June 18 2025",
        "20250618",
        "https://www.federalreserve.gov/mediacenter/files/FOMCpresconf20250618.pdf",
    ),
]

SOURCE_LABELS = {
    "wikipedia": "Wikipedia public passages snapshotted in passages.jsonl",
    "fed_dialogue": "Federal Reserve press-conference dialogue excerpts snapshotted in passages.jsonl",
}


@dataclass(frozen=True)
class Passage:
    passage_id: str
    title: str
    source_url: str
    text: str


def resolve_fireworks_api_key(op_ref: str | None, op_account: str | None) -> str:
    for env_name in ("FIREWORKS_API_KEY", "LLM_GATEWAY_DEFAULT_FIREWORKS_API_KEY"):
        value = os.environ.get(env_name, "").strip()
        if value:
            return value

    if not op_ref:
        raise RuntimeError(
            "Set FIREWORKS_API_KEY or LLM_GATEWAY_DEFAULT_FIREWORKS_API_KEY, "
            "or pass --op-ref with a 1Password secret reference."
        )

    cmd = ["op", "read", op_ref]
    if op_account:
        cmd.extend(["--account", op_account])

    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    except FileNotFoundError as exc:
        raise RuntimeError("1Password CLI `op` is not installed.") from exc
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(f"Could not read 1Password ref {op_ref!r}: {exc.stderr.strip()}") from exc

    key = result.stdout.strip()
    if not key:
        raise RuntimeError(f"1Password ref {op_ref!r} resolved to an empty value.")
    return key


def token_counter() -> tuple[str, Any]:
    try:
        import tiktoken  # type: ignore

        enc = tiktoken.get_encoding("cl100k_base")
        return "tiktoken:cl100k_base", lambda text: len(enc.encode(text))
    except Exception:
        token_re = re.compile(r"\w+|[^\w\s]", re.UNICODE)
        return "regex_token_proxy", lambda text: len(token_re.findall(text))


def fetch_wikipedia_extract(title: str) -> tuple[str, str]:
    params = {
        "action": "query",
        "format": "json",
        "prop": "extracts",
        "explaintext": "1",
        "redirects": "1",
        "titles": title,
    }
    url = "https://en.wikipedia.org/w/api.php?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "isc-s2-measurement/1.0"})
    with urllib.request.urlopen(req, timeout=30) as res:
        data = json.loads(res.read().decode("utf-8"))
    pages = data["query"]["pages"]
    page = next(iter(pages.values()))
    canonical_title = page.get("title", title)
    extract = page.get("extract", "")
    source_url = "https://en.wikipedia.org/wiki/" + urllib.parse.quote(canonical_title.replace(" ", "_"))
    return source_url, extract


def clean_paragraph(text: str) -> str:
    text = re.sub(r"\[[^\]]+\]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def passage_candidates(limit: int) -> list[Passage]:
    passages: list[Passage] = []
    for title in WIKIPEDIA_TITLES:
        source_url, extract = fetch_wikipedia_extract(title)
        para_ix = 0
        for raw in extract.split("\n"):
            paragraph = clean_paragraph(raw)
            words = paragraph.split()
            if len(words) < 70 or len(words) > 190:
                continue
            para_ix += 1
            passages.append(
                Passage(
                    passage_id=f"{title}:{para_ix}",
                    title=title.replace("_", " "),
                    source_url=source_url,
                    text=paragraph,
                )
            )
            if len(passages) >= limit:
                return passages
    return passages


def fetch_pdf_text(url: str) -> str:
    try:
        from pypdf import PdfReader  # type: ignore
    except Exception as exc:
        raise RuntimeError(
            "The fed_dialogue source set requires pypdf. Run with `uv run --with pypdf --with tiktoken ...`."
        ) from exc

    from io import BytesIO

    req = urllib.request.Request(url, headers={"User-Agent": "isc-s2-measurement/1.0"})
    with urllib.request.urlopen(req, timeout=60) as res:
        data = res.read()
    reader = PdfReader(BytesIO(data))
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def is_dialogue_speaker(label: str) -> bool:
    label = re.sub(r"\s+", " ", label.strip())
    if label in {"CHAIR POWELL", "MICHELLE SMITH"}:
        return True
    return " " in label and 4 <= len(label) <= 45


def transcript_turns(text: str) -> list[tuple[str, str]]:
    header_re = re.compile(r"^[A-Z][a-z]+ \d{1,2}, \d{4}\s+Chair Powell.s Press Conference\s+FINAL$")
    speaker_re = re.compile(r"^([A-Z][A-Z .'-]{2,45})\.\s*(.*)$")
    turns: list[tuple[str, str]] = []
    speaker: str | None = None
    buf: list[str] = []

    def flush() -> None:
        nonlocal buf, speaker
        if speaker and buf:
            body = clean_paragraph(" ".join(buf))
            if body:
                turns.append((speaker, body))
        buf = []

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if header_re.match(line) or re.match(r"^Page \d+ of \d+$", line):
            continue
        if line == "Transcript of Chair Powell’s Press Conference":
            continue
        match = speaker_re.match(line)
        if match and is_dialogue_speaker(match.group(1)):
            flush()
            speaker = re.sub(r"\s+", " ", match.group(1).strip())
            remainder = match.group(2).strip()
            buf = [remainder] if remainder else []
        elif speaker:
            buf.append(line)

    flush()
    return turns


def sentence_clip(text: str, max_words: int) -> str:
    words = text.split()
    if len(words) <= max_words:
        return text
    clipped = " ".join(words[:max_words])
    boundary = max(clipped.rfind(". "), clipped.rfind("? "), clipped.rfind("! "))
    if boundary > len(clipped) * 0.65:
        return clipped[: boundary + 1].strip()
    return clipped.rstrip(" ,;:") + "."


def fed_dialogue_candidates(limit: int) -> list[Passage]:
    passages: list[Passage] = []
    for title, date_slug, source_url in FED_TRANSCRIPTS:
        try:
            turns = transcript_turns(fetch_pdf_text(source_url))
        except urllib.error.HTTPError:
            continue
        pair_ix = 0
        for ix in range(len(turns) - 1):
            question_speaker, question = turns[ix]
            answer_speaker, answer = turns[ix + 1]
            if question_speaker in {"CHAIR POWELL", "MICHELLE SMITH"}:
                continue
            if answer_speaker != "CHAIR POWELL":
                continue

            text = f"{question_speaker}. {question}\nCHAIR POWELL. {answer}"
            text = sentence_clip(clean_paragraph(text), 260)
            words = text.split()
            if len(words) < 90 or len(words) > 280:
                continue
            if not re.search(r"\b(it|this|that|these|those|we|our|you know|I think|so)\b", text, re.I):
                continue

            pair_ix += 1
            passages.append(
                Passage(
                    passage_id=f"fed_dialogue:{date_slug}:{pair_ix}",
                    title=title,
                    source_url=source_url,
                    text=text,
                )
            )
            if len(passages) >= limit:
                return passages
    return passages


def collect_passages(source_set: str, limit: int) -> list[Passage]:
    if source_set == "wikipedia":
        return passage_candidates(limit)
    if source_set == "fed_dialogue":
        return fed_dialogue_candidates(limit)
    raise RuntimeError(f"Unknown source set: {source_set}")


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


def parse_json_object(content: str) -> dict[str, Any]:
    try:
        parsed = json.loads(content)
    except json.JSONDecodeError:
        start = content.find("{")
        end = content.rfind("}")
        if start == -1 or end <= start:
            return {"parse_error": content}
        try:
            parsed = json.loads(content[start : end + 1])
        except json.JSONDecodeError:
            return {"parse_error": content}
    return parsed if isinstance(parsed, dict) else {"parse_error": content}


def rephrase_messages(passage: Passage, source_set: str) -> list[dict[str, str]]:
    if source_set == "fed_dialogue":
        system = (
            "You perform S2 fact rephrasing for an ingest-time fact compilation pipeline. "
            "Your first character must be `{`; do not reason before writing JSON. "
            "Rewrite dialogue into compact, self-contained, pronoun-free atomic facts. "
            "Remove filler, stutters, repetition, backchannels, hedging phrases, and conversational scaffolding. "
            "Resolve pronouns and back-references to explicit entities when the referent is recoverable. "
            "Preserve speaker attribution for claims, forecasts, decisions, dates, quantities, negation, and causal claims. "
            "Do not add information not present in the passage. Prefer fewer compact facts when no factual detail is lost. "
            "Return only a JSON object. Do not include analysis, markdown, comments, or text outside the JSON object."
        )
    else:
        system = (
            "You perform S2 fact rephrasing for an ingest-time fact compilation pipeline. "
            "Your first character must be `{`; do not reason before writing JSON. "
            "Rewrite the passage into compact, self-contained, pronoun-free atomic facts. "
            "Preserve names, dates, quantities, negation, definitions, and causal claims. "
            "Do not add information not present in the passage. Return only a JSON object. "
            "Do not include analysis, markdown, comments, or text outside the JSON object."
        )
    user = f"""Source title: {passage.title}
Source URL: {passage.source_url}

Passage:
{passage.text}

Return strict JSON with this schema:
{{
  "facts": ["atomic fact 1", "atomic fact 2"]
}}

The response must begin with `{{` and end with `}}`.
"""
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


def judge_messages(passage: Passage, facts: list[str], source_set: str) -> list[dict[str, str]]:
    system = (
        "You judge source fidelity for fact rephrasing. Use only the passage as ground truth. "
        "A fact is entailed if the passage directly supports it. Mark unsupported facts and "
        "major missing claims. The QA fidelity pass should be true only if the fact set would "
        "preserve answers to ordinary factual questions answerable from the passage. "
        "For dialogue passages, do not require preservation of filler, stutters, repetitions, "
        "or conversational scaffolding if the factual commitments and speaker attributions are preserved."
    )
    user = f"""Passage:
{passage.text}

Generated facts:
{json.dumps(facts, ensure_ascii=False, indent=2)}

Return strict JSON with this schema:
{{
  "entailed_fact_indices": [0],
  "unsupported_fact_indices": [],
  "missing_major_claims": [],
  "qa_fidelity_pass": true,
  "rationale": "short explanation"
}}
"""
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


def facts_from_text(text: str) -> list[str]:
    facts: list[str] = []
    in_facts_section = False
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        lower = stripped.lower()
        if "facts:" in lower or lower.startswith("possible facts"):
            in_facts_section = True
            continue
        bullet = re.match(r"^(?:[-*]|\d+[.)])\s+(.*)$", stripped)
        if bullet and (in_facts_section or lower.startswith(("-", "*")) or re.match(r"^\d+[.)]", lower)):
            fact = bullet.group(1).strip().strip('"').rstrip(",")
            if len(fact.split()) >= 4 and not fact.lower().startswith(("let's ", "we need ", "possible ")):
                facts.append(fact)

    if facts:
        return facts

    if '"facts"' in text:
        tail = text.split('"facts"', 1)[1]
        quoted = re.findall(r'"([^"\n]{20,300})"', tail)
        return [
            item.strip()
            for item in quoted
            if len(item.split()) >= 4 and item not in {"facts", "atomic fact 1", "atomic fact 2"}
        ]

    return []


def normalize_facts(parsed: dict[str, Any]) -> list[str]:
    if "parse_error" in parsed and "facts" not in parsed:
        parse_error = parsed.get("parse_error")
        if isinstance(parse_error, str):
            return facts_from_text(parse_error)
        return []

    raw = parsed.get("facts", [])
    if not raw:
        for key in ("atomic_facts", "rephrased_facts", "fact_rows", "statements"):
            if parsed.get(key):
                raw = parsed[key]
                break
    if not isinstance(raw, list):
        parse_error = parsed.get("parse_error")
        if isinstance(parse_error, str):
            return facts_from_text(parse_error)
        return []
    facts = []
    for item in raw:
        text = str(item).strip()
        if text:
            facts.append(text)
    return facts


def mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def median(values: list[float]) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    mid = len(ordered) // 2
    if len(ordered) % 2:
        return ordered[mid]
    return (ordered[mid - 1] + ordered[mid]) / 2


def percentile(values: list[float], pct: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    ix = round((len(ordered) - 1) * pct)
    return ordered[ix]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def run(args: argparse.Namespace) -> None:
    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    tokenizer_name, count_tokens = token_counter()
    passages = collect_passages(args.source_set, args.limit)
    if not passages:
        raise RuntimeError(f"No {args.source_set} passages matched the sampling constraints.")

    passage_rows = [p.__dict__ for p in passages]
    write_jsonl(out_dir / "passages.jsonl", passage_rows)

    if args.snapshot_only:
        print(f"wrote {len(passages)} passages to {out_dir / 'passages.jsonl'}")
        return

    api_key = resolve_fireworks_api_key(args.op_ref, args.op_account)
    rows: list[dict[str, Any]] = []

    for ix, passage in enumerate(passages, start=1):
        print(f"{ix}/{len(passages)} rephrasing {passage.passage_id}...", flush=True)
        started = time.perf_counter()
        rephrase_response = post_chat_completion(
            api_key,
            args.model,
            rephrase_messages(passage, args.source_set),
            args.max_tokens,
            args.temperature,
            args.timeout,
        )
        rephrase_ms = round((time.perf_counter() - started) * 1000, 1)
        rephrase_content = rephrase_response.get("choices", [{}])[0].get("message", {}).get("content", "")
        rephrase_parsed = parse_json_object(rephrase_content)
        facts = normalize_facts(rephrase_parsed)

        print(f"{ix}/{len(passages)} judging {passage.passage_id} ({len(facts)} facts)...", flush=True)
        started = time.perf_counter()
        judge_response = post_chat_completion(
            api_key,
            args.judge_model,
            judge_messages(passage, facts, args.source_set),
            args.max_tokens,
            0.0,
            args.timeout,
        )
        judge_ms = round((time.perf_counter() - started) * 1000, 1)
        judge_content = judge_response.get("choices", [{}])[0].get("message", {}).get("content", "")
        judge = parse_json_object(judge_content)

        original_tokens = int(count_tokens(passage.text))
        facts_text = "\n".join(facts)
        fact_tokens = int(count_tokens(facts_text))
        unsupported = judge.get("unsupported_fact_indices", [])
        entailed = judge.get("entailed_fact_indices", [])
        missing = judge.get("missing_major_claims", [])
        if not isinstance(unsupported, list):
            unsupported = []
        if not isinstance(entailed, list):
            entailed = []
        if not isinstance(missing, list):
            missing = []

        row = {
            "passage_id": passage.passage_id,
            "title": passage.title,
            "source_url": passage.source_url,
            "original_tokens": original_tokens,
            "fact_tokens": fact_tokens,
            "compression_ratio": round(fact_tokens / original_tokens, 4) if original_tokens else None,
            "fact_count": len(facts),
            "entailed_fact_count": len(entailed),
            "unsupported_fact_count": len(unsupported),
            "missing_major_claim_count": len(missing),
            "qa_fidelity_pass": bool(judge.get("qa_fidelity_pass")),
            "rephrase_latency_ms": rephrase_ms,
            "judge_latency_ms": judge_ms,
            "facts": facts,
            "judge": judge,
            "rephrase_raw_content": rephrase_content,
            "judge_raw_content": judge_content,
        }
        rows.append(row)

    write_jsonl(out_dir / "answers.jsonl", rows)

    csv_fields = [
        "passage_id",
        "title",
        "source_url",
        "original_tokens",
        "fact_tokens",
        "compression_ratio",
        "fact_count",
        "entailed_fact_count",
        "unsupported_fact_count",
        "missing_major_claim_count",
        "qa_fidelity_pass",
        "rephrase_latency_ms",
        "judge_latency_ms",
    ]
    with (out_dir / "scores.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=csv_fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row[field] for field in csv_fields})

    ratios = [float(row["compression_ratio"]) for row in rows if row["compression_ratio"] is not None]
    original_total = sum(int(row["original_tokens"]) for row in rows)
    fact_total = sum(int(row["fact_tokens"]) for row in rows)
    fact_count = sum(int(row["fact_count"]) for row in rows)
    unsupported_count = sum(int(row["unsupported_fact_count"]) for row in rows)
    missing_count = sum(int(row["missing_major_claim_count"]) for row in rows)
    qa_pass_count = sum(1 for row in rows if row["qa_fidelity_pass"])
    summary = {
        "date": datetime.now(UTC).date().isoformat(),
        "passages": len(rows),
        "source_set": args.source_set,
        "source": SOURCE_LABELS[args.source_set],
        "model": args.model,
        "judge_model": args.judge_model,
        "tokenizer": tokenizer_name,
        "original_tokens": original_total,
        "fact_tokens": fact_total,
        "overall_compression_ratio": round(fact_total / original_total, 4) if original_total else None,
        "mean_compression_ratio": round(mean(ratios), 4),
        "median_compression_ratio": round(median(ratios), 4),
        "min_compression_ratio": round(min(ratios), 4) if ratios else None,
        "max_compression_ratio": round(max(ratios), 4) if ratios else None,
        "p25_compression_ratio": round(percentile(ratios, 0.25), 4),
        "p75_compression_ratio": round(percentile(ratios, 0.75), 4),
        "facts": fact_count,
        "unsupported_facts": unsupported_count,
        "entailed_fact_rate": round((fact_count - unsupported_count) / fact_count, 4) if fact_count else None,
        "passages_with_missing_major_claims": sum(1 for row in rows if row["missing_major_claim_count"]),
        "missing_major_claims": missing_count,
        "qa_fidelity_passages": qa_pass_count,
        "qa_fidelity_rate": round(qa_pass_count / len(rows), 4) if rows else None,
        "mean_rephrase_latency_ms": round(mean([float(row["rephrase_latency_ms"]) for row in rows]), 1),
        "mean_judge_latency_ms": round(mean([float(row["judge_latency_ms"]) for row in rows]), 1),
    }
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")

    if summary["overall_compression_ratio"] <= 1:
        s2_sentence = (
            f'On {summary["passages"]} {summary["source"]}, S2 reduced token count to '
            f'{summary["overall_compression_ratio"]:.2f}x of the original passage text using '
            f'`{summary["tokenizer"]}`, with {summary["entailed_fact_rate"]:.1%} of generated '
            f'facts judged source-entailed and {summary["qa_fidelity_rate"]:.1%} passage-level '
            "QA-fidelity pass rate."
        )
    else:
        s2_sentence = (
            f'On {summary["passages"]} {summary["source"]}, S2 fact rephrasing produced '
            f'{summary["overall_compression_ratio"]:.2f}x as many tokens as the original passage '
            f'text using `{summary["tokenizer"]}`, with {summary["entailed_fact_rate"]:.1%} of '
            f'generated facts judged source-entailed and {summary["qa_fidelity_rate"]:.1%} '
            "passage-level QA-fidelity pass rate."
        )

    summary_md = f"""# S2 Fact Rephrasing Measurement

Passage set: {summary["passages"]} {summary["source"]}.

Token counter: `{summary["tokenizer"]}`.

| Metric | Value |
| :-- | --: |
| Original tokens | {summary["original_tokens"]:,} |
| S2 fact tokens | {summary["fact_tokens"]:,} |
| Overall compression ratio | {summary["overall_compression_ratio"]:.4f} |
| Median passage compression ratio | {summary["median_compression_ratio"]:.4f} |
| Compression ratio range | {summary["min_compression_ratio"]:.4f}-{summary["max_compression_ratio"]:.4f} |
| Generated facts | {summary["facts"]:,} |
| Entailed fact rate | {summary["entailed_fact_rate"]:.4f} |
| QA fidelity rate | {summary["qa_fidelity_rate"]:.4f} |
| Passages with missing major claims | {summary["passages_with_missing_major_claims"]} |

Suggested manuscript sentence:

> {s2_sentence}
"""
    (out_dir / "summary.md").write_text(summary_md)

    manifest = {
        "experiment": "S2 fact rephrasing compression and fidelity",
        "command": " ".join(sys.argv),
        "source_set": args.source_set,
        "outputs": ["passages.jsonl", "answers.jsonl", "scores.csv", "summary.json", "summary.md"],
        "credential_source": "FIREWORKS_API_KEY, LLM_GATEWAY_DEFAULT_FIREWORKS_API_KEY, or --op-ref <1Password secret reference>",
    }
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Measure S2 fact rephrasing on real passages.")
    parser.add_argument("--source-set", choices=sorted(SOURCE_LABELS), default="wikipedia")
    parser.add_argument("--limit", type=int, default=30)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--judge-model", default=DEFAULT_MODEL)
    parser.add_argument("--max-tokens", type=int, default=5000)
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--timeout", type=float, default=120.0)
    parser.add_argument("--op-ref", default=None)
    parser.add_argument("--op-account", default=None)
    parser.add_argument("--snapshot-only", action="store_true")
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path(__file__).resolve().parent / "results" / "s2-real-passages",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        run(args)
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
