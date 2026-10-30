import numpy as np
from scipy.linalg import expm
from scipy.integrate import quad_vec
import json
I=np.eye(2); X=np.array([[0,1],[1,0]],complex)
kappa=.7; omega=.09; T=13.0
R=np.zeros((4,4),complex)
for s in range(2):
 j=np.zeros((2,2));j[0,s]=1
 R+=np.kron(j.conj(),j)
K=-1j*omega*(np.kron(I,X)-np.kron(X.T,I))
L=kappa*(R-np.eye(4))+K
# Sector order active, cleared. Complete reset gain moves active to cleared.
A=np.block([[-kappa*np.eye(4)+K,np.zeros((4,4))],[kappa*R,L]])
B=np.block([[-kappa*np.eye(4),np.zeros((4,4))],[kappa*R,L]])
embed=np.vstack([np.eye(4),np.zeros((4,4))]);forget=np.hstack([np.eye(4),np.eye(4)])
actual=expm(T*L); lifted=forget@expm(T*A)@embed
protected=forget@expm(T*B)@embed
rem,_=quad_vec(lambda s:expm((T-s)*L)@K*np.exp(-kappa*s),0,T)
report={'summed_lift_max_error':float(np.max(abs(actual-lifted))), 'first_reinsertion_identity_max_error':float(np.max(abs(actual-protected-rem))), 'analytic_uniform_diamond_remainder_bound':2*omega/kappa,'finite_horizon_bound':2*omega*(1-np.exp(-kappa*T))/kappa,'note':'Matrix identities tested, not a numerical diamond norm computation. Constant-rate replacement toy model; full transactional proof is in the note.'}
print(json.dumps(report,indent=2))
assert report['summed_lift_max_error']<1e-12
assert report['first_reinsertion_identity_max_error']<1e-12
