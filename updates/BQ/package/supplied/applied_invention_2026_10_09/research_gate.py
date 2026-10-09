#!/usr/bin/env python3
"""Executable investigation of noise-coded, snapshot-only network identification.

This is a candidate-mechanism test suite, not a demonstrated breakthrough.
It deliberately includes a stronger comparison: known, randomized mean shifts.
Synthetic Gaussian samples are generated from exact stationary covariances for
checking the mathematics. This does NOT acquire stationarity in a laboratory.

Run: OPENBLAS_NUM_THREADS=1 python research_gate.py --output results.json
Dependencies: Python >=3.10, NumPy, SciPy.
"""
from __future__ import annotations

import argparse
import json
import math
import platform
import time
from pathlib import Path
from typing import Any

import numpy as np
import scipy
from numpy.typing import NDArray
from scipy.linalg import solve_continuous_lyapunov

Array = NDArray[np.float64]


def symmetric(a: Array) -> Array:
    return (a + a.T) / 2.0


def stationary_covariance(drift: Array, diffusion_cov: Array) -> Array:
    """Solve B Sigma + Sigma B.T + Q = 0 for a stable, supplied simulator."""
    if drift.ndim != 2 or drift.shape[0] != drift.shape[1]:
        raise ValueError("drift must be square")
    if diffusion_cov.shape != drift.shape:
        raise ValueError("diffusion covariance and drift shapes differ")
    if np.max(np.linalg.eigvals(drift).real) >= 0:
        raise ValueError("stationary covariance requires a Hurwitz drift")
    sigma = symmetric(solve_continuous_lyapunov(drift, -diffusion_cov))
    if np.linalg.eigvalsh(sigma).min() < -1e-10 * max(1.0, np.linalg.norm(sigma, 2)):
        raise ArithmeticError("computed stationary covariance is not PSD")
    return sigma


def lyapunov_design(covariances: list[Array]) -> Array:
    """Build a SMALL-SYSTEM dense design, with Frobenius/isometric scaling.

    For n variables and m conditions, stores O(m*n**4) floats and is NOT a
    scalable implementation. The report specifies the matrix-free alternative.
    """
    if not covariances:
        raise ValueError("at least one covariance matrix is required")
    n = covariances[0].shape[0]
    if n > 24:
        raise ValueError("dense research implementation is limited to n <= 24")
    out = np.empty((len(covariances) * n * n, n * n))
    for i in range(n):
        for j in range(n):
            e = np.zeros((n, n))
            e[i, j] = 1
            out[:, i*n+j] = np.concatenate(
                [(e @ c + c @ e.T).ravel() for c in covariances]
            ) / math.sqrt(len(covariances))
    return out


def decode_covariance_differences(covs: list[Array], forcings: list[Array],
                                  gamma: float) -> tuple[Array, dict[str, float]]:
    """Recover A in drift A-gamma*I from covariance differences and known D.

    covs are measured Sigma_s - Sigma_baseline, and extra diffusion is 2*gamma*D_s.
    No true A or true background diffusion is passed to this decoder.
    Its returned singular value is numerical, not an interval certificate.
    """
    if len(covs) != len(forcings) or not covs or gamma <= 0:
        raise ValueError("invalid covariance/forcing lists or gamma")
    n = covs[0].shape[0]
    design = lyapunov_design(covs)
    target = np.concatenate([2*gamma*(c-d).ravel() for c,d in zip(covs,forcings)])
    target /= math.sqrt(len(covs))
    a, _, rank, singular = np.linalg.lstsq(design, target, rcond=None)
    if rank != n*n:
        raise ArithmeticError("the supplied experiments do not identify all drift entries")
    return a.reshape(n,n), {
        "design_sigma_min": float(singular[-1]),
        "design_condition": float(singular[0]/singular[-1]),
        "rms_equation_residual": float(np.linalg.norm(design@a-target)),
    }


def random_binary_code(n: int, rng: np.random.Generator,
                       relative_distance: float = 0.25) -> tuple[Array, float]:
    """Generate and explicitly check a conservative logarithmic-length code.

    m=ceil(8 log(n(n-1)))+1 makes the union bound for a pair closer than m/4
    less than 1/2. Rejection sampling has finite expected trials. The pairwise
    check costs O(n**2*m). These conservative constants often erase any saving
    in condition count at small n; they are not suppressed in the output.
    """
    if n < 2 or relative_distance != 0.25:
        raise ValueError("this checked construction uses n>=2 and distance 1/4")
    m = max(8, math.ceil(8*math.log(max(2,n*(n-1))))+1)
    for _ in range(100):
        h = rng.choice(np.array([-1.,1.]), size=(m,n))
        gram = h.T @ h
        dist = (m - gram)/2
        np.fill_diagonal(dist, m)
        delta = float(dist.min()/m)
        if delta >= relative_distance:
            return h, delta
    raise RuntimeError("code construction failed after 100 checked attempts")


