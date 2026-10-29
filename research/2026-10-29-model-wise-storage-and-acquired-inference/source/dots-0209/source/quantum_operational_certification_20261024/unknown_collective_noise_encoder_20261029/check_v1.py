import numpy as np,json
from scipy.spatial.transform import Rotation
from scipy.linalg import expm,eigh
from functools import reduce
rng=np.random.default_rng(20261029)
P=np.array([[[0,1],[1,0]],[[0,-1j],[1j,0]],[[1,0],[0,-1]]],complex)
kron=lambda xs:reduce(np.kron,xs)
def su(O):
 v=Rotation.from_matrix(O).as_rotvec(); return expm(-.5j*np.einsum('a,aij->ij',v,P))
def polar(A):
 u,s,v=np.linalg.svd(A); return u@np.diag([1,1,np.linalg.det(u@v)])@v
def learn(T,m):
 # Each entry is expectation of output sigma_a sigma_b from +c,+d inputs.
 # Separate independent product-Pauli measurement banks: 81*m full calls per pair.
 H=2*rng.binomial(m,np.clip((1+T)/2,0,1))/m-1 if m else T
 _,s,v=np.linalg.svd(np.eye(9)-H)
 A=np.sqrt(3)*v[-1].reshape(3,3)
 candidates=[polar(A),polar(-A)]; errors=[np.linalg.norm(c-A) for c in candidates[:1]]+[np.linalg.norm(candidates[1]+A)]
 return candidates[np.argmin(errors)],s,np.linalg.norm(H-T,2)
n=4; O=Rotation.random(n,random_state=rng).as_matrix()
# Root frame gauge: true W_i = O_i O_0^T.
W=[x@O[0].T for x in O]; V=kron([su(x) for x in W])
R=Rotation.from_rotvec(np.array([[.8,0,0],[0,1.1,0],[0,0,1.3],[.6,.3,.4]])).as_matrix(); p=np.array([.2,.25,.25,.3])
# All noise matrices in root-relative frame.
A=[[O[i]@r@O[i].T for r in R] for i in range(n)]
Ts=[sum(p[z]*np.kron(A[i][z],A[0][z]) for z in range(len(p))) for i in range(1,n)]
# Four-qubit total-spin-zero basis, dimension 2.
J=[]
for a in range(3):
 J.append(sum(kron([P[a] if i==j else np.eye(2) for i in range(n)]) for j in range(n))/2)
v,Q=eigh(sum(x@x for x in J)); E=Q[:,v<1e-9]
assert E.shape==(16,2)
# Full system-bath coherent collective interaction, retained two-level bath.
# U_t is conjugated collective on system; generator sum J_a tensor B_a.
H=sum(np.kron(V@J[a]@V.conj().T,P[a]) for a in range(3))
# Test entangled logical/reference input; report entanglement fidelity including leakage.
phi=np.eye(2).reshape(4)/np.sqrt(2)
res=[]
for m in [0,1000,10000,100000]:
 inferred=[np.eye(3)]; errs=[]; gaps=[]
 for i,T in enumerate(Ts):
  C,s,e=learn(T,m);inferred.append(C);errs.append(e);gaps.append(float(np.linalg.svd(np.eye(9)-T,compute_uv=False)[-2]))
 VH=kron([su(x) for x in inferred]); EH=VH@E
 # Density order system,bath,reference; start bath |0>, reference maximally entangled code.
 psi=np.einsum('sl,lr,b->sbr',EH,np.eye(2)/np.sqrt(2),[1,0]).reshape(-1)
 values=[]
 for t in [0,1,10,100,1000]:
  out=np.kron(expm(-1j*t*H),np.eye(2))@psi
  out=out.reshape(16,2,2)
  decoded=np.einsum('ls,sbr->lbr',EH.conj().T,out)
  F=sum(abs(np.vdot(phi,decoded[:,b,:].reshape(-1)))**2 for b in range(2))
  values.append({'time':t,'entanglement_fidelity_with_leakage':float(F)})
 res.append({'shots_per_setting':m,'full_n_qubit_calls':81*(n-1)*m,'frame_F_errors':[float(np.linalg.norm(x-y)) for x,y in zip(inferred,W)],'block_operator_errors':errs,'gaps':gaps,'storage':values})
# Obstructions: identity and single-axis rotations.
ob=[]
for label,rot in [('identity',np.eye(3)),('abelian',Rotation.from_rotvec([0,0,.7]).as_matrix())]:
 s=np.linalg.svd(np.eye(9)-np.kron(rot,rot),compute_uv=False);ob.append({'source':label,'fixed_dimension':int(sum(s<1e-10))})
print(json.dumps({'seed':20261029,'n':n,'singlet_dim':E.shape[1],'results':res,'degeneracies':ob},indent=2))
