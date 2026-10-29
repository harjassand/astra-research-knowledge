import numpy as np,math,json
from itertools import combinations
from pathlib import Path
rng=np.random.default_rng(20261029)
I=np.eye(2);P=[np.array([[0,1],[1,0]],complex),np.array([[0,-1j],[1j,0]]),np.diag([1,-1])]
def kronall(xs):
 a=np.array([[1]],complex)
 for x in xs:a=np.kron(a,x)
 return a
rows=[]
for n in [3,4,5]:
 edges=list(combinations(range(n),2));alpha=1/(n-1);L=len(edges)*alpha;g=1.;eps=.5
 terms=[]
 for u,v in edges:
  mats=[I]*n;mats=mats.copy();mats[u]=P[int(rng.integers(3))];mats[v]=P[int(rng.integers(3))]
  terms.append((1 if rng.integers(2) else -1)*alpha*kronall(mats))
 H=sum(terms);q=math.ceil(512*L*L/(eps*eps*n));lam=512*g*g/(eps*eps)+4*g/eps
 D=math.ceil(9*lam)+math.ceil(math.log2(max(2,200*g/eps)))
 worst=0.;deleted=0;maxdeg=0
 for trial in range(40):
  counts=rng.multinomial(q,np.ones(len(edges))/len(edges));deg=np.zeros(n,int)
  for c,(u,v) in zip(counts,edges):deg[u]+=c;deg[v]+=c
  bad=deg>D;keep=[not(bad[u] or bad[v]) for u,v in edges]
  Hhat=sum((L/q)*c*h/alpha for c,h in zip(counts,terms))
  Htilde=sum(((L/q)*c*h/alpha for c,h,k in zip(counts,terms,keep) if k),np.zeros_like(H))
  ndelete=sum(c for c,k in zip(counts,keep) if not k)
  assert np.linalg.norm(Hhat-Htilde,2)<=(L/q)*ndelete+1e-10
  finaldeg=np.zeros(n,int)
  for c,(u,v),k in zip(counts,edges,keep):
   if k:finaldeg[u]+=c;finaldeg[v]+=c
  assert max(finaldeg)<=D
  err=np.linalg.norm(Htilde-H,2);worst=max(worst,err);deleted+=ndelete;maxdeg=max(maxdeg,int(max(deg)))
 rows.append({'n':n,'terms':len(edges),'sample_count':q,'degree_cap':D,'largest_sampled_degree':maxdeg,'trials':40,'maximum_operator_error':worst,'promised_operator_budget':eps*n/2,'deleted_occurrences':int(deleted)})
res={'seed':20261029,'cases':rows,'scope':'Small dense diagnostic of normalization, operator errors and degree/deletion bookkeeping; does not statistically validate tiny tail probabilities. Conservative theoretical cap caused no deletions here.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res,indent=2))
