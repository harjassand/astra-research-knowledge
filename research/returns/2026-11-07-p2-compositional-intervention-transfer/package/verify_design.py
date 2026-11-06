"""Independent final-design tangent certificate from the acquired lower model.

This does not trust the ellipsoid transcript or its normalization. It solves
the returned design directly in the original global coordinates, constructs
an exact concave-objective tangent, and bounds every point in the budget
polytope by checking its explicit vertices. No unknown-source access occurs.
"""
from fractions import Fraction as Q
from pathlib import Path
import json
import time
from port_transfer import (Arithmetic, rational_matrix, add, scale, sum_matrices,
                           schur_psd, quadratic, qtree)

HERE = Path(__file__).resolve().parent


def verify():
    start = time.perf_counter(); meter = Arithmetic()
    design_path = HERE/'new_design.json'
    assembly_path = HERE/'new_assemblies.json'
    design = json.loads(design_path.read_text())
    assemblies = json.loads(assembly_path.read_text())
    assembly = next(x for x in assemblies
                    if x['specification']['label'] == design['assembly_label'])
    u = list(map(Q, design['result']['actuation']))
    vertices = [list(map(Q, v)) for v in design['vertices']]
    assert min(u) >= 0 and sum(u) <= 2
    e = list(map(Q, design['loading'])); price = list(map(Q, design['price']))
    base = rational_matrix(assembly['certificate']['lower_matrix'])
    directions = [rational_matrix(c) for c in design['directions']]
    mat = base
    for x, c in zip(u, directions):
        mat = add(mat, scale(x, c, meter), meter)
    response, lift = schur_psd(mat, len(e), meter)
    state = e + [sum(x*z for x, z in zip(row, e)) for row in lift]
    value = quadratic(response, e, meter)-sum(x*z for x, z in zip(price, u))
    gradient = [quadratic(c, state, meter)-cost for c, cost in zip(directions, price)]
    vertex_bounds = [sum(g*(v_j-u_j) for g, v_j, u_j in zip(gradient, v, u))
                     for v in vertices]
    tangent_gap = max(vertex_bounds)
    previous_gap = Q(design['result']['gap_upper'])
    assert 0 <= tangent_gap <= previous_gap
    assert Q(design['result']['value_interval'][0]) <= value <= Q(design['result']['value_interval'][1])
    delta = Q(assembly['certificate']['gamma'])-1
    scale_bound = Q(design['result']['lower_energy_task_bound'])
    audit = dict(status='passed independent original-coordinate tangent certificate',
        lower_model_value=value, gradient=gradient, vertex_tangent_bounds=vertex_bounds,
        independently_certified_lower_model_gap=tangent_gap,
        ellipsoid_gap=previous_gap,
        independently_certified_true_regret=tangent_gap+delta*scale_bound,
        independently_certified_true_optimum_upper=value+tangent_gap+delta*scale_bound,
        new_source_acquisitions=0, input_bytes=design_path.stat().st_size+assembly_path.stat().st_size,
        matrix_kernel_cost=meter.record(), elapsed_seconds=time.perf_counter()-start)
    (HERE/'DESIGN_AUDIT.json').write_text(json.dumps(qtree(audit), indent=2)+'\n')
    print(json.dumps(dict(status=audit['status'], tangent_gap=float(tangent_gap),
                         true_regret_upper=float(audit['independently_certified_true_regret']),
                         elapsed_seconds=audit['elapsed_seconds']), indent=2))


if __name__ == '__main__':
    verify()
