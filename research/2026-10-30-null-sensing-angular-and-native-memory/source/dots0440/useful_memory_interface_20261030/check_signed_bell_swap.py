#!/usr/bin/env python3
"""Exact dense small-code audit of signed-sector physical Bell swapping."""
import itertools, json
import numpy as np
I=np.eye(2,dtype=complex); X=np.array([[0,1],[1,0]],complex)
Y=np.array([[0,-1j],[1j,0]],complex); Z=np.diag([1,-1]).astype(complex)
def kron_all(seq):
    a=np.ones((1,1),complex)
    for b in seq:a=np.kron(a,b)
    return a
def check(n, generators):
    D=2**n;r=len(generators);d=D//2**r
    projectors={}
    for s in itertools.product([0,1],repeat=r):
        q=np.eye(D,dtype=complex)
        for si,g in zip(s,generators):q=q@(np.eye(D)+(-1)**si*g)/2
        projectors[s]=q
    max_err=0.;max_zero=0.;max_prob=0.;cases=0
    kraus_gram=np.zeros((2**(2*r),2**(2*r)),complex)
    sectors=list(projectors)
    for labels in itertools.product(range(4),repeat=n):
        P=kron_all([[I,X,Y,Z][j] for j in labels])
        delta=tuple(int(np.max(np.abs(P@g-g@P))>1e-9) for g in generators)
        G=np.zeros((2**r,2**(2*r)),complex)
        for si,s in enumerate(sectors):
            for ti,t in enumerate(sectors):
                output=projectors[s]@P.conj().T@projectors[t]@P/(d*np.sqrt(D))
                compatible=all(a^b==c for a,b,c in zip(s,t,delta))
                target=projectors[s]/(d*np.sqrt(D)) if compatible else np.zeros((D,D))
                error=np.linalg.norm(output-target)
                max_err=max(max_err,float(error))
                prob=np.linalg.norm(output)**2
                max_prob=max(max_prob,float(abs(prob-(1/(d*D) if compatible else 0))))
                if not compatible:max_zero=max(max_zero,float(prob))
                if compatible:G[si,si*2**r+ti]=1/np.sqrt(d*D)
                cases+=1
        kraus_gram+=G.conj().T@G
    gram_error=float(np.linalg.norm(kraus_gram-np.eye(2**(2*r))))
    return dict(n=n,k=n-r,cases=cases,max_matrix_identity_error=max_err,
                max_probability_error=max_prob,max_forbidden_probability=max_zero,
                gauge_instrument_completeness_error=gram_error,
                passed=max(max_err,max_prob,gram_error)<1e-10)
results=[check(2,[kron_all([Z,Z])]),check(4,[kron_all([X]*4),kron_all([Z]*4)])]
print(json.dumps(results,indent=2))
assert all(x['passed'] for x in results)
