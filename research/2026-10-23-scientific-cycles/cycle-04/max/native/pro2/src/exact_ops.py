"""Small exact rational operations; no floating solver acceptance conditions."""
from fractions import Fraction as F


def dot(a, b):
    return sum((x*y for x,y in zip(a,b)), F(0))


def rref(A, width=None):
    B=[list(map(F,r)) for r in A]
    width=len(B[0]) if B else (width or 0)
    piv=[]; k=0
    for j in range(width):
        i=next((i for i in range(k,len(B)) if B[i][j]),None)
        if i is None: continue
        B[k],B[i]=B[i],B[k]
        d=B[k][j]; B[k]=[v/d for v in B[k]]
        for i in range(len(B)):
            if i!=k and B[i][j]:
                a=B[i][j]; B[i]=[x-a*y for x,y in zip(B[i],B[k])]
        piv.append(j); k+=1
        if k==len(B): break
    return B,piv


def null(A,n):
    B,p=rref(A,n)
    j=next((j for j in range(n) if j not in p),None)
    if j is None: raise ValueError('empty kernel')
    v=[F(0)]*n; v[j]=F(1)
    for row,i in zip(B,p): v[i]=-row[j]
    return v,len(p)


def solve(A,b):
    n=len(A[0]); B,p=rref([list(r)+[v] for r,v in zip(A,b)])
    if n in p: raise ValueError('inconsistent system')
    x=[F(0)]*n
    for r,j in zip(B,p): x[j]=r[-1]
    return x


def action(n,q,D,X):
    Y=[[F(0)]*q for _ in range(n)]
    for (i,j),a in D.items():
        for k in range(q):
            Y[i][k]+=a*X[j][k]
            if i!=j: Y[j][k]+=a*X[i][k]
    return Y


def frob2(A):
    return sum((dot(r,r) for r in A),F(0))


def rotate(x):
    """A fixed exact orthogonal transform, making coordinate fixtures dense."""
    x=list(x)
    for j in range(len(x)-1):
        a,b=x[j],x[j+1]
        x[j]=(3*a-4*b)/5; x[j+1]=(4*a+3*b)/5
    return x


def basis(q):
    return [rotate([F(i==j) for j in range(q)]) for i in range(q)]


def core_graph(t,m):
    s=t-1; n=s+m
    edges={(i,j) for i in range(s) for j in range(i+1,n)}
    edges.update((s+i,s+i+1) for i in range(m-1))
    return n,edges


def core_rows(n,q):
    from math import isqrt
    state=20261022; X=[]
    for i in range(n):
        vals=[]
        for j in range(q):
            state=(1103515245*state+12345)%2147483648
            vals.append(state%5-2)
        if not any(vals): vals[0]=1
        s=sum(x*x for x in vals); d=isqrt(s)
        if d*d<s:d+=1
        X.append(rotate([F(x,d) for x in vals]))
    return X


def serial(v):
    if isinstance(v,F): return str(v)
    if isinstance(v,dict):
        if v and all(isinstance(k,tuple) for k in v):
            return [[i,j,str(a)] for (i,j),a in sorted(v.items()) if a]
        return {k:serial(x) for k,x in v.items()}
    if isinstance(v,(list,tuple)): return [serial(x) for x in v]
    return v


def graph_size(t,R):
    """Integer proof-family size only; never materialize this huge graph."""
    if t==0:return 1
    h=t*(t+1)//2; q=h+t
    m=q*(t-1)-t*(t-1)//2+2; n0=m+t-1
    N=4*(t+1)*n0*R**4
    return n0+m*N*h*graph_size(t-1,2*h*R)
