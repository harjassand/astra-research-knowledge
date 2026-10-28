#!/usr/bin/env python3
"""Acquire products of matrix algebras and their interacting target geometry.

No isomorphism, matrix units, target subspaces or multiplier factors are given.
The homogeneous rank distribution is reconstructed by Grassmann intersection
numbers and submodule-lattice Mobius inversion after actual level checks.
"""
from pathlib import Path
import sys,time
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from complete_target_geometry import *
from finite_simple_binary_algebra import certify_finite_simple_matrix_algebra


def acquire_semisimple_matrix_dual(certificate):
    begun=time.perf_counter();C=certificate['nucleus'];U=C['left_dimension'];M=C['output_dimension']
    if U!=M:raise ValueError('regular matrix-dual modules require equal dimensions')
    a=C['field_degree'];p=C['left_matrix_rows'];ap=a*p
    dual=certificate['dual_reverse_matrices'];c=len(dual)
    if not c:raise ValueError('zero dual needs no algebra compression')
    DS=BinaryCoordinates(dual);Dmat=[rectangular_unpack(x,U,M) for x in dual]
    L=certificate['endomorphism_basis'][:];dimensions=[len(L)]
    for D in Dmat:
        images=[remainder(DS,pack(product(unpack(X,U),D),U)) for X in L]
        L=[apply_binary(L,v) for v in linear_kernel(images,U*M)];dimensions.append(len(L))
    LC=BinaryCoordinates(L);decoded=[unpack(x,U) for x in L];K=len(L)
    unit=LC.coordinates(pack([1<<j for j in range(U)],U))
    table=[[LC.coordinates(pack(product(A,B),U)) for B in decoded] for A in decoded]
    def mul(x,y):return apply_binary([apply_binary(row,y) for row in table],x)
    center=linear_kernel([sum((table[i][j]^table[j][i])<<(K*j) for j in range(K)) for i in range(K)],K*K)
    Z=BinaryCoordinates(center);squares=[Z.coordinates(mul(z,z)) for z in center]
    if len(independent_basis(squares))!=len(center):raise ValueError('matrix multiplier center has nilpotents')
    fixed=linear_kernel([z^(1<<i) for i,z in enumerate(squares)],len(center));atoms=[unit]
    for coordinate in fixed:
        e=apply_binary(center,coordinate);refined=[]
        for f in atoms:
            left=mul(e,f);right=f^left
            if left:refined.append(left)
            if right:refined.append(right)
        atoms=refined
    if len(atoms)!=len(fixed):raise AssertionError('central atoms did not exhaust reduced center')
    base_center=[apply_binary(C['nucleus_input_operators'],z) for z in C['nucleus_certificate']['center_basis']]
    pieces=[]
    for e in atoms:
        projector=apply_binary(L,e);P=unpack(projector,U)
        image=independent_basis(P);IC=BinaryCoordinates(image);u=len(image)
        factor_words=independent_basis(mul(e,1<<j) for j in range(K));factor=[apply_binary(L,x) for x in factor_words]
        local=[pack([IC.coordinates(apply_binary(unpack(A,U),v)) for v in image],u) for A in factor]
        simple=certify_finite_simple_matrix_algebra(local,u)
        if simple['field_degree']!=a:raise ValueError('matrix factor has incompatible center degree')
        s=simple['matrix_degree'];h,rem=divmod(u,ap*s)
        if rem or not h:raise ValueError('matrix factor has incompatible natural multiplicity')
        field_actual=BinaryCoordinates(apply_binary(local,z) for z in simple['center_basis'])
        for z in base_center:
            restricted=pack([IC.coordinates(apply_binary(unpack(z,U),v)) for v in image],u)
            try:field_actual.coordinates(restricted)
            except ValueError as error:raise ValueError('factor and nucleus scalar fields differ') from error
        component=independent_basis(pack(product(P,D),U) for D in Dmat)
        if len(component)!=a*s*s:raise ValueError('dual component is not a regular matrix-factor module')
        pieces.append(dict(projector=projector,image_basis=image,component_basis=component,
            field_degree=a,matrix_degree=s,natural_multiplicity=h,local_algebra_certificate=simple,
            factor_basis=factor,dual_coordinate_basis=[DS.coordinates(x) for x in component]))
    rows=[sum(((D[j]>>i)&1)<<j for j in range(M)) for D in Dmat for i in range(U)]
    if len(independent_basis(rows))!=M:raise ValueError('actual regular dual has nonzero common kernel')
    if sum(a*x['matrix_degree']**2 for x in pieces)!=c:raise AssertionError('regular factors lost dual dimensions')
    return dict(components=pieces,multiplier_basis=L,multiplier_dimension=K,
        multiplier_dimensions=dimensions,central_factor_count=len(pieces),codimension=c,
        common_kernel_zero_verified=True,actual_scalar_fields_verified=True,
        isomorphism_supplied_constructed_or_searched=False,matrix_units_supplied_or_constructed=False,
        dual_elements_enumerated=0,seconds=time.perf_counter()-begun)