def observational_ambiguity() -> dict[str, Any]:
    j = np.array([[0.,-1.],[1.,0.]])
    records=[]
    for omega in [0.,1.,10.,1000.]:
        b = -np.eye(2)+omega*j
        sigma=stationary_covariance(b,2*np.eye(2))
        records.append({"omega":omega,"distance_from_identity":float(np.linalg.norm(sigma-np.eye(2)))})
    assert max(x["distance_from_identity"] for x in records) < 1e-11
    return {"model":"B=-I+omega*J; diffusion covariance=2I", "checks":records}


def two_noise_counterexample() -> dict[str, Any]:
    c0=np.eye(3)
    c1=np.diag([1.,1.,2.])
    k=np.array([[0.,0.,1.],[0.,0.,0.],[-1.,0.,0.]])
    j=np.array([[0.,1.,0.],[-1.,0.,0.],[0.,0.,0.]])
    b0=-5*np.eye(3)+k
    q0=-(b0@c0+c0@b0.T)
    q1=-(b0@c1+c1@b0.T)
    maximum=0.0
    for theta in [0.,0.5,2.,20.,200.]:
        b=b0+theta*j
        maximum=max(maximum,np.linalg.norm(stationary_covariance(b,q0)-c0),
                    np.linalg.norm(stationary_covariance(b,q1)-c1))
    assert maximum < 1e-10
    eig=np.linalg.eigvalsh(q1)
    assert np.min(np.diff(eig)) > 0.09
    return {"B0":b0.tolist(),"invisible_generator_J":j.tolist(),"Q0":q0.tolist(),
            "Q1":q1.tolist(),"Sigma0":c0.tolist(),"Sigma1":c1.tolist(),
            "Q1_eigenvalues":eig.tolist(),"max_covariance_replay_error":float(maximum)}


def coded_recovery(rng: np.random.Generator) -> list[dict[str, Any]]:
    records=[]
    for n in [3,5,8,12]:
        h,delta=random_binary_code(n,rng)
        # Complement every setting. D_s=I+/-H_s is positive semidefinite.
        forcings=[np.diag(1+sign*row) for row in h for sign in [-1.,1.]]
        raw=rng.normal(size=(n,n))
        a=raw/np.linalg.norm(raw,2)
        gamma=9.0
        b=a-gamma*np.eye(n)
        # Unknown, correlated background diffusion; ignored by the decoder.
        z=rng.normal(size=(n,n))
        background=2*gamma*(np.eye(n)+0.05*z@z.T/n)
        sigma0=stationary_covariance(b,background)
        covs=[stationary_covariance(b,background+2*gamma*d)-sigma0 for d in forcings]
        ahat,diag=decode_covariance_differences(covs,forcings,gamma)
        exact_error=float(np.linalg.norm(ahat-a))
        a0=2*math.sqrt(delta)
        r=np.linalg.norm(a,2)/gamma
        analytic_lower=a0-4*r/(1-r)
        observed_gap_lower=a0-2*max(np.linalg.norm(c-d,2) for c,d in zip(covs,forcings))
        assert exact_error < 1e-10
        assert diag["design_sigma_min"] >= analytic_lower-1e-10
        assert diag["design_sigma_min"] >= observed_gap_lower-1e-10
        records.append({"n":n,"code_bits":len(h),"total_conditions_including_baseline":len(forcings)+1,
                        "checked_relative_code_distance":delta,"gamma_over_A_norm":float(gamma/np.linalg.norm(a,2)),
                        "recovery_frobenius_error":exact_error,"analytic_singular_lower_bound":float(analytic_lower),
                        "observed_design_lower_bound":float(observed_gap_lower),**diag})
    return records


def fisher_information(q: Array, k: Array, gamma: float=1.0) -> tuple[float,float]:
    """Exact local information at B=-gamma*I for a skew-drift direction K.

    Noise experiment: extra diffusion 2*gamma*Q, X~N(0,I+Q).
    Mean experiment: record Z~N(0,Q), apply constant input gamma*Z;
                     X|Z~N(Z,I) at the reference point.
    Equal added stationary second moment tr(Q), not an assertion of equal
    physical actuator power, bandwidth, calibration cost, or feasibility.
    """
    if gamma <= 0 or q.shape != k.shape:
        raise ValueError("invalid arguments")
    if not np.allclose(k,-k.T,atol=1e-10):
        raise ValueError("K must be skew-symmetric")
    eigen, vectors=np.linalg.eigh(symmetric(q))
    if eigen.min() < -1e-10:
        raise ValueError("Q must be positive semidefinite")
    eigen=np.maximum(eigen,0)
    kt=vectors.T@k@vectors
    inoise=0.0
    imean=0.0
    for i in range(len(eigen)):
        for j in range(i+1,len(eigen)):
            weight=kt[i,j]**2
            qi,qj=eigen[i],eigen[j]
            inoise+=weight*(qi-qj)**2/(4*gamma**2*(1+qi)*(1+qj))
            imean+=weight*(qi+qj)/gamma**2
    return float(inoise),float(imean)


