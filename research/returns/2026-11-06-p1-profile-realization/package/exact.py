"""Exact dense Q(i) linear algebra. No numerical tolerances or square roots.

This kernel is shared by the compiler and certificate checker; the latter is
therefore a separate implementation check, not an independent formal review.
"""
from dataclasses import dataclass
from fractions import Fraction as F

@dataclass(frozen=True)
class Q:
    re:F=F(0)
    im:F=F(0)
    def __add__(self,other):
        z=q(other);return Q(self.re+z.re,self.im+z.im)
    __radd__=__add__
    def __neg__(self):return Q(-self.re,-self.im)
    def __sub__(self,other):return self+-q(other)
    def __rsub__(self,other):return q(other)+-self
    def __mul__(self,other):
        z=q(other);return Q(self.re*z.re-self.im*z.im,self.re*z.im+self.im*z.re)
    __rmul__=__mul__
    def __truediv__(self,other):
        z=q(other);d=z.re*z.re+z.im*z.im
        if not d:raise ZeroDivisionError
        w=self*z.conj();return Q(w.re/d,w.im/d)
    def conj(self):return Q(self.re,-self.im)
    def __bool__(self):return bool(self.re or self.im)
    def out(self):return str(self.re) if not self.im else [str(self.re),str(self.im)]

def q(x):
    if isinstance(x,Q):return x
    if isinstance(x,float):raise ValueError('Use exact rational strings, not floating point')
    if isinstance(x,(list,tuple)):
        if len(x)!=2:raise ValueError('Complex scalars require [real,imag]')
        u,v=q(x[0]),q(x[1])
        if u.im or v.im:raise ValueError('Complex parts must be real rationals')
        return Q(u.re,v.re)
    return Q(F(x))
def mat(a):return [[q(x) for x in row] for row in a]
def out(a):return [[x.out() for x in row] for row in a]
def zero(n,m=None):return [[Q() for _ in range(n if m is None else m)] for _ in range(n)]
def eye(n):return [[q(i==j) for j in range(n)] for i in range(n)]
def adj(a):return [[a[i][j].conj() for i in range(len(a))] for j in range(len(a[0]))]
def add(a,b):return [[x+y for x,y in zip(row,col)] for row,col in zip(a,b)]
def scale(s,a):return [[q(s)*x for x in row] for row in a]
def mul(a,b):
    assert len(a[0])==len(b)
    return [[sum((x*y for x,y in zip(row,col) if x and y),Q()) for col in zip(*b)] for row in a]
def tr(a):return sum((a[i][i] for i in range(len(a))),Q())
def flat(a):return [x for row in a for x in row]
def kron(a,b):return [[x*y for x in ra for y in rb] for ra in a for rb in b]
def real(z):
    z=q(z)
    if z.im:raise ArithmeticError('Expected an exactly real scalar')
    return z.re

def inv(a):
    n=len(a)
    if any(len(row)!=n for row in a):raise ValueError('Square matrix required')
    rows=[row[:]+e for row,e in zip(a,eye(n))]
    for j in range(n):
        i=next((i for i in range(j,n) if rows[i][j]),None)
        if i is None:raise ValueError('Singular matrix')
        rows[j],rows[i]=rows[i],rows[j]
        pivot=rows[j][j];rows[j]=[x/pivot for x in rows[j]]
        for i in range(n):
            if i!=j and rows[i][j]:
                c=rows[i][j];rows[i]=[x-c*y for x,y in zip(rows[i],rows[j])]
    return [row[n:] for row in rows]

class Span:
    def __init__(self):self.rows=[]
    def insert(self,v):
        w=list(v)
        for j,row in self.rows:
            if w[j]:
                c=w[j];w=[x-c*y for x,y in zip(w,row)]
        j=next((j for j,x in enumerate(w) if x),None)
        if j is None:return False
        c=w[j];w=[x/c for x in w];self.rows.append((j,w))
        return True