def rectangular_rank_polynomial(source,target,multiplicity,a):
    """Rank polynomial of maps Fq^source -> Fq^target."""
    out=[0]*(multiplicity*min(source,target)+1);onto=1
    for j in range(min(source,target)+1):
        if j:onto*=((1<<(a*source))-(1<<(a*(j-1))))
        out[multiplicity*j]=gaussian_binomial(target,j,a)*onto
    return out


def matrix_geometry_histogram(components,a,ap):
    """Certified target-module rows and local matrix factors -> rank counts."""
    begun=time.perf_counter();groups={};d=c=0
    for index,item in enumerate(components):
        rows=canonical_binary_span(item['row_basis']);g,rem=divmod(len(rows),ap)
        s=item['matrix_degree'];h=item['natural_multiplicity']
        if rem or not 0<=g<=s:raise ValueError('invalid one-copy target-submodule dimension')
        d+=h*s;c+=a*s*s
        group=groups.setdefault(rows,dict(natural_dimension=g,intersection_activities=[[1] for _ in range(g+1)],components=[]))
        for ell in range(g+1):
            local=rectangular_rank_polynomial(s,s-g+ell,h,a)
            group['intersection_activities'][ell]=polynomial_product(group['intersection_activities'][ell],local)
        group['components'].append(index)
    ambient=canonical_binary_span(v for rows in groups for v in rows);k,rem=divmod(len(ambient),ap)
    if rem:raise AssertionError('nonintegral total target rank')
    levels={}
    for rows,item in groups.items():
        g=item['natural_dimension']
        if g not in levels:levels[g]=dict(activities=item['intersection_activities'],groups=[])
        if levels[g]['activities']!=item['intersection_activities']:raise ValueError('unequal intersection activity polynomials')
        levels[g]['groups'].append(rows)
    for g,item in levels.items():
        required=gaussian_binomial(k,g,a)
        if len(item['groups'])!=required:raise ValueError(f'matrix target level {g} is incomplete: {len(item["groups"])} of {required}')
    contained=[]
    for j in range(k+1):
        value=[1]
        for g,item in levels.items():
            total_members=0
            for ell in range(max(0,g+j-k),min(g,j)+1):
                number=gaussian_binomial(j,ell,a)*gaussian_binomial(k-j,g-ell,a)*(1<<(a*(j-ell)*(g-ell)))
                total_members+=number
                value=polynomial_product(value,polynomial_power(item['activities'][ell],number))
            if total_members!=len(item['groups']):raise AssertionError('Grassmann intersection census lost submodules')
        if len(value)>d+1:raise AssertionError('contained polynomial exceeds actual dual rank')
        contained.append(value)
    histogram={}
    for rho in range(k+1):
        exact=[0]*(d+1)
        for j in range(rho+1):
            e=rho-j;weight=gaussian_binomial(rho,j,a)*((-1)**e)*(1<<(a*e*(e-1)//2))
            for t,n in enumerate(contained[j]):exact[t]+=weight*n
        multiplier=gaussian_binomial(k,rho,a)
        for t,n in enumerate(exact):
            if n<0:raise AssertionError('negative homogeneous character population')
            if n:histogram[t,rho]=multiplier*n
    if sum(histogram.values())!=1<<c:raise AssertionError('matrix geometry lost character mass')
    return histogram,dict(target_rank=k,dual_maximum_rank=d,codimension=c,
        complete_levels=[dict(natural_dimension=g,distinct_subspaces=len(item['groups']),intersection_activity_polynomials=item['activities']) for g,item in sorted(levels.items())],
        actual_submodules=[dict(row_basis=list(rows),**item) for rows,item in groups.items()],
        histogram_states=len(histogram),characters_enumerated=0,
        subspaces_enumerated_beyond_actual_components=0,seconds=time.perf_counter()-begun)


def matrix_geometry_target(certificate,compression,target,affine_hom_offset=0):
    C=certificate['nucleus'];U=C['left_dimension'];M=C['output_dimension'];m=C['marked_quadratics']
    if type(target) is not int or target<0 or target.bit_length()>m:raise ValueError('invalid target')
    if type(affine_hom_offset) is not int or affine_hom_offset<0 or affine_hom_offset.bit_length()>len(certificate['hom_basis']):raise ValueError('invalid Hom offset')
    if any((lam&affine_hom_offset).bit_count()%2 for lam in certificate['right_annihilator_basis']):raise ValueError('nontrivial affine phases need a different matrix-geometry consumer')
    rhs=target^C['output_constant'];y=sum(((rhs>>i)&1)<<j for j,i in enumerate(C['output_basis_mark_indices']))
    if any((row&y).bit_count()%2!=((rhs>>i)&1) for i,row in enumerate(C['marked_output_coordinates'])):return dict(population=0,reason='target violates affine output dependencies')
    a=C['field_degree'];p=C['left_matrix_rows'];d=C['inner_dimension'];r=C['right_matrix_columns'];ap=a*p
    actions=[unpack(A,U) for A in C['nucleus_input_operators']];components=[];orbit_checks=[]
    for item in compression['components']:
        vectors=[apply_binary(rectangular_unpack(D,U,M),y) for D in item['component_basis']];joint=[];rows=[]
        for v in vectors:
            images=[apply_binary(A,v) for A in actions];joint.extend(images)
            rows.extend(sum(((z>>j)&1)<<i for i,z in enumerate(images)) for j in range(U))
        joint_dimension=len(independent_basis(joint));s=item['matrix_degree']
        if joint_dimension not in (0,ap*s):raise ValueError('target component occupies multiple joint simple-module copies')
        R=canonical_binary_span(rows)
        components.append(dict(row_basis=R,matrix_degree=s,natural_multiplicity=item['natural_multiplicity']))
        orbit_checks.append(dict(joint_dimension=joint_dimension,allowed_nonzero_dimension=ap*s,orbit_row_rank=len(R),natural_target_rank=len(R)//ap))
    histogram,geometry=matrix_geometry_histogram(components,a,ap);k=geometry['target_rank']
    output_actions=[unpack(A,M) for A in C['nucleus_output_operators']]
    if len(independent_basis(apply_binary(A,y) for A in output_actions))!=ap*k:raise AssertionError('target kernels lost original target rank')
    if geometry['dual_maximum_rank']!=d or geometry['codimension']!=compression['codimension']:raise AssertionError('matrix factors changed acquired dimensions')
    total=sum(count*signed_universal_product(p,d,r,a,k,t,rho) for (t,rho),count in histogram.items())
    answer,rem=divmod(total,1<<compression['codimension'])
    if rem or not 0<=answer<=1<<C['input_bits']:raise AssertionError('invalid reconstructed original-input count')
    return dict(population=answer,matrix_target_rank=k,codimension=compression['codimension'],
        target_component_orbit_checks=orbit_checks,geometry_certificate=geometry,
        rank_pair_histogram={f'{t},{rho}':v for (t,rho),v in sorted(histogram.items())},
        histogram_states=len(histogram),characters_enumerated=0,
        original_assignments_enumerated=0,isomorphism_constructed_or_searched=False)
