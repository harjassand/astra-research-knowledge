#!/usr/bin/env python3
"""Check a sharp LOCAL Fisher-information identity for two OU experiments.

This is a mathematical comparison, not a new operational capability.
At B_theta=-gamma*I+theta*E, the same known background diffusion 2*gamma*I
is present in both experiments. The noise experiment adds diffusion 2*gamma*Q.
The mean experiment records Z~N(0,Q), applies constant force gamma*Z/2,
and obtains one independent stationary sample. Its added stationary second
moment at theta=0 is tr(Q)/4 versus tr(Q) in the noise experiment.

A variance budget is not actuator power. Equilibration, replicate acquisition,
full-state observation, and intervention calibration are assumptions, not free.
"""
from __future__ import annotations
import argparse
import json
import math
from pathlib import Path
from typing import Any
import numpy as np
from scipy.linalg import solve_continuous_lyapunov


def covariance_fisher(cov: np.ndarray, derivative: np.ndarray) -> float:
    """Fisher information of N(0,cov(theta)) at a positive definite cov."""
    chol = np.linalg.cholesky(cov)
    tmp = np.linalg.solve(chol, derivative)
    whitened = np.linalg.solve(chol, tmp.T).T
    return float(0.5 * np.sum(whitened * whitened))


def compare(q: np.ndarray, e: np.ndarray, gamma: float = 1.0,
            mean_fraction: float = 0.25) -> dict[str, float]:
    """Use the full covariance derivative, allowing an arbitrary real E."""
    if q.shape != e.shape or q.ndim != 2 or q.shape[0] != q.shape[1]:
        raise ValueError("Q and E must be square matrices of the same size")
    if gamma <= 0 or mean_fraction < 0 or not np.allclose(q, q.T):
        raise ValueError("Invalid gamma, mean fraction, or non-symmetric Q")
    if np.linalg.eigvalsh(q).min() < -1e-9 * max(1, np.linalg.norm(q, 2)):
        raise ValueError("Q must be positive semidefinite")
    n = len(q)
    c = np.eye(n) + q
    dc = (e @ c + c @ e.T) / (2 * gamma)
    db = (e + e.T) / (2 * gamma)
    inoise = covariance_fisher(c, dc)
    ibase = covariance_fisher(np.eye(n), db)
    imean = ibase + mean_fraction * float(np.trace(e @ q @ e.T)) / gamma**2
    # Exact nonnegative identity, stated specifically for mean_fraction=1/4.
    eigen, u = np.linalg.eigh(q)
    eigen = np.maximum(eigen, 0)
    er = u.T @ e @ u
    weights = (eigen / (1 + eigen))[:, None] * (1 + eigen)[None, :]
    gain = float(np.sum(weights * er**2)) / (4 * gamma**2)
    return {"noise_information": inoise, "mean_information": imean,
            "quarter_variance_predicted_gain": gain,
            "quarter_variance_identity_error": imean - inoise - gain}


def stationary(b: np.ndarray, diffusion: np.ndarray) -> np.ndarray:
    cov = solve_continuous_lyapunov(b, -diffusion)
    return (cov + cov.T) / 2


def finite_difference_check(q: np.ndarray, e: np.ndarray, gamma: float,
                            step: float = 1e-4) -> dict[str, float]:
    n = len(q)
    ident = np.eye(n)
    plus, minus = -gamma*ident + step*e, -gamma*ident - step*e
    noise_deriv = (stationary(plus, 2*gamma*(ident+q)) -
                   stationary(minus, 2*gamma*(ident+q))) / (2*step)
    base_deriv = (stationary(plus, 2*gamma*ident) -
                  stationary(minus, 2*gamma*ident)) / (2*step)
    mean_deriv = (-np.linalg.solve(plus, gamma*ident/2) +
                  np.linalg.solve(minus, gamma*ident/2)) / (2*step)
    info_noise = covariance_fisher(ident+q, noise_deriv)
    info_mean = covariance_fisher(ident, base_deriv) + float(np.trace(mean_deriv @ q @ mean_deriv.T))
    exact = compare(q, e, gamma)
    return {"noise_information_relative_error": abs(info_noise-exact['noise_information']) / max(1, exact['noise_information']),
            "mean_information_relative_error": abs(info_mean-exact['mean_information']) / max(1, exact['mean_information'])}


