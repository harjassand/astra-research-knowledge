#!/usr/bin/env python3
"""Exact finite checks for the pairwise Schur-Weyl collision scale.

No third-party packages are used.  This checks (i) the exact pair product from
adjacent gaps, (ii) its predicted multi-rate exponent on an exact dyadic
family, (iii) the critical qubit counterexample where B_n stays constant, and
(iv) normalization of the exact Schur-Weyl sector law
    q_lambda = dim(S_lambda) * s_lambda(p).

These are arithmetic/finite checks, not a proof of the analytic bounds in the
accompanying note.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations
import json
import math
from pathlib import Path


def spectrum_from_adjacent_gaps(gaps: list[Fraction]) -> list[Fraction]:
    """Return the unique trace-one spectrum with listed consecutive gaps."""
    d = len(gaps) + 1
    x = [Fraction(0) for _ in range(d)]
    for i in range(d - 1):
        x[i + 1] = x[i] - gaps[i]
    mean = sum(x, Fraction(0)) / d
    p = [Fraction(1, d) + z - mean for z in x]
    assert sum(p, Fraction(0)) == 1
    assert all(p[i] >= p[i + 1] for i in range(d - 1))
    assert min(p) > 0
    return p


def collision_product(n: int, p: list[Fraction]) -> Fraction:
    out = Fraction(1)
    for i, j in combinations(range(len(p)), 2):
        out *= 1 + n * (p[i] - p[j]) ** 2
    return out


def partitions(n: int, d: int, cap: int | None = None):
    """Yield weakly decreasing d-tuples summing to n."""
    if cap is None:
        cap = n

    def rec(left: int, slots: int, ceiling: int, prefix: tuple[int, ...]):
        if slots == 0:
            if left == 0:
                yield prefix
            return
        hi = min(left, ceiling)
        lo = (left + slots - 1) // slots
        for a in range(hi, lo - 1, -1):
            yield from rec(left - a, slots - 1, a, prefix + (a,))

    yield from rec(n, d, cap, ())


def hook_dimension(lam: tuple[int, ...]) -> int:
    n = sum(lam)
    col_heights = [sum(1 for x in lam if x >= j) for j in range(1, max(lam, default=0) + 1)]
    hook_product = 1
    for i, row in enumerate(lam):
        for j in range(1, row + 1):
            hook_product *= row - j + col_heights[j - 1] - i
    return math.factorial(n) // hook_product


def determinant(a: list[list[Fraction]]) -> Fraction:
    """Exact determinant by fraction-preserving Gaussian elimination."""
    m = len(a)
    a = [row[:] for row in a]
    sign = 1
    out = Fraction(1)
    for k in range(m):
        pivot = next((r for r in range(k, m) if a[r][k]), None)
        if pivot is None:
            return Fraction(0)
        if pivot != k:
            a[k], a[pivot] = a[pivot], a[k]
            sign = -sign
        z = a[k][k]
        out *= z
        for r in range(k + 1, m):
            if a[r][k]:
                factor = a[r][k] / z
                for c in range(k + 1, m):
                    a[r][c] -= factor * a[k][c]
                a[r][k] = 0
    return sign * out


def complete_homogeneous(p: list[Fraction], n: int) -> list[Fraction]:
    """Coefficients of product_i (1-p_i t)^(-1), through degree n."""
    h = [Fraction(0) for _ in range(n + 1)]
    h[0] = Fraction(1)
    for x in p:
        for k in range(1, n + 1):
            h[k] += x * h[k - 1]
    return h


def schur_polynomial(lam: tuple[int, ...], p: list[Fraction]) -> Fraction:
    n = sum(lam)
    d = len(p)
    h = complete_homogeneous(p, n + d)
    a = []
    for i in range(1, d + 1):
        row = []
        for j in range(1, d + 1):
            k = lam[i - 1] - i + j
            row.append(Fraction(0) if k < 0 else h[k])
        a.append(row)
    return determinant(a)


def schur_weyl_probabilities(n: int, p: list[Fraction]) -> dict[tuple[int, ...], Fraction]:
    return {
        lam: hook_dimension(lam) * schur_polynomial(lam, p)
        for lam in partitions(n, len(p))
    }


def main() -> None:
    # Three adjacent gap scales: n^(-1/8), n^(-1/2), n^(-3/4).
    # Taking n=2^(8k) makes all gaps exactly rational dyadics.
    multiscale = []
    for k in (3, 4, 5):
        n = 2 ** (8 * k)
        gaps = [Fraction(1, 2**k), Fraction(1, 2 ** (4 * k)), Fraction(1, 2 ** (6 * k))]
        p = spectrum_from_adjacent_gaps(gaps)
        assert min(p) >= Fraction(1, 8) and max(p) <= Fraction(3, 8)
        b = collision_product(n, p)
        multiscale.append({
            "k": k,
            "n": n,
            "gaps": [str(g) for g in gaps],
            "spectrum": [str(x) for x in p],
            "B_n_exact": str(b),
            "log2_B_over_log2_n": math.log2(float(b)) / math.log2(n),
            "expected_limit": 2.25,
        })
    assert abs(multiscale[-1]["log2_B_over_log2_n"] - 2.25) < abs(multiscale[0]["log2_B_over_log2_n"] - 2.25)

    # Critical qubit sequence n=k^2, gap=3/k.  B_n is exactly 10 for every k.
    critical = []
    for k in (6, 12, 24, 48):
        n = k * k
        gap = Fraction(3, k)
        p = [Fraction(1, 2) + gap / 2, Fraction(1, 2) - gap / 2]
        assert min(p) >= Fraction(1, 4) and max(p) <= Fraction(3, 4)
        b = collision_product(n, p)
        assert b == 10
        critical.append({"k": k, "n": n, "gap": str(gap), "B_n_exact": str(b)})

    # Verify exact Schur-Weyl probabilities for spectra with distinct and
    # repeated eigenvalues.  Jacobi-Trudi plus hook lengths gives exact rationals.
    schur_cases = []
    spectra = [
        [Fraction(1, 2), Fraction(1, 3), Fraction(1, 6)],
        [Fraction(1, 2), Fraction(1, 4), Fraction(1, 4)],
        [Fraction(1, 4)] * 4,
    ]
    for p in spectra:
        for n in range(1, 9):
            q = schur_weyl_probabilities(n, p)
            total = sum(q.values(), Fraction(0))
            assert total == 1, (n, p, total)
            assert all(v >= 0 for v in q.values())
            schur_cases.append({"d": len(p), "n": n, "sectors": len(q), "sum_q_lambda": str(total)})

    report = {
        "status": "PASS: exact arithmetic fixtures; analytic theorem remains a candidate",
        "multiscale": multiscale,
        "critical_constant_B": critical,
        "schur_weyl_normalization_cases": len(schur_cases),
        "schur_weyl_cases": schur_cases,
        "scope": "Does not validate the uniform HCIZ estimate, orbit-ball geometry, or compression theorem.",
    }
    out = Path(__file__).with_name("collision_scalings_checks.json")
    out.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({
        "status": report["status"],
        "multiscale_log2_B_over_log2_n": [x["log2_B_over_log2_n"] for x in multiscale],
        "critical_B_values": [x["B_n_exact"] for x in critical],
        "schur_weyl_normalization_cases": report["schur_weyl_normalization_cases"],
        "output": str(out),
    }, indent=2))


if __name__ == "__main__":
    main()
