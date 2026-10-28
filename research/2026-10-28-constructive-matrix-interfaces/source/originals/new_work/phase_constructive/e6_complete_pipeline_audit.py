#!/usr/bin/env python3
"""One raw acquisition, E6 count, affine section, and admitted exact sampler.

The native fixture is an ordinary Boolean gate DAG.  All consumers reuse the
same acquired certificates.  Character sampling is used only after the actual
description-byte budget admits its 2**codimension cost.  This is an integration
audit, not a comparative benchmark or a sampling theorem for growing E6
codimension.  No recovered source file is modified.
"""
from pathlib import Path
import hashlib
import json
import random
import sys
import time

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
SECTION = HERE.parent / 'independent_audit'
SAMPLER = HERE.parent / 'affine_sampler'
sys.path[:0] = [str(HERE), str(SECTION), str(SAMPLER)]
from e6_phase_counter import count_affine_e6_native
from acquired_affine_section import AcquiredAffineSection
from affine_slice_prefix_sampler import AcquiredAffineSliceSampler, apply_binary


def literal_wires(program, assignment):
    """Separate literal interpreter; no acquired algebra or count routine."""
    wires = [(assignment >> i) & 1 for i in range(program['inputs'])]
    for gate in program['gates']:
        op = gate['op']
        if op == 'const':
            value = gate['value']
        elif op == 'xor':
            value = 0
            for argument in gate['args']:
                value ^= wires[argument]
        elif op == 'and':
            value = 1
            for argument in gate['args']:
                value &= wires[argument]
        else:
            raise ValueError('literal audit does not implement ' + op)
        wires.append(value)
    return wires


