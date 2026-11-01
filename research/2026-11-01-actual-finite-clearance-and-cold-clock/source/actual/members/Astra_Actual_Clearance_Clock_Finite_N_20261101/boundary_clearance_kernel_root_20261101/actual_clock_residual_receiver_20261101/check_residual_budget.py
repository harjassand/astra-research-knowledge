#!/usr/bin/env python3
"""Exact checks for the constructed residual receiver, not independent review."""
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict
import hashlib,json
import sympy as sp
ROOT=Path(__file__).resolve().parent
K=F(800,171); J=F(404,17)
A,L,E,C=sp.symbols('A L E CD', nonnegative=True)
assertions=0
def check(v,label):
 global assertions
 assert v,label
 assertions+=1

def frac(v): return F(int(sp.numer(v)),int(sp.denom(v)))
# Return a power polynomial in T: keys n mean coefficient/T**n.
def charge(poly,p,k):
 out=defaultdict(F); terms=[]
 for powers,coeff in sp.Poly(sp.expand(poly),A,L,E,C).terms():
  a,r,s,c=powers; coeff=frac(coeff)
  check(coeff>=0,'nonnegative monomial')
  if c:
   check(c==1,'only one CD factor')
   R=r+a
   check(p>=1+F(R)+F(s,2),'CD weighted exponent')
   value=coeff*6*F(3,2)**s*J
   exponent=R+3*s-k+3
   mode='weighted CD'
  elif a:
   R=r+a-1
   if p>=1+F(R)+F(s,2):
    value=coeff*6*F(3,2)**s*K
    exponent=R+3*s-k-2
    mode='weighted A'
   else:
    check(p>=F(R)+F(s,2),'unweighted A exponent')
    value=coeff*F(3,2)**s
    exponent=R+3*s-k
    mode='unweighted A'
  else:
   check(p>=F(r)+F(s,2),'horizon exponent')
   value=coeff*4*F(3,2)**s
   exponent=r+3*s-k+1
   mode='original horizon'
  out[-exponent]+=value
  terms.append({'powers_A_L_E_CD':powers,'coefficient':str(coeff),'mode':mode,'T_denominator_power':-exponent,'integrated_coefficient':str(value)})
 return dict(out),terms

# Independently reconstruct the convenient slow-rate envelopes from the exact rates.
a,b,c,d,e=sp.symbols('a b c d e',nonnegative=True)
state=(a,b,c,d,e)
reactions=[(1,(1,0,0,0,0)),(a,(-1,0,0,0,0)),
(a*(a-1),(-1,0,1,0,0)),(a*c,(1,0,-1,0,0)),
(a*(a-1),(-1,0,0,1,0)),(a*d,(1,0,0,-1,0)),
(a*(a-1),(-1,0,0,0,1)),(a*e,(1,0,0,0,-1)),
(a*e,(-1,0,1,1,-1)),(2*c*d,(1,0,-1,-1,1)),
(c*d,(1,1,-1,-1,0)),(a*b,(-1,-1,1,1,0))]
litL=a+(c+d)/2
qLL=sL=qEE=0
for rate,nu in reactions:
 u=nu[0]+sp.Rational(nu[2]+nu[3],2); v=nu[4]
 qLL+=rate*u*u; sL+=rate*abs(u);qEE+=rate*v*v
check(sp.expand(qLL-(1-a/sp.Integer(2)+a*a+a*litL/2+a*e))==0,'qLL literal')
check(sp.expand(sL-(1-a+a*a+a*litL+a*e))==0,'sL literal')
check(sp.expand(qEE-(a*(a-1)+2*a*e+2*c*d))==0,'qEE literal')

# Groups are the actual exact-corrector residual, bounded before integration.
specs=[
 ('first_l', A+2*A*L,F(5,2),1),
 ('first_e_without_Z',6*(5*A*L+2*A*E),F(2),3),
 ('rh_without_Z_countpart',E+10*A*E*L+3*A*L**2+2*C+A*E**2+2*A*E,F(5,2),6),
 ('rh_countpart',12*A*E,F(5,2),5),
 ('Taylor_ll',5*(1+sp.Rational(3,2)*A*L+A*E),F(7,2),2),
 ('Taylor_le',14*(A*L+A*E),F(3),4),
 ('Taylor_ee',75*(A*L+2*A*E+2*C),F(5,2),6),
 ('product_ll',10*(A+1)*(E+1)*(1+2*A*L+A*E),F(7,2),7),
 ('product_le',14*(A+1)*(E+1)*(A*L+2*A*E+2*C),F(3),9),
]
total=defaultdict(F); groups={}
for name,poly,p,k in specs:
 budget,terms=charge(poly,p,k)
 for n,value in budget.items():total[n]+=value
 groups[name]={'p':str(p),'T_denominator_before_integration':k,'polynomial':str(sp.expand(poly)),
               'integrated_budget':{str(n):str(v) for n,v in sorted(budget.items())},'monomial_receipts':terms}
