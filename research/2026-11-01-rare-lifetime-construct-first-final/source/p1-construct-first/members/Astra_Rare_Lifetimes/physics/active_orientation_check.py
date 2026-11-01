"""Independent finite check of a controlled orientation completion.

Not a proof and not a thermal implementation. Uses scipy for finite CTMCs.
Run: python research_work/physics/active_orientation_check.py
"""
from itertools import product
from pathlib import Path
import json
import numpy as np
from scipy.linalg import expm

def generator(off):
    q = np.array(off, dtype=float)
    np.fill_diagonal(q, -q.sum(axis=1))
    return q

def stationary(q):
    a = q.T.copy()
    a[-1] = 1
    b = np.zeros(len(q)); b[-1] = 1
    return np.linalg.solve(a, b)

def reversed_generator(q, p):
    return (q.T * p[None, :]) / p[:, None]

def lift(q, p, epsilon, kappa, clock):
    n = len(q)
    qstar = reversed_generator(q, p)
    l = np.zeros((4*n,4*n))
    index = lambda x,s,h: 4*x+2*s+h
    a, b = kappa*epsilon, kappa*(1-epsilon)
    for x,s,h in product(range(n),range(2),range(2)):
        i = index(x,s,h)
        qq = q if s == 0 else qstar
        for y in range(n):
            if y != x:
                l[i,index(y,s,h)] = qq[x,y]
        flip = a if s == 0 else b
        l[i,index(x,1-s,h)] = flip
        l[i,index(x,s,1-h)] = clock + q[x,x] - flip
        l[i,i] = -clock
    rho = np.array([p[x]*([1-epsilon,epsilon][s])/2
                    for x,s,h in product(range(n),range(2),range(2))])
    theta = np.array([index(x,1-s,h)
                      for x,s,h in product(range(n),range(2),range(2))])
    return l,rho,theta

def intrinsic(q,p,theta):
    result = 0.
    for i in range(len(q)):
        for j in range(len(q)):
            if i!=j and q[i,j]>0:
                result += p[i]*q[i,j]*np.log(q[i,j]/q[theta[j],theta[i]])
        result += p[i]*(-q[theta[i],theta[i]]+q[i,i])
    return result

def active_tv(qs,ls,p0,rho0,dt,steps):
    """Exact finite grid transcript enumeration, adapt action to visible history."""
    n = len(p0)
    ps = [expm(dt*q) for q in qs]
    pls = [expm(dt*l) for l in ls]
    masks = [np.repeat(np.arange(n)==x,4) for x in range(n)]
    histories = [(tuple([x]),p0[x],rho0*masks[x]) for x in range(n)]
    for k in range(steps):
        nxt=[]
        for hist,prob,rv in histories:
            # Feedback depends on both present state and full past count.
            u=(hist[-1]+sum(hist)+k)%len(qs)
            newrv=rv @ pls[u]
            for y in range(n):
                nxt.append((hist+(y,),prob*ps[u][hist[-1],y],newrv*masks[y]))
        histories=nxt
    return sum(abs(p-r.sum()) for _,p,r in histories)/2, len(histories)

def main():
    qs=[generator([[0,2,1],[1,0,2],[2,1,0]]),
        generator([[0,3,.5],[.25,0,1.5],[1,2,0]])]
    pis=[stationary(q) for q in qs]
    clock=max(max(-np.diag(q)) for q in qs)+1
    epsilon,kappa=1e-4,1e-6
    data=[lift(q,p,epsilon,kappa,clock) for q,p in zip(qs,pis)]
    ls=[d[0] for d in data]
    rows=[]
    for q,p,(l,rho,theta) in zip(qs,pis,data):
        c=clock+np.diag(q)
        exact=sum(p*(1-2*epsilon)*c*np.log((c-kappa*epsilon)/(c-kappa*(1-epsilon))))
        rows.append(dict(target_stationary=p.tolist(),
                         target_all_even_rate=intrinsic(q,p,np.arange(len(q))),
                         lifted_intrinsic_rate=intrinsic(l,rho,theta),
                         exact_formula=exact,
                         stationary_residual=float(np.max(np.abs(rho@l))),
                         row_residual=float(np.max(np.abs(l.sum(axis=1)))),
                         escape_clock_spread=float(np.ptp(-np.diag(l)))))
        assert np.max(np.abs(rho@l))<1e-12
        assert np.max(np.abs(l.sum(axis=1)))<1e-12
        assert abs(rows[-1]['lifted_intrinsic_rate']-exact)<1e-12
    dt,steps=.5,8
    tv,count=active_tv(qs,ls,pis[0],data[0][1],dt,steps)
    bound=epsilon+(1-epsilon)*(1-np.exp(-kappa*epsilon*dt*steps))
    assert tv <= bound+1e-12
    result=dict(epsilon=epsilon,kappa=kappa,clock=clock,models=rows,
                grid_transcripts=count,steps=steps,dt=dt,active_transcript_tv=tv,
                complete_continuous_transcript_bound=bound,
                note='Numerical check, not interval-certified; theorem supplies exact inequalities.')
    Path(__file__).with_name('active_orientation_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__': main()
