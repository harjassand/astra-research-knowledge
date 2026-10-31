"""Small algebraic diagnostics, not a numerical proof or hardware model."""
import json
import numpy as np
from pathlib import Path
rng=np.random.default_rng(20261031)
I2=np.eye(2); n=np.diag([0.,1.]); up=np.array([[0,0],[1,0]],complex)
minimum=1.0
for _ in range(80):
    T=rng.normal(size=(3,3))+1j*rng.normal(size=(3,3))
    bound=np.linalg.norm(T,2)
    u,v=rng.uniform(size=2)
    H=np.kron(np.kron(up,up.conj().T),T)
    H=H+H.conj().T
    V=np.kron(np.kron(I2+u*n,I2+v*n),np.eye(3))
    rhs=bound*(u+v)*np.kron(np.kron(n,I2+v*n)+np.kron(I2+u*n,n),np.eye(3))
    slack=rhs-1j*(H@V-V@H)
    minimum=min(minimum,float(np.linalg.eigvalsh(slack).min()))
assert minimum>-1e-11
Q=np.diag([0.,0.,1.]); P0=np.diag([1.,0.,0.]); I3=np.eye(3)
H=np.array([[0,1e20,0],[1e20,0,0],[0,0,0]],complex)
loss=[]
for j in (0,1):
    L=np.zeros((3,3),complex); L[j,2]=1; loss.append(L)
inj=np.zeros((3,3),complex);inj[2,0]=1

def adj(L,V):
    C=L.conj().T@L
    return L.conj().T@V@L-(C@V+V@C)/2
maxres=0.
for u in np.linspace(0,1,21):
    V=I3+u*Q
    assert np.array_equal(H@V,V@H)
    drift=sum((adj(L,V) for L in loss),np.zeros((3,3),complex))
    maxres=max(maxres,float(np.linalg.norm(drift+2*u*Q)))
    maxres=max(maxres,float(np.linalg.norm(adj(inj,V)-u*P0)))
    for theta in (0.,.1,.7):
        W=I3+(np.exp(theta)-1)*Q
        tilt=sum((np.exp(theta)*L.conj().T@W@L-
                  ((L.conj().T@L)@W+W@(L.conj().T@L))/2
                  for L in loss),np.zeros((3,3),complex))
        assert np.linalg.norm(tilt)<1e-12
assert maxres<1e-12
out={'kind':'floating algebraic diagnostic only','operator_edges':80,
     'minimum_edge_slack_eigenvalue':minimum,
     'qutrit_weight_points':21,'qutrit_max_identity_residual':maxres,
     'large_ground_hamiltonian':1e20,'thermal_or_hardware_claim':False}
print(json.dumps(out,indent=2))
if __name__=='__main__':
    Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
