#!/usr/bin/env python3
"""Exact symbolic checks of the full 12-channel task-observable corrector.
No simulation and no fast-state equilibrium assumption.
"""
import json
from pathlib import Path
import sympy as s
A,B,C,D,E,N,T,l,e=s.symbols('A B C D E N T l e', positive=True)
x=(A,B,C,D,E)
a2=A*(A-1); h=A*E; L=A+(C+D)/2; Z=C-D; n=sum(x)
channels=[
 ('0->A',1,(1,0,0,0,0)), ('A->0',A,(-1,0,0,0,0)),
 ('2A->AC',a2,(-1,0,1,0,0)), ('AC->2A',A*C,(1,0,-1,0,0)),
 ('2A->AD',a2,(-1,0,0,1,0)), ('AD->2A',A*D,(1,0,0,-1,0)),
 ('2A->AE',a2,(-1,0,0,0,1)), ('AE->2A',h,(1,0,0,0,-1)),
 ('AE->CD',h,(-1,0,1,1,-1)), ('CD->AE',2*C*D,(1,0,-1,-1,1)),
 ('CD->AB',C*D,(1,1,-1,-1,0)), ('AB->CD',A*B,(-1,-1,1,1,0)),
]
def shift(p,nu): return s.expand(p.subs({v:v+d for v,d in zip(x,nu)}, simultaneous=True))
def delta(p,nu): return s.expand(shift(p,nu)-p)
def G(p): return s.expand(sum(rate*delta(p,nu) for _,rate,nu in channels))
def gamma(p,q): return s.expand(sum(rate*delta(p,nu)*delta(q,nu) for _,rate,nu in channels))
def assert_zero(p,label):
    assert s.cancel(s.expand(p))==0,label
    checks.append(label)
checks=[]
assert len(channels)==12
assert_zero(G(A)-(1-A-3*a2+A*(C+D)+3*C*D-A*B),'full A generator')
assert_zero(G(L)-(1+A+A*L+h-3*A*A),'full L generator')
assert_zero(G(E)-(a2-2*h+2*C*D),'full E generator')
assert_zero(G(Z)+A*Z,'imbalance drift')
assert_zero(gamma(Z,Z)-(2*a2+A*(C+D)),'imbalance bracket')
assert_zero(gamma(Z,Z)-2*A*(L-1),'imbalance bracket compressed')
assert_zero(G(n)-(1-A),'total-count drift')
Q=2*A*L-A*A+Z*Z/4
assert_zero(Q-(L*L-C*D),'imbalance and fast-A geometric defect')
rh=E-3*E*Q+2*A*C*D+A*(A-1)**2+2*C*D+h*(N-B+2*L+2-7*A)
assert_zero(G(h)-(-N*h+3*E*L*L+rh),'full AE correction identity')
assert_zero(N-B+2*L+2-7*A-(N-n+E+4*L+2-8*A),'total-count residual compression')
qLL=1+A+s.Rational(3,2)*a2+A*(C+D)/4+h
qEE=a2+2*h+2*C*D
w=a2+h
assert_zero(gamma(L,L)-qLL,'L bracket')
assert_zero(gamma(E,E)-qEE,'E bracket')
assert_zero(gamma(L,E)+w,'signed L E covariation')
qhh=E**2*(1+A+2*a2+A*(C+D)+C*D+A*B)+a2*(A-E-1)**2+2*h*((E-1)**2+A*A)+2*C*D*(A+E+1)**2
assert_zero(gamma(h,h)-qhh,'AE bracket full 12 channels')
SL=1+A+2*a2+A*(C+D)/2+h
PL=E*((A+1)+a2+a2*(A-1)+A*(C+D)*(A+1)/2)+a2*(A-1)*(E+1)+h*(A+1)*(E-1)
PE=a2*(A-1)*(E+1)+2*A*h*(E-1)+2*C*D*(A+1)*(E+1)
assert_zero(sum(rate*abs(delta(L,nu)) for _,rate,nu in channels)-SL,'absolute L jump intensity')
assert_zero(sum(rate*shift(h,nu)*abs(delta(L,nu)) for _,rate,nu in channels)-PL,'weighted product L intensity')
assert_zero(sum(rate*shift(h,nu)*abs(delta(E,nu)) for _,rate,nu in channels)-PE,'weighted product E intensity')
assert_zero(sum(rate*abs(delta(L,nu)*delta(E,nu)) for _,rate,nu in channels)-w,'absolute L E covariance intensity')
subs={l:L/T,e:E/T**3}
for total in range(5):
    for i in range(total+1):
        j=total-i; f=l**i*e**j; g=s.diff(f,l)
        fx=f.subs(subs); gx=g.subs(subs)
        fl=s.diff(f,l).subs(subs); fe=s.diff(f,e).subs(subs)
        F=fx+h*gx/(N*T)
        R2=G(fx)-fl*G(L)/T-fe*G(E)/T**3
        P=sum(rate*shift(h,nu)*delta(gx,nu) for _,rate,nu in channels)/(N*T)
        residual=fl*(A+A*L-3*A*A)/T+fe*(a2-2*h-2*Q)/T**3+fl*rh/(N*T)+R2+P
        target=fl*(1/T+3*E*L*L/(N*T))+fe*2*L*L/T**3
        assert_zero(G(F)-target-residual,f'generic corrected observable monomial l^{i} e^{j}')
# Deterministic finite-state falsification tests of every pointwise polynomial bound.
checked_states=0
for aa in range(7):
 for bb in (0,1,7,100):
  for cc in range(5):
   for dd in range(5):
    for ee in range(5):
     xx=dict(zip(x,(aa,bb,cc,dd,ee))); ll=s.Rational(2*aa+cc+dd,2)
     hp=(aa+1)*(ee+1); rr=aa+ee+1
     vals=lambda p:s.expand(p).subs(xx)
     assert vals(Q)>=0
     assert abs(aa+aa*ll-3*aa*aa)<=aa+2*aa*ll
     assert abs(4*ll-8*aa)<=4*ll
     assert vals(PL)<=hp*vals(SL)
     assert vals(PE)<=hp*vals(qEE)
     for _,rate,nu in channels:
      if vals(rate):
       assert 0<=vals(shift(h,nu))<=hp
       assert abs(vals(delta(h,nu)))<=rr
     bound=ee**2*(1+aa+2*aa*aa+2*aa*ll+ll*ll+aa*bb)+rr**2*(aa*aa+2*aa*ee+2*ll*ll)
     assert vals(qhh)<=bound
     checked_states+=1
report={'status':'PASS','channels':12,'symbolic_checks':checks,'symbolic_check_count':len(checks),'polynomial_monomials_through_total_degree':4,'finite_state_bound_checks':checked_states,'scope':'Exact algebra and deterministic bound falsification; not an independent theorem review or clearance certificate.'}
out=Path(__file__).with_name('exact_checks.json'); out.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
