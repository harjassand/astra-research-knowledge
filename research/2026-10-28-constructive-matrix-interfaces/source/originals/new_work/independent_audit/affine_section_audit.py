#!/usr/bin/env python3
"""Independent original-gate and all-target audits of the affine section.

Fixture coordinates are used only to generate test inputs/reference checks.
The production entry receives the ordinary DAG alone.
"""
from pathlib import Path
import copy
import json
import random
import time
from acquired_affine_section import *
from raw_bilinear_product_checks import (
    FixtureField, rectangular_forms, compose_quadratic, source_free_program)
from matrix_target_geometry import matrix_geometry_target

HERE = Path(__file__).resolve().parent


def literal_gate_wires(program, assignment):
    """Separate gate evaluator; no polynomial or acquired-coordinate use."""
    n = program.get('inputs', program.get('n'))
    values = [(assignment >> j) & 1 for j in range(n)]
    for gate in program['gates']:
        op = gate['op']
        args = gate.get('args', ())
        if op == 'const':
            bit = gate['value']
        elif op == 'not':
            bit = 1 ^ values[args[0]]
        elif op == 'and':
            bit = values[args[0]] & values[args[1]]
        elif op == 'or':
            bit = values[args[0]] | values[args[1]]
        elif op == 'xor':
            bit = values[args[0]] ^ values[args[1]]
        else:
            raise ValueError('unknown original gate operation')
        values.append(bit)
    return values


def native_checks():
    files = [
        'work_trace_frontier/noncommutative_dual_native_small.json',
        'work_trace_frontier/noncommutative_dual_native_a2_s2_h2_p2.json',
        'work_trace_frontier/noncommutative_affine_native_a1_s3_h2_p3.json',
        'work_trace_frontier/noncommutative_affine_native_a2_s2_h2_p2.json',
        'work_matrix_root/matrix_geometry_native_two_factors_n72.json',
        'work_matrix_root/matrix_affine_flag_native_n72.json',
        'work_phase_diamond/matrix_affine_diamond_native_n72.json']
    records = []
    for index, relative in enumerate(files):
        program = json.loads((SNAPSHOT / relative).read_text())
        section, result = acquire_native_section(program, random.Random(949100+index))
        rev = acquire_reversible_terminal_and(program)
        wires = literal_gate_wires(program, result['witness']['assignment'])
        assert wires[program['output']] == 1
        width = section.N['marked_quadratics']
        targets = (list(range(1 << width)) if index == 0 else
                   [0, (1 << width)-1] +
                   [random.Random(949400+index*100+j).getrandbits(width)
                    for j in range(32)])
        targets_checked = 0
        geometry_declines = 0
        obsolete_offset_fails = 0
        points = []
        exported = section.export_section()
        for target in targets:
            witness = section.witness(target)
            if not witness['satisfiable']:
                continue
            wires = literal_gate_wires(program, witness['assignment'])
            obtained = sum(wires[wire] << j for j, wire in enumerate(rev['initial_wires']))
            assert obtained == target, (relative, target, obtained)
            rhs = target ^ section.N['output_constant']
            y = sum(((rhs >> j) & 1) << i
                    for i, j in enumerate(section.N['output_basis_mark_indices']))
            assert witness['assignment'] == exported['original_input_offset'] ^ apply_binary(
                exported['original_input_columns'], y)
            try:
                matrix_geometry_target(section.C, section.compression, target, section.offset)
            except ValueError:
                geometry_declines += 1
            obsolete = section.split['affine_offset'] ^ apply_binary(
                section.split['coordinate_columns'], witness['local_assignment'])
            bad_wires = literal_gate_wires(program, obsolete)
            bad_target = sum(bad_wires[wire] << j for j, wire in enumerate(rev['initial_wires']))
            obsolete_offset_fails += bad_target != target
            targets_checked += 1
            if len(points) < 3:
                points.append(witness)
        records.append(dict(source=relative, original_inputs=result['original_input_bits'],
            ordinary_gates=result['ordinary_gates'], original_boolean_output_verified=True,
            literal_original_register_targets_verified=targets_checked,
            old_homogeneous_geometry_declines=geometry_declines,
            left_input_shift=section.C.get('left_input_shift', 0),
            outside_actual_right_image=not section.C.get('affine_offset_in_actual_right_input', True),
            obsolete_polar_offset_failing_targets=obsolete_offset_fails,
            acquisition_seconds=result['acquisition_seconds'],
            affine_section=exported, section_stats=section.stats, example_witnesses=points))
        print(json.dumps({key: value for key, value in records[-1].items()
                          if key not in ('affine_section', 'section_stats', 'example_witnesses')}), flush=True)
    return records


