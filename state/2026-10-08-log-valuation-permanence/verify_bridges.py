#!/usr/bin/env python3
"""Independent exact-rational checks for full-denominator lifting and 2D checker."""
from fractions import Fraction as F
from random import Random
from itertools import product
import importlib.util
from pathlib import Path

loc=Path(__file__).with_name('tropical_check_2d.py')
spec=importlib.util.spec_from_file_location('tc2',str(loc))
tc=importlib.util.module_from_spec(spec)
import sys
sys.modules['tc2']=tc
spec.loader.exec_module(tc)
rand=Random(2601008)
def dot(x,y):return x[0]*y[0]+x[1]*y[1]
def brute_criterion(edges,r):
    eligible=[]
    for e in edges:
        drift=dot(e.nu,r)
        if drift:
            num=min(dot(x,r) for x in e.numerator)
            den=min(dot(x,r) for x in e.denominator)
            eligible.append((num-den,drift))
    if not eligible:return True
    t=min(v for v,z in eligible)
    return all(z>0 for v,z in eligible if v==t)

cases=200
lifts=0; brute_checks=0
for idx in range(cases):
    E=[]
    for ei in range(rand.randint(2,5)):
        A=[(F(rand.randint(-3,3)),F(rand.randint(-3,3))) for _ in range(rand.randint(1,3))]
        B=[(F(rand.randint(-3,3)),F(rand.randint(-3,3))) for _ in range(rand.randint(1,3))]
        nu=(rand.randint(-2,2),rand.randint(-2,2))
        E.append(tc.reaction(str(ei),A,B,nu))
    # independently expand the common denominator:  e's numerator times every f != e denominator.
    for ri,ej in enumerate(E):
        terms=[tuple(F(z) for z in a) for a in ej.numerator]
        for fi,ef in enumerate(E):
            if fi==ri:continue
            terms=[(x[0]+b[0],x[1]+b[1]) for x in terms for b in ef.denominator]
        for rx in range(-3,4):
            for ry in range(-3,4):
                if not (rx or ry):continue
                r=(F(rx),F(ry))
                common=sum(min(dot(b,r) for b in ef.denominator) for ef in E)
                tau=(min(dot(a,r) for a in ej.numerator)
                      -min(dot(b,r) for b in ej.denominator))
                assert min(dot(a,r) for a in terms)==tau+common,(idx,ri,r)
                lifts+=1
    ans=tc.check(E)
    for rx in range(-4,5):
        for ry in range(-4,5):
            if not(rx or ry):continue
            brute_checks+=1
            r=(F(rx),F(ry))
            if ans['valid']:
                assert brute_criterion(E,r),(idx,r)
            if not brute_criterion(E,r):
                assert ans['valid'] is False,(idx,r)
    if not ans['valid']:
        assert not brute_criterion(E,tuple(map(F,ans['direction']))),(idx,ans)
print('Exact rational denominator-lift identities:',lifts, 'PASS')
print('Independent rational-direction comparator:',brute_checks,'PASS')
print('Random networks:',cases,'seed=2601008')

# Direct falsifier check: x'=-k*x*y, y'=a-b*y*y, all a,b,k>0.
# Generic sectors satisfy criterion, yet x->0 as y->sqrt(a/b).
FEX=[tc.reaction('0->Y',[(0,0)],[(0,0)],(0,1)),
     tc.reaction('2Y->Y',[(0,2)],[(0,0)],(0,-1)),
     tc.reaction('X+Y->Y',[(1,1)],[(0,0)],(-1,0))]
directions,_=tc.all_directions(FEX)
assert all(brute_criterion(FEX,tuple(map(F,r))) for r,s in directions if s=='open sector')
assert not brute_criterion(FEX,(F(1),F(0)))
print('Generic-directions-only test falsifier: all open sectors PASS; boundary ray (1,0) FAIL')

# Non-rational subpower-deformed mass-action model: d=2 and
# phi_e(x)=x^alpha exp(c_e(1+||log x||_2^2)^1/4).
# Uniform perturbation of log_h phi <= |c_e|*(1+d*L^2)^.25/L for L=|log h|,
# which tends to zero; e.g. on p in [-1,1]^2 at L=10000.
from math import sqrt
L=10000; d=2; ce=3
err=abs(ce)*(1+d*L*L)**.25/L
assert err < 0.04
print('Uniform subpower exponent distortion bound at |ln h|=10000,d=2,c=3:',round(err,8),'PASS')
