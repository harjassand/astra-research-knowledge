"""Small exact rational-complex matrices, using existing NumPy object arrays."""
from dataclasses import dataclass
from fractions import Fraction as Q
import numpy as np


@dataclass(frozen=True)
class Z:
    re: Q = Q(0)
    im: Q = Q(0)

    def __post_init__(self):
        object.__setattr__(self,"re",Q(self.re))
        object.__setattr__(self,"im",Q(self.im))

    @staticmethod
    def cast(x):
        return x if isinstance(x,Z) else Z(Q(x))

    def __add__(self,x):
        x=Z.cast(x); return Z(self.re+x.re,self.im+x.im)
    __radd__=__add__
    def __neg__(self): return Z(-self.re,-self.im)
    def __sub__(self,x): return self+-Z.cast(x)
    def __rsub__(self,x): return Z.cast(x)+-self
    def __mul__(self,x):
        x=Z.cast(x); return Z(self.re*x.re-self.im*x.im,self.re*x.im+self.im*x.re)
    __rmul__=__mul__
    def __truediv__(self,x):
        x=Z.cast(x); d=x.re*x.re+x.im*x.im
        return Z((self.re*x.re+self.im*x.im)/d,(self.im*x.re-self.re*x.im)/d)
    def __rtruediv__(self,x): return Z.cast(x)/self
    def conjugate(self): return Z(self.re,-self.im)
    def __bool__(self): return bool(self.re or self.im)
    def __complex__(self): return complex(float(self.re),float(self.im))
    def __eq__(self,x):
        try: x=Z.cast(x)
        except (TypeError,ValueError): return False
        return self.re==x.re and self.im==x.im


I=Z(0,1)


def mat(rows): return np.array([[Z.cast(x) for x in r] for r in rows],dtype=object)
def zeros(n,m=None): return mat([[0]*(n if m is None else m) for _ in range(n)])
def eye(n): return mat([[int(i==j) for j in range(n)] for i in range(n)])
def adj(A): return np.vectorize(lambda x:Z.cast(x).conjugate(),otypes=[object])(A.T)
def equal(A,B): return A.shape==B.shape and all(x==y for x,y in zip(A.flat,B.flat))
def trace(A): return sum((A[i,i] for i in range(len(A))),Z())
def numeric(A): return np.array([[complex(Z.cast(x)) for x in r] for r in A],complex)
def real_scalar(z):
    z=Z.cast(z)
    assert z.im==0
    return z.re


def psd(A):
    A=A.copy()
    if not equal(A,adj(A)): return False
    while len(A):
        diag=[real_scalar(A[i,i]) for i in range(len(A))]
        if min(diag)<0: return False
        ix=[i for i,d in enumerate(diag) if d>0]
        if not ix: return all(not x for x in A.flat)
        p=ix[0]; rest=[i for i in range(len(A)) if i!=p]
        A=A[np.ix_(rest,rest)]-A[np.ix_(rest,[p])]@A[np.ix_([p],rest)]/A[p,p]
    return True


def psd_or_separator(A):
    """Polynomial rational PSD separation, including singular candidates.

    If infeasible, return v with v^dagger A v < 0. For a real symmetric input
    the vector is real. This is the concrete separation query used by the
    finite-dimensional ellipsoid reduction, not an optimization oracle.
    """
    original=A.copy(); A=A.copy(); T=eye(len(A))
    if not equal(A,adj(A)): raise ValueError("Hermitian input required")
    while len(A):
        diag=[real_scalar(A[i,i]) for i in range(len(A))]
        neg=[i for i,d in enumerate(diag) if d<0]
        if neg:
            v=zeros(len(A),1); v[neg[0],0]=Z(1)
            v=T@v
            return False,v,real_scalar((adj(v)@original@v)[0,0])
        positive=[i for i,d in enumerate(diag) if d>0]
        if not positive:
            pairs=[(i,j) for i in range(len(A)) for j in range(i+1,len(A)) if A[i,j]]
            if not pairs: return True,None,None
            i,j=pairs[0]; v=zeros(len(A),1); v[i,0]=Z(1); v[j,0]=-Z.cast(A[i,j]).conjugate()
            v=T@v
            return False,v,real_scalar((adj(v)@original@v)[0,0])
        p=positive[0]; rest=[i for i in range(len(A)) if i!=p]
        E=zeros(len(A),len(rest))
        for j,i in enumerate(rest):
            E[i,j]=Z(1); E[p,j]=-A[p,i]/A[p,p]
        T=T@E
        A=A[np.ix_(rest,rest)]-A[np.ix_(rest,[p])]@A[np.ix_([p],rest)]/A[p,p]
    return True,None,None


