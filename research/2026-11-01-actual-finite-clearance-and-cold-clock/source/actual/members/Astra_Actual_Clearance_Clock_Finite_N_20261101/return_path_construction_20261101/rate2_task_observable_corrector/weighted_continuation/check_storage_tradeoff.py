#!/usr/bin/env python3
from fractions import Fraction as F
from pathlib import Path
import json, math
import sympy as s
A,B,C,D,E,T,k=s.symbols('A B C D E T k',positive=True)
x=(A,B,C,D,E);L=A+(C+D)/2;a2=A*(A-1);ae=A*E
channels=[('0->A',1,(1,0,0,0,0)),('A->0',A,(-1,0,0,0,0)),('2A->AC',a2,(-1,0,1,0,0)),('AC->2A',A*C,(1,0,-1,0,0)),('2A->AD',a2,(-1,0,0,1,0)),('AD->2A',A*D,(1,0,0,-1,0)),('2A->AE',a2,(-1,0,0,0,1)),('AE->2A',ae,(1,0,0,0,-1)),('AE->CD',ae,(-1,0,1,1,-1)),('CD->AE',2*C*D,(1,0,-1,-1,1)),('CD->AB',C*D,(1,1,-1,-1,0)),('AB->CD',A*B,(-1,-1,1,1,0))]
def shift(f,nu):return f.subs({v:v+d for v,d in zip(x,nu)},simultaneous=True)
def delta(f,nu):return shift(f,nu)-f
def G(f):return sum(rate*delta(f,nu) for _,rate,nu in channels)
checks=[]
def zero(expr,label):
 assert s.cancel(expr)==0,label
 checks.append(label)
phi=(E/T**3)**-2;psi=T**3/E;W=A*phi+k*T**3*psi
dp=phi.subs(E,E+1)-phi;dm=phi.subs(E,E-1)-phi
ap=T**3*(psi-psi.subs(E,E+1));am=T**3*(psi.subs(E,E-1)-psi)
GA=1+2*A-5*A*A+2*A*L+3*C*D-A*B
K=a2*(A-1)+2*C*D*(A+1)
GW=phi*GA+K*dp+2*A*A*E*dm-k*(a2+2*C*D)*ap+2*k*A*E*am
zero(G(A)-GA,'full A generator with exact -5A^2 term')
zero(ap/phi-E/(E+1),'exact forward primitive ratio')
zero(am/phi-E/(E-1),'exact backward primitive ratio')
DE=E*(2*E-1)/(E-1)**2
zero(E*dm/phi-DE,'exact backward derivative loss')
zero(G(W)-GW,'full arbitrary-k weighted generator')
reorganized=phi*(1+A*(2+2*L+2*k*E/(E-1)*E-B)+(2*DE-5)*A*A+(3-2*k*E/(E+1))*C*D)+K*dp-k*a2*E/(E+1)*phi
zero(GW-reorganized,'exact full A^2/source/capture decomposition')
jumpmap={'2A->AE':-phi+(A-1)*dp-k*ap,'CD->AE':phi+(A+1)*dp-k*ap,'AE->2A':phi+(A+1)*dm+k*am,'AE->CD':-phi+(A-1)*dm+k*am}
for name,rate,nu in channels:zero(delta(W,nu)-jumpmap.get(name,nu[0]*phi),f'arbitrary k jump: {name}')
zero(sum(rate for _,rate,nu in channels)-(1+A*B+3*C*D+A*A-2*A+2*A*L+2*A*E),'exact total rate compressed')
assert F(1,50)+F(1,5)+F(64,99)==F(4289,4950)<F(9,10)
assert 2*F(8,5)*F(100,101)-3==F(17,101)
assert max(F(17),F(303,17))==F(303,17)
state_checks=0;m=100;am=F(m,m+1);bm=F(m,m-1);dmcap=F(m*(2*m-1),(m-1)**2);theta=F(1,10)
assert dmcap<=F(5,2)
for kk in (F(8,5),F(2),F(3)):
 sigma=2*kk*am-3;assert sigma>0
 for aa in (0,1,2,7,20,100):
  for cc in (0,1,5,31):
   for dd in (0,1,5,31):
    for ee in (m,m+1,2*m,5*m,20*m):
     ll=F(2*aa+cc+dd,2)
     base=(2+2*ll+2*kk*bm*ee)/(1-theta)
     bb=(base.numerator+base.denominator-1)//base.denominator
     xx=(aa,bb,cc,dd,ee);t3=8;ev=F(ee,t3);ph=ev**-2
     def w(st):
      a,b,c,d,z=st;e=F(z,t3)
      return a/e**2+kk*t3/e
     rates=[1,aa,aa*(aa-1),aa*cc,aa*(aa-1),aa*dd,aa*(aa-1),aa*ee,aa*ee,2*cc*dd,cc*dd,aa*bb]
     gw=F(0);qw=F(0);jstate=1+kk*bm+dmcap*F(aa+1,ee)
     for (name,_,nu),rate in zip(channels,rates):
      if not rate:continue
      yy=tuple(v+d for v,d in zip(xx,nu));assert min(yy)>=0
      jump=w(yy)-w(xx);assert abs(jump)<=jstate*ph
      gw+=rate*jump;qw+=rate*jump*jump
     assert gw<=ph-theta*aa*bb*ph-sigma*cc*dd*ph
     CB=1+F(3,2)*(1-theta)
     assert qw<=jstate*jstate*ph*ph*(1+CB*aa*bb+3*cc*dd)
     state_checks+=1
report={'status':'PASS','symbolic_check_count':len(checks),'symbolic_checks':checks,'exact_rational_state_checks':state_checks,'tested_k':['8/5','2','3'],'moderate_ratio_gate':{'k':'8/5','m':100,'theta':'1/10','sigma':'17/101','gate_lhs_upper':'4289/4950','gate_rhs':'9/10','C_Q':'303/17'},'scope':'Storage coefficient tradeoff only; no cone admission, exit, or clearance certificate.'}
Path(__file__).with_name('storage_tradeoff_checks.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
