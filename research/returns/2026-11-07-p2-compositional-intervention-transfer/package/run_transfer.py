"""End-to-end exact-rational numerical source, acquisition, new wiring, design.

Run from this directory with Python 3. Standard library only. This executes
numerical source computations, not physical experiments. Source matrices are
kept outside the learner and used separately for validation. Every source solve
is paid and logged. No speedup over directly known microscopic data is asserted.
"""
from fractions import Fraction as Q
from pathlib import Path
import hashlib
import json
import random
import time
import platform

from port_transfer import (Arithmetic, add, sub, scale, eye, zeros, transpose,
    matmul, outer, quadratic, solve_consistent, schur_psd, psd_certificate,
    acquire_law, assemble, compile_interval, robust_design, sum_matrices, qtree)
from predecessor_intervention import precision_for, round_dyadic

HERE = Path(__file__).resolve().parent


def save(name, obj):
    path = HERE / name
    path.write_text(json.dumps(qtree(obj), indent=2) + '\n')
    return path.stat().st_size


def finite_source(matrix, ports):
    """Explicit fresh minimization on every scalar call, with dyadic rounding."""
    records = []; validation = []; meter = Arithmetic()
    n = len(matrix)
    psd_certificate(sub(matrix, eye(n)), meter=meter)
    psd_certificate(sub(scale(16, eye(n)), matrix), meter=meter)
    def read(v, radius):
        start = time.perf_counter()
        before = sum(meter.counts.values())
        h = [row[ports:] for row in matrix[ports:]]
        rhs = [[-sum(matrix[i][j]*v[j] for j in range(ports))]
               for i in range(ports, n)]
        y = solve_consistent(h, rhs, meter)
        state = list(v) + [row[0] for row in y]
        energy = quadratic(matrix, state, meter)
        bits = precision_for(radius)+1
        mid = round_dyadic(energy, bits)
        err = Q(1, 1 << (bits+1))
        assert abs(energy-mid) <= err <= radius
        rec = dict(loading=list(v), mid=mid, error=err,
                   requested_radius=radius, reading_fraction_bits=bits,
                   setting='exact rational coordinates in numerical source',
                   calibration='dyadic rounding enclosure of exact rational solve')
        records.append(rec)
        validation.append(dict(exact_energy=energy,
            matrix_kernel_operations=sum(meter.counts.values())-before,
            elapsed_seconds=time.perf_counter()-start))
        return rec
    return read, records, validation, meter


