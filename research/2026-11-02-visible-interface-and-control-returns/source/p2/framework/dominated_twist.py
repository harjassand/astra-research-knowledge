#!/usr/bin/env python3
"""Exact finite-step robust noise-twisting experiment with unknown drift.

Physics contract (observable only): S_{k+1}=S_k + beta_k dt + sigma sqrt(dt) Z_k,
with arbitrary hidden/path-dependent beta_k <= B. The externally programmed noise
Z_k has baseline N(0,1), and the laboratory can generate and log samples from
our specified adaptive *non-Gaussian* proposal q_k(z|S_k).

H_k(s) = 1 + C Phi((s+B(T-t_k)-c)/sqrt(sigma^2(T-t_k)+eta^2))
F(s)=1+C Phi((s-c)/eta)
q_k(z|s)=normal(z) H_{k+1}(s+Bdt+sigma sqrt(dt) z)/H_k(s)

It is normalized exactly; the sampler below uses a mixture of an ordinary N(0,1)
and the first coordinate of a Gaussian conditioned on a noisy terminal threshold.

For each trajectory the baseline likelihood L satisfies L F(S_T)<= H_0(S_0)
PATHWISE whenever beta_k <= B, by telescoping and monotonicity of H. Hence
L 1{S_T>=a} <= H_0(S_0)/F(a). This yields exact bounded-iid Hoeffding and
empirical-Bernstein certification. All weights computed without hidden drift.

Existing stochastic control / importance sampling machinery is not new.
"""
import json
from pathlib import Path
import numpy as np
from scipy.special import ndtr, ndtri
from scipy.stats import norm, beta

OUT=Path(__file__).parent
T=1.;DT=.005;STEPS=int(T/DT)
SIGMA=.6; S0=0.; A=1.; B=-.6
ETA=.05;CENTER=A-.08;C=500.0
U_GAUSS=(A-S0-B*T)/(SIGMA*T)
DELTA=.05

def hidden_drift(s):
    return -.8-.2*np.tanh(2*s)

def h(k,s):
    remain=T-k*DT
    return 1+C*ndtr((s+B*remain-CENTER)/np.sqrt(SIGMA**2*remain+ETA**2))

def sample_biased_noise(rng,s,k):
    """Exact sampling of q_k using a two-component Gaussian mixture."""
    rem=T-k*DT
    variance=SIGMA**2*rem+ETA**2
    std=np.sqrt(variance)
    cdf_success=ndtr((s+B*rem-CENTER)/std)
    hk=1+C*cdf_success
    biased_branch=rng.random(len(s))<(C*cdf_success/hk)
    z=rng.normal(size=len(s))
    count=int(biased_branch.sum())
    if count:
        s_b=s[biased_branch]
        threshold=(CENTER-s_b-B*rem)/std
        # Draw Z_Y conditioned to exceed threshold in a bivariate normal.
        surv=norm.sf(threshold)
        p=surv*rng.random(count)
        # sf numbers remain normal under this scenario; use isf for tail stability.
        zy=norm.isf(np.maximum(p,np.finfo(float).tiny))
        rho=SIGMA*np.sqrt(DT)/std
        z[biased_branch]=rho*zy+np.sqrt(1-rho**2)*rng.normal(size=count)
    return z

def sim(n,seed,proposal='baseline'):
    rng=np.random.default_rng(seed)
    s=np.full(n,S0)
    logL=np.zeros(n)
    for k in range(STEPS):
        if proposal=='twist':
            z=sample_biased_noise(rng,s,k)
            # Compute q density ratio from exact H; no unknown drift.
            nominal=s+B*DT+SIGMA*np.sqrt(DT)*z
            logL+=np.log(h(k,s))-np.log(h(k+1,nominal))
        elif proposal=='gaussian':
            z=rng.normal(size=n)+U_GAUSS*np.sqrt(DT)
            # Under controlled Gaussian shift, baseline proposal weight.
            w=z-U_GAUSS*np.sqrt(DT)
            logL+= -U_GAUSS*np.sqrt(DT)*w-0.5*U_GAUSS**2*DT
        else:
            z=rng.normal(size=n)
        s+=hidden_drift(s)*DT+SIGMA*np.sqrt(DT)*z
    event=s>=A
    weight=np.exp(logL)*event
    return {'event':event,'Y':weight,'logL':logL,'final_s':s}

