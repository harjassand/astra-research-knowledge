#!/usr/bin/env python3
"""Acquire actual first-source-switch clocks and full normalized output kernels."""
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict
import sympy as sp
import json
from episode_diagnostics import ordered,rate

P=Path(__file__).resolve().parent

def killed(raw,z,linkage):
    ix={y:i for i,y in enumerate(linkage)};Q=sp.zeros(len(ix));outputs={};rows=[]
    for j in linkage:
        i=ix[j];x=tuple(a+b for a,b in zip(z,j));q=F(0)
        for s,u,k in raw:
            r=rate(x,s,k);q+=r
            if not r:continue
            if s==j:
                assert u in ix;Q[i,ix[u]]+=sp.Rational(r.numerator,r.denominator)
            else:
                zz=tuple(a+b-c for a,b,c in zip(z,j,s));assert min(zz)>=0
                key=(zz,u)
                if key not in outputs:outputs[key]=len(outputs)
                rows.append((i,outputs[key],r))
        Q[i,i]-=sp.Rational(q.numerator,q.denominator)
    B=sp.zeros(len(ix),len(outputs))
    for i,j,r in rows:B[i,j]+=sp.Rational(r.numerator,r.denominator)
    assert Q*sp.ones(len(ix),1)+B*sp.ones(len(outputs),1)==sp.zeros(len(ix),1)
    G=(-Q).inv();PP=G*B;vv=G*sp.ones(len(ix),1)
    assert PP*sp.ones(len(outputs),1)==sp.ones(len(ix),1)
    assert all(x>=0 for x in PP) and all(x>0 for x in vv)
    # Exact summed Laplace derivative at zero is the negative physical mean.
    assert -G*G*B*sp.ones(len(outputs),1)==-vv
    return Q,B,PP,vv,outputs

def symbolic_ordered_clock():
    n=sp.symbols('n',integer=True,positive=True);c=[1,n+1,2*(n+1)**2,6*(n+1)**2*(n+2)**2]
    kill=[0,1,2*(n+1)+1,6*(n+2)**2+3*(n+2)+1]
    Q=sp.zeros(4)
    for i in range(4):Q[i,(i+1)%4]=c[i];Q[i,i]-=c[i]+kill[i]
    v=[sp.factor(t) for t in (-Q).inv()*sp.ones(4,1)]
    assert sp.limit(v[0]/n,n,sp.oo)==F(1,2)
    return {'physical_clock_from_tag_zero_exact':str(v[0]),'leading_clock_over_n_exact':'1/2',
            'all_phase_clocks_exact':[str(x) for x in v]}

if __name__=='__main__':
    raw=ordered();L=[e[0] for e in raw];rows=[]
    for n in [2,10,100]:
        z=(0,n,n);Q,B,PP,vv,outputs=killed(raw,z,L)
        outrows=[]
        for (zz,u),i in outputs.items():
            assert all(a>=b for a,b in zip(zz,z))
            outrows.append({'residual':zz,'target':u,'probability_from_tag_zero':str(PP[0,i])})
        rows.append({'n':n,'physical_mean_from_tag_zero_exact':str(vv[0]),'output_channels':len(outputs),
                     'all_probability_rows_sum_exact':'1','Laplace_derivative_clock_identity_exact':True,
                     'actual_outputs':outrows})
    out={'scope':'Exact local actual-time operation for an evolving-inventory marked process; outward output rewards are retained and no recurrence follows from normalization.',
         'symbolic_ordered_clock':symbolic_ordered_clock(),'exact_normalization_checks':rows}
    (P/'results/tagged_resolvent.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'leading_physical_clock_over_n':'1/2','exact_normalized_instances':len(rows),
                      'all_first_switch_residuals':'coordinatewise outward; not a recurrence proof'},indent=2))
