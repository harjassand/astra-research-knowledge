import itertools,json,time,random
from collections import Counter
P=list(itertools.permutations(range(4))); ix={p:i for i,p in enumerate(P)}
def comp(p,q):return tuple(p[q[i]] for i in range(4))
def inv(p):return tuple(p.index(i) for i in range(4))
R=[[ix[comp(p,inv(q))] for q in P] for p in P]
L=[]
for inds in itertools.combinations(range(24),4):
 if all(len({P[k][j] for k in inds})==4 for j in range(4)): L.append(inds)
print('Latin sets',len(L),flush=True)
def factor(C):
 support=[i for i,v in enumerate(C) if v]
 nB=0
 for bs in itertools.combinations_with_replacement(support,4):
  B=Counter(bs)
  if any(v>C[k] for k,v in B.items()):continue
  nB+=1
  ts=[]; seen=set()
  for h in range(24):
   t=[0]*24
   for b in bs:t[R[b][h]]+=1
   t=tuple(t)
   if t not in seen and all(v<=C[i] for i,v in enumerate(t)):
    seen.add(t);ts.append((t,h))
  target=list(C)
  for b in bs:target[b]-=1
  # Match three translated copies to C-B.
  valids=[(t,h) for t,h in ts if all(v<=target[i] for i,v in enumerate(t))]
  pair={}
  for ai,(a,ha) in enumerate(valids):
   for b,hb in valids[ai:]:
    s=tuple(x+y for x,y in zip(a,b))
    if all(v<=target[i] for i,v in enumerate(s)):pair[s]=(ha,hb)
  for a,ha in valids:
   rem=tuple(x-y for x,y in zip(target,a))
   if rem in pair:return {'B':bs,'H':(0,ha,*pair[rem]),'nB':nB}
 return {'nB':nB}
r=random.Random(993718); t=time.perf_counter()
for trial in range(200):
 ls=r.choices(L,k=4); C=[0]*24
 for a in ls:
  for i in a:C[i]+=1
 f=factor(tuple(C)); print(trial, 'factor' if 'B'in f else 'NO FACTOR',f['nB'],time.perf_counter()-t,flush=True)
 if 'B' not in f:
  out={'D':4,'n':3,'permutations':P,'counts':C,'latin_sets':ls,'factor_test':f,'trials':trial+1,'wall_seconds':time.perf_counter()-t}
  open('/Users/harjas/Documents/Codex/2026-10-21/take-principal-ownership-of-a-substantive/work/Cycle3/invariant/PARTITION_COUNTEREXAMPLE.json','w').write(json.dumps(out,indent=2)+'\n');break