def cp95(hit):
    n=len(hit);k=int(hit.sum())
    return [0. if k==0 else float(beta.ppf(DELTA/2,k,n-k+1)),
            1. if k==n else float(beta.ppf(1-DELTA/2,k+1,n-k))]

def eb95(y,K):
    n=len(y); v=float(y.var(ddof=1)); log=np.log(4/DELTA)
    rad=np.sqrt(2*v*log/n)+7*K*log/(3*(n-1))
    return [max(0,float(y.mean()-rad)),float(y.mean()+rad)]

def hoeff95(y,K):
    n=len(y);rad=K*np.sqrt(np.log(2/DELTA)/(2*n))
    return [max(0,float(y.mean()-rad)),float(y.mean()+rad)]

def main():
    K_twist=float(h(0,np.array([S0]))[0]/h(STEPS,np.array([A]))[0])
    K_gauss=float(np.exp(-U_GAUSS*(A-S0)/SIGMA+(U_GAUSS*B/SIGMA+.5*U_GAUSS**2)*T))
    assert np.isfinite(K_twist)
    print('derived pathwise caps: twist',K_twist,'shift',K_gauss,flush=True)
    records={}
    for n in [2000,10000,50000]:
        bs=sim(n,198081+n,'baseline')
        tw=sim(n,198091+n,'twist')
        ga=sim(n,198101+n,'gaussian')
        assert tw['Y'].max()<=K_twist*(1+1e-8),('twist cap fail',tw['Y'].max(),K_twist)
        assert ga['Y'].max()<=K_gauss*(1+1e-8),('shift cap fail',ga['Y'].max(),K_gauss)
        rec={'passive':{'hits':int(bs['event'].sum()),'p_estimate':float(bs['event'].mean()),
                        'cp_95':cp95(bs['event'])}}
        rec['passive']['width']=rec['passive']['cp_95'][1]-rec['passive']['cp_95'][0]
        for name,v,cap in [('twist',tw,K_twist),('gaussian_shift',ga,K_gauss)]:
            ci=eb95(v['Y'],cap);chi=hoeff95(v['Y'],cap)
            rec[name]={'success_count':int(v['event'].sum()),
                'success_rate_under_proposal':float(v['event'].mean()),
                'weighted_event_estimate':float(v['Y'].mean()),'ci_95_eb':ci,
                'ci_95_hoeff':chi,'ci_95_width_eb':ci[1]-ci[0],
                'observed_max_weight':float(v['Y'].max()),
                'pathwise_certified_bound':cap,'mean_proposal_kl_est':float(-v['logL'].mean()),
                'weight_effective_n':float(v['Y'].sum()**2/(np.sum(v['Y']**2)+1e-50))}
            rec[f'passive_to_{name}_width_ratio']=rec['passive']['width']/(ci[1]-ci[0])
        records[str(n)]=rec
        print('n=',n,rec,flush=True)
    records['scenario']={'drift_bound':B,'T':T,'dt':DT,'sigma':SIGMA,'x0':S0,'target_threshold':A,
       'c':CENTER,'eta':ETA,'C':C,'gaussian_u':U_GAUSS,
       'twist_weight_bound':K_twist,'gaussian_weight_bound':K_gauss,
       'hidden_drift_for_checker_only':'-.8-.2*tanh(2*x)',
       'noise_access':'programmable independent Gaussian and conditional Gaussian innovation samples, accurately logged',
       'finite_step_identity':'exact for Euler-Markov input channel; no continuum discretization bound assumed'}
    with open(OUT/'dominated_twist_results.json','w') as f:json.dump(records,f,indent=2)

if __name__=='__main__':main()
