#!/usr/bin/env python3
"""Summarize token usage for one Codex thread and its collaboration descendants.

Discovery reads only the first session_meta line of candidate logs. Full JSONL
content is read only for the root session and logs matched to collaboration
spawn_agent calls by timestamp. Token usage records are cumulative snapshots;
the script keeps the latest thread_token_usage snapshot per thread.
"""

from __future__ import annotations

import argparse
import json
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_ROOT_SESSION = Path(
    "/Users/harjas/.codex/sessions/2026/10/08/"
    "rollout-2026-10-08T19-50-25-01a11aeb-d321-71e3-a5ef-ecd7e0e32bae.jsonl"
)
DEFAULT_SESSIONS_ROOT = Path("/Users/harjas/.codex/sessions")
MODEL_RATES_USD_PER_MILLION = {
    # Supplied standard rate card. Prices are estimates, not billing records.
    "gpt-6.1-sol": {"input": 2.0, "cached_input": 0.10, "output": 10.0},
    "gpt-6-sol": {"input": 2.0, "cached_input": 0.10, "output": 10.0},
    "gpt-6-luna": {"input": 0.10, "cached_input": 0.01, "output": 0.50},
    "gpt-6-astra": {"input": 10.0, "cached_input": 1.0, "output": 50.0},
}
TOKEN_FIELDS = (
    "input_tokens",
    "cached_input_tokens",
    "cache_write_input_tokens",
    "output_tokens",
    "reasoning_output_tokens",
    "total_tokens",
)


def parse_json_line(line: str) -> dict[str, Any] | None:
    try:
        value = json.loads(line)
    except (json.JSONDecodeError, TypeError):
        return None
    return value if isinstance(value, dict) else None


def read_session_meta(path: Path) -> dict[str, Any] | None:
    """Read only the first line, and return only non-content identifiers."""
    try:
        with path.open("r", encoding="utf-8") as stream:
            record = parse_json_line(stream.readline())
    except OSError:
        return None
    if not record or record.get("type") != "session_meta":
        return None
    payload = record.get("payload")
    if not isinstance(payload, dict):
        return None
    return {
        "id": payload.get("id"),
        "session_id": payload.get("session_id"),
        "timestamp": payload.get("timestamp") or record.get("timestamp"),
    }


def iso_time(value: Any) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def root_date_from_path(path: Path) -> date:
    # Codex rollout filenames begin rollout-YYYY-MM-DDT...
    prefix = path.name.removeprefix("rollout-")[:10]
    return date.fromisoformat(prefix)


def discover_candidate_logs(sessions_root: Path, first_date: date) -> tuple[list[dict[str, Any]], int]:
    """Scan only session_meta headers from the root date onward."""
    candidates: list[dict[str, Any]] = []
    scanned = 0
    for path in sessions_root.rglob("rollout-*.jsonl"):
        try:
            candidate_date = root_date_from_path(path)
        except ValueError:
            continue
        if candidate_date < first_date:
            continue
        scanned += 1
        meta = read_session_meta(path)
        if meta and isinstance(meta.get("id"), str):
            candidates.append({**meta, "path": path})
    return candidates, scanned


