#!/usr/bin/env python3
"""Exact counting with an arbitrary supplied Boolean trace program.

The source is Tr(tr(XYZ)+tr(DX^2)+eta*tr(DX))+P(tr X), with distinct
equal-degree source factors of degree at least three. Only P(0),P(eta)
are evaluated. Internal program states never become independent inputs.
"""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'work_norm_frontier_agent'))
from matrix_kloosterman import Field,factor_polynomial
from exponential_pfaffian_kernel import exponential_kernel_refined


def validate_trace_program(program,inputs):
    if not isinstance(program,dict):raise ValueError('explicit Boolean gate-program object required')
    n=program.get('inputs',program.get('n'))
    if type(n) is not int or n!=inputs or ('n' in program and program['n']!=n):
        raise ValueError('trace program must have exactly the field-degree input bits')
    gates=program.get('gates');output=program.get('output')
    if not isinstance(gates,list) or type(output) is not int or not 0<=output<n+len(gates):
        raise ValueError('invalid trace gate program or output')
    for k,gate in enumerate(gates):
        if not isinstance(gate,dict):raise ValueError('explicit Boolean gate object required')
        op=gate.get('op');args=gate.get('args',[])
        if not isinstance(args,list) or any(type(i) is not int or not 0<=i<n+k for i in args):
            raise ValueError('trace program is not topologically ordered')
        if op=='const' and not args and gate.get('value') in (0,1):continue
        if op=='not' and len(args)==1:continue
        if op in ('and','or','xor') and len(args)==2:continue
        raise ValueError('unsupported or malformed Boolean trace gate')
    return n,gates,output


def evaluate_trace_program(program,value,inputs=None):
    if not isinstance(program,dict):raise ValueError('explicit Boolean gate-program object required')
    if inputs is None:inputs=program.get('inputs',program.get('n'))
    n,gates,output=validate_trace_program(program,inputs)
    if type(value) is not int or not 0<=value<1<<n:raise ValueError('trace input is outside its binary domain')
    wires=[(value>>i)&1 for i in range(n)]
    for gate in gates:
        op=gate['op'];args=gate.get('args',[])
        if op=='const':v=gate['value']
        elif op=='not':v=1^wires[args[0]]
        elif op=='and':v=wires[args[0]]&wires[args[1]]
        elif op=='or':v=wires[args[0]]|wires[args[1]]
        else:v=wires[args[0]]^wires[args[1]]
        wires.append(v)
    return wires[output]


def squarefree_equidegree_response(field_h,factors):
    """Return exact E,O and q^K: the signed trace response has two points."""
    F=Field(field_h);factors=[list(f) for f in factors]
    if not factors:raise ValueError('at least one source factor required')
    d=len(factors[0])-1;r=len(factors);t=d*r
    if d<3 or len({tuple(f) for f in factors})!=r:
        raise ValueError('distinct common-degree factors with degree at least three required')
    if any(len(f)!=d+1 or f[-1]!=1 or any(type(c) is not int or not 0<=c<F.q for c in f) or
            factor_polynomial(f,F)!=[(f,1)] for f in factors):
        raise ValueError('certified equal-degree irreducible factors required')
    weights,backend=exponential_kernel_refined(t,F.q,d);row=weights[r]
    E=row[0]+row[2];O=row[1]+row[3];K=t*t+t*(t-1)//2
    return E,O,dict(field_modulus=field_h,field_degree=F.a,matrix_size=t,
        primary_degree=d,source_factors=factors,original_bits=3*F.a*t*t,
        full_profile_weights=row,response_exponent=K,response_scale=F.q**K,
        profile_backend=backend,enumerated_original_assignments=0,
        enumerated_field_elements=0,enumerated_subspaces=0,enumerated_profiles=0)


def squarefree_equidegree_trace_program(field_h,factors,program,eta=0):
    F=Field(field_h)
    if type(eta) is not int or not 0<=eta<F.q:raise ValueError('invalid field-valued eta')
    _,gates,_=validate_trace_program(program,F.a)
    E,O,metadata=squarefree_equidegree_response(field_h,factors)
    at_zero=evaluate_trace_program(program,0,F.a)
    at_eta=evaluate_trace_program(program,eta,F.a) if eta else at_zero
    gap=metadata['response_scale']*((1-2*at_zero)*E+(1-2*at_eta)*O)
    n=metadata['original_bits']
    if abs(gap)>1<<n or gap%2:raise AssertionError('invalid original-domain program count')
    metadata.update(route='arbitrary Boolean trace program, manufactured two-point response',
        eta=eta,trace_program_inputs=F.a,trace_program_gates=len(gates),
        program_at_zero=at_zero,program_at_eta=at_eta,
        program_evaluations=1+int(bool(eta)),trace_program_anf_expanded=False,
        auxiliary_independent_inputs=0,response_even=E,response_odd=O,
        zeros=((1<<n)+gap)//2,ones=((1<<n)-gap)//2)
    return gap,metadata