def tensor(xs):
    ans=eye(1)
    for x in xs: ans=np.kron(ans,x)
    return ans


def paulis():
    return [mat([[0,1],[1,0]]),mat([[0,-I],[I,0]]),mat([[1,0],[0,-1]])]


def site_ops(n,reference=False):
    if reference:
        # Bell vectors without sqrt(2); B^dag B=2 I.
        omega=mat([[1],[0],[0],[1]])
        basis=np.hstack([omega]+[np.kron(p,eye(2))@omega for p in paulis()])
        local=[adj(basis)@np.kron(p,eye(2))@basis/2 for p in paulis()]; d=4
    else: local=paulis(); d=2
    return [tensor([p if j==i else eye(d) for j in range(n)]) for i in range(n) for p in local]


def block_parts(A,n):
    D=zeros(3*n)
    for i in range(n): D[3*i:3*i+3,3*i:3*i+3]=A[3*i:3*i+3,3*i:3*i+3]
    return D,A-D


def from_factors(V,F,G,n):
    D=V@V.T; B=V@F.T; R=D+F@F.T+G@G.T; J=B.T-B
    S,U=block_parts(-B-B.T,n)
    C=R+J*I
    return dict(D=D,B=B,R=R,J=J,S=S,U=U,C=C,
                Sigma=np.block([[D,B],[B.T,R-D]]))


def hamiltonian(U,A):
    H=zeros(len(A[0]))
    for a in range(len(A)):
        for b in range(a+1,len(A)):
            H += (A[a]@A[b])*U[a,b]
    return H


def generator(rho,C,U,A):
    H=hamiltonian(U,A); out=(H@rho-rho@H)*(-I)
    for a in range(len(A)):
        for b in range(len(A)):
            if C[a,b]:
                BA=A[b]@A[a]
                out += (A[a]@rho@A[b]-(BA@rho+rho@BA)/2)*C[a,b]
    return out


def lowering(n):
    local=[]
    for a in range(1,4):
        q=zeros(4); q[0,a]=Z(1); local.append(q)
    return [tensor([q if j==i else eye(4) for j in range(n)]) for i in range(n) for q in local]


def moment_matrices(rho,n):
    a=lowering(n); K=3*n; M=zeros(K); N=zeros(K)
    for i in range(K):
        for j in range(K):
            M[i,j]=trace(adj(a[j])@a[i]@rho)
            if i//3!=j//3: N[i,j]=trace(a[i]@a[j]@rho)
    return M,N


def pt(A,dims,party):
    out=zeros(len(A))
    for i in range(len(A)):
        for j in range(len(A)):
            x=list(np.unravel_index(i,dims)); y=list(np.unravel_index(j,dims))
            x[party],y[party]=y[party],x[party]
            out[np.ravel_multi_index(x,dims),np.ravel_multi_index(y,dims)]=A[i,j]
    return out


def inner(A,B): return sum((x*y for x,y in zip(A.flat,B.flat)),Z())


def dual(Y,R,J,U,n):
    K=3*n; P,Qm,T=Y[:K,:K],Y[:K,K:],Y[K:,K:]
    valid=(psd(Y) and equal(block_parts(P-T,n)[0],zeros(K)) and
           equal(block_parts(Qm+Qm.T,n)[0],zeros(K)))
    return valid,real_scalar(inner(Qm,U+J)-inner(T,R))


def dual_witness(Y,n):
    K=3*n; P,Qm,T=Y[:K,:K],Y[:K,K:],Y[K:,K:]; a=lowering(n)
    W=zeros(4**n)
    for i in range(K):
        for j in range(K):
            O=adj(a[j])@a[i]
            W += (O+adj(O))*(P[i,j]+T[i,j])/4-(O-adj(O))*Qm[i,j]/(2*I)
            if i//3!=j//3:
                O=a[i]@a[j]
                W += (O+adj(O))*(P[i,j]-T[i,j])/4+(O-adj(O))*Qm[i,j]/(2*I)
    return W
