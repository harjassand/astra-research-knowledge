"""Exact actual-generator diagnostics and uniform envelopes; not independent review."""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import hashlib,json
import sympy as s
root=Path(__file__).resolve().parent
z=lambda *ii:tuple(ii.count(i) for i in range(5))
A,B,C,D,E=range(5);two=z(A,A)
pairs=[(z(),z(A),1,1),(two,z(A,C),1,1),(two,z(A,D),1,1),(two,z(A,E),1,1),(z(A,E),z(C,D),1,2),(z(C,D),z(A,B),1,1)]
raw=[r for u,v,k,l in pairs for r in [(u,v,k),(v,u,l)]]
def rate(u,x):
 p=1
 for n,j in zip(x,u):
  for k in range(j):p*=n-k
 return p
def jump(x,u,v):return tuple(a+b-c for a,c,b in zip(x,u,v))
def H(x):
 c=x[A]+x[C];d=x[A]+x[D]
 return Q(2*c*d,c+d) if c+d else Q(0)
def W(x,N):return H(x)-Q(100*x[A]*(x[A]-1),N)
def genvar(x,fn):
 f=fn(x);g=v=0
 for u,w,k in raw:
  q=k*rate(u,x)
  if q<=0:continue
  df=fn(jump(x,u,w))-f;g+=q*df;v+=q*df*df
 return g,v
# Global polynomial identities, not selected numerical substitutions.
a,b,c,d,e=s.symbols('a b c d e');xx=(a,b,c,d,e)
gff=s.expand(sum(k*rate(u,xx)*((jump(xx,u,v)[A])*(jump(xx,u,v)[A]-1)-a*(a-1)) for u,v,k in raw))
want=-6*a**3+10*a*a-2*a+2*a*a*(c+d)+2*a*e+6*a*c*d-2*a*(a-1)*b
assert s.expand(gff-want)==0
for index,other in [(C,d),(D,c)]:
 gc=s.expand(sum(k*rate(u,xx)*((jump(xx,u,v)[A]+jump(xx,u,v)[index])-(a+xx[index])) for u,v,k in raw))
 assert s.expand(gc-(1+a-2*a*a+a*(other+e)))==0
cc,dd=s.symbols('cc dd',positive=True);hh=2*cc*dd/(cc+dd)
assert s.simplify(s.diff(hh,cc)-2*dd**2/(cc+dd)**2)==0
assert s.simplify(s.diff(hh,dd)-2*cc**2/(cc+dd)**2)==0
assert s.simplify(s.diff(hh,cc,dd)-4*cc*dd/(cc+dd)**3)==0
# Literal uniform constant comparisons.
delta=Q(1,10**6);Nmin=200000
assert Q(1,2)-Q(8,1000)-1000*delta>=Q(49,100)
assert 1-Q(4,1000)-Q(200,Nmin)>=Q(49,100)
assert 1-Q(4,1000)>=Q(99,100)
assert Q(1,Nmin*Nmin)+delta/Nmin+3*delta*delta+12*delta<=13*delta
assert 8+24+104*10000*delta<=34
v0=Q(1,4)-delta/2
assert 6*delta+Q(12,Nmin)<=Q(24,100)*v0
assert delta/v0<=Q(5,10**6)
assert 16+34*Q(5,10**6)<=17
assert Q(99,100)+Q(49,100)*499-18>=Q(1,4)*(1+499+1)
assert Q(1,400)-200*Q(1,400)**2==Q(1,800)
assert 2+200*delta<3
# Full-generator rational cases include A=0, A=1, ties and extreme imbalance.
N=10**15;values=[0,1,500,1000,10**4,10**6,10**8,N//16,N//2]
cases=marks=0;ming=None;maxratio=Q(0)
for aa,cc_,dd_,bb,total in product([0,1,2,10,1000,10**5,10**8],values,values,[0,N//4-1,N//4,N//2,N],[N,3*N//2]):
 ee=total-aa-bb-cc_-dd_
 if ee<0:continue
 x=(aa,bb,cc_,dd_,ee);hx=H(x)
 if not 1000<=hx<=delta*N:continue
 g,v=genvar(x,lambda y:W(y,N));X=max(cc_,dd_)+ee
 lower=Q(99,100)+Q(49,100)*aa*X-6*aa*aa-12*aa+Q(200*aa*(aa-1)*bb,N)
 assert g>=lower,(x,hx,g,lower)
 assert g>0 and v<=200*g,(x,hx,g,v)
 if bb>=N//4:assert g>=Q(1+aa*X+aa*aa,4)
 else:assert g>=Q(99,100)+Q(aa*X,4)
 for u,w,k in raw:
  if k*rate(u,x)>0:
   assert abs(W(jump(x,u,w),N)-W(x,N))<=3
   marks+=1
 cases+=1;ming=g if ming is None else min(ming,g);maxratio=max(maxratio,v/g)
# Service-scale and counter margins at the largest admitted m0; smaller m0 helps.
m0=delta;h=Q(400,m0*m0);NN=32*h
assert NN>=Nmin and m0*NN/2>=1000
assert m0*NN-Q(2)-100*m0*m0*NN-m0*NN/2>=Q(2,5)*m0*NN
assert Q(3,16)*m0*m0*h==75
assert Q(1,32)-Q(1,16)*Q(2,3)==-Q(1,96)
assert Q(3,4)+Q(1,16)==Q(13,16)
result={'status':'PASS_AUTHOR_FULL_GENERATOR_RATIONAL_CHECKS_NOT_INDEPENDENT_REVIEW','global_polynomial_identities':3,'actual_states':cases,'actual_mark_checks':marks,'max_Gamma_over_GW_exact':str(maxratio),'proof_sha256':hashlib.sha256((root/'EXPLICIT_HARMONIC_PERSISTENCE_AND_REMOVAL.md').read_bytes()).hexdigest(),'all_actual_channels':12}
(root/'CHECK_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
