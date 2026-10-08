#!/usr/bin/env python3
"""Small exact/algebraic diagnostics; no theorem or novelty certification."""
import json
import math
from fractions import Fraction as F
from pathlib import Path


def gaussian_mixture_moment(order, a):
    if order % 2:
        return F(0)
    sigmasq = 1 - a * a
    out = F(0)
    for j in range(order // 2 + 1):
        dfact = math.prod(range(1, 2 * j, 2))
        out += math.comb(order, 2 * j) * a ** (order - 2 * j) * sigmasq ** j * dfact
    return out


def tilt_kernel_norm_squared(degree, a):
    moments = [gaussian_mixture_moment(k, a) for k in range(2 * degree + 1)]
    mgf = [moments[k] / math.factorial(k) for k in range(degree + 1)]
    inverse = [F(1)]
    for k in range(1, degree + 1):
        inverse.append(-sum(mgf[j] * inverse[k - j] for j in range(1, k + 1)))
    poly = [inverse[degree - j] / math.factorial(j) for j in range(degree + 1)]
    return sum(poly[j] * poly[k] * moments[j + k]
               for j in range(degree + 1) for k in range(degree + 1))


def quantum_cumulant_energy(b):
    d = len(b)
    assert sum(b) == 0
    variance = sum(x * x for x in b) / d
    p_jordan_p = [[(b[i] if i == j else F(0)) - (b[i] + b[j]) / d
                  for j in range(d)] for i in range(d)]
    diagonal = sum(x * x for row in p_jordan_p for x in row)
    off_diagonal = sum(2 * ((b[i] + b[j]) / 2) ** 2
                       for i in range(d) for j in range(i + 1, d))
    return (diagonal + off_diagonal) / variance, diagonal / variance


report = {"status": "FINITE-EVIDENCE", "theorem_validation": False,
          "external_validation": False, "tests": {}}
quantum_rows = []
for d in list(range(2, 17)) + [32, 64]:
    for b in ([F(1), F(-1)] + [F(0)] * (d - 2),
              [F(i) - F(d - 1, 2) for i in range(d)]):
        full, diagonal = quantum_cumulant_energy(b)
        assert full == F(d * d, 2) - 2
        assert diagonal == d - 2
    quantum_rows.append({"dimension": d, "full_energy": str(full),
                         "commuting_energy": str(diagonal)})
report["tests"]["quantum_exact"] = quantum_rows
quantum_proxy_rows = []
for d in [2, 4, 8, 16, 64]:
    multiplicity = d * d // 4 - 1
    for t in [0.01, 0.1, 0.5]:
        eigenvalues = ([1 + t] * multiplicity + [1 - t] * multiplicity
                       + [1] * (d * d // 2) + [1 - t * t])
        assert len(eigenvalues) == d * d - 1
        kl = (t * t + sum(x - 1 - math.log(x) for x in eigenvalues)) / 2
        exact_kl = -d * d / 8 * math.log1p(-t * t)
        assert math.isclose(kl, exact_kl, rel_tol=1e-9, abs_tol=1e-12)
        hs_squared = sum((x - 1) ** 2 for x in eigenvalues)
        exact_hs_squared = t * t * (d * d / 2 - 2) + t ** 4
        assert math.isclose(hs_squared, exact_hs_squared, rel_tol=1e-9)
        quantum_proxy_rows.append({"dimension": d, "t": t,
                                   "quantum_chi_square": t * t,
                                   "gaussian_proxy_kl": exact_kl,
                                   "covariance_hs_squared": exact_hs_squared,
                                   "infinitesimal_fisher_amplification": d * d / 4})
report["tests"]["quantum_proxy"] = quantum_proxy_rows

mixture_rows = []
for a in [F(0), F(3, 5), F(4, 5), F(12, 13), F(24, 25), F(99, 101), F(1)]:
    for degree in range(1, 21):
        normsq = tilt_kernel_norm_squared(degree, a)
        assert 0 <= normsq <= F(16) ** degree
        if degree == 1:
            assert normsq == 1
        mixture_rows.append({"a": str(a), "degree": degree,
                             "operator_norm_squared": str(normsq),
                             "ratio_to_claimed_squared_bound": float(normsq / F(16) ** degree)})
report["tests"]["mixture_exact_taylor"] = {
    "count": len(mixture_rows), "max_degree": 20,
    "a_values": ["0", "3/5", "4/5", "12/13", "24/25", "99/101", "1"],
    "largest_ratio_to_claimed_squared_bound": max(r["ratio_to_claimed_squared_bound"] for r in mixture_rows),
    "note": "a=1 is the singular Bernoulli limit, only used as an algebraic diagnostic."}

analytic_bound = math.exp(1 / 8) * math.sqrt(math.cosh(1)) / math.cos(1 / 2)
assert analytic_bound < 2
report["tests"]["complex_kernel_bound"] = analytic_bound

bottleneck_rows = []
for sigma in [0.4, 0.2, 0.1, 0.05, 0.01]:
    a = math.sqrt(1 - sigma * sigma)
    w = sigma * sigma / a
    assert w <= a / 2
    exponent = a * a / (2 * sigma * sigma)
    qbar = 2 * w * math.cosh(1) / (sigma * math.sqrt(2 * math.pi)) * math.exp(-exponent)
    log_lower = (3 * math.log(sigma) + math.log(math.sqrt(2 * math.pi) / (2 * a * math.cosh(1)))
                 + math.log1p(-qbar) + exponent)
    bottleneck_rows.append({"sigma": sigma, "mass_upper": qbar,
                            "log10_poincare_lower_bound": log_lower / math.log(10)})
report["tests"]["mixture_bottleneck"] = bottleneck_rows

likelihood_rows = []
for k in [F(2), F(3), F(4), F(16), F(64), F(1024)]:
    prob = 1 / (k + 1)
    first = prob * k + 1 - prob
    second = prob * k * k + 1 - prob
    delta = second / (first * first) - 1
    assert delta == (k - 1) ** 2 / (4 * k)
    likelihood_rows.append({"contrast_ratio": str(k), "sharp_chi_square": str(delta)})
report["tests"]["likelihood_exact"] = likelihood_rows

certificate_rows = []
for b in [0.001, 0.01, 0.05, 0.1, 0.2, 0.25]:
    delta = math.sinh(b / 2) ** 2
    eta = math.sqrt(8 * delta) + delta
    assert eta < 1
    kl_bound = delta / 2 + eta * eta / (4 * (1 - eta))
    tv_bound = math.sqrt(kl_bound / 2)
    assert tv_bound <= b
    certificate_rows.append({"log_contrast": b, "chi_square_upper": delta,
                             "covariance_hs_upper": eta, "gaussian_kl_upper": kl_bound,
                             "gaussian_tv_upper": tv_bound})
report["tests"]["surrogate_certificate"] = certificate_rows

kl_rows = []
for epsilon in [0.5, 0.1, 0.01, 0.001]:
    jeffreys = epsilon + 1 / epsilon - 2
    gaussian_kl = 1 / (epsilon * epsilon) - 1 / epsilon + math.log(epsilon)
    kl_rows.append({"rate": epsilon, "jeffreys": jeffreys,
                    "gaussian_kl": gaussian_kl, "ratio": gaussian_kl / jeffreys})
report["tests"]["global_kl_failure"] = kl_rows
report["tests"]["fisher_constant_lower"] = (5 + math.sqrt(17)) / 2

for m in range(3, 201):
    coefficient = F(32, 144) * F(m * m, (m - 1) ** 2) + F(1, 3) * F(m - 3, m - 1)
    assert coefficient <= 1
    assert m + 1 + 16 * (m - 1) ** 2 <= 16 * m * m
report["tests"]["cumulant_induction_constants"] = {
    "drift_C": 16, "K": 144, "m_range": [3, 200],
    "note": "Finite arithmetic check of constants; the all-m inequalities are algebraic in mechanism_audit.txt."}

output = Path(__file__).with_name("checks.json")
output.write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps({"output": str(output), "status": "FINITE-EVIDENCE",
                  "exact_quantum_cases": 2 * len(quantum_rows),
                  "exact_mixture_taylor_cases": len(mixture_rows),
                  "likelihood_cases": len(likelihood_rows),
                  "all_assertions_passed": True}))
