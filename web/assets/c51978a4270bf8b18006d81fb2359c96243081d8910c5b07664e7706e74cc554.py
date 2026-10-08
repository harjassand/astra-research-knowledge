#!/usr/bin/env python3
"""Exact coefficient algebra and a numeric first-sine constrained check.

Uses only Python's standard library. The Fraction block is exact. The
Simpson block is diagnostic evidence for the pure-sine trial only; it is not
used in the proof that non-sine modes cannot change the p^3 coefficient.
"""

from fractions import Fraction as F
import json
import math


def simpson(f, n=16384):
    if n % 2:
        raise ValueError("Simpson subdivision count must be even")
    h = 1.0 / n
    terms = [f(0.0), f(1.0)]
    for i in range(1, n):
        terms.append((4.0 if i % 2 else 2.0) * f(i * h))
    return h * math.fsum(terms) / 3.0


def exact_coefficients():
    # Coefficients in rho and rho^2:
    # rho=theta^2/4-theta^4/48+theta^6/1440+O(theta^8),
    # rho^2=theta^4/16-theta^6/96+O(theta^8).
    c4_over_lambda = F(1, 48) - F(1, 3) * F(1, 16)
    c6_over_lambda = F(1, 3) * F(1, 96) - F(1, 1440)
    assert c4_over_lambda == 0
    assert c6_over_lambda == F(1, 360)

    int_sin2 = F(1, 2)
    int_sin4 = F(3, 8)
    int_sin6 = F(5, 16)
    assert (int_sin2, int_sin4, int_sin6) == (F(1, 2), F(3, 8), F(5, 16))

    # theta=t sin(pi x): p=t^2/8+O(t^4), E=lambda_c*t^6/1152+O(t^8).
    fixed_amplitude_over_lambda = c6_over_lambda * int_sin6
    p_leading_over_t2 = F(1, 4) * int_sin2
    reduced_over_lambda = fixed_amplitude_over_lambda / p_leading_over_t2**3
    assert fixed_amplitude_over_lambda == F(1, 1152)
    assert p_leading_over_t2 == F(1, 8)
    assert reduced_over_lambda == F(4, 9)

    # With lambda_c=2 J pi^2, the reduced coefficient is 8 J pi^2 / 9.
    return {
        "quartic_energy_coefficient_over_lambda_c": str(c4_over_lambda),
        "sixth_energy_coefficient_over_lambda_c": str(c6_over_lambda),
        "integral_sin2": str(int_sin2),
        "integral_sin4": str(int_sin4),
        "integral_sin6": str(int_sin6),
        "fixed_amplitude_t6_coefficient_over_lambda_c": str(fixed_amplitude_over_lambda),
        "mass_leading_coefficient_p_over_t2": str(p_leading_over_t2),
        "fixed_mass_p3_coefficient_over_lambda_c": str(reduced_over_lambda),
        "fixed_mass_p3_coefficient_for_lambda_c_2Jpi2": "8*J*pi^2/9",
        "exact_checks_passed": True,
    }


def numeric_sine_trials():
    J = 1.0
    lam = 2.0 * J * math.pi**2
    kap = lam / 3.0
    rows = []
    for t in (0.4, 0.3, 0.2, 0.15, 0.1):
        rho = lambda x: math.sin(0.5 * t * math.sin(math.pi * x)) ** 2
        p = simpson(rho)
        int_rho2 = simpson(lambda x: rho(x) ** 2)
        kinetic = J * math.pi**2 * t**2 / 4.0
        energy = kinetic - kap * int_rho2 - lam * p
        rows.append({
            "t": t,
            "p": p,
            "E_over_p3": energy / p**3,
        })
    target = 4.0 * lam / 9.0
    return {
        "J": J,
        "lambda_c": lam,
        "kappa_t": kap,
        "target_4lambda_over_9": target,
        "trials": rows,
        "interpretation": "pure-sine quadrature check; ratios approach target as p tends to zero; not the all-shape proof",
    }


def main():
    print(json.dumps({
        "exact": exact_coefficients(),
        "numeric": numeric_sine_trials(),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
