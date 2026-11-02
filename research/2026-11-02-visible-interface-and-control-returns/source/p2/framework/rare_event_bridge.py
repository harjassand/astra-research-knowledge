#!/usr/bin/env python3
"""Noise-logged rare-event certification for unknown nonlinear drift.

Governing mathematical operation: stopped Girsanov change of measure, with a
pathwise cap obtained only from a physical one-sided drift bound. This is
established probability theory; its use as an experimental protocol is tested.

The learner receives: external Wiener innovations from digital noise drive,
actuator amplitude u, b<=B, terminal hit bit and its first hit time. It does NOT
receive b(x). The simulator uses b(x) only to generate observations.
"""
import json
from pathlib import Path
import numpy as np
from scipy.stats import beta

OUT=Path(__file__).parent
T=1.0;DT=.005;STEPS=int(T/DT)
SIGMA=.6; X0=0.; A=1.; B_UP=-.6
U=(A-X0-B_UP*T)/(SIGMA*T) # minimizes conservative hit cap for this regime
DELTA=.05

def hidden_drift(x):
    return -.8-.2*np.tanh(2*x)

def data(n,seed,u):
    rng=np.random.default_rng(seed)
    x=np.full(n,X0)
    hit=np.zeros(n,dtype=bool)
    lstop=np.zeros(n)
    tau=np.full(n,T)
    energy=np.zeros(n)
    for k in range(STEPS):
        live=~hit
        if not live.any(): break
        z=rng.normal(size=live.sum())
        idx=np.flatnonzero(live)
        x[idx]+=hidden_drift(x[idx])*DT+SIGMA*(u*DT+np.sqrt(DT)*z)
        lstop[idx]+= -u*np.sqrt(DT)*z-0.5*u*u*DT
        energy[idx]+=u*u*DT
        newly=x[idx]>=A
        if np.any(newly):
            hit[idx[newly]]=True
            tau[idx[newly]]=(k+1)*DT
    weights=np.exp(lstop)*hit
    return {'hit':hit,'weighted':weights,'energy':energy,'tau':tau,
            'max_success_weight':float(max(weights,default=0.))}

def empirical_bernstein_interval(x,lo,hi,delta):
    n=len(x)
    v=np.var(x,ddof=1)
    radius=np.sqrt(2*v*np.log(4/delta)/n)+7*(hi-lo)*np.log(4/delta)/(3*(n-1))
    return [max(lo,float(x.mean()-radius)),min(hi,float(x.mean()+radius))]

def cp_interval(hit,delta):
    n=len(hit); k=int(hit.sum())
    low=0. if k==0 else beta.ppf(delta/2,k,n-k+1)
    up=1. if k==n else beta.ppf(1-delta/2,k+1,n-k)
    return [float(low),float(up)]

def main():
    print('u selected from physical one-sided bound, not drift',U,flush=True)
    kappa=U*B_UP/SIGMA+.5*U*U
    K=float(np.exp(-U*(A-X0)/SIGMA+T*max(0,kappa)))
    print('certified success-weight cap K=',K,flush=True)
    records={}
    for n in [2000,10000,50000]:
        k=n+2026
        passiv=data(n,123456+k,0)
        biased=data(n,345678+k,U)
        assert biased['max_success_weight']<=K*(1+1e-9)
        pi=cp_interval(passiv['hit'],DELTA)
        wi=empirical_bernstein_interval(biased['weighted'],0,K,DELTA)
        pihat=float(passiv['hit'].mean());pw=float(biased['weighted'].mean())
        records[str(n)]={
            'passive':{'hits':int(passiv['hit'].sum()),'estimate':pihat,
                       'confidence_95pct':pi,'width':pi[1]-pi[0]},
            'active':{'hits':int(biased['hit'].sum()),'hit_fraction':float(biased['hit'].mean()),
                      'importance_estimate':pw,'confidence_95pct':wi,'width':wi[1]-wi[0],
                      'effective_success_weight_sample_size':float(biased['weighted'].sum()**2/(np.sum(biased['weighted']**2)+1e-50)),
                      'mean_energy_until_stop':float(biased['energy'].mean()),
                      'max_observed_weight':biased['max_success_weight']},
            'confidence_width_ratio_passive_to_active':(pi[1]-pi[0])/(wi[1]-wi[0])}
        print('n',n,records[str(n)],flush=True)
    truth=data(400000,555333,0)
    records['reference_large_passive']={'n':400000,'hit_frequency':float(truth['hit'].mean()),
                                        'cp95':cp_interval(truth['hit'],DELTA)}
    records['scenario']={'T':T,'dt':DT,'sigma':SIGMA,'x0':X0,'hit_threshold':A,
       'one_sided_global_upper_drift':B_UP,'injected_noise':'perfectly logged independent Gaussian increments',
       'selected_open_loop_u':U,'success_weight_upper_bound':K,
       'hidden_drift_for_checker_only':'-0.8-0.2*tanh(2*x)',
       'physical_scope':'unknown smooth bounded drift with b<=-0.6; exact discretized hitting event'}
    with open(OUT/'rare_event_results.json','w') as f:json.dump(records,f,indent=2)
if __name__=='__main__':main()
