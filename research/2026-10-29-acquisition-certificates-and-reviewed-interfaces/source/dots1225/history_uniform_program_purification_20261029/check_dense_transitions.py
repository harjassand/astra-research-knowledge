import itertools,math,json,numpy as np
from pathlib import Path

def wedge(d,k):
 cols=[];sets=list(itertools.combinations(range(d),k))
 for subset in sets:
  a=np.zeros(d**k)
  for p in itertools.permutations(subset):
   inv=sum(p[i]>p[j] for i in range(k) for j in range(i+1,k));idx=0
   for v in p:idx=idx*d+v
   a[idx]=(-1)**inv/math.sqrt(math.factorial(k))
  cols.append(a)
 return np.array(cols).T,sets
rows=[]
for d,k in [(3,1),(3,2),(4,1),(4,2),(4,3)]:
 x=.07;a=(1-x)/(d-1);V,sets=wedge(d,k);Vn,_=wedge(d,k+1);P=Vn@Vn.T;F=np.eye(d**(k+1))-P
 occ=np.diag([sum(t==0 for t in tup) for tup in itertools.product(range(d),repeat=k)])
 Nold=np.kron(occ,np.eye(d));Nnew=np.diag([sum(t==0 for t in tup) for tup in itertools.product(range(d),repeat=k+1)])
 sigma=np.diag([x]+[a]*(d-1));Sactual=np.zeros((2,2));Factual=np.zeros((2,2))
 for cls in [0,1]:
  chosen=[j for j,ss in enumerate(sets) if (0 in ss)==bool(cls)]
  rho=V[:,chosen]@V[:,chosen].T/len(chosen);inp=np.kron(rho,sigma)
  out=P@inp@P;tot=np.trace(out);dark=np.trace(Nnew@out);Sactual[:,cls]=[tot-dark,dark]
  out=F@inp@F;tot=np.trace(out);dark=np.trace(Nold@out);Factual[:,cls]=[tot-dark,dark]
 S=np.array([[(d-1-k)*a/(k+1),0],[x/(k+1),(d-k)*a/(k+1)]])
 f01=k*x/(k+1)**2;f10=(d-k)*a/(k+1)**2
 FF=np.array([[1-S[:,0].sum()-f01,f10],[f01,1-S[:,1].sum()-f10]])
 er=max(np.max(abs(S-Sactual)),np.max(abs(FF-Factual)));assert er<1e-12
 rows.append(dict(d=d,k=k,max_residual=float(er)))
Path(__file__).with_suffix('.json').write_text(json.dumps(rows,indent=2)+'\n');print(rows)
