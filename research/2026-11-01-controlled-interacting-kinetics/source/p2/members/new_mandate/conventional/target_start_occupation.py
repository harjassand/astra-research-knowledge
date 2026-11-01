"""Conventional mean hitting-time estimator with no rare waiting.

For a reversible chain with known stationary target weight and gap lower bound,
the Green-function diagonal is measured by starting ordinary microscopic paths
at the target and recording its occupation only for a mixing-scale duration.
No Gaussian propagation or perturbed-chain spectrum is used in sampling.
"""
import os
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
import json
import time
from pathlib import Path
import numpy as np
from scipy.special import expit


def occupation_paths(n,J,epsilon,T,samples,seed):
    """Exact uniformization; no discretization of the continuous-time chain."""
    rng=np.random.default_rng(seed)
    proposal_rate=(1+epsilon)*n
    creation=expit(-4*J)
    annihilation=1-creation
    occupied=[]
    proposals=0
    for _ in range(samples):
        count=rng.poisson(proposal_rate*T)
        proposals+=int(count)
        times=np.sort(rng.uniform(0,T,count))
        indices=rng.integers(0,n,count)
        uniforms=rng.uniform(0,1+epsilon,count)
        walls=0
        last=0.
        local_time=0.
        for event_time,ii,u in zip(times,indices,uniforms):
            i=int(ii);j=(i+1)%n;k=(i+2)%n
            if walls==0:
                local_time+=event_time-last
            x=(walls>>i)&1;y=(walls>>j)&1
            rate=creation if x+y==0 else annihilation if x+y==2 else .5
            rate*=1+epsilon*((walls>>k)&1)
            if u<rate:
                walls^=(1<<i)^(1<<j)
            last=event_time
        if walls==0:
            local_time+=T-last
        occupied.append(local_time)
    return np.array(occupied),proposals


def experiment(n,J=-.4,epsilon=.7,samples=1024,confidence=.95):
    start=time.perf_counter()
    # The perturbed dynamics preserve the same Gibbs law and dominate the
    # reference Dirichlet form.  Hence this reference gap is a lower bound.
    gap=2*(1-abs(np.tanh(2*J))*np.cos(np.pi/n))
    Lambda=2*(1+epsilon)*n
    r=np.exp(-2*J)
    logpi=-np.log(((1+r)**n+(1-r)**n)/2)
    pi=np.exp(logpi)
    bias_budget=.002
    T=np.log(Lambda/(gap*bias_budget))/gap
    values,proposals=occupation_paths(n,J,epsilon,T,samples,20261101+n)
    estimate=float(values.mean()-pi*T)
    rmax=pi*T*Lambda/(1-pi)
    # Exact Markov occupation moment identity gives Var(L_T)<=E[L_T]^2.
    # Since E[L_T]<=W+pi*T, Chebyshev supplies this finite-sample guarantee.
    statistical_relative=(1+rmax)/np.sqrt((1-confidence)*samples)
    relative_radius=statistical_relative+bias_budget
    denominator=pi*(1-pi)
    result=dict(n=n,epsilon=epsilon,samples=samples,confidence=confidence,
                pi_target=pi,gap_lower_bound=gap,spectral_upper_bound=Lambda,
                horizon=T,proposal_count=proposals,
                integrated_excess_estimate=estimate,
                empirical_standard_error=float(values.std(ddof=1)/np.sqrt(samples)),
                guaranteed_relative_radius=relative_radius,
                mean_estimate=estimate/denominator,
                mean_confidence_interval=[estimate/((1+relative_radius)*denominator),
                                          estimate/((1-relative_radius)*denominator)],
                seconds=time.perf_counter()-start)
    return result


if __name__=="__main__":
    results=dict(scope="ordinary exact uniformization; rigorous bias/variance formulas, floating-point parameter evaluation",
                 experiments=[experiment(n) for n in [32,64,256]])
    Path(__file__).with_name("target_start_results.json").write_text(json.dumps(results,indent=2))
    print(json.dumps(results,indent=2))
