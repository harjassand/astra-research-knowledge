#!/usr/bin/env python3
"""Acquire quadratic information from a Boolean DAG and integrate it exactly.

This is an exponential-in-acquired-summary-rank algorithm, not a generic
polynomial counter.  It never inverts a quadratic map or scans the original
input domain.  The response is a sum of explicitly parametrized signed
affine quadratic components.  Gaussian elimination is classical; acquisition
and composition are explicit parts of this adapter.
"""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT/p) for p in ('work_norm_slice_agent',
    'work_norm_glue_agent', 'work_norm_frontier_agent', 'work_matrix_root')]
from equidegree_trace_program import validate_trace_program
from program_span_trace_response import BinarySpan, apply_binary
from quadratic_trace_pushforward import anf_value, compile_quadratic_pushforward


def positions(mask):
    while mask:
        bit = mask & -mask
        yield bit.bit_length()-1
        mask ^= bit


def quadratic_product(left, right):
    if left == set() or right == set(): return set()
    if left == {0}: return right
    if right == {0}: return left
    if left is None or right is None: return None
    if left == right: return set(left)
    if left ^ right == {0}: return set()
    # A high-degree coefficient can be certified locally: only monomials
    # contained in that <=4-bit union can contribute to it.  This safely
    # rejects most dense nonlinear products before expanding O(n^4) terms.
    # Absence of a witness is never acceptance; the complete product below
    # remains the fallback, so high-degree cancellation is handled exactly.
    seen=set()
    for x in list(left)[:16]:
        for y in list(right)[:16]:
            mask=x|y
            if mask.bit_count()<=2 or mask in seen:continue
            seen.add(mask);bits=list(positions(mask))
            candidates=[0]+[1<<i for i in bits]
            candidates.extend((1<<i)|(1<<j) for index,i in enumerate(bits) for j in bits[index+1:])
            parity=0
            for a in candidates:
                if a not in left:continue
                for b in candidates:
                    if a|b==mask and b in right:parity^=1
            if parity:return None
    result = set()
    for x in left:
        for y in right:
            monomial = x | y
            if monomial in result: result.remove(monomial)
            else: result.add(monomial)
    return None if any(x.bit_count() > 2 for x in result) else result


def acquire_quadratic_program(program):
    """Certify P(x)=R(Q_1(x),...,Q_r(x)) from exact quadratic DAG cuts.

    Known means exact degree <=2; unknown means no certificate.  No degree
    truncation occurs, including at intermediate gates.  Constants are kept
    in cut bindings rather than in the quadratic span.
    """
    n=program.get('inputs',program.get('n'))
    n,gates,output=validate_trace_program(program,n)
    forms=[{1<<i} for i in range(n)]
    for gate in gates:
        op=gate['op'];args=gate.get('args',[]);values=[forms[x] for x in args]
        if op=='const':value={0} if gate['value'] else set()
        elif op=='not':value=None if values[0] is None else values[0]^{0}
        elif op=='xor':
            value=set() if args[0]==args[1] else None if None in values else values[0]^values[1]
        elif op=='and':value=quadratic_product(*values)
        elif op=='or':
            if {0} in values:value={0}
            elif args[0]==args[1]:value=values[0]
            elif None in values:value=None
            else:
                product=quadratic_product(*values)
                value=None if product is None else values[0]^values[1]^product
        forms.append(value)
    needed=set();cuts={};pending=[output]
    while pending:
        wire=pending.pop()
        if wire in needed:continue
        needed.add(wire)
        if forms[wire] is not None:cuts[wire]=forms[wire]
        else:pending.extend(gates[wire-n].get('args',[]))
    monomials=[1<<i for i in range(n)]
    monomials.extend((1<<i)|(1<<j) for i in range(n) for j in range(i+1,n))
    index={x:i for i,x in enumerate(monomials)}
    span=BinarySpan();basis=[];encoded={}
    for wire,terms in sorted(cuts.items()):
        vector=sum(1<<index[x] for x in terms if x)
        encoded[wire]=vector
        if span.add(vector,1<<len(basis)):basis.append(sorted(terms-{0}))
    bindings={wire:dict(frequency=span.coordinates(encoded[wire]),constant=int(0 in terms))
        for wire,terms in cuts.items()}
    assert all(item['frequency'] is not None for item in bindings.values())
    return dict(input_bits=n,program_gates=len(gates),summary_bits=len(basis),
        quadratic_basis=basis,bindings=bindings,needed=sorted(needed),output=output,
        certified_quadratic_gates=sum(x is not None for x in forms),
        cut_count=len(cuts),nonlinear_retained_nodes=len(needed)-len(cuts),
        original_input_assignments_enumerated=0,exact_DAG_identity=True,
        quadratic_map_assumed_onto=False,quadratic_map_inverted=False)


