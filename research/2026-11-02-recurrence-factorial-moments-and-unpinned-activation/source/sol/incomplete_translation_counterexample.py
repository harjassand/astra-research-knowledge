#!/usr/bin/env python3
"""Exact geometry and finite diagnostic checks for the nonchemical corridor.

Infinite explosion follows from the summable analytic bounds in the proof file,
not from the finite numerical recursion here.
"""
from fractions import Fraction as F
from math import prod
from pathlib import Path
import json

P=Path(__file__).resolve().parent

def grid(n):
    assert n%2==0 and n>=2
    ij=[(0,0)]
    for j in range(n):
        columns=range(1,n) if j%2==0 else range(n-1,0,-1)
        ij.extend((i,j) for i in columns)
    ij.extend((0,j) for j in range(n-1,0,-1))
    assert len(ij)==n*n and len(set(ij))==n*n and ij[-1]==(0,1)
    out=[(n+i,n+j,3*n-i-j) for i,j in ij]
    assert len(set(out))==n*n and all(sum(x)==5*n and min(x)>=n for x in out)
    return out

def reference_ratio(v,w):
    # mu(w)/mu(v), with mu(x)=1/x!; never form huge factorials.
    r=F(1)
    for a,b in zip(v,w):
        if b>a:r/=prod(range(a+1,b+1))
        elif a>b:r*=prod(range(b+1,a+1))
    return r

def run(nmax=100):
    T=1.0;rows=[];all_directions=set();edge_checks=0
    for n in range(20,nmax+1,2):
        path=grid(n);etime=0.0;Tstart=T
        for v,w in zip(path,path[1:]):
            direction=tuple(b-a for a,b in zip(v,w));all_directions.add(direction)
            assert sum(abs(t) for t in direction)==2 and sum(direction)==0
            r=reference_ratio(v,w);assert F(1,4)<=r<=4
            lam=16*n**20*float(r/(1+r));assert lam>=3*n**20
            etime+=T/lam
            T=1+T/(16*float(r));edge_checks+=1
        assert T<2
        endT=T;w=grid(n+2)[0];v=path[-1]
        direction=tuple(b-a for a,b in zip(v,w));all_directions.add(direction);assert direction==(2,1,7)
        r=reference_ratio(v,w)
        exact=F(1,(n+1)*(n+2)**2*prod(3*n+k for k in range(7)))
        assert r==exact and F(1,(6*n)**10)<=r<=F(1,n**10)
        lam=16*n**20*float(r/(1+r));assert lam>=8*n**10/6**10
        cross=T/lam;etime+=cross
        T=1+T/(16*float(r));edge_checks+=1
        analytic=6**10*(n**-8+n**-10)
        assert etime<=analytic
        rows.append({'n':n,'states':len(path),'T_start':Tstart,'T_end':endT,
                     'expected_increment_time':etime,'expected_ordinary_hazard_bound':6*n*etime,
                     'analytic_increment_upper':analytic})
    return {'scope':'Finite exact geometry/rate checks and numerical birth-death recursion; infinite explosion is proved by summable bounds, not this finite diagnostic.',
            'grids_checked':len(rows),'directed_edges_checked':edge_checks,
            'corridor_directions':sorted(all_directions),'rate_distortion':[1,16],
            'expected_time_partial_sum':sum(r['expected_increment_time'] for r in rows),
            'expected_ordinary_hazard_partial_bound':sum(r['expected_ordinary_hazard_bound'] for r in rows),'rows':rows}

if __name__=='__main__':
    out=run();(P/'results/incomplete_translation_counterexample.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='rows'},indent=2))
