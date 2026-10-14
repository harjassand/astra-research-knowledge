"""Exact local-response acquisition for a reversible Ising ring.
No equilibrium samples, full-chain state vector, or hidden transition-rate oracle.
"""
from __future__ import annotations
from fractions import Fraction as F
from functools import lru_cache
from math import comb
import time, json
import sympy as sp


def mm(A,B):
    return tuple(tuple(sum(A[i][k]*B[k][j] for k in range(2)) for j in range(2)) for i in range(2))
def mpow(A,n):
    O=((F(1),F(0)),(F(0),F(1)))
    while n:
        if n&1: O=mm(O,A)
        A=mm(A,A); n//=2
    return O

def sf(x): return sp.Rational(x.numerator,x.denominator)
def ff(x): return F(int(x.p),int(x.q))

class Ring:
    def __init__(self,n:int,r:F,t:F,nu:F=F(1),kappa:F=F(1)):
        if n<3 or r<=0 or t<1 or nu<=0 or kappa<=0: raise ValueError('invalid parameters')
        self.n=n; self.r=F(r); self.t=F(t); self.nu=F(nu); self.kappa=F(kappa)
        self.T=tuple(tuple(self.r**b*self.t**int(a==b) for b in range(2)) for a in range(2))
        Zmat=mpow(self.T,n); self.Z=Zmat[0][0]+Zmat[1][1]
        self._marg={}; self.p=self.marginal(1)[1]
        self.q={}
        for a in range(2):
            for b in range(2):
                R=self.r*self.t**(2*(a+b)-2)
                self.q[(a,0,b)]=self.nu*R/(1+R)
                self.q[(a,1,b)]=self.nu/(1+R)
        c=max(abs(self.q[(1,0,b)]-self.q[(0,0,b)])/self.nu for b in range(2))
        self.dobrushin=max(F(0),self.nu*(1-2*c))
        self.gap=self.dobrushin
        # No unproved fallback spectral bound. Moment certification requires gap>0.
    def marginal(self,m):
        if m>self.n: raise ValueError('local support exceeds full ring')
        if m in self._marg: return self._marg[m]
        P=mpow(self.T,self.n-m+1)
        out=[]
        for s in range(1<<m):
            bits=[(s>>i)&1 for i in range(m)]
            w=P[bits[-1]][bits[0]]
            for i in range(m-1): w*=self.T[bits[i]][bits[i+1]]
            out.append(w/self.Z)
        assert sum(out)==1
        self._marg[m]=out
        return out
    def avg(self,v):
        m=(len(v)-1).bit_length()
        return sum(a*b for a,b in zip(v,self.marginal(m)))
    def K_extend(self,v):
        m=(len(v)-1).bit_length(); mask=(1<<m)-1
        if m+2>self.n: raise ValueError('too large local support')
        out=[]
        for s in range(1<<(m+2)):
            middle=(s>>1)&mask
            val=self.kappa*((middle>>(m//2))&1)*v[middle]
            for j in range(m):
                a=(s>>j)&1; b=(s>>(j+1))&1; c=(s>>(j+2))&1
                val+=self.q[(a,b,c)]*(v[middle]-v[middle^(1<<j)])
            out.append(val)
        return out
    def moments(self,order):
        v=[-self.kappa*self.p,self.kappa*(1-self.p)]
        moments=[]
        for j in range(order+1):
            moments.append(self.avg([x*x for x in v]))
            if j==order: break
            w=self.K_extend(v); mean=self.avg(w)
            cv=[x-mean for x in w]
            m=(len(v)-1).bit_length(); mask=(1<<m)-1
            odd=self.avg([v[(s>>1)&mask]*cv[s] for s in range(len(cv))])
            moments.append(odd)
            v=cv
            assert self.avg(v)==0
        return moments,v

def inverse_bounds(m,gap,k):
    """Gauss lower and left-Radau upper, exact rational arithmetic."""
    if gap<=0: raise ValueError("no acquired positive spectral bound")
    A=sp.Matrix(k,k,lambda i,j: sf(m[i+j+1]))
    b=sp.Matrix([sf(m[i]) for i in range(k)])
    lo=ff((b.T*A.inv()*b)[0])
    Ag=sp.Matrix(k,k,lambda i,j: sf(m[i+j+2]-gap*m[i+j+1]))
    bg=sp.Matrix([sf(m[i+1]-gap*m[i]) for i in range(k)])
    up=(m[0]-ff((bg.T*Ag.inv()*bg)[0]))/gap
    if up<lo or lo<0: raise AssertionError('invalid inverse interval')
    return lo,up

def run(n,r,t,order=4,nu=F(1),kappa=F(1)):
    start=time.perf_counter(); R=Ring(n,F(r),F(t),F(nu),F(kappa)); acquired=time.perf_counter()
    moments,_=R.moments(order); mt=time.perf_counter()
    out={'n':n,'r':str(r),'t':str(t),'nu':str(nu),'kappa':str(kappa),'p':float(R.p),'gap':float(R.gap),
         'construction_s':acquired-start,'moments_s':mt-acquired,'orders':[],'local_max_states':1<<(2*order+1)}
    mu=R.kappa*R.p
    for k in range(1,order+1):
        a,b=inverse_bounds(moments,R.gap,k)
        lo=1/(mu-a)
        upper=1/(mu-b) if b<mu else None
        row={'k':k,'chi_lo':float(a/mu),'chi_hi':float(b/mu),'tau_lo':float(lo),'tau_hi':float(upper) if upper else None,
             'ratio':float(upper/lo) if upper else None}
        if upper:
            row['closed_lo']=float((lo-1/R.kappa)/(1-R.p)); row['closed_hi']=float((upper-1/R.kappa)/(1-R.p))
        out['orders'].append(row)
    out['total_s']=time.perf_counter()-start
    return out,R,moments

if __name__=='__main__':
    for r,t in [(F(1,1000000),F(2)),(F(1,9),F(2)),(F(1),F(2)),(F(1),F(10)),(F(1),F(100))]:
        ans,_,_=run(32,r,t,4)
        print(json.dumps(ans),flush=True)
