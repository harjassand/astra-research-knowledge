"""Exact-rational check of the randomized hypergeometric elevation lemma.

This is a validation program, not the full conditional Bernoulli factory.
Production quantities use univariate moments and product-envelope factors.
For small fixtures only, full enumeration independently checks their values.
No physical experimental results are claimed.
"""
from fractions import Fraction as F
from math import comb, factorial
from itertools import product
from pathlib import Path
import json

from randomized_elevation import ProductEnvelope


def falling(n, k):
    ans = 1
    for j in range(k):
        ans *= n - j
    return ans


def stirling_second(n, k):
    row = [1]
    for i in range(1, n + 1):
        nxt = [0] * (i + 1)
        for j in range(1, i + 1):
            nxt[j] = (row[j - 1] if j - 1 < len(row) else 0) + (
                j * row[j] if j < len(row) else 0
            )
        row = nxt
    return row[k] if k < len(row) else 0


def centered_hypergeom_moments(n, s, order):
    """O(order^3) rational arithmetic, no sum over the n-sized support."""
    x = F(s, 2 * n)
    raw = []
    for k in range(order + 1):
        value = sum(
            (
                F(stirling_second(k, j) * falling(n, j) * falling(s, j),
                  falling(2 * n, j))
                if falling(2 * n, j) else F(0)
            )
            for j in range(k + 1)
        )
        raw.append(value)
    return [
        sum(F(comb(k, j)) * (-x) ** (k - j) * raw[j] / n ** j
            for j in range(k + 1))
        for k in range(order + 1)
    ]


def poly_add(a, b):
    out = dict(a)
    for key, val in b.items():
        out[key] = out.get(key, F(0)) + val
    return {k: v for k, v in out.items() if v}


def poly_mul(a, b, order):
    out = {}
    for ka, va in a.items():
        for kb, vb in b.items():
            key = tuple(x + y for x, y in zip(ka, kb))
            if sum(key) <= order:
                out[key] = out.get(key, F(0)) + va * vb
    return {k: v for k, v in out.items() if v}


def product_affine_series(x, sign, a, order):
    m = len(x)
    zero = (0,) * m
    out = {zero: F(1)}
    for i in range(m):
        key = tuple(int(j == i) for j in range(m))
        constant = a + (1 - a) * (x[i] if sign == 1 else 1 - x[i])
        out = poly_mul(out, {zero: constant, key: sign * (1 - a)}, order)
    return out


def ratio_series(x, a, order):
    """Taylor series of A/(A+B), A=prod(a+(1-a)x_i), B=prod(1-(1-a)x_i)."""
    m = len(x)
    zero = (0,) * m
    aa = product_affine_series(x, 1, a, order)
    bb = product_affine_series(x, -1, a, order)
    zz = poly_add(aa, bb)
    z0 = zz.pop(zero)
    u = {k: -v / z0 for k, v in zz.items()}
    power = {zero: F(1)}
    inv = {zero: F(1)}
    for _ in range(order):
        power = poly_mul(power, u, order)
        inv = poly_add(inv, power)
    return {k: v / z0 for k, v in poly_mul(aa, inv, order).items()}


def eval_series(coeff, y):
    return sum(v * prod(yj ** kj for yj, kj in zip(y, key))
               for key, v in coeff.items())


def prod(seq):
    ans = F(1)
    for item in seq:
        ans *= item
    return ans


def ratio_value(x, a):
    aa = prod(a + (1 - a) * xx for xx in x)
    bb = prod(a + (1 - a) * (1 - xx) for xx in x)
    return aa / (aa + bb)


