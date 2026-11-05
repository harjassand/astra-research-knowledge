import json
import numpy as np

def perm_swap(n, a, b):
    d = 1 << n
    p = np.arange(d)
    x = ((p >> (n-1-a)) ^ (p >> (n-1-b))) & 1
    p = p ^ (x << (n-1-a)) ^ (x << (n-1-b))
    return np.eye(d, dtype=complex)[p]

def marginal(rho, n, keep):
    # Sequentially trace unwanted qubits, preserving surviving order.
    a = rho.reshape([2]*(2*n))
    current = n
    for k in sorted(set(range(n))-set(keep), reverse=True):
        a = np.trace(a, axis1=k, axis2=k+current)
        current -= 1
    return a.reshape(1 << len(keep), 1 << len(keep))

phi = np.array([1.,0.,0.,1.])/np.sqrt(2)
bell = np.outer(phi,phi)
rows=[]
for theta in [0.07,0.3,0.8,1.4]:
    c,s=np.cos(theta),np.sin(theta)
    for K in range(1,5):
        n=K+3 # R,S,E_1,...,E_K,D
        d=1<<n
        rho=np.kron(bell,np.eye(1<<(K+1))/(1<<(K+1)))
        eye=np.eye(d)
        for j in range(K):
            P=perm_swap(n,1,2+j)
            U=c*eye+1j*s*P
            rho=U@rho@U.conj().T
        for j in reversed(range(K)):
            P=perm_swap(n,2+j,3+j)
            W=c*P-1j*s*eye
            rho=W@rho@W.conj().T
        out=marginal(rho,n,[0,2])
        lam=1-(1-s**4)**K
        expected=lam*bell+(1-lam)*np.eye(4)/4
        residual=float(np.max(np.abs(out-expected)))
        rows.append(dict(theta=theta,K=K,maximum_entry_residual=residual,
                         entanglement_infidelity=float(1-np.vdot(phi,out@phi).real),
                         predicted_infidelity=float(.75*(1-s**4)**K)))
assert max(r['maximum_entry_residual'] for r in rows)<1e-12
print(json.dumps(rows,indent=2))
