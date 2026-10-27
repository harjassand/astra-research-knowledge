#!/usr/bin/env python3
"""Acquire sparse dual relations from raw affine/phase programs.

The compiler and projector are executable. The finite counter enumerates
assignments; it is NOT the subexponential replacement counter. Python 3.12,
standard library only. Run this file for exact reproducible validation.
"""
from collections import defaultdict
from itertools import combinations
from math import comb
from pathlib import Path
import json
import random


def parity(x):
    return x.bit_count() & 1


def add_independent(basis, value):
    x = value
    while x:
        p = x.bit_length() - 1
        if p in basis:
            x ^= basis[p]
        else:
            basis[p] = x
            return True
    return False


def dual_generators(rows):
    """Return rank(A) and a basis of ker(A^T), retaining certificates."""
    basis, relations = {}, []
    for i, row in enumerate(rows):
        value, certificate = row, 1 << i
        while value:
            p = value.bit_length() - 1
            if p in basis:
                old, old_cert = basis[p]
                value ^= old
                certificate ^= old_cert
            else:
                basis[p] = value, certificate
                break
        else:
            relations.append(certificate)
    return len(basis), relations


def acquire_dual(rows, offset, cutoff):
    r = len(rows)
    rank, full = dual_generators(rows)
    span, short = {}, []
    examined = 0
    # Retain ORIGINAL short rows, not their possibly dense row reductions.
    # Increasing weight is the linear-matroid greedy minimum-weight basis.
    for size in range(1, min(cutoff, r) + 1):
        for subset in combinations(range(r), size):
            examined += 1
            value = relation = 0
            for i in subset:
                value ^= rows[i]
                relation |= 1 << i
            if value == 0 and add_independent(span, relation):
                short.append(relation)
    remaining = []
    for h in full:
        if add_independent(span, h):
            remaining.append(h)
    assert len(short) + len(remaining) == r - rank
    return {
        'rank': rank, 'short': short, 'remaining': remaining,
        'short_rhs': [parity(h & offset) for h in short],
        'remaining_rhs': [parity(h & offset) for h in remaining],
        'short_total_weight': sum(h.bit_count() for h in short),
        'examined_subsets': examined,
    }


def compile_raw(spec):
    """Collapse raw XOR/NOT states and list the actual distinct phase inputs."""
    n, b = spec['inputs'], spec['phase_bits']
    q = 1 << b
    wires = [(1 << i, 0) for i in range(n)]
    forms, form_index = [], {}
    phase = defaultdict(int)
    for gate in spec['instructions']:
        op = gate['op']
        args = gate.get('args', [])
        if any(i < 0 or i >= len(wires) for i in args):
            raise ValueError('invalid affine source index')
        if op == 'xor':
            row = offset = 0
            for i in args:
                row ^= wires[i][0]
                offset ^= wires[i][1]
            wires.append((row, offset))
        elif op == 'not':
            if len(args) != 1:
                raise ValueError('not arity')
            row, offset = wires[args[0]]
            wires.append((row, offset ^ 1))
        elif op in ('phase', 'table'):
            loc = []
            for i in args:
                form = wires[i]
                if form not in form_index:
                    form_index[form] = len(forms)
                    forms.append(form)
                loc.append(form_index[form])
            if op == 'phase':
                mask = 0
                for i in loc:
                    mask |= 1 << i
                phase[mask] += gate['coefficient']
            else:
                table = list(gate['values'])
                if len(table) != 1 << len(loc):
                    raise ValueError('table length')
                for j in range(len(loc)):
                    for mask in range(len(table)):
                        if mask >> j & 1:
                            table[mask] -= table[mask ^ (1 << j)]
                for mask, coefficient in enumerate(table):
                    support = 0
                    for j, i in enumerate(loc):
                        if mask >> j & 1:
                            support |= 1 << i
                    phase[support] += coefficient
        else:
            raise ValueError('unknown instruction')
    return {
        'inputs': n, 'phase_bits': b,
        'rows': [row for row, _ in forms],
        'offset': sum(c << i for i, (_, c) in enumerate(forms)),
        'terms': [(s, c % q) for s, c in phase.items() if c % q],
        'raw_instructions': len(spec['instructions']),
        'affine_states': len(wires) - n,
    }


