"""Exact finite cyclic-graph audit: null killing, score folding, and canonical law."""
from fractions import Fraction as F
from collections import deque
from pathlib import Path
import itertools,json,time,sys,math
start=time.perf_counter()
edges=[(0,1),(1,2),(2,3),(1,3),(3,4)];cost=[1]*5;p=[F(1,10)]*5;left={0};right={4};checks={1,2,3};adj={i:[] for i in range(5)}
for e,(u,v) in enumerate(edges):adj[u].append((v,e));adj[v].append((u,e))
states=[(u,v,e,b) for e,(u,v) in enumerate(edges) for u,v in [(u,v),(v,u)] for b in (0,1)];sid={s:i for i,s in enumerate(states)};short={tuple(sorted(e)):c for e,c in zip(edges,cost)}
w=[p[e]*2**cost[e] if b else (1-p[e])/2**cost[e] for u,v,e,b in states];delta=[cost[e]*(2*b-1) for u,v,e,b in states]
starts=[i for i,(u,v,e,b) in enumerate(states) if u in left]
# Exhaustive deterministic minimum-cost correction, independent of PyMatching.
def syndrome(mask):return tuple(sum((mask>>e)&1 for _,e in adj[v])%2 for v in sorted(checks))
best={}
for mask in range(1<<len(edges)):
 s=syndrome(mask);key=(sum(cost[e] for e in range(5) if (mask>>e)&1),mask)
 if s not in best or key<best[s]:best[s]=key

def witness(mask):
 c=best[syndrome(mask)][1];res=mask^c
 if not(res&1):return None
 prev={0:None};todo=deque([0]);end=None
 while todo:
  v=todo.popleft()
  if v in right:end=v;break
  for z,e in adj[v]:
   if (res>>e)&1 and z not in prev:prev[z]=(v,e);todo.append(z)
 assert end is not None
 es=[]
 while prev[end] is not None:end,e=prev[end];es.append(e)
 es=tuple(es[::-1]);assert sum(cost[e]*(2*((mask>>e)&1)-1) for e in es)>=0
 return es
PF=sum(math.prod(p[e] if (mask>>e)&1 else 1-p[e] for e in range(5)) for mask in range(32) if witness(mask) is not None)

def solve(A,b):
 n=len(b)
 for k in range(n):
  pivot=next(i for i in range(k,n) if A[i][k]);A[k],A[pivot]=A[pivot],A[k];b[k],b[pivot]=b[pivot],b[k]
  q=A[k][k]
  for j in range(k,n):A[k][j]/=q
  b[k]/=q
  for i in range(n):
   if i==k or not A[i][k]:continue
   q=A[i][k]
   for j in range(k,n):A[i][j]-=q*A[k][j]
   b[i]-=q*b[k]
 return b
