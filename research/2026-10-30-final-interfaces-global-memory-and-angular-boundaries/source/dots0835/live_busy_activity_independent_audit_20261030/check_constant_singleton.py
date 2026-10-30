"""Finite noncommuting algebra diagnostic, not a simulation of native memory."""
import json
import numpy as np
from scipy.linalg import expm, eigvalsh

I2=np.eye(2, dtype=complex)
px=np.array([[0,1],[1,0]],complex)
pz=np.diag([1,-1]).astype(complex)
p1=np.diag([0,1]).astype(complex)
sm=np.array([[0,1],[0,0]],complex)
def tensor(xs):
    a=np.ones((1,1),complex)
    for x in xs:a=np.kron(a,x)
    return a
def on(op, k):
    a=[I2]*4;a[k]=op
    return tensor(a)
I=np.eye(16,dtype=complex)
P=[on(p1,h) for h in range(3)]
J=[on(sm,h) for h in range(3)]
aux=[2*I2+.3*px, 2*I2+.3*pz, 2*I2+.3*(px+pz)/np.sqrt(2)]
X=[P[h]@on(aux[h],3) for h in range(3)]
H=[on(px,h)@(I+.2*on(pz,3)) for h in range(3)]
M=sum(P)
Q0=(I-P[0])@(I-P[1])@(I-P[2])
active=I-Q0
mins=[]
for x,p in zip(X,P):
    mins.append(float(eigvalsh(x-1.7*p)[0]))

def L0(O):
    return sum(j.conj().T@O@j-.5*(j.conj().T@j@O+O@j.conj().T@j) for j in J)
def herm(a):return (a+a.conj().T)/2
rows=[]
for delta in [.01,.03,.07]:
    Y=I.copy()
    for x in X:Y=expm(delta*x)@Y
    G=Y.conj().T@Y
    Yi=np.linalg.inv(Y)
    def pull(O):return herm(Yi.conj().T@O@Yi)
    fast=pull(L0(G))
    R=fast-2*delta*sum(L0(x) for x in X)
    w,v=np.linalg.eigh(M)
    invhalf=(v*np.array([1/np.sqrt(z) if z>1e-10 else 0 for z in w]))@v.conj().T
    relative_fast=float(np.linalg.norm(invhalf@R@invhalf,2)/delta**2)
    lower=float(eigvalsh(G-expm(3.4*delta*M))[0])
    upper=float(eigvalsh(expm(4.6*delta*M)-G)[0])
    for eps in [.005,.02,.08]:
        weak=[pull(1j*(h@G-G@h)) for h in H]
        zero=max(np.linalg.norm((I-p)@k@(I-p),2) for p,k in zip(P,weak))
        K=fast+eps*sum(weak)
        # a=1 is a reserved fraction of the earned singleton service.
        source=float(eigvalsh(K+delta*M)[-1]/(delta*eps**2*3))
        rows.append(dict(delta=delta,epsilon=eps,fast_relative_delta2=relative_fast,
                         weak_idle_idle_residual=float(zero),
                         weak_norm_over_delta=max(float(np.linalg.norm(k,2)/delta) for k in weak),
                         scalar_source_over_delta_eps2_N=source,
                         all_idle_fast_remainder=float(np.linalg.norm(Q0@R,2)),
                         lower_barrier_min_eigenvalue=lower,upper_barrier_min_eigenvalue=upper))
        assert zero<1e-12
        assert np.linalg.norm(Q0@R,2)<1e-12
        assert lower>-1e-12 and upper>-1e-12
        assert source<12
result=dict(scope="Noncommuting 16-dimensional full-Hilbert activity fixture; not native service/memory simulation",
            gate_generator_commutator_norm=float(np.linalg.norm(X[0]@X[1]-X[1]@X[0],2)),
            witness_lower_residual=min(mins),rows=rows)
print(json.dumps(result,indent=2))
