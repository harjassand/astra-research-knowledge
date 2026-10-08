#!/usr/bin/env python3
"""Exact killed-boundary truncations for the specified B-chain reward."""

from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BETAS = {
    "1/5": Fraction(1, 5),
    "1": Fraction(1, 1),
    "3": Fraction(3, 1),
    "5": Fraction(5, 1),
}
N_VALUES = (2, 3, 5, 10, 20, 40)


def add(x, y):
    return x[0] + y[0], x[1] + y[1]


def scale(c, x):
    return c * x[0], c * x[1]


def killed_truncation(beta: Fraction, N: int) -> Fraction:
    """Exact E_1[pair deaths before B=0 or birth from N to cemetery].

    At state N, a birth is sent to a reward-free absorbing cemetery; a pair
    death N->N-2 still earns one reward and continues in the truncated chain.
    The resulting value is a pathwise lower bound on the unbounded reward.
    """
    if beta <= 0 or N < 2:
        raise ValueError("require beta>0 and N>=2")

    # Each unknown f_b is represented as A_b*t + C_b, where t=f_1=f_2.
    affine = [(Fraction(0), Fraction(0)) for _ in range(N + 2)]
    affine[1] = (Fraction(1), Fraction(0))
    affine[2] = (Fraction(1), Fraction(0))

    # Interior Bellman equations, for 2 <= b < N:
    # (beta+b-1) f_b = beta f_(b+1) + (b-1)(1+f_(b-2)).
    for b in range(2, N):
        ab, cb = affine[b]
        alo, clo = affine[b - 2]
        affine[b + 1] = (
            ((beta + b - 1) * ab - (b - 1) * alo) / beta,
            ((beta + b - 1) * cb - (b - 1) * (1 + clo)) / beta,
        )

    # At the upper boundary, birth from N exits without further reward:
    # (beta+N-1) f_N = (N-1)(1+f_(N-2)); this is f_(N+1)=0.
    an, cn = affine[N]
    alo, clo = affine[N - 2]
    coefficient = (beta + N - 1) * an - (N - 1) * alo
    constant = (beta + N - 1) * cn - (N - 1) * (1 + clo)
    if coefficient == 0:
        raise ArithmeticError("degenerate affine boundary equation")
    return -constant / coefficient


def main():
    import mpmath as mp

    mp.mp.dps = 80
    output = {
        "chain": {
            "birth_rate_at_b": "beta*b",
            "pair_death_rate_at_b": "b*(b-1), with transition b -> b-2",
            "absorbing_state": 0,
            "initial_state": 1,
            "reward": "one per pair-death transition",
        },
        "finite_boundary": {
            "states": "0..N plus cemetery",
            "boundary_condition": "birth from state N exits to a reward-free absorbing cemetery; pair deaths from N are still counted",
            "recurrence": "(beta+b-1) f_b = beta f_(b+1) + (b-1)(1+f_(b-2)), 2<=b<N",
            "top_equation": "(beta+N-1) f_N = (N-1)(1+f_(N-2)); equivalently f_(N+1)=0",
            "bound_direction": "lower bound on the unbounded expected pair-death count, by pathwise stopping and nonnegative reward",
            "monotonicity": "nondecreasing in N under the coupled first-upcrossing construction",
        },
        "truncations": {},
        "candidate_formula": {},
    }

    for label, beta in BETAS.items():
        b = mp.mpf(beta.numerator) / beta.denominator
        formula = (1 + b * mp.e ** (2 * b) * (2 * b) ** (-b) * mp.gammainc(b, 0, 2 * b)) / 2
        output["candidate_formula"][label] = {
            "value_decimal_50dp": mp.nstr(formula, 50),
            "formula": "(1 + beta*exp(2*beta)*(2*beta)^(-beta)*gamma_lower(beta,2*beta))/2",
        }
        entries = []
        previous = None
        for N in N_VALUES:
            value = killed_truncation(beta, N)
            decimal = mp.mpf(value.numerator) / value.denominator
            drift_upper = 1 - beta * value
            entries.append({
                "N": N,
                "exact_numerator": str(value.numerator),
                "exact_denominator": str(value.denominator),
                "lower_bound_decimal_30dp": mp.nstr(decimal, 30),
                "formula_minus_lower_bound_decimal_20dp": mp.nstr(formula - decimal, 20),
                "monotone_from_previous_N": None if previous is None else value >= previous,
                "upper_bound_on_1_minus_beta_h_if_h_is_unbounded_target": {
                    "exact_numerator": str(drift_upper.numerator),
                    "exact_denominator": str(drift_upper.denominator),
                    "decimal_30dp": mp.nstr(mp.mpf(drift_upper.numerator) / drift_upper.denominator, 30),
                },
            })
            previous = value
        output["truncations"][label] = entries

    epsilons = [mp.mpf("1e-3"), mp.mpf("1e-6"), mp.mpf("1e-9")]
    limit_checks = []
    for b in epsilons:
        h = (1 + b * mp.e ** (2 * b) * (2 * b) ** (-b) * mp.gammainc(b, 0, 2 * b)) / 2
        limit_checks.append({"beta": mp.nstr(b, 5), "formula_value": mp.nstr(h, 30)})
    output["small_beta"] = {
        "asymptotic": "beta*gamma_lower(beta,2*beta)->1 and exp(2*beta)*(2*beta)^(-beta)->1, hence h_1(beta)->1 as beta decreases to 0 through positive values",
        "numerical_checks": limit_checks,
    }

    h_fifth = (1 + mp.mpf(1) / 5 * mp.e ** (mp.mpf(2) / 5)
               * (mp.mpf(2) / 5) ** (-mp.mpf(1) / 5)
               * mp.gammainc(mp.mpf(1) / 5, 0, mp.mpf(2) / 5)) / 2
    output["default_drift"] = {
        "expression": "1 - (1/5)*h_1(1/5)",
        "value_from_candidate_formula": mp.nstr(1 - h_fifth / 5, 50),
        "status": "numerical evaluation of the candidate functional; not an infinite-chain proof",
    }

    (ROOT / "results.json").write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps({
        "formula_values": {key: value["value_decimal_50dp"]
                           for key, value in output["candidate_formula"].items()},
        "N40_exact_lower_bound_decimals": {key: rows[-1]["lower_bound_decimal_30dp"]
                                           for key, rows in output["truncations"].items()},
        "default_drift": output["default_drift"]["value_from_candidate_formula"],
        "small_beta_checks": limit_checks,
    }, indent=2))


if __name__ == "__main__":
    main()
