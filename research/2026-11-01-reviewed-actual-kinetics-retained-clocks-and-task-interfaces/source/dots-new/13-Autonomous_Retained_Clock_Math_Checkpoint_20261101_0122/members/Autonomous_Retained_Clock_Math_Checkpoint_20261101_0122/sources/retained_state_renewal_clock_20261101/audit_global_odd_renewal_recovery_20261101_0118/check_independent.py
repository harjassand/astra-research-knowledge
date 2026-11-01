"""Independent exact global-source/count algebra. No candidate imports."""
from pathlib import Path
import hashlib,json
import sympy as s
P=Path(__file__).resolve().parent;checks=[]
def ok(label,condition):
 assert condition,label
 checks.append(label)
def eq(label,left,right=0):ok(label,s.simplify(left-right)==0)
M,R,beta,eta,bf,cs=s.symbols('M R beta eta bf cs',positive=True)
N=s.symbols('N',positive=True)
k=2/(beta*M*R)
eq('global first spectral moment',(4/(beta*R))/(k*N),2*M/N)
eq('global inverse spectral moment',k*beta*M*M*R/N,2*M/N)
eq('residual inverse normalization',beta*(eta*M/2)**2*R*(1+cs)/(beta*M*M*R),eta**2*(1+cs)/4)
eq('weighted inverse triangle gap',(1+eta/2)*(bf+eta*(1+cs)/2)-(s.sqrt(bf)+eta*s.sqrt(1+cs)/2)**2,eta*(s.sqrt(bf)-s.sqrt(1+cs))**2/2)
Ztot=2*M+eta*M;slab=eta*M/Ztot;C=Ztot/M
neq=eq
neq('intensity relative normalization',2/(beta*R*Ztot),(1-slab)*k/2)
eq('initial density slab cost',C*slab,eta)
# Reflection: J_ref(x)=-R J(Rx) preserves longitudinal flux, reverses divergence.
A=s.Matrix(3,3,s.symbols('a0:9'));Ref=s.diag(-1,1,1)
eq('reflected divergence',s.trace(-Ref*A*Ref),-s.trace(A))
b11,b12,b22=s.symbols('b11 b12 b22');Dinv=s.Matrix([[1,0,0],[0,b11,b12],[0,b12,b22]])
ok('block inverse mobility reflection',Ref*Dinv*Ref==Dinv)
J=s.Matrix(s.symbols('jy jz1 jz2'))
eq('matching normal reflection',(-Ref*J)[0],J[0])
eq('reflected quadratic norm',((-Ref*J).T*Dinv*(-Ref*J))[0],(J.T*Dinv*J)[0])
rest,rplus=s.symbols('rest rplus',nonnegative=True)
eq('once barrier twice wells',2*(beta*M*M*rplus/2+beta*rest),beta*(M*M*rplus+2*rest))
r,e1,e2,eps=s.symbols('r e1 e2 eps',nonnegative=True)
eq('whole vector correlation subtraction',(r*r+e2)-2*r*(r+e1)+r*r,e2-2*r*e1)
n,x,ss,CC=s.symbols('n x ss CC',nonnegative=True)
total=n*CC*ss+CC*n*(x*x+eps/2+3*ss)/2+n*x*x/2
neq('complete coupling error non-grid',total,(CC+1)*n*x*x/2+CC*n*eps/4+s.Rational(5,2)*n*CC*ss)
xx=s.symbols('x',nonnegative=True)
F=1-2*xx+2*xx*xx-s.exp(-2*xx)
eq('cluster Taylor value',F.subs(xx,0),0)
eq('cluster Taylor first derivative',s.diff(F,xx).subs(xx,0),0)
eq('cluster Taylor second derivative',s.diff(F,xx,2),4*(1-s.exp(-2*xx)))
eq('small-mesh remainder margin',4*xx-8*xx*xx-2*xx,2*xx*(1-4*xx))
for count in range(201):ok('integer parity cluster '+str(count),int(count>=2)<=(count-count%2)/2)
# Both completed-transition square jumps are -1.
for old,new in [(0,1),(1,0)]:eq('label square jump '+str((old,new)),(new-new)**2-(new-old)**2,-1)
# Exact weighted finite reversible path fixtures, independent of continuum proof.
for mass in [s.Rational(1,2),s.Rational(1),s.Rational(3)]:
 for sm in [s.Rational(1,20),s.Rational(1,3),s.Rational(2)]:
  for cw,cb in [(s.Rational(1),s.Rational(2)),(s.Rational(7),s.Rational(1,4))]:
   W=s.diag(mass,sm,sm,mass);weights=W*s.ones(4,1);tot=sum(weights)
   H=s.Matrix([[cw,-cw,0,0],[-cw,cw+cb,-cb,0],[0,-cb,cw+cb,-cw],[0,0,-cw,cw]])
   K=W.inv()*H
   aug=H.row_join(weights).col_join(weights.T.row_join(s.zeros(1,1)))
   def inverse_form(f,g=None):
    if g is None:g=f
    sol=aug.inv()*(W*g).col_join(s.zeros(1,1));u=sol[:4,0]
    return (f.T*W*u)[0]
   f=s.Matrix([1,0,0,-1]);Qf=inverse_form(f)
   eq('global source current norm '+str((mass,sm,cw,cb)),Qf,mass**2*(2/cw+1/cb))
   q=s.Matrix([0,cb/(cw+2*cb),(cw+cb)/(cw+2*cb),1])
   # Harmonic interior follows from this equivalent resistor formula.
   ok('actual graph committor harmonic '+str((mass,sm,cw,cb)),(H*q)[1]==0 and (H*q)[2]==0)
   cap=(q.T*H*q)[0]
   eq('left charge cap '+str((mass,sm,cw,cb)),-(H*q)[0],cap)
   eq('right charge cap '+str((mass,sm,cw,cb)),(H*q)[3],cap)
   states=[(0,0),(1,0),(2,0),(3,1),(1,1),(2,1)];G=s.zeros(6,6)
   for i,(node,label) in enumerate(states):
    for dest in range(4):
     rate=-K[node,dest] if dest!=node else 0
     if rate:
      nl=0 if dest==0 else 1 if dest==3 else label
      j=states.index((dest,nl));G[i,j]+=rate;G[i,i]-=rate
   muaug=s.Matrix([weights[node]*(q[node] if label else 1-q[node])/tot for node,label in states])
   ok('stationary augmented graph law '+str((mass,sm,cw,cb)),muaug.T*G==s.zeros(1,6))
   intensity=sum(muaug[i]*G[i,j] for i in range(6) for j in range(6) if states[i][1]!=states[j][1])
   eq('two-direction stationary intensity '+str((mass,sm,cw,cb)),intensity,2*cap/tot)
   for a in [s.Rational(1,4),s.Rational(1,2),s.Rational(3,4)]:
    residual=s.Matrix([0,a,-a,0]);psi=f+residual
    Qr=inverse_form(residual);Qp=inverse_form(psi);cross=inverse_form(f,residual)
    norm=(psi.T*W*psi)[0];energy=(psi.T*H*psi)[0];kk=energy/(2*mass)
    label=str((mass,sm,cw,cb,a))
    eq('odd residual current price '+label,Qr,(sm*a)**2/cb)
    eq('global psi current price '+label,Qp,2*mass**2/cw+(mass+sm*a)**2/cb)
    ok('global odd source means '+label,(weights.T*f)[0]==0 and (weights.T*residual)[0]==0 and (weights.T*psi)[0]==0)
    ok('inverse cross Cauchy '+label,cross**2<=Qf*Qr)
    ok('global form inverse Cauchy '+label,energy*Qp>=norm**2)
    ok('global spectral first moment '+label,energy/(kk*norm)<=1)
    ok('spectral epsilon positivity '+label,kk*Qp/norm>=1)
# Rate two is forced even in the exact two-state model.
lam=s.symbols('lambda',positive=True);K2=s.Matrix([[lam,-lam],[-lam,lam]]);sign=s.Matrix([1,-1])
ok('correlation twice flip rate',K2*sign==2*lam*sign)
for path,row in json.loads((P/'INPUT_SHA256.json').read_text()).items():
 data=(P.parent.parent/path).read_bytes();ok('frozen dependency '+path,hashlib.sha256(data).hexdigest()==row['sha256'] and len(data)==row['bytes'])
report={'status':'PASS','exact_assertions':len(checks),'scope':'independent theorem identities and finite reversible algebra fixtures; not a numerical receiver or continuum-proof substitute','checks':checks}
(P/'CHECK_RESULTS.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='checks'}))
