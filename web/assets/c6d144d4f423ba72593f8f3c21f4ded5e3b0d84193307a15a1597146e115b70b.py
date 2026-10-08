#!/usr/bin/env python3
"""Exact arithmetic checks for the Cycle 3 hidden-type control witness."""

from fractions import Fraction as F
from math import ceil, exp, isclose, log

prior = {"H1": F(4, 5), "H2": F(1, 5)}
plus = {
    "H1": {"A": (F(3), F(1)), "B": (F(1), F(3))},
    "H2": {"A": (F(1), F(3)), "B": (F(3), F(1))},
}
minus = {
    h: {a: (u, r) for a, (r, u) in actions.items()}
    for h, actions in plus.items()
}


def p_regen(rates):
    r, u = rates
    return r / (r + u)


def clone_success(model, action):
    # One shared founder type, two conditionally independent daughters;
    # at infinite horizon, safe reach is the event that both daughters are R.
    return sum(prior[h] * p_regen(model[h][action]) ** 2 for h in prior)


def clone_harm(model, action):
    return 1 - clone_success(model, action)


def observed_report_probability(model, h, action, sensitivity, false_positive):
    r, u = model[h][action]
    return (sensitivity * r + false_positive * u) / (r + u)


def clone_report_success(model, action, sensitivity, false_positive):
    return sum(
        prior[h]
        * observed_report_probability(model, h, action, sensitivity, false_positive) ** 2
        for h in prior
    )


def finite_clone_success(model, action, t):
    c = 1 - exp(-4 * t)
    e = exp(-4 * t)
    return sum(
        float(prior[h]) * ((e + c * float(p_regen(model[h][action]))) ** 2 - e**2)
        for h in prior
    )


def finite_clone_harm(model, action, t):
    c = 1 - exp(-4 * t)
    return sum(
        float(prior[h]) * (1 - (1 - c * float(1 - p_regen(model[h][action]))) ** 2)
        for h in prior
    )


sens_plus, fp_plus = F(9, 10), F(1, 10)
sens_minus, fp_minus = F(1, 10), F(9, 10)
for h in prior:
    for action in ("A", "B"):
        assert observed_report_probability(plus, h, action, sens_plus, fp_plus) == observed_report_probability(
            minus, h, action, sens_minus, fp_minus
        )

assert clone_success(plus, "A") == F(37, 80)   # 0.4625
assert clone_success(plus, "B") == F(13, 80)   # 0.1625
assert clone_success(minus, "A") == F(13, 80)
assert clone_success(minus, "B") == F(37, 80)
assert clone_harm(plus, "A") == F(43, 80)      # 0.5375
assert clone_harm(plus, "B") == F(67, 80)      # 0.8375
assert clone_report_success(plus, "A", sens_plus, fp_plus) == F(41, 100)
assert clone_report_success(plus, "B", sens_plus, fp_plus) == F(17, 100)
assert clone_report_success(minus, "A", sens_minus, fp_minus) == F(41, 100)
assert clone_report_success(minus, "B", sens_minus, fp_minus) == F(17, 100)
assert isclose(finite_clone_success(plus, "A", 1), 0.46908741463240694)
assert isclose(finite_clone_success(plus, "B", 1), 0.1691880534207777)
assert isclose(finite_clone_harm(plus, "A", 1), 0.5305771227396905)
assert isclose(finite_clone_harm(plus, "B", 1), 0.8304764839513198)

alpha = 0.05
gap = 0.30
n_direct = ceil(log(1 / alpha) / gap**2)
observed_clone_gap = float(F(41, 100) - F(17, 100))
n_noisy = ceil(log(1 / alpha) / observed_clone_gap**2)
h = 0.05
n_selector = ceil(log(4 * 2 / alpha) / (2 * h**2))
assert n_direct == 34
assert n_noisy == 53
assert n_selector == 1016

print({
    "success_plus_A": str(clone_success(plus, "A")),
    "success_plus_B": str(clone_success(plus, "B")),
    "success_minus_A": str(clone_success(minus, "A")),
    "success_minus_B": str(clone_success(minus, "B")),
    "harm_plus_A": str(clone_harm(plus, "A")),
    "harm_plus_B": str(clone_harm(plus, "B")),
    "reporter_clone_success_plus_A": str(clone_report_success(plus, "A", sens_plus, fp_plus)),
    "reporter_clone_success_plus_B": str(clone_report_success(plus, "B", sens_plus, fp_plus)),
    "finite_T1_success_plus_A": finite_clone_success(plus, "A", 1),
    "finite_T1_success_plus_B": finite_clone_success(plus, "B", 1),
    "ranking_n_per_action_direct_gap_0.30_alpha_0.05": n_direct,
    "ranking_n_per_action_known_sensitivity_0.9_fp_0.1": n_noisy,
    "selector_n_per_action_m2_h0.05_alpha0.05": n_selector,
    "status": "internal exact finite diagnostic; not biological validation",
})
