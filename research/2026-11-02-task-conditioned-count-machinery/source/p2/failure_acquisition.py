"""Source-paid failure discovery (not a full-generator oracle).

The learner samples the named-site terminal observable from actual local SSA
trajectories, rejects its previous anonymous-state prediction, and invokes
an output-compatibility refinement. Exact full-state evaluation is a SEPARATE
posthoc benchmark, not the learner's error signal.
"""
from __future__ import annotations
import json,math,time
from pathlib import Path
import numpy as np
from experiments import create_sis,discover,counts_initial,direct_full_one_site
from machinery import build_coarse, expm_distribution, state_to_counts

rng=np.random.default_rng(20261102)

def sample_ssa(m,x0,T,site):
    x=list(x0);t=0.;events=0;rate_evals=0
    while True:
        moves=[];rates=[]
        for j in range(m.n):
            s=x[j]
            for k in range(m.q):
                if k==s:continue
                r=float(m.unary[j,s,k])
                for i in range(m.n):
                    if i==j:continue
                    r+=float(m.pair[i,j,x[i],s,k])
                    rate_evals+=1
                if r>0:moves.append((j,k));rates.append(r)
        total=sum(rates)
        if total<=0:break
        jump=-math.log(float(rng.random()))/total
        if t+jump>T:break
        t+=jump
        u=float(rng.random())*total
        cum=0.;chosen=len(moves)-1
        for i,r in enumerate(rates):
            cum+=r
            if u<=cum:chosen=i;break
        j,k=moves[chosen];x[j]=k;events+=1
    return int(x[site]==1),events,rate_evals

def run():
    start=time.perf_counter();m,_=create_sis([4,3],rates=([.37,.29],[[.04,.015],[.012,.055]]))
    groups,_=discover(m)
    x0=[0]*m.n;x0[0]=1;T=2.8
    counts=state_to_counts(x0,groups,2)
    Q,states,idx,_=build_coarse(m,groups)
    p=np.zeros(len(states));p[idx[counts]]=1
    out=expm_distribution(Q,p,T)
    naive=float(sum(z[gi][1]/len(g)*prob for prob,z in zip(out,states)
                    for gi,g in enumerate(groups) if 0 in g))
    samples=512
    datum=[sample_ssa(m,x0,T,0) for _ in range(samples)]
    mean=sum(v[0] for v in datum)/samples
    halfwidth=math.sqrt(math.log(2/0.01)/(2*samples))
    assert not (mean-halfwidth<=naive<=mean+halfwidth)
    # Refinement triggered by observed failed prediction; output guard prescribes
    # the minimum informative site split, with physical source rate comparisons.
    refined,account=discover(m,forced=(0,))
    rcounts=state_to_counts(x0,refined,2)
    R,st,ri,_=build_coarse(m,refined)
    p=np.zeros(len(st));p[ri[rcounts]]=1
    pp=expm_distribution(R,p,T)
    gidx=next(g for g,v in enumerate(refined) if v==[0])
    pred=float(sum(w*c[gidx][1] for w,c in zip(pp,st)))
    truth=direct_full_one_site(m,x0,T,0) # posthoc comparator only
    return {'samples':samples,'simulated_episodes':samples,
            'simulated_reaction_events':sum(v[1] for v in datum),
            'local_native_pair_rate_accesses':sum(v[2] for v in datum),
            'terminal_readouts':samples,
            'confidence':0.99,'hoeffding_halfwidth':halfwidth,
            'observed_probability':mean,
            'observed_99pct_interval':[max(0,mean-halfwidth),min(1,mean+halfwidth)],
            'unrefined_prediction':naive,
            'unrefined_prediction_rejected_by_observations':True,
            'new_state_variables':refined,'refined_prediction':pred,
            'new_prediction_inside_observed_interval':abs(pred-mean)<=halfwidth,
            'posthoc_exact_full_state_prediction':truth,
            'posthoc_abs_error_after_refine':abs(pred-truth),
            'refinement_checks':account,
            'total_elapsed_sec':time.perf_counter()-start,
            'simulation_is_not_real_experimental_measurement':True}

if __name__=='__main__':
    r=run()
    Path(__file__).with_name('failure_acquisition_results.json').write_text(json.dumps(r,indent=2))
    print(json.dumps(r,indent=2))
