#!/usr/bin/env python3
"""Acquired phase-kernel flags for affine products of matrix dual factors.

Nonzero target carriers coincide. Actual phase-kernel image carriers must be
nested; their number and dimensions are unbounded. A subspace-flag transfer
and a triangular containment transform replace character enumeration.
"""
from pathlib import Path
import sys,time
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
from matrix_target_geometry import *


def signed_rectangular_rank_polynomial(source,target,phase_rank,multiplicity,a):
    """Rank Fourier polynomial for all target-by-source matrices."""
    if not 0<=phase_rank<=min(source,target):raise ValueError('invalid rectangular phase rank')
    exact=[]
    for v in range(target+1):
        value=gaussian_binomial(target-phase_rank,v,a)*(1<<(a*source*v))
        value-=sum(exact[u]*gaussian_binomial(target-u,v-u,a) for u in range(v))
        if v>source and value:raise AssertionError('impossible rectangular rank')
        exact.append(value)
    out=[0]*(multiplicity*min(source,target)+1)
    for j in range(min(source,target)+1):out[multiplicity*j]=exact[j]
    if sum(out)!=(1<<(a*source*target) if phase_rank==0 else 0):raise AssertionError('rectangular character mass')
    return out


def _add_scaled(destination,source,scale):
    if len(destination)<len(source):destination.extend([0]*(len(source)-len(destination)))
    for j,x in enumerate(source):destination[j]+=scale*x


