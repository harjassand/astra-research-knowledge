"""Exact fourth-root Pfaffian samples, moments, and bounded independent audits.

All output is owned by c01_s01. No peer code is executed. Gaussian-rational
arithmetic is reused only from this worker's own earlier implementation.
"""
from fractions import Fraction as Q
from itertools import combinations, product
from math import comb, factorial
from pathlib import Path
from time import perf_counter
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from near_monomial_dp import G
from cutrank_mps import det, pfaffian, adjoint, matmul, factor_rect

PHASES = (G(1), G(-1), G(0, 1), G(0, -1))


def conv(F):
    return [[x if isinstance(x, G) else G(x) for x in row] for row in F]


def scalar(x):
    return G(x)


def lift(F, z):
    n = len(F)
    return [[z[i] * F[i][j] - z[j] * F[j][i] for j in range(n)]
            for i in range(n)]


def sample_direct(F, z, k):
    A = lift(F, z)
    return sum((pfaffian([[A[i][j] for j in R] for i in R]).abs2()
                for R in combinations(range(len(F)), 2 * k)), Q(0))


def sample_formal(F, z):
    """Polynomial ring-operation implementation: Newton traces + formal root.

    The Gaussian normal-form identity is justified in the accompanying proof.
    No principal-Pfaffian enumeration is used here.
    """
    n = len(F)
    A = lift(F, z)
    B = matmul(adjoint(A), A)
    power = [[G(int(i == j)) for j in range(n)] for i in range(n)]
    traces, elementary = [Q(0)], [Q(1)]
    for r in range(1, n // 2 + 1):
        power = matmul(power, B)
        tr = sum((power[i][i] for i in range(n)), G())
        assert not tr.im
        traces.append(tr.re)
        e = sum(((-1) ** (j - 1) * elementary[r - j] * traces[j]
                 for j in range(1, r + 1)), Q(0)) / r
        elementary.append(e)
    root = [Q(1)]
    for r in range(1, n // 2 + 1):
        root.append((elementary[r] - sum((root[j] * root[r - j]
                     for j in range(1, r)), Q(0))) / 2)
    assert all(x >= 0 for x in root)
    return root


def coefficients(F, k):
    """Tiny-fixture exterior coefficient vectors a_S; exponential audit only."""
    n = len(F)
    rows = list(combinations(range(n), 2 * k))
    answer = {}
    for S in combinations(range(n), k):
        vec = []
        for R in rows:
            M = []
            for i in R:
                row = []
                for j in S:
                    row += [G(int(i == j)), F[j][i]]
                M.append(row)
            vec.append(det(M))
        answer[S] = tuple(vec)
    return answer


def inner(a, b):
    return sum((x.conjugate() * y for x, y in zip(a, b)), G())


def vector_sample(coeff, z):
    width = len(next(iter(coeff.values())))
    v = [G() for _ in range(width)]
    for S, a in coeff.items():
        character = G(1)
        for i in S:
            character *= z[i]
        v = [x + character * y for x, y in zip(v, a)]
    return sum((x.abs2() for x in v), Q(0))


def moments(coeff):
    """Exact Fourier grouping; does not enumerate phase samples."""
    mu = sum((inner(a, a).re for a in coeff.values()), Q(0))
    channels = {}
    support = [S for S, a in coeff.items() if any(a)]
    diameter = 0
    for S, a in coeff.items():
        for T, b in coeff.items():
            U, V = tuple(sorted(set(S) - set(T))), tuple(sorted(set(T) - set(S)))
            key = (U, V)
            channels[key] = channels.get(key, G()) + inner(b, a)
            if any(a) and any(b):
                diameter = max(diameter, len(U))
    assert channels[((), ())] == G(mu)
    variance = sum((v.abs2() for key, v in channels.items() if key != ((), ())), Q(0))
    second = mu * mu + variance
    assert second <= comb(2 * diameter, diameter) * mu * mu
    return mu, second, diameter, len(support)


def cycle_matrix(lengths, weights=None):
    n = sum(lengths)
    F = [[G() for _ in range(n)] for _ in range(n)]
    at = 0
    if weights is None:
        weights = [G(1)] * n
    for ell in lengths:
        for j in range(ell):
            F[at + j][at + (j + 1) % ell] = weights[at + j]
        at += ell
    return F


def monomial_bound(lengths, weights):
    at, result = 0, Q(1)
    for ell in lengths:
        if ell % 2:
            at += ell
            continue
        a, b = Q(1), Q(1)
        for j in range(ell):
            if j % 2:
                b *= weights[at + j].abs2()
            else:
                a *= weights[at + j].abs2()
        if a + b:
            result *= 1 + 2 * a * b / (a + b) ** 2
        at += ell
    return result


def independent_peer_audit():
    """Independently reconstruct the finite mathematical claims being reviewed."""
    receipt = {"peer_code_executed": False}
    for exponent in (2, 7, 20):
        e = Q(1, 2 ** exponent)
        F = [[G() for _ in range(6)] for _ in range(6)]
        for i in range(6):
            F[i][(i + 1) % 6] = G(1)
            F[i][(i - 1) % 6] = G(e)
        weights = {}
        amps = {}
        for I in combinations(range(6), 3):
            J = tuple(i for i in range(6) if i not in I)
            a = det([[F[i][j] for j in J] for i in I])
            assert not a.im
            amps[I] = a.re
            if a:
                weights[I] = a.abs2()
        counts = {str(value): list(amps.values()).count(value)
                  for value in set(amps.values())}
        assert sorted(counts.values()) == [2, 6, 6, 6]
        assert list(amps.values()).count(1 + e ** 3) == 2
        assert list(amps.values()).count(e) == 6
        assert list(amps.values()).count(e ** 2) == 6
        assert list(amps.values()).count(0) == 6
        Z = sum(weights.values(), Q(0))
        a = (1 + e ** 3) ** 2
        assert Z == 2 * a + 6 * e ** 2 + 6 * e ** 4
        O = (1, 3, 5)
        neigh = [I for I in weights if len(set(I) - set(O)) == 1]
        phi = sum((min(weights[I], weights[O]) for I in neigh), Q(0)) / (9 * weights[O])
        assert phi == (e ** 2 + e ** 4) / (3 * a)
        reached, todo = {O}, [O]
        while todo:
            I = todo.pop()
            for J in weights:
                if J not in reached and len(set(I) - set(J)) == 1:
                    reached.add(J)
                    todo.append(J)
        assert len(reached) == 14
        sign = {I: 1 if sum(i % 2 == 0 for i in I) >= 2 else -1 for I in weights}
        assert sum((weights[I] * sign[I] for I in weights), Q(0)) == 0
        for radius, target in ((1, 3 * e ** 2 + 15 * e ** 4),
                               (2, 12 * e ** 2 + 12 * e ** 4)):
            cut = sum((min(weights[I], weights[J]) for I in weights for J in weights
                       if I < J and sign[I] != sign[J]
                       and len(set(I) - set(J)) == radius), Q(0))
            assert cut == target
        s = 2 * a * a / (Z * Z)
        phi12 = phi / 2
        assert 3 * (1 - s) / phi12 > 0
    receipt["ring_precision_exponents"] = [2, 7, 20]
    receipt["ring_amplitude_classes_and_connectedness"] = "PASS"
    receipt["radius_one_two_cut_sums"] = "PASS"
    for n in (4, 6, 12, 20):
        M = comb(n, n // 2)
        a = Q(1, M)
        y = 1 / (1 + 2 * a)
        energy = 2 * a * (1 + y * y) / 3 + (1 - y) ** 2 / 3
        assert 1 / energy == Q(3 * M * (M + 2), 4 * (M + 1))
    receipt["uniform_MH_optimal_additive_constant"] = "PASS"
    return receipt


def dense_family(n):
    m = n // 2
    # Integer-scaled symmetric Cauchy matrix: every square subminor is nonzero.
    H = factorial(2 * n)
    B = factorial(m) * (1 + H) ** m
    N = comb(n, m)
    # A dyadic choice makes the input encoding explicit and all arithmetic exact.
    h = (128 * N * B).bit_length()
    eta = Q(1, 2 ** h)
    F0 = cycle_matrix([2] * m)
    F = [[F0[i][j] + G(eta * (H // (i + j + 1))) for j in range(n)] for i in range(n)]
    return F, eta, B


def run_checks():
    start = perf_counter()
    receipt = {"status": "PASS", "method": "Gaussian rational arithmetic",
               "peer_audit": independent_peer_audit()}
    fixtures = [conv([[0, G(2, 1), -1, G(1, -2)],
                      [3, 0, G(1, 1), 2],
                      [G(0, 2), 1, 0, -2],
                      [1, -1, 3, 0]]),
                conv([[0, Q(1, 2), G(Q(1, 3), Q(1, 4))],
                      [2, 0, -1], [G(1, 1), Q(2, 3), 0]])]
    phases_checked, formal_checked, fixture_rows = 0, 0, []
    for fno, F in enumerate(fixtures):
        n = len(F)
        for k in range(n // 2 + 1):
            a = coefficients(F, k)
            mu, second, diameter, support = moments(a)
            total = total2 = Q(0)
            for index, z in enumerate(product(PHASES, repeat=n)):
                x = sample_direct(F, z, k)
                assert x == vector_sample(a, z)
                total += x
                total2 += x * x
                phases_checked += 1
                if index < 8:
                    assert x == sample_formal(F, z)[k]
                    formal_checked += 1
            assert total / 4 ** n == mu
            assert total2 / 4 ** n == second
            fixture_rows.append({"fixture": fno, "n": n, "k": k,
                                 "mean": str(mu), "second": str(second),
                                 "support_size": support, "support_diameter": diameter})
    receipt["phase_sector_checks"] = phases_checked
    receipt["formal_polynomial_sample_checks"] = formal_checked
    receipt["generic_fixtures"] = fixture_rows
    cycle_receipts = []
    for lengths in ([4], [6], [8], [2, 2], [2, 4], [2, 2, 2], [3, 3], [3, 5]):
        n = sum(lengths)
        weights = [G(1) for _ in range(n)]
        F = cycle_matrix(lengths, weights)
        bound = monomial_bound(lengths, weights)
        for k in range(n // 2 + 1):
            mu, second, _, _ = moments(coefficients(F, k))
            assert second <= bound * mu * mu
            if k == n // 2 and all(ell % 2 == 0 for ell in lengths):
                assert second == bound * mu * mu
        cycle_receipts.append({"cycles": lengths, "uniform_second_moment_bound": str(bound)})
    # Strongly biased dense-sector cycles: number of sites grows but the variance
    # per two-cycle is suppressed by its acquired amplitude imbalance.
    weights = [G(1), G(Q(1, 16)), G(1), G(Q(1, 16)), G(1), G(Q(1, 16))]
    F = cycle_matrix([2, 2, 2], weights)
    mu, second, _, _ = moments(coefficients(F, 3))
    assert second == monomial_bound([2, 2, 2], weights) * mu * mu
    receipt["permutation_cycle_checks"] = cycle_receipts
    receipt["biased_cycle_relative_second"] = str(second / (mu * mu))
    dense_receipts = []
    for n in (4, 6, 8):
        F, eta, B = dense_family(n)
        k = n // 2
        coeff = coefficients(F, k)
        mu, second, diameter, support = moments(coeff)
        assert support == comb(n, k)
        assert all(F[i][j] == F[j][i] and F[i][j].re > 0
                   for i in range(n) for j in range(n))
        assert abs(mu - 2 ** k) <= Q(3, 128)
        assert second / (mu * mu) >= Q(1, 2) * Q(3, 2) ** k
        # At a phase string where the old top Pfaffian vanishes, the perturbed
        # sample remains far below half its positive mean. No phase integration
        # of the dense family is needed for its confidence lower bound.
        bad_phase = tuple(G(1) for _ in range(n))
        assert sample_direct(F, bad_phase, k) <= Q(1, 128 ** 2)
        for cut in range(1, n):
            rank1 = factor_rect([row[cut:] for row in F[:cut]])[0]
            rank2 = factor_rect([row[:cut] for row in F[cut:]])[0]
            assert rank1 == rank2 == min(cut, n - cut)
        dense_receipts.append({"n": n, "k": k, "eta_bits": eta.denominator.bit_length(),
                               "support_size": support, "support_diameter": diameter,
                               "symmetric_and_every_entry_positive": True,
                               "relative_second_decimal": float(second / (mu * mu)),
                               "exact_ratio_numerator_bits": second.numerator.bit_length(),
                               "cross_cut_ranks": "full on every natural cut"})
    receipt["dense_positive_full_support_checks"] = dense_receipts
    receipt["seconds"] = perf_counter() - start
    return receipt


if __name__ == "__main__":
    out = run_checks()
    Path(__file__).with_name("phase_pfaffian_checks.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))
