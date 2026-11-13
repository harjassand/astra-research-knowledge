"""Tiny exact sparse-amplitude trajectory backend, Gaussian integers and rational weights.
Exhaustively integrates categories/reset/early records and compares original channel.
"""
from fractions import Fraction as F
from itertools import product
from collections import defaultdict
from pathlib import Path
import json,time,sympy as s
ledger={'max_support':0,'max_amplitude_integer_bits':0,'max_probability_denominator_bits':0,'processed_branches':0}
def register(state,p=F(1)):
 ledger['max_support']=max(ledger['max_support'],len(state));ledger['max_probability_denominator_bits']=max(ledger['max_probability_denominator_bits'],p.denominator.bit_length())
 for a,b in state.values():ledger['max_amplitude_integer_bits']=max(ledger['max_amplitude_integer_bits'],abs(a).bit_length(),abs(b).bit_length())
 ledger['processed_branches']+=1

def norm(st):return sum(a*a+b*b for a,b in st.values())
def diagonal(st,e):
 out={}
 for x,(a,b) in st.items():
  sign=1 if ((x>>e[0])&1)==((x>>e[1])&1) else -1
  out[x]=(3*a-4*sign*b,4*sign*a+3*b)
 return out

def rare(st,e):
 mask=sum(1<<v for v in e);out=defaultdict(lambda:[0,0])
 for x,(a,b) in st.items():out[x][0]+=12*a;out[x][1]+=12*b;out[x^mask][0]+=5*b;out[x^mask][1]-=5*a
 return {x:tuple(v) for x,v in out.items() if v[0] or v[1]}

def measured(st,sites):
 den=norm(st)
 for bits in product([0,1],repeat=len(sites)):
  sub={x:a for x,a in st.items() if all(((x>>v)&1)==b for v,b in zip(sites,bits))};num=norm(sub)
  if num:yield F(num,den),sub,bits

def exact_distribution(n,edges,r,eps,early):
 out=[F(0) for _ in range(1<<n)]
 for categories in product(range(3),repeat=len(edges)):
  catprob=F(1)
  for cat in categories:catprob*=([1-r-eps,eps,r][cat])
  future=[False]*n;earlysites=[[] for _ in edges]
  for t in reversed(range(len(edges))):
   if categories[t]==2:
    for v in edges[t]:future[v]=False
   elif categories[t]==1:
    for v in edges[t]:
     if not future[v]:earlysites[t].append(v)
     future[v]=True
  branches=[(catprob,{0:(1,0)})]
  for t,(e,cat) in enumerate(zip(edges,categories)):
   new=[]
   for prob,st in branches:
    if cat==2:
     mask=sum(1<<v for v in e)
     for p,sub,bits in measured(st,e):
      for bb in product([0,1],repeat=2):
       base=sum(b<<v for v,b in zip(e,bb));fresh={(x&~mask)|base:a for x,a in sub.items()};new.append((prob*p/4,fresh))
    else:
     st=diagonal(st,e)
     if cat==1:st=rare(st,e)
     new.append((prob,st))
   branches=new
   if early and earlysites[t]:
    branches=[(prob*p,sub) for prob,st in branches for p,sub,bits in measured(st,earlysites[t])]
   for prob,st in branches:register(st,prob)
  for prob,st in branches:
   z=norm(st)
   for x,(a,b) in st.items():out[x]+=prob*F(a*a+b*b,z)
 assert sum(out)==1
 return out

def original_density(n,edges,r,eps):
 N=1<<n;rho=s.zeros(N);rho[0,0]=1;rr=s.Rational(r.numerator,r.denominator);ee=s.Rational(eps.numerator,eps.denominator)
 for e in edges:
  mask=sum(1<<v for v in e);D=s.diag(*[(3+(4 if ((x>>e[0])&1)==((x>>e[1])&1) else -4)*s.I)/5 for x in range(N)]);Q=s.Rational(12,13)*s.eye(N)
  for x in range(N):Q[x^mask,x]=-5*s.I/13
  reset=s.zeros(N);rest=[x for x in range(N) if not x&mask];shifts=[0,1<<e[0],1<<e[1],mask]
  for x in rest:
   for y in rest:
    tr=sum(rho[x+b,y+b] for b in shifts)/4
    for b in shifts:reset[x+b,y+b]=tr
  rho=((1-rr-ee)*D*rho*D.conjugate().T+ee*Q*D*rho*D.conjugate().T*Q.conjugate().T+rr*reset).applyfunc(s.expand)
 return [F(int(rho[x,x].p),int(rho[x,x].q)) for x in range(N)]

if __name__=='__main__':
 start=time.time();checks=[]
 for eps in [F(1,50),F(1,20)]:
  n=3;edges=[(0,1),(1,2),(0,1)];r=F(3,100);reference=original_density(n,edges,r,eps)
  for early in [False,True]:
   result=exact_distribution(n,edges,r,eps,early);assert result==reference
   checks.append({'n':n,'edges':edges,'r':str(r),'epsilon':str(eps),'early':early,'all_output_probabilities_equal_exactly':True,'distribution':[str(x) for x in result]})
 output={'checks':checks,'ledger':ledger,'seconds':time.time()-start,'scope':'Exhaustive tiny exact Gaussian-integer trajectory implementation. Sparse global support, no scalable logical-component backend or rank theorem. No floating arithmetic in quantum evolution/probabilities.'}
 Path(__file__).with_suffix('.json').write_text(json.dumps(output,indent=2));print(json.dumps(output,indent=2))
