import numpy as np,json
from pathlib import Path
rng=np.random.default_rng(20261028)
I=np.eye(2); P=np.array([I,[[0,1],[1,0]],[[0,-1j],[1j,0]],[[1,0],[0,-1]]],complex)
def psd(x):
 d,u=np.linalg.eigh(x);return (u*np.maximum(d,0)[...,None,:])@u.conj().swapaxes(-1,-2)
def project(y,mult):
 # compressed per-label coordinates, metric sum mult_i||x_i-y_i||²
 x=y.copy();p=np.zeros_like(x);q=p.copy();A=sum(mult)
 for k in range(20000):
  z=psd(x+p);p=x+p-z
  u=z+q;v=u+(I-np.einsum('i,ijk->jk',mult,u))/A
  q=u-v
  if np.max(abs(v-x))<1e-13:
   x=v;break
  x=v
 return x,k+1
A=64;full=np.repeat((I/A)[None,:,:],A,axis=0).astype(complex)
known=[];maxdiff=0;maxit=0;maxresid=0
for t in range(24):
 x=int(rng.integers(A));w=int(rng.integers(4));b=int(rng.choice([-1,1]));G=.04*b*P[w]
 if x not in known:known.append(x)
 unseen=[i for i in range(A) if i not in known]
 cent=full.copy();cent[x]+=G
 cf=np.array([cent[i] for i in known]+([cent[unseen[0]]] if unseen else []))
 mult=np.array([1]*len(known)+([len(unseen)] if unseen else []))
 out,it=project(cent,np.ones(A));co,jt=project(cf,mult)
 rebuilt=np.empty_like(out)
 for i,k in enumerate(known):rebuilt[k]=co[i]
 for k in unseen:rebuilt[k]=co[-1]
 maxdiff=max(maxdiff,float(np.max(abs(out-rebuilt))));maxit=max(maxit,it,jt)
 maxresid=max(maxresid,float(np.max(abs(out.sum(0)-I))))
 assert np.min(np.linalg.eigvalsh(out))>-1e-10
 full=out
assert maxdiff<1e-10
out={'projection_pairs':24,'alphabet':A,'flag_dimension':2,'maximum_full_compressed_difference':maxdiff,'maximum_affine_residual':maxresid,'maximum_dykstra_iterations':maxit,'scope':'floating diagnostic of projection symmetry only; not certified finite solver, source pilot, or statistical guarantee'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
