"""Small dense and larger symbolic tests of affine realization synthesis.
The acquisition code itself is standard-library-only; dense tests use NumPy.
"""
import copy
from itertools import product
import json
from pathlib import Path
import random
import numpy as np
from compile_affine_source import (compile_affine, verify_affine, validate_affine,
                                  controllable_space, multiply_matrix, inverse_matrix,
                                  linear, digest)
from acquire_clifford_source import acquire
from acquire_affine_pauli_consumer import acquire_classical_coupling
from test_acquisition import unitary


def dense_check(raw, result):
    assert verify_affine(raw, result)
    if result['status'] != 'synthesized_uniform_pure_return':
        return False
    n = raw['n']; program = result['source_program']; e = program['env']; d = 1 << n
    U = unitary(program['gates'], n+e)
    kraus = [U[j*d:(j+1)*d, :d] for j in range(1 << e)]
    P = np.zeros((d, d))
    for x in range(d):
        for coins in range(1 << len(raw['G_columns'])):
            y = linear(raw['F_columns'], x) ^ linear(raw['G_columns'], coins) ^ raw['offset']
            P[x, y] += 1/(1 << len(raw['G_columns']))
    Pquantum = sum(np.abs(k.T)**2 for k in kraus)
    assert np.max(np.abs(P-Pquantum)) < 1e-11
    assert np.linalg.norm(sum(k.conj().T@k for k in kraus)-np.eye(d)) < 1e-10
    psi = np.ones(d)/np.sqrt(d); c = np.ones(1 << e)/np.sqrt(1 << e)
    assert np.linalg.norm(U[:, :d]@psi-np.kron(c, psi)) < 1e-10
    words = [np.eye(d)]
    horizon = result['source_certificate']['horizon']
    assert e*horizon <= 14  # Explicitly bounded dense diagnostic only.
    for _ in range(horizon):
        words = [k@word for k in kraus for word in words]
    Q = np.eye(d)-np.outer(psi, psi)
    assert max(np.linalg.norm(Q@word) for word in words) < 1e-10
    assert np.linalg.norm(sum(word.conj().T@word for word in words)-np.eye(d)) < 1e-9
    return True