def run_fixture(n, counts, a=F(1, 2), r=2, K=4):
    m = len(counts)
    x = [F(s, 2 * n) for s in counts]
    taylor = ratio_series(x, a, 2 * r - 1)
    moments = [centered_hypergeom_moments(n, s, 2 * r - 1) for s in counts]
    expected_taylor = sum(
        coef * prod(moments[i][key[i]] for i in range(m))
        for key, coef in taylor.items()
    )
    support = []
    Z, V = [], []
    integer_normalizer_bits = []
    for s, xx in zip(counts, x):
        row = []
        Zi = Vi = F(0)
        base_int_total = moment_int_total = 0
        for k in range(max(0, s - n), min(s, n) + 1):
            pp = F(comb(s, k) * comb(2 * n - s, n - k), comb(2 * n, n))
            yy = F(k, n) - xx
            tilt = (1 + abs(yy)) ** K
            row.append((yy, pp))
            Zi += pp * tilt
            Vi += pp * tilt * yy ** (2 * r)
            d = 2 * k - s
            iw = comb(s, k) * comb(2 * n - s, n - k) * (2 * n + abs(d)) ** K
            base_int_total += iw
            moment_int_total += iw * d ** (2 * r)
        assert Zi == F(base_int_total, comb(2 * n, n) * (2 * n) ** K)
        assert Vi == F(moment_int_total, comb(2 * n, n) * (2 * n) ** (K + 2 * r))
        support.append(row)
        Z.append(Zi)
        V.append(Vi)
        integer_normalizer_bits.append(base_int_total.bit_length())
    # The scalar C*h is irrelevant to testing the product-envelope identities.
    prefactor = F(m ** (2 * r - 1))
    B0 = prefactor * prod(Z) * sum(v / z for v, z in zip(V, Z))
    direct_taylor = exact_mean = direct_B = Q_total = remainder_from_Q = F(0)
    max_remainder_ratio = F(0)
    for entries in product(*support):
        y = [item[0] for item in entries]
        pp = prod(item[1] for item in entries)
        value = ratio_value([xx + yy for xx, yy in zip(x, y)], a)
        tt = eval_series(taylor, y)
        BB = prefactor * sum(yy ** (2 * r) for yy in y) * prod((1 + abs(yy)) ** K for yy in y)
        exact_mean += pp * value
        direct_taylor += pp * tt
        direct_B += pp * BB
        if BB:
            qq = pp * BB / B0
            Q_total += qq
            remainder_from_Q += qq * B0 * (value - tt) / BB
            max_remainder_ratio = max(max_remainder_ratio, abs(value - tt) / BB)
        else:
            assert value == tt
    assert direct_taylor == expected_taylor
    assert direct_B == B0
    if B0:
        assert Q_total == 1
    assert remainder_from_Q == exact_mean - expected_taylor
    for i, s in enumerate(counts):
        for k, moment in enumerate(moments[i]):
            direct = sum(pp * yy ** k for yy, pp in support[i])
            assert moment == direct
            if k % 2:
                assert moment == 0
    return {
        "n": n, "counts": counts, "dimension": m,
        "taylor_order": 2 * r - 1,
        "hypergeom_vector_count_validation_only": prod(len(row) for row in support).numerator,
        "univariate_terms_production": sum(len(row) for row in support),
        "normalizer_max_bits": max(integer_normalizer_bits),
        "mean_exact": str(exact_mean),
        "taylor_expectation_exact": str(expected_taylor),
        "remainder_mean": float(exact_mean - expected_taylor),
        "max_abs_remainder_over_unscaled_envelope": float(max_remainder_ratio),
        "all_exact_equalities_passed": True,
    }


def main():
    fixtures = [
        run_fixture(4, [2, 5], r=2, K=4),
        run_fixture(5, [2, 4, 8], r=2, K=4),
        run_fixture(5, [3, 6], r=4, K=8),
        run_fixture(4, [0, 8], r=4, K=8),
    ]
    module_fixture = validate_product_envelope_module()
    output = {"claim": "Exact arithmetic identities only; not a full Bernoulli factory or physical experiment.",
              "fixtures": fixtures, "production_module_mixture_check": module_fixture}
    path = Path(__file__).with_name("randomized_elevation_results.json")
    path.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps(output, indent=2))


def validate_product_envelope_module():
    n, totals = 5, (3, 5, 8)
    env = ProductEnvelope(n, totals, r=2, K=4, scale=F(27))
    count = 0
    total_probability = F(0)
    for ks in product(*env.supports):
        yy = tuple(F(2 * k - s, 2 * n) for k, s in zip(ks, totals))
        pp = prod(F(comb(s, k) * comb(2 * n - s, n - k), comb(2 * n, n))
                  for k, s in zip(ks, totals))
        intended = pp * env.value(yy) / env.expectation
        actual = F(0)
        for distinguished, cw in enumerate(env.component_weights):
            if not cw:
                continue
            term = F(cw, sum(env.component_weights))
            for i, k in enumerate(ks):
                weights = env.moment_weights[i] if i == distinguished else env.base_weights[i]
                term *= F(weights[env.supports[i].index(k)], sum(weights))
            actual += term
        assert intended == actual
        total_probability += actual
        count += 1
    assert total_probability == 1
    return {"vectors_exhaustively_checked": count,
            "univariate_support_terms": env.support_terms,
            "mixture_matches_product_envelope_exactly": True}


if __name__ == "__main__":
    main()
