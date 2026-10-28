#!/usr/bin/env python3
"""Source-free acquired bilinear-product counting from an ordinary gate DAG.

The left nucleus certifies a universal module evaluation. All shapes, field
degree, affine input coordinates, output dependencies and target rank are
manufactured. No canonical field, matrix units, or supplied product map.
"""
from pathlib import Path
from math import gcd
import argparse,json,sys,time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/p) for p in ('work_matrix_root','work_multiprimary_audit','work_trace_frontier')]
from adjoint_matrix_product_counter import (BinaryCoordinates,pack,unpack,product,
    apply_binary,affine_solutions,independent_basis,gaussian_binomial)
from finite_simple_binary_algebra import certify_finite_simple_matrix_algebra
from projector_quadratic_fibers import (acquire_reversible_terminal_and,invert_terminal,
    validate_trace_program,prepared_program)
if hasattr(sys,'set_int_max_str_digits'):sys.set_int_max_str_digits(0)


def acquire_left_product_nucleus(split,require_saturated=True):
    """Acquire every pair (A,C) satisfying Q(Au,v)=C Q(u,v)."""
    begun=time.perf_counter();U=split['left_dimension'];V=split['right_dimension']
    forms=split['cross_matrices'];m=len(forms);span=BinaryCoordinates();basis_indices=[]
    for i,H in enumerate(forms):
        if len(H)!=V or any(x<0 or x.bit_length()>U for x in H):
            raise ValueError('invalid cross-form matrix')
        if span.insert(pack(H,U)) is not None:basis_indices.append(i)
    M=len(span.basis)
    if not M:raise ValueError('zero output map')
    basis_forms=[[value>>(U*j)&((1<<U)-1) for j in range(V)] for value in span.basis]
    left_rows=[H[j] for H in basis_forms for j in range(V)]
    right_rows=[sum(((H[j]>>i)&1)<<j for j in range(V)) for H in basis_forms for i in range(U)]
    if affine_solutions([(x,0) for x in left_rows],U)[1] or affine_solutions(
        [(x,0) for x in right_rows],V)[1]:raise ValueError('bilinear map has a one-sided radical')
    value_columns=[[sum(((H[j]>>i)&1)<<k for k,H in enumerate(basis_forms))
        for j in range(V)] for i in range(U)]
    spread={z:sum(((z>>j)&1)<<(M*j) for j in range(M))
        for row in value_columns for z in row}
    equations=[];input_width=U*U
    for i,H in enumerate(basis_forms):
        for a in range(U):
            for b in range(V):
                equations.append(((H[b]<<(U*a))^(spread[value_columns[a][b]]<<(input_width+i)),0))
    solution=affine_solutions(equations,input_width+M*M)
    nucleus=solution[1];left_mask=(1<<input_width)-1
    inputs=[value&left_mask for value in nucleus]
    outputs=[value>>input_width for value in nucleus]
    output_coordinates=BinaryCoordinates(outputs)
    if len(output_coordinates.basis)!=len(nucleus):
        raise AssertionError('output nucleus representation is not faithful')
    # A simple matrix algebra of dimension a*p^2 has ap dividing both
    # faithful module dimensions. Reject impossible parabolic alternatives
    # before building their otherwise potentially large multiplication table.
    if len(nucleus)>gcd(U,M)**2:
        raise ValueError('nucleus dimension is incompatible with two simple-module multiplicities')
    algebra=certify_finite_simple_matrix_algebra(outputs,M)
    if algebra['basis']!=outputs:raise AssertionError('nucleus basis order changed')
    a=algebra['field_degree'];p=algebra['matrix_degree'];r=algebra['module_multiplicity']
    if U%(a*p):raise ValueError('left input is not an integral simple-module multiple')
    d=U//(a*p)
    if d<1 or V>a*d*r:raise ValueError('right input exceeds the module-homomorphism space')
    if require_saturated and V!=a*d*r:
        raise ValueError('right input does not fill the module-homomorphism space')
    unit=algebra['unit_coordinates']
    if apply_binary(inputs,unit)!=pack([1<<i for i in range(U)],U):
        raise AssertionError('nucleus identity acts incorrectly on input')
    # All defining linear identities were solved in actual coefficient space.
    # Check representation multiplication as an additional finite certificate.
    input_matrices=[unpack(A,U) for A in inputs]
    for i,A in enumerate(input_matrices):
        for j,B in enumerate(input_matrices):
            if pack(product(A,B),U)!=apply_binary(inputs,algebra['multiplication_table'][i][j]):
                raise AssertionError('input and output nucleus actions disagree')
    return dict(input_bits=U+V,marked_quadratics=m,output_dimension=M,
        left_dimension=U,right_dimension=V,field_degree=a,
        left_matrix_rows=p,inner_dimension=d,right_matrix_columns=r,
        output_basis_mark_indices=basis_indices,
        marked_output_coordinates=[span.coordinates(pack(H,U)) for H in forms],
        output_constant=split['output_constant'],nucleus_input_operators=inputs,
        nucleus_output_operators=outputs,nucleus_certificate=algebra,
        no_left_or_right_radical=True,homomorphism_space_dimension=a*d*r,
        right_input_fills_homomorphism_space=(V==a*d*r),
        right_input_codimension=a*d*r-V,nucleus_equations=len(equations),
        supplied_field_shape_source_or_decomposition=False,
        global_output_values_enumerated=0,seconds=time.perf_counter()-begun)


