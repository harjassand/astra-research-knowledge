"""Restricted separable cone search for the original ABA Choi matrix.

PSD factors on the output and fixed real rank-one input factors.
Feasible floating output is only a candidate pending rational reconstruction.
"""
import argparse,json,time
from pathlib import Path
import cvxpy as cp
import numpy as np
from exact_rank import rational_model

def invsqrt(a):
    w,v=np.linalg.eigh(a)
    return (v*(1/np.sqrt(w)))@v.T

def whiten(j,d,e,steps=40):
    x=np.eye(d);y=np.eye(e)
    for _ in range(steps):
        t=j.reshape(d,e,d,e);f=invsqrt(np.einsum('iaja->ij',t))
        ff=np.kron(f,np.eye(e));j=ff@j@ff.T;x=f@x
        t=j.reshape(d,e,d,e);f=invsqrt(np.einsum('iaib->ab',t))
        ff=np.kron(np.eye(d),f);j=ff@j@ff.T;y=f@y
        scale=np.sqrt(np.trace(j));j/=scale**2;y/=scale
    return j,x,y

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--atoms',type=int,default=400)
    ap.add_argument('--iterations',type=int,default=10000);args=ap.parse_args()
    _,_,_,ji=rational_model();jt=float(np.trace(ji))
    j=np.array(ji,dtype=float)/jt;d,e=10,6;j,x,y=whiten(j,d,e)
    rng=np.random.default_rng(2723)
    vec=[np.eye(d)[i] for i in range(d)]
    vec += [np.eye(d)[i]+np.eye(d)[k] for i in range(d) for k in range(i+1,d)]
    vec += [np.eye(d)[i]-np.eye(d)[k] for i in range(d) for k in range(i+1,d)]
    vec += list(rng.normal(size=(args.atoms-len(vec),d)))
    vec=np.array(vec);vec/=np.linalg.norm(vec,axis=1,keepdims=True)
    pu=[(i,k) for i in range(d) for k in range(i,d)]
    qu=[(a,b) for a in range(e) for b in range(a,e)]
    p=np.array([[v[i]*v[k] for i,k in pu] for v in vec])
    target=np.array([[j[i*e+a,k*e+b] for a,b in qu] for i,k in pu])
    factors=[cp.Variable((e,e),symmetric=True) for _ in vec]
    v=cp.vstack([cp.hstack([b[a,c] for a,c in qu]) for b in factors])
    t=cp.Variable();constraints=[p.T@v==target]
    constraints += [b-t*np.eye(e) >> 0 for b in factors]
    prob=cp.Problem(cp.Maximize(t),constraints)
    before=time.monotonic()
    prob.solve(solver='SCS',eps=1e-6,max_iters=args.iterations,verbose=False)
    after=time.monotonic()
    out=dict(status=prob.status,margin=None if t.value is None else float(t.value),
             atoms=len(vec),seconds=after-before,
             solver_iterations=prob.solver_stats.num_iters)
    if t.value is not None:
        bs=np.array([b.value for b in factors]);res=np.einsum('ni,nj,nab->iajb',vec,vec,bs)
        out.update(residual=float(np.max(abs(res-j.reshape(d,e,d,e)))),
                   min_factor_eig=float(min(np.linalg.eigvalsh(b)[0] for b in bs)))
        np.savez(Path(__file__).with_name('sep_candidate.npz'),vec=vec,bs=bs,x=x,y=y,j=j)
    Path(__file__).with_name('sep_sdp.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
