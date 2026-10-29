"""Rational coefficient compilation and exact receiver arithmetic (stdlib).

The real/skew Z coefficients retain arbitrary complex quantum references.
The Choi convention is C[a*f+p,b*f+q]=Phi(E_ab)[p,q].
"""
from fractions import Fraction as F


def zeros(n, m=None):
    return [[F(0) for _ in range(n if m is None else m)] for _ in range(n)]


def eye(n, a=F(1)):
    M=zeros(n)
    for i in range(n): M[i][i]=a
    return M


def encode(M):
    return [[str(v) for v in row] for row in M]


def decode(M):
    return [[F(v) for v in row] for row in M]


def source_coefficients(L):
    ell,n=len(L),len(L[0]);e=n+ell+1
    assert all(v>=0 for row in L for v in row)
    assert all(sum(row)>0 for row in L), 'delete identically zero reference rows first'
    assert all(sum(L[z][i] for z in range(ell))==1 for i in range(n))
    A0=zeros(e)
    for i in range(n): A0[i][i]=F(1,n)
    for z in range(ell): A0[n+z][n+z]=sum(L[z])/n
    A0[-1][-1]=F(1)
    out=[('constant',A0)]
    for kind in ('X','Y','Z'):
        for i in range(n-1):
            A=zeros(e)
            if kind=='X': A[i][i]=F(1);A[n-1][n-1]=F(-1)
            for z in range(ell):
                d=L[z][i]-L[z][n-1]
                if kind=='X': A[n+z][n+z]=d
                else:
                    A[n+z][-1]=d
                    A[-1][n+z]=d if kind=='Y' else -d
            out.append((kind+str(i),A))
    assert sum(A0[i][i] for i in range(e))==3
    assert all(sum(A[i][i] for i in range(e))==0 for _,A in out[1:])
    return out


def target_coefficients(K,c):
    m,n=len(K),len(K[0]);f=m+1
    B0=zeros(f)
    for y in range(m): B0[y][y]=sum(K[y])/n
    B0[-1][-1]=c
    out=[('constant',B0)]
    for kind in ('X','Y','Z'):
        for i in range(n-1):
            B=zeros(f)
            for y in range(m):
                d=K[y][i]-K[y][n-1]
                if kind=='X': B[y][y]=d
                else:
                    B[y][-1]=d
                    B[-1][y]=d if kind=='Y' else -d
            out.append((kind+str(i),B))
    return out


def phi(C,A,f):
    out=zeros(f)
    for a,row in enumerate(A):
        for b,v in enumerate(row):
            if v:
                for p in range(f):
                    for q in range(f): out[p][q]+=v*C[a*f+p][b*f+q]
    return out


def minus(A,B):
    return [[a-b for a,b in zip(ar,br)] for ar,br in zip(A,B)]


def trace_product(A,B):
    return sum(A[i][j]*B[j][i] for i in range(len(A)) for j in range(len(A)))


def upper_coords(n):
    return [(i,j) for i in range(n) for j in range(i,n)]


def pack(C,K):
    return [C[i][j] for i,j in upper_coords(len(C))]+[v for row in K for v in row]


def unpack(v,d,m,n):
    C=zeros(d);coords=upper_coords(d)
    for x,(i,j) in zip(v,coords): C[i][j]=x;C[j][i]=x
    K=[list(v[len(coords)+y*n:len(coords)+(y+1)*n]) for y in range(m)]
    return C,K


def linear_system(L,m):
    """All independent symmetric/skew entries plus stochasticity.

    Returns exact rows A,b for A pack(C,K)=b; some rows can be dependent.
    R is eliminated as B0(K,c)-Phi(A0).
    """
    n=len(L[0]);f=m+1;source=source_coefficients(L);e=len(source[0][1]);d=e*f
    coords=upper_coords(d);nv=len(coords)+m*n
    specs=[]
    for j,(tag,A) in enumerate(source[1:],1):
        positions=[(p,q) for p in range(f) for q in range(p+(tag[0]=='Z'),f)]
        specs.extend((j,p,q) for p,q in positions)
    rows=[];rhs=[]
    for j,p,q in specs:
        A=source[j][1];row=[F(0)]*nv
        for h,(u,v) in enumerate(coords):
            a,pp=divmod(u,f);b,qq=divmod(v,f)
            if pp==p and qq==q: row[h]+=A[a][b]
            if u!=v and qq==p and pp==q: row[h]+=A[b][a]
        for y in range(m):
            for i in range(n):
                K=zeros(m,n);K[y][i]=F(1)
                row[len(coords)+y*n+i]=-target_coefficients(K,F(0))[j][1][p][q]
        rows.append(row);rhs.append(F(0))
    for i in range(n):
        row=[F(0)]*nv
        for y in range(m): row[len(coords)+y*n+i]=F(1)
        rows.append(row);rhs.append(F(1))
    return source,rows,rhs,specs


def quadratic_matrix(v,n):
    """Convert upper-coordinate coefficients to trace-product matrix."""
    M=zeros(n)
    for x,(i,j) in zip(v,upper_coords(n)):
        M[i][j]=x if i==j else x/2
        M[j][i]=M[i][j]
    return M


def ldl_positive(M):
    """Exact positive-definiteness, no numerical eigenvalue premise."""
    n=len(M);assert all(M[i][j]==M[j][i] for i in range(n) for j in range(n))
    L=eye(n);piv=[]
    for j in range(n):
        dj=M[j][j]-sum(L[j][k]**2*piv[k] for k in range(j))
        if dj<=0:return False,{'failed_pivot':j,'value':str(dj)}
        piv.append(dj)
        for i in range(j+1,n):
            L[i][j]=(M[i][j]-sum(L[i][k]*L[j][k]*piv[k] for k in range(j)))/dj
    return True,{'minimum_LDL_pivot':str(min(piv)),'order':n}


def matvec(A,v):
    return [sum(a*x for a,x in zip(row,v)) for row in A]


def baseline(L,m,c):
    source=source_coefficients(L);e=len(source[0][1]);f=m+1
    eta=min(F(1,m),c)/6;C=eye(e*f,eta);K=[[F(1,m)]*len(L[0]) for _ in range(m)]
    R=minus(target_coefficients(K,c)[0][1],phi(C,source[0][1],f))
    assert ldl_positive(C)[0] and ldl_positive(R)[0]
    return C,K,R


def min_floor_columns(W,kappa):
    m,n=len(W),len(W[0])
    return sum(kappa*sum(W[y][i] for y in range(m))+
               (1-m*kappa)*min(W[y][i] for y in range(m)) for i in range(n))
