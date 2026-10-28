#!/usr/bin/env python3
"""Checked intrinsic interface to uniform single-primary Pfaffian counting.

The input algebra is manufactured from the third polarization. No matrix
units, source operator decomposition or extension field are supplied here.
The raw entry point additionally manufactures and verifies the source unit.
Admission is exact; raw unit acquisition is complete only for its separately
proved routes, while the backend is complete for both primary classes.
"""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'work_matrix_root'))
sys.path.insert(0,str(ROOT/'work_norm_frontier_agent'))
from cyclic_primary_pfaffian import cyclic_primary_gap


def count_acquired_primary_source(algebra,beta,D,phi,eta=0):
    """Certify a cyclic or semisimple single primary, then count exactly."""
    if type(D) is not int or D<0 or D.bit_length()>algebra.d:
        raise ValueError('operator is outside the acquired algebra')
    polynomial,primary=algebra.primary_data(D)
    if len(primary)!=1:
        raise ValueError('uniform primary backend requires one irreducible factor')
    block=primary[0];f=block['irreducible'];e=block['multiplicity']
    columns=block['jordan_columns'];d=len(f)-1
    if d*e!=algebra.t:raise AssertionError('primary dimension does not match acquired matrix size')
    if columns==[1]*e:semisimple=False
    elif columns==[e]:semisimple=True
    else:
        raise ValueError('primary is neither cyclic nor semisimple')
    if d==2 and not semisimple:
        from cyclic_quadratic_primary_counter import cyclic_quadratic_primary_gap
        gap,metadata=cyclic_quadratic_primary_gap(e,algebra.h,f,beta,phi,eta)
        route='four-height transfer for an acquired cyclic quadratic primary'
    else:
        gap,metadata=cyclic_primary_gap(e,algebra.h,f,beta,phi,eta,semisimple)
        route='uniform finite Pfaffian for an acquired single primary'
    metadata.update(route=route,
        acquired_primary_data=primary,source_reduced_charpoly=polynomial,
        matrix_size=algebra.t,field_degree=algebra.a,
        supplied_matrix_units=False,supplied_primary_decomposition=False,
        uniform_polynomial_time=True,enumerated_profiles=0,
        enumerated_subspaces=0,enumerated_field_elements=0,
        enumerated_original_assignments=0)
    return gap,metadata


def compile_raw_primary_quadratic(poly,n):
    """Checked raw affine-hidden cubic entry point; no source data supplied.

Manufacture the matrix algebra and one-group source. Try the existing
central-commutator/odd-radical unit proof, the center-field rank-two pencil,
then the proved Lie unit lift. Every successful route checks all source
coefficients and the admitted primary type before returning a count.
Failure to manufacture a unit is a checked rejection, not a false count.
"""
    from raw_matrix_trace import (hidden_groups,AcquiredMatrixAlgebra,
        acquire_center,bits,inverse,identity,linear_apply,solve)
    from invariant_quadratic_matrix import quadratic_anf,polynomial_value
    from operator_quadratic_counter import acquire_operator_linear_refinement
    from regular_chain_pencil_field import fit_center_rank_two_source
    begun=time.perf_counter();poly=set(poly)
    if type(n) is not int or n<=0 or any(type(m) is not int or m<0 or
            m.bit_length()>n or m.bit_count()>3 for m in poly):
        raise ValueError('raw cubic Boolean ANF required')
    grouped,slices,group_map,stats=hidden_groups(poly,n)
    algebra=AcquiredMatrixAlgebra(slices);dimension=algebra.d
    centered,offset=acquire_center(grouped,slices,dimension,allow_within=True)
    lower=[m for m in centered if 0<m.bit_count()<=2]
    groups={i//dimension for monomial in lower for i in bits(monomial)}
    if len(groups)!=1:raise ValueError('one acquired group must contain the nonconstant source')
    group=next(iter(groups));local={m>>(group*dimension) for m in lower}
    if 0 in centered:local.add(0)
    back=inverse([identity(dimension),algebra.Y,algebra.Z][group])
    source=quadratic_anf(lambda x:polynomial_value(local,linear_apply(back,x)),dimension)
    try:
        beta,D,phi,eta,evidence=acquire_operator_linear_refinement(source,algebra)
        gap,backend=count_acquired_primary_source(algebra,beta,D,phi,eta)
    except ValueError:
        try:
            gap,backend,evidence=fit_center_rank_two_source(source,algebra,accept_primary=True)
        except ValueError:
            from matrix2_pfaffian_unit import count_matrix2_pfaffian_source
            try:gap,backend,evidence=count_matrix2_pfaffian_source(source,algebra)
            except ValueError:
                from primary_operator_quadratic import count_unmarked_primary_lie_source
                gap,backend,evidence=count_unmarked_primary_lie_source(source,algebra)
    if abs(gap)>1<<n or gap%2:raise AssertionError('invalid original-domain count')
    stats.update(algebra.stats);stats.update(evidence)
    stats.update(backend=backend,raw_monomials=len(poly),affine_offset=offset,
        quadratic_group=group,supplied_unit_or_operator_decomposition=False,
        seconds=time.perf_counter()-begun)
    return dict(original_bits=n,zeros=((1<<n)+gap)//2,ones=((1<<n)-gap)//2,gap=gap,stats=stats)
