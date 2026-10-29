#!/usr/bin/env python3
"""Symbolic finite receiver compiler, not a hardware pulse generator.
Run: python p2_operation/compile_receiver.py --epsilon 1/100
Optional --input JSON: C_batches and optional source_labels (binary lists).
"""
from fractions import Fraction as F
from pathlib import Path
import argparse, json
import numpy as np
from projective_compiler_checks import normal_form, inverse_phases, quadratic

def pauli_mul(a, b):
    p, x, z = a
    q, y, w = b
    return ((p+q+2*sum(i*j for i, j in zip(z, y))) % 4,
            [(i+j) % 2 for i, j in zip(x, y)],
            [(i+j) % 2 for i, j in zip(z, w)])

def frames(b, rmat, rinv, r):
    n, nq = len(b), len(b)-r
    canonical = []
    for j in range(n):
        p, x, z = 0, [0]*nq, [0]*nq
        k = j//2 if j < 2*r else r+j-2*r
        if j < 2*r and j % 2 == 0:
            x[k] = 1
        else:
            z[k] = 1
        canonical.append((p, x, z))
    phases = inverse_phases(b, rmat, rinv)
    result = []
    for i in range(n):
        word = (phases[i], [0]*nq, [0]*nq)
        for j in range(n):
            if rinv[j, i]:
                word = pauli_mul(word, canonical[j])
        p, x, z = word
        assert not any(x[r:])
        assert (2*p+2*sum(a*c for a, c in zip(x, z))) % 4 == 0
        result.append({'source_generator': i+1,
                       'retained_i_power': p, 'retained_X': x[:r],
                       'retained_Z': z[:r], 'radical_record_Z': z[r:]})
    for i in range(n):
        for j in range(n):
            a, c = result[i], result[j]
            sign = sum(x*z+y*w for x, z, y, w in
                       zip(a['retained_X'], c['retained_Z'],
                           c['retained_X'], a['retained_Z'])) % 2
            assert sign == int(b[i, j])
    return result

def example():
    a, b = np.zeros((4, 4), int), np.zeros((4, 4), int)
    a[0, 1] = a[1, 0] = 1
    b[2, 3] = b[3, 2] = 1
    return {'name': 'two independent pairs, staggered arrivals and retirement',
            'C_batches': [a.tolist(), b.tolist(), a.tolist(), b.tolist()]}

