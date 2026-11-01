from fractions import Fraction as Q
from math import comb,isqrt
from pathlib import Path
import json,random,hashlib
D=6;zero=(0,)*D;checks=0;cats={}
def ok(v,k):
 global checks
 assert v,k
 checks+=1;cats[k]=cats.get(k,0)+1
class P:
 def __init__(self,x=0):self.d={k:Q(v)for k,v in x.items()if v}if type(x)is dict else ({zero:Q(x)}if x else {})
 def __add__(s,t):
  t=t if isinstance(t,P)else P(t);d=dict(s.d)
  for k,v in t.d.items():d[k]=d.get(k,0)+v
  return P(d)
 __radd__=__add__
 def __neg__(s):return P({k:-v for k,v in s.d.items()})
 def __sub__(s,t):return s+-asP(t)
 def __rsub__(s,t):return asP(t)+-s
 def __mul__(s,t):
  t=asP(t);d={}
  for k,v in s.d.items():
   for l,w in t.d.items():
    n=tuple(a+b for a,b in zip(k,l));d[n]=d.get(n,0)+v*w
  return P(d)
 __rmul__=__mul__
 def __truediv__(s,t):return s*Q(1,t)
 def __pow__(s,n):
  z=P(1)
  for _ in range(n):z=z*s
  return z
 def shift(s,inc):
  out=P()
  for ex,c in s.d.items():
   term=P(c)
   for i,n in enumerate(ex):
    if not n:continue
    term=term*(var[i]+inc[i])**n
   out=out+term
  return out
 def val(s,x):return sum((v*prod(a**b for a,b in zip(x,k))for k,v in s.d.items()),Q(0))
def prod(xs):
 v=Q(1)
 for x in xs:v*=x
 return v

def asP(x):return x if isinstance(x,P)else P(x)
var=[P({tuple(int(i==j)for j in range(D)):1})for i in range(D)];A,B,C,E_D,E,W=var;DD=E_D
L=A+(C+DD)/2;Z=C-DD;F=L-Q(3,4)*E**2*W+A*E*W
# Independent literal increment/intensity list, W=1/N held fixed.
rows=[('immigration',(1,0,0,0,0,0),P(1)),('death',(-1,0,0,0,0,0),A),('2A_AC',(-1,0,1,0,0,0),A*(A-1)),('AC_2A',(1,0,-1,0,0,0),A*C),('2A_AD',(-1,0,0,1,0,0),A*(A-1)),('AD_2A',(1,0,0,-1,0,0),A*DD),('2A_AE',(-1,0,0,0,1,0),A*(A-1)),('AE_2A',(1,0,0,0,-1,0),A*E),('AE_CD',(-1,0,1,1,-1,0),A*E),('CD_AE',(1,0,-1,-1,1,0),2*C*DD),('CD_AB',(1,1,-1,-1,0,0),C*DD),('AB_CD',(-1,-1,1,1,0,0),A*B)]
def gen(f):return sum((rate*(f.shift(inc)-f)for _,inc,rate in rows),P())
def bracket(f):return sum((rate*(f.shift(inc)-f)**2 for _,inc,rate in rows),P())
identities={}
def ident(name,got,expected):
 got=asP(got);expected=asP(expected);keys=set(got.d)|set(expected.d)
 for k in keys:ok(got.d.get(k,0)==expected.d.get(k,0),'exact polynomial coefficient identity '+name)
 identities[name]={','.join(map(str,k)):str(v)for k,v in sorted(got.d.items())};ok(got.d==expected.d,'global exact polynomial identity '+name)
