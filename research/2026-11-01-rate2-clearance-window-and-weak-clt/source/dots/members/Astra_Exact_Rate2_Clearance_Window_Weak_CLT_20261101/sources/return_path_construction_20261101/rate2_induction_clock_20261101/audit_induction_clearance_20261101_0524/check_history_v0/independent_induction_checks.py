"""Independent exact algebra/receiving checks, no author imports or float arithmetic.
Finite checks supplement MATHEMATICAL_REVIEW.md; they do not prove stopping theorems.
Writes deterministic adjacent results. Replay only in a copy.
"""
from fractions import Fraction as Q
from itertools import product
from math import isqrt,factorial
from pathlib import Path
import json,hashlib
import sympy as sy
HERE=Path(__file__).resolve().parent
counts={'assertions':0,'enabled_retained_jump_cases':0,'parameter_cases':0,'geometric_stages':0}
def ck(x,ctx=''):
 counts['assertions']+=1
 if not x:raise AssertionError(ctx)
a,b,c,d,e,w=sy.symbols('a b c d e w');xs=(a,b,c,d,e)
# Literal full increments and propensities; independent of author complex helpers.
channels=[('imm',(1,0,0,0,0),sy.Integer(1)),('death',(-1,0,0,0,0),a),
 ('2A_AC',(-1,0,1,0,0),a*(a-1)),('AC_2A',(1,0,-1,0,0),a*c),
 ('2A_AD',(-1,0,0,1,0),a*(a-1)),('AD_2A',(1,0,0,-1,0),a*d),
 ('2A_AE',(-1,0,0,0,1),a*(a-1)),('AE_2A',(1,0,0,0,-1),a*e),
 ('AE_CD',(-1,0,1,1,-1),a*e),('CD_AE',(1,0,-1,-1,1),2*c*d),
 ('CD_AB',(1,1,-1,-1,0),c*d),('AB_CD',(-1,-1,1,1,0),a*b)]
retained={'imm','AE_2A','AE_CD','CD_AE','CD_AB','AB_CD'}
F=lambda x:x[0]+(x[2]+x[3])/2-sy.Rational(3,4)*w*x[4]**2+w*x[0]*x[4]
LF=sy.Integer(0);LA=sy.Integer(0);qrem=sy.Integer(0);marks={}
for name,delta,rate in channels:
 y=tuple(x+v for x,v in zip(xs,delta))
 mark=sy.expand(F(y)-F(xs));marks[name]=str(mark)
 ck(sum(delta)==(1 if name=='imm' else -1 if name=='death' else 0))
 if name in retained:
  LF+=rate*mark;LA+=rate*delta[0]
  di=int(name=='imm');dr=int(name=='AE_2A');dj=int(name=='CD_AE');ds=int(name=='AE_CD')
  ck(delta[0]+delta[2]==di+dr)
  ck(delta[0]+delta[3]==di+dr)
  ck(delta[1]==-di-2*dr+delta[0]-delta[4])
  ck(delta[4]==dj-dr-ds)
 else:qrem+=rate
LF=sy.expand(LF);LA=sy.expand(LA)
expected=1+w*e+w*c*d/2+2*w*a*c*d+a*e*(1+w*(3*e-2*a-sy.Rational(3,2)-b))
ck(sy.expand(LF-expected)==0)
ck(sy.expand(LA-(1+3*c*d-a*b))==0)
ck(sy.expand(qrem-(a+3*a*(a-1)+a*(c+d)))==0)
wantmarks={'imm':1+w*e,'AB_CD':-w*e,'CD_AB':w*e,'CD_AE':w*(a-e/2+sy.Rational(1,4)),
 'AE_CD':w*(e/2-a+sy.Rational(1,4)),'AE_2A':1+w*(5*e/2-a-sy.Rational(7,4))}
for n,v in wantmarks.items():ck(sy.expand(sy.sympify(marks[n])-v)==0)
for x in product(range(4),repeat=5):
 vals=dict(zip(xs,x))
 for name,delta,rate in channels:
  if name not in retained or rate.subs(vals)<=0:continue
  y=tuple(z+v for z,v in zip(x,delta));ck(min(y)>=0)
  di=int(name=='imm');dr=int(name=='AE_2A');dj=int(name=='CD_AE');ds=int(name=='AE_CD')
  ck(y[0]+y[2]-x[0]-x[2]==di+dr)
  ck(y[0]+y[3]-x[0]-x[3]==di+dr)
  ck(y[1]-x[1]==-di-2*dr+(y[0]-x[0])-(y[4]-x[4]))
  ck(y[4]-x[4]==dj-dr-ds)
  counts['enabled_retained_jump_cases']+=1
