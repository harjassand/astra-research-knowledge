"""Finite matrix diagnostic for a prefix compression commutator map.

This is not a theorem or a physical simulation. It evaluates the spectral
profile relevant when the true source is granted as decoder side information.
"""
from pathlib import Path
import json
import numpy as np
from scipy.linalg import eigvalsh


PAULIS = [np.array([[0,1],[1,0]],complex),
          np.array([[0,-1j],[1j,0]],complex),
          np.diag([1.,-1.]).astype(complex)]


def source_swap(n,j):
    dim=1<<(n+1)
    perm=np.arange(dim)
    b1=n
    b2=n-j
    for k in range(dim):
        if ((k>>b1)^(k>>b2))&1:
            perm[k]=k^(1<<b1)^(1<<b2)
    return np.eye(dim)[perm]


def data(n,theta):
    d=1<<n
    u=np.eye(2*d,dtype=complex)
    c,s=np.cos(theta),np.sin(theta)
    for j in range(1,n+1):
        u=(c*np.eye(2*d)+1j*s*source_swap(n,j))@u
    phi=np.zeros((d*d,d*d),complex)
    for p in PAULIS:
        logical=u@np.kron(p,np.eye(d))@u.conj().T
        for a in range(2):
            for b in range(2):
                k=logical[a*d:(a+1)*d,b*d:(b+1)*d]/np.sqrt(6)
                phi+=np.kron(k.conj(),k)
    hermitian_residual=float(np.linalg.norm(phi-phi.conj().T))
    vals=eigvalsh((phi+phi.conj().T)/2)
    gap=2*(1-vals[-2])
    out={"n":n,"theta":theta,"dimension":d,
         "commutator_gap":float(gap),"top_eigenvalues":vals[-min(12,len(vals)):].tolist(),
         "hermitian_residual":hermitian_residual,
         "identity_eigenvalue":float(vals[-1])}
    print(json.dumps(out),flush=True)
    return out


if __name__=='__main__':
    results=[data(n,t) for t in (.1,.3,.6) for n in range(1,5)]
    (Path(__file__).parent/'commutant_probe.json').write_text(json.dumps(results,indent=2)+'\n')
