"""Exact hook/content evaluation of the symmetric logical-spin programme.

No source draws, Haar grid, decoder optimizer or unknown physical model.
"""

from fractions import Fraction as F
from math import factorial,isqrt
from pathlib import Path
import argparse,json,time


def partitions(n,maximum=None):
    if n==0:
        yield ();return
    maximum=n if maximum is None else min(maximum,n)
    for a in range(maximum,0,-1):
        for rest in partitions(n-a,a):yield (a,)+rest


def dimension(mu):
    out=factorial(sum(mu))
    hooks=1
    for i,row in enumerate(mu):
        for j in range(row):
            hooks*=row-j+sum(v>j for v in mu[i+1:])
    assert out%hooks==0
    return out//hooks


def addable(mu):
    for i,row in enumerate(mu):
        if i==0 or mu[i-1]>row:
            out=list(mu);out[i]+=1;yield tuple(out),row-i
    yield mu+(1,),-len(mu)


def sqrt_upper(n,bits=48):
    d=1<<bits;x=isqrt(n*d*d)
    if x*x<n*d*d:x+=1
    return F(x,d)


def evaluate(Q,r):
    n=Q+1;den=factorial(n)*r**Q
    mass=abscontent=content=content2=0;checks=0;rows=0
    for mu in partitions(Q):
        if len(mu)>r:continue
        rows+=1;f=dimension(mu);c=1
        for i,row in enumerate(mu):
            for j in range(row):c*=r+j-i
        assert c>0
        local=[0,0,0]
        for lam,t in addable(mu):
            g=dimension(lam);checks+=1
            local[0]+=g;local[1]+=g*t;local[2]+=g*t*t
            assert r+t>=0 and Q*r-t>=0
            a=c*f*g;mass+=a;abscontent+=a*abs(t)
            content+=a*t;content2+=a*t*t
        assert local==[n*f,0,Q*n*f]
    assert mass==den and content==0 and content2==Q*den
    eabs=F(abscontent,den)
    fidelity=F(1,4)+F(Q+1,8*r*Q)*eabs
    upper=F(1,4)+F(Q+1,8*r*Q)*sqrt_upper(Q)
    assert fidelity<=upper and fidelity<=F(1,2)
    return {'Q':Q,'r':r,'logical_irrep_dimension':Q+1,
            'retained_partitions':rows,'positive_branch_checks':checks,
            'all_transition_normalizations_and_moments':[True,True,True],
            'all_total_probabilities_normalize':True,
            'content_absolute_mean':str(eabs),'content_second_moment':Q,
            'optimal_Bell_fidelity':str(fidelity),'optimal_Bell_fidelity_decimal':float(fidelity),
            'Cauchy_upper_outward':str(upper),'Cauchy_upper_decimal':float(upper),
            'identity_recovery_achieved':False,'query_calls_in_circuit_contract':Q,
            'actual_source_or_quantum_circuit_calls':0}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--Q',type=int,default=32);ap.add_argument('--r',type=int,default=32)
    a=ap.parse_args();assert a.Q>=1 and a.r>=1
    start=time.perf_counter();out=evaluate(a.Q,a.r)
    out['scope']='exact one-design scalar receiver for analytic all-r Schur-branch mechanism; no stochastic source or physical circuit'
    out['seconds_after_imports']=time.perf_counter()-start
    Path(__file__).with_name('SYMMETRIC_BRANCH.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
