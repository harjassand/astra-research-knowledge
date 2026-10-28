#!/usr/bin/env python3
"""Acquire hidden quadratic blocks from commuting source-relative projectors.

The polar operators B0^-1 Bi manufacture orthogonal joint eigenspaces.
Local rank-one information then reduces a target fiber to a weighted
binary coset. Its acquired nullity is charged, never presumed small.
"""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'work_trace_frontier'),str(ROOT/'work_norm_slice_agent'),
    str(ROOT/'work_matrix_root'),str(ROOT/'work_norm_glue_agent')]
from reversible_quadratic_fibers import (polar_rows,independent_basis,acquire_reversible_terminal_and,
    invert_terminal,affine_solutions,apply_binary,compose_quadratic,quadratic_gap,
    positions,anf_value,prepared_program,validate_trace_program)


def linear_kernel(columns,output_bits):
    rows=[sum(((column>>i)&1)<<j for j,column in enumerate(columns)) for i in range(output_bits)]
    return affine_solutions([(row,0) for row in rows],len(columns))[1]


def acquire_projector_blocks(source_anf,quadratics,n):
    source=set(source_anf);B0=polar_rows(source,n);inverse=[]
    for i in range(n):
        solution=affine_solutions([(row,int(j==i)) for j,row in enumerate(B0)],n)
        if solution is None or solution[1]:raise ValueError('nondegenerate source polar form required')
        inverse.append(solution[0])
    operators=[]
    for terms in quadratics:
        polar=polar_rows(terms,n);operator=[apply_binary(inverse,column) for column in polar]
        if any(apply_binary(operator,column)!=column for column in operator):
            raise ValueError('an acquired source-relative polar operator is not idempotent')
        operators.append(operator)
    for i,A in enumerate(operators):
        for B in operators[:i]:
            if any(apply_binary(A,B[j])!=apply_binary(B,A[j]) for j in range(n)):
                raise ValueError('the acquired source-relative projectors do not commute')
    blocks=[dict(columns=[1<<i for i in range(n)],signature=0)]
    for index,operator in enumerate(operators):
        next_blocks=[]
        for block in blocks:
            columns=block['columns'];images=[apply_binary(operator,v) for v in columns]
            if all(x==0 for x in images):next_blocks.append(block);continue
            if images==columns:
                next_blocks.append(dict(columns=columns,signature=block['signature']|(1<<index)));continue
            kernel0=linear_kernel(images,n)
            kernel1=linear_kernel([x^v for x,v in zip(images,columns)],n)
            if len(kernel0)+len(kernel1)!=len(columns):raise AssertionError('joint projector eigenspace did not split')
            for value,kernel in enumerate((kernel0,kernel1)):
                if kernel:next_blocks.append(dict(columns=[apply_binary(columns,v) for v in kernel],
                    signature=block['signature']|(value<<index)))
        blocks=next_blocks
    assert len(independent_basis(v for block in blocks for v in block['columns']))==n
    local=[];emission=[];unobserved=[]
    for block in blocks:
        columns=block['columns'];nonzero=[];mask=0
        for i,terms in enumerate(quadratics):
            restricted=compose_quadratic(set(terms)-{0},0,columns)
            if restricted:
                if nonzero and restricted!=nonzero[0]:
                    raise ValueError('a joint eigenspace carries more than one quadratic information bit')
                if not nonzero:nonzero.append(restricted)
                mask|=1<<i
        source_local=compose_quadratic(source-{0},0,columns)
        if nonzero:
            local.append(dict(columns=columns,input_bits=len(columns),source_anf=sorted(source_local),
                information_anf=sorted(nonzero[0]),emission_column=mask,signature=block['signature']))
            emission.append(mask)
        else:unobserved.append(dict(columns=columns,input_bits=len(columns),source_anf=sorted(source_local)))
    constant=sum(int(0 in row)<<i for i,row in enumerate(quadratics))
    return dict(input_bits=n,marked_quadratics=len(quadratics),blocks=local,unobserved_blocks=unobserved,
        emission_columns=emission,output_constant=constant,source_constant=int(0 in source),
        manufactured_joint_eigenspaces=len(blocks),commuting_idempotents_verified=True,
        enumerated_eigenvalue_patterns=0)


