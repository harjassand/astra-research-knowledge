#!/usr/bin/env python3
"""Constructed before source comparison. Research tests, not a certified float solver."""
import itertools, json, time
from pathlib import Path
import numpy as np
from scipy.linalg import cho_factor, cho_solve

ROOT=Path(__file__).resolve().parent

def top(a,k,axis=1):
    if k<=0: return np.zeros(a.shape[0]) if axis==1 else 0.
    k=min(k,a.shape[axis])
    return np.partition(a,a.shape[axis]-k,axis=axis).take(indices=range(a.shape[axis]-k,a.shape[axis]),axis=axis).sum(axis=axis)

def native(n,edges,w,p):
    m=len(edges); A=np.zeros((n-1,m))
    for j,(a,b) in enumerate(edges):
        if a<n-1:A[a,j]=1.
        if b<n-1:A[b,j]=-1.
    K=(A*w)@A.T
    cf=cho_factor(K)
    C=cho_solve(cf,A)
    T=w[:,None]*(A.T@C)
    f=w*(A.T@cho_solve(cf,p[:-1]))
    return A,K,T,f

def certificate(T,f,k,steps=160,weight_search=0):
    m=len(f); d=1-np.diag(T)
    if min(d)<=1e-12:return dict(status='UNKNOWN',reason='bridge_or_small_diagonal_margin',min_diagonal_margin=float(min(d)))
    M=np.abs(T);np.fill_diagonal(M,0.)
    v=np.sqrt(np.maximum(np.abs(np.diag(T)),1e-9)) # overwritten by physically scaling if desired; generic positive start
    v=np.ones(m)
    best=(float('inf'),v.copy())
    for it in range(weight_search+1):
        z=top(M*v[None,:],k-1)/d
        rho=float(max(z/v))
        if rho<best[0]:best=(rho,v.copy())
        v=(v+z)/2+1e-12
        v/=max(v)
    rho,v=best
    if rho>=1-1e-12:return dict(status='UNKNOWN',reason='row_relaxation_not_contractive',rho=rho,min_diagonal_margin=float(min(d)))
    if k==1:u=np.abs(f)/d
    else:u=max(np.abs(f)/(d*v))*v/(1-rho)
    L=-u;U=u
    absbound=np.abs(f)+top(M*u[None,:],k)
    TT=T.copy();np.fill_diagonal(TT,0.)
    for _ in range(steps):
        pu=np.maximum(np.maximum(TT*L[None,:],TT*U[None,:]),0.)
        pl=np.maximum(np.maximum(-TT*L[None,:],-TT*U[None,:]),0.)
        Un=(f+top(pu,k-1))/d
        Ln=(f-top(pl,k-1))/d
        # Float enclosure only evaluated as theorem test; final exact test is separate.
        L,U=Ln,Un
    pu=np.maximum(np.maximum(TT*L[None,:],TT*U[None,:]),0.)
    pl=np.maximum(np.maximum(-TT*L[None,:],-TT*U[None,:]),0.)
    hi=f+top(pu,k);lo=f-top(pl,k)
    res=max(float(max((f+top(pu,k-1))-d*U)),float(max(d*L-(f-top(pl,k-1)))))
    return dict(status='ENCLOSURE',rho=rho,min_diagonal_margin=float(min(d)),L=L,U=U,lo=lo,hi=hi,absbound=absbound,upper_residual=res,v=v)

