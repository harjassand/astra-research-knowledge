#!/usr/bin/env python3
"""Checks a non-CP hybrid example; the mathematical proof is in the note."""
import numpy as np
from scipy.linalg import expm
import json
J=np.array([[0,1],[0,0]],complex); I=np.eye(2); A=J.conj().T@J
D=np.kron(J.conj(),J)-.5*np.kron(I,A)-.5*np.kron(A.T,I)
def choi(S):
    out=np.zeros((4,4),complex)
    for i in range(2):
        for j in range(2):
            e=np.zeros((2,2),complex);e[i,j]=1
            y=(S@e.reshape(-1,order='F')).reshape(2,2,order='F')
            out+=np.kron(e,y)
    return out
out=[]
for a in [.001,.01,.05,.1]:
    # Actual total generator is 0: N1=aD, N2=-aD.
    E=2*np.eye(4)-expm(a*D)-expm(-a*D)
    upper=float(np.linalg.norm(choi(E),ord='nuc'))
    bound=float(np.expm1(2*a)**2) # ||D||diamond=2.
    inp=np.array([[0,0],[0,1]],complex)
    bad=(expm(-a*D)@inp.reshape(-1,order='F')).reshape(2,2,order='F')
    out.append(dict(a=a,choi_trace_norm_upper=upper,proved_bound=bound,
                    noncp_hybrid_min_eigenvalue=float(np.linalg.eigvalsh(bad)[0])))
    assert upper<=bound+1e-12
    assert np.linalg.eigvalsh(bad)[0]<0
print(json.dumps(dict(scope='Finite generator-algebra diagnostic; physical box theorem has an independent analytic proof.',results=out),indent=2))
