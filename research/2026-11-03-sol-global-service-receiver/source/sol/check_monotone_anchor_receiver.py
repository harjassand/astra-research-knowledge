#!/usr/bin/env python3
"""Exact-rational finite checks of the new raw generator identities.

The proof is the uniform analytic classification in the companion Markdown.
These finite probes check formulas and competing channels, not universality.
"""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parent
Y=((0,0,0),(1,1,0),(2,1,1),(3,2,2))
V=((1,1,0),(1,0,1),(1,1,1),(-3,-2,-2))

def ff(x,y):
    p=1
    for a,n in zip(x,y):
        if a<n:return 0
        for j in range(n):p*=a-j
    return p

def coeff(r):
    k0,k1,k2,k3=r
    K=max(Q(1),4*k3/k2);L=4+4*K*k1/k2;C=L+5
    return K,L,C,3*C+L+3

def h(b,c):
    t=min(b,c)
    return abs(b-c)+Q(3*t+t%2,2)

def profile(b,c,L,C):
    if b==c==0:return 3*C+3
    if c==0:return 2*C+(2 if b==1 else L+1)
    if b==0:return 2*C+2
    if min(b,c)==1:return C+(L if c==1 and b>=2 else 1)
    return 0

def F(x,r):
    a,b,c=x;K,L,C,_=coeff(r)
    return 16*(K*max(Q(0),a-h(b,c))**2+C*a+profile(b,c,L,C))

def block(x,r):
    return [(r[i]*ff(x,Y[i]),tuple(x[j]+V[i][j] for j in range(3)))
            for i in range(4) if ff(x,Y[i])]

def drift(x,r):
    return sum(q*(F(z,r)-F(x,r)) for q,z in block(x,r))

def sufficient_n(r):
    k0,k1,k2,k3=r;K,L,C,_=coeff(r)
    for a in range(8,1000000):
        if Q(k0,k1*a)*(C+L-1)>Q(1,2):continue
        if (C+L-1)*k0/(k2*a*(a-1))+C*k1/(k2*(a-1))>Q(1,2):continue
        if C*k0/(2*k2*a*(a-1))>1:continue
        if C*k1/(2*k2*(a-1))+(K*(2*a+1)-1)*k0/(2*k2*a*(a-1))>Q(1,2):continue
        ratios=(k0/(4*k3*a*(a-1)*(a-2)),k1/(2*k3*(a-1)*(a-2)),k2/(k3*(a-2)))
        if sum(ratios)>1:continue
        if C*ratios[2]+(K*(2*a+1)+C)*sum(ratios[:2])>2:continue
        if 3+(C-K*(2*a-7))*ratios[2]+C*sum(ratios[:2])>-2:continue
        # The unready q/qmax<=2 conditions follow from these stronger positive
        # bounds because C>=1,L>=4. The S-class leading margin uses a>=4.
        return a
    raise AssertionError('head scan exceeded; no universality conclusion')

def strip_value(x,rD,J):
    a,b,c,d,e,f=x
    return F((d,e,f),rD)+b+c+Q(e+f,2)+3*(J+1-a)

def strip_edges(x,rI,rD,kf,kb):
    for off,r in ((0,rI),(3,rD)):
        for q,z in block(x[off:off+3],r):
            out=list(x);out[off:off+3]=z
            yield q,tuple(out)
    a,b,c,d,e,f=x
    for rate,sgn in ((kf*a*d*ff((b,c),(2,2)),1),(kb*a*d*ff((e,f),(2,2)),-1)):
        if rate:yield rate,(a,b-2*sgn,c-2*sgn,d,e+2*sgn,f+2*sgn)

def main():
    sets=[tuple(map(Q,r)) for r in ((1,1,1,1),(2,3,1,2),(1,1,4,1),(3,1,2,1))]
    rows=[];checks=0
    hidden=(0,1,2,3,4,5,10,100,1000000)
    for r in sets:
        n=sufficient_n(r);worst=None
        for a,b,c in product((n,n+1,2*n,10*n),hidden,hidden):
            x=(a,b,c);q=sum(v for v,z in block(x,r));v=drift(x,r)
            assert v<=-4*q,(r,x,v,q)
            assert F((a,b+2,c+2),r)<=F(x,r)
            if b>=2 and c>=2:
                K,L,C,fmax=coeff(r)
                assert F((a,b-2,c-2),r)-F(x,r)<=96*K*a+16*fmax
            ratio=v/q
            worst=ratio if worst is None else max(worst,ratio)
            checks+=1
        rows.append({'rates':list(map(str,r)),'acquired_sufficient_N':n,'worst_generator_over_q':str(worst)})
    rI=sets[0];rD=sets[0];kf=Q(2);kb=Q(1);J=10
    n=sufficient_n(rD);K,L,C,fmax=coeff(rD)
    T=max(n+3,int(6*rI[3]*J*J/kf)+1)
    while (3+96*K*T+16*fmax)*kb*J>rD[3]*(T-1)*(T-2):T+=1
    stripchecks=0;worst=None
    for a,d in product((0,1,2,3,J),(T,T+1,2*T)):
        for b,c,e,f in product((0,1,2,10,1000000),repeat=4):
            x=(a,b,c,d,e,f);v0=strip_value(x,rD,J)
            edges=list(strip_edges(x,rI,rD,kf,kb));q=sum(v for v,z in edges)
            gen=sum(v*(strip_value(z,rD,J)-v0) for v,z in edges)
            assert gen<=-q,(x,gen,q)
            ratio=gen/q;worst=ratio if worst is None else max(worst,ratio)
            stripchecks+=1
    out={'scope':'Exact finite formula checks; uniform theorem is the analytic source classification, not this finite sample.',
         'one_port_checks':checks,'one_port':rows,'strip_checks':stripchecks,
         'unit_beta_strip_J':J,'unit_beta_strip_T':T,'strip_worst_generator_over_all_activity':str(worst)}
    (ROOT/'results/monotone_anchor_receiver_checks.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