def pinv_psd(a):
    """Support inverse of a PSD matrix by a rational range projector."""
    n=len(a);span=Span();cols=[]
    for j in range(n):
        col=[a[i][j] for i in range(n)]
        if span.insert(col):cols.append(col)
    if not cols:return zero(n),zero(n),0
    c=[list(row) for row in zip(*cols)]
    p=mul(mul(c,inv(mul(adj(c),c))),adj(c))
    inverse=mul(inv(add(a,add(eye(n),scale(-1,p)))),p)
    return inverse,p,len(cols)

def psd(a):
    if not a or any(len(row)!=len(a) for row in a) or a!=adj(a):return False
    n=len(a);rem=[row[:] for row in a]
    while any(flat(rem)):
        if any(rem[i][i].im or rem[i][i].re<0 for i in range(n)):return False
        j=next((i for i in range(n) if rem[i][i].re>0),None)
        if j is None:return False
        d=rem[j][j].re;v=[rem[i][j]/d for i in range(n)]
        rem=[[rem[i][h]-d*v[i]*v[h].conj() for h in range(n)] for i in range(n)]
    return True

def partial(a,left,right,which):
    if which=='right':return [[sum((a[i*right+t][j*right+t] for t in range(right)),Q()) for j in range(left)] for i in range(left)]
    if which=='left':return [[sum((a[t*right+i][t*right+j] for t in range(left)),Q()) for j in range(right)] for i in range(right)]
    raise ValueError('which must be left or right')

def hermitian_basis(a):
    basis=[];labels=[]
    for i in range(a-1):
        h=zero(a);h[i][i]=q(1);h[a-1][a-1]=q(-1)
        basis.append(h);labels.append('Z_%d'%i)
    for i in range(a):
        for j in range(i+1,a):
            h=zero(a);h[i][j]=h[j][i]=q(1)
            basis.append(h);labels.append('X_%d_%d'%(i,j))
            h=zero(a);h[i][j]=Q(F(0),F(-1));h[j][i]=Q(F(0),F(1))
            basis.append(h);labels.append('Y_%d_%d'%(i,j))
    return basis,labels

class Channel:
    def __init__(self,obj):
        self.a=obj['input_dim'];self.b=obj['output_dim']
        a,b=self.a,self.b
        if type(a)!=int or type(b)!=int or min(a,b)<1:raise ValueError('Positive integer dimensions required')
        self.j=mat(obj['choi'])
        if len(self.j)!=a*b or any(len(row)!=a*b for row in self.j):raise ValueError('Choi size mismatch')
        if not psd(self.j):raise ValueError('Choi not positive semidefinite')
        if partial(self.j,a,b,'right')!=eye(a):raise ValueError('Choi not trace preserving')
        self.omega=self.apply(eye(a))
        self.oinv,self.projector,self.rank=pinv_psd(self.omega)
    def apply(self,x,r=1):
        a,b=self.a,self.b;y=zero(b*r)
        for i in range(a):
            for j in range(a):
                for k in range(b):
                    for l in range(b):
                        c=self.j[i*b+k][j*b+l]
                        if c:
                            for p in range(r):
                                for z in range(r):
                                    v=x[i*r+p][j*r+z]
                                    if v:y[k*r+p][l*r+z]=y[k*r+p][l*r+z]+c*v
        return y
    def chi(self,sigma,rho,r):
        rr=self.apply(rho,r);dd=self.apply(add(sigma,scale(-1,rho)),r)
        pp,_,_=pinv_psd(rr)
        return real(tr(mul(mul(dd,pp),dd)))

def from_kraus(ks):
    ks=[mat(k) for k in ks];b=len(ks[0]);a=len(ks[0][0]);j=zero(a*b)
    for k in ks:
        v=[k[y][x] for x in range(a) for y in range(b)]
        j=add(j,[[x*y.conj() for y in v] for x in v])
    return {'input_dim':a,'output_dim':b,'choi':out(j)}

def max_bits(a):
    return max((max(x.re.numerator.bit_length(),x.re.denominator.bit_length(),x.im.numerator.bit_length(),x.im.denominator.bit_length()) for x in flat(a)),default=0)
