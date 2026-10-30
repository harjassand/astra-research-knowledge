"""Finite CP/TNI hybrid diagnostic with actual unsafe leakage that persists."""
import numpy as np,json
from pathlib import Path
I=np.eye(2,dtype=complex);X=np.array([[0,1],[1,0]],complex)
Z=np.diag([1,-1]).astype(complex);H=np.array([[1,1],[1,-1]],complex)/np.sqrt(2)
S=np.diag([1,1j]); rng=np.random.default_rng(31415)
def mat(a,b):
 q=np.zeros((3,3),complex);q[a,b]=1;return q
def sup(ks):return sum(np.kron(k.conj(),k) for k in ks)
def apply(T,r):return (T@r.reshape(-1,order='F')).reshape(r.shape,order='F')
def trnorm(a):return float(np.linalg.svd(a,compute_uv=False).sum())
Ftot=np.eye(36,dtype=complex);Gtot=Ftot.copy();Utot=I.copy();probs=[]
for j in range(12):
 U=[H,S,S@H][j%3];p=float(rng.uniform(.001,.015));probs.append(p)
 good=[np.sqrt(1-p)*np.kron(U,mat(0,a)) for a in [0,1]]
 bad=[np.sqrt(p)*np.kron(X@U,mat(2,a)) for a in [0,1]]+[np.kron(Z@U,mat(2,2))]
 assert np.linalg.norm(sum(k.conj().T@k for k in good+bad)-np.eye(6))<1e-12
 Ftot=sup(good+bad)@Ftot;Gtot=sup(good)@Gtot;Utot=U@Utot
# Choi on logical input with initially safe aux0. Use explicit blocks.
CF=np.zeros((12,12),complex);CG=CF.copy()
for i in range(2):
 for j in range(2):
  E=np.zeros((2,2),complex);E[i,j]=1
  initial=np.kron(E,mat(0,0))
  CF[i*6:(i+1)*6,j*6:(j+1)*6]=apply(Ftot,initial)
  CG[i*6:(i+1)*6,j*6:(j+1)*6]=apply(Gtot,initial)
survival=float(np.prod(1-np.array(probs)));loss=1-survival
assert np.linalg.eigvalsh(CF-CG).min()>-1e-12
normalized_choi_difference=trnorm((CF-CG)/2)
assert abs(normalized_choi_difference-loss)<1e-11 and loss<=sum(probs)
# Exact ideal-prefix output factor remains U_total, safe aux0, subnormalized.
psi=np.array([1,1j],complex)/np.sqrt(2);rho=np.outer(psi,psi.conj())
f=apply(Ftot,np.kron(rho,mat(0,0)));g=apply(Gtot,np.kron(rho,mat(0,0)))
expected=survival*np.kron(Utot@rho@Utot.conj().T,mat(0,0))
res=float(np.linalg.norm(g-expected));assert res<1e-11
actual_leak=float(np.trace(f.reshape(2,3,2,3)[:,2,:,2]).real)
assert abs(actual_leak-loss)<1e-11
logical=np.einsum('iaja->ij',f.reshape(2,3,2,3))
logical_error=trnorm(logical-Utot@rho@Utot.conj().T)
assert logical_error<=2*sum(probs)+1e-11
out={'cycles':12,'sum_uniform_source_errors':sum(probs),'comparison_trace_loss':loss,
 'normalized_reference_Choi_difference':normalized_choi_difference,
 'actual_unsafe_population':actual_leak,'ideal_prefix_factor_residual':res,
 'actual_reduced_logical_trace_error':logical_error,'normalization_budget_2sum':2*sum(probs),
 'scope':'Finite hybrid algebra diagnostic, not native dynamics/gadget threshold simulation. Actual unsafe states persist; only ideal prefixes return safe.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
