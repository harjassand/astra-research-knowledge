#!/usr/bin/env python3
"""Manufacture an unmarked 2x2 source unit through a degree-two Pfaffian.

The field and full matrix algebra are already certified from the raw cubic.
This routine supplies the missing unit for arbitrary beta and field-linear
trace refinements when D is a full chain or irreducible degree two.
It uses the acquired center, not supplied matrix units.
"""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'work_norm_slice_agent'))
sys.path.insert(0,str(ROOT/'work_norm_frontier_agent'))
from raw_matrix_trace import solve,bits,compose,linear_apply
from invariant_quadratic_matrix import quadratic_anf,invariant_features
from matrix_kloosterman import factor_polynomial

def central_envelope(poly,algebra):
    """Unique A tensor A^op coefficients of a center-linear trace-dual polar."""
    d=algebra.d;m=algebra.D;a=algebra.a;F=algebra.F;polar=[0]*d
    for monomial in poly:
        if monomial.bit_count()==2:
            i,j=bits(monomial);polar[i]^=1<<j;polar[j]^=1<<i
    H=[solve(algebra.gram,column) for column in polar]
    for scalar in algebra.center:
        C=algebra.left_matrix(scalar)
        if compose(H,C)!=compose(C,H):raise ValueError('source polar is not center-linear')
    cache={}
    def coordinates(x):
        if x not in cache:cache[x]=solve(algebra.field_columns,x)
        if cache[x] is None:raise AssertionError('missing acquired field coordinates')
        return cache[x]
    def scale(s,x,length):
        return sum(F.mul(s,(x>>(a*j))&(F.q-1))<<(a*j) for j in range(length))
    basis=algebra.field_module_basis;columns=[]
    for left in basis:
        for right in basis:
            packed=sum(coordinates(algebra.mul(left,algebra.mul(b,right)))<<(d*j)
                       for j,b in enumerate(basis))
            for bit in range(a):columns.append(scale(1<<bit,packed,m*m))
    target=sum(coordinates(linear_apply(H,b))<<(d*j) for j,b in enumerate(basis))
    result=solve(columns,target)
    if result is None:raise AssertionError('certified simple envelope is not an isomorphism')
    M=[[(result>>(a*(i*m+j)))&(F.q-1) for j in range(m)] for i in range(m)]
    if any(M[i][i] for i in range(m)) or any(M[i][j]!=M[j][i] for i in range(m) for j in range(i)):
        raise ValueError('multiplication coefficient matrix is not alternating')
    return M

def pfaffian4(M,F):
    return F.mul(M[0][1],M[2][3])^F.mul(M[0][2],M[1][3])^F.mul(M[0][3],M[1][2])

def count_matrix2_pfaffian_source(poly,algebra):
    if algebra.t!=2:raise ValueError('degree-two Pfaffian branch requires matrix size two')
    from regular_chain_pencil_field import fit_center_rank_two_source
    from operator_quadratic_counter import acquire_operator_linear_refinement,count_acquired_cyclic_refinement
    F=algebra.F;poly=set(poly);evaluate=invariant_features(algebra)
    determinant=quadratic_anf(lambda x:F.trace(evaluate(x)[1]),algebra.d)
    M=central_envelope(poly,algebra);J=central_envelope(determinant,algebra)
    coefficients=[pfaffian4(M,F),0,pfaffian4(J,F)]
    for i,j,k,l in ((0,1,2,3),(0,2,1,3),(0,3,1,2)):
        coefficients[1]^=F.mul(M[i][j],J[k][l])^F.mul(J[i][j],M[k][l])
    if not coefficients[2]:raise AssertionError('determinant polar has singular envelope')
    monic=[F.mul(c,F.inv(coefficients[2])) for c in coefficients]
    roots=sorted(g[0] for g,multiplicity in factor_polynomial(monic,F) if len(g)==2)
    failures=[]
    for theta in roots:
        removal=quadratic_anf(lambda x:F.trace(F.mul(theta,evaluate(x)[1])),algebra.d)
        try:
            _,_,pencil=fit_center_rank_two_source(poly^removal,algebra,accept_simple=True)
            beta,D,phi,eta,evidence=acquire_operator_linear_refinement(poly,algebra,
                inverse_unit=pencil['acquired_inverse_unit'])
            gap,backend=count_acquired_cyclic_refinement(algebra,beta,D,phi,eta)
        except ValueError as error:
            failures.append(dict(theta=theta,reason=str(error)));continue
        evidence.update(unit_acquisition_route='degree-two Pfaffian and acquired center-field pencil',
            pfaffian_polynomial=monic,determinant_coefficient=theta,
            candidate_field_roots=roots,failed_earlier_candidates=failures,
            source_pencil=pencil['source_pencil'],pencil_unit_trials=pencil['pencil_unit_trials'],
            full_coefficient_identity_verified=True)
        return gap,backend,evidence
    raise ValueError('no Pfaffian root supplies an admitted full source identity')
