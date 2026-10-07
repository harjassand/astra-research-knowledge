"""Scoped checks for the same-Fisher-spectrum archive counterexample.

Standard library only. Exact checks audit the graded-hat scalar constants.
Floating checks audit the periodic scalar codec, not the quantum/asymptotic proof.
"""

from fractions import Fraction as F
import json
import math
from pathlib import Path


def exact_graded(J):
    nodes = [-1 + 6 * F(j, J) ** 2 - 4 * F(j, J) ** 3 for j in range(J + 1)]
    gaps = [nodes[j + 1] - nodes[j] for j in range(J)]
    biases, weights, variances = [], [], []
    for j in range(J + 1):
        left = gaps[j - 1] if j else F(0)
        right = gaps[j] if j < J else F(0)
        biases.append((right - left) / 3)
        weights.append((left + right) / 4)
        variances.append((left * left + left * right + right * right) / 18)
    dirichlet = sum(w * var for w, var in zip(weights, variances))
    l2bias = sum(gaps[j] * (biases[j] ** 2 + biases[j] * biases[j + 1]
                           + biases[j + 1] ** 2) / 6 for j in range(J))
    assert sum(weights) == 1
    assert max(gaps) <= F(3, J)
    assert max(abs(b) for b in biases) <= F(4, J * J)
    assert dirichlet <= F(9, J * J)
    assert l2bias <= F(16, J ** 4)
    return dict(J=J, max_gap_times_J=float(max(gaps) * J),
                max_bias_times_J2=float(max(abs(b) for b in biases) * J * J),
                dirichlet_times_J2=float(dirichlet * J * J),
                l2bias_times_J4=float(l2bias * J ** 4))


def periodic_check(b=0.35, modes=30, samples=4096):
    c = math.sqrt(2 / 3)
    a = min(0.25, math.sqrt(math.expm1(2 * b)) / 4)
    s = [a * math.exp(-b * i) for i in range(1, modes + 1)]
    q = math.exp(-2 * b)
    fourth_sum = q * (1 + 11 * q + 11 * q * q + q ** 3) / (1 - q) ** 5
    M2 = c * (2 * math.pi) ** 2 * a * math.sqrt(fourth_sum)
    positivity_bound = c * a / math.sqrt(math.expm1(2 * b))
    assert positivity_bound < 0.25
    fixtures = []
    for coordinate in (0, 1, 3, 10, 20):
        v = [0.0] * modes
        v[coordinate] = 1.0
        fixtures.append(v)
    for phase in (0.0, 0.4, 1.9):
        v = [math.cos((i + 1) * phase) / (i + 1) for i in range(modes)]
        norm = math.sqrt(sum(z * z for z in v))
        fixtures.append([z / norm for z in v])
    checks = []
    for J in (8, 16, 32, 64, 128):
        sinc2 = [(math.sin(math.pi * i / J) / (math.pi * i / J)) ** 2
                 for i in range(1, modes + 1)]
        for fi, v in enumerate(fixtures):
            coeff = [c * si * vi for si, vi in zip(s, v)]
            cell_values = [1 + sum(ci * attenuation * math.cos(2 * math.pi * i * j / J)
                                   for i, (ci, attenuation) in enumerate(zip(coeff, sinc2), 1))
                           for j in range(J)]
            abs_sum = 0.0
            signed_sum = 0.0
            maximum = 0.0
            for k in range(samples):
                x = (k + 0.5) / samples
                target = 1 + sum(ci * math.cos(2 * math.pi * i * x)
                                 for i, ci in enumerate(coeff, 1))
                position = J * x
                left = int(position)
                fraction = position - left
                rebuilt = ((1 - fraction) * cell_values[left % J]
                           + fraction * cell_values[(left + 1) % J])
                difference = rebuilt - target
                abs_sum += abs(difference)
                signed_sum += difference
                maximum = max(maximum, abs(difference))
            tv = abs_sum / (2 * samples)
            tv_bound = 5 * M2 / (48 * J * J)
            sup_bound = 5 * M2 / (24 * J * J)
            assert tv <= tv_bound + 1e-10
            assert maximum <= sup_bound + 1e-10
            assert abs(signed_sum / samples) < 2e-10
            checks.append(dict(J=J, fixture=fi, tv=tv, tv_bound=tv_bound,
                               tv_times_J2=tv * J * J,
                               max_error=maximum, normalization_residual=signed_sum / samples))
    # Orthogonal cosine scores have the same exact variances as uniform x_i.
    gram_residual = 0.0
    gram_modes = 12
    for i in range(1, gram_modes + 1):
        for j in range(1, gram_modes + 1):
            empirical = sum((c * math.cos(2 * math.pi * i * (k + 0.5) / samples))
                            * (c * math.cos(2 * math.pi * j * (k + 0.5) / samples))
                            for k in range(samples)) / samples
            gram_residual = max(gram_residual, abs(empirical - (1 / 3 if i == j else 0)))
    assert gram_residual < 1e-12
    return dict(b=b, a=a, modes=modes, samples=samples,
                positivity_deviation_upper=positivity_bound,
                uniform_second_derivative_upper=M2,
                gram_residual=gram_residual, checks=checks)


def main():
    exact = [exact_graded(J) for J in range(1, 129)]
    periodic = periodic_check()
    payload = dict(status="Scoped exact algebra and floating quadrature checks; not theorem validation",
                   exact_graded=exact, periodic=periodic)
    destination = Path(__file__).with_name("statistical_memory_check.json")
    destination.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(dict(exact_graded_fixtures=len(exact),
                          periodic_fixtures=len(periodic["checks"]),
                          maximum_gram_residual=periodic["gram_residual"],
                          maximum_normalization_residual=max(abs(c["normalization_residual"])
                                                             for c in periodic["checks"]),
                          result_path=str(destination)), indent=2))


if __name__ == "__main__":
    main()
