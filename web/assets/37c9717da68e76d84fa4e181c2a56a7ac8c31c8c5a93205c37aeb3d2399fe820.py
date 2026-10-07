"""Exact conditional-mass identities plus a bounded sampler smoke check."""
from collections import Counter
from fractions import Fraction as Q
import random
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from functional_digraph_dp import count_poly, brute_poly
from revisions.functional_digraph_sampler import sample_canonical_rows


def check_conditional_mass():
    # Repeated columns, a cycle with trees, and a zero row.
    p = [1, 1, 1, 2, 2, 5, None]
    w = [Q(1), Q(4), Q(1, 4), Q(9), Q(4), Q(25, 9), Q(0)]
    t = [Q(0), Q(2), Q(1, 3), Q(3, 2), Q(1), Q(4), Q(2)]
    counts = count_poly(p, w, t)
    assert counts == brute_poly(p, w, t)
    for k, z in enumerate(counts):
        if not z:
            continue
        for row in range(len(p)):
            z0 = count_poly(p, w, t, {row: 0})[k]
            z1 = count_poly(p, w, t, {row: 1})[k]
            assert z0 + z1 == z
    return counts


def smoke_sample():
    p = [1, 1, 1, 2, 2, 5, None]
    f = [Q(1), Q(2), Q(1, 2), Q(3), Q(2), Q(5, 3), Q(0)]
    w = [x*x for x in f]
    t = [Q(0), Q(2), Q(1, 3), Q(3, 2), Q(1), Q(4), Q(2)]
    expected = count_poly(p, w, t)
    k = 2
    assert expected[k] > 0
    rng = random.Random(11162026)
    observed = Counter()
    max_abort_bound = Q(0)
    for _ in range(200):
        rows, columns, abort_bound = sample_canonical_rows(
            p, w, t, k, rng=rng, failure_budget=Q(1, 1000000))
        observed[(rows, columns)] += 1
        max_abort_bound = max(max_abort_bound, abort_bound)
    assert all(len(rows) == k and len(columns) == k for rows, columns in observed)
    return {"canonical_sector_weight": str(expected[k]),
            "samples": sum(observed.values()),
            "distinct_outputs_observed": len(observed),
            "max_abort_probability_bound": str(max_abort_bound),
            "note": "empirical smoke check only; conditional-mass identity is the exact justification"}


if __name__ == "__main__":
    print({"conditional_coefficients": [str(x) for x in check_conditional_mass()],
           "sampler": smoke_sample()})
