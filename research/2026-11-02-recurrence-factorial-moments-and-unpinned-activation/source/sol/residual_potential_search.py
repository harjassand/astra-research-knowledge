#!/usr/bin/env python3
"""Test a primal availability-residual potential against actual boundary rays.

R_p(x)=p.x-max_{source y<=x}p.y. Maximal-source firings cannot increase R_p.
This search tests whether that exact property is enough for global receiving.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import random,json
import sympy as sp
from coverability_clock import cubic,rate_at,le

P=Path(__file__).resolve().parent
n=sp.Symbol('n',integer=True,positive=True)

def residual(x,raw,p):
    src=[y for y,z,k in raw if le(y,x)]
    if not src:return sum(a*b for a,b in zip(p,x))
    return sum(a*b for a,b in zip(p,x))-max(sum(a*b for a,b in zip(p,y)) for y in src)

def ray_drift(raw,a,c):
    # At n>=10 all finite source B counts in the searched inputs are enabled.
    x=(a,20,c);sources={y for y,z,k in raw}
    m=max(y[1] for y in sources if le(y,x))
    terms=[];dr=0
    for y,z,k in raw:
        if not le(y,x):continue
        out=tuple(v-u+w for v,u,w in zip(x,y,z))
        mout=max(w[1] for w in sources if le(w,out))
        inc=z[1]-y[1]-mout+m
        factor=sp.Rational(k.numerator,k.denominator)
        for count,order in [(a,y[0]),(c,y[2])]:
            for j in range(order):factor*=count-j
        for j in range(y[1]):factor*=n-j
        dr+=factor*inc
        terms.append({'source':y,'target':z,'delta_R':inc,'rate_polynomial':str(sp.expand(factor)),'maximal_source':y[1]==m})
        if y[1]==m:assert inc<=0
    dr=sp.Poly(sp.expand(dr),n)
    return dr,terms

if __name__=='__main__':
    cases=[]
    raw=cubic()
    for a,c in product(range(5),repeat=2):
        d,terms=ray_drift(raw,a,c)
        if d.LC()>0 or d.is_zero:cases.append({'network':'banked cubic','a':a,'c':c,'drift':str(d.as_expr()),'terms':terms})
    rng=random.Random(20261102)
    complexes=[v for v in product(range(4),repeat=3) if sum(v)==3]
    witness=None;checked=0
    for trial in range(600):
        cs=rng.sample(complexes,rng.randint(3,6))
        raw=[(cs[i],cs[(i+1)%len(cs)],F(rng.randint(1,7))) for i in range(len(cs))]
        raw+=[((0,0,0),(1,0,0),F(1)),((1,0,0),(0,0,0),F(1))]
        for a,c in product(range(4),repeat=2):
            d,terms=ray_drift(raw,a,c);checked+=1
            if not d.is_zero and d.LC()>0:
                witness={'trial':trial,'a':a,'c':c,'drift':str(d.as_expr()),
                         'raw':[{'source':y,'target':z,'rate':str(k)} for y,z,k in raw],
                         'terms':terms};break
        if witness:break
    out={'scope':'Actual polynomial boundary-ray calculation for a new primal residual potential. No recurrence verdict follows from failure of this ansatz.',
         'tested_ray_phases':checked,'cubic_zero_or_positive':cases,'positive_witness':witness,
         'pathwise_principle':'Every firing from a maximal available source has delta R<=0, exactly.',
         'whole_recurrence':'NOT_PROVED'}
    (P/'results/residual_potential_search.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'tested_ray_phases':checked,'positive_witness':witness,
                      'cubic_problematic_phases':[{'a':r['a'],'c':r['c'],'drift':r['drift']} for r in cases]},indent=2))
