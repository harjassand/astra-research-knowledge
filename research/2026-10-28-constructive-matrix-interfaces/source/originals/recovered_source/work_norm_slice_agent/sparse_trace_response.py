#!/usr/bin/env python3
"""Aggregate point/character responses and manufacture small actual support.

With M nonzero Fourier characters and P point corrections, uncertainty
gives support >= ceil(2^a/M)-P.  If that does not exceed budget B, the
entire field has at most M(P+B) elements, so bounded enumeration is an
explicitly polynomial operation in the supplied representation and B.
"""
from quadratic_trace_pushforward import anf_value


def canonical_sparse_spec(spec):
    a=spec.get('output_bits')
    if type(a) is not int or a<0:raise ValueError('explicit nonnegative output width required')
    out=dict(spec)
    for name in ('points','characters'):
        coefficients={}
        for key,value in spec[name]:
            if type(key) is not int or key<0 or key.bit_length()>a or type(value) is not int:
                raise ValueError('binary indices and exact integer sparse coefficients required')
            coefficients[key]=coefficients.get(key,0)+value
        out[name]=[[x,c] for x,c in sorted(coefficients.items()) if c]
    phi=set(spec.get('output_boolean_quadratic',()))
    if any(type(x) is not int or x<0 or x.bit_length()>a or x.bit_count()>2 for x in phi):
        raise ValueError('explicit common Boolean output quadratic required')
    out['output_boolean_quadratic']=sorted(phi)
    return out


def aggregate_field_responses(weighted_responses):
    """Combine compiled pencil responses, including cancellation of characters."""
    entries=list(weighted_responses)
    if not entries:raise ValueError('at least one explicit field response required')
    first=entries[0][1];a=first['output_bits'];h=first['field_polynomial'];phi=first['output_boolean_quadratic']
    points={};characters={}
    for weight,response in entries:
        if type(weight) is not int:raise ValueError('exact integer response weights required')
        if (response['output_bits'],response['field_polynomial'],response['output_boolean_quadratic'])!=(a,h,phi):
            raise ValueError('one field basis and one common output quadratic required')
        if not weight or response['empty']:continue
        kind=response['field_response_kind']
        if kind=='point':
            point=response['support_offset']
            sign=anf_value(response['sign_anf'],0)^anf_value(phi,point)
            points[point]=points.get(point,0)+weight*response['amplitude']*(1-2*sign)
        elif kind=='full_character':
            frequency=response['base_character_binary_frequency']
            characters[frequency]=characters.get(frequency,0)+weight*response['amplitude']*(1-2*response['base_character_constant'])
        else:raise ValueError('unrecognized nonzero field response')
    return dict(output_bits=a,field_polynomial=h,output_boolean_quadratic=list(phi),
        points=[[x,c] for x,c in sorted(points.items()) if c],
        characters=[[x,c] for x,c in sorted(characters.items()) if c],
        input_response_terms=len(entries),character_cancellations_combined=True,
        enumerated_field_elements=0)


def sparse_response_value(spec,point):
    value=sum(coefficient*(1-2*((frequency&point).bit_count()&1)) for frequency,coefficient in spec['characters'])
    value+=sum(coefficient for x,coefficient in spec['points'] if x==point)
    return value*(1-2*anf_value(spec['output_boolean_quadratic'],point))


def acquire_sparse_response_support(spec,budget,maximum_field_scan=None):
    """List bounded support or return an exact support/budget certificate.

    ``None`` retains the polynomial-in-(sparse-input,budget) scan from the
    uncertainty proof. An explicit scan cap forbids scanning a larger field,
    even when that polynomial bound would permit it. It does not charge
    evaluations of an arbitrary output program; this routine uses no program.
    """
    if type(budget) is not int or budget<0:raise ValueError('explicit nonnegative support budget required')
    if maximum_field_scan is not None and (type(maximum_field_scan) is not int or maximum_field_scan<0):
        raise ValueError('nonnegative explicit field-scan budget required')
    spec=canonical_sparse_spec(spec)
    a=spec['output_bits'];q=1<<a;M=len(spec['characters']);P=len(spec['points'])
    common=dict(output_bits=a,budget=budget,nonzero_character_terms=M,point_corrections=P,
        enumerated_field_elements=0,support=None)
    if M==0:
        if P>budget:return dict(**common,status='support_exceeds_budget',support_lower_bound=P,
            exact_support_cardinality=P,certificate='exact nonzero point list')
        result=dict(common);result.update(status='support_acquired',support=[
            [x,c*(1-2*anf_value(spec['output_boolean_quadratic'],x))] for x,c in spec['points']],
            exact_support_cardinality=P,certificate='all character terms cancel exactly')
        return result
    lower=(q+M-1)//M-P
    if q>M*(P+budget):
        assert lower>budget
        return dict(**common,status='support_exceeds_budget',support_lower_bound=lower,
            exact_support_cardinality=None,certificate='Fourier uncertainty after point corrections')
    if maximum_field_scan is not None and q>maximum_field_scan:
        return dict(**common,status='field_scan_budget_insufficient',
            required_complete_scan=q,field_scan_budget=maximum_field_scan,
            enumeration_bound=M*(P+budget),exact_support_cardinality=None,
            certificate='explicit field-scan budget is insufficient for complete support acquisition')
    # In this branch the field size is itself bounded polynomially by
    # the explicit sparse input size and the chosen support budget.
    points=dict(spec['points']);found=[]
    for x in range(q):
        value=points.get(x,0)
        for frequency,coefficient in spec['characters']:
            value+=coefficient*(1-2*((frequency&x).bit_count()&1))
        if value:
            value*=1-2*anf_value(spec['output_boolean_quadratic'],x)
            found.append([x,value])
            if len(found)>budget:
                result=dict(common);result.update(status='support_exceeds_budget',
                    support_lower_bound=len(found),exact_support_cardinality=None,
                    enumerated_field_elements=x+1,enumeration_bound=M*(P+budget),
                    certificate='explicit distinct nonzero output points')
                return result
    result=dict(common);result.update(status='support_acquired',support=found,
        exact_support_cardinality=len(found),enumerated_field_elements=q,
        enumeration_bound=M*(P+budget),certificate='complete polynomially bounded output domain')
    return result


def evaluate_program_on_sparse_response(spec,program,budget):
    from equidegree_trace_program import validate_trace_program,evaluate_trace_program
    validate_trace_program(program,spec['output_bits'])
    support=acquire_sparse_response_support(spec,budget)
    if support['status']!='support_acquired':return dict(status=support['status'],support_certificate=support,
        weighted_gap=None,program_evaluations=0)
    value=0;observations=[]
    for point,coefficient in support['support']:
        bit=evaluate_trace_program(program,point,spec['output_bits']);value+=coefficient*(1-2*bit)
        if len(support['support'])<=32:observations.append([point,bit])
    return dict(status='counted',weighted_gap=value,program_evaluations=len(support['support']),
        observations=observations,support_certificate=support,trace_program_anf_expanded=False,
        auxiliary_independent_inputs=0)
