"""Rare collective hitting from compact return kernels.

This is an explicit, independently derived baseline/construction, not a claim
of priority. No sampled transition, coarse reaction coordinate, or fitted rate
is used. Time is in units of the microscopic rates supplied as input.

For independent two-state coordinates, the target is all coordinates equal 1.
The initial law is equilibrium conditioned outside the target. The extension
has flip rate multiplier 1 + epsilon*(2*x[left_neighbor]-1), preserving the
product equilibrium distribution but introducing kinetic interactions.

Run: python3 new_mandate/independent/return_kernel.py
"""
import json
import math
import time
from pathlib import Path

import numpy as np
from scipy.integrate import quad
from scipy.linalg import solve


def return_excess(t, p, lam):
    """P_bb(t)-pi_b, evaluated without subtracting nearly equal products."""
    p = np.asarray(p, dtype=float)
    lam = np.asarray(lam, dtype=float)
    logpi = np.log(p).sum()
    boost = np.log1p(((1-p)/p)*np.exp(-lam*t)).sum()
    if boost > 50:
        return float(np.exp(logpi+boost) * (-np.expm1(-boost)))
    return float(np.exp(logpi)*np.expm1(boost))


def compact_mean(p, lam, reltol=1e-10):
    p, lam = np.asarray(p, float), np.asarray(lam, float)
    logpi = np.log(p).sum()
    pi = float(np.exp(logpi))
    low = (1-pi)/lam.sum()  # rigorous lower bound on return-excess integral
    cutoff = math.log(lam.sum()/(reltol*lam.min()))/lam.min()
    value, estimate = quad(lambda t: return_excess(t,p,lam), 0, cutoff,
                           epsabs=reltol*low/10, epsrel=reltol/10, limit=250)
    tail_bound = (1-pi)*math.exp(-lam.min()*cutoff)/lam.min()
    # quad's estimate is a numerical error estimate, not interval arithmetic.
    log_mean = math.log(value)-logpi-math.log1p(-pi)
    return {"normalized_mean":value,"log_mean":log_mean,
            "mean":math.exp(log_mean) if log_mean < 700 else None,
            "log10_mean":log_mean/math.log(10),"log10_target_probability":logpi/math.log(10),
            "quadrature_error_estimate":estimate,"tail_bound":tail_bound,
            "cutoff":cutoff,"pi":pi}


def compact_laplace(s,p,lam,reltol=1e-10):
    """Positive-real Laplace transform of the complete first hitting law."""
    p,lam=np.asarray(p,float),np.asarray(lam,float)
    pi=float(np.exp(np.log(p).sum()))
    cutoff=math.log(lam.sum()/(reltol*lam.min()))/lam.min()
    R,_=quad(lambda t: np.exp(-s*t)*return_excess(t,p,lam),0,cutoff,
             epsabs=reltol*(1-pi)/lam.sum()/10,epsrel=reltol/10,limit=250)
    return float((1/(1+s*R/pi)-pi)/(1-pi))


def first_order_correction(p,lam,reltol=1e-10):
    """Normalized coefficient C in M(eps)= (R0-eps*C+...)/(pi*(1-pi)).

    A two-time perturbation integral reduces analytically to one dimension.
    The remaining product and neighbor sum cost O(n) per quadrature node.
    """
    p,lam=np.asarray(p,float),np.asarray(lam,float)
    n=len(p)
    if n < 3:
        raise ValueError("Use at least 3 coordinates for distinct cyclic neighbors")
    cutoff=math.log(100*n/(reltol*lam.min()))/lam.min()

    def integrand(v):
        e=np.exp(-lam*v)
        r=p+(1-p)*e
        product=float(np.exp(np.log(r).sum()))
        ell=(1-p)*lam*e
        zbar=v*(p*(2*p-1)+(1-p)*(1-2*p)*e) + 4*p*(1-p)*(-np.expm1(-lam*v))/lam
        return float(product*np.sum(ell*np.roll(zbar,1)/(r*np.roll(r,1))))

    value,estimate=quad(integrand,0,cutoff,epsabs=reltol/lam.sum()/10,
                        epsrel=reltol/10,limit=250)
    return value,estimate


