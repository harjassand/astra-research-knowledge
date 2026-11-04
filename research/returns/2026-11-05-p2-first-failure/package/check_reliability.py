"""Finite diagnostics for the 2026-11-05 reliability research note.

Floating-point checks, not formal verification. The general theorem invokes
Karger's static FPRAS. This file does not implement that general static oracle.
"""
import json, math
from pathlib import Path
import numpy as np
from scipy.linalg import solve, expm

OUT = Path(__file__).resolve().parent
RNG = np.random.default_rng(20261105)

def full_model(a, b, bad):
    m = len(a); size = 1 << m
    Q = np.zeros((size, size)); pi = np.ones(size)
    for x in range(size):
        for i in range(m):
            down = bool(x & (1 << i))
            rate = b[i] if down else a[i]
            Q[x, x ^ (1 << i)] += rate
            Q[x, x] -= rate
            pi[x] *= (a[i] if down else b[i]) / (a[i] + b[i])
    safe = np.flatnonzero(~np.array([bad(x) for x in range(size)]))
    B = np.flatnonzero(np.array([bad(x) for x in range(size)]))
    h = solve(-Q[np.ix_(safe, safe)], np.ones(len(safe)))
    return Q, pi, safe, B, h

def is_disconnected(x, vertices, edges):
    seen = {0}; stack = [0]
    while stack:
        u = stack.pop()
        for i, (v,w) in enumerate(edges):
            if x & (1 << i): continue
            if v == u and w not in seen: seen.add(w); stack.append(w)
            if w == u and v not in seen: seen.add(v); stack.append(v)
    return len(seen) != vertices

def sensitivities(a,b,bad):
    Q,pi,safe,B,h = full_model(a,b,bad)
    hfull = np.zeros(len(Q)); hfull[safe] = h
    start = int(np.flatnonzero(safe==0)[0]); M = h[start]
    e = np.zeros(len(safe)); e[start] = 1
    adj = solve(-Q[np.ix_(safe,safe)].T,e)
    sa=[]; sb=[]
    for i in range(len(a)):
        da=[]; db=[]
        for x in safe:
            change=hfull[x^(1<<i)]-hfull[x]
            da.append(0 if x&(1<<i) else a[i]*change)
            db.append(b[i]*change if x&(1<<i) else 0)
        sa.append(float(adj@da/M)); sb.append(float(adj@db/M))
    return M,np.array(sa),np.array(sb)

def deadline(Q,safe,B,t):
    # Read the failure coordinate directly, avoiding 1-survival cancellation.
    G=np.zeros((len(safe)+1,len(safe)+1))
    G[:-1,:-1]=Q[np.ix_(safe,safe)]
    G[:-1,-1]=Q[np.ix_(safe,B)].sum(axis=1)
    start=int(np.flatnonzero(safe==0)[0])
    return float(expm(t*G)[start,-1])

def random_checks():
    count=0; mean_pairs=0; cdf_pairs=0
    worst_sign=0.; worst_unit=0.; worst_sum=0.; worst_l1=0.
    largest_mean_fraction=0.; largest_cdf_fraction=0.
    for m in range(2,7):
        for case in range(25):
            cuts=RNG.integers(1,1<<m,size=int(RNG.integers(1,10))).tolist()
            bad=lambda x: any((x&c)==c for c in cuts)
            a=np.exp(RNG.uniform(-1.5,1.5,m)); b=np.exp(RNG.uniform(-1.5,1.5,m))
            M,sa,sb=sensitivities(a,b,bad)
            worst_sign=max(worst_sign,float(sa.max()),float(-sb.min()))
            worst_unit=max(worst_unit,float((-sa-1).max()))
            worst_sum=max(worst_sum,abs(float(sa.sum()+sb.sum()+1)))
            worst_l1=max(worst_l1,float(np.abs(sa).sum()+np.abs(sb).sum()-(2*m-1)))
            da=RNG.uniform(-.2,.2,m); db=RNG.uniform(-.2,.2,m)
            eta=float(max(np.abs(da).max(),np.abs(db).max()))
            ap=a*np.exp(da); bp=b*np.exp(db)
            Mp=sensitivities(ap,bp,bad)[0]
            frac=abs(math.log(Mp/M))/((2*m-1)*eta)
            largest_mean_fraction=max(largest_mean_fraction,frac)
            assert frac<=1+1e-8; mean_pairs+=1
            if m<=5 and case<10:
                Q,_,safe,B,_=full_model(a,b,bad)
                Qp,_,sp,Bp,_=full_model(ap,bp,bad)
                for t in (.02,.2,2.,20.):
                    f=deadline(Q,safe,B,t); fp=deadline(Qp,sp,Bp,t)
                    frac=abs(math.log(fp/f))/(2*m*eta)
                    largest_cdf_fraction=max(largest_cdf_fraction,frac)
                    assert frac<=1+1e-8; cdf_pairs+=1
            assert np.all(sa>=-1-1e-8) and np.all(sa<=1e-8)
            assert np.all(sb>=-1e-8); count+=1
    return dict(models=count,mean_finite_change_checks=mean_pairs,
                deadline_finite_change_checks=cdf_pairs,
                max_sign_violation=worst_sign,max_unit_violation=worst_unit,
                max_euler_residual=worst_sum,max_l1_violation=worst_l1,
                largest_fraction_of_mean_bound=largest_mean_fraction,
                largest_fraction_of_cdf_bound=largest_cdf_fraction)

