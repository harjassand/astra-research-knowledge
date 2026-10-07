"""Independent score-moment fixtures; this does not execute a sampling algorithm."""
from pathlib import Path
import json
import math


def simpson_score_fixture(name, density, score, beta, radius, n=100000):
    step = 2 * radius / n
    totals = [0.0] * 10
    for i in range(n + 1):
        x = -radius + i * step
        w = 1 if i in (0, n) else 2 if i % 2 == 0 else 4
        p = density(x)
        s = score(x) ** 2
        totals[0] += w * p
        power = 1.0
        for k in range(1, 9):
            power *= s
            totals[k] += w * p * power
        totals[9] += w * p * math.exp(s / (4 * beta))
    vals = [t * step / 3 for t in totals]
    moments = [v / vals[0] for v in vals[1:9]]
    bound = 1.0
    ratios = []
    for k, moment in enumerate(moments, 1):
        bound *= beta * (1 + 2 * (k - 1))
        ratios.append(moment / bound)
    return {
        "name": name,
        "beta": beta,
        "normalizer_on_numerical_interval": vals[0],
        "moments_2_through_16": moments,
        "ratios_to_beta_power_rising_dimension_bound": ratios,
        "score_square_mgf_at_one_over_four_beta": vals[9] / vals[0],
        "mgf_upper_bound": math.sqrt(2),
        "maximum_moment_ratio": max(ratios),
        "quadrature_is_not_a_rigorous_tail_or_error_certificate": True,
    }


def normal_density(x, mean=0.0, variance=1.0):
    return math.exp(-(x - mean) ** 2 / (2 * variance)) / math.sqrt(2 * math.pi * variance)


fixtures = []
for beta in (0.5, 1.0, 3.0):
    fixtures.append(simpson_score_fixture(
        f"Gaussian_beta_{beta}",
        lambda x, beta=beta: normal_density(x, variance=1 / beta),
        lambda x, beta=beta: beta * x,
        beta, 24 / math.sqrt(beta),
    ))

for amplitude in (1.5, 3.0):
    fixtures.append(simpson_score_fixture(
        f"Nonconvex_cosine_amplitude_{amplitude}",
        lambda x, amplitude=amplitude: math.exp(-x * x / 2 - amplitude * math.cos(x)),
        lambda x, amplitude=amplitude: x - amplitude * math.sin(x),
        1 + amplitude, 24,
    ))

convolution_fixtures = []
for separation in (1.5, 2.0, 3.0):
    beta = max(1.0, separation * separation - 1)
    fixtures.append(simpson_score_fixture(
        f"Nonconvex_mixture_separation_{separation}",
        lambda x, separation=separation: (normal_density(x, separation) + normal_density(x, -separation)) / 2,
        lambda x, separation=separation: x - separation * math.tanh(separation * x),
        beta, separation + 24,
    ))
    h = 0.5 / beta
    radius = separation + 24 * math.sqrt(1 + h)
    n = 100000
    step = 2 * radius / n
    mgf = 0.0
    for i in range(n + 1):
        x = -radius + i * step
        w = 1 if i in (0, n) else 2 if i % 2 == 0 else 4
        p = (normal_density(x, separation, 1 + h) + normal_density(x, -separation, 1 + h)) / 2
        g = x - separation * math.tanh(separation * x)
        mgf += w * p * math.exp(g * g / (8 * beta))
    convolution_fixtures.append({"separation": separation, "beta_h": beta * h,
                                 "mgf_at_one_over_eight_beta": mgf * step / 3,
                                 "mgf_upper_bound": 2.0})

gaussian_warm_fixtures = []
for dimension in (10, 100, 1000):
    for warm_exponent in (1, 10, 100):
        h = 0.1
        log_one_plus_chi2 = warm_exponent * math.log(dimension)
        gradient_second_moment = (1 + h) * (dimension + log_one_plus_chi2)
        entropy_bound = 8 * (dimension * math.log(2) + log_one_plus_chi2)
        gaussian_warm_fixtures.append({"dimension": dimension, "warm_exponent": warm_exponent,
                                      "log_one_plus_chi2": log_one_plus_chi2,
                                      "exact_gradient_second_moment": gradient_second_moment,
                                      "entropy_bound": entropy_bound})

assert all(x["maximum_moment_ratio"] < 1 + 1e-9 for x in fixtures)
assert all(x["score_square_mgf_at_one_over_four_beta"] <= x["mgf_upper_bound"] + 1e-9 for x in fixtures)
assert all(x["mgf_at_one_over_eight_beta"] <= x["mgf_upper_bound"] + 1e-9 for x in convolution_fixtures)
assert all(x["exact_gradient_second_moment"] <= x["entropy_bound"] for x in gaussian_warm_fixtures)

result = {"status": "fixtures_passed", "score_fixtures": fixtures,
          "noised_mixture_fixtures": convolution_fixtures,
          "shifted_gaussian_warmness_fixtures": gaussian_warm_fixtures,
          "full_sampler_executed": False, "bit_compiler_executed": False}
Path(__file__).with_suffix(".json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({"score_fixtures": len(fixtures),
                  "maximum_moment_ratio": max(x["maximum_moment_ratio"] for x in fixtures),
                  "noised_mixture_fixtures": len(convolution_fixtures),
                  "exact_shifted_gaussian_fixtures": len(gaussian_warm_fixtures),
                  "full_sampler_executed": False}))
