#!/usr/bin/env python3
"""Finite exact checks for principal-height cap/taper formulas in SU(m).

Enumerates Gelfand--Tsetlin patterns for small regular highest weights,
compares their stable shells and Cartan traces with the PBW product formula,
builds all-root conductances from exact commutator recurrences, and checks
the low-rank, near-full-rank, and global filters with Fraction arithmetic.
This is a finite algebra diagnostic, not a proof of the uniform bounds.
"""

from fractions import Fraction
from itertools import product
from math import comb, e, log


def highest_row(labels: tuple[int, ...]) -> tuple[int, ...]:
    m = len(labels) + 1
    return tuple(sum(labels[i:]) for i in range(m - 1)) + (0,)


def weyl_dimension(labels: tuple[int, ...]) -> int:
    row = highest_row(labels)
    value = Fraction(1)
    for i in range(len(row)):
        for j in range(i + 1, len(row)):
            value *= Fraction(row[i] - row[j] + j - i, j - i)
    assert value.denominator == 1
    return value.numerator


def gt_spectrum(labels: tuple[int, ...]):
    """Return depth multiplicities and root-coroot traces from GT patterns."""
    m = len(labels) + 1
    top = highest_row(labels)
    roots = [(i, j) for i in range(m) for j in range(i + 1, m)]
    counts: dict[int, int] = {}
    traces = {root: {} for root in roots}
    total = 0

    def descend(upper: tuple[int, ...], rows: tuple[tuple[int, ...], ...]):
        if len(upper) == 1:
            by_length = {len(row): row for row in rows}
            mu = []
            for length in range(1, m + 1):
                upper_sum = sum(by_length[length])
                lower_sum = sum(by_length.get(length - 1, ()))
                mu.append(upper_sum - lower_sum)
            h2 = [m + 1 - 2 * i for i in range(1, m + 1)]
            numerator = sum(
                h2[i] * (top[i] - mu[i]) for i in range(m)
            )
            assert numerator % 2 == 0
            q = numerator // 2
            assert q >= 0
            counts[q] = counts.get(q, 0) + 1
            for i, j in roots:
                by_q = traces[(i, j)]
                by_q[q] = by_q.get(q, 0) + mu[i] - mu[j]
            return 1

        ranges = [range(upper[i + 1], upper[i] + 1) for i in range(len(upper) - 1)]
        subtotal = 0
        for lower in product(*ranges):
            subtotal += descend(tuple(lower), rows + (tuple(lower),))
        return subtotal

    total = descend(top, (top,))
    assert total == weyl_dimension(labels)
    return counts, traces, roots


def pbw_shells(m: int, cutoff: int) -> list[int]:
    """Coefficients of prod_{ell=1}^{m-1}(1-z^ell)^(-(m-ell))."""
    coeff = [0] * (cutoff + 1)
    coeff[0] = 1
    for ell in range(1, m):
        for _ in range(m - ell):
            for q in range(ell, cutoff + 1):
                coeff[q] += coeff[q - ell]
    return coeff


def root_pairing(root: tuple[int, int], coroot: tuple[int, int]) -> int:
    k, l = root
    i, j = coroot
    return int(k == i) - int(k == j) - int(l == i) + int(l == j)