def fisher_tests(rng: np.random.Generator) -> dict[str, Any]:
    ratios=[]
    max_violation=-math.inf
    for n in [2,3,5,8,16,32]:
        for _ in range(30):
            u,_=np.linalg.qr(rng.normal(size=(n,n)))
            eigen=np.exp(rng.uniform(-5,5,size=n))
            q=(u*eigen)@u.T
            raw=rng.normal(size=(n,n))
            k=(raw-raw.T)/2
            noise,mean=fisher_information(q,k)
            max_violation=max(max_violation,4*noise-mean)
            if noise>1e-15:
                ratios.append(mean/noise)
    assert min(ratios) >= 4-1e-10
    asymptotic=[]
    k=np.array([[0.,1.],[-1.,0.]])
    for scale in [1.,10.,100.,10000.]:
        noise,mean=fisher_information(np.diag([scale,0.]),k)
        asymptotic.append({"q":scale,"mean_to_noise_information_ratio":mean/noise,
                           "theory_ratio":4*(1+1/scale)})
    assert abs(asymptotic[-1]["mean_to_noise_information_ratio"]-4.0004)<1e-9
    return {"random_psd_cases":180,"minimum_mean_to_noise_information_ratio":min(ratios),
            "maximum_4I_noise_minus_I_mean":max_violation,"sharp_factor_four_sequence":asymptotic,
            "balanced_binary_noise_code_ratio":12.0,
            "comparison_budget":"Equal added stationary second moment; known mean-intervention label observed."}


def score_monte_carlo(rng: np.random.Generator, total: int=600000) -> dict[str, Any]:
    """Check exact information formulas using raw Gaussian experiments.

    Four equiprobable masks: Q diagonal entries independently 0 or 2.
    The mean-shift experiment records its randomized applied offset Z.
    """
    q=2*rng.integers(0,2,size=(total,2))
    d=1+q
    x=rng.normal(size=(total,2))*np.sqrt(d)
    noise_score=(d[:,1]-d[:,0])*x[:,0]*x[:,1]/(2*d[:,0]*d[:,1])
    z=rng.normal(size=(total,2))*np.sqrt(q)
    residual=rng.normal(size=(total,2))
    mean_score=residual[:,0]*z[:,1]-residual[:,1]*z[:,0]
    measured_noise=float(np.mean(noise_score**2))
    measured_mean=float(np.mean(mean_score**2))
    assert abs(measured_noise-1/6)<0.003
    assert abs(measured_mean-2)<0.03
    return {"independent_samples_each_protocol":total,
            "noise_score_second_moment":measured_noise,"noise_theory":1/6,
            "mean_score_second_moment":measured_mean,"mean_theory":2,
            "measured_information_ratio":measured_mean/measured_noise,"theory_ratio":12.0}


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",type=Path,default=Path("results.json"))
    parser.add_argument("--seed",type=int,default=20261009)
    args=parser.parse_args()
    rng=np.random.default_rng(args.seed)
    started=time.perf_counter()
    result={"status":"NO_FOUNDATIONAL_BREAKTHROUGH_ESTABLISHED; candidate comparison gate failed",
            "seed":args.seed,"environment":{"python":platform.python_version(),
                                             "numpy":np.__version__,"scipy":scipy.__version__},
            "observational_ambiguity":observational_ambiguity(),
            "two_noise_counterexample":two_noise_counterexample(),
            "coded_exact_recovery":coded_recovery(rng),
            "fisher_comparison":fisher_tests(rng),
            "raw_sample_score_check":score_monte_carlo(rng),
            "limits":["Synthetic mathematical checks, not a representative application benchmark.",
                      "No hardware test, no real biological data, no trained scientific model.",
                      "The dense decoder is intentionally limited to small systems.",
                      "Floating-point replay is not a formal proof or interval arithmetic certification.",
                      "Stationary covariance generation is simulator ground truth, not acquisition by the learner.",
                      "Local Fisher information concerns regular local inference and the specified shared budget."]}
    result["elapsed_seconds"]=time.perf_counter()-started
    args.output.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))

if __name__=="__main__":
    main()
