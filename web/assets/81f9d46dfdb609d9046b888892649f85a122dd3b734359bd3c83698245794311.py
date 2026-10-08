#!/usr/bin/env python3
"""Exact finite sanity check of the simple weighted-edge PM gadget.

For each W in the configured range, construct the bit-indexed DAG, form its
bipartite L/R expansion, and count perfect matchings after consuming each
subset of the two logical endpoint ports. This checks small instances only;
the general signature proof is in RESULT.txt and the leaf derivation.
"""

from __future__ import annotations

import json
from pathlib import Path


def gadget_signature(weight: int) -> tuple[int, int, int, int]:
    if weight < 1:
        raise ValueError("weight must be positive")
    k = weight.bit_length()
    names = ["s", "t"] + [f"x{i}" for i in range(k)]
    arcs: list[tuple[str, str]] = []
    for i in range(k):
        arcs.append((f"x{i}", "t"))
        arcs.extend((f"x{i}", f"x{j}") for j in range(i))
    for i in range(k):
        if (weight >> i) & 1:
            arcs.append(("s", f"x{i}"))

    left = [f"L:{name}" for name in names]
    right = [f"R:{name}" for name in names]
    adjacency: dict[str, set[str]] = {u: set() for u in left}
    for name in names:
        adjacency[f"L:{name}"].add(f"R:{name}")
    for u, v in arcs:
        adjacency[f"L:{u}"].add(f"R:{v}")

    # External left endpoint consumes L_t; external right endpoint consumes R_s.
    def count(consumed: tuple[bool, bool]) -> int:
        left_remaining = left.copy()
        right_remaining = right.copy()
        if consumed[0]:
            left_remaining.remove("L:t")
        if consumed[1]:
            right_remaining.remove("R:s")
        if len(left_remaining) != len(right_remaining):
            return 0
        right_set = set(right_remaining)

        def rec(index: int, available: set[str]) -> int:
            if index == len(left_remaining):
                return 1
            u = left_remaining[index]
            return sum(
                rec(index + 1, available - {v})
                for v in adjacency[u] & available
            )

        return rec(0, right_set)

    return (
        count((False, False)),
        count((True, True)),
        count((True, False)),
        count((False, True)),
    )


def main() -> None:
    rows = []
    for weight in range(1, 21):
        observed = gadget_signature(weight)
        expected = (1, weight, 0, 0)
        rows.append({"weight": weight, "observed": list(observed), "expected": list(expected)})
        if observed != expected:
            raise AssertionError(f"weight {weight}: {observed} != {expected}")
    result = {
        "check": "finite exact matching enumeration",
        "weights": [1, 20],
        "all_signatures_match": True,
        "rows": rows,
        "status": "FINITE-EVIDENCE",
        "limitation": "This is a small-instance sanity check, not proof validation or OA113 validation.",
    }
    out = Path(__file__).with_name("weight_gadget_check.json")
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"all_signatures_match": True, "instances": len(rows), "output": out.name}))


if __name__ == "__main__":
    main()