def compile_schedule(spec, epsilon):
    if not 0 < epsilon < 1:
        raise ValueError('epsilon must be a positive rational below one')
    batches = spec['C_batches']
    if not batches:
        raise ValueError('at least one arrival is required')
    n = len(batches[0])
    if not n:
        raise ValueError('at least one source generator is required')
    cs = []
    for c in batches:
        a = np.asarray(c)
        if a.shape != (n, n) or not np.all((a == 0) | (a == 1)):
            raise ValueError('each C must be an n by n binary matrix')
        a = a.astype(int)
        if not np.array_equal(a, a.T) or np.any(np.diag(a)):
            raise ValueError('each C must be symmetric with zero diagonal')
        cs.append(a)
    labels = spec.get('source_labels')
    if labels is None:
        weight = n
    else:
        if not labels or any(len(x) != n or any(a not in (0, 1) for a in x)
                             for x in labels):
            raise ValueError('source_labels must be nonempty binary n-vectors')
        weight = max(map(sum, labels))
    total = np.zeros((n, n), int)
    for c in cs:
        total ^= c
    if np.any(total):
        raise ValueError('final commutator is nonzero; this exact-erasure compiler does not apply')
    tmax, b, prev_r = len(cs), np.zeros((n, n), int), 0
    stages, error, queries, bits = [], F(0), 0, 0
    old_frames = [{'source_generator': i+1, 'i_power': 0, 'X': [], 'Z': []}
                  for i in range(n)]
    for t, c in enumerate(cs, 1):
        b ^= c
        rmat, rinv, r = normal_form(b)
        le = int(rmat.sum())
        coefficient = F(weight*(2*le+1)*110, 49)
        # pi/sqrt(2) < (22/7)*(5/7)=110/49. Exact rational certificate.
        m, size = 1, 2
        while coefficient/size > epsilon/tmax:
            m, size = m+1, 2*size
        allowance = coefficient/size
        stage = {'arrival': t, 'prefix_B': b.tolist(),
                 'retained_qubits_before': prev_r, 'retained_qubits_after': r,
                 'R_columns_in_original_generators': rmat.tolist(),
                 'R_inverse': rinv.tolist(), 'L': le,
                 'incoming_retained_generator_frames': old_frames,
                 'controlled_A_definition': 'A_i = old_P_i tensor U_i,t. old_P_i=i^p X^x Z^z includes its controlled scalar phase. In time order apply Z factors, X factors and control phase p*pi/2, together with controlled actual U_i,t.',
                 'canonical_words': [
                     {'index': j+1, 'i_power': quadratic(rmat[:, j], b),
                      'control_phase_constant_pi_over_2': quadratic(rmat[:, j], b),
                      'control_phase_phi_coefficients': ['-1/2' if rmat[i, j] else '0' for i in range(n)],
                      'control_phase_rule': 'Add q_j*pi/2 - sum_i R_ij*phi_i/2 to the control, in addition to each old Pauli frame controlled phase. This queries H_j(Ahat), not H_j(A).',
                      'operator_order': [i+1 for i in range(n) if rmat[i, j]],
                      'execution_order': [i+1 for i in reversed(range(n)) if rmat[i, j]]}
                     for j in range(n)],
                 'retained_generator_frames': frames(b, rmat, rinv, r),
                 'phase_register': {'M': size, 'qubits': m, 'estimates': n,
                                    'actual_outcomes': 'j_i=0,...,M-1; phi_i=2pi j_i/M'},
                 'radical_record_bits': n-2*r,
                 'actual_record_bits': n*m+n-2*r,
                 'elementary_controlled_field_queries': 2*n*(size-1)+le,
                 'conservative_temporary_finite_qubits': m+prev_r+r+1,
                 'complete_error_rational_upper': str(allowance),
                 'phase_feedback_increment_for_generator_i':
                     'phi_i/2 + pi * dot(radical_record_Z_i, actual_radical_bits)',
                 'retirement': 'after extraction, trace previous memory and residual arriving field'}
        stage['pair_extraction_circuit'] = [
            {'retained_output_qubit': k+1,
             'time_order': ['prepare 0', 'H', f'controlled canonical word {2*k+2}',
                            'H', f'controlled canonical word {2*k+1}']}
            for k in range(r)]
        stage['radical_readout_circuit'] = [
            {'radical_bit': j-2*r+1,
             'time_order': ['prepare 0', 'H', f'controlled canonical word {j+1}',
                            'H', 'measure computational basis', 'reset using actual bit or supply fresh qubit']}
            for j in range(2*r, n)]
        stages.append(stage)
        error += allowance
        queries += stage['elementary_controlled_field_queries']
        bits += stage['actual_record_bits']
        prev_r = r
        old_frames = [{'source_generator': f['source_generator'],
                       'i_power': f['retained_i_power'], 'X': f['retained_X'],
                       'Z': f['retained_Z']} for f in stage['retained_generator_frames']]
    assert prev_r == 0 and error <= epsilon
    return {'name': spec.get('name', 'binary projective receiver'),
            'contract': 'all joint source/batch/reference inputs; all actual records; same actual receiver common-input baseline; diagonal source G retained; no extra source coupling',
            'source_generators': n, 'max_source_word_weight': weight,
            'requested_error': str(epsilon), 'certified_complete_error_upper': str(error),
            'controlled_field_queries': queries, 'actual_record_bits': bits,
            'retained_qubit_schedule': [s['retained_qubits_after'] for s in stages],
            'stages': stages,
            'final_source_feedback': 'Negate the sum of recorded increments for each generator, and add the negative final retained_i_power*pi/2 constant. Apply these phases controlled by source bits after the declared diagonal interaction.',
            'essential_supplied_controls': ['controlled actual U_i,t with known phase reference',
                'finite qubit gates, prepared/reset registers and deterministic readout',
                'field capture through each stage and source coherence through feedback'],
            'separate_costs': ['query duration and power synthesis', 'field and memory loss',
                'intermediate field energy and discarded energy', 'calibration and model errors',
                'old-memory controlled Pauli synthesis and connectivity', 'feedback and source storage'],
            'scope': 'Conservative finite-circuit certificate, not optimized performance or a device/workload error. Actual physical errors are additional; arbitrary-energy Weyl calibration continuity is not assumed.'}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path)
    parser.add_argument('--epsilon', default='1/100')
    parser.add_argument('--output', type=Path,
                        default=Path(__file__).with_name('COMPILED_EXAMPLE.json'))
    args = parser.parse_args()
    spec = json.loads(args.input.read_text()) if args.input else example()
    result = compile_schedule(spec, F(args.epsilon))
    args.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: result[k] for k in ['retained_qubit_schedule',
                      'certified_complete_error_upper', 'controlled_field_queries',
                      'actual_record_bits']}, indent=2))

if __name__ == '__main__':
    main()
