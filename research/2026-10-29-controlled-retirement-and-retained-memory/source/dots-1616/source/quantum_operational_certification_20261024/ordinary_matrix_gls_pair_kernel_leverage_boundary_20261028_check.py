from pathlib import Path
from itertools import combinations
import numpy as np,json,hashlib
rng=np.random.default_rng(492817)
results=[];maxres=0.
for k in range(4,11):
 w=np.array([[1,t,t*t,t*t*t] for t in range(1,k+1)],float)
 S=w.T@w;ev,Q=np.linalg.eigh(S);inv=(Q*(1/np.sqrt(ev)))@Q.T;v=w@inv
 maxres=max(maxres,float(np.linalg.norm(v.T@v-np.eye(4))))
 c=min(np.linalg.eigvalsh(v[list(ix)].T@v[list(ix)]).min() for ix in combinations(range(k),4))
 assert c>0 and c>=k**(-28)
 pairs=list(combinations(range(k),2));P=len(pairs);eta=c/(64*P)
 xs=[]
 for i,j in pairs:
  _,_,vh=np.linalg.svd(v[[i,j]])
  z=vh[2]+.381*vh[3];z/=np.linalg.norm(z);xs.append(z)
  assert np.sum((v[[i,j]]@z)**2)<1e-18
 xs.extend(z/np.linalg.norm(z) for z in rng.normal(size=(50,4)))
 xs=np.array(xs);p=(xs@v.T)**2
 assert np.max(np.sum(p<c/4,axis=1))<=3
 f=np.array([4*eta/(p[:,i]+p[:,j]+4*eta) for i,j in pairs]).T
 bound=3+16*P*eta/c
 assert np.max(f.sum(axis=1))<=bound+1e-7
 for tag,pi in [('uniform',np.ones(len(xs))/len(xs)),('random',rng.dirichlet(np.ones(len(xs))))]:
  ef=pi@f;cert=np.max(1/ef);assert cert+1e-7>=P/bound
  results.append({'k':k,'design':tag,'pairs':P,'c':float(c),'eta':float(eta),'max_simultaneously_small':int(np.max(np.sum(p<c/4,axis=1))),'max_pointwise_pair_sum':float(np.max(f.sum(axis=1))),'universal_bound':float(P/bound),'Cauchy_leverage_lower_certificate':float(cert)})
assert maxres<1e-7,maxres
p=Path(__file__).with_name('ordinary_matrix_gls_pair_kernel_leverage_boundary_20261028.md')
out={'status':'PASS author algebraic/numerical checks; independent receiving pending','source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'max_Parseval_residual':maxres,'tested_designs':len(results),'results':results,'source_calls':0,'scope':'Checks one physical Parseval-frame family, pair roots, four-frame positive constants, pointwise packing and leverage lower certificates. Does not simulate source acquisition, solve a design SDP, or claim an operational learning lower bound.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k] for k in ['status','source_sha256','max_Parseval_residual','tested_designs']},indent=2))
