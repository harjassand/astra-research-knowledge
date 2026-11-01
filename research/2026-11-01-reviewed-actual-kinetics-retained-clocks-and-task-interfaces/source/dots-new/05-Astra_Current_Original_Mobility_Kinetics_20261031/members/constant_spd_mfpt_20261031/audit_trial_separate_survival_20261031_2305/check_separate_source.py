"""Independent exact checks; no candidate executable or prior artifact mutation."""
from pathlib import Path
import hashlib,json
import sympy as s
HERE=Path(__file__).resolve().parent
checks=[]
def ok(label,condition):
 assert condition,label
 checks.append(label)
def eq(label,left,right): ok(label,s.simplify(left-right)==0)
C,M,R,beta,BA,BS,bnew,bold,rho=s.symbols('C M R beta BA BS bnew bold rho', positive=True)
eq('coupled specialization',C*(s.sqrt(BA)+s.sqrt(rho**2*BA))**2/M**2-1,C*BA*(1+rho)**2/M**2-1)
eq('old-new dimensionless normalization',(C*(s.sqrt(BA)+rho*s.sqrt(BS))**2/M**2-1).subs({C:1/(beta*R),BA:bnew*beta*M**2*R,BS:bold*beta*M**2*R}),(s.sqrt(bnew)+rho*s.sqrt(bold))**2-1)
lo,hi,t=s.symbols('lo hi t',positive=True)
eq('midpoint endpoint distance',(lo+hi)/2-lo,(hi-lo)/2)
eq('midpoint relative penalty',(hi-lo)/(2*s.E*lo),(hi/lo-1)/(2*s.E))
ok('rational e partial sum',sum(s.Rational(1,s.factorial(i)) for i in range(4))==s.Rational(8,3))
eq('rational midpoint coefficient',s.Rational(1,2)/s.Rational(8,3),s.Rational(3,16))
eq('rate derivative',s.diff(s.exp(-lo*t),lo),-t*s.exp(-lo*t))
eq('all-time maximizer derivative',s.diff(t*s.exp(-lo*t),t),s.exp(-lo*t)*(1-lo*t))
eq('all-time maximum',(t*s.exp(-lo*t)).subs(t,1/lo),1/(s.E*lo))
# Independently varied exact A/S inverse bounds, including nonharmonic trial h.
for ms in [s.Rational(1,100),s.Rational(1,4),s.Rational(1),s.Rational(7)]:
 for ca,cb,cs in [(1,1,1),(2,0,3),(7,2,1)]:
  W=s.diag(1,ms); H=s.Matrix([[ca+cb,-ca],[-ca,ca+cs]])
  K=W.inv()*H; Ki=K.inv(); A=s.Matrix([1,0]); S=s.Matrix([0,1]); D=A+S
  qa=(A.T*W*Ki*A)[0];qs=(S.T*W*Ki*S)[0];qas=(A.T*W*Ki*S)[0]
  for hv in [s.Rational(0),s.Rational(1,4),s.Rational(1)]:
   h=s.Matrix([1,hv]);N=(h.T*W*h)[0];E=(h.T*H*h)[0];qh=(h.T*W*Ki*h)[0];qd=(D.T*W*Ki*D)[0]
   for fa,fs in [(1,1),(s.Rational(5,4),2),(3,s.Rational(9,8))]:
    ba=fa*qa;bs=fs*qs;U=(s.sqrt(ba)+s.sqrt(bs))**2
    label=str((ms,ca,cb,cs,hv,fa,fs))
    ok('source inverse cross '+label,qas>=0 and qas**2<=qa*qs)
    ok('source domination '+label,qh<=qd and s.simplify(U-qd)>=0)
    ok('form inverse Cauchy '+label,E*qh>=N**2)
    ok('positive normalized epsilon '+label,s.simplify(E*U-1)>=0)
    ok('spectral first moment '+label,E/(N*E)<=1)
    ok('spectral inverse moment '+label,s.simplify(E*U-E*qh/N)>=0)
for name,row in json.loads((HERE/'INPUT_SHA256.json').read_text()).items():
 data=(HERE.parent/name).read_bytes()
 ok('frozen source '+name,hashlib.sha256(data).hexdigest()==row['sha256'] and len(data)==row['bytes'])
report={'status':'PASS','exact_assertions':len(checks),'scope':'theorem algebra and independent exact finite fixtures only; no executable or numerical KS claim accepted','checks':checks}
(HERE/'CHECK_RESULTS.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='checks'}))