rows=[]
for N in [1,2,4]:
 for geo in [False,True]:
  nxt=[]
  for u,v,e,b in states:
   ns=[]
   if v in checks:
    for z,f in adj[v]:
     if z==u:continue
     tri=short.get(tuple(sorted((u,z))),100)>0 and short.get(tuple(sorted((u,z))),100)<cost[e]+cost[f]
     for bb in [0,1]:
      if not(geo and b==bb==0 and tri):ns.append(sid[v,z,f,bb])
   nxt.append(ns)
  M=len(states)*N;A=[[F(int(i==j)) for j in range(M)] for i in range(M)];rhs=[];slack=F(1,1000)
  for i,(u,v,e,b) in enumerate(states):
   for r in range(N):
    rhs.append((F(1,2**r) if v in right else F(0))+slack)
    for j in nxt[i]:A[i*N+r][j*N+(r+delta[j])%N]-=w[j]
  H=solve(A,rhs);assert all(h>0 for h in H)
  def h(i,r):return H[i*N+r]
  Z=sum(w[i]*h(i,delta[i]%N) for i in starts)
  categories={'null':F(0),'repeat':F(0),'terminal':F(0)};terminal=[]
  def visit(i,r,S,es,bs,seen,prob):
   u,v,e,b=states[i]
   if v in right:
    stop=F(1,2**r)/h(i,r);assert stop<=1
    categories['terminal']+=prob*stop;categories['null']+=prob*(1-stop)
    terminal.append((es,bs,S,r,prob*stop));return
   moves=[(j,w[j]*h(j,(r+delta[j])%N)/h(i,r)) for j in nxt[i]]
   assert sum(q for j,q in moves)<=1
   categories['null']+=prob*(1-sum(q for j,q in moves))
   for j,q in moves:
    uu,vv,ee,bb=states[j]
    if vv in seen:categories['repeat']+=prob*q
    else:visit(j,(r+delta[j])%N,S+delta[j],es+(ee,),bs+(bb,),seen|{vv},prob*q)
  for i in starts:
   u,v,e,b=states[i];visit(i,delta[i]%N,delta[i],(e,),(b,),{u,v},w[i]*h(i,delta[i]%N)/Z)
  assert sum(categories.values())==1
  accepted=F(0);wrong_terminal_mass=F(0)
  for es,bs,S,r,mass in terminal:
   path_probability=math.prod(p[e] if b else 1-p[e] for e,b in zip(es,bs))
   assert mass==path_probability*F(2)**(S-r)/Z
   if S<0:continue
   thin=F(1,2**(S-r));assert thin<=1
   outside=[e for e in range(5) if e not in es]
   for vals in itertools.product([0,1],repeat=len(outside)):
    mask=sum(b<<e for e,b in zip(es,bs))+sum(b<<e for e,b in zip(outside,vals))
    if witness(mask)!=es:continue
    pout=math.prod(p[e] if b else 1-p[e] for e,b in zip(outside,vals));accepted+=mass*thin*pout
    # Deliberately omit the r>1 terminal correction: demonstrates a real bias
    # in the tempting but incorrect rounded-terminal variant, not in actual code.
    wrong_terminal_mass+=mass*thin*pout*2**max(0,r-1)
  assert accepted*Z==PF
  if N==4:assert wrong_terminal_mass*Z!=PF
  rows.append({'N':N,'geodesic':geo,'Z_exact':str(Z),'failure_probability_exact':str(PF),'acceptance_exact':str(accepted),'terminal_paths_and_bit_patterns':len(terminal),'total_proposal_mass_exact':str(sum(categories.values())),'null_mass_exact':str(categories['null']),'repeat_mass_exact':str(categories['repeat'])})
# Adversarial numerical proposals for confidence_fast: invalid suggestions must
# only yield wider valid bounds or trigger the exact fallback.
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root/'canonical_qec_witness_20261105'));import confidence_fast as cf
original=cf.beta.ppf;tests=0
for fake in [float('nan'),0.,1.,.5,-10.,10.]:
 cf.beta.ppf=lambda *args,**kwargs:fake
 for n in [1,5,17,31]:
  for x in sorted(set([0,1,n//2,n-1,n])):
   if x>n:continue
   lo,hi=cf.exact_cp(x,n,bits=12);D=4096;den=D**n
   if x:assert (den-cf.cdf_num(n,x-1,int(lo*D),D))*2000<=den
   if x<n:assert cf.cdf_num(n,x,int(hi*D),D)*2000<=den
   tests+=1
cf.beta.ppf=original
out={'status':'PASS: exact full accepted-mass identity including cyclic proposal, null killing, geodesic pruning and score aliases','finite_cases':rows,'adversarial_confidence_quantile_tests':tests,'termination_counterexample':'A one-state T=1,b=0,H=1 satisfies H>=b+TH yet never stops. The actual implementation avoids this with early-repeat rejection and its stronger W>=1+TW certificate.','elapsed_seconds':time.perf_counter()-start}
Path(__file__).with_name('finite_exact_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
