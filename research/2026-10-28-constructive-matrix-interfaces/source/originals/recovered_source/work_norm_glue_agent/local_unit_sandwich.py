#!/usr/bin/env python3
"""Recover a unit sandwich line after an acquired local-ring coset.

Scope: E=F[D] is single-primary, and the F[D]-module has >=2 cyclic blocks.
S(X)=beta H X H+T(X), H in E^*, beta !=0, image(T) contained in E.
The ambient algebra and E basis are supplied by preceding acquisition.
This helper does not manufacture a missing EW coset or count circuits.
"""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'work_norm_frontier_agent'),str(ROOT/'work_matrix_root')]
from lie_source_unit import (kernel,relations,field_solve,power,xor,combination,rref)


def recover_local_unit_sandwich(A,S,E):
    m=len(E)
    if not m:raise ValueError('nonempty local-ring basis required')
    if any(A.mul(x,y)!=A.mul(y,x) for x in E for y in E):
        raise ValueError('the acquired ring is not commutative')
    annihilator=kernel([A.coordinates(e) for e in E],A.F,A.m)
    def project(value):
        coordinates=A.coordinates(value)
        return [xor(A.F.mul(v,w) for v,w in zip(row,coordinates)) for row in annihilator]
    columns=[]
    for left in E:
        for right in E:
            columns.append(sum((project(A.mul(left,A.mul(x,right))) for x in A.basis),[]))
    target=sum((project(S(x)) for x in A.basis),[])
    coefficients,rank=field_solve(list(map(list,zip(*columns))),target,A.F,m*m)
    if coefficients is None:raise ValueError('no local sandwich tensor lift')
    tensor=[coefficients[i*m:(i+1)*m] for i in range(m)]
    # q^height >= m >= nilpotence length, and this Frobenius is F-linear.
    height=(m-1).bit_length()
    frobenius=[A.coordinates(power(A,e,A.F.q**height)) for e in E]
    radical=relations(frobenius,A.F)
    residue_rows=kernel(radical,A.F,m)
    projected=[[xor(A.F.mul(row[i],tensor[i][j]) for i in range(m)) for j in range(m)]
               for row in residue_rows]
    reduced,pivots=rref(projected,A.F,m)
    if len(pivots)!=1:raise ValueError('residue-projected tensor is not rank one')
    H=combination(A,reduced[0],E)
    if not A.is_unit(H):raise ValueError('recovered sandwich line is not a unit')
    return H,dict(local_ring_dimension=m,radical_dimension=len(radical),
        residue_degree=len(residue_rows),tensor_unknowns=m*m,tensor_projection_rank=rank,
        full_tensor_unique=(rank==m*m),projected_tensor_rank=1,
        acquired_local_ring_and_coset_required=True)
