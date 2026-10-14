"""Small tensor-train utilities. No global configuration arrays are formed."""
import numpy as np
from scipy.linalg import svd, eigh

def scale(A,c):
    B=[x.copy() for x in A]; B[0]*=c; return B

def product(vs): return [np.asarray(v,float).reshape(1,-1,1) for v in vs]

def add(A,B):
    n=len(A)
    if n==1:return [A[0]+B[0]]
    C=[np.concatenate((A[0],B[0]),axis=2)]
    for a,b in zip(A[1:-1],B[1:-1]):
        c=np.zeros((a.shape[0]+b.shape[0],a.shape[1],a.shape[2]+b.shape[2]));c[:a.shape[0],:,:a.shape[2]]=a;c[a.shape[0]:,:,a.shape[2]:]=b;C.append(c)
    C.append(np.concatenate((A[-1],B[-1]),axis=0));return C

def inner(A,B):
    E=np.ones((1,1))
    for a,b in zip(A,B): E=np.einsum('ab,aic,bid->cd',E,a,b,optimize=True)
    return float(E[0,0])

def rounded(A,rank=16,tol=1e-13):
    A=[x.copy() for x in A]
    for i in range(len(A)-1):
        a,d,b=A[i].shape;Q,R=np.linalg.qr(A[i].reshape(a*d,b),mode='reduced');A[i]=Q.reshape(a,d,-1);A[i+1]=np.einsum('ab,bic->aic',R,A[i+1])
    for i in range(len(A)-1,0,-1):
        a,d,b=A[i].shape;U,s,V=svd(A[i].reshape(a,d*b),full_matrices=False,check_finite=False,lapack_driver='gesvd');
        rr=min(rank,max(1,int(np.count_nonzero(s>tol*(s[0] if len(s) else 1.)))))
        A[i]=V[:rr].reshape(rr,d,b);A[i-1]=np.einsum('aib,bc->aic',A[i-1],U[:,:rr]*s[:rr])
    return A

def transform(A,Ms):return [np.einsum('ij,ajb->aib',m,a,optimize=True) for a,m in zip(A,Ms)]

def apply_terms(terms,A,rank=16,tol=1e-14):
    out=None
    for Ms in terms:
        z=transform(A,Ms);out=z if out is None else rounded(add(out,z),rank,tol)
    return rounded(out,rank,tol)

def rightcanonical(A):
    A=[x.copy() for x in A]
    for i in range(len(A)-1,0,-1):
        a,d,b=A[i].shape;Q,R=np.linalg.qr(A[i].reshape(a,d*b).T,mode='reduced');A[i]=Q.T.reshape(-1,d,b);A[i-1]=np.einsum('aib,cb->aic',A[i-1],R)
    return A

def env_left(E,A,lam):
    return np.einsum('ab,aic,bid->cd',E,A,A,optimize=True)+np.einsum('aic,i,aid->cd',A,lam,A,optimize=True)

def env_right(E,A,lam):
    return np.einsum('aic,bid,cd->ab',A,A,E,optimize=True)+np.einsum('aic,i,bic->ab',A,lam,A,optimize=True)

def ov_left(E,A,B):return np.einsum('ab,aic,bid->cd',E,A,B,optimize=True)
def ov_right(E,A,B):return np.einsum('aic,bid,cd->ab',A,B,E,optimize=True)

def solve_sum_diagonal(lams,B,rank=12,sweeps=2,initial=None):
    """Two-site variational inverse of a separable SPD diagonal operator.
    Each local equation is a Kronecker sum, not a dense q^B matrix.
    """
    n=len(B);A=rightcanonical(B if initial is None else initial)
    for sweep in range(sweeps):
        ER=[None]*(n+1);OR=[None]*(n+1);ER[n]=np.zeros((1,1));OR[n]=np.ones((1,1))
        for j in range(n-1,-1,-1): ER[j]=env_right(ER[j+1],A[j],lams[j]);OR[j]=ov_right(OR[j+1],A[j],B[j])
        EL=np.zeros((1,1));OL=np.ones((1,1))
        for j in range(n-1):
            b=np.einsum('ap,piq,qjs,cs->aijc',OL,B[j],B[j+1],OR[j+2],optimize=True)
            le,U=eigh((EL+EL.T)/2);re,V=eigh((ER[j+2]+ER[j+2].T)/2)
            le=np.maximum(le,0);re=np.maximum(re,0)
            d=le[:,None,None,None]+lams[j][None,:,None,None]+lams[j+1][None,None,:,None]+re[None,None,None,:]
            if d.min()<=0: raise ValueError('Nonpositive separable local denominator')
            x=np.einsum('ab,aijc,cd->bijd',U,b,V,optimize=True)/d
            x=np.einsum('ab,bijd,cd->aijc',U,x,V,optimize=True)
            a,di,dj,c=x.shape;UU,s,VV=svd(x.reshape(a*di,dj*c),full_matrices=False,check_finite=False,lapack_driver='gesvd');rr=min(rank,len(s))
            A[j]=UU[:,:rr].reshape(a,di,rr);A[j+1]=(s[:rr,None]*VV[:rr]).reshape(rr,dj,c)
            EL=env_left(EL,A[j],lams[j]);OL=ov_left(OL,A[j],B[j])
        LL=[None]*(n+1);LO=[None]*(n+1);LL[0]=np.zeros((1,1));LO[0]=np.ones((1,1))
        for j in range(n):LL[j+1]=env_left(LL[j],A[j],lams[j]);LO[j+1]=ov_left(LO[j],A[j],B[j])
        ERc=np.zeros((1,1));ORc=np.ones((1,1))
        for j in range(n-2,-1,-1):
            b=np.einsum('ap,piq,qjs,cs->aijc',LO[j],B[j],B[j+1],ORc,optimize=True)
            le,U=eigh((LL[j]+LL[j].T)/2);re,V=eigh((ERc+ERc.T)/2);le=np.maximum(le,0);re=np.maximum(re,0)
            d=le[:,None,None,None]+lams[j][None,:,None,None]+lams[j+1][None,None,:,None]+re[None,None,None,:]
            if d.min()<=0: raise ValueError('Nonpositive separable local denominator')
            x=np.einsum('ab,aijc,cd->bijd',U,b,V,optimize=True)/d
            x=np.einsum('ab,bijd,cd->aijc',U,x,V,optimize=True)
            a,di,dj,c=x.shape;UU,s,VV=svd(x.reshape(a*di,dj*c),full_matrices=False,check_finite=False,lapack_driver='gesvd');rr=min(rank,len(s))
            A[j]=(UU[:,:rr]*s[:rr]).reshape(a,di,rr);A[j+1]=VV[:rr].reshape(rr,dj,c)
            ERc=env_right(ERc,A[j+1],lams[j+1]);ORc=ov_right(ORc,A[j+1],B[j+1])
    return A

def dense_for_audit_only(A):
    x=np.ones((1,1))
    for a in A:x=np.einsum('xa,aib->xib',x,a).reshape(-1,a.shape[2])
    return x[:,0]
