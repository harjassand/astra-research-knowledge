#!/usr/bin/env python3
"""Polynomial counting for an acquired source operator with one unbounded chain.

Source Tr(beta e2(X)+tr(J_t X^2)+eta*tr(J_t X))+phi(tr X).
Profiles are manufactured by remaining size/current height; a level parity
and one residue modulo four preserve the linear source. No partitions are listed.
"""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'work_norm_slice_agent'))
from invariant_quadratic_matrix import quadratic_anf,polynomial_value,quadratic_sum
from invariant_quadratic_scalar_gauss import two_scalar_matrix_gaussians
from matrix_kloosterman import Field
from two_invariant_quadratic_matrix import gaussian_rows
from feedback_nilpotent_gaussians import shifted_trace_polynomial

def regular_chain_quadratic_gap(t,field_h,beta,phi,eta=0):
    F=Field(field_h);q=F.q;phi=set(phi)
    if type(t) is not int or t<1 or not 0<=beta<q or not 0<=eta<q:
        raise ValueError('invalid dimension or field coefficient')
    if any(type(m) is not int or m<0 or m.bit_length()>F.a or m.bit_count()>2 for m in phi):
        raise ValueError('Boolean quadratic trace source required')
    gaussian=gaussian_rows(t,q)
    # tail[remaining][previous_height][next_level_parity][even_height_sum_mod4].
    # next_level_parity=1 means an even numbered profile level.
    tail=[[[[0]*4 for _ in range(2)] for _ in range(t+1)] for _ in range(t+1)]
    for k in range(t+1):
        for p in range(2):tail[0][k][p][0]=1
    transitions=0
    for remaining in range(1,t+1):
        for previous in range(1,t+1):
            for height in range(1,min(previous,remaining)+1):
                weight=q**(height*(height+1)//2)*gaussian[previous][height]
                for level in range(2):
                    shift=level*height
                    for residue in range(4):
                        tail[remaining][previous][level][(residue+shift)%4] += weight*tail[remaining-height][height][1-level][residue]
                transitions+=1
    top=[1]
    for k in range(t):top.append(top[-1]*(q**(t-k)-1))
    profiles=[[0]*4 for _ in range(t+1)];profiles[0][0]=1
    for c in range(1,t+1):
        for k in range(1,c+1):
            for residue in range(4):profiles[c][residue]+=top[k]*tail[c-k][k][1][residue]
    if beta:
        first,first_meta=two_scalar_matrix_gaussians(t,field_h,beta,phi)
        shifted=shifted_trace_polynomial(phi,F,eta,beta)
        second,second_meta=two_scalar_matrix_gaussians(t,field_h,beta,shifted)
        values=[first,second]
        phase_bit=F.trace(F.mul(beta,F.mul(eta,eta)))
        gaussians=[[(1-2*(phase_bit*((r*(r-1)//2)%2)))*values[r%2][b]
                    for r in range(4)] for b in range(t+1)]
        gauss_meta=dict(original=first_meta,shifted=second_meta,
                        shifted_trace_anf=sorted(shifted),phase_bit=phase_bit)
    else:
        scalar=quadratic_sum(lambda x:polynomial_value(phi,x),F.a)
        gauss_meta=dict(scalar_gauss=scalar,gauss_dimensions=[F.a])
        gaussians=[]
        for b in range(t+1):
            if b%2:values=[q**(b*(b+1)//2-1)*scalar]*4
            else:values=[(1-2*polynomial_value(phi,eta if (residue+b//2)%2 else 0))*q**(b*(b+1)//2)
                         for residue in range(4)]
            gaussians.append(values)
    normalized=0
    for c in range(t+1):
        b=t-c
        normalized+=q**(c*(c-1)//2+c*b)*sum(profiles[c][r]*gaussians[b][r] for r in range(4))
    gap=q**(t*t)*normalized
    return gap,dict(route='unbounded regular chain, remaining-size and height aggregation',
        matrix_size=t,field_degree=F.a,field_modulus=field_h,beta=beta,eta=eta,
        trace_quadratic_anf=sorted(phi),profile_weights_by_even_height_mod4=profiles,
        residual_gaussians_by_trace_shift=gaussians,scalar_gaussian_backend=gauss_meta,
        profile_transitions=transitions,uniform_polynomial_time=True,
        enumerated_profiles=0,enumerated_subspaces=0,enumerated_field_elements=0,
        enumerated_original_assignments=0)

def count_acquired_regular_chain(algebra,beta,D,phi,eta=0):
    cp,primary=algebra.primary_data(D)
    if len(primary)!=1:raise ValueError('source operator does not have a single primary block')
    block=primary[0]
    if len(block['irreducible'])!=2 or block['jordan_columns']!=[1]*algebra.t:
        raise ValueError('source is not scalar plus one full nilpotent Jordan chain')
    scalar=block['irreducible'][0];F=algebra.F
    shifted=quadratic_anf(lambda s:polynomial_value(phi,s)^F.trace(
        F.mul(scalar,F.mul(s,s))^F.mul(F.mul(eta,scalar),s)),F.a)
    gap,data=regular_chain_quadratic_gap(algebra.t,algebra.h,beta,shifted,eta)
    data.update(operator_class='unrestricted single Jordan chain',source_eigenvalue=scalar,
                source_reduced_charpoly=cp,acquired_jordan_columns=block['jordan_columns'])
    return gap,data


def count_binary_rank_two_source(poly,algebra):
    """Manufacture a source pencil over F2, without a nonlinear trace marker.

The trace-dual polar is expanded in the certified A tensor A^op envelope.
Its rank-two alternating coefficient matrix manufactures span{W,DW}.
A unit in this binary two-space normalizes it to an inner derivation.
This branch currently counts a single full Jordan chain with its induced
linear chain term; it verifies every coefficient and the primary type.
"""
    from raw_matrix_trace import solve,flat,compose,bits,linear_apply,identity
    from binary_modules import basis
    if algebra.a!=1:raise ValueError('binary rank-two pencil branch requires F2')
    d=algebra.d;poly=set(poly);polar=[0]*d
    for monomial in poly:
        if monomial.bit_count()==2:
            i,j=bits(monomial);polar[i]^=1<<j;polar[j]^=1<<i
    H=[solve(algebra.gram,column) for column in polar]
    envelope=[flat(compose(L,R),d) for L in algebra.left for R in algebra.right]
    coefficients=solve(envelope,flat(H,d))
    if coefficients is None:raise AssertionError('certified bimodule envelope failed')
    rows=[(coefficients>>(d*i))&((1<<d)-1) for i in range(d)]
    if any((rows[i]>>i)&1 for i in range(d)) or any(((rows[i]>>j)^(rows[j]>>i))&1
            for i in range(d) for j in range(i+1,d)):
        raise ValueError('source polar has no alternating multiplication pencil')
    pencil=basis(rows)
    if len(pencil)!=2:raise ValueError('multiplication-envelope coefficient rank is not two')
    candidates=pencil+[pencil[0]^pencil[1]]
    unit=next((value for value in candidates if algebra.is_unit(value)),None)
    if unit is None:raise ValueError('manufactured binary pencil contains no unit')
    R=solve(algebra.left_matrix(unit),algebra.one)
    normalized=quadratic_anf(lambda x:polynomial_value(poly,algebra.mul(R,x)),d)
    npolar=[0]*d
    for monomial in normalized:
        if monomial.bit_count()==2:
            i,j=bits(monomial);npolar[i]^=1<<j;npolar[j]^=1<<i
    NH=[solve(algebra.gram,column) for column in npolar]
    derivations=[flat([algebra.mul(1<<i,1<<j)^algebra.mul(1<<j,1<<i)
                     for j in range(d)],d) for i in range(d)]
    D=solve(derivations,flat(NH,d))
    if D is None:raise ValueError('normalized source pencil is not an inner derivation')
    cp,primary=algebra.primary_data(D)
    if len(primary)!=1 or len(primary[0]['irreducible'])!=2 or primary[0]['jordan_columns']!=[1]*algebra.t:
        raise ValueError('binary pencil source is not a single full Jordan chain')
    scalar=primary[0]['irreducible'][0];N=D^(algebra.one if scalar else 0)
    canonical=quadratic_anf(lambda x:algebra.trace(algebra.mul(N,algebra.mul(x,x))),d)
    residual=normalized^canonical
    if any(m.bit_count()>1 for m in residual):raise AssertionError('inner polar did not cancel')
    linear=sum(m for m in residual if m)
    source=algebra.source(linear,identity(d))
    params=solve([algebra.one,N],source)
    if params is None:raise ValueError('linear refinement is outside the manufactured source pencil')
    phi=({0} if 0 in residual else set())|({1} if params&1 else set());eta=(params>>1)&1
    reconstructed=canonical^quadratic_anf(lambda x:polynomial_value(phi,algebra.relative_trace(x))^
        (algebra.trace(algebra.mul(N,x)) if eta else 0),d)
    if reconstructed!=normalized:raise AssertionError('binary pencil full coefficient identity')
    gap,backend=regular_chain_quadratic_gap(algebra.t,3,0,phi,eta)
    backend.update(operator_class='binary rank-two pencil with unbounded Jordan chain',
        source_reduced_charpoly=cp,acquired_jordan_columns=primary[0]['jordan_columns'])
    return gap,backend,dict(acquired_unit=unit,acquired_inverse_unit=R,
        multiplication_pencil_basis=pencil,multiplication_tensor_rank=2,
        acquired_squarezero_or_nilpotent_operator=N,extra_linear_chain_coefficient=eta,
        full_coefficient_identity_verified=True,unit_acquisition_route='rank-two multiplication envelope')