def main(output: Path) -> None:
    rng = np.random.default_rng(2026100917)
    ncases = 0
    max_identity_error = 0.0
    min_gain = math.inf
    max_fd = 0.0
    for n in [2, 3, 5, 8, 12]:
        for case in range(60):
            rot, _ = np.linalg.qr(rng.normal(size=(n,n)))
            eigen = np.exp(rng.uniform(-4, 4, size=n))
            # Include singular interventions, not only positive definite Q.
            if case % 3 == 0:
                eigen[:max(1,n//2)] = 0
            q = (rot*eigen) @ rot.T
            e = rng.normal(size=(n,n))
            e /= np.linalg.norm(e, 2)
            gamma = float(np.exp(rng.uniform(-0.5, 0.5)))
            result = compare(q,e,gamma)
            scale = max(1,result['noise_information'],result['mean_information'])
            err = abs(result['quarter_variance_identity_error']) / scale
            max_identity_error = max(max_identity_error,err)
            min_gain = min(min_gain,result['mean_information']-result['noise_information'])
            assert err < 5e-11, result
            assert result['mean_information'] >= result['noise_information']-1e-10*scale
            ncases += 1
            if case % 10 == 0:
                fd = finite_difference_check(q,e,gamma)
                max_fd = max(max_fd,*fd.values())
    assert max_fd < 1e-6
    # Sharpness: one feed-forward perturbation gives equality exactly at 1/4.
    q = np.diag([0.,2.])
    e = np.array([[0.,1.],[0.,0.]])
    sharpness = []
    for fraction in [0.,0.10,0.20,0.249,0.25,1.0]:
        res = compare(q,e,mean_fraction=fraction)
        sharpness.append({"mean_added_variance_fraction":fraction,
                          "noise_information":res['noise_information'],
                          "mean_information":res['mean_information']})
    assert abs(sharpness[-2]['mean_information']-0.75) < 1e-12
    assert abs(sharpness[-2]['noise_information']-0.75) < 1e-12
    assert sharpness[-3]['mean_information'] < sharpness[-3]['noise_information']
    # Raw score check: no exact score expectation is substituted into this MC.
    nsamples = 600_000
    noise_x = rng.normal(size=(nsamples,2))*np.sqrt([1.,3.])
    score_noise = noise_x[:,0]*noise_x[:,1]/2
    z2 = rng.normal(size=nsamples)*math.sqrt(2)
    residual = rng.normal(size=(nsamples,2))
    score_mean = residual[:,0]*z2/2 + residual[:,0]*residual[:,1]/2
    mc_noise, mc_mean = float(np.mean(score_noise**2)),float(np.mean(score_mean**2))
    assert abs(mc_noise-0.75)<0.015 and abs(mc_mean-0.75)<0.015
    payload: dict[str,Any] = {
        "status":"LOCAL_INFORMATION_IDENTITY_CHECKED; NO_FOUNDATIONAL_CAPABILITY_ESTABLISHED",
        "random_matrix_cases":ncases,
        "includes_arbitrary_non_skew_E":True,
        "includes_rotated_rank_deficient_Q":True,
        "maximum_scaled_identity_error":max_identity_error,
        "minimum_observed_information_gain":min_gain,
        "finite_difference_cases":30,
        "maximum_finite_difference_information_error":max_fd,
        "sharp_quarter_variance_examples":sharpness,
        "raw_score_monte_carlo": {"independent_samples_per_experiment":nsamples,
             "noise_score_second_moment":mc_noise,"quarter_variance_mean_score_second_moment":mc_mean,
             "both_theoretical_information":0.75},
        "scope": ["Local at B=-gamma*I with known isotropic background diffusion 2*gamma*I",
                  "Arbitrary real drift tangent E; any PSD noise design Q",
                  "The Gaussian shift Z is recorded; one independent stationary snapshot per replica",
                  "Stationary variance is the resource metric, not actuator energy or laboratory cost",
                  "No claim for general nonlinear models, hidden states, or unknown nuisance diffusion",
                  "Analytic proof is in REPORT.md; numerical checks are not formal verification",
                  "Historical novelty and independent correctness not established"]}
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(payload,indent=2)+'\n')
    print(json.dumps(payload,indent=2))

if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=Path('quarter_variance_results.json'))
    main(parser.parse_args().output)
