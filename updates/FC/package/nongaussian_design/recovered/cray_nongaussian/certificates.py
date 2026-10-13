"""Local-label free-energy certificates with arbitrary interacting surroundings.

The inequalities proved in RESEARCH_NOTE.md are rigorous. General routines here
use double precision and are diagnostics, not outward-rounded certificates.
The separate exact_fixture.py verifies a sign decision with rational arithmetic.
"""
from __future__ import annotations
import numpy as np
from scipy.linalg import eigh, expm
from scipy.optimize import linprog
from scipy.special import logsumexp


def thermal_statistics(H: np.ndarray, beta: float, labels: np.ndarray, k: int):
    if beta <= 0: raise ValueError('beta must be positive')
    E, U = eigh(H, check_finite=True)
    ell = -beta * (E - E[0]); logz = logsumexp(ell)
    diagonal = (np.abs(U)**2) @ np.exp(ell-logz)
    p = np.bincount(labels, weights=diagonal, minlength=k)
    return float(E[0]-logz/beta), p


def coherence_budget(graph: np.ndarray, beta: float) -> tuple[float,float]:
    g=np.asarray(graph,dtype=float)
    if beta<=0 or np.any(g<0) or not np.allclose(g,g.T) or not np.allclose(np.diag(g),0):
        raise ValueError('positive beta and symmetric nonnegative zero-diagonal graph required')
    C=max(1.0,float(np.max(np.diag(expm(beta*g)))))
    return C,1.0-1.0/C


def histogram_interval(p: np.ndarray, shifts: np.ndarray, beta: float, C: float):
    """One histogram; keep mass 1/C with least reweighting. Costs O(k log k)."""
    p=np.asarray(p,dtype=float); v=np.asarray(shifts,dtype=float)
    if p.shape!=v.shape or beta<=0 or C<1 or np.any(p<0) or abs(p.sum()-1)>1e-8:
        raise ValueError('invalid arguments')
    vmin=float(v.min()); logu=-beta*(v-vmin)
    keep=np.zeros_like(p); mass=1.0/C
    for i in np.argsort(logu):
        take=min(float(p[i]),mass); keep[i]=take; mass-=take
        if mass<=0: break
    if mass>1e-10: raise ArithmeticError('could not allocate retained probability')
    lu=logsumexp(logu,b=p); ll=logsumexp(logu,b=keep)
    # Intersect with the exact min/max perturbation bound; important for constants.
    return max(vmin,vmin-lu/beta),min(float(v.max()),vmin-ll/beta)


def confidence_interval(phat: np.ndarray, error: float, shifts: np.ndarray,
                        beta: float, C: float):
    """Optimize over simultaneous per-bin confidence intervals; numerical LP."""
    p=np.asarray(phat,dtype=float); v=np.asarray(shifts,dtype=float); k=len(p)
    if error<0 or beta<=0 or C<1 or p.shape!=v.shape: raise ValueError('invalid inputs')
    vmin=float(v.min()); u=np.exp(-beta*(v-vmin))
    lb=np.maximum(0,p-error); ub=np.minimum(1,p+error)
    if lb.sum()>1 or ub.sum()<1: raise ValueError('inconsistent probability box')
    upper=linprog(-u,A_eq=np.ones((1,k)),b_eq=[1],bounds=list(zip(lb,ub)),method='highs')
    # variables: p then w. 0<=w<=p, sum(p)=1, sum(w)>=1/C.
    A=np.zeros((k+1,2*k)); A[:k,:k]=-np.eye(k); A[:k,k:]=np.eye(k); A[k,k:]=-1
    b=np.r_[np.zeros(k),-1/C]; eq=np.zeros((1,2*k)); eq[0,:k]=1
    lower=linprog(np.r_[np.zeros(k),u],A_ub=A,b_ub=b,A_eq=eq,b_eq=[1],
                  bounds=list(zip(lb,ub))+[(0,None)]*k,method='highs')
    if not (upper.success and lower.success): raise ArithmeticError('LP failure')
    if lower.fun<=0: return max(vmin,vmin-np.log(-upper.fun)/beta),float(v.max())
    return max(vmin,vmin-np.log(-upper.fun)/beta),min(float(v.max()),vmin-np.log(lower.fun)/beta)


def conditional_pair_interval(p: np.ndarray, C: float):
    """Dimensionless conditional pair free energy beta*(f00+f11-f01-f10).

    Uses the necessary polytope q_i<=C*p_i, sum(q)=1. Bounds are exact for
    this outer polytope, not claimed optimal over compatible quantum baths.
    Ordering is [00,01,10,11].
    """
    u=np.minimum(1,C*np.asarray(p,dtype=float))
    def max_odds(a,b,c,d):
        if u[a]+u[b]>=1: return float('inf')
        rem=1-u[a]-u[b]; left=max(0,rem-u[d]); right=min(u[c],rem)
        den=min(left*(rem-left),right*(rem-right))
        return float('inf') if den<=0 else u[a]*u[b]/den
    rmax=max_odds(0,3,1,2); inverse_rmin=max_odds(1,2,0,3)
    return -np.log(rmax),np.log(inverse_rmin)