def read_records(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    try:
        with path.open("r", encoding="utf-8") as stream:
            for line in stream:
                record = parse_json_line(line)
                if record is not None:
                    records.append(record)
    except OSError:
        return records
    return records


def parse_spawn_args(payload: dict[str, Any]) -> dict[str, Any] | None:
    arguments = payload.get("arguments")
    if isinstance(arguments, str):
        try:
            arguments = json.loads(arguments)
        except json.JSONDecodeError:
            return None
    if not isinstance(arguments, dict):
        return None
    # Deliberately discard the message/prompt and retain assignment metadata only.
    return {
        "task_name": arguments.get("task_name"),
        "requested_model": arguments.get("model"),
        "requested_effort": arguments.get("reasoning_effort"),
    }


def spawn_calls(records: list[dict[str, Any]], parent_thread_id: str) -> list[dict[str, Any]]:
    calls = []
    for record in records:
        payload = record.get("payload", {})
        if not isinstance(payload, dict) or record.get("type") != "response_item":
            continue
        if payload.get("type") != "function_call" or payload.get("name") != "spawn_agent":
            continue
        args = parse_spawn_args(payload)
        if args is None:
            continue
        args.update({
            "call_id": payload.get("call_id"),
            "timestamp": record.get("timestamp"),
            "parent_thread_id": parent_thread_id,
        })
        calls.append(args)
    return sorted(calls, key=lambda item: item.get("timestamp") or "")


def match_child(call: dict[str, Any], candidates: list[dict[str, Any]],
                used_ids: set[str], root_id: str, max_seconds: float = 600.0) -> dict[str, Any] | None:
    call_time = iso_time(call.get("timestamp"))
    possible = []
    for candidate in candidates:
        candidate_id = candidate.get("id")
        if not candidate_id or candidate_id == root_id or candidate_id in used_ids:
            continue
        # Codex descendants commonly inherit the root session_id. Some runtimes
        # instead record the direct parent thread id.
        if candidate.get("session_id") not in (root_id, call.get("parent_thread_id")):
            continue
        created = iso_time(candidate.get("timestamp"))
        if call_time and created:
            delta = (created - call_time).total_seconds()
            if delta < -1.0 or delta > max_seconds:
                continue
            possible.append((abs(delta), created, candidate))
        elif created:
            possible.append((0.0, created, candidate))
    if not possible:
        return None
    possible.sort(key=lambda row: (row[0], row[1]))
    return possible[0][2]


def discover_collaboration_tree(root_path: Path, root_id: str,
                                candidates: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    by_id: dict[str, list[dict[str, Any]]] = {}
    for candidate in candidates:
        by_id.setdefault(candidate["id"], []).append(candidate)
    root_entries = by_id.get(root_id, [])
    if not any(entry["path"].resolve() == root_path.resolve() for entry in root_entries):
        meta = read_session_meta(root_path) or {"id": root_id, "session_id": root_id, "timestamp": None}
        root_entries.append({**meta, "path": root_path})

    selected: dict[str, dict[str, Any]] = {
        root_id: {"thread_id": root_id, "root": True, "paths": [root_path],
                  "session_id": root_id, "timestamp": next((x.get("timestamp") for x in root_entries), None)}
    }
    used_ids = {root_id}
    pending = [root_id]
    launches: list[dict[str, Any]] = []
    processed = set()

    while pending:
        parent_id = pending.pop(0)
        if parent_id in processed:
            continue
        processed.add(parent_id)
        parent = selected[parent_id]
        all_calls = []
        for path in parent["paths"]:
            all_calls.extend(spawn_calls(read_records(path), parent_id))
        # A call can appear in resumed/duplicated logs; call_id prevents a repeat.
        unique_calls = {}
        for call in all_calls:
            unique_calls[call.get("call_id") or (call.get("timestamp"), call.get("task_name"))] = call
        for call in sorted(unique_calls.values(), key=lambda item: item.get("timestamp") or ""):
            child_meta = match_child(call, candidates, used_ids, root_id)
            launch = dict(call)
            launch["matched_thread_id"] = child_meta["id"] if child_meta else None
            launch["match_status"] = "matched_by_launch_time" if child_meta else "log_not_found_yet"
            launches.append(launch)
            if child_meta is None:
                continue
            child_id = child_meta["id"]
            used_ids.add(child_id)
            same_id_paths = [entry["path"] for entry in by_id.get(child_id, [])
                             if entry.get("session_id") in (root_id, parent_id)]
            if child_meta["path"] not in same_id_paths:
                same_id_paths.append(child_meta["path"])
            selected[child_id] = {
                "thread_id": child_id,
                "root": False,
                "paths": sorted(set(same_id_paths), key=str),
                "session_id": child_meta.get("session_id"),
                "timestamp": child_meta.get("timestamp"),
                "task_name": call.get("task_name"),
                "requested_model": call.get("requested_model"),
                "requested_effort": call.get("requested_effort"),
                "parent_thread_id": parent_id,
            }
            pending.append(child_id)
    return list(selected.values()), launches


def normalized_usage(value: Any) -> dict[str, int] | None:
    if not isinstance(value, dict):
        return None
    output = {}
    for key in TOKEN_FIELDS:
        try:
            output[key] = max(0, int(value.get(key, 0) or 0))
        except (TypeError, ValueError):
            output[key] = 0
    return output


def analyze_thread(thread: dict[str, Any]) -> dict[str, Any]:
    contexts: set[tuple[str | None, str | None]] = set()
    record_snapshots: list[tuple[str, dict[str, int]]] = []
    fallback_snapshots: list[tuple[str, dict[str, int]]] = []
    record_count = 0
    event_count = 0
    for path in thread["paths"]:
        for ordinal, record in enumerate(read_records(path)):
            payload = record.get("payload", {})
            if not isinstance(payload, dict):
                continue
            if record.get("type") == "turn_context":
                contexts.add((payload.get("model"), payload.get("effort")))
            timestamp = record.get("timestamp") or f"{path.name}:{ordinal:012d}"
            if record.get("type") == "token_usage_record":
                record_count += 1
                usage = normalized_usage(payload.get("thread_token_usage"))
                if usage is not None:
                    record_snapshots.append((str(timestamp), usage))
            elif record.get("type") == "event_msg" and payload.get("type") == "token_count":
                event_count += 1
                info = payload.get("info", {})
                usage = normalized_usage(info.get("total_token_usage") if isinstance(info, dict) else None)
                if usage is not None:
                    fallback_snapshots.append((str(timestamp), usage))

    contexts_sorted = sorted(contexts, key=lambda pair: (pair[0] or "", pair[1] or ""))
    observed_models = sorted({model for model, _ in contexts_sorted if model})
    observed_efforts = sorted({effort for _, effort in contexts_sorted if effort})
    if record_snapshots:
        source = "latest token_usage_record.thread_token_usage snapshot"
        snapshot = max(record_snapshots, key=lambda row: row[0])[1]
        status = "observed"
    elif fallback_snapshots:
        source = "latest event_msg.token_count.info.total_token_usage snapshot"
        snapshot = max(fallback_snapshots, key=lambda row: row[0])[1]
        status = "fallback_snapshot"
    else:
        source = None
        snapshot = {field: 0 for field in TOKEN_FIELDS}
        status = "no_snapshot_yet"

    model = observed_models[0] if len(observed_models) == 1 else None
    requested_model = thread.get("requested_model")
    requested_effort = thread.get("requested_effort")
    model_matches = (None if thread.get("root") or not requested_model else model == requested_model)
    effort_matches = (None if thread.get("root") or not requested_effort else
                      bool(observed_efforts) and all(effort == requested_effort for effort in observed_efforts))
    input_tokens = snapshot["input_tokens"]
    cached_tokens = snapshot["cached_input_tokens"]
    uncached_tokens = max(0, input_tokens - cached_tokens)
    output_tokens = snapshot["output_tokens"]
    reasoning_tokens = snapshot["reasoning_output_tokens"]
    rates = MODEL_RATES_USD_PER_MILLION.get(model) if model else None
    if rates and status != "no_snapshot_yet":
        estimated_cost = (
            uncached_tokens * rates["input"]
            + cached_tokens * rates["cached_input"]
            + output_tokens * rates["output"]
        ) / 1_000_000
    else:
        estimated_cost = None

    result = {
        "thread_id": thread["thread_id"],
        "root_thread": thread.get("root", False),
        "task_name": "root" if thread.get("root") else thread.get("task_name"),
        "parent_thread_id": thread.get("parent_thread_id"),
        "requested_model": requested_model,
        "requested_effort": requested_effort,
        "turn_contexts": [{"model": model, "effort": effort} for model, effort in contexts_sorted],
        "observed_models": observed_models,
        "observed_efforts": observed_efforts,
        "requested_model_matches_turn_context": model_matches,
        "requested_effort_matches_turn_context": effort_matches,
        "usage_status": status,
        "usage_snapshot_source": source,
        "token_usage_record_count": record_count,
        "token_count_event_count_ignored_for_double_counting": event_count,
        "usage": snapshot,
        "uncached_input_tokens_derived": uncached_tokens,
        "estimated_cost_usd_from_supplied_rates": round(estimated_cost, 8) if estimated_cost is not None else None,
        "log_paths": [str(path) for path in thread["paths"]],
    }
    return result


def add_totals(thread_rows: list[dict[str, Any]]) -> dict[str, Any]:
    sums = {field: sum(row["usage"].get(field, 0) for row in thread_rows) for field in TOKEN_FIELDS}
    sums["uncached_input_tokens_derived"] = sum(row["uncached_input_tokens_derived"] for row in thread_rows)
    priced_rows = [row for row in thread_rows if row["estimated_cost_usd_from_supplied_rates"] is not None]
    cost = sum(row["estimated_cost_usd_from_supplied_rates"] for row in priced_rows)
    return {
        "thread_count": len(thread_rows),
        "threads_with_usage_snapshot": sum(row["usage_status"] != "no_snapshot_yet" for row in thread_rows),
        "threads_without_usage_snapshot": sum(row["usage_status"] == "no_snapshot_yet" for row in thread_rows),
        **sums,
        "output_reasoning_is_subset": True,
        "estimated_cost_usd_from_supplied_rates": round(cost, 8),
        "unpriced_or_ambiguous_cost_threads": len(thread_rows) - len(priced_rows),
        "sol_uncached_input_rate_equivalent_million_tokens": round(cost / 2.0, 8),
    }


def render_table(rows: list[dict[str, Any]], totals: dict[str, Any]) -> str:
    def fmt_int(value: Any) -> str:
        return f"{value:,}" if isinstance(value, int) else "—"

    lines = [
        "| Thread / task | Configured model / effort | Input | Cached | Output (reasoning subset) | Est. USD |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for row in rows:
        model = ", ".join(row["observed_models"]) or "unknown"
        efforts = ", ".join(row["observed_efforts"]) or "unknown"
        label = "root" if row["root_thread"] else (row["task_name"] or "descendant")
        output = fmt_int(row["usage"]["output_tokens"])
        reason = fmt_int(row["usage"]["reasoning_output_tokens"])
        output_cell = f"{output} ({reason})"
        usd = row["estimated_cost_usd_from_supplied_rates"]
        usd_cell = f"${usd:.4f}" if usd is not None else "—"
        lines.append(
            f"| {label} | {model} / {efforts} | {fmt_int(row['usage']['input_tokens'])} "
            f"| {fmt_int(row['usage']['cached_input_tokens'])} | {output_cell} | {usd_cell} |"
        )
    cost = totals["estimated_cost_usd_from_supplied_rates"]
    lines.append(
        f"| **Total, root included** | {totals['thread_count']} threads | "
        f"{fmt_int(totals['input_tokens'])} | {fmt_int(totals['cached_input_tokens'])} | "
        f"{fmt_int(totals['output_tokens'])} ({fmt_int(totals['reasoning_output_tokens'])}) | ${cost:.4f} |"
    )
    lines += [
        "",
        "Usage is the latest cumulative thread snapshot per log, never the sum of repeated snapshots. Cached input is a subset of input; reasoning output is a subset of output. USD values apply the supplied standard rate card and are estimates, not billing records. `turn_context` records the configured runtime model and effort; it does not attest backend identity.",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root-session", type=Path, default=DEFAULT_ROOT_SESSION)
    parser.add_argument("--sessions-root", type=Path, default=DEFAULT_SESSIONS_ROOT)
    parser.add_argument("--output-json", type=Path, default=Path(__file__).with_name("resource_usage.json"))
    parser.add_argument("--output-table", type=Path, default=Path(__file__).with_name("resource_usage.md"))
    args = parser.parse_args()

    root_path = args.root_session.expanduser().resolve()
    root_meta = read_session_meta(root_path)
    if not root_meta or not isinstance(root_meta.get("id"), str):
        parser.error("root session must begin with a valid session_meta record")
    root_id = root_meta["id"]
    candidates, scanned = discover_candidate_logs(args.sessions_root.expanduser().resolve(), root_date_from_path(root_path))
    selected, launches = discover_collaboration_tree(root_path, root_id, candidates)
    rows = [analyze_thread(thread) for thread in selected]
    rows.sort(key=lambda row: (not row["root_thread"], row["task_name"] or "", row["thread_id"]))
    totals = add_totals(rows)
    assignment_counts: dict[str, int] = {}
    for launch in launches:
        key = f"{launch.get('requested_model') or 'unspecified'}/{launch.get('requested_effort') or 'unspecified'}"
        assignment_counts[key] = assignment_counts.get(key, 0) + 1
    mismatches = [
        {"task_name": row["task_name"], "thread_id": row["thread_id"],
         "model_match": row["requested_model_matches_turn_context"],
         "effort_match": row["requested_effort_matches_turn_context"]}
        for row in rows if not row["root_thread"]
        and (row["requested_model_matches_turn_context"] is False
             or row["requested_effort_matches_turn_context"] is False)
    ]
    report = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "scope": {
            "root_thread_id": root_id,
            "root_session_log": str(root_path),
            "collaboration_descendants": totals["thread_count"] - 1,
            "session_discovery": {
                "candidate_headers_scanned_from_root_date_forward": scanned,
                "header_content_read": "first session_meta JSONL record only",
                "full_jsonl_read": "root and logs matched to collaboration spawn_agent calls only",
                "child_match_rule": "session metadata timestamp nearest after launch, within ten minutes, with inherited root/direct-parent session_id",
            },
        },
        "model_identity": {
            "evidence": "session turn_context model/effort fields",
            "interpretation": "configured runtime model and effort only; backend identity is not independently attested",
        },
        "pricing": {
            "standard_rates_usd_per_million": MODEL_RATES_USD_PER_MILLION,
            "formula": "(input_tokens - cached_input_tokens)*input_rate + cached_input_tokens*cached_input_rate + output_tokens*output_rate",
            "notes": [
                "Supplied rate card produces estimates, not actual billing.",
                "Reasoning output is reported separately but is already included in output_tokens; it is not added again.",
                "cache_write_input_tokens is preserved from the usage record and not added separately because it is a detail of input usage; all observed counts in this run are checked in the per-thread rows.",
                "Cost is unknown for missing snapshots or threads with multiple configured models because cumulative tokens cannot be split by model from these records.",
            ],
            "sol_uncached_input_rate_equivalent": "estimated USD divided by supplied Sol input rate of $2 per million uncached input tokens; this is a rate ratio, not a platform quota unit",
        },
        "assignment_validation": {
            "launch_count": len(launches),
            "matched_launch_count": sum(launch.get("matched_thread_id") is not None for launch in launches),
            "requested_assignment_counts": assignment_counts,
            "turn_context_mismatches": mismatches,
            "launches_without_log_yet": [
                {k: launch.get(k) for k in ("task_name", "requested_model", "requested_effort", "timestamp")}
                for launch in launches if launch.get("matched_thread_id") is None
            ],
        },
        "aggregation": {
            "rule": "latest token_usage_record.thread_token_usage snapshot per thread; event_msg token_count snapshots are fallback only and are not added to token_usage_record counts",
            "totals_root_included": totals,
            "threads": rows,
            "collaboration_launches": [
                {k: launch.get(k) for k in ("parent_thread_id", "task_name", "requested_model", "requested_effort", "timestamp", "matched_thread_id", "match_status")}
                for launch in launches
            ],
        },
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_table.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    table = render_table(rows, totals)
    args.output_table.write_text(table, encoding="utf-8")
    print(table, end="")
    print(f"JSON: {args.output_json}")
    print(f"Table: {args.output_table}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
