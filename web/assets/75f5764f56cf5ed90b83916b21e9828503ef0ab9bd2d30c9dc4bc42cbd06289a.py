"""Probe for harmonic-center formula; floating point is diagnostic only."""
import numpy as np
from scipy.linalg import null_space
from scipy.optimize import minimize
from support_witness_probe import fisher

def harmonic_constant(w):
    k=w.shape[0]
    common=(w>0).all(axis=0)
    if not common.any(): return 1., np.full(k,1/k)
    rec=1/w[:,common]
    def obj(th):return np.sum(1/(th@rec))
    def jac(th):return -np.sum(rec/(th@rec)**2,axis=1)
    rr=minimize(obj,np.full(k,1/k),jac=jac,bounds=[(0,1)]*k,
        constraints={'type':'eq','fun':lambda th:np.sum(th)-1,'jac':lambda th:np.ones(k)},
        method='SLSQP',options={'ftol':1e-13,'maxiter':2000})
    if not rr.success: raise RuntimeError(rr.message)
    return 1-rr.fun,rr.x

def construct(theta,p,s,tau=None):
    k=len(theta)
    d=np.sqrt(theta)
    basis=null_space(d.reshape(1,-1))
    us=basis/np.sqrt(k-1)
    tau=np.full(k,1/k) if tau is None else tau
    rr=np.zeros((k,k));rr[-1,-1]=1
    blocks=[];tangents=[]
    for x in range(k):
        f=np.r_[np.sqrt(1-s)*us[x],np.sqrt(s)*d[x]]
        ff=np.outer(f,f)
        blocks.append((1-p)*ff+p*tau[x]*rr)
        tangents.append(-ff+tau[x]*rr)
    return np.array(blocks),np.array(tangents)

def evaluate(w,theta,p,s):
    bs,ds=construct(theta,p,s)
    o=np.einsum('xy,xij->yij',w,bs)
    do=np.einsum('xy,xij->yij',w,ds)
    gr=fisher(bs.sum(0),ds.sum(0))
    gi=sum(fisher(a,h) for a,h in zip(bs,ds))-gr
    go=sum(fisher(a,h) for a,h in zip(o,do))-gr
    return go/gi,gi,go

if __name__=='__main__':
    channels={}
    for a in [.6,.01,.1,.8]:
        b=(1-a)/2
        channels['sym'+str(a)]=np.full((3,3),b)+(a-b)*np.eye(3)
    channels['triangle']=(np.ones((3,3))-np.eye(3))/2
    channels['asym']=np.array([[.1,.3,.6],[.5,.4,.1],[.4,.2,.4]])
    channels['partial_zero']=np.array([[.3,.3,.4],[.5,.5,0],[.2,.3,.5]])
    for name,w in channels.items():
        eta,theta=harmonic_constant(w)
        theta=.99999*theta+.00001/len(theta)
        print(name,'predicted',eta,'theta',theta,flush=True)
        for p,s in [(1e-2,1e-5),(1e-3,1e-7),(1e-4,1e-9),(1e-5,1e-11)]:
            print(p,s,evaluate(w,theta,p,s),flush=True)
