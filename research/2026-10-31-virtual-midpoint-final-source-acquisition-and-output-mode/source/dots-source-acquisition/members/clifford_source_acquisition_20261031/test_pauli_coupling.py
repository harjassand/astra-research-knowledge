"""Independent dense checks for exact signed sparse-Pauli acquisition."""
import copy
from fractions import Fraction
import json
import random
from pathlib import Path
import numpy as np
from acquire_clifford_source import acquire
from acquire_pauli_coupling import acquire_coupling, expectation
from test_acquisition import unitary, pauli_matrix


def dense_terms(terms, ns, n):
    out = np.zeros((1 << (ns+n), 1 << (ns+n)), complex)
    for term in terms:
        sx, sz, x, z = [term[k] for k in ('system_x', 'system_z', 'source_x', 'source_z')]
        out += float(Fraction(term['coefficient'])) * np.kron(pauli_matrix((sx & sz).bit_count() % 4, sx, sz, ns), pauli_matrix((x & z).bit_count() % 4, x, z, n))
    return out


def run():
    rng = random.Random(20261101)
    preparations = [
        (1, []), (1, [['X', 0]]), (1, [['H', 0], ['S', 0]]),
        (1, [['H', 0], ['SDG', 0]]),
        (2, [['H', 0], ['CX', 0, 1], ['Z', 0]])]
    for _ in range(20):
        n = rng.choice([2, 3])
        gates = []
        for _ in range(14):
            op = rng.choice(['H', 'S', 'CX'])
            gates.append([op, *rng.sample(range(n), 2 if op == 'CX' else 1)])
        preparations.append((n, gates))
    expectation_checks = 0
    max_error = 0.
    for n, prep in preparations:
        program = {'n': n, 'env': n, 'gates': [['SWAP', j, n+j] for j in range(n)]+prep}
        certificate = acquire(program)
        assert certificate['status'] == 'accepted_pure_return'
        psi = unitary(certificate['psi_preparation'], n)[:, 0]
        for x in range(1 << n):
            for z in range(1 << n):
                mu = expectation(certificate['constant_state_stabilizers'], n, x, z)
                exact = np.vdot(psi, pauli_matrix((x & z).bit_count() % 4, x, z, n) @ psi)
                assert abs(mu-exact) < 1e-10
                expectation_checks += 1
        ns = 2
        terms = []
        for _ in range(25):
            terms.append({'coefficient': str(Fraction(rng.randint(-5, 5), rng.randint(1, 7))),
                          'system_x': rng.randrange(1 << ns), 'system_z': rng.randrange(1 << ns),
                          'source_x': rng.randrange(1 << n), 'source_z': rng.randrange(1 << n)})
        terms += [dict(terms[0]), dict(terms[0], coefficient=str(-Fraction(terms[0]['coefficient'])))]
        spec = {'system_qubits': ns, 'terms': terms}
        result = acquire_coupling(program, certificate, spec)
        K = dense_terms(result['original_terms'], ns, n)
        Kc = dense_terms(result['centered_terms'], ns, n)
        mean = np.zeros((1 << ns, 1 << ns), complex)
        for term in result['mean_terms']:
            x, z = term['system_x'], term['system_z']
            mean += float(Fraction(term['coefficient']))*pauli_matrix((x & z).bit_count() % 4, x, z, ns)
        embed = np.kron(np.eye(1 << ns), psi.reshape(-1, 1))
        error = max(np.linalg.norm(embed.conj().T @ K @ embed-mean),
                    np.linalg.norm(K-Kc-np.kron(mean, np.eye(1 << n))),
                    np.linalg.norm(embed.conj().T @ Kc @ embed))
        max_error = max(max_error, float(error))
        assert error < 1e-10
        assert np.linalg.norm(Kc, 2) <= float(Fraction(result['centered_lcu_bound']))+1e-10
    # Identity-source terms are not silently discarded from the physical mean.
    p = {'n': 1, 'env': 1, 'gates': [['SWAP', 0, 1]]}; c = acquire(p)
    spec = {'system_qubits': 1, 'terms': [
        {'coefficient': '2', 'system_x': 0, 'system_z': 1, 'source_x': 0, 'source_z': 0},
        {'coefficient': '3/2', 'system_x': 0, 'system_z': 0, 'source_x': 0, 'source_z': 0}]}
    result = acquire_coupling(p, c, spec)
    assert result['centered_terms'] == [] and result['nontrivial_mean_lcu_bound'] == '2' and result['scalar_mean'] == '3/2'
    assert not result['physical_mean_commutator_is_zero']
    failures = [None, {}, {'system_qubits': True, 'terms': []}, {'system_qubits': 1, 'terms': {}}]
    for coeff in ['__import__("os")', '1/0', 0.5, float('nan')]:
        bad = copy.deepcopy(spec); bad['terms'][0]['coefficient'] = coeff; failures.append(bad)
    bad = copy.deepcopy(spec); bad['terms'][0]['source_x'] = True; failures.append(bad)
    for bad in failures:
        try:
            acquire_coupling(p, c, bad)
            raise AssertionError('Malformed coupling accepted.')
        except ValueError:
            pass
    bad = copy.deepcopy(c); bad['filtration'][-1] = [0]
    try:
        acquire_coupling(p, bad, spec)
        raise AssertionError('Forged source certificate accepted.')
    except ValueError:
        pass
    summary = {'scope': 'Exact classical acquisition/LCU specification, not quantum circuit synthesis',
               'pure_source_cases': len(preparations), 'signed_pauli_expectation_checks': expectation_checks,
               'dense_centering_cases': len(preparations), 'maximum_dense_identity_error': max_error,
               'mean_preservation_case': True, 'malformed_coupling_cases': len(failures),
               'forged_source_certificate_rejected': True, 'passed': True}
    Path(__file__).with_name('pauli_coupling_checks.json').write_text(json.dumps(summary, indent=2)+'\n')
    ex = Path(__file__).with_name('examples')
    (ex/'mean_preservation.coupling.json').write_text(json.dumps(spec, indent=2)+'\n')
    (ex/'mean_preservation.acquired.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    run()
