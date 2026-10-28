#!/usr/bin/env python3
"""Manufacture complete target-submodule levels and compress their rank sum.

This consumes the *actual* semisimple dual certificate.  No field coordinates,
list of subspaces, or target decomposition is supplied to the native caller.
Completeness and equal local activity polynomials are checked before using
submodule-lattice Mobius inversion.  Nonadditive targets are allowed.
"""
from pathlib import Path
import sys,time
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from semisimple_dual_counter import *


def canonical_binary_span(vectors):
    """Canonical reduced row basis, including the empty subspace."""
    pivots={}
    for value in vectors:
        for p in sorted(pivots,reverse=True):
            if value>>p&1:value^=pivots[p]
        if not value:continue
        p=value.bit_length()-1
        for j,row in list(pivots.items()):
            if row>>p&1:pivots[j]=row^value
        pivots[p]=value
    return tuple(pivots[p] for p in sorted(pivots,reverse=True))


def polynomial_product(left,right):
    result=[0]*(len(left)+len(right)-1)
    for i,x in enumerate(left):
        if x:
            for j,y in enumerate(right):
                if y:result[i+j]+=x*y
    while len(result)>1 and not result[-1]:result.pop()
    return result


def polynomial_power(base,exponent):
    result=[1]
    while exponent:
        if exponent&1:result=polynomial_product(result,base)
        exponent>>=1
        if exponent:base=polynomial_product(base,base)
    return result


