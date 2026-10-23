"""Descriptive source-scope check, not a research performance experiment.

Reads frozen exported records only. No owner scientific entrypoint is imported or
executed. Counts are used to delimit what reasoning/process evidence is visible;
they must not be interpreted as productivity, tokens, serial wall time or cost.
"""
from pathlib import Path
import collections
import json

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "inputs/collection/branches"
outer = json.loads((BASE / "max/COMPLETE_API.json").read_text())
inner = json.loads(outer["content"][0]["text"])
turn = inner["turns"][0]
items = turn["items"]
reasons = [x for x in items if x["type"] == "reasoning"]
limits = json.loads((BASE / "max/SOURCE_EXPORT_LIMITS.json").read_text())
dots = json.loads((BASE / "dots/COMPLETE_RENDERED_DOM.json").read_text())
out = {
    "scope": "Finite descriptive export inspection only; no scientific replay or causal comparison.",
    "max": {
        "visible_turns": len(inner["turns"]),
        "has_more_history": inner["page"]["hasMore"],
        "preserved_item_count": len(items),
        "item_types": dict(collections.Counter(x["type"] for x in items)),
        "reasoning_typed_entries": len(reasons),
        "entries_with_visible_summary": sum(bool(x.get("summary")) for x in reasons),
        "entries_with_visible_reasoning_content": sum(bool(x.get("content")) for x in reasons),
        "recorded_elapsed_turn_seconds": turn["durationMs"] / 1000,
        "capped_fields": len(limits["capped_item_paths"]),
        "capped_scope": "Per-field 20,000-character export cap; not proof that every field was fully read.",
        "elapsed_scope": "Includes integration and transport; not model compute, discovery time or serial tool time.",
    },
    "dots": {
        "visible_final_response_characters": len(dots["text"]),
        "record_scope": "Rendered final response only, supplemented by producer PROCESS_RECORD and original scientific assets.",
        "independent_full_execution_trace_available_here": False,
    },
    "inference": "The exports support action, artifact and claim-scope review. They do not identify cognitive strategies, token costs, or causal benefit from autonomy, fresh instances or subagents.",
}
target = Path(__file__).with_suffix(".json")
target.write_text(json.dumps(out, indent=2) + "\n")
print(json.dumps(out, indent=2))
