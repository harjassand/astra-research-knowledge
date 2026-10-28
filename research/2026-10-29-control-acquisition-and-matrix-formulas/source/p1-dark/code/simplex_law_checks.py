"""Small exact algebra/source checks, separate from the main acquisition run.

No hardware or experimental sample-size claim. Analytic all-dimension results
remain proofs in SIMPLEX_LAW_ACQUISITION.md. Counts below record actual cases.
"""
from fractions import Fraction as F
from math import comb
from pathlib import Path
import json
import random
import sys

from simplex_law import (SimplexLaw, barycentric, bernstein_weights, chebyshev,
                         compositions, falling_binomial, lagrange_weights,
                         nodal_to_bernstein, solve)


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT.parent / 'p1_next' / 'theory'))
from unnormalized_representation_checks import compiled, canonical, gram
from dark_intervention_order_checks import path_gram_factor


def serial(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {k: serial(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [serial(v) for v in value]
    return value


def multiply(a, b, degree):
    out = [F(0)] * (min(len(a) + len(b) - 2, degree) + 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            if i + j <= degree:
                out[i + j] += x * y
    return out


def power(a, exponent, degree):
    out = [F(1)]
    while exponent:
        if exponent & 1:
            out = multiply(out, a, degree)
        a = multiply(a, a, degree)
        exponent //= 2
    return out


def elevated(alphas, coefficients, beta, degree):
    total = sum(beta)
    value, mass = F(0), F(0)
    for alpha, coefficient in zip(alphas, coefficients):
        if all(a <= b for a, b in zip(alpha, beta)):
            w = F(1, comb(total, degree))
            for a, b in zip(alpha, beta):
                w *= comb(b, a)
            mass += w
            value += w * coefficient
    assert mass == 1
    return value


def chebyshev_inverse_polynomial(k, q):
    """Return s_(k-1)(x) exactly, with (1+x)s=1-r_k."""
    linear = [F(-1), 2 / q]
    previous, current = [F(1)], linear
    for degree in range(1, k):
        product = [2 * a for a in multiply(linear, current, k)]
        for i, a in enumerate(previous):
            product[i] -= a
        previous, current = current, product
    denominator = chebyshev(k, -(2 + q) / q)
    numerator = [-x / denominator for x in current]
    numerator[0] += 1
    answer = []
    for j in range(k):
        answer.append(numerator[j] - (answer[-1] if j else 0))
    assert numerator[k] == answer[-1]
    return answer


def source_polynomial(c0, g, B, u, coefficients):
    value, v = c0, g[:]
    for coefficient in coefficients:
        value += coefficient * sum(gi * ui * vi for gi, ui, vi in zip(g, u, v))
        v = [sum(B[i][j] * u[j] * v[j] for j in range(len(g))) for i in range(len(g))]
    return value


def main():
    rng = random.Random(28102673)
    counts = {'cardinal_entries': 0, 'exact_transform_coefficients': 0,
              'polynomial_evaluation_equalities': 0, 'elevation_point_bounds': 0,
              'source_query_checks': 0, 'source_node_checks': 0,
              'bernstein_one_sided_checks': 0, 'spectral_comparator_checks': 0,
              'compliance_representation_checks': 0, 'compliance_interval_checks': 0}
    algebra_cases = []
    for n in (1, 2, 3):
        for k in range(1, 6):
            law = SimplexLaw(n, k)
            for j, node in enumerate(law.nodes):
                w = lagrange_weights(law.alphas, barycentric(node, law.delta), k)
                assert w == [F(int(i == j)) for i in range(len(w))]
                counts['cardinal_entries'] += len(w)
            coefficients = [F(rng.randrange(-7, 8), 3) for _ in law.alphas]
            nodal = [sum(c * w for c, w in zip(coefficients,
                          bernstein_weights(law.alphas, barycentric(u, law.delta), k)))
                     for u in law.nodes]
            recovered, blocks = nodal_to_bernstein(law.alphas, nodal, k)
            assert recovered == coefficients
            counts['exact_transform_coefficients'] += len(coefficients)
            for _ in range(5):
                integers = [rng.randrange(1, 20) for _ in range(n + 1)]
                lambdas = [F(a, sum(integers)) for a in integers]
                left = sum(c * w for c, w in zip(nodal, lagrange_weights(law.alphas, lambdas, k)))
                right = sum(c * w for c, w in zip(coefficients, bernstein_weights(law.alphas, lambdas, k)))
                assert left == right
                counts['polynomial_evaluation_equalities'] += 1
            m = k + 3
            coefficient_range = max(coefficients) - min(coefficients)
            bound = coefficient_range * k * (k - 1) / (2 * m)
            maximum_gap = F(0)
            for beta in compositions(m, n + 1):
                elevated_value = elevated(law.alphas, coefficients, beta, k)
                point_value = sum(c * w for c, w in zip(coefficients,
                                  bernstein_weights(law.alphas, [F(b, m) for b in beta], k)))
                gap = abs(elevated_value - point_value)
                assert gap <= bound
                maximum_gap = max(maximum_gap, gap)
                counts['elevation_point_bounds'] += 1
            algebra_cases.append({'n': n, 'k': k, 'nodes': len(law.nodes),
                                  'transform': blocks, 'elevated_degree': m,
                                  'elevation_gap_max': maximum_gap, 'elevation_gap_bound': bound})

    sharpness = []
    for k in range(1, 7):
        rows = []
        for N in (k + 1, 2 * k, 16 * k, 128 * k):
            t = F(k, N)
            lebesgue = power([abs(falling_binomial(t, j)) for j in range(k + 1)], N, k)[k]
            bound = F(comb(2 * k - 1, k))
            assert 1 <= lebesgue <= bound
            rows.append({'barycentric_dimensions': N, 'lebesgue': lebesgue,
                         'upper_bound': bound, 'ratio_diagnostic': float(lebesgue / bound)})
        sharpness.append({'k': k, 'cases': rows})

    source_cases = []
    g = [F(1), F(0), F(1, 2)]
    factor = [[F(1, 2), F(1, 2)], [F(1, 2), F(-1, 2)], [F(1, 4), F(1, 2)]]
    B = gram(factor)
    assert max(B[i][i] for i in range(3)) <= 1
    for delta in (F(1, 5), F(1), F(2)):
        for k in range(1, 5):
            law = SimplexLaw(3, k, delta=delta)
            exact_nodes, intervals = [], []
            eta = F(1, 10**6)
            for i, u in enumerate(law.nodes):
                value = compiled(F(1), g, B, u)[0]
                assert value == canonical(F(1), g, factor, u)[0]
                exact_nodes.append(value)
                error = eta * (1 if i % 2 else -1)
                intervals.append((value + error - eta, value + error + eta))
                counts['source_node_checks'] += 1
            law.ingest(intervals)
            coefficients = chebyshev_inverse_polynomial(k, delta)
            queries = [[F(0)] * 3, [delta, F(0), F(0)], [delta / 3] * 3]
            for _ in range(7):
                integers = [rng.randrange(1, 20) for _ in range(4)]
                queries.append([delta * F(x, sum(integers)) for x in integers[1:]])
            maximum_error = F(0)
            maximum_bernstein_bias = F(0)
            for u in queries:
                true = compiled(F(1), g, B, u)[0]
                prediction = law.predict(u)
                for key in ('interpolation_interval', 'bernstein_interval', 'intersection_interval'):
                    lo, hi = prediction[key]
                    assert lo <= true <= hi
                exact_positive = sum(w * y for w, y in zip(
                    bernstein_weights(law.alphas, barycentric(u, delta), k), exact_nodes))
                assert 0 <= true - exact_positive <= law.bernstein_bias
                counts['bernstein_one_sided_checks'] += 1
                H = source_polynomial(F(1), g, B, u, coefficients)
                assert abs(true - H) <= law.spectral_comparator_error
                counts['spectral_comparator_checks'] += 1
                maximum_error = max(maximum_error, abs(true - prediction['estimate']))
                maximum_bernstein_bias = max(maximum_bernstein_bias, true - exact_positive)
                counts['source_query_checks'] += 1
            source_cases.append({'delta': delta, 'k': k, 'nodes': len(law.nodes),
                                 'bounds': law.uniform_bounds(),
                                 'maximum_tested_interpolant_error': maximum_error,
                                 'maximum_tested_bernstein_bias': maximum_bernstein_bias})

    compliance_cases = []
    c_lo = F(1, 2)
    for c0 in (F(1, 2), F(3, 4), F(1)):
        h = [x / c0 for x in g]
        A = [[B[i][j] + g[i] * g[j] / c0 for j in range(3)] for i in range(3)]
        law = SimplexLaw(3, 3, G=1 / c_lo, kappa=1 + 1 / c_lo)
        assert max(abs(x) for x in h) <= law.G
        assert max(A[i][i] for i in range(3)) <= law.kappa
        nodal = []
        for u in law.nodes:
            minus_z = -1 / compiled(c0, g, B, u)[0]
            assert minus_z == compiled(-1 / c0, h, A, u)[0]
            nodal.append((minus_z, minus_z))
            counts['compliance_representation_checks'] += 1
        law.ingest(nodal)
        for integers in ((1, 1, 1, 1), (1, 2, 3, 4), (0, 1, 2, 5)):
            u = [law.delta * F(x, sum(integers)) for x in integers[1:]]
            minus_z = -1 / compiled(c0, g, B, u)[0]
            prediction = law.predict(u)
            lo, hi = prediction['intersection_interval']
            assert lo <= minus_z <= hi
            counts['compliance_interval_checks'] += 1
        compliance_cases.append({'actual_c0_checker_only': c0, 'warranted_c0_lower': c_lo,
                                 'G_Z_used': law.G, 'kappa_Z_used': law.kappa,
                                 'bounds': law.uniform_bounds()})

    twins = []
    for k in (1, 2, 3, 4):
        n = k + 1
        g = [F(int(i in (0, n - 1))) for i in range(n)]
        bp, bm = gram(path_gram_factor(n, 1)), gram(path_gram_factor(n, -1))
        law = SimplexLaw(n, k)
        plus = [compiled(F(1), g, bp, u)[0] for u in law.nodes]
        minus = [compiled(F(1), g, bm, u)[0] for u in law.nodes]
        assert plus == minus
        law.ingest([(v, v) for v in plus])
        joint = [law.delta / n] * n
        jp = compiled(F(1), g, bp, joint)[0]
        jm = compiled(F(1), g, bm, joint)[0]
        assert jp != jm
        lo, hi = law.predict(joint)['intersection_interval']
        assert lo <= jp <= hi and lo <= jm <= hi
        twins.append({'k': k, 'n': n, 'indistinguishing_lattice_readings': len(plus),
                      'joint_command': joint, 'J_plus': jp, 'J_minus': jm,
                      'gap': abs(jp - jm), 'acquired_interval': (lo, hi)})

    output = {'scope': 'Finite exact algebra/source checks; no main-run acquisition or whole-proof audit.',
              'all_passed': True, 'counts': counts, 'algebra_cases': algebra_cases,
              'dimension_sharpness_diagnostics': sharpness, 'source_cases': source_cases,
              'compliance_cases': compliance_cases,
              'dark_path_twins': twins,
              'floating_values': 'Display diagnostics only; all pass conditions use Fraction.'}
    (ROOT / 'theory' / 'SIMPLEX_LAW_CHECKS.json').write_text(json.dumps(serial(output), indent=2) + '\n')
    print(json.dumps({'all_passed': True, 'counts': counts, 'dark_twin_cases': len(twins)}, indent=2))


if __name__ == '__main__':
    main()
