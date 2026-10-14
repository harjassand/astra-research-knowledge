"""Variational tensor-train solver for an explicit reversible soft-East generator.
No configuration list or equilibrium trajectories are constructed.
Floating optimization is NOT a certificate: exact_check.py validates dyadic cores.
"""
from __future__ import annotations
import time, warnings
import numpy as np
from scipy.linalg import solve, svd


def east_mpo(n: int, k: float, eps: float):
    if n < 2 or k <= 0 or not 0 < eps <= 1:
        raise ValueError('Require n>=2, k>0 and 0<eps<=1')
    q=1/(1+k*k); s=k/(1+k*k)
    I=np.eye(2); h=np.diag([0.,1.]); N=np.array([[q,-s],[-s,1-q]])
    cores=[]
    for i in range(n):
        W=np.zeros((3,3,2,2))
        W[0,0]=I; W[1,0]=h; W[2,2]=I
        W[2,1]=(1-eps)*N
        O=(1. if i==0 else eps)*h
        if i==0: O=O+q*eps*I
        if i==n-1: O=O+q*(1-eps)*N
        W[2,0]=O
        if i==0: W=W[2:3]
        if i==n-1: W=W[:,0:1]
        cores.append(W)
    return cores


def left_step(L,A,W):
    return np.einsum('amb,aic,mnik,bkd->cnd',L,A,W,A,optimize=True)

def right_step(R,A,W):
    return np.einsum('aic,mnik,bkd,cnd->amb',A,W,A,R,optimize=True)

def source_left(l,A): return l@A[:,0,:]
def source_right(r,A): return A[:,0,:]@r

def overlap(A,B):
    e=np.ones((1,1))
    for x,y in zip(A,B):
        e=np.einsum('ab,aic,bid->cd',e,x,y,optimize=True)
    return float(e[0,0])

def source_overlap(A):
    v=np.ones(1)
    for x in A: v=v@x[:,0,:]
    return float(v[0])

def apply_mpo(W,A):
    out=[]
    for w,a in zip(W,A):
        c=np.einsum('mnij,aib->manjb',w,a,optimize=True) if False else np.einsum('mnij,ajb->ma inb',w,a,optimize=True)
        # physical output i, combined left (m,a), right (n,b)
        out.append(c.reshape(w.shape[0]*a.shape[0],2,w.shape[1]*a.shape[2]))
    return out

def dense_mps(A):
    v=np.ones((1,1))
    for a in A:
        v=np.einsum('xa,aib->xib',v,a).reshape(-1,a.shape[2])
    return v[:,0]

def dense_mpo(W):
    # only for explicitly labelled SMALL reference checks
    E=np.ones((1,1,1))
    for w in W:
        E=np.einsum('xym,mnij->xiyjn',E,w).reshape(E.shape[0]*2,E.shape[1]*2,w.shape[1])
    return E[:,:,0]

def diagnostics(A,W,eps,q):
    f=source_overlap(A)
    L=np.ones((1,1,1))
    for a,w in zip(A,W): L=left_step(L,a,w)
    energy=float(L[0,0,0])
    y=apply_mpo(W,A)
    hy=source_overlap(y)
    yn=overlap(y,y)
    rr=1-2*hy+yn
    lower=2*f-energy
    r0=1-hy
    gap=(r0*r0/q+max(0.,rr-r0*r0)/(1+q))/eps
    return {'source':f,'energy':energy,'lower_float':lower,'residual_sq_float':rr,'r0_float':r0,'upper_two_sector_float':lower+gap,'max_rank':max(a.shape[2] for a in A)}

