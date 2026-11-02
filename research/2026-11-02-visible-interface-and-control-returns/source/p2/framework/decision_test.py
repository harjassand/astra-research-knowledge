#!/usr/bin/env python3
"""Two-physical-intervention risk ranking from rare-event experiments.

Both arms share the SAME known global upper drift B and the SAME adaptive
noise-conditioning H, q. Hidden source responses differ but neither response
formula enters the sampler or likelihood. Independent arm samples and Bonferroni
confidence establish the ordering when the two intervals do not overlap.
"""
from pathlib import Path
import numpy as np, json
from scipy.stats import beta
import dominated_twist as d
OUT=Path(__file__).parent
N=25000
DELTA_PER_ARM=.025

def experiment(offset,n,seed,twist):
    rng=np.random.default_rng(seed); s=np.full(n,d.S0); logL=np.zeros(n)
    for k in range(d.STEPS):
        if twist:
            z=d.sample_biased_noise(rng,s,k)
            logL+=np.log(d.h(k,s))-np.log(d.h(k+1,s+d.B*d.DT+d.SIGMA*np.sqrt(d.DT)*z))
        else:
            z=rng.normal(size=n)
        # This exact hidden numerical drift is known only to the simulator.
        s+=(d.hidden_drift(s)-offset)*d.DT+d.SIGMA*np.sqrt(d.DT)*z
    ev=s>=d.A
    return ev,np.exp(logL)*ev

def bern_ci(y,cap,delta):
    n=len(y);v=float(y.var(ddof=1));rad=np.sqrt(2*v*np.log(4/delta)/n)+7*cap*np.log(4/delta)/(3*(n-1))
    return [float(max(0,y.mean()-rad)),float(y.mean()+rad)]

def cp_ci(ev,delta):
    k=int(ev.sum());n=len(ev)
    return [0. if k==0 else float(beta.ppf(delta/2,k,n-k+1)),1. if k==n else float(beta.ppf(1-delta/2,k+1,n-k))]

def main():
    R={};cap=float(d.h(0,np.array([d.S0]))[0]/d.h(d.STEPS,np.array([d.A]))[0])
    for key,offset,seed in [('untreated',0.,33101),('mitigation',.08,77315)]:
        ev,y=experiment(offset,N,seed,True)
        p_ev,_=experiment(offset,N,seed+5000,False)
        assert np.max(y)<=cap*(1+1e-9)
        R[key]={'hidden_drift_for_checker_only':f'-.8-.2*tanh(2*s)-{offset}',
               'same_proven_upper_drift_B':d.B,
               'n_active':N,'n_passive':N,'active_success_count':int(ev.sum()),
               'active_weighted_p':float(y.mean()),'active_97_5pct_CI':bern_ci(y,cap,DELTA_PER_ARM),
               'passive_success_count':int(p_ev.sum()),'passive_p':float(p_ev.mean()),
               'passive_97_5pct_CI':cp_ci(p_ev,DELTA_PER_ARM)}
    r1,r2=R['untreated'],R['mitigation']
    R['decisions']={
       '95pct_joint_active_guarantees_mitigation_lower_risk':r2['active_97_5pct_CI'][1]<r1['active_97_5pct_CI'][0],
       '95pct_joint_passive_guarantees_mitigation_lower_risk':r2['passive_97_5pct_CI'][1]<r1['passive_97_5pct_CI'][0],
       'familywise_delta':.05,
       'common_known_upper_drift':d.B,
       'known_intervention_effect_size_to_learner':False,
       'no_adaptive_arm_selection_or_tuning_on_eval_data':True}
    (OUT/'decision_results.json').write_text(json.dumps(R,indent=2)+'\n')
    print(json.dumps(R,indent=2))

if __name__=='__main__':main()
