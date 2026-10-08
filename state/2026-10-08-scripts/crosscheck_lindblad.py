"""Independent 64-by-64 Lindblad superoperator integration, no Schur formulas."""
import numpy as np
from scipy.linalg import expm
N=3; D=1<<N; nu=3/20; s=5/2
Jplus=np.zeros((D,D))
for i in range(D):
    for b in range(N):
        if not (i & (1<<b)):
            Jplus[i | (1<<b),i]=1.
Jminus=Jplus.T
ident=np.eye(D)
def dissipator(A):
    K=A.T@A
    return np.kron(A,A) - .5*(np.kron(ident,K) + np.kron(K.T,ident))
L=(nu+1)*dissipator(Jminus) + nu*dissipator(Jplus)
rho0=np.eye(D)/D
rho=expm(s*L)@rho0.reshape(-1,order='F')
rho=rho.reshape((D,D),order='F')
pt=rho.reshape(2,4,2,4).transpose(2,1,0,3).reshape((8,8))
from thermal_pt_experiment import build_rho,make_projectors
rep=build_rho(N,nu,s,make_projectors(N))
print('full-Lindblad vs Schur max entry error',np.max(np.abs(rho-rep)))
print('norm/tr/psd rho',np.linalg.norm(rho-rho.T),np.trace(rho),np.min(np.linalg.eigvalsh(rho)))
print('PT min eigenvalue via independent calculation:',np.min(np.linalg.eigvalsh(pt)))
assert np.max(np.abs(rho-rep))<1e-12
assert np.min(np.linalg.eigvalsh(pt))< -6.9e-5
