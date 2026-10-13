"""Exact rational finite checks; no producer imports or external observations."""
from collections import defaultdict
from fractions import Fraction as F
from math import comb,factorial
from pathlib import Path
import json


def evidence(n,s,p):
    likelihood=p**s*(1-p)**(n-s)
    return F(1,(n+1)*comb(n,s))/likelihood


def crossing_probability(p,alpha,horizon):
    surviving={0:F(1)}
    crossed=F(0)
    for n in range(1,horizon+1):
        nxt=defaultdict(F)
        for s,mass in surviving.items():
            for value,probability in [(0,1-p),(1,p)]:
                t=s+value;weight=mass*probability
                if evidence(n,t,p)>=1/alpha:
                    crossed+=weight
                else:
                    nxt[t]+=weight
        surviving=dict(nxt)
        assert crossed+sum(surviving.values(),F(0))==1
    return crossed


def binary_bounds(lo,hi,coherence,u0,u1):
    mass=1/coherence;eta=1-mass
    a=u0+(hi if u1>=u0 else lo)*(u1-u0)
    wlo=max(F(0),lo-eta);whi=min(mass,hi)
    assert wlo<=whi
    w=wlo if u1>=u0 else whi
    return mass*u0+w*(u1-u0),a,(wlo,whi)


def stopped_transcript(p,cap):
    # Stop at first success, or the cap, keeping its exact time/outcome.
    out={('success',j):(1-p)**(j-1)*p for j in range(1,cap+1)}
    out[('no-success',cap)]=(1-p)**cap
    expected=sum((1-p)**j for j in range(cap))
    assert sum(out.values())==1
    return out,expected


def main():
    counts=dict(beta_martingale_steps=0,dirichlet_martingale_steps=0,
                exact_crossing_fixtures=0,binary_optimization_fixtures=0,
                rare_families=0,stopped_transcript_couplings=0)
    probabilities=[F(1,100),F(1,10),F(1,2),F(9,10),F(99,100)]
    for p in probabilities:
        for n in range(14):
            for s in range(n+1):
                assert (1-p)*evidence(n+1,s,p)+p*evidence(n+1,s+1,p)==evidence(n,s,p)
                counts['beta_martingale_steps']+=1
    # Three-label mixture identity uses distinct rational probabilities.
    pvec=[F(1,7),F(2,7),F(4,7)]
    def multi(counts):
        n=sum(counts);k=len(counts)
        value=F(factorial(k-1),factorial(n+k-1))
        for c,p in zip(counts,pvec):value*=factorial(c)/p**c
        return value
    for n in range(9):
        for i in range(n+1):
            for j in range(n-i+1):
                cs=[i,j,n-i-j];average=F(0)
                for label,p in enumerate(pvec):
                    nxt=cs.copy();nxt[label]+=1;average+=p*multi(nxt)
                assert average==multi(cs)
                counts['dirichlet_martingale_steps']+=1
    crossings=[]
    for p in probabilities:
        for alpha in [F(1,5),F(1,20),F(1,100)]:
            crossed=crossing_probability(p,alpha,30)
            assert crossed<=alpha
            crossings.append(dict(p=str(p),alpha=str(alpha),horizon=30,probability=str(crossed)))
            counts['exact_crossing_fixtures']+=1
    for lo,hi in [(F(0),F(1)),(F(1,10),F(2,5)),(F(3,5),F(9,10))]:
        for coherence in [F(1),F(101,100),F(3,2)]:
            for u0,u1 in [(F(1,3),F(5)),(F(7),F(1,10)),(F(2),F(2))]:
                lower,upper,(wlo,whi)=binary_bounds(lo,hi,coherence,u0,u1)
                mass=1/coherence
                # Independent dense rational feasible sweep of the tiny LP.
                for index in range(41):
                    p=lo+(hi-lo)*F(index,40)
                    assert u0+p*(u1-u0)<=upper
                    for w in [max(F(0),mass-(1-p)),min(mass,p)]:
                        assert lower<=mass*u0+w*(u1-u0)
                # Verify actual equality endpoints admit a histogram.
                for w in [wlo,whi]:
                    assert max(lo,w)<=min(hi,1-mass+w)
                counts['binary_optimization_fixtures']+=1
    rare=[]
    for m in range(2,35):
        theta=F(1,2**m);r=2**m
        a0=1+(r-1)*theta;a1=1+(r-1)*2*theta
        assert a0==2-theta and a1==3-2*theta
        assert a1/a0>=F(10,7)
        q0=theta*r/a0;q1=2*theta*r/a1
        assert q1-q0==1/((3-2*theta)*(2-theta))>=F(1,6)
        rare.append(dict(m=m,theta=str(theta),partition_ratio_separation=str(a1/a0),tilted_label_separation=str(q1-q0)))
        counts['rare_families']+=1
        for cap in [1,2,5,12,32]:
            t0,en=stopped_transcript(theta,cap);t1,_=stopped_transcript(2*theta,cap)
            tv=sum(abs(t0[key]-t1[key]) for key in t0)/2
            assert tv<=theta*en
            counts['stopped_transcript_couplings']+=1
    result=dict(status='PASS',counts=counts,crossing_probabilities=crossings,rare_families=rare,
                arithmetic='Exact fractions/integer combinatorics throughout; no eigensolver or Monte Carlo decision.',
                boundary='Finite fixtures only. Infinite-horizon coverage and all-algorithm lower bounds follow the written proof. No physical data,prior-art clearance or external validation.')
    Path('sequential_overlap_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',counts=counts),indent=2))


if __name__=='__main__':main()
