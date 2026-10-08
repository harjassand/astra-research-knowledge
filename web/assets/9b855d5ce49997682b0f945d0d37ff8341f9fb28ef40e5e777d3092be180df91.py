#!/usr/bin/env python3
"""Replay C8's exact support recognizer on the two Goldbeter–Koshland fixtures."""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
C8 = HERE.parent
sys.path.insert(0, str(C8))

import recognize_sparse_rational as recognizer


def replay(filename: str) -> dict:
    path = HERE / "fixtures" / filename
    data = json.loads(path.read_text())
    edges, dimension = recognizer.parse_network(data)
    result = recognizer.recognize(
        edges, dimension, property_name="endotactic", timeout_ms=30_000,
        max_checks=None, rlimit=None,
    )
    return {"fixture": filename, **result}


def main() -> int:
    result = {
        "recognizer": f"Z3 {recognizer.z3.get_version_string()}" if recognizer.z3 else None,
        "property": "C8 P/N33 essential-source rule; exact top ties are all checked",
        "results": [
            replay("goldbeter_koshland_1981_mm.json"),
            replay("goldbeter_koshland_1981_mass_action_mechanism.json"),
        ],
        "interpretation": (
            "Both REFUTED outputs are exact for the recognizer's declared all-positive-orthant "
            "support property. The reduced MM fixture is physically confined to W+W*=1; the "
            "explicit mechanism has fixed target/enzyme totals. Neither formal result by itself "
            "asserts instability or failure of permanence on those compact compatibility classes."
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if all(x["status"] == "REFUTED" for x in result["results"]) else 1


if __name__ == "__main__":
    raise SystemExit(main())
