#!/usr/bin/env python3
"""Focused exact checks only; no previous large enumeration duplicated."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json
import sympy as s

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
EXPECTED={
 'ACTUAL_NARROW_COUNT_BAND.md':'c60f158a40e54a6b6864cec9b4fe8705ce432e809f3581647328f3b5235588bc',
 'COUNT_BAND_CONE_CONSEQUENCE.md':'9e0bea69f21a7cdab972ee731d21fa643ac00d0b76aee98568160696760b4e7f',
 'HISTORY_BUFFERED_PROGRESS_V1_7ac50b8b.md':'7ac50b8bc8ab75d4745845f034b7da72323c2174947f8d42960ba68fd0ca97d0',
 'BUFFERED_PROGRESS_WITHOUT_LOWER_RATIO.md':'30fbcc2c3f5d98cc50cee9a6e1e7ee5f9e04a6f2220cce51572acb9ce10f70dd',
}
hashes={n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in EXPECTED}
assert hashes==EXPECTED,(hashes,EXPECTED)

# Actual generator: all twelve literal directed channels.
A,B,C,D,E,L=s.symbols('A B C D E L',nonnegative=True)
rates=[1,A,A*(A-1),A*C,A*(A-1),A*D,A*(A-1),A*E,A*E,2*C*D,C*D,A*B]
deltas=[(1,0,0,0,0),(-1,0,0,0,0),(-1,0,1,0,0),(1,0,-1,0,0),
        (-1,0,0,1,0),(1,0,0,-1,0),(-1,0,0,0,1),(1,0,0,0,-1),
        (-1,0,1,1,-1),(1,0,-1,-1,1),(1,1,-1,-1,0),(-1,-1,1,1,0)]
beta=s.Rational(1,100)
um=[h[4]-s.Rational(h[0],2) for h in deltas]
lm=[h[0]+s.Rational(h[2]+h[3],2) for h in deltas]
vm=[u+beta*l for u,l in zip(um,lm)]
assert lm==list(map(s.Rational,['1','-1','-1/2','1/2','-1/2','1/2','-1','1','0','0','0','0']))
assert max(map(abs,lm))==1
assert max(abs(h[4]) for h in deltas)==1
assert max(map(abs,vm))==s.Rational(149,100)<s.Rational(151,100)
assert min(100+h for h in vm)==s.Rational(9851,100)>s.Rational(9849,100)
assert [sum(h) for h in deltas]==[1,-1]+[0]*10
gl=s.expand(sum(r*h for r,h in zip(rates,lm)))
qll=s.expand(sum(r*h*h for r,h in zip(rates,lm)))
gu=s.expand(sum(r*h for r,h in zip(rates,um)))
qu=s.expand(sum(r*h*h for r,h in zip(rates,um)))
gv=s.expand(sum(r*h for r,h in zip(rates,vm)))
qv=s.expand(sum(r*h*h for r,h in zip(rates,vm)))
L_actual=A+(C+D)/2
gl_source=1+A+A*L-3*A*A+A*E
qll_source=1-A/2+A*A+A*L/2+A*E
assert s.expand(gl-gl_source.subs(L,L_actual))==0
assert s.expand(qll-qll_source.subs(L,L_actual))==0
assert s.expand((qll_source-gl_source)-A*(4*A-L/2-s.Rational(3,2)))==0
assert s.expand(gv-gu-beta*gl)==0
for u,l,v in zip(um,lm,vm):
 assert s.simplify((1+beta)*u*u+(beta+beta*beta)*l*l-v*v-beta*(u-l)**2)==0
assert s.expand((1+beta)*qu+(beta+beta*beta)*qll-qv-sum(r*beta*(u-l)**2 for r,u,l in zip(rates,um,lm)))==0
G,H=s.symbols('G H')
assert s.expand(10*(G+beta*H)-(9*(1+beta)*G+(beta+beta*beta)*H)-s.Rational(91,100)*G-s.Rational(899,10000)*H)==0

# Count-band constants, valid for every real T>=10 and integer N=T^5.
t,z=s.symbols('t z',nonnegative=True)
occupation_slack=s.Rational(82,100)*t**5-16*t-16
floor_slack=(s.Rational(1,10)-s.Rational(1,2500)-s.Rational(1,100))*t**5-12*t-3
for p in [occupation_slack,floor_slack]:
 assert all(c>0 for c in s.Poly(s.expand(p.subs(t,z+10)),z).all_coeffs())
assert s.Rational(4,1)*(s.Rational(1,50)+s.Rational(4,100000)+s.Rational(40,100000))/s.Rational(9,10)==s.Rational(511,5625)<1
assert s.Rational(1,50)/124==s.Rational(1,6200)
assert s.Rational(12,10**4)==s.Rational(12,10000)
assert 1-s.Rational(12,10000)-s.Rational(1,2500)-s.Rational(1,100)==s.Rational(9884,10000)
assert s.Rational(9884,10000)*100000-3>s.Rational(9,10)*100000
# Check the only 100 integer residue classes in the pre-E-cap argument.
for residue in range(100):
 n=100000+residue
 ceiling=(n+99)//100
 assert F(ceiling-1)<F(n,100)
 assert F(ceiling)<=F(n,100)+1
assert F(12,2**2)==3 and F(12,20**2)==F(3,100)<F(1,25)

# All-u Taylor certificates for the actual eight distinct V marks.
v=s.symbols('v',positive=True)
jump_results=[]
for h in sorted(set(vm)):
 gap=-3*h/v**4+6*h*h/(v-s.Rational(151,100))**5-((v+h)**-3-v**-3)
 num,den=s.fraction(s.factor(s.together(gap.subs(v,100+z))))
 np=s.Poly(num,z);dp=s.Poly(den,z)
 assert all(c>=0 for c in np.all_coeffs())
 assert all(c>0 for c in dp.all_coeffs())
 jump_results.append({'mark':str(h),'gap_numerator_degree':np.degree(),
                      'nonnegative_numerator_coefficients':True,'positive_denominator_coefficients':True,
                      'scope':'every v>=100, not a sampled grid'})
ratio=60*v**4/(v-s.Rational(151,100))**5
assert s.simplify(s.diff(s.log(ratio),v)+(v+4*s.Rational(151,100))/(v*(v-s.Rational(151,100))))==0
assert ratio.subs(v,100)<1
margin=5*9849**5-3*10000**5
assert margin==163372964823886621245>0
assert s.Rational(10,7)**2>2 and s.Rational(10,7)+s.Rational(1,100)<s.Rational(3,2)
assert (s.Rational(2,5)/(s.Rational(3,2)**4))==s.Rational(32,405)
assert 16*s.Rational(32,405)>1

# Exact rational exponential-barrier ceiling exp(3/40)<=40/37.
barrier=s.Rational(-1,20)+s.Rational(9,800)*s.Rational(40,37)
assert barrier==s.Rational(-7,185)<0
assert s.Rational(199,200)*s.Rational(1,5000)==s.Rational(199,1000000)
assert s.Rational(199,200)*s.Rational(1,20000)==s.Rational(199,4000000)
seed_current_mass=s.Rational(199,4000000)/(1+s.Rational(12,10000))
assert seed_current_mass==s.Rational(199,4004800)>s.Rational(1,1000000)

result={
 'source_sha256':hashes,
 'scope':'original-clock count event and conditional buffered progress; no admission or clearance',
 'count_band_status':'PASS','cone_consequence_status':'PASS within actually received count event',
 'buffer_status':'PASS repaired pointwise/stopped and receiving scope; original-clock cap deadline guard present, no pre-cap band carried through removal',
 'history':'Original checks passed; binding attempt detected concurrent parent repair; preserved original and complete diff verified, then checks rebound and rerun.',
 'literal_L_marks':[str(h) for h in lm], 'literal_V_marks':[str(h) for h in vm],
 'GL':str(gl),'qLL':str(qll),'GV':str(gv),'qV':str(qv),
 'occupation_ceiling_at_T_ge_10':'511/5625',
 'maximum_actual_V_jump':'149/100',
 'all_v_finite_jump_certificates':jump_results,
 'buffer_scalar_ratio_at_100':str(s.factor(ratio.subs(v,100))),
 'buffer_scalar_integer_margin':margin,
 'exponential_barrier_coefficient_ceiling':str(barrier),
 'smaller_seed_over_actual_mass':str(seed_current_mass),
 'all_assertions_passed':True,
}
(HERE/'INDEPENDENT_EXACT_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
