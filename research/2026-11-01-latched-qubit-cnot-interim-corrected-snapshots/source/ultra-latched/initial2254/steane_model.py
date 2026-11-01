"""Small CSS code and pure stabilizer arithmetic used by the gate controls.

This is a finite [[7,1,3]] fixture, not the asymptotic Tanner family.
Paulis are i**p X**x Z**z, with qubit 0 the least significant bit.
"""
from __future__ import annotations
import numpy as np

HROWS = tuple(sum(1 << j for j in range(7) if ((j+1) >> a) & 1) for a in range(3))
ALL = (1 << 7)-1

def parity(x): return x.bit_count() & 1
def multiply(a,b):
    x,z,p=a; u,v,q=b
    return x^u,z^v,(p+q+2*parity(z&u))%4
def anti(a,b): return parity((a[0]&b[1]) ^ (a[1]&b[0]))
def conjugate_cnot(a,c,t):
    x,z,p=a
    return x ^ (((x>>c)&1)<<t), z ^ (((z>>t)&1)<<c), p
def syndrome(a):
    x,z,_=a
    return sum(parity(x&h)<<j for j,h in enumerate(HROWS)),sum(parity(z&h)<<j for j,h in enumerate(HROWS))
def correction(sx,sz):
    return (0 if sx==0 else 1<<(sx-1)),(0 if sz==0 else 1<<(sz-1)),0
def statevector_pauli(v,a):
    x,z,p=a; j=np.arange(len(v),dtype=np.int64)
    signs=np.array([1-2*parity(int(k)&z) for k in j])
    out=np.empty_like(v);out[j^x]=(1j**p)*signs*v
    return out
def encoder_and_syndrome_unitary():
    enc=np.zeros((128,2),complex)
    words=[0]
    for h in HROWS:words += [w^h for w in words]
    for w in words:enc[w,0]=enc[w^ALL,1]=1/np.sqrt(8)
    basis=np.empty((128,128),complex)
    for sx in range(8):
        for sz in range(8):
            a=correction(sx,sz);s=8*sx+sz
            for q in range(2):basis[:,2*s+q]=statevector_pauli(enc[:,q],a)
    assert np.max(np.abs(basis.conj().T@basis-np.eye(128)))<1e-13
    return enc,basis.conj().T

class Stabilizer:
    def __init__(self,gens):
        self.g=list(gens);self.n=len(self.g)
    def pauli(self,a):
        self.g=[(x,z,(p+2*anti((x,z,p),a))%4) for x,z,p in self.g]
    def cnot(self,c,t):self.g=[conjugate_cnot(a,c,t) for a in self.g]
    def expectation(self,a):
        if any(anti(a,b) for b in self.g):return 0
        # Row reduction on combined x/z bits, retaining exact Pauli phases.
        basis={}
        for b in self.g:
            v=b[0] | (b[1]<<self.n)
            while v:
                j=v.bit_length()-1
                if j not in basis:basis[j]=(v,b);break
                w,c=basis[j];v^=w;b=multiply(b,c)
        v=a[0] | (a[1]<<self.n);b=a
        while v:
            j=v.bit_length()-1
            if j not in basis:raise AssertionError("incomplete pure stabilizer")
            w,c=basis[j];v^=w;b=multiply(b,c)
        assert b[2] in (0,2)
        return 1 if b[2]==0 else -1
    def measure(self,a,rng):
        ids=[j for j,b in enumerate(self.g) if anti(a,b)]
        if not ids:return 0 if self.expectation(a)==1 else 1
        pivot=ids[0];old=self.g[pivot]
        for j in ids[1:]:self.g[j]=multiply(self.g[j],old)
        result=int(rng.integers(2));self.g[pivot]=(a[0],a[1],(a[2]+2*result)%4)
        return result

def choi_stabilizer():
    gs=[]
    for shift in (0,7):
        gs += [(h<<shift,0,0) for h in HROWS]
        gs += [(0,h<<shift,0) for h in HROWS]
    for shift,r in ((0,14),(7,15)):
        gs += [((ALL<<shift)|(1<<r),0,0),(0,(ALL<<shift)|(1<<r),0)]
    assert len(gs)==16
    return Stabilizer(gs)

def recover(s,block,rng):
    sh=7*block
    sx=sum(s.measure((0,h<<sh,0),rng)<<j for j,h in enumerate(HROWS))
    sz=sum(s.measure((h<<sh,0,0),rng)<<j for j,h in enumerate(HROWS))
    x,z,p=correction(sx,sz);s.pauli((x<<sh,z<<sh,p))

def target_choi_generators():
    return [((ALL|(ALL<<7))|(1<<14),0,0),(0,ALL|(1<<14),0),
            ((ALL<<7)|(1<<15),0,0),(0,ALL|(ALL<<7)|(1<<15),0)]

def target_fidelity(s):
    gg=target_choi_generators();total=0
    for mask in range(16):
        a=(0,0,0)
        for j in range(4):
            if (mask>>j)&1:a=multiply(a,gg[j])
        total+=s.expectation(a)
    return total/16
