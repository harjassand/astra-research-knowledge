"""Exact four-exterior-register DP for rational-complex hard BCS norms.
No external dependencies. rank(F) is acquired, not supplied by an oracle.
Letters E,R,C are empty/up-row/down-column site occupations.
"""
from fractions import Fraction as Q
from dataclasses import dataclass
from itertools import combinations,permutations,product
import secrets

@dataclass(frozen=True)
class G:
    re: Q=Q(0)
    im: Q=Q(0)
    def __post_init__(self):
        object.__setattr__(self,'re',Q(self.re));object.__setattr__(self,'im',Q(self.im))
    def __add__(self,b):
        b=cast(b);return G(self.re+b.re,self.im+b.im)
    __radd__=__add__
    def __neg__(self):return G(-self.re,-self.im)
    def __sub__(self,b):return self+-cast(b)
    def __rsub__(self,b):return cast(b)+-self
    def __mul__(self,b):
        b=cast(b);return G(self.re*b.re-self.im*b.im,self.re*b.im+self.im*b.re)
    __rmul__=__mul__
    def conj(self):return G(self.re,-self.im)
    def __truediv__(self,b):
        b=cast(b);d=b.re*b.re+b.im*b.im
        if not d:raise ZeroDivisionError()
        c=self*b.conj();return G(c.re/d,c.im/d)
    def __bool__(self):return bool(self.re or self.im)
    def norm(self):return self.re*self.re+self.im*self.im

def cast(a):
    if isinstance(a,G):return a
    if isinstance(a,tuple):return G(*a)
    return G(a)

def rref(A):
    A=[[cast(x) for x in row] for row in A]
    rows=len(A);cols=len(A[0]) if rows else 0;r=0;piv=[]
    for j in range(cols):
        p=next((i for i in range(r,rows) if A[i][j]),None)
        if p is None:continue
        A[r],A[p]=A[p],A[r]
        v=A[r][j];A[r]=[x/v for x in A[r]]
        for i in range(rows):
            if i!=r and A[i][j]:
                v=A[i][j];A[i]=[x-v*y for x,y in zip(A[i],A[r])]
        piv.append(j);r+=1
        if r==rows:break
    return A,piv

def inverse(A):
    n=len(A)
    M,p=rref([list(row)+[G(int(i==j)) for j in range(n)] for i,row in enumerate(A)])
    if p[:n]!=list(range(n)):raise ValueError('singular')
    return [row[n:] for row in M]

def factorize(F):
    """Acquire exact U,V, with F=UV^T by rational-complex elimination."""
    F=[[cast(x) for x in row] for row in F];n=len(F)
    _,cols=rref(F);r=len(cols)
    if not r:return [[] for _ in range(n)],[[] for _ in range(n)]
    U=[[F[i][j] for j in cols] for i in range(n)]
    _,rows=rref(list(map(list,zip(*U))))
    B=inverse([U[i] for i in rows])
    VT=[[sum((B[i][a]*F[rows[a]][j] for a in range(r)),G()) for j in range(n)] for i in range(r)]
    V=list(map(list,zip(*VT)))
    assert all(sum((U[i][a]*V[j][a] for a in range(r)),G())==F[i][j] for i in range(n) for j in range(n))
    return U,V

def dense_offdiagonal_rank_one(F):
    """Acquire a rank-one diagonal completion on the admitted dense case.
    Returns None if n<3, an off-diagonal zero occurs, or verification fails.
    Does not solve general diagonal low-rank completion.
    """
    F=[[cast(x) for x in row] for row in F];n=len(F)
    if n<3 or any(not F[i][j] for i in range(n) for j in range(n) if i!=j):return None
    u=[G(1)]+[G() for _ in range(n-1)];v=[G()]+F[0][1:]
    for i in range(1,n):
        j=next(j for j in range(1,n) if j!=i);u[i]=F[i][j]/v[j]
    v[0]=F[1][0]/u[1]
    if any(u[i]*v[j]!=F[i][j] for i in range(n) for j in range(n) if i!=j):return None
    return [[x] for x in u],[[x] for x in v]

def extend(mask,row):
    for j,x in enumerate(row):
        if x and not mask>>j&1:
            yield mask|1<<j,x*((-1)**((mask>>(j+1)).bit_count()))

