#!/usr/bin/env python3
"""A two-point trace-program counter and a separate one-query #SAT reduction.

The reduction emits an ordinary Boolean circuit; it does not compute its
target count.  Small physical histograms are generated only by the audit.
"""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / p) for p in (
    'work_matrix_root', 'work_chain_root', 'work_ring_count_agent')]
from universal_circuit_phase import circuit_value, compile_circuit_phase
from circuit_field_packing import BinaryField, power_two_field_modulus
from diagonal_operator_boolean_circuit import BooleanDAG, FieldCircuit
from joint_trace_response import (
    paired_coordinate_quadratic, trace_dual_coordinates,
    _attach_program, _xor_all)


def response_constants(q):
    if type(q) is not int or q < 2 or q & (q - 1):
        raise ValueError('a binary prime-power field size is required')
    origin = q**8 + (q*q - 1) * q**4
    ordinary = (q + 1) * q**6 + (q*q - q - 1) * q**4
    correction = q**5 * (q - 1)**2 * (q + 1)
    assert origin - ordinary == correction
    return origin, ordinary, correction


def prepare_quadratic_marker_query(circuit, minimum_field_degree=2):
    """Manufacture one target, with no source or target count oracle call."""
    compile_circuit_phase(circuit)
    if type(minimum_field_degree) is not int or minimum_field_degree < 2:
        raise ValueError('minimum even field degree must be at least two')
    n = circuit['n']
    a = 1 << (max(n, minimum_field_degree, 2) - 1).bit_length()
    F = BinaryField(power_two_field_modulus(a))
    c = F.eta  # A basis coordinate of absolute trace one, not a field search.
    assert F.trace(c) == 1
    A, B, correction = response_constants(F.q)
    return dict(
        source_circuit=circuit, field_degree=a, field_modulus=F.h,
        irreducible_operator_polynomial=[c, 1, 1],
        source_operator=[[0, c], [1, 1]], matrix_size=2, beta=1,
        original_target_bits=12*a, original_circuit_inputs=n,
        uniform_trace_padding_power=a-n,
        response_origin=A, response_ordinary=B,
        response_origin_correction=correction,
        reduction_kind='resonant-two-by-two-fixed-quadratic-marker',
        original_circuit_count_computed=False,
        target_count_computed=False,
        internal_gates_are_free_inputs=False)


def prepare_binary_summary_query(circuit, minimum_field_degree=2):
    """One explicitly manufactured binary-linear summary already suffices.

    w=v+P(s), P(s)=sum_i s_(2i+1)*dual_basis[2i].  Its binary rank is a/2,
    so this P is not field-linear.  The only extra program is C(w)+g*(w).
    """
    query = prepare_quadratic_marker_query(circuit, minimum_field_degree)
    F = BinaryField(query['field_modulus'])
    dual = F.dual_basis()
    columns = [dual[j-1] if j % 2 else 0 for j in range(F.n)]
    query.update(
        reduction_kind='resonant-two-by-two-one-binary-linear-summary',
        summary_P_columns=columns, summary_P_binary_rank=F.n//2,
        summary_is_field_linear=False)
    return query


def summary_P(query, s):
    value = 0
    for j, coefficient in enumerate(query['summary_P_columns']):
        if s >> j & 1:
            value ^= coefficient
    return value


