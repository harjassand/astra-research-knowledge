"""One-parameter physical channel: decay triplets into the two-spin singlet."""
from __future__ import annotations
import numpy as np
from scipy.linalg import eigh
from scipy.optimize import minimize_scalar
from experiment import heisenberg,local_pair,kagome
s=np.array([0,1,-1,0])/np.sqrt(2);Ps=np.outer(s,s);Pt=np.eye(4)-Ps

def channel_image(H,q):
    r=H.shape[0]//4;K=Ps+q*Pt
    term=np.kron(K,np.eye(r))@H@np.kron(K,np.eye(r))
    ss=np.einsum('i,iajb,j->ab',s,H.reshape(4,r,4,r),s)
    return term+(1-q*q)*np.kron(Pt,ss)

if __name__=='__main__':
 for name in ['chain','dimer','kagome']:
    if name=='chain':edges=[(i,(i+1)%12,1.) for i in range(12)]
    elif name=='dimer':edges=[(0,1,1.),(1,2,.2),(2,3,1.)]
    else:_,edges=kagome()
    ha,hb,sites=local_pair(edges,[0,1],(0,1,1.))
    def f(q):return float(eigh(ha-channel_image(hb,q),eigvals_only=True)[0])
    z=minimize_scalar(lambda q:-f(q),bounds=(0,1),method='bounded',options={'xatol':1e-13})
    print(name,'q',z.x,'lower',-z.fun,'q=.5',f(.5),'q=.4',f(.4),'q=1/3',f(1/3),flush=True)
