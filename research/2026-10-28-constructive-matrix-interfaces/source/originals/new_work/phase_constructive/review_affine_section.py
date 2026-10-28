#!/usr/bin/env python3
"""Independent affine-section review on the new E6 ordinary circuit."""
from pathlib import Path
import hashlib
import itertools
import json
import random
import sys
import time

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
SECTION = HERE.parent/'independent_audit'
sys.path.insert(0, str(SECTION))
from acquired_affine_section import (
    AcquiredAffineSection, BinaryCoordinates, apply_binary, unpack,
    rectangular_unpack, product, pack)


def literal_wires(program, x):
    wires = [(x >> i) & 1 for i in range(program['inputs'])]
    for gate in program['gates']:
        if gate['op'] == 'const': value = gate['value']
        elif gate['op'] == 'xor':
            value = 0
            for argument in gate['args']: value ^= wires[argument]
        elif gate['op'] == 'and':
            value = 1
            for argument in gate['args']: value &= wires[argument]
        else: raise ValueError(gate['op'])
        wires.append(value)
    return wires


def main():
    started = time.perf_counter()
    native = json.loads((HERE/'e6_phase_audit_results.json').read_text())['native']['result']
    program = json.loads((HERE/'e6_distinct_targets_native_n72.json').read_text())
    C, S, A = (native['affine_slice_certificate'], native['split_certificate'],
               native['compression_certificate'])
    section = AcquiredAffineSection(S, C, A, random.Random(2026102828))
    exported = section.export_section()
    U, M = section.U, section.M
    D0 = rectangular_unpack(section.D0, U, M)
    D0_span = BinaryCoordinates(pack(product(unpack(a, U), D0), U)
                               for a in A['multiplier_basis'])
    dual = BinaryCoordinates(C['dual_reverse_matrices'])
    assert len(D0_span.basis) == len(dual.basis)
    for d in dual.basis: D0_span.coordinates(d)
    for j in range(M):
        assert section.D0_inverse.coordinates(apply_binary(D0, 1 << j)) == 1 << j

    h0 = rectangular_unpack(apply_binary(C['hom_basis'], C['affine_hom_offset']), M, U)
    delta = [a ^ b for a, b in zip(section.H_actual, h0)]
    endomorphism = BinaryCoordinates(C['endomorphism_basis'])
    for d in C['dual_reverse_matrices']:
        composition = pack(product(rectangular_unpack(d, U, M), delta), U)
        assert (endomorphism.coordinates(composition) & C['trace_functional']).bit_count() % 2 == 0

    # Independent literal-gate extraction of every coefficient of the
    # composed degree-at-most-two marked map: zero, singletons, and pairs.
    probes = [0] + [1 << j for j in range(M)]
    probes += [(1 << i) | (1 << j) for i in range(M) for j in range(i)]
    initial_wires = native['reversible_certificate']['initial_wires']
    for y in probes:
        x = exported['original_input_offset'] ^ apply_binary(exported['original_input_columns'], y)
        wires = literal_wires(program, x)
        marked = sum(wires[wire] << i for i, wire in enumerate(initial_wires))
        expected = exported['marked_output_constant'] ^ apply_binary(exported['marked_output_columns'], y)
        assert marked == expected
    witness = section.witness(native['target'])
    assert witness['satisfiable']
    assert literal_wires(program, witness['assignment'])[program['output']] == 1

    # Check the joint module ordering directly on every actual multiplier:
    # its first-row coordinate matrix must have identical repeated blocks.
    Q = section.Q
    F = Q.F
    start = 0
    actions_checked = 0
    for item in A['components']:
        s, h = item['matrix_degree'], item['natural_multiplicity']
        for packed in item['factor_basis']:
            action = unpack(packed, U)
            rows = []
            for j in range(Q.d):
                u = apply_binary(section.module_columns, F.one << (Q.a*j))
                image = section.module_inverse.coordinates(apply_binary(action, u))
                assert image >> (Q.a*Q.d) == 0
                rows.append(Q.matrix(image, 1, Q.d)[0])
            block = [row[start:start+s] for row in rows[start:start+s]]
            expected = [[0]*Q.d for _ in range(Q.d)]
            for copy in range(h):
                for i in range(s):
                    for j in range(s): expected[start+copy*s+i][start+copy*s+j] = block[i][j]
            assert rows == expected
            actions_checked += 1
        start += s*h
    assert start == Q.d
    out = dict(passed=True, reviewed_code_sha256=hashlib.sha256((SECTION/'acquired_affine_section.py').read_bytes()).hexdigest(),
        reviewed_proof_sha256=hashlib.sha256((SECTION/'ACQUIRED_AFFINE_RIGHT_INVERSE.tex').read_bytes()).hexdigest(),
        input_fixture='e6_distinct_targets_native_n72.json', original_input_bits=program['inputs'],
        original_gates=len(program['gates']), reused_raw_acquisition=True,
        invertible_dual_map_manufactured_again=True, dual_equals_A_D0_checked=True,
        actual_reduced_trace_annihilator_checks=len(C['dual_reverse_matrices']),
        joint_repeated_block_actions_checked=actions_checked,
        independent_literal_gate_coefficient_probes=len(probes),
        independent_output_bits=M, original_marked_bits=len(initial_wires),
        all_target_identity_certified_by_degree_two=True,
        native_positive_witness=witness['assignment'], native_positive_original_gate_passed=True,
        seed=2026102828, seconds=time.perf_counter()-started)
    (HERE/'affine_section_independent_review_results.json').write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps(out, indent=2))


if __name__ == '__main__': main()
