"""Exact checks of the constructed signed evaluator and compiler coefficients.

Validation uses a separate 2x2 adjugate formula and ordinary polynomial series,
not the production Gaussian-elimination jet routine. It does not execute the
astronomically conservative generic starting level.
"""
from fractions import Fraction as F
from math import comb
from pathlib import Path
import json
import sys
from time import perf_counter

from rational_program import (ProbabilityProgram, signed_response_program,
                              compiler_constants, indices)

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "broad_mechanism"))
from randomized_elevation import centered_moments


def padd(a, b):
    return [(a[i] if i < len(a) else F(0)) + (b[i] if i < len(b) else F(0))
            for i in range(max(len(a), len(b)))]


def pmul(a, b):
    out = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


def scale(a, c):
    return [c * x for x in a]


def quotient_series(a, b, order):
    out = []
    for k in range(order + 1):
        out.append(((a[k] if k < len(a) else F(0)) -
                    sum(b[j] * out[k - j] for j in range(1, min(k, len(b) - 1) + 1))) / b[0])
    return out


def direct_series(point, direction, order):
    p, q = [[point[i], F(direction[i])] for i in range(2)]
    a = padd(scale(p, 2), [-1])
    b = padd(q, scale(p, -1))
    c = padd(padd(p, q), [-1])
    d = padd([1], scale(q, -2))
    a11 = padd([1], padd(pmul(a, a), pmul(b, b)))
    a22 = padd([1], padd(pmul(c, c), pmul(d, d)))
    a12 = padd(pmul(a, c), pmul(b, d))
    denominator = padd(padd(pmul(a11, a22), scale(pmul(a12, a12), -1)), a22)
    return quotient_series(a22, denominator, order)


def main():
    started = perf_counter()
    program = ProbabilityProgram(2, signed_response_program)
    fixtures = []
    for point in ((F(1, 3), F(2, 5)), (F(0), F(1)), (F(1, 2), F(1, 2))):
        jet = program.jet(point, 12)
        comparisons = 0
        for direction in [(0, 1)] + [(1, k) for k in range(13)]:
            expected = direct_series(point, direction, 12)
            for k in range(13):
                actual = sum(v * direction[0] ** alpha[0] * direction[1] ** alpha[1]
                             for alpha, v in jet.coeff.items() if sum(alpha) == k)
                assert actual == expected[k]
                comparisons += 1
        assert jet.value() == program.value(point)
        fixtures.append(dict(point=list(map(str, point)), probability=str(jet.value()),
                             jet_coefficients=len(jet.coeff),
                             exact_directional_series_comparisons=comparisons,
                             maximum_coefficient_bits=max(max(v.numerator.bit_length(),
                                                             v.denominator.bit_length())
                                                          for v in jet.coeff.values())))

    moment_checks = 0
    for n in range(3, 61):
        for s in range(2 * n + 1):
            x = F(s, 2 * n)
            v = x * (1 - x)
            moments = centered_moments(n, s, 6)
            assert moments[2] == v / (2 * n - 1)
            assert moments[4] == (3 * v * v - v / n) / ((2 * n - 1) * (2 * n - 3))
            assert all(moments[k] == 0 for k in (1, 3, 5))
            assert abs(moments[2] - v / (2 * n) - v / (4 * n * n)) <= F(1, 16 * n ** 3)
            assert abs(moments[4] - 3 * v * v / (4 * n * n)) <= F(5, 8 * n ** 3)
            moment_checks += 1

    # Global simple norm bounds for this actual pencil: R=2, L=6.
    R, L = 2, 6
    H = 1 + 2 * R * L + 2 * L * L
    K = 8 * H * (2 + R * R)
    constants = compiler_constants(2, K)
    assert constants["n0"] ** 3 >= 4 * constants["C"]
    point = (F(1, 3), F(2, 5))
    n = constants["n0"]
    lo = program.coefficient_oracle(n, constants["C"], -1)
    hi = program.coefficient_oracle(n, constants["C"], 1)
    f = program.value(point)
    assert 0 < lo.value(point) < hi.value(point) < 1
    assert hi.value(point) - lo.value(point) == F(2 * constants["C"], n ** 3) * f * (1 - f)
    # This checks actual rational coefficient derivatives, without taking n0 bits.
    selected_derivatives = {str(alpha): str(lo.derivative(point, alpha))
                            for alpha in ((1, 0), (0, 1), (2, 2), (4, 4))}
    result = dict(
        scope="Exact evaluator/jet and coefficient checks, not a generic-factory performance run.",
        signed_program_fixtures=fixtures,
        hypergeometric_moment_grid_checks=moment_checks,
        explicit_certificate=dict(R=R, L=L, H=H, K=K),
        generic_constants={key: str(value) for key, value in constants.items()},
        generic_initial_source_calls_if_executed=str(2 * n),
        generic_initial_level_executed=False,
        coefficient_width_identity_exact=True,
        selected_lower_coefficient_derivatives_exact=True,
        grid_evaluations=program.grid_evaluations,
        elapsed_seconds_nonportable=perf_counter() - started,
    )
    path = Path(__file__).with_name("program_check_results.json")
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
