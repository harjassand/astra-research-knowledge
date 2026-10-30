import numpy as np,json
rng=np.random.default_rng(29);d=2
A=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d));h=.01*(A+A.conj().T)/2
K=.05*(rng.normal(size=(d,d))+1j*rng.normal(size=(d,d)))
def noise(X):return -1j*(h@X-X@h)+K@X@K.conj().T-(K.conj().T@K@X+X@K.conj().T@K)/2
eps=2*np.linalg.norm(h,2)+2*np.linalg.norm(K,2)**2;delta=d*d*eps
Delta=lambda X:np.trace(X)*np.eye(d)/d
Phi=lambda X:Delta(X)+noise(X)/delta
J=np.zeros((d*d,d*d),complex);res=0.;tr=0.
for i in range(d):
 for j in range(d):
  E=np.zeros((d,d));E[i,j]=1
  J+=np.kron(E,Phi(E))/d
  res=max(res,np.linalg.norm(noise(E)+delta*(Delta(E)-E)-delta*(Phi(E)-E)))
  tr=max(tr,abs(np.trace(Phi(E))-np.trace(E)))
vals=np.linalg.eigvalsh(J)
assert vals.min()>-1e-12 and res<1e-12 and tr<1e-12
print(json.dumps(dict(epsilon_bound=eps,delta=delta,Choi_eigenvalues=vals.tolist(),generator_identity_error=res,trace_preservation_error=tr),indent=2))
