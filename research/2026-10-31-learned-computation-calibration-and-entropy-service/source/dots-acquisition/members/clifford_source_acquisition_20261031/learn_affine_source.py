"""Classical chosen-input acquisition of a promised affine noise kernel.

Assumption: every query at x returns F*x + beta + eta, where eta is fresh,
independent and uniform on one unknown fixed GF(2) subspace. State labels
are complete and correct. The code does not verify that model promise.
It learns a canonical transition LAW, not hidden original coefficients or
coin records, then invokes the separately verified realization compiler.
"""
import argparse
from fractions import Fraction
import json
from pathlib import Path
from acquire_clifford_source import basis, kernel_columns, linear, digest
from acquire_pauli_coupling import rational
from compile_affine_source import (transpose_columns, solver_table, solve,
                                  compile_affine, verify_affine)


SCOPE = {
    'model_family_promise_verified_from_data': False,
    'confidence_interpretation': 'Frequentist bounds over training transcripts and, when admitted, their conditional average; not posterior correctness of each dataset or rare later postselection.',
    'reuse_scope': 'One successful acquisition event fixes the exact transition law for all finite future admissible adaptive uses; numerical execution errors and costs still accumulate.',
    'known_clock_rate_required': True,
    'access_scope': 'Classical chosen-input one-step/reset samples with correct full state labels and fresh independent uniform-subspace noise; future exogenous source-diagonal system coupling is separately supplied.',
    'unknown_quantum_backaction_or_coupling_identified': False,
    'rare_postselection_covered': False,
}


def query_plan(n, failure_probability):
    if type(n) is not int or n < 1:
        raise ValueError('Require n>=1 and complete n-bit state labels.')
    delta = rational(failure_probability)
    if not 0 < delta < 1:
        raise ValueError('Failure probability must be an exact rational in (0,1).')
    target_num, target_den = 2*delta.denominator, delta.numerator
    ell = max(0, target_num.bit_length()-target_den.bit_length())
    while (target_den << ell) < target_num:
        ell += 1
    while ell and (target_den << (ell-1)) >= target_num:
        ell -= 1
    differences = n+ell
    return {'n': n, 'requested_failure_probability': str(delta),
            'confidence_bits': ell, 'difference_samples': differences,
            'proved_failure_upper_bound': str(Fraction(1, 1 << ell)),
            'inputs': [0]*(differences+1)+[1 << i for i in range(n)]}


def validate_transcript(transcript):
    required = {'n', 'failure_probability', 'outputs'}
    if not isinstance(transcript, dict) or set(transcript) != required:
        raise ValueError('Require exactly n, failure_probability and outputs in the fixed query-plan order.')
    plan = query_plan(transcript['n'], transcript['failure_probability'])
    outputs = transcript['outputs']; n = transcript['n']
    if not isinstance(outputs, list) or len(outputs) != len(plan['inputs']):
        raise ValueError('Output count does not match the prescribed chosen-input query plan.')
    if any(type(y) is not int or not 0 <= y < (1 << n) for y in outputs):
        raise ValueError('Outputs must be complete n-bit integer state labels.')
    return plan


def infer_model(transcript):
    plan = validate_transcript(transcript)
    n = transcript['n']; outputs = transcript['outputs']; count = plan['difference_samples']
    reference = outputs[0]
    noise = basis([y ^ reference for y in outputs[1:count+1]])
    quotient = transpose_columns(kernel_columns(transpose_columns(noise, n)), n)
    quotient_offset = linear(quotient, reference)
    drift = [linear(quotient, outputs[count+1+i]) ^ quotient_offset for i in range(n)]
    section = solver_table(quotient)
    model = {'n': n, 'F_columns': [solve(section, y) for y in drift],
             'G_columns': noise, 'offset': solve(section, quotient_offset)}
    # Deterministic consistency with supplied zero/basis observations is NOT
    # a validation of the global affine/uniform-noise statistical assumption.
    for x, y in zip(plan['inputs'], outputs):
        assert linear(quotient, y ^ linear(model['F_columns'], x) ^ model['offset']) == 0
    return {'query_plan': plan, 'reference_output': reference, 'noise_basis': noise,
            'quotient_columns': quotient, 'quotient_drift_columns': drift,
            'quotient_offset': quotient_offset, 'learned_model': model}


def learn_and_compile(transcript):
    inference = infer_model(transcript)
    realization = compile_affine(inference['learned_model'])
    bound = Fraction(inference['query_plan']['proved_failure_upper_bound'])
    admitted = realization['status'] == 'synthesized_uniform_pure_return'
    return {'transcript_digest': digest(transcript), **inference,
            'realization': realization,
            'admitted_transcript_average_failure_upper_bound': str(bound/(1-bound)) if admitted else None,
            **SCOPE}


def verify_learning_record(transcript, record):
    """Check the inferred-model algebra, NOT the truth of the model promise."""
    try:
        if not isinstance(record, dict) or record.get('transcript_digest') != digest(transcript):
            return False
        if any((record.get(key) is not value) if type(value) is bool else (record.get(key) != value) for key, value in SCOPE.items()):
            return False
        expected = infer_model(transcript)
        if any(record.get(key) != value for key, value in expected.items()):
            return False
        if not verify_affine(expected['learned_model'], record['realization']):
            return False
        bound = Fraction(expected['query_plan']['proved_failure_upper_bound'])
        admitted = record['realization']['status'] == 'synthesized_uniform_pure_return'
        return record.get('admitted_transcript_average_failure_upper_bound') == (str(bound/(1-bound)) if admitted else None)
    except (ValueError, KeyError, TypeError, IndexError, AssertionError, AttributeError):
        return False


def sample_and_compile(n, failure_probability, one_step):
    """The caller supplies authorized classical chosen-input access.

    Synthetic tests use this interface. It performs no device/network access
    on its own and never inspects the sampler's hidden implementation.
    """
    plan = query_plan(n, failure_probability)
    transcript = {'n': n, 'failure_probability': plan['requested_failure_probability'],
                  'outputs': [one_step(x) for x in plan['inputs']]}
    record = learn_and_compile(transcript)
    if not verify_learning_record(transcript, record):
        raise AssertionError('Generated inference record failed algebraic verification.')
    return transcript, record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('transcript', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    transcript = json.loads(args.transcript.read_text())
    result = learn_and_compile(transcript)
    if not verify_learning_record(transcript, result):
        raise RuntimeError('Inference record failed algebraic verification.')
    output = json.dumps(result, indent=2)+'\n'
    if args.output:
        args.output.write_text(output)
    else:
        print(output, end='')


if __name__ == '__main__':
    main()
