"""Development experiment: exact minimax conductance-query policy on soft-East kinetics.
The learner receives only masses, edge endpoints, conductance bounds and an edge oracle.
No trajectory, committor, facilitation parent or transport map enters its decisions.
"""
from pathlib import Path
ROOT = Path(__file__).resolve().parent
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
os.environ.setdefault('OMP_NUM_THREADS','1')
import time, json
import numpy as np
from scipy.linalg import solve, inv
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import spsolve


def soft_east(L=9, q=.08, softness=1e-5, seed=81426):
    """Open soft-East chain; last site is the absorbing target, others are relabelled.
    This is a microscopic binary-state Markov model, NOT a fitted molecular MSM.
    Source: product Bernoulli(q) conditioned on target site being zero.
    """
    n=L-1; N=1<<n
    rng=np.random.default_rng(seed)
    order=list(rng.permutation(n))+[n]
    parent={order[0]:None}
    for j in range(1,L): parent[order[j]]=order[j-1]
    ids=np.arange(N)
    bits=((ids[:,None]>>np.arange(n))&1)
    counts=bits.sum(axis=1)
    m=q**counts*(1-q)**(n-counts)
    aa=[]; bb=[]; base=[]; fac=[]; dims=[]
    for i in range(n):
        for x in ids[bits[:,i]==0]:
            aa.append(int(x));bb.append(int(x^(1<<i)));dims.append(i)
            base.append(m[x]*q)
            p=parent[i]
            fac.append(1. if p is None or ((int(x)>>p)&1) else softness)
    for x in ids:
        aa.append(int(x));bb.append(-1);dims.append(n);base.append(m[x]*q)
        p=parent[n]
        fac.append(1. if (int(x)>>p)&1 else softness)
    return {'a':np.array(aa),'b':np.array(bb),'m':m,'base':np.array(base),
            'fac':np.array(fac),'dims':np.array(dims),'order':order,
            'q':q,'softness':softness,'L':L}

def matrix(model, c):
    a,b=model['a'],model['b']; N=len(model['m']); mask=b>=0
    rows=np.r_[a,b[mask],a[mask],b[mask]]
    cols=np.r_[a,b[mask],b[mask],a[mask]]
    data=np.r_[c,c[mask],-c[mask],-c[mask]]
    return coo_matrix((data,(rows,cols)),shape=(N,N)).tocsc()

def edge_values(K, m, a,b):
    u=K@m; v=u[a].copy(); R=K[a,a].copy(); ok=b>=0
    v[ok]-=u[b[ok]]
    R[ok]+=K[b[ok],b[ok]]-2*K[a[ok],b[ok]]
    return u,v,R

def update(K, a,b, delta):
    if delta==0:return
    k=K[:,a].copy()
    if b>=0:k-=K[:,b]
    R=k[a]-(k[b] if b>=0 else 0.)
    den=1+delta*R
    if den<=0: raise ArithmeticError('loss of positive definiteness')
    K-= (delta/den)*np.outer(k,k)

