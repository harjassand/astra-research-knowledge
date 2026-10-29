"""Exact finite-reset Kraus gadget checks; no FT/compiler claim."""
import numpy as np
from scipy.linalg import expm
from scipy.integrate import quad
import json

def check(g,k):
    A=np.array([[0,-g],[g,-k/2.]])
    def f(t):
        v=expm(t*A)@np.array([1.,0.])
        return k*v[1]**2
    rp=(k+np.sqrt(k*k-16*g*g))/2
    rm=4*g*g/rp
    rows=[]
    for s in [0,.01,.1,1]:
        numeric=quad(lambda t: np.exp(-s*t)*f(t),0,np.inf,epsabs=1e-11)[0]
        formula=2*k*g*g/((s+k/2)*(s*s+k*s+4*g*g))
        phase=(k/2)/(s+k/2)*rp/(s+rp)*rm/(s+rm)
        rows.append(dict(s=s,numeric=numeric,formula=formula,phase=phase))
        assert abs(numeric-formula)<1e-8
        assert abs(phase-formula)<1e-12
    mean=quad(lambda t:t*f(t),0,np.inf)[0]
    assert abs(mean-(k/(4*g*g)+2/k))<1e-6
    return dict(g=g,kappa=k,rplus=rp,rminus=rm,mean=mean,checks=rows)

# Check operator closure for a genuinely nonunitary 2-Kraus amplitude-damping update.
d=.37
K=[np.diag([1,np.sqrt(1-d)]),np.array([[0,np.sqrt(d)],[0,0]])]
g=.1;k=1.;m=2;ds=2;da=m+1
H=np.zeros((ds*da,ds*da),complex)
for s,ks in enumerate(K,1):
    B=np.zeros((da,da));B[s,0]=1
    H+=g*(np.kron(ks,B)+np.kron(ks.conj().T,B.T))
Pe=np.diag([0,1,1]);Heff=H-1j*k/2*np.kron(np.eye(ds),Pe)
psi=np.array([1,1j])/np.sqrt(2)
u=np.kron(psi,[1,0,0]);v=sum(np.kron(ks@psi,np.eye(da)[s]) for s,ks in enumerate(K,1))
for t in [.1,1,10,100]:
    a,y=expm(t*np.array([[0,-g],[g,-k/2]]))@np.array([1.,0.])
    assert np.linalg.norm(expm(-1j*t*Heff)@u-(a*u-1j*y*v))<1e-12
results=[check(g,1) for g in [.05,.1,.2,.249]]
print(json.dumps(results,indent=2))
open('autonomous_noise_bridge_20261029/renewal_results.json','w').write(json.dumps(results,indent=2)+'\n')
