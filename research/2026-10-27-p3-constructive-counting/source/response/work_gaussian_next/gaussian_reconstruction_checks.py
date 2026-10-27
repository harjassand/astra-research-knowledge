#!/usr/bin/env python3
"""Exact finite checks for Gaussian replacement failures; no speed claims.

Standard library only. Run from any directory. The JSON is written beside this
file. No asymptotic source algorithm is implemented here.
"""
from collections import Counter
from itertools import combinations, product
from math import comb
from pathlib import Path
import json
import random


def rank(rows):
    pivots = {}
    for row in rows:
        while row:
            pivot = row.bit_length() - 1
            if pivot not in pivots:
                pivots[pivot] = row
                break
            row ^= pivots[pivot]
    return len(pivots)


def inverse(rows):
    n = len(rows)
    aug = [row | (1 << (n + i)) for i, row in enumerate(rows)]
    for col in range(n):
        pivot = next((j for j in range(col, n) if aug[j] >> col & 1), None)
        if pivot is None:
            return None
        aug[col], aug[pivot] = aug[pivot], aug[col]
        for j in range(n):
            if j != col and aug[j] >> col & 1:
                aug[j] ^= aug[col]
    return [row >> n for row in aug]


def matvec(rows, x):
    return sum(((row & x).bit_count() & 1) << i for i, row in enumerate(rows))


def qvalue(rows, x):
    value = 0
    for i, row in enumerate(rows):
        if x >> i & 1:
            value ^= (row & x & ~((1 << (i + 1)) - 1)).bit_count() & 1
    return value


def random_alternating(n, rng):
    rows = [0] * n
    for i in range(n):
        for j in range(i + 1, n):
            if rng.randrange(2):
                rows[i] |= 1 << j
                rows[j] |= 1 << i
    return rows


def fwht(values):
    out = list(values)
    h = 1
    while h < len(out):
        for start in range(0, len(out), h * 2):
            for j in range(start, start + h):
                a, b = out[j], out[j + h]
                out[j], out[j + h] = a + b, a - b
        h *= 2
    return out


def compress_bits(x, positions):
    return sum(((x >> pos) & 1) << j for j, pos in enumerate(positions))


def cross_rank(rows, mask):
    n = len(rows)
    other = ((1 << n) - 1) ^ mask
    return rank([rows[i] & other for i in range(n) if mask >> i & 1])


