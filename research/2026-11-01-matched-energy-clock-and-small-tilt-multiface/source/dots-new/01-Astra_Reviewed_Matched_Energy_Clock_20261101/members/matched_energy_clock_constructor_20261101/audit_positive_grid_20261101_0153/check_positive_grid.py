"""Independent algebra of positive scalar receiving. No candidate implementation."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json
import sympy as s
P=Path(__file__).resolve().parent;checks=[]
def ok(label,b):
 assert b,label
 checks.append(label)
def eq(label,a,b=0):ok(label,s.simplify(a-b)==0)
beta,V,a,k,t,u,y=s.symbols('beta V alpha k t u y',positive=True)
A0,Ap,B0,Bp=s.symbols('A0 Aphi B0 Bphi',nonnegative=True);J=A0+B0;D=A0*Bp-Ap*B0
neq=eq
neq('u derivative sign',(-beta*Bp*J+beta*B0*(Ap+Bp))/(2*J**2),-beta*D/(2*J**2))
eq('longitudinal transformed prefactor',beta*V**a*beta**(a-1)/(beta*V)**a,1)
eq('transverse transformed prefactor squared',(beta*V**a*beta**(a-1)*beta**2/(beta*V)**(a+s.Rational(3,2)))**2,beta/V**3)
phi=k*(2*y*y-y**4);f=s.exp(-t*phi/V);aa=t/V
neq('phi derivative',s.diff(phi,y),4*k*y*(1-y*y))
eq('phi second derivative',s.diff(phi,y,2),4*k*(1-3*y*y))
eq('f second derivative',s.diff(f,y,2),(aa**2*s.diff(phi,y)**2-aa*s.diff(phi,y,2))*f)
eq('phi f second derivative',s.diff(phi*f,y,2),(s.diff(phi,y,2)-2*aa*s.diff(phi,y)**2+phi*(aa**2*s.diff(phi,y)**2-aa*s.diff(phi,y,2)))*f)
# Algebraic nonnegative excess for the cross-cell prefix/suffix upper.
A,p,q,B,Ap,Pp,Qp,Bp=s.symbols('A p q B Ap Pp Qp Bp',nonnegative=True)
upper=(A+p+q)*(Pp+Qp+Bp)-Ap*B
actual=(A+p)*(Qp+Bp)-(Ap+Pp)*(q+B)
neq('D cell upper excess',upper-actual,Pp*(A+p+2*q+B)+q*(Qp+Bp+Ap))
# The trapezoid Peano weight gives h^3/12.
z,h=s.symbols('z h',positive=True)
eq('trapezoid error constant',s.integrate(z*(h-z)/2,(z,0,h)),h**3/12)
X,gamma,xx=s.symbols('X gamma x',positive=True);a0=2*k/V;gam=V/(4*k)
neq('lower J transform exponent',(-t*k*(2*y*y-y**4)/V).subs(y,xx/s.sqrt(a0*t)),-xx*xx+gam*xx**4/t)
for j in range(7):
 # Symmetric Gaussian x^(4j) moment after s=x² transformation.
 eq('Gaussian moment exponent '+str(j),s.Rational(4*j,2)-s.Rational(1,2),2*j-s.Rational(1,2))
 if j:
  eq('half Gamma recurrence '+str(j),s.gamma(s.Rational(1,2)+j)/s.gamma(s.Rational(1,2)),s.rf(s.Rational(1,2),j))
shape,zz=s.symbols('shape z',positive=True)
eq('upper tail logarithmic slope margin',(-1+(shape-1)/zz)-(-1+(shape-1)/X),-(shape-1)*(zz-X)/(zz*X))
neq('phi slab maximum',phi.subs(y,s.Rational(1,2)),7*k/16)
neq('tail central strip bound',t*(2*k*(s.Rational(1,2)/s.sqrt(1+t))**2)/V,k*t/(2*V*(1+t)))
neq('t32 domination margin',t+t*t-2*t**s.Rational(3,2),t*(s.sqrt(t)-1)**2)
neq('transverse tail coefficient',s.Rational(1,16)*s.Rational(1,2),s.Rational(1,32))
r=s.symbols('r',positive=True)
for j in [1,2]:
 eq('tilted Gamma factor '+str(j),s.gamma(a+j)/s.gamma(a),s.rf(a,j))
for shape_n in [1,4,5,8,16]:
 Sf=s.exp(-t)*sum(t**j/s.factorial(j) for j in range(shape_n))
 eq('integer Gamma survival derivative '+str(shape_n),s.diff(Sf,t),-s.exp(-t)*t**(shape_n-1)/s.factorial(shape_n-1))
 eq('integer Gamma at zero '+str(shape_n),Sf.subs(t,0),1)
# Exact finite positive-kernel analogues of D; no floating exponential evidence.
for n in range(2,10):
 ph=[F(j*j,n*n) for j in range(n)];weights=[F(j+1,n*(n+1)//2) for j in range(n)]
 for ti in [0,1,2,5]:
  ff=[weights[j]/(1+ph[j])**ti for j in range(n)]
  ffnext=[weights[j]/(1+ph[j])**(ti+1) for j in range(n)]
  for cut in range(n+1):
   def calc(fs):
    A=sum(fs[:cut]);B=sum(fs[cut:]);Ap=sum(ph[j]*fs[j] for j in range(cut));Bp=sum(ph[j]*fs[j] for j in range(cut,n))
    return A*Bp-Ap*B
   exact=calc(ff);nex=calc(ffnext)
   double=sum((ph[j]-ph[i])*ff[i]*ff[j] for i in range(cut) for j in range(cut,n))
   ok('positive D double integral algebra '+str((n,ti,cut)),exact==double>=0)
   ok('positive D decreasing parameter '+str((n,ti,cut)),nex<=exact)
# Raw literal aggregate example, explicitly not replacing coefficients by dmin.
d1=F(1)+F(3);d2=F(2);g=F(5)+F(7);mu1=F(2);mu2=F(3)
ok('literal coefficient aggregation',12*mu1*d1+2*mu2*g==168 and 12*mu2*d2+2*mu1*g==120)
ok('dmin not a trace upper',12*mu1*min(d1,d2)+2*mu2*g<168)
Cu,Ml,M,N,Q=s.symbols('Cu Ml M N Q',positive=True);kk=2*Cu/Ml
neq('reference first moment ceiling',4*Cu/(kk*N),2*Ml/N)
neq('reference inverse moment ceiling',kk*Q/(2*Ml),Cu*Q/Ml**2)
Z=s.symbols('Z',positive=True)
neq('capacity count normalized ratio',(2*Cu/Z)/(Cu/Ml),2*Ml/Z)
ok('fixture c norm exact',2*52**2+510*92**2==4322048)
for path,row in json.loads((P/'INPUT_SHA256.json').read_text()).items():
 data=(P.parent.parent/path).read_bytes();ok('immutable source '+path,hashlib.sha256(data).hexdigest()==row['sha256'] and len(data)==row['bytes'])
report={'status':'PASS','exact_assertions':len(checks),'scope':'positive-grid theorem algebra and finite exact fixtures only; no numerical consumer/diagnostic target accepted','checks':checks}
(P/'CHECK_RESULTS.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='checks'}))
