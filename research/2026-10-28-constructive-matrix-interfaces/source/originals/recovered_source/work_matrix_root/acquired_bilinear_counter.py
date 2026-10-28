#!/usr/bin/env python3
"""Polynomial-only portfolio for certified ordinary Boolean bilinear families.

Receives an ordinary DAG, manufactures affine input/output data, and tries full
evaluation, rank-one dual compression, semisimple dual compression, then a
description-length-bounded character sum. Declines circuits without a proved
certificate. This is not an unrestricted polynomial Boolean model counter.
"""
from pathlib import Path
import argparse,json,sys,time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/p) for p in ('work_matrix_root','work_trace_frontier',
    'work_multiprimary_audit','work_partition_free_agent','work_phase_diamond')]
from unsaturated_bilinear_counter import *
from affine_unsaturated_bilinear_counter import acquire_affine_hom_slice,transpose_affine_split
from rank_one_dual_counter import acquire_rank_one_dual,rank_one_slice_target
from semisimple_dual_counter import acquire_semisimple_dual,compressed_semisimple_target
from complete_target_geometry import complete_geometry_target
from noncommutative_dual_counter import acquire_noncommutative_dual
from noncommutative_phase_moments import compressed_noncommutative_affine_target
from matrix_target_geometry import acquire_semisimple_matrix_dual,matrix_geometry_target
from matrix_affine_flag_counter import affine_matrix_flag_target
from phase_diamond import affine_matrix_diamond_target


def count_acquired_bilinear(program):
    begun=time.perf_counter();n=program.get('inputs',program.get('n'))
    if type(n) is not int or n<1 or n>len(program.get('gates',[]))+1:
        raise ValueError('zero-common-radical family requires explicit input ancestry')
    n,gates,output=validate_trace_program(program,n)
    length=len(json.dumps(program,separators=(',',':')).encode())
    R=acquire_reversible_terminal_and(program);target=invert_terminal(R)
    split=acquire_source_free_bilinear_split(R['initial_quadratics'],n,
        require_shared_center=False,allow_paired_components=True)
    declines=[];candidates=[];answer=None
    orientations=sorted((split,transpose_affine_split(split)),key=lambda s:s['left_dimension'])
    for oriented in orientations:
        try:C=acquire_affine_hom_slice(oriented)
        except ValueError as error:declines.append(str(error));continue
        candidates.append((C,oriented));phase=C['affine_hom_offset'];compression=None
        if C['codimension']==0:
            F=bilinear_product_target_fiber(C['nucleus'],target);method='full universal evaluation'
            answer=(F,C,oriented,compression,method);break
        try:
            compression=acquire_rank_one_dual(C)
            F=rank_one_slice_target(compression,target,phase);method='rank-one dual compression'
            answer=(F,C,oriented,compression,method);break
        except ValueError as error:declines.append(str(error))
        try:
            compression=acquire_semisimple_dual(C)
            try:
                F=compressed_semisimple_target(C,compression,target,phase);method='semisimple dual compression'
            except ValueError as error:
                declines.append(str(error))
                F=complete_geometry_target(C,compression,target,phase);method='complete target geometry'
            answer=(F,C,oriented,compression,method);break
        except ValueError as error:declines.append(str(error))
        try:
            compression=acquire_noncommutative_dual(C)
            F=compressed_noncommutative_affine_target(C,compression,target,phase)
            method='noncommutative affine character moments'
            answer=(F,C,oriented,compression,method);break
        except ValueError as error:declines.append(str(error))
        try:
            compression=acquire_semisimple_matrix_dual(C)
            try:
                F=matrix_geometry_target(C,compression,target,phase)
                method='matrix factors and target geometry'
            except ValueError as error:
                declines.append(str(error))
                try:
                    F=affine_matrix_flag_target(C,compression,target,phase)
                    method='matrix factors and acquired affine phase flag'
                except ValueError as error:
                    declines.append(str(error))
                    F=affine_matrix_diamond_target(C,compression,target,phase)
                    method='matrix factors and acquired crossing affine phases'
            answer=(F,C,oriented,compression,method);break
        except ValueError as error:declines.append(str(error))
    if answer is None:
        for C,oriented in sorted(candidates,key=lambda pair:pair[0]['codimension']):
            # The bound is fixed by the actual description, not a user promise.
            if C['codimension']<length.bit_length():
                F=slice_target_fiber(C,target,C['affine_hom_offset'])
                answer=(F,C,oriented,None,'description-bounded exact character sum');break
    if answer is None:
        raise ValueError('not admitted by the polynomial counting portfolio: '+'; '.join(declines))
    F,C,oriented,compression,method=answer;ones=F['population']
    return dict(original_input_bits=n,ordinary_gates=len(gates),description_bytes=length,
        ones=ones,zeros=(1<<n)-ones,gap=(1<<n)-2*ones,target=target,method=method,
        fiber=F,affine_slice_certificate=C,compression_certificate=compression,
        split_certificate=oriented,reversible_certificate=R,other_branch_declines=declines,
        auxiliary_independent_inputs=0,original_assignments_enumerated=0,
        unrestricted_polynomial_counting_claim=False,seconds=time.perf_counter()-begun)


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('source',type=Path)
    parser.add_argument('--output',type=Path);args=parser.parse_args()
    result=count_acquired_bilinear(json.loads(args.source.read_text()));text=json.dumps(result,indent=2)+'\n'
    if args.output:args.output.write_text(text)
    else:print(text,end='')


if __name__=='__main__':main()
