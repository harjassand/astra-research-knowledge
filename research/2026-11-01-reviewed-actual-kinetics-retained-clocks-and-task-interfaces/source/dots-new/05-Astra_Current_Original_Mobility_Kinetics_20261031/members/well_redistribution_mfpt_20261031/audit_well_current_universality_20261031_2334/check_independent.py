"""Independent theorem identities and exact fixtures. No candidate code import."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json
import sympy as s
P=Path(__file__).resolve().parent
checks=[]
def ok(label,condition):
 assert condition,label
 checks.append(label)
def eq(label,left,right=0): ok(label,s.simplify(left-right)==0)
y,x,k,a,beta,mu,d,u,V,ss,v=s.symbols('y x k alpha beta mu d U V s v',positive=True)
profile=lambda x:1+k*(1-x*x)**2
vp=s.diff(profile(y),y)
eq('profile derivative',vp,4*k*y*(y*y-1))
eq('quartic derivative margin',s.diff(profile(x),x)-8*k*(x-1),4*k*(x-1)**2*(x+2))
eq('profile convexity',s.diff(profile(x),x,2),4*k*(3*x*x-1))
eq('near-well endpoint margin',profile(s.Rational(1,2))-profile(s.Rational(5,4)),63*k/256)
eq('v equals barrier roots',profile(x)-(1+k),k*x*x*(x*x-2))
ok('redistribution length < one',s.Rational(2)<s.Rational(3,2)**2)
ok('far extension starts below sqrt2',s.Rational(5,4)**2<2)
eq('far reciprocal-square integral',s.integrate((x-1)**-2,(x,s.Rational(5,4),s.oo)),4)
eq('far sixteen constant',s.Rational(4,64),s.Rational(1,16))
eq('middle 128 constant',s.Rational(1,2)/64,s.Rational(1,128))
eq('moment K constant',s.Rational(1,16)*s.sqrt(a*(4*a)/(beta*d))/mu,a/(8*mu*s.sqrt(beta*d)))
# pi_s differentiated at fixed z, using Euler z.grad U=4U and m=4 alpha.
eq('homogeneous density continuity',a/ss-beta*u,(4*a-4*beta*ss*u)/(4*ss))
# Explicit nonseparable homogeneous quartic fixture (identity independent of alpha>=4 restriction).
z1,z2=s.symbols('z1 z2',real=True)
UU=z1**4+2*z2**4+3*z1*z1*z2*z2
pi=ss**s.Rational(1,2)*s.exp(-beta*ss*UU)
eq('explicit fiber continuity',s.diff(pi,ss),(s.diff(z1*pi,z1)+s.diff(z2*pi,z2))/(4*ss))
eq('homotopy divergence orientation',-(s.Symbol('piV')-s.Symbol('piv')),s.Symbol('piv')-s.Symbol('piV'))
eq('density-ratio beta exponent',2*a-a-a,0)
eq('density-ratio energy exponent',-2*beta*ss*u+beta*v*u,-beta*(2*ss-v)*u)
eq('longitudinal density prefactor',v*ss**2/(v*(2*ss-v)),ss**2/(2*ss-v))
eq('homotopy norm prefactor',ss**2/(v*(2*ss-v))/v,ss**2/(v*v*(2*ss-v)))
eq('parallel resistance >= scalar',V*V/(2*V-v)-v,(V-v)**2/(2*V-v))
eq('s-ratio derivative',s.diff(ss**2/(2*ss-v),ss),2*ss*(ss-v)/(2*ss-v)**2)
eq('v-ratio logarithmic derivative',s.diff(s.log(V*V/(v*v*(2*V-v))),v),1/(2*V-v)-2/v)
eq('negative logarithmic derivative form',1/(2*V-v)-2/v,(3*v-4*V)/(v*(2*V-v)))
eq('cumulative antiderivative',s.diff(v**(1-a)/(1-a),v),v**(-a))
eq('global Lyapunov coefficient margin',y*vp+(4+k)*profile(y)-4,k*(y*y-1)**2*(k+8)+4*k*(y*y-1)+k)
# A simpler universally nonnegative proof: y v'>=-k, (4+k)v>=4+k.
eq('longitudinal Lyapunov lower',y*vp+k,k*(2*y*y-1)**2)
eta,A,T,C=s.symbols('eta A T C',nonnegative=True)
eq('mean AMGM gap',(1+eta/2)*A+eta*T*C/2-(A+eta*s.sqrt(A*T*C)),eta*(s.sqrt(A)-s.sqrt(T*C))**2/2)
eq('spectral separate-source CS gap',(1+eta)*(A+eta*C)-(s.sqrt(A)+eta*s.sqrt(C))**2,eta*(s.sqrt(A)-s.sqrt(C))**2)
c,dd=s.symbols('c dd',positive=True)
q1=s.series(s.log(1-c*y*y+dd*y**4),y,0,6).removeO()
q2=s.series(-s.log(1+c*y*y-dd*y**4),y,0,6).removeO()
eq('R local expansion',q1,-c*y*y+(dd-c*c/2)*y**4)
eq('Rplus local expansion',q2,-c*y*y+(dd+c*c/2)*y**4)
eq('Gaussian fourth-moment ratio',s.integrate(x**4*s.exp(-c*x*x),(x,-s.oo,s.oo))/s.integrate(s.exp(-c*x*x),(x,-s.oo,s.oo)),3/(4*c*c))
eq('universal witness coefficient',3*((dd+c*c/2)-(dd-c*c/2))/(4*c*c),s.Rational(3,4))
eq('leading time prefactor',s.sqrt(s.pi)/(2*s.sqrt(k))*s.sqrt(s.pi/(2*k/(1+k))),s.pi*s.sqrt(1+k)/(2*s.sqrt(2)*k))
t=s.symbols('t',nonnegative=True)
eq('dominator monotonicity derivative',s.diff(s.log(1+t)-t/(1+t),t),t/(1+t)**2)
eq('basin global quadratic lower margin',profile(y)-1-s.Rational(9,4)*k*(y-1)**2,k*(y-1)**2*((y+1)**2-s.Rational(9,4)))
eq('slab Gaussian lower margin',(k/(1+k))*(2*y*y-y**4)-s.Rational(7,4)*k/(1+k)*y*y,k/(1+k)*y*y*(s.Rational(1,4)-y*y))
eq('slab u maximum',(k/(1+k))*(2*s.Rational(1,2)**2-s.Rational(1,2)**4),7*k/(16*(1+k)))
# Rational model/shape fixtures. Exact, but not substitutes for global proof.
for kk in [F(1,100),F(1,3),F(1),F(4),F(100)]:
 vv=1+kk;ab=1+9*kk/16;g1=vv*vv/(2*vv-1);gb=vv*vv/(2*vv-ab)
 ok('strict scalar growth ordering '+str(kk),1<ab<vv and 1<g1<vv and 1<gb<vv)
 for aa in [4,5,8,16,64,512]:
  delta=F(1,aa)
  ok('near-well containment '+str((kk,aa)),1+kk*(1-(1+delta)**2)**2<=ab)
  ok('basin dual and L2 tail integrable '+str((kk,aa)),2-4*aa<-1 and 4-4*aa<-1)
  ok('middle constant alpha factor '+str((kk,aa)),1/((aa-1)**2*delta**2)==F(aa*aa,(aa-1)**2))
 for j in range(21):
  xx=F(j,40);vvx=1+kk*(1-xx*xx)**2;uy=kk/vv*(2*xx*xx-xx**4)
  ok('whole-slab domain '+str((kk,j)),ab<=vvx<=vv and 0<=uy<=7*kk/(16*vv)<F(7,16))
  ok('whole-slab lower Gaussian '+str((kk,j)),uy>=7*kk/(4*vv)*xx*xx)
  ok('whole-slab resistance ordering '+str((kk,j)),vv*vv/(2*vv-vvx)>=vvx)
 for j in range(1,21):
  vvcur=1+kk*F(j,20)
  for ell in [0,1,5,10]:
   sj=vvcur+(vv-vvcur)*F(ell,10)
   ratio=sj*sj/(vvcur*vvcur*(2*sj-vvcur))
   ok('homotopy density majorant '+str((kk,j,ell)),ratio<=g1)
for name,row in json.loads((P/'INPUT_SHA256.json').read_text()).items():
 data=(P.parent/name).read_bytes()
 ok('immutable source '+name,hashlib.sha256(data).hexdigest()==row['sha256'] and len(data)==row['bytes'])
report={'status':'PASS','exact_assertions':len(checks),'scope':'independent algebra/fixtures only; no candidate implementation or finite numerical claim accepted','checks':checks}
(P/'CHECK_RESULTS.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='checks'}))