def pbw_traces(labels: tuple[int, ...], shells: list[int], roots):
    """Compute stable coroot trace coefficients using PBW first moments."""
    m = len(labels) + 1
    top = highest_row(labels)
    out = {coroot: [] for coroot in roots}
    cutoff = len(shells) - 1
    for coroot in roots:
        i, j = coroot
        lam_ij = top[i] - top[j]
        moment = [0] * (cutoff + 1)
        for root in roots:
            ell = root[1] - root[0]
            pairing = root_pairing(root, coroot)
            if not pairing:
                continue
            for q in range(cutoff + 1):
                moment[q] += pairing * sum(
                    shells[q - t * ell]
                    for t in range(1, q // ell + 1)
                )
        out[coroot] = [lam_ij * shells[q] - moment[q] for q in range(cutoff + 1)]
    return out


def conductances(traces, roots, max_depth: int):
    """Source-shell c_ij(q), using c(q+ell)-c(q)=s_ij(q)."""
    result = {}
    for root in roots:
        i, j = root
        ell = j - i
        values = [0] * (max_depth + 1)
        for q in range(ell, max_depth + 1):
            values[q] = values[q - ell] + traces[root].get(q - ell, 0)
        result[root] = values
    return result


def volume(shells: dict[int, int], r: int) -> int:
    return sum(v for q, v in shells.items() if q <= r)


def energy_norm(profile, counts, edge_weights, roots):
    max_depth = max(counts)
    norm2 = sum(Fraction(n) * profile(q) ** 2 for q, n in counts.items())
    energy = Fraction(0)
    for i, j in roots:
        ell = j - i
        c = edge_weights[(i, j)]
        for q in range(ell, max_depth + 1):
            delta = profile(q) - profile(q - ell)
            energy += c[q] * delta * delta
    return energy, norm2


def constants(m: int):
    p = m * (m - 1) // 2
    h = m - 1
    gamma = max(comb(2 * h + p, p), (2 * p * h * (p + 1)) ** p)
    roots3 = sum((m - ell) * ell**3 for ell in range(1, h + 1))
    low_const = 10 * (4 * p * h * (p + 1)) ** p * roots3
    taper_const = 1 + 5 * gamma * sum(
        (m - ell) * ell**3 for ell in range(2, h + 1)
    )
    s_const = Fraction(5, 2) * (m - 1) * p**p
    global_const = Fraction(384 * (m - 1) ** 2, m)
    return p, h, gamma, low_const, taper_const, s_const, global_const


def check_case(labels: tuple[int, ...], n_scale: int) -> None:
    m = len(labels) + 1
    p, h, gamma, low_c, taper_c, s_c, global_c = constants(m)
    counts, traces, roots = gt_spectrum(labels)
    d = weyl_dimension(labels)
    assert sum(counts.values()) == d
    max_depth = max(counts)
    assert max_depth % 2 == 0
    top_height = Fraction(max_depth, 2)
    predicted_top = Fraction(
        sum(label * r * (m - r) for r, label in enumerate(labels, start=1)), 2
    )
    assert top_height == predicted_top
    assert all(counts.get(q, 0) == counts.get(max_depth - q, 0) for q in counts)

    # Stable PBW shell counts and first Cartan moments.
    stable = n_scale // 4
    shells = pbw_shells(m, stable)
    pbw_moments = pbw_traces(labels, shells, roots)
    for q in range(stable + 1):
        assert counts.get(q, 0) == shells[q]
        for root in roots:
            assert traces[root].get(q, 0) == pbw_moments[root][q]
            ell = root[1] - root[0]
            assert Fraction(ell * n_scale, 2) * shells[q] <= traces[root].get(q, 0)
            assert traces[root].get(q, 0) <= Fraction(5 * ell * n_scale, 2) * shells[q]

    c = conductances(traces, roots, max_depth)
    for root in roots:
        i, j = root
        ell = j - i
        for q in range(ell, stable + 1):
            assert c[root][q] >= 0
            assert c[root][q] <= Fraction(5, 2) * ell * n_scale * volume(counts, q - ell)
            for step in range(ell):
                edge = q - step
                if edge >= 1:
                    c1 = sum(c[(r, r + 1)][edge] for r in range(m - 1))
                    assert c[root][q] <= 5 * ell * gamma * c1
    for q in range(1, stable + 1):
        c1 = sum(c[(r, r + 1)][q] for r in range(m - 1))
        assert c1 >= Fraction(n_scale, 2) * volume(counts, q - 1)

    # Low-rank ramp with exact integer rank and the uniform displayed bound.
    r0 = stable
    assert r0 >= 1
    q0 = volume(counts, r0 - 1)
    budgets = sorted({1, max(1, q0 // 2), q0})
    for budget in budgets:
        radius = 1
        while radius < r0 and volume(counts, radius) <= budget:
            radius += 1
        rank = volume(counts, radius - 1)
        assert rank <= budget
        f = lambda q, R=radius: max(Fraction(0), Fraction(R - q, R))
        en, norm2 = energy_norm(f, counts, c, roots)
        assert norm2 >= Fraction(radius**p, 4 * (4 * p * h) ** p)
        assert en <= Fraction(5, 2) * (p + 1) ** p * sum(
            (m - ell) * ell**3 for ell in range(1, h + 1)
        ) * n_scale * radius ** (p - 1)
        assert en / norm2 <= low_c * n_scale / radius

    # Harmonic near-full taper; choose a cap budget within the stable window.
    M = stable
    r_star = max(1, M // 2)
    c1 = {q: sum(c[(r, r + 1)][q] for r in range(m - 1)) for q in range(M + 1)}
    k0 = volume(counts, r_star - 1)
    for k in sorted({1, k0}):
        R = 0
        while volume(counts, R) < k:
            R += 1
        assert R < r_star
        B = R + 1
        assert B <= M
        rho = sum((Fraction(1, c1[q]) for q in range(B, M + 1)), Fraction(0))
        assert rho > 0

        def alpha(q: int) -> Fraction:
            if q <= R:
                return Fraction(1)
            if q >= M:
                return Fraction(0)
            return sum((Fraction(1, c1[j]) for j in range(q + 1, M + 1)), Fraction(0)) / rho

        x = lambda q: 1 - alpha(q)
        en, norm2 = energy_norm(x, counts, c, roots)
        e1 = sum(
            c1[q] * (x(q) - x(q - 1)) ** 2 for q in range(1, M + 1)
        )
        nullity = volume(counts, R)
        assert nullity >= k
        assert d - nullity <= d - k
        assert e1 == 1 / rho
        assert en <= taper_c * e1
        assert norm2 >= Fraction(d, 2)

    # Global half-rank positive-part filter for the endpoint patch.
    L = top_height
    gx = lambda q: max(Fraction(0), Fraction(q, 1) / L - 1)
    gen, gnorm = energy_norm(gx, counts, c, roots)
    grank = sum(v for q, v in counts.items() if Fraction(q) > L)
    assert grank <= d // 2
    assert gnorm > 0
    assert gen / gnorm <= global_c

    # SU(2)'s all-the-way one-dimensional resistance has the explicit
    # harmonic-number/log form used in the p=1 endpoint statement.
    if m == 2:
        n = labels[0]
        M1 = n // 2
        k1 = M1 // 4
        for k in sorted({1, k1}):
            R1 = k - 1
            rho1 = sum(
                (Fraction(1, q * (n - q + 1)) for q in range(k, M1 + 1)),
                Fraction(0),
            )
            assert rho1 == sum(
                (Fraction(1, n + 1) * (Fraction(1, q) + Fraction(1, n + 1 - q))
                 for q in range(k, M1 + 1)),
                Fraction(0),
            )

            def alpha1(q: int) -> Fraction:
                if q <= R1:
                    return Fraction(1)
                if q >= M1:
                    return Fraction(0)
                return sum(
                    (Fraction(1, j * (n - j + 1)) for j in range(q + 1, M1 + 1)),
                    Fraction(0),
                ) / rho1

            x1 = lambda q: 1 - alpha1(q)
            en1, norm1 = energy_norm(x1, counts, c, roots)
            assert en1 == 1 / rho1
            assert norm1 >= Fraction(d, 2)
            assert float(en1 / norm1) <= 6 / log(e * d / k)

    print(
        f"SU({m}) labels={labels} d={d} stable={stable} low_rank_cap={q0} "
        f"near_nullity_sample={k}/{d} global_ratio={float(gen/gnorm):.8g}; checks passed"
    )


def main() -> None:
    check_case((40,), 40)
    check_case((40, 40), 40)
    check_case((8, 8, 8), 8)


if __name__ == "__main__":
    main()
