#!/usr/bin/env python3
"""Exact full-chain checks of the weighted source-time storage.
No simulation, equilibrium law, or deterministic time substitution.
"""
from fractions import Fraction as F
from pathlib import Path
import json
import sympy as s
A,B,C,D,E,T=s.symbols('A B C D E T',positive=True)
x=(A,B,C,D,E); a2=A*(A-1); ae=A*E
channels=[('0->A',1,(1,0,0,0,0)),('A->0',A,(-1,0,0,0,0)),
('2A->AC',a2,(-1,0,1,0,0)),('AC->2A',A*C,(1,0,-1,0,0)),
('2A->AD',a2,(-1,0,0,1,0)),('AD->2A',A*D,(1,0,0,-1,0)),
('2A->AE',a2,(-1,0,0,0,1)),('AE->2A',ae,(1,0,0,0,-1)),
('AE->CD',ae,(-1,0,1,1,-1)),('CD->AE',2*C*D,(1,0,-1,-1,1)),
('CD->AB',C*D,(1,1,-1,-1,0)),('AB->CD',A*B,(-1,-1,1,1,0))]
def sh(f,nu):return f.subs({v:v+d for v,d in zip(x,nu)},simultaneous=True)
def de(f,nu):return sh(f,nu)-f
def gen(f):return sum(rate*de(f,nu) for _,rate,nu in channels)
checks=[]
def check_zero(expr,label):
 assert s.cancel(expr)==0,label
 checks.append(label)
GA=1-A-3*a2+A*(C+D)+3*C*D-A*B
check_zero(gen(A)-GA,'full A generator, all 12 channels')
for p in (2,3,5):
 phi=(E/T**3)**(-p);psi=(E/T**3)**(1-p)/F(p-1)
 dp=phi.subs(E,E+1)-phi;dm=phi.subs(E,E-1)-phi
 ap=T**3*(psi-psi.subs(E,E+1));am=T**3*(psi.subs(E,E-1)-psi)
 W=A*phi+3*T**3*psi
 K=a2*(A-1)+2*C*D*(A+1)
 weighted=phi*GA+K*dp+2*A*A*E*dm
 check_zero(gen(A*phi)-weighted,f'p={p}: exact weighted A product generator')
 check_zero(gen(T**3*psi)-(-(a2+2*C*D)*ap+2*A*E*am),f'p={p}: exact primitive generator')
 GW=weighted-3*(a2+2*C*D)*ap+6*A*E*am
 check_zero(gen(W)-GW,f'p={p}: full storage generator')
 slack=(A*phi*(B/2-C-D-4*p*A-12*E)+A*phi+3*a2*phi+3*a2*ap-K*dp
        +(4*p*A*A*phi-2*A*A*E*dm)+(12*A*E*phi-6*A*E*am)+C*D*(6*ap-4*phi))
 check_zero(phi-A*B*phi/2-C*D*phi-GW-slack,f'p={p}: nonnegative drift slack decomposition')
 jumpmap={'2A->AE':-phi+(A-1)*dp-3*ap,'CD->AE':phi+(A+1)*dp-3*ap,
          'AE->2A':phi+(A+1)*dm+3*am,'AE->CD':-phi+(A-1)*dm+3*am}
 qdirect=sum(rate*de(W,nu)**2 for _,rate,nu in channels)
 qtable=0
 for name,rate,nu in channels:
  pred=jumpmap.get(name,nu[0]*phi)
  check_zero(de(W,nu)-pred,f'p={p}: {name} exact storage jump')
  qtable+=rate*pred**2
 check_zero(qdirect-qtable,f'p={p}: exact bracket from complete jump table')
# Fraction-only checks avoid numerical tolerance and check every active endpoint.
state_count=0
for p in (2,3,5):
 for aa in (0,1,2,7,20):
  for cc in (0,1,5,11):
   for dd in (0,1,5,11):
    for ee in (4*p,4*p+1,8*p,16*p,64*p):
     for margin in (0,1,50):
      bb=2*(cc+dd+4*p*aa+12*ee)+margin
      xx=(aa,bb,cc,dd,ee);t3=8
      def weight(state):
       a,b,c,d,Ee=state;ev=F(Ee,t3)
       return a*ev**(-p)+3*t3*ev**(1-p)/F(p-1)
      ev=F(ee,t3);ph=ev**(-p);dp=(ev+F(1,t3))**(-p)-ph;dm=(ev-F(1,t3))**(-p)-ph
      psi=lambda z:z**(1-p)/F(p-1)
      ap=t3*(psi(ev)-psi(ev+F(1,t3)));am=t3*(psi(ev-F(1,t3))-psi(ev))
      assert 0<=-dp<=F(p,ee)*ph
      assert 0<=dm<=F(2*p,ee)*ph
      assert F(3,4)*ph<=ap<=ph and ph<=am<=2*ph
      rates=[1,aa,aa*(aa-1),aa*cc,aa*(aa-1),aa*dd,aa*(aa-1),aa*ee,aa*ee,2*cc*dd,cc*dd,aa*bb]
      GW=F(0);qW=F(0);jstate=7+F(2*p*(aa+1),ee)
      for (name,_,nu),rate in zip(channels,rates):
       if not rate:continue
       yy=tuple(z+d for z,d in zip(xx,nu));assert min(yy)>=0
       jump=weight(yy)-weight(xx)
       assert abs(jump)<=jstate*ph,(p,name,xx)
       GW+=rate*jump;qW+=rate*jump*jump
      assert GW<=ph-(F(aa*bb,2)+cc*dd)*ph
      assert qW<=jstate*jstate*ph*ph*(1+3*aa*bb+3*cc*dd)
      state_count+=1
report={'status':'PASS','model_channels':12,'symbolic_check_count':len(checks),'symbolic_checks':checks,'exact_rational_state_checks':state_count,'tested_exponents':[2,3,5],'scope':'Weighted source-time author component only; no independent review, cone admission, imbalance control, or clearance result.'}
Path(__file__).with_name('weighted_exact_checks.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