def evaluate_quotient_program(program,certificate,summary):
    r=certificate['summary_bits'];n=certificate['input_bits']
    if type(summary) is not int or summary<0 or summary.bit_length()>r:
        raise ValueError('summary outside its explicit binary cube')
    values={}
    for wire in certificate['needed']:
        binding=certificate['bindings'].get(wire)
        if binding is not None:
            bit=binding['constant']^((binding['frequency']&summary).bit_count()&1)
        else:
            gate=program['gates'][wire-n];op=gate['op'];args=gate.get('args',[])
            if op=='const':bit=gate['value']
            elif op=='not':bit=1^values[args[0]]
            elif op=='xor':bit=values[args[0]]^values[args[1]]
            elif op=='and':bit=values[args[0]]&values[args[1]]
            else:bit=values[args[0]]|values[args[1]]
        values[wire]=bit
    return values[certificate['output']]


def compose_quadratic(terms,offset,columns):
    """Exact affine pullback, acquired by coefficient evaluation of degree <=2."""
    terms=set(terms);d=len(columns);constant=anf_value(terms,offset)
    linear=[anf_value(terms,offset^column)^constant for column in columns]
    out={0} if constant else set()
    out.update(1<<j for j,bit in enumerate(linear) if bit)
    for j in range(d):
        for k in range(j+1,d):
            if anf_value(terms,offset^columns[j]^columns[k])^linear[j]^linear[k]^constant:
                out.add((1<<j)|(1<<k))
    return out


def quadratic_gap(terms,n):
    response=compile_quadratic_pushforward(terms,[0]*n,0)
    if response['empty']:return 0
    assert response['support_cardinality']==1
    return response['amplitude']*(1-2*anf_value(response['sign_anf'],0))


def walsh(values):
    out=list(values);stride=1
    while stride<len(out):
        for start in range(0,len(out),2*stride):
            for j in range(start,start+stride):
                left,right=out[j],out[j+stride]
                out[j]=left+right;out[j+stride]=left-right
        stride*=2
    return out


def validate_component(component,ambient):
    offset=component['offset'];columns=component['basis'];sign=component['sign_anf']
    if type(offset) is not int or offset<0 or offset.bit_length()>ambient:
        raise ValueError('invalid affine component offset')
    if any(type(x) is not int or x<0 or x.bit_length()>ambient for x in columns):
        raise ValueError('invalid component basis')
    span=BinarySpan()
    for column in columns:
        if not span.add(column,0):raise ValueError('component parametrization must be injective')
    if any(type(x) is not int or x<0 or x.bit_length()>len(columns) or x.bit_count()>2 for x in sign):
        raise ValueError('component sign must be an explicit quadratic')
    if type(component['coefficient']) is not int:raise ValueError('integer component coefficient required')


def integrate_quadratic_program(components,program,maximum_summary_points=0):
    """Exact weighted gap; charge 2^r quadratic sums and quotient evaluations.

    components describe sum c*1_(x=offset+basis*y)*(-1)^Q(y).  The basis
    in each component is injective and explicitly verified.  A zero-bit
    component is a point.  All acquisition occurs before the budget check.
    """
    if type(maximum_summary_points) is not int or maximum_summary_points<0:
        raise ValueError('an explicit nonnegative summary budget is required')
    certificate=acquire_quadratic_program(program);n=certificate['input_bits']
    components=list(components)
    for item in components:validate_component(item,n)
    r=certificate['summary_bits'];size=1<<r
    common=dict(certificate=certificate,summary_domain_size=size,
        component_count=len(components),original_input_assignments_enumerated=0,
        original_field_elements_scanned=0,auxiliary_independent_inputs=0)
    if size>maximum_summary_points:
        return dict(**common,status='summary_budget_insufficient',weighted_gap=None,
            quadratic_gauss_evaluations=0,quotient_program_evaluations=0)
    spectrum=[0]*size;gauss_evaluations=0;point_terms=[]
    for item in components:
        coefficient=item['coefficient'];d=len(item['basis'])
        if not coefficient:continue
        if not d:
            x=item['offset'];y=sum(anf_value(row,x)<<j for j,row in enumerate(certificate['quadratic_basis']))
            point_terms.append((y,coefficient*(1-2*anf_value(item['sign_anf'],0))))
            continue
        pullbacks=[compose_quadratic(row,item['offset'],item['basis'])
            for row in certificate['quadratic_basis']]
        for frequency in range(size):
            terms=set(item['sign_anf'])
            for j in positions(frequency):terms.symmetric_difference_update(pullbacks[j])
            spectrum[frequency]+=coefficient*quadratic_gap(terms,d)
            gauss_evaluations+=1
    transformed=walsh(spectrum);weights=[]
    for value in transformed:
        weight,remainder=divmod(value,size)
        if remainder:raise AssertionError('signed fiber Fourier inversion was not integral')
        weights.append(weight)
    for point,coefficient in point_terms:weights[point]+=coefficient
    values=[evaluate_quotient_program(program,certificate,y) for y in range(size)]
    gap=sum(weight*(1-2*bit) for weight,bit in zip(weights,values))
    return dict(**common,status='counted',weighted_gap=gap,
        quadratic_gauss_evaluations=gauss_evaluations,quotient_program_evaluations=size,
        signed_fiber_weights=weights,quotient_program_values=values,
        fiber_weight_nonnegativity_assumed=False)


