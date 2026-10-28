#!/usr/bin/env python3
"""Independent finite-field subspaces, literal dual matrices, and raw-DAG checks."""
from collections import Counter
from pathlib import Path
import itertools
import json
import random
import sys
import time

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import e6_phase_counter as E
from phase_diamond import affine_matrix_diamond_target
from phase_diamond_audit import subspaces
from matrix_geometry_independent_audit import (
    Field, column_span, matrix_columns, matrix_from_word, multiply, matrix_rank)
from matrix_target_geometry_checks import (
    repeated_matrix_factors_fixture, mix_target, source_free_program,
    binary_factor_left_oracle, prepared_program, apply_binary,
    FixtureField, rectangular_value)
from complete_target_geometry_checks import direct_character_histogram
from unsaturated_bilinear_counter import slice_target_fiber, affine_solutions


def compositions(total, length):
    if length == 1:
        yield (total,)
    else:
        for first in range(total+1):
            for tail in compositions(total-first, length-1):
                yield (first,) + tail


def flags_from_grid(grid):
    k = sum(grid)
    flags = [[], [], [], []]  # E1,F1,E2,F2
    position = 0
    for cell, count in enumerate(grid):
        i, j = divmod(cell, 3)
        for _ in range(count):
            vector = tuple(int(v == position) for v in range(k))
            if i < 2: flags[0].append(vector)
            if i == 0: flags[1].append(vector)
            if j < 2: flags[2].append(vector)
            if j == 0: flags[3].append(vector)
            position += 1
    return flags


def geometry_audit():
    records = []
    for modulus, largest in ((3, 4), (7, 3), (11, 3)):
        F = Field(modulus)
        for k in range(largest+1):
            all_J = subspaces(F, k)
            cases = comparisons = profiles = 0
            # Include every canonical pair-of-flags orbit with E1+E2=R.
            for first in compositions(k, 8):
                grid = first + (0,)
                flags = flags_from_grid(grid)
                literal = Counter()
                for J in all_J:
                    stats = (len(J),) + tuple(len(J)+len(S)-len(column_span(F, tuple(J)+tuple(S), k)) for S in flags)
                    literal[stats] += 1
                acquired, count = E.two_flag_subspace_census(grid, F.a)
                assert acquired == dict(literal), (modulus, grid, acquired, dict(literal))
                cases += 1
                comparisons += len(set(acquired) | set(literal))
                profiles += count
            records.append(dict(field_order=F.q, ambient_dimension=k,
                canonical_pair_flag_types=cases, actual_subspaces_per_case=len(all_J),
                census_coefficients_compared=comparisons, multiplicity_profiles=profiles))
    return records


def field_kernel(F, matrix):
    n = len(matrix[0])
    work = [list(row) for row in matrix]
    pivots = []
    for j in range(n):
        pivot = next((i for i in range(len(pivots), len(work)) if work[i][j]), None)
        if pivot is None: continue
        i = len(pivots)
        work[i], work[pivot] = work[pivot], work[i]
        scale = F.inv(work[i][j])
        work[i] = [F.mul(scale, v) for v in work[i]]
        for r in range(len(work)):
            if r != i and work[r][j]:
                factor = work[r][j]
                work[r] = [x ^ F.mul(factor, y) for x, y in zip(work[r], work[i])]
        pivots.append(j)
    answer = []
    for j in range(n):
        if j in pivots: continue
        vector = [int(i == j) for i in range(n)]
        for row, pivot in enumerate(pivots): vector[pivot] = work[row][j]
        answer.append(vector)
    return answer


def binary_expansion(F, vectors):
    return E.canonical_binary_span(sum(F.mul(scalar, value) << (F.a*j) for j, value in enumerate(v))
        for v in vectors for scalar in (1 << bit for bit in range(F.a)))


