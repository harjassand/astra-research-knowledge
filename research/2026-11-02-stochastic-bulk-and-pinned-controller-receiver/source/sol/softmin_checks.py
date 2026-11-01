#!/usr/bin/env python3
"""Finite discriminators for the exact stochastic affine receiver.

Tests arbitrary finite-jump data, an adversarial kink, and actual mass-action
source-cut inequalities. These checks do not instantiate the entire primary
affine-family theorem or establish the unbounded-state bulk theorem by sampling.
"""
from pathlib import Path
from fractions import Fraction as F
import random, math, json

P=Path(__file__).resolve().parent
rng=random.Random(20261102)

def lse(v):
    b=max(v)
    return b+math.log(sum(math.exp(x-b) for x in v))

def soft_value(aff,x,theta):
    return theta*lse([-(sum(r*t for r,t in zip(s,x))+b)/theta for s,b in aff])

def check_jump_bound(aff,x,jumps,rates,theta):
    logits=[-(sum(r*t for r,t in zip(s,x))+b)/theta for s,b in aff]
    z=lse(logits);weights=[math.exp(a-z) for a in logits]
    rad=max(abs(sum(a*b for a,b in zip(s,j))) for s,_ in aff for j in jumps)
    delta=rad*math.exp(rad/theta)/(2*theta)
    actual=sum(q*(soft_value(aff,[a+b for a,b in zip(x,j)],theta)-soft_value(aff,x,theta)) for j,q in zip(jumps,rates))
    bound=0.
    for w,(s,_) in zip(weights,aff):
        projs=[sum(a*b for a,b in zip(s,j)) for j in jumps]
        d=sum(q*t for q,t in zip(rates,projs))
        gamma=sum(q*abs(t) for q,t in zip(rates,projs))
        bound+=w*(-d+delta*gamma)
    err=actual-bound
    assert err<=1e-9*(1+abs(actual)+abs(bound)),(actual,bound,err)
    return err,actual,bound

def falling(n,k):
    if n<k:return 0
    a=1
    for j in range(k):a*=n-j
    return a

def propensity(x,y,k):
    a=k
    for t,j in zip(x,y):a*=falling(t,j)
    return a

if __name__=='__main__':
    worst=-math.inf
    for _ in range(2500):
        dim=rng.randint(1,5);nm=rng.randint(1,9);ne=rng.randint(1,12)
        aff=[([rng.uniform(-1,1) for j in range(dim)],rng.uniform(-8,8)) for i in range(nm)]
        x=[rng.uniform(-4,4) for i in range(dim)]
        jumps=[[rng.randint(-4,4) for i in range(dim)] for e in range(ne)]
        rates=[10**rng.uniform(-3,3) for e in range(ne)]
        rad=max(abs(sum(a*b for a,b in zip(s,j))) for s,_ in aff for j in jumps)
        theta=4*max(rad,1)
        err,_,_=check_jump_bound(aff,x,jumps,rates,theta);worst=max(worst,err)
    # At a kink the naive nonsmooth active-branch rule fails. The smooth bound
    # still receives the actual symmetric jumps, with their nonzero curvature.
    aff=[([1.],0.),([-1.],0.)];x=[0.];jumps=[[1.],[-1.]];rates=[1.,1.]
    kink=check_jump_bound(aff,x,jumps,rates,4.)
    assert kink[1]>0
    # A raw weakly reversible three-complex cycle, with actual factorials.
    # y0=(2,0), y1=(1,1), y2=(0,2), r=(-1,0). Source monomials
    # separate as x_A/x_B grows, so the downward source flux is dominated.
    complexes=[(2,0),(1,1),(0,2)]
    edges=[(0,1,F(3,2)),(1,2,F(7,3)),(2,0,F(5,4))]
    slope=(F(-1),F(0));rows=[]
    for a,b in [(1000,10),(10000,10),(1000000,100),(10**12,10**4)]:
        x=(a,b);q=[propensity(x,complexes[i],k) for i,j,k in edges]
        levels=sorted({sum(s*t for s,t in zip(slope,y)) for y in complexes})
        cut_up=[];cut_down=[]
        for level in levels[:-1]:
            up=sum(rate for (i,j,k),rate in zip(edges,q) if sum(s*t for s,t in zip(slope,complexes[i]))<=level<sum(s*t for s,t in zip(slope,complexes[j])))
            down=sum(rate for (i,j,k),rate in zip(edges,q) if sum(s*t for s,t in zip(slope,complexes[j]))<=level<sum(s*t for s,t in zip(slope,complexes[i])))
            assert down<=up/3
            cut_up.append(up);cut_down.append(down)
        projs=[sum(s*(v-u) for s,u,v in zip(slope,complexes[i],complexes[j])) for i,j,k in edges]
        d=sum(rate*t for rate,t in zip(q,projs));gamma=sum(rate*abs(t) for rate,t in zip(q,projs))
        assert d>=gamma/2
        assert d==sum((levels[j+1]-levels[j])*(cut_up[j]-cut_down[j]) for j in range(len(levels)-1))
        assert gamma==sum((levels[j+1]-levels[j])*(cut_up[j]+cut_down[j]) for j in range(len(levels)-1))
        rows.append({'counts':list(x),'d_over_Gamma':str(d/gamma)})
    out={'scope':'Finite checks of an exact finite-jump inequality, kink failure of a naive rule, and actual source-cut arithmetic. Not a sampled proof of a global theorem.',
         'random_finite_jump_cases':2500,'worst_actual_minus_bound':worst,
         'kink_actual_generator':kink[1],'kink_certified_upper':kink[2],
         'raw_cycle_source_cut_checks':rows,
         'bulk_family_instantiation':'NOT_PERFORMED; the full abstract theorem uses the read governing finite affine-family lemma, not an alleged numerical acquisition'}
    (P/'results/softmin_checks.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
