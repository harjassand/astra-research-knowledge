"""Finite Monte Carlo check of the bosonic virtual-word identity.
Not certified arithmetic or a compiled quantum algorithm.
"""
import json,math
import numpy as np
from scipy.linalg import expm
from scipy.special import gammaln,logsumexp

rng=np.random.default_rng(310652)
I=np.eye(2,dtype=complex);Y=np.array([[0,-1j],[1j,0]],complex)
C=np.array([[0,1],[0,0]],complex);L=3;T=.6;omega=.4;Gamma=.3;samples=3000
def drift(t):return np.cos(.2*t)*I-1j*np.sin(.2*t)*Y
def bridge(n,m,lam):
    delta=2*lam;nu=Gamma/2;x=delta*T;p=np.exp(-x);one=-np.expm1(-x)
    beta=nu*one/delta
    logz=-x-2*np.log(one)-np.log(nu/delta)
    ks=np.arange(min(n,m)+1)
    logs=gammaln(n+1)-gammaln(ks+1)-gammaln(n-ks+1)+gammaln(m+1)-gammaln(m-ks+1)+ks*logz
    probs=np.exp(logs-logsumexp(logs));k=int(rng.choice(ks,p=probs))
    def te():return -np.log1p(-rng.random()*one)/delta
    events=[(te(),-1) for _ in range(n-k)]+[(T-te(),1) for _ in range(m-k)]
    nc=int(rng.poisson(nu*T))
    for _ in range(nc):
        b=T*rng.random();d=b+rng.exponential(1/delta)
        if d<=T:events.extend([(b,1),(d,-1)])
    events.sort();return events
def weight(m,n,lam):
    g=np.sqrt(Gamma*lam);x=2*lam*T;one=-np.expm1(-x)
    alpha=g*one/(2*lam);cc=Gamma*T/2-Gamma*one/(4*lam)
    terms=[]
    for k in range(min(m,n)+1):
        terms.append((m+n-2*k)*np.log(alpha)-x*k-gammaln(m-k+1)-gammaln(n-k+1)-gammaln(k+1))
    return np.exp(cc+.5*(gammaln(m+1)+gammaln(n+1))+logsumexp(terms))
rows=[]
for lam in [2.,100.]:
    a=np.diag(np.sqrt(np.arange(1,L+1)),1).astype(complex);N=np.diag(np.arange(L+1))
    H=np.kron(.2*Y,np.eye(L+1))+omega*np.kron(I,N)+np.sqrt(Gamma*lam)*(np.kron(C,a.conj().T)+np.kron(C.conj().T,a))-2j*lam*np.kron(I,N)
    exact=expm(-1j*T*H).reshape(2,L+1,2,L+1)
    err2=0.;maxevents=0
    for n in range(L+1):
      for m in range(L+1):
        avg=np.zeros((2,2),complex)
        for _ in range(samples):
            ev=bridge(n,m,lam);maxevents=max(maxevents,len(ev));occ=n;U=I.copy();last=0.;phase=0.;zero=False
            for t,sign in ev:
                phase+=omega*occ*(t-last)
                U=(-1j*(C if sign==1 else C.conj().T))@drift(t-last)@U
                occ+=sign;assert occ>=0
                if occ>L:zero=True
                last=t
            assert occ==m
            phase+=omega*occ*(T-last);U=np.exp(-1j*phase)*drift(T-last)@U
            if not zero:avg+=U
        estimate=weight(m,n,lam)*avg/samples
        err2+=np.linalg.norm(estimate-exact[:,m,:,n],'fro')**2
    error=float(np.sqrt(err2));assert error<.12
    rows.append({'lambda':lam,'Gamma':Gamma,'samples_per_entry':samples,'frobenius_error':error,'maximum_virtual_events':maxevents})
print(json.dumps({'seed':310652,'scope':'Monte Carlo finite-word diagnostic only','cutoff':L,'rows':rows},indent=2))
