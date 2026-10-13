"""Compiled implementation of the same finite translation-orbit Pauli algebra."""
import numpy as np
import scipy.sparse as sp
from numba import njit
B=28
MASK=(1<<B)-1
@njit(cache=True)
def pc(x):
    n=0
    while x:
        n+=1;x&=x-1
    return n
@njit(cache=True)
def bitlen(x):
    n=0
    while x:n+=1;x>>=1
    return n
@njit(cache=True)
def rev(x,l):
    y=0
    for i in range(l):y=(y<<1)|(x&1);x>>=1
    return y
@njit(cache=True)
def ckey(x,z):
    u=x|z
    while (u&1)==0:
        x>>=1;z>>=1;u>>=1
    l=bitlen(u)
    key=(x<<B)|z;rkey=(rev(x,l)<<B)|rev(z,l)
    if key==rkey:return key,0
    return (key,1) if key<rkey else (rkey,-1)
@njit(cache=True)
def _basis(L,parity):
    keys=[]
    for ell in range(2,L+1):
      for x in range(1<<ell):
        if pc(x)%2:continue
        for z in range(1<<ell):
          if (x|z)&1==0 or (x|z)&(1<<(ell-1))==0:continue
          if pc(x&z)%2!=parity or pc(z)%2!=1:continue
          key=(x<<B)|z;rkey=(rev(x,ell)<<B)|rev(z,ell)
          if key<rkey:keys.append(key)
    return np.array(keys,dtype=np.int64)
def basis(L,parity):
    keys=_basis(L,parity)
    return sorted([(int(k)>>B,int(k)&MASK) for k in keys],key=lambda w:((w[0]|w[1]).bit_length(),w))
@njit(cache=True)
def _entries(words,t,U,V):
    N=len(words);L=0
    for j in range(N):L=max(L,bitlen(words[j,0]|words[j,1]))
    cap=N*4*(L+3)
    rr=np.empty(cap,np.int64);cc=np.empty(cap,np.int32);vv=np.empty(cap,np.float64);k=0
    aa0=np.array([3,3,0,0]);bb0=np.array([0,3,3,5]);hh=np.array([-t/2,-t/2,U/4,V/4]);ranges=np.array([1,1,1,2])
    for j in range(N):
      x0,z0=words[j];ell=bitlen(x0|z0);x=x0<<2;z=z0<<2
      for term in range(4):
        h=hh[term]
        if h==0:continue
        for shift in range(2-ranges[term],ell+2):
          a=aa0[term]<<shift;b=bb0[term]<<shift
          if (pc(a&z)+pc(b&x))%2==0:continue
          xx=x^a;zz=z^b
          exp=(pc(a&b)+pc(x&z)-pc(xx&zz)+2*pc(b&x))%4
          sig=1 if exp==1 else -1
          key,s=ckey(xx,zz)
          if s:
            rr[k]=key;cc[k]=j;vv[k]=s*2*h*sig;k+=1
    return rr[:k],cc[:k],vv[:k]
def build(words,t,U,V):
    if any((int(x)|int(z)).bit_length()>B-2 for x,z in words):
        raise ValueError("Pauli word exceeds collision-free packed-key range")
    keys,cols,vals=_entries(np.asarray(words,dtype=np.int64),t,U,V)
    rowsk,inds=np.unique(keys,return_inverse=True)
    mat=sp.csc_matrix((vals,(inds,cols)),shape=(len(rowsk),len(words)))
    mat.sum_duplicates();mat.eliminate_zeros()
    rows=[(int(k)>>B,int(k)&MASK) for k in rowsk]
    return rows,mat