def literal_affine_histogram(F, targets, phases, multiplicities):
    distributions = []
    total_local = 0
    for C, Q, h in zip(targets, phases, multiplicities):
        s = len(Q)
        counts = Counter()
        for word in range(F.q**(s*s)):
            A = matrix_from_word(F, word, s, s)
            phase = 0
            for i in range(s):
                for j in range(s): phase ^= F.trace(F.mul(Q[i][j], A[j][i]))
            image = column_span(F, matrix_columns(multiply(F, C, A)), len(C))
            counts[h*matrix_rank(F, A), image] += -1 if phase else 1
        distributions.append({key: value for key, value in counts.items() if value})
        total_local += F.q**(s*s)
    histogram = Counter()
    for (r1, J1), n1 in distributions[0].items():
        for (r2, J2), n2 in distributions[1].items():
            rho = len(column_span(F, J1+J2, len(targets[0])))
            histogram[r1+r2, rho] += n1*n2
    return {key: value for key, value in histogram.items() if value}, total_local


def field_histogram_audit():
    rng = random.Random(2026102801)
    records = []
    for modulus in (3, 7, 11):
        F = Field(modulus)
        for case in range(12):
            p = 3 if case < 8 else 2
            s = 2
            if case == 0:
                targets = [[[1, 0], [0, 1], [0, 0]], [[0, 0], [1, 0], [0, 1]]]
                phases = [[[0, 0], [0, 1]], [[1, 0], [0, 0]]]
            else:
                targets = [[[rng.randrange(F.q) for _ in range(s)] for _ in range(p)] for _ in range(2)]
                phases = [[[rng.randrange(F.q) for _ in range(s)] for _ in range(s)] for _ in range(2)]
            multiplicities = [2, 1+(case % 3)]
            components = []
            for C, Q, h in zip(targets, phases, multiplicities):
                image = column_span(F, matrix_columns(C), p)
                kernel = field_kernel(F, Q)
                phase_image = []
                for v in kernel:
                    column = [0]*p
                    for i in range(p):
                        for j in range(s): column[i] ^= F.mul(C[i][j], v[j])
                    phase_image.append(column)
                components.append(dict(target_rows=binary_expansion(F, image),
                    phase_kernel_rows=binary_expansion(F, phase_image), matrix_degree=s,
                    natural_multiplicity=h, phase_rank=matrix_rank(F, Q)))
            actual, certificate = E.affine_e6_histogram(components, F.a, F.a)
            reference, local = literal_affine_histogram(F, targets, phases, multiplicities)
            assert actual == reference, (modulus, case, actual, reference)
            records.append(dict(field_order=F.q, case=case, targets=targets, phases=phases,
                local_matrices_enumerated=local, certificate=certificate))
    return records


def positive_gate_checks(program, planted, target, count=32):
    """Audit-only planted linear solve, followed by evaluation of original gates.

    These are positive checks, avoiding the weak test of only random inputs
    to a circuit with a rare accepting output. This is not a sampler claim.
    """
    rng = random.Random(2026102899)
    n = program['inputs']
    evaluate, _, _ = prepared_program(program, n)
    F = FixtureField(3)
    embedding = planted['right_embedding']
    inverse_input = E.BinaryCoordinates(planted['input_columns'])
    answers = []
    attempts = 0
    while len(answers) < count:
        attempts += 1
        X = rng.getrandbits(16)
        columns = [rectangular_value(F, 2, 8, 8, X | (v << 16)) for v in embedding]
        constant = rectangular_value(F, 2, 8, 8, X | (planted['right_affine_offset'] << 16))
        equations = [(sum(((column >> j) & 1) << v for v, column in enumerate(columns)),
                      ((target ^ constant) >> j) & 1) for j in range(16)]
        try:
            particular, kernel = affine_solutions(equations, len(embedding))
        except ValueError:
            continue
        if particular is None:
            continue
        right = particular ^ apply_binary(kernel, rng.getrandbits(len(kernel)))
        z = X | (right << 16)
        original = inverse_input.coordinates(z ^ planted['input_offset'])
        assert original < 1 << n and evaluate(original) == 1
        answers.append(original)
    return dict(original_assignments=answers, positive_original_gate_evaluations=count,
                left_trials=attempts, purpose='independent positive fixture audit; no uniformity claim')


