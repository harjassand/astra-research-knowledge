"""Supplementary independently entered exact checks; not a proof or source edit."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'ACTIVATED_TO_MACRO_AND_POSITIVE_FRACTIONS.md'
EXPECTED = 'e527fafdfe790fa753b4584fca338bf9e4aa37179643a1f1596e39b140cb99a0'
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == EXPECTED

# Explicit independent channel entries: delta, propensity, M/J marks by sign(C-D).
channels = [
    ((1,0,0,0,0), lambda a,b,c,d,e: 1, ((1,6),(1,6),(1,6))),
    ((-1,0,0,0,0), lambda a,b,c,d,e: a, ((-1,-6),(-1,-6),(-1,-6))),
    ((-1,0,1,0,0), lambda a,b,c,d,e: a*(a-1), ((0,-1),(-1,-5),(-1,-5))),
    ((1,0,-1,0,0), lambda a,b,c,d,e: a*c, ((0,1),(0,1),(1,5))),
    ((-1,0,0,1,0), lambda a,b,c,d,e: a*(a-1), ((-1,-5),(-1,-5),(0,-1))),
    ((1,0,0,-1,0), lambda a,b,c,d,e: a*d, ((1,5),(0,1),(0,1))),
    ((-1,0,0,0,1), lambda a,b,c,d,e: a*(a-1), ((-1,-5),(-1,-5),(-1,-5))),
    ((1,0,0,0,-1), lambda a,b,c,d,e: a*e, ((1,5),(1,5),(1,5))),
    ((-1,0,1,1,-1), lambda a,b,c,d,e: a*e, ((0,-1),(0,-1),(0,-1))),
    ((1,0,-1,-1,1), lambda a,b,c,d,e: 2*c*d, ((0,1),(0,1),(0,1))),
    ((1,1,-1,-1,0), lambda a,b,c,d,e: c*d, ((0,0),(0,0),(0,0))),
    ((-1,-1,1,1,0), lambda a,b,c,d,e: a*b, ((0,0),(0,0),(0,0))),
]
def M(x): return x[0]+min(x[2],x[3])
def R(x): return sum(x[2:])
def J(x): return R(x)+2*x[0]+4*M(x)
def h(a,N): return max(F(1,4),1-F(a,4*N))
def generator_scaled_v(x,N):
    total=F(0)
    for delta,rate,_ in channels:
        q=rate(*x)
        if not q: continue
        y=tuple(v+d for v,d in zip(x,delta))
        total+=q*(F(2)**(M(x)-M(y))*h(y[0],N)-h(x[0],N))
    return total

states=marks=assertions=0
for x in product(range(6), repeat=5):
    a,b,c,d,e=x
    branch=0 if c<d else 1 if c==d else 2
    pos=neg=0
    drift=[0]*5
    for delta,rate,expected in channels:
        q=rate(*x)
        if not q: continue
        y=tuple(v+vdelta for v,vdelta in zip(x,delta))
        assert min(y)>=0
        dm=M(y)-M(x)
        assert (dm,J(y)-J(x))==expected[branch]
        if dm==1: pos+=q; assert delta[0]==1
        if dm==-1: neg+=q; assert delta[0]==-1
        drift=[v+q*vdelta for v,vdelta in zip(drift,delta)]
        marks+=1; assertions+=2+(dm!=0)
    assert pos==1+a*e+(a*max(c,d) if c!=d else 0)
    assert pos>=1+a*(R(x)-2*M(x))
    assert neg==a+(3 if c==d else 2)*a*(a-1)
    assert neg<=3*a*a
    assert sum(drift)==1-a
    quadratic=(-3*a*a+a*(c+d-b)+3*c*d,c*d-a*b,
               a*a-a*c+a*e+a*b-3*c*d,
               a*a-a*d+a*e+a*b-3*c*d,a*a-2*a*e+2*c*d)
    correction=(2*a+1,0,-a,-a,-a)
    assert tuple(drift)==tuple(v+w for v,w in zip(quadratic,correction))
    N=10000
    bound=-F(49,100)-F(49,100)*a*R(x)+F(98,100)*a*M(x)+F(303,100)*a*a
    bound+=F(a*(b+e)+a*(a-1)-3*c*d,4*N)
    assert generator_scaled_v(x,N)<=bound
    assertions+=7; states+=1

N=10**40
r=F(1,1000); delta=F(1,10**12); cutoff=int(delta*N)
large=0
for a,m,gap,e in product([0,1,cutoff//8,cutoff//2,cutoff-1],
                         [0,1,cutoff//8,cutoff//2],
                         [0,1,N//1000,N//100], [0,N//1000,N//100]):
    for c,d in [(m,m+gap),(m+gap,m)]:
        b=N-a-c-d-e
        x=(a,b,c,d,e)
        if b<0 or R(x)<2*r*N or M(x)>=delta*N: continue
        assert generator_scaled_v(x,N)<=-F(M(x)**2,8*N)*h(a,N)
        assert 7+18*delta*N<=r*N/2<=F(R(x),4)
        assert F(401,100)*delta*N+F(1,2)+delta/4<=F(24,100)*R(x)
        assert 1-delta/4-F(1,4*N)>=F(99,100)
        large+=1; assertions+=4

eta=delta**4/(1000*3**40)
for margin in [delta/(2*3**6),delta**2/(8*3**18),delta**4/(128*3**38),
               3*delta**2/(4*3**18),delta**2/(4*3**14),delta**2/(2*3**16)]:
    assert margin>eta; assertions+=1
assert 2+5*eta/2<3; assertions+=1
assert max(54,12,42,42,30)<=100; assertions+=1
counterexample=(N//2,0,0,0,N//2)
assert F(3*N,4)<sum(counterexample)<=2*N
assert R(counterexample)>=4*r*N and M(counterexample)>delta*N+1
assertions+=2
result={'status':'PASS_SUPPLEMENTARY_EXACT_CHECKS_NOT_A_UNIFORM_PROOF',
        'source_sha256':EXPECTED,'small_states':states,'enabled_marks':marks,
        'large_activated_cases':large,'assertions':assertions,
        'initial_macro_overshoot_counterexample_confirmed':True}
(HERE/'CHECK_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
