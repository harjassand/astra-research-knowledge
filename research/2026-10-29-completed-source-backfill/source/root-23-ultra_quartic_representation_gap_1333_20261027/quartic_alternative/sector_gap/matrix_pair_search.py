"""Global PC support search after exact amplitude/background elimination.

For positive homogeneous quarticF define T(R)=H_F(R)/2-g(R)g(R)^T/(4F(R)).
PC requires T(Rplus)/detRplus - T(Rminus)/detRminus PSD for every signed
pair. A negative numerical eigenvalue supplies only a candidate witness.
"""
import json,time
from pathlib import Path
import numpy as np
from search_support import energy,invariants,gradient

def hessian_batch(z,tau=11.3):
    z=np.asarray(z);a,b,c,d=z.T;u,v,w,q=invariants(z)
    n=len(z);B=np.zeros((n,4,4))
    B[:,:,0]=np.stack([2*a,0*a,2*c,0*a],axis=1)
    B[:,:,1]=np.stack([0*a,2*b,0*a,2*d],axis=1)
    B[:,:,2]=np.stack([b,a,d,c],axis=1)
    B[:,:,3]=np.stack([d,-c,-b,a],axis=1)
    J=np.array([[2,0,0,4],[0,2,0,-4],[0,0,6,0],[4,-4,0,2*tau]],float)
    H=B@J@np.swapaxes(B,1,2)
    D=np.stack([2*u+4*q,2*v-4*q,6*w,2*tau*q+4*(u-v)],axis=1)
    Hu=np.diag([2,0,2,0]);Hv=np.diag([0,2,0,2])
    Hw=np.array([[0,1,0,0],[1,0,0,0],[0,0,0,1],[0,0,1,0]])
    Hq=np.array([[0,0,0,1],[0,0,-1,0],[0,-1,0,0],[1,0,0,0]])
    H+=np.einsum('ni,ijk->njk',D,np.stack([Hu,Hv,Hw,Hq]))
    return H

def S(z,tau=11.3):
    z=np.atleast_2d(z);a,b,c,d=z.T;u,v,w,q=invariants(z)
    du,dv,dw,dq=2*u+4*q,2*v-4*q,6*w,2*tau*q+4*(u-v)
    g=np.stack([2*a*du+b*dw+d*dq,2*b*dv+a*dw-c*dq,
                2*c*du+d*dw-b*dq,2*d*dv+c*dw+a*dq],axis=1)
    T=hessian_batch(z,tau)/2-g[:,:,None]*g[:,None,:]/(4*energy(z,tau)[:,None,None])
    return T/q[:,None,None]

def main():
    start=time.monotonic();rng=np.random.default_rng(20261028);n=100000;tau=11.3
    plus=rng.normal(size=(n,4));plus/=np.linalg.norm(plus,axis=1)[:,None]
    minus=rng.normal(size=(n,4));minus/=np.linalg.norm(minus,axis=1)[:,None]
    # Column sign flips map either determinant half-sphere to the other.
    sign=invariants(plus)[3]<0;plus[sign,1]*=-1;plus[sign,3]*=-1
    sign=invariants(minus)[3]>0;minus[sign,1]*=-1;minus[sign,3]*=-1
    difference=S(plus,tau)-S(minus,tau)
    eigen,vec=np.linalg.eigh(difference);j=int(np.argmin(eigen[:,0]));A=vec[j,:,0]
    Rm,Rp=minus[j],plus[j]
    result={'status':'NUMERICAL_CANDIDATE_ONLY','tau':tau,'pairs':n,
            'minimum_eigenvalue':float(eigen[j,0]),'A':A.tolist(),
            'Rminus':Rm.tolist(),'Rplus':Rp.tolist(),'wall_seconds':time.monotonic()-start,
            'interpretation':'Only exact rational reconstruction can establish a non-PC witness'}
    Path('matrix_pair_search.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

if __name__=='__main__':main()
