#!/usr/bin/env python3
"""Exact polynomial dual aggregation from a manufactured full matrix algebra.

No unit map, field coordinates, matrix units, or multiplier algebra is given.
A regular-module dimension and zero common kernel certify the needed torsor
without constructing an isomorphism. A joint target orbit certifies one
natural multiplicity component. Every dual matrix can then be aggregated by
rank and target-image rank, including a growing noncommutative matrix degree.
"""
from pathlib import Path
import argparse,json,sys,time
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
sys.path[:0]=[str(ROOT/'work_matrix_root'),str(ROOT/'work_multiprimary_audit')]
from semisimple_dual_counter import (remainder,BinaryCoordinates,pack,unpack,
    product,apply_binary,linear_kernel,independent_basis,rectangular_unpack,
    gaussian_binomial,signed_universal_product,acquire_source_free_bilinear_split,
    acquire_best_hom_slice,validate_trace_program,acquire_reversible_terminal_and,
    invert_terminal)
from finite_simple_binary_algebra import certify_finite_simple_matrix_algebra


def acquire_noncommutative_dual(certificate):
    begun=time.perf_counter();C=certificate['nucleus'];U=C['left_dimension'];M=C['output_dimension']
    a=C['field_degree'];p=C['left_matrix_rows'];d=C['inner_dimension']
    if U!=M:raise ValueError('regular dual-torsor certificate requires equal input/output module dimensions')
    dual=certificate['dual_reverse_matrices'];c=len(dual)
    if not c:raise ValueError('zero dual needs no multiplier compression')
    DS=BinaryCoordinates(dual);Dmat=[rectangular_unpack(x,U,M) for x in dual]
    L=certificate['endomorphism_basis'][:];dimensions=[len(L)]
    for D in Dmat:
        images=[remainder(DS,pack(product(unpack(X,U),D),U)) for X in L]
        L=[apply_binary(L,v) for v in linear_kernel(images,U*M)];dimensions.append(len(L))
    algebra=certify_finite_simple_matrix_algebra(L,U)
    if algebra['field_degree']!=a:raise ValueError('multiplier center has a different field degree')
    s=algebra['matrix_degree']
    if c!=a*s*s:raise ValueError('actual dual is not one regular left-multiplier module')
    if d%s:raise ValueError('multiplier degree does not divide the original inner module dimension')
    h=d//s
    center_actual=[apply_binary(L,z) for z in algebra['center_basis']]
    Z=BinaryCoordinates(center_actual)
    for z in C['nucleus_certificate']['center_basis']:
        try:Z.coordinates(apply_binary(C['nucleus_input_operators'],z))
        except ValueError as error:raise ValueError('multiplier center is not the acquired base scalar field') from error
    common_kernel_rows=[sum(((D[j]>>i)&1)<<j for j in range(M)) for D in Dmat for i in range(U)]
    if len(independent_basis(common_kernel_rows))!=M:
        raise ValueError('actual dual has a nonzero common kernel')
    # These checks imply a simple-module torsor; no search for a full-rank
    # linear combination is necessary, and none is performed here.
    return dict(multiplier_basis=L,multiplier_certificate=algebra,
        multiplier_dimensions=dimensions,multiplier_dimension=len(L),
        field_degree=a,matrix_degree=s,natural_multiplicity=h,codimension=c,
        regular_dual_module_dimension_verified=True,zero_common_dual_kernel_verified=True,
        common_base_scalar_field_verified=True,isomorphism_supplied_or_constructed=False,
        matrix_units_supplied_or_constructed=False,dual_elements_enumerated=0,
        seconds=time.perf_counter()-begun)


def projected_matrix_rank_population(s,k,j,rho,a):
    """# A in M_s(F_(2^a)) of rank j with rank(CA)=rho, rank(C)=k."""
    if not (0<=k<=s and 0<=j<=s and 0<=rho<=min(k,j) and j-rho<=s-k):return 0
    onto=1
    for i in range(j):onto*=((1<<(a*s))-(1<<(a*i)))
    return (gaussian_binomial(s-k,j-rho,a)*gaussian_binomial(k,rho,a)*onto*
        (1<<(a*(s-k-j+rho)*rho)))


