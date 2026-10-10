"""66 bounded qubit-concurrence interface checks. Distinct from the peel/lift script."""
import json
from pathlib import Path
import numpy as np
rng=np.random.default_rng(947132);tol=3e-10

def gin(n,m):return rng.normal(size=(n,m))+1j*rng.normal(size=(n,m))
def sqrtm(a):
 e,u=np.linalg.eigh((a+a.conj().T)/2)
 return (u*np.sqrt(np.maximum(e,0)))@u.conj().T

def invsqrt(a):
 e,u=np.linalg.eigh((a+a.conj().T)/2)
 return (u*(1/np.sqrt(e)))@u.conj().T

def pt(a,d):return a.reshape(2,d,2,d).transpose(2,1,0,3).reshape(2*d,2*d)
def reda(a,d):return np.einsum('aibi->ab',a.reshape(2,d,2,d))
def concurrence(v,d):
 z=v.reshape(2,d);a=z@z.conj().T
 return 2*np.sqrt(max(0,float(np.linalg.det(a).real)))
flags=[];filters=[];pure=[]
for d in [2,3,4,5,6,8]:
 r=d//2;u,_=np.linalg.qr(gin(d,2*r))
 vs=[np.concatenate([u[:,j],u[:,r+j]])/np.sqrt(2) for j in range(r)]
 V=np.stack(vs,axis=1);z=gin(r,r);tau=z@z.conj().T;tau/=np.trace(tau)
 rho=V@tau@V.conj().T
 low=float(np.linalg.eigvalsh(pt(rho,d))[0]);expected=-float(np.linalg.eigvalsh(tau)[-1])/2
 assert abs(low-expected)<tol
 pol=0
 for i in range(r):
  for j in range(r):
   Mi=vs[i].reshape(2,d).T;Mj=vs[j].reshape(2,d).T
   pol=max(pol,np.linalg.norm(Mi.conj().T@Mj-(np.eye(2)/2 if i==j else 0)))
 assert pol<tol
 flags.append({'d':d,'flag_rank':r,'partial_transpose_min':low,'expected_min':expected,'polarization_error':float(pol)})
 for repeat in range(5):
  g=gin(2*d,2*d);a=g@g.conj().T
  a+=(max(0,-np.linalg.eigvalsh(pt(a,d))[0])+.1)*np.eye(2*d);a/=np.trace(a)
  H=invsqrt(2*reda(a,d));F=np.kron(H,np.eye(d));a=F@a@F.conj().T
  assert np.linalg.eigvalsh(pt(a,d))[0]>-tol
  assert np.linalg.norm(reda(a,d)-np.eye(2)/2)<tol
  W=sqrtm(a);avg=sum(concurrence(W[:,j],d) for j in range(2*d))
  M=gin(2,2);M*=np.sqrt(2)/np.linalg.norm(M);W2=np.kron(M,np.eye(d))@W
  filtered=sum(concurrence(W2[:,j],d) for j in range(2*d));predicted=abs(np.linalg.det(M))*avg
  assert abs(filtered-predicted)<tol and avg<1
  assert abs(np.trace(W2@W2.conj().T)-1)<tol
  filters.append({'d':d,'ensemble_concurrence':float(avg),'filtered_ensemble':float(filtered),'predicted':float(predicted)})
  psi=gin(2*d,1).ravel();psi/=np.linalg.norm(psi)
  U,s,Vh=np.linalg.svd(psi.reshape(2,d),full_matrices=False)
  product=np.outer(U[:,0],Vh[0,:]).ravel()
  distance=float(np.linalg.svd(np.outer(psi,psi.conj())-np.outer(product,product.conj()),compute_uv=False).sum())
  bound=float(np.sqrt(2)*concurrence(psi,d));assert distance<=bound+tol
  pure.append({'d':d,'trace_distance':distance,'sqrt2_concurrence':bound})
report={'status':'PASS','seed':947132,'absolute_tolerance':tol,'flag_cases':flags,'filter_cases':filters,'pure_distance_cases':pure,'scope':'Finite numerical algebra checks only; no optimization of convex roofs or certification of a uniform constant.'}
Path(__file__).with_name('qubit_concurrence_verification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'status':'PASS','flag_cases':len(flags),'filter_cases':len(filters),'pure_distance_cases':len(pure),'max_filter_identity_error':max(abs(x['filtered_ensemble']-x['predicted']) for x in filters)},indent=2))
