"""Exact Q(exp(2 pi i/3)) evaluation for different left/right graph bases.
This is an exponential-time restricted search, not an all-copy proof.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path
import numpy as np


def diagonalize3(A):
    """Return E,d with E^T A E=diag(d,0), all arithmetic modulo 3."""
    B=np.array(A,dtype=np.int64)%3; N=len(B); E=np.eye(N,dtype=np.int64);ds=[]
    for k in range(N):
        candidates=np.flatnonzero(np.diag(B)[k:])
        if len(candidates): i=k+int(candidates[0])
        else:
            pairs=np.argwhere(np.triu(B[k:,k:],1)!=0)
            if len(pairs)==0:break
            i,j=map(lambda x:k+int(x),pairs[0])
            B[:,i]=(B[:,i]+B[:,j])%3;B[i,:]=(B[i,:]+B[j,:])%3;E[:,i]=(E[:,i]+E[:,j])%3
        B[[k,i],:]=B[[i,k],:];B[:,[k,i]]=B[:,[i,k]];E[:,[k,i]]=E[:,[i,k]]
        d=int(B[k,k]);ds.append(d)
        for j in range(k+1,N):
            t=int(B[k,j])*d%3  # 1 and 2 are their own inverses.
            if t:
                B[:,j]=(B[:,j]-t*B[:,k])%3;B[j,:]=(B[j,:]-t*B[k,:])%3;E[:,j]=(E[:,j]-t*E[:,k])%3
    ds=np.array(ds,dtype=np.int64)
    assert np.array_equal((E.T@A@E)%3,np.diag(np.r_[ds,np.zeros(N-len(ds),dtype=np.int64)]))
    return E,ds


def evaluate(G,H,delta,v,w):
    n=len(G);batch=len(delta)
    if n>16:raise ValueError('int64 safety bound requires n<=16')
    if delta.shape!=v.shape or v.shape!=w.shape or v.shape[1]!=n:raise ValueError('label shapes')
    A0=np.zeros((2*n,2*n),dtype=np.int64);A0[:n,:n]=2*G;A0[n:,n:]=2*H
    zero=np.zeros_like(delta)
    # All arrays are row vectors.  Pair 0/1 are diagonals; pair 2 is crossed coherence.
    bx=np.concatenate((zero,-delta),axis=1)
    by=np.concatenate((v,w-delta),axis=1)
    bc=np.concatenate((zero,w-delta),axis=1)
    kc=np.concatenate((v,-delta),axis=1)
    accum=np.zeros((3,batch,2),dtype=np.int64)
    for mask in range(1<<n):
        S=[i for i in range(n) if mask>>i&1];perm=np.arange(2*n)
        for i in S:perm[i],perm[i+n]=perm[i+n],perm[i]
        A=(A0[np.ix_(perm,perm)]-A0)%3;E,ds=diagonalize3(A);r=len(ds);k=r//2
        scalar=(-1)**(len(S)+int(np.sum(ds==2))+k)*2**(n-len(S))*3**(n-k-(r%2))
        p0,q0=(scalar,2*scalar) if r%2 else (scalar,0)
        factors=np.array([[p0,q0],[-q0,p0-q0],[q0-p0,-p0]],dtype=np.int64)
        for j,L in enumerate((bx[:,perm]-bx,by[:,perm]-by,kc[:,perm]-bc)):
            lp=(L@E)%3;good=np.all(lp[:,r:]==0,axis=1)
            phase=(-np.sum(lp[:,:r]**2*ds,axis=1))%3
            accum[j]+=factors[phase]*good[:,None]
    # Diagonal values must be real, hence their omega coefficients vanish.
    assert not np.any(accum[:2,:,1]),'Diagonal is not real'
    return accum[0,:,0],accum[1,:,0],accum[2,:,0],accum[2,:,1],2**n*3**n


def check():
    from npt_core import endpoint_action,endpoint
    rng=np.random.default_rng(7721);maximum=0.;cases=0
    for n in (1,2,3,4):
        graphs=[]
        for _ in range(2):
            G=np.triu(rng.integers(0,3,(n,n)),1);graphs.append(G+G.T)
        G,H=graphs
        delta=rng.integers(0,3,(5,n));v=rng.integers(0,3,(5,n));w=rng.integers(0,3,(5,n))
        v[:,0]=w[:,0]=1
        ax,ay,p,q,scale=evaluate(G,H,delta,v,w)
        basis=np.array(list(np.ndindex(*(3,)*n)),dtype=int);omega=np.exp(2j*np.pi/3)
        def state(K,a):
            Q=np.sum((basis@np.triu(K,1))*basis,axis=1)
            return omega**((Q+basis@a)%3)/np.sqrt(3**n)
        for j in range(5):
            X=np.outer(state(G,np.zeros(n,dtype=int)),state(H,-delta[j]).conj())
            Y=np.outer(state(G,v[j]),state(H,w[j]-delta[j]).conj())
            vals=(endpoint(X,(3,)*n),endpoint(Y,(3,)*n),np.vdot(X,endpoint_action(Y,(3,)*n)))
            expected=(int(ax[j])/scale,int(ay[j])/scale,(int(p[j])+int(q[j])*omega)/scale)
            for a,b in zip(vals,expected):
                err=abs(a-b);maximum=max(maximum,float(err));assert err<1e-12,(n,j,a,b);cases+=1
    return {'materialized_complex_comparisons':cases,'max_absolute_error':maximum}


def run(n,graphs,batch,seed):
    rng=np.random.default_rng(seed);records=[];neg=[]
    for trial in range(graphs):
        gh=[]
        for j in range(2):
            if trial==0:
                G=np.zeros((n,n),dtype=np.int64)
                for i in range(n-1):G[i,i+1]=G[i+1,i]=1+j
            else:
                G=np.triu(rng.integers(0,3,(n,n)),1);G=G+G.T
            gh.append(G)
        G,H=gh
        delta=rng.integers(0,3,(batch,n));v=rng.integers(0,3,(batch,n));w=rng.integers(0,3,(batch,n))
        w[:batch//3]=v[:batch//3];delta[batch//3:2*batch//3]=0
        for i in range(batch):
            if not np.any(v[i]):v[i,0]=1
            if not np.any(w[i]):w[i,0]=1
        a,b,p,q,L=evaluate(G,H,delta,v,w)
        assert np.all(a>=0) and np.all(b>=0)
        gaps=[int(aa)*int(bb)-(int(pp)**2-int(pp)*int(qq)+int(qq)**2) for aa,bb,pp,qq in zip(a,b,p,q)]
        for i,x in enumerate(gaps):
            if x<0:neg.append({'G':G.tolist(),'H':H.tolist(),'delta':delta[i].tolist(),'v':v[i].tolist(),'w':w[i].tolist(),'a':int(a[i]),'b':int(b[i]),'p':int(p[i]),'q':int(q[i]),'scale':L})
        rec={'sites':n,'trial':trial,'candidate_planes':batch,'negative_determinants':sum(x<0 for x in gaps),
             'zero_determinants':sum(x==0 for x in gaps),'minimum_scaled_determinant':str(min(gaps)),
             'scale':L,'G':G.tolist(),'H':H.tolist()}
        print(json.dumps(rec),flush=True);records.append(rec)
    out={'status':'exact finite restricted plane tests; not global positivity','seed':seed,'records':records,'negatives':neg}
    Path(__file__).with_name(f'MIXED_GRAPH_n{n}.json').write_text(json.dumps(out,indent=2)+'\n')

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--n',type=int,default=6);ap.add_argument('--graphs',type=int,default=4);ap.add_argument('--batch',type=int,default=512);ap.add_argument('--check',action='store_true')
    args=ap.parse_args()
    if args.check:
        z=check();print(json.dumps(z));Path(__file__).with_name('MIXED_GRAPH_FORMULA_RECEIPT.json').write_text(json.dumps(z,indent=2)+'\n')
    run(args.n,args.graphs,args.batch,20261009+211*args.n)