# Z² terms: first_e <=epsilon² and rh <=(9/2)epsilon².
total[0]+=F(11,20000)
expected={0:F(11,20000),1:20+45*K,2:6+F(537,2)*K+252*J,
3:60+312*K+1164*J,4:24+936*K,5:2100*K+168*J,
6:40+180*K+168*J,7:948*K,8:372*K,9:144*K,10:84*K}
check(dict(total)==expected,'complete residual coefficients')
remainder=expected[2]+sum(expected[n]/F(10000)**(n-2) for n in range(3,11))
check(remainder<F(7254),'uniform T>=10000 simplification')
check(expected[1]==F(4380,19),'leading constant')
# Segment inflation is checked without irrational arithmetic.
a=F(200,199)
check(81*a**7<100,'ll segment inflation')
check(13*a**3<14,'le segment inflation')
check(148**2*a**5<150**2,'ee segment inflation')
check(F(401,10000)<F(1,2),'startup l rectangle')
check(F(8*400**3+1,10000**3)<F(1,1000),'startup e rectangle')
check(F(197)-F(1,50)-F(1,10000**5)>0,'post-startup cone segment padding')
check(F(2349,16)<148,'small-l ee extension')
check(F(64*400**6,10**20)<2,'startup source upper R')
check(F(5)*F(1001,1000)<6,'startup e derivative')
# exp(1)<3 from factorial series plus geometric remainder.
sum_exp=sum(F(1,__import__('math').factorial(i)) for i in range(12))
remainder_exp=F(1,__import__('math').factorial(12))/(1-F(1,13))
check(sum_exp+remainder_exp<3,'exp(1)<3 startup J')

def iroot5(N):
 lo,hi=0,N+1
 while hi-lo>1:
  mid=(lo+hi)//2
  if mid**5<=N:lo=mid
  else:hi=mid
 return lo

def outward_decimal(v,digits=12):
 n=(v.numerator*10**digits+v.denominator-1)//v.denominator
 return str(n//10**digits)+'.'+str(n%10**digits).zfill(digits)
examples=[]
for power in range(20,26):
 N=10**power;Tlo=iroot5(N)
 r=F(11,20000)+F(4380,19*Tlo)+F(7254,Tlo*Tlo)
 raw=sum(v/F(Tlo)**n for n,v in expected.items())
 check(raw<r,'example simplification')
 check(Tlo**5<=N<(Tlo+1)**5,'root enclosure')
 examples.append({'N':str(N),'T_integer_lower':Tlo,'r_upper':outward_decimal(r),'r_exact_at_T_lower':str(r),
                  'raw_initial_discrepancy_upper':str(F(1,Tlo)),
                  'full_endpoint_corrector_upper':str(F(2,Tlo*Tlo))})

sources=[ROOT.parent/'GLOBAL_L_WEIGHTED_CLOCK_DERIVATIVES.md',ROOT.parent/'REGULARIZED_WEIGHTED_SOURCE_BUDGET.md',
 ROOT.parent/'REMAINING_CLOCK_OBSERVABLE.md',ROOT.parent/'CLOCK_WINDOW_REMAINING_CLOCK_INDEPENDENT_REVIEW.md',
 ROOT.parent/'actual_state_gates/ACTUAL_ENTRANCE_A_Z_GATES.md',
 ROOT.parent.parent/'return_path_construction_20261101/rate2_task_observable_corrector/TASK_OBSERVABLE_CORRECTOR.md']
report={'status':'PASS supporting exact author checks; independent receiver review pending','assertions':assertions,
 'residual_simplified':'11/20000 + 4380/(19T) + 7254/T^2, T>=10000',
 'coefficient_by_inverse_T_power':{str(n):str(v) for n,v in sorted(expected.items())},
 'T2_remainder_ceiling_exact':str(remainder),'groups':groups,'examples':examples,
 'source_bindings':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},
 'scope':'Residual/endpoint component only, not bracket, gate survival, or automatic clearance.'}
(ROOT/'CHECK_RESULTS.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='groups'},indent=2))
