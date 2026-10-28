#!/usr/bin/env python3
"""Acquire and count a nonconjugation-invariant, full-rank quadratic source.

Source family: Q(X)=Tr sum_{i<j,k<l} S_ij T_kl
 (X_ik X_jl + X_il X_jk), with S,T nondegenerate alternating forms.
Their bases and the forms themselves are not inputs to the raw compiler.
The binary polar manufactures an involution and a Pfaffian-trace refinement.
"""
from pathlib import Path
from math import prod
import sys,time
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'work_matrix_root'))
from polynomial_nilpotent_pair import choose
from matrix_kloosterman import Field

def isotropic_subspaces(m,k,q):
    if not 0<=k<=m:return 0
    return choose(m,k,q)*prod(q**(m-i)+1 for i in range(k))

def symplectic_restriction_subspaces(m,r,s,q):
    """Number of r-subspaces in a 2m symplectic space of restriction rank 2s."""
    k=r-2*s
    if not (0<=k<=m and 0<=s<=m-k):return 0
    return isotropic_subspaces(m,k,q)*q**(2*s*(m-k-s))*choose(m-k,s,q*q)

def symplectic_minor_gap(t,field_h=3,constant=0):
    """Full signed sum of Tr tr(XYZ)+Q(X)+constant, all 3at² bits free."""
    F=Field(field_h);q=F.q
    if t<2 or t%2:raise ValueError('positive even matrix size at least two required')
    if constant not in (0,1):raise ValueError('binary constant')
    m=t//2;onto=[1]
    for h in range(t):onto.append(onto[-1]*(q**t-q**h))
    normalized=0;strata=0
    for r in range(t+1):
        for s in range(r//2+1):
            number=symplectic_restriction_subspaces(m,r,s,q)
            if number:
                normalized+=number*onto[t-r]*q**(t*(r-s));strata+=1
    gap=(-1)**constant*q**(t*t)*normalized
    return gap,dict(route='symplectic restriction-type aggregation',matrix_size=t,
        field_degree=F.a,field_modulus=field_h,restriction_strata=strata,
        enumerated_subspaces=0,enumerated_matrices=0,enumerated_original_assignments=0,
        uniform_polynomial_time=True)

def quadratic_anf(value,n):
    c=value(0);single=[value(1<<i)^c for i in range(n)]
    out={0} if c else set()
    out.update(1<<i for i,v in enumerate(single) if v)
    for i in range(n):
        for j in range(i+1,n):
            if value((1<<i)|(1<<j))^single[i]^single[j]^c:
                out.add((1<<i)|(1<<j))
    return out

def fit_symplectic_minor(poly,algebra):
    """Manufacture an intrinsic symplectic involution from the raw polar."""
    from raw_matrix_trace import bits,solve,linear_apply,compose,identity,reduced_charpoly,charpoly
    d=algebra.d;t=algebra.t;F=algebra.F;poly=set(poly)
    if t%2:raise ValueError('nondegenerate alternating form requires even degree')
    if any(m.bit_count()>2 or m.bit_length()>d for m in poly):raise ValueError('quadratic source required')
    polar=[0]*d
    for monomial in poly:
        if monomial.bit_count()==2:
            i,j=bits(monomial);polar[i]^=1<<j;polar[j]^=1<<i
    P=[solve(algebra.gram,c) for c in polar]
    if any(x is None for x in P):raise AssertionError('trace-dual polar acquisition')
    H=linear_apply(P,algebra.one)
    if not algebra.is_unit(H):raise ValueError('polar at identity is not a unit')
    Hinv=solve(algebra.left_matrix(H),algebra.one)
    tau=[algebra.mul(Hinv,x) for x in P]
    if linear_apply(tau,algebra.one)!=algebra.one:raise ValueError('normalization does not fix identity')
    if any(linear_apply(tau,c)!=c for c in algebra.center):raise ValueError('involution does not fix acquired center')
    if compose(tau,tau)!=identity(d):raise ValueError('polar normalization is not involutive')
    for i in range(d):
        for j in range(d):
            if linear_apply(tau,algebra.table[i][j])!=algebra.mul(tau[j],tau[i]):
                raise ValueError('polar normalization is not an anti-automorphism')
    alt=[(1<<i)^tau[i] for i in range(d)]
    one_witness=solve(alt,algebra.one);H_witness=solve(alt,H)
    if one_witness is None:raise ValueError('involution is not symplectic')
    if H_witness is None:raise ValueError('second form is not alternating')
    def pfaffian_trace_refinement(x):
        gram=algebra.mul(linear_apply(P,x),x)
        cp=reduced_charpoly(charpoly(algebra.field_left_matrix(gram),F),t,F)
        if any(cp[j] for j in range(1,len(cp),2)):
            raise AssertionError('alternating Gram characteristic polynomial is not a square')
        root=[F.pow(cp[j],1<<(F.a-1)) for j in range(0,len(cp),2)]
        return F.trace(root[-2])
    manufactured=quadratic_anf(pfaffian_trace_refinement,d)
    constant=int(0 in poly)
    if manufactured!=(poly^({0} if constant else set())):
        raise ValueError('source is not the acquired Pfaffian-trace quadratic refinement')
    return constant,dict(acquired_polar_at_identity=H,acquired_involution=tau,
        alternating_identity_witness=one_witness,alternating_H_witness=H_witness,
        anti_multiplication_checks=d*d,refinement_coefficients_verified=1+d+d*(d-1)//2,
        polar_rank=d,supplied_bilinear_forms=False,supplied_matrix_units=False)

def compile_raw_symplectic_quadratic(poly,n):
    from raw_matrix_trace import (hidden_groups,AcquiredMatrixAlgebra,acquire_center,
        bits,identity,inverse,linear_apply,polynomial_value)
    start=time.perf_counter();poly=set(poly)
    if n<=0 or any(m<0 or m.bit_length()>n or m.bit_count()>3 for m in poly):
        raise ValueError('raw cubic Boolean ANF required')
    grouped,slices,group_map,stats=hidden_groups(poly,n)
    algebra=AcquiredMatrixAlgebra(slices);d=algebra.d
    centered,offset=acquire_center(grouped,slices,d,allow_within=True)
    lower=[m for m in centered if 0<m.bit_count()<=2]
    groups={i//d for m in lower for i in bits(m)}
    if len(groups)!=1:raise ValueError('source must lie in one acquired matrix group')
    group=next(iter(groups));local={m>>(group*d) for m in lower}
    if 0 in centered:local.add(0)
    maps=[identity(d),algebra.Y,algebra.Z];back=inverse(maps[group])
    intrinsic=quadratic_anf(lambda x:polynomial_value(local,linear_apply(back,x)),d)
    constant,acquired=fit_symplectic_minor(intrinsic,algebra)
    gap,backend=symplectic_minor_gap(algebra.t,algebra.h,constant)
    stats.update(algebra.stats);stats.update(acquired)
    stats.update(raw_monomials=len(poly),affine_offset=offset,source_group=group,
        full_coefficient_identity_verified=True,backend=backend,seconds=time.perf_counter()-start)
    return dict(original_bits=n,gap=gap,zeros=((1<<n)+gap)//2,ones=((1<<n)-gap)//2,stats=stats)
