#!/usr/bin/env python3
"""Count acquired quadratic fibers after recognizing reversible DAG updates.

Large total quadratic rank is allowed. The source polar form acquires
orthogonal information components, whose separate local distributions are
manufactured. A terminal AND of the complete register set is inverted
through recognized NOT/CNOT/Toffoli updates. This is a restricted compiler;
it neither assumes small components nor solves arbitrary #CircuitSAT.
"""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'work_trace_frontier'),str(ROOT/'work_norm_slice_agent'),
    str(ROOT/'work_matrix_root'),str(ROOT/'work_norm_glue_agent')]
from quadratic_program_response import (quadratic_product,positions,compose_quadratic,
    quadratic_gap,walsh,validate_trace_program,anf_value,apply_binary,BinarySpan)
from quadratic_trace_pushforward import affine_solutions
from pencil_trace_response_evaluator import prepared_program


def exact_quadratic_forms(program):
    n=program.get('inputs',program.get('n'));n,gates,output=validate_trace_program(program,n)
    forms=[{1<<i} for i in range(n)]
    for gate in gates:
        op=gate['op'];args=gate.get('args',[]);v=[forms[x] for x in args]
        if op=='const':out={0} if gate['value'] else set()
        elif op=='not':out=None if v[0] is None else v[0]^{0}
        elif op=='xor':out=set() if args[0]==args[1] else None if None in v else v[0]^v[1]
        elif op=='and':out=quadratic_product(*v)
        else:
            if {0} in v:out={0}
            elif args[0]==args[1]:out=v[0]
            elif None in v:out=None
            else:
                product=quadratic_product(*v);out=None if product is None else v[0]^v[1]^product
        forms.append(out)
    return n,gates,output,forms


def acquire_reversible_terminal_and(program):
    """Recognize a complete-register AND by peeling actual reversible updates.

    The evolving frontier is the complete register set. Controls must be
    other current frontier wires; a replaced predecessor must not already
    be a register. Every accepted step is thus a literal bijection, even
    if the underlying quadratic registers have dependent values.
    """
    n,gates,output,forms=exact_quadratic_forms(program)
    leaves=set();pending=[output];visited=set()
    while pending:
        wire=pending.pop()
        if wire in visited:continue
        visited.add(wire)
        if wire>=n and gates[wire-n]['op']=='and' and forms[wire] is None:
            pending.extend(gates[wire-n]['args'])
        else:leaves.add(wire)
    frontier=sorted(leaves);terminal=list(frontier);reverse=[]
    def candidate(position):
        wire=frontier[position]
        if wire<n:return None
        gate=gates[wire-n];op=gate['op'];args=gate.get('args',[])
        others={x:i for i,x in enumerate(frontier) if i!=position}
        if op=='not' and args[0] not in others:
            return dict(target=position,controls=[],predecessor=args[0],wire=wire)
        if op!='xor':return None
        for previous,control in (args,args[::-1]):
            if previous in others:continue
            if control in others:
                return dict(target=position,controls=[others[control]],predecessor=previous,wire=wire)
            if control>=n:
                specification=gates[control-n]
                if specification['op']=='const':
                    if specification['value']==1:
                        return dict(target=position,controls=[],predecessor=previous,wire=wire)
                    return dict(target=position,controls=None,predecessor=previous,wire=wire)
                controls=specification.get('args',[])
                if specification['op']=='and' and all(x in others for x in controls):
                    return dict(target=position,controls=sorted({others[x] for x in controls}),
                        predecessor=previous,wire=wire)
        return None
    while True:
        step=None
        for position in sorted(range(len(frontier)),key=lambda j:frontier[j],reverse=True):
            step=candidate(position)
            if step is not None:break
        if step is None:break
        reverse.append(step);frontier[step['target']]=step['predecessor']
    if any(forms[x] is None for x in frontier):
        raise ValueError('terminal register frontier contains an unrecognized irreversible update')
    return dict(input_bits=n,registers=len(frontier),terminal_wires=terminal,
        initial_wires=frontier,initial_quadratics=[sorted(forms[x]) for x in frontier],
        reverse_updates=reverse,recognized_reversible_updates=len(reverse),
        original_program_gates=len(gates),readout='AND of the complete acquired register frontier',
        useful_initial_decomposition_supplied=False,
        terminal_and_wires_visited=len(visited))


def invert_terminal(certificate,terminal_value=None):
    m=certificate['registers']
    state=(1<<m)-1 if terminal_value is None else terminal_value
    if type(state) is not int or state<0 or state.bit_length()>m:raise ValueError('invalid terminal state')
    for step in certificate['reverse_updates']:
        controls=step['controls']
        if controls is not None and all(state>>j&1 for j in controls):state^=1<<step['target']
    return state


def polar_rows(terms,n):
    rows=[0]*n
    for mask in terms:
        if mask.bit_count()==2:
            i,j=tuple(positions(mask));rows[i]^=1<<j;rows[j]^=1<<i
    return rows