def count_uv(U,V,allowed=None,row_weights=None,col_weights=None):
    n=len(U);r=len(U[0]) if n else 0
    if len(V)!=n or any(len(row)!=r for row in U+V):raise ValueError('bad factor dimensions')
    allowed=[set('ERC') for _ in range(n)] if allowed is None else allowed
    row_weights=[Q(1)]*n if row_weights is None else row_weights
    col_weights=[Q(1)]*n if col_weights is None else col_weights
    if len(allowed)!=n or any(not set(t)<=set('ERC') for t in allowed):raise ValueError('bad site table')
    if len(row_weights)!=n or len(col_weights)!=n or any(w<0 for w in row_weights+col_weights):raise ValueError('bad nonnegative activities')
    D={(0,0,0,0):G(1)};max_states=1
    for i in range(n):
        N={}
        def add(key,val):
            if val:N[key]=N.get(key,G())+val
        for (a,b,c,d),val in D.items():
            if 'E' in allowed[i]:add((a,b,c,d),val)
            if 'R' in allowed[i]:
                for aa,x in extend(a,U[i]):
                    for bb,y in extend(b,U[i]):add((aa,bb,c,d),val*x*y.conj()*row_weights[i])
            if 'C' in allowed[i]:
                for cc,x in extend(c,V[i]):
                    for dd,y in extend(d,V[i]):add((a,b,cc,dd),val*x*y.conj()*col_weights[i])
        D={k:v for k,v in N.items() if v};max_states=max(max_states,len(D))
    coeff=[G() for _ in range(r+1)]
    for (a,b,c,d),val in D.items():
        if a==c and b==d:coeff[a.bit_count()]+=val
    for v in coeff:assert not v.im and v.re>=0
    return [v.re for v in coeff],max_states

def acquire(F,try_dense_completion=True):
    n=len(F)
    if any(len(row)!=n for row in F):raise ValueError('F must be square')
    UV=dense_offdiagonal_rank_one(F) if try_dense_completion else None
    completed=UV is not None
    if UV is None:UV=factorize(F)
    return UV,{'rank_used':len(UV[0][0]) if F else 0,'diagonal_completion':completed}

def count(F,allowed=None,row_weights=None,col_weights=None,try_dense_completion=True):
    UV,meta=acquire(F,try_dense_completion)
    coeff,m=count_uv(*UV,allowed,row_weights,col_weights)
    return coeff,dict(meta,max_states=m)


def uniform_below(m,randbits=secrets.randbits):
    if m<=0:raise ValueError('nonpositive range')
    b=(m-1).bit_length()
    while True:
        x=randbits(b)
        if x<m:return x

