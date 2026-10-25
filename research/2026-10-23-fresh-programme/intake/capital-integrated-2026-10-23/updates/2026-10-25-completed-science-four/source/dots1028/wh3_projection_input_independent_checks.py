"""Independent bounded checks of algebraic interfaces; not proof of universal theorem."""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
import numpy as np,json,time
from pathlib import Path
start=time.perf_counter();rng=np.random.default_rng(202610250848)
def ent(A):
 w=np.linalg.eigvalsh((A+A.conj().T)/2);w=w[w>1e-14];return float(-np.sum(w*np.log(w)))
def log(A):
 w,v=np.linalg.eigh(A);assert min(w)>0;return (v*np.log(w))@v.conj().T
cases=[]
for m in [1,2,3,4]:
 n=3*m;Z=rng.normal(size=(3*n,m))+1j*rng.normal(size=(3*n,m));U=np.linalg.qr(Z)[0];P=U@U.conj().T
 def E(X):
  R=np.trace(X.reshape(3,n,3,n),axis1=0,axis2=2)
  return np.kron(np.eye(3)/3,R)
 def N(X):
  R=np.trace(X.reshape(3,n,3,n),axis1=0,axis2=2);PT=X.reshape(3,n,3,n).transpose(2,1,0,3).reshape(3*n,3*n)
  return (np.kron(np.eye(3),R)-PT)/2
 B=E(P);NP=N(P);C=(P+3*B)/4
 survivor=U.conj().T@(2*log(C)-log(B))@U
 row={'projection_rank':m,'reference_dimension':n,'projection_residual':float(np.linalg.norm(P@P-P)),'marginal_min_eigenvalue':float(np.linalg.eigvalsh(B)[0]),'saturated_compressed_inverse_error':float(np.linalg.norm(U.conj().T@np.linalg.solve(B,U)-9*np.eye(m))),'complement_index_min_eigenvalue':float(np.linalg.eigvalsh(8*np.eye(3*n)-9*B+P)[0]),'channel_square_error':float(np.linalg.norm(N(NP)-C)),'survivor_max_eigenvalue':float(np.linalg.eigvalsh(survivor)[-1]),'homogeneous_entropy_gap':2*ent(NP)-ent(B)}
 assert row['projection_residual']<1e-10 and row['saturated_compressed_inverse_error']<1e-8 and row['channel_square_error']<1e-10
 assert row['complement_index_min_eigenvalue']>-1e-10 and row['survivor_max_eigenvalue']<1e-9 and row['homogeneous_entropy_gap']>-1e-9
 cases.append(row)
out={'scope':'Four reproducible generic projector diagnostics; universal statement is analytically audited separately','seed':202610250848,'cases':cases,'seconds':time.perf_counter()-start}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