def essential_space(terms,n):
    terms=set(terms);constant=int(0 in terms);polar=polar_rows(terms,n)
    _,radical=affine_solutions([(row,0) for row in polar],n)
    values=[anf_value(terms,v)^constant for v in radical]
    pivot=next((i for i,value in enumerate(values) if value),None)
    if pivot is None:invariant=radical
    else:invariant=[v^(radical[pivot] if values[i] else 0) for i,v in enumerate(radical) if i!=pivot]
    _,rows=affine_solutions([(v,0) for v in invariant],n)
    return rows,polar


def independent_basis(vectors):
    span=BinarySpan();out=[]
    for vector in vectors:
        if span.add(vector,0):out.append(vector)
    return out


class Union:
    def __init__(self,n):self.parent=list(range(n))
    def find(self,i):
        while self.parent[i]!=i:self.parent[i]=self.parent[self.parent[i]];i=self.parent[i]
        return i
    def merge(self,i,j):
        i=self.find(i);j=self.find(j)
        if i!=j:self.parent[j]=i


def acquire_orthogonal_quadratic_components(source_anf,quadratics,n):
    """Use the source symplectic dual pairing and actual essential spaces.

    Fundamental dependencies and nonzero pairings merge information blocks.
    Orthogonal radical completion is manufactured by binary linear solves.
    """
    source=set(source_anf);B=polar_rows(source,n);inverse=[]
    for i in range(n):
        answer=affine_solutions([(row,int(j==i)) for j,row in enumerate(B)],n)
        if answer is None or answer[1]:raise ValueError('this component compiler requires a nondegenerate source polar form')
        inverse.append(answer[0])
    def covector(v):return apply_binary(inverse,v)
    def pair(u,v):return (u&covector(v)).bit_count()&1
    essential=[];polars=[]
    for terms in quadratics:
        rows,polar=essential_space(terms,n);essential.append(rows);polars.append(polar)
    union=Union(len(quadratics));basis=[];owners=[]
    for i,rows in enumerate(essential):
        for row in rows:basis.append(row);owners.append(i)
    pivots={}
    for j,row in enumerate(basis):
        value=row;relation=1<<j
        while value:
            pivot=value.bit_length()-1
            if pivot not in pivots:pivots[pivot]=(value,relation);break
            old,witness=pivots[pivot];value^=old;relation^=witness
        if not value:
            involved=[owners[k] for k in positions(relation)]
            for other in involved[1:]:union.merge(involved[0],other)
    for i in range(len(quadratics)):
        for j in range(i):
            if any(pair(x,y) for x in essential[i] for y in essential[j]):union.merge(i,j)
    groups={}
    for i in range(len(quadratics)):groups.setdefault(union.find(i),[]).append(i)
    groups=list(groups.values());hparts=[];radicals=[]
    for group in groups:
        work=independent_basis(v for i in group for v in essential[i]);pairs=[];radical=[]
        while work:
            u=work.pop();mate=next((j for j,v in enumerate(work) if pair(u,v)),None)
            if mate is None:radical.append(u);continue
            v=work.pop(mate);pairs.extend([u,v])
            work=[w^(u if pair(w,v) else 0)^(v if pair(w,u) else 0) for w in work]
        hparts.append(pairs);radicals.append(radical)
    H=[x for block in hparts for x in block]
    R=[(owner,v) for owner,block in enumerate(radicals) for v in block]
    extensions=[list(h)+list(r) for h,r in zip(hparts,radicals)];partners=[]
    for j,(owner,radical) in enumerate(R):
        equations=[(covector(h),0) for h in H]
        equations.extend((covector(v),int(j==k)) for k,(_,v) in enumerate(R))
        equations.extend((covector(v),0) for v in partners)
        answer=affine_solutions(equations,n)
        if answer is None:raise AssertionError('orthogonal radical completion failed')
        partner=answer[0];partners.append(partner);extensions[owner].append(partner)
    all_dual=[v for block in extensions for v in block]
    _,complement=affine_solutions([(covector(v),0) for v in all_dual],n)
    primal_blocks=[[covector(v) for v in block] for block in extensions]
    extra=[covector(v) for v in complement]
    assert len(independent_basis([v for block in primal_blocks for v in block]+extra))==n
    # Runtime certificates of all cross-block invisibility and source orthogonality.
    checks=0
    for c,group in enumerate(groups):
        outside=[v for j,block in enumerate(primal_blocks) if j!=c for v in block]+extra
        for i in group:
            const=int(0 in quadratics[i])
            for v in outside:
                assert apply_binary(polars[i],v)==0 and (anf_value(quadratics[i],v)^const)==0
                checks+=1
    components=[]
    for group,columns in zip(groups,primal_blocks):
        local=[compose_quadratic(quadratics[i],0,columns) for i in group]
        d=len(columns);monomials=[1<<i for i in range(d)]+[(1<<i)|(1<<j) for i in range(d) for j in range(i+1,d)]
        index={x:i for i,x in enumerate(monomials)};span=BinarySpan();q_basis=[];encoded=[]
        for terms in local:
            row=sum(1<<index[x] for x in terms if x);encoded.append(row)
            if span.add(row,1<<len(q_basis)):q_basis.append(sorted(terms-{0}))
        bindings=[dict(register=i,frequency=span.coordinates(row),constant=int(0 in terms))
            for i,row,terms in zip(group,encoded,local)]
        components.append(dict(registers=group,primal_columns=columns,input_bits=d,
            source_anf=sorted(compose_quadratic(source-{0},0,columns)),
            quadratic_basis=q_basis,quadratic_rank=len(q_basis),bindings=bindings))
    extra_terms=compose_quadratic(source-{0},0,extra)
    return dict(input_bits=n,components=components,complement_columns=extra,
        complement_source_anf=sorted(extra_terms),source_constant=int(0 in source),
        essential_space_dimensions=[len(x) for x in essential],
        acquired_component_count=len(components),
        total_quadratic_rank=sum(c['quadratic_rank'] for c in components),
        maximum_component_quadratic_rank=max((c['quadratic_rank'] for c in components),default=0),
        exact_cross_block_invariance_checks=checks,source_polar_nondegenerate=True)


