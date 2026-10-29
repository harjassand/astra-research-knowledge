#!/usr/bin/env python3
"""Synthetic binomial-count check; each grouped draw charges m native trials.
No physical source, return operation, or apparatus acquisition is executed.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib,json
import numpy as np

ROOT=Path(__file__).resolve().parent

def ceilf(q):return (q.numerator+q.denominator-1)//q.denominator

def ceil_log2(q):
    out=0;p=F(1)
    while p<q:p*=2;out+=1
    return out

def schedule(v,delta):
    L=ceil_log2(8/v);s=ceil_log2(2/delta);b=ceil_log2(128/v)
    levels=[]
    for l in range(1,L+1):
        t=F(1,2**l);n=ceilf(128*s*t/v);m=ceilf(8*b/t)
        levels.append((l,t,n,m))
    D=sum(n for _,_,n,_ in levels);N=sum(n*m for _,_,n,m in levels)
    bound=F(1024*L*s*b+128*s+256*b)/v+L
    assert N<=bound
    assert D<=128*s/v+L
    assert F(1,2**L)<=v/8
    # exp(-s)<=2^-s and exp(-b)<=2^-b make failure allocation exact.
    assert F(2,2**s)<=delta
    assert F(2,2**b)<=v/64
    return levels,{'L':L,'s_integer_upper':s,'b_integer_upper':b,
                   'independent_specimens':D,'returned_trials':N,'upper_call_bound':str(bound)}

def simulate(v,delta,name,probabilities,masses,trueV,seed):
    levels,resource=schedule(v,delta)
    assert sum(masses)==1
    assert sum(w*(p-F(1,2))**2 for w,p in zip(masses,probabilities))==trueV
    rng=np.random.default_rng(seed);Q=F(0);rows=[]
    for l,t,n,m in levels:
        idx=rng.choice(len(probabilities),size=n,p=np.array(masses,dtype=float))
        ps=np.array(probabilities,dtype=float)[idx]
        counts=rng.binomial(m,ps)
        # Exact integer equivalent of |count/m-1/2| >3sqrt(t)/4.
        assert 4*(2**l)*m*m<np.iinfo(np.int64).max
        flags=4*(2**l)*(2*counts-m)**2>9*m*m
        count=int(np.count_nonzero(flags));Q+=t*F(count,n)
        rows.append({'l':l,'t':str(t),'specimens':n,'trials_per_specimen':m,'flags':count})
    U=min(F(1),levels[-1][1]+(2*Q+v/16)/(1-v/64))
    assert trueV<=U
    if trueV<=v/64:assert U<=v
    if trueV>v:assert U>v
    return {'name':name,'true_V':str(trueV),'true_V_float':float(trueV),
            'Q':str(Q),'U':str(U),'U_float':float(U),'passes':U<=v,
            'resources':resource,'levels':rows,'seed':seed}

def main():
    v=F(1,1024);delta=F(1,32)
    cases=[
      ('exact_null',[F(1,2)],[F(1)],F(0)),
      ('diffuse_near_null',[F(1,2)-F(1,512),F(1,2)+F(1,512)],[F(1,2)]*2,F(1,512**2)),
      ('diffuse_failure',[F(7,16),F(9,16)],[F(1,2)]*2,F(1,256)),
      ('rare_symmetric_failure',[F(1,4),F(1,2),F(3,4)],[F(1,64),F(31,32),F(1,64)],F(1,512)),
    ]
    runs=[simulate(v,delta,*c,seed=2026102900+i) for i,c in enumerate(cases)]
    curve=[]
    for vv in [F(1,100),F(1,10000),F(1,1000000),F(1,100000000)]:
        _,cost=schedule(vv,F(1,100));curve.append({'v':str(vv),**cost})
    # Two-flip-batch lower-bound algebra for the balanced weak alternative.
    vv=F(1,1000);p=[F(1,4)+vv,F(1,4)-vv,F(1,4)-vv,F(1,4)+vv]
    chi=sum((x-F(1,4))**2/F(1,4) for x in p)
    assert chi==16*vv*vv
    result={'status':'PASS','scope':'Four predetermined synthetic count runs and exact schedule/algebra checks. Binomial draws compress simulation only; every implied trial is charged. Not a physical acquisition or an empirical proof of confidence coverage.',
      'v':str(v),'delta':str(delta),'runs':runs,'resource_curve':curve,
      'two_flip_chi_square':str(chi),'two_flip_formula':'16*v^2',
      'unpaid_costs':['independent physical preparation','all visible-return native calls','return duration/tail exposure','sensors and timing','actuation and randomizer','calibration/deployment conditioning'],
      'proof_sha256':hashlib.sha256((ROOT/'MULTISCALE_RETURNED_COIN_CERTIFICATE.md').read_bytes()).hexdigest(),
      'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    out=ROOT/'MULTISCALE_RETURNED_COIN_CHECKS.json'
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'cases':[{'name':r['name'],'V':r['true_V_float'],'U':r['U_float'],'passes':r['passes']} for r in runs],'resources_each_run':runs[0]['resources'],'curve':curve},indent=2))

if __name__=='__main__':main()
