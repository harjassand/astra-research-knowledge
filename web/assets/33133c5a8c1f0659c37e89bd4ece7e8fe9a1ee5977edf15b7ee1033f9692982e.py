#!/usr/bin/env python3
"""Exact even-windability recognizer for even functions on four bits."""
from fractions import Fraction
import json
from pathlib import Path

N = 4
FULL = 15
PAIRINGS = (((0,1),(2,3)),((0,2),(1,3)),((0,3),(1,2)))


def pair_mask(pair):
    return (1 << pair[0]) | (1 << pair[1])


def pairing_index(matching):
    normalized = tuple(sorted(tuple(sorted(p)) for p in matching))
    candidates = [tuple(sorted(tuple(sorted(p)) for p in m)) for m in PAIRINGS]
    return candidates.index(normalized)


def matchings_for_difference(diff):
    sites = [i for i in range(N) if (diff >> i) & 1]
    if not sites:
        return [()]
    if len(sites) == 2:
        return [(tuple(sites),)]
    if len(sites) == 4:
        return list(PAIRINGS)
    return []


def analyze_even_signature(f):
    """Return exact witness data iff f is even-windable on four sites.

    The criterion is necessary and sufficient for the McQuillan witness on a
    four-site even function. It checks all pinnings through the direct ordered
    pair witness construction below.
    """
    if len(f) != 16 or any(f[m] < 0 for m in range(16)):
        raise ValueError("expected 16 nonnegative rational coefficients")
    if any(f[m] != 0 for m in range(16) if m.bit_count() % 2):
        raise ValueError("function is not supported on even subsets")
    capacities = []
    for first, second in PAIRINGS:
        capacities.append(f[pair_mask(first)] * f[pair_mask(second)])
    demand = f[0] * f[FULL]
    residual = (sum(capacities) - demand) / 2
    if residual < 0:
        return {"windable": False, "reason": "negative four-hole defect", "demand": demand, "capacities": capacities}
    lower = [max(Fraction(0), h - residual) for h in capacities]
    upper = capacities
    if sum(lower) > demand or sum(upper) < demand:
        return {
            "windable": False,
            "reason": "four-hole orbit masses have incompatible nonnegative bounds",
            "demand": demand,
            "capacities": capacities,
            "cross_orbit_total": residual,
            "lower_bounds": lower,
            "lower_bound_sum": sum(lower),
        }
    a = list(lower)
    remaining = demand - sum(a)
    for i in range(3):
        increment = min(remaining, upper[i] - a[i])
        a[i] += increment
        remaining -= increment
    if remaining:
        raise AssertionError("greedy fill failed despite the exact interval criterion")
    b = [a[i] + residual - capacities[i] for i in range(3)]
    assert all(x >= 0 for x in a + b)
    assert sum(a) == demand and sum(b) == residual
    assert all(capacities[i] == a[i] + sum(b[j] for j in range(3) if j != i)
               for i in range(3))

    def witness(x, y):
        diff = x ^ y
        matchings = matchings_for_difference(diff)
        value = f[x] * f[y]
        if not value:
            return {m: Fraction(0) for m in matchings}
        if diff.bit_count() in (0, 2):
            assert len(matchings) == 1
            return {matchings[0]: value}
        assert diff.bit_count() == 4 and len(matchings) == 3
        out = {}
        for matching in matchings:
            index = pairing_index(matching)
            aligned = all(((x >> i) & 1) == ((x >> j) & 1)
                          for i, j in matching)
            out[matching] = a[index] if aligned else b[index]
        return out

    pair_checks = 0
    flip_checks = 0
    for x in range(1 << N):
        for y in range(1 << N):
            masses = witness(x, y)
            assert sum(masses.values()) == f[x] * f[y]
            pair_checks += 1
            for matching, mass in masses.items():
                for edge in matching:
                    flipped = pair_mask(edge)
                    assert witness(x ^ flipped, y ^ flipped)[matching] == mass
                    flip_checks += 1
    return {
        "windable": True,
        "demand": demand,
        "pairing_capacities": capacities,
        "cross_orbit_total": residual,
        "empty_orbit_masses": a,
        "cross_orbit_masses": b,
        "ordered_assignment_pairs_checked": pair_checks,
        "pair_flip_equalities_checked": flip_checks,
    }


def format_result(result):
    out = {}
    for key, value in result.items():
        if isinstance(value, Fraction):
            out[key] = str(value)
        elif isinstance(value, list):
            out[key] = [str(x) if isinstance(x, Fraction) else x for x in value]
        else:
            out[key] = value
    return out


def main():
    from cross_aux_counterexample import (
        CROSS_EDGES, F as F6, hole_signature, transform_slice
    )

    original_f4 = [Fraction(0) for _ in range(16)]
    original_f4[0] = Fraction(4)
    original_f4[15] = Fraction(1)
    for mask in (5, 6, 9, 10):
        original_f4[mask] = Fraction(1)

    larger_delta_but_not_windable = [Fraction(0) for _ in range(16)]
    larger_delta_but_not_windable[0] = Fraction(1)
    larger_delta_but_not_windable[15] = Fraction(1)
    larger_delta_but_not_windable[3] = Fraction(3)
    larger_delta_but_not_windable[12] = Fraction(1)

    sig6 = hole_signature(F6)
    minimal_edges = CROSS_EDGES[:7]
    rescued_slice = transform_slice(sig6, minimal_edges)
    # The displayed seven-edge set is (04,05,14,15,24,25,34).
    results = {
        "F4_original": analyze_even_signature(original_f4),
        "positive_delta_but_infeasible": analyze_even_signature(larger_delta_but_not_windable),
        "cross_coordinate_rescued_slice": analyze_even_signature(rescued_slice),
    }
    assert results["F4_original"]["windable"] is False
    assert results["positive_delta_but_infeasible"]["windable"] is False
    assert results["positive_delta_but_infeasible"]["reason"].startswith("four-hole orbit")
    assert results["cross_coordinate_rescued_slice"]["windable"] is True
    out = {name: format_result(value) for name, value in results.items()}
    path = Path(__file__).with_name("four_site_windability_recognizer_result.json")
    path.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))

if __name__ == "__main__":
    main()
