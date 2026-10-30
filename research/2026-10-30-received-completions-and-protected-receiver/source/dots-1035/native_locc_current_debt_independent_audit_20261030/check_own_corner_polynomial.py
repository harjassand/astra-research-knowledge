"""Independent non-diagonal own-corner regression, not the native FSM theorem.
A bad two-dimensional qutrit sector has coherent mixing and only one direct
reset to the good level. Construct the exact telescoping polynomial witness.
"""
from pathlib import Path
import numpy as np, json
from scipy.linalg import expm, eigvalsh
n=3; I=np.eye(n); Q=np.diag([0.,1.,1.]); H=np.zeros((n,n),complex)
H[1,2]=H[2,1]=.8
J=np.zeros((n,n),complex); J[0,1]=1.1
A=J.conj().T@J
L=1j*(np.kron(I,H)-np.kron(H.T,I))+np.kron(J.T,J.conj().T)-.5*(np.kron(I,A)+np.kron(A.T,I))
v=lambda x:x.reshape(-1,order='F')
m=lambda x:x.reshape((n,n),order='F')
T=4.; M=80; dt=T/M; K=12
O=Q.copy().astype(complex); F=np.zeros_like(O)
for step in range(M):
    old=O.copy(); O=old.copy(); inc=dt*old; deriv=old.copy(); coef=1.
    # Q_K and R_K=(Q_K-1)/L, degree K and K-1 respectively.
    for k in range(1,K+1):
        deriv=m(L@v(deriv)); coef*=dt/k; O+=coef*deriv
        if k<K:inc+=dt*coef/(k+1)*deriv
    F+=inc
E=m(expm(T*L)@v(Q)); p=1-eigvalsh(E[1:,1:])[-1]
nu=np.linalg.norm(m(L@v(Q)),2); a=(1-np.exp(-nu*T))/nu
Z=F/(1.5*T); alpha=a/(3*T); r=p/(3*T)
herm=lambda X:(X+X.conj().T)/2
emin=lambda X:float(eigvalsh(herm(X))[0]);emax=lambda X:float(eigvalsh(herm(X))[-1])
res={
 'bad_sector_dimension':2,'T':T,'steps':M,'polynomial_degree_per_step':K,
 'uniform_cooling_p':float(p),'alpha':float(alpha),'r':float(r),
 'telescoping_identity_error':float(np.linalg.norm(m(L@v(F))-(O-Q),2)),
 'endpoint_approximation_error':float(np.linalg.norm(O-E,2)),
 'own_corner_error':float(np.linalg.norm(Z-Q@Z@Q,2)),
 'offdiagonal_witness_magnitude':float(abs(Z[1,2])),
 'minimum_Z_minus_alphaQ':emin(Z-alpha*Q),'minimum_Q_minus_Z':emin(Q-Z),
 'maximum_drift_LZ_plus_rQ':emax(m(L@v(Z))+r*Q),
 'scope':'non-diagonal own-corner and telescoping algebra only; not native finite-rate path evidence'}
assert p>0 and res['offdiagonal_witness_magnitude']>.001
assert res['telescoping_identity_error']<1e-10
assert res['own_corner_error']<1e-12
assert res['minimum_Z_minus_alphaQ']>=-1e-12
assert res['minimum_Q_minus_Z']>=-1e-12
assert res['maximum_drift_LZ_plus_rQ']<=1e-12
Path(__file__).with_suffix('.json').write_text(json.dumps(res,indent=2)+'\n'); print(json.dumps(res,indent=2))
