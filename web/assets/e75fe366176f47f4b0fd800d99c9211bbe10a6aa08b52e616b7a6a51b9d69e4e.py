"""New exact U(4)/U(5) Pieri, physical branching and vacuum checks.

This does not rerun any earlier suite, or test an iid memory inequality.
Jacobi--Trudi character determinants independently check the decomposition
and normalization used in TOP_COLLISION_QUDIT_CONVERSE.txt.
"""
from fractions import Fraction as F
from itertools import permutations, product
from functools import lru_cache
from math import comb, factorial, gamma, pi, sqrt
from pathlib import Path
import json


def determinant(a):
    z = F(0)
    for perm in permutations(range(len(a))):
        sign = (-1) ** sum(perm[i] > perm[j]
                           for i in range(len(a)) for j in range(i + 1, len(a)))
        value = F(sign)
        for i, j in enumerate(perm):
            value *= a[i][j]
        z += value
    return z


@lru_cache(None)
def complete(xs, degree):
    h = [F(1)] + [F(0)] * degree
    for x in xs:
        for t in range(1, degree + 1):
            h[t] += x * h[t - 1]
    return tuple(h)


@lru_cache(None)
def character(weights, xs):
    assert len(weights) == len(xs)
    assert all(weights[i] >= weights[i + 1] for i in range(len(xs) - 1))
    shift = max(0, -weights[-1])
    lam = [x + shift for x in weights]
    h = complete(xs, lam[0] + len(xs) - 1)
    result = determinant([[h[t] if t >= 0 else F(0)
                           for j in range(len(xs))
                           for t in [lam[i] - i + j]]
                          for i in range(len(xs))])
    if shift:
        det_x = F(1)
        for x in xs:
            det_x *= x
        result /= det_x ** shift
    return result


def dimension(weights):
    result = F(1)
    for i in range(len(weights)):
        for j in range(i + 1, len(weights)):
            result *= F(weights[i] - weights[j] + j - i, j - i)
    assert result.denominator == 1
    return int(result)


def physical_components(top):
    bottom = list(top[1:]) + [0]
    yield from product(*(range(low, high + 1) for low, high in zip(bottom, top)))


def dual_pieri_components(top, number):
    total = sum(top) - number
    for prefix in product(*(range(top[i + 1], top[i] + 1)
                            for i in range(len(top) - 1))):
        last = total - sum(prefix)
        if last <= top[-1] and (not prefix or prefix[-1] >= last):
            yield tuple(prefix) + (last,)


