"""Exact Q[sqrt(delta)] etale algebra and fixed-degree finite fields.
No floating arithmetic, general algebraic-compositum package or hidden roots.
"""
from fractions import Fraction as Q
from math import isqrt

class Degenerate(ValueError):pass

class Rational:
    zero=Q(0);one=Q(1)
    def embed(self,x):return Q(x)
    def add(self,a,b):return a+b
    def sub(self,a,b):return a-b
    def neg(self,a):return -a
    def mul(self,a,b):return a*b
    def inv(self,a):
        if not a:raise Degenerate('zero rational denominator')
        return 1/a
    def div(self,a,b):return self.mul(a,self.inv(b))

class Prime:
    def __init__(self,p):self.p=p;self.zero=0;self.one=1
    def embed(self,x):return int(x)%self.p
    def add(self,a,b):return (a+b)%self.p
    def sub(self,a,b):return (a-b)%self.p
    def neg(self,a):return -a%self.p
    def mul(self,a,b):return a*b%self.p
    def inv(self,a):
        if not a:raise Degenerate('zero prime denominator')
        return pow(a,-1,self.p)
    def div(self,a,b):return a*self.inv(b)%self.p

class Quadratic:
    def __init__(self,delta):
        self.delta=Q(delta)
        if not self.delta:raise Degenerate('zero quadratic discriminant')
        self.zero=(Q(0),Q(0));self.one=(Q(1),Q(0))
    def embed(self,x):return (Q(x),Q(0))
    def add(self,a,b):return (a[0]+b[0],a[1]+b[1])
    def sub(self,a,b):return (a[0]-b[0],a[1]-b[1])
    def neg(self,a):return (-a[0],-a[1])
    def mul(self,a,b):return (a[0]*b[0]+self.delta*a[1]*b[1],a[0]*b[1]+a[1]*b[0])
    def norm(self,a):return a[0]*a[0]-self.delta*a[1]*a[1]
    def inv(self,a):
        n=self.norm(a)
        if not n:raise Degenerate('zero etale norm')
        return (a[0]/n,-a[1]/n)
    def div(self,a,b):return self.mul(a,self.inv(b))
    def sqrt_base(self,d):
        if Q(d)!=self.delta:raise ValueError('wrong formal discriminant')
        return (Q(0),Q(1))

