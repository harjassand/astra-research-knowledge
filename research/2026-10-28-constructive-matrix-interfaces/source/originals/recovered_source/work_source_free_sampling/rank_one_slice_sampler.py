#!/usr/bin/env python3
"""Exact sampling with one affine row or column restriction on a product factor.

The restricted vector may obey arbitrarily many binary affine equations.
No field elements, solution spaces, or original assignments are enumerated.
The acquired wrapper manufactures the field and matrix coordinates.
"""
from pathlib import Path
import random,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'work_matrix_root'),str(ROOT/'work_source_free_sampling')]
from adjoint_matrix_product_counter import (apply_binary,affine_solutions,
    BinaryCoordinates,gaussian_binomial)


def xor_all(values):
    out=0
    for value in values:out^=value
    return out


def dot(F,x,y):return xor_all(F.mul(a,b) for a,b in zip(x,y))
def transpose(A,columns=None):
    if A:return [list(x) for x in zip(*A)]
    return [[] for _ in range(columns or 0)]
def matmul(F,A,B,columns=None):
    width=len(B[0]) if B else (columns or 0)
    return [[xor_all(F.mul(A[i][k],B[k][j]) for k in range(len(B)))
        for j in range(width)] for i in range(len(A))]
def pack_vector(F,x):return sum(v<<(F.a*i) for i,v in enumerate(x))
def unpack_vector(F,x,n):return [(x>>(F.a*i))&(F.q-1) for i in range(n)]


def solve_field(F,A,b,variables):
    rows=[list(row)+[rhs] for row,rhs in zip(A,b)];pivots=[];at=0
    for j in range(variables):
        pivot=next((i for i in range(at,len(rows)) if rows[i][j]),None)
        if pivot is None:continue
        rows[at],rows[pivot]=rows[pivot],rows[at];scale=F.inv(rows[at][j])
        rows[at]=[F.mul(x,scale) for x in rows[at]]
        for i in range(len(rows)):
            if i!=at and rows[i][j]:
                z=rows[i][j];rows[i]=[x^F.mul(z,y) for x,y in zip(rows[i],rows[at])]
        pivots.append(j);at+=1
    if any(not any(row[:variables]) and row[-1] for row in rows):return None
    offset=[0]*variables
    for i,j in enumerate(pivots):offset[j]=rows[i][-1]
    basis=[]
    for free in range(variables):
        if free in pivots:continue
        v=[0]*variables;v[free]=F.one
        for i,j in enumerate(pivots):v[j]=rows[i][free]
        basis.append(v)
    return offset,basis


def rank_field(F,A,columns=None):
    variables=len(A[0]) if A else (columns or 0)
    return variables-len(solve_field(F,A,[0]*len(A),variables)[1])


def independent_columns(F,columns,height):
    selected=[];rank=0
    for column in columns:
        after=rank_field(F,transpose(selected+[column],height),len(selected)+1)
        if after>rank:selected.append(column);rank=after
    return selected


def complete_basis(F,basis,n):
    columns=list(basis)
    for i in range(n):
        e=[0]*n;e[i]=F.one
        if len(independent_columns(F,columns+[e],n))>len(columns):columns.append(e)
    if len(columns)!=n:raise AssertionError('field basis completion failed')
    return columns


def inverse(F,A):
    n=len(A);columns=[]
    for i in range(n):
        b=[0]*n;b[i]=F.one;sol=solve_field(F,A,b,n)
        if sol is None or sol[1]:raise ValueError('singular field matrix')
        columns.append(sol[0])
    return transpose(columns,n)


def sample_field_affine(F,offset,basis,rng):
    out=list(offset)
    for vector in basis:
        z=rng.getrandbits(F.a);out=[x^F.mul(z,y) for x,y in zip(out,vector)]
    return out


def binary_field_span(F,vectors):
    return BinaryCoordinates(pack_vector(F,[F.mul(1<<ell,x) for x in v])
        for v in vectors for ell in range(F.a))


def contains(span,value):
    try:span.coordinates(value);return True
    except ValueError:return False


def choose_weighted(items,rng):
    total=sum(weight for weight,item in items)
    if not total:raise ValueError('empty fiber')
    draw=rng.randrange(total)
    for weight,item in items:
        if draw<weight:return item,total
        draw-=weight
    raise AssertionError('integer draw out of range')


