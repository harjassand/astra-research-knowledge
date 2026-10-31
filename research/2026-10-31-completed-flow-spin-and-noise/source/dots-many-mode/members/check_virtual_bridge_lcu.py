"""Classical Monte Carlo diagnostic of the virtual-path LCU identity.
This is not the certified finite-bit source or a quantum implementation.
"""
import json
import numpy as np
from scipy.linalg import expm
from scipy.optimize import brentq

rng=np.random.default_rng(310634)
I=np.eye(2,dtype=complex);X=np.array([[0,1],[1,0]],complex)
Y=np.array([[0,-1j],[1j,0]],complex);Z=np.diag([1,-1]).astype(complex)
As=[.7*X,.9*Z];anorm=[.7,.9];gamma=[.5,.8];H0=.3*Y;T=.3
P=np.diag([0,1]);n_samples=1500
def transition(s,d,i,j,t):
    v=s+d;e=np.exp(-v*t);z=-np.expm1(-v*t)
    if i==0:return (d+s*e)/v if j==0 else s*z/v
    return d*z/v if j==0 else (s+d*e)/v
def bridge(s,d,start,end,t):
    now=0.;i=start;out=[]
    for k in range(100):
        rem=t-now
        if rem<1e-13:
            assert i==end
            return out
        p=transition(s,d,i,end,rem);q=s if i==0 else d
        atom=np.exp(-q*rem)/p if i==end else 0.
        u=rng.random()
        if u>=1-atom:
            assert i==end
            return out
        def f(x):return 1-np.exp(-q*x)*transition(s,d,i,end,rem-x)/p-u
        wait=brentq(f,0,rem,xtol=2e-14)
        now+=wait;out.append(now);i=1-i
    raise RuntimeError('fixture cap reached')
def drift(t):return np.cos(.3*t)*I-1j*np.sin(.3*t)*Y
rows=[]
for rates in [[1.,1.7],[64.,108.8]]:
    v=np.sqrt(np.array(gamma)*rates);g=v*np.array(anorm)
    omega=np.sqrt(np.array(rates)**2+g*g)
    slow=g*g/(omega+rates);fast=omega+rates
    Ms=[np.array([[0,g[i]],[g[i],-2*rates[i]]]) for i in range(2)]
    M=np.kron(Ms[0],I.real)+np.kron(I.real,Ms[1])
    E=expm(T*M)
    Heff=np.kron(H0,np.eye(4))
    for k in range(2):
        xx=np.kron(X,I) if k==0 else np.kron(I,X)
        pp=np.kron(P,I) if k==0 else np.kron(I,P)
        Heff+=v[k]*np.kron(As[k],xx)-2j*rates[k]*np.kron(I,pp)
    exact=expm(-1j*T*Heff).reshape(2,4,2,4)
    totalerr=0.;maxevents=0
    for a in range(4):
      for b in range(4):
        mean=np.zeros((2,2),complex)
        for _ in range(n_samples):
            events=[]
            for k in range(2):
                # Bit 0 in this list is the high Kronecker-factor bit.
                ai=(a>>(1-k))&1;bi=(b>>(1-k))&1
                events += [(t,k) for t in bridge(slow[k],fast[k],ai,bi,T)]
            events.sort();maxevents=max(maxevents,len(events))
            U=I.copy();last=0.
            for t,k in events:
                U=(-1j*As[k]/anorm[k])@drift(t-last)@U;last=t
            U=drift(T-last)@U;mean+=U
        estimate=E[b,a]*mean/n_samples
        totalerr+=np.linalg.norm(estimate-exact[:,b,:,a],'fro')**2
    err=float(np.sqrt(totalerr))
    assert err<.12,(rates,err)
    rows.append({'rates':rates,'samples_per_entry':n_samples,'frobenius_error':err,'largest_virtual_event_count':maxevents})
print(json.dumps({'seed':310634,'scope':'Monte Carlo consistency diagnostic only','rows':rows},indent=2))