def gaussian_duality(rng):
    fixtures = walsh_entries = cut_checks = weighted_checks = 0
    for n in (2, 4, 6, 8, 10):
        for _ in range(8):
            while True:
                b = random_alternating(n, rng)
                bi = inverse(b)
                if bi is not None:
                    break
            signs = [(-1) ** qvalue(b, x) for x in range(1 << n)]
            transform = fwht(signs)
            g0 = transform[0]
            assert abs(g0) == 1 << (n // 2)
            for a in range(1 << n):
                dual = (-1) ** qvalue(b, matvec(bi, a))
                assert transform[a] == g0 * dual
                walsh_entries += 1
            for mask in range(1, (1 << n) - 1):
                assert cross_rank(b, mask) == cross_rank(bi, mask)
                cut_checks += 1
            # Arbitrary local group functions, not just phases.
            groups = [list(range(j, n, 3)) for j in range(3)]
            tables = [[rng.randrange(-3, 4) for _ in range(1 << len(g))]
                      for g in groups]
            hats = [fwht(t) for t in tables]
            direct = 0
            transformed = 0
            for x in range(1 << n):
                value = signs[x]
                dual = (-1) ** qvalue(b, matvec(bi, x))
                for g, f, fh in zip(groups, tables, hats):
                    a = compress_bits(x, g)
                    value *= f[a]
                    dual *= fh[a]
                direct += value
                transformed += dual
            assert (1 << n) * direct == g0 * transformed
            weighted_checks += 1
            fixtures += 1
    return dict(fixtures=fixtures, walsh_entries=walsh_entries,
                cut_rank_equalities=cut_checks, weighted_duality=weighted_checks)


class GF2e:
    def __init__(self, degree, modulus):
        self.degree = degree
        self.modulus = modulus
        self.q = 1 << degree

    def mul(self, a, b):
        out = 0
        while b:
            if b & 1:
                out ^= a
            b >>= 1
            a <<= 1
            if a & self.q:
                a ^= self.modulus
        return out

    def power(self, a, k):
        out = 1
        while k:
            if k & 1:
                out = self.mul(out, a)
            a = self.mul(a, a)
            k >>= 1
        return out

    def trace(self, a):
        out = 0
        for _ in range(self.degree):
            out ^= a
            a = self.mul(a, a)
        assert out in (0, 1)
        return out

    def jet(self, coeffs, t, order):
        out = 0
        for i in range(order, len(coeffs)):
            if (i & order) == order:
                out ^= self.mul(coeffs[i], self.power(t, i - order))
        return out


def finite_field_jets():
    fixtures = histograms = scalar_observations = total_coefficients = 0
    examples = []
    for e, modulus, degree in ((1, 0b11, 1), (2, 0b111, 1),
                               (2, 0b111, 3), (3, 0b1011, 2),
                               (4, 0b10011, 2)):
        field = GF2e(e, modulus)
        coeffs = list(product(range(field.q), repeat=degree + 1))
        total_coefficients += len(coeffs)
        populations = [[c for c in coeffs if field.trace(c[0]) == sign]
                       for sign in (0, 1)]
        assert len(populations[0]) == len(populations[1]) == len(coeffs) // 2
        for t in range(1, field.q):
            for order in range(1, degree + 1):
                hist = []
                for population in populations:
                    hist.append(Counter(tuple(field.jet(c, t, j) for j in range(order))
                                        for c in population))
                assert hist[0] == hist[1]
                assert len(hist[0]) == field.q ** order
                assert len(set(hist[0].values())) == 1
                histograms += 1
                # Enumerate all additive characters of the complete observed jet.
                for lambdas in product(range(field.q), repeat=order):
                    vals = []
                    for h in hist:
                        total = 0
                        for jet, multiplicity in h.items():
                            dot = 0
                            for a, b in zip(lambdas, jet):
                                dot ^= field.mul(a, b)
                            total += multiplicity * (-1) ** field.trace(dot)
                        vals.append(total)
                    assert vals[0] == vals[1]
                    scalar_observations += 1
        targets = [sum((-1) ** field.trace(c[0]) for c in pop) for pop in populations]
        assert targets == [len(coeffs) // 2, -len(coeffs) // 2]
        examples.append(dict(field_order=field.q, polynomial_degree=degree,
                             population_size=len(coeffs) // 2, target_sums=targets))
        fixtures += 1
    return dict(fixtures=fixtures, complete_jet_histogram_equalities=histograms,
                additive_character_observations=scalar_observations,
                coefficient_vectors=total_coefficients, examples=examples)


def positive_compositions(total, length):
    if length == 1:
        yield (total,)
    else:
        for first in range(1, total - length + 2):
            for rest in positive_compositions(total - first, length - 1):
                yield (first,) + rest


def joint_jet_threshold():
    histograms = full_threshold_checks = 0
    examples = []
    for e, modulus, degree in ((2, 0b111, 3), (3, 0b1011, 2), (4, 0b10011, 2)):
        field = GF2e(e, modulus)
        coeffs = list(product(range(field.q), repeat=degree + 1))
        populations = [[c for c in coeffs if field.trace(c[0]) == sign]
                       for sign in (0, 1)]
        jets = {c: {t: tuple(field.jet(c, t, j) for j in range(degree + 1))
                    for t in range(1, field.q)} for c in coeffs}
        this_histograms = 0
        for total in range(1, degree + 1):
            for count in range(1, min(total, field.q - 1) + 1):
                for nodes in combinations(range(1, field.q), count):
                    for orders in positive_compositions(total, count):
                        hist = []
                        for population in populations:
                            hist.append(Counter(tuple(value for t, order in zip(nodes, orders)
                                                      for value in jets[c][t][:order])
                                                for c in population))
                        assert hist[0] == hist[1]
                        assert len(hist[0]) == field.q ** total
                        assert len(set(hist[0].values())) == 1
                        histograms += 1
                        this_histograms += 1
        # Exactly D+1 joint coordinates determine c; choose several nodes.
        nodes = tuple(range(1, min(degree + 1, field.q - 1) + 1))
        orders = (degree + 2 - len(nodes),) + (1,) * (len(nodes) - 1)
        hist = []
        for population in populations:
            hist.append(Counter(tuple(value for t, order in zip(nodes, orders)
                                      for value in jets[c][t][:order]) for c in population))
        assert not (hist[0].keys() & hist[1].keys())
        assert len(hist[0]) + len(hist[1]) == len(coeffs)
        assert set(hist[0].values()) == {1} == set(hist[1].values())
        full_threshold_checks += 1
        examples.append(dict(field_order=field.q, degree=degree,
                             deficient_joint_histograms=this_histograms,
                             sufficient_nodes=list(nodes), sufficient_orders=list(orders)))
    return dict(deficient_joint_histogram_equalities=histograms,
                exact_threshold_injectivity=full_threshold_checks, examples=examples)


def valuation(x):
    if x == 0:
        return None
    x = abs(x)
    return (x & -x).bit_length() - 1


def gaussian_moment_precision(rng):
    block_fixtures = coefficients = tails = 0
    for m in range(1, 6):
        n = 3 * m
        observed = [0] * (m + 1)
        for x in range(1 << n):
            quadratic = 0
            active = 0
            for j in range(m):
                a, b, c = [(x >> (3 * j + k)) & 1 for k in range(3)]
                quadratic ^= a & b
                active += a & b & c
            for t in range(active + 1):
                observed[t] += (-1) ** quadratic * (-2) ** t * comb(active, t)
        expected = [comb(m, t) * 2 ** (2 * m - t) for t in range(m + 1)]
        assert observed == expected
        assert sum(observed) == 6 ** m
        assert valuation(observed[-1]) == m
        for cut in range(1, m + 1):
            assert sum(observed[cut:]) % (1 << (n + 2)) != 0
            tails += 1
        coefficients += m + 1
        block_fixtures += 1

    moment_checks = 0
    for n in (4, 6, 8, 10):
        for _ in range(8):
            b = random_alternating(n, rng)
            monomials = [sum(1 << v for v in rng.sample(range(n), 3)) for _ in range(5)]
            for selection in range(1 << len(monomials)):
                fixed = 0
                for j, monomial in enumerate(monomials):
                    if selection >> j & 1:
                        fixed |= monomial
                remaining = ((1 << n) - 1) ^ fixed
                mfree = n - fixed.bit_count()
                rfree = rank([b[i] & remaining for i in range(n) if remaining >> i & 1])
                assert rfree % 2 == 0
                moment = sum((-1) ** qvalue(b, x) for x in range(1 << n)
                             if x & fixed == fixed)
                if moment:
                    assert abs(moment) == 1 << (mfree - rfree // 2)
                    t = selection.bit_count()
                    term = (-2) ** t * moment
                    assert valuation(term) >= t + (max(0, n - 3 * t) + 1) // 2
                moment_checks += 1
    return dict(block_fixtures=block_fixtures, exact_coefficients=coefficients,
                failed_truncations=tails, gaussian_moment_checks=moment_checks,
                obstruction_formula="H_m(V)=(4+2V)^m; n=3m; H_m(1)=6^m")


def main():
    rng = random.Random(2026102703)
    results = {
        "scope": "Exact tests of restricted reconstruction failures, not an algorithmic lower bound",
        "gaussian_fourier_duality": gaussian_duality(rng),
        "finite_field_jet_obstruction": finite_field_jets(),
        "joint_jet_threshold": joint_jet_threshold(),
        "gaussian_moment_precision": gaussian_moment_precision(rng),
    }
    path = Path(__file__).with_name("gaussian_reconstruction_results.json")
    path.write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
