import sys,itertools,numpy as np,json
sys.path.insert(0,'producer-workspace/online_ssf_stress_20261029')
from stress import make_code,choose,reduce
L=3;code=make_code(L);sec=code['sectors'][0];checks=sec['checks'];M=len(checks)
# syndrome graph: checks are adjacent if one data qubit meets both.
adj=[0]*M
for col in sec['cols']:
 for i in range(M):
  if col>>i&1:adj[i]|=col^(1<<i)
animals=[]
for mask in range(1,1<<M):
 seen=mask&-mask
 while True:
  nxt=seen
  for i in range(M):
   if seen>>i&1:nxt|=adj[i]&mask
  if nxt==seen:break
  seen=nxt
 if seen==mask:animals.append(mask)
states=list(sec['reps']);idx={s:i for i,s in enumerate(states)};trans={s:[] for s in states}
for s in states:
 for h,fam in enumerate(sec['families']):
  mv=choose(s,fam)
  if mv:trans[s].append((h,s^mv[1],mv[0]))
rows=[]
for theta in [.01,.03,.1]:
 for a in [.3,1.,2.]:
  for ell in range(2,M+1):
   AA=[A for A in animals if A.bit_count()<=ell]
   vals={s:sum(np.exp(a*A.bit_count())*theta**(A.bit_count()-(A&s).bit_count()) for A in AA) for s in states}
   weights={s:sum(A.bit_count()*np.exp(a*A.bit_count())*theta**(A.bit_count()-(A&s).bit_count()) for A in AA) for s in states}
   dr={s:sum(vals[t]-vals[s] for h,t,f in trans[s]) for s in states}
   s=max(states,key=lambda s:dr[s]/weights[s])
   nontrap=[s for s in states if trans[s]]
   u=max(nontrap,key=lambda s:dr[s]/weights[s])
   rows.append(dict(theta=theta,a=a,ell=ell,max_drift_W=dr[s]/weights[s],syndrome=s,minimum_error=sec['reps'][s],minimum_weight=sec['dist'][s],moves=len(trans[s]),max_nontrap_drift_W=dr[u]/weights[u],nontrap_syndrome=u,nontrap_minweight=sec['dist'][u],nontrap_drift=dr[u],nontrap_W=weights[u],nontrap_moves=trans[u]))
# exact malignant local edges: same syndrome recovery differs by nontrivial logical.
mal=[]
for s in states:
 for q,col in enumerate(sec['cols']):
  t=s^col
  if reduce(sec['reps'][s]^(1<<q)^sec['reps'][t],sec['basis']):
   mal.append(dict(s=s,t=t,q=q,syndrome_weight=s.bit_count(),minimum_weight=sec['dist'][s]))
out=dict(control='cycle HGP, NOT expander counterexample',L=L,syndrome_graph=adj,animals=len(animals),rows=rows,malignant_edges=len(mal),min_syndrome_weight_malignant=min(x['syndrome_weight'] for x in mal),min_weight_malignant=min(x['minimum_weight'] for x in mal),example=min(mal,key=lambda x:x['syndrome_weight']))
print(json.dumps(out,indent=2))