def rectangular_product_population(p,d,r,k,field_degree):
    if k<0 or k>min(p,r):raise ValueError('invalid target rank')
    answer=0
    for s in range(k,min(p,d)+1):
        onto=1
        for j in range(s):onto*=((1<<(field_degree*d))-(1<<(field_degree*j)))
        answer+=gaussian_binomial(p-k,s-k,field_degree)*onto*(1<<(field_degree*r*(d-s)))
    return answer


def bilinear_product_target_fiber(certificate,target):
    C=certificate;m=C['marked_quadratics']
    if not C['right_input_fills_homomorphism_space']:
        raise ValueError('unsaturated right input requires the slice Fourier consumer')
    if type(target) is not int or target<0 or target.bit_length()>m:raise ValueError('invalid target')
    rhs=target^C['output_constant']
    value=sum(((rhs>>i)&1)<<j for j,i in enumerate(C['output_basis_mark_indices']))
    for i,row in enumerate(C['marked_output_coordinates']):
        if (row&value).bit_count()%2!=((rhs>>i)&1):
            return dict(population=0,reason='target violates actual affine output dependencies')
    M=C['output_dimension'];orbit=[apply_binary(unpack(A,M),value) for A in C['nucleus_output_operators']]
    dimension=len(independent_basis(orbit));a=C['field_degree'];p=C['left_matrix_rows']
    k,remainder=divmod(dimension,a*p)
    if remainder:raise AssertionError('target orbit has incompatible module dimension')
    answer=rectangular_product_population(p,C['inner_dimension'],C['right_matrix_columns'],k,a)
    if not 0<=answer<=1<<C['input_bits']:raise AssertionError('invalid original fiber population')
    return dict(population=answer,target_output_coordinates=value,
        target_orbit_dimension=dimension,matrix_target_rank=k,
        reason='acquired universal module evaluation',original_assignments_enumerated=0,
        global_output_values_enumerated=0)


def count_bilinear_product_native(program):
    from source_free_bilinear_split import acquire_source_free_bilinear_split
    begun=time.perf_counter();n=program.get('inputs',program.get('n'))
    if type(n) is not int or n<1 or n>len(program.get('gates',[]))+1:
        raise ValueError('the zero-common-radical family requires every declared input in the explicit DAG')
    n,gates,output=validate_trace_program(program,n)
    reversible=acquire_reversible_terminal_and(program)
    split=acquire_source_free_bilinear_split(reversible['initial_quadratics'],n)
    nucleus=acquire_left_product_nucleus(split);target=invert_terminal(reversible)
    fiber=bilinear_product_target_fiber(nucleus,target);ones=fiber['population']
    return dict(original_input_bits=n,ordinary_gates=len(gates),ones=ones,zeros=(1<<n)-ones,
        gap=(1<<n)-2*ones,target=target,fiber=fiber,split_certificate=split,
        nucleus_certificate=nucleus,reversible_certificate=reversible,
        source_scaffold_supplied_or_required=False,auxiliary_independent_inputs=0,
        original_assignments_enumerated=0,seconds=time.perf_counter()-begun)


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('source',type=Path)
    parser.add_argument('--output',type=Path);args=parser.parse_args()
    result=count_bilinear_product_native(json.loads(args.source.read_text()))
    rendered=json.dumps(result,indent=2)+'\n'
    if args.output:args.output.write_text(rendered)
    else:print(rendered,end='')


if __name__=='__main__':main()
