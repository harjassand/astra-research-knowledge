#!/usr/bin/env python3
"""Exact optimal Boolean synthesis on ACQUIRED mod-four summaries.

Leaves are exhaustive finite counters. Default Fourier recomputation uses
polynomial workspace; the finite cached checks are explicitly labelled.
The asymptotic replacement-form engine is not implemented.
"""
from itertools import product
from pathlib import Path
import json
import random
from orbit_phase_compiler import (hidden_instance, acquire_raw_cubic, indices,
    phase, matrix_polynomial, apply, truth_sum)
from heterogeneous_orbit_compiler import acquire_raw


def i_power(e):
    return ((1, 0), (0, 1), (-1, 0), (0, -1))[e % 4]


def gaussian_multiply(a, b):
    return a[0]*b[0]-a[1]*b[1], a[0]*b[1]+a[1]*b[0]


def summary_at(U, y):
    return tuple((u & y).bit_count() % 4 for u in U)


def quotient_sign(K, s):
    parity = sum(((K[a] >> a) & 1)*(s[a]*(s[a]-1)//2) for a in range(len(K)))
    parity += sum(((K[a] >> b) & 1)*(s[a] & 1)*(s[b] & 1)
                  for a in range(len(K)) for b in range(a+1, len(K)))
    return -1 if parity % 2 else 1


def finite_leaf(local, U, character, n):
    re = im = 0
    for y in range(1 << n):
        exponent = sum(a*(u & y).bit_count() for a, u in zip(character, U)) % 4
        x, z = i_power(exponent)
        sign = phase(local, y)
        re += sign*x
        im += sign*z
    return re, im


def residue_counts(size):
    result = [1, 0, 0, 0]
    for _ in range(size):
        result = [result[j]+result[(j-1) % 4] for j in range(4)]
    return result


def iter_fibers(record, cache_characters=False):
    """Stream labeled fibers; default stores neither characters nor output rows."""
    n = record['original_variables']
    U = record['code_generators']
    d = len(U)
    assert sum(u.bit_count() for u in U) == n
    assert all(not (U[a] & U[b]) for a in range(d) for b in range(a))
    local = set(record['foreground_polynomial']) ^ matrix_polynomial(record['sparse_matrix'])
    K = record['quotient']
    characters = lambda: product(range(4), repeat=d)
    stored = ({ch: finite_leaf(local, U, ch, n) for ch in characters()}
              if cache_characters else None)
    populations = [residue_counts(u.bit_count()) for u in U]
    normalization = 4**d
    for s in product(range(4), repeat=d):
        nr = ni = 0
        for character in characters():
            leaf = stored[character] if stored is not None else finite_leaf(local, U, character, n)
            weight = i_power(-sum(a*b for a, b in zip(character, s)))
            re, im = gaussian_multiply(weight, leaf)
            nr += re
            ni += im
        assert ni == 0 and nr % normalization == 0
        signed_local = nr // normalization
        population = 1
        for counts, residue in zip(populations, s):
            population *= counts[residue]
        signed_target = quotient_sign(K, s)*signed_local
        assert abs(signed_target) <= population and (population-signed_target) % 2 == 0
        zeros = (population+signed_target)//2
        ones = (population-signed_target)//2
        errors = min(zeros, ones)
        yield dict(summary=list(s), population=population, signed_local=signed_local,
                   zeros=zeros, ones=ones, predicted_bit=int(ones > zeros), errors=errors)


def synthesize(record, cache_characters=False):
    """Finite validator: explicitly collect the small output table for checking."""
    n = record['original_variables']
    d = len(record['code_generators'])
    rows = list(iter_fibers(record, cache_characters))
    total_errors = sum(r['errors'] for r in rows)
    assert sum(r['population'] for r in rows) == 1 << n
    assert sum(r['zeros']-r['ones'] for r in rows) == truth_sum(set(record['final_polynomial']), n)
    return dict(original_variables=n, acquired_summary_dimension=d, summary_alphabet=4,
                summary_rows=rows, minimum_uniform_errors=total_errors, total_inputs=1 << n,
                cached_finite_characters=cache_characters, asymptotic_phase_engine_executed=False)


def compile_program(n, instructions):
    """Exact ANFs; reject any intermediate Boolean function of degree above 3."""
    wires = [{1 << i} for i in range(n)]
    maximum_degree = 1
    for op, operands in instructions:
        if op == 'const':
            value = {0} if operands[0] else set()
        elif op == 'xor':
            value = wires[operands[0]] ^ wires[operands[1]]
        elif op == 'and':
            value = set()
            for a in wires[operands[0]]:
                for b in wires[operands[1]]:
                    term = a | b
                    if term in value:
                        value.remove(term)
                    else:
                        value.add(term)
        else:
            raise ValueError('Unsupported Boolean instruction.')
        degree = max((s.bit_count() for s in value), default=0)
        if degree > 3:
            raise ValueError('An intermediate function has Boolean degree above three.')
        maximum_degree = max(maximum_degree, degree)
        wires.append(value)
    return wires[-1], dict(instructions=len(instructions), intermediate_states=len(wires)-n,
                           maximum_certified_boolean_degree=maximum_degree)


def evaluate_program(n, instructions, x):
    values = [(x >> i) & 1 for i in range(n)]
    for op, operands in instructions:
        if op == 'const':
            value = operands[0]
        elif op == 'xor':
            value = values[operands[0]] ^ values[operands[1]]
        else:
            value = values[operands[0]] & values[operands[1]]
        values.append(value)
    return values[-1]


def raw_program_fixture(rng):
    n = 9
    fixture = hidden_instance(3, 1, 2, rng, affine_disguise=False)
    instructions = []
    def emit(op, *operands):
        instructions.append((op, list(operands)))
        return n+len(instructions)-1
    registers = list(range(n))
    for _ in range(2000):
        a, b = rng.sample(range(n), 2)
        registers[a] = emit('xor', registers[a], registers[b])
    one = emit('const', 1)
    zero = emit('const', 0)
    for a in range(n):
        if rng.randrange(2):
            registers[a] = emit('xor', registers[a], one)
    total = zero
    for term in sorted(fixture['base']):
        node = one
        for j in indices(term):
            node = emit('and', node, registers[j])
        total = emit('xor', total, node)
    emit('xor', total, zero)
    poly, metadata = compile_program(n, instructions)
    rec = acquire_raw(poly, n, 3)
    signed = sum(1-2*evaluate_program(n, instructions, x) for x in range(1 << n))
    assert signed == truth_sum(poly, n) == truth_sum(set(rec['final_polynomial']), n)
    for x in range(1 << n):
        assert 1-2*evaluate_program(n, instructions, x) == phase(poly, x)
    metadata.update(original_variables=n, raw_anf_terms=len(poly),
                    raw_cubic_terms=sum(s.bit_count() == 3 for s in poly),
                    acquired_rank=rec['low_rank'], residual_edges=rec['residual_edges'],
                    exact_zero_count=((1 << n)+signed)//2,
                    exhaustive_original_program_checks=1 << n, instructions_program=instructions)
    return rec, metadata


def test():
    rng = random.Random(2026102713)
    program, program_record = raw_program_fixture(rng)
    fixtures = [program]
    for N, c, errors in [(2, 1, 0), (4, 1, 3)]:
        instance = hidden_instance(N, c, errors, rng)
        fixtures.append(acquire_raw_cubic(instance['raw'], instance['n'], c))
    results = []
    checked = fiber_checks = 0
    for i, rec in enumerate(fixtures):
        result = synthesize(rec, cache_characters=(i != 1))
        U = rec['code_generators']
        oracle = {tuple(r['summary']): [0, 0] for r in result['summary_rows']}
        for y in range(1 << rec['original_variables']):
            x = apply(rec['full_coordinate_columns'], y)
            bit = int(phase(set(rec['raw_polynomial']), x) == -1)
            oracle[summary_at(U, y)][bit] += 1
            checked += 1
        for row in result['summary_rows']:
            assert oracle[tuple(row['summary'])] == [row['zeros'], row['ones']]
            assert row['errors'] == min(row['zeros'], row['ones'])
            fiber_checks += 1
        results.append(result)
    return dict(status='all exact assertions passed', source_program=program_record,
                exact_original_input_label_checks=checked, exact_labeled_fibers=fiber_checks,
                classifiers=results, asymptotic_phase_engine_executed=False,
                claim='Optimal only among Boolean functions of the acquired Z4 summaries.')


if __name__ == '__main__':
    out = test()
    Path(__file__).with_name('summary_synthesis_results.json').write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps({k: v for k, v in out.items() if k not in ['source_program', 'classifiers']}, indent=2))
    print(json.dumps({k: v for k, v in out['source_program'].items() if k != 'instructions_program'}))
    for r in out['classifiers']:
        print(json.dumps({k: v for k, v in r.items() if k != 'summary_rows'}))
