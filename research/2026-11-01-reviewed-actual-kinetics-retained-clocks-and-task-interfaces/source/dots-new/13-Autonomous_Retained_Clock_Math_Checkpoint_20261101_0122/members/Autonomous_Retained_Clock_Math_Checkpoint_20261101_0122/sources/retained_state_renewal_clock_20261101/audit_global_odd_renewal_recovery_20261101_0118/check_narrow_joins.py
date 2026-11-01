from pathlib import Path
import hashlib,json
from fractions import Fraction as Q
import sympy as s
P=Path(__file__).resolve().parent;checks=[]
def ok(label,b):
 assert b,label
 checks.append(label)
def eq(label,a,b=0):ok(label,s.simplify(a-b)==0)
l,u,x,d,C,n,eta,eps,Tg=s.symbols('l u x d C n eta eps Tg',positive=True)
star=(l+u)/2;dd=(u-l)/(u+l)
eq('exact midpoint lower',(1-dd)*star,l)
eq('exact midpoint upper',(1+dd)*star,u)
eq('physical reference scaled spacing',star*(x/star),x)
eq('count drift margin',d*x+x*x/2-((1+d)*x-((1-d)*x-(1-d)**2*x*x))/2,d*(2-d)*x*x/2)
eq('jitter full error',Tg+C*n*(d*x+x*x/2+eps/4+3*eta/(2*C))+n*x*x/2,Tg+(C+1)*n*x*x/2+C*n*eps/4+s.Rational(3,2)*n*eta+C*n*d*x)
a,sigma,Y=s.symbols('a sigma Y',positive=True);bb=1/s.sqrt(2*a);gamma=(a-sigma)/(a*sigma)
eq('storage completing square',2*bb*Y-2*gamma*Y*Y,bb*bb/(2*gamma)-2*gamma*(Y-bb/(2*gamma))**2)
eq('storage hidden bound',bb*bb/(2*gamma),sigma/(4*(a-sigma)))
defect=sigma/(a-sigma)
eq('orthogonal full bound',defect/4+defect*defect/4,defect*(1+defect)/4)
ok('Euler rational lower series',sum(Q(1,s.factorial(i)) for i in range(4))==Q(8,3))
eq('Euler reciprocal upper',1/s.Rational(8,3),s.Rational(3,8))
for low in [Q(1,100),Q(1),Q(7,3),Q(100)]:
 for ratio in [Q(1),Q(101,100),Q(4,3),Q(2),Q(100)]:
  high=low*ratio;st=(low+high)/2;dd=(high-low)/(high+low)
  ok('positive midpoint interval '+str((low,ratio)),0<=dd<1 and (1-dd)*st==low and (1+dd)*st==high)
  for j in range(11):
   lam=low+(high-low)*Q(j,10)
   bound=Q(3,8)*dd/(1-dd)
   ok('uniform rate rational majorant '+str((low,ratio,j)),Q(3,8)*abs(lam-st)/min(lam,st)<=bound)
  for xx in [Q(1,100),Q(1,4),Q(1),Q(3)]:
   exact=((1+dd)*xx-((1-dd)*xx-(1-dd)**2*xx**2))/2
   ok('count drift rational majorant '+str((low,ratio,xx)),exact<=dd*xx+xx*xx/2)
for alpha in [4,5,16,128]:
 ok('tail variance dominates squared mean '+str(alpha),1-4*alpha<0)
 ok('Rayleigh tail exponent '+str(alpha),(-1-4*alpha)-(1-4*alpha)==-2)
for path,row in json.loads((P/'ADDENDUM_INPUT_SHA256.json').read_text()).items():
 data=(P.parent.parent/path).read_bytes();ok('immutable addendum '+path,hashlib.sha256(data).hexdigest()==row['sha256'] and len(data)==row['bytes'])
report={'status':'PASS','exact_assertions':len(checks),'scope':'narrow theorem algebra only; no executable, processing or finite numerical acceptance','checks':checks}
(P/'NARROW_CHECK_RESULTS.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='checks'}))
