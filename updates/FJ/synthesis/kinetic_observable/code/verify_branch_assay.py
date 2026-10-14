#!/usr/bin/env python3
"""Exact checks for the source-prepared branching/offspring assay.

This reads the pinned finite-response result as data; it does not execute or
modify any capital code.  All arithmetic below is rational.
"""
from fractions import Fraction as F
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
FINITE_RESPONSE = (
    ROOT
    / "work/astra-capital/updates/FI/synthesis/kinetics_critic/finite_response_results.json"
)


def mixture_moments(rates, weights):
    mean = sum((p / lam for p, lam in zip(weights, rates)), F(0))
    second = 2 * sum((p / (lam * lam) for p, lam in zip(weights, rates)), F(0))
    variance = second - mean * mean
    return mean, second, variance


def main():
    src = json.loads(FINITE_RESPONSE.read_text())
    rates0 = [F(s) for s in src["baseline_rates"]]
    weights0 = [F(s) for s in src["baseline_weights"]]
    shifts = [F(s) for s in src["shifts"]]
    response0 = [F(s) for s in src["baseline_response"]]

    def response(rates, weights, shift):
        return sum((p / (lam + shift) for p, lam in zip(weights, rates)), F(0))

    assert sum(weights0, F(0)) == 1
    assert [response(rates0, weights0, s) for s in shifts] == response0
    mean0, second0, var0 = mixture_moments(rates0, weights0)
    assert mean0 == F(src["baseline_mean"])

    hidden = next(x for x in src["exact_samples"] if x["epsilon"] == "1/100000000")
    eps = F(hidden["epsilon"])
    rates1 = rates0 + [eps]
    weights1 = [F(s) for s in hidden["old_weights"]] + [F(src["hidden_mass"])]
    assert sum(weights1, F(0)) == 1
    assert min(weights1) > 0
    response1 = [response(rates1, weights1, s) for s in shifts]
    assert response1 == response0
    mean1, second1, var1 = mixture_moments(rates1, weights1)
    assert mean1 == F(hidden["mean"])
    assert mean1 > mean0

    # If a parent lives for T and emits children at constant rate alpha,
    # then K|T ~ Poisson(alpha*T).  At alpha=1/E[T],
    # Var(K)=1+Var(T)/E[T]^2.
    def offspring_variance_at_critical(mean, variance):
        alpha = 1 / mean
        return alpha * mean + alpha * alpha * variance

    # A connected two-state reversible killed CTMC.  Q=-A has symmetric
    # interconversion eps and killing rates 1 (state 0), eps (state 1).
    delta = F(1, 1000)
    A00, A01, A11 = 1 + eps, -eps, 2 * eps
    det = A00 * A11 - A01 * A01
    assert det > 0
    # A^{-1} 1 = (3 eps, 1+2 eps)/(2 eps+eps^2).
    inv1 = [3 * eps / det, (1 + 2 * eps) / det]
    p = [1 - delta, delta]
    mean2 = sum((pi * ui for pi, ui in zip(p, inv1)), F(0))
    # E[T^2]=2 p^T A^{-2} 1.  Apply A^{-1} once more exactly.
    inv2_1 = [
        (A11 * inv1[0] - A01 * inv1[1]) / det,
        (-A01 * inv1[0] + A00 * inv1[1]) / det,
    ]
    second2 = 2 * sum((pi * ui for pi, ui in zip(p, inv2_1)), F(0))
    var2 = second2 - mean2 * mean2
    assert mean2 > 0 and var2 >= 0

    # Exact finite-sample variance identity for N independent founder runs.
    # K|R ~ Poisson(alpha R), so Var(K)=alpha*mu+alpha^2*Var(R).
    alpha = 1 / mean2
    mean_k = alpha * mean2
    var_k = alpha * mean2 + alpha * alpha * var2
    assert mean_k == 1
    assert var_k == 1 + var2 / (mean2 * mean2)
    chebyshev_n_fraction = var_k / F(1, 2000)
    chebyshev_n = (chebyshev_n_fraction.numerator + chebyshev_n_fraction.denominator - 1) // chebyshev_n_fraction.denominator
    rarity_start_lower_bound = math.ceil(math.log(2 / 3) / math.log(float(1 - delta)))

    out = {
        "input": "pinned N804 finite_response_results.json, read as data",
        "finite_response_pair": {
            "shifts": [str(x) for x in shifts],
            "identical_responses": [str(x) for x in response0],
            "baseline": {
                "mean": str(mean0),
                "critical_birth_rate": str(1 / mean0),
                "second_lifetime_moment": str(second0),
                "lifetime_variance": str(var0),
                "offspring_variance_at_critical": str(
                    offspring_variance_at_critical(mean0, var0)
                ),
            },
            "hidden_slow_component_epsilon_1e-8": {
                "weights": [str(x) for x in weights1],
                "minimum_weight": str(min(weights1)),
                "mean": str(mean1),
                "mean_float": float(mean1),
                "critical_birth_rate": str(1 / mean1),
                "critical_birth_rate_float": float(1 / mean1),
                "second_lifetime_moment": str(second1),
                "lifetime_variance": str(var1),
                "offspring_variance_at_critical": str(
                    offspring_variance_at_critical(mean1, var1)
                ),
            },
        },
        "connected_two_state_reversible_killed_chain": {
            "epsilon": str(eps),
            "source": [str(x) for x in p],
            "A_minus_Q": [[str(A00), str(A01)], [str(A01), str(A11)]],
            "determinant": str(det),
            "mean_lifetime": str(mean2),
            "mean_lifetime_float": float(mean2),
            "critical_birth_rate": str(alpha),
            "critical_birth_rate_float": float(alpha),
            "second_lifetime_moment": str(second2),
            "lifetime_variance": str(var2),
            "offspring_mean_at_critical": str(mean_k),
            "offspring_variance_at_critical": str(var_k),
            "offspring_variance_at_critical_float": float(var_k),
            "relative_variance_factor_at_critical": str(var_k),
            "founder_runs_for_10pct_relative_error_95pct_chebyshev": chebyshev_n,
            "expected_source_preparations_at_critical": 2 * chebyshev_n,
            "expected_root_kinetic_time_at_critical": float(mean2) * chebyshev_n,
        },
        "sampling_formula": {
            "mu_hat": "sum(K_i)/(N*alpha)",
            "variance": "[mu/alpha + Var(R)]/N",
            "chebyshev_relative_error_bound": "[1/(alpha*mu)+CV(R)^2]/(N*epsilon_rel^2)",
            "scope": "instance-wise bound; CV(R), source-preparation cost, and physical branch actuator must be acquired",
        },
        "source_rarity_lower_bound": {
            "delta": str(delta),
            "epsilon": str(eps),
            "model_0": "every source draw has T~Exp(1)",
            "model_1": "each source draw is slow with probability delta and then T~Exp(epsilon); otherwise T~Exp(1)",
            "censored_path_tv_per_source_draw_upper_bound": "delta",
            "N_draw_product_tv_upper_bound": "1-(1-delta)^N <= N*delta",
            "starts_for_error_below_one_third_at_delta_1e-3": rarity_start_lower_bound,
            "interpretation": "under controls that preserve the fast branch and do not label hidden components, distinguishing the hidden source component with error <1/3 needs Omega(1/delta) independent source starts",
        },
        "checks": {
            "finite_responses_exactly_equal": response1 == response0,
            "all_adjusted_source_masses_positive": min(weights1) > 0,
            "finite_response_mean_separated": mean1 > mean0,
            "critical_birth_rate_exact_reciprocal": alpha * mean2 == 1,
            "offspring_variance_identity_exact": var_k == 1 + var2 / mean2**2,
        },
        "scope": "exact rational algebra checks; not a physical experiment, external review, or novelty result",
    }
    result_path = ROOT / "work/FJ-kinetic-observable/results/branch_assay_exact_results.json"
    result_path.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
