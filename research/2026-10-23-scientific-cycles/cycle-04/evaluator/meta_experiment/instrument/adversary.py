"""Finite admissible-witness search for an explicitly declared operator claim.

Never certifies an upper bound, asymptotic claim, or physical performance.
All operator outputs below are witnessed LOWER estimates. Floating-point
admissibility checks produce candidates for an independent rigorous check.
Root-built experimental scientific instrument; development cost is additional.
"""
import argparse
import json
from pathlib import Path
import time
import numpy as np


def softmax(z):
    w = np.exp(np.asarray(z)-np.max(z))
    return w/w.sum()


def kernel(pi, q, Q, eta, alpha=.5):
    logq, logpi = np.log(q), np.log(pi)
    lw = logpi-logq
    G = q[None, :]*np.exp(np.minimum(0, lw[None, :]-lw[:, None]))
    L = Q*np.exp(np.minimum(0, eta*(logq[None, :]-logq[:, None])))
    L *= np.exp(np.minimum(0, logpi[None, :]-logpi[:, None]
                          -eta*(logq[None, :]-logq[:, None])))
    np.fill_diagonal(G, 0)
    np.fill_diagonal(L, 0)
    np.fill_diagonal(G, 1-G.sum(1))
    np.fill_diagonal(L, 1-L.sum(1))
    return (np.eye(len(q))+alpha*G+(1-alpha)*L)/2


def witnessed_norm(T, p, rng):
    """Nonnegative explicit trial vectors; no upper-bound or optimizer claim."""
    starts = [np.ones(len(T))]
    starts += list(np.eye(len(T)))
    starts += [np.exp(rng.uniform(-5, 0, len(T)))]
    best = (-np.inf, None)
    for v in starts:
        v = v/(np.sum(v**p)**(1/p))
        for _ in range(25):
            w = v@T
            ratio = np.sum(w**p)**(1/p)
            if ratio > best[0]:
                best = (float(ratio), v.copy())
            grad = T@(np.maximum(w, 1e-300)**(p-1))
            lg = np.log(np.maximum(grad, 1e-300))/(p-1)
            new = np.exp(lg-lg.max())
            new /= np.sum(new**p)**(1/p)
            if np.max(np.abs(new-v)) < 1e-11:
                break
            v = new
    return best


def fixed_Q(m, kind):
    Q = np.zeros((m+1, m+1))
    if kind == 'complete':
        Q[:m, :m] = 1/m
    elif kind == 'path':
        for j in range(m-1):
            Q[j,j+1] = Q[j+1,j] = .5
    elif kind == 'star':
        for j in range(1,m):
            Q[0,j] = Q[j,0] = 1/(m-1)
    else:
        for j in range(0,m-1,2):
            Q[j,j+1] = Q[j+1,j] = 1
    for j in range(m+1):
        Q[j,j] += 1-Q[j].sum()
    return Q


def evaluate(q, pi, Q, eta, c, h, rng):
    assert np.all(q>0) and np.all(pi>0)
    assert np.max(np.abs(Q-Q.T)) < 1e-12
    assert np.max(np.abs(Q.sum(1)-1)) < 1e-12 and Q.min() >= -1e-15
    kl = float(pi@(np.log(pi)-np.log(q)))
    if kl > 1+1e-12:
        return None
    C = kernel(pi,q,Q,eta)
    assert np.min(C)>-1e-14 and np.max(abs(C.sum(1)-1))<1e-12
    assert np.max(abs(pi[:,None]*C-pi[None,:]*C.T))<1e-12
    ids = np.flatnonzero(pi/q<h)
    if not len(ids):
        return None
    theta = c*min(eta,.5)
    p = 1/(1-theta)
    D = q[ids]**theta
    T = C[np.ix_(ids,ids)]*D[:,None]/D[None,:]
    val, v = witnessed_norm(T,p,rng)
    return {'candidate_only':True,'K':1,'alpha':.5,'h':h,'c':c,'eta':eta,
            'theta':theta,'p':p,'q':q.tolist(),'pi':pi.tolist(),'Q':Q.tolist(),
            'KL_float':kl,'unsafe_indices':ids.tolist(),'C_AA':C[np.ix_(ids,ids)].tolist(),
            'T':T.tolist(),'trial_v':v.tolist(),'witnessed_ratio_float':val,
            'killed_row_sums':C[np.ix_(ids,ids)].sum(1).tolist(),
            'claims':['explicit trial-vector lower estimate only',
                      'floating admission, not outward-rounded certification',
                      'no conditional renormalization','no asymptotic conclusion']}


def main():
    a=argparse.ArgumentParser()
    a.add_argument('--queries',type=int,default=600)
    a.add_argument('--seed',type=int,default=1729)
    a.add_argument('--c',type=float,default=.5)
    a.add_argument('--h',type=float,default=.001)
    a.add_argument('--out',type=Path,required=True)
    args=a.parse_args()
    args.out.mkdir(exist_ok=True,parents=True)
    rng=np.random.default_rng(args.seed)
    start=time.perf_counter();cpu=time.process_time();best=None;accepted=0
    with (args.out/'queries.jsonl').open('w') as log:
        for k in range(args.queries):
            m=int(rng.choice([2,3,4,6]))
            eta=float(rng.choice([1,.5,.2,.1,.05,.02]))
            b=float(rng.uniform(.1,.62))
            qA=b*softmax(rng.uniform(-min(100,8/eta),0,m))
            q=np.r_[qA,1-b]
            piA=qA*args.h*np.exp(rng.uniform(-90,-.01,m))
            pi=np.r_[piA,1-piA.sum()]
            kind=str(rng.choice(['complete','path','star','pairs']))
            Q=fixed_Q(m,kind)
            row=evaluate(q,pi,Q,eta,args.c,args.h,rng)
            if row is None:
                log.write(json.dumps({'query':k,'rejected':'KL'})+'\n');continue
            row['query']=k;row['fixed_Q_family']=kind;accepted+=1
            log.write(json.dumps(row)+'\n')
            if best is None or row['witnessed_ratio_float']>best['witnessed_ratio_float']:
                best=row
    if best is not None:
        (args.out/'best_candidate.json').write_text(json.dumps(best,indent=2)+'\n')
    costs={'queries':args.queries,'accepted':accepted,'wall_s':time.perf_counter()-start,
           'cpu_s':time.process_time()-cpu,'seed':args.seed,'development_cost_included':False,
           'interpretation':'Search output does not certify the candidate or universal bounds.'}
    (args.out/'COSTS.json').write_text(json.dumps(costs,indent=2)+'\n')
    print(json.dumps({'costs':costs,'best_witnessed_ratio':None if best is None else best['witnessed_ratio_float']}))


if __name__=='__main__':
    main()
