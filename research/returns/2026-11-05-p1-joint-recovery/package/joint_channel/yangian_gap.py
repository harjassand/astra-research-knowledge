import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import LinearOperator, eigsh
from math import sqrt
from collections import defaultdict
import sys,time

def schur(n):
    # dictionary (path,twice J, twice m)-> normalized computational vector
    D={((),0,0):np.array([1.])}
    for k in range(n):
        R={}
        paths=sorted(set((p,j) for (p,j,m) in D))
        for p,j in paths:
            for jj in (j+1,j-1):
                if jj<0:continue
                pp=p+(jj,)
                for mm in range(-jj,jj+1,2):
                    v=np.zeros(2**(k+1))
                    if (p,j,mm-1) in D:
                        coeff=sqrt((j+mm+1)/(2*(j+1))) if jj==j+1 else -sqrt((j-mm+1)/(2*(j+1)))
                        v+=coeff*np.kron(D[p,j,mm-1],[1,0])
                    if (p,j,mm+1) in D:
                        coeff=sqrt((j-mm+1)/(2*(j+1))) if jj==j+1 else sqrt((j+mm+1)/(2*(j+1)))
                        v+=coeff*np.kron(D[p,j,mm+1],[0,1])
                    R[pp,jj,mm]=v
        D=R
    keys=sorted(D,key=lambda z:(z[1],z[2],z[0]))
    Q=np.stack([D[k] for k in keys],axis=1)
    groups=defaultdict(list)
    for i,(p,j,m) in enumerate(keys):groups[j,m].append(i)
    return Q,dict(groups)

def Yz(n):
    dim=2**n; rows=[];cols=[];data=[]
    # Yz=sum_{j<k}(sigma_j^x sigma_k^y-sigma_j^y sigma_k^x)
    for b in range(dim):
        for j in range(n):
            for k in range(j+1,n):
                bj=(b>>(n-1-j))&1;bk=(b>>(n-1-k))&1
                if bj==bk:continue
                a=b^(1<<(n-1-j))^(1<<(n-1-k))
                rows.append(a);cols.append(b);data.append(2j*(bj-bk))
    return coo_matrix((data,(rows,cols)),shape=(dim,dim)).tocsr()

def run(n):
    Q,G=schur(n);d=len(Q);yz=Q.T@(Yz(n)@Q)
    js=sorted(set(j for j,m in G));mult={j:len(G[j,j]) for j in js}
    offsets={};size=0
    for j in js:offsets[j]=size;size+=mult[j]**2
    # normalized Hilbert-Schmidt coordinate sqrt(2J+1) B_J so Euclidean norm
    blocks={}
    for j in js:
        for k in js:
            if abs(j-k)>2:continue
            blocks[j,k]=[yz[np.ix_(G[j,m],G[k,m])] for m in range(-min(j,k),min(j,k)+1,2)]
    def unpack(v):return {j:v[offsets[j]:offsets[j]+mult[j]**2].reshape(mult[j],mult[j])/sqrt(j+1) for j in js}
    def apply(v):
        X=unpack(v);R={j:np.zeros_like(X[j],dtype=complex) for j in js}
        for (j,k),YY in blocks.items():
            for A in YY:
                AA=A@A.conj().T
                R[j]+=AA@X[j]+X[j]@AA-2*A@X[k]@A.conj().T
        # invariant projection includes average over j+1 m states; sum components 3/16
        return np.concatenate([(3/16)*R[j].reshape(-1)/sqrt(j+1) for j in js])
    ident=np.concatenate([sqrt(j+1)*np.eye(mult[j]).reshape(-1) for j in js])/sqrt(d)
    def shifted(v):return apply(v)+2*n*n*ident*np.vdot(ident,v)
    L=LinearOperator((size,size),matvec=shifted,dtype=complex)
    if size<=10:
        vals=np.linalg.eigvalsh(np.stack([shifted(v) for v in np.eye(size)],axis=1))
    else:
        vals,vecs=eigsh(L,k=min(6,size-2),which='SA',tol=1e-10,maxiter=10000)
    print(n,size, np.sort(vals), 'identity_err',np.linalg.norm(apply(ident)),flush=True)

for n in map(int,sys.argv[1:] or ['2','3','4','5','6','7']):
 t=time.time();run(n);print('seconds',time.time()-t,flush=True)
