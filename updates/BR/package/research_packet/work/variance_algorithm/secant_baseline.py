"""Exact rational secant/continuous-knapsack upper bound for a box ratio.

Input tuples are (lower x, upper x, coefficient c), all nonnegative,
for max sum(c*x*x) / sum(x)**2 over the box with positive denominator.
This is a conventional relaxation, not a claimed new algorithmic principle.
"""
from fractions import Fraction


def secant_bounds(coords):
    items = [(Fraction(lo), Fraction(hi), Fraction(c)) for lo, hi, c in coords]
    if any(lo < 0 or hi < lo or c < 0 for lo, hi, c in items):
        raise ValueError("Require 0 <= lower <= upper and coefficient >= 0")
    if not items or not any(hi > 0 for lo, hi, c in items):
        return {"lower": Fraction(0), "upper": Fraction(0),
                "witness": tuple(lo for lo, hi, c in items),
                "segments": 0, "all_zero": True}
    total = sum((lo for lo, hi, c in items), Fraction(0))
    value = sum((c*lo*lo for lo, hi, c in items), Fraction(0))
    if total == 0:
        chosen = max((i for i, (_, hi, _) in enumerate(items) if hi > 0),
                     key=lambda i: items[i][2])
        exact = items[chosen][2]
        witness = tuple(hi if i == chosen else Fraction(0)
                        for i, (lo, hi, c) in enumerate(items))
        return {"lower": exact, "upper": exact, "witness": witness,
                "segments": 0, "all_zero": False}
    # The optimum is attained at a nonzero corner. If all lower bounds are
    # zero, every nonzero corner has sum at least min positive upper bound.
    minimum_corner_sum = total or min(hi for lo, hi, c in items if hi > 0)
    feasible_witness = total > 0
    best_prefix = -1
    best_single = None
    lower = value / total**2 if total else Fraction(0)
    upper = lower
    # O(d) stronger feasible baseline: flip just one coordinate from the
    # all-lower corner. Store its index; build a full witness only once.
    for i, (lo, hi, c) in enumerate(items):
        s = total + hi - lo
        if s:
            candidate = (value+c*(hi*hi-lo*lo))/s**2
            if candidate > lower:
                lower, best_single = candidate, i
    upper = max(upper, lower)
    order = sorted(range(len(items)),
                   key=lambda i: items[i][2]*(items[i][0]+items[i][1]),
                   reverse=True)
    segment_count = 0
    for prefix, i in enumerate(order):
        lo, hi, c = items[i]
        width = hi - lo
        if not width:
            continue
        slope = c*(lo+hi)
        intercept = value - slope*total
        end = total + width
        start = max(total, minimum_corner_sum)
        if start <= end and end > 0:
            candidates = [start, end]
            if slope > 0 and intercept < 0:
                stationary = -2*intercept/slope
                if start <= stationary <= end:
                    candidates.append(stationary)
            for s in candidates:
                if s > 0:
                    upper = max(upper, (slope*s+intercept)/s**2)
            segment_count += 1
        total = end
        value += slope*width
        candidate = value/total**2 if total else Fraction(0)
        if total and (not feasible_witness or candidate > lower):
            lower, best_prefix = candidate, prefix
            best_single = None
            feasible_witness = True
        upper = max(upper, candidate)
    # This generic simplex bound is cheap and especially useful for zero
    # lower bounds where the secant relaxation can otherwise be loose.
    upper = min(upper, max(c for lo, hi, c in items if hi > 0))
    upper_indices = ({best_single} if best_single is not None
                     else set(order[:best_prefix+1]))
    witness = tuple(hi if i in upper_indices else lo
                    for i, (lo, hi, c) in enumerate(items))
    assert lower <= upper
    return {"lower": lower, "upper": upper, "witness": witness,
            "segments": segment_count, "all_zero": False}


def secant_upper(coords):
    """Return a sound exact-Fraction upper bound, including zero-lower boxes."""
    return secant_bounds(coords)["upper"]


def _check():
    from itertools import product
    from random import Random
    rng = Random(20261010)
    count = 0
    positive_count = 0
    exact_count = 0
    fixtures = [[(0, 1, 1)], [(0, 0, 2)], [(1, 1, 3)],
                [(0, 1, 0)], [(0, 0, 99), (0, 1, 0)],
                [(0, 10, 1), (0, 1, 10)],
                [(Fraction(1, 3), 1, 2), (Fraction(1, 7), 2, 3)]]
    for _ in range(250):
        row = []
        for _ in range(rng.randrange(1, 9)):
            lo = Fraction(rng.randrange(0, 10), rng.randrange(1, 11))
            hi = lo + Fraction(rng.randrange(0, 15), rng.randrange(1, 11))
            c = Fraction(rng.randrange(0, 25), rng.randrange(1, 11))
            row.append((lo, hi, c))
        fixtures.append(row)
    for row in fixtures:
        row = [(Fraction(lo), Fraction(hi), Fraction(c)) for lo, hi, c in row]
        result = secant_bounds(row)
        optimum = Fraction(0)
        for point in product(*[(lo, hi) for lo, hi, c in row]):
            s = sum(point)
            if s:
                optimum = max(optimum, sum(c*x*x for (_, _, c), x in
                              zip(row, point))/s**2)
        assert result["lower"] <= optimum <= result["upper"], (row, result, optimum)
        s = sum(result["witness"])
        assert s > 0 or result["all_zero"]
        witness_value = (sum(c*x*x for (_, _, c), x in zip(row, result["witness"]))
                         /s**2 if s else Fraction(0))
        assert result["lower"] == witness_value
        if all(lo > 0 for lo, hi, c in row):
            kappa = max((lo+hi)**2/(4*lo*hi) for lo, hi, c in row)
            assert result["upper"] <= kappa*result["lower"]
            positive_count += 1
        exact_count += result["upper"] == optimum
        count += 1
    return {"status": "PASS", "exhaustive_cases": count,
            "positive_box_factor_checks": positive_count,
            "upper_equal_exact_optimum": exact_count}


if __name__ == "__main__":
    import json
    print(json.dumps(_check(), indent=2))