def read_quadratic_marker_count(query, target_ones):
    """Read one supplied exact target count; do not calculate that count."""
    if query.get('reduction_kind') not in (
            'resonant-two-by-two-fixed-quadratic-marker',
            'resonant-two-by-two-one-binary-linear-summary'):
        raise ValueError('wrong reduction certificate')
    a, n = query['field_degree'], query['original_circuit_inputs']
    N = query['original_target_bits']
    if a % 2 or N != 12*a or type(target_ones) is not int or not 0 <= target_ones <= 1 << N:
        raise ValueError('invalid field degree, original dimension, or count')
    _, B, correction = response_constants(1 << a)
    c0 = circuit_value(query['source_circuit'], 0)
    residual = (1 << N) - 2*target_ones - correction*(1 - 2*c0)
    trace_gap, remainder = divmod(residual, B * (1 << (a//2)))
    if remainder or abs(trace_gap) > 1 << a:
        raise ValueError('target count has no valid trace-gap readout')
    source_count, remainder = divmod((1 << a) - trace_gap, 1 << (a-n+1))
    if remainder or not 0 <= source_count <= 1 << n:
        raise ValueError('inferred source count is nonintegral or out of range')
    return source_count


def count_one_central_trace_program(circuit, field_h, coefficient_s=1,
                                    coefficient_v=0, linear_s=0, linear_v=0):
    """Exact full count with an arbitrary program of one central marked trace.

    w = coefficient_s tr(X) + coefficient_v tr(DX).
    The base phase has the optional linear_s tr(X)+linear_v tr(DX).
    This counts its 12a original inputs, never the source program alone.
    """
    compile_circuit_phase(circuit)
    F = BinaryField(field_h)
    if circuit['n'] > F.n:
        raise ValueError('the trace field has too few binary input coordinates')
    scalars = (coefficient_s, coefficient_v, linear_s, linear_v)
    if any(type(x) is not int or not 0 <= x < F.q for x in scalars):
        raise ValueError('invalid coefficient in the acquired field')
    A, B, correction = response_constants(F.q)
    root = F.frobenius(F.mul(coefficient_s, coefficient_v), F.n - 1)
    point = (F.mul(coefficient_s, linear_v) ^
             F.mul(coefficient_v, linear_s) ^ root)
    phase = F.trace(F.mul(linear_s, linear_v))
    mask = (1 << circuit['n']) - 1
    p0 = circuit_value(circuit, 0)
    p1 = circuit_value(circuit, point & mask)
    gap = correction*(1 - 2*p0) + B*F.q*(1 - 2*(phase ^ p1))
    N = 12*F.n
    assert abs(gap) <= 1 << N and gap % 2 == 0
    return dict(
        original_bits=N, gap=gap, ones=((1 << N)-gap)//2,
        zeros=((1 << N)+gap)//2,
        source_operator=[[0, F.eta], [1, 1]],
        acquired_support_points=sorted({0, point}),
        support_field_degree=F.n, program_evaluations=2,
        linear_phase_bit=phase,
        uniform_polynomial_time=True,
        original_circuit_count_computed=False,
        source_program_gates=len(circuit['gates']))


def literal_quadratic_marker_query(query):
    """Emit a causal Boolean DAG with exactly 12a original input variables."""
    a = query['field_degree']
    F = BinaryField(query['field_modulus'])
    if a != F.n or a % 2:
        raise ValueError('validated even-degree query required')
    dag = BooleanDAG(12*a)
    fc = FieldCircuit(dag, F.h)
    X, Y, Z = [
        [[tuple((group*4 + 2*i+j)*a+k for k in range(a))
          for j in range(2)] for i in range(2)] for group in range(3)]
    s = fc.add(X[0][0], X[1][1])
    v = fc.add(fc.add(X[0][1], fc.multiply(fc.constant(F.eta), X[1][0])),
               X[1][1])
    field_phase = fc.multiply(s, v)
    for i in range(2):
        for j in range(2):
            xy = fc.add(fc.multiply(X[i][0], Y[0][j]),
                        fc.multiply(X[i][1], Y[1][j]))
            field_phase = fc.add(field_phase, fc.multiply(xy, Z[j][i]))
    traced = _xor_all(dag, [field_phase[i] for i in range(a)
                           if F.trace_mask >> i & 1])
    single_summary = query['reduction_kind'] == 'resonant-two-by-two-one-binary-linear-summary'
    if single_summary:
        projected = tuple(_xor_all(dag, [s[j] for j, coefficient in
                          enumerate(query['summary_P_columns']) if coefficient >> i & 1])
                          for i in range(a))
        argument = fc.add(v, projected)
    else:
        argument = s
    output = dag.xor(traced, _attach_program(dag, query['source_circuit'], argument))
    dual_argument = [_xor_all(dag, [argument[j] for j in range(a)
                                   if F.trace(F.mul(1 << i, 1 << j))]) for i in range(a)]
    for i in range(0, a, 2):
        output = dag.xor(output, dag.and_(dual_argument[i], dual_argument[i+1]))
        if not single_summary:
            output = dag.xor(output, dag.and_(v[i], v[i+1]))
    return dict(n=12*a, gates=dag.gates, output=output, query=query,
                target_kind=query['reduction_kind'],
                internal_gates_are_free_inputs=False)


def direct_field_value(program, packed):
    query = program['query']
    F = BinaryField(query['field_modulus'])
    a = F.n
    X, Y, Z = [
        [[(packed >> ((group*4 + 2*i+j)*a)) & (F.q-1)
          for j in range(2)] for i in range(2)] for group in range(3)]
    s = X[0][0] ^ X[1][1]
    v = X[0][1] ^ F.mul(F.eta, X[1][0]) ^ X[1][1]
    phase = F.mul(s, v)
    for i in range(2):
        for j in range(2):
            for k in range(2):
                phase ^= F.mul(F.mul(X[i][j], Y[j][k]), Z[k][i])
    source = query['source_circuit']
    single_summary = query['reduction_kind'] == 'resonant-two-by-two-one-binary-linear-summary'
    argument = v ^ summary_P(query, s) if single_summary else s
    result = (F.trace(phase) ^
              circuit_value(source, argument & ((1 << source['n']) - 1)) ^
              paired_coordinate_quadratic(trace_dual_coordinates(F, argument), a))
    if not single_summary:
        result ^= paired_coordinate_quadratic(v, a)
    return result
