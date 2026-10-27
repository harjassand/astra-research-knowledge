"""Exploratory local S4 decomposition; no claim of an endpoint witness."""
import numpy as np
from itertools import combinations, combinations_with_replacement
from scipy.linalg import null_space
from scipy.optimize import linprog
pairs=list(combinations(range(4),2))
Q=null_space(np.ones((1,4)))
Q2=null_space(np.ones((1,3)))
matchings=[frozenset((frozenset((0,1)),frozenset((2,3)))),frozenset((frozenset((0,2)),frozenset((1,3)))),frozenset((frozenset((0,3)),frozenset((1,2))))]
reps=[[],[],[],[]]
for a,b in pairs:
    perm=list(range(4));perm[a],perm[b]=perm[b],perm[a]
    P=np.eye(4)[perm]
    R=Q.T@P@Q
    P2=np.zeros((3,3))
    for j,m in enumerate(matchings):
        image=frozenset(frozenset(perm[x] for x in edge) for edge in m)
        P2[matchings.index(image),j]=1
    reps[0].append(np.ones((1,1)))
    reps[1].append(R)
    reps[2].append(Q2.T@P2@Q2)
    reps[3].append(-R)
for n in (1,2,3,4):
    minima={1.: (1e9,None),1/3:(1e9,None),0.:(1e9,None),-1/3:(1e9,None),-1.:(1e9,None)}
    for types in combinations_with_replacement(range(4),n):
        K=0;T=0
        for a in range(6):
            F=np.ones((1,1));A=np.ones((1,1))
            for typ in types:
                f=reps[typ][a]
                F=np.kron(F,f);A=np.kron(A,f-.5*np.eye(len(f)))
            K=K+A/6;T=T+F/6
        vals,V=np.linalg.eigh(T)
        for t in minima:
            use=np.flatnonzero(np.isclose(vals,t))
            if len(use):
                val=np.linalg.eigvalsh(V[:,use].T@K@V[:,use])[0]
                if val<minima[t][0]-1e-9:minima[t]=(float(val),types)
    keys=[1.,1/3,0.]
    c=[minima[t][0] for t in keys]
    opt=linprog(c,A_eq=[np.ones(3),keys],b_eq=[1,.5],bounds=[(0,None)]*3,method='highs')
    print(n,minima,'relaxed',opt.fun,'weights',opt.x,flush=True)
