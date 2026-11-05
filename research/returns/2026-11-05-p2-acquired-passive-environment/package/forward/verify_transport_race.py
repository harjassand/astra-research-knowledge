"""Reproduce finite checks of the adaptive transport-race construction.
No claim is inferred from Monte Carlo alone: identities are proved in the report.
"""
from __future__ import annotations
import json
import math
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from scipy.special import ndtr, expit

HERE = Path(__file__).resolve().parent


def flux_check(shift: float, delta: float, q: float, m: float = 3.0) -> dict:
    # Coordinates are x=-m+z and y=m+z under the two conditional samplers.
    normal = lambda z: math.exp(-z*z/2)/math.sqrt(2*math.pi)
    residual = shift-2*m
    logodds = math.log1p(-q)-math.log(q)
    def a_integrand(z):
        logr = -.5*(z+residual)**2+.5*z*z-delta
        return normal(z)*math.exp(min(0.,logodds+logr))
    def b_integrand(z):
        logr = -.5*z*z+.5*(z-residual)**2-delta
        return normal(z)*math.exp(min(0.,-logodds-logr))
    a,err_a=quad(a_integrand,-15.,15.,epsabs=1e-12,epsrel=1e-10,limit=300)
    b,err_b=quad(b_integrand,-15.,15.,epsabs=1e-12,epsrel=1e-10,limit=300)
    hazard=q*a+(1-q)*b
    p=q*a/hazard
    truth=float(expit(-delta))
    assert abs(p-truth)<2e-8, (shift,delta,q,p,truth)
    return dict(shift=shift,delta=delta,q=q,a=a,b=b,hazard=hazard,
                implied_p_B=p,true_p_B=truth,abs_error=abs(p-truth),
                quadrature_error_a=err_a,quadrature_error_b=err_b)


def run_race(seed: int, K: int, m: float, delta: float,
             adaptive_map: bool, adaptive_branch: bool) -> dict:
    rng=np.random.default_rng(seed)
    labels=np.empty(K,dtype=np.int8)
    counts=np.zeros(2,dtype=np.int64)
    means=np.zeros(2)
    accepted=0
    n_b=0
    attempts=0
    while accepted<K:
        # All adaptation is predictable: freeze before branch/source sample.
        shift=(means[1]-means[0]) if adaptive_map and counts.min()>0 else (0. if adaptive_map else 2*m)
        q=float(np.clip((n_b+1)/(accepted+2),.05,.95)) if adaptive_branch else .5
        source_a=rng.random()<q
        if source_a:
            x=float(rng.normal(-m,1.))
            y=x+shift
            logr=-.5*(y-m)**2-delta+.5*(x+m)**2
            logacc=min(0.,math.log1p(-q)-math.log(q)+logr)
            obs=x
            source=0
            label=1
        else:
            y=float(rng.normal(m,1.))
            x=y-shift
            logr=-.5*(y-m)**2-delta+.5*(x+m)**2
            logacc=min(0.,math.log(q)-math.log1p(-q)-logr)
            obs=y
            source=1
            label=0
        success=math.log(rng.random())<logacc
        # Only after the decision may the current observation train the map.
        counts[source]+=1
        means[source]+=(obs-means[source])/counts[source]
        attempts+=1
        if success:
            labels[accepted]=label
            accepted+=1
            n_b+=label
    p_hat=float(labels.mean())
    lag1=float(np.corrcoef(labels[:-1],labels[1:])[0,1])
    eps=math.sqrt(math.log(40)/(2*K))
    truth=float(expit(-delta))
    return dict(seed=seed,K=K,m=m,delta=delta,adaptive_map=adaptive_map,
                adaptive_branch=adaptive_branch,attempts=attempts,
                attempts_per_label=attempts/K,p_hat=p_hat,true_p_B=truth,
                lag_one_correlation=lag1,hoeffding_95_half_width=eps,
                truth_in_hoeffding_interval=abs(p_hat-truth)<=eps,
                final_phase_sample_counts=counts.tolist(),
                final_mean_estimates=means.tolist())


def phase_chain_check(seed: int = 512) -> dict:
    rng=np.random.default_rng(seed)
    k=9
    pi=rng.dirichlet(np.full(k,.3))
    P=np.zeros((k,k))
    for i in range(k):
        for j in range(k):
            if i!=j:
                P[i,j]=pi[j]/((k-1)*(pi[i]+pi[j]))
        P[i,i]=1-P[i].sum()
    min_slack=float(np.min(P-np.tile(pi,(k,1))/(k-1)))
    balance_err=float(np.max(np.abs(pi[:,None]*P-pi[None,:]*P.T)))
    stationary_err=float(np.max(np.abs(pi@P-pi)))
    assert min_slack>=-1e-14 and balance_err<1e-14 and stationary_err<1e-14
    return dict(k=k,pi=pi.tolist(),minimum_minorization_slack=min_slack,
                maximum_detailed_balance_error=balance_err,
                maximum_stationarity_error=stationary_err)


def main():
    flux=[flux_check(s,d,q) for s in (2.,4.5,6.,8.)
          for d in (-2.,0.,math.log(3.)) for q in (.1,.5,.9)]
    runs=[run_race(20261105,50000,6.,math.log(3.),False,False),
          run_race(20261105,50000,6.,math.log(3.),True,False),
          run_race(20261105,50000,6.,math.log(3.),True,True)]
    reps=[run_race(7000+i,5000,6.,math.log(3.),True,True) for i in range(20)]
    overlap=[dict(residual_mean_error=e,acceptance=float(2*ndtr(-e/2)),
                  expected_attempts_per_label=float(1/(2*ndtr(-e/2))))
             for e in (0.,1.,2.,4.,8.,12.)]
    out=dict(description='Finite falsification checks; proofs are in FORWARD_CONSTRUCTION.md',
             fixed_map_flux_checks=flux,
             maximum_flux_probability_error=max(r['abs_error'] for r in flux),
             main_runs=runs,replicate_runs=reps,
             replicate_summary=dict(count=len(reps),
                 mean_p_hat=float(np.mean([r['p_hat'] for r in reps])),
                 sd_p_hat=float(np.std([r['p_hat'] for r in reps],ddof=1)),
                 iid_binomial_sd=math.sqrt(.25*.75/5000),
                 covered_count=sum(r['truth_in_hoeffding_interval'] for r in reps)),
             balanced_gaussian_overlap=overlap,many_phase_check=phase_chain_check())
    (HERE/'verification_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('fixed_map_flux_checks','replicate_runs')},indent=2))

if __name__=='__main__':
    main()