def choose_rational(weights,randbits=secrets.randbits):
    # Exact integer draw after a shared denominator, no rare event rejection.
    from math import lcm
    den=1
    for w in weights:den=lcm(den,w.denominator)
    nums=[w.numerator*(den//w.denominator) for w in weights]
    x=uniform_below(sum(nums),randbits)
    for i,v in enumerate(nums):
        if x<v:return i
        x-=v
    raise AssertionError()

def sample_uv(U,V,k=None,allowed=None,row_weights=None,col_weights=None,randbits=secrets.randbits):
    n=len(U);tables=[set(t) for t in (allowed or [set('ERC') for _ in range(n)])]
    def mass():
        coeff,_=count_uv(U,V,tables,row_weights,col_weights)
        return sum(coeff) if k is None else (coeff[k] if k<len(coeff) else Q(0))
    total=mass()
    if not total:raise ValueError('zero sector')
    out=[]
    for i in range(n):
        old=tables[i];choices=[t for t in 'ERC' if t in old];weights=[]
        for t in choices:
            tables[i]={t};weights.append(mass())
        assert sum(weights)==total
        idx=choose_rational(weights,randbits);tables[i]={choices[idx]};out.append(choices[idx]);total=weights[idx]
    return ''.join(out)

def forward_branch(D,Urow,Vrow,t,rw=Q(1),cw=Q(1)):
    N={}
    def add(key,val):
        if val:N[key]=N.get(key,G())+val
    for (a,b,c,d),val in D.items():
        if t=='E':add((a,b,c,d),val)
        elif t=='R':
            for aa,x in extend(a,Urow):
                for bb,y in extend(b,Urow):add((aa,bb,c,d),val*x*y.conj()*rw)
        elif t=='C':
            for cc,x in extend(c,Vrow):
                for dd,y in extend(d,Vrow):add((a,b,cc,dd),val*x*y.conj()*cw)
        else:raise ValueError('bad branch')
    return {key:val for key,val in N.items() if val}

def backward_site(L,Urow,Vrow,allowed,rw=Q(1),cw=Q(1)):
    # Algebraic transpose of the forward transfer, NOT conjugate transpose.
    N={}
    def add(key,val):
        if val:N[key]=N.get(key,G())+val
    def remove(mask,row):
        for j,x in enumerate(row):
            if x and mask>>j&1:
                yield mask^(1<<j),x*((-1)**((mask>>(j+1)).bit_count()))
    for (a,b,c,d),val in L.items():
        if 'E' in allowed:add((a,b,c,d),val)
        if 'R' in allowed:
            for aa,x in remove(a,Urow):
                for bb,y in remove(b,Urow):add((aa,bb,c,d),val*x*y.conj()*rw)
        if 'C' in allowed:
            for cc,x in remove(c,Vrow):
                for dd,y in remove(d,Vrow):add((a,b,cc,dd),val*x*y.conj()*cw)
    return {key:val for key,val in N.items() if val}

def sample_uv_cached(U,V,k=None,allowed=None,row_weights=None,col_weights=None,randbits=secrets.randbits):
    """Same exact law as sample_uv; cache suffix duals to make sampling linear in n.
    Cost O(n r^2 16^r) operations and O(n16^r) field storage for r>=1.
    """
    n=len(U);r=len(U[0]) if n else 0
    tables=[set(t) for t in (allowed if allowed is not None else [set('ERC') for _ in range(n)])]
    rw=[Q(1)]*n if row_weights is None else row_weights
    cw=[Q(1)]*n if col_weights is None else col_weights
    coeff,_=count_uv(U,V,tables,rw,cw) # Validate and independently establish total.
    total=sum(coeff) if k is None else (coeff[k] if 0<=k<len(coeff) else Q(0))
    if not total:raise ValueError('zero sector')
    L=[None]*(n+1)
    L[n]={(a,b,a,b):G(1) for a in range(1<<r) for b in range(1<<r) if a.bit_count()==b.bit_count() and (k is None or a.bit_count()==k)}
    for i in range(n-1,-1,-1):L[i]=backward_site(L[i+1],U[i],V[i],tables[i],rw[i],cw[i])
    assert L[0].get((0,0,0,0),G())==G(total)
    D={(0,0,0,0):G(1)};out=[]
    for i in range(n):
        choices=[t for t in 'ERC' if t in tables[i]];branches=[];weights=[]
        for t in choices:
            P=forward_branch(D,U[i],V[i],t,rw[i],cw[i]);branches.append(P)
            w=sum((v*L[i+1].get(key,G()) for key,v in P.items()),G())
            assert not w.im and w.re>=0;weights.append(w.re)
        assert sum(weights)==total
        j=choose_rational(weights,randbits);out.append(choices[j]);D=branches[j];total=weights[j]
    return ''.join(out),{'suffix_state_entries':sum(len(v) for v in L),'largest_suffix_states':max(map(len,L))}


def sample(F,k=None,allowed=None,row_weights=None,col_weights=None,randbits=secrets.randbits,try_dense_completion=True):
    """Acquire factorization from F and sample its exact admitted occupation law."""
    UV,meta=acquire(F,try_dense_completion)
    word,stats=sample_uv_cached(*UV,k,allowed,row_weights,col_weights,randbits)
    return word,dict(meta,**stats)


def determinant(A):
    n=len(A);val=G()
    for p in permutations(range(n)):
        term=G((-1)**sum(p[i]>p[j] for i in range(n) for j in range(i+1,n)))
        for i in range(n):term*=cast(A[i][p[i]])
        val+=term
    return val

def enumerate_count(F,allowed=None,row_weights=None,col_weights=None):
    n=len(F);allowed=allowed or [set('ERC') for _ in range(n)]
    row_weights=row_weights or [Q(1)]*n;col_weights=col_weights or [Q(1)]*n
    coeff=[Q(0)]*(n//2+1);law={}
    for word in product('ERC',repeat=n):
        if any(word[i] not in allowed[i] for i in range(n)):continue
        I=[i for i,t in enumerate(word) if t=='R'];J=[i for i,t in enumerate(word) if t=='C']
        if len(I)!=len(J):continue
        w=determinant([[F[i][j] for j in J] for i in I]).norm()
        for i in I:w*=row_weights[i]
        for j in J:w*=col_weights[j]
        coeff[len(I)]+=w
        if w:law[''.join(word)]=w
    return coeff,law
