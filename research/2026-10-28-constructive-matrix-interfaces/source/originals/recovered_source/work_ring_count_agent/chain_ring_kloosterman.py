#!/usr/bin/env python3
"""Exact sums over F_(2^d)[t]/t^e; no field/ring point enumeration.
Established stationary-phase ancestry: Sawin, arXiv:2209.02170. This
implementation uses the elementary proof in CHAIN_RING_COUNTER.md and does
not rely on that paper's magnitude bounds. Exhaustive oracles are separate.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'work_field_root'))
from field_kloosterman import gf_mul,gf_pow,gf_trace,irreducible_binary,kloosterman_dwork

class ChainRing:
    def __init__(self,h,e):
        if not irreducible_binary(h): raise ValueError('field modulus is not irreducible')
        if not isinstance(e,int) or e<1: raise ValueError('positive chain length required')
        self.h,self.e=h,e; self.d=h.bit_length()-1; self.q=1<<self.d
        self.zero=(0,)*e; self.one=(1,)+(0,)*(e-1)
    def element(self,a):
        a=tuple(a)
        if len(a)!=self.e or any(not isinstance(x,int) or not 0<=x<self.q for x in a):
            raise ValueError('ring coefficient vector has wrong shape or range')
        return a
    def add(self,*vectors):
        out=[0]*self.e
        for v in vectors:
            for i,x in enumerate(v[:self.e]): out[i]^=x
        return tuple(out)
    def mul(self,a,b):
        out=[0]*self.e
        for i,ai in enumerate(a[:self.e]):
            if ai:
                for j,bj in enumerate(b[:self.e-i]):
                    if bj: out[i+j]^=gf_mul(ai,bj,self.h)
        return tuple(out)
    def inv(self,a):
        if not a or not a[0]: raise ValueError('inverse requires a unit')
        out=[gf_pow(a[0],self.q-2,self.h)]+[0]*(self.e-1)
        for i in range(1,self.e):
            v=0
            for j in range(1,i+1):
                if j<len(a): v^=gf_mul(a[j],out[i-j],self.h)
            out[i]=gf_mul(out[0],v,self.h)
        return tuple(out)
    def sqrt_field(self,a): return gf_pow(a,self.q//2,self.h)
    def bit(self,a): return gf_trace(a[self.e-1],self.h)
    def psi(self,a): return 1-2*self.bit(a)
    def valuation(self,a): return next((i for i,x in enumerate(a) if x),self.e)
    def packed(self,num): return tuple((num>>(self.d*i))&(self.q-1) for i in range(self.e))

def quadratic_sum(value,n):
    """Exact Walsh sum of known quadratic value function, no truth table."""
    constant=value(0); singles=[value(1<<i)^constant for i in range(n)]
    poly={0} if constant else set()
    poly.update(1<<i for i,x in enumerate(singles) if x)
    for i in range(n):
        for j in range(i+1,n):
            if value((1<<i)|(1<<j))^singles[i]^singles[j]^constant: poly.add((1<<i)|(1<<j))
    remaining=set(range(n)); multiplier=1
    while True:
        pair=next((m for m in poly if m.bit_count()==2),None)
        if pair is None:
            if any(poly): return 0
            return multiplier*(-1 if 0 in poly else 1)*(1<<len(remaining))
        i,j=[v for v in remaining if pair>>v&1]
        A={m^(1<<i) for m in poly if m>>i&1 and not (m>>j&1)}
        B={m^(1<<j) for m in poly if m>>j&1 and not (m>>i&1)}
        poly={m for m in poly if not m&pair}
        for x in A:
            for y in B:
                m=x|y
                if m in poly: poly.remove(m)
                else: poly.add(m)
        remaining.remove(i); remaining.remove(j); multiplier*=2

def unit_kloosterman(R,u,*,details=False):
    """K_e(1,u), u a unit. Polynomial in e,d, no enumeration."""
    u=R.element(u)
    if not u[0]: raise ValueError('normalized Kloosterman parameter must be a unit')
    if R.e==1:
        answer,evidence=kloosterman_dwork(u[0],R.h,use_hasse=True)
        data=dict(method='field Dwork',**evidence)
        return (answer,data) if details else answer
    e=R.e; c=(e+2)//3; z=(e+1)//3
    a=[R.sqrt_field(u[0])]+[0]*(e-1)
    def derivatives(center):
        inverse=R.inv(center); square=R.mul(inverse,inverse)
        U=R.add(R.one,R.mul(u,square)); V=R.mul(u,R.mul(square,inverse))
        return U,V
    for j in range(1,z):
        U,V=derivatives(a); vi=4*j-e+1
        target=U[2*j]^(R.sqrt_field(V[vi]) if vi>=0 else 0)
        a[j]=gf_mul(a[0],R.sqrt_field(target),R.h)
    U,V=derivatives(a); failures=[]
    for i in range(e-c):
        vi=2*i-e+1
        if U[i]^(R.sqrt_field(V[vi]) if vi>=0 else 0): failures.append(i)
    data=dict(method='coefficient stationary phase',length=e,residue_degree=R.d,
              deep_ideal=c,center_length=z,center=a[:z],failed_equations=failures,
              field_points_enumerated=0,ring_points_enumerated=0)
    if failures: return (0,data) if details else 0
    phase=R.psi(R.add(a,R.mul(u,R.inv(a))))
    if c==z:
        result=phase*pow(R.q,e-c); data['quadratic_dimension']=0
    else:
        beta=U[2*z]^R.sqrt_field(V[z])
        gamma=gf_pow(gf_mul(a[0],a[0],R.h),R.q-2,R.h)
        def value(x):
            cube=gf_mul(gf_mul(x,x,R.h),x,R.h)
            return gf_trace(gf_mul(gamma,cube,R.h)^gf_mul(beta,x,R.h),R.h)
        gauss=quadratic_sum(value,R.d); result=phase*pow(R.q,e-c)*gauss
        data.update(quadratic_dimension=R.d,quadratic_sum=gauss,
                    cubic_coefficient=gamma,linear_coefficient=beta)
    return (result,data) if details else result

def kloosterman(R,A,D):
    A,D=R.element(A),R.element(D); s=min(R.valuation(A),R.valuation(D))
    if s==R.e: return (R.q-1)*pow(R.q,R.e-1)
    if s:
        small=ChainRing(R.h,R.e-s)
        return pow(R.q,s)*kloosterman(small,A[s:],D[s:])
    if R.e==1 and (not A[0] or not D[0]): return -1
    if not A[0] or not D[0]: return 0
    return unit_kloosterman(R,R.mul(A,D))

def product_fiber_sum(R,a,b,c):
    """Sum_(xy=c) psi(ax+by), arbitrary parameters including zeros."""
    a,b,c=R.element(a),R.element(b),R.element(c)
    vb,vc=R.valuation(b),R.valuation(c)
    total=pow(R.q,R.e) if vb==vc==R.e else 0
    for k in range(min(vb,vc,R.e-1)+1):
        small=ChainRing(R.h,R.e-k); D=small.mul(b[k:],c[k:])
        total+=pow(R.q,k)*kloosterman(small,a[:R.e-k],D)
    return total

def cubic_sum(R,lam,A,B,C,D,E,F,G):
    """Sum psi(lam xyz+Axy+Bxz+Cyz+Dx+Ey+Fz+G); lam unit."""
    lam,A,B,C,D,E,F,G=[R.element(x) for x in (lam,A,B,C,D,E,F,G)]
    inv_lam=R.inv(lam); B,C,F=[R.mul(x,inv_lam) for x in (B,C,F)]
    a=R.add(D,R.mul(A,B)); b=R.add(E,R.mul(A,C)); c=R.add(F,R.mul(B,C))
    g=R.add(G,R.mul(D,C),R.mul(E,B),R.mul(F,A))
    return pow(R.q,R.e)*R.psi(g)*product_fiber_sum(R,a,b,c)