def make_assembly(types, port_dimensions, size, external, label, seed):
    """A new explicit topology, constructed only after acquisition in main()."""
    rng = random.Random(seed)
    placements = []
    position = 0
    for j, name in enumerate(types):
        p = port_dimensions[name]
        mapping = zeros(p, size)
        for i in range(p):
            # Successive covered coordinates; sharing makes nontrivial loops.
            mapping[i][position % size] = Q(1)
            position += 1
        placements.append(dict(type=name, map=mapping))
    assert position >= size
    known = zeros(size)
    couplings = []
    for j in range(max(2, size//3)):
        a, b = rng.sample(range(size), 2)
        v = [Q(int(i == a)-int(i == b)) for i in range(size)]
        w = Q(j+1, 7)
        known = add(known, outer(v, w))
        couplings.append(dict(endpoints=[a, b], weight=w))
    return dict(label=label, total_coordinates=size, external_coordinates=external,
                placements=placements, known=known, new_couplings=couplings)


def main():
    start = time.perf_counter()
    ports = dict(A=3, B=4, C=5, D=6)
    sizes = dict(A=9, B=11, C=13, D=15)
    source_inputs = {}; sources = {}; construction_meter = Arithmetic()
    for index, name in enumerate(ports):
        n = sizes[name]
        rng = random.Random(90531+index)
        r = [[Q(rng.randrange(-3, 4)) for j in range(n)] for i in range(n)]
        matrix = add(eye(n), scale(Q(1, 32*n),
            matmul(transpose(r), r, construction_meter), construction_meter), construction_meter)
        source_inputs[name] = dict(ports=ports[name], matrix=matrix, alpha=Q(1), beta=Q(16))
        sources[name] = finite_source(matrix, ports[name])
    save('source_inputs.json', source_inputs)

    delta = Q(1, 10000)
    acquire_start = time.perf_counter()
    library = {name: acquire_law(sources[name][0], p, Q(1), delta)
               for name, p in ports.items()}
    acquisition_seconds = time.perf_counter()-acquire_start
    initial_source_calls = sum(len(sources[name][1]) for name in ports)
    assert initial_source_calls == 52
    acquisition_bytes = save('acquired_port_laws.json', library)

    # Independently read microscopic code to validate learned laws; these calls
    # and matrices are NOT supplied to the acquisition/assembly compiler.
    validation_meter = Arithmetic()
    truth = {}
    true_port_checks = {}
    for name in ports:
        truth[name], _ = schur_psd(source_inputs[name]['matrix'], ports[name], validation_meter)
        low = psd_certificate(sub(truth[name], library[name]['lower']), meter=validation_meter)
        high = psd_certificate(sub(library[name]['upper'], truth[name]), meter=validation_meter)
        true_port_checks[name] = dict(lower=low, upper=high)

    # New sizes, topologies and cross-port couplings, after the learner finishes.
    cases = [make_assembly(['A', 'B'], ports, 7, 2, 'two_modules', 52),
             make_assembly(['C', 'A', 'D', 'B', 'A'], ports, 12, 3, 'five_modules', 117),
             make_assembly(['D', 'C', 'A', 'B']*3, ports, 20, 4, 'twelve_modules', 218)]
    compiler_meter = Arithmetic(); assembly_results = []; assembly_summary = []
    compiler_start = time.perf_counter()
    for spec in cases:
        cert = compile_interval(library, spec['placements'], spec['known'],
                                spec['external_coordinates'], compiler_meter)
        true_matrix = assemble(truth, spec['placements'], spec['known'], validation_meter)
        true_response, _ = schur_psd(true_matrix, spec['external_coordinates'], validation_meter)
        low_check = psd_certificate(sub(true_response, cert['lower_response']), meter=validation_meter)
        high_check = psd_certificate(sub(cert['upper_response'], true_response), meter=validation_meter)
        width = sub(cert['upper_response'], cert['lower_response'])
        width_bound = max(sum(abs(x) for x in row) for row in width)
        assembly_results.append(dict(specification=spec, certificate=cert,
            true_matrix_validation_only=true_matrix, true_response_validation_only=true_response,
            truth_lower_certificate=low_check, truth_upper_certificate=high_check))
        assembly_summary.append(dict(label=spec['label'], modules=len(spec['placements']),
            total_coordinates=spec['total_coordinates'], external_coordinates=spec['external_coordinates'],
            all_direction_relative_factor=cert['gamma'], absolute_operator_width_bound=width_bound))
    compilation_seconds = time.perf_counter()-compiler_start
    assembly_bytes = save('new_assemblies.json', assembly_results)

    # Independent order of elimination: glue microscopic forms first, then
    # eliminate every internal coordinate in one larger exact solve.
    spec = cases[0]
    macro_size = spec['total_coordinates']
    full_size = macro_size + sum(sizes[item['type']]-ports[item['type']]
                                 for item in spec['placements'])
    full_known = zeros(full_size)
    for i in range(macro_size):
        for j in range(macro_size):
            full_known[i][j] = spec['known'][i][j]
    microscopic_placements = []; offset = macro_size
    for item in spec['placements']:
        name = item['type']; p = ports[name]; n = sizes[name]
        mapping = zeros(n, full_size)
        for i in range(p):
            mapping[i][:macro_size] = item['map'][i][:]
        for i in range(p, n):
            mapping[i][offset+i-p] = Q(1)
        offset += n-p
        microscopic_placements.append(dict(type=name, map=mapping))
    full_matrix = assemble({name: item['matrix'] for name, item in source_inputs.items()},
                          microscopic_placements, full_known, validation_meter)
    direct_response, _ = schur_psd(full_matrix, spec['external_coordinates'], validation_meter)
    assert direct_response == assembly_results[0]['true_response_validation_only']
    save('direct_microscopic_validation.json', dict(assembly=spec['label'],
        expanded_coordinates=full_size, placements=microscopic_placements,
        known=full_known, response=direct_response,
        matches_port_first_composition_exactly=True))

    # Singular PSD branch: a disconnected unused internal coordinate is legal.
    floating = [[Q(2), Q(-1), Q(0)], [Q(-1), Q(1), Q(0)], [Q(0), Q(0), Q(0)]]
    floating_law, floating_lift = schur_psd(floating, 1, compiler_meter)
    assert floating_law == [[Q(1)]] and floating_lift == [[Q(1)], [Q(0)]]

    # A new design problem, with positive directions absent from the training
    # experiments. A continuous budget simplex; no discrete topology claim.
    design_start = time.perf_counter()
    selected = assembly_results[1]
    n = selected['specification']['total_coordinates']
    p = selected['specification']['external_coordinates']
    edges = [(0, 3), (1, 4), (0, 6)]
    directions = [outer([Q(int(i == a)-int(i == b)) for i in range(n)]) for a, b in edges]
    vertices = [[Q(0)]*3] + [[Q(2*int(i == j)) for j in range(3)] for i in range(3)]
    loading = [Q(1), Q(-4, 5), Q(1, 3)]
    price = [Q(1, 50), Q(1, 80), Q(1, 50)]
    epsilon = Q(1, 100)
    result = robust_design(selected['certificate']['lower_matrix'], directions, p,
                           loading, vertices, epsilon, price)
    u = result['actuation']
    assert min(u) >= 0 and sum(u) <= 2
    direction_sum = sum_matrices([scale(x, c) for x, c in zip(u, directions)], n)
    true_at_u = add(selected['true_matrix_validation_only'], direction_sum)
    true_f, _ = schur_psd(true_at_u, p, validation_meter)
    true_objective = quadratic(true_f, loading)-sum(c*x for c, x in zip(price, u))
    lower_at_u = add(selected['certificate']['lower_matrix'], direction_sum)
    lower_f, _ = schur_psd(lower_at_u, p, validation_meter)
    lower_objective = quadratic(lower_f, loading)-sum(c*x for c, x in zip(price, u))
    assert result['value_interval'][0] <= lower_objective <= result['value_interval'][1]
    regret_bound = result['gap_upper'] + delta*result['lower_energy_task_bound']
    true_optimum_upper = result['optimum_interval'][1] + delta*result['lower_energy_task_bound']
    assert true_objective <= true_optimum_upper
    design_seconds = time.perf_counter()-design_start
    design_bytes = save('new_design.json', dict(assembly_label='five_modules',
        edges=edges, directions=directions, vertices=vertices, loading=loading,
        price=price, epsilon=epsilon, result=result,
        validation_only=dict(true_objective=true_objective, lower_objective=lower_objective),
        true_regret_upper=regret_bound, true_optimum_upper=true_optimum_upper))

    final_source_calls = sum(len(sources[name][1]) for name in ports)
    assert final_source_calls == initial_source_calls
    source_validation = {name: dict(exact_records=sources[name][2],
                        matrix_kernel_cost=sources[name][3].record()) for name in ports}
    source_validation['construction_kernel_cost'] = construction_meter.record()
    source_validation['port_interval_checks'] = true_port_checks
    save('source_validation.json', source_validation)
    summary = dict(status='all exact-rational checks passed',
        physical_experiments=0, scalar_source_acquisitions=initial_source_calls,
        additional_source_acquisitions_for_new_assemblies_and_design=final_source_calls-initial_source_calls,
        modules=[dict(type=name, ports=ports[name], microscopic_coordinates=sizes[name],
                      scalar_readings=len(sources[name][1])) for name in ports],
        delta=delta, gamma=1+delta, acquired_data_bytes=acquisition_bytes,
        source_input_bytes=(HERE/'source_inputs.json').stat().st_size,
        new_assemblies_data_bytes=assembly_bytes, new_design_data_bytes=design_bytes,
        assembly_checks=assembly_summary,
        compiler_matrix_kernel_cost=compiler_meter.record(),
        independent_validation_matrix_kernel_cost=validation_meter.record(),
        singular_internal_branch=dict(response=floating_law, minimizing_lift=floating_lift),
        direct_microscopic_composition=dict(expanded_coordinates=full_size,
            matches_exactly=True),
        new_design=dict(actuation=u, certified_lower_model_gap=result['gap_upper'],
            true_objective=true_objective, true_regret_upper=regret_bound,
            true_optimum_upper=true_optimum_upper,
            lower_energy_task_bound=result['lower_energy_task_bound'],
            digital_model_evaluations=result['model_evaluations'],
            ellipsoid_iterations=result['solver_certificate']['iterations'],
            ellipsoid_iteration_cap=result['solver_certificate']['maximum_iterations'],
            precision_bits=dict(record=result['solver_certificate']['record_bits'],
                actuation=result['solver_certificate']['actuation_bits'],
                center=result['solver_certificate']['center_bits'],
                shape=result['solver_certificate']['shape_bits']),
            termination_reason=result['solver_certificate']['reason']),
        elapsed_seconds=dict(acquisition=acquisition_seconds,
            assembly_compilation_and_validation=compilation_seconds, design_and_validation=design_seconds,
            entire_run=time.perf_counter()-start),
        runtime=dict(python=platform.python_version(), machine=platform.machine(),
                     implementation=platform.python_implementation(),
                     timing_scope='single run in existing session; environment-dependent, not a benchmark'))
    save('RESULTS.json', summary)
    compact = dict(status=summary['status'], scalar_source_acquisitions=initial_source_calls,
        new_source_acquisitions=0, design_model_evaluations=result['model_evaluations'],
        design_iterations=result['solver_certificate']['iterations'],
        actuation=[float(x) for x in u],
        design_gap=float(result['gap_upper']), true_regret_upper=float(regret_bound),
        elapsed_seconds=summary['elapsed_seconds'])
    print(json.dumps(compact, indent=2))


if __name__ == '__main__':
    main()
