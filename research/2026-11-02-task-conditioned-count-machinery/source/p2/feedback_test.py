"""Native-rule closed-loop feedback application of retained count machinery.

A policy observes the global count of infected sites and temporarily increases
recoveries in one cohort. Both micro and macro generators implement the SAME
state-dependent policy. This is not an experiment on a physical instrument.
"""
from __future__ import annotations
import json, math, time
from itertools import product
from pathlib import Path
import numpy as np
from scipy.sparse import csr_matrix
from experiments import create_sis,discover,counts_initial,distributed_hetero
from machinery import (full_generator,build_coarse,uniform_initial_micro,expm_distribution,
                       deviations,quadratic_certificate,observable_extinct,observable_full_extinct)

def feedback_generator_full(m,groups,focus,trigger,boost):
    n,q=m.n,m.q
    assert q==2
    Q,states,index=full_generator(m)
    R=Q.tolil()
    for i,x in enumerate(states):
        if sum(v==1 for v in x)<trigger:continue
        for j in groups[focus]:
            if x[j]!=1:continue
            y=list(x);y[j]=0
            R[i,index[tuple(y)]]+=boost
            R[i,i]-=boost
    return R.tocsr(),states,index

def feedback_generator_coarse(m,groups,focus,trigger,boost):
    Q,states,index,_=build_coarse(m,groups)
    R=Q.tolil()
    for i,c in enumerate(states):
        if sum(v[1] for v in c)<trigger:continue
        k=c[focus][1]
        if not k:continue
        y=[list(v) for v in c];y[focus][1]-=1;y[focus][0]+=1
        j=index[tuple(map(tuple,y))]
        R[i,j]+=k*boost
        R[i,i]-=k*boost
    return R.tocsr(),states,index

def run():
    model,_=create_sis([3,3,2],rates=([.32,.37,.26],[[.039,.021,0],[.011,.047,.015],[0,.014,.05]]))
    groups,_=discover(model)
    m=distributed_hetero(model,groups,0.0057)
    counts,_=counts_initial(groups,2,[0,3,6]);T=2.4
    eta=deviations(m,groups)['eta_upper']
    out=[]
    for threshold in [1,3,5,7,8]:
        for boost in [0.00,0.06,0.12]:
            fq,fs,fi=feedback_generator_full(m,groups,0,threshold,boost)
            cq,cs,ci=feedback_generator_coarse(m,groups,0,threshold,boost)
            p0=uniform_initial_micro(counts,groups,2,fi)
            c0=np.zeros(len(cs));c0[ci[counts]]=1
            pred=float(expm_distribution(cq,c0,T)@observable_extinct(cs))
            true=float(expm_distribution(fq,p0,T)@observable_full_extinct(fs))
            b=quadratic_certificate(eta,T)
            assert abs(true-pred)<b+1e-11,(threshold,boost,true,pred,b)
            out.append({'trigger':threshold,'boost':boost,'predicted':pred,'exact':true,
                        'error':abs(true-pred),'certified_upper':b,
                        'full_states':len(fs),'coarse_states':len(cs)})
    obj={'cases':out,'max_observed_error':max(x['error'] for x in out),
         'theorem_error_upper':quadratic_certificate(eta,T),
         'source_interface':'Full observed count at each jump and symmetric feedback actuation; only simulated here',
         'old_compiler_reused_without_relearning_source_groups':True}
    Path(__file__).with_name('feedback_results.json').write_text(json.dumps(obj,indent=2))
    print('feedback cases',len(out),'maxerror',obj['max_observed_error'],'bound',obj['theorem_error_upper'])
    print('threshold 1 policies',[(r['boost'],r['exact'],r['predicted']) for r in out if r['trigger']==1])

if __name__=='__main__':run()