def character_checks():
    model_sets = [
        ((F(3, 10), F(29, 100), F(7, 25)), F(13, 100),
         [(0, 0, 0), (1, 0, 0), (2, 1, 0), (2, 2, 0), (3, 1, 0)]),
        ((F(6, 25), F(23, 100), F(11, 50), F(21, 100)), F(1, 10),
         [(0, 0, 0, 0), (1, 0, 0, 0), (2, 1, 0, 0), (2, 2, 1, 0)]),
    ]
    carriers = []
    gap_count = dual_count = 0
    for xs, b, mus in model_sets:
        p = len(xs)
        assert sum(xs) + b == 1 and b < min(xs)
        qbar = b / min(xs)
        wstar = F(1)
        for x in xs:
            wstar *= 1 - b / x
        for mu in mus:
            for m in (1, 2, 3):
                top = tuple(m + v for v in mu)
                lam = top + (0,)
                r, d = dimension(top), dimension(lam)
                exact_ratio = F(1)
                for i in range(p):
                    exact_ratio *= F(m + mu[i] + p - i, p - i)
                assert F(d, r) == exact_ratio
                top_char = character(top, xs)
                full_char = character(lam, xs + (b,))
                physical_sum = F(0)
                layer_dims = {}
                components = list(physical_components(top))
                for nu in components:
                    number = sum(top) - sum(nu)
                    nu_char = character(nu, xs)
                    normalized_ratio = (nu_char / dimension(nu)) / (top_char / r)
                    assert normalized_ratio <= min(xs) ** (-number)
                    assert b ** number * normalized_ratio <= qbar ** number
                    physical_sum += b ** number * nu_char
                    layer_dims[number] = layer_dims.get(number, 0) + dimension(nu)
                    gap_count += 1
                assert physical_sum == full_char
                assert sum(layer_dims.values()) == d
                for number in range(m + 6):
                    rational_nus = list(dual_pieri_components(top, number))
                    lhs = sum((character(nu, xs) for nu in rational_nus), F(0))
                    rhs = top_char * complete(tuple(1 / x for x in xs), number)[number]
                    assert lhs == rhs
                    assert sum(dimension(nu) for nu in rational_nus) == r * comb(number + p - 1, p - 1)
                    expected_physical = sorted(nu for nu in rational_nus if nu[-1] >= 0)
                    observed_physical = sorted(nu for nu in components if sum(top) - sum(nu) == number)
                    assert expected_physical == observed_physical
                    if number <= m:
                        assert len(expected_physical) == len(rational_nus)
                    dual_count += 1
                vacuum = top_char / full_char
                physical_norm = wstar * full_char / top_char
                defect = 1 - physical_norm
                tail = qbar ** (m + 1) * sum((F(comb(m + j, j)) * (1 - qbar) ** j
                                             for j in range(p)), F(0))
                assert 0 <= defect <= tail
                assert vacuum == wstar / physical_norm
                assert vacuum >= (1 - qbar) ** p
                carriers.append({"p": p, "mu": list(mu), "m": m,
                                 "dimension": d, "fiber_rank": r,
                                 "vacuum_mass": float(vacuum),
                                 "physical_support_defect": float(defect),
                                 "negative_binomial_tail": float(tail)})
    return carriers, gap_count, dual_count


def scalar_walk_checks():
    count = 0
    largest_ratio = 0.0
    for p in range(1, 5):
        ap = 2 * p ** (2 * p - 1) / (factorial(p) * factorial(p - 1))
        bp = 2 ** (2 * p - 3) * (gamma(p) + 2 ** (2 * p - 1) * sqrt(pi))
        hp = ap * factorial(p) * (1 + bp) * (p + 2) ** p
        for m in range(1, 17):
            dm = comb(m + p, p)
            hs = [comb(ell + p, p) ** 2 - (comb(ell + p - 1, p) ** 2 if ell else 0)
                  for ell in range(m + 1)]
            beta = [F(factorial(m) * factorial(m + p),
                      factorial(m - ell) * factorial(m + p + ell))
                    for ell in range(m + 1)]
            assert sum(hs) == dm ** 2
            assert beta[0] == 1 and beta[1] == F(m, m + p + 1)
            for s in range(1, m + 2):
                value = sum((F(h) * be ** s for h, be in zip(hs, beta)), F(0)) / dm
                ratio = float(value) * s ** p / hp
                assert ratio <= 1
                largest_ratio = max(largest_ratio, ratio)
                count += 1
    return {"p_range": [1, 4], "m_range": [1, 16],
            "heat_fixtures": count, "largest_bound_ratio": largest_ratio}


def main():
    carriers, gap_count, dual_count = character_checks()
    result = {"status": "FINITE-EVIDENCE", "verdict": "PASS",
              "scope": "New exact U4/U5 characters, Pieri gap, dual-Pieri full-vs-physical branching, Weyl ratios and vacuum/tail normalization; scalar CPp heat constants only",
              "carriers": carriers, "component_gap_cases": gap_count,
              "dual_pieri_number_cases": dual_count,
              "scalar_walk": scalar_walk_checks(),
              "old_suites_rerun": False,
              "uniform_operator_iid_external_or_priority_validation": False}
    Path(__file__).with_suffix('.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: len(v) if k == 'carriers' else v for k, v in result.items()}, indent=2))


if __name__ == '__main__':
    main()
