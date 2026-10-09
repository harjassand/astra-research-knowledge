"""Exact rational checks of the coherent-flag and flat-projection identities.

This script checks finite identities with Fraction arithmetic. It is not a
proof assistant, a novelty check, or a certificate of all-copy positivity.
It also includes a known rank-three negative control to detect false
extensions beyond the rank-two target. Run with Python 3.10+ (stdlib only).
"""
from __future__ import annotations
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from typing import Dict, List, Tuple
import hashlib
import json
import random
import time

Digits = Tuple[int, ...]
Sparse = Dict[Tuple[Digits, Digits], F]
Matrix = List[List[F]]

def require(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(f'Exact audit failed: {label}')

def mm(a: Matrix, b: Matrix) -> Matrix:
    return [[sum((a[i][k]*b[k][j] for k in range(len(b))), F(0))
             for j in range(len(b[0]))] for i in range(len(a))]

def trans(a: Matrix) -> Matrix:
    return list(map(list, zip(*a)))

def plus(*matrices: Matrix) -> Matrix:
    return [[sum((a[i][j] for a in matrices), F(0))
             for j in range(len(matrices[0][0]))] for i in range(len(matrices[0]))]

def scale(s: F, a: Matrix) -> Matrix:
    return [[s*x for x in row] for row in a]

def outer(u: List[F], v: List[F]) -> Matrix:
    return [[x*y for y in v] for x in u]

def eye(n: int) -> Matrix:
    return [[F(i==j) for j in range(n)] for i in range(n)]

def sparse(a: Matrix, dims: Tuple[int,...]) -> Sparse:
    basis=list(product(*(range(d) for d in dims)))
    require(len(basis)==len(a)==len(a[0]), 'matrix dimensions')
    return {(basis[i],basis[j]):x for i,row in enumerate(a)
            for j,x in enumerate(row) if x}

def q_sparse(a: Sparse, sites: int) -> F:
    """Definition by all partial traces; does NOT use a flag formula."""
    result=F(0)
    for mask in range(1<<sites):
        traced=[i for i in range(sites) if mask>>i&1]
        kept=[i for i in range(sites) if not mask>>i&1]
        pt: Sparse={}
        for (r,c),x in a.items():
            if any(r[i]!=c[i] for i in traced):
                continue
            key=(tuple(r[i] for i in kept),tuple(c[i] for i in kept))
            pt[key]=pt.get(key,F(0))+x
        result+=F(-1,2)**len(traced)*sum((x*x for x in pt.values()),F(0))
    return result

def q(a: Matrix, dims: Tuple[int,...]) -> F:
    return q_sparse(sparse(a,dims),len(dims))

def flags(blocks: List[Tuple[Digits,Digits,Matrix]], dims: Tuple[int,...]) -> Sparse:
    out: Sparse={}
    for rflag,cflag,a in blocks:
        for (r,c),x in sparse(a,dims).items():
            key=(rflag+r,cflag+c)
            out[key]=out.get(key,F(0))+x
    return out

def householder(rng: random.Random,n: int) -> Matrix:
    v=[F(rng.randrange(-2,3)) for _ in range(n)]
    if not any(v): v[0]=F(1)
    norm=sum(x*x for x in v)
    return plus(eye(n),scale(-F(2)/norm,outer(v,v)))

def rational_frame(rng: random.Random,n: int) -> Matrix:
    u=mm(householder(rng,n),householder(rng,n))
    require(mm(trans(u),u)==eye(n),'orthogonal rational frame')
    return u

def run() -> dict:
    start=time.perf_counter()
    rng=random.Random(901773)
    rows=[]
    # Arbitrary rank-two factorizations: real rational, no SVD or matched-Gram
    # assumption is needed for the exact coherent-flag identity itself.
    for dims,m in [((3,),1),((3,),2),((3,),3),((3,3),1),((3,3),2),
                   ((3,3),3),((3,3,3),1),((3,3,3),2)]:
        d=1
        for x in dims: d*=x
        x=[[F(rng.randrange(-2,3)) for _ in range(2)] for _ in range(d)]
        y=[[F(rng.randrange(-2,3)) for _ in range(2)] for _ in range(d)]
        a=mm(x,trans(x)); b=mm(y,trans(y)); c=mm(x,trans(y))
        f0=(0,)*m; f1=(1,)*m
        big=flags([(f0,f0,a),(f1,f1,b),(f0,f1,c),(f1,f0,trans(c))],dims)
        lhs=q_sparse(big,len(dims)+m)
        rhs=2*q(c,dims)+F(1,2)**m*q(plus(a,scale(F((-1)**m),b)),dims)
        require(lhs==rhs,f'coherent flag {dims}, m={m}')
        rows.append({'kind':'coherent flag','dims':dims,'flags':m,'lhs':str(lhs),'rhs':str(rhs)})

    # Exact flat projection, with singular values 3 and 1. Then the auxiliary
    # coefficient sqrt(2*tau*(sigma-tau)) equals the rational number 2.
    dims=(3,3); d=9; sigma=F(3); tau=F(1)
    uf=rational_frame(rng,d); vf=rational_frame(rng,d); zf=rational_frame(rng,d)
    u1=[r[0] for r in uf];u2=[r[1] for r in uf]
    v1=[r[0] for r in vf];v2=[r[1] for r in vf];z=[r[0] for r in zf]
    a=plus(scale(sigma,outer(u1,u1)),scale(tau,outer(u2,u2)))
    b=plus(scale(sigma,outer(v1,v1)),scale(tau,outer(v2,v2)))
    c=plus(scale(sigma,outer(u1,v1)),scale(tau,outer(u2,v2)))
    e=scale(F(4),outer(z,z)); g=scale(F(2),outer(u2,z)); h=scale(F(2),outer(v2,z))
    blockrows=[[a,c,g],[trans(c),b,h],[trans(g),trans(h),e]]
    compressed=[[blockrows[i//d][j//d][i%d][j%d] for j in range(3*d)] for i in range(3*d)]
    require(mm(compressed,compressed)==scale(2*sigma,compressed),'D^2=2*sigma*D')
    require(sum(compressed[i][i] for i in range(3*d))==4*sigma,'projection trace=2')
    require(compressed==trans(compressed),'projection self-adjoint')
    for k in [1,2,3]:
        fa=(0,)*(2*k);fb=(1,)*(2*k);fc=(0,)*k+(1,)*k
        blocks=[(fa,fa,a),(fb,fb,b),(fc,fc,e),(fa,fb,c),(fb,fa,trans(c)),
                (fa,fc,g),(fc,fa,trans(g)),(fb,fc,h),(fc,fb,trans(h))]
        big=flags(blocks,dims)
        lhs=q_sparse(big,len(dims)+2*k)
        rhs=2*q(c,dims)+F(2)**(1-k)*(q(g,dims)+q(h,dims))+F(4)**(-k)*q(plus(a,b,scale(F((-1)**k),e)),dims)
        require(lhs==rhs,f'flat projection k={k}')
        err=abs(lhs/(4*sigma*sigma)-q(c,dims)/(2*sigma*sigma))
        bound=F(2)**(-k-1)+F(4)**(1-k)
        require(err<=bound,f'flat projection quantitative bound k={k}')
        rows.append({'kind':'flat projection','dims':dims,'k':k,'identity_residual':'0',
                     'scaled_error':str(err),'error_bound':str(bound)})

    # Negative control: P=|Phi_3><Phi_3| tensor I_3 is a rank-three projection.
    # A successful universal rank-two result MUST NOT silently extend to it.
    p: Sparse={}
    for i,j,k in product(range(3),repeat=3): p[((i,i,k),(j,j,k))]=F(1,3)
    value=q_sparse(p,3)
    require(value==F(-11,8),'rank-three negative control')
    rows.append({'kind':'rank-three negative control','q_projection':str(value),
                 'q_normalized_state':str(value/9),'rank':3})
    # Endpoint saturation control: I_2 embedded in first qutrit times pure
    # product projectors on the other sites.
    p2={((0,0,0),(0,0,0)):F(1),((1,0,0),(1,0,0)):F(1)}
    require(q_sparse(p2,3)==0,'rank-two zero control')
    rows.append({'kind':'rank-two product zero control','q':'0'})
    return {'status':'PASS','arithmetic':'exact rational; real finite fixtures',
            'identity_fixtures':len(rows),'rows':rows,'elapsed_seconds':time.perf_counter()-start,
            'scope':'Finite identities and controls only. Not all-copy positivity, novelty, or formal certification.',
            'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}

if __name__=='__main__':
    receipt=run()
    output=Path(__file__).with_name('exact_flag_receipt.json')
    output.write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))
