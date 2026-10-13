"""Reproducible finite checks; none substitutes for the general proof.

Independent references: triangular moment ODE and, for small mark count,
finite partition CTMC matrix exponential. Floating numerical references are
not interval-certified. Fixed seed and input are recorded in JSON output.
"""
from __future__ import annotations
import argparse, json, time
from collections import deque
from math import exp, sqrt, pi, gamma
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp, simpson
from scipy.linalg import expm
from scipy.special import eval_genlaguerre, poch, gammaln
from scipy.stats import poisson, nbinom, binom
from collision_dual import (DiscreteVariance, terminal_blocks, laplace_sample,
                            density_sample, approximate_velocity, tv_bound)

SEED=20261013
A,B=1.,3.
INITIAL=DiscreteVariance((1.,3.),(.5,.5))


def moment_reference(times: list[float], degree: int=96):
    initial=np.full(degree+1,.5); initial[0]=1.
    k=np.arange(degree+1)
    def rhs(_t,m):
        result=np.convolve(m,m)[:degree+1]/(k+1)-m
        result[0]=result[1]=0.
        return result
    start=time.perf_counter()
    sol=solve_ivp(rhs,(0.,max(times)),initial,t_eval=times,
                  method='DOP853',rtol=2e-12,atol=2e-14)
    if not sol.success:
        raise RuntimeError(sol.message)
    return sol.y.T, time.perf_counter()-start, sol.nfev


def partition_distribution(n: int,t: float):
    start=(n,); states=[start]; lookup={start:0}; transitions=[]
    for state in states:
        row={}
        for i,k in enumerate(state):
            if k<2: continue
            for r in range(1,k):
                nxt=tuple(sorted(state[:i]+state[i+1:]+(r,k-r)))
                if nxt not in lookup:
                    lookup[nxt]=len(states); states.append(nxt)
                idx=lookup[nxt]
                row[idx]=row.get(idx,0.)+1/(k+1)
        transitions.append(row)
    q=np.zeros((len(states),len(states)))
    for i,row in enumerate(transitions):
        for j,rate in row.items(): q[i,j]+=rate
        q[i,i]=-sum(row.values())
    p=expm(t*q)[0]
    pmf=np.zeros(n+1)
    for weight,state in zip(p,states):
        poly=np.array([1.])
        for k in state:
            factor=np.zeros(k+1); factor[0]=factor[k]=.5
            poly=np.convolve(poly,factor)
        pmf+=weight*poly
    return pmf,len(states)


