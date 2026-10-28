#!/usr/bin/env python3
"""Rebase the acquired F4 center so its identity word is 2, not 1."""
import copy
import json
import random
from affine_section_audit import *


def main():
    path = SNAPSHOT/'work_trace_frontier/noncommutative_affine_native_a2_s2_h2_p2.json'
    program = json.loads(path.read_text())
    initial, raw = acquire_native_section(program, random.Random(950404))
    C = copy.deepcopy(initial.C)
    algebra = C['nucleus']['nucleus_certificate']
    algebra['center_basis'].reverse()
    Z = BinaryCoordinates(algebra['center_basis'])
    table = algebra['multiplication_table']
    def mul(x, y):
        return apply_binary([apply_binary(row, y) for row in table], x)
    algebra['center_frobenius_columns'] = [Z.coordinates(mul(z,z))
                                         for z in algebra['center_basis']]
    section = AcquiredAffineSection(initial.split,C,initial.compression,random.Random(950405))
    assert section.Q.F.one == 2
    E = section.export_section()
    rev = acquire_reversible_terminal_and(program)
    for i, form in enumerate(rev['initial_quadratics']):
        observed = compose_quadratic(set(form), E['original_input_offset'], E['original_input_columns'])
        expected = {0} if E['marked_output_constant'] >> i & 1 else set()
        expected ^= {1 << j for j, column in enumerate(E['marked_output_columns']) if column >> i & 1}
        assert observed == expected
    points = [raw['target']] + [random.Random(950406+j).getrandbits(section.N['marked_quadratics'])
                                for j in range(32)]
    for target in points:
        witness = section.witness(target)
        wires = literal_gate_wires(program, witness['assignment'])
        assert sum(wires[wire] << j for j, wire in enumerate(rev['initial_wires'])) == target
    record = dict(passed=True, acquired_field_identity_coordinate=section.Q.F.one,
                  original_gate_targets_verified=len(points),
                  exact_original_quadratic_section_identity_verified=True)
    (HERE/'affine_section_center_basis_audit_results.json').write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps(record))


if __name__ == '__main__':
    main()