def phase_coordinate(exponent, b):
    d = 1 << (b - 1)
    exponent %= 2 * d
    out = [0] * d
    out[exponent % d] = 1 if exponent < d else -1
    return out


def finite_phase_sum(variables, terms, b):
    out = [0] * (1 << (b - 1))
    for x in range(1 << variables):
        exponent = sum(c for mask, c in terms if x & mask == mask)
        for j, v in enumerate(phase_coordinate(exponent, b)):
            out[j] += v
    return out


def original_sum(spec):
    out = [0] * (1 << (spec['phase_bits'] - 1))
    for x in range(1 << spec['inputs']):
        wires = [(x >> i) & 1 for i in range(spec['inputs'])]
        exponent = 0
        for gate in spec['instructions']:
            args = [wires[i] for i in gate.get('args', [])]
            op = gate['op']
            if op == 'xor':
                wires.append(sum(args) & 1)
            elif op == 'not':
                wires.append(args[0] ^ 1)
            elif op == 'phase':
                exponent += gate['coefficient'] * int(all(args))
            elif op == 'table':
                index = sum(value << j for j, value in enumerate(args))
                exponent += gate['values'][index]
        for j, v in enumerate(phase_coordinate(exponent, spec['phase_bits'])):
            out[j] += v
    return out