def fixture(poly, p, s, h, phase_word, seed, dependent_output=False):
    """All native affine phases, with an independent left shift and hiding."""
    F = FixtureField(poly)
    a = F.a
    d = s*h
    constraints = [xor_all(1 << (a*((block*s+i)*d+block*s+j)+ell)
                           for block in range(h))
                   for i in range(s) for j in range(s) for ell in range(a)]
    W = affine_solutions([(row, 0) for row in constraints], a*d*d)[1]
    Y0 = sum(((phase_word >> (a*(i*s+j)+ell)) & 1) << (a*(i*d+j)+ell)
             for i in range(s) for j in range(s) for ell in range(a))
    forms, _ = rectangular_forms(F, p, d, d)
    left = a*p*d
    embedding = [1 << j for j in range(left)] + [word << left for word in W]
    n = len(embedding)
    rng = random.Random(seed)
    initial_offset = rng.getrandbits(left) | (Y0 << left)
    marks = [compose_quadratic(form, initial_offset, embedding) for form in forms]
    columns = [1 << j for j in range(n)]
    for _ in range(5*n):
        i, j = rng.sample(range(n), 2)
        columns[i] ^= columns[j]
    affine_offset = rng.getrandbits(n)
    marks = [compose_quadratic(form, affine_offset, columns) for form in marks]
    mix = [1 << j for j in range(len(marks))]
    for _ in range(5*len(marks)):
        i, j = rng.sample(range(len(marks)), 2)
        mix[i] ^= mix[j]
    original = marks
    marks = [set() for _ in mix]
    for j, row in enumerate(mix):
        for i, form in enumerate(original):
            if row >> i & 1:
                marks[j] ^= form
    if dependent_output:
        marks.append(marks[0] ^ marks[1] ^ {0})
    return marks, n


def new_affine_checks():
    records = []
    cases = [(3,2,2,2,phase,True) for phase in range(16)]
    cases += [(3,2,2,3,9,False), (3,2,1,4,1,False), (7,2,2,2,219,True)]
    for index, (poly,p,s,h,phase,dependency) in enumerate(cases):
        marks, n = fixture(poly,p,s,h,phase,950000+index,dependency)
        # Choose a consistent target using a literal fixture assignment.
        probe = 0
        target = sum((sum((probe & monomial) == monomial for monomial in form) % 2) << i
                     for i, form in enumerate(marks))
        program = source_free_program(marks,n,target,40,950100+index)
        section, result = acquire_native_section(program,random.Random(950200+index))
        rev = acquire_reversible_terminal_and(program)
        values = literal_gate_wires(program,result['witness']['assignment'])
        assert values[program['output']] == 1
        free_width = section.M
        checked = refused = bad_offset = 0
        # Entire output space on binary small cases, bounded witnesses on F4.
        ys = range(1 << free_width) if free_width <= 12 else [0]+[
            random.Random(950300+index*100+j).getrandbits(free_width) for j in range(64)]
        exported = section.export_section()
        dependency_violation = None
        if dependency:
            output_span = BinaryCoordinates(exported['marked_output_columns'])
            for j in range(exported['marked_output_bits']):
                try:
                    output_span.coordinates(1 << j)
                except ValueError:
                    dependency_violation = 1 << j
                    break
            assert dependency_violation is not None
        for y in ys:
            target = exported['marked_output_constant'] ^ apply_binary(exported['marked_output_columns'],y)
            answer = section.witness(target)
            assert answer['satisfiable']
            values = literal_gate_wires(program,answer['assignment'])
            got = sum(values[wire] << j for j,wire in enumerate(rev['initial_wires']))
            assert got == target
            if dependency:
                assert not section.witness(target ^ dependency_violation)['satisfiable']
                refused += 1
            obsolete = section.split['affine_offset'] ^ apply_binary(
                section.split['coordinate_columns'],answer['local_assignment'])
            bad_values=literal_gate_wires(program,obsolete)
            bad_target=sum(bad_values[wire] << j for j,wire in enumerate(rev['initial_wires']))
            bad_offset += bad_target != target
            checked += 1
        records.append(dict(field_polynomial=poly,p=p,s=s,h=h,phase=phase,
            original_inputs=n,ordinary_gates=len(program['gates']),
            targets_verified_through_original_gates=checked,
            inconsistent_dependencies_declined=refused,
            nonzero_left_shift=bool(section.C.get('left_input_shift',0)),
            outside_actual_right_image=not section.C.get('affine_offset_in_actual_right_input',True),
            obsolete_polar_offset_failing_targets=bad_offset,
            affine_section=exported,section_stats=section.stats))
        if index == 9:
            (HERE/'section_affine_native20.json').write_text(json.dumps(program,indent=2)+'\n')
        (HERE/'affine_section_new_cases_checkpoint.json').write_text(
            json.dumps(records,indent=2)+'\n')
        print(json.dumps({key:value for key,value in records[-1].items()
                          if key not in ('affine_section','section_stats')}),flush=True)
    return records


def main():
    began=time.perf_counter()
    native=native_checks()
    (HERE/'affine_section_native_checkpoint.json').write_text(
        json.dumps(native,indent=2)+'\n')
    affine=new_affine_checks()
    result=dict(passed=True,native_cases=native,new_affine_cases=affine,
                original_gate_target_checks=sum(r['literal_original_register_targets_verified'] for r in native)
                    +sum(r['targets_verified_through_original_gates'] for r in affine),
                theoretical_operation='all-target affine right inverse, not uniform fiber sampling',
                seconds=time.perf_counter()-began)
    (HERE/'affine_section_audit_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({key:value for key,value in result.items()
                      if key not in ('native_cases','new_affine_cases')}),flush=True)


if __name__=='__main__':
    main()
