"""Exact full-field syndrome decoder: BM, Chien, Forney, explicit zero point.
No q-by-q multiplication table. CSS readout uses classical FFT/transpose FFT.
"""
import numpy as np,math,json,time,random,resource,hashlib
from pathlib import Path
from received_additive_fft import Compiler
from received_grs_wrapper_v1 import GF,decode_syndrome
HERE=Path(__file__).parent
class Field:
 def __init__(self,h,mod):
  assert 2<=h<=16, "uint16 field implementation supports h=2..16"
  self.h=h;self.q=1<<h;self.order=self.q-1;g=GF(h,mod)
  primes=[p for p in range(2,self.order+1) if self.order%p==0 and all(p%d for d in range(2,math.isqrt(p)+1))]
  self.generator=next(a for a in range(2,self.q) if all(g.pow(a,self.order//p)!=1 for p in primes))
  self.log=np.zeros(self.q,np.int32);ex=[];x=1
  for i in range(self.order):ex.append(x);self.log[x]=i;x=g.mul(x,self.generator)
  assert x==1 and len(set(ex))==self.order
  self.exp=np.array(ex+ex,np.uint16);self.phase_codes=np.zeros(self.q,np.uint16)
  for j in range(h):
   mask=0
   for k in range(h):
    z=g.mul(1<<j,1<<k);tr=0
    for _ in range(h):tr^=z;z=g.mul(z,z)
    assert tr in [0,1];mask|=tr<<k
   self.phase_codes[1<<j]=mask
  for v in range(1,self.q):
   low=v&-v
   if v!=low:self.phase_codes[v]=self.phase_codes[low]^self.phase_codes[v^low]
  assert len(set(map(int,self.phase_codes)))==self.q
  self.phase_decode=np.zeros(self.q,np.uint16);self.phase_decode[self.phase_codes]=np.arange(self.q,dtype=np.uint16)
  self.elements=np.arange(1,self.q,dtype=np.uint16);self.inverses=self.exp[self.order-self.log[self.elements]]
 def mul(self,a,b):return 0 if not a or not b else int(self.exp[int(self.log[a])+int(self.log[b])])
 def div(self,a,b):
  if not b:raise ZeroDivisionError
  return 0 if not a else int(self.exp[(int(self.log[a])-int(self.log[b]))%self.order])
 def vmul(self,a,b):
  a=np.asarray(a,dtype=np.uint16);b=np.asarray(b,dtype=np.uint16);return np.where((a!=0)&(b!=0),self.exp[self.log[a]+self.log[b]],0).astype(np.uint16)
 def vdiv(self,a,b):
  a=np.asarray(a,dtype=np.uint16);b=np.asarray(b,dtype=np.uint16)
  if np.any(b==0):raise ZeroDivisionError
  return np.where(a!=0,self.exp[(self.log[a]-self.log[b])%self.order],0).astype(np.uint16)
 def dot(self,a,b):return int(np.bitwise_xor.reduce(self.vmul(a,b),initial=np.uint16(0)))
 def eval(self,coeff,x):
  y=np.zeros_like(np.asarray(x,dtype=np.uint16))
  for a in reversed(coeff):y=self.vmul(y,x)^int(a)
  return y
 def bm(self,seq):
  seq=np.array(seq,np.uint16);N=len(seq);C=np.zeros(N+1,np.uint16);B=C.copy();C[0]=B[0]=1;L=0;m=1;b=1
  for n in range(N):
   dis=int(seq[n])^self.dot(C[1:L+1],seq[n-L:n][::-1])
   if dis==0:m+=1;continue
   T=C.copy();coef=self.div(dis,b);C[m:]^=self.vmul(coef,B[:-m])
   if 2*L<=n:L=n+1-L;B=T;b=dis;m=1
   else:m+=1
  return C[:L+1],L
 def moments(self,error,count):
  loc=np.flatnonzero(error);amp=np.asarray(error,dtype=np.uint16)[loc];powers=np.ones(len(loc),np.uint16);out=[]
  for j in range(count):out.append(self.dot(amp,powers));powers=self.vmul(powers,loc)
  return np.array(out,np.uint16)
 def candidate(self,seq,limit):
  C,L=self.bm(seq)
  if L>limit:return None,{'reason':'locator_degree','L':L}
  roots=np.flatnonzero(self.eval(C,self.inverses)==0);nodes=self.elements[roots];z=self.inverses[roots]
  if len(nodes)!=L:return None,{'reason':'root_count','L':L,'roots':len(nodes)}
  if L==0:return (nodes,np.array([],np.uint16)),{'L':0}
  omega=np.zeros(L,np.uint16)
  for j in range(L):omega[j:]^=self.vmul(C[j],np.asarray(seq[:L-j],np.uint16))
  derivative=np.array([int(C[j+1]) if (j+1)%2 else 0 for j in range(L)],np.uint16)
  denom=self.eval(derivative,z)
  if np.any(denom==0):return None,{'reason':'repeated_root'}
  weights=self.vdiv(self.vmul(nodes,self.eval(omega,z)),denom)
  return (nodes,weights),{'L':L}
 def decode(self,S,t):
  S=np.asarray(S,np.uint16);assert len(S)==2*t;attempts=[]
  for shifted in [False,True]:
   candidate,detail=self.candidate(S[1:] if shifted else S,t-1 if shifted else t);detail['shifted']=shifted;attempts.append(detail)
   if candidate is None:continue
   loc,amp=candidate
   if shifted:amp=self.vdiv(amp,loc)
   e=np.zeros(self.q,np.uint16);e[loc]=amp
   if shifted:e[0]=int(S[0])^int(np.bitwise_xor.reduce(amp,initial=np.uint16(0)))
   if np.count_nonzero(e)<=t and np.array_equal(self.moments(e,2*t),S):return e,True,{'case':'zero_possible' if shifted else 'zero_absent','attempts':attempts}
  return np.zeros(self.q,np.uint16),False,{'case':'fallback','attempts':attempts}
class ClassicalFFT:
 def __init__(self,f):
  self.f=f;self.h=f.h;self.q=f.q;sv=np.arange(f.q,dtype=np.uint16);ts=[]
  for j in range(f.h):
   c=int(sv[1<<j]);ts.append(f.vdiv(sv,c));sv=f.vmul(sv,sv)^f.vmul(c,sv)
  self.field=[]
  def visit(j,start,alpha):
   if j<0:return
   half=1<<j;c=int(ts[j][alpha])
   for i in range(half):
    a=start+i;b=start+half+i
    if c:self.field.append((b,a,c))
    self.field.append((a,b,1))
   visit(j-1,start,alpha);visit(j-1,start+half,alpha^(1<<j))
  visit(f.h-1,0,0)
 def apply(self,x,inverse=False):
  x=list(map(int,x))
  for src,dst,c in reversed(self.field) if inverse else self.field:x[dst]^=self.f.mul(c,x[src])
  return x
class CSSDecoder:
 def __init__(self,h,mod,t):
  assert 1<=t and 4*t<(1<<h)
  self.f=Field(h,mod);self.h=h;self.q=1<<h;self.t=t;self.s=2*t;self.c=ClassicalFFT(self.f)
  # Known classical degree-triangular novel-polynomial coefficient matrix.
  f=self.f;sp=np.array([0,1],np.uint16);tp=[]
  for j in range(h):
   den=int(f.eval(sp,np.uint16(1<<j)));tp.append(f.vdiv(sp,den));nxt=np.zeros(2*len(sp)-1,np.uint16);nxt[::2]=f.vmul(sp,sp);nxt[:len(sp)]^=f.vmul(den,sp);sp=nxt
  basis=[np.array([1],np.uint16)]
  for i in range(1,self.s):
   bit=i&-i;j=bit.bit_length()-1;A=basis[i-bit];B=tp[j];C=np.zeros(len(A)+len(B)-1,np.uint16)
   for k in np.flatnonzero(B):C[k:k+len(A)]^=f.vmul(B[k],A)
   basis.append(C)
  self.L=np.zeros((self.s,self.s),np.uint16)
  for i,v in enumerate(basis):self.L[i,:len(v)]=v;assert self.L[i,i]
 def transpose_fft(self,x):
  x=list(map(int,x))
  for src,dst,c in reversed(self.c.field):x[src]^=self.f.mul(c,x[dst])
  return np.array(x,np.uint16)
 def mono_from_novel(self,Y):
  x=np.zeros(self.s,np.uint16)
  for i in range(self.s):x[i]=self.f.div(int(Y[i])^self.f.dot(self.L[i,:i],x[:i]),int(self.L[i,i]))
  return x
 def actual_readout(self,e,f):
  # Same exact field map as already-checked binary CNOT and trace-dual readout.
  ep=np.array(self.c.apply(list(map(int,e)),True),np.uint16);fp=self.transpose_fft(f)
  return ep[-self.s:],self.f.phase_codes[fp[:self.s]]
 def decode_readout(self,last_X,first_phase_bits):
  first_phase_field=self.f.phase_decode[np.asarray(first_phase_bits,np.uint16)]
  v=np.zeros(self.q,np.uint16);v[-self.s:]=last_X
  canonical=np.array(self.c.apply(list(map(int,v))),np.uint16)
  Xnovel=self.transpose_fft(canonical)[:self.s]
  SX=self.mono_from_novel(Xnovel);SZ=self.mono_from_novel(first_phase_field)
  ex,okx,dx=self.f.decode(SX,self.t);fz,okz,dz=self.f.decode(SZ,self.t)
  ok=okx and okz and np.count_nonzero(ex|fz)<=self.t
  return ex,fz,ok,{'X':dx,'Z':dz}
 def logical_correction_bits(self,ex,fz):
  ep=np.array(self.c.apply(list(map(int,ex)),True),np.uint16);fp=self.transpose_fft(fz)
  return ep[self.s:-self.s],self.f.phase_codes[fp[self.s:-self.s]]