def sparse_spec_components(spec):
    from sparse_trace_response import canonical_sparse_spec
    spec=canonical_sparse_spec(spec);n=spec['output_bits'];phi=set(spec['output_boolean_quadratic'])
    out=[]
    for frequency,coefficient in spec['characters']:
        terms=phi^{1<<j for j in positions(frequency)}
        out.append(dict(offset=0,basis=[1<<j for j in range(n)],
            sign_anf=sorted(terms),coefficient=coefficient))
    for point,coefficient in spec['points']:
        out.append(dict(offset=point,basis=[],sign_anf=[],
            coefficient=coefficient*(1-2*anf_value(phi,point))))
    return out


def evaluate_trace_response_quadratic_program(response,program,maximum_summary_points=0):
    from pencil_trace_response_evaluator import count_response_sparse_spec
    result=integrate_quadratic_program(sparse_spec_components(count_response_sparse_spec(response)),
        program,maximum_summary_points)
    result.update(original_independent_bits=response['original_independent_bits'],
        counted_domain_size=response['counted_domain_size'],full_matrix_domain=response['full_matrix_domain'])
    if result['status']=='counted':
        gap=result['weighted_gap'];domain=response['counted_domain_size']
        if abs(gap)>domain or (domain-gap)%2:raise AssertionError('invalid original-domain count')
        result.update(gap=gap,ones=(domain-gap)//2,zeros_on_counted_domain=(domain+gap)//2)
    return result


def count_resonant_two_trace_program(program,field_h,maximum_summary_points=0):
    """Full exact count of the 12a-bit resonant matrix source plus P(s,v).

    Input P is an ordinary causal program on the 2a bits of s=tr X and
    v=tr(DX). D=[[0,c],[1,1]], with trace(c)=1 acquired from a basis.
    No trace-summary decomposition of P is supplied or assumed.
    """
    sys.path.insert(0,str(ROOT/'work_ring_count_agent'))
    from circuit_field_packing import BinaryField
    from resonant_two_trace_boundary import response_constants
    F=BinaryField(field_h);a=F.n
    validate_trace_program(program,2*a)
    # Exact binary coefficients of Tr(sv); the trace pairing is explicit.
    phase={(1<<i)|(1<<(a+j)) for i in range(a) for j in range(a)
        if F.trace(F.mul(1<<i,1<<j))}
    _,B,delta=response_constants(F.q)
    components=[dict(offset=0,basis=[1<<i for i in range(2*a)],
        sign_anf=sorted(phase),coefficient=B),
        dict(offset=0,basis=[],sign_anf=[],coefficient=delta)]
    result=integrate_quadratic_program(components,program,maximum_summary_points)
    result.update(field_polynomial=field_h,field_degree=a,source_D=[[0,F.eta],[1,1]],
        original_independent_bits=12*a,counted_domain_size=1<<(12*a),
        manufactured_response_components=components,
        source_identity='Tr(tr(XYZ)+e2(X)+tr(DX^2))+P(trX,trDX)')
    if result['status']=='counted':
        gap=result['weighted_gap'];domain=result['counted_domain_size']
        if abs(gap)>domain or (domain-gap)%2:raise AssertionError('invalid full native count')
        result.update(gap=gap,ones=(domain-gap)//2,zeros=(domain+gap)//2)
    return result