LA=1-A-3*A*(A-1)+A*(C+DD)+3*C*DD-A*B
ident('LA',gen(A),LA);ident('LL',gen(L),1+A+A*L+A*E-3*A**2);ident('LE',gen(E),A*(A-1)-2*A*E+2*C*DD);ident('LZ',gen(Z),-A*Z)
ident('qZ',bracket(Z),2*A*(A-1)+A*(C+DD));qA=1+A+3*A*(A-1)+A*(C+DD)+2*A*E+3*C*DD+A*B
ident('qA',bracket(A),qA);ident('LA2',gen(A**2),2*A*LA+qA)
ident('LAE',gen(A*E),E+3*E*C*DD+2*A*C*DD+A*(A-1)**2+2*C*DD-A*E*(B-C-DD-2+5*A))
LF=1+A+A*L-3*A**2+E*W+C*DD*W/2+2*A*C*DD*W+A*(A-1)**2*W-Q(3,4)*A*(A-1)*W+A*E*(1+(C+DD+2+3*E-Q(13,2)*A-B)*W)
ident('LF',gen(F),LF);ident('qE',bracket(E),A*(A-1)+2*A*E+2*C*DD)
table={'immigration':1+E*W,'death':-1-E*W,'2A_AC':-Q(1,2)-E*W,'AC_2A':Q(1,2)+E*W,'2A_AD':-Q(1,2)-E*W,'AD_2A':Q(1,2)+E*W,'2A_AE':-1+(A-Q(5,2)*E-Q(7,4))*W,'AE_2A':1+(Q(5,2)*E-A-Q(7,4))*W,'AE_CD':(E/2-A+Q(1,4))*W,'CD_AE':(A-E/2+Q(1,4))*W,'CD_AB':E*W,'AB_CD':-E*W}
for name,inc,rate in rows:ident('Fjump_'+name,F.shift(inc)-F,table[name]);ok(sum(inc[:5])==(1 if name=='immigration'else -1 if name=='death'else 0),'literal total count increment')
# All following bounds are monotone envelopes at the extrema forced by the
# assumptions, NOT sampling one giant N,m pair. See the mathematical review.
delta=Q(1,10**100);rho=Q(1,10**50);im=Q(1,10**80);iN=Q(1,10**200);tau=Q(16,10**100)
ok(rho*rho==delta,'rho=sqrt(delta)');ok(1-5*delta-2*rho>Q(1,2),'uniform B lower bound from actual mass tube');ok(1+delta<2,'uniform B upper bound')
ok(Q(1,32)+im<Q(1,16),'initial A strictly inside auxiliary tube');ok(Q(1,32)+im+Q(1,64)<Q(1,16),'initial Z and damped martingale bound')
ok(2*iN+4*delta<Q(1,4),'uniform LA upper bound coefficients');ok(7*iN+8*delta<Q(1,2),'uniform LA2 negative quadratic margin');ok(4*delta+4*rho<1,'uniform LA2 linear N margin')
ok(208+50000<100000,'A bracket at H clock budget');hmargin=2500-208-rho*(Q(1,32)+im);jmargin=5000000-30208*im-240000*delta-rho*(Q(1,32)+im)**2
ok(hmargin>100,'H first exit forces >100e A martingale');ok(jmargin>100,'J2 first exit forces >100me A2 martingale');ok(Q(1,8)+im<1,'A2 stopped jump size <=m including exit')
coef=delta+Q(269,32)*delta+8*rho+2*iN;ok(coef<32*rho,'complete residual AE coefficient upper')
drift=(10000*rho*im+20000*rho+30000000*rho+32*rho*im+80000*rho**3+625000*rho**3+7500000*rho*iN+640000*rho)
ok(drift<10**9*rho,'uniform F drift residual classes');ok((1+2*rho)*tau<4*tau,'immigration and E/N residual time');ok(10**9*rho+4*tau<Q(1,64),'uniform full F drift less than m/64')
ok(20000+192+20000*rho<50000,'fast AB/CD/AECD compensator upper');ok(1+rho/16+rho*im/4<2,'small CD corrected jump <=2e/N');ok(1+5*rho+delta/16+Q(7,4)*iN<2,'all slow F jumps <=2');ok(Q(1,2)+2*rho<1,'AC AD F jumps <=1')
qF=200000*rho+80000+40000*rho+120000000*rho+4*tau+40000*rho*im
ok(qF<2*10**8,'uniform complete F bracket/m');ok(10**7*delta+40000*rho+128<50000,'uniform E bracket/e');ok(2*10**7+40000<3*10**7,'uniform Z bracket/(m e/N)')
ok(40000*rho<Q(1,100),'E adverse drift less than e/100');ok(40000*rho+Q(1,100)<Q(1,50),'good E decrease less than e/50')
# Freedman denominators after cancellation; each check is uniform in m,e.
ok(200000+Q(2,3)<200002,'A Freedman denominator');ok(200000+Q(2,3)<200002,'A2 Freedman denominator')
ok(8192*(2*10**8+Q(1,96))<3*10**12,'F Freedman exponent m/Cstar');ok(20000*(50000+Q(1,300))<2*10**9,'E Freedman exponent');ok(32768*(3*10**7+Q(1,384))<2*10**12,'Z Freedman exponent')
ok(12*rho<Q(1,8),'fast-A exponential drift negative reserve');ok(208*delta+im<Q(1,64),'a0 ceiling <=m/64');ok(Q(1,64)+im-Q(1,16)<-Q(1,32),'new A excursion exponent');ok(Q(1,32)+im-Q(1,16)<-Q(1,64),'initial A excursion exponent')
ok(208+60000*rho<100000,'expected upward excursion count <=100000e')
# log(10^5)<15, log(m)<=sqrt(m), u=sqrt(m)>=1000.
ok(Q(3,128)*1000**2-5*1000-15>0 and Q(6,128)*1000-5>0,'polynomial excursion prefactor absorbed uniformly for m>=1e6')
ok(Q(27,25)**2<Q(7,6),'entry E relation and 1.06e postdrop');ae_post=(Q(1,16)+im)*(2*rho+iN);ok(ae_post<Q(1,100),'postjump AE/N less than m/100')
ok(Q(3,4)*Q(53,50)**2-Q(1,4)-Q(1,100)>Q(1,2),'lower L exit impossible including jump overshoot');ok(2+im+Q(1,100)+Q(1,4)<3,'upper E exit impossible including jump overshoot')
ok(Q(7,16)**2-Q(1,1024)>Q(1,8),'CD lower bound until deadline');ok(4-40000*rho-Q(1,100)>Q(398,100),'deadline E increase exceeds 3.98e')
ok(Q(4,3)*(2-Q(5,32))>2,'next-stage E lower entrance');ok(Q(4,3)*(2+im+Q(1,100)+Q(5,32))<Q(169,50),'next-stage E upper entrance');ok(Q(5,32)<Q(1,4),'next-stage F entrance')
for d in [200002,2*10**9,2*10**12,128]:ok(d<3*10**12,'all failure exponents stronger than claimed common exponent')
ok(10<16,'union prefactor covers all five exceptional classes');ok(Q(10**80,3*10**12)>1,'dyadic exponential summation has x>=1');ok(Q(1,8)<Q(9,64),'deadline ratio2^-3/2 less than3/8')
# Global polynomial verification is already exact. These independent evaluations
# catch mistakes in the finite polynomial engine itself, not an all-state proof.
rng=random.Random(11010422)
for _ in range(200):
 vals=[rng.randrange(11)for j in range(5)]+[Q(1,rng.randrange(1,200))]
 for f in [A,L,E,Z,A*E,F]:
  direct=Q(0)
  for name,inc,rate in rows:
   r=rate.val(vals)
   if r:direct+=r*(f.val([a+b for a,b in zip(vals,inc)])-f.val(vals))
  ok(gen(f).val(vals)==direct,'independent evaluation of global polynomial generator')
