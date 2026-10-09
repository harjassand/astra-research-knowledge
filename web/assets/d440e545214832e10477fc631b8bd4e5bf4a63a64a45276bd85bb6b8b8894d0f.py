"""Numerical evaluation of the exact simplex witness. Not a formal proof."""
import numpy as np
from scipy.linalg import null_space

def fisher(a,h):
    lam,v=np.linalg.eigh(a)
    keep=lam>1e-14*max(1.,lam.max())
    v=v[:,keep];lam=lam[keep]
    hh=v.conj().T@h@v
    ans=0.
    for i in range(len(lam)):
        for j in range(len(lam)):
            if abs(lam[i]-lam[j])<1e-9*max(lam[i],lam[j]):
                ff=2/(lam[i]+lam[j])
            else: ff=np.log(lam[i]/lam[j])/(lam[i]-lam[j])
            ans+=ff*abs(hh[i,j])**2
    return ans

def construct(k,p,s):
    n=k-1;d=n-1;q=1-p
    basis=null_space(np.ones((1,n)))
    vs=np.sqrt(n/d)*basis
    states=[]
    for v in vs:
        psi=np.r_[np.sqrt(1-s)*v,np.sqrt(s)]
        states.append(np.outer(psi,psi))
    rr=np.zeros((n,n));rr[-1,-1]=1
    blocks=np.array([q/n*x for x in states]+[p*rr])
    tangents=np.array([-x/n for x in states]+[rr])
    return blocks,tangents

def evaluate(w,p,s):
    k=w.shape[0];blocks,tangents=construct(k,p,s)
    out=np.einsum('xy,xij->yij',w,blocks)
    dout=np.einsum('xy,xij->yij',w,tangents)
    marginal=blocks.sum(axis=0);dm=tangents.sum(axis=0)
    # Analytic conditional input Fisher metric avoids subtractive cancellation.
    gin=s/(p*(1-p)*(p+(1-p)*s))
    gout=sum(fisher(a,h) for a,h in zip(out,dout))-fisher(marginal,dm)
    return gout/gin

if __name__=='__main__':
    for k in [3,4,5,8]:
        w=(np.ones((k,k))-np.eye(k))/(k-1)
        for p,s in [(1e-2,1e-5),(1e-3,1e-7),(1e-4,1e-9)]:
            print('k',k,'p',p,'s',s,'ratio',evaluate(w,p,s),'classical',1/(k-1),flush=True)
    # An asymmetric zero-common-column example (not a permutation-symmetric channel).
    w=np.array([[0,.2,.8,.0],[.1,0,.3,.6],[.4,.5,0,.1],[.1,.2,.7,0]])
    for p,s in [(1e-2,1e-5),(1e-3,1e-7),(1e-4,1e-9)]:
        print('asymmetric',p,s,evaluate(w,p,s),flush=True)
