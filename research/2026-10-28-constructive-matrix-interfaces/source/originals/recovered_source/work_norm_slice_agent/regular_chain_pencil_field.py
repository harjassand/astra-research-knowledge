#!/usr/bin/env python3
"""Acquire a regular-chain source from a rank-two tensor over its center field.

Complete for Tr tr(D(WX)^2)+Tr(alpha tr(WX)+eta tr(DWX))+c,
where W is a unit and D is scalar plus one full Jordan chain. All fields
have characteristic two. Every raw coefficient and source-type condition
is checked; no matrix coordinates or field decomposition are supplied.
"""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'work_matrix_root'))
sys.path.insert(0,str(ROOT/'work_norm_frontier_agent'))
from raw_matrix_trace import (solve,flat,compose,bits,linear_apply,identity,
    hidden_groups,AcquiredMatrixAlgebra,acquire_center,inverse)
from invariant_quadratic_matrix import quadratic_anf,polynomial_value
from matrix_kloosterman import rref
from feedback_nilpotent_gaussians import regular_chain_gap_linear

def fit_center_rank_two_source(poly,algebra,accept_simple=False,accept_primary=False,accept_equidegree=False):
    d=algebra.d;Ddim=algebra.D;a=algebra.a;F=algebra.F;poly=set(poly)
    polar=[0]*d
    for monomial in poly:
        if monomial.bit_count()==2:
            i,j=bits(monomial);polar[i]^=1<<j;polar[j]^=1<<i
    H=[solve(algebra.gram,column) for column in polar]
    for scalar in algebra.center:
        C=algebra.left_matrix(scalar)
        if compose(H,C)!=compose(C,H):
            raise ValueError('source polar is not linear over the acquired center')
    coordinate_cache={}
    def coordinates(x):
        if x not in coordinate_cache:
            coordinate_cache[x]=solve(algebra.field_columns,x)
            if coordinate_cache[x] is None:raise AssertionError('lost acquired field coordinates')
        return coordinate_cache[x]
    def scale_packed(s,x,length):
        return sum(F.mul(s,(x>>(a*j))&(F.q-1))<<(a*j) for j in range(length))
    def scalar_mul(s,x):
        return linear_apply(algebra.field_columns,scale_packed(s,coordinates(x),Ddim))
    field_basis=algebra.field_module_basis
    # Encode F-linear maps by images of an F-basis, using a*Ddim^2 bits.
    envelope=[]
    for left in field_basis:
        for right in field_basis:
            packed=sum(coordinates(algebra.mul(left,algebra.mul(b,right)))<<(d*j)
                       for j,b in enumerate(field_basis))
            for bit in range(a):envelope.append(scale_packed(1<<bit,packed,Ddim*Ddim))
    target=sum(coordinates(linear_apply(H,b))<<(d*j) for j,b in enumerate(field_basis))
    coefficients=solve(envelope,target)
    if coefficients is None:raise AssertionError('certified central simple envelope failed')
    M=[[(coefficients>>(a*(i*Ddim+j)))&(F.q-1) for j in range(Ddim)] for i in range(Ddim)]
    if any(M[i][i] for i in range(Ddim)) or any(M[i][j]!=M[j][i] for i in range(Ddim) for j in range(i)):
        raise ValueError('multiplication coefficient matrix is not alternating over its center')
    rows,pivots=rref(M,F)
    if len(pivots)!=2:raise ValueError('multiplication coefficient rank is not two over its center')
    pencil=[linear_apply(algebra.field_columns,sum(v<<(a*j) for j,v in enumerate(row))) for row in rows[:2]]
    # A degree-t univariate reduced determinant suffices: at most t+2
    # points, or all q+1 projective points when q<=t. This is not PIT.
    candidates=[pencil[1]]+[pencil[0]^scalar_mul(s,pencil[1]) for s in range(min(F.q,algebra.t+1))]
    unit=None;trials=0
    for value in candidates:
        trials+=1
        if algebra.is_unit(value):unit=value;break
    if unit is None:raise ValueError('manufactured center-field pencil contains no unit')
    R=solve(algebra.left_matrix(unit),algebra.one)
    normalized=quadratic_anf(lambda x:polynomial_value(poly,algebra.mul(R,x)),d)
    polar=[0]*d
    for monomial in normalized:
        if monomial.bit_count()==2:
            i,j=bits(monomial);polar[i]^=1<<j;polar[j]^=1<<i
    H=[solve(algebra.gram,column) for column in polar]
    derivations=[flat([algebra.mul(1<<i,1<<j)^algebra.mul(1<<j,1<<i)
                      for j in range(d)],d) for i in range(d)]
    D=solve(derivations,flat(H,d))
    if D is None:raise ValueError('normalized pencil is not an inner derivation')
    cp,primary=algebra.primary_data(D)
    if len(primary)==1 and len(primary[0]['irreducible'])==2 and primary[0]['jordan_columns']==[1]*algebra.t:
        eigenvalue=primary[0]['irreducible'][0];N=D^scalar_mul(eigenvalue,algebra.one)
        operator_kind='regular_chain'
    elif accept_simple and len(primary)==1 and len(primary[0]['irreducible'])==algebra.t+1 and primary[0]['jordan_columns']==[1]:
        N=D;operator_kind='irreducible'
    elif accept_primary and len(primary)==1 and (primary[0]['jordan_columns']==[1]*primary[0]['multiplicity'] or primary[0]['jordan_columns']==[primary[0]['multiplicity']]):
        N=D;operator_kind='uniform_primary'
    elif accept_equidegree and primary and all(p['multiplicity']==1 and p['jordan_columns']==[1] for p in primary) and len({len(p['irreducible']) for p in primary})==1:
        N=D;operator_kind='squarefree_equidegree'
    else:
        raise ValueError('source operator has neither an admitted full Jordan chain nor irreducible degree')
    canonical=quadratic_anf(lambda x:algebra.trace(algebra.mul(N,algebra.mul(x,x))),d)
    residual=normalized^canonical
    if any(m.bit_count()>1 for m in residual):raise AssertionError('normalized inner polar failed to cancel')
    source=algebra.source(sum(m for m in residual if m),identity(d))
    scalar_columns=[scalar_mul(1<<i,algebra.one) for i in range(a)]+[scalar_mul(1<<i,N) for i in range(a)]
    params=solve(scalar_columns,source)
    if params is None:raise ValueError('linear refinement is outside the acquired source pencil')
    alpha=params&(F.q-1);eta=params>>a;constant=int(0 in residual)
    phi=quadratic_anf(lambda s:constant^F.trace(F.mul(alpha,s)),a)
    reconstructed=canonical^quadratic_anf(lambda x:
        polynomial_value(phi,algebra.relative_trace(x))^
        F.trace(F.mul(eta,algebra.relative_trace(algebra.mul(N,x)))),d)
    if reconstructed!=normalized:raise AssertionError('complete normalized source coefficient identity failed')
    if operator_kind=='regular_chain':
        gap,backend=regular_chain_gap_linear(algebra.t,algebra.h,0,phi,eta)
    elif operator_kind=='irreducible':
        from simple_operator_quadratic import simple_operator_gap
        gap,backend=simple_operator_gap(algebra.t,algebra.h,cp,0,phi,eta)
    elif operator_kind=='uniform_primary':
        from acquired_primary_counter import count_acquired_primary_source
        gap,backend=count_acquired_primary_source(algebra,0,N,phi,eta)
    else:
        from equidegree_squarefree_counter import count_acquired_squarefree_equidegree
        gap,backend=count_acquired_squarefree_equidegree(algebra,0,N,phi,eta)
    return gap,backend,dict(source_pencil_field_rank=2,source_pencil=pencil,
        pencil_unit_trials=trials,pencil_unit_trial_bound=min(F.q+1,algebra.t+2),
        acquired_unit=unit,acquired_inverse_unit=R,acquired_operator=N,
        acquired_primary_data=primary,source_reduced_charpoly=cp,
        alpha=alpha,eta=eta,constant=constant,operator_kind=operator_kind,
        full_coefficient_identity_verified=True,
        unit_acquisition_route='rank-two multiplication envelope over acquired center field')

