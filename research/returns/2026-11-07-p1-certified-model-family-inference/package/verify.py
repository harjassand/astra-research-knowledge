"""Exact checks and completed positive inference fixtures.

The data are synthetic mathematical inputs, not measured physical data.
The general CAD solver is not implemented or executed in this package.
"""
from fractions import Fraction as Q
from pathlib import Path
import copy
import json
import time

from interpolation import complete_values, check_values, RationalPotential, weight
from network import (Envelope, Network, certified_trajectory, verify_trajectory,
                     certified_equilibrium, verify_equilibrium, contraction_scaling)
from algebraic_problem import compile_euler

ROOT = Path(__file__).resolve().parent


def rational_document(x):
    if isinstance(x, Q):
        return str(x)
    if isinstance(x, dict):
        return {k: rational_document(v) for k, v in x.items()}
    if isinstance(x, (tuple, list)):
        return [rational_document(v) for v in x]
    return x


def display_interval(lo, hi):
    # Display only; exact endpoints remain in the certificate.
    return {'lower': str(lo), 'upper': str(hi),
            'decimal_display': [float(lo), float(hi)]}


def source_pair(samples, lower_slope, upper_slope):
    return (Envelope(lower_slope, upper_slope, samples, 'lower'),
            Envelope(lower_slope, upper_slope, samples, 'upper'))


def periodic_network(side):
    n = side*side
    rows = []
    sources_lower, sources_upper = [], []
    for i in range(n):
        x, y = divmod(i, side)
        neighbors = [((x+1)%side)*side+y, ((x-1)%side)*side+y,
                     x*side+(y+1)%side, x*side+(y-1)%side]
        row = [(i, Q(-1, 4))]+[(j, Q(1, 16)) for j in neighbors]
        rows.append(row)
        slope = Q(3, 4)+Q(i%4, 16)
        samples = [(Q(0), Q(0), Q(0)),
                   (Q(1, 2), slope/2-Q(1, 64), slope/2+Q(1, 64)),
                   (Q(1), slope-Q(1, 32), slope+Q(1, 32))]
        low, high = source_pair(samples, Q(1, 2), Q(3, 2))
        sources_lower.append(low)
        sources_upper.append(high)
    forcing = [Q(1, 4)+Q(i%3, 32) for i in range(n)]
    # Larger constitutive force produces the lower state trajectory.
    return (Network(rows, sources_upper, forcing),
            Network(rows, sources_lower, forcing))


