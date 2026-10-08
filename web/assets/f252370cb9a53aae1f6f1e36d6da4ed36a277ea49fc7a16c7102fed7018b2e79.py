"""Test a stronger, optional co-Choi Schur certificate; never a proof."""
import numpy as np

def reduction(c,dims):
    n=len(dims); a=c.reshape(dims+dims).copy()
    for i,d in enumerate(dims):
        t=np.trace(a,axis1=i,axis2=n+i)
        t=np.expand_dims(t,axis=(i,n+i))
        shape=[1]*(2*n); shape[i]=shape[n+i]=d
        a=t*np.eye(d).reshape(shape)-.5*a
    return a.reshape(c.shape)

def cochoi(dims):
    N=int(np.prod(dims)); c=np.empty((N,N,N,N))
    for a in range(N):
        for b in range(N):
            e=np.zeros((N,N));e[b,a]=1
            c[a,:,b,:]=reduction(e,dims)
    return c.reshape(N*N,N*N)

def schur_test(u,dims):
    N=len(u); ell=np.empty((N,N,N),complex)
    for a in range(N):
        e=np.zeros((N,N),complex);e[a,:]=u.conj()
        ell[a]=reduction(e,dims)
    A=np.einsum('a,aij->ij',u,ell)
    ai=np.linalg.inv(A)
    S=np.einsum('bik,kl,ajl->aibj',ell,ai,ell.conj()).reshape(N*N,N*N)
    R=cochoi(dims)
    return np.linalg.eigvalsh(R-S),np.linalg.eigvalsh(R+S)

if __name__=='__main__':
    rng=np.random.default_rng(367)
    for dims in [(3,),(3,3),(3,3,3)]:
        N=int(np.prod(dims));u=rng.normal(size=N)+1j*rng.normal(size=N);u/=np.linalg.norm(u)
        a,b=schur_test(u,dims)
        print(dims,a[0],b[0])
