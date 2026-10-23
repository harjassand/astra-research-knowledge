#!/usr/bin/env python3
"""Bounded algebraic replays, no simulations or favorable-regime sweep.

Fractions verify finite identities. erf/exp/log numerics illustrate the exact
displayed analytic inequalities; they are not outward-rounded certificates.
"""

from fractions import Fraction as F
import json
import math
from pathlib import Path
from statistics import NormalDist


def main():
    # One fixed constant-amplitude case. Set r=1,s=4,a=1/2 and
    # kappa=16 log2, so each exposure survives with exact probability p=1/2.
    p, a, n = F(1, 2), F(1, 2), 2
    rho = 1 - p ** n
    expected_attempts = sum(p ** j for j in range(n))
    expected_successes = sum(p ** j for j in range(1, n + 1))
    obs_info = a ** 2 * expected_successes
    obs_hazard_moment = a ** 4 * expected_successes
    assert rho == F(3, 4)
    assert expected_attempts == F(3, 2)
    assert expected_successes == F(3, 4)
    assert obs_info ** 2 == expected_successes * obs_hazard_moment
    assert expected_successes == p * rho / (1 - p)
    log2 = math.log(2)
    kappa = 16 * log2
    risk_ceiling = float(rho) / kappa
    assert float(obs_hazard_moment) < risk_ceiling
    conversion_ratio = float(obs_hazard_moment) / risk_ceiling
    assert math.isclose(conversion_ratio, log2, rel_tol=1e-14)

    # Additive expected stopped hazard cannot be inserted into exp(-E H).
    expected_hazard = log2 * float(expected_attempts)
    incorrect_risk = 1 - math.exp(-expected_hazard)
    assert incorrect_risk < float(rho) <= expected_hazard

    # Hazard ordering is NOT needed for the survival-only licensing bound.
    # Shared private tape chooses a (prob3/4) or b (prob1/4). On a: permission
    # if alive; on b: refuse if alive. Safe survival(a,b)=(1,1/2), unsafe=(1/4,1).
    # Thus hazards cross across the actions, yet the permission/death inequality
    # holds with equality, using only the common immortal live process.
    tape_a, tape_b = F(3, 4), F(1, 4)
    q_safe, q_unsafe = {"a": F(1), "b": F(1, 2)}, {"a": F(1, 4), "b": F(1)}
    permit_safe = tape_a * q_safe["a"]
    permit_unsafe = tape_a * q_unsafe["a"]
    death_unsafe = tape_a * (1 - q_unsafe["a"]) + tape_b * (1 - q_unsafe["b"])
    assert q_safe["a"] > q_unsafe["a"] and q_safe["b"] < q_unsafe["b"]
    assert permit_safe - permit_unsafe == death_unsafe == F(9, 16)

    # Exact-formula adaptive survivor selection check, from batched_mean's
    # frozen analytic counterexample: r=1,s=2,theta0=0,a1=1; a2=.1 if Z1<=-1
    # else1. The reported ordinary 95% first-readout interval is inspected only
    # after surviving both exposures. No target experiment or data are simulated.
    normal = NormalDist()
    z = normal.inv_cdf(0.975)
    q_low, q_high = math.exp(-3 * 0.1 ** 2), math.exp(-3)
    below = normal.cdf(-1)
    denom = q_low * below + q_high * (1 - below)
    num = (q_low * (below - normal.cdf(-z))
           + q_high * (normal.cdf(z) - below))
    selected_coverage = num / denom
    completion = math.exp(-3) * denom
    assert 0.86 < selected_coverage < 0.88
    assert selected_coverage < 0.95
    assert completion < 0.01  # discarded deaths must stay visible

    result = {
        "status": "PASS",
        "scope": "exact finite identities plus analytic formula evaluations; no sampled data",
        "constant_exposure_identity": {
            "p": str(p), "N": n, "a": str(a),
            "rho": str(rho), "expected_attempts": str(expected_attempts),
            "expected_successes": str(expected_successes),
            "observed_information_exposure": str(obs_info),
            "observed_a_to_s_moment": str(obs_hazard_moment),
            "holder_equality": True,
            "actual_risk_conversion_ratio": conversion_ratio,
            "exact_conversion_ratio_expression": "log(2)",
            "incorrect_one_minus_exp_negative_expected_stopped_hazard": incorrect_risk},
        "nonmonotone_survival_only_identity": {
            "safe_permission": str(permit_safe),
            "unsafe_permission": str(permit_unsafe),
            "unsafe_death": str(death_unsafe),
            "permission_gap_equals_unsafe_death": True},
        "adaptive_survivor_confidence_counterexample": {
            "nominal_coverage": 0.95,
            "conditional_coverage_after_source_completion": selected_coverage,
            "source_completion_probability": completion,
            "joint_completion_and_coverage_probability": completion * selected_coverage,
            "source_death_probability": 1 - completion,
            "formula_source": "luna_batched_mean/OPENING_CHALLENGE_FROZEN.md"},
        "limitations": [
            "not a formal floating-point or outward-rounded numeric certificate",
            "exact theorems proved separately; finite checks do not prove adaptive claims",
            "no physical exponent calibration or comparative performance experiment",
            "no random source samples, simulator discovery, or downstream task benchmark"]}
    out = Path(__file__).with_name("ANALYTIC_CHECKS.json")
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
