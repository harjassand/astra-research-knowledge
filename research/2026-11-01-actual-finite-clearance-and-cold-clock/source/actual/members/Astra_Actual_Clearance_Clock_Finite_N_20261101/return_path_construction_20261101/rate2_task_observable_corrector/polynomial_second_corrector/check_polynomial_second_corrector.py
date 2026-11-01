#!/usr/bin/env python3
from fractions import Fraction as F
from pathlib import Path
import json
import sympy as s
A,L,E,Z,n,N,r0,r1,r2=s.symbols('A L E Z n N r0 r1 r2')
x=(A,L,E,Z,n);a2=A*(A-1);cd=(L-A)**2-Z**2/4;B=n-2*L+A-E
rows=[('0->A',1,(1,1,0,0,1)),('A->0',A,(-1,-1,0,0,-1)),('2A->AC',a2,(-1,-s.Rational(1,2),0,1,0)),('AC->2A',A*(L-A+Z/2),(1,s.Rational(1,2),0,-1,0)),('2A->AD',a2,(-1,-s.Rational(1,2),0,-1,0)),('AD->2A',A*(L-A-Z/2),(1,s.Rational(1,2),0,1,0)),('2A->AE',a2,(-1,-1,1,0,0)),('AE->2A',A*E,(1,1,-1,0,0)),('AE->CD',A*E,(-1,0,-1,0,0)),('CD->AE',2*cd,(1,0,1,0,0)),('CD->AB',cd,(1,0,0,0,0)),('AB->CD',A*B,(-1,0,0,0,0))]
def sh(f,nu):return f.subs({v:v+d for v,d in zip(x,nu)},simultaneous=True)
def G(f):return sum(rate*(sh(f,nu)-f) for _,rate,nu in rows)
def Q(f):return 3*L**2*(f.subs(A,A+1)-f)+N*A*(f.subs(A,A-1)-f)
checks=[]
def zero(expr,label):
 assert s.cancel(expr)==0,label
 checks.append(label)
mu=3*L**2/N;alpha=r2/(2*N);beta=(r1+r2*(mu+s.Rational(1,2)))/N
chi=alpha*A*A+beta*A
zero(Q(chi)+r0+r1*A+r2*A*A-(r0+r1*mu+r2*(mu*mu+mu)),'degree-two algebraic inverse')
dp=1+A*E-4*A*L+A*A-3*Z*Z/4;dm=A*(n-N-2*L+4*A-2)
zero(sum(rate for _,rate,nu in rows if nu[0]==1)-3*L**2-dp,'actual upward reference difference')
zero(sum(rate for _,rate,nu in rows if nu[0]==-1)-N*A-dm,'actual downward reference difference')
ac=L+2*E+3*Z+n;bc=L*L+E*n+Z*Z;test=ac*A*A+bc*A
parameter=sum(rate*((A+nu[0])**2*(sh(ac,nu)-ac)+(A+nu[0])*(sh(bc,nu)-bc)) for _,rate,nu in rows)
fast=dp*(ac*(2*A+1)+bc)+dm*(ac*(-2*A+1)-bc)
zero(G(test)-Q(test)-fast-parameter,'parameter-motion identity with nonconstant coefficients')
R=E*E/(N*L);chi=-A*R/N
parameter=-sum(rate*(A+nu[0])*(sh(R,nu)-R) for _,rate,nu in rows)/N
fast=R/N*(-1+A*(n-N)+2*A*L+3*A*A-2*A-A*E+3*Z*Z/4)
zero(G(chi)-(R*A-3*R*L*L/N)-fast-parameter,'linear second corrector exact actual decomposition')
for name,rate,nu in rows:
 u,v=nu[1:3]
 pred=R*(2*v/E+v*v/E**2-u/L)/(1+u/L)
 zero(sh(R,nu)-R-pred,f'exact ratio finite jump {name}')
F1=R*(1-A*E/(N*L));D0=E*L/N*(4-3*R)-R/L
poly=s.Poly(s.cancel(G(F1)-D0),A)
assert poly.degree()==3
checks.append('exact F1 residual has degree three, not two')
# Rational state checks of all extra-charge/jump bounds.
state_checks=0
for aa in (0,1,2,5,10):
 for cc in (2,3,10):
  for dd in (2,3,10):
   for ee in (2,5,20):
    for bb in (10,100):
     NN=1000;ll=F(2*aa+cc+dd,2);zz=cc-dd;nn=aa+bb+cc+dd+ee
     rr=F(ee*ee,NN)/ll;xx=(aa,ll,ee,zz,nn)
     rates=[1,aa,aa*(aa-1),aa*cc,aa*(aa-1),aa*dd,aa*(aa-1),aa*ee,aa*ee,2*cc*dd,cc*dd,aa*bb]
     def rv(st):a,l,e,z,n=st;return F(e*e,NN)/l
     def cv(st):return -st[0]*rv(st)/NN
     er=F(0);qchi=F(0);rate_sum=0
     ell0=F(2);mm=F(2);lam=ll/NN;nu=F(ee,NN);eta=ll/ee;dn=abs(nn-NN);c0=ell0/(ell0-1);cm=2+1/mm
     jc=rr/NN*(1+c0*(1+1/ell0)+c0*cm*(eta+1/mm))
     for (_,_,jump),rate in zip(rows,rates):
      if not rate:continue
      jtuple=tuple(F(v) for v in jump);yy=tuple(v+d for v,d in zip(xx,jtuple))
      dr=rv(yy)-rr;dchi=cv(yy)-cv(xx)
      dl=rr/(ll-1);de=rr*ll/(ll-1)*(F(2,ee)+F(1,ee*ee))
      assert abs(dr)<=dl*abs(jtuple[1])+de*abs(jtuple[2])
      assert abs(dchi)<=jc
      er-=rate*(aa+jtuple[0])*dr/NN;qchi+=rate*dchi*dchi;rate_sum+=rate
     ef=rr/NN*(-1+aa*(nn-NN)+2*aa*ll+3*aa*aa-2*aa-aa*ee+F(3,4)*zz*zz)
     fast_bound=rr*(F(1,NN)+(F(dn,NN)+5*lam+nu+F(2,NN))*aa+F(3*zz*zz,4*NN))
     param_bound=c0*rr*(1/(NN*ell0)+(3*lam+nu*(1+1/ell0)+(4+2/ell0)/NN+cm*(3*lam*eta+2*lam+(eta+2)/NN))*aa+2*cm*cc*dd/(NN*mm))
     assert abs(ef)<=fast_bound
     assert abs(er)<=param_bound
     vb=jc*jc*(1+aa*bb+3*cc*dd+(3*lam+2*nu)*NN*aa)
     assert qchi<=vb
     assert abs(cv(xx))<=nu*nu
     state_checks+=1
report={'status':'PASS','symbolic_checks':checks,'symbolic_check_count':len(checks),'exact_rational_state_checks':state_checks,'exact_first_ratio_residual_degree':poly.degree(),'scope':'Algebraic inverse and linear second-corrector charges; E1, imbalance, cone admission, and clearance remain unproved.'}
Path(__file__).with_name('polynomial_second_checks.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
