#!/usr/bin/env python3
"""Exact small controls for the N129 audit. No admissible source graph is built."""
from fractions import Fraction as Q
from math import ceil
import json
from pathlib import Path


def solve(a, b):
    a = [list(row) + [rhs] for row, rhs in zip(a, b)]
    n = len(b)
    for c in range(n):
        k = next(i for i in range(c, n) if a[i][c])
        a[c], a[k] = a[k], a[c]
        pivot = a[c][c]
        a[c] = [x / pivot for x in a[c]]
        for i in range(n):
            if i != c:
                multiplier = a[i][c]
                a[i] = [x - multiplier * y for x, y in zip(a[i], a[c])]
    return [row[-1] for row in a]


def kernel(q):
    v = q * q + q + 1
    p = Q(q + 1, v)
    b = Q(1, (q + 1) ** 2)
    # Categories: ordinary paired with an extra, remaining ordinary, extra.
    return [
        [7 * p * p, (v - 7) * p * p, Q(6, 4)],
        [7 * b, (v - 8) * b, 7 * p * p],
        [6 * b, (v - 7) * b, 7 * p * p],
    ]


def matvec(a, v):
    return [sum(x * y for x, y in zip(row, v)) for row in a]


def kernel_controls():
    result = []
    for q in [4, 8, 16, 32, 64, 128]:
        m = kernel(q)
        a = [[Q(i == j) - m[i][j] for j in range(3)] for i in range(3)]
        f = solve(a, [Q(1)] * 3)
        if all(x > 0 for x in f):
            assert all(x < y for x, y in zip(matvec(m, f), f))
            kind = "subcritical: exact positive f with Mf < f"
        else:
            assert all(x < 0 for x in f)
            u = [-x for x in f]
            assert all(x > y for x, y in zip(matvec(m, u), u))
            kind = "supercritical: exact positive u with Mu > u"
        result.append({"q": q, "certificate": kind,
                       "vector": [str(x) for x in f]})
    m = kernel(128)
    f = [Q(4), Q(1), Q(1)]
    mf = matvec(m, f)
    lam = max(x / y for x, y in zip(mf, f))
    assert lam < 1
    assert all(x > 0 for x in f)
    return result, {"lambda": str(lam), "lambda_decimal": float(lam),
                    "margin": str(1 - lam), "Mf": [str(x) for x in mf]}


def square_patch(r):
    inv = {"a": "A", "A": "a", "b": "B", "B": "b"}
    word = ("a", "b", "A", "B")
    assert all(word[(i + 1) % 4] != inv[word[i]] for i in range(4))
    positions = {(x, y, e) for x in range(r) for y in range(r) for e in range(4)}
    pairs = []
    for x in range(r):
        for y in range(r):
            if x + 1 < r:
                pairs.append(((x, y, 1), (x + 1, y, 3)))
            if y + 1 < r:
                pairs.append(((x, y, 2), (x, y + 1, 0)))
    used = set()
    for a, b in pairs:
        assert a in positions and b in positions
        assert a not in used and b not in used
        assert word[a[2]] == inv[word[b[2]]]
        assert a[2] != b[2]  # The four graph edges are distinct.
        used.update((a, b))
    h = len(positions)
    unpaired = len(positions - used)
    assert h == 4 * r * r
    assert unpaired == 4 * r
    assert len(pairs) == 2 * r * (r - 1)
    return h, unpaired, len(pairs)


def budget_controls():
    # Rational upper bounds on square roots certify c_sep < 16.
    s2, s23 = Q(99, 70), Q(49, 60)
    assert s2 * s2 > 2 and s23 * s23 > Q(2, 3)
    assert 2 * s2 / (1 - s23) < 16
    results = []
    for epsilon in [Q(1, 4), Q(1, 16), Q(1, 64), Q(1, 128)]:
        d0 = 1
        u = max(3, ceil(96 * d0 / epsilon))
        eta = min(Q(1, 32 * u), epsilon / (64 * u))
        assert 3 * Q(d0, u) <= epsilon / 32
        assert eta * u <= epsilon / 64
        losses = epsilon / 64 + eta * u + 3 * Q(d0, u)
        assert losses <= epsilon / 16
        # c_sep > 1 gives a lower bound on the manuscript's actual K0.
        k_lower = ceil(1 / (eta * eta))
        r = ceil(1 / epsilon)
        h, b, comparisons = square_patch(r)
        assert Q(b, h) <= epsilon
        assert r * r <= k_lower
        assert 4 <= h <= k_lower * (u + d0) * 4
        assert comparisons <= 192 * k_lower * (u + d0)
        results.append({"epsilon": str(epsilon), "r": r, "loops": r * r,
                        "H": h, "unpaired": b, "comparisons": comparisons,
                        "fraction_unpaired": str(Q(b, h)),
                        "K0_lower_bound": k_lower})
    return results


def main():
    thresholds, source = kernel_controls()
    budgets = budget_controls()
    result = {"status": "FINITE-EVIDENCE",
              "scope": "Exact rational kernel certificates and square-patch controls; no source graph acquired.",
              "source_q128_kernel": source,
              "kernel_threshold_controls": thresholds,
              "square_patch_controls": budgets}
    out = Path(__file__).with_name("CHECKS.json")
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"checks": "passed", "lambda_q128": source["lambda_decimal"],
                      "controls": len(thresholds) + len(budgets), "output": str(out)}))


if __name__ == "__main__":
    main()
