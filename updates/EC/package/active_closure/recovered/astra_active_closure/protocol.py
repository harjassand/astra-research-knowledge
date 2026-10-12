#!/usr/bin/env python3
"""Finite-field protocol design and reconstruction.

All quantities use time units with maximum microscopic exit rate <=1.
The design is deliberately conservative. It gives a sample budget, not a
claim that the experiment has been performed or is practically optimal.
"""
from __future__ import annotations
from fractions import Fraction
import argparse
import json
import numpy as np

FIELD_WEIGHTS = {Fraction(2): Fraction(-1,6),
                 Fraction(1,2): Fraction(1,6),
                 Fraction(3,2): Fraction(9,10),
                 Fraction(2,3): Fraction(-9,10)}


def ceil_frac(x: Fraction) -> int:
    return -((-x.numerator)//x.denominator)


def log_upper(x: Fraction) -> int:
    """Integer upper bound on ln(x) for x>1, via ceil(log2(x))."""
    n = max(1, x.numerator.bit_length()-x.denominator.bit_length())
    while Fraction(2)**n < x:
        n += 1
    return n


def design(k: int, rho: Fraction, eta: Fraction, failure: Fraction,
           noise_bound: Fraction = Fraction(1)) -> dict:
    if k < 2 or not (0 < rho <= Fraction(1,k)):
        raise ValueError('Need k>=2 and 0<rho<=1/k.')
    if not (0 < eta <= 1 and 0 < failure < 1 and noise_bound >= 1):
        raise ValueError('Invalid accuracy, confidence or noise bound.')
    u = eta*rho*rho/Fraction(100*k*k)
    s = u/Fraction(1000)
    beta = u*s*s/Fraction(100)
    scalar_statistics = 16*k*k
    # Target stochastic error beta/2. Sensor-calibration and setting bias
    # must together be <= beta/2 per raw scalar mean.
    batch = ceil_frac(8*noise_bound**4/beta**2 *
                      log_upper(Fraction(8*scalar_statistics)/failure))
    total = scalar_statistics * batch
    return {'time_units':'generator divided by supplied exit-rate upper bound',
            'k':k,'rho':str(rho),'operator_accuracy':str(eta),
            'failure':str(failure),'noise_inverse_bound':str(noise_bound),
            'raw_jet_tolerance_u':str(u),'time_step_s':str(s),
            'raw_mean_tolerance_beta':str(beta),
            'field_multiplier_z':[str(z) for z in FIELD_WEIGHTS],
            'field_energy_h':'2*log(z), applied to one true observed label',
            'scalar_statistics_upper_bound':scalar_statistics,
            'samples_per_scalar_upper_bound':str(batch),
            'total_trials_upper_bound':str(total),
            'mixing_wait':'gamma^-1 * log(4*M0*total_trials/failure)',
            'status':'Budget only. No laboratory samples generated.'}


def reconstruct(mu: np.ndarray, C_s: np.ndarray, C_2s: np.ndarray,
                means_s: dict[str,np.ndarray], means_2s: dict[str,np.ndarray],
                s: float) -> tuple[np.ndarray,np.ndarray]:
    """Return raw L and symmetric Gamma estimates from corrected means.

    means arrays have shape (k,k): row a is the applied label potential,
    column b is the terminal label being counted. Values may already be
    corrected for an independently known sensor confusion channel.
    Enforce confidence intervals and generator constraints separately;
    this function does NOT convert small estimated Gamma into exact zero.
    """
    mu=np.asarray(mu,float)
    k=mu.size
    if s<=0 or np.any(mu<=0): raise ValueError('Positive s and label masses required.')
    if C_s.shape!=(k,k) or C_2s.shape!=(k,k): raise ValueError('Incorrect matrix shapes.')
    C0=np.diag(mu)
    A=(C_s-C0)/s
    C2=(C_2s-2*C_s+C0)/s**2
    X2=np.zeros((k,k))
    for z,w in FIELD_WEIGHTS.items():
        key=str(z)
        X2 += float(w)*(means_2s[key]-2*means_s[key])/s**2
    L=A/mu[:,None]
    G=-2*X2-C2-A.T@np.diag(1/mu)@A
    return L,(G+G.T)/2


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--labels',type=int,default=2)
    parser.add_argument('--rho',default='1/2')
    parser.add_argument('--accuracy',default='1/10')
    parser.add_argument('--failure',default='1/20')
    parser.add_argument('--noise-bound',default='1')
    args=parser.parse_args()
    print(json.dumps(design(args.labels,Fraction(args.rho),Fraction(args.accuracy),
                            Fraction(args.failure),Fraction(args.noise_bound)),indent=2))


def reconstruct_exact(mu, C_s, C_2s, means_s, means_2s, s):
    """Exact rational reconstruction using SymPy matrices.

    Use this version, rather than floating reconstruct(), for the very small
    time steps in a certified schedule. Inputs may be rational empirical
    means after correction by a rational sensor confusion matrix. Confidence
    still requires the sampling/access assumptions in proof_note.md.
    """
    import sympy as sp
    mu=sp.Matrix(mu)
    k=mu.rows
    s=sp.Rational(s)
    if s<=0 or any(p<=0 for p in mu):
        raise ValueError('Positive time and estimated label masses required.')
    M=sp.diag(*mu)
    A=(sp.Matrix(C_s)-M)/s
    C2=(sp.Matrix(C_2s)-2*sp.Matrix(C_s)+M)/s**2
    X2=sp.zeros(k)
    for z,w in FIELD_WEIGHTS.items():
        weight=sp.Rational(w.numerator,w.denominator)
        key=str(z)
        X2 += weight*(sp.Matrix(means_2s[key])-2*sp.Matrix(means_s[key]))/s**2
    rawGamma=-2*X2-C2-A.T*M.inv()*A
    Gamma=(rawGamma+rawGamma.T)/2
    rawL=M.inv()*A
    L=sp.zeros(k)
    for a in range(k):
        for b in range(k):
            if a!=b: L[a,b]=max(sp.Rational(0),rawL[a,b])
        L[a,a]=-sum(L[a,b] for b in range(k) if a!=b)
    return L,Gamma
