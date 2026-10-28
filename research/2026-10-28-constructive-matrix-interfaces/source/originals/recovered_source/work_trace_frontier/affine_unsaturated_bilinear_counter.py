#!/usr/bin/env python3
"""Acquire affine Hom slices directly from raw Boolean quadratic programs.

The right offset may lie outside the actual right-input subspace.  No common
original affine center is assumed.  Every residual linear output is checked;
none is discarded by reduction to the independent cross-output coordinates.
"""
from pathlib import Path
import argparse,json,sys,time
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
sys.path[:0]=[str(ROOT/'work_matrix_root'),str(ROOT/'work_multiprimary_audit')]
from unsaturated_bilinear_counter import (acquire_hom_slice,transpose_split,
    slice_target_fiber,BinaryCoordinates,pack,apply_binary,affine_solutions,
    validate_trace_program,acquire_reversible_terminal_and,invert_terminal)
from source_free_bilinear_split import acquire_source_free_bilinear_split
from central_quadratic_tensor_compiler import compose_quadratic


def transpose_affine_split(split):
    result=transpose_split(split)
    result['left_linear_output_columns']=split['right_linear_output_columns'][:]
    result['right_linear_output_columns']=split['left_linear_output_columns'][:]
    return result


def acquire_affine_hom_slice(split):
    """Certify Q=B(u,v)+L(u)+R(v)+c as evaluation on T0+iota(V)."""
    began=time.perf_counter();certificate=acquire_hom_slice(split);C=certificate['nucleus']
    U=C['left_dimension'];V=C['right_dimension'];M=C['output_dimension'];m=C['marked_quadratics']
    indices=C['output_basis_mark_indices'];dependencies=C['marked_output_coordinates']
    L=split['left_linear_output_columns'];R=split['right_linear_output_columns']
    if len(L)!=U or len(R)!=V:raise ValueError('missing complete affine linear output columns')
    def project(column):return sum(((column>>j)&1)<<b for b,j in enumerate(indices))
    def dependencies_hold(column):
        value=project(column)
        return all((row&value).bit_count()%2==((column>>i)&1) for i,row in enumerate(dependencies))
    if not all(dependencies_hold(column) for column in L+R):
        raise ValueError('a residual linear output violates an acquired cross-output dependency')
    reduced_L=list(map(project,L));reduced_R=list(map(project,R))
    forms=[split['cross_matrices'][j] for j in indices]
    shift=affine_solutions([(forms[b][j],(reduced_R[j]>>b)&1)
        for j in range(V) for b in range(M)],U)
    if shift is None:raise ValueError('right linear term is not evaluation at one common left shift')
    if shift[1]:raise AssertionError('left shift is nonunique despite zero left bilinear radical')
    u0=shift[0];HC=BinaryCoordinates(certificate['hom_basis'])
    try:offset=HC.coordinates(pack(reduced_L,M))
    except ValueError as error:raise ValueError('left linear term is outside the acquired full Hom space') from error
    original_offset=split['affine_offset']^apply_binary(split['coordinate_columns'][:U],u0)
    actual_constant=split['output_constant']^apply_binary(L,u0)
    C=dict(C,output_constant=actual_constant);certificate=dict(certificate,nucleus=C)
    # Verify the complete original marked-polynomial identity after the shift.
    coordinates=[1<<j for j in range(U+V)]
    shifted=[compose_quadratic(set(f),u0,coordinates) for f in split['centered_quadratics']]
    for i,f in enumerate(shifted):
        expected={0} if actual_constant>>i&1 else set()
        expected^={1<<j for j in range(U) if L[j]>>i&1}
        expected^={(1<<j)|(1<<(U+k)) for k,column in enumerate(split['cross_matrices'][i])
            for j in range(U) if column>>j&1}
        if f!=expected:raise AssertionError('complete affine Hom reconstruction failed')
    certificate.update(affine_hom_offset=offset,left_input_shift=u0,
        original_affine_input_offset=original_offset,original_input_coordinate_columns=split['coordinate_columns'],
        residual_linear_output_dependencies_verified=True,
        common_original_affine_center_acquired=split['shared_affine_center_acquired'],
        affine_offset_in_actual_right_input=True,complete_marked_affine_identity_verified=True,
        affine_acquisition_seconds=time.perf_counter()-began)
    right=BinaryCoordinates(certificate['right_embedding_columns'])
    try:right.coordinates(offset)
    except ValueError:certificate['affine_offset_in_actual_right_input']=False
    return certificate


def acquire_best_affine_hom_slice(quadratics,n):
    split=acquire_source_free_bilinear_split(quadratics,n,require_shared_center=False)
    accepted=[];declines=[]
    for oriented in (split,transpose_affine_split(split)):
        try:certificate=acquire_affine_hom_slice(oriented)
        except ValueError as error:declines.append(str(error));continue
        accepted.append((certificate,oriented))
    if not accepted:raise ValueError('neither acquired orientation admits the full affine slice: '+'; '.join(declines))
    certificate,oriented=min(accepted,key=lambda pair:pair[0]['codimension'])
    certificate['orientations_examined']=2;certificate['orientation_declines']=declines
    return certificate,oriented


def affine_slice_target_fiber(certificate,target):
    return slice_target_fiber(certificate,target,certificate['affine_hom_offset'])


def count_affine_unsaturated_target(quadratics,n,target=0):
    C,split=acquire_best_affine_hom_slice(quadratics,n)
    fiber=affine_slice_target_fiber(C,target);ones=fiber['population']
    return dict(original_input_bits=n,ones=ones,zeros=(1<<n)-ones,target=target,
        fiber=fiber,split_certificate=split,affine_slice_certificate=C,
        auxiliary_independent_inputs=0,original_assignments_enumerated=0,
        supplied_field_shape_source_offset_or_decomposition=False)


def count_affine_unsaturated_native(program):
    began=time.perf_counter();n=program.get('inputs',program.get('n'))
    if type(n) is not int or n<1 or n>len(program.get('gates',[]))+1:
        raise ValueError('zero-common-radical admission requires every input in the explicit DAG')
    n,gates,output=validate_trace_program(program,n)
    reversible=acquire_reversible_terminal_and(program);target=invert_terminal(reversible)
    result=count_affine_unsaturated_target(reversible['initial_quadratics'],n,target)
    result.update(ordinary_gates=len(gates),gap=(1<<n)-2*result['ones'],
        reversible_certificate=reversible,seconds=time.perf_counter()-began)
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('source',type=Path)
    parser.add_argument('--output',type=Path);args=parser.parse_args()
    result=count_affine_unsaturated_native(json.loads(args.source.read_text()));text=json.dumps(result,indent=2)+'\n'
    if args.output:args.output.write_text(text)
    else:print(text,end='')
