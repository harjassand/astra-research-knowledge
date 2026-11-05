"""Finite checks supplementing, not proving, the population theorems."""
from pathlib import Path
from itertools import product
import json
import math
import numpy as np
import sympy as sp


def exact_invariant():
    rho = [sp.Rational(1,5), sp.Rational(3,10), sp.Rational(1,2)]
    q = sp.Matrix([[0,2,0],[0,0,3],[5,0,0]])
    t = [sp.Rational(2),sp.Rational(3),sp.Rational(5)]
    flow = sp.Matrix(3,3,lambda i,j: rho[i]*q[i,j]*t[i]/t[j])
    g = [(sum(flow[i,j] for j in range(3))-
          sum(flow[j,i] for j in range(3)))/2 for i in range(3)]
    assert sum(g)==0
    cases={}
    for replicas in [1,2,3,4]:
        count=0
        for states in product(range(3),repeat=replicas):
            transport=2*sum(g[i]/rho[i] for i in states)
            jumps=sum((sum(flow[j,i] for j in range(3))-
                       sum(flow[i,j] for j in range(3)))/rho[i] for i in states)
            assert sp.cancel(transport+jumps)==0
            count+=1
        cases[replicas]=count
    return cases


def values(q,rho,u):
    edge=q*np.exp((u[:,None]-u[None,:])/2)
    Q=edge-np.diag(edge.sum(axis=1))
    return Q,np.sum(rho[:,None]*edge),-(rho@Q)/2


def finite_jump_checks():
    rng=np.random.default_rng(20261105)
    worst=0.;max_ratio=0.;jump_cases=0;drift_cases=0
    for n in [2,3,5]:
        for kind in ["cycle","dense"]:
            q=np.zeros((n,n))
            if kind=="cycle":
                for i in range(n):q[i,(i+1)%n]=rng.uniform(.5,2.)
            else:
                q=rng.uniform(.5,2.,(n,n));np.fill_diagonal(q,0)
            rho=rng.uniform(1.,2.,n);rho/=rho.sum();gain=.7
            us=np.zeros(n)
            for iteration in range(100):
                _,F,g=values(q,rho,us)
                if np.linalg.norm(g)<1e-12:break
                flow=rho[:,None]*q*np.exp((us[:,None]-us[None,:])/2)
                Hess=(np.diag(flow.sum(axis=1)+flow.sum(axis=0))-flow-flow.T)/4
                step=np.r_[np.linalg.solve(Hess[:-1,:-1],g[:-1]),0.]
                size=1.
                while values(q,rho,us-size*step)[1]>F-1e-4*size*(g@step):size/=2
                us-=size*step
            us-=rho@us
            _,Fs,gs=values(q,rho,us);assert np.linalg.norm(gs)<1e-7
            r=rho.min();positive=q[q>0];ub=max(abs(us))+1
            Qb=(n-1)*positive.max()*math.exp(ub)
            m=r*positive.min()*math.exp(-ub)/(4*n*(n-1));a=gain*r*m
            eps=min(m/2,gain/4,a/(2*(gain/r+(2*Qb)**2/(4*m))))
            H=2*gain/r
            for rep in range(100):
                N=2000;p=rng.multinomial(N,rho)/N
                u=us+rng.uniform(-.1,.1,n);u-=rho@u
                x=p-rho;y=u-us;Q,F,g=values(q,rho,u);ratio=p/rho
                velocity=gain*(ratio-1);pdot=p@Q
                W=F-Fs+gain/2*np.sum(p*np.log(ratio))+eps*(x@y)
                gp=gain/2*(np.log(ratio)+1)+eps*y;gu=g+eps*x
                actual=gp@pdot+gu@velocity
                phi=ratio[:,None]*np.log(ratio[:,None]/ratio[None,:])-ratio[:,None]+ratio[None,:]
                edge=Q.copy();np.fill_diagonal(edge,0)
                cross=gain*np.sum(x*x/rho)+y@pdot
                expected=-gain/2*np.sum(rho[:,None]*edge*phi)+eps*cross
                worst=max(worst,abs(actual-expected))
                assert actual<=1e-10;drift_cases+=1;correction=0.
                for i,j in zip(*np.nonzero(q)):
                    v=np.zeros(n);v[i]-=1/N;v[j]+=1/N;pp=p+v
                    Wp=F-Fs+gain/2*np.sum(pp*np.log(pp/rho))+eps*((pp-rho)@y)
                    rem=Wp-W-gp@v
                    assert rem>=-1e-12 and rem<=H/N**2+1e-12
                    max_ratio=max(max_ratio,rem*N**2/H)
                    correction+=N*p[i]*Q[i,j]*rem;jump_cases+=1
                assert correction<=H*Qb/N+1e-10
    assert worst<1e-10
    return dict(negative_drift_cases=drift_cases,finite_jump_cases=jump_cases,
                max_identity_residual=worst,max_fraction_of_entropy_bound=max_ratio)


if __name__=="__main__":
    report=dict(exact_replica_invariant_cases=exact_invariant(),
                numerical_checks=finite_jump_checks(),
                scope="Finite supplementary algebra; no asymptotic or physical certification")
    Path(__file__).with_name("finite_population_checks.json").write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps(report,indent=2))
