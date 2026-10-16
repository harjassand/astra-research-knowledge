"""Original check: physical pair-space, two-sided finite-difference certificate.
Floating point evaluation is a check, not a rigorous numerical enclosure.
"""
import os
os.environ['OPENBLAS_NUM_THREADS']='1';os.environ['OMP_NUM_THREADS']='1'
import numpy as np,itertools, math,json,time
from scipy.linalg import eigh
from scipy.optimize import brentq
from pathlib import Path
OUT=Path(__file__).resolve().parent

def pair_spec(n,edges,rates):
    pairs=list(itertools.combinations(range(n),2)); idx={p:i for i,p in enumerate(pairs)}
    W=np.zeros((n,n))
    for (x,y),r in zip(edges,rates):W[x,y]=W[y,x]=r
    H=np.zeros((len(pairs),len(pairs)))
    for i,(x,y) in enumerate(pairs):
        H[i,i]=2*W[x,y]
        for a,z in ((x,y),(y,x)):
            for v in range(n):
                if v in (a,z):continue
                j=idx[tuple(sorted((v,z)))];H[i,i]+=W[a,v];H[i,j]-=W[a,v]
    lam,V=eigh(H); assert lam.min()>-1e-8
    lam=np.maximum(lam,0); A=V*(V.T@np.ones(len(pairs)))[None,:]
    return lam,A,[idx[tuple(sorted(e))] for e in edges],H

def profile_certificate(n,edges,rates,capped):
    l,A,ei,H=pair_spec(n,edges,rates); m,B,_,G=pair_spec(n,edges,capped)
    d=np.abs(l[:,None]-m[None,:]); small=d<1e-10
    J=np.exp(-np.minimum(l[:,None],m[None,:]))
    J[~small]*=-np.expm1(-d[~small])/d[~small]
    # Limit factor =1 where d=0
    vals=np.sum((A@J)*B,axis=1)
    per=(np.asarray(rates)-capped)*vals[ei]
    return float(per.sum()),per.tolist(),float(vals.min())

def endpoint(n,edges,rates):
    states=list(itertools.permutations(range(n))); idx={s:i for i,s in enumerate(states)}
    L=np.zeros((len(states),len(states))); I=np.arange(len(states))
    for e,r in zip(edges,rates):
        p=[]
        for s in states:
            a=list(s);a[e[0]],a[e[1]]=a[e[1]],a[e[0]];p.append(idx[tuple(a)])
        L[I,I]+=r;L[I,np.array(p)]-=r
    lam,V=eigh(L,check_finite=False); lam=np.maximum(lam,0)
    p=V@(np.exp(-lam)*V[0,:]);err=abs(p.sum()-1);p=np.maximum(p,0);p/=p.sum()
    return p,float(err)

def averaging_cert(n,edges,rates,cutmask):
    # Path partitions; exact Aldous spectral gap controls full interchange mixing.
    clusters=[];last=0
    for i in range(n-1):
        if cutmask>>i&1:clusters.append(list(range(last,i+1)));last=i+1
    clusters.append(list(range(last,n)))
    total=0;parts=[];boundary=sum(r for i,r in enumerate(rates) if cutmask>>i&1)
    for C in clusters:
        s=len(C)
        if s==1:continue
        L=np.zeros((s,s)); ids={x:j for j,x in enumerate(C)}; gamma=0
        for (x,y),r in zip(edges,rates):
            if x in C and y in C:
                a=ids[x];b=ids[y];L[a,a]+=r;L[b,b]+=r;L[a,b]-=r;L[b,a]-=r
            elif (x in C)!=(y in C):gamma+=r
        gap=eigh(L,eigvals_only=True)[1]; amp=.5*math.sqrt(math.factorial(s)-1)
        d1=min(1,amp*math.exp(-gap))
        if amp<=1: integ=amp*(-math.expm1(-gap))/gap
        else:
            t0=math.log(amp)/gap
            integ=1 if t0>=1 else t0+(1-amp*math.exp(-gap))/gap
        error=d1+gamma*(gamma+2)*integ
        total+=error;parts.append(dict(C=C,gap=gap,Gamma=gamma,mixing_error=error))
    return dict(clusters=clusters,certificate=total,boundary_intensity=boundary,parts=parts)

rows=[]
for n,rs in [(6,[1,10,100,1000,10000]),(6,[.1,1,10,100,1000]),(6,[1,3,9,27,81]),(6,[.2,2,20,200,2000])]:
    edges=[(i,i+1) for i in range(n-1)];rs=np.array(rs,float)
    po,mass=endpoint(n,edges,rs)
    cases=[]
    for K in [1,2,5,10,20,50,100,200,500,1000,2000,5000]:
        if K>=max(rs):continue
        cap=np.minimum(rs,K);b,per,mn=profile_certificate(n,edges,rs,cap);p,merr=endpoint(n,edges,cap);tv=.5*abs(po-p).sum()
        assert tv<=b+1e-7,(rs,K,tv,b)
        cases.append(dict(K=K,certificate=b,TV=tv,event_intensity=float(cap.sum()),per_edge=per))
    K=brentq(lambda k:profile_certificate(n,edges,rs,np.minimum(rs,k))[0]-.05,.01,max(rs))
    cap=np.minimum(rs,K);p,merr=endpoint(n,edges,cap)
    av=[averaging_cert(n,edges,rs,j) for j in range(2**(n-1))]
    # all singleton partition makes no approximation and is SSA, so requires no certification
    eligible=[x for x in av if x['certificate']<=.05]
    best=min(eligible,key=lambda x:x['boundary_intensity'])
    row=dict(n=n,rates=rs.tolist(),state_count=math.factorial(n),pair_states=n*(n-1)//2,original_intensity=float(rs.sum()),certificate_05_K=K,certificate_05_intensity=float(cap.sum()),certificate_05_actual_TV=float(.5*abs(po-p).sum()),best_certified_averaging=best,cases=cases)
    rows.append(row);print(json.dumps({k:v for k,v in row.items() if k!='cases'}),flush=True)
(OUT/'pair_profile_results.json').write_text(json.dumps(rows,indent=2))
