#!/usr/bin/env python3
"""Polynomial contraction of acquired rank-one dual Hom slices."""
from pathlib import Path
import argparse,json,sys,time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'work_matrix_root'),str(ROOT/'work_multiprimary_audit')]
from unsaturated_bilinear_counter import *
from adjoint_matrix_product_counter import linear_kernel

def acquire_rank_one_dual(certificate):
    C=certificate;A=C['nucleus'];U=A['left_dimension'];M=A['output_dimension']
    unit_rank=A['field_degree']*A['left_matrix_rows']
    basis=C['dual_reverse_matrices'];checks=0
    for i,D in enumerate(basis):
        rank=len(independent_basis(rectangular_unpack(D,U,M)));checks+=1
        if rank!=unit_rank:raise ValueError('a dual basis map does not have field rank one')
        for E in basis[:i]:
            rank=len(independent_basis(rectangular_unpack(D^E,U,M)));checks+=1
            if rank>unit_rank:raise ValueError('a dual pair sum has field rank greater than one')
    return dict(slice_certificate=C,dual_basis_count=len(basis),
        checked_basis_and_pair_ranks=checks,entire_dual_span_rank_at_most_one=True,
        dual_vectors_enumerated=0,proof='pairwise rank-one common-image/common-row lemma')

def rank_one_slice_target(certificate,target,affine_hom_offset=0):
    begun=time.perf_counter();C=certificate['slice_certificate'];A=C['nucleus']
    m=A['marked_quadratics'];U=A['left_dimension'];M=A['output_dimension']
    if type(target) is not int or target<0 or target.bit_length()>m:raise ValueError('invalid target')
    if type(affine_hom_offset) is not int or affine_hom_offset<0 or affine_hom_offset.bit_length()>len(C['hom_basis']):
        raise ValueError('invalid acquired Hom-space offset')
    rhs=target^A['output_constant']
    y=sum(((rhs>>i)&1)<<j for j,i in enumerate(A['output_basis_mark_indices']))
    if any((row&y).bit_count()%2!=((rhs>>i)&1) for i,row in enumerate(A['marked_output_coordinates'])):
        return dict(population=0,reason='target violates actual affine output dependencies')
    a=A['field_degree'];p=A['left_matrix_rows'];d=A['inner_dimension'];r=A['right_matrix_columns']
    actions=[unpack(z,M) for z in A['nucleus_output_operators']]
    k,remainder=divmod(len(independent_basis(apply_binary(z,y) for z in actions)),a*p)
    if remainder:raise AssertionError('nonintegral target rank')
    images=[apply_binary(rectangular_unpack(z,U,M),y) for z in C['dual_reverse_matrices']]
    kernel=linear_kernel(images,U);c=C['codimension'];h=c-len(kernel)
    phase=sum(((lam&affine_hom_offset).bit_count()%2)<<j
        for j,lam in enumerate(C['right_annihilator_basis']))
    sum_all=(1<<c) if phase==0 else 0
    sum_kernel=(1<<len(kernel)) if all((phase&v).bit_count()%2==0 for v in kernel) else 0
    profiles=[(0,0,1),(1,0,sum_kernel-1),(1,1,sum_all-sum_kernel)]
    total=0;used=[]
    for t,rho,coefficient in profiles:
        if not coefficient:continue
        value=signed_universal_product(p,d,r,a,k,t,rho)
        total+=coefficient*value
        used.append(dict(dual_rank=t,composition_rank=rho,
            signed_character_multiplicity=coefficient,weighted_full_fiber=value))
    population,remainder=divmod(total,1<<c)
    if remainder or not 0<=population<=1<<A['input_bits']:raise AssertionError('invalid rank-one slice count')
    return dict(population=population,target_rank=k,codimension=c,
        target_evaluation_rank=h,profiles=used,profile_evaluations=len(used),
        characters_evaluated=0,original_assignments_enumerated=0,
        signed_character_sum=total,seconds=time.perf_counter()-begun)

def count_rank_one_dual_native(program):
    begun=time.perf_counter();n=program.get('inputs',program.get('n'))
    if type(n) is not int or n<1 or n>len(program.get('gates',[]))+1:
        raise ValueError('zero-common-radical family requires explicit input ancestry')
    n,gates,output=validate_trace_program(program,n)
    R=acquire_reversible_terminal_and(program)
    original=acquire_source_free_bilinear_split(R['initial_quadratics'],n)
    accepted=[];declines=[]
    for S in sorted((original,transpose_split(original)),key=lambda z:z['left_dimension']):
        try:C=acquire_hom_slice(S);K=acquire_rank_one_dual(C)
        except ValueError as error:declines.append(str(error));continue
        accepted.append((K,S));break
    if not accepted:raise ValueError('neither acquired orientation has rank-one dual: '+'; '.join(declines))
    K,S=min(accepted,key=lambda z:z[0]['checked_basis_and_pair_ranks'])
    target=invert_terminal(R);F=rank_one_slice_target(K,target);ones=F['population']
    return dict(original_input_bits=n,ordinary_gates=len(gates),ones=ones,
        zeros=(1<<n)-ones,gap=(1<<n)-2*ones,target=target,fiber=F,
        rank_one_certificate=K,split_certificate=S,reversible_certificate=R,
        orientation_declines=declines,auxiliary_independent_inputs=0,
        seconds=time.perf_counter()-begun)

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('source',type=Path)
    parser.add_argument('--output',type=Path);args=parser.parse_args()
    result=count_rank_one_dual_native(json.loads(args.source.read_text()))
    text=json.dumps(result,indent=2)+'\n'
    if args.output:args.output.write_text(text)
    else:print(text,end='')

if __name__=='__main__':main()
