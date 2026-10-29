import numpy as np,json
from scipy.linalg import expm
rng=np.random.default_rng(2026102904)
I=np.eye(2);X=np.array([[0,1],[1,0]]);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1]);P=np.array([X,Y,Z])
V=np.kron(expm(-.2j*np.einsum('a,aij->ij',rng.normal(size=3),P)),expm(-.2j*np.einsum('a,aij->ij',rng.normal(size=3),P)))
bells=np.array([[1,0,0,1],[1,0,0,-1],[0,1,1,0],[0,1,-1,0]],complex).T/np.sqrt(2);signs=np.array([1,1,1,-1]);bells=V@bells;S=bells@np.diag(signs)@bells.conj().T
D=8;St=np.kron(S,I)
g=.23;Ks=[np.kron(np.diag([1,np.sqrt(1-g)]),np.eye(4)),np.kron(np.array([[0,np.sqrt(g)],[0,0]]),np.eye(4))]
probs=np.zeros((4,4))
for b in range(4):
 rho=np.kron(np.outer(bells[:,b],bells[:,b].conj()),I/2)
 out=sum(K@rho@K.conj().T for K in Ks)
 for c in range(4):probs[b,c]=np.trace(np.kron(np.outer(bells[:,c],bells[:,c].conj()),I)@out).real/4
q=sum(probs[b,c] for b in range(4) for c in range(4) if signs[b]!=signs[c]);delta=1-sum(np.trace(St@K.conj().T@St@K).real for K in Ks)/D
assert abs(probs.sum()-1)<1e-12 and abs(q-delta/2)<1e-12
print(json.dumps({'seed':2026102904,'joint_bell_label_probabilities':probs.tolist(),'pair_transition_failure':q,'delta_over_two':delta/2,'no_long_lived_quantum_reference':True},indent=2))
