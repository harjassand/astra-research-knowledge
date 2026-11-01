from pathlib import Path
from fractions import Fraction as F
import hashlib,json
import sympy as s
P=Path(__file__).resolve().parent;checks=[]
def ok(label,b):
 assert b,label
 checks.append(label)
def eq(label,a,b=0):ok(label,s.simplify(a-b)==0)
a,v,V,k,x,alpha=s.symbols('a v V k x alpha',positive=True)
eq('density price parameter derivative',s.diff(a*a/(2*a-v),a),2*a*(a-v)/(2*a-v)**2)
eq('positive slab resistance excess',a*a/(2*a-v)-v,(a-v)**2/(2*a-v))
profile=lambda xx:1+k*(1-xx*xx)**2
vb=1+9*k/16;VV=1+k
neq=eq
neq('uniform slab denominator',2*vb-VV,1+k/8)
eq('near well margin',vb-profile(s.Rational(5,4)),63*k/256)
eq('convex tail derivative margin',s.diff(profile(x),x)-8*k*(x-1),4*k*(x-1)**2*(x+2))
ok('threshold above rational extension',s.Rational(7,4)>s.Rational(25,16))
ok('threshold upper length',s.Rational(2)<s.Rational(9,4))
eq('old far integral constant',s.integrate((x-1)**-2,(x,s.Rational(5,4),s.oo))/64,s.Rational(1,16))
eq('optimized parameter admission',VV*(1-1/(2*alpha))-vb,7*k/16-VV/(2*alpha))
for kk in [F(1,1000),F(1,10),F(1,3),F(1),F(4),F(100)]:
 VV=1+kk;vb=1+9*kk/16;G1=VV*VV/(2*VV-1);Gb=VV*VV/(2*VV-vb)
 for tt in [F(3,4),F(4,5),F(9,10),F(1)]:
  aa=1+kk*tt*tt;xasq=1+tt
  ok('threshold and slab '+str((kk,tt)),vb<=aa<=VV and F(25,16)<F(7,4)<=xasq<=2 and 2*aa-VV>=1+kk/8)
  for al in [4,5,16,128,2048]:
   delta=F(1,al);vv=1+kk*(1-(1+delta)**2)**2
   ok('near well within constant branch '+str((kk,tt,al)),vv<=vb<=aa and (1+delta)**2<xasq)
   opt=VV*(1-F(1,2*al));condition=al>=8*VV/(7*kk)
   ok('optimized parameter iff admission '+str((kk,tt,al)),(opt>=vb)==condition)
  for j in range(21):
   vv=1+(aa-1)*F(j,20)
   current=aa*aa/(2*aa-vv);old=VV*VV/(2*VV-vv)
   ok('all well density monotonicity '+str((kk,tt,j)),current<=old)
   ok('middle density ceiling '+str((kk,tt,j)),current/(vv*vv)<=G1)
   if vv<=vb:ok('near density ceiling '+str((kk,tt,j)),current<=Gb)
for path,row in json.loads((P/'INPUT_SHA256.json').read_text()).items():
 data=(P.parent.parent/path).read_bytes();ok('immutable source '+path,hashlib.sha256(data).hexdigest()==row['sha256'] and len(data)==row['bytes'])
report={'status':'PASS','exact_assertions':len(checks),'scope':'shifted-current theorem identities and rational fixtures, no finite numerical receiver accepted','checks':checks}
(P/'CHECK_RESULTS.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='checks'}))
