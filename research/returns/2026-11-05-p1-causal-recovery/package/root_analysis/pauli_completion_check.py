"""Finite check of Pauli-frame closure for the rotated-tensor instrument.

Tests only the candidate local Pauli gauge, not all possible receivers.
System order is source S, reference-like receiver R, active receiver A, bath E.
"""
import itertools
import json
import numpy as np
from pathlib import Path
from spectrum import swap_matrix

P = [np.eye(2), np.array([[0,1],[1,0]]),
     np.array([[0,-1j],[1j,0]]), np.diag([1,-1])]
bell = np.array([1,0,0,1],dtype=complex)/np.sqrt(2)
phi = np.outer(bell,bell.conj())

def kron(*xs):
    z=np.ones((1,1),dtype=complex)
    for x in xs:z=np.kron(z,x)
    return z

def trace_e(x):
    z=x.reshape(8,2,8,2)
    return np.einsum('aibi->ab',z)

def update(family,theta,k=None):
    u=np.cos(theta)*np.eye(16)+1j*np.sin(theta)*swap_matrix(4,0,3)
    v=np.cos(theta)*np.eye(16)-2j*np.sin(theta)*kron(P[0],P[0],phi)
    if k is not None:v=v@kron(P[0],P[0],P[k],P[0])/2
    return [trace_e(v@u@kron(x,P[0]/2)@u.conj().T@v.conj().T) for x in family]

def main():
    out=[]
    for theta in [.1,.4,.8]:
        initial=[kron(p/2,phi) for p in P]
        first=update(initial,theta)
        target=update(first,theta)
        for k in range(4):
            branch=update(first,theta,k)
            prob=float(np.trace(branch[0]).real)
            normalized=[x/prob for x in branch]
            baseline_spectrum_error=float(np.max(np.abs(np.linalg.eigvalsh(normalized[0])-np.linalg.eigvalsh(target[0]))))
            best=(float('inf'),None)
            for labels in itertools.product(range(4),repeat=4):
                ps,pr,pa,pin=labels
                w=kron(P[ps],P[pr],P[pa])
                signs=[float(np.trace(P[pin]@p@P[pin]@p).real/2) for p in P]
                err=max(np.linalg.norm(w@normalized[a]@w.conj().T-signs[a]*target[a]) for a in range(4))
                if err<best[0]:best=(float(err),labels)
            out.append(dict(theta=theta,outcome=k,probability=prob,
                            baseline_spectrum_error=baseline_spectrum_error,
                            best_pauli_gauge_error=best[0],best_frame=best[1],
                            target_distinguishability=[float(np.linalg.norm(x,ord='nuc')) for x in target[1:]],
                            branch_distinguishability=[float(np.linalg.norm(x,ord='nuc')) for x in normalized[1:]]))
    with Path(__file__).with_name('pauli_completion_results.json').open('w') as f:
        json.dump(out,f,indent=2)
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