def main(output: Path):
    rng=np.random.default_rng(SEED)
    result={'seed':SEED,'model':{'a':A,'b':B,'values':[1.,3.],'weights':[.5,.5]},
            'status':'Floating-point finite diagnostics, not formal verification or priority clearance.'}
    times=[0.,1.,3.,10.,30.,100.]
    moments,elapsed,nfev=moment_reference(times)
    result['moment_reference']={'max_degree':96,'runtime_seconds':elapsed,'rhs_evaluations':nfev,
       'max_m2_closed_form_error':float(max(abs(moments[i,2]-(.25+.25*exp(-t/3))) for i,t in enumerate(times)))}
    rows=[]
    z=1.; repeats=24000
    for t,m in zip(times,moments):
        start=time.perf_counter()
        draws=np.array([laplace_sample(z,t,A,B,INITIAL,rng) for _ in range(repeats)])
        target=exp(-A*z)*float(poisson.pmf(np.arange(len(m)),(B-A)*z)@m)
        estimate=float(draws[:,0].mean()); se=float(draws[:,0].std(ddof=1)/sqrt(repeats))
        rows.append({'time':t,'z':z,'samples':repeats,'estimate':estimate,'reference':target,
            'standard_error':se,'standardized_error':(estimate-target)/se,
            'mean_poisson_degree':float(draws[:,1].mean()),'mean_splits':float(draws[:,2].mean()),
            'runtime_seconds':time.perf_counter()-start})
    result['laplace_checks']=rows
    # Independent finite partition-chain reference for actual sampling law.
    n=8; t=3.; pmf,count=partition_distribution(n,t)
    hist=np.zeros(n+1); repeats=32000
    start=time.perf_counter()
    for _ in range(repeats):
        _,variance,_,_=approximate_velocity(n,t,A,B,INITIAL,rng)
        hist[round((variance-A)*n/(B-A))]+=1
    empirical=hist/repeats
    result['partition_reference']={'n':n,'time':t,'partition_states':count,'samples':repeats,
        'pmf':pmf.tolist(),'empirical_pmf':empirical.tolist(),
        'empirical_TV_to_reference':float(abs(pmf-empirical).sum()/2),
        'runtime_seconds':time.perf_counter()-start}
    # End-to-end work and latent second-moment checks.
    rows=[]; n=64; repeats=3500
    for t in [0.,1.,3.,10.,100.,1e6]:
        start=time.perf_counter(); vals=[];splits=[]; nodes=[]
        for _ in range(repeats):
            _,variance,split,node=approximate_velocity(n,t,A,B,INITIAL,rng)
            vals.append(variance); splits.append(split); nodes.append(node)
        vals=np.array(vals)
        rows.append({'time':t,'n':n,'samples':repeats,'mean_variance_parameter':float(vals.mean()),
          'second_central_moment':float(np.mean((vals-2)**2)),
          'second_central_moment_reference':exp(-t/3)+(1-exp(-t/3))/n,
          'mean_splits':float(np.mean(splits)),'max_splits':max(splits),'max_nodes':max(nodes),
          'uniform_TV_bound':tv_bound(n,A,B),'runtime_seconds':time.perf_counter()-start})
    result['full_sampler_checks']=rows
    # Numerical full-law TV comparisons via exact small-n partition probabilities
    # and a deterministic Laguerre/moment reconstruction of the true PDE solution.
    radius=np.linspace(0.,14.,10001)
    r2=radius**2; x=r2/(2*B)
    base=(2*pi*B)**(-1.5)*np.exp(-x)
    lags=np.array([eval_genlaguerre(k,.5,x) for k in range(len(moments[0]))])
    true_index=2 # t=3
    weights=((B-A)/B)**np.arange(lags.shape[0])*moments[true_index]
    true_density=base*(weights@lags)
    spectail=.5*(B/A)**1.5*nbinom.sf(len(moments[0])-1,1.5,A/B)
    tvrows=[]
    for n in [1,2,4,8,16]:
        pmf,_=partition_distribution(n,3.)
        variances=A+(B-A)*np.arange(n+1)/n
        density=np.sum(pmf[:,None]*(2*pi*variances[:,None])**(-1.5)*np.exp(-r2[None,:]/(2*variances[:,None])),axis=0)
        tv=float(.5*simpson(4*pi*r2*abs(density-true_density),x=radius))
        tvrows.append({'time':3.,'n':n,'numerical_TV':tv,'proven_uniform_TV_bound':tv_bound(n,A,B),
          'proven_time_refined_TV_bound':sqrt(15/2)*(1-exp(-1))/(4*n)})
    result['full_law_TV_checks']={'note':'Radial quadrature and ODE errors are not interval certified.',
        'analytic_series_tail_L1_half_bound':float(spectail),'rows':tvrows}
    # Long-time law can be evaluated directly (all n blocks singleton).
    equilibrium=(2*pi*2)**(-1.5)*np.exp(-r2/4)
    rows=[]
    for n in [8,16,32,64,128,256]:
        variances=A+(B-A)*np.arange(n+1)/n
        p=binom.pmf(np.arange(n+1),n,.5)
        density=np.sum(p[:,None]*(2*pi*variances[:,None])**(-1.5)*np.exp(-r2[None,:]/(2*variances[:,None])),axis=0)
        tv=float(.5*simpson(4*pi*r2*abs(density-equilibrium),x=radius))
        rows.append({'n':n,'numerical_TV_at_infinity':tv,'uniform_TV_bound':tv_bound(n,A,B)})
    result['equilibrium_full_law_checks']=rows
    # Density observable oracle: bounded signed output, no inversion grid needed.
    rows=[]; t=3.;repeats=28000
    for radius_value in [0.,2.]:
        v=np.array([radius_value,0.,0.]); samples=[];degrees=[]
        for _ in range(repeats):
            value,degree,_=density_sample(v,t,A,B,INITIAL,rng);samples.append(value);degrees.append(degree)
        x0=radius_value**2/(2*B)
        reference=float((2*pi*B)**(-1.5)*exp(-x0)*sum(
          eval_genlaguerre(k,.5,x0)*((B-A)/B)**k*moments[true_index,k] for k in range(len(moments[0]))))
        samples=np.array(samples); se=float(samples.std(ddof=1)/sqrt(repeats))
        rows.append({'time':t,'radius':radius_value,'samples':repeats,'estimate':float(samples.mean()),
          'reference':reference,'standard_error':se,'standardized_error':float((samples.mean()-reference)/se),
          'mean_degree':float(np.mean(degrees))})
    result['density_checks']=rows
    # Negative control: replacing every mark by an independent initial sample at t=0.
    result['negative_control']={'n':64,'time':0.,'correct_latent_variance':1.,
          'incorrect_independent_marks_latent_variance':1/64,
          'explanation':'Shared ancestry cannot be replaced by independent marks.'}
    output.write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=Path('results.json'))
    main(p.parse_args().output)
