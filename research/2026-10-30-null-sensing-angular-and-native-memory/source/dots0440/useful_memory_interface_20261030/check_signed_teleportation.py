#!/usr/bin/env python3
"""Dense operator checks of reference-preserving signed-resource teleportation."""
import itertools,json
import numpy as np
I=np.eye(2,dtype=complex);X=np.array([[0,1],[1,0]],complex)
Y=np.array([[0,-1j],[1j,0]],complex);Z=np.diag([1,-1]).astype(complex)
def kron(seq):
    a=np.ones((1,1),complex)
    for b in seq:a=np.kron(a,b)
    return a
def check(n,gens,all_errors=False):
    D=2**n;r=len(gens);K=D//2**r
    sectors=list(itertools.product([0,1],repeat=r));ps={}
    for s in sectors:
        q=np.eye(D,dtype=complex)
        for b,g in zip(s,gens):q=q@(np.eye(D)+(-1)**b*g)/2
        ps[s]=q
    paulis=[kron([[I,X,Y,Z][j] for j in a]) for a in itertools.product(range(4),repeat=n)]
    errors=paulis if all_errors else [np.eye(D,dtype=complex)]
    syndrome=lambda p:tuple(int(np.max(np.abs(p@g-g@p))>1e-9) for g in gens)
    worst=0.;cases=0
    for s,t in itertools.product(sectors,repeat=2):
      for P in paulis:
       sp=syndrome(P)
       for E in errors:
        se=syndrome(E)
        yes=all(a^b^c==d for a,b,c,d in zip(s,t,se,sp))
        for F in errors:
            actual=P@F@ps[s]@P.conj().T@E@ps[t]/np.sqrt(K*D)
            sign=np.trace(P@F@P.conj().T@F.conj().T)/D
            target=sign*F@E@ps[t]/np.sqrt(K*D) if yes else np.zeros((D,D))
            worst=max(worst,float(np.linalg.norm(actual-target)));cases+=1
    return dict(n=n,k=n-r,operator_cases=cases,max_error=worst,passed=worst<1e-10)
res=[check(2,[kron([Z,Z])],True),check(4,[kron([X]*4),kron([Z]*4)])]
print(json.dumps(res,indent=2));assert all(x['passed'] for x in res)
