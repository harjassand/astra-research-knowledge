#!/usr/bin/env python3
"""Acquire a matrix source from raw ANF/program and count its whole domain.

The full-count bound is polynomial for each fixed acquired minimal
polynomial degree h. Neither a unit nor an operator decomposition is an
input. Rejection of descriptions outside the admitted family is explicit.
"""
from pathlib import Path
import sys,time,json,argparse
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/p) for p in ('work_matrix_root','work_norm_frontier_agent',
    'work_norm_glue_agent','work_norm_slice_agent')]
from primary_modular_compiler import (hidden_groups,AcquiredMatrixAlgebra,acquire_center,
    bits,identity,inverse,linear_apply,solve,quadratic_anf,polynomial_value,
    acquire_operator_linear_refinement,recover_from_raw_arbitrary_source)
from arbitrary_operator_hall import quotient_matrix,transpose_partition
from minimal_polynomial_counter import full_matrix_cubic_count


def count_acquired_minimal_polynomial(algebra,beta,D,phi=(),eta=0):
    polynomial,components=algebra.primary_data(D)
    shapes=[transpose_partition(item['jordan_columns']) for item in components]
    representative=quotient_matrix(components,shapes,algebra.F)
    result=full_matrix_cubic_count(representative,algebra.h,beta,phi,eta)
    result['acquisition'].update(acquired_reduced_characteristic_polynomial=polynomial,
        source_unit_and_operator_manufactured=True)
    return result