def compressed_noncommutative_target(certificate,compression,target,affine_hom_offset=0):
    C=certificate['nucleus'];U=C['left_dimension'];M=C['output_dimension'];m=C['marked_quadratics']
    if type(target) is not int or target<0 or target.bit_length()>m:raise ValueError('invalid target')
    if type(affine_hom_offset) is not int or affine_hom_offset<0 or affine_hom_offset.bit_length()>len(certificate['hom_basis']):
        raise ValueError('invalid Hom offset')
    if any((lam&affine_hom_offset).bit_count()%2 for lam in certificate['right_annihilator_basis']):
        raise ValueError('nontrivial affine phase is outside this unweighted noncommutative rank consumer')
    rhs=target^C['output_constant'];y=sum(((rhs>>i)&1)<<j for j,i in enumerate(C['output_basis_mark_indices']))
    if any((row&y).bit_count()%2!=((rhs>>i)&1) for i,row in enumerate(C['marked_output_coordinates'])):
        return dict(population=0,reason='target violates actual output dependencies')
    a=C['field_degree'];p=C['left_matrix_rows'];d=C['inner_dimension'];r=C['right_matrix_columns']
    s=compression['matrix_degree'];h=compression['natural_multiplicity'];ap=a*p
    input_actions=[unpack(x,U) for x in C['nucleus_input_operators']]
    output_actions=[unpack(x,M) for x in C['nucleus_output_operators']]
    k,rem=divmod(len(independent_basis(apply_binary(A,y) for A in output_actions)),ap)
    if rem:raise AssertionError('nonintegral original target rank')
    vectors=[apply_binary(rectangular_unpack(D,U,M),y) for D in certificate['dual_reverse_matrices']]
    joint=independent_basis(apply_binary(A,z) for A in input_actions for z in vectors)
    if y:
        if len(joint)!=ap*s:
            raise ValueError('target is not supported on one acquired joint simple-module copy')
        if k>s:raise AssertionError('single joint-copy target has too large original rank')
    elif joint:raise AssertionError('zero target has a nonzero joint orbit')
    histogram={}
    for j in range(s+1):
        for rho in range(min(k,j)+1):
            population=projected_matrix_rank_population(s,k,j,rho,a)
            if population:histogram[h*j,rho]=population
    if sum(histogram.values())!=1<<compression['codimension']:
        raise AssertionError('matrix-rank profile does not exhaust the actual dual dimension')
    total=sum(population*signed_universal_product(p,d,r,a,k,t,rho)
        for (t,rho),population in histogram.items())
    answer,rem=divmod(total,1<<compression['codimension'])
    if rem or not 0<=answer<=1<<C['input_bits']:raise AssertionError('invalid reconstructed original-input population')
    return dict(population=answer,matrix_target_rank=k,
        acquired_joint_target_orbit_dimension=len(joint),target_copy_certificate='zero or one natural joint S-A copy',
        codimension=compression['codimension'],matrix_multiplier_degree=s,
        multiplier_natural_multiplicity=h,
        rank_pair_histogram={f'{t},{rho}':v for (t,rho),v in histogram.items()},
        histogram_states=len(histogram),characters_enumerated=0,
        invertible_dual_element_search_performed=False,original_assignments_enumerated=0)


def count_noncommutative_dual_native(program):
    began=time.perf_counter();n=program.get('inputs',program.get('n'))
    if type(n) is not int or n<1 or n>len(program.get('gates',[]))+1:
        raise ValueError('explicit input-size admission failed')
    n,gates,output=validate_trace_program(program,n)
    reversible=acquire_reversible_terminal_and(program)
    split=acquire_source_free_bilinear_split(reversible['initial_quadratics'],n,allow_paired_components=True)
    C,split=acquire_best_hom_slice(split);compression=acquire_noncommutative_dual(C)
    target=invert_terminal(reversible);fiber=compressed_noncommutative_target(C,compression,target)
    ones=fiber['population']
    return dict(original_input_bits=n,ordinary_gates=len(gates),ones=ones,zeros=(1<<n)-ones,
        gap=(1<<n)-2*ones,target=target,fiber=fiber,compression_certificate=compression,
        slice_certificate=C,split_certificate=split,reversible_certificate=reversible,
        auxiliary_independent_inputs=0,original_assignments_enumerated=0,seconds=time.perf_counter()-began)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('source',type=Path)
    parser.add_argument('--output',type=Path);args=parser.parse_args()
    result=count_noncommutative_dual_native(json.loads(args.source.read_text()));text=json.dumps(result,indent=2)+'\n'
    if args.output:args.output.write_text(text)
    else:print(text,end='')
