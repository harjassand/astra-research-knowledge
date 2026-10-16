"""Independent bounded reconstruction; no downloaded code is executed."""
import json
import numpy as np
from scipy.linalg import expm, eigvalsh
from scipy.integrate import quad

rng=np.random.default_rng(104890)
I=np.eye(8,dtype=complex)
Z=[np.diag([(-1)**((a//2 >> (1-i))&1) for a in range(8)]) for i in range(2)]
P0=np.diag([1,1,0,0,0,0,0,0])
PF=np.diag([0,0,0,0,0,0,1,1])
def herm(n):
    x=rng.normal(size=(n,n))+1j*rng.normal(size=(n,n))
    return (x+x.conj().T)/2
def effect(H,g,T):
    L=-1j*(np.kron(I,H)-np.kron(H.T,I))
    for z,rate in zip(Z,g):
        L+=rate*(np.kron(z.T,z)-np.eye(64))
    # Vec convention is column-major; obtain adjoint Born effect.
    E=(expm(L*T).conj().T@PF.reshape(-1,order='F')).reshape((8,8),order='F')
    return float(eigvalsh((E[:2,:2]+E[:2,:2].conj().T)/2)[-1])
rows=[]
for trial in range(12):
    J=rng.uniform(.15,.7,2); g=rng.uniform(.2,2.0,2); T=float(rng.uniform(.1,1.2))
    H0=np.zeros((8,8),complex)
    for s in range(4): H0[2*s:2*s+2,2*s:2*s+2]=herm(2)
    V=[]
    for i in range(2):
        v=np.zeros((8,8),complex)
        for s in range(4):
            t=s^(1<<(1-i))
            if s<t:
                x=rng.normal(size=(2,2))+1j*rng.normal(size=(2,2))
                v[2*s:2*s+2,2*t:2*t+2]=x
                v[2*t:2*t+2,2*s:2*s+2]=x.conj().T
        v*=J[i]/np.linalg.norm(v,2); V.append(v)
        assert np.linalg.norm(v@Z[i]+Z[i]@v)<1e-12
        assert np.linalg.norm(v@Z[1-i]-Z[1-i]@v)<1e-12
    eps=J**2/g*(T+np.expm1(-2*g*T)/(2*g))
    probability=effect(H0+V[0]+V[1],g,T)
    bound=float(np.prod(np.minimum(1,eps)))
    rows.append(dict(trial=trial,probability=probability,bound=bound,ratio=probability/bound))
    assert probability<=bound+1e-11

# Independent quadrature of the no-cut square-gap identity.
g=.8; T=.7; J=.4
integral=2*quad(lambda t: quad(lambda s:J*J*np.exp(-2*g*(t-s)),0,t)[0],0,T)[0]
formula=J*J/g*(T+np.expm1(-2*g*T)/(2*g))
assert abs(integral-formula)<1e-12

# A two-parity coupling deliberately violates deletion locality.
X=np.array([[0,1],[1,0]])
J=.2; T=.1; g=np.array([.3,.4])
p=effect(J*np.kron(np.kron(X,X),np.eye(2)),g,T)
fake=float(np.prod(J*J/g*(T+np.expm1(-2*g*T)/(2*g))))
assert p>fake
out=dict(seed=104890,independent_endpoint_checks=rows,max_ratio=max(r['ratio'] for r in rows),
    gap_identity=dict(quadrature=integral,formula=formula),
    cross_parity_falsifier=dict(actual=p,invalid_singleton_product=fake,ratio=p/fake),
    scope='Finite checks plus independent analytic reconstruction; not a universal proof or external review.')
print(json.dumps(out,indent=2))
