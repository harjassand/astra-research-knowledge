"""Independent deterministic algebra checks. No source trials or hardware data."""
import numpy as np,json,hashlib
from pathlib import Path
rng=np.random.default_rng(280134)
def pt(A,k):return A.reshape(2,k,2,k).transpose(2,1,0,3).reshape(2*k,2*k)
def ptr(A,k):return np.trace(A.reshape(2,k,2,k),axis1=0,axis2=2)
def iso(n,m):
 z=rng.normal(size=(n,m))+1j*rng.normal(size=(n,m));return np.linalg.qr(z)[0][:,:m]
phi=np.array([1,0,0,1])/np.sqrt(2);P=np.outer(phi,phi)
Jminus=np.array([[0,-1],[1,0]])
res={'filter_identity':0.,'observable_identity':0.,'acceptance_identity':0.,'ad_example':0.}
count=0
for k in (2,3,5,8):
 for _ in range(120):
  VA=iso(2,2);VB=iso(k,2);s=rng.uniform(.0001,.9999)
  v=np.kron(VA,VB)@np.array([np.sqrt(s),0,0,np.sqrt(1-s)])
  W=pt(np.outer(v,v.conj()),k)
  FA=(VA@np.diag([np.sqrt(s),np.sqrt(1-s)])@Jminus).T;FB=VB.conj().T;F=np.kron(FA,FB)
  res['filter_identity']=max(res['filter_identity'],float(np.linalg.norm(W-2*F.conj().T@(.5*np.eye(4)-P)@F)))
  # Physical arbitrary channel via isometry to receiver times environment.
  r=3; V=iso(k*r,2);Ks=[V.reshape(k,r,2)[:,j,:] for j in range(r)]
  J=sum(np.outer(K.T.reshape(-1),K.T.reshape(-1).conj())/2 for K in Ks)
  # Solve the exact loss-state transform J=2 I tensor Tr_A T - 3T.
  T=(2*np.kron(np.eye(2),ptr(J,k))-J)/3
  assert np.linalg.eigvalsh(T).min()>-1e-12 and abs(np.trace(T)-1)<1e-12
  O=2*np.kron(np.eye(2),ptr(np.outer(v,v.conj()),k))-3*W
  theta=np.trace(J@W).real
  res['observable_identity']=max(res['observable_identity'],float(abs(np.trace(T@O)-theta)))
  Jf=F@J@F.conj().T;a=np.trace(Jf).real;FF=np.trace(Jf@P).real/a
  res['acceptance_identity']=max(res['acceptance_identity'],float(abs(theta-a*(1-2*FF))))
  assert theta>=-np.sqrt(s*(1-s))-1e-12
  assert np.linalg.norm(O,2)<=5+1e-12
  count+=1
for r in (1/256,1/64,1/16,1/4,1/2):
 K0=np.diag([1,np.sqrt(r)]);K1=np.array([[0,np.sqrt(1-r)],[0,0]])
 J=sum(np.outer(K.T.reshape(-1),K.T.reshape(-1).conj())/2 for K in (K0,K1))
 v=np.array([0,1,-np.sqrt(r),0])/np.sqrt(1+r)
 F=np.kron(np.diag([1,np.sqrt(r)])/np.sqrt(1+r),np.eye(2));Jf=F@J@F.T
 a=np.trace(Jf);FF=np.trace(P@Jf)/a
 err=max(np.linalg.norm(pt(J,2)@v+(r/2)*v),abs(a-.5),abs(FF-(1+r)/2))
 res['ad_example']=max(res['ad_example'],float(err))
assert max(res.values())<1e-10
p=Path(__file__).parent
out={'kind':'deterministic algebra, no source sampling','random_complex_physical_cases':count,'amplitude_damping_cases':5,'max_residuals':res,'source_sha256':hashlib.sha256((p/'ORDINARY_NPT_FILTERED_SEED_FRONTEND.md').read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'pass':True}
(p/'npt_frontend_root_checks.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
