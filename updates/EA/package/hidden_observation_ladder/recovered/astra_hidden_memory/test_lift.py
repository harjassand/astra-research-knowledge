"""Exact algebra and numerical falsification tests for the hidden-memory lift.
No general proof or historical-priority claim is made by these tests.
"""
from __future__ import annotations
from fractions import Fraction as F
import json
from pathlib import Path
import numpy as np


def setup(r: int):
    if r < 1:
        raise ValueError('r must be a positive integer')
    if r == 1:
        d, f = 2, 1
        def theta_char(a):
            return a ^ ((a >> 1 & 1) * 1)
        c = [2]
    else:
        d, f = max(4, 3 + (r - 2).bit_length()), 1
        def theta_char(a):
            return a ^ ((a >> 2 & 1) * 1) ^ ((a >> 3 & 1) * 2)
        c = [None] * (2*r - 1)
        c[r-1] = 4
        for j in range(r-1):
            z = (j & 1) << 2
            z |= (j >> 1) << 4
            a = 8 ^ z
            c[j] = a
            c[2*r - 2 - j] = f ^ theta_char(a)
    target = [f ^ a for a in c] + [f]
    source = [f] + c
    edges = dict(zip(source, target))
    used = {0, f, *c, *(f ^ a for a in c)}
    assert len(used) == 4*r
    assert max(used) < 2**d
    assert 2**d <= 16*r
    for a, b in edges.items():
        assert edges[theta_char(b)] == theta_char(a)
    return d, f, c, edges, theta_char


def Aapply(v, edges):
    out = {}
    for a, coef in v.items():
        if a in edges:
            b = edges[a]
            out[b] = out.get(b, F(0)) + coef
    return {a:c for a,c in out.items() if c}


def propagate(v, edges, eps, t, z):
    out = {a: coef * (1 if a == 0 else z) for a, coef in v.items()}
    w = Aapply(v, edges)
    w2 = Aapply(w, edges)
    for a, coef in w.items(): out[a] = out.get(a, F(0)) + z*eps*t*coef
    for a, coef in w2.items(): out[a] = out.get(a, F(0)) + z*eps**2*t**2*coef/2
    return {a:c for a,c in out.items() if c}


def moment(f, edges, eps, ts, zs):
    v = {f: F(1)}
    for t,z in zip(reversed(ts), reversed(zs)):
        v = propagate(v, edges, eps, t, z)
        v = {a ^ f: coef for a,coef in v.items()}
    return v.get(0,F(0))


def state_permutation(r):
    d, f, c, edges, theta = setup(r)
    return np.array([sum(((theta(1 << i) & x).bit_count() % 2) << i
                         for i in range(d)) for x in range(2**d)])


def dense(r):
    d,f,c,edges,theta = setup(r)
    n=2**d
    if 16*r*n+2*r > np.iinfo(np.int64).max:
        raise OverflowError("The dense NumPy export requires signed 64-bit matrix entries.")
    # Integer matrix equal to n*A; use Walsh characters directly.
    def chi(a):
        return np.array([1 if (a & x).bit_count()%2==0 else -1 for x in range(n)], dtype=np.int64)
    Araw=np.zeros((n,n),dtype=np.int64)
    for src,dst in edges.items(): Araw += np.outer(chi(dst),chi(src))
    Qnum=16*r*(np.ones((n,n),dtype=np.int64)-n*np.eye(n,dtype=np.int64))+Araw
    return Qnum, 16*r*n, Araw, chi(f)


def run():
    checks=0
    for r in range(1,33):
        d,f,c,edges,theta=setup(r)
        eps=F(1,16*r)
        for a in range(2**d):
            assert not Aapply(Aapply(Aapply({a:F(1)},edges),edges),edges)
            checks+=1
        for k in range(1,2*r+1):
            ts=[F((i%5)+1,(i%3)+2) for i in range(k-1)]
            zs=[F((i%4)+1,(i%4)+3) for i in range(k-1)]
            assert moment(f,edges,eps,ts,zs)==moment(f,{},eps,ts,zs)
            checks+=1
        k=2*r+1
        ts=[F((i%3)+1,(i%2)+2) for i in range(k-1)]
        zs=[F((i%4)+1,(i%4)+3) for i in range(k-1)]
        target=eps**(2*r)
        for t,z in zip(ts,zs): target *= t*z
        assert moment(f,edges,eps,ts,zs)==target
        checks+=1
        # Exact linear-response inner product in the Walsh basis.
        Af=Aapply({f:F(1)},edges)
        Astarf={a:F(1) for a,b in edges.items() if b==f}
        assert len(Af)==len(Astarf)==1
        assert next(iter(Af))!=next(iter(Astarf))
        checks+=1
    dense_results=[]
    for r in range(1,10):
        Qnum,den,Araw,f=dense(r)
        n=len(Qnum)
        assert np.all(Qnum.sum(axis=0)==0) and np.all(Qnum.sum(axis=1)==0)
        off=Qnum[~np.eye(n,dtype=bool)]
        assert off.min()>=14*r and off.max()<=18*r
        assert np.all(Araw@Araw@Araw==0)
        assert np.trace(Araw@Araw.T)==n*n*(2*r)
        Q=Qnum/den
        pi=np.ones(n)/n
        sigma=0.
        for i in range(n):
            for j in range(i+1,n):
                a=Q[i,j]/n; b=Q[j,i]/n
                sigma+=(a-b)*np.log(a/b)
        assert 1/(144*r)<=sigma<=1/(112*r)
        dense_results.append({'r':r,'states':n,'sigma_floating':float(sigma),
                              'rate_ratio_max':float(off.max()/off.min())})
        checks+=4
    # Four-state explicit matrices for the illustrative eps=1/4 model.
    _,_,Araw,f=dense(1)
    n=4
    Qnum=4*(np.ones((n,n),dtype=int)-n*np.eye(n,dtype=int))+Araw
    results={'exact_assertions':checks,'tested_r':list(range(1,33)),
             'dense_cases':dense_results,
             'four_state_Q_numerator_eps_quarter':Qnum.tolist(),
             'four_state_Q_denominator_eps_quarter':16,
             'four_state_observable':f.tolist(),
             'status':'Exact finite algebra checks; entropy values numerical. Not general proof or priority review.'}
    with open(Path(__file__).resolve().parent/'check_results.json','w') as h: json.dump(results,h,indent=2)
    print(json.dumps(results,indent=2))

if __name__=='__main__': run()
