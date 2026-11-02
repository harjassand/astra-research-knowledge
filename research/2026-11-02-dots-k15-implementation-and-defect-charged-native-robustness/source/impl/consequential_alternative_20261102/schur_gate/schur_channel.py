"""Exact finite-flag product-Schur reduction, float64 diagnostic implementation.
Uses all histograms and representation multiplicities, never postselection.
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
os.environ.setdefault('OMP_NUM_THREADS','1')
import numpy as np
from scipy.special import comb, gammaln, xlogy
from scipy.linalg import eigvalsh
from itertools import product
import math, time


def weak_compositions(n,b):
    if b==1:
        yield (n,);return
    for k in range(n+1):
        for rest in weak_compositions(n-k,b-1):yield (k,)+rest


def sym_power(M,n):
    """Normalized Dicke matrix of Sym^n M, M shape (...,2,2)."""
    out=np.zeros(M.shape[:-2]+(n+1,n+1),dtype=M.dtype)
    a,b,c,d=M[...,0,0],M[...,0,1],M[...,1,0],M[...,1,1]
    for k in range(n+1):
      for l in range(n+1):
        for x in range(max(0,k-l),min(k,n-l)+1):
          y=k-x
          out[...,k,l]+=math.sqrt(comb(n,l)/comb(n,k))*comb(n-l,x)*comb(l,y)*a**(n-l-x)*c**x*b**(l-y)*d**y
    return out


def pauli_action(M,p):
    """p ordering I,X,Y,Z."""
    I=np.eye(2);X=np.array([[0,1],[1,0]]);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1])
    return sum(q*np.einsum('ab,...bc,cd->...ad',P,M,P.conj().T) for q,P in zip(p,[I,X,Y,Z]))


def entropy(A):
    e=np.linalg.eigvalsh(A); e=np.maximum(e,0)
    return -np.sum(xlogy(e,e),axis=-1)/math.log(2)


class SchurChannel:
  def __init__(self,n,w,paulis, verbose=False):
    self.n=n;self.din=n+1;self.w=np.asarray(w);self.paulis=np.asarray(paulis);self.groups={}
    self.meta=[];start=time.time();N=n+1
    z=np.exp(2j*np.pi*np.arange(N)/N)
    vec=np.stack([np.ones(N),z],axis=1)
    M=vec[:,None,:,None]*vec[None,:,None,:].conj()
    transformed=[pauli_action(M,p) for p in paulis]
    cache={}
    for a,T in enumerate(transformed):
      for size in range(n+1):
        for j in range(size//2+1):
          cache[a,size,j]=np.linalg.det(T)[...,None,None]**j*sym_power(T,size-2*j)
    C=np.sqrt(comb(n,np.arange(N)));denom=N*C[:,None]*C[None,:]
    for hist in weak_compositions(n,len(w)):
      logW=gammaln(n+1)-sum(gammaln(np.array(hist)+1))+np.dot(hist,np.log(w))
      W=math.exp(logW)
      for js in product(*[range(h//2+1) for h in hist]):
        mult=math.prod(int(round(comb(h,j)-comb(h,j-1))) for h,j in zip(hist,js))
        Q=np.ones((N,N,1,1),complex)
        for a,(h,j) in enumerate(zip(hist,js)):
          T=cache[a,h,j]
          Q=np.einsum('ijab,ijcd->ijacbd',Q,T).reshape(N,N,Q.shape[-1]*T.shape[-1],-1)
        T=np.fft.ifft(np.fft.fft(Q,axis=0),axis=1)/denom[:,:,None,None]
        imax=np.max(abs(T.imag))
        if imax>1e-9:raise ValueError(('imaginary transfer',imax))
        T=T.real
        d=T.shape[-1]
        if d not in self.groups:self.groups[d]=[[],[]]
        self.groups[d][0].append(T);self.groups[d][1].append(W*mult)
        self.meta.append((hist,js,d,W,mult))
    for d,(T,c) in self.groups.items():self.groups[d]=(np.array(T),np.array(c))
    self.bytes=sum(T.nbytes+c.nbytes for T,c in self.groups.values())
    if verbose:print('build',n,len(w),'sec',time.time()-start,'blocks',len(self.meta),'MB',self.bytes/1e6,'maxd',max(self.groups),flush=True)

  def coherent(self,A,gradient=False,diagnostics=False):
    """Real or complex purification A (reference, Dicke basis), not automatically normalized.
    Gradient is d/d Re(A) + i d/d Im(A).
    """
    A=np.asarray(A);R=A.shape[0];val=0.;grad=np.zeros_like(A);traceB=0.;mineig=1.
    for d,(T,c) in self.groups.items():
      Y=np.einsum('ak,bl,hklmn->hambn',A,A.conj(),T,optimize=True).reshape(len(c),R*d,R*d)
      X=np.einsum('haman->hmn',Y.reshape(len(c),R,d,R,d))
      if gradient:
        ey,uy=np.linalg.eigh(Y);ex,ux=np.linalg.eigh(X)
        mineig=min(mineig,ey.min(),ex.min())
        eyclip=np.maximum(ey,1e-18);exclip=np.maximum(ex,1e-18)
        val+=np.dot(c,(np.sum(xlogy(np.maximum(ey,0),np.maximum(ey,0)),axis=1)-np.sum(xlogy(np.maximum(ex,0),np.maximum(ex,0)),axis=1))/math.log(2))
        logY=np.einsum('hij,hj,hkj->hik',uy,np.log(eyclip),uy.conj())
        logX=np.einsum('hij,hj,hkj->hik',ux,np.log(exclip),ux.conj())
        G=logY.reshape(len(c),R,d,R,d).transpose(0,1,3,2,4)
        for a in range(R):G[:,a,a]-=logX
        grad+=2*np.einsum('h,habmn,bl,hklmn->ak',c,G,A,T,optimize=True)/math.log(2)
      else:
        val+=np.dot(c,entropy(X)-entropy(Y))
        if diagnostics:mineig=min(mineig,np.linalg.eigvalsh(X).min(),np.linalg.eigvalsh(Y).min())
      traceB+=np.dot(c,np.trace(X,axis1=-2,axis2=-1))
    if diagnostics:return dict(ic=float(val),trace=float(np.real(traceB)),mineig=float(mineig),refeig=np.linalg.eigvalsh(A@A.conj().T).tolist())
    return (val,grad) if gradient else val


def dicke_isometry(n):
    U=np.zeros((2**n,n+1))
    for k in range(2**n):
      h=k.bit_count();U[k,h]=1/math.sqrt(comb(n,h))
    return U


def apply_qubit_channel(mat,p,site,n,R=1):
    # straightforward full matrix for independent validation
    pauli=[np.eye(2),np.array([[0,1],[1,0]]),np.array([[0,-1j],[1j,0]]),np.diag([1,-1])]
    out=np.zeros_like(mat,dtype=complex)
    for prob,P in zip(p,pauli):
      op=np.array([[1.]])
      if R>1:op=np.eye(R)
      for j in range(n):op=np.kron(op,P if j==site else np.eye(2))
      out+=prob*(op@mat@op.conj().T)
    return out


def direct_coherent(n,w,paulis,A):
    U=dicke_isometry(n);psi=(A@U.T).ravel();Y=np.outer(psi,psi.conj());R=A.shape[0];value=0.;trace=0.
    for flags in product(range(len(w)),repeat=n):
      out=Y;prob=1.
      for i,a in enumerate(flags):out=apply_qubit_channel(out,paulis[a],i,n,R);prob*=w[a]
      X=np.einsum('aman->mn',out.reshape(R,2**n,R,2**n))
      value+=prob*(entropy(X)-entropy(out));trace+=prob*np.trace(X).real
    return float(value),float(trace)


if __name__=='__main__':
    rng=np.random.default_rng(10)
    for n in [1,2,3,4]:
      w=np.array([.4,.6]);ps=np.array([[.84,.08,.03,.05],[.5,.2,.2,.1]])
      A=rng.normal(size=(2,n+1));A/=np.linalg.norm(A)
      engine=SchurChannel(n,w,ps,True)
      val,g=engine.coherent(A,True);direct,tr=direct_coherent(n,w,ps,A)
      eps=1e-6;gn=np.empty_like(A)
      for i in range(A.size):
        ep=np.zeros_like(A);ep.ravel()[i]=eps
        gn.ravel()[i]=(engine.coherent(A+ep)-engine.coherent(A-ep))/(2*eps)
      print(n,val,direct,'difference',val-direct,'gradient',np.max(abs(g-gn)),'trace',engine.coherent(A,diagnostics=True),flush=True)
