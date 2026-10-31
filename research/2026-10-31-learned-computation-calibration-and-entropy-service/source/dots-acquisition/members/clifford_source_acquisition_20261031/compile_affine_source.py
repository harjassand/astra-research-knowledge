"""Law-preserving quantum realization of a controllable GF(2) source.

The input is a CLASSICAL update x' = F x + G r + offset with fresh fair r.
Only its state-label process and admitted diagonal-algebra consumers are
preserved. An arbitrary original quantum dilation or public coin record is
not preserved. This emits a Clifford program/certificate, not a simulator.
"""
import argparse
import json
from pathlib import Path
from acquire_clifford_source import (acquire, verify, validate as validate_clifford,
                                    digest, basis, linear, kernel_columns)


def validate_affine(raw):
    required = {'n', 'F_columns', 'G_columns', 'offset'}
    if not isinstance(raw, dict) or set(raw) != required:
        raise ValueError('Require exactly n, F_columns, G_columns and offset.')
    n = raw['n']
    if type(n) is not int or n < 1:
        raise ValueError('Require n>=1.')
    if not isinstance(raw['F_columns'], list) or len(raw['F_columns']) != n or not isinstance(raw['G_columns'], list):
        raise ValueError('F must have n columns; G must be a column list.')
    if any(type(x) is not int or not 0 <= x < (1 << n) for x in [*raw['F_columns'], *raw['G_columns'], raw['offset']]):
        raise ValueError('Matrix columns and offset must be n-bit integer masks.')


def multiply_matrix(a, b):
    return [linear(a, column) for column in b]


def power_matrix(a, exponent):
    result = [1 << j for j in range(len(a))]
    while exponent:
        if exponent & 1:
            result = multiply_matrix(a, result)
        a = multiply_matrix(a, a)
        exponent >>= 1
    return result


def solver_table(columns):
    pivots = {}
    for j, value in enumerate(columns):
        tag = 1 << j
        while value:
            k = value.bit_length()-1
            if k in pivots:
                v, t = pivots[k]
                value ^= v
                tag ^= t
            else:
                pivots[k] = (value, tag)
                break
    return pivots


def solve(table, value):
    solution = 0
    while value:
        k = value.bit_length()-1
        if k not in table:
            raise ValueError('Linear equation has no solution.')
        v, t = table[k]
        value ^= v
        solution ^= t
    return solution


def inverse_matrix(columns):
    n = len(columns)
    table = solver_table(columns)
    if len(table) != n:
        raise ValueError('Matrix is singular.')
    return [solve(table, 1 << j) for j in range(n)]


def transpose_columns(columns, rows):
    return [sum(((column >> i) & 1) << j for j, column in enumerate(columns)) for i in range(rows)]


def controllable_space(f, noise, n):
    current, layer = [], basis(noise)
    for _ in range(n):
        current = basis(current+layer)
        layer = [linear(f, x) for x in layer]
    return current


def nilpotence_index(a):
    current = [1 << j for j in range(len(a))]
    for k in range(1, len(a)+1):
        current = multiply_matrix(a, current)
        if not any(current):
            return k
    return None


def deadbeat_section(a0, fibres):
    """Exact greedy cyclic feedback; output is verified by nilpotence."""
    n = len(a0)
    if nilpotence_index(a0) is not None:
        return list(a0), 'already_nilpotent_section'
    if len(controllable_space(a0, fibres, n)) != n:
        raise ValueError('Reverse fibre pair is not controllable.')
    chain = [fibres[0]]
    controls = []
    for _ in range(n-1):
        span = basis(chain)
        image = linear(a0, chain[-1])
        chosen = None
        for u in [0]+[1 << j for j in range(len(fibres))]:
            candidate = image ^ linear(fibres, u)
            if len(basis(span+[candidate])) > len(span):
                chosen = (u, candidate)
                break
        if chosen is None:
            raise AssertionError('Controllability failed to extend the cyclic chain.')
        u, candidate = chosen
        controls.append(u)
        chain.append(candidate)
    controls.append(0)
    tinv = inverse_matrix(chain)
    l0 = multiply_matrix(controls, tinv)
    a1 = [x ^ y for x, y in zip(a0, multiply_matrix(fibres, l0))]
    v = fibres[0]
    for expected in chain:
        assert v == expected
        v = linear(a1, v)
    transform = multiply_matrix(tinv, power_matrix(a1, n))
    krow = sum(((column >> (n-1)) & 1) << j for j, column in enumerate(transform))
    feedback = [column ^ ((krow >> j) & 1) for j, column in enumerate(l0)]
    answer = [x ^ y for x, y in zip(a0, multiply_matrix(fibres, feedback))]
    assert not any(power_matrix(answer, n))
    return answer, 'cyclic_feedback_then_deadbeat'