def compile_raw_regular_pencil(poly,n):
    begun=time.perf_counter();poly=set(poly)
    if type(n) is not int or n<=0 or any(type(m) is not int or m<0 or m.bit_length()>n or m.bit_count()>3 for m in poly):
        raise ValueError('raw Boolean cubic ANF required')
    grouped,slices,group_map,stats=hidden_groups(poly,n)
    algebra=AcquiredMatrixAlgebra(slices);d=algebra.d
    centered,offset=acquire_center(grouped,slices,d,allow_within=True)
    lower=[m for m in centered if 0<m.bit_count()<=2]
    groups={i//d for m in lower for i in bits(m)}
    if len(groups)!=1:raise ValueError('source must occupy one acquired group')
    group=next(iter(groups));local={m>>(group*d) for m in lower}
    if 0 in centered:local.add(0)
    back=inverse([identity(d),algebra.Y,algebra.Z][group])
    intrinsic=quadratic_anf(lambda x:polynomial_value(local,linear_apply(back,x)),d)
    gap,backend,evidence=fit_center_rank_two_source(intrinsic,algebra)
    if abs(gap)>1<<n or gap%2:raise AssertionError('invalid original-domain gap')
    stats.update(algebra.stats);stats.update(evidence)
    stats.update(backend=backend,affine_offset=offset,quadratic_group=group,
                 raw_monomials=len(poly),seconds=time.perf_counter()-begun)
    return dict(original_bits=n,ones=((1<<n)-gap)//2,zeros=((1<<n)+gap)//2,gap=gap,stats=stats)
