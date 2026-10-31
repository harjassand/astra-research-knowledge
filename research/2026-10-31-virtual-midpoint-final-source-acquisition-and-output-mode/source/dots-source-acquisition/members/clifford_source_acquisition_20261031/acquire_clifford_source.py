"""Exact certificate finder for Clifford-dilation source channels.

Input: n source qubits, env zero-initialized qubits, a Clifford gate list;
keep the first n outputs and discard the environment outputs.
No density matrix, supplied return horizon or supplied fixed state is used.
This is a research prototype, not a full quantum simulation compiler.
"""
import argparse
import hashlib
import json
from pathlib import Path

OPS = {'H': 1, 'S': 1, 'SDG': 1, 'X': 1, 'Z': 1, 'CX': 2, 'SWAP': 2}


def validate(program):
    if not isinstance(program, dict) or not all(k in program for k in ('n', 'env', 'gates')) or not isinstance(program['gates'], list):
        raise ValueError('Require a program mapping with n, env and a gate list.')
    n, e = program['n'], program['env']
    if type(n) is not int or type(e) is not int or n < 1 or e < 0:
        raise ValueError('Require n>=1 source qubits and env>=0.')
    for gate in program['gates']:
        if not isinstance(gate, list) or not gate or not isinstance(gate[0], str) or gate[0] not in OPS:
            raise ValueError('Unsupported gate.')
        if len(gate) != OPS[gate[0]] + 1:
            raise ValueError('Incorrect gate arity.')
        if any(type(q) is not int or not 0 <= q < n+e for q in gate[1:]):
            raise ValueError('Invalid qubit index.')
        if len(set(gate[1:])) != len(gate[1:]):
            raise ValueError('Repeated qubit in gate.')


