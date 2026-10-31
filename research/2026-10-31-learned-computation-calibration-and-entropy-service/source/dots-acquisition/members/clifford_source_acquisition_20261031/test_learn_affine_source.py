"""Synthetic and finite exact-probability checks for promised source learning.
These tests do not establish that any external device satisfies the promise.
"""
import copy
from collections import Counter
from fractions import Fraction
from itertools import product
import json
from pathlib import Path
import random
from acquire_clifford_source import basis, kernel_columns, linear
from compile_affine_source import transpose_columns, multiply_matrix, inverse_matrix
from learn_affine_source import (query_plan, learn_and_compile, verify_learning_record,
                                 sample_and_compile, validate_transcript)


def same_law(true_model, learned):
    n = true_model['n']; noise = basis(true_model['G_columns'])
    if basis(learned['G_columns']) != noise:
        return False
    R = transpose_columns(kernel_columns(transpose_columns(noise, n)), n)
    return (multiply_matrix(R, true_model['F_columns']) == multiply_matrix(R, learned['F_columns'])
            and linear(R, true_model['offset'] ^ learned['offset']) == 0)


def run():
    rng = random.Random(20261103)
    high_confidence = 0; queries = 0; admission_counts = Counter()
    for n in range(1, 6):
        for _ in range(20):
            hidden = {'n': n, 'F_columns': [rng.randrange(1 << n) for _ in range(n)],
                      'G_columns': [rng.randrange(1 << n) for _ in range(rng.randrange(n+2))],
                      'offset': rng.randrange(1 << n)}
            calls = []
            def one_step(x):
                calls.append(x)
                return linear(hidden['F_columns'], x) ^ linear(hidden['G_columns'], rng.randrange(1 << len(hidden['G_columns']))) ^ hidden['offset']
            transcript, record = sample_and_compile(n, '1/1048576', one_step)
            assert calls == query_plan(n, '1/1048576')['inputs']
            assert same_law(hidden, record['learned_model'])
            assert verify_learning_record(transcript, record)
            high_confidence += 1; queries += len(calls)
            admission_counts[record['realization']['status']] += 1
    large = []
    for n in [8, 16, 32, 64]:
        change = [1 << i for i in range(n)]
        for _ in range(8*n):
            c, t = rng.sample(range(n), 2)
            change = [v ^ ((1 << t) if (v >> c) & 1 else 0) for v in change]
        f = multiply_matrix(change, multiply_matrix([0]+[1 << (j-1) for j in range(1, n)], inverse_matrix(change)))
        hidden = {'n': n, 'F_columns': f, 'G_columns': [linear(change, 1 << (n-1))], 'offset': rng.randrange(1 << n)}
        count = [0]
        def one_step(x):
            count[0] += 1
            return linear(hidden['F_columns'], x) ^ (hidden['G_columns'][0] if rng.randrange(2) else 0) ^ hidden['offset']
        transcript, record = sample_and_compile(n, '1/1048576', one_step)
        assert same_law(hidden, record['learned_model']) and record['realization']['status'] == 'synthesized_uniform_pure_return'
        large.append({'n': n, 'classical_transition_queries': count[0],
                      'observed_bits': n*count[0], 'learned_noise_rank': len(record['noise_basis']),
                      'return_horizon': record['realization']['source_certificate']['horizon'],
                      'dense_state_table_used': False})
    # Exhaustive no-false-admission check for an uncontrollable promised model.
    n = 2; delta = '1/4'; plan = query_plan(n, delta)
    hidden = {'n': 2, 'F_columns': [1, 2], 'G_columns': [1], 'offset': 0}
    no_false = 0
    for noises in product(range(2), repeat=len(plan['inputs'])):
        outputs = [linear(hidden['F_columns'], x) ^ noise for x, noise in zip(plan['inputs'], noises)]
        transcript = {'n': n, 'failure_probability': delta, 'outputs': outputs}
        record = learn_and_compile(transcript)
        assert record['realization']['status'] == 'outside_controllable_uniform_class'
        assert verify_learning_record(transcript, record)
        no_false += 1
    # Exact aggregation for a full-noise source. It includes bad but admitted
    # transcripts, showing algebraic verification is NOT pointwise truth.
    M = plan['difference_samples']
    subspace_counts = Counter(tuple(basis(differences)) for differences in product(range(4), repeat=M))
    admitted_weight = wrong_admitted_weight = total_weight = 0
    rare_wrong = None
    true_full = {'n': 2, 'F_columns': [0, 0], 'G_columns': [1, 2], 'offset': 0}
    grouped_records = 0
    for subspace, multiplicity in subspace_counts.items():
        differences = list(subspace)+[0]*(M-len(subspace))
        for y0 in range(4):
            for probe_outputs in product(range(4), repeat=2):
                outputs = [y0]+[y0 ^ d for d in differences]+list(probe_outputs)
                transcript = {'n': 2, 'failure_probability': delta, 'outputs': outputs}
                record = learn_and_compile(transcript); grouped_records += 1
                assert verify_learning_record(transcript, record)
                total_weight += multiplicity
                if record['realization']['status'] == 'synthesized_uniform_pure_return':
                    admitted_weight += multiplicity
                    if not same_law(true_full, record['learned_model']):
                        wrong_admitted_weight += multiplicity
                        rare_wrong = {'transcript': transcript, 'record': record}
    conditional = Fraction(wrong_admitted_weight, admitted_weight)
    assert total_weight == 4**len(plan['inputs'])
    assert conditional <= Fraction(delta) and wrong_admitted_weight > 0
    assert rare_wrong is not None and rare_wrong['record']['model_family_promise_verified_from_data'] is False
    assert verify_learning_record(rare_wrong['transcript'], rare_wrong['record'])
    t = rare_wrong['transcript']; r = rare_wrong['record']
    malformed = [None, [], {}, dict(t, n=True), dict(t, failure_probability='0'),
                 dict(t, failure_probability='2'), dict(t, failure_probability=0.1),
                 dict(t, outputs=t['outputs'][:-1]), dict(t, extra='unsupported')]
    invalid_output = copy.deepcopy(t); invalid_output['outputs'][0] = True; malformed.append(invalid_output)
    invalid_output = copy.deepcopy(t); invalid_output['outputs'][0] = -1; malformed.append(invalid_output)
    for bad in malformed:
        try:
            validate_transcript(bad)
            raise AssertionError('Malformed transcript accepted.')
        except ValueError:
            pass
    tampered = []
    bad = copy.deepcopy(r); bad['model_family_promise_verified_from_data'] = True; tampered.append(bad)
    bad = copy.deepcopy(r); bad['confidence_interpretation'] = 'Posterior certainty for this dataset'; tampered.append(bad)
    bad = copy.deepcopy(r); bad['rare_postselection_covered'] = True; tampered.append(bad)
    bad = copy.deepcopy(r); bad['admitted_transcript_average_failure_upper_bound'] = '0'; tampered.append(bad)
    bad = copy.deepcopy(r); bad['learned_model']['offset'] ^= 1; tampered.append(bad)
    for bad in tampered:
        assert not verify_learning_record(t, bad)
    for bad in [None, [], 0, 'bad']:
        assert not verify_learning_record(t, bad)
    result = {'scope': 'promised classical chosen-input learning and compilation; no promise validation or downstream simulation',
              'synthetic_high_confidence_models': high_confidence, 'their_transition_queries': queries,
              'their_admission_counts': dict(admission_counts), 'large_symbolic_models': large,
              'exhaustive_uncontrollable_transcripts': no_false,
              'exact_grouped_full_noise_records': grouped_records,
              'represented_equiprobable_full_noise_transcripts': total_weight,
              'conditional_wrong_model_among_admitted': str(conditional),
              'requested_failure_probability': delta,
              'verified_but_wrong_rare_transcript_preserved': True,
              'malformed_transcripts_rejected': len(malformed), 'tampered_scope_or_model_records_rejected': len(tampered),
              'malformed_records_rejected': 4, 'passed': True}
    folder = Path(__file__).parent
    (folder/'learning_checks.json').write_text(json.dumps(result, indent=2)+'\n')
    (folder/'examples'/'rare_wrong_admitted_transcript.json').write_text(json.dumps(rare_wrong, indent=2)+'\n')
    # Reproducible successful transcript with no hidden coefficients in learner input.
    hidden = {'n': 3, 'F_columns': [0, 1, 2], 'G_columns': [4], 'offset': 3}
    def oracle(x):
        return linear(hidden['F_columns'], x) ^ (4 if rng.randrange(2) else 0) ^ 3
    successful_t, successful_r = sample_and_compile(3, '1/1024', oracle)
    assert same_law(hidden, successful_r['learned_model'])
    (folder/'examples'/'learned_history.transcript.json').write_text(json.dumps(successful_t, indent=2)+'\n')
    (folder/'examples'/'learned_history.result.json').write_text(json.dumps(successful_r, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    run()
