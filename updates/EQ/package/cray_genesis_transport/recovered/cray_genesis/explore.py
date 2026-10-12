from __future__ import annotations
import itertools, time, json
from collections import defaultdict
import numpy as np
import sympy as sp
from scipy.linalg import lstsq

def subsets(items):
    items=tuple(items)
    return [frozenset(items[j] for j in range(len(items)) if k>>j&1) for k in range(1<<len(items))]

def canonical(A):
    if not A: return ()
    v=min(A)
    return tuple(sorted(x-v for x in A))

def poly_add(d, a, v):
    d[a] = d.get(a,0)+v
    if d[a] == 0: del d[a]

def dual_setup(r):
    outer=tuple(x for x in range(-r,r+2) if x not in (0,1))
    rate_pair=frozenset((-1,2))
    basis=[a for a in subsets(outer) if not rate_pair <= a]
    cols=[]; shapes=set()
    for a in basis:
        q={}
        for point,sign in [(0,1),(1,-1)]:
            poly_add(q,a|{point},sign)
            poly_add(q,a|{point}|rate_pair,-sign)
        col={}
        for a,v in q.items(): poly_add(col,canonical(a),v)
        shapes.update(col); cols.append(col)
    shapes=sorted(shapes,key=lambda a:(len(a),a)); lookup={x:i for i,x in enumerate(shapes)}
    B=sp.zeros(len(shapes),len(basis))
    for j,col in enumerate(cols):
        for a,v in col.items(): B[lookup[a],j]=v
    start=time.perf_counter(); ns=B.nullspace()
    N=sp.Matrix.hstack(*ns) if ns else sp.zeros(len(basis),0)
    print('DUAL_SETUP',r,'vars',len(basis),'constraints',len(shapes),'nullity',N.cols,'sec',time.perf_counter()-start,flush=True)
    assert B*N==sp.zeros(B.rows,N.cols)
    return basis,N

def dual_eval(basis,N,p,exact=False):
    pair=frozenset((-1,2)); n=len(basis)
    if exact:
        pp=sp.Rational(p)
        b=sp.Matrix([pp**len(a)-pp**len(a|pair) for a in basis])
        W=sp.Matrix(n,n,lambda i,j: pp**len(basis[i]|basis[j])-pp**len(basis[i]|basis[j]|pair))
        H=N.T*W*N; v=N.T*b
        z=H.inv()*v
        return (v.T*z)[0],N*z
    pp=float(p); NN=np.asarray(N,dtype=float)
    b=np.array([pp**len(a)-pp**len(a|pair) for a in basis])
    W=np.array([[pp**len(a|aa)-pp**len(a|aa|pair) for aa in basis] for a in basis])
    H=NN.T@W@NN; v=NN.T@b
    z=lstsq(H,v,cond=1e-13)[0]
    return float(v@z),NN@z

def grad_sum(A):
    d={}
    shifts=set(-a for a in A)|set(1-a for a in A)
    for x in shifts:
        s=frozenset(a+x for a in A)
        if (0 in s) == (1 in s): continue
        ss=(s-{0})|{1} if 0 in s else (s-{1})|{0}
        poly_add(d,ss,1); poly_add(d,s,-1)
    return d

def primal_setup(m):
    # All translation orbits contained in m consecutive sites; constants/singletons vanish.
    basis=[a|{0} for a in subsets(range(1,m)) if a]
    polys=[grad_sum(a) for a in basis]
    nonzero=[(a,p) for a,p in zip(basis,polys) if p]
    basis,polys=map(list,zip(*nonzero))
    # Centered-product polynomials have the same swap-difference representation.
    return basis,polys

def primal_eval(m,p,exact=False):
    basis,polys=primal_setup(m)
    if exact: p=sp.Rational(p)
    else: p=float(p)
    chi=p*(1-p)
    mu=[1,0,chi]; nu=[p,chi,p*(1-p)**2]
    def inner(a,b):
        outside=frozenset((-1,2))
        aa=a-outside; bb=b-outside
        if aa!=bb:return 0
        k=int(-1 in a)+int(-1 in b); l=int(2 in a)+int(2 in b)
        return chi**len(aa)*(mu[k]*mu[l]-nu[k]*nu[l])
    a_poly={frozenset((0,)):1,frozenset((1,)):-1}
    def ip(f,g):return sum(v*w*inner(a,b) for a,v in f.items() for b,w in g.items())/(2*chi)
    n=len(polys)
    if exact:
        H=sp.Matrix(n,n,lambda i,j:ip(polys[i],polys[j])); b=sp.Matrix([ip(f,a_poly) for f in polys])
        # H is positive definite modulo any polynomial gradient dependencies.
        sol=list(sp.linsolve((H,-b)))[0]
        free=set().union(*(s.free_symbols for s in sol))
        z=sp.Matrix([s.subs({t:0 for t in free}) for s in sol])
        U=1-p*p+(b.T*z)[0]
    else:
        H=np.array([[ip(f,g) for g in polys] for f in polys]); b=np.array([ip(f,a_poly) for f in polys])
        z=lstsq(H,-b,cond=1e-12)[0]
        U=float(1-p*p+b@z)
    return U,basis,z

if __name__=='__main__':
    out=[]
    for r in [1,2,3,4]:
        start=time.perf_counter();basis,N=dual_setup(r)
        for p in ['1/2','4/5','19/20']:
            value,coeff=dual_eval(basis,N,sp.Rational(p))
            print('LOWER',r,p,value,flush=True)
            out.append(dict(type='lower',r=r,p=p,value=value))
    for m in [4,5,6,7]:
        start=time.perf_counter()
        for p in ['1/2','4/5','19/20']:
            value,basis,z=primal_eval(m,sp.Rational(p))
            print('UPPER',m,p,value,'vars',len(basis),flush=True)
            out.append(dict(type='upper',m=m,p=p,value=value))
        print('TIME',m,time.perf_counter()-start,flush=True)
    from pathlib import Path
    with Path(__file__).with_name('exploratory_results.json').open('w') as f:json.dump(out,f,indent=2)
