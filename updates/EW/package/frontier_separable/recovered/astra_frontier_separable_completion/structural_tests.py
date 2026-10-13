"""Exact physical-source identities and independent infinite-tail coefficient checks.
Also falsifies exact low-rank preservation by a Sylvester inverse.
"""
from fractions import Fraction as F
from collections import defaultdict
from itertools import product
from pathlib import Path
import json,time,random
import sympy as sp
import numpy as np
import gap_algebra as ga
import reference_majorana as ref
from pressure_basis import geo,val

def run():
    start=time.perf_counter();a,b=sp.symbols('a b');h=(a-b)*(2*a+b+1)*(a+2*b+1)
    sub=lambda x,y:sp.expand(h.subs({a:x,b:y},simultaneous=True))
    bulk=6*h-sum(sub(a+da,b+db) for da,db in [(1,0),(0,1),(-1,0),(-1,1),(0,-1),(1,-1)])
    assert sp.expand(bulk)==0
    assert sp.expand(sub(-1,b)+sub(-1,b+1)-2*sub(0,b))==0
    assert sp.expand(sub(a,-1)+sub(a+1,-1)-2*sub(a,0))==0
    assert sub(1,0)+sub(0,1)-2*sub(0,0)==0
    moment=sub(0,1)-sub(1,0);assert moment==-12
    J=ga.current();Fmid={ga.atom((3,t,t,3),(geo(0),)*3):-F(1,2) for t in (1,2)}
    dens=(((0,1),F(1)),)
    double=ga.apply(ga.apply(J,densities=dens,part='diag'),densities=dens,part='diag')
    r=ga.add((1,double),(8,J),(-8,Fmid));assert ga.inner(r,r)==0
    expected={ga.atom((3,3,3),(geo(0),geo(0,1))):F(-1),ga.atom((3,3,3),(geo(0,1),geo(0))):F(1)}
    r=ga.add((1,ga.pop(ga.apply(Fmid,part='hop'))),(-1,expected));assert ga.inner(r,r)==0
    r=ga.pop(ga.apply(ga.apply(ga.apply(J,densities=dens,part='diag'),part='hop'),part='hop'))
    assert ga.inner(r,r)==0
    # Independently expand input configurations, then use the previous finite-word algebra.
    f={ga.atom((3,1,1,3),(geo(F(1,2)),geo(0),geo(F(1,3)))):F(1),
       ga.atom((3,2,2,3),(geo(F(1,2)),geo(0),geo(F(1,3)))):F(1)}
    densities=(((0,1),F(1)),((0,2),F(1,4)));infinite=ga.apply(f,densities=densities)
    explicit=defaultdict(F)
    for x,y in product(range(9),repeat=2):
        positions=[0,x+1,x+2,x+y+3]
        for t in (0,1):
            word=tuple(sorted([0,1,2*positions[1]+t,2*positions[2]+t,2*positions[3],2*positions[3]+1]))
            for w,c in ref.column(word,F(1),densities).items():explicit[w]+=F(1,2)**x*F(1,3)**y*c
    checked=0
    for w,c in sorted(explicit.items()):
        key=next(iter(ga.from_word(w)))
        if max((s[0] for s in key[1]),default=0)>4:continue
        got=sum(C*sp.prod(val(s,g[0]) for s,g in zip(k[1],key[1])) for k,C in infinite.items() if k[0]==key[0])
        assert got==c;checked+=1
    # Exact separable rank need not be preserved by a well-defined inverse.
    L=6;X=sp.Matrix([[sp.Rational(1,i+j+2) for j in range(L)] for i in range(L)])
    A=sp.diag(*range(1,L+1));assert A*X+X*A==sp.ones(L,L)
    assert X.det()!=0 and X.rank()==L
    # Projected Richardson contraction checked in independent finite coordinates.
    rng=np.random.default_rng(1302610);iteration_checks=0
    for n in(5,8,13):
        Q,_=np.linalg.qr(rng.normal(size=(n,n)));V=Q[:,:n-2];W=rng.normal(size=(n,n));W=W-W.T
        z=V@rng.normal(size=n-2);K=V.T@W@V;M=float(np.linalg.norm(W,2));tau=1/(1+M*M)
        theta=np.sqrt(1-tau);exact=V@np.linalg.solve(np.eye(n-2)+K,V.T@z);x=np.zeros(n)
        for _ in range(20):
            nxt=(1-tau)*x+tau*V@(V.T@(z-W@x))
            assert np.linalg.norm(nxt-exact)<=theta*np.linalg.norm(x-exact)+1e-12
            x=nxt;iteration_checks+=1
    return dict(harmonic_polynomial=str(h),exact_boundary_identities=4,harmonic_source_moment=int(moment),
       exact_physical_current_identities=3,independent_infinite_commutator_coefficients=checked,
       cauchy_rank=L,rank_one_rhs=True,richardson_float_checks=iteration_checks,
       seconds=time.perf_counter()-start,
       scope='Exact harmonic/source/rank algebra; finite floating iteration diagnostics, not a physical solver benchmark')
if __name__=='__main__':
    if not __debug__:raise RuntimeError('Run without Python -O: exact tests must execute')
    out=run();Path('structural_tests.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
