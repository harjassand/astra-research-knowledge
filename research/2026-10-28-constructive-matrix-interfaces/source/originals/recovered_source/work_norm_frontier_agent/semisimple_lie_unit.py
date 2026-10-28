#!/usr/bin/env python3
"""Acquire unmarked beta-nonzero units for every semisimple single primary."""
from primary_lie_unit import *


def recover_semisimple_source_unit(A,P):
    if A.t<4:raise ValueError('semisimple Lie route requires size at least four')
    stabilizer=polar_stabilizer(A,P);brackets=[]
    for i,(a,b) in enumerate(stabilizer):
        for c,d in stabilizer[:i]:
            left=A.mul(a,c)^A.mul(c,a);right=A.mul(b,d)^A.mul(d,b)
            if left or right:brackets.append((left,right))
    if not brackets:raise ValueError('semisimple multiplicity must exceed one')
    U=intertwiner_space(A,brackets);degree=len(U)
    if degree<1 or A.t%degree or A.t//degree<2:
        raise ValueError('commutator intertwiners have inadmissible dimension')
    V=next((x for x in U if A.is_unit(x)),None)
    if V is None:raise ValueError('no unit in displayed coefficient-field coset')
    Vinv=A.inv(V);R=[A.mul(x,Vinv) for x in U];basis=[A.one]
    for x in R:
        if len(independent([A.coordinates(v) for v in basis+[x]],A.F,A.m))>len(basis):basis.append(x)
    if len(basis)!=degree or any(A.mul(x,y)!=A.mul(y,x) for x in basis for y in basis):
        raise ValueError('acquired commutant is not a commutative field candidate')
    K=CoefficientField(A,basis)
    if any(power(A,x,K.q)!=x for x in basis):raise ValueError('coefficient-field Frobenius identity failed')
    normalizer_dimension=len(independent([A.coordinates(b) for a,b in stabilizer],A.F,A.m))
    if normalizer_dimension!=A.t*A.t//degree:raise ValueError('normalizer and coefficient-field dimensions disagree')
    normalized=lambda x:A.mul(P(A.mul(Vinv,x)),Vinv)
    S=reshuffle(A,normalized);diagonal=intertwiner_space(A,[(x,x) for x in basis])
    if len(diagonal)!=normalizer_dimension:raise ValueError('coefficient-field double centralizer dimension failed')
    annihilator=kernel([A.coordinates(x) for x in basis],A.F,A.m)
    def projected(x):
        coords=A.coordinates(x)
        return [xor(A.F.mul(v,w) for v,w in zip(row,coords)) for row in annihilator]
    columns=[sum((projected(A.mul(k,x)) for x in diagonal),[]) for k in basis]
    target=sum((projected(S(x)) for x in diagonal),[])
    gamma,rank=field_solve(list(map(list,zip(*columns))),target,A.F,degree)
    if gamma is None or rank!=degree:raise ValueError('semisimple quotient scale was not uniquely acquired')
    packed=sum(c<<(A.F.a*i) for i,c in enumerate(gamma))
    if not packed:raise ValueError('zero exterior-square source scale')
    H=K.embed(K.pow(packed,1<<(K.a-1)));W=A.mul(H,V)
    if not A.is_unit(W):raise ValueError('manufactured semisimple source unit is singular')
    return W,dict(route='semisimple polar commutators and coefficient-field quotient scale',
        matrix_size=A.t,field_degree=A.F.a,coefficient_field_degree=degree,
        semisimple_multiplicity=A.t//degree,stabilizer_dimension=len(stabilizer),
        right_normalizer_dimension=normalizer_dimension,commutator_pairs=len(brackets),
        unit_intertwiner_dimension=degree,quotient_scale_rank=rank,
        supplied_matrix_units=False,supplied_source_unit=False)


def recover_from_raw_semisimple_source(poly,algebra):
    d=algebra.d;polar=[0]*d
    for monomial in poly:
        if monomial.bit_count()==2:
            i,j=bits(monomial);polar[i]^=1<<j;polar[j]^=1<<i
    columns=[binary_solve(algebra.gram,v) for v in polar]
    P=lambda x:linear_apply(columns,x);A=Intrinsic(algebra)
    for e in A.basis:
        for bit in range(A.F.a):
            if P(scale(A,1<<bit,e))!=scale(A,1<<bit,P(e)):
                raise ValueError('source polar is not linear over the acquired center')
    return recover_semisimple_source_unit(A,P)
