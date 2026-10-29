"""Independent exact-interface and perturbation diagnostics (not proof/experiment)."""
import numpy as np,json
from scipy.spatial.transform import Rotation
from scipy.linalg import expm
from pathlib import Path
rng=np.random.default_rng(38191)
I=np.eye(3)
P=np.array([[[0,1],[1,0]],[[0,-1j],[1j,0]],[[1,0],[0,-1]]],complex)
def lift(O):return expm(-.5j*np.einsum('a,aij->ij',Rotation.from_matrix(O).as_rotvec(),P))
def nearest(A):
 u,_,vt=np.linalg.svd(A);return u@np.diag([1,1,np.linalg.det(u@vt)])@vt
ratios=[];nonnormal=[];fixed=[];lift_ratios=[]
for _ in range(500):
 rots=Rotation.random(5,random_state=rng).as_matrix();weights=rng.dirichlet(np.ones(5))
 oi,oj=Rotation.random(2,random_state=rng).as_matrix();C=oi@oj.T
 T=sum(w*np.kron(oi@r@oi.T,oj@r@oj.T) for w,r in zip(weights,rots))
 A=np.eye(9)-T;g=np.linalg.svd(A,compute_uv=False)[-2]
 residual=np.linalg.norm(A@C.reshape(-1));fixed.append(residual);assert residual<1e-12
 nonnormal.append(float(np.linalg.norm(T@T.T-T.T@T)))
 # Independently verify channel action versus row-major representation.
 D=rng.normal(size=(3,3));physical=sum(w*(oi@r@oi.T)@D@(oj@r@oj.T).T for w,r in zip(weights,rots))
 assert np.linalg.norm(T@D.reshape(-1)-physical.reshape(-1))<1e-12
 H=rng.normal(size=(9,9));H*=.02*g/np.linalg.norm(H,2);e=np.linalg.norm(H,2)
 _,_,vt=np.linalg.svd(A+H);M=np.sqrt(3)*vt[-1].reshape(3,3)
 opts=[nearest(M),nearest(-M)];err=[np.linalg.norm(opts[0]-M),np.linalg.norm(opts[1]+M)];cc=opts[np.argmin(err)]
 ratio=np.linalg.norm(cc-C)/(4*np.sqrt(6)*e/g);ratios.append(float(ratio));assert ratio<=1+1e-10
 u,v=lift(cc),lift(C);dd=min(np.linalg.norm(u-v,2),np.linalg.norm(u+v,2));bound=np.linalg.norm(cc-C)/2
 assert dd<=bound+1e-12;lift_ratios.append(float(dd/bound))
# Boundary SO3 separation and SU lift theta=pi.
Q=Rotation.from_rotvec([np.pi,0,0]).as_matrix()
assert abs(np.linalg.norm(I+Q)-2)<1e-12
assert abs(min(np.linalg.norm(lift(Q)-np.eye(2),2),np.linalg.norm(lift(Q)+np.eye(2),2))-np.linalg.norm(Q-I)/2)<1e-12
out={'seed':38191,'cases':500,'max_fixed_residual':max(fixed),'max_rounding_bound_ratio':max(ratios),'max_lift_bound_ratio':max(lift_ratios),'max_T_nonnormality':max(nonnormal),'all_passed':True}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