def acquire_raw_minimal_source(poly,n,raw_affine_markers=(),allow_zero_beta=False):
    """Manufacture the source and its coordinate maps; verify every coefficient.

    Optional markers are literal affine-gate coefficient masks in the
    original input coordinates. They are only candidates for a source
    unit. Each candidate must pass the full source identity afterwards.
    No marker is assumed to be the desired field trace.
    """
    begun=time.perf_counter();poly=set(poly);raw_affine_markers=tuple(raw_affine_markers)
    if type(n) is not int or n<=0 or any(type(m) is not int or m<0 or m.bit_length()>n or m.bit_count()>3 for m in poly):
        raise ValueError('explicit raw cubic Boolean ANF required')
    grouped,slices,group_map,stats=hidden_groups(poly,n)
    algebra=AcquiredMatrixAlgebra(slices);d=algebra.d
    centered,offset=acquire_center(grouped,slices,d,allow_within=True)
    lower=[m for m in centered if 0<m.bit_count()<=2]
    groups={i//d for m in lower for i in bits(m)}
    if len(groups)==1:group=next(iter(groups))
    elif not groups and allow_zero_beta:
        # A pure cubic has no distinguished source group. Manufacture one
        # from a needed affine gate, using the same verified trace duality.
        group=None
        for marker in raw_affine_markers:
            if type(marker) is not int or marker<=0 or marker.bit_length()>n:continue
            mask=sum(((marker&column).bit_count()%2)<<i for i,column in enumerate(group_map))
            support={i//d for i in bits(mask)}
            if len(support)!=1:continue
            candidate=next(iter(support));local_mask=mask>>(candidate*d)
            candidate_back=inverse([identity(d),algebra.Y,algebra.Z][candidate])
            normalized_mask=sum(((local_mask&column).bit_count()%2)<<i for i,column in enumerate(candidate_back))
            if algebra.is_unit(algebra.source(normalized_mask,identity(d))):group=candidate;break
        if group is None:raise ValueError('pure cubic requires an acquired affine trace marker to select its source group')
    else:raise ValueError('one acquired group must contain every nonconstant source term')
    local={m>>(group*d) for m in lower}
    if 0 in centered:local.add(0)
    back=inverse([identity(d),algebra.Y,algebra.Z][group])
    source=quadratic_anf(lambda x:polynomial_value(local,linear_apply(back,x)),d)
    fitted=None;marker_basis={};marker_attempts=0
    for marker in raw_affine_markers:
        if type(marker) is not int or marker<0 or marker.bit_length()>n:
            raise ValueError('affine marker is not an original-input linear mask')
        independent=marker
        while independent:
            pivot=independent.bit_length()-1
            if pivot not in marker_basis:marker_basis[pivot]=independent;break
            independent^=marker_basis[pivot]
        if not independent:continue
        grouped_mask=sum(((marker&column).bit_count()%2)<<i for i,column in enumerate(group_map))
        if grouped_mask&~(((1<<d)-1)<<(group*d)):continue
        local_mask=grouped_mask>>(group*d)
        normalized_mask=sum(((local_mask&column).bit_count()%2)<<i for i,column in enumerate(back))
        unit=algebra.source(normalized_mask,identity(d))
        if not algebra.is_unit(unit):continue
        marker_attempts+=1;inverse_unit=solve(algebra.left_matrix(unit),algebra.one)
        try:fitted=acquire_operator_linear_refinement(source,algebra,inverse_unit)
        except ValueError:continue
        fitted[-1].update(unit_acquisition_route='observed affine gate, trace duality, and full source identity',
            original_affine_marker=marker,affine_marker_attempts=marker_attempts)
        break
    if fitted is None:
        try:fitted=acquire_operator_linear_refinement(source,algebra)
        except ValueError:
            if algebra.t==2:
                from matrix2_pfaffian_unit import count_matrix2_pfaffian_source
                _,_,unit_evidence=count_matrix2_pfaffian_source(source,algebra)
                inverse_unit=unit_evidence['acquired_inverse_unit']
            elif algebra.t>=4:
                unit,unit_evidence=recover_from_raw_arbitrary_source(source,algebra)
                inverse_unit=solve(algebra.left_matrix(unit),algebra.one)
            else:raise ValueError('general intrinsic unit fallback requires matrix size>=4 or a verified affine marker')
            fitted=acquire_operator_linear_refinement(source,algebra,inverse_unit)
            fitted[-1].update(intrinsic_unit_acquisition=unit_evidence,
                unit_acquisition_route='manufactured intrinsic unit and exact full source fit')
    beta,D,phi,eta,evidence=fitted
    if not beta and not allow_zero_beta:
        raise ValueError('raw acquisition route requires nonzero exterior-square coefficient')
    acquired_seconds=time.perf_counter()-begun
    stats.update(algebra.stats);stats.update(evidence)
    return dict(algebra=algebra,beta=beta,D=D,phi=phi,eta=eta,evidence=evidence,
        stats=stats,affine_offset=offset,quadratic_group=group,group_map=group_map,
        local_to_algebra=[identity(d),algebra.Y,algebra.Z][group],
        raw_monomials=len(poly),original_bits=n,acquisition_seconds=acquired_seconds)


def compile_raw_minimal_polynomial(poly,n):
    begun=time.perf_counter();acquired=acquire_raw_minimal_source(poly,n)
    algebra=acquired['algebra'];beta=acquired['beta'];D=acquired['D']
    phi=acquired['phi'];eta=acquired['eta']
    result=count_acquired_minimal_polynomial(algebra,beta,D,phi,eta)
    if result['original_independent_bits']!=n:raise AssertionError('original input count changed')
    result.update(raw_cubic_input=True,original_bits=n,zeros=((1<<n)+result['gap'])//2)
    result['raw_acquisition']=dict(details=acquired['stats'],raw_monomials=acquired['raw_monomials'],
        affine_offset=acquired['affine_offset'],quadratic_group=acquired['quadratic_group'],
        acquisition_seconds=acquired['acquisition_seconds'],
        original_domain_preserved=True,full_source_coefficient_identity_verified=True,
        supplied_unit_or_operator_decomposition=False,total_seconds=time.perf_counter()-begun)
    return result


def compile_minimal_polynomial_program(program):
    from matrix_circuit_counter import compile_gate_anf
    poly,program_stats=compile_gate_anf(program)
    result=compile_raw_minimal_polynomial(poly,program['inputs'])
    result['program']=program_stats
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('source',type=Path)
    parser.add_argument('--output',type=Path);args=parser.parse_args()
    data=json.loads(args.source.read_text())
    result=compile_minimal_polynomial_program(data) if 'gates' in data else compile_raw_minimal_polynomial(data['anf'],data['n'])
    rendered=json.dumps(result,indent=2)+'\n'
    if args.output:args.output.write_text(rendered)
    else:print(rendered,end='')


if __name__=='__main__':main()