def dense_generator(p,lam,epsilon):
    p,lam=np.asarray(p,float),np.asarray(lam,float)
    n=len(p); N=1<<n
    Q=np.zeros((N,N))
    pi=np.empty(N)
    for x in range(N):
        bits=np.array([(x>>i)&1 for i in range(n)])
        pi[x]=np.prod(np.where(bits,p,1-p))
        for i in range(n):
            neighbor=bits[(i-1)%n]
            factor=1+epsilon*(2*neighbor-1)
            rate=lam[i]*(1-p[i] if bits[i] else p[i])*factor
            Q[x,x^(1<<i)]=rate
            Q[x,x]-=rate
    return Q,pi


def dense_mean(p,lam,epsilon):
    Q,pi=dense_generator(p,lam,epsilon)
    target=len(pi)-1
    h=solve(-Q[:target,:target],np.ones(target),assume_a="gen")
    return float(pi[:target]@h/(1-pi[target]))


def main():
    t0=time.perf_counter()
    tests=[]
    for n in (3,5,8):
        p=np.linspace(.22,.35,n);lam=np.linspace(.8,1.7,n)
        base=compact_mean(p,lam)
        C,Cerr=first_order_correction(p,lam)
        m0=base["mean"]
        dense0=dense_mean(p,lam,0)
        assert abs(dense0/m0-1)<3e-9,(n,dense0,m0)
        for eps in (-.4,-.15,.15,.4,.8):
            exact=dense_mean(p,lam,eps)
            lower=m0*(1-eps*C/base["normalized_mean"])
            upper=lower+eps*eps/(1-abs(eps))*m0
            assert lower-1e-7*m0 <= exact <= upper+1e-7*m0,(n,eps,lower,exact,upper)
            tests.append({"n":n,"epsilon":eps,"exact_dense_mean":exact,
                          "base_mean":m0,"first_order_lower":lower,
                          "first_order_upper":upper,
                          "exact_over_base":exact/m0,
                          "first_order_over_base":lower/m0,
                          "quadrature_coefficient_error_estimate":Cerr})

    n=128;p=np.full(n,.1);lam=np.linspace(1,2,n)
    start=time.perf_counter()
    base=compact_mean(p,lam)
    C,Cerr=first_order_correction(p,lam)
    eps=.2
    ratio_lower=1-eps*C/base["normalized_mean"]
    ratio_upper=ratio_lower+eps*eps/(1-abs(eps))
    laplace=[{"s_times_mean":u,"value":compact_laplace(u/base["mean"],p,lam),
              "exponential_limit":1/(1+u)} for u in (.1,1,10)]
    large={"n":n,"microscopic_states":str(1<<n),"epsilon":eps,
           "independent":base,"interacting_mean_lower_over_independent":ratio_lower,
           "interacting_mean_upper_over_independent":ratio_upper,
           "correction_C":C,"coefficient_quadrature_error_estimate":Cerr,
           "positive_real_laplace":laplace,"runtime_seconds":time.perf_counter()-start}
    results={"small_dense_checks":tests,"large_compact_construction":large,
             "all_tests_pass":True,"runtime_seconds":time.perf_counter()-t0,
             "qualification":"Dense checks verify formulas; scipy quadrature is not rigorous interval arithmetic. Analytic truncation and operator bounds are rigorous under stated assumptions."
             }
    out=Path(__file__).with_name("return_kernel_results.json")
    out.write_text(json.dumps(results,indent=2)+"\n")
    print(json.dumps({"all_tests_pass":True,"dense_checks":len(tests),"large":large,
                      "results_path":str(out)},indent=2))


if __name__=="__main__":
    main()
