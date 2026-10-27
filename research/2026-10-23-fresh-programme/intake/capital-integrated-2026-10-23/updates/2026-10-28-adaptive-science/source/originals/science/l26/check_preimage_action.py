#!/usr/bin/env python3
"""Check the legal four-value preimage action, including source covariance."""
import json
import math
from pathlib import Path
import numpy as np


def check():
    rng=np.random.default_rng(47261)
    kappa,b,beta=.5,.5,.5
    a=math.sqrt(1-kappa*kappa)
    delta2=(1-beta)*(1-b*b)/2
    delta=math.sqrt(delta2)
    slope,amp,freq,offset=.2,.4,2.,2.3
    L=slope+amp
    count=400000
    calls=0
    def g(x):
        nonlocal calls
        calls+=1
        return offset+slope*x+amp*np.sin(freq*x)/freq
    def heat_action(c,v):
        r=delta*np.sqrt(np.sum(rng.normal(size=(count,3))**2,axis=1))
        return v*(g(c+r)-g(c-r))/(2*r)
    xx,ww=np.polynomial.legendre.leggauss(150)
    ts,ws=(xx+1)*b/2,ww/2
    def exact_r0(y):
        n11=1-ts*ts/(a*a)
        n22=1-b*b/(a*a)
        n12=-kappa*kappa*ts*b/(a*a)
        mu1,mu2=ts*y/a,b*y/a
        first=slope*slope+slope*amp*(np.exp(-freq*freq*n11/2)*np.cos(freq*mu1)+np.exp(-freq*freq*n22/2)*np.cos(freq*mu2))
        second=amp*amp/2*(np.exp(-freq*freq*(n11+n22+2*n12)/2)*np.cos(freq*(mu1+mu2))+np.exp(-freq*freq*(n11+n22-2*n12)/2)*np.cos(freq*(mu1-mu2)))
        return b*b*np.sum(ws*(first+second))-kappa*kappa
    errors=[]; query_counts=[]; maxnormratio=0.; covariance_error=0.
    for y,v in [(-.7,.4),(.2,-1.3),(.9,1.)]:
        seeds=rng.normal(size=(count,3))
        t=b*(1+seeds[:,0]/np.sqrt(np.sum(seeds*seeds,axis=1)))/2
        n11=1-t*t/(a*a); n22=1-b*b/(a*a)
        n12=-kappa*kappa*t*b/(a*a)
        c11=n11-delta2; c22=n22-delta2
        W1,W2=rng.normal(size=count),rng.normal(size=count)
        C1=np.sqrt(c11)*W1
        C2=n12/np.sqrt(c11)*W1+np.sqrt(c22-n12*n12/c11)*W2
        c1,c2=(t/a)*y+C1,(b/a)*y+C2
        swap=rng.normal(size=count)>0
        first=np.where(swap,c1,c2); second=np.where(swap,c2,c1)
        old=calls
        word=heat_action(second,heat_action(first,v))
        value=b*b*word-kappa*kappa*v
        query_counts.append(calls-old)
        target=exact_r0(y)*v
        errors.append(float(abs(np.mean(value)-target)))
        maxnormratio=max(maxnormratio,float(np.max(np.abs(value))/((b*b*L*L+kappa*kappa)*abs(v))))
        covariance_error=max(covariance_error,float(np.max(np.abs(n11+kappa*kappa*t*t/(a*a)-(1-t*t)))))
    tgrid=np.linspace(0,b,1001)
    minpadding=1.
    for t in tgrid:
        N=np.diag([1-t*t,1-b*b])-kappa*kappa/(a*a)*np.outer([t,b],[t,b])
        minpadding=min(minpadding,float(np.linalg.eigvalsh(N-delta2*np.eye(2))[0]))
    out={
        'kappa':kappa,'b':b,'beta':beta,'smoothing_condition_lhs':(kappa*kappa/(a*a))*2*b*b/(1-b*b),
        'residual_heat_smoothing_delta2':delta2,
        'sample_count_per_outer_point':count,
        'queries_per_action_per_execution':query_counts,
        'conditional_mean_absolute_errors':errors,
        'max_observed_norm_over_proved_bound':maxnormratio,
        'minimum_common_covariance_eigenvalue_grid':minpadding,
        'source_covariance_identity_max_error':covariance_error,
        'actual_input_g_Lip_bound':L,
        'full_mean_hb_is_not_acquired_by_this_test':True,
        'numerical_checks_are_not_TV_proofs':True,
    }
    assert all(q==4 for q in query_counts)
    assert max(errors)<.0005
    assert maxnormratio<=1+1e-12
    assert minpadding>0
    return out


if __name__=='__main__':
    result=check()
    (Path(__file__).resolve().parent/'preimage_checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
