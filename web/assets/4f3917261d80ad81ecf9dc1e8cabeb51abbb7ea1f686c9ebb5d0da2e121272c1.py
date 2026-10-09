"""Numerical, non-certifying probe of conditional BSC contraction.
Uses BKM Hessians on a binary classical input with a qubit reference.
"""
import numpy as np
from scipy.linalg import null_space, eigh

BASIS=np.array([np.eye(2),[[0,1],[1,0]],[[0,-1j],[1j,0]],[[1,0],[0,-1]]],complex)/np.sqrt(2)
Q=null_space(np.array([[1.,0,0,0,1.,0,0,0]]))

def bkm(a):
    w,v=np.linalg.eigh(a)
    if w.min()<=0: raise ValueError('Nonfaithful base')
    delta=w[:,None]-w[None,:]
    with np.errstate(invalid='ignore',divide='ignore'):
        f=(np.log(w[:,None])-np.log(w[None,:]))/delta
    for i in range(len(w)):
        for j in range(len(w)):
            if abs(delta[i,j])<1e-9*max(w[i],w[j]): f[i,j]=2/(w[i]+w[j])
    b=np.einsum('ij,bjk,kl->bil',v.conj().T,BASIS,v)
    return np.einsum('bij,ij,cij->bc',b.conj(),f,b).real

def ratio(a,b,c=.6):
    p=(1+c)/2; q=(1-c)/2
    g0=bkm(a+b)
    gin=np.block([[bkm(a)-g0,-g0],[-g0,bkm(b)-g0]])
    ga=bkm(p*a+q*b); gb=bkm(q*a+p*b)
    gout=np.block([[p*p*ga+q*q*gb-g0,p*q*(ga+gb)-g0],[p*q*(ga+gb)-g0,q*q*ga+p*p*gb-g0]])
    gi=Q.T@gin@Q; go=Q.T@gout@Q
    w,v=eigh(gi)
    keep=w>max(1e-9,1e-10*w.max())
    if not keep.any(): return np.nan,None,w
    trans=v[:,keep]/np.sqrt(w[keep])
    vals,vecs=eigh(trans.T@go@trans)
    return vals[-1],Q@trans@vecs[:,-1],w

if __name__=='__main__':
    rng=np.random.default_rng(20261009)
    best=(0,None)
    for i in range(12000):
        pa=rng.uniform(.01,.99)
        va=10**rng.uniform(-7,0); vb=10**rng.uniform(-7,0)
        theta=rng.uniform(0,np.pi)
        rot=np.array([[np.cos(theta/2),-np.sin(theta/2)],[np.sin(theta/2),np.cos(theta/2)]])
        a=pa*np.diag([va,1])/(1+va)
        b=(1-pa)*rot@np.diag([vb,1])@rot.T/(1+vb)
        r,d,w=ratio(a,b)
        if r>best[0] and r<1.01:
            best=(r,(pa,va,vb,theta,a,b,d,w))
    r,dat=best
    print('Best numerical ratio',r,'classical bound',.6**2,'convex upper',.6)
    print('parameters',dat[:4])
    print('A',dat[4],'B',dat[5], 'direction',dat[6],sep='\n')
    np.savez('/mnt/data/adaptive_foundational_research_20261009/bsc_probe_best.npz',ratio=r,a=dat[4],b=dat[5],direction=dat[6],input_eigenvalues=dat[7])