class Quartic:
    """Fp[t,u]/(t^2-nu,u^2-kappa), always a FIELD of degree4.

    Nonresidues found by deterministic scans. Cost may be O(p) candidate tests;
    no uniform polynomial-in-log(p) setup claim is made for these scans.
    """
    zero=(0,0,0,0);one=(1,0,0,0)
    def __init__(self,p):
        if p<=3 or not is_prime(p):raise ValueError('verified odd prime>3 required')
        self.p=p
        self.nu=next(a for a in range(2,p) if pow(a,(p-1)//2,p)==p-1)
        self.kappa=next((a,1) for a in range(p) if self.pow2((a,1),(p*p-1)//2)==(p-1,0))
    def embed(self,x):return (int(x)%self.p,0,0,0)
    def add2(self,a,b):return ((a[0]+b[0])%self.p,(a[1]+b[1])%self.p)
    def neg2(self,a):return (-a[0]%self.p,-a[1]%self.p)
    def sub2(self,a,b):return ((a[0]-b[0])%self.p,(a[1]-b[1])%self.p)
    def mul2(self,a,b):
        p=self.p;ac=a[0]*b[0];bd=a[1]*b[1]
        return ((ac+self.nu*bd)%p,((a[0]+a[1])*(b[0]+b[1])-ac-bd)%p)
    def inv2(self,a):
        p=self.p;n=(a[0]*a[0]-self.nu*a[1]*a[1])%p
        if not n:raise Degenerate('zero Fp2 denominator')
        k=pow(n,-1,p);return (a[0]*k%p,-a[1]*k%p)
    def pow2(self,a,n):
        out=(1,0)
        while n:
            if n&1:out=self.mul2(out,a)
            a=self.mul2(a,a);n>>=1
        return out
    def sqrt2(self,a):
        if a==(0,0):return a
        q=self.p*self.p
        if self.pow2(a,(q-1)//2)!=(1,0):raise Degenerate('not square in Fp2')
        t=q-1;s=0
        while t%2==0:t//=2;s+=1
        c=self.pow2(self.kappa,t);x=self.pow2(a,(t+1)//2);b=self.pow2(a,t);m=s
        while b!=(1,0):
            i=0;y=b
            while y!=(1,0) and i<m:y=self.mul2(y,y);i+=1
            if i>=m:raise ArithmeticError('Tonelli-Shanks invariant failed')
            d=self.pow2(c,1<<(m-i-1));x=self.mul2(x,d);c=self.mul2(d,d);b=self.mul2(b,c);m=i
        if self.mul2(x,x)!=a:raise ArithmeticError('invalid Fp2 square root')
        return x
    def add(self,a,b):return tuple((x+y)%self.p for x,y in zip(a,b))
    def sub(self,a,b):return tuple((x-y)%self.p for x,y in zip(a,b))
    def neg(self,a):return tuple(-x%self.p for x in a)
    def mul(self,a,b):
        ac=self.mul2(a[:2],b[:2]);bd=self.mul2(a[2:],b[2:])
        cross=self.sub2(self.sub2(self.mul2(self.add2(a[:2],a[2:]),self.add2(b[:2],b[2:])),ac),bd)
        return self.add2(ac,self.mul2(self.kappa,bd))+cross
    def inv(self,a):
        den=self.sub2(self.mul2(a[:2],a[:2]),self.mul2(self.kappa,self.mul2(a[2:],a[2:])))
        d=self.inv2(den);return self.mul2(a[:2],d)+self.neg2(self.mul2(a[2:],d))
    def div(self,a,b):return self.mul(a,self.inv(b))
    def pow(self,a,n):
        out=self.one
        while n:
            if n&1:out=self.mul(out,a)
            a=self.mul(a,a);n>>=1
        return out
    def sqrt_f2(self,a):
        if a[2:]!=(0,0):raise ValueError('Fp2 radicand required')
        r=a[:2]
        if r==(0,0):return self.zero
        if self.pow2(r,(self.p*self.p-1)//2)==(1,0):ans=self.sqrt2(r)+(0,0)
        else:ans=(0,0)+self.sqrt2(self.mul2(r,self.inv2(self.kappa)))
        if self.mul(ans,ans)!=a:raise ArithmeticError('invalid quartic root')
        return ans
    def sqrt_base(self,d):return self.sqrt_f2(self.embed(d))
    def base_value(self,a):
        if a[1:]!=(0,0,0):raise Degenerate('output did not cancel to original Fp subfield')
        return a[0]

def is_prime(n):
    if n<2:return False
    if n%2==0:return n==2
    return all(n%d for d in range(3,isqrt(n)+1,2))

def primes():
    n=5
    while True:
        if is_prime(n):yield n
        n+=2

class QuadraticFinite(Quartic):
    """Actual compiler field Fp2. Quartic prototype is retained above, unused.
    sqrt2 uses the same-field nonresidue kappa, with exact Tonelli-Shanks.
    """
    zero=(0,0);one=(1,0)
    def embed(self,x):return (int(x)%self.p,0)
    def add(self,a,b):return self.add2(a,b)
    def sub(self,a,b):return self.sub2(a,b)
    def neg(self,a):return self.neg2(a)
    def mul(self,a,b):return self.mul2(a,b)
    def inv(self,a):return self.inv2(a)
    def div(self,a,b):return self.mul2(a,self.inv2(b))
    def pow(self,a,n):return self.pow2(a,n)
    def sqrt_base(self,d):return self.sqrt2(self.embed(d))
    def sqrt_f2(self,a):return self.sqrt2(a)
    def base_value(self,a):
        if a[1]:raise Degenerate('output failed to cancel to original Fp')
        return a[0]
