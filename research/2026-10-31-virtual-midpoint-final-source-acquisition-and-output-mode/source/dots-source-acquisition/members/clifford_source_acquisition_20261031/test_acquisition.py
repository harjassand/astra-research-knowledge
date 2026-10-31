"""Independent small dense-matrix checks of the exact GF(2) frontend.
NumPy is used only here, never by the certificate finder/verifier.
"""
import copy
import json
import random
from pathlib import Path
import numpy as np
from acquire_clifford_source import (acquire, verify, conjugate, inverse_gates,
                                    linear, validate)


def pauli_matrix(p, x, z, q):
    out = np.zeros((1 << q, 1 << q), complex)
    for col in range(1 << q):
        out[col ^ x, col] = (1j ** p) * ((-1) ** ((z & col).bit_count()))
    return out


def gate_matrix(gate, q):
    op, i = gate[:2]
    dim = 1 << q
    out = np.zeros((dim, dim), complex)
    for col in range(dim):
        bit = (col >> i) & 1
        if op == 'H':
            out[col & ~(1 << i), col] = 1/np.sqrt(2)
            out[col | (1 << i), col] = (-1 if bit else 1)/np.sqrt(2)
        elif op in ('S', 'SDG'):
            out[col, col] = (1j if op == 'S' else -1j) ** bit
        elif op == 'Z':
            out[col, col] = (-1) ** bit
        elif op == 'X':
            out[col ^ (1 << i), col] = 1
        elif op == 'CX':
            out[col ^ ((1 << gate[2]) if bit else 0), col] = 1
        elif op == 'SWAP':
            j = gate[2]
            row = col ^ (((1 << i) | (1 << j)) if bit != ((col >> j) & 1) else 0)
            out[row, col] = 1
    return out


def unitary(gates, q):
    answer = np.eye(1 << q, dtype=complex)
    for gate in gates:
        answer = gate_matrix(gate, q) @ answer
    return answer


def history(n):
    return {'n': n, 'env': 1,
            'gates': [['H', n]] + [['SWAP', j, j+1] for j in range(n)]}


def dense_check(program):
    cert = acquire(program)
    assert verify(program, cert)
    n, e = program['n'], program['env']
    d = 1 << n
    U = unitary(program['gates'], n+e)
    kraus = [U[j*d:(j+1)*d, :d] for j in range(1 << e)]
    superop = sum(np.kron(k.conj(), k) for k in kraus)
    # All source Paulis, including mixed-Y phases, checked independently.
    inv = inverse_gates(program['gates'])
    for v in range(1 << (2*n)):
        x, z = v & (d-1), v >> n
        p = (x & z).bit_count() % 4
        target = sum(k.conj().T @ pauli_matrix(p, x, z, n) @ k for k in kraus)
        pp, xx, zz = conjugate((p, x, z), inv)
        predicted = np.zeros_like(target) if (xx >> n) else pauli_matrix(pp, xx & (d-1), zz & (d-1), n)
        assert np.linalg.norm(target-predicted) < 1e-10
        if not (xx >> n):
            assert linear(cert['source_map'], v) == (xx & (d-1)) | ((zz & (d-1)) << n)
        assert linear(cert['survival_constraints'], v) == xx >> n
    if cert['status'] == 'persistent_pauli':
        for t in range(1, 2*n+4):
            power = np.linalg.matrix_power(superop, t)
            sigma = (power @ (np.eye(d)/d).reshape(-1, order='F')).reshape(d, d, order='F')
            reset = np.outer(sigma.reshape(-1, order='F'), np.eye(d).reshape(-1, order='F'))
            assert np.linalg.norm(power-reset) > .5
    else:
        power = np.linalg.matrix_power(superop, cert['horizon'])
        sigma = (power @ (np.eye(d)/d).reshape(-1, order='F')).reshape(d, d, order='F')
        reset = np.outer(sigma.reshape(-1, order='F'), np.eye(d).reshape(-1, order='F'))
        assert np.linalg.norm(power-reset) < 1e-10
        expected_rank = 1 << cert['constant_state_rank_log2']
        assert np.sum(np.linalg.eigvalsh(sigma) > 1e-8) == expected_rank
        if cert['status'] == 'accepted_pure_return':
            psi = unitary(cert['psi_preparation'], n)[:, 0]
            assert np.linalg.norm(sigma-np.outer(psi, psi.conj())) < 1e-10
            cp = unitary(cert['c_preparation_with_clean_source_work'], n+e)[:, 0].reshape(1 << e, d)
            c = cp[:, 0]
            assert np.linalg.norm(cp[:, 1:]) < 1e-10
            # This checks the RELATIVE GLOBAL PHASE, not only density matrices.
            assert np.linalg.norm(U[:, :d] @ psi - np.kron(c, psi)) < 1e-10
    return cert


