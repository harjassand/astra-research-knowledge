"""Small arithmetic check for the serial reset-race theorem."""
from math import isclose, log, exp


def rates_for_stage_success(x, mu):
    return mu * x / (1.0 - x)


def response_probabilities(stage_rates, mu0, mu1):
    p0 = 1.0
    p1 = 1.0
    for k in stage_rates:
        p0 *= k / (k + mu0)
        p1 *= k / (k + mu1)
    return p0, p1


def expected_absorption_time(stage_rates, mu):
    reached = 1.0
    total = 0.0
    for k in stage_rates:
        total += reached / (k + mu)
        reached *= k / (k + mu)
    return total


def optimal_false_positive(p1, r, m):
    x = p1 ** (1.0 / m)
    return (x / (r - (r - 1.0) * x)) ** m


mu1, mu0, p1 = 1.0, 2.0, 0.25
r = mu0 / mu1
for m in (1, 2, 8, 64):
    x = p1 ** (1.0 / m)
    k = rates_for_stage_success(x, mu1)
    rates = [k] * m
    p0, measured_p1 = response_probabilities(rates, mu0, mu1)
    assert isclose(measured_p1, p1, rel_tol=1e-10, abs_tol=1e-12)
    assert p0 + 1e-12 >= p1 ** r
    assert isclose(p0, optimal_false_positive(p1, r, m), rel_tol=1e-10)
    assert isclose(expected_absorption_time(rates, mu1), (1.0-p1)/mu1, rel_tol=1e-10)
    print(f"m={m:2d} p0={p0:.9f} floor={p1**r:.9f} mean_T1={expected_absorption_time(rates,mu1):.9f}")

print(f"conditional-success latency limit={-log(p1)/mu1:.9f}")
print(f"asymptotic p0={exp(r*log(p1)):.9f}")
