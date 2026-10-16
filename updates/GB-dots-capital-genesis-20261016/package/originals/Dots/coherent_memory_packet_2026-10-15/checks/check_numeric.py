import numpy as np
from scipy.linalg import expm
I=np.eye(2); X=np.array([[0,1],[1,0]]); Z=np.diag([1,-1]); n=16
kron=np.kron
Z1=kron(Z,np.eye(8)); Z2=kron(kron(I,Z),np.eye(4)); X1=kron(X,np.eye(8))
# Seven rank-one active patterns, with a Pauli correction taking each to 0000.
Ks=[]
for j in range(7):
    K=np.zeros((n,n),complex); K[0,j]=1; Ks.append(K)
K0=np.diag([0]*7+[1]*9); Ks.append(K0)
def choi(Ks):
    return sum(np.outer(K.reshape(-1,order='F'),K.reshape(-1,order='F').conj()) for K in Ks)
J=choi(Ks)
theta=.17; U=expm(-1j*theta*X1)
Jtwo=choi([U@K/np.sqrt(2) for K in Ks]+[Z1@U@K@Z1/np.sqrt(2) for K in Ks])
print('two_frame_Frobenius_error',np.linalg.norm(Jtwo-(np.cos(theta)**2*J+np.sin(theta)**2*choi([X1@K for K in Ks]))))
rng=np.random.default_rng(919); h=rng.normal(size=(4,4))+1j*rng.normal(size=(4,4));h=(h+h.conj().T)/2;h=h/np.linalg.norm(h,2)
U=kron(expm(-1j*.13*h),np.eye(4)); eps=np.linalg.norm(U-np.eye(n),2)
Rs=[(np.eye(n)+a*Z1)@(np.eye(n)+b*Z2)/4 for a in [-1,1] for b in [-1,1]]
Kref=[K@R for K in Ks for R in Rs if np.linalg.norm(K@R)>1e-12]
G=[np.eye(n),Z1,Z2,Z1@Z2]
Jtw=choi([g@U@g@K/2 for g in G for K in Kref])
D=Jtw-(1-eps**2)*choi(Kref)
print('epsilon_squared',eps**2,'min_Choi_residual_eigenvalue',np.linalg.eigvalsh(D)[0])
Jrawtw=choi([g@U@g@K/2 for g in G for K in Ks])
print('unrefined_min_Choi_residual_eigenvalue',np.linalg.eigvalsh(Jrawtw-(1-eps**2)*J)[0])
# Explicit coarse inactive obstruction with a stabilizer rotation.
U=expm(-1j*.13*Z1); psi=np.zeros(n,complex);psi[7]=psi[8]=1/np.sqrt(2)
out=U@psi
print('inactive_pure_input_fidelity',abs(np.vdot(psi,out))**2)
print('inactive_output_minus_0.5_input_min_eigenvalue',np.linalg.eigvalsh(np.outer(out,out.conj())-.5*np.outer(psi,psi.conj()))[0])