def manufacture_component_tables(certificate,maximum_component_points):
    if type(maximum_component_points) is not int or maximum_component_points<0:
        raise ValueError('explicit nonnegative component budget required')
    required=max((1<<c['quadratic_rank'] for c in certificate['components']),default=1)
    if required>maximum_component_points:
        return dict(status='component_budget_insufficient',required_component_points=required,
            quadratic_gauss_evaluations=0,component_tables=None)
    tables=[];evaluations=0
    for component in certificate['components']:
        r=component['quadratic_rank'];spectrum=[]
        for frequency in range(1<<r):
            terms=set(component['source_anf'])
            for j in positions(frequency):terms.symmetric_difference_update(component['quadratic_basis'][j])
            spectrum.append(quadratic_gap(terms,component['input_bits']));evaluations+=1
        values=walsh(spectrum);table=[]
        for value in values:
            quotient,remainder=divmod(value,1<<r)
            if remainder:raise AssertionError('nonintegral component fiber')
            table.append(quotient)
        tables.append(table)
    extra=quadratic_gap(certificate['complement_source_anf'],len(certificate['complement_columns']))
    extra*=1-2*certificate['source_constant'];evaluations+=1
    total=extra
    for table in tables:total*=sum(table)
    return dict(status='compiled',required_component_points=required,quadratic_gauss_evaluations=evaluations,
        component_tables=tables,complement_weight=extra,total_response=total)


def component_fiber(certificate,tables,register_value):
    value=tables['complement_weight']
    for component,table in zip(certificate['components'],tables['component_tables']):
        equations=[(binding['frequency'],((register_value>>binding['register'])&1)^binding['constant'])
            for binding in component['bindings']]
        answer=affine_solutions(equations,component['quadratic_rank'])
        if answer is None:return 0
        if answer[1]:raise AssertionError('component basis not determined by its generating register polynomials')
        value*=table[answer[0]]
    return value


def count_reversible_quadratic_response(source_anf,program,maximum_component_points=0):
    reversible=acquire_reversible_terminal_and(program);n=reversible['input_bits']
    components=acquire_orthogonal_quadratic_components(set(source_anf),reversible['initial_quadratics'],n)
    tables=manufacture_component_tables(components,maximum_component_points)
    common=dict(reversible_certificate=reversible,component_certificate=components,
        table_certificate=tables,original_input_assignments_enumerated=0,
        complete_summary_cube_enumerated=False,auxiliary_independent_inputs=0)
    if tables['status']!='compiled':return dict(**common,status=tables['status'],weighted_gap=None)
    initial=invert_terminal(reversible);accepted_weight=component_fiber(components,tables,initial)
    return dict(**common,status='counted',accepted_initial_register_value=initial,
        accepted_signed_fiber_weight=accepted_weight,
        weighted_gap=tables['total_response']-2*accepted_weight,
        inverted_terminal_states=1)


def count_reversible_resonant_program(program,field_h,maximum_component_points=0):
    sys.path.insert(0,str(ROOT/'work_ring_count_agent'))
    from circuit_field_packing import BinaryField
    from resonant_two_trace_boundary import response_constants
    F=BinaryField(field_h);a=F.n;validate_trace_program(program,2*a)
    source={(1<<i)|(1<<(a+j)) for i in range(a) for j in range(a) if F.trace(F.mul(1<<i,1<<j))}
    result=count_reversible_quadratic_response(source,program,maximum_component_points)
    result.update(field_polynomial=field_h,field_degree=a,source_D=[[0,F.eta],[1,1]],
        original_independent_bits=12*a,counted_domain_size=1<<(12*a))
    if result['status']=='counted':
        _,B,delta=response_constants(F.q);evaluate,_,_=prepared_program(program,2*a)
        result['gap']=B*result['weighted_gap']+delta*(1-2*evaluate(0))
        domain=result['counted_domain_size'];gap=result['gap']
        if abs(gap)>domain or (domain-gap)%2:raise AssertionError('invalid original-domain count')
        result.update(ones=(domain-gap)//2,zeros=(domain+gap)//2,source_ordinary=B,
            source_origin_correction=delta)
    return result
