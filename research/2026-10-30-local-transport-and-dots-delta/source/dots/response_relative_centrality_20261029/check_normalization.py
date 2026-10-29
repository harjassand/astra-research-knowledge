import numpy as np,json
from pathlib import Path
rng=np.random.default_rng(9182)
paulis=[np.array([[0,1],[1,0]],complex),np.array([[0,-1j],[1j,0]]),np.diag([1.,-1.])]
z=rng.normal(size=(6,2))+1j*rng.normal(size=(6,2));ks=np.linalg.qr(z)[0].reshape(2,3,2)
ds=[sum(k@s@k.conj().T for k in ks) for s in paulis]
def stats(ds):
 K=sum(a@a for a in ds);v,w=np.linalg.eigh(K);iv=w@np.diag(np.where(v>1e-12,v**(-.25),0))@w.conj().T
 A=[iv@a@iv for a in ds]
 defect=lambda x:max(np.linalg.norm(((a@b+b@a)/2)@c-c@((a@b+b@a)/2),2) for a in x for b in x for c in x)
 return K,A,defect(ds),defect(A)
K,A,d,e=stats(ds);rows=[]
for r in [1,2,3,5,9]:
 dr=[np.kron(a,np.eye(r)/r) for a in ds];Kr,Ar,dd,ee=stats(dr)
 assert abs(dd*r**3-d)<1e-10 and abs(ee-e)<1e-10
 assert max(np.linalg.norm(a-np.kron(b,np.eye(r)),2) for a,b in zip(Ar,A))<1e-10
 assert max(np.linalg.norm(a,2) for a in Ar)<=1+1e-10
 rows.append(dict(r=r,raw_defect=dd,normalized_defect=ee,max_axis_norm=max(np.linalg.norm(a,2) for a in Ar)))
out={'scope':'numerical identities only; no approximate-central decoder','rows':rows,'raw_base_defect':d,'normalized_base_defect':e}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print('PASS',len(rows),'junk-dilution / normalized tuple cases')
v,w=np.linalg.eigh(K);S=w@np.diag(np.sqrt(v))@w.conj().T
E=sum(a@a for a in A)-np.eye(len(K));lhs=sum(np.linalg.norm(a@S-S@a,'fro')**2 for a in A);rhs=2*np.trace(K@E).real
assert abs(lhs-rhs)<1e-10
out['fixedpoint_residual']=float(np.linalg.norm(sum(a@S@a for a in A)-S));out['sphere_residual']=float(np.linalg.norm(E,2));out['weighted_commutator_square']=float(lhs);out['dirichlet_rhs']=float(rhs)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print('Dirichlet PASS',lhs,rhs,'sphere',np.linalg.norm(E,2))
