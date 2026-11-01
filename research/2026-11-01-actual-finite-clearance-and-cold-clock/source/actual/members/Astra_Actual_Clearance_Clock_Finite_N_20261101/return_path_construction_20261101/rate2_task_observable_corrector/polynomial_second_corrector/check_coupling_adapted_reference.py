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
lambda0=1+3*L*L-3*Z*Z/4;k=n+2*L-E-2;beta=E
Qc=lambda f:(lambda0+beta*A)*(f.subs(A,A+1)-f)+(k+beta)*A*(f.subs(A,A-1)-f)
checks=[]
def zero(expr,label):
 assert s.cancel(expr)==0,label
 checks.append(label)
zero(G(A)-(lambda0-k*A-3*A*A),'exact full A drift matched to coupling reference')
zero(G(A*A)-Qc(A*A)-(-6*A**3+5*A*A-8*L*A),'exact second moment mismatch with AE variance canceled')
zero(sum(rate for _,rate,nu in rows if nu[0]==1)-(lambda0+E*A)-(A*A-4*A*L),'actual upward reference discrepancy')
zero(sum(rate for _,rate,nu in rows if nu[0]==-1)-(k+E)*A-(4*A*A-4*A*L),'actual downward reference discrepancy')
mu=lambda0/k;ac=r2/(2*k);bc=(r1+r2*(mu+s.Rational(1,2)+E/k))/k
zero(Qc(ac*A*A+bc*A)+r0+r1*A+r2*A*A-(r0+r1*mu+r2*(mu*mu+mu*(1+E/k))),'exact quadratic inverse including branching variance')
zero(G(A*A)-Qc(A*A)+6*A**3-5*A*A+8*L*A,'frozen quadratic mismatch')
R=E*E/(N*L);q=R/k;chi=-A*q
zero(Qc(chi)-(R*A-R*lambda0/k),'linear reference cancellation with honest mean')
zero(-q*(G(A)-Qc(A))-3*R*A*A/k,'positive frozen linear discrepancy')
neg={'A->0','2A->AC','2A->AD','2A->AE','CD->AE'}
for name,rate,nu in rows:
 dk=nu[4]+2*nu[1]-nu[2]
 zero(sh(k,nu)-k-dk,f'exact k jump {name}')
 zero(sh(lambda0,nu)-lambda0-(6*L*nu[1]+3*nu[1]**2-s.Rational(3,2)*Z*nu[3]-s.Rational(3,4)*nu[3]**2),f'exact lambda0 jump {name}')
 zero(sh(q,nu)-q-(sh(R,nu)-R-R*dk/k)/(k+dk),f'exact quotient jump {name}')
 frozen=-nu[0]*q;param=-(A+nu[0])*(sh(q,nu)-q)
 zero(sh(chi,nu)-chi-frozen-param,f'linear actual/frozen/parameter split {name}')
zero(sum(rate*(A+nu[0])*abs(nu[1]) for name,rate,nu in rows if name in neg)-a2*(2*A-1),'negative row L-weight polynomial')
zero(sum(rate*(A+nu[0])*abs(nu[2]) for name,rate,nu in rows if name in neg)-(a2*(A-1)+2*cd*(A+1)),'negative row E-weight polynomial')
zero(sum(rate*(A+nu[0])*abs(nu[4]+2*nu[1]-nu[2]) for name,rate,nu in rows if name in neg)-(a2*(5*A-2)+2*cd*(A+1)),'negative row k-weight polynomial')
state_checks=0
for aa in (0,1,2,5,10):
 for cc in (2,3,10):
  for dd in (2,3,10):
   for ee in (2,5,20):
    for bb in (10,100):
     NN=1000;ll=F(2*aa+cc+dd,2);zz=cc-dd;nn=aa+bb+cc+dd+ee
     kk=nn+2*ll-ee-2;assert kk>3
     rr=F(ee*ee,NN)/ll;xx=(aa,ll,ee,zz,nn)
     rates=[1,aa,aa*(aa-1),aa*cc,aa*(aa-1),aa*dd,aa*(aa-1),aa*ee,aa*ee,2*cc*dd,cc*dd,aa*bb]
     def qv(st):a,l,e,z,n=st;return F(e*e,NN)/(l*(n+2*l-e-2))
     def cv(st):return -st[0]*qv(st)
     ell0=F(2);mm=F(2);lam=ll/NN;nu=F(ee,NN);eta=ll/ee;c0=ell0/(ell0-1);cm=2+1/mm
     jc=rr/kk+rr/(kk-3)*(c0*(1+1/ell0)+c0*cm*(eta+1/mm)+3*(lam*NN+1)/kk)
     pminus=F(0);param=F(0);qchi=F(0)
     for (name,rateexpr,jump),rate in zip(rows,rates):
      if not rate:continue
      jt=tuple(F(v) for v in jump);yy=tuple(v+d for v,d in zip(xx,jt))
      dq=qv(yy)-qv(xx);part=-rate*(aa+jt[0])*dq
      if name in neg:assert part<=0;pminus-=part
      else:assert part>=0
      param+=part
      dj=cv(yy)-cv(xx);assert abs(dj)<=jc;qchi+=rate*dj*dj
     assert param>=-pminus
     bound=rr/(kk-3)*(c0*(2*lam*NN+3*cm*lam*eta*NN)*aa+2*c0*cm*cc*dd/mm+(7*lam*lam*NN*NN*aa+2*cc*dd)/kk)
     assert pminus<=bound
     vb=jc*jc*(1+aa*bb+3*cc*dd+(3*lam+2*nu)*NN*aa)
     assert qchi<=vb
     assert abs(cv(xx))<=F(ee*ee,NN)/kk
     state_checks+=1
report={'status':'PASS','symbolic_check_count':len(checks),'symbolic_checks':checks,'exact_rational_state_checks':state_checks,'scope':'Coupling-adapted algebra and conditional one-sided correction costs; E1, cone/imbalance admission, and clearance unproved.'}
Path(__file__).with_name('coupling_adapted_checks.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