def digest(program):
    return hashlib.sha256(json.dumps(program, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def inverse_gates(gates):
    inv = {'S': 'SDG', 'SDG': 'S'}
    return [[inv.get(g[0], g[0]), *g[1:]] for g in reversed(gates)]


def multiply(a, b):
    """Paulis are i**phase X**x Z**z, with bit-mask exponents."""
    p, x, z = a
    q, u, v = b
    return ((p+q+2*(z & u).bit_count()) % 4, x ^ u, z ^ v)


def conjugate_gate(pauli, gate):
    p, x, z = pauli
    op, i = gate[:2]
    xb, zb = (x >> i) & 1, (z >> i) & 1
    if op == 'H':
        p += 2*xb*zb
        if xb != zb:
            x ^= 1 << i
            z ^= 1 << i
    elif op in ('S', 'SDG'):
        p += xb * (1 if op == 'S' else 3)
        if xb:
            z ^= 1 << i
    elif op == 'X':
        p += 2*zb
    elif op == 'Z':
        p += 2*xb
    elif op == 'CX':
        j = gate[2]
        if xb:
            x ^= 1 << j
        if (z >> j) & 1:
            z ^= 1 << i
    elif op == 'SWAP':
        j = gate[2]
        if ((x >> i) ^ (x >> j)) & 1:
            x ^= (1 << i) | (1 << j)
        if ((z >> i) ^ (z >> j)) & 1:
            z ^= (1 << i) | (1 << j)
    return (p % 4, x, z)


def conjugate(pauli, gates):
    for gate in gates:
        pauli = conjugate_gate(pauli, gate)
    return pauli


def basis(vectors):
    pivots = {}
    for v in vectors:
        while v:
            j = v.bit_length()-1
            if j in pivots:
                v ^= pivots[j]
            else:
                pivots[j] = v
                break
    for j in sorted(pivots):
        for k in sorted(pivots):
            if k > j and ((pivots[k] >> j) & 1):
                pivots[k] ^= pivots[j]
    return [pivots[j] for j in sorted(pivots, reverse=True)]


def linear(columns, coefficients):
    answer = 0
    while coefficients:
        bit = coefficients & -coefficients
        answer ^= columns[bit.bit_length()-1]
        coefficients ^= bit
    return answer


def kernel_columns(columns):
    pivots, relations = {}, []
    for i, value in enumerate(columns):
        tag = 1 << i
        while value:
            j = value.bit_length()-1
            if j in pivots:
                old, oldtag = pivots[j]
                value ^= old
                tag ^= oldtag
            else:
                pivots[j] = (value, tag)
                break
        if not value:
            relations.append(tag)
    return basis(relations)


def canonical_stabilizers(generators, n):
    pivots = {}
    for raw in generators:
        row = tuple(raw)
        value = row[1] | (row[2] << n)
        while value:
            j = value.bit_length()-1
            if j in pivots:
                row = multiply(row, pivots[j])
                value = row[1] | (row[2] << n)
            else:
                pivots[j] = row
                break
        if not value and row[0] != 0:
            raise ValueError('Inconsistent stabilizer group.')
    for j in sorted(pivots):
        for k in sorted(pivots):
            value = pivots[k][1] | (pivots[k][2] << n)
            if k > j and ((value >> j) & 1):
                pivots[k] = multiply(pivots[k], pivots[j])
    return [pivots[j] for j in sorted(pivots, reverse=True)]


def channel_stabilizers(generators, program):
    """Propagate a mixed stabilizer state, then take the environment trace."""
    n, e = program['n'], program['env']
    mask = (1 << n)-1
    joint = [tuple(g) for g in generators] + [(0, 0, 1 << (n+j)) for j in range(e)]
    joint = [conjugate(g, program['gates']) for g in joint]
    environment_columns = [(x >> n) | ((z >> n) << e) for _, x, z in joint]
    result = []
    for relation in kernel_columns(environment_columns):
        row = (0, 0, 0)
        for i, g in enumerate(joint):
            if (relation >> i) & 1:
                row = multiply(row, g)
        assert (row[1] >> n) == (row[2] >> n) == 0
        result.append((row[0], row[1] & mask, row[2] & mask))
    return canonical_stabilizers(result, n)


def pauli_maps(program):
    n = program['n']
    mask = (1 << n)-1
    inverse = inverse_gates(program['gates'])
    f, constraints = [], []
    for j in range(2*n):
        row = (0, 1 << j, 0) if j < n else (0, 0, 1 << (j-n))
        _, x, z = conjugate(row, inverse)
        f.append((x & mask) | ((z & mask) << n))
        constraints.append(x >> n)
    return f, constraints


def image_step(current, f, constraints):
    restricted = [linear(constraints, v) for v in current]
    intersection = [linear(current, r) for r in kernel_columns(restricted)]
    return basis([linear(f, v) for v in intersection])


def prepare_stabilizer(generators, n):
    """Return a Clifford preparation circuit, with its actual circuit phase."""
    rows = canonical_stabilizers(generators, n)
    if len(rows) != n:
        raise ValueError('The stabilizer state is not pure.')
    reduction = []

    def apply(gate):
        nonlocal rows
        reduction.append(gate)
        rows = [conjugate_gate(row, gate) for row in rows]

    for i in range(n):
        support = rows[i][1] | rows[i][2]
        j = next(j for j in range(i, n) if (support >> j) & 1)
        if i != j:
            apply(['SWAP', i, j])
        for j in range(i, n):
            x, z = (rows[i][1] >> j) & 1, (rows[i][2] >> j) & 1
            if x and z:
                apply(['SDG', j])
                apply(['H', j])
            elif x:
                apply(['H', j])
        for j in range(i+1, n):
            if (rows[i][2] >> j) & 1:
                apply(['CX', j, i])
        assert rows[i][1:] == (0, 1 << i)
        if rows[i][0] == 2:
            apply(['X', i])
        assert rows[i] == (0, 0, 1 << i)
        for j in range(i+1, n):
            assert not ((rows[j][1] >> i) & 1)
            if (rows[j][2] >> i) & 1:
                rows[j] = multiply(rows[j], rows[i])
    return inverse_gates(reduction)


def preparation_stabilizers(gates, n):
    return canonical_stabilizers([conjugate((0, 0, 1 << j), gates) for j in range(n)], n)


def acquire(program):
    validate(program)
    n = program['n']
    f, constraints = pauli_maps(program)
    current = basis([1 << j for j in range(2*n)])
    result = {'source_digest': digest(program), 'n': n, 'env': program['env'],
              'source_map': f, 'survival_constraints': constraints, 'filtration': [current]}
    for step in range(1, 2*n+1):
        following = image_step(current, f, constraints)
        assert basis(current+following) == current
        result['filtration'].append(following)
        if not following:
            result['horizon'] = step
            state = []  # Maximally mixed source, not a guessed pure initial state.
            for _ in range(step):
                state = channel_stabilizers(state, program)
            result['constant_state_stabilizers'] = [list(g) for g in state]
            result['constant_state_rank_log2'] = n-len(state)
            if len(state) != n:
                result['status'] = 'mixed_reset'
                return result
            prep = prepare_stabilizer(state, n)
            assert preparation_stabilizers(prep, n) == state
            assert channel_stabilizers(state, program) == state
            result['status'] = 'accepted_pure_return'
            result['psi_preparation'] = prep
            # DO NOT synthesize c from only a stabilizer ray: this exact template
            # preserves the phase relative to the actual acquired source U.
            result['c_preparation_with_clean_source_work'] = prep + program['gates'] + inverse_gates(prep)
            return result
        if following == current:
            result['status'] = 'persistent_pauli'
            result['stabilization_step'] = step
            return result
        current = following
    raise AssertionError('Finite-dimensional image filtration did not terminate.')


def verify(program, certificate):
    """Exact gate/algebra verification; no dense state table or circuit execution."""
    try:
        if not isinstance(certificate, dict):
            return False
        validate(program)
        n = program['n']
        if certificate.get('n') != n or certificate.get('env') != program['env']:
            return False
        if certificate['source_digest'] != digest(program):
            return False
        f, constraints = pauli_maps(program)
        if certificate['source_map'] != f or certificate['survival_constraints'] != constraints:
            return False
        chain = certificate['filtration']
        if not 2 <= len(chain) <= 2*n+1:
            return False
        if any(not isinstance(row, list) or len(row) > 2*n or any(type(v) is not int or not 0 <= v < (1 << (2*n)) for v in row) for row in chain):
            return False
        if any(row != basis(row) for row in chain):
            return False
        if basis(chain[0]) != basis([1 << j for j in range(2*n)]):
            return False
        for before, after in zip(chain, chain[1:]):
            if basis(after) != image_step(basis(before), f, constraints):
                return False
        status = certificate['status']
        if status == 'persistent_pauli':
            return certificate.get('stabilization_step') == len(chain)-1 and bool(basis(chain[-1])) and basis(chain[-1]) == basis(chain[-2])
        if chain[-1] or certificate['horizon'] != len(chain)-1:
            return False
        if status == 'mixed_reset':
            state = []
            for _ in range(certificate['horizon']):
                state = channel_stabilizers(state, program)
            return len(state) < n and certificate.get('constant_state_rank_log2') == n-len(state) and [list(g) for g in state] == certificate['constant_state_stabilizers']
        if status != 'accepted_pure_return':
            return False
        prep = certificate['psi_preparation']
        validate({'n': n, 'env': 0, 'gates': prep})
        state = preparation_stabilizers(prep, n)
        if certificate.get('constant_state_rank_log2') != 0 or certificate.get('constant_state_stabilizers') != [list(g) for g in state]:
            return False
        if channel_stabilizers(state, program) != state:
            return False
        expected_c = prep + program['gates'] + inverse_gates(prep)
        return certificate['c_preparation_with_clean_source_work'] == expected_c
    except (KeyError, ValueError, TypeError, IndexError, AssertionError, StopIteration):
        return False


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('program', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    program = json.loads(args.program.read_text())
    result = acquire(program)
    if not verify(program, result):
        raise RuntimeError('Generated certificate failed exact verification.')
    output = json.dumps(result, indent=2)+'\n'
    if args.output:
        args.output.write_text(output)
    else:
        print(output, end='')


if __name__ == '__main__':
    main()
