#!/usr/bin/env python3
"""Finite marked optimal-stopping diagnostics at the PHYSICAL reward only.

The common candidate is U=(1+sum log(residual!))^2. Finite diagnostics are not
global certificates. Exact rational transition probabilities and relative
factorial ratios avoid subtracting huge nearly equal absolute potentials.
"""
from fractions import Fraction as F
from collections import defaultdict
from functools import lru_cache
from math import prod
from pathlib import Path
import mpmath as mp
import json

mp.mp.dps=80
P=Path(__file__).resolve().parent
def ff(a,b):return 0 if a<b else prod(range(a-b+1,a+1))
def falling(x,y):return prod(ff(a,b) for a,b in zip(x,y))
def mv(a):return mp.mpf(a.numerator)/a.denominator if isinstance(a,F) else mp.mpf(a)
def relative_factorial(z,root):
    r=F(1)
    for a,b in zip(z,root):
        if a>b:r*=prod(range(b+1,a+1))
        elif a<b:r/=prod(range(a+1,b+1))
    return r
def ordered(k=3,constants=None):
    C=[(0,0,0),(1,1,0)]+[(j,j-1,j-1) for j in range(2,k+1)]
    constants=constants or [1]*k+[2]
    return [(C[j],C[(j+1)%len(C)],F(constants[j])) for j in range(len(C))]
def adjacent():
    I=ordered(3);II=ordered(3,[1,1,1,3])
    return [(y+(0,),u+(0,),k) for y,u,k in I]+[((0,)+y,(0,)+u,k) for y,u,k in II]
def conservative():
    return [((2,0),(1,1),F(100)),((1,1),(2,0),F(1)),
            ((0,0),(1,0),F(1)),((1,0),(0,0),F(1)),
            ((0,0),(0,1),F(1)),((0,1),(0,0),F(1))]

def probe(raw,x,t,horizon=12):
    x,t=tuple(x),tuple(t);root=tuple(a-b for a,b in zip(x,t));assert min(root)>=0
    v0=1+sum(mp.loggamma(a+1) for a in root)
    scale=2*v0
    @lru_cache(None)
    def val(xx,tt):
        z=tuple(a-b for a,b in zip(xx,tt));ratio=relative_factorial(z,root)
        delta=mp.log(mv(ratio))
        return delta+delta*delta/scale
    @lru_cache(None)
    def trans(xx):
        rr=[k*falling(xx,y) for y,u,k in raw];q=sum(rr);assert q>0
        return [(tuple(a-b+c for a,b,c in zip(xx,y,u)),u,r/q) for (y,u,k),r in zip(raw,rr) if r],q
    @lru_cache(None)
    def best(xx,tt,left):
        now=val(xx,tt)
        if left==0:return now
        tr,q=trans(xx)
        cont=1/(mv(q)*scale)+sum(mv(p)*best(y,u,left-1) for y,u,p in tr)
        return min(now,cont)
    tr,q=trans(x);rows=[]
    for h in range(1,horizon+1):
        value=1/(mv(q)*scale)+sum(mv(p)*best(y,u,h-1) for y,u,p in tr)
        rows.append({'horizon':h,'physical_cost_plus_energy_change_over_2V':mp.nstr(value,35)})
    return {'input':x,'mark':t,'candidate':'(1+sum log(residual factorial))^2','rows':rows,'dp_states':best.cache_info().currsize}

if __name__=='__main__':
    fixtures=[('ordered3',ordered(),(1000,0,0),(0,0,0)),
              ('ordered3',ordered(),(0,1000,1000),(0,0,0)),
              ('ordered3',ordered(),(0,0,1000),(0,0,0)),
              ('ordered3',ordered(),(0,1000,0),(0,0,0)),
              ('ordered4',ordered(4),(1000,0,0),(0,0,0)),
              ('adjacent',adjacent(),(0,1000,0,0),(0,0,0,0)),
              ('conservative_control',conservative(),(500,1000),(1,1))]
    out=[]
    for label,raw,x,t in fixtures:
        r={'fixture':label,**probe(raw,x,t,horizon=12)};out.append(r)
        print(json.dumps({'fixture':label,'input':x,'first_negative':next((z for z in r['rows'] if mp.mpf(z['physical_cost_plus_energy_change_over_2V'])<0),None),'last':r['rows'][-1],'states':r['dp_states']}),flush=True)
    (P/'results').mkdir(exist_ok=True)
    (P/'results/marked_physical_probe.json').write_text(json.dumps({'scope':'Finite exact-transition/multiprecision energy diagnostics, not a global or asymptotic proof.','fixtures':out},indent=2)+'\n')
