"""Guarded sparse-Pauli consumer of a law-preserving CLASSICAL realization.

This checks the coupling algebra only. It does not implement or verify an
arbitrary future instrument/control program or the downstream simulator.
"""
import argparse
import json
from pathlib import Path
from compile_affine_source import verify_affine
from acquire_pauli_coupling import read_terms, acquire_coupling


def acquire_classical_coupling(raw, realization, coupling):
    if not verify_affine(raw, realization) or realization.get('status') != 'synthesized_uniform_pure_return':
        raise ValueError('A verified positive classical realization is required.')
    _, terms = read_terms(coupling, raw['n'])
    if any(key[2] != 0 for key in terms):
        raise ValueError('A source-coherence-sensitive coupling is not preserved by this classical-law realization.')
    result = acquire_coupling(realization['source_program'], realization['source_certificate'], coupling)
    result['classical_program_digest'] = realization['input_digest']
    result['equivalence_scope'] = realization['equivalence_scope']
    result['source_diagonal_coupling_verified'] = True
    result['future_control_instrument_algebra_verified'] = False
    result['original_coin_records_preserved'] = False
    result['arbitrary_original_quantum_dilation_preserved'] = False
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('program', type=Path)
    parser.add_argument('realization', type=Path)
    parser.add_argument('coupling', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = acquire_classical_coupling(json.loads(args.program.read_text()),
                                        json.loads(args.realization.read_text()),
                                        json.loads(args.coupling.read_text()))
    output = json.dumps(result, indent=2)+'\n'
    if args.output:
        args.output.write_text(output)
    else:
        print(output, end='')


if __name__ == '__main__':
    main()