def run(model, policy='minimax', rtol=.10, seed=1, max_queries=None, refresh=64, oracle=None):
    start=time.perf_counter();a,b,m=model['a'],model['b'],model['m']
    base=model['base'];E=len(a);N=len(m)
    if oracle is None:
        # A fixture oracle: only selected indices are accessed, never used for scores.
        oracle=lambda e: model['fac'][e]
    observations=[]
    lo=base*model['softness'];hi=base.copy();seen=np.zeros(E,dtype=bool)
    kl=inv(matrix(model,lo).toarray(),check_finite=False)
    kh=inv(matrix(model,hi).toarray(),check_finite=False)
    rng=np.random.default_rng(seed)
    hist=[];selected=[];max_queries=E if max_queries is None else max_queries
    bad=0
    for step in range(max_queries+1):
        ul,vl,rl=edge_values(kl,m,a,b);uh,vh,rh=edge_values(kh,m,a,b)
        Fmax=float(m@ul);Fmin=float(m@uh)
        if step%16==0 or Fmax/Fmin<=1+rtol or step==max_queries:
            hist.append({'queries':step,'lower':Fmin,'upper':Fmax,'ratio':Fmax/Fmin,
                         'seconds':time.perf_counter()-start})
        if Fmax/Fmin<=1+rtol or step==max_queries:break
        width=hi-lo
        if policy=='minimax':
            improve_if_high=width*vl**2/(1+width*rl)
            denom=1-width*rh
            improve_if_low=width*vh**2/np.maximum(denom,1e-300)
            score=np.minimum(improve_if_high,improve_if_low)
            score[seen]=-1
            e=int(np.argmax(score))
        elif policy=='relative':
            from relative_query import worst_relative
            worst,_=worst_relative(Fmax,Fmin,vl,vh,rl,rh,width)
            worst[seen]=np.inf;e=int(np.argmin(worst))
        elif policy=='pessimistic':
            score=width*vl**2/(1+width*rl);score[seen]=-1;e=int(np.argmax(score))
        elif policy=='optimistic':
            score=width*vh**2/np.maximum(1-width*rh,1e-300);score[seen]=-1;e=int(np.argmax(score))
        elif policy=='random':
            e=int(rng.choice(np.flatnonzero(~seen)))
        else:raise ValueError(policy)
        observed=float(oracle(e));observations.append(observed)
        if not model['softness'] <= observed <= 1.:raise ValueError('oracle violates supplied envelope')
        value=base[e]*observed # sole rate-oracle access in the learner
        selected.append(e)
        update(kl,a[e],b[e],value-lo[e])
        update(kh,a[e],b[e],value-hi[e])
        lo[e]=hi[e]=value;seen[e]=True
        if (step+1)%refresh==0:
            kl=inv(matrix(model,lo).toarray(),check_finite=False)
            kh=inv(matrix(model,hi).toarray(),check_finite=False)
    # Fresh solves avoid reporting accumulated rank-update error as a certificate.
    Fl=float(m@spsolve(matrix(model,hi),m));Fu=float(m@spsolve(matrix(model,lo),m))
    return {'policy':policy,'queries':len(selected),'possible_edges':E,'states':N,
            'lower':Fl,'upper':Fu,'ratio':Fu/Fl,'seconds':time.perf_counter()-start,
            'history':hist,'selected_edges':selected,'observed_facilitations':observations,'queried_dimensions':np.bincount(model['dims'][selected],minlength=model['L']).tolist(),
            'max_relative_row_residual_lower':float(np.max(np.abs(matrix(model,hi)@spsolve(matrix(model,hi),m)-m)/m)),
            'max_relative_row_residual_upper':float(np.max(np.abs(matrix(model,lo)@spsolve(matrix(model,lo),m)-m)/m))}

if __name__=='__main__':
    output=[]
    for L,q,soft in [(8,.1,1e-4),(9,.08,1e-5),(10,.05,1e-6)]:
        model=soft_east(L,q,soft)
        t=time.perf_counter(); c=model['base']*model['fac']
        truth=float(model['m']@spsolve(matrix(model,c),model['m']))
        ref_seconds=time.perf_counter()-t
        print('MODEL',L,q,soft,len(model['m']),len(c),'truth',truth,'solve secs',ref_seconds,flush=True)
        runs=[]
        for policy in ['minimax','optimistic','pessimistic','random']:
            r=run(model,policy)
            runs.append(r)
            print(policy,'queries',r['queries'],'ratio',r['ratio'],'time',r['seconds'],'bracket',r['lower'],r['upper'],flush=True)
        output.append({'L':L,'q':q,'softness':soft,'truth':truth,'direct_solve_seconds':ref_seconds,
                       'hidden_chain_order':[int(x) for x in model['order']],'runs':runs})
        with open(str(ROOT / 'probe_results.json'),'w') as f:json.dump(output,f,indent=2)