def complete_rows(rows, size):
    completed = list(rows)
    span = basis(completed)
    if len(span) != len(rows):
        raise ValueError('Initial rows are dependent.')
    for j in range(size):
        if len(span) == size:
            break
        candidate = 1 << j
        new = basis(span+[candidate])
        if len(new) > len(span):
            completed.append(candidate)
            span = new
    if len(completed) != size:
        raise AssertionError('Invertible completion failed.')
    return completed


def linear_gate_program(columns):
    """Gaussian row reduction, reversed, implements the requested map."""
    size = len(columns)
    rows = transpose_columns(columns, size)
    reduction = []
    for col in range(size):
        pivot = next(j for j in range(col, size) if (rows[j] >> col) & 1)
        if pivot != col:
            rows[pivot], rows[col] = rows[col], rows[pivot]
            reduction.append(['SWAP', pivot, col])
        for target in range(size):
            if target != col and ((rows[target] >> col) & 1):
                rows[target] ^= rows[col]
                reduction.append(['CX', col, target])
    assert rows == [1 << j for j in range(size)]
    return list(reversed(reduction))


def affine_action(program, fresh_bits):
    """Extract actual classical permutation after the mandated fair-bit prep."""
    validate_clifford(program)
    n, e = program['n'], program['env']
    if e != fresh_bits:
        raise ValueError('Incorrect fresh-bit count.')
    prefix = [['H', n+j] for j in range(e)]
    if program['gates'][:e] != prefix:
        raise ValueError('The explicit fresh-fair preparation prefix is missing.')
    size = n+e
    columns = [1 << j for j in range(size)]
    offset = 0
    for gate in program['gates'][e:]:
        op, i = gate[:2]
        if op == 'X':
            offset ^= 1 << i
        elif op == 'CX':
            target = gate[2]
            columns = [x ^ ((1 << target) if ((x >> i) & 1) else 0) for x in columns]
            if (offset >> i) & 1:
                offset ^= 1 << target
        elif op == 'SWAP':
            target = gate[2]
            def swap(x):
                return x ^ (((1 << i) | (1 << target)) if (((x >> i) ^ (x >> target)) & 1) else 0)
            columns = [swap(x) for x in columns]
            offset = swap(offset)
        else:
            raise ValueError('Only affine reversible gates may follow fair-bit preparation.')
    return columns, offset


def compile_affine(raw):
    validate_affine(raw)
    n, f, g, bias = raw['n'], raw['F_columns'], raw['G_columns'], raw['offset']
    reachable = controllable_space(f, g, n)
    result = {'input_digest': digest(raw), 'n': n, 'reachable_basis': reachable,
              'equivalence_scope': 'classical state-label process and outcome-retaining diagonal algebra only',
              'original_coin_records_preserved': False, 'arbitrary_original_quantum_dilation_preserved': False}
    if len(reachable) != n:
        result['status'] = 'outside_controllable_uniform_class'
        return result
    noise = basis(g)
    rank = len(noise)
    # Rows of the quotient annihilate im(G); transpose for column arithmetic.
    annihilator = kernel_columns(transpose_columns(noise, n))
    quotient = transpose_columns(annihilator, n)
    h = multiply_matrix(quotient, f)
    assert len(basis(h)) == n-rank
    table = solver_table(h)
    a0 = [solve(table, target) for target in quotient]
    fibres = kernel_columns(h)
    assert len(fibres) == rank
    a, method = deadbeat_section(a0, fibres)
    assert multiply_matrix(h, a) == quotient
    inverse_offset = linear(a, bias)
    top_rows = transpose_columns(a+fibres, n)
    inverse_rows = complete_rows(top_rows, n+rank)
    inverse_columns = transpose_columns(inverse_rows, n+rank)
    forward_columns = inverse_matrix(inverse_columns)
    gates = [['H', n+j] for j in range(rank)]
    gates += [['X', j] for j in range(n) if (inverse_offset >> j) & 1]
    gates += linear_gate_program(forward_columns)
    program = {'n': n, 'env': rank, 'gates': gates}
    source_certificate = acquire(program)
    assert source_certificate['status'] == 'accepted_pure_return'
    assert source_certificate['horizon'] <= n
    result.update({'status': 'synthesized_uniform_pure_return', 'noise_rank': rank,
                   'original_noise_bits': len(g), 'method': method,
                   'quotient_columns': quotient, 'reverse_constraint_columns': h,
                   'reverse_section_columns': a, 'reverse_fibre_columns': fibres,
                   'reverse_affine_offset': inverse_offset,
                   'nilpotence_horizon': nilpotence_index(a),
                   'source_program': program, 'source_certificate': source_certificate})
    if not verify_affine(raw, result):
        raise AssertionError('Synthesized law-preserving certificate failed verification.')
    return result


