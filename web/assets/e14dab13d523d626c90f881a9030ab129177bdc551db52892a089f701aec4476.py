#!/usr/bin/env python3
"""Exact finite checks for the principal-Cartan SU(3) shell taper.

Uses integer GT-pattern enumeration, Fraction arithmetic for the taper, and
the root commutator identities [E_ij,E_ji]=E_ii-E_jj. This checks the shell
counts, Cartan traces, conductance recurrences, cutoff rank, and energy
decomposition for selected finite regular highest weights.
"""

from fractions import Fraction
from math import floor, sqrt


def dimension(a: int, b: int) -> int:
    return (a + 1) * (b + 1) * (a + b + 2) // 2


def shell_volume(r: int) -> int:
    if r < 0:
        return 0
    if r % 2 == 0:
        t = r // 2
        return (t + 1) * (t + 2) * (4 * t + 3) // 6
    t = (r - 1) // 2
    return (t + 1) * (t + 2) * (4 * t + 9) // 6


def gt_shells(a: int, b: int):
    """Enumerate all GT basis states in (x,y,z) cap coordinates."""
    counts = {}
    e11_counts = {}
    traces = {"12": {}, "23": {}, "13": {}}
    total = 0
    for x in range(a + 1):
        for y in range(b + 1):
            for z in range(a - x + y + 1):
                q = 2 * x + y + z
                t = x + y
                h12 = a - x + y - 2 * z
                h23 = b - x - 2 * y + z
                h13 = a + b - q
                counts[q] = counts.get(q, 0) + 1
                e11_counts[t] = e11_counts.get(t, 0) + 1
                traces["12"][q] = traces["12"].get(q, 0) + h12
                traces["23"][q] = traces["23"].get(q, 0) + h23
                traces["13"][q] = traces["13"].get(q, 0) + h13
                total += 1
    assert total == dimension(a, b)
    return counts, e11_counts, traces


def principal_cap_shell(q: int) -> int:
    return ((q + 2) ** 2) // 4


def conductances(traces, m: int):
    """Return source-shell conductances for jumps 1, 1, and 2."""
    c12, c23, c13 = {}, {}, {}
    running12 = Fraction(0)
    running23 = Fraction(0)
    for q in range(m + 1):
        c12[q] = running12
        c23[q] = running23
        running12 += traces["12"].get(q, 0)
        running23 += traces["23"].get(q, 0)
    for q in range(m + 2):
        c13[q] = sum(
            (traces["13"].get(p, 0) for p in range(q - 1) if p % 2 == q % 2),
            Fraction(0),
        )
    return c12, c23, c13


def least_cap_radius(qnull: int) -> int:
    r = 0
    while shell_volume(r) < qnull:
        r += 1
    return r


def e11_exact_ratio(n: int, a: int, b: int, qnull: int, e11_counts) -> float:
    """Reconstruct the existing E_11 harmonic filter's exact finite ratio."""
    r = 0
    while (a + 1) * (r + 1) * (r + 2) // 2 < qnull:
        r += 1
    cutoff = n // 2
    assert r < cutoff
    weights = {
        t: Fraction((a + 1) * (t + 1) * (t + 2) * (a + 2 * b - 2 * t), 2)
        for t in range(r, cutoff)
    }
    rho = sum((Fraction(1, weights[t]) for t in range(r, cutoff)), Fraction(0))

    def alpha(t: int) -> Fraction:
        if t <= r:
            return Fraction(1)
        if t >= cutoff:
            return Fraction(0)
        return sum((Fraction(1, weights[j]) for j in range(t, cutoff)), Fraction(0)) / rho

    norm2 = sum(Fraction(v) * (1 - alpha(t)) ** 2 for t, v in e11_counts.items())
    return float((1 / rho) / norm2)