def projector_target_fiber(certificate,target,maximum_coset_points):
    if type(maximum_coset_points) is not int or maximum_coset_points<0:raise ValueError('explicit coset budget required')
    m=certificate['marked_quadratics'];columns=certificate['emission_columns'];width=len(columns)
    value=target^certificate['output_constant']
    rows=[sum(((column>>i)&1)<<j for j,column in enumerate(columns)) for i in range(m)]
    solution=affine_solutions([(row,(value>>i)&1) for i,row in enumerate(rows)],width)
    if solution is None:
        return dict(status='empty_fiber',fiber_weight=0,coset_dimension=None,
            coset_points_evaluated=0,quadratic_gauss_evaluations=0)
    raw_dimension=len(solution[1])
    tables=[];queries=0;prefactor=1-2*certificate['source_constant']
    for block in certificate['unobserved_blocks']:
        prefactor*=quadratic_gap(block['source_anf'],block['input_bits']);queries+=1
    for block in certificate['blocks']:
        Z=quadratic_gap(block['source_anf'],block['input_bits'])
        W=quadratic_gap(set(block['source_anf'])^set(block['information_anf']),block['input_bits'])
        if (Z+W)%2 or (Z-W)%2:raise AssertionError('nonintegral local response')
        tables.append([(Z+W)//2,(Z-W)//2]);queries+=2
    total=prefactor
    for table in tables:total*=sum(table)
    # Pin one-point local distributions and integrate uniform local bits.
    # These are exact signed weights, so equality/zero are integer tests.
    target=value;uniform=[];active=[];uniform_scale=1;forced=0
    for j,table in enumerate(tables):
        if not table[0] and not table[1]:
            return dict(status='counted',fiber_weight=0,coset_dimension=0,raw_coset_dimension=raw_dimension,
                coset_points_evaluated=0,quadratic_gauss_evaluations=queries,total_response=total,
                local_tables=tables,zero_local_distribution=True)
        if table[0]==table[1]:uniform.append(j);uniform_scale*=table[0]
        elif not table[0]:target^=columns[j];prefactor*=table[1];forced+=1
        elif not table[1]:prefactor*=table[0];forced+=1
        else:active.append(j)
    _,annihilator=affine_solutions([(columns[j],0) for j in uniform],m)
    rank_uniform=m-len(annihilator)
    prefactor*=uniform_scale*(1<<(len(uniform)-rank_uniform))
    equations=[(sum(((functional&columns[j]).bit_count()&1)<<k for k,j in enumerate(active)),
        (functional&target).bit_count()&1) for functional in annihilator]
    reduced=affine_solutions(equations,len(active))
    common=dict(raw_coset_dimension=raw_dimension,uniform_bits_eliminated=len(uniform),
        forced_local_bits=forced,nonuniform_bits=len(active),quadratic_gauss_evaluations=queries,
        total_response=total,local_tables=tables)
    if reduced is None:
        return dict(**common,status='empty_fiber',fiber_weight=0,coset_dimension=None,
            coset_points_evaluated=0)
    offset,kernel=reduced;required=1<<len(kernel)
    if required>maximum_coset_points:
        return dict(**common,status='coset_budget_insufficient',fiber_weight=None,coset_dimension=len(kernel),
            required_coset_points=required,coset_points_evaluated=0)
    answer=0
    for parameter in range(required):
        point=offset^apply_binary(kernel,parameter);weight=prefactor
        for k,j in enumerate(active):weight*=tables[j][(point>>k)&1]
        answer+=weight
    return dict(**common,status='counted',fiber_weight=answer,coset_dimension=len(kernel),
        coset_offset=offset,coset_basis=kernel,coset_points_evaluated=required,
        active_latent_indices=active)


def count_projector_reversible_response(source_anf,program,maximum_coset_points=0):
    reversible=acquire_reversible_terminal_and(program)
    certificate=acquire_projector_blocks(source_anf,reversible['initial_quadratics'],reversible['input_bits'])
    target=invert_terminal(reversible);fiber=projector_target_fiber(certificate,target,maximum_coset_points)
    common=dict(reversible_certificate=reversible,projector_certificate=certificate,fiber_certificate=fiber,
        original_input_assignments_enumerated=0,auxiliary_independent_inputs=0,
        complete_quadratic_summary_cube_enumerated=False)
    if fiber['status']=='coset_budget_insufficient':return dict(**common,status=fiber['status'],weighted_gap=None)
    total=fiber.get('total_response');extra_query=int(total is None)
    if total is None:total=quadratic_gap(source_anf,reversible['input_bits'])
    return dict(**common,status='counted',accepted_initial_register_value=target,
        weighted_gap=total-2*fiber['fiber_weight'],inverted_terminal_states=1,
        total_quadratic_gauss_evaluations=fiber['quadratic_gauss_evaluations']+extra_query)


def count_projector_resonant_program(program,field_h,maximum_coset_points=0):
    sys.path.insert(0,str(ROOT/'work_ring_count_agent'))
    from circuit_field_packing import BinaryField
    from resonant_two_trace_boundary import response_constants
    F=BinaryField(field_h);a=F.n;validate_trace_program(program,2*a)
    source={(1<<i)|(1<<(a+j)) for i in range(a) for j in range(a) if F.trace(F.mul(1<<i,1<<j))}
    result=count_projector_reversible_response(source,program,maximum_coset_points)
    result.update(field_polynomial=field_h,field_degree=a,source_D=[[0,F.eta],[1,1]],
        original_independent_bits=12*a,counted_domain_size=1<<(12*a))
    if result['status']=='counted':
        _,B,delta=response_constants(F.q);evaluate,_,_=prepared_program(program,2*a)
        gap=B*result['weighted_gap']+delta*(1-2*evaluate(0));domain=1<<(12*a)
        if abs(gap)>domain or (domain-gap)%2:raise AssertionError('invalid original-domain count')
        result.update(gap=gap,ones=(domain-gap)//2,zeros=(domain+gap)//2)
    return result
