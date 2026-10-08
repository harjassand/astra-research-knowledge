#!/usr/bin/env python3
"""Exact plumbing test for candidate rank-witness verification over Q.

This only demonstrates the finite verification predicate on 1x1 matrix
multiplication. It does not run or bound the general FindBlock search.
"""

from __future__ import annotations

import itertools
import json
from fractions import Fraction
from pathlib import Path


def is_scalar_mm_rank_one(a: Fraction, b: Fraction, c: Fraction) -> bool:
    """Verify tr(ABC)=abc for 1x1 matrices by exact coefficient equality."""
    return a * b * c == 1


def main() -> None:
    # A finite prefix of a canonical rational enumeration.
    candidates = [Fraction(0), Fraction(1), Fraction(-1), Fraction(1, 2), Fraction(2)]
    checked = 0
    witness = None
    for a, b, c in itertools.product(candidates, repeat=3):
        checked += 1
        if is_scalar_mm_rank_one(a, b, c):
            witness = [str(a), str(b), str(c)]
            break
    assert witness == ["1", "1", "1"]

    # Reject a malformed proposed polynomial identity exactly.
    assert not is_scalar_mm_rank_one(Fraction(1), Fraction(1), Fraction(2))
    receipt = {
        "status": "EXACT_FINITE_PREDICATE_TEST_ONLY",
        "field": "Q",
        "block_dimension": 1,
        "rank": 1,
        "candidates_checked": checked,
        "accepted_witness": witness,
        "malformed_candidate_rejected": True,
        "limitations": [
            "does not run the general exhaustive search",
            "does not validate the L03 exponent premise",
            "does not establish useful search-time or height bounds",
        ],
    }
    out = Path(__file__).with_name("search_demo.json")
    out.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
