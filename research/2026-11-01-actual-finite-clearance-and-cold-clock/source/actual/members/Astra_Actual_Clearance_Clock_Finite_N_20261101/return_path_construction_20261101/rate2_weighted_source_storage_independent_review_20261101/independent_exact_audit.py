#!/usr/bin/env python3
"""Receiver checks. Reactions reconstructed from reactant/product stoichiometry.
Ordinary proof in INDEPENDENT_REVIEW.md is primary; these checks are supplementary.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib, json, math
import sympy as s
HERE=Path(__file__).resolve().parent
V=s.symbols('A B C D E', nonnegative=True); A,B,C,D,E=V
# Falling-factorial mass action and literal rate multiplier; no imported author code.
R=[('immigration',{}, {'A':1},1),('death',{'A':1},{},1),
 ('AA_AC',{'A':2},{'A':1,'C':1},1),('AC_AA',{'A':1,'C':1},{'A':2},1),
 ('AA_AD',{'A':2},{'A':1,'D':1},1),('AD_AA',{'A':1,'D':1},{'A':2},1),
 ('AA_AE',{'A':2},{'A':1,'E':1},1),('AE_AA',{'A':1,'E':1},{'A':2},1),
 ('AE_CD',{'A':1,'E':1},{'C':1,'D':1},1),('CD_AE',{'C':1,'D':1},{'A':1,'E':1},2),
 ('CD_AB',{'C':1,'D':1},{'A':1,'B':1},1),('AB_CD',{'A':1,'B':1},{'C':1,'D':1},1)]
channels=[]
for name,react,prod,k in R:
 rate=s.Integer(k)
 for v in V:
  for j in range(react.get(str(v),0)): rate*=v-j
 nu=tuple(prod.get(str(v),0)-react.get(str(v),0) for v in V)
 channels.append((name,rate,nu))
def dz(f,nu):return f.subs(dict(zip(V,[v+d for v,d in zip(V,nu)])),simultaneous=True)-f
def gen(f):return sum(rate*dz(f,nu) for _,rate,nu in channels)
checks=[]
def zero(f,label):
 assert s.factor(f)==0,(label,s.factor(f)); checks.append(label)
phi,pm,pp,alpha_m,alpha_p,k=s.symbols('phi pm pp alpha_m alpha_p k')
# Arbitrary functions on E-1,E,E+1: finite-jump product identity without Taylor.
phi_by_E={-1:pm,0:phi,1:pp}
primitive_delta={-1:alpha_m,0:0,1:-alpha_p}
direct=0; jumps={}
for name,rate,nu in channels:
 da,de=nu[0],nu[4]
 jump=(A+da)*phi_by_E[de]-A*phi+k*primitive_delta[de]
 direct+=rate*jump;jumps[name]=jump
L=A+(C+D)/2;a2=A*(A-1);K=a2*(A-1)+2*C*D*(A+1)
GA=1-A-3*a2+A*(C+D)+3*C*D-A*B
zero(gen(A)-GA,'12-channel A generator')
zero(GA-(1+2*A-5*A*A+2*A*L+3*C*D-A*B),'full -5A^2 cancellation identity')
zero(direct-(phi*GA+K*(pp-phi)+2*A*A*E*(pm-phi)-k*(a2+2*C*D)*alpha_p+2*k*A*E*alpha_m),'arbitrary-weight/primitive generator identity')
qA=sum(rate for _,rate,_ in channels)
zero(qA-(1+A*B+3*C*D+A*A-2*A+2*A*L+2*A*E),'total rate identity')
for name,rate,nu in channels:
 assert nu[0] in (-1,1)
 assert abs(nu[0]+F(nu[2]+nu[3],2))<=1 and abs(nu[4])<=1
 assert sum(nu)<=0 or name=='immigration'
 checks.append('jump/rate/total-count structure: '+name)
# k arbitrary exact p=2 functions, T^6 common scaling omitted homogeneously.
f=E**-2; prim=E**-1
AP=f*E/(E+1);AM=f*E/(E-1);DE=E*(2*E-1)/(E-1)**2
zero(prim-prim.subs(E,E+1)-AP,'p2 forward primitive ratio')
zero(prim.subs(E,E-1)-prim-AM,'p2 backward primitive ratio')
zero(E*(f.subs(E,E-1)-f)/f-DE,'p2 backward difference ratio')
zero(s.diff(DE,E)-(1-3*E)/(E-1)**3,'D(E) derivative sign formula')
zero(F(5,2)-DE-(E*E-8*E+5)/(2*(E-1)**2),'m>=8 finite cancellation threshold')
W=A*f+k*prim
zero(gen(W)-direct.subs({phi:f,pp:f.subs(E,E+1),pm:f.subs(E,E-1),alpha_p:AP,alpha_m:AM}),'p2 generator via separate function shift')
for name,rate,nu in channels:
 zero(dz(W,nu)-jumps[name].subs({phi:f,pp:f.subs(E,E+1),pm:f.subs(E,E-1),alpha_p:AP,alpha_m:AM}),'p2 actual jump: '+name)
# Rational scalar checks near the one-step limit and well above it.
scalar_cases=0
for p in (2,3,4,7,17):
 for ee in sorted(set([4*p,4*p+1,4*p+2,8*p,64*p,1000*p])):
  f=F(1,ee)**p;dp=F(1,ee+1)**p-f;dm=F(1,ee-1)**p-f
  ap=(F(1,ee)**(p-1)-F(1,ee+1)**(p-1))/(p-1)
  am=(F(1,ee-1)**(p-1)-F(1,ee)**(p-1))/(p-1)
  assert 0<=-dp<=F(p,ee)*f and 0<=dm<=F(2*p,ee)*f
  assert F(3,4)*f<=ap<=f and f<=am<=2*f
  scalar_cases+=1

def concrete_rates(state):
 out=[]
 for _,react,prod,k in R:
  r=k
  for i,v in enumerate(V):
   for j in range(react.get(str(v),0)):r*=state[i]-j
  out.append(r)
 return out

def eval_state(state,p,k,J):
 aa,bb,cc,dd,ee=state
 def w(z):return F(z[0],z[4]**p)+k*F(1,(p-1)*z[4]**(p-1))
 w0=w(state);gw=F(0);qw=F(0);active=0
 for (_,rate,nu),r in zip(channels,concrete_rates(state)):
  if r==0:continue
  y=tuple(v+d for v,d in zip(state,nu)); assert min(y)>=0 and y[4]>0
  delta=w(y)-w0;assert abs(delta)<=J*F(1,ee**p)
  assert w(y)>=0
  gw+=r*delta;qw+=r*delta*delta;active+=1
 return gw,qw,active
fixed_cases=trade_cases=active_rows=0
for p in (2,3,7):
 for aa in (0,1,2,3,13,97):
  for cc in (0,1,2,17):
   for dd in (0,1,3,19):
    for ee in (4*p,4*p+1,50*p):
     for extra in (0,1):
      bb=2*(cc+dd+4*p*aa+12*ee)+extra
      J=7+F(2*p*(aa+1),ee);f=F(1,ee**p)
      gw,qw,n=eval_state((aa,bb,cc,dd,ee),p,F(3),J)
      assert gw<=f*(1-F(aa*bb,2)-cc*dd)
      assert qw<=J*J*f*f*(1+3*aa*bb+3*cc*dd)
      fixed_cases+=1;active_rows+=n
for m in (8,9,100):
 a=F(m,m+1);b=F(m,m-1);d=F(m*(2*m-1),(m-1)**2)
 for k in (F(3*(m+1),2*m)+F(1,100),F(2),F(3)):
  sigma=2*k*a-3;assert sigma>0
  for theta in (F(1,10),F(1,2)):
   for aa in (0,1,2,13,101):
    for cc in (0,1,23):
     for dd in (0,1,29):
      for ee in (m,m+1,9*m):
       ll=aa+F(cc+dd,2);bb=math.ceil((2+2*ll+2*k*b*ee)/(1-theta))
       J=1+k*b+d*F(aa+1,ee);f=F(1,ee**2)
       gw,qw,n=eval_state((aa,bb,cc,dd,ee),2,k,J)
       CB=1+F(3,2)*(1-theta)
       assert gw<=f*(1-theta*aa*bb-sigma*cc*dd)
       assert qw<=J*J*f*f*(1+CB*aa*bb+3*cc*dd)
       trade_cases+=1;active_rows+=n
# Literal E/B=.2 admissible lattice point, with A an order-B fraction.
state=(30,1000,70,70,200);aa,bb,cc,dd,ee=state;ll=aa+F(cc+dd,2)
m=100;k=F(8,5);theta=F(1,10);a=F(100,101);b=F(100,99);d=F(19900,9801);sigma=F(17,101)
assert ll/bb==F(1,10) and F(ee,bb)==F(1,5)
assert 2+2*ll+2*k*b*ee<=(1-theta)*bb
assert F(1,50)+F(1,5)+F(64,99)==F(4289,4950)<F(9,10)
assert 2*k*a-3==sigma and max(F(17),3/sigma)==F(303,17)
J=1+k*b+d*F(aa+1,ee);gw,qw,n=eval_state(state,2,k,J)
assert gw<=F(1,ee**2)*(1-theta*aa*bb-sigma*cc*dd)
active_rows+=n
# A literal nonempty padded growing-cone instance at the moderate ratio.
TT=10;NN=TT**5;AA=3000;BB=100000;CC=DD=7000;EE=20000
e0=F(2);nu=F(1,5);g=F(2);H=F(3);c=F(1);kap=F(1,TT**3)
ev=F(EE,TT**3);lv=(AA+F(CC+DD,2))/TT
assert e0<=ev<=nu*TT**2 and BB>=c*NN and EE>=100
assert g*(ev+kap)**2+F(1,TT)<=lv<=H*(ev-kap)**2-F(1,TT)
assert F(2,NN)+2*H*nu**2+2*k*b*nu<=(1-theta)*c
report={'status':'PASS','basis':'Supplementary exact algebra and rational checks; see ordinary proof receipt.',
 'exact_assertion_groups':len(checks),'symbolic_identity_assertions':len(checks)-len(channels),'reaction_structure_groups':len(channels),'assertion_labels':checks,'finite_scalar_cases':scalar_cases,
 'fixed3_rational_states':fixed_cases,'tradeoff_rational_states':trade_cases,'active_channel_cases':active_rows,
 'moderate_ratio_lattice_state':state,'moderate_ratio_L_over_B':'1/10','moderate_ratio_E_over_B':'1/5',
 'scope':'Actual stopped weighted occupations only; no cone admission, cone survival, imbalance, clearance, recurrence, or mixing conclusion.'}
(HERE/'independent_exact_results.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
