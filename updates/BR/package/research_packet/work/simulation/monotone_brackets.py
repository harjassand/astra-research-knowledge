#!/usr/bin/env python3
"""Exact 2D monotone-membership probability enclosure; synthetic audit only.

Run: python3 work/simulation/monotone_brackets.py
No learned monotonicity, numerical simulator, or external dependencies are used.
"""
from fractions import Fraction as F
from math import ceil, log
import csv
import json
import pathlib
import time


def edges(m, octaves):
    positive = [F(m-i, m * (1 << j))
                for j in range(octaves) for i in range(m//2)]
    positive.append(F(1, 1 << octaves))
    return [F(0)] + positive[::-1]


def bracket(oracle, epsilon=F(1, 10), max_octaves=256):
    assert 0 < epsilon <= 1
    m = ceil(8 / epsilon)
    m += m % 2
    cache = {}
    max_coordinate_bits = 0

    def query(x, y):
        nonlocal max_coordinate_bits
        key = (x, y)
        if key not in cache:
            cache[key] = bool(oracle(x, y))
            max_coordinate_bits = max(max_coordinate_bits,
                x.numerator.bit_length(), x.denominator.bit_length(),
                y.numerator.bit_length(), y.denominator.bit_length())
        return cache[key]

    octave_count = 1
    stages = []
    while octave_count <= max_octaves:
        xs = edges(m, octave_count)
        last_true = []
        j = len(xs) - 1
        for x in xs:
            while j >= 0 and not query(x, xs[j]):
                j -= 1
            last_true.append(j)

        lower = F(0)
        upper = F(0)
        for i in range(len(xs)-1):
            dx = xs[i+1] - xs[i]
            jt = last_true[i+1]
            lower += dx * (xs[jt] if jt >= 0 else 0)
            jt = last_true[i]
            upper += dx * (xs[min(jt+1, len(xs)-1)] if jt >= 0 else 0)
        tau = F(1, 1 << octave_count)
        r = 1 + F(2, m)
        # These are theorem-internal sanity checks, not a monotonicity audit.
        assert lower <= upper
        assert upper <= r*r*lower + 2*tau
        stages.append({"octaves": octave_count, "queries_cumulative": len(cache),
                       "lower": str(lower), "upper": str(upper)})
        if upper == 0 or (lower and upper <= (1+epsilon)*lower):
            return {"status": "CERTIFIED_CONDITIONAL_ON_MONOTONICITY",
                    "lower": lower, "upper": upper, "queries": len(cache),
                    "coordinate_max_bits": max_coordinate_bits,
                    "octaves": octave_count, "epsilon": epsilon,
                    "stages": stages}
        octave_count *= 2
    return {"status": "UNKNOWN_BUDGET", "lower": lower, "upper": upper,
            "queries": len(cache), "coordinate_max_bits": max_coordinate_bits,
            "octaves": octave_count//2, "epsilon": epsilon, "stages": stages}


def cases():
    for k in (2, 4, 8, 12, 20):
        a = F(1, 1 << k)
        yield f"rectangle_k{k}", (lambda x, y, a=a: x <= a and y <= 3*a/5), 3*a*a/5
        yield f"triangle_k{k}", (lambda x, y, a=a: x+y <= a), a*a/2
        yield f"thin_strip_k{k}", (lambda x, y, a=a: x <= a*a), a*a
        # Disconnected in boundary representation but still a global downset.
        yield f"two_arms_k{k}", (lambda x, y, a=a: x <= a*a or y <= a*a), 2*a*a-a**4
        # Nonconvex staircase: union of two incomparable down-rectangles.
        aa, bb, cc, dd = a/5, 4*a/5, 3*a/5, 2*a/5
        yield f"staircase_k{k}", (lambda x, y, aa=aa, bb=bb, cc=cc, dd=dd:
                                 (x <= aa and y <= bb) or (x <= cc and y <= dd)), aa*bb+cc*dd-aa*dd


def exhaustive_grid_audit():
    """All 252 monotone 5x5 Boolean tables, extended as step-function downsets."""
    from itertools import combinations_with_replacement
    checked = 0
    for ascending in combinations_with_replacement(range(6), 5):
        heights = tuple(reversed(ascending))
        # A is union [0,(i+1)/5] x [0,height_i/5]; exact area known.
        p = sum(F(h, 25) for h in heights)
        if not p:
            continue
        def oracle(x, y, heights=heights):
            return any(x <= F(i+1, 5) and y <= F(h, 5)
                       for i, h in enumerate(heights) if h)
        res = bracket(oracle, F(1, 2), max_octaves=16)
        assert res["lower"] <= p <= res["upper"]
        assert res["upper"] <= F(3, 2)*res["lower"]
        checked += 1
    return checked


def main():
    out = pathlib.Path(__file__).resolve().parent
    results = []
    start = time.perf_counter()
    audited = exhaustive_grid_audit()
    for name, oracle, p in cases():
        t0 = time.perf_counter()
        res = bracket(oracle)
        elapsed = time.perf_counter()-t0
        assert res["status"] == "CERTIFIED_CONDITIONAL_ON_MONOTONICITY"
        assert res["lower"] <= p <= res["upper"]
        assert res["upper"] <= F(11, 10)*res["lower"]
        # Comparator is an explicit, sufficient multiplicative-Chernoff MC
        # count at relative error .1 and failure .05; it is not minimax optimal.
        mc_sufficient = ceil(3*log(40)/(float(F(1, 10)**2)*float(p)))
        results.append({"case": name, "p_exact": str(p), "p": float(p),
                        "lower": float(res["lower"]), "upper": float(res["upper"]),
                        "relative_bracket_width": float(res["upper"]/res["lower"]-1),
                        "oracle_queries": res["queries"], "max_coordinate_bits": res["coordinate_max_bits"],
                        "octaves": res["octaves"], "seconds": elapsed,
                        "mc_chernoff_sufficient_queries": mc_sufficient,
                        "stage_details": res["stages"]})
    # Deliberate broken-premise test: a disconnected missed component can be
    # completely invisible to the monotone query path. The algorithm does not
    # infer or verify monotonicity from its queried data.
    a = F(1, 1 << 12)
    base = bracket(lambda x, y: x <= a and y <= a)
    broken = bracket(lambda x, y: (x <= a and y <= a) or
                     (F(3, 4) <= x <= F(7, 8) and F(3, 4) <= y <= F(7, 8)))
    broken_p = a*a + F(1, 64)
    assert broken["lower"] == base["lower"] and broken["upper"] == base["upper"]
    assert broken["queries"] == base["queries"]
    assert broken_p > broken["upper"]
    negative = {"label": "INVALID_RESULT_IF_MONOTONICITY_PROMISE_IS_FALSE",
                "true_probability": str(broken_p),
                "reported_lower": str(broken["lower"]),
                "reported_upper": str(broken["upper"]),
                "queries": broken["queries"], "same_transcript_as_core": True}
    summary = {"status": "INTERNALLY_RECONSTRUCTED_SYNTHETIC_VALIDATION",
               "seed": None, "exact_rational": True,
               "exhaustive_nonempty_tables_checked": audited,
               "cases_checked": len(results), "seconds": time.perf_counter()-start,
               "results": results, "negative_broken_monotonicity": negative,
               "limits": ["Global monotonicity is supplied, not learned or certified.",
                          "Exact membership queries and exact uniform-coordinate transform are supplied.",
                          "Toy distributions only; no physical simulator or real-data validation.",
                          "No advance over strongest monotone-reliability prior art established."]}
    (out/"monotone_results.json").write_text(json.dumps(summary, indent=2)+"\n")
    fields = [k for k in results[0] if k != "stage_details"]
    with (out/"monotone_results.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows({k:v for k,v in row.items() if k in fields} for row in results)
    print(json.dumps({"tables": audited, "cases": len(results), "seconds": summary["seconds"],
                      "rarest": results[-5:]}, indent=2))


if __name__ == "__main__":
    main()
