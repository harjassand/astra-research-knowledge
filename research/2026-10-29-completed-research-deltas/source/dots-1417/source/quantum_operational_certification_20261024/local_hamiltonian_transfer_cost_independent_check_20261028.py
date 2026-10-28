#!/usr/bin/env python3
"""Exact finite-width/cost certificates; no Hamiltonian/source sampling or RNG."""
from fractions import Fraction as F
from pathlib import Path
import itertools,json,math
import sympy as s
C0=506880*3**12
B0=126720*3**12

def ceil_rat(x):return -((-x.numerator)//x.denominator)
def ceil_log2_rat(x):
 assert x>=1
 k=max(0,x.numerator.bit_length()-x.denominator.bit_length())
 while x.numerator>x.denominator*(1<<k):k+=1
 while k>0 and x.numerator<=x.denominator*(1<<(k-1)):k-=1
 assert x<=2**k and (k==0 or x>2**(k-1))
 return k

cases=[]; full=0; proper=0
for b,kappa,eps,q in itertools.product([F(0),F(1,10),F(1),F(10)],[F(1),F(1,4),F(1,1024)],[F(1),F(1,100),F(1,10**6)],[1,2,31,128]):
 l1=ceil_log2_rat(32/kappa);l2=ceil_log2_rat(F(C0*q)/(kappa*eps))
 d=ceil_rat(36*b)+max(18,2*l1,l2)
 assert d>=18 and d>=36*b+2*l1 and d>=36*b+l2
 # Analytic exp/log reductions leave these exact rational budget certificates.
 visible=F(4,2**l1); floor=F(B0*q,2**l2)/kappa
 assert visible<=kappa/8 and floor<=eps/4
 for n in [q,2*q,max(1000,q)]:
  w=min(n,2*d+1);W=min(n,3*w-2);C=min(q,4*W-2)
  span=W+2*(C-1)*(W-1);K=min(q,2*span);A=min(q,K*K)
  assert span<=8*W*W and K<=16*W*W
  assert A<=256*W**4<=20736*w**4<=3**12*d**4
  assert 4**w<=4*16**d
  # Keep exp(O(B)) as16^ceil(36B), making this cost bound wholly rational.
  poly=max(16**18,(F(64)/kappa)**8,(2*F(C0*q)/(kappa*eps))**4)
  assert 4**w<=4*16**ceil_rat(36*b)*poly
  isfull=(w==n);full+=isfull;proper+=not isfull
  cases.append({'B':str(b),'kappa':str(kappa),'epsilon':str(eps),'q':q,'n':n,'D':d,'w':w,'A':A,'full_support_exact_tau_zero':isfull})
# Sufficient base facts for the analytic logarithm inequalities, using exact partial sums.
assert sum(F(1,math.factorial(i)) for i in range(4))==F(8,3)
assert F(8,3)**3>18 # hence ln18<3 and6lnD<D forD>=18
assert 126720==7920*16 and C0==4*B0
assert 20736*F(9,4)**4==3**12
# A genuinely hidden four-branch Pauli/gauge source fixture, checked without evolution.
I=s.eye(2);X=s.Matrix([[0,1],[1,0]]);Y=s.Matrix([[0,-s.I],[s.I,0]]);Z=s.diag(1,-1)
R=s.Rational
sigmas=[s.diag(R(999,1000),R(1,1000)),(I+R(4,5)*X)/2,(I+R(3,5)*Z+R(1,5)*X)/2,(I+Y)/2]
pI=[s.S(1),R(9,10),R(17,20),R(4,5)]
def psd2(a):return a==a.H and a[0,0]>=0 and a[1,1]>=0 and s.expand(a.det())>=0
for a in sigmas:assert s.trace(a)==1 and psd2(a)
assert any(a*b!=b*a for a,b in itertools.combinations(sigmas,2))
barG=sum(sigmas,s.zeros(2))/4
barHZ=sum(((2*p-1)*a for p,a in zip(pI,sigmas)),s.zeros(2))/4
assert psd2(barHZ-R(3,5)*barG)
assert all(2*p-1>=R(3,5) for p in pI)
O=s.Matrix([[1,1,1,1],[1,-1,1,-1],[1,1,-1,-1],[1,-1,-1,1]])/2
assert O.T*O==s.eye(4)
# Each branch has identity and one fixed nonidentity q-logical Pauli only.
# Therefore GI−Gerror>=0 termwise for every encoder; optimal success isx^TQx.
Q=O*s.diag(*pI)*O.T
assert Q.eigenvals()=={p:1 for p in pI}
assert Q*O[:,0]==O[:,0]
out={'status':'PASS','source_calls':0,'RNG_used':False,'Hamiltonian_simulation':False,'finite_parameter_cases':len(cases),'full_support_fallback_cases':full,'proper_local_width_cases':proper,'maximum_checked_D':max(c['D'] for c in cases),'C0':C0,'floor_prefactor':B0,'rational_cap':'ceil(36B)+max(18,2ceil(log2(32/kappa)),ceil(log2(C0*q/(kappa*epsilon))))','fixed_B_local_dimension_bound':'4^w <=64 exp(36B ln16) max(16^18,(64/kappa)^8,(2C0 q/(kappa epsilon))^4)','visibility_and_floor_rational_certificates':True,'tail_base_inequalities_certified':'e>8/3, (8/3)^3>18, D>=18','nonvacuous_hidden_selector_fixture':{'branch_identity_probabilities':[str(p) for p in pI],'gauge_states_noncommuting':True,'gauge_states_include_rank_deficient':True,'minimum_fixed_gauge_eigenvalue':'1/1000','all_generator_margins_at_least':'3/5','global_identity_dominance':'termwise PSD for every x','encoder_oracle':'x^T Q x; unique maximum1 at unknown first selector direction up to sign'},'kind':'exact arithmetic and prescribed finite source-family matrices; not source acquisition or a verification of the imported Lieb–Robinson theorem'}
p=Path(__file__).with_suffix('.json');p.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(p.read_text(),end='')