def run():
    started = time.monotonic()
    results = {'scope': 'Exact rational synthetic inference checks',
               'physical_data_acquired': False, 'general_CAD_executed': False}

    # 1. Complete finite-gradient interpolation in two dimensions.
    points = [(Q(0), Q(0)), (Q(1), Q(0)), (Q(0), Q(1)),
              (Q(1), Q(1)), (Q(-1), Q(2))]
    gradients = [(x, 2*y) for x, y in points]
    completion = complete_values(points, gradients, Q(0), Q(3))
    assert completion['feasible']
    potential = RationalPotential(points, gradients, completion['values'], Q(0), Q(3))
    at_data = [potential.evaluate(x) for x in points]
    assert [x[1] for x in at_data] == gradients
    assert [x[0] for x in at_data] == completion['values']
    queries = points+[(Q(1, 3), Q(2, 5)), (Q(-2), Q(-1)), (Q(3), Q(1, 2))]
    evaluated = [potential.evaluate(x) for x in queries]
    ok, consistency = check_values(queries, [v[1] for v in evaluated],
                                   [v[0] for v in evaluated], Q(0), Q(3))
    assert ok
    results['interpolation'] = rational_document({
        'completion': completion, 'new_point_checks': consistency,
        'sample_values_and_gradients': [(x, v, g) for x, (v, g, _) in zip(queries, evaluated)],
        'active_faces_tried': [c['faces_tried'] for _, _, c in evaluated]})
    print('Global rational interpolant: PASS', flush=True)

    # 2. Exact cycle falsifier: all two-point sector tests pass.
    square = [(Q(0), Q(0)), (Q(1), Q(0)), (Q(1), Q(1)), (Q(0), Q(1))]
    rotation = [(x-y, x+y) for x, y in square]
    assert all(weight(square[i], rotation[i], square[j], rotation[j], Q(0), Q(2))
               +weight(square[j], rotation[j], square[i], rotation[i], Q(0), Q(2)) == 0
               for i in range(4) for j in range(4))
    failure = complete_values(square, rotation, Q(0), Q(2))
    assert not failure['feasible']
    explicit_cycle_weight = sum(
        (weight(square[(j+1)%4], rotation[(j+1)%4], square[j], rotation[j], Q(0), Q(2))
         for j in range(4)), Q(0))
    assert explicit_cycle_weight == 2
    results['cycle_counterexample'] = rational_document({
        'points': square, 'gradients': rotation,
        'all_pair_sector_tests_pass': True, 'four_cycle_weight': explicit_cycle_weight,
        'detected': failure})
    print('Long-cycle consistency counterexample: PASS', flush=True)

    # 3. General shared-potential polynomial compiler.
    A, B, C = [[Q(0)]], [[Q(-1)]], [[Q(1)]]
    problem = compile_euler(A, B, C, Q(1), Q(3), [(Q(1), Q(1))], Q(0),
                            [([Q(1)], [(Q(2), Q(2))], (Q(1), Q(1)))],
                            [Q(1, 4), Q(1, 4)], [[Q(0)], [Q(0)]])
    values = {'anchor_g_0': Q(0), 'cal_0_g_0': Q(2), 'cal_0_f': Q(1)}
    for j, z in enumerate([Q(1), Q(1, 2), Q(1, 4)]):
        values.update({'z_'+str(j)+'_0': z, 'node_'+str(j)+'_g_0': 2*z,
                       'node_'+str(j)+'_f': z*z})
    assert problem.verify_assignment(values)
    (ROOT/'GENERAL_POLYNOMIAL_FIXTURE.json').write_text(
        json.dumps(problem.document(), indent=2)+'\n')
    results['general_compiler'] = {
        'variables': len(problem.names), 'constraints': len(problem.constraints),
        'maximum_degree': problem.document()['maximum_degree'],
        'rational_assignment_verified': True, 'optimization_executed': False}
    print('Shared-potential finite algebraic compiler: PASS', flush=True)

    # 4. A whole nonlinear force family, with sharp dynamic endpoints.
    low_force, high_force = source_pair(
        [(Q(0), Q(0), Q(0)), (Q(1), Q(2), Q(2))], Q(1), Q(3))
    scalar_low = Network([[]], [high_force], [Q(0)])
    scalar_high = Network([[]], [low_force], [Q(0)])
    scalar_certificates = []
    for model in [scalar_low, scalar_high]:
        cert = certified_trajectory(model, [Q(1)], Q(1), Q(1, 2048))
        assert verify_trajectory(model, cert)
        scalar_certificates.append({'model': model.document(), 'certificate': cert})
    scalar_l = Q(scalar_certificates[0]['certificate']['state'][0])
    scalar_u = Q(scalar_certificates[1]['certificate']['state'][0])
    scalar_lr = Q(scalar_certificates[0]['certificate']['radius'])
    scalar_ur = Q(scalar_certificates[1]['certificate']['radius'])
    results['scalar_full_family'] = {
        'task': 'x(1), xprime=-g(x), x(0)=1; g(0)=0,g(1)=2; slopes [1,3]',
        'sharp_range_outer': display_interval(scalar_l-scalar_lr, scalar_u+scalar_ur),
        'exact_endpoint_formulas': ['(32/27)*exp(-3)', '2^(-1/3)*exp(-1)'],
        'lower_source_steps': scalar_certificates[0]['certificate']['steps'],
        'upper_source_steps': scalar_certificates[1]['certificate']['steps'],
        'numerical_radii': [str(scalar_lr), str(scalar_ur)]}
    (ROOT/'SCALAR_TRAJECTORY_CERTIFICATES.json').write_text(
        json.dumps(scalar_certificates, separators=(',', ':'))+'\n')
    print('Sharp scalar nonlinear-family prediction: PASS', flush=True)

    # 5. Coupled 4x4 periodic network: actual loops, no tree assumption.
    lower_model, upper_model = periodic_network(4)
    lower_initial = [Q(3, 4)+Q(i%4, 32)-Q(1, 128) for i in range(16)]
    upper_initial = [Q(3, 4)+Q(i%4, 32)+Q(1, 128) for i in range(16)]
    trajectory_certs = []
    for label, model, initial in [('lower', lower_model, lower_initial),
                                  ('upper', upper_model, upper_initial)]:
        cert = certified_trajectory(model, initial, Q(1), Q(1, 512))
        assert verify_trajectory(model, cert)
        trajectory_certs.append({'endpoint': label, 'model': model.document(), 'certificate': cert})
        print('16-node '+label+' trajectory: PASS, steps='+str(cert['steps']), flush=True)
    lc, uc = [c['certificate'] for c in trajectory_certs]
    lo = [Q(x)-Q(lc['radius']) for x in lc['state']]
    hi = [Q(x)+Q(uc['radius']) for x in uc['state']]
    assert all(a <= b for a, b in zip(lo, hi))
    results['coupled_16_node_transient'] = {
        'dimension': 16, 'horizon': '1',
        'range_node_zero': display_interval(lo[0], hi[0]),
        'range_mean_state': display_interval(sum(lo)/16, sum(hi)/16),
        'gamma': str(lower_model.gamma),
        'lipschitz': str(lower_model.lipschitz),
        'steps': [lc['steps'], uc['steps']],
        'total_steps_including_refinement': [lc['total_steps_including_refinements'],
                                            uc['total_steps_including_refinements']],
        'precision_bits': [lc['precision_bits'], uc['precision_bits']],
        'numerical_radii': [lc['radius'], uc['radius']]}
    (ROOT/'NETWORK_TRAJECTORY_CERTIFICATES.json').write_text(
        json.dumps(trajectory_certs, separators=(',', ':'))+'\n')

    # 6. 64-node equilibrium inference: exact residual, high precision.
    eq_lower, eq_upper = periodic_network(8)
    equilibrium_certs = []
    for label, model in [('lower', eq_lower), ('upper', eq_upper)]:
        cert = certified_equilibrium(model, Q(1, 1 << 48))
        assert verify_equilibrium(model, cert)
        equilibrium_certs.append({'endpoint': label, 'model': model.document(), 'certificate': cert})
        print('64-node '+label+' equilibrium: PASS, iterations='+str(cert['iterations']), flush=True)
    ec0, ec1 = [v['certificate'] for v in equilibrium_certs]
    e_lo = [Q(x)-Q(ec0['radius']) for x in ec0['state']]
    e_hi = [Q(x)+Q(ec1['radius']) for x in ec1['state']]
    assert all(a <= b for a, b in zip(e_lo, e_hi))
    results['coupled_64_node_equilibrium'] = {
        'dimension': 64, 'requested_radius': '2^-48',
        'alpha': ec0['alpha'],
        'range_node_zero': display_interval(e_lo[0], e_hi[0]),
        'range_mean_state': display_interval(sum(e_lo)/64, sum(e_hi)/64),
        'iterations': [ec0['iterations'], ec1['iterations']],
        'precision_bits': [ec0['precision_bits'], ec1['precision_bits']],
        'numerical_radii': [ec0['radius'], ec1['radius']]}
    (ROOT/'EQUILIBRIUM_CERTIFICATES.json').write_text(
        json.dumps(equilibrium_certs, indent=2)+'\n')

    # A derived statement about EVERY future time, not just the limit.
    initial_box = [(Q(3, 4)+Q(i%4, 32)-Q(1, 128),
                    Q(3, 4)+Q(i%4, 32)+Q(1, 128)) for i in range(64)]
    tail_radius = max(max(abs(a-u), abs(b-l))
                      for (a, b), l, u in zip(initial_box, e_lo, e_hi))
    future_upper = sum(e_hi)/64+tail_radius/16
    assert future_upper < Q(1, 2)
    consequence = {
        'scope': 'All compatible 64-node laws and all initial states in the stated box',
        'initial_box': [[str(a), str(b)] for a, b in initial_box],
        'alpha': '1/2', 'start_time': '8',
        'equilibrium_mean_upper': str(sum(e_hi)/64),
        'uniform_initial_equilibrium_distance_bound': str(tail_radius),
        'rational_tail_multiplier': '1/16',
        'all_future_mean_upper': str(future_upper), 'threshold': '1/2',
        'strict_gap': str(Q(1, 2)-future_upper),
        'display': {'distance': float(tail_radius), 'all_future_upper': float(future_upper)},
        'proof': 'For t>=8, exp(-alpha*t)<=2^(-floor(alpha*t))<=1/16. '
                 'Each trajectory contracts toward its own equilibrium. '
                 'All equilibria lie in the certified box.'}
    (ROOT/'DERIVED_CONSEQUENCES.json').write_text(json.dumps(consequence, indent=2)+'\n')
    results['all_future_consequence'] = {k: v for k, v in consequence.items() if k != 'initial_box'}

    # Rejection control: a numerical certificate must not accept an
    # artificially lowered last-step radius.
    broken = copy.deepcopy(scalar_certificates[0]['certificate'])
    broken['trace'][-1]['radius'] = '0'
    broken['radius'] = '0'
    rejected = False
    try:
        verify_trajectory(scalar_low, broken)
    except (AssertionError, ValueError):
        rejected = True
    assert rejected
    results['tampered_radius_rejected'] = True

    # A nonnormal cooperative network that the unweighted row test misses.
    unweighted = Network([[(0, -2), (1, 10)], [(1, -2)]],
                         [high_force, high_force], [1, 1])
    assert unweighted.gamma == 7
    weights, scaled = contraction_scaling(unweighted)
    assert weights == [Q(13, 9), Q(1, 3)] and scaled.gamma == Q(-9, 13)
    weighted_cert = certified_equilibrium(scaled, Q(1, 1 << 32))
    assert verify_equilibrium(scaled, weighted_cert)
    results['automatic_weighted_contraction'] = {
        'unweighted_gamma': str(unweighted.gamma), 'weights': list(map(str, weights)),
        'weighted_gamma': str(scaled.gamma),
        'coordinate_error_bounds': [str(w*Q(weighted_cert['radius'])) for w in weights],
        'iterations': weighted_cert['iterations']}
    (ROOT/'WEIGHTED_CONTRACTION_CERTIFICATE.json').write_text(json.dumps({
        'original_model': unweighted.document(), 'weights': list(map(str, weights)),
        'scaled_model': scaled.document(), 'certificate': weighted_cert}, indent=2)+'\n')

    # Certificates must reject malformed dimensions even under python -O.
    malformed = copy.deepcopy(scalar_certificates[0]['certificate'])
    malformed['trace'][-1]['x'] = []
    try:
        verify_trajectory(scalar_low, malformed)
    except ValueError:
        results['malformed_dimension_rejected'] = True
    else:
        raise AssertionError('Malformed dimensions were accepted')
    results['status'] = 'PASS: exact arithmetic checks and completed scoped inference fixtures'
    results['runtime_seconds'] = time.monotonic()-started
    (ROOT/'RESULTS.json').write_text(json.dumps(results, indent=2)+'\n')
    print(json.dumps({k: v for k, v in results.items() if k not in ['interpolation']},
                     indent=2), flush=True)


if __name__ == '__main__':
    run()
