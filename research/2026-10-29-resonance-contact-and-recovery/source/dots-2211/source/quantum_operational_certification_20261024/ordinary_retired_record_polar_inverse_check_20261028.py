import numpy as np,json,hashlib
from pathlib import Path
rng=np.random.default_rng(2820261031)
def fit(M):
 u,s,v=np.linalg.svd(M);d=np.ones(s.shape);d[...,-1]=np.linalg.det(u@v);return (u*d[...,None,:])@v
max_rem=0.;identity_res=0.
for _ in range(400):
 R=fit(rng.normal(size=(3,3)));V=fit(rng.normal(size=(3,3)));eig=rng.uniform(.2,1,3);S=(V*eig)@V.T;a=min(eig)
 E=rng.normal(size=(3,3));E*=rng.uniform(.001,.45)*a/np.linalg.norm(E);F=R.T@E
 O=R.T@fit(R@S+E);K=O-np.eye(3);skew=V.T@(F-F.T)@V;Omega=V@(skew/(eig[:,None]+eig[None,:]))@V.T
 lhs=S@(K-Omega)+(K-Omega)@S;rhs=-F.T@K+K.T@F-K.T@K@S
 identity_res=max(identity_res,np.linalg.norm(lhs-rhs));assert np.linalg.norm(lhs-rhs)<1e-12
 bound=4*np.linalg.norm(E)**2/a**3;ratio=np.linalg.norm(K-Omega)/bound;max_rem=max(max_rem,ratio);assert ratio<=1+1e-10
rows=[];saved={};calls=0;nb=512
for gamma in [.2,.6]:
 R=fit(rng.normal(size=(3,3)));A=fit(rng.normal(size=(3,3)));S=A@np.diag([np.sqrt(1-gamma),np.sqrt(1-gamma),1-gamma])@A.T
 c=R@A@np.array([0.,0.,gamma]);B=R@S
 for N in [256,1024,4096]:
  ui=rng.integers(0,3,size=(nb,N));vi=rng.integers(0,3,size=(nb,N));us=2*rng.integers(0,2,size=(nb,N))-1;vs=2*rng.integers(0,2,size=(nb,N))-1
  mean=vs*(B[vi,ui]*us+c[vi]);assert max(abs(mean).ravel())<=1+1e-12
  Y=np.where(rng.random((nb,N))<(1+mean)/2,1,-1)
  M=np.zeros((nb,3,3));indices=np.arange(nb)[:,None];np.add.at(M,(indices,vi,ui),9*Y*vs*us/N)
  Q=fit(M);T=np.einsum('bji,jk->bik',Q,R);b=(3-np.trace(T,axis1=1,axis2=2))/4
  calls+=nb*N;saved[f'g{gamma}_N{N}']=M;saved[f'R_g{gamma}']=R;saved[f'B_g{gamma}']=B
  rows.append({'gamma':gamma,'N':N,'banks':nb,'mean_Bell_deficit':float(b.mean()),'mean_M_squared_error':float(np.mean(np.sum((M-B)**2,axis=(1,2)))),'predicted_M_squared_error':float((81-np.linalg.norm(B)**2)/N),'finite_ensemble_mean_rotation_error':float(np.linalg.norm(T.mean(0)-np.eye(3))),'scope':'Finite sample ensemble bias is noisy; not a certificate of exact expected diamond error.'})
p=Path(__file__);np.savez_compressed(p.with_suffix('.npz'),**saved)
out={'status':'PASS_AUTHOR_SYLVESTER_IDENTITIES_AND_ORDINARY_SAMPLED_FIXTURES','identity_checks':400,'max_Sylvester_identity_residual':identity_res,'max_remainder_bound_ratio':max_rem,'ordinary_source_calls_simulated':calls,'independent_banks':6*nb,'seed':2820261031,'scope':'Unknown-axis amplitude damping with dense mixer; ordinary finite Pauli states/readouts. Floating SVD, no production algebraic compiler or pilot confidence acceptance.','rows':rows};out['governing_source']='ordinary_retired_record_polar_inverse_20261028.md';out['governing_source_sha256']=hashlib.sha256(p.with_name(out['governing_source']).read_bytes()).hexdigest();p.with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