# Coefficientwise global envelopes, independently expanded.
p,q=sy.symbols('p q',nonnegative=True);H=p+q+1
polys={
 'drift':100*H**4-q-p**2/2-16*p**4-40*H*p**2*q,
 'bracket':64*H**5-4-32*p**2*q-7*H**2*p**2-8*H**2*p**2*q,
 'up_count':12*H**3-1-3*p**2-8*p**2*q}
for name,f in polys.items():ck(all(v>=0 for _,v in sy.Poly(sy.expand(f),p,q).terms()),name)
# Exact probability multiplier and time-shift margins.
ck(4*64*64==16384)
ck(32*144==4608)
ck(24*(32+16)==1152)
ck(16384*3+8+800*3+4608*3+1152*3+48*3==68984<100000)
for tol in [Q(1,4),Q(1,100),Q(1,10**20)]:
 dd=tol/2;eps=tol**3/12
 ck(Q(2,3)*(tol-dd)**3==eps)
 ck(Q(2,3)*tol**3>=eps)
 ck(tol>=dd and dd>=tol/4)
 ck(Q(2)+tol+tol/4<4)
# e<3 and e>2, sufficient for the A exponential barrier.
low=sum(Q(1,factorial(j)) for j in range(9))
upper=low+Q(1,factorial(9))/(1-Q(1,10))
ck(2<low<upper<3)
ck(Q(1)-1/low>Q(1,2))
# Algebraic proof-level constants received by the continuation.
D=Q(1,10**100);sqrtD=Q(1,10**50);eps_in=D/4;Cstar=3*10**12
ck(sqrtD*sqrtD==D)
ck(Q(1,8)<Q(1,4)) # 2^-3/2<1/2 -> deadline geometric factor<2.
ck(Q(1,2)<Q(9,16)) # 2^-1/2<3/4 -> occupation geometric factor<4.
ck(Q(4,3)*(1-Q(4,32))>=1)
ck(Q(4,3)*(1+Q(2,32))<=Q(13,10)**2)
ck(Q(4,3)*(1-Q(5,32))>=Q(1,4))
ck((Q(8,27)**2)*(Q(3,4)**3)==Q(1,27)) # squared tail coefficient sqrt(3)/9.
ck(Q(7,8)*(1+D)<Q(15,16))
# Exact rational outward square roots used only for independent finite diagnostics.
def sqrt_interval(x,scale=10**180):
 x=Q(x);z=isqrt(x.numerator*scale*scale//x.denominator)
 lo=Q(z,scale);hi=lo if lo*lo==x else Q(z+1,scale)
 ck(lo*lo<=x<=hi*hi)
 return lo,hi
for n,T,tol in [(10**20+1,10**40,Q(1,4)),(10**20+1,10**60,Q(1,100)),(10**30+1,10**60,Q(1,4)),(10**40+1,10**80,Q(1,10**20))]:
 K=n*n-1;p=K+1;q=2*n+1;H=p+q+1;N=T**5
 ck(K>=10**40 and N>=10**200)
 ck(T*T>=16*H and T**3>=64*p*p and T*T>=4*p*q/tol)
 ck(N-2*p*T-q*T**3>=Q(N,2))
 ck(2*q*T**3<=Q(N,8))
 ck(2+6*p*p*T*T<=Q(N,8))
 ck(1+5*p*T<=6*p*T)
 ck(48*3*p**3<=100000*H**6/tol**6)
 ck(K*T<=D*N and K*T+1<D*N)
 ck(K*T/Cstar>=1)
 ck(Q(32,K)<1)
 ck(Q(1,T)+tol/2<=2)
 ck(Q(4,3)*(1-Q(4,K))>=1)
 ck(Q(4,3)*(1+Q(2,K))<=Q(13,10)**2)
 ck(Q(4,K)<=Q(1,8))
 # State-envelope corners satisfy retained invariants and the full coefficient bound.
 for L in [1,K*T,K*T+1]:
  for A in [0,1,L]:
   if A>L:continue
   for E in [0,q*T**3]:
    for I in [0,L-1]:
     R=L-1-I;B=N-I-2*R+A-E
     ck(B>=N/2) # N/2 is exact here (N even); no float is used below.
     coeff=N-B+3*E-2*A-Q(3,2)
     ck(abs(coeff)<=5*H*T**3)
     # All retained small F marks fit H/T^2; both large marks fit 2.
     small=[-Q(E,N),Q(E,N),Q(A,N)-Q(E,2*N)+Q(1,4*N),Q(E,2*N)-Q(A,N)+Q(1,4*N)]
     ck(all(abs(v)<=Q(H,T*T) for v in small))
     ck(abs(1+Q(E,N))<=2)
     ck(abs(1+Q(5*E,2*N)-Q(A,N)-Q(7,4*N))<=2)
 # Literal geometric stage sums, not just an O(.) notation.
 m0=K*T;m=m0;hsum=Q(0);tsum=Q(0)
 while m<D*N:
  elo,ehi=sqrt_interval(Q(N*m))
  hsum+=Q(10**4,N)*ehi
  tsum+=Q(16,m*m)*ehi
  counts['geometric_stages']+=1
  m*=2
 _,khi=sqrt_interval(K)
 Dlower=Q(32*T,K)/khi
 ck(hsum<4*10**4*sqrtD)
 ck(tsum<Dlower)
 # Macro first-hit and actual-total epsilon margins.
 ck(Q(29,32)*D*N-Q(3,2)>=D*N/2)
 ck((1-3*D-2*sqrtD)*N-3>=N/2)
 ck(D/2>=eps_in*(1+D))
 ck(Q(1,2)>=eps_in*(1+D))
 ck(sqrtD/2>=eps_in*(1+D))
 ck(Q(7,8)*(1+D)*N<Q(15,16)*(N+2))
 ck(D*N/2-2>0)
 counts['parameter_cases']+=1
# Integer rounding of tiny-band and clearance death requirements, including nonmultiples.
def ceil(x):return -((-x.numerator)//x.denominator)
for N in [10**200,10**200+1,10**200+15,10**200+16,10**201+37]:
 need_band=(D*N+2).numerator//(D*N+2).denominator+1
 ck(need_band>=ceil(D*N))
 S0=N+2;need_clear=ceil(Q(S0,16))
 ck(need_clear>=Q(S0,16))
 ck(Q(S0,32)*2<=need_clear)
 ck((1-D)*N>Q(15,16)*(N+2)) # tiny lower-band loss is NOT clearance.
# Exact unchanged source hashes and clean author replay.
for manifest in ['FINITE_LEVEL_AUTHOR_FREEZE.json','CLEARANCE_AUTHOR_FREEZE.json']:
 data=json.loads((HERE/'inputs'/manifest).read_text())
 for n,h in data['files'].items():ck(hashlib.sha256((HERE/'inputs'/n).read_bytes()).hexdigest()==h)
for n in ['CLOCK_CHECK_RESULTS.json','CLEARANCE_CHECK_RESULTS.json']:
 ck((HERE/'inputs'/n).read_bytes()==(HERE/'author_replay/rate2_induction_clock_20261101'/n).read_bytes())
(HERE/'EXACT_IDENTITIES.json').write_text(json.dumps({'retained_LF':str(LF),'retained_LA':str(LA),'full_jump_marks':marks,'remaining_intensity':str(sy.expand(qrem)),'probability_coefficient_sum':68984},indent=2,sort_keys=True)+'\n')
report={'status':'PASS_INDEPENDENT_EXACT_SUPPORTING_CHECKS','counts':counts,'author_imports':False,
 'scope':'Finite-level corrected clock, proof-level stage occupation receiving, analytical clearance window and LLN; no numerical interior acquisition.',
 'not_proved_by_tests':['optional stopping','pathwise scalar comparison','conditional stage composition','strong Markov interior service','LLN order of limits'],
 'proof':'MATHEMATICAL_REVIEW.md'}
(HERE/'INDEPENDENT_CHECK_RESULTS.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
print(json.dumps(report,indent=2,sort_keys=True))