def k4_example():
    edges=[(i,j) for i in range(4) for j in range(i+1,4)]
    a=np.array([.012,.008,.015,.010,.007,.011])
    b=np.array([1.,.8,1.2,.9,1.1,.95])
    bad=lambda x:is_disconnected(x,4,edges)
    Q,pi,safe,B,h=full_model(a,b,bad)
    Lambda=float((a+b).sum()); gamma=float((a+b).min()); g=gamma/Lambda
    eta=.01; H=sum(1/j for j in range(1,len(a)+1))
    k=math.ceil((H+math.log(1/eta)+2)/g)
    P=np.eye(len(Q))+Q/Lambda; PA=P[np.ix_(safe,safe)]
    survival=np.linalg.matrix_power(PA,k)@np.ones(len(safe))
    p=float(pi[B].sum())
    z=float((pi[B]/p)@P[np.ix_(B,safe)]@survival)
    d=p*z; M=float(h[np.flatnonzero(safe==0)[0]])
    Mpi=float(pi[safe]@h)
    flux=float(pi[B]@Q[np.ix_(B,safe)]@np.ones(len(safe)))
    return dict(vertices=4,edges=6,states=64,p=p,g=g,k=k,
                rare_threshold=eta/(2*(k+1)),rare_gate_passes=p<=eta/(2*(k+1)),
                conditional_success=z,conditional_success_lower=g*(1-2*eta),
                exact_generator_mean=M,stationary_mean=Mpi,
                inverse_frequency=1/flux,reactive_flux_mean=1/(Lambda*d),
                reactive_relative_error=1/(Lambda*d*M)-1,
                initial_mean_excess=M-Mpi,initial_excess_bound=H/gamma)

def chattering_parallel(n,eta=.01):
    states=[(j,f) for j in range(n+1) for f in (0,1)]
    idx={s:i for i,s in enumerate(states)}; size=len(states)
    Q=np.zeros((size,size)); pi=np.zeros(size)
    for z,(j,f) in enumerate(states):
        pi[z]=math.comb(n,j)/2**(n+1)
        for target,rate in [((j+1,f),n-j),((j-1,f),j),((j,1-f),n*n)]:
            if rate: Q[z,idx[target]]+=rate; Q[z,z]-=rate
    B=idx[(n,1)]; safe=np.array([i for i in range(size) if i!=B])
    h=solve(-Q[np.ix_(safe,safe)],np.ones(len(safe)))
    M=float(h[np.flatnonzero(safe==idx[(0,0)])[0]])
    Lambda=2*n+2*n*n; g=2/Lambda
    H=sum(1/j for j in range(1,n+2)); k=math.ceil((H+math.log(1/eta)+2)/g)
    P=np.eye(size)+Q/Lambda
    p=float(pi[B]); D=float(pi[B]*P[B,safe]@np.linalg.matrix_power(P[np.ix_(safe,safe)],k)@np.ones(len(safe)))
    flux=p*(n+n*n)
    return dict(slow_edges=n,total_edges=n+1,rate_contrast=n*n,
                configurations=2**(n+1),lumped_states=size,p=p,k=k,
                rare_gate_passes=p<=eta/(2*(k+1)),
                mean=M,inverse_stationary_frequency=1/flux,
                frequency_undercount_factor=M*flux,
                reactive_flux_mean=1/(Lambda*D),
                reactive_relative_error=1/(Lambda*D*M)-1,
                conditional_success=D/p,
                conditional_success_lower=g*(1-2*eta))

def two_edge_counterexample():
    records=[]
    for a in (.1,.01,.001,.0001):
        Q,pi,safe,B,h=full_model(np.array([a,1.]),np.ones(2),lambda x:x==3)
        numeric=float(h[0]); exact=(a*a+3*a+4)/(a*(a+3))
        records.append(dict(a=a,mean_formula=exact,mean_generator=numeric,
                            relative_difference=numeric/exact-1,
                            inverse_frequency=(1+a)/a,mean_times_frequency=exact*a/(1+a)))
    return records

def main():
    result={"status":"floating_point_diagnostics_not_formal_verification",
            "seed":20261105,"random_checks":random_checks(),
            "heterogeneous_K4":k4_example(),
            "two_edge_counterexample":two_edge_counterexample(),
            "chattering_parallel":[chattering_parallel(n) for n in (4,8,12,16,20,24)]}
    (OUT/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__': main()
