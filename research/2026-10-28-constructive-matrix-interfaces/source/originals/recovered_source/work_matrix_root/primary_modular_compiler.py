#!/usr/bin/env python3
"""Acquire a primary matrix source from raw cubic ANF and count modulo M_J.

This manufactures the matrix representation and verifies every source
coefficient. Rejection is explicit; arbitrary Boolean circuits are not
asserted to possess the admitted representation. J is charged separately.
"""
from pathlib import Path
import sys,time,json,argparse
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/p) for p in ('work_matrix_root','work_norm_frontier_agent','work_norm_glue_agent','work_norm_slice_agent')]
from raw_matrix_trace import (hidden_groups,AcquiredMatrixAlgebra,acquire_center,bits,
    identity,inverse,linear_apply,solve)
from invariant_quadratic_matrix import quadratic_anf,polynomial_value
from operator_quadratic_counter import acquire_operator_linear_refinement
from arbitrary_operator_lie_unit import recover_from_raw_arbitrary_source
from arbitrary_operator_hall import transpose_partition
from nonresonant_primary_gaussian import shifted_polynomial
from nonresonant_primary_modular import count_primary_modulo
from resonant_primary_modular import count_resonant_primary_modulo


def count_acquired_primary_modulo(algebra,beta,D,phi=(),eta=0,row_budget=2):
    polynomial,components=algebra.primary_data(D)
    if len(components)!=1:raise ValueError('the acquired operator is not single-primary')
    item=components[0];f=item['irreducible'];shape=transpose_partition(item['jordan_columns'])
    resonant=shifted_polynomial(f,beta,algebra.F)==list(f)
    api=count_resonant_primary_modulo if resonant else count_primary_modulo
    result=api(shape,algebra.h,f,beta,phi,eta,row_budget)
    result.update(supplied_primary_decomposition=False,acquired_characteristic_polynomial=polynomial,
        acquired_irreducible=f,acquired_primary_columns=item['jordan_columns'],resonant=resonant)
    return result


def compile_raw_primary_modulo(poly,n,row_budget=2):
    begun=time.perf_counter();poly=set(poly)
    if type(n) is not int or n<=0 or any(type(m) is not int or m<0 or m.bit_length()>n or m.bit_count()>3 for m in poly):
        raise ValueError('an explicit raw cubic Boolean ANF is required')
    grouped,slices,group_map,stats=hidden_groups(poly,n)
    algebra=AcquiredMatrixAlgebra(slices);d=algebra.d
    centered,offset=acquire_center(grouped,slices,d,allow_within=True)
    lower=[m for m in centered if 0<m.bit_count()<=2]
    groups={i//d for m in lower for i in bits(m)}
    if len(groups)!=1:raise ValueError('one acquired group must contain every nonconstant source term')
    group=next(iter(groups));local={m>>(group*d) for m in lower}
    if 0 in centered:local.add(0)
    back=inverse([identity(d),algebra.Y,algebra.Z][group])
    source=quadratic_anf(lambda x:polynomial_value(local,linear_apply(back,x)),d)
    try:
        beta,D,phi,eta,evidence=acquire_operator_linear_refinement(source,algebra)
    except ValueError:
        if algebra.t<4:
            raise ValueError('the general intrinsic source-unit fallback in this frontend requires t>=4')
        unit,unit_evidence=recover_from_raw_arbitrary_source(source,algebra)
        inverse_unit=solve(algebra.left_matrix(unit),algebra.one)
        beta,D,phi,eta,evidence=acquire_operator_linear_refinement(source,algebra,inverse_unit)
        evidence.update(intrinsic_unit_acquisition=unit_evidence,
            unit_acquisition_route='manufactured all-operator unit followed by exact full source fit')
    if not beta:raise ValueError('nonzero exterior-square coefficient is required')
    acquired_seconds=time.perf_counter()-begun
    result=count_acquired_primary_modulo(algebra,beta,D,phi,eta,row_budget)
    if result['original_bits']!=n:raise AssertionError('original independent-input count changed')
    M=result['modulus'];result['zeros_residue']=(pow(2,n,M)+result['gap_residue'])*pow(2,-1,M)%M
    stats.update(algebra.stats);stats.update(evidence)
    result['stats'].update(raw_acquisition=stats,raw_monomials=len(poly),affine_offset=offset,
        quadratic_group=group,acquired_beta=beta,acquired_eta=eta,acquired_trace_anf=sorted(phi),
        original_domain_preserved=True,full_source_coefficient_identity_verified=True,
        supplied_unit_or_operator_decomposition=False,acquisition_seconds=acquired_seconds,
        total_seconds=time.perf_counter()-begun)
    result['raw_cubic_input']=True
    return result


def compile_primary_modular_program(program,row_budget=2):
    """Exact original-input frontend, with degree <=3 at every gate."""
    from matrix_circuit_counter import compile_gate_anf
    poly,program_stats=compile_gate_anf(program)
    result=compile_raw_primary_modulo(poly,program['inputs'],row_budget)
    result['program']=program_stats
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source',type=Path);parser.add_argument('--row-budget',type=int,default=2)
    parser.add_argument('--output',type=Path);args=parser.parse_args()
    source=json.loads(args.source.read_text())
    result=(compile_primary_modular_program(source,args.row_budget) if 'gates' in source
        else compile_raw_primary_modulo(source['anf'],source['n'],args.row_budget))
    text=json.dumps(result,indent=2)+'\n'
    if args.output:args.output.write_text(text)
    else:print(text,end='')

if __name__=='__main__':main()
