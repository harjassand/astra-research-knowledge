#!/usr/bin/env python3
"""Summarize token usage for one Codex session and its descendant agents.

Discovery reads only the first JSONL record (session_meta) from sibling session
logs to establish parentage. Full records are read only from the requested root
session and sessions proven to be descendants by session_meta or dispatch IDs.
No message, prompt, tool input, or tool output content is emitted.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_ROOT = Path(
    "/Users/harjas/.codex/sessions/2026/10/09/"
    "rollout-2026-10-09T00-43-59-01a11bf8-98a4-7342-b565-17a798a3759f.jsonl"
)

# Standard short-context rates, USD per million tokens. These are the rates
# supplied for this audit from the official comparison page, not billing data.
PRICE_SOURCE = "https://developers.openai.com/api/docs/models/compare"
RATES_USD_PER_MTOK = {
    "gpt-6-astra": {"input": 10.0, "cached_input": 1.0, "output": 50.0},
    "gpt-6.1-sol": {"input": 2.0, "cached_input": 0.1, "output": 10.0},
    "gpt-6-sol": {"input": 2.0, "cached_input": 0.1, "output": 10.0},
    "gpt-6-luna": {"input": 0.1, "cached_input": 0.01, "output": 0.5},
}
PRICE_SCALE = 1_000_000
CONCURRENT_SOL_MAX_CEILING = 30.0
ACTIVE_RESERVATION_WEIGHTS = {
    "gpt-6-astra": 10.0,
    "gpt-6.1-sol": 1.0,
    "gpt-6-sol": 1.0,
    "gpt-6-luna": 0.1,
}


def _as_int(value: Any) -> int:
    try:
        return max(0, int(value))
    except (TypeError, ValueError, OverflowError):
        return 0


def _read_meta(path: Path) -> dict[str, Any] | None:
    """Read only the first record, which is session metadata."""
    try:
        with path.open("r", encoding="utf-8") as handle:
            first = handle.readline()
        row = json.loads(first)
    except (OSError, UnicodeError, json.JSONDecodeError):
        return None
    if row.get("type") != "session_meta" or not isinstance(row.get("payload"), dict):
        return None
    return row["payload"]


def _nested_parent_ids(value: Any) -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        parent = value.get("parent_thread_id")
        if isinstance(parent, str) and parent:
            found.add(parent)
        for child in value.values():
            found.update(_nested_parent_ids(child))
    elif isinstance(value, list):
        for child in value:
            found.update(_nested_parent_ids(child))
    return found


def _meta_id(meta: dict[str, Any]) -> str | None:
    value = meta.get("id") or meta.get("session_id")
    return value if isinstance(value, str) and value else None


def _meta_parents(meta: dict[str, Any]) -> set[str]:
    parents = _nested_parent_ids(meta)
    # Older subagent metadata can identify its parent only through session_id.
    own_id = _meta_id(meta)
    session_id = meta.get("session_id")
    if not parents and isinstance(session_id, str) and session_id and session_id != own_id:
        parents.add(session_id)
    return parents


def _dispatch_ids(path: Path | None) -> set[str]:
    if path is None or not path.exists():
        return set()
    raw = path.read_text(encoding="utf-8")
    try:
        value = json.loads(raw)
    except json.JSONDecodeError:
        # Plain-text dispatch files may list one UUID/thread ID per line.
        return {
            item.strip().strip('"\'')
            for item in raw.splitlines()
            if re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{7,}", item.strip().strip('"\''))
        }

    ids: set[str] = set()
    id_keys = {
        "id",
        "session_id",
        "thread_id",
        "agent_id",
        "sessionId",
        "threadId",
        "agentId",
        "root_session_id",
        "descendant_session_id",
    }
    many_keys = {"session_ids", "thread_ids", "agent_ids", "descendant_ids", "descendants"}

    def visit(node: Any, key: str | None = None) -> None:
        if isinstance(node, dict):
            for child_key, child in node.items():
                visit(child, child_key)
        elif isinstance(node, list):
            for child in node:
                visit(child, key)
        elif isinstance(node, str) and key in id_keys | many_keys:
            if re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{7,}", node):
                ids.add(node)

    visit(value)
    return ids


def _active_ids(path: Path | None) -> set[str]:
    """Read the active roster, refreshed from live agent status before each run."""
    if path is None or not path.exists():
        return set()
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError, UnicodeError):
        return set()
    ids: set[str] = set()
    active_keys = {"active_session_ids", "active_thread_ids", "active_agent_ids", "active_ids"}

    def visit(node: Any, key: str | None = None) -> None:
        if isinstance(node, dict):
            for child_key, child in node.items():
                visit(child, child_key)
        elif isinstance(node, list):
            for child in node:
                visit(child, key)
        elif isinstance(node, str) and key in active_keys:
            if re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{7,}", node):
                ids.add(node)

    visit(value)
    return ids


def _latest_context_and_usage(path: Path) -> dict[str, Any]:
    context: dict[str, Any] | None = None
    usage: dict[str, Any] | None = None
    usage_source: str | None = None
    usage_record_time: str | None = None
    usage_thread_id: str | None = None
    usage_session_id: str | None = None
    record_count = 0
    try:
        with path.open("r", encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, start=1):
                try:
                    row = json.loads(line)
                except json.JSONDecodeError:
                    continue
                kind = row.get("type")
                payload = row.get("payload") or {}
                if kind == "turn_context" and isinstance(payload, dict):
                    context = payload
                elif kind == "token_usage_record" and isinstance(payload, dict):
                    record_count += 1
                    # thread_token_usage is the cumulative total in the current
                    # JSONL schema; usage is only the latest response delta.
                    for field in (
                        "thread_token_usage",
                        "total_token_usage",
                        "turn_token_usage",
                        "usage",
                    ):
                        candidate = payload.get(field)
                        if isinstance(candidate, dict):
                            usage = candidate
                            usage_source = field
                            usage_record_time = row.get("timestamp")
                            usage_thread_id = payload.get("thread_id")
                            usage_session_id = payload.get("session_id")
                            break
                    if usage is None:
                        nested = payload.get("usage")
                        if isinstance(nested, dict):
                            for field in ("thread_token_usage", "total_token_usage", "turn_token_usage"):
                                candidate = nested.get(field)
                                if isinstance(candidate, dict):
                                    usage = candidate
                                    usage_source = f"usage.{field}"
                                    usage_record_time = row.get("timestamp")
                                    usage_thread_id = payload.get("thread_id")
                                    usage_session_id = payload.get("session_id")
                                    break
    except OSError as error:
        return {"error": str(error), "path": str(path)}

    if context is None:
        context = {}
    if usage is None:
        usage = {}

    tokens = {
        "input_tokens": _as_int(usage.get("input_tokens")),
        "cached_input_tokens": _as_int(usage.get("cached_input_tokens")),
        "cache_write_input_tokens": _as_int(usage.get("cache_write_input_tokens")),
        "output_tokens": _as_int(usage.get("output_tokens")),
        "reasoning_output_tokens": _as_int(usage.get("reasoning_output_tokens")),
        "reported_total_tokens": _as_int(usage.get("total_tokens")),
    }
    tokens["uncached_input_tokens"] = max(
        0, tokens["input_tokens"] - tokens["cached_input_tokens"]
    )
    token_warnings: list[str] = []
    if tokens["cached_input_tokens"] > tokens["input_tokens"]:
        token_warnings.append("cached_input_tokens exceeds input_tokens")
    if tokens["reasoning_output_tokens"] > tokens["output_tokens"]:
        token_warnings.append("reasoning_output_tokens exceeds output_tokens")

    return {
        "path": str(path),
        "session_meta_id": None,
        "model": context.get("model"),
        "effort": context.get("effort"),
        "turn_id": context.get("turn_id"),
        "root_turn_id": context.get("root_turn_id"),
        "token_usage_source": usage_source,
        "token_usage_record_timestamp": usage_record_time,
        "token_usage_record_count": record_count,
        "token_usage_thread_id": usage_thread_id,
        "token_usage_session_id": usage_session_id,
        "tokens": tokens,
        "warnings": token_warnings,
    }


def _rates_for_model(model: Any) -> tuple[str | None, dict[str, float] | None]:
    if not isinstance(model, str):
        return None, None
    normalized = model.lower()
    if normalized in RATES_USD_PER_MTOK:
        return normalized, RATES_USD_PER_MTOK[normalized]
    if "astra" in normalized:
        return "gpt-6-astra", RATES_USD_PER_MTOK["gpt-6-astra"]
    if "luna" in normalized:
        return "gpt-6-luna", RATES_USD_PER_MTOK["gpt-6-luna"]
    if "sol" in normalized:
        return "gpt-6.1-sol", RATES_USD_PER_MTOK["gpt-6.1-sol"]
    return None, None


def _reservation_family(model: Any) -> str | None:
    key, _ = _rates_for_model(model)
    if key == "gpt-6-astra":
        return key
    if key in ("gpt-6-sol", "gpt-6.1-sol"):
        return "gpt-6.1-sol"
    if key == "gpt-6-luna":
        return key
    return None


def _price_proxy(session: dict[str, Any]) -> dict[str, Any]:
    model_key, rates = _rates_for_model(session.get("model"))
    if rates is None:
        return {
            "status": "unpriced_model",
            "pricing_family": None,
            "usd_proxy": None,
        }

    tokens = session["tokens"]
    uncached = tokens["uncached_input_tokens"]
    cached = tokens["cached_input_tokens"]
    output = tokens["output_tokens"]
    dollars = (
        uncached * rates["input"]
        + cached * rates["cached_input"]
        + output * rates["output"]
    ) / PRICE_SCALE
    return {
        "status": "estimated_from_standard_short_context_rates",
        "pricing_family": model_key,
        "usd_proxy": round(dollars, 9),
        "components_usd_proxy": {
            "uncached_input": round(uncached * rates["input"] / PRICE_SCALE, 9),
            "cached_input": round(cached * rates["cached_input"] / PRICE_SCALE, 9),
            "output_including_reasoning": round(output * rates["output"] / PRICE_SCALE, 9),
        },
    }


def _dispatch_requests(root_path: Path) -> list[dict[str, Any]]:
    """Extract safe dispatch metadata without retaining prompt/message fields."""
    requests: list[dict[str, Any]] = []
    try:
        with root_path.open("r", encoding="utf-8") as handle:
            for line in handle:
                try:
                    row = json.loads(line)
                except json.JSONDecodeError:
                    continue
                payload = row.get("payload") or {}
                if (
                    row.get("type") != "response_item"
                    or payload.get("type") != "function_call"
                    or payload.get("name") != "spawn_agent"
                ):
                    continue
                arguments = payload.get("arguments")
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        arguments = {}
                if not isinstance(arguments, dict):
                    arguments = {}
                # Deliberately discard the free-form task message and all other
                # fields. It can contain prompts or private source material.
                task_name = arguments.get("task_name")
                requests.append(
                    {
                        "task_name": task_name if isinstance(task_name, str) else None,
                        "requested_model": arguments.get("model")
                        if isinstance(arguments.get("model"), str)
                        else None,
                        "requested_effort": arguments.get("reasoning_effort")
                        if isinstance(arguments.get("reasoning_effort"), str)
                        else None,
                    }
                )
    except OSError:
        return []
    return requests


def _load_candidate_metadata(
    directory: Path, root_path: Path, explicit_ids: set[str]
) -> tuple[dict[str, tuple[Path, dict[str, Any]]], int]:
    candidates: dict[str, tuple[Path, dict[str, Any]]] = {}
    scanned = 0
    try:
        if explicit_ids:
            # With an ID dispatch file, resolve only those filenames; do not
            # open metadata from unrelated sibling sessions.
            paths = []
            for session_id in sorted(explicit_ids):
                paths.extend(directory.rglob(f"*{session_id}*.jsonl"))
        else:
            # Source-tree fallback: inspect only session_meta (the first line)
            # until parentage proves which logs are descendants.
            paths = directory.rglob("*.jsonl")
        for path in paths:
            if path.resolve() == root_path.resolve():
                continue
            scanned += 1
            meta = _read_meta(path)
            if meta is None:
                continue
            own_id = _meta_id(meta)
            if own_id:
                candidates[own_id] = (path, meta)
    except OSError:
        pass
    return candidates, scanned


def _discover(root_path: Path, dispatch_path: Path | None) -> tuple[list[tuple[Path, dict[str, Any]]], dict[str, Any]]:
    root_meta = _read_meta(root_path)
    if root_meta is None:
        raise ValueError(f"root session has no readable session_meta first record: {root_path}")
    root_id = _meta_id(root_meta)
    if not root_id:
        raise ValueError("root session_meta has no session id")

    explicit_ids = _dispatch_ids(dispatch_path)
    explicit_ids.discard(root_id)
    candidates, scanned = _load_candidate_metadata(root_path.parent, root_path, explicit_ids)

    descendant_ids: set[str] = set()
    frontier = {root_id}
    changed = True
    while changed:
        changed = False
        for candidate_id, (_, meta) in candidates.items():
            if candidate_id in descendant_ids:
                continue
            if _meta_parents(meta) & frontier:
                descendant_ids.add(candidate_id)
                frontier.add(candidate_id)
                changed = True

    # An explicit dispatch ID is accepted only if its metadata proves ancestry.
    unresolved = sorted(explicit_ids - set(candidates))
    unverified = sorted(explicit_ids & set(candidates) - descendant_ids)
    sessions = [(root_path, root_meta)]
    sessions.extend(candidates[item] for item in sorted(descendant_ids) if item in candidates)
    discovery = {
        "root_session_id": root_id,
        "discovery_method": "session_meta_parent_tree" + ("+dispatch_ids" if explicit_ids else ""),
        "metadata_only_candidate_files_scanned": scanned,
        "dispatch_file": str(dispatch_path) if dispatch_path and dispatch_path.exists() else None,
        "dispatch_ids_requested": sorted(explicit_ids),
        "dispatch_ids_unresolved": unresolved,
        "dispatch_ids_not_proven_descendants": unverified,
        "session_count_including_root": len(sessions),
        "descendant_count": len(sessions) - 1,
    }
    return sessions, discovery


def build_snapshot(root_path: Path, dispatch_path: Path | None) -> dict[str, Any]:
    sessions_found, discovery = _discover(root_path, dispatch_path)
    active_ids = _active_ids(dispatch_path)
    session_results: list[dict[str, Any]] = []
    totals: dict[str, int] = defaultdict(int)
    by_model: dict[str, dict[str, Any]] = {}
    priced_sessions = 0
    unpriced_sessions = 0
    total_cost = 0.0

    for path, meta in sessions_found:
        item = _latest_context_and_usage(path)
        item["session_meta_id"] = _meta_id(meta)
        usage_thread_id = item.get("token_usage_thread_id")
        item["usage_thread_id_matches_session_meta"] = (
            usage_thread_id == item["session_meta_id"]
            if usage_thread_id is not None and item.get("session_meta_id") is not None
            else None
        )
        if item["usage_thread_id_matches_session_meta"] is False:
            item.setdefault("warnings", []).append(
                "token usage thread_id differs from session_meta id; usage may not be thread-local"
            )
        item["parent_thread_id"] = next(iter(sorted(_meta_parents(meta))), None)
        item["agent_path"] = meta.get("agent_path")
        item["session_source"] = meta.get("thread_source") or meta.get("source")
        item["active_for_reservation"] = item["session_meta_id"] in active_ids
        item["price_proxy"] = _price_proxy(item)
        tokens = item.get("tokens", {})
        for key in (
            "input_tokens",
            "uncached_input_tokens",
            "cached_input_tokens",
            "cache_write_input_tokens",
            "output_tokens",
            "reasoning_output_tokens",
            "reported_total_tokens",
        ):
            totals[key] += _as_int(tokens.get(key))

        proxy = item["price_proxy"]
        model_key = proxy.get("pricing_family") or str(item.get("model") or "UNKNOWN")
        bucket = by_model.setdefault(
            model_key,
            {
                "latest_context_model_names": set(),
                "efforts": set(),
                "session_count": 0,
                "tokens": defaultdict(int),
                "usd_proxy": 0.0,
                "unpriced_session_count": 0,
            },
        )
        bucket["latest_context_model_names"].add(str(item.get("model") or "UNKNOWN"))
        bucket["efforts"].add(str(item.get("effort") or "UNKNOWN"))
        bucket["session_count"] += 1
        for key in totals:
            bucket["tokens"][key] += _as_int(tokens.get(key))
        if proxy.get("usd_proxy") is None:
            unpriced_sessions += 1
            bucket["unpriced_session_count"] += 1
        else:
            priced_sessions += 1
            total_cost += proxy["usd_proxy"]
            bucket["usd_proxy"] += proxy["usd_proxy"]
        session_results.append(item)

    for value in by_model.values():
        value["latest_context_model_names"] = sorted(value["latest_context_model_names"])
        value["efforts"] = sorted(value["efforts"])
        value["tokens"] = dict(value["tokens"])
        value["usd_proxy"] = round(value["usd_proxy"], 9)

    active_sessions = [item for item in session_results if item.get("active_for_reservation")]
    active_model_counts: dict[str, int] = defaultdict(int)
    reservation = 0.0
    unweighted_active: list[str] = []
    for item in active_sessions:
        family = _reservation_family(item.get("model"))
        if family is None:
            unweighted_active.append(str(item.get("session_meta_id")))
            continue
        active_model_counts[family] += 1
        reservation += ACTIVE_RESERVATION_WEIGHTS[family]
    active_ids_not_found = active_ids - {item.get("session_meta_id") for item in session_results}
    reservation_complete = bool(active_ids) and not unweighted_active and not active_ids_not_found
    active_roster_as_of = None
    if dispatch_path and dispatch_path.exists():
        try:
            dispatch_data = json.loads(dispatch_path.read_text(encoding="utf-8"))
            if isinstance(dispatch_data, dict):
                active_roster_as_of = dispatch_data.get("active_as_of_utc")
        except (OSError, json.JSONDecodeError, UnicodeError):
            pass

    for item in session_results:
        item.pop("path", None)
        # Paths are available through source filenames during the run, but are
        # intentionally omitted from the durable snapshot to avoid leaking the
        # user's local directory layout.

    generated = datetime.now(timezone.utc).isoformat(timespec="seconds")
    return {
        "snapshot_generated_at_utc": generated,
        "scope": "root_session_and_metadata_proven_descendant_sessions",
        "discovery": discovery,
        "sessions": session_results,
        "aggregate_tokens": dict(totals),
        "aggregate_pricing_proxy": {
            "status": "estimate_not_actual_billing",
            "priced_session_count": priced_sessions,
            "unpriced_session_count": unpriced_sessions,
            "usd_proxy": round(total_cost, 9),
            "by_pricing_family": by_model,
        },
        "concurrent_reservation": {
            "ceiling_sol_max_equivalents": CONCURRENT_SOL_MAX_CEILING,
            "status": "within_limit"
            if reservation_complete and reservation <= CONCURRENT_SOL_MAX_CEILING
            else "exceeded_limit"
            if reservation_complete
            else "active_roster_unavailable_or_unpriced",
            "active_roster_source": str(dispatch_path) if dispatch_path else None,
            "active_roster_as_of_utc": active_roster_as_of,
            "active_thread_count": len(active_sessions),
            "active_model_counts": dict(active_model_counts),
            "reservation_weights_in_sol_max_equivalents": ACTIVE_RESERVATION_WEIGHTS,
            "active_reservation_sol_max_equivalents": round(reservation, 3)
            if reservation_complete
            else None,
            "headroom_sol_max_equivalents": round(
                max(0.0, CONCURRENT_SOL_MAX_CEILING - reservation), 3
            )
            if reservation_complete
            else None,
            "excess_sol_max_equivalents": round(
                max(0.0, reservation - CONCURRENT_SOL_MAX_CEILING), 3
            )
            if reservation_complete
            else None,
            "active_session_ids_not_in_audited_tree": sorted(active_ids_not_found),
            "active_sessions_without_reservation_weight": sorted(unweighted_active),
            "basis": "Active model reservations are separate from cumulative token use and price proxy; coordinator-supplied ratios: Astra max component 10, Sol 1, Luna 0.1.",
        },
        "dispatch_verification": _dispatch_summary(_dispatch_requests(root_path), session_results),
        "pricing_basis": {
            "source": PRICE_SOURCE,
            "rates_usd_per_million_tokens": RATES_USD_PER_MTOK,
            "sol_reference_model": "gpt-6.1-sol",
            "rate_date": "2026-10-09; supplied by coordinator from official comparison page",
            "effort_multiplier": "none applied; effort is reported as metadata only",
            "proxy_formula": "(uncached input x input rate + cached input x cached rate + output x output rate) / 1,000,000",
        },
        "accounting_notes": [
            "Current token_usage_record schema exposes thread_token_usage as the latest cumulative total; usage is a response delta and is not used when the cumulative field exists.",
            "cached_input_tokens is a subset of input_tokens; uncached input is input_tokens minus cached_input_tokens.",
            "reasoning_output_tokens is reported separately as a subset of output_tokens and is not added a second time.",
            "cache_write_input_tokens is reported separately; with only input and cached-input rates supplied, it remains in the uncached-input price bucket.",
            "If a thread changed models during its history, this snapshot uses its latest turn_context model to price its cumulative thread total; historical model-specific attribution is unavailable from this summary method.",
            "The pricing estimate excludes service-specific adjustments, long-context rates, discounts, retries not represented in these usage records, non-token charges, and any billing corrections.",
            "Concurrent reservation and cumulative token usage answer different questions; the 30 Sol-max limit is applied only to the active roster using the specified reservation weights.",
            "Metadata discovery scans only the first session_meta line of sibling JSONL candidates. Full session records are parsed only after metadata proves descendant parentage.",
        ],
    }


def _dispatch_summary(
    requests: list[dict[str, Any]], sessions: list[dict[str, Any]]
) -> dict[str, Any]:
    observed = {
        item.get("agent_path", "").rsplit("/", 1)[-1]: item
        for item in sessions
        if item.get("agent_path")
    }
    requested_names = {item["task_name"] for item in requests if item.get("task_name")}
    requested_models: dict[str, int] = defaultdict(int)
    requested_efforts: dict[str, int] = defaultdict(int)
    effective_models: dict[str, int] = defaultdict(int)
    effective_efforts: dict[str, int] = defaultdict(int)
    for item in requests:
        requested_models[item.get("requested_model") or "unspecified"] += 1
        requested_efforts[item.get("requested_effort") or "unspecified"] += 1
    for item in sessions:
        effective_models[item.get("model") or "unspecified"] += 1
        effective_efforts[item.get("effort") or "unspecified"] += 1
    return {
        "spawn_agent_call_count": len(requests),
        "requested_model_counts": dict(requested_models),
        "requested_effort_counts": dict(requested_efforts),
        "effective_context_model_counts_including_root": dict(effective_models),
        "effective_context_effort_counts_including_root": dict(effective_efforts),
        "dispatched_task_names": sorted(requested_names),
        "task_names_with_session_metadata": sorted(requested_names & set(observed)),
        "task_names_without_session_metadata_yet": sorted(requested_names - set(observed)),
        "all_dispatched_task_names_have_session_metadata": requested_names <= set(observed),
        "observed_agent_paths_without_matching_dispatch_name": sorted(set(observed) - requested_names),
        "prompt_content_retained": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root-session", type=Path, default=DEFAULT_ROOT)
    parser.add_argument("--dispatch-file", type=Path, default=None)
    parser.add_argument("--output", type=Path, default=None, help="Write JSON here; otherwise print to stdout.")
    args = parser.parse_args()
    root_path = args.root_session.expanduser().resolve()
    dispatch_path = args.dispatch_file.expanduser().resolve() if args.dispatch_file else None
    if not root_path.is_file():
        parser.error(f"root session file does not exist: {root_path}")
    try:
        snapshot = build_snapshot(root_path, dispatch_path)
    except (OSError, ValueError) as error:
        print(f"audit_usage: {error}", file=sys.stderr)
        return 2
    rendered = json.dumps(snapshot, indent=2, sort_keys=True) + "\n"
    if args.output:
        output_path = args.output.expanduser().resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(rendered, encoding="utf-8")
    else:
        sys.stdout.write(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