def native_audit():
    rng = random.Random(2026102802)
    right_offset = (1 << 9) | (1 << 36)
    marks, n, planted = repeated_matrix_factors_fixture(3, 2, 2, 2, 2026102803,
                                                     right_offset=right_offset)
    # Two different target lines, so the recovered common-carrier consumer
    # rejects. The two target matrices are each within one joint simple copy.
    target = (1 << 0) | (1 << 12)
    desired = mix_target(planted, target)
    program = source_free_program(marks, n, desired, 500, 2026102804)
    (HERE/'e6_distinct_targets_native_n72.json').write_text(json.dumps(program, indent=2)+'\n')
    result = E.count_affine_e6_native(program)
    C, A = result['affine_slice_certificate'], result['compression_certificate']
    # source_free_program shifts the quadratic frontier by known constants
    # before its reversible suffix. Recover that correspondence from the
    # actual ANFs when changing the target in this independent audit.
    target_conversion = []
    for frontier in result['reversible_certificate']['initial_quadratics']:
        frontier = set(frontier)
        matches = [j for j, original in enumerate(marks)
                   if frontier - {0} == set(original) - {0}]
        assert len(matches) == 1
        j = matches[0]
        target_conversion.append((j, int(0 in frontier) ^ int(0 in marks[j])))
    def convert_target(original):
        return sum((((original >> j) & 1) ^ shift) << i
                   for i, (j, shift) in enumerate(target_conversion))
    assert convert_target(desired) == result['target']
    try:
        affine_matrix_diamond_target(C, A, result['target'], C['affine_hom_offset'])
    except ValueError as error:
        old_decline = str(error)
        assert 'target carriers do not coincide' in old_decline
    else:
        raise AssertionError('supposed new target geometry was already admitted by diamonds')
    expected, oracle = binary_factor_left_oracle(2, 2, 2, target, right_offset)
    assert result['ones'] == expected
    evaluate, _, _ = prepared_program(program, n)
    for _ in range(128):
        x = rng.getrandbits(n)
        z = apply_binary(planted['input_columns'], x) ^ planted['input_offset']
        full = (z & ((1 << 16)-1)) | ((apply_binary(planted['right_embedding'], z >> 16) ^ right_offset) << 16)
        assert evaluate(x) == int(rectangular_value(FixtureField(3), 2, 8, 8, full) == target)
    positive = positive_gate_checks(program, planted, target)
    phases = []
    for word in range(256):
        offset = affine_solutions([(row, (word >> j) & 1) for j, row in enumerate(C['right_annihilator_basis'])], len(C['hom_basis']))[0]
        counted = E.affine_matrix_e6_target(C, A, result['target'], offset)
        assert counted['rank_pair_histogram'] == direct_character_histogram(C, A, result['target'], offset)
        assert counted['population'] == slice_target_fiber(C, result['target'], offset)['population']
        phases.append(dict(phase_word=word, population=counted['population']))
    target_cases = []
    for c1 in range(16):
        for c2 in range(16):
            literal_target = sum(((c1 >> (i*2+j)) & 1) << (i*8+j) for i in range(2) for j in range(2))
            literal_target |= sum(((c2 >> (i*2+j)) & 1) << (i*8+4+j) for i in range(2) for j in range(2))
            actual_target = convert_target(mix_target(planted, literal_target))
            offset = rng.randrange(1 << len(C['hom_basis']))
            counted = E.affine_matrix_e6_target(C, A, actual_target, offset)
            assert counted['rank_pair_histogram'] == direct_character_histogram(C, A, actual_target, offset)
            assert counted['population'] == slice_target_fiber(C, actual_target, offset)['population']
            target_cases.append(dict(target1=c1, target2=c2, offset=offset,
                                     population=counted['population']))
    return dict(fixture='e6_distinct_targets_native_n72.json', result=result,
        old_diamond_decline=old_decline, independent_original_left_oracle=oracle,
        original_gate_evaluations=128, positive_gate_checks=positive, all_256_phase_words=phases,
        all_256_target_pairs_with_independent_phases=target_cases, planted_fixture=planted,
        comparative_runtime_claim=False)