def run():
    total = accepted = rejected = 0; methods = {}; dense_cases = 0; admitted_dense_single = 0
    # Includes zero input columns, unlike the nonzero-input mathematical sample.
    for n in [1, 2, 3]:
        for f in product(range(1 << n), repeat=n):
            for g in range(1 << n):
                raw = {'n': n, 'F_columns': list(f), 'G_columns': [g], 'offset': 0}
                result = compile_affine(raw); total += 1
                assert verify_affine(raw, result)
                expected = len(controllable_space(list(f), [g], n)) == n
                assert (result['status'] == 'synthesized_uniform_pure_return') == expected
                if expected:
                    accepted += 1; methods[result['method']] = methods.get(result['method'], 0)+1
                else:
                    rejected += 1
                if total % 71 == 0 or n == 1:
                    admitted_dense_single += int(dense_check(raw, result)); dense_cases += 1
    rng = random.Random(20261102)
    multi = 0; admitted_dense_multi = 0
    for n in [2, 3, 4]:
        for _ in range(18):
            count = rng.choice([1, 2])
            g = [rng.randrange(1 << n) for _ in range(count)]
            # Repeated and zero coins exercise exact rank reduction.
            g += [g[0], 0]
            f = [rng.randrange(1 << n) for _ in range(n)]
            for bias in range(1 << n):
                raw = {'n': n, 'F_columns': f, 'G_columns': g, 'offset': bias}
                result = compile_affine(raw)
                assert verify_affine(raw, result)
                admitted_dense_multi += int(dense_check(raw, result)); multi += 1
    large = []
    for n in [8, 16, 32, 64]:
        change = [1 << j for j in range(n)]
        for _ in range(10*n):
            control, target = rng.sample(range(n), 2)
            change = [v ^ ((1 << target) if (v >> control) & 1 else 0) for v in change]
        inv = inverse_matrix(change)
        shift = [0]+[1 << (j-1) for j in range(1, n)]
        f = multiply_matrix(change, multiply_matrix(shift, inv))
        g = [linear(change, 1 << (n-1))]
        raw = {'n': n, 'F_columns': f, 'G_columns': g+[0, g[0]], 'offset': rng.randrange(1 << n)}
        result = compile_affine(raw)
        assert verify_affine(raw, result) and result['status'] == 'synthesized_uniform_pure_return'
        large.append({'n': n, 'original_noise_bits': 3, 'synthesized_noise_bits': result['noise_rank'],
                      'gate_count': len(result['source_program']['gates']),
                      'horizon': result['source_certificate']['horizon'],
                      'method': result['method'], 'dense_matrices_used': False})
    xor = {'n': 1, 'F_columns': [1], 'G_columns': [1], 'offset': 0}
    repair = compile_affine(xor)
    original = {'n': 1, 'env': 1, 'gates': [['H', 1], ['CX', 1, 0]]}
    assert acquire(original)['status'] == 'persistent_pauli'
    assert repair['source_certificate']['status'] == 'accepted_pure_return'
    dense_check(xor, repair)
    diagonal = {'system_qubits': 1, 'terms': [{'coefficient': '1', 'system_x': 1, 'system_z': 0, 'source_x': 0, 'source_z': 1}]}
    acquired = acquire_classical_coupling(xor, repair, diagonal)
    assert acquired['source_diagonal_coupling_verified'] and not acquired['future_control_instrument_algebra_verified']
    assert acquired['mean_terms'] == []
    coherent = copy.deepcopy(diagonal); coherent['terms'][0]['source_x'] = 1
    try:
        acquire_classical_coupling(xor, repair, coherent)
        raise AssertionError('Coherence-sensitive coupling accepted as classical.')
    except ValueError:
        pass
    cancel = copy.deepcopy(coherent)
    cancel['terms'].append(dict(cancel['terms'][0], coefficient='-1'))
    assert acquire_classical_coupling(xor, repair, cancel)['original_terms'] == []
    tampered = []
    bad = copy.deepcopy(repair); bad['original_coin_records_preserved'] = True; tampered.append(bad)
    bad = copy.deepcopy(repair); bad['arbitrary_original_quantum_dilation_preserved'] = True; tampered.append(bad)
    bad = copy.deepcopy(repair); bad['reverse_section_columns'][0] ^= 1; tampered.append(bad)
    bad = copy.deepcopy(repair); bad['source_program']['gates'].append(['Z', 0]); tampered.append(bad)
    bad = copy.deepcopy(repair); bad['source_certificate']['filtration'][-1] = [0]; tampered.append(bad)
    for bad in tampered:
        assert not verify_affine(xor, bad)
    for bad in [None, [], 0, 'bad', {}]:
        assert not verify_affine(xor, bad)
    # Bypass digest alone deliberately; wrong offset outside the noise image
    # must still be rejected by the actual forward/inverse fibre checks.
    raw = {'n': 2, 'F_columns': [2, 1], 'G_columns': [1], 'offset': 0}
    cert = compile_affine(raw); changed = dict(raw, offset=2)
    cert['input_digest'] = digest(changed)
    assert not verify_affine(changed, cert)
    invalid = [None, [], {}, {'n': True, 'F_columns': [0], 'G_columns': [1], 'offset': 0},
               dict(xor, F_columns=[-1]), dict(xor, G_columns='1'), dict(xor, offset=True),
               dict(xor, F_columns=[1, 0]), dict(xor, extra='not supported')]
    for raw in invalid:
        try:
            validate_affine(raw)
            raise AssertionError('Invalid affine input accepted.')
        except ValueError:
            pass
    result = {'scope': 'known classical affine law-preserving acquisition, not full dynamics simulation',
              'exhaustive_single_input_cases': total, 'admitted': accepted, 'outside_class': rejected,
              'method_counts': methods, 'selected_single_input_calls': dense_cases, 'admitted_dense_single_input_cases': admitted_dense_single,
              'multi_redundant_noise_all_offset_calls': multi, 'admitted_dense_multi_offset_cases': admitted_dense_multi, 'xor_fixture_dense_cases': 1,
              'large_symbolic_cases': large, 'xor_naive_rejected_recompiled_accepted': True, 'classical_coupling_guard_cases': 3,
              'tampered_positive_certificates_rejected': len(tampered),
              'malformed_certificates_rejected': 5, 'wrong_offset_despite_digest_change_rejected': True,
              'malformed_programs_rejected': len(invalid), 'passed': True}
    Path(__file__).with_name('affine_compiler_checks.json').write_text(json.dumps(result, indent=2)+'\n')
    ex = Path(__file__).with_name('examples')
    (ex/'xor_noise.affine.json').write_text(json.dumps(xor, indent=2)+'\n')
    (ex/'xor_noise.realization.json').write_text(json.dumps(repair, indent=2)+'\n')
    (ex/'xor_noise.coupling.json').write_text(json.dumps(diagonal, indent=2)+'\n')
    (ex/'xor_noise.acquired_coupling.json').write_text(json.dumps(acquired, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    run()
