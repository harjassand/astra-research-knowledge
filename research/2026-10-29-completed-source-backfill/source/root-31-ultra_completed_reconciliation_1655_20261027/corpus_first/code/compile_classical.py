"""Acquire a finite exact rational HMM, not just a blockwise decomposition."""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
from fractions import Fraction as F
import json,time
import sympy as S
from exact_instrument import *
BASE=Path(__file__).resolve().parents[1]

def fraction(x):
 x=S.expand(x)
 assert x.is_Rational,x
 return F(int(x.p),int(x.q))
def coordinates(M):
 ans=[fraction(M[i,i]) for i in range(D)]
 for i in range(D):
  for j in range(i+1,D):
   ans += [fraction(S.re(M[i,j])),fraction(S.im(M[i,j]))]
 return ans

def expectation(e,r):
 return sum((e[k]*r[k]*(1 if k<D else 2) for k in range(D*D)),F())
def add_scaled(acc,c,v):
 for k in range(D*D): acc[k]+=c*v[k]
def formatf(x): return str(x.numerator) if x.denominator==1 else str(x)
def enc(v): return [formatf(x) for x in v]

def compile_model():
 t=time.monotonic(); maps=model(); seeds=[]; seed_lookup={}; words={}
 def insert(rho):
  k=key(rho)
  if k not in seed_lookup:
   seed_lookup[k]=len(seeds); seeds.append(rho)
  return seed_lookup[k]
 for a in range(len(maps)):
  for b in range(len(maps)):
   terms=holevo(maps[a],maps[b]); encoded=[]
   actual=choi(lambda X:branch(maps[b]['A'],branch(maps[a]['A'],X)))
   predicted=sum((S.kronecker_product(E.T,rho) for E,rho in terms),S.zeros(D*D))
   assert clean(actual-predicted)==S.zeros(D*D)
   for E,rho in terms:
    assert S.trace(rho)==1
    encoded.append((coordinates(E),insert(rho)))
   words[a,b]=encoded
 print('all 16 word decompositions exact; output seeds',len(seeds),flush=True)
 initial=insert(S.eye(D)/D)
 seed_count=len(seeds)
 states=[coordinates(rho) for rho in seeds]
 state_matrices=seeds[:]
 prefix={}; edges=[[] for _ in maps]
 for j,rho in enumerate(seeds):
  for a,mp in enumerate(maps):
   image=branch(mp['A'],rho); prob=fraction(S.trace(image)); assert prob>0
   normalized=clean(image/S.Rational(prob.numerator,prob.denominator))
   idx=len(states); prefix[j,a]=(idx,prob)
   states.append(coordinates(normalized)); state_matrices.append(normalized)
   edges[a].append([j,idx,prob])
 print('prefix states',len(states),flush=True)
 for j,rho in enumerate(seeds):
  vec=states[j]
  for a in range(len(maps)):
   idx,prob=prefix[j,a]
   for b in range(len(maps)):
    merged={}
    for effect,k in words[a,b]:
     p=expectation(effect,vec)/prob
     assert p>=0,(j,a,b,k,p)
     merged[k]=merged.get(k,F())+p
    for k,p in merged.items():
     if p: edges[b].append([idx,k,p])
 # Every column is stochastic under either control, and each one-step image
 # equals the physical branch image in the full Hermitian matrix space.
 checks=0
 for a,mp in enumerate(maps):
  sums=[[F() for _ in range(D*D)] for _ in states]
  for source,target,p in edges[a]: add_scaled(sums[source],p,states[target])
  for j,M in enumerate(state_matrices):
   assert sums[j]==coordinates(branch(mp['A'],M)),(a,j)
   checks+=1
  print('branch',a,'all exact intertwining columns PASS',flush=True)
 for x in range(2):
  cs=[F() for _ in states]
  for a,mp in enumerate(maps):
   if mp['x']==x:
    for source,target,p in edges[a]: cs[source]+=p
  assert all(p==1 for p in cs)
 result=dict(d=D,controls=2,outcomes=2,word_cutoff_used=2,
  branch_count=len(maps),holevo_terms_per_word=25,seed_count=seed_count,
  classical_states=len(states),initial_state=initial,exact_intertwining_columns=checks,
  sparse_edges=[len(e) for e in edges],normalization='exact rational',
  nonnegativity='exact rational',elapsed_seconds=time.monotonic()-t)
 artifact=dict(result=result,state_coordinates=[enc(v) for v in states],
  maps=[dict(x=m['x'],a=m['a']) for m in maps],
  edges=[[[src,dst,formatf(p)] for src,dst,p in e] for e in edges])
 (BASE/'results'/'CLASSICAL_MODEL.json').write_text(json.dumps(artifact,separators=(',',':'))+'\n')
 (BASE/'results'/'COMPILER_RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result,indent=2))

if __name__=='__main__': compile_model()