def solve_tt(n:int,k:float,eps:float,rank:int=8,sweeps:int=8,seed:int=0, verbose:bool=True, initial=None):
    W=east_mpo(n,k,eps); q=1/(1+k*k)
    if initial is None:
        A=[np.array([[[1.],[0.]]]) for _ in range(n)]
        A[-1]*=1/(q*(eps+(1-eps)*q))
    else:
        A=[a.copy() for a in initial]
    logs=[]; t0=time.perf_counter()
    for sweep in range(sweeps):
        # Forward sweep. The previous backward sweep left right-canonical cores.
        R=[None]*(n+1); rb=[None]*(n+1)
        R[n]=np.ones((1,1,1)); rb[n]=np.ones(1)
        for i in range(n-1,-1,-1):
            R[i]=right_step(R[i+1],A[i],W[i]); rb[i]=source_right(rb[i+1],A[i])
        L=np.ones((1,1,1)); lb=np.ones(1)
        for i in range(n-1):
            a=A[i].shape[0]; c=A[i+1].shape[2]
            H=np.einsum('amb,mnik,npjl,cpd->aijcbkld',L,W[i],W[i+1],R[i+2],optimize=True).reshape(a*4*c,a*4*c)
            H=(H+H.T)/2
            b=np.zeros((a,2,2,c)); b[:,0,0,:]=lb[:,None]*rb[i+2][None,:]
            with warnings.catch_warnings(record=True) as warn:
                x=solve(H,b.ravel(),assume_a='pos',check_finite=False)
            if warn: logs.append({'warning':str(warn[0].message),'sweep':sweep,'site':i,'direction':'forward'})
            U,S,Vh=svd(x.reshape(a*2,2*c),full_matrices=False,check_finite=False,lapack_driver='gesvd')
            rr=min(rank,len(S))
            A[i]=U[:,:rr].reshape(a,2,rr)
            A[i+1]=(S[:rr,None]*Vh[:rr,:]).reshape(rr,2,c)
            L=left_step(L,A[i],W[i]); lb=source_left(lb,A[i])
        # Backward sweep
        LL=[None]*(n+1); lbb=[None]*(n+1)
        LL[0]=np.ones((1,1,1)); lbb[0]=np.ones(1)
        for i in range(n):
            LL[i+1]=left_step(LL[i],A[i],W[i]); lbb[i+1]=source_left(lbb[i],A[i])
        Rcur=np.ones((1,1,1)); rbcur=np.ones(1)
        for i in range(n-2,-1,-1):
            a=A[i].shape[0]; c=A[i+1].shape[2]
            H=np.einsum('amb,mnik,npjl,cpd->aijcbkld',LL[i],W[i],W[i+1],Rcur,optimize=True).reshape(a*4*c,a*4*c)
            H=(H+H.T)/2
            b=np.zeros((a,2,2,c)); b[:,0,0,:]=lbb[i][:,None]*rbcur[None,:]
            with warnings.catch_warnings(record=True) as warn:
                x=solve(H,b.ravel(),assume_a='pos',check_finite=False)
            if warn: logs.append({'warning':str(warn[0].message),'sweep':sweep,'site':i,'direction':'backward'})
            U,S,Vh=svd(x.reshape(a*2,2*c),full_matrices=False,check_finite=False,lapack_driver='gesvd')
            rr=min(rank,len(S))
            A[i]=(U[:,:rr]*S[:rr]).reshape(a,2,rr)
            A[i+1]=Vh[:rr,:].reshape(rr,2,c)
            Rcur=right_step(Rcur,A[i+1],W[i+1]); rbcur=source_right(rbcur,A[i+1])
        d=diagnostics(A,W,eps,q); d['sweep']=sweep+1; d['seconds']=time.perf_counter()-t0
        logs.append(d)
        if verbose: print(n,k,eps,rank,d,flush=True)
    return A,logs

if __name__=='__main__':
    import argparse, json
    p=argparse.ArgumentParser(); p.add_argument('--n',type=int,default=8); p.add_argument('--k',type=float,default=2); p.add_argument('--eps',type=float,default=1e-4);p.add_argument('--rank',type=int,default=8);p.add_argument('--sweeps',type=int,default=4);p.add_argument('--out',default='trial')
    a=p.parse_args()
    cores,logs=solve_tt(a.n,a.k,a.eps,a.rank,a.sweeps)
    np.savez(a.out+'.npz',**{f'a{i}':x for i,x in enumerate(cores)})
    with open(a.out+'.json','w') as f: json.dump({'n':a.n,'k':a.k,'eps':a.eps,'rank':a.rank,'logs':logs},f,indent=2)
    if a.n<=10:
        H=dense_mpo(east_mpo(a.n,a.k,a.eps)); b=np.zeros(2**a.n); b[0]=1
        true=solve(H,b,assume_a='pos')[0]
        print('dense_reference',true,'spectrum_min',np.linalg.eigvalsh(H)[0])