def hash_file(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    started = time.perf_counter()
    fixture = HERE / 'e6_distinct_targets_native_n72.json'
    original_bytes = fixture.read_bytes()
    program = json.loads(original_bytes)
    compact_bytes = len(json.dumps(program, separators=(',', ':')).encode())

    # Exactly one invocation of a native acquisition entry point.
    then = time.perf_counter()
    result = count_affine_e6_native(program)
    recognition_count_seconds = time.perf_counter() - then
    split = result['split_certificate']
    C = result['affine_slice_certificate']
    compression = result['compression_certificate']
    target = result['target']
    assert result['description_bytes'] == compact_bytes
    assert result['ones'] == 71228562270584832
    initial_wires = result['reversible_certificate']['initial_wires']

    def check_original(draw):
        assignment = draw['assignment']
        assert 0 <= assignment < 1 << program['inputs']
        wires = literal_wires(program, assignment)
        marked = sum(wires[wire] << i for i, wire in enumerate(initial_wires))
        assert marked == target
        assert wires[program['output']] == 1
        return dict(assignment=assignment, marked_target=marked,
                    original_output=wires[program['output']],
                    original_gate_interpreter_passed=True)

    then = time.perf_counter()
    section = AcquiredAffineSection(split, C, compression, random.Random(2026102831))
    section_seconds = time.perf_counter() - then
    then = time.perf_counter()
    section_witness = section.witness(target)
    assert section_witness['satisfiable']
    witness_record = check_original(section_witness)
    section_witness_seconds = time.perf_counter() - then

    # Budget is checked before constructing or invoking the exponential-in-c
    # sampler.  Both raw file bytes and the smaller compact DAG suffice here.
    character_budget = 1 << C['codimension']
    assert character_budget <= len(original_bytes)
    assert character_budget <= compact_bytes
    then = time.perf_counter()
    sampler = AcquiredAffineSliceSampler(split, C, target, random.Random(2026102832))
    sampler_construction_seconds = time.perf_counter() - then
    assert sampler.split is split and sampler.C is C
    assert sampler.population == sampler.count['population'] == result['ones']
    assert sampler.engine.population == result['ones']
    assert sampler.engine.c == C['codimension']
    assert sampler.coords.a * sampler.coords.d * (sampler.coords.p + sampler.coords.r) - C['codimension'] == program['inputs']

    draws = []
    first = None
    for _ in range(2):
        then = time.perf_counter()
        draw = sampler.sample()
        draw_seconds = time.perf_counter() - then
        then = time.perf_counter()
        record = check_original(draw)
        record.update(draw_seconds=draw_seconds,
                      original_gate_check_seconds=time.perf_counter() - then)
        draws.append(record)
        if first is None:
            first = draw

    then = time.perf_counter()
    Q = sampler.coords
    # Use one complete acquired row and one bit of the next.  These are
    # translated to actual original-input affine equations, possibly dense.
    yword = apply_binary(Q.hom_columns, first['full_hom_coordinates'])
    row_bits = Q.a * Q.r
    used = min(Q.a * Q.d * Q.r, row_bits + 1)
    row_count, partial_bits = divmod(used, row_bits)
    rows = [[(yword >> (Q.a * (i * Q.r + j))) & (Q.F.q - 1)
             for j in range(Q.r)] for i in range(row_count)]
    partial = (yword >> (row_count * row_bits)) & ((1 << partial_bits) - 1)
    constraints = sampler.prefix_constraints_on_original(rows, partial, partial_bits)
    assert len(constraints) == used
    assert all(((mask & first['assignment']).bit_count() & 1) == rhs
               for mask, rhs in constraints)
    prefix_population = sampler.engine.count_prefix(rows, partial, partial_bits)
    assert 0 < prefix_population <= sampler.population
    # A substantive local completion check: the two next-bit children add
    # exactly to the prefix population, and the actual sampled child is positive.
    assert partial_bits < row_bits
    child_populations = [sampler.engine.count_prefix(
        rows, partial | (bit << partial_bits), partial_bits + 1) for bit in (0, 1)]
    assert sum(child_populations) == prefix_population
    actual_next = (yword >> used) & 1
    assert child_populations[actual_next] > 0
    prefix_seconds = time.perf_counter() - then

    source_files = [fixture, Path(__file__), HERE/'e6_phase_counter.py',
                    HERE/'TWO_FACTOR_ARBITRARY_TARGET_PHASE_THEOREM.tex',
                    SECTION/'acquired_affine_section.py',
                    SECTION/'ACQUIRED_AFFINE_RIGHT_INVERSE.tex',
                    SAMPLER/'affine_slice_prefix_sampler.py',
                    SAMPLER/'ACQUIRED_AFFINE_SLICE_CONSTRUCTIVE_THEOREM.tex']
    output = dict(
        passed=True,
        fixture=fixture.name,
        native_acquisition_calls=1,
        source_hashes={str(path.relative_to(HERE.parent)): hash_file(path) for path in source_files},
        original_input_bits=program['inputs'],
        ordinary_gates=len(program['gates']),
        total_wires=program['inputs'] + len(program['gates']),
        auxiliary_independent_inputs=0,
        actual_file_bytes=len(original_bytes),
        compact_original_description_bytes=compact_bytes,
        binary_codimension=C['codimension'],
        original_dual_characters=character_budget,
        character_budget_checked_before_sampler=True,
        description_bounded_character_sampling_admitted=True,
        acquired_certificates_reused_for_all_consumers=True,
        e6_count=result['ones'],
        generic_character_count=sampler.count['population'],
        prefix_engine_count=sampler.engine.population,
        e6_equals_generic_character_count=True,
        e6_histogram_states=result['fiber']['histogram_states'],
        affine_section_statistics=section.stats,
        affine_section_witness=witness_record,
        affine_section_export=section.export_section(),
        sampler_coordinate_statistics=sampler.coords.stats,
        exact_sampling_method='positive completion-count branching, then uniform affine left fiber',
        uniformity_status='algorithmic theorem; this audit checks integration and valid original assignments, not empirical uniformity',
        sample_draws=draws,
        acquired_prefix=dict(complete_rows=rows, partial_word=partial,
                             partial_bits=partial_bits,
                             original_input_equations=constraints,
                             tested_assignment=first['assignment'],
                             original_equations_satisfied=True,
                             population=prefix_population,
                             next_bit_child_populations=child_populations,
                             child_populations_sum_to_parent=True),
        sampler_statistics=sampler.stats,
        prefix_engine_statistics=sampler.engine.stats,
        timing_seconds=dict(recognition_and_e6_count=recognition_count_seconds,
                            affine_section_construction=section_seconds,
                            section_witness_and_original_gate_check=section_witness_seconds,
                            sampler_coordinates_and_character_preprocessing=sampler_construction_seconds,
                            sample_draws=sum(x['draw_seconds'] for x in draws),
                            sample_original_gate_checks=sum(x['original_gate_check_seconds'] for x in draws),
                            prefix_export_and_partition_checks=prefix_seconds,
                            total=time.perf_counter() - started),
        scope=dict(one_actual_ordinary_circuit=True,
                   e6_counting_does_not_enumerate_characters=True,
                   sampler_cost='2^c times a polynomial; admitted here because 2^c <= actual description bytes',
                   polynomial_sampling_for_linearly_growing_c_claim=False,
                   arbitrary_original_input_pinning_claim=False,
                   comparative_performance_claim=False))
    destination = HERE / 'e6_complete_pipeline_audit_results.json'
    destination.write_text(json.dumps(output, indent=2) + '\n')
    print(json.dumps({key: output[key] for key in (
        'passed', 'native_acquisition_calls', 'original_input_bits', 'ordinary_gates',
        'total_wires', 'binary_codimension', 'actual_file_bytes',
        'compact_original_description_bytes', 'e6_count', 'generic_character_count',
        'character_budget_checked_before_sampler', 'timing_seconds')}, indent=2))


if __name__ == '__main__':
    main()
