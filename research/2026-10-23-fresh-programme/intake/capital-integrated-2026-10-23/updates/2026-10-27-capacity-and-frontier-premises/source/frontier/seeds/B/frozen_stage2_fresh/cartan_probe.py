"""Numerical opposition screen for the Cartan hierarchy, binary physical support."""
import numpy as np
from itertools import combinations,permutations
from scipy.sparse import csr_matrix
from scipy.linalg import null_space

def parity(p):
    return -1 if sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))%2 else 1
for n in (1,2,3):
    D=2**n;pairs=list(combinations(range(D),2));d=len(pairs)
    cols=[];rows=[];vals=[]
    for i,(a,b) in enumerate(pairs):
        for j,(c,e) in enumerate(pairs):
            for aa,bb,sg1 in [(a,b,1),(b,a,-1)]:
                for cc,ee,sg2 in [(c,e,1),(e,c,-1)]:
                    rows.append(((aa*D+bb)*D+cc)*D+ee);cols.append(i*d+j);vals.append(sg1*sg2/2)
    W=csr_matrix((vals,(rows,cols)),shape=(D**4,d*d))
    sy=[]
    for i in range(d):
        for j in range(i,d):
            v=np.zeros(d*d);v[i*d+j]=1 if i==j else 1/np.sqrt(2)
            if i!=j:v[j*d+i]=1/np.sqrt(2)
            sy.append(v)
    S=np.array(sy).T
    # Remove exterior fourth powers: contraction wedges both columns.
    E=[]
    for four in combinations(range(D),4):
        v=np.zeros(d*d)
        for p in permutations(four):
            if p[0]<p[1] and p[2]<p[3]:
                v[pairs.index(p[:2])*d+pairs.index(p[2:])]=parity(p)/np.sqrt(6)
        E.append(v)
    V=S if not E else S@null_space(np.array(E)@S)
    WV=W@V
    B=np.zeros((len(V.T),len(V.T)))
    base=np.arange(D**4);ee=base%D;cc=(base//D)%D;bb=(base//D**2)%D;aa=base//D**3
    for mask in range(2**n):
        swapmask=mask
        aaa=(aa&~swapmask)|(cc&swapmask);ccc=(cc&~swapmask)|(aa&swapmask)
        perm=((aaa*D+bb)*D+ccc)*D+ee
        B+=(-.5)**(n-mask.bit_count())*WV.T@WV[perm]
    ev=np.linalg.eigvalsh(B)
    print(n,D,V.shape,ev[0],ev[-1],flush=True)