def affine_flag_histogram(components,a,ap):
    """Certified target/phase module rows and matrix-factor ranks -> counts."""
    begun=time.perf_counter();carriers=[];zeros=[];d=c=0
    for item in components:
        E=canonical_binary_span(item['target_rows']);F=canonical_binary_span(item['phase_kernel_rows'])
        g,rem=divmod(len(E),ap);f,rem2=divmod(len(F),ap)
        s=item['matrix_degree'];h=item['natural_multiplicity'];t=item['phase_rank']
        if rem or rem2 or not 0<=g<=s or not 0<=t<=s or not max(0,g-t)<=f<=min(g,s-t):raise ValueError('invalid actual target/phase module ranks')
        EC=BinaryCoordinates(E)
        for row in F:
            try:EC.coordinates(row)
            except ValueError as error:raise ValueError('phase carrier lies outside target carrier') from error
        record=dict(target_rows=E,phase_kernel_rows=F,target_rank=g,phase_image_rank=f,
            matrix_degree=s,natural_multiplicity=h,phase_rank=t)
        (carriers if g else zeros).append(record);d+=h*s;c+=a*s*s
    k=carriers[0]['target_rank'] if carriers else 0;ambient=carriers[0]['target_rows'] if carriers else ()
    if any(x['target_rows']!=ambient for x in carriers):raise ValueError('nonzero target carriers do not coincide')
    groups={():[]};groups.setdefault(ambient,[])
    for item in carriers:groups.setdefault(item['phase_kernel_rows'],[]).append(item)
    chain=sorted(groups,key=lambda rows:(len(rows),rows));last=()
    for rows in chain:
        RC=BinaryCoordinates(rows)
        for v in last:
            try:RC.coordinates(v)
            except ValueError as error:raise ValueError('acquired phase-kernel carriers are not nested') from error
        last=rows
    zero_polynomial=[1]
    for item in zeros:
        zero_polynomial=polynomial_product(zero_polynomial,signed_rectangular_rank_polynomial(
            item['matrix_degree'],item['matrix_degree'],item['phase_rank'],item['natural_multiplicity'],a))
    contained=[];transfer_states=0
    for j in range(k+1):
        states={0:zero_polynomial[:]};previous_dimension=0
        for rows in chain:
            f=len(rows)//ap;gap=f-previous_dimension;updated={}
            for previous,poly in states.items():
                for eta in range(previous,min(j,f)+1):
                    delta=eta-previous
                    if delta>gap or j-eta>k-f:continue
                    factor=gaussian_binomial(gap,delta,a)*(1<<(a*(previous_dimension-previous)*delta))
                    value=poly
                    for item in groups[rows]:
                        s=item['matrix_degree'];r=s-k+j;tau=item['phase_rank']-k+j+f-eta
                        local=signed_rectangular_rank_polynomial(s,r,tau,item['natural_multiplicity'],a)
                        value=polynomial_product(value,local)
                    if len(value)>d+1:raise AssertionError('flag polynomial exceeds actual dual rank')
                    _add_scaled(updated.setdefault(eta,[]),value,factor)
            states=updated;previous_dimension=f;transfer_states+=len(states)
        if set(states)!={j}:raise AssertionError('final ambient flag did not force dimension j')
        contained.append(states[j])
    # M_j = sum_D chi(D) [k-rho(D) choose j-rho(D)] x^rank(D).
    exact=[];histogram={}
    for rho in range(k+1):
        value=contained[rho]+[0]*(d+1-len(contained[rho]))
        for u in range(rho):_add_scaled(value,exact[u],-gaussian_binomial(k-u,rho-u,a))
        exact.append(value)
        for t,x in enumerate(value):
            if x:histogram[t,rho]=x
    if histogram.get((0,0))!=1:raise AssertionError('zero matrix lost')
    if sum(histogram.values())!=(1<<c if all(x['phase_rank']==0 for x in components) else 0):raise AssertionError('flag transform lost signed mass')
    return histogram,dict(target_rank=k,dual_maximum_rank=d,codimension=c,
        phase_flag_dimensions=[len(rows)//ap for rows in chain],phase_flag_row_bases=[list(rows) for rows in chain],
        target_row_basis=list(ambient),zero_target_components=len(zeros),
        transfer_dimension_states=transfer_states,histogram_states=len(histogram),
        characters_enumerated=0,subspaces_enumerated=0,seconds=time.perf_counter()-begun)


def acquire_matrix_phase_carriers(certificate,compression,target,affine_hom_offset=0):
    """Manufacture actual target and phase-kernel modules for any consumer."""
    C=certificate['nucleus'];U=C['left_dimension'];M=C['output_dimension'];m=C['marked_quadratics']
    if type(target) is not int or target<0 or target.bit_length()>m:raise ValueError('invalid target')
    if type(affine_hom_offset) is not int or affine_hom_offset<0 or affine_hom_offset.bit_length()>len(certificate['hom_basis']):raise ValueError('invalid Hom offset')
    rhs=target^C['output_constant'];y=sum(((rhs>>i)&1)<<j for j,i in enumerate(C['output_basis_mark_indices']))
    if any((row&y).bit_count()%2!=((rhs>>i)&1) for i,row in enumerate(C['marked_output_coordinates'])):return dict(population=0,reason='target violates affine output dependencies')
    a=C['field_degree'];p=C['left_matrix_rows'];d=C['inner_dimension'];ap=a*p
    actions=[unpack(A,U) for A in C['nucleus_input_operators']];components=[];proofs=[]
    def orbit_rows(vectors):
        rows=[];joint=[]
        for v in vectors:
            images=[apply_binary(A,v) for A in actions];joint.extend(images)
            rows.extend(sum(((z>>j)&1)<<i for i,z in enumerate(images)) for j in range(U))
        return canonical_binary_span(rows),len(independent_basis(joint))
    for item in compression['components']:
        s=item['matrix_degree'];basis=item['component_basis'];BC=BinaryCoordinates(basis)
        matrices=[rectangular_unpack(D,U,M) for D in basis];vectors=[apply_binary(D,y) for D in matrices]
        E,joint=orbit_rows(vectors)
        if joint not in (0,ap*s):raise ValueError('target component occupies multiple joint simple copies')
        phase=sum(((apply_binary(certificate['right_annihilator_basis'],word)&affine_hom_offset).bit_count()%2)<<j
            for j,word in enumerate(item['dual_coordinate_basis']))
        translates=[]
        for A in item['factor_basis']:
            AA=unpack(A,U)
            translates.append(sum(((BC.coordinates(pack(product(AA,D),U))&phase).bit_count()%2)<<j for j,D in enumerate(matrices)))
        t,rem=divmod(len(independent_basis(translates)),a*s)
        if rem:raise AssertionError('phase orbit has nonintegral rank')
        kernel=affine_solutions([(row,0) for row in translates],len(basis))[1]
        if len(kernel)!=a*s*(s-t):raise AssertionError('phase annihilator dimension mismatch')
        F,_=orbit_rows([apply_binary(vectors,v) for v in kernel])
        components.append(dict(target_rows=E,phase_kernel_rows=F,matrix_degree=s,
            natural_multiplicity=item['natural_multiplicity'],phase_rank=t))
        proofs.append(dict(target_joint_dimension=joint,matrix_degree=s,target_row_rank=len(E),
            phase_rank=t,phase_kernel_row_rank=len(F),phase_annihilator_dimension=len(kernel)))
    output_actions=[unpack(A,M) for A in C['nucleus_output_operators']]
    target_rank,rem=divmod(len(independent_basis(apply_binary(A,y) for A in output_actions)),ap)
    if rem:raise AssertionError('nonintegral original target rank')
    return dict(components=components,phase_carrier_acquisition=proofs,
        target_output_coordinates=y,target_rank=target_rank,field_degree=a,
        natural_module_dimension=ap,inner_dimension=d)


def affine_matrix_flag_target(certificate,compression,target,affine_hom_offset=0):
    acquired=acquire_matrix_phase_carriers(certificate,compression,target,affine_hom_offset)
    if 'population' in acquired:return acquired
    C=certificate['nucleus'];a=C['field_degree'];p=C['left_matrix_rows'];d=C['inner_dimension'];ap=a*p
    histogram,flag=affine_flag_histogram(acquired['components'],a,ap);k=flag['target_rank']
    if acquired['target_rank']!=k:raise AssertionError('flag lost original target rank')
    if flag['dual_maximum_rank']!=d or flag['codimension']!=compression['codimension']:raise AssertionError('flag changed acquired dimensions')
    total=sum(weight*signed_universal_product(p,d,d,a,k,t,rho) for (t,rho),weight in histogram.items())
    answer,rem=divmod(total,1<<compression['codimension'])
    if rem or not 0<=answer<=1<<C['input_bits']:raise AssertionError('invalid original-input affine count')
    return dict(population=answer,matrix_target_rank=k,codimension=compression['codimension'],
        phase_carrier_acquisition=acquired['phase_carrier_acquisition'],flag_certificate=flag,
        rank_pair_histogram={f'{t},{rho}':v for (t,rho),v in sorted(histogram.items())},
        histogram_states=len(histogram),characters_enumerated=0,original_assignments_enumerated=0)
