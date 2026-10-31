"""Exact sparse-Pauli mean acquisition from a verified source certificate.

This module does not construct arbitrary Boolean-function expectations or
silently remove the physical mean Hamiltonian. Coefficients are explicit
integers or rational strings p/q. The output is an exact classical LCU
specification, not a synthesized quantum circuit.
"""
import argparse
from fractions import Fraction
import json
from pathlib import Path
import re
from acquire_clifford_source import verify, canonical_stabilizers, multiply

FIELDS = ('system_x', 'system_z', 'source_x', 'source_z')
RATIONAL = re.compile(r'[+-]?[0-9]+(?:/[0-9]+)?\Z')


def rational(value):
    if type(value) is int:
        return Fraction(value)
    if not isinstance(value, str) or not RATIONAL.fullmatch(value):
        raise ValueError('Use an exact integer or rational string p/q.')
    try:
        return Fraction(value)
    except (ValueError, ZeroDivisionError) as error:
        raise ValueError('Invalid rational coefficient.') from error


def read_terms(spec, n):
    if not isinstance(spec, dict) or type(spec.get('system_qubits')) is not int or spec['system_qubits'] < 1 or not isinstance(spec.get('terms'), list):
        raise ValueError('Require positive system_qubits and an explicit term list.')
    q = spec['system_qubits']
    result = {}
    for term in spec['terms']:
        if not isinstance(term, dict) or any(k not in term for k in ('coefficient', *FIELDS)):
            raise ValueError('Every term requires coefficient and all four Pauli masks.')
        values = tuple(term[k] for k in FIELDS)
        if any(type(v) is not int or not 0 <= v < (1 << (q if i < 2 else n)) for i, v in enumerate(values)):
            raise ValueError('Invalid Pauli mask.')
        coefficient = rational(term['coefficient'])
        result[values] = result.get(values, Fraction(0)) + coefficient
    return q, {key: value for key, value in result.items() if value}


def prepare_membership(generators, n):
    """Preprocess a verified signed tableau once for a whole future term list."""
    return tuple((g, (g[1] | (g[2] << n)).bit_length()-1)
                 for g in canonical_stabilizers(generators, n))


def expectation_prepared(membership, n, x, z):
    """Signed membership with precomputed pivots, including Y phases."""
    row = ((x & z).bit_count() % 4, x, z)
    for generator, pivot in membership:
        current = row[1] | (row[2] << n)
        if (current >> pivot) & 1:
            row = multiply(row, generator)
    if row[1] or row[2]:
        return 0
    if row[0] == 0:
        return 1
    if row[0] == 2:
        return -1
    raise AssertionError('A Hermitian stabilizer member acquired an imaginary sign.')


def expectation(generators, n, x, z):
    """Convenience one-off wrapper; use prepared membership for repeated terms."""
    return expectation_prepared(prepare_membership(generators, n), n, x, z)


def term_list(terms):
    return [dict(zip(FIELDS, key), coefficient=str(value)) for key, value in sorted(terms.items()) if value]


def acquire_coupling(program, certificate, spec):
    # The command-line path deliberately rechecks proof integrity. An application
    # may separately cache an immutable verified certificate, with that cost paid.
    if not verify(program, certificate) or certificate.get('status') != 'accepted_pure_return':
        raise ValueError('A verified accepted pure-return source certificate is required.')
    n = program['n']
    q, terms = read_terms(spec, n)
    generators = certificate['constant_state_stabilizers']
    membership = prepare_membership(generators, n)
    means, observations = {}, []
    for key, value in sorted(terms.items()):
        sx, sz, x, z = key
        mu = expectation_prepared(membership, n, x, z)
        observations.append({'source_x': x, 'source_z': z, 'expectation': mu,
                             'system_x': sx, 'system_z': sz, 'coefficient': str(value)})
        means[(sx, sz)] = means.get((sx, sz), Fraction(0)) + value*mu
    means = {key: value for key, value in means.items() if value}
    centered = dict(terms)
    for (sx, sz), value in means.items():
        key = (sx, sz, 0, 0)
        centered[key] = centered.get(key, Fraction(0))-value
    centered = {key: value for key, value in centered.items() if value}
    # Exact symbolic recheck of PK_centered P=0.
    residual = {}
    for (sx, sz, x, z), value in centered.items():
        residual[(sx, sz)] = residual.get((sx, sz), Fraction(0))+value*expectation_prepared(membership, n, x, z)
    assert all(value == 0 for value in residual.values())
    original_bound = sum(map(abs, terms.values()), Fraction(0))
    centered_bound = sum(map(abs, centered.values()), Fraction(0))
    mean_bound = sum(map(abs, means.values()), Fraction(0))
    assert centered_bound <= 2*original_bound and mean_bound <= original_bound
    scalar = means.get((0, 0), Fraction(0))
    nontrivial = {key: value for key, value in means.items() if key != (0, 0)}
    return {
        'source_digest': certificate['source_digest'], 'source_qubits': n,
        'system_qubits': q, 'return_horizon': certificate['horizon'],
        'original_terms': term_list(terms), 'term_expectations': observations,
        'mean_terms': [{'system_x': x, 'system_z': z, 'coefficient': str(value)} for (x, z), value in sorted(means.items())],
        'centered_terms': term_list(centered), 'centered_mean_exactly_zero': True,
        'original_lcu_bound': str(original_bound), 'centered_lcu_bound': str(centered_bound),
        'mean_lcu_bound': str(mean_bound), 'scalar_mean': str(scalar),
        'nontrivial_mean_lcu_bound': str(sum(map(abs, nontrivial.values()), Fraction(0))),
        'physical_mean_commutator_is_zero': not nontrivial,
        'model_identity': 'Hsys + sqrt(lambda) K = (Hsys + sqrt(lambda) Hbar) + sqrt(lambda) K_centered',
        'scope': 'Sparse known Pauli lists only; actual LCU synthesis, mean Hamiltonian action and consumer costs remain paid.',
        'global_phase_note': 'The scalar system-identity part of Hbar may be omitted for the stated CPTP dynamics; nontrivial mean terms remain physical.'
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('program', type=Path)
    parser.add_argument('certificate', type=Path)
    parser.add_argument('coupling', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = acquire_coupling(json.loads(args.program.read_text()),
                              json.loads(args.certificate.read_text()),
                              json.loads(args.coupling.read_text()))
    output = json.dumps(result, indent=2)+'\n'
    if args.output:
        args.output.write_text(output)
    else:
        print(output, end='')


if __name__ == '__main__':
    main()
