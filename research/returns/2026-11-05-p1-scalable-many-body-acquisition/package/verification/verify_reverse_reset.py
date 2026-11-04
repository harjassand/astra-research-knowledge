"""Small exact checks for the reverse-reset decoder; analytical proof is separate."""
import json
from pathlib import Path
import numpy as np
from scipy.linalg import expm
I=np.eye(2,dtype=complex)
X=np.array([[0,1],[1,0]],complex)
Y=np.array([[0,-1j],[1j,0]],complex)
Z=np.diag([1,-1]).astype(complex)
P=[I,X,Y,Z]
PAULI=[np.kron(a,b) for a in P for b in P]
n,d,p=2,4,16
H=np.kron(X,X)+0.37*np.kron(Z,I)+0.23*np.kron(I,Z)
K=np.array([[np.trace(a.conj().T@(H@b-b@H))/d for b in PAULI] for a in PAULI])
def reset_star(a,site):
    t=a.reshape(4,4,4,4); out=np.zeros_like(t)
    if site==0:
        for b in range(4): out[b,:,b,:]=t[0,:,0,:]
    else:
        for b in range(4): out[:,b,:,b]=t[:,0,:,0]
    return out.reshape(p,p)
def matrix_for_map(fn,dimension):
    mat=np.zeros((dimension**2,dimension**2),complex)
    for a in range(dimension):
        for b in range(dimension):
            e=np.zeros((dimension,dimension),complex); e[a,b]=1
            mat[:,a*dimension+b]=fn(e).reshape(-1)
    return mat
def swap_matrix(a,b):
    ans=np.zeros((16,16),complex)
    for i in range(16):
        z=[(i>>(3-j))&1 for j in range(4)]
        z[a],z[b]=z[b],z[a]
        j=sum(x<<(3-k) for k,x in enumerate(z)); ans[j,i]=1
    return ans
V=expm(-0.3j*np.kron(H,np.eye(4)))
U=V@swap_matrix(1,3)@V@swap_matrix(0,2)@V

def C(a):
    out=U@np.kron(a,np.eye(4)/4)@U.conj().T
    return np.einsum('abad->bd',out.reshape(4,4,4,4))
def D(a):
    out=U.conj().T@np.kron(np.eye(4)/4,a)@U
    return np.einsum('abcb->ac',out.reshape(4,4,4,4))
R_direct=np.array([[np.trace(a.conj().T@D(C(b)))/d for b in PAULI] for a in PAULI])
vac=np.zeros((p,p),complex); vac[0,0]=1
R_op=vac.copy()
for site in [1,0,None]:
    v=expm(-0.3j*K); R_op=v.conj().T@R_op@v
    if site is not None: R_op=reset_star(R_op,site)
r,beta=6.,2.
kappa=r-beta
W=np.diag([int(a!=0)+int(b!=0) for a in range(4) for b in range(4)]).astype(complex)
def Lstar(a):
    return 1j*(K@a-a@K)+r*(reset_star(a,0)+reset_star(a,1)-2*a)
Lmat=matrix_for_map(Lstar,p)
lyap=float(np.linalg.eigvalsh(Lstar(W)+kappa*W).max())
checks=[]
for T in [.2,.5,1.,2.]:
    R=(expm(Lmat*T)@vac.reshape(-1)).reshape(p,p)
    R=(R+R.conj().T)/2
    eig=np.linalg.eigvalsh(R); resid=float(1-eig.min())
    def physical(a):
        coeff=np.array([np.trace(b.conj().T@a)/d for b in PAULI])
        return sum(c*b for c,b in zip(R@coeff,PAULI))
    choi=np.zeros((d*d,d*d),complex)
    for a in range(d):
        for b in range(d):
            e=np.zeros((d,d),complex); e[a,b]=1
            choi+=np.kron(e,physical(e))/d
    choi=(choi+choi.conj().T)/2
    checks.append(dict(time=T,hs_residual_operator_norm=resid,lyapunov_upper_bound=float(n*np.exp(-kappa*T)),maximum_recovery_eigenvalue=float(eig.max()),minimum_choi_eigenvalue=float(np.linalg.eigvalsh(choi).min()),trace_preservation_error=float(np.linalg.norm(R[0,:]-np.eye(p)[0,:])),diamond_upper_bound_from_computed_residual=float(2*np.sqrt(max(resid,0)))))
results=dict(model='n=2 q=2; H=XX+0.37 ZI+0.23 IZ; reset rate r=6 per site',trajectory_direct_vs_operator_space_error=float(np.linalg.norm(R_direct-R_op,ord=2)),trajectory_adjoint_identity_error=float(np.linalg.norm(matrix_for_map(D,d)-matrix_for_map(C,d).conj().T)),operator_space_H_hermiticity_error=float(np.linalg.norm(K-K.conj().T)),maximum_eigenvalue_LstarW_plus_kappaW=lyap,continuous_checks=checks,scope='Finite exact matrix checks audit identities and constants; the general bound is analytical.')
assert results['trajectory_direct_vs_operator_space_error']<1e-10
assert results['trajectory_adjoint_identity_error']<1e-10
assert lyap<1e-10
assert all(v['hs_residual_operator_norm']<=v['lyapunov_upper_bound']+1e-10 for v in checks)
assert all(v['minimum_choi_eigenvalue']>=-1e-10 for v in checks)
Path(__file__).with_name('reverse_reset_verification.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
