#!/usr/bin/env python3
"""Numerical independent checks of noisy replay and the first-stage identity.

These checks support the algebra; Monte Carlo is not its proof. The fixed
seed, sample count, paired standard errors and all scope counterexamples are
retained in the JSON result.
"""
import json
import math
from pathlib import Path

import numpy as np


def paired_report(observed, predicted):
    difference = observed-predicted
    se = float(np.std(difference, ddof=1)/math.sqrt(len(difference)))
    mean = float(np.mean(difference))
    return {"observed_mean": float(np.mean(observed)),
            "predicted_mean": float(np.mean(predicted)),
            "paired_difference": mean, "paired_standard_error": se,
            "paired_z_score": mean/se}


def main():
    seed, N, s = 20261031, 100000, .5
    rng = np.random.default_rng(seed)
    V = rng.normal(size=(N, 2))
    noise = math.sqrt(s)*rng.normal(size=(N, 2))
    y1 = V[:, 0]+noise[:, 0]
    coefficients = np.array([[1., 0.], [0., 1.], [1., 1.]])/np.array([[1.], [1.], [math.sqrt(2)]])
    covariances, means = [], []
    for word in [0, 1]:
        angle = .7*np.tanh(y1)+word*math.pi/2
        u2 = np.stack([np.cos(angle), np.sin(angle)], axis=1)
        M = np.zeros((N, 2, 2))
        M[:, 0, 0] = 1
        M[:, 1, :] = u2
        y2 = np.sum(u2*V, axis=1)+noise[:, 1]
        precision = np.eye(2)+np.einsum("bji,bjk->bik", M, M)/s
        P = np.linalg.inv(precision)
        rhs = np.stack([y1, np.zeros(N)], axis=1)+u2*y2[:, None]
        mean = np.einsum("bij,bj->bi", P, rhs)/s
        covariances.append(P)
        means.append(mean)
    P = np.stack(covariances, axis=1)
    mean = np.stack(means, axis=1)
    index = np.arange(N)
    actual_squared_errors = np.zeros(N)
    actual_covariance_risks = np.zeros(N)
    replay_minima = np.zeros(N)
    for C in coefficients:
        # Controller chooses its one bit after the first legal noisy V read.
        words = ((C[1]-.4*C[0])*(y1+.25) >= 0).astype(int)
        estimates = np.einsum("bi,i->b", mean[index, words], C)
        truth = V@C
        risks = np.einsum("i,bwij,j->bw", C, P, C)
        actual_squared_errors += (truth-estimates)**2/len(coefficients)
        actual_covariance_risks += risks[index, words]/len(coefficients)
        replay_minima += risks.min(axis=1)/len(coefficients)
    replay_check = paired_report(actual_squared_errors, actual_covariance_risks)
    assert abs(replay_check["paired_z_score"]) < 6
    gap = actual_covariance_risks-replay_minima
    assert np.min(gap) >= -1e-12

    # Independent noisy first stage H=X+sqrt(tau) Z, nonlinear a and nonzero g.
    tau = .7
    rho, r = 1/(1+tau), tau/(1+tau)
    X = rng.normal(size=N)
    H = X+math.sqrt(tau)*rng.normal(size=N)
    conditional_mean = rho*H
    C = np.stack([conditional_mean, conditional_mean**2+r-1], axis=1)
    mu_g = conditional_mean**2+r+.3*conditional_mean
    a = np.stack([X, X**2-1], axis=1)
    g = X**2+.3*X
    V2 = rng.normal(size=(N, 2))
    j = np.argmax(C*C, axis=1)
    Y = V2[index, j]+math.sqrt(s)*rng.normal(size=N)
    estimate = mu_g+C[index, j]*Y/(1+s)
    truth = g+np.sum(a*V2, axis=1)
    J0_H = 1.09*r+4*r*r+8*r*conditional_mean**2+1.2*r*conditional_mean
    predicted = J0_H+np.sum(C*C, axis=1)-C[index, j]**2/(1+s)
    first_stage_check = paired_report((truth-estimate)**2, predicted)
    assert abs(first_stage_check["paired_z_score"]) < 6
    residual = (g-mu_g)+np.sum((a-C)*V2, axis=1)
    J0 = 1.09*r+4*r*r+8*r*rho
    residual_check = paired_report(residual*residual, np.full(N, J0))
    assert abs(residual_check["paired_z_score"]) < 6
    output = {
        "seed": seed, "independent_replay_draws": N, "noise_variance": s,
        "scope": "Numerical checks; proofs and exclusions are in NOISY_CONTROL_AUDIT.txt.",
        "adaptive_noisy_posterior_identity": replay_check,
        "replay_pointwise_minimum_gap": float(np.min(gap)),
        "replay_expected_minimum_risk": float(np.mean(replay_minima)),
        "first_stage_total_risk_identity": first_stage_check,
        "first_stage_irreducible_residual_identity": residual_check,
        "analytic_J0": J0,
        "excluded_access_models": {
            "actuator_only_output": {"actual_risk": 1., "controller_risk": s/(1+s)},
            "uncharged_B1_termination": {
                "three_word_risk": s/(1+s), "two_word_optimum": 1-2/(3*(1+s))},
            "uncharged_public_context": {
                "context_adapted_risk": s/(1+s), "unconditional_one_matrix_risk": 1-1/(2*(1+s))},
        },
    }
    path = Path(__file__).with_name("noisy_control_checks_results.json")
    path.write_text(json.dumps(output, indent=2)+"\n")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