def population(F,p,d,r,k):
    if k<0 or k>min(p,d,r):return 0
    total=0
    for s in range(k,min(p,d)+1):
        onto=1
        for j in range(s):onto*=F.q**d-F.q**j
        total+=gaussian_binomial(p-k,s-k,F.a)*onto*F.q**(r*(d-s))
    return total


def sample_product(F,Z,d,rng):
    p=len(Z);r=len(Z[0]) if Z else 0;k=rank_field(F,Z,r)
    if not population(F,p,d,r,k):raise ValueError('empty product fiber')
    weights=[]
    for s in range(k,min(p,d)+1):
        onto=1
        for j in range(s):onto*=F.q**d-F.q**j
        weights.append((gaussian_binomial(p-k,s-k,F.a)*onto*F.q**(r*(d-s)),s))
    s,_=choose_weighted(weights,rng)
    K=independent_columns(F,transpose(Z,r),p);basis=complete_basis(F,K,p)
    while True:
        A=[[rng.getrandbits(F.a) for _ in range(s-k)] for _ in range(p-k)]
        if rank_field(F,A,s-k)==s-k:break
    W=K+[[xor_all(F.mul(basis[k+i][h],A[i][j]) for i in range(p-k))
        for h in range(p)] for j in range(s-k)]
    while True:
        R=[[rng.getrandbits(F.a) for _ in range(d)] for _ in range(s)]
        if rank_field(F,R,d)==s:break
    X=matmul(F,transpose(W,p),R,d);columns=[]
    for z in transpose(Z,r):
        sol=solve_field(F,X,z,d)
        if sol is None:raise AssertionError('sampled image does not contain target')
        columns.append(sample_field_affine(F,*sol,rng))
    Y=transpose(columns,d)
    if matmul(F,X,Y,r)!=Z:raise AssertionError('full sampler reconstruction failed')
    return X,Y


def update_options(F,Z,w):
    """Disjoint x classes by rank(Z+x*w), with exact sizes and samplers."""
    p=len(Z);r=len(w);k=rank_field(F,Z,r)
    K=independent_columns(F,transpose(Z,r),p);Kspan=binary_field_span(F,K)
    rowspace=binary_field_span(F,Z);wbits=pack_vector(F,w)
    def uniform_all(rng):return [rng.getrandbits(F.a) for _ in range(p)]
    def uniform_K(rng):return sample_field_affine(F,[0]*p,K,rng)
    if not any(w):return [(F.q**p,k,uniform_all)]
    if not contains(rowspace,wbits):
        def outside(rng):
            while True:
                x=uniform_all(rng)
                if not contains(Kspan,pack_vector(F,x)):return x
        return [(F.q**k,k,uniform_K),(F.q**p-F.q**k,k+1,outside)]
    v=solve_field(F,transpose(Z,r),w,p)[0]
    lambdas=[dot(F,v,x) for x in K]
    drop=solve_field(F,[lambdas],[F.one],k)
    if drop is None:raise AssertionError('nonzero row functional vanished on image')
    def lower(rng):
        t=sample_field_affine(F,*drop,rng)
        return [xor_all(F.mul(K[j][i],t[j]) for j in range(k)) for i in range(p)]
    def same(rng):
        while True:
            x=uniform_all(rng)
            if not (contains(Kspan,pack_vector(F,x)) and dot(F,v,x)==F.one):return x
    return [(F.q**(k-1),k-1,lower),(F.q**p-F.q**(k-1),k,same)]


class BinaryAffine:
    def __init__(self,offset,basis,width):
        self.offset=offset;self.basis=list(basis);self.width=width
        self.coordinates=BinaryCoordinates(self.basis)
        if len(self.coordinates.basis)!=len(self.basis):raise ValueError('dependent affine basis')
        self.size=1<<len(self.basis)
    def contains(self,x):return contains(self.coordinates,x^self.offset)
    def sample(self,rng):return self.offset^apply_binary(self.basis,rng.getrandbits(len(self.basis)))
    def intersect_linear(self,span):
        annihilator=affine_solutions([(x,0) for x in span.basis],self.width)[1]
        rows=[(sum(((h&b).bit_count()%2)<<i for i,b in enumerate(self.basis)),
            (h&self.offset).bit_count()%2) for h in annihilator]
        solved=affine_solutions(rows,len(self.basis))
        if solved is None:return None
        offset=self.offset^apply_binary(self.basis,solved[0])
        basis=[apply_binary(self.basis,v) for v in solved[1]]
        return BinaryAffine(offset,basis,self.width)


