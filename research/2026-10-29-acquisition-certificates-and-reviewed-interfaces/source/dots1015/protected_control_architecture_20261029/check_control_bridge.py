import numpy as np, json
from scipy.linalg import expm
from pathlib import Path
I=np.eye(2); X=np.array([[0,1],[1,0]]);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1])
def kron(*a):
 r=np.array([[1.]])
 for x in a:r=np.kron(r,x)
 return r
def local(a,j,n=4):return kron(*[a if k==j else I for k in range(n)])
def swap(i,j,n=4):return (np.eye(2**n)+sum(local(a,i,n)@local(a,j,n) for a in [X,Y,Z]))/2
s=np.array([0,1,-1,0])/np.sqrt(2);v0=np.kron(s,s);v1=np.zeros(16);v1[3]=v1[12]=1/np.sqrt(3);v1[[5,6,9,10]]=-1/np.sqrt(12)
V=np.stack([v0,v1],axis=1);P=V@V.T;S=swap(0,1);H0=np.pi*local(Z,0);theta=np.pi*np.sqrt(5)/2
N=expm(-1j*H0);U=expm(-1j*(H0+theta*S));target=expm(-1j*theta*S)
leak=float(np.linalg.norm((np.eye(16)-P)@U@v0)**2)
# Protected global model with noncommuting memory, 2 time segments.
J=[sum(local(a,j) for j in range(4))/2 for a in [X,Y,Z]]
Hbath=kron(J[0],3*X)+kron(J[1],7*Z)+kron(np.eye(16),.9*Y)
HC=.4*S+.7*swap(1,2)
Ugood=expm(-1j*(Hbath+kron(HC,I)))
Vbig=kron(V,I);ideal=kron(expm(-1j*HC),expm(-1j*.9*Y))
res=float(np.linalg.norm((Ugood-ideal)@Vbig,2))
# Exact relative-frame exchange mismatch identity.
errs=[]
for phi in [.01,.2,1,2.7]:
 A=expm(-.5j*phi*Z);W=kron(A,I);S2=swap(0,1,2)
 errs.append(abs(np.linalg.norm(W@S2@W.conj().T-S2,2)-2*abs(np.sin(phi/2))))
out={'endpoint_identity_residual':float(np.linalg.norm(N+np.eye(16),2)),'theta':theta,'psi0_leakage':leak,'exact_leakage_4_over_9':4/9,'protected_shared_bath_factorization_residual':res,'relative_frame_norm_identity_max_residual':max(errs),'S12_logical':(V.T@S@V).real.tolist(),'S23_logical':(V.T@swap(1,2)@V).real.tolist()}
assert abs(leak-4/9)<1e-12 and res<1e-12 and max(errs)<1e-12
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
