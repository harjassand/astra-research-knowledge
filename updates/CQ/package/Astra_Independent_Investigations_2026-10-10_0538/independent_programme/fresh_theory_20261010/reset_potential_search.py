"""Exact tests for pair-distance MST as an amortized synchronization potential."""
from collections import deque
from itertools import combinations,product
import random,json,time

def pair_dist(A):
 n=len(A[0]); pairs=[(i,j) for i in range(n) for j in range(i,n)]
 idx={p:k for k,p in enumerate(pairs)}; rev=[[] for _ in pairs]
 for k,(i,j) in enumerate(pairs):
  for a,f in enumerate(A):
   u,v=sorted((f[i],f[j]));rev[idx[u,v]].append((k,a))
 d=[None]*len(pairs);words=[None]*len(pairs);q=deque()
 for i in range(n):d[idx[i,i]]=0;words[idx[i,i]]=();q.append(idx[i,i])
 while q:
  k=q.popleft()
  for h,a in rev[k]:
   if d[h] is None:d[h]=d[k]+1;words[h]=(a,)+words[k];q.append(h)
 return {p:d[k] for k,p in enumerate(pairs)},{p:words[k] for k,p in enumerate(pairs)}

def mst(S,d):
 if len(S)<2:return 0
 seen={S[0]};rest=set(S[1:]);total=0
 while rest:
  v,c=min(((v,min(d[tuple(sorted((v,u)))] for u in seen)) for v in rest),key=lambda z:(z[1],z[0]))
  total+=c;seen.add(v);rest.remove(v)
 return total

def image(S,A,w):
 for a in w:S=tuple(sorted({A[a][i] for i in S}))
 return S

def reset_bfs(A,start=None):
 n=len(A[0]);start=tuple(range(n)) if start is None else start
 q=deque([start]);dw={start:()}
 while q:
  S=q.popleft();w=dw[S]
  if len(S)<=1:return w,len(dw)
  for a in range(len(A)):
   T=image(S,A,(a,))
   if T not in dw:dw[T]=w+(a,);q.append(T)
 return None,len(dw)

def audit(A,allsub=False):
 n=len(A[0]);d,words=pair_dist(A)
 if any(x is None for x in d.values()):return None
 full=tuple(range(n));w,_=reset_bfs(A)
 res={'n':n,'A':A,'pair_dist':{'%d,%d'%p:v for p,v in d.items()},'mst_full':mst(full,d),'reset_length':len(w),'reset_word':w}
 if len(w)>res['mst_full']:res['failure']='MST underestimates reset length';return res
 for r in range(2,n+1) if allsub else [n]:
  for S in combinations(range(n),r):
   p=mst(S,d)
   vals=[mst(image(S,A,(a,)),d) for a in range(len(A))]
   if min(vals)>=p:
    merging=[{'pair':pair,'word':words[pair],'cost_plus_potential':len(words[pair])+mst(image(S,A,words[pair]),d)} for pair in combinations(S,2)]
    res.update({'failure':'one-letter descent fails','S':S,'potential':p,'letter_potentials':vals,'pair_merges':merging})
    return res
 return res

def main():
 out=[]
 for n in range(2,11):
  A=[tuple((i+1)%n for i in range(n)),tuple(0 if i==n-1 else i for i in range(n))]
  r=audit(A,True);out.append(r)
  print('Cerny',n,'MST',r['mst_full'],'reset',r['reset_length'],r.get('failure'),r.get('S'),flush=True)
 rng=random.Random(20261011)
 for n in range(3,8):
  for t in range(2000):
   A=[tuple(rng.randrange(n) for _ in range(n)) for _ in range(2)]
   r=audit(A,True)
   if r and r.get('failure')=='MST underestimates reset length':
    out.append(r);print(json.dumps(r,indent=2),flush=True)
    json.dump(out,open('independent_programme/fresh_theory_20261010/reset_potential_results.json','w'),indent=2);return
  print('random passed',n,flush=True)
 json.dump(out,open('independent_programme/fresh_theory_20261010/reset_potential_results.json','w'),indent=2)
if __name__=='__main__':main()