def compile_characters(compiled, cutoff):
    rows, offset = compiled['rows'], compiled['offset']
    r, q = len(rows), 1 << compiled['phase_bits']
    dual = acquire_dual(rows, offset, cutoff)
    common = list(compiled['terms'])
    for j, h in enumerate(dual['short']):
        lam = 1 << (r + j)
        for i in range(r):
            if h >> i & 1:
                common.append((lam | (1 << i), q // 2))
        if parity(h & offset):
            common.append((lam, q // 2))
    return dual, common


def finite_compiled_sum(compiled, cutoff):
    dual, common = compile_characters(compiled, cutoff)
    r, b = len(compiled['rows']), compiled['phase_bits']
    variables = r + len(dual['short'])
    total = [0] * (1 << (b - 1))
    for eta in range(1 << len(dual['remaining'])):
        combined = 0
        for j, h in enumerate(dual['remaining']):
            if eta >> j & 1:
                combined ^= h
        terms = common + [(1 << i, 1 << (b - 1)) for i in range(r)
                          if combined >> i & 1]
        if parity(combined & compiled['offset']):
            terms.append((0, 1 << (b - 1)))
        value = finite_phase_sum(variables, terms, b)
        # The actual asymptotic counter reconstructs this inner sum exactly
        # at N+2 modular bits BEFORE any projector/fiber normalization.
        for j, v in enumerate(value):
            total[j] += v
    exponent = compiled['inputs'] - r
    if exponent >= 0:
        result = [v << exponent for v in total]
    else:
        divisor = 1 << (-exponent)
        assert all(v % divisor == 0 for v in total)
        result = [v // divisor for v in total]
    return result, dual, variables


def random_basis(n, rng):
    span, result = {}, []
    while len(result) < n:
        value = rng.randrange(1, 1 << n)
        if add_independent(span, value):
            result.append(value)
    return result


def fixture(n, b, structured, rng):
    basis = random_basis(n, rng)
    rows = list(basis)
    extra = (n + 1) // 2
    if structured:
        pairs = list(combinations(range(n), 2))
        rng.shuffle(pairs)
        rows += [basis[i] ^ basis[j] for i, j in pairs[:extra]]
    else:
        rows += [rng.randrange(1, 1 << n) for _ in range(extra)]
    rng.shuffle(rows)
    offsets = [rng.randrange(2) for _ in rows]
    instructions, endpoints, wire_count = [], [], n
    for row, c in zip(rows, offsets):
        bits = [i for i in range(n) if row >> i & 1]
        last = bits[0]
        for i in bits[1:]:
            instructions.append({'op': 'xor', 'args': [last, i]})
            last = wire_count
            wire_count += 1
        if c:
            instructions.append({'op': 'not', 'args': [last]})
            last = wire_count
            wire_count += 1
        endpoints.append(last)
    for endpoint in endpoints:
        instructions.append({'op': 'phase', 'args': [endpoint],
                             'coefficient': rng.randrange(1, 1 << b)})
    for j in range(len(endpoints)):
        args = rng.sample(endpoints, min(3, len(endpoints)))
        if j & 1:
            instructions.append({'op': 'table', 'args': args,
                                 'values': [rng.randrange(1 << b) for _ in range(1 << len(args))]})
        else:
            instructions.append({'op': 'phase', 'args': args,
                                 'coefficient': rng.randrange(1, 1 << b)})
    return {'inputs': n, 'phase_bits': b, 'instructions': instructions}


def validate():
    rng = random.Random(2710202603)
    records = []
    total_original = total_compiled = nonzero_rhs = 0
    for n in (3, 4, 5):
        for b in (1, 2, 3):
            for structured in (False, True):
                spec = fixture(n, b, structured, rng)
                compiled = compile_raw(spec)
                expected = original_sum(spec)
                for cutoff in (0, 3):
                    value, dual, variables = finite_compiled_sum(compiled, cutoff)
                    assert value == expected
                    r = len(compiled['rows'])
                    assert dual['examined_subsets'] == sum(comb(r, j) for j in range(1, min(cutoff, r) + 1))
                    total_compiled += 1 << (variables + len(dual['remaining']))
                    nonzero_rhs += sum(dual['short_rhs'])
                    records.append(dict(inputs=n, order=1 << b, structured=structured,
                                        forms=r, cutoff=cutoff,
                                        affine_states=compiled['affine_states'],
                                        short_rank=len(dual['short']), residual_rank=len(dual['remaining']),
                                        short_weight=dual['short_total_weight'],
                                        monomials=len(compiled['terms']), exact_sum=value))
                total_original += 1 << n
    # The complement relation has RHS 1 and must not be discarded.
    relation = acquire_dual([1, 1], 2, 2)
    assert relation['short'] == [3] and relation['short_rhs'] == [1]
    # Zero-linear-row constants are weight-one affine relations.
    relation = acquire_dual([0, 0], 2, 1)
    assert len(relation['short']) == 2 and relation['short_rhs'] == [0, 1]
    empty = {'inputs': 4, 'phase_bits': 3, 'instructions': [
        {'op': 'phase', 'args': [], 'coefficient': 3}]}
    assert finite_compiled_sum(compile_raw(empty), 2)[0] == original_sum(empty)
    large = []
    for structured in (True, False):
        spec = fixture(64, 3, structured, rng)
        compiled = compile_raw(spec)
        dual, common = compile_characters(compiled, 3)
        if structured:
            assert not dual['remaining']
        else:
            assert not dual['short']
        large.append(dict(inputs=64, structured=structured,
                          forms=len(compiled['rows']), raw_instructions=compiled['raw_instructions'],
                          affine_states=compiled['affine_states'],
                          raw_matrix_ones=sum(row.bit_count() for row in compiled['rows']),
                          short_rank=len(dual['short']), residual_rank=len(dual['remaining']),
                          short_weight=dual['short_total_weight'],
                          examined_subsets=dual['examined_subsets'],
                          compiled_phase_terms=len(common),
                          phase_evaluation_executed=False))
    return dict(status='all exact assertions passed', seed=2710202603,
                raw_programs=18, projector_count_checks=len(records),
                original_assignments=total_original, compiled_phase_assignments=total_compiled,
                nonzero_short_rhs_checks=nonzero_rhs, boundary_checks=3,
                fixtures=records, larger_compilation_only=large,
                backend='exhaustive finite counts; asymptotic counter not implemented')


if __name__ == '__main__':
    result = validate()
    path = Path(__file__).with_name('affine_phase_results.json')
    path.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k not in ('fixtures',)}))