def verify_affine(raw, certificate):
    """Verify actual gate semantics, affine fibre law and pure-return proof."""
    try:
        validate_affine(raw)
        if not isinstance(certificate, dict) or certificate.get('input_digest') != digest(raw):
            return False
        if certificate.get('original_coin_records_preserved') is not False or certificate.get('arbitrary_original_quantum_dilation_preserved') is not False:
            return False
        if certificate.get('equivalence_scope') != 'classical state-label process and outcome-retaining diagonal algebra only':
            return False
        n = raw['n']
        if type(certificate.get('n')) is not int or certificate['n'] != n:
            return False
        reachable = controllable_space(raw['F_columns'], raw['G_columns'], n)
        if certificate.get('reachable_basis') != reachable:
            return False
        if certificate.get('status') == 'outside_controllable_uniform_class':
            return len(reachable) < n
        if certificate.get('status') != 'synthesized_uniform_pure_return' or len(reachable) != n:
            return False
        noise = basis(raw['G_columns']); rank = len(noise)
        if certificate.get('noise_rank') != rank or certificate.get('original_noise_bits') != len(raw['G_columns']):
            return False
        quotient = transpose_columns(kernel_columns(transpose_columns(noise, n)), n)
        h = multiply_matrix(quotient, raw['F_columns'])
        program = certificate['source_program']
        if program.get('n') != n:
            return False
        actual_columns, actual_offset = affine_action(program, rank)
        inv = inverse_matrix(actual_columns)
        mask = (1 << n)-1
        a = [column & mask for column in inv[:n]]
        fibres = [column & mask for column in inv[n:]]
        inv_offset = linear(inv, actual_offset) & mask
        if certificate.get('quotient_columns') != quotient or certificate.get('reverse_constraint_columns') != h:
            return False
        if certificate.get('reverse_section_columns') != a or certificate.get('reverse_fibre_columns') != fibres or certificate.get('reverse_affine_offset') != inv_offset:
            return False
        if multiply_matrix(h, a) != quotient or any(multiply_matrix(h, fibres)) or len(basis(fibres)) != rank:
            return False
        if linear(h, inv_offset) != linear(quotient, raw['offset']):
            return False
        horizon = nilpotence_index(a)
        if horizon is None or certificate.get('nilpotence_horizon') != horizon:
            return False
        # Independent forward-law check, not just the claimed inverse section.
        forward_f = [column & mask for column in actual_columns[:n]]
        forward_g = [column & mask for column in actual_columns[n:]]
        if basis(forward_g) != noise or multiply_matrix(quotient, forward_f) != multiply_matrix(quotient, raw['F_columns']):
            return False
        if linear(quotient, actual_offset & mask) != linear(quotient, raw['offset']):
            return False
        source_certificate = certificate['source_certificate']
        if not verify(program, source_certificate) or source_certificate.get('status') != 'accepted_pure_return' or source_certificate['horizon'] > n:
            return False
        # The constructed affine permutation fixes the all-plus vector exactly.
        expected_stabilizers = [[0, 1 << j, 0] for j in reversed(range(n))]
        return source_certificate['constant_state_stabilizers'] == expected_stabilizers
    except (KeyError, ValueError, TypeError, IndexError, AssertionError, StopIteration, AttributeError):
        return False


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('program', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = compile_affine(json.loads(args.program.read_text()))
    output = json.dumps(result, indent=2)+'\n'
    if args.output:
        args.output.write_text(output)
    else:
        print(output, end='')


if __name__ == '__main__':
    main()