def run():
    examples = {
        'reset_zero': {'n': 1, 'env': 1, 'gates': [['SWAP', 0, 1]]},
        'reset_plus_i': {'n': 1, 'env': 1, 'gates': [['H', 1], ['S', 1], ['SWAP', 0, 1]]},
        'reset_with_global_minus': {'n': 1, 'env': 1, 'gates': [['SWAP', 0, 1], ['Z', 0], ['X', 0], ['Z', 0], ['X', 0]]},
        'dephase_z_then_h': {'n': 1, 'env': 1, 'gates': [['CX', 0, 1], ['H', 0]]},
        'classical_reset_but_quantum_memory': {'n': 1, 'env': 1, 'gates': [['H', 1], ['CX', 1, 0]]},
        'unitary_only': {'n': 2, 'env': 0, 'gates': [['H', 0], ['CX', 0, 1], ['S', 1]]},
        'history_1': history(1), 'history_2': history(2), 'history_3': history(3),
    }
    records = {}
    for name, program in examples.items():
        cert = dense_check(program)
        records[name] = {'status': cert['status'], 'horizon': cert.get('horizon'),
                         'image_dimensions': [len(row) for row in cert['filtration']]}
    assert records['dephase_z_then_h']['status'] == 'mixed_reset'
    assert records['dephase_z_then_h']['horizon'] == 2
    assert records['classical_reset_but_quantum_memory']['status'] == 'persistent_pauli'
    for n in range(1, 4):
        assert records[f'history_{n}']['horizon'] == n
    rng = random.Random(20261031)
    histogram = {}
    for n, e in [(1, 1), (2, 1), (2, 2)]:
        for _ in range(60):
            gates = []
            for _ in range(18):
                op = rng.choice(['H', 'S', 'SDG', 'X', 'Z', 'CX', 'SWAP'])
                indices = rng.sample(range(n+e), 2 if op in ('CX', 'SWAP') else 1)
                gates.append([op, *indices])
            cert = dense_check({'n': n, 'env': e, 'gates': gates})
            histogram[cert['status']] = histogram.get(cert['status'], 0)+1
    # No dense matrices: hidden-coordinate history sources at larger n.
    large = []
    for n in [8, 16, 32, 64]:
        change = []
        for _ in range(5*n):
            op = rng.choice(['H', 'S', 'CX'])
            indices = rng.sample(range(n), 2 if op == 'CX' else 1)
            change.append([op, *indices])
        program = history(n)
        program['gates'] = inverse_gates(change) + program['gates'] + change
        cert = acquire(program)
        assert verify(program, cert) and cert['status'] == 'accepted_pure_return' and cert['horizon'] == n
        large.append({'n': n, 'source_gates': len(program['gates']), 'horizon': cert['horizon'],
                      'psi_preparation_gates': len(cert['psi_preparation']),
                      'maximum_binary_space_dimension': 2*n})
    p = examples['reset_with_global_minus']; c = acquire(p)
    bad = copy.deepcopy(c); bad['filtration'][0][0] = -1
    assert not verify(p, bad)
    bad = copy.deepcopy(c); bad['source_map'][0] ^= 1
    assert not verify(p, bad)
    bad = copy.deepcopy(c); bad['horizon'] += 1
    assert not verify(p, bad)
    bad = copy.deepcopy(c); bad['c_preparation_with_clean_source_work'].extend([['Z', 0], ['X', 0], ['Z', 0], ['X', 0]])
    assert not verify(p, bad)
    bad = copy.deepcopy(c); bad['constant_state_rank_log2'] = 1
    assert not verify(p, bad)
    for malformed in [None, [], 0, 'x']:
        assert not verify(p, malformed)
    reset_program = examples['reset_zero']
    forged = acquire(reset_program)
    forged['filtration'] = [forged['filtration'][0], [0], [0]]
    forged['status'] = 'persistent_pauli'
    forged['stabilization_step'] = 2
    assert not verify(reset_program, forged)
    forged = acquire(reset_program)
    forged['filtration'][0].append(forged['filtration'][0][0])
    assert not verify(reset_program, forged)
    for invalid in [ {'n': 0, 'env': 1, 'gates': []}, {'n': 1, 'env': 0, 'gates': [['H', 1]]}, {'n': 1, 'env': 0, 'gates': [['EXEC', 'anything']]} ]:
        try:
            validate(invalid)
            raise AssertionError('Invalid input accepted.')
        except ValueError:
            pass
    result = {'scope': 'certificate-finder prototype; not a full simulator or unknown-source learner',
              'named_dense_checks': records, 'random_dense_cases': 180, 'random_status_histogram': histogram,
              'large_symbolic_cases': large, 'tamper_checks': 7, 'malformed_certificate_checks': 4, 'invalid_program_checks': 3, 'passed': True}
    path = Path(__file__).with_name('acquisition_checks.json')
    path.write_text(json.dumps(result, indent=2)+'\n')
    example_dir = Path(__file__).with_name('examples'); example_dir.mkdir(exist_ok=True)
    for name in ['history_3', 'reset_with_global_minus', 'dephase_z_then_h', 'classical_reset_but_quantum_memory']:
        program = examples[name]
        (example_dir/(name+'.json')).write_text(json.dumps(program, indent=2)+'\n')
        (example_dir/(name+'.certificate.json')).write_text(json.dumps(acquire(program), indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    run()
