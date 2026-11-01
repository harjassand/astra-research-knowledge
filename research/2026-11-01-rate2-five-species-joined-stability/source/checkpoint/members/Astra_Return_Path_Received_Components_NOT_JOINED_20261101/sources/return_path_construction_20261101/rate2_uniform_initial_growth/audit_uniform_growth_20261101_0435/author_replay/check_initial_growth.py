"""Exact finite algebra checks; not a substitute for the uniform proof."""
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
def mm(x):return x[A]+min(x[C],x[D])
def rr(x):return x[C]+x[D]+x[E]
def phi(x):return min(Q(1),max(Q(0),(96-Q(rr(x),mm(x)+1))/48))
def h(x,N):return 1+Q(16,N)*phi(x)*x[A]**2
def gd(x,N):
 M=mm(x);hx=h(x,N)
 return sum(k*rate(u,x)*(Q(2)**(M-mm(jump(x,u,v)))*h(jump(x,u,v),N)-hx) for u,v,k in raw if rate(u,x))
count=jumps=0
m=20;N=10**8*(m+1)**2
states=set()
for a,c,d,e in product(range(5),repeat=4):
 for b in [N//2,N,10*N]:states.add((a,b,c,d,e))
for a,s in product(range(8),range(5)):
 M=a+s
 for R in [48*(M+1)+j for j in [-2,-1,0,1,2]]+[96*(M+1)+j for j in [-2,-1,0,1,2]]:
  for c,d,e in [(s,s,R-2*s),(s,R-s,0),(R-s,s,0),(s,(R-s)//2,R-s-(R-s)//2)]:
   for b in [N//2,N,100*N]:states.add((a,b,c,d,e))
for x in sorted(states):
 M=mm(x);assert M<m
 neg=0
 for u,v,k in raw:
  q=k*rate(u,x)
  if not q:continue
  y=jump(x,u,v);dm=mm(y)-M
  assert dm in [-1,0,1]
  if dm==-1:neg+=q;assert h(y,N)<=h(x,N)
  if dm==1:assert Q(1,2)*h(y,N)-h(x,N)<=-Q(99,200)
  assert h(y,N)<=Q(101,100)
  jumps+=1
 a,b,c,d,e=x
 assert neg==a+(3 if c==d else 2)*a*(a-1)
 value=gd(x,N)
 assert value<=-Q(12,25),(x,value)
 assert value<=-h(x,N)/4
 count+=1
result={'status':'PASS_AUTHOR_EXACT_CHECKS_NOT_INDEPENDENT_REVIEW','states':count,'enabled_jump_checks':jumps,'all_actual_channels':len(raw),'reference_N':N,'m':m,'proof_sha256':hashlib.sha256((root/'UNIFORM_FULL_GENERATOR_INITIAL_GROWTH.md').read_bytes()).hexdigest()}
(root/'CHECK_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
