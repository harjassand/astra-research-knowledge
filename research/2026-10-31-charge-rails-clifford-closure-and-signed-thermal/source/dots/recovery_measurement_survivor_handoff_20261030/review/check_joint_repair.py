import numpy as np,json
from pathlib import Path
I=np.eye(2);X=np.array([[0,1],[1,0]]); eps=.037
# Input M,S (4); output classical C,S,retained B (8).
Ks=[];Ws=[]
for z in (0,1):
 K=np.zeros((8,4));W=np.zeros((8,4))
 for s in (0,1):
  K[4*z+2*s+z,2*z+s]=1
  W[4*z+2*(1-s)+z,2*z+s]=1
 Ks.append(K);Ws.append(W)
def choi(ks):
 return sum(np.outer(k.reshape(-1,order='F'),k.reshape(-1,order='F').conj()) for k in ks)
Cgood=choi(Ks);Cbad=choi(Ws);Cactual=(1-eps)*Cgood+eps*Cbad
# The maximally mixed survivor probe in each branch yields the correct B state.
maxprobe=0
for z in (0,1):
 rho=np.zeros((4,4));rho[2*z:2*z+2,2*z:2*z+2]=I/2
 out=(1-eps)*sum(k@rho@k.T for k in Ks)+eps*sum(k@rho@k.T for k in Ws)
 branch=out[4*z:4*z+4,4*z:4*z+4].reshape(2,2,2,2)
 A=np.einsum('sbsB->bB',branch)
 expected=np.zeros((2,2));expected[z,z]=1
 maxprobe=max(maxprobe,np.linalg.norm(A-expected))
# Test the full reference extension on a coherent maximally entangled MS:R input.
phi=np.eye(4).reshape(-1)/2;rho=np.outer(phi,phi)
def apply(ks):return sum(np.kron(k,np.eye(4))@rho@np.kron(k,np.eye(4)).T for k in ks)
reference_error=np.linalg.svd(eps*(apply(Ws)-apply(Ks)),compute_uv=False).sum()
result={'epsilon_bad_CP_map':eps,'positive_repair_min_choi_eigenvalue':float(np.linalg.eigvalsh(Cgood).min()),'maxmix_survivor_probe_residual':maxprobe,'reference_extended_trace_error':float(reference_error),'proved_2b_bound':2*eps,'trace_preserving_residual':float(np.linalg.norm(sum(k.T@k for k in Ks)-np.eye(4))),'scope':'Two-qubit rank-one measured-plus-unknown-survivor CP repair with outcome-dependent retained bath; algebra illustration, not native hardware certification.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