def row_constraint_categories(F,Z,d,T):
    p=len(Z);r=len(Z[0]);k=rank_field(F,Z,r)
    rows=binary_field_span(F,Z);inside=T.intersect_linear(rows)
    zero=int(T.contains(0));nin=(inside.size if inside else 0)-zero;nout=T.size-(inside.size if inside else 0)
    N=lambda j:population(F,p,d-1,r,j)
    weights=[F.q**p*N(k), (F.q**(k-1)*N(k-1)+(F.q**p-F.q**(k-1))*N(k)) if k else 0,
        F.q**k*N(k)+(F.q**p-F.q**k)*N(k+1)]
    return rows,inside,[(zero*weights[0],0),(nin*weights[1],1),(nout*weights[2],2)]


def sample_row_restricted(F,Z,d,T,rng):
    p=len(Z);r=len(Z[0]);rows,inside,weights=row_constraint_categories(F,Z,d,T)
    category,total=choose_weighted(weights,rng)
    if category==0:w=[0]*r
    elif category==1:
        while True:
            bits=inside.sample(rng)
            if bits:break
        w=unpack_vector(F,bits,r)
    else:
        while True:
            bits=T.sample(rng)
            if not contains(rows,bits):break
        w=unpack_vector(F,bits,r)
    options=update_options(F,Z,w)
    sampler,_=choose_weighted([(count*population(F,p,d-1,r,rank),sampler)
        for count,rank,sampler in options],rng)
    x=sampler(rng);remaining=[[Z[i][j]^F.mul(x[i],w[j]) for j in range(r)] for i in range(p)]
    X2,Y2=sample_product(F,remaining,d-1,rng)
    X=[[x[i]]+X2[i] for i in range(p)];Y=[w]+Y2
    if matmul(F,X,Y,r)!=Z or not T.contains(pack_vector(F,Y[0])):
        raise AssertionError('row-restricted reconstruction failed')
    return X,Y,total


def column_constraint_weights(F,Z,d,T):
    p=len(Z);r=len(Z[0]);z=[row[0] for row in Z];C=[row[1:] for row in Z]
    k=rank_field(F,C,r-1);zero=int(T.contains(0))
    zero_weight=population(F,p,d,r-1,k) if not any(z) else 0
    options=update_options(F,transpose(C,r-1),z)
    nonzero_weight=sum(count*population(F,p,d-1,r-1,rank) for count,rank,_ in options)
    return z,C,options,[(zero*zero_weight,0),((T.size-zero)*nonzero_weight,1)]


def sample_column_restricted(F,Z,d,T,rng):
    p=len(Z);r=len(Z[0]);z,C,options,weights=column_constraint_weights(F,Z,d,T)
    category,total=choose_weighted(weights,rng)
    if category==0:
        X,Y2=sample_product(F,C,d,rng);Y=[[0]+row for row in Y2]
    else:
        while True:
            bits=T.sample(rng)
            if bits:break
        b=unpack_vector(F,bits,d);R=transpose(complete_basis(F,[b],d),d);Rinv=inverse(F,R)
        sampler,_=choose_weighted([(count*population(F,p,d-1,r-1,rank),sampler)
            for count,rank,sampler in options],rng)
        w=sampler(rng);remaining=[[C[i][j]^F.mul(z[i],w[j]) for j in range(r-1)] for i in range(p)]
        X2,Y2=sample_product(F,remaining,d-1,rng)
        Xlocal=[[z[i]]+X2[i] for i in range(p)]
        Ylocal=[[F.one]+w]+[[0]+row for row in Y2]
        X=matmul(F,Xlocal,Rinv,d);Y=matmul(F,R,Ylocal,r)
    if matmul(F,X,Y,r)!=Z or not T.contains(pack_vector(F,[row[0] for row in Y])):
        raise AssertionError('column-restricted reconstruction failed')
    return X,Y,total

