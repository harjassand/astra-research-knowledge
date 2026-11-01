"""Independent exact robust-envelope theorem tests; no candidate imports."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json
import sympy as s
P=Path(__file__).resolve().parent
checks=[]
def ok(label,b):
 assert b,label
 checks.append(label)
def eq(label,l,r=0):ok(label,s.simplify(l-r)==0)
y,x,k,e,al,beta,d,mu=s.symbols('y x k e alpha beta d mu',positive=True)
v=1+k*(1-y*y)**2;g=y*y*(1-y*y)**2/(1+y*y);b=v+e*g
r=(2*x*x+3*x-1)/(1+x)**2
q=1+k;ab=1+9*k/16;Gb=q*q/(2*q-ab);G1=q*q/(2*q-1)
eq('exact b derivative',s.diff(b,y),2*y*(y*y-1)*(2*k+e*r.subs(x,y*y)))
eq('profile rational lower',r+1,x*(3*x+5)/(1+x)**2)
eq('profile rational upper below one',r-1,(x-1)*(x+2)/(1+x)**2)
eq('y g derivative',y*s.diff(g,y),2*y*y*(y*y-1)*r.subs(x,y*y))
eq('y v lower',y*s.diff(v,y)+k,k*(2*y*y-1)**2)
eq('g profile bound',(v-1)/k-g,(1-y*y)**2/(1+y*y))
eq('well g leading coefficient',s.limit(g/(y-1)**2,y,1),2)
eq('well b curvature',s.diff(b,y,2).subs(y,1)/2,4*k+2*e)
eq('barrier b curvature',s.diff(b,y,2).subs(y,0)/2,-2*k+e)
eq('barrier preserved',b.subs(y,0),q)
eq('well preserved',b.subs(y,1),1)
eq('strict localized threshold',k*(1-Gb/q),7*k*k/(16+23*k))
eq('kappa1 threshold',(k*(1-Gb/q)).subs(k,1),s.Rational(7,39))
eq('S exponent implication margin',ab*(q+1)-2*q,k/s.Integer(8)+9*k*k/16)
eq('Gb ratio bound margin',Gb-q/ab,q*(ab*(q+1)-2*q)/(ab*(2*q-ab)))
eta,BA,CC=s.symbols('eta BA CC',nonnegative=True)
eq('mean rational source AMGM gap',(1+eta/2)*BA+eta*CC/2-(BA+eta*s.sqrt(BA*CC)),eta*(s.sqrt(BA)-s.sqrt(CC))**2/2)
eq('spectral rational source CS gap',(1+eta)*(BA+eta*CC)-(s.sqrt(BA)+eta*s.sqrt(CC))**2,eta*(s.sqrt(BA)-s.sqrt(CC))**2)
t=s.symbols('t',nonnegative=True)
eq('limiting ratio',(1+e/(2*k))/s.sqrt(1-e/(2*k)),((2*k+e)/(2*k))*s.sqrt(2*k/(2*k-e)))
eq('small-defect limiting derivative',s.diff((1+t)/s.sqrt(1-t)-1,t).subs(t,0),s.Rational(3,2))
# Denominator comparison uses s>=v and g<=v/k.
ss,vv,gg=s.symbols('s v g',positive=True)
eq('squared density denominator margin',(2*ss-vv-e*gg)-(1-e/k)*(2*ss-vv),e*((2*ss-vv)/k-gg))
eq('cross density denominator margin',(ss+s.Symbol('T',positive=True)-vv-e*gg)-(1-e/k)*(ss+s.Symbol('T',positive=True)-vv),e*((ss+s.Symbol('T',positive=True)-vv)/k-gg))
# Brownian/tan counterexample to extension to unbounded state-dependent mobility.
xx=s.symbols('X',real=True);D=(1+xx*xx)**2;logw=-s.log(1+xx*xx)
drift=s.diff(D,xx)+D*s.diff(logw,xx)
eq('unbounded-mobility drift',drift,2*xx*(1+xx*xx))
eq('atan drift zero',D*s.diff(s.atan(xx),xx,2)+drift*s.diff(s.atan(xx),xx),0)
eq('atan diffusivity one',D*s.diff(s.atan(xx),xx)**2,1)
eq('finite formal Gibbs',s.integrate(1/(1+xx*xx),(xx,-s.oo,s.oo)),s.pi)
# Rational all-domain algebra fixtures, including above the sufficient asymptotic threshold.
for kk in [F(1,10),F(1,3),F(1),F(4),F(100)]:
 V=1+kk;aa=1+9*kk/16;gb=V*V/(2*V-aa);thr=kk*(1-gb/V)
 for ee in [F(0),thr/2,thr*F(9,10),kk*F(9,10)]:
  L=1/(1-ee/kk)
  ok('finite pricing strict '+str((kk,ee)),0<=ee<kk and L>=1)
  if ee<thr:
   ok('localized three exponent gaps '+str((kk,ee)),L*gb<V and L*(V*V/(2*V-1))<V and L<V)
   ok('separate S exponent gap '+str((kk,ee)),L<aa)
  for yy in [F(0),F(1,10),F(1,2),F(3,4),F(1),F(5,4),F(2),F(10)]:
   vv=1+kk*(1-yy*yy)**2;gg=yy*yy*(1-yy*yy)**2/(1+yy*yy);bb=vv+ee*gg
   rr=(2*yy**4+3*yy*yy-1)/(1+yy*yy)**2
   ok('global envelope/profile '+str((kk,ee,yy)),gg>=0 and gg<=(vv-1)/kk and 2*kk+ee*rr>0)
   ok('global g drift lower '+str((kk,ee,yy)),2*yy*yy*(yy*yy-1)*rr>=-F(1,2))
   if yy<=F(1,2):ok('slab denominator '+str((kk,ee,yy)),bb<=V and 2*V-bb>=V)
   for h in [F(0),F(1),vv]:
    ss=vv+h
    ok('density pricing denominator '+str((kk,ee,yy,h)),2*ss-bb>0 and 2*ss-bb>=(1-ee/kk)*(2*ss-vv))
# Finite weighted path forms independently test upper-source/lower-price comparison.
for ma in [s.Rational(1,4),s.Rational(1),s.Rational(3)]:
 for ms in [s.Rational(1,10),s.Rational(2)]:
  for c1,c2 in [(s.Rational(1),s.Rational(2)),(s.Rational(5),s.Rational(1,3))]:
   W=s.diag(ma,ms);H=s.Matrix([[c1,-c1],[-c1,c1+c2]])
   Hlo=H/2;Hup=2*H;K=W.inv()*H;Ki=K.inv();A=s.Matrix([1,0]);S=s.Matrix([0,1]);DD=A+S
   upperA=2*ma;upperS=3*ms;lowerA=ma/3
   # Upper A flux: upperA on both edges; upper S flux only on target edge.
   BA=upperA**2*(2/c1+2/c2);BS=upperS**2*(2/c2)
   QA=(A.T*W*Ki*A)[0];QS=(S.T*W*Ki*S)[0];QAS=(A.T*W*Ki*S)[0]
   ok('actual source dual '+str((ma,ms,c1,c2)),QA<=BA and QS<=BS and QAS>=0 and QAS**2<=QA*QS)
   for hv in [s.Rational(0),s.Rational(1,3),s.Rational(1)]:
    h=s.Matrix([1,hv]);N=(h.T*W*h)[0];E=(h.T*H*h)[0];C0=(h.T*Hup*h)[0];Qh=(h.T*W*Ki*h)[0];U=(s.sqrt(BA)+s.sqrt(BS))**2
    label=str((ma,ms,c1,c2,hv));k0=C0/lowerA;eps=C0*U/lowerA**2-1
    ok('lower-mass reference first moment '+label,E/(N*k0)<=1)
    ok('lower-mass reference inverse moment '+label,s.simplify(1+eps-k0*Qh/N)>=0)
    ok('positive robust epsilon '+label,s.simplify(eps)>=0)
    ok('actual improved mean lower '+label,(QA+QAS)/ma>=ma/C0>=lowerA/C0)
for name,row in json.loads((P/'INPUT_SHA256.json').read_text()).items():
 data=(P.parent/name).read_bytes();ok('immutable source '+name,hashlib.sha256(data).hexdigest()==row['sha256'] and len(data)==row['bytes'])
report={'status':'PASS','exact_assertions':len(checks),'scope':'independent theorem identities and finite algebra fixtures; no candidate implementation accepted','checks':checks}
(P/'CHECK_RESULTS.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='checks'}))
