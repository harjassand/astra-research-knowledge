"""Finite algebra checks only; does not validate actual physical drift contracts."""
import numpy as np, json
rng=np.random.default_rng(20261030)
N=7;s=.3;g=.1;k=.2;lam=.8;rho=.02;c=.9;a=1.2
# Arbitrary unitary-mixture positive unital pullback on Q, diagonal classical block.
E=np.diag(rng.integers(0,5,8)); G=np.diag(np.exp(rng.uniform(0,g*N,8)))
V=np.diag(np.exp(s*np.diag(E)))*G
Us=[]
for j in range(3):
 q,r=np.linalg.qr(rng.normal(size=(8,8))+1j*rng.normal(size=(8,8)));Us.append(q)
def T(A):return sum(U.conj().T@A@U for U in Us)/len(Us)
R=3.7; logV=np.diag(np.log(np.diag(V)))
Qbound=-k*T(V@logV)*R+k*g*N*T(V)*R
Qactual=-lam*T(E@V)*R
q_gap=np.linalg.eigvalsh(Qbound-Qactual).min()
raw=V*R;lograw=np.diag(np.log(np.diag(raw)))
log_identity=np.linalg.norm(T(raw@lograw)-(T(V@logV)*R+T(V)*R*np.log(R)))
# Exact scalar Foster inequality after arbitrary positive pullback.
foster_gap=np.linalg.eigvalsh(T(raw@lograw)-c*N*T(raw)+np.exp(c*N-1)*np.eye(8)).min()
Z=np.eye(8)+np.exp(-a*N)*T(raw)
Zdrop=np.eye(8)+np.exp(-a*N)*T(V)*1.4
drop_gap=np.linalg.eigvalsh(Z-Zdrop).min()
out={'quantum_drift_comparison_min_eigenvalue':float(q_gap),'raw_log_split_residual':float(log_identity),'scalar_Foster_pullback_min_eigenvalue':float(foster_gap),'drop_factor_min_eigenvalue':float(drop_gap),'scope':'finite algebra only, no actual capture/noise contract verification'}
assert min(q_gap,foster_gap,drop_gap)>-1e-9 and log_identity<1e-10
print(json.dumps(out,indent=2))