def check_one(n: int, a: int, b: int, qnull: int) -> tuple[float, float, float]:
    assert n <= a <= 2 * n and n <= b <= 2 * n
    d = dimension(a, b)
    assert 1 <= qnull <= d // 512
    counts, e11_counts, traces = gt_shells(a, b)
    m = min(a, b)

    # Exact cap shell and Cartan-trace formulas for all q used by this taper.
    r = least_cap_radius(qnull)
    cutoff = 2 * (r + 1)
    assert cutoff <= m
    for q in range(cutoff):
        g = principal_cap_shell(q)
        assert counts.get(q, 0) == g
        assert traces["12"].get(q, 0) == (Fraction(a) - Fraction(q, 2)) * g
        assert traces["23"].get(q, 0) == (Fraction(b) - Fraction(q, 2)) * g
        assert traces["13"].get(q, 0) == (a + b - q) * g
        assert shell_volume(q) == sum(principal_cap_shell(j) for j in range(q + 1))

    c12, c23, c13 = conductances(traces, m)
    c1 = {q: c12[q] + c23[q] for q in range(m + 1)}
    for q in range(m):
        assert c12[q + 1] - c12[q] == traces["12"].get(q, 0)
        assert c23[q + 1] - c23[q] == traces["23"].get(q, 0)
        assert c13[q + 2] - c13[q] == traces["13"].get(q, 0)
    for q in range(1, m + 1):
        lower = Fraction(m * q * (q + 1) * (2 * q + 1), 48)
        upper = Fraction(m * (q + 1) * (q + 2) * (2 * q + 3), 12)
        assert lower <= c12[q] <= upper
        assert lower <= c23[q] <= upper
    for q in range(2, m + 2):
        assert Fraction(m * q**3, 128) <= c13[q] <= Fraction(2 * m * q**3, 3)

    rho = sum((Fraction(1, c1[q]) for q in range(r + 1, cutoff + 1)), Fraction(0))
    assert rho > 0
    gap = cutoff - r

    def alpha(q: int) -> Fraction:
        if q <= r:
            return Fraction(1)
        if q >= cutoff:
            return Fraction(0)
        return sum((Fraction(1, c1[j]) for j in range(q + 1, cutoff + 1)), Fraction(0)) / rho

    profile = [alpha(q) for q in range(max(counts) + 1)]
    assert all(Fraction(0) <= x <= 1 for x in profile)
    assert all(profile[i] >= profile[i + 1] for i in range(len(profile) - 1))
    nullity = sum(v for q, v in counts.items() if q <= r)
    assert nullity == shell_volume(r) >= qnull
    assert d - nullity <= d - qnull
    norm2 = sum(Fraction(v) * (1 - alpha(q)) ** 2 for q, v in counts.items())
    assert norm2 >= Fraction(7 * d, 8)

    e1 = sum(
        c1[q] * (alpha(q) - alpha(q - 1)) ** 2
        for q in range(1, cutoff + 1)
    )
    e2 = sum(
        c13[q] * (alpha(q) - alpha(q - 2)) ** 2
        for q in range(2, cutoff + 2)
    )
    energy = e1 + e2
    assert e1 == 1 / rho
    assert e2 <= 4 * e1
    assert energy <= 5 / rho
    assert energy <= 60 * m * (r + 1) ** 2

    ratio = float(energy / norm2)
    assert energy / norm2 <= Fraction(480 * m * (r + 1) ** 2, 7 * d)
    e11_ratio = e11_exact_ratio(n, a, b, qnull, e11_counts)
    existing_e11_bound = 24 * n * n / d * (1 + sqrt(2 * qnull / n))
    print(
        f"N={n} (a,b)=({a},{b}) D={d} Q={qnull} R={r} M={cutoff} "
        f"nullity={nullity} principal_ratio={ratio:.8g} "
        f"E11_exact_ratio={e11_ratio:.8g} E11_bound={existing_e11_bound:.8g}"
    )
    return ratio, e11_ratio, existing_e11_bound


def main() -> None:
    cases = []
    for n, a, b in (
        (16, 16, 16),
        (16, 16, 32),
        (16, 32, 32),
        (24, 24, 48),
        (64, 64, 64),
        (128, 128, 128),
    ):
        d = dimension(a, b)
        qmax = d // 512
        if qmax:
            selected = {1, qmax, max(1, qmax // 2)}
            if n >= 64:
                selected.add(n)
            cases.extend((n, a, b, q) for q in sorted(selected))
    for case in cases:
        check_one(*case)


if __name__ == "__main__":
    main()
