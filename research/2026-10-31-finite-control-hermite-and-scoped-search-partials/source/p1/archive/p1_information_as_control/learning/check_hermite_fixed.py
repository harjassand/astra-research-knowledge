"""Independent checks of the Hermite sensing hierarchy's fixed-design bound.

Finite floating-point checks supplement the proof. Cubic checks also integrate
the conditional expectation directly from Gaussian moments, independently of
the tensor contraction formula, using degree-six-exact Gaussian quadrature.
"""
from itertools import permutations, product
from math import factorial, prod, sqrt, pi
from pathlib import Path
import json
import numpy as np


def indices(r,p):
    if r==1:
        yield (p,)
    else:
        for first in range(p,-1,-1):
            for rest in indices(r-1,p-first):
                yield (first,)+rest


def tensor(r,p,c):
    aa=list(indices(r,p)); m=len(aa); d=p+1; n=r+m
    t=np.zeros((n,)*d)
    for j,a in enumerate(aa):
        slots=[i for i,k in enumerate(a) for _ in range(k)]+[r+j]
        coefficient=c[j]*sqrt(prod(factorial(k) for k in a))/(factorial(d)*sqrt(m))
        for entry in set(permutations(slots)):
            t[entry]=coefficient
    return t,aa


def contract(t,l):
    d=t.ndim
    old="abcdef"[:d]; new="ijklmn"[:d]
    expression=old+","+",".join(old[j]+new[j] for j in range(d))+"->"+new
    return np.einsum(expression,t,*([l]*d),optimize=True)


def posterior_factor(measurements,noise):
    h=measurements.T@measurements
    values,vectors=np.linalg.eigh(h)
    keep=values>1e-10
    values=values[keep]; vectors=vectors[:,keep]
    return vectors*np.sqrt(values/(values+noise))


def grid4(q):
    nodes,weights=np.polynomial.hermite.hermgauss(4)
    nodes=nodes*sqrt(2); weights=weights/sqrt(pi)
    for ix in product(range(4),repeat=q):
        yield np.array([nodes[i] for i in ix]),prod(weights[i] for i in ix)


def cubic_conditional_mean(mean,covariance,r,aa,c):
    total=0.0
    for j,a in enumerate(aa):
        ii=[i for i,k in enumerate(a) for _ in range(k)]
        i,k=ii; v=r+j
        if i==k:
            value=((mean[i]**2+covariance[i,i]-1)*mean[v]
                   +2*mean[i]*covariance[i,v])/sqrt(2)
        else:
            value=(mean[i]*mean[k]*mean[v]+covariance[i,k]*mean[v]
                   +mean[i]*covariance[k,v]+mean[k]*covariance[i,v])
        total+=c[j]*value
    return total/sqrt(len(aa))


def main():
    rng=np.random.default_rng(20261101)
    out=dict(seed=20261101,normalization_checks=0,noiseless_mixed_design_checks=0,
             noisy_mixed_design_checks=0,independent_cubic_quadrature_checks=0,
             max_normalization_error=0.0,max_cubic_quadrature_error=0.0,
             max_fixed_bound_excess=0.0)
    for r,p in ((2,1),(3,1),(2,2),(3,2),(4,2),(2,3),(3,3)):
        aa=list(indices(r,p)); m=len(aa); n=r+m; d=p+1
        c=rng.uniform(0.8,1.2,size=m)
        t,_=tensor(r,p,c)
        variance=float(np.mean(c*c))
        error=abs(factorial(d)*np.sum(t*t)-variance)
        out["max_normalization_error"]=max(out["max_normalization_error"],float(error))
        assert error<1e-12
        out["normalization_checks"]+=1
        for q in sorted(set((1,2,min(3,n),n-1,n))):
            for _ in range(3):
                l=np.linalg.qr(rng.normal(size=(n,n)))[0][:,:q]
                gain=float(factorial(d)*np.sum(contract(t,l)**2))
                bound=min(variance,d*np.max(c*c)*q/m)
                excess=gain-bound
                out["max_fixed_bound_excess"]=max(out["max_fixed_bound_excess"],excess)
                assert excess<1e-10
                out["noiseless_mixed_design_checks"]+=1
                observations=rng.normal(size=(q,n))
                observations/=np.linalg.norm(observations,axis=1,keepdims=True)
                for noise in (0.01,0.5,2.0):
                    l=posterior_factor(observations,noise)
                    gain=float(factorial(d)*np.sum(contract(t,l)**2))
                    bound=min(variance,d*np.max(c*c)*q/(m*(1+noise)))
                    excess=gain-bound
                    out["max_fixed_bound_excess"]=max(out["max_fixed_bound_excess"],excess)
                    assert excess<1e-10
                    out["noisy_mixed_design_checks"]+=1
    r,p=2,2; aa=list(indices(r,p)); m=len(aa); n=r+m
    c=np.array([0.9,1.2,-0.8]); t,_=tensor(r,p,c)
    for q in (1,2,3):
        for noise in (0.0,0.1,1.0):
            for _ in range(3):
                observations=rng.normal(size=(q,n))
                observations/=np.linalg.norm(observations,axis=1,keepdims=True)
                l=posterior_factor(observations,noise)
                covariance=np.eye(n)-l@l.T
                predicted=6*np.sum(contract(t,l)**2)
                measured=0.0
                for y,weight in grid4(l.shape[1]):
                    conditional=cubic_conditional_mean(l@y,covariance,r,aa,c)
                    measured+=weight*conditional**2
                error=float(abs(measured-predicted))
                out["max_cubic_quadrature_error"]=max(out["max_cubic_quadrature_error"],error)
                assert error<1e-10
                out["independent_cubic_quadrature_checks"]+=1
    out["status"]="PASS"
    Path(__file__).with_name("check_hermite_fixed_results.json").write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps(out,indent=2))


if __name__=="__main__":
    main()
