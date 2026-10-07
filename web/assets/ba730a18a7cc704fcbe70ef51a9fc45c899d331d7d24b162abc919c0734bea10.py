"""Scoped fixtures for optimization_sampling.txt, not a sampler implementation."""
from fractions import Fraction as F
import json
import math
from pathlib import Path


def rational_unit(m, k):
    if m == 1:
        return [F(1)]
    t = [F((i + 2) * (k + 1) % 11 - 5, 13) for i in range(m - 1)]
    s = sum(x * x for x in t)
    return [2 * x / (1 + s) for x in t] + [(1 - s) / (1 + s)]


rank_fixtures = []
for m in range(1, 9):
    for k in range(5):
        for sine, cosine in [(F(5, 13), F(12, 13)),
                             (F(8, 17), F(15, 17)),
                             (F(7, 25), F(24, 25))]:
            D = F(k + 2, 3)
            u = rational_unit(m, k)
            v = [2 * D * sine * x for x in u]
            q = sum(x * x for x in v)
            assert q <= D * D
            P = [[F(i == j) - v[i] * v[j] / (4 * D * D * (1 + cosine))
                  for j in range(m)] for i in range(m)]
            for i in range(m):
                for j in range(m):
                    product = sum(P[i][a] * P[j][a] for a in range(m))
                    assert product + v[i] * v[j] / (4 * D * D) == F(i == j)
            for i in range(m):
                assert sum(P[i][j] * v[j] for j in range(m)) == cosine * v[i]
            rank_fixtures.append({"slots": m, "k": k, "sine": str(sine)})


def simpson(fun, radius=12.0, n=100_000):
    step = 2 * radius / n
    total = fun(-radius) + fun(radius)
    total += 4 * sum(fun(-radius + i * step) for i in range(1, n, 2))
    total += 2 * sum(fun(-radius + i * step) for i in range(2, n, 2))
    return total * step / 3


mixture_checks = []
for a in [1.1, math.sqrt(2), 2.0]:
    beta = max(1.0, a * a - 1.0)
    def density(x):
        return (math.exp(-0.5 * (x-a)**2) + math.exp(-0.5 * (x+a)**2)) / (2*math.sqrt(2*math.pi))
    def gradient(x):
        return x - a * math.tanh(a*x)
    def hessian(x):
        return 1 - a*a / math.cosh(a*x)**2
    mass = simpson(density)
    fisher = simpson(lambda x: density(x) * gradient(x)**2)
    mean_hessian = simpson(lambda x: density(x) * hessian(x))
    fourth = simpson(lambda x: density(x) * gradient(x)**4)
    fourth_identity = simpson(lambda x: density(x) * 3 * gradient(x)**2 * hessian(x))
    assert abs(mass - 1) < 1e-10
    assert abs(fisher - mean_hessian) < 1e-10
    assert abs(fourth - fourth_identity) < 1e-9
    assert fisher <= beta + 1e-10
    assert fourth <= 3 * beta**2 + 1e-9
    mixture_checks.append({"a": a, "minimum_hessian": 1-a*a,
                           "beta": beta, "mass": mass, "fisher": fisher,
                           "mean_hessian": mean_hessian, "fourth": fourth,
                           "fourth_identity": fourth_identity,
                           "fourth_bound": 3*beta**2})


translation_error = 0.0
sample_translation_error = 0.0
for k in range(1000):
    x = (k % 19 - 9) / 5
    displacement = (k % 13 - 6) / 17
    r = (k % 7 + 1) / 11
    seed = (k % 31 - 15) / 9
    def g(z):
        return 0.03 * (z + 0.2 * math.tanh(z))
    before = g(x + r*seed)
    after = g(x+displacement+r*(seed-displacement/r))
    translation_error = max(translation_error, abs(before-after))
    sample_before = seed-r*before
    sample_after = seed-displacement/r-r*after
    sample_translation_error = max(sample_translation_error,
                                   abs(sample_after-sample_before+displacement/r))
assert translation_error < 1e-15
assert sample_translation_error < 1e-14

result = {
    "status": "scoped_algebra_and_quadrature_only",
    "exact_rank_one_covariance_fixtures": len(rank_fixtures),
    "exact_covariance_failures": 0,
    "terminal_translation_fixtures": 1000,
    "maximum_mean_translation_error": translation_error,
    "maximum_sample_translation_error": sample_translation_error,
    "nonconvex_mixture_quadratures": mixture_checks,
    "not_executed": ["OA139 full sampler", "PI transfer sampler",
                     "finite-bit compiler", "Chen-Liu FPRAS", "Lean build"],
}
path = Path(__file__).with_name("optimization_sampling_checks.json")
path.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
