"""Exact Gaussian robustness formulas and signed-output estimation.

Research prototype: floating-point, not an interval-certified implementation.
This estimates bounded functions of outputs. It is NOT a full-distribution
sampler for the signed target law. Physical eta is particle survival probability.
"""
from __future__ import annotations
from typing import Callable, Optional, Sequence
import math
import numpy as np
from fermion_completion import (vacuum_covariance, pair_covariance,
                                gaussian_loss, sample_covariance)


def magic_robustness(eta: float) -> float:
    """Both standard and generalized convex-Gaussian robustness."""
    if not math.isfinite(eta) or not 0 <= eta <= 1:
        raise ValueError("Require finite 0 <= eta <= 1.")
    a,b=(1-eta)**2,eta**2
    return b*b/(4*a) if b <= 2*a and a > 0 else b-a


def magic_trace_distance(eta: float) -> float:
    """Exact distance to the convex hull of all pure fermionic Gaussians."""
    if not math.isfinite(eta) or not 0 <= eta <= 1:
        raise ValueError("Require finite 0 <= eta <= 1.")
    a,b=(1-eta)**2,eta**2
    return b*b/(math.sqrt(a+b)+math.sqrt(a))**2 if b <= 3*a else (b-a)/2


def signed_magic_component(eta: float, rng: np.random.Generator) -> tuple[int,np.ndarray]:
    """Draw sign and a 4-mode Gaussian; weighted mean has mass 1+2R."""
    R=magic_robustness(eta);a,b=(1-eta)**2,eta**2
    gamma=1+2*R
    positive = rng.random() < (1+R)/gamma
    if not positive:
        if b <= 2*a:
            full=True
        else:
            full=bool(rng.random() < b/(2*R))
        return -1, -vacuum_covariance(4) if full else vacuum_covariance(4)
    even_weight = (a+b+R)/(1+R)
    if rng.random() < even_weight:
        zmag=math.sqrt(b/(2*a)) if b <= 2*a and a>0 else 1.0
        phase=np.exp(2j*math.pi*int(rng.integers(3))/3)
        g=np.zeros((8,8))
        g[:4,:4]=pair_covariance(zmag*phase)
        g[4:,4:]=pair_covariance(zmag*phase)
    else:
        g=vacuum_covariance(4);j=int(rng.integers(4))
        g[2*j,2*j+1],g[2*j+1,2*j]=1.,-1.
    return 1,g


def estimate_output_function(etas: Sequence[float], transfer: np.ndarray,
                             function: Callable[[np.ndarray],float],
                             draws: int, failure_probability: float = .05,
                             seed: Optional[int] = None) -> dict:
    """Unbiased (ideal arithmetic) signed estimate of E[f(output)], |f|<=1.

    Complexity includes Gamma^2 for an additive-error confidence interval.
    The reported interval is the exact-arithmetic Hoeffding statistical radius;
    numerical rounding is NOT included. transfer follows the declared input loss.
    """
    if draws < 1 or not 0 < failure_probability < 1:
        raise ValueError("Positive draws and failure probability in (0,1) required.")
    etas=list(etas)
    rs=[magic_robustness(e) for e in etas]
    log_gamma=sum(math.log1p(2*r) for r in rs)
    if log_gamma > 650:
        raise OverflowError("Signed overhead too large for this prototype.")
    weight=math.exp(log_gamma)
    t=np.asarray(transfer,complex);m=4*len(etas)
    if t.ndim!=2 or t.shape[1]!=m or np.linalg.norm(t,2)>1+2e-10:
        raise ValueError("Transfer dimensions/contraction invalid.")
    rng=np.random.default_rng(seed);values=np.empty(draws)
    for k in range(draws):
        g=np.zeros((2*m,2*m));sign=1
        for j,e in enumerate(etas):
            ss,gg=signed_magic_component(e,rng);sign*=ss
            g[8*j:8*j+8,8*j:8*j+8]=gg
        out=sample_covariance(gaussian_loss(g,t),rng)
        f=float(function(out))
        if not math.isfinite(f) or abs(f)>1+1e-12:
            raise ValueError("Function must return finite values in [-1,1].")
        values[k]=weight*sign*f
    radius=weight*math.sqrt(2*math.log(2/failure_probability)/draws)
    return {"estimate":float(values.mean()),"hoeffding_radius":radius,
            "failure_probability":failure_probability,"draws":draws,
            "absolute_signed_mass":weight,
            "sample_standard_error":float(values.std(ddof=1)/math.sqrt(draws)) if draws>1 else None,
            "status":"floating-point; statistical interval excludes rounding error"}


def optimal_loss_concentration(eta: float, target_eta: float = .5) -> dict:
    """Exact one-copy Gaussian filtering parameters in the robustness regime.

    Each mode uses K_success=diag(sqrt(s),1). All four successes transform
    rho_eta into rho_target_eta. Probability saturates R(eta)/R(target_eta).
    A beamsplitter with a filled ancillary mode and occupation measurement
    realizes each Kraus operator. eta and target_eta are input loss parameters.
    """
    cutoff=math.sqrt(2)/(1+math.sqrt(2))
    if not 0 < eta <= target_eta <= cutoff:
        raise ValueError("Require 0 < eta <= target_eta <= sqrt(2)/(1+sqrt(2)).")
    s=eta*(1-target_eta)/(target_eta*(1-eta))
    p=eta**4*(1-target_eta)**2/(target_eta**4*(1-eta)**2)
    return {"empty_mode_survival_s":s,"all_four_success_probability":p,
            "optimality_bound":magic_robustness(eta)/magic_robustness(target_eta),
            "expected_independent_attempts":1/p}
