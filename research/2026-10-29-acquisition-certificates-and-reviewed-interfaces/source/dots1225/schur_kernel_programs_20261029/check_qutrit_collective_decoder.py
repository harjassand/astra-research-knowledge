"""Explicit N=3,d=3 Schur(2,1) kernel-program extraction, retaining bath."""
import numpy as np,itertools,math,json
from pathlib import Path
rng=np.random.default_rng(202610291045);d=3;n=3
A=np.zeros((3,9),complex)
for a in range(3):
 rest=[j for j in range(3) if j!=a]
 for p in itertools.permutations(rest):A[a,3*p[0]+p[1]]=(-1)**(a+int(p[0]>p[1]))/math.sqrt(2)
J=np.kron(A.conj().T,np.eye(3)) # 27x9, column-antisymmetric copy
# Remove completely antisymmetric ray, which maps to maximally entangled in wedge-dual x V.
f=np.eye(3).ravel()/math.sqrt(3)
U,sv,Vh=np.linalg.svd(f.reshape(1,9));B=Vh.conj().T[:,1:];J0=J@B
S=np.zeros((27,27))
for i,j,k in itertools.product(range(3),repeat=3):S[9*i+3*k+j,9*i+3*j+k]=1
C=J0.conj().T@S@J0;c=np.trace(C)/8;assert np.linalg.norm(C-c*np.eye(8))<1e-12
J1=(S@J0-c*J0)/math.sqrt(1-abs(c)**2);assert np.linalg.norm(J1.conj().T@J1-np.eye(8))<1e-12;assert np.linalg.norm(J0.conj().T@J1)<1e-12
Ks=[np.kron(A,np.eye(3))@J0@Jx.conj().T for Jx in [J0,J1]]
# Independent central projector using permutation symmetry.
Ps=np.zeros((27,27));Pa=np.zeros((27,27))
for p in itertools.permutations(range(3)):
 mat=np.zeros((27,27));sg=(-1)**sum(p[i]>p[j] for i in range(3) for j in range(i+1,3))
 for abc in itertools.product(range(3),repeat=3):dest=[abc[p[j]] for j in range(3)];mat[9*dest[0]+3*dest[1]+dest[2],9*abc[0]+3*abc[1]+abc[2]]=1
 Ps+=mat/6;Pa+=sg*mat/6
P21=np.eye(27)-Ps-Pa;effect=sum(K.conj().T@K for K in Ks);assert np.linalg.norm(effect-P21)<1e-12
rows=[]
for _ in range(30):
 v=rng.normal(size=3)+1j*rng.normal(size=3);v/=np.linalg.norm(v);Q,_=np.linalg.qr(np.column_stack([v,rng.normal(size=(3,2))+1j*rng.normal(size=(3,2))]));v=Q[:,0];W=Q[:,1:];embed=np.kron(np.kron(W,W),W);z=rng.normal(size=(8,2))+1j*rng.normal(size=(8,2));z/=np.linalg.norm(z);psi=embed@z
 P=np.outer(v.conj(),v);res=0.;pr=0.
 for K in Ks:
  out=(K@psi).reshape(3,3,2);res=max(res,np.linalg.norm(np.einsum('ab,bjk->ajk',np.eye(3)-P,out)));pr+=np.linalg.norm(out)**2
 assert res<1e-12
 rho=embed@embed.conj().T/8;iidpr=np.trace(effect@rho).real;assert abs(iidpr-.5)<1e-12
 rows.append(dict(decoupling_residual=float(res),correlated_success=float(pr),iid_success=float(iidpr)))
Path(__file__).with_suffix('.json').write_text(json.dumps(dict(scope='Dense floating diagnostic of exact generic representation argument; d3,N3,not full9dim compiler',cases=len(rows),copy_overlap=float(c.real),effect_projector_residual=float(np.linalg.norm(effect-P21)),rows=rows),indent=2)+'\n');print(len(rows),c,np.linalg.norm(effect-P21))
