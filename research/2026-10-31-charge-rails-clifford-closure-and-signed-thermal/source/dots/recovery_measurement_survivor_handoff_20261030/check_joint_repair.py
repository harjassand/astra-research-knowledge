"""Finite joint logical algebra diagnostics, not native drift/gadget certification."""
import numpy as np, json
from pathlib import Path
I=np.eye(2,dtype=complex); X=np.array([[0,1],[1,0]],complex)
Z=np.diag([1,-1]).astype(complex)
P=[np.diag([1,0]).astype(complex),np.diag([0,1]).astype(complex)]
def k3(a,b,c): return np.kron(np.kron(a,b),c)
def apply(ks,r): return sum((k@r@k.conj().T for k in ks),np.zeros_like(r))
def choi(ks):
 return sum((np.outer(k.reshape(-1,order='F'),k.reshape(-1,order='F').conj()) for k in ks),np.zeros((64,64),complex))
def trnorm(a):return float(np.linalg.svd(a,compute_uv=False).sum())
p=.037
# M,C first factor; S unknown second factor; retained auxiliary A third factor.
# Good branch bath unitary explicitly depends on z. Bad map preserves M coherences
# and flips survivor S; it is not incorrectly assumed to be another good instrument.
V=[I,X]
actual=[np.sqrt(1-p)*k3(P[z],I,V[z]) for z in range(2)]+[np.sqrt(p)*k3(I,X,I)]
repaired=[np.sqrt(1-p)*k3(P[z],I,V[z]) for z in range(2)]+[np.sqrt(p)*k3(P[z],I,I) for z in range(2)]
assert np.linalg.norm(sum(k.conj().T@k for k in actual)-np.eye(8))<1e-12
assert np.linalg.norm(sum(k.conj().T@k for k in repaired)-np.eye(8))<1e-12
# Derive A_z by exact basis probes of the actual map, using I_S/2 and matching C.
max_res=0.
for z in range(2):
 for i in range(2):
  for j in range(2):
   E=np.zeros((2,2),complex); E[i,j]=1
   r=k3(P[z],I/2,E)
   y=apply(actual,r).reshape(2,2,2,2,2,2)
   block=y[z,:,:,z,:,:]
   extracted=np.einsum('iaib->ab',block)
   expected=(1-p)*V[z]@E@V[z].conj().T+p*E
   max_res=max(max_res,float(np.linalg.norm(extracted-expected)))
assert max_res<1e-12
# General referenced-input diagnostic from normalized Choi matrices.
J=choi(actual); Jpos=choi(repaired)
assert np.linalg.eigvalsh(Jpos).min()>-1e-12
choi_distance=trnorm((J-Jpos)/8)
assert choi_distance<=2*p+1e-12
# Unknown entangled measured/surviving input: no independent-branches assumption.
bell=np.array([1,0,0,1],complex)/np.sqrt(2)
a=np.array([1,1j],complex)/np.sqrt(2)
v=np.kron(bell,a); rho=np.outer(v,v.conj())
distance=trnorm(apply(actual,rho)-apply(repaired,rho))
assert distance<=2*p+1e-12
# Necessity of outcome-dependent bath: inputs z=0,1 with same S,A yield orthogonal
# retained A values under the ideal good map when A starts at zero.
aux0=P[0]; good=[k3(P[z],I,V[z]) for z in range(2)]
aux=[]
for z in range(2):
 y=apply(good,k3(P[z],P[0],aux0)).reshape(2,2,2,2,2,2)
 aux.append(np.einsum('ijaijb->ab',y))
assert abs(trnorm(aux[0]-aux[1])-2)<1e-12
out={'probe_matrix_unit_cases':8,'maximum_branch_extraction_residual':max_res,
 'normalized_Choi_repair_distance':choi_distance,'entangled_MS_input_repair_distance':distance,
 'proved_comparison_budget_2b':2*p,'outcome_conditioned_aux_trace_distance':trnorm(aux[0]-aux[1]),
 'scope':'Finite CP branch-extraction and entangled-input diagnostics; not a numerical diamond-norm or native threshold certification.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
