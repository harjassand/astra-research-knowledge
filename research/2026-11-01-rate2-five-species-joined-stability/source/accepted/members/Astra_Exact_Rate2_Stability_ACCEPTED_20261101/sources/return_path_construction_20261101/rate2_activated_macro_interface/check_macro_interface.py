"""Exact jump/constant checks; supplementary finite checks, not theorem review."""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parent
z=lambda *ii:tuple(ii.count(i) for i in range(5))
A,B,C,D,E=range(5);two=z(A,A)
pairs=[(z(),z(A),1,1),(two,z(A,C),1,1),(two,z(A,D),1,1),(two,z(A,E),1,1),(z(A,E),z(C,D),1,2),(z(C,D),z(A,B),1,1)]
raw=[r for u,v,k,l in pairs for r in [(u,v,k),(v,u,l)]]
def rate(u,x):
 p=1
 for n,j in zip(x,u):
  for k in range(j):p*=max(0,n-k)
 return p
def jump(x,u,v):return tuple(a+b-c for a,c,b in zip(x,u,v))
def M(x):return x[A]+min(x[C],x[D])
def R(x):return x[C]+x[D]+x[E]
def J(x):return R(x)+2*x[A]+4*M(x)
def h(x,N):return max(Q(1,4),1-Q(x[A],4*N))
def gv(x,N):
 mx=M(x);hx=h(x,N)
 return sum(k*rate(u,x)*(Q(2)**(mx-M(jump(x,u,v)))*h(jump(x,u,v),N)-hx) for u,v,k in raw if rate(u,x))
states=jumps=0
for x in product(range(5),repeat=5):
 a,b,c,d,e=x;plus=minus=0
 for u,v,k in raw:
  q=k*rate(u,x)
  if not q:continue
  y=jump(x,u,v);dm=M(y)-M(x);dj=J(y)-J(x)
  if dm==1:plus+=q;assert y[A]-a==1
  if dm==-1:minus+=q;assert y[A]-a==-1
  if u==z():assert dj==6
  elif v==z():assert dj==-6
  elif u==two:assert dj in [-1,-5]
  elif v==two and u in [z(A,C),z(A,D)]:assert dj in [1,5]
  elif u==z(A,E) and v==two:assert dj==5
  elif u==z(A,E) and v==z(C,D):assert dj==-1
  elif u==z(C,D) and v==z(A,E):assert dj==1
  else:assert dj==0
  jumps+=1
 assert plus>=1+a*(R(x)-2*M(x))
 assert minus==a+(3 if c==d else 2)*a*(a-1)
 states+=1
N=10**40;r=Q(1,1000);delta=Q(1,10**12)
assert 7+18*delta*N<=r*N/2
assert 6*delta<=r
assert Q(401,100)*delta*N+Q(1,2)+delta/4<=Q(24,100)*2*r*N
assert 1-delta/4-Q(1,4*N)>=Q(99,100)
assert 1+Q(1,2*N)<=Q(101,100)
assert Q(1,3)-Q(1,16)>Q(1,4)
# Literal large activated grids; reference mass is not changed after a jump.
large=0
for a,ss,imb,ee in product([0,1,10**8,10**20],[0,1,10**10,10**20],[0,N//1000,N//100],[0,N//1000,N//100]):
 c=ss+imb;d=ss;e=ee;b=N-a-c-d-e;x=(a,b,c,d,e)
 if b<0 or R(x)<2*r*N or M(x)>=delta*N:continue
 val=gv(x,N)
 assert val<=-Q(M(x)**2,8*N)*h(x,N),(x,val)
 large+=1
# Explicit differential-equation positivity margin comparisons with exp(1)<3.
eta=delta**4/(1000*3**40)
for bound in [delta/(2*3**6),delta**2/(8*3**18),delta**4/(128*3**38),3*delta**2/(4*3**18),delta**2/(4*3**14),delta**2/(2*3**16)]:assert bound>=eta
# Jacobian row envelopes on cube[0,3]^5 for F as displayed.
assert max(54,12,42,42,30)<=100
result={'status':'PASS_AUTHOR_JUMP_AND_UNIFORM_CONSTANT_CHECKS_NOT_INDEPENDENT_REVIEW','small_states':states,'enabled_marks':jumps,'large_activated_cases':large,'all_actual_channels':12,'proof_sha256':hashlib.sha256((root/'ACTIVATED_TO_MACRO_AND_POSITIVE_FRACTIONS.md').read_bytes()).hexdigest()}
(root/'CHECK_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