def formula_growth():
    """Large-field formula execution, explicitly without raw acquisition."""
    started = time.perf_counter()
    s, a = 6, 17
    d, ap = 4*s, a*s
    # Standard actual right-simple-module blocks have ap binary dimensions
    # each. Only their coordinate submodule labels are manufactured here;
    # no raw DAG or hidden-algebra acquisition is claimed by this test.
    def rows(indices):
        return [1 << (ap*j+bit) for j in indices for bit in range(ap)]
    components = [
        dict(target_rows=rows((0, 1, 2, 3)), phase_kernel_rows=rows((0, 2)),
             matrix_degree=s, natural_multiplicity=2, phase_rank=4),
        dict(target_rows=rows((2, 3, 4, 5)), phase_kernel_rows=rows((3, 5)),
             matrix_degree=s, natural_multiplicity=2, phase_rank=4)]
    histogram, certificate = E.affine_e6_histogram(components, a, ap)
    total = sum(weight*E.signed_universal_product(s, d, d, a, 6, t, rho)
                for (t, rho), weight in histogram.items())
    answer, remainder = divmod(total, 1 << (2*a*s*s))
    assert remainder == 0 and answer >= 0
    return dict(raw_acquisition_performed=False, formula_only=True,
        field_order=1 << a, field_degree=a, matrix_degree=s,
        parameter_original_input_bits=18*a*s*s, codimension=2*a*s*s,
        answer_bits=answer.bit_length(), population=answer,
        certificate=certificate, seconds=time.perf_counter()-started)


def main():
    started = time.perf_counter()
    out = dict(catalogue_types=len(E.TYPES), positive_roots=len(E.ROOTS),
               catalogue=[dict(**T, base_grid=E.TYPE_GRIDS[i], statistics=E.TYPE_STATS[i]) for i, T in enumerate(E.TYPES)],
               hom_table=E.HOM)
    (HERE/'e6_catalogue.json').write_text(json.dumps(out, indent=2)+'\n')
    out['geometry'] = geometry_audit()
    print(json.dumps(dict(event='geometry_passed', pair_flag_types=sum(x['canonical_pair_flag_types'] for x in out['geometry']),
                          coefficients=sum(x['census_coefficients_compared'] for x in out['geometry']))), flush=True)
    (HERE/'e6_phase_audit_results.json').write_text(json.dumps(out, indent=2)+'\n')
    out['literal_field_histograms'] = field_histogram_audit()
    print(json.dumps(dict(event='literal_field_histograms_passed', cases=len(out['literal_field_histograms']))), flush=True)
    (HERE/'e6_phase_audit_results.json').write_text(json.dumps(out, indent=2)+'\n')
    out['formula_growth'] = formula_growth()
    (HERE/'e6_formula_growth.json').write_text(json.dumps(out['formula_growth'], indent=2)+'\n')
    out['native'] = native_audit()
    out['all_assertions_passed'] = True
    out['seconds'] = time.perf_counter()-started
    (HERE/'e6_phase_audit_results.json').write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps(dict(event='all_passed', seconds=out['seconds'],
        native_count=out['native']['result']['ones'], native_gates=out['native']['result']['ordinary_gates'],
        original_inputs=out['native']['result']['original_input_bits'])), flush=True)


if __name__ == '__main__':
    main()
