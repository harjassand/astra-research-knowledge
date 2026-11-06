"""Finite rational primitives and certified elementary functions.

No floating-point computation is used to establish a certificate.
"""
from fractions import Fraction as Q
from math import isqrt


def require(ok,message='Invalid contract or certificate'):
    if not ok:raise ValueError(message)


def ceilq(x):
    x=Q(x);return -(-x.numerator//x.denominator)


def dyadic(x,p):
    x=Q(x)*(1<<p)
    return Q((2*x.numerator+x.denominator)//(2*x.denominator),1<<p)


def down(x,p):
    x=Q(x)*(1<<p);return Q(x.numerator//x.denominator,1<<p)


def up(x,p):
    x=Q(x)*(1<<p);return Q(ceilq(x),1<<p)


def qbits(x):
    x=Q(x);return max(abs(x.numerator).bit_length(),x.denominator.bit_length())


def sqrt_up(x,p=48):
    x=Q(x);require(x>=0)
    j=isqrt((x.numerator<<(2*p))//x.denominator)
    if Q(j*j,1<<(2*p))<x:j+=1
    return Q(j,1<<p)


def encode(x):
    if isinstance(x,Q):return str(x)
    if isinstance(x,C):return [str(x.re),str(x.im)]
    if isinstance(x,list):return [encode(v) for v in x]
    if isinstance(x,dict):return {k:encode(v) for k,v in x.items()}
    return x


class C:
    def __init__(self,re=0,im=0):self.re=Q(re);self.im=Q(im)
    def __add__(self,o):
        if not isinstance(o,C):o=C(o)
        return C(self.re+o.re,self.im+o.im)
    __radd__=__add__
    def __neg__(self):return C(-self.re,-self.im)
    def __sub__(self,o):return self+(-o if isinstance(o,C) else C(-o))
    def __rsub__(self,o):return -self+o
    def __mul__(self,o):
        if not isinstance(o,C):return C(self.re*o,self.im*o)
        return C(self.re*o.re-self.im*o.im,self.re*o.im+self.im*o.re)
    __rmul__=__mul__
    def __truediv__(self,o):
        if not isinstance(o,C):return C(self.re/o,self.im/o)
        d=o.re*o.re+o.im*o.im;require(d!=0,'Singular complex division')
        return C((self.re*o.re+self.im*o.im)/d,(self.im*o.re-self.re*o.im)/d)
    def __bool__(self):return bool(self.re or self.im)
    def norm1(self):return abs(self.re)+abs(self.im)
    def rounded(self,p):return C(dyadic(self.re,p),dyadic(self.im,p))


def inverse(matrix):
    n=len(matrix)
    a=[[v if isinstance(v,C) else C(v) for v in row]+[C(int(i==j)) for j in range(n)]
       for i,row in enumerate(matrix)]
    for j in range(n):
        pivot=next((i for i in range(j,n) if a[i][j]),None)
        require(pivot is not None,'Singular acquired response matrix')
        a[j],a[pivot]=a[pivot],a[j]
        scale=a[j][j];a[j]=[v/scale for v in a[j]]
        for i in range(n):
            if i!=j:
                scale=a[i][j]
                if scale:a[i]=[v-scale*w for v,w in zip(a[i],a[j])]
    return [row[n:] for row in a]


def spectral_bound(matrix):
    """max of row/column absolute sums, with |re|+|im| above |complex|."""
    v=[[x.norm1() if isinstance(x,C) else abs(x) for x in row] for row in matrix]
    return max([sum(row,Q(0)) for row in v]+
               [sum((row[j] for row in v),Q(0)) for j in range(len(v))],default=Q(0))


def psd(matrix):
    """Exact rational PSD check via symmetric Schur elimination."""
    a=[list(map(Q,row)) for row in matrix];n=len(a)
    require(all(len(row)==n for row in a))
    require(all(a[i][j]==a[j][i] for i in range(n) for j in range(n)))
    for k in range(n):
        if a[k][k]<0:return False
        if a[k][k]==0:
            if any(a[k][j]!=0 for j in range(k+1,n)):return False
        else:
            for i in range(k+1,n):
                for j in range(k+1,n):a[i][j]-=a[i][k]*a[k][j]/a[k][k]
    return True


def exp_minus(x,p=80):
    """Dyadic interval containing exp(-x), x>=0; exact alternating series."""
    x=Q(x);require(x>=0)
    m=0;u=x
    while u>Q(1,2):u/=2;m+=1
    work=p+m+8;term=Q(1);s=Q(1);j=0;maxbits=qbits(u)
    while True:
        j+=1;term*=-u/j;s+=term
        next_term=term*(-u)/(j+1)
        maxbits=max(maxbits,qbits(term),qbits(s),qbits(next_term))
        if abs(next_term)<=Q(1,1<<work):
            lo=min(s,s+next_term);hi=max(s,s+next_term);break
    lo,hi=down(lo,work),up(hi,work)
    for _ in range(m):lo=down(lo*lo,work);hi=up(hi*hi,work)
    require(lo>=0)
    return down(lo,p),up(hi,p),{'taylor_terms':j+1,'squarings':m,
                               'series_coefficient_bits_max':maxbits}


def pi_interval(p=120):
    def atan(x):
        total=Q(0);term=x;j=0
        while True:
            value=term/(2*j+1);total+=value
            following=-term*x*x/(2*j+3)
            if abs(following)<Q(1,1<<(p+8)):
                return min(total,total+following),max(total,total+following)
            term*=-x*x;j+=1
    l1,h1=atan(Q(1,5));l2,h2=atan(Q(1,239))
    return down(16*l1-4*h2,p),up(16*h1-4*l2,p)


def sincos(x,pi_bounds,p=80):
    """Rational centres and certified errors, range reduction included."""
    low,high=pi_bounds;mid=(low+high)/2
    k=ceilq(Q(x)/(2*mid)-Q(1,2));z=Q(x)-2*k*mid
    require(abs(z)<4)
    reduction_error=abs(k)*(high-low)
    term=Q(1);cos=Q(1);sin=Q(0);power_error=Q(1)
    j=0;target=Q(1,1<<(p+8));maxbits=qbits(z)
    while True:
        j+=1;term*=z/j
        if j%4==0:cos+=term
        elif j%4==1:sin+=term
        elif j%4==2:cos-=term
        else:sin-=term
        power_error=abs(term*z/(j+1))
        maxbits=max(maxbits,qbits(term),qbits(sin),qbits(cos),qbits(power_error))
        if j>8 and power_error<target:break
    # Taylor's real-variable Lagrange remainder bounds both sin and cos.
    error=up(power_error+reduction_error+Q(1,1<<(p+1)),p)
    return dyadic(sin,p),dyadic(cos,p),error,{'taylor_terms':j+1,'range_cycles':k,
                                           'series_coefficient_bits_max':maxbits}
