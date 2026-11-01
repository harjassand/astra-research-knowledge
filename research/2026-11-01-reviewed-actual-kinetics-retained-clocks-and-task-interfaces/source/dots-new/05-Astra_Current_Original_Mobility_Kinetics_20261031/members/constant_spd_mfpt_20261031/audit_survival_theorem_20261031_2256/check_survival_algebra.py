#!/usr/bin/env python3
"""Exact independent spectral/source algebra; no candidate implementation import."""
import sympy as S
from fractions import Fraction as Q
from pathlib import Path
import hashlib,json
HERE=Path(__file__).resolve().parent
checks=[]
def eq(n,a,b=0):
 r=S.simplify(a-b);assert r==0,(n,r);checks.append(n)
def truth(n,a):
 assert a,n;checks.append(n)
x,u,s,eps=S.symbols('x u s eps',positive=True)
eq('Taylor positive-side integral',S.integrate((x-u)/u**2,(u,1,x)),x-1-S.log(x))
eq('Taylor negative-side integral',S.integrate((u-x)/u**2,(u,x,1)),x-1-S.log(x))
eq('log inequality derivative',S.diff(S.log(x)-1+1/x,x),(x-1)/x**2)
eq('weighted squared-deviation identity',(x-1)**2/x,x+1/x-2)
eq('log-to-weighted-variance gap',(x-1)**2/x-(x-1-S.log(x)),S.log(x)-1+1/x)
eq('Taylor scale maximizer derivative',S.diff(s*s*S.exp(-s*u),s),s*S.exp(-s*u)*(2-s*u))
eq('Taylor maximum',(s*s*S.exp(-s*u)).subs(s,2/u),4/(S.E**2*u*u))
eq('first-moment deficit bound identity',1-1/(1+eps),eps/(1+eps))
truth('e lower series partial sum',sum(Q(1,S.factorial(j)) for j in range(4))==Q(8,3))
truth('exact rational coefficient sufficient',Q(3,8)+Q(9,16)==Q(15,16)<1)
truth('rate midpoint rational constant',Q(1,2)/Q(8,3)==Q(3,16))
# Many rational distributions: exact moment conditions and algebra, not sampled exponential proof.
for n in range(1,9):
 for shift in range(1,9):
  weights=[Q(j+shift) for j in range(1,n+1)];sw=sum(weights);weights=[w/sw for w in weights]
  rates=[Q((j+shift)**2,j+1) for j in range(1,n+1)]
  mean=sum(w*r for w,r in zip(weights,rates));rates=[r/mean for r in rates]
  for factor in [Q(1),Q(9,10),Q(1,2)]:
   xx=[factor*r for r in rates]
   ex=sum(w*r for w,r in zip(weights,xx));ei=sum(w/r for w,r in zip(weights,xx));ee=ei-1
   truth('moment input '+str((n,shift,factor)),ex<=1 and ei>=1 and ee>=0)
   truth('first moment deficit '+str((n,shift,factor)),1-ex<=ee/(1+ee))
   vv=sum(w*(r-1)**2/r for w,r in zip(weights,xx))
   truth('weighted variance identity '+str((n,shift,factor)),vv==ex+ei-2)
   truth('weighted variance bound '+str((n,shift,factor)),0<=vv<=ee)
# Weighted finite reversible star/chain fixtures: exact form/inverse moments.
for massS in [S.Rational(1,100),S.Rational(1,10),S.Rational(1),S.Rational(4)]:
 for ca,cb,cs in [(1,1,1),(1,0,3),(2,3,5),(7,1,2)]:
  M=S.Rational(1);D=S.diag(M,massS);rho=massS/M
  H=S.Matrix([[ca+cb,-ca],[-ca,ca+cs]])
  K=D.inv()*H;Ki=K.inv();a=S.Matrix([1,0]);g=S.ones(2,1);ss=S.Matrix([0,1])
  QA=(a.T*D*Ki*a)[0];QS=(ss.T*D*Ki*ss)[0];QAS=(a.T*D*Ki*ss)[0]
  BA=max(QA,QS/rho**2)
  for hv in [S.Rational(ca,ca+cs),S.Rational(1,4),S.Rational(3,4)]:
   h=S.Matrix([1,hv]);N=(h.T*D*h)[0];C0=(h.T*H*h)[0];Qh=(h.T*D*Ki*h)[0];QD=(g.T*D*Ki*g)[0]
   ee=C0*BA*(1+rho)**2/M**2-1;k0=C0/M
   truth('weighted selfadjoint '+str((massS,ca,cb,cs,hv)),D*K==K.T*D)
   truth('source cross Cauchy '+str((massS,ca,cb,cs,hv)),0<=QAS and QAS**2<=QA*QS)
   truth('source domination '+str((massS,ca,cb,cs,hv)),Qh<=QD<=BA*(1+rho)**2)
   truth('epsilon nonnegative '+str((massS,ca,cb,cs,hv)),ee>=0)
   truth('spectral first moment '+str((massS,ca,cb,cs,hv)),C0/(N*k0)<=1)
   truth('spectral inverse moment '+str((massS,ca,cb,cs,hv)),k0*Qh/N<=1+ee)
   truth('form inverse Cauchy '+str((massS,ca,cb,cs,hv)),C0*Qh>=N*N)
# Initial-law difference identity for arbitrary linear operator.
p00,p01,p10,p11,hv,ms=S.symbols('p00 p01 p10 p11 hv ms',real=True)
P=S.Matrix([[p00,p01],[p10,p11]]);D=S.diag(1,ms)
a=S.Matrix([1,0]);h=S.Matrix([1,hv]);g=S.ones(2,1);e=h-a;d=g-h
eq('exact initialization difference',(a.T*D*P*g)[0]-(h.T*D*P*h)[0],(a.T*D*P*d)[0]-(e.T*D*P*h)[0])
# Explicit heavy spectral tail satisfying arbitrarily sharp moment hypotheses.
delta=S.symbols('delta',positive=True)
aa=(1-2*delta/3)/(1-delta)
eq('heavy-tail spectral mean',(1-delta)*aa+delta*S.integrate(2*x*x,(x,0,1)),1)
eq('heavy-tail inverse excess',(1-delta)/aa+2*delta-1,delta*(2-delta)/(3-2*delta))
eq('heavy-tail transform',S.integrate(2*x*S.exp(-s*x),(x,0,1)),2*(1-(1+s)*S.exp(-s))/s**2)
for de in [S.Rational(1,1000),S.Rational(1,100),S.Rational(1,10),S.Rational(1,2)]:
 ee=(delta*(2-delta)/(3-2*delta)).subs(delta,de)
 truth('heavy-tail small excess '+str(de),0<ee<=de)
# Source unchanged; no numerical KS figure is accepted.
row=json.loads((HERE/'input_hash.json').read_text());data=(HERE.parent/row['source']).read_bytes()
truth('frozen root source binding',hashlib.sha256(data).hexdigest()==row['sha256'] and len(data)==row['bytes'])
report={'status':'PASS','exact_assertions':len(checks),'scope':'theorem algebra and exact finite fixtures only; no candidate executable or numerical KS bound accepted','checks':checks}
(HERE/'check_results.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='checks'},indent=2))