def exhaustive(A,K,w,p,T,f,k):
    m=len(w); lows=f.copy();highs=f.copy(); minmineig=1.;count=0;singular=0;max_formula_error=0.
    badsets=[]; witnesses=[None]*m
    for kk in range(1,k+1):
      for S in itertools.combinations(range(m),kk):
        S=np.array(S,dtype=int);count+=1
        # normalized T_SS is similar to the symmetric Q_SS.
        Qss=T[np.ix_(S,S)]*np.sqrt(w[S])[None,:]/np.sqrt(w[S])[:,None]
        mineig=float(np.linalg.eigvalsh(np.eye(kk)-Qss)[0]); minmineig=min(minmineig,mineig)
        if mineig<1e-10:
            singular+=1
            if len(badsets)<3:badsets.append(S.tolist())
            continue
        KS=K-(A[:,S]*w[S])@A[:,S].T
        theta=np.linalg.solve(KS,p[:-1]);ff=w*(A.T@theta)
        z=np.linalg.solve(np.eye(kk)-T[np.ix_(S,S)],f[S]);pred=f+T[:,S]@z
        valid=np.ones(m,dtype=bool);valid[S]=False
        max_formula_error=max(max_formula_error,float(max(abs(pred[valid]-ff[valid]),default=0.)))
        for e in np.where(valid)[0]:
            if ff[e]>highs[e]:highs[e]=ff[e];witnesses[e]=S.tolist()
            if ff[e]<lows[e]:lows[e]=ff[e]
    return dict(count=count,singular=singular,min_spectral_margin=minmineig,lo=lows,hi=highs,formula_error=max_formula_error,badsets=badsets,witnesses=witnesses)

def complete(n):return list(itertools.combinations(range(n),2))
def ring(n,r):return sorted({tuple(sorted((i,(i+j)%n))) for i in range(n) for j in range(1,r+1)})
def case(name,n,edges,w,p,k):
    t=time.perf_counter();A,K,T,f=native(n,edges,w,p); setup=time.perf_counter()-t
    t=time.perf_counter(); cert=certificate(T,f,k,weight_search=300); certtime=time.perf_counter()-t
    t=time.perf_counter(); actual=exhaustive(A,K,w,p,T,f,k);extime=time.perf_counter()-t
    row=dict(name=name,n=n,m=len(edges),k=k,status=cert['status'],rho=cert.get('rho'),outages_checked=actual['count'],islanding=actual['singular'],true_min_spectral_margin=actual['min_spectral_margin'],formula_error=actual['formula_error'],setup_seconds=setup,certificate_seconds=certtime,exhaustive_seconds=extime)
    if cert['status']=='ENCLOSURE':
        trueamp=np.maximum(abs(actual['lo']),abs(actual['hi']));amp=np.maximum(abs(cert['lo']),abs(cert['hi']))
        row.update(max_enclosure_violation=float(max(np.max(actual['hi']-cert['hi']),np.max(cert['lo']-actual['lo']))),median_bound_ratio=float(np.median(amp/np.maximum(trueamp,1e-14))),worst_bound_ratio=float(max(amp/np.maximum(trueamp,1e-14))),absolute_to_signed_ratio=float(np.median(cert['absbound']/np.maximum(amp,1e-14))),true_worst_flow=float(max(trueamp)),certified_uniform_capacity=float(max(amp)),float_supersolution_residual=cert['upper_residual'])
    return row

def main():
    rng=np.random.default_rng(993102)
    results=[]
    cases=[]
    for n in [6,8]:
      p=rng.normal(size=n);p-=p.mean()
      for k in range(1,min(4,n-1)):
        cases.append((f'complete{n}_k{k}',n,complete(n),np.ones(n*(n-1)//2),p,k))
    for n,r in [(8,2),(10,2),(10,3)]:
      es=ring(n,r);p=rng.normal(size=n);p-=p.mean()
      for k in [1,2,3]:cases.append((f'ring{n}_r{r}_k{k}',n,es,np.ones(len(es)),p,k))
    for eps in [1.,.05,.001]:
      es=complete(4)+[(i+4,j+4) for i,j in complete(4)]+[(i,i+4) for i in range(4)]
      w=np.r_[np.ones(12),np.full(4,eps)];p=np.r_[np.ones(4),-np.ones(4)]
      for k in [1,2,3]:cases.append((f'weak_four_cut_eps{eps}_k{k}',8,es,w,p,k))
    # Nonuniform weights make physical-coordinate row bounds ill-scaled. Weight search is charged.
    n=7;es=complete(n);w=np.exp(rng.uniform(-2,2,len(es)));p=rng.normal(size=n);p-=p.mean()
    for k in [1,2,3]:cases.append((f'heterogeneous_complete7_k{k}',n,es,w,p,k))
    for args in cases:
      row=case(*args);results.append(row);print(json.dumps(row),flush=True)
    (ROOT/'results.json').write_text(json.dumps(results,indent=2))

if __name__=='__main__':main()