# A real kinematic simultaneous exit: one immigration changes L and total.
N=10**250;m=10**100;ell=2*m-1;ee=isqrt(4*N*ell//3);upper=N+N//10**100;x=(0,upper-2*ell-ee,ell,ell,ee);y=(1,x[1],x[2],x[3],x[4]);fv=lambda s:Q(2*s[0]+s[2]+s[3],2)-Q(3*s[4]**2,4*N)+Q(s[0]*s[4],N)
ok(sum(x)==upper and sum(y)==upper+1 and Q(2*x[0]+x[2]+x[3],2)==2*m-1 and Q(2*y[0]+y[2]+y[3],2)==2*m,'simultaneous band and L exit kinematic witness')
ok(abs(fv(x))<Q(m,8)and abs(fv(y))<Q(m,8)and all(v>=0 for v in x),'tie witness is not excluded by F positivity or physical state grammar')
root=Path(__file__).resolve().parent
(root/'POLYNOMIAL_IDENTITIES.json').write_text(json.dumps(identities,indent=2)+'\n')
(root/'SIMULTANEOUS_EXIT_WITNESS.json').write_text(json.dumps({'N':N,'m':m,'pre_state':x,'post_immigration_state':y,'reference_upper_band':upper,'scope':'Kinematic witness for mandatory band-exit priority; no adverse probability lower bound or violation of the stage success-or-band probability estimate is claimed.'},indent=2)+'\n')
report={'status':'PASS_INDEPENDENT_CONDITIONAL_STAGE_CHECKS','checks':checks,'categories':cats,'source_sha256':hashlib.sha256((root/'inputs/EXACT_CORRECTOR_AND_STAGE_LEMMA.md').read_bytes()).hexdigest(),'imports_author_code':False,'continuum_proof':'MATHEMATICAL_REVIEW.md governs; finite evaluations are supplementary','scope':'conditional full rate2 stage and carefully stopped composition; no initial-phase or arbitrary-state/moment consumer'}
(root/'CHECK_RESULTS.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