def complete_level_histogram(components,field_degree,simple_dimension):
    """Certified S-submodule rows -> exact signed (dual rank,target rank) counts.

    `components` contains row_basis, rank, and nonzero_character_weight.  The
    production constructor below obtains these rows from actual orbit maps.
    This lower-level function assumes that module origin, not arbitrary binary
    spaces with merely divisible dimensions.
    """
    begun=time.perf_counter();groups={};d=0
    for index,item in enumerate(components):
        rows=canonical_binary_span(item['row_basis'])
        g,rem=divmod(len(rows),simple_dimension)
        if rem:raise ValueError('nonintegral natural target-submodule rank')
        h=item['rank'];weight=item['nonzero_character_weight']
        if type(h) is not int or h<=0:raise ValueError('nonpositive dual component rank')
        d+=h
        group=groups.setdefault(rows,dict(natural_dimension=g,activity=[1],components=[]))
        group['activity']=polynomial_product(group['activity'],[1]+[0]*(h-1)+[weight])
        group['components'].append(index)
    total=canonical_binary_span(v for rows in groups for v in rows)
    k,rem=divmod(len(total),simple_dimension)
    if rem:raise AssertionError('nonintegral total target-submodule rank')
    levels={}
    for rows,item in groups.items():
        g=item['natural_dimension']
        if g not in levels:levels[g]=dict(activity=item['activity'],groups=[])
        if levels[g]['activity']!=item['activity']:
            raise ValueError('target subspaces at one dimension have unequal activity polynomials')
        levels[g]['groups'].append(rows)
    for g,item in levels.items():
        required=gaussian_binomial(k,g,field_degree)
        if len(item['groups'])!=required:
            raise ValueError(f'target level {g} is incomplete: {len(item["groups"])} of {required} submodules')
    # A_j(x) is the signed support polynomial contained in any fixed j-space.
    contained=[]
    for j in range(k+1):
        value=[1]
        for g,item in levels.items():
            if g<=j:
                power=gaussian_binomial(j,g,field_degree)
                value=polynomial_product(value,polynomial_power(item['activity'],power))
        if len(value)>d+1:raise AssertionError('contained polynomial exceeds actual dual rank')
        contained.append(value)
    histogram={};spanning=[]
    for rho in range(k+1):
        exact=[0]*(d+1)
        for j in range(rho+1):
            delta=rho-j
            coefficient=gaussian_binomial(rho,j,field_degree)*((-1)**delta)*(
                1<<(field_degree*delta*(delta-1)//2))
            for t,value in enumerate(contained[j]):exact[t]+=coefficient*value
        multiplicity=gaussian_binomial(k,rho,field_degree)
        for t,value in enumerate(exact):
            if value:histogram[t,rho]=multiplicity*value
        spanning.append(exact)
    expected=1
    for item in components:expected*=1+item['nonzero_character_weight']
    if sum(histogram.values())!=expected:raise AssertionError('signed character mass lost')
    return histogram,dict(target_rank=k,dual_maximum_rank=d,
        complete_levels=[dict(natural_dimension=g,distinct_subspaces=len(item['groups']),
            activity_polynomial=item['activity']) for g,item in sorted(levels.items())],
        actual_target_subspaces=[dict(row_basis=list(rows),**item) for rows,item in groups.items()],
        total_orbit_row_basis=list(total),histogram_states=len(histogram),
        characters_enumerated=0,subspaces_enumerated_beyond_actual_components=0,
        field_coordinates_constructed=False,seconds=time.perf_counter()-begun)


def complete_geometry_target(certificate,compression,target,affine_hom_offset=0):
    C=certificate['nucleus'];U=C['left_dimension'];M=C['output_dimension'];m=C['marked_quadratics']
    if type(target) is not int or target<0 or target.bit_length()>m:raise ValueError('invalid target')
    if type(affine_hom_offset) is not int or affine_hom_offset<0 or affine_hom_offset.bit_length()>len(certificate['hom_basis']):
        raise ValueError('invalid acquired Hom offset')
    rhs=target^C['output_constant']
    y=sum(((rhs>>i)&1)<<j for j,i in enumerate(C['output_basis_mark_indices']))
    if any((row&y).bit_count()%2!=((rhs>>i)&1) for i,row in enumerate(C['marked_output_coordinates'])):
        return dict(population=0,reason='target violates actual affine output dependencies')
    a=C['field_degree'];p=C['left_matrix_rows'];d=C['inner_dimension'];r=C['right_matrix_columns'];ap=a*p
    actions=[unpack(x,U) for x in C['nucleus_input_operators']]
    components=[]
    for item in compression['components']:
        z=apply_binary(rectangular_unpack(item['selected_map'],U,M),y)
        images=[apply_binary(A,z) for A in actions]
        rows=canonical_binary_span(sum(((value>>j)&1)<<i for i,value in enumerate(images)) for j in range(U))
        phase_nontrivial=any((apply_binary(certificate['right_annihilator_basis'],word)&affine_hom_offset).bit_count()%2
            for word in item['dual_coordinate_basis'])
        weight=-1 if phase_nontrivial else (1<<item['field_degree'])-1
        components.append(dict(row_basis=rows,rank=item['rank'],nonzero_character_weight=weight))
    histogram,geometry=complete_level_histogram(components,a,ap)
    k=geometry['target_rank']
    z=apply_binary(rectangular_unpack(compression['manufactured_isomorphism'],U,M),y)
    if len(independent_basis(apply_binary(A,z) for A in actions))!=ap*k:
        raise AssertionError('orbit row spaces lost the actual target rank')
    if geometry['dual_maximum_rank']!=d:raise AssertionError('dual components lost module rank')
    total=sum(weight*signed_universal_product(p,d,r,a,k,t,rho) for (t,rho),weight in histogram.items())
    answer,rem=divmod(total,1<<compression['codimension'])
    if rem or not 0<=answer<=1<<C['input_bits']:raise AssertionError('invalid exact reconstructed population')
    return dict(population=answer,matrix_target_rank=k,codimension=compression['codimension'],
        geometry_certificate=geometry,
        rank_pair_histogram={f'{t},{rho}':value for (t,rho),value in sorted(histogram.items())},
        histogram_states=len(histogram),characters_enumerated=0,
        target_component_rank_additivity_required=False,original_assignments_enumerated=0)
