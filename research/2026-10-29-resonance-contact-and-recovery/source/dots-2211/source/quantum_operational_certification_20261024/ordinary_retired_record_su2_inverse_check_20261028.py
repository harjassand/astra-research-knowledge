import numpy as np,json
from pathlib import Path
rng=np.random.default_rng(202610282026)
def fit(M):
 u,s,v=np.linalg.svd(M);d=np.ones(s.shape);d[...,-1]=np.linalg.det(u@v);return (u*d[...,None,:])@v

def rotations(k):
 x=rng.normal(size=(k,3,3));return fit(x)
checks=0;maxcov=0.;maxpolar=0.
for _ in range(200):
 R,A,B=rotations(3);M=R+rng.normal(size=(3,3))*.04;E=rng.normal(size=(3,3))*.01;Q=fit(M);Qp=fit(M+E)
 res=np.linalg.norm(fit(A@M@B.T)-A@Q@B.T);maxcov=max(maxcov,res);assert res<1e-12
 upper=2*np.linalg.norm(E)/(np.linalg.svd(M,compute_uv=False)[-1]+np.linalg.svd(M+E,compute_uv=False)[-1])
 ratio=np.linalg.norm(Qp-Q)/upper;maxpolar=max(maxpolar,ratio);assert ratio<=1+1e-12;checks+=1
rows=[];saved={};calls=0;N=2048;banks=256
for a in [.5,1.]:
 for ri,R in enumerate(rotations(2)):
  u=rng.normal(size=(banks,N,3));u/=np.linalg.norm(u,axis=-1)[...,None]
  v=rng.normal(size=(banks,N,3));v/=np.linalg.norm(v,axis=-1)[...,None]
  mean=a*np.einsum('bni,ij,bnj->bn',v,R,u)
  y=np.where(rng.random((banks,N))<(1+mean)/2,1.,-1.)
  C=np.einsum('bn,bni,bnj->bij',y,v,u)/N;M=9*C/a;Q=fit(M)
  err=np.linalg.norm(Q-R,axis=(-2,-1));raw=np.linalg.norm(M-R,axis=(-2,-1));assert np.all(err<=2*raw+1e-12)
  b=err**2/8;T=np.einsum('bji,jk->bik',Q,R)
  assert np.max(np.abs(b-(3-np.trace(T,axis1=1,axis2=2))/4))<1e-12
  saved[f'a{a}_R{ri}']=C;saved[f'R_a{a}_R{ri}']=R;calls+=N*banks
  rows.append({'a':a,'N':N,'banks':banks,'mean_Bell_deficit':float(b.mean()),'standard_error':float(b.std(ddof=1)/np.sqrt(banks)),'ideal_analytic_bound':float((81/a**2-3)/(2*N)),'mean_M_squared_error':float((raw**2).mean()),'predicted_M_squared_error':float((81/a**2-3)/N),'finite_ensemble_anisotropy':float(np.linalg.norm(T.mean(0)-np.eye(3)*np.trace(T.mean(0))/3))})
path=Path(__file__);np.savez_compressed(path.with_suffix('.npz'),**saved)
out={'status':'PASS_AUTHOR_IDENTITIES_AND_FLOATING_HAAR_FIXTURE','polar_and_covariance_checks':checks,'max_covariance_residual':maxcov,'max_polar_bound_ratio':maxpolar,'actual_simulated_probe_calls':calls,'independent_banks':4*banks,'seed':202610282026,'scope':'Gaussian normalized vectors simulate ideal sphere design; finite-grid mechanism is analytic, not executed here. Floating SVD is not the finite algebraic compiler. Samples test mechanism, not exact ensemble isotropy.','rows':rows};path.with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
