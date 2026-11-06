#!/usr/bin/env python3
"""Exact finite verification. It does not simulate a universal machine."""
from pathlib import Path
from fractions import Fraction as F
import json
import time

from compiler import (
    GQ, build_frame, add, sub, scale, mul, constant, sine, cosine, derivative,
    dv, dot, vadd, vsub, vnorm, gunther_observations, nonlinear, make_certificate,
    picard_step, metric_residual, linearized_metric, eval_quarters,
    serialize_fraction, serialize_poly, finite_precision_embedding,
)

ROOT = Path(__file__).resolve().parent


def upper_power_two(x: F):
    if x <= 0:
        return None
    n = x.numerator.bit_length() - x.denominator.bit_length()
    while F(2) ** n < x:
        n += 1
    while F(2) ** (n - 1) >= x:
        n -= 1
    return n


def run():
    started = time.monotonic()
    results = {'arithmetic': 'exact Gaussian rational Fourier coefficients',
               'universal_machine_executed': False, 'physical_experiment': False,
               'checks': {}, 'frames': []}
    data_one = None
    frame_identifications = 0
    for d in range(1, 5):
        data = build_frame(d)
        if d == 1:
            data_one = data
        # A separate all-frequency interpolation check verifies the right inverse.
        for i, frame_row in enumerate(data['frame']):
            for j, column in enumerate(data['columns']):
                assert dot(frame_row, column) == constant(int(i == j), d + 1)
                frame_identifications += 1
        results['frames'].append({
            'torus_dimension': d,
            'with_clock_dimension': d + 1,
            'natural_configuration_dimension': 2 * len(data['q0']),
            'free_frame_rank': len(data['frame']),
            'readout_modes': len(data['frequencies']),
            'gram_constant_in_all_coordinates': True,
            'right_inverse_norm': serialize_fraction(data['ce']),
        })
        print(f'Free frame d={d}: exact PASS', flush=True)
    results['checks']['free_frame_interpolation_identities'] = frame_identifications

    data = data_one
    m = data['m']
    trial = [scale(sine((1, 0)), F(1, 7)),
             scale(cosine((0, 1)), F(1, 11)),
             scale(sine((1, 1)), F(1, 13)),
             scale(cosine((2, -1)), F(1, 17)), {}, {}]
    qi, qij = gunther_observations(trial, m)
    for index, (i, j) in enumerate(data['pairs']):
        reconstructed = add(add(derivative(qi[j], i), derivative(qi[i], j)), qij[index])
        assert reconstructed == dot(dv(trial, i), dv(trial, j))
    b_trial = nonlinear(data, trial)
    lb = linearized_metric(data, b_trial)
    for (i, j), value in zip(data['pairs'], lb):
        assert add(value, dot(dv(trial, i), dv(trial, j))) == {}
    results['checks']['gunther_product_and_sign_identities'] = 2 * len(data['pairs'])

    y = [sine((1, 0))]
    certificate = make_certificate(data, y, F(1, 4))
    assert vnorm(b_trial) <= certificate['B'] * vnorm(trial) ** 2
    v = [{} for _ in data['q0']]
    iterations = []
    for step in range(1, 4):
        next_v = picard_step(data, certificate, v)
        assert vnorm(next_v) <= certificate['radius']
        difference = vnorm(vsub(next_v, v))
        tail = certificate['lipschitz'] * difference / (1 - certificate['lipschitz'])
        iterations.append({'step': step,
                           'retained_coefficients': sum(map(len, next_v)),
                           'difference_norm_le_power_two': upper_power_two(difference),
                           'limit_tail_norm_le_power_two': upper_power_two(tail),
                           'tail_bound': serialize_fraction(tail)})
        v = next_v
        print(f'Picard step {step}: exact PASS, coefficients={sum(map(len, v))}', flush=True)
    # Independent identity relating the metric residual to the fixed-point defect.
    fixed_defect = vsub(v, picard_step(data, certificate, v))
    assert metric_residual(data, certificate, v) == linearized_metric(data, fixed_defect)
    results['checks']['picard_ball_and_residual'] = 4
    results['picard_iterations'] = iterations

    s = F(3, 5)
    L = len(data['q0']) // 2
    readouts = 0
    # The retained first block gives exact position-only readout, independent of v.
    frozen = [scale(p, s) for p in data['q0']]
    anchor = data['anchor']
    amplitude = data['amplitude']
    for x in range(4):
        for theta in range(4):
            q = [eval_quarters(p, (x, theta)) for p in frozen]
            cos_read = (q[0] * q[1] + q[L] * q[L + 1]) / (s * s * anchor * amplitude)
            sin_read = (q[0] * q[2] + q[L] * q[L + 2]) / (s * s * anchor * amplitude)
            assert cos_read == eval_quarters(cosine((1, 0)), (x, theta))
            assert sin_read == eval_quarters(sine((1, 0)), (x, theta))
            readouts += 2
    results['checks']['fixed_quadratic_position_readouts'] = readouts

    # The metric shear makes X=(epsilon Y,1) exactly unit speed, algebraically.
    eps = certificate['epsilon']
    gm = data['gm'][0][0]
    xx = constant(gm, 2)
    xt = scale(y[0], -eps * gm)
    tt = add(constant(1, 2), scale(mul(y[0], y[0]), eps * eps * gm))
    speed = add(add(scale(mul(mul(y[0], y[0]), xx), eps * eps),
                    scale(mul(y[0], xt), 2 * eps)), tt)
    assert speed == constant(1, 2)
    assert add(scale(mul(xx, y[0]), eps), xt) == {}
    assert add(scale(mul(xt, y[0]), eps), tt) == constant(1, 2)
    results['checks']['geodesic_shear_metric_identities'] = 3

    approximation, accuracy = finite_precision_embedding(data, certificate, 512, 4)
    assert accuracy['C_r_error'] <= F(1, 1 << 512)
    results['checks']['finite_precision_C4_evaluation'] = 1
    results['finite_precision_evaluation'] = {
        **{k: val for k, val in accuracy.items() if k not in ('weak_norm_error', 'C_r_error')},
        'retained_coefficients': sum(map(len, approximation)),
        'C4_error_le_power_two': upper_power_two(accuracy['C_r_error']),
        'error_certificate': serialize_fraction(accuracy['C_r_error']),
    }

    cert_output = {
        'input': {'d': 1, 'velocity': 'Y(x)=sin(x)', 'eta': '1/4'},
        'configuration_dimension': 12,
        'epsilon': serialize_fraction(eps),
        'epsilon_power_two_exponent': certificate['epsilon_exponent'],
        'physical_time_per_source_time': f'2^{certificate["epsilon_exponent"]}',
        'field_constants': {key: serialize_fraction(certificate[key]) for key in
                            ['A', 'B', 'radius', 'lipschitz', 'co_lipschitz',
                             'tube_radius', 'projection_eigenvalue',
                             'curvature_constant', 'certified_hessian_error',
                             'value_jet_constant', 'gradient_jet_constant']},
        'curvature_error_upper_power_two': upper_power_two(certificate['certified_hessian_error']),
        'coefficient_matrix_gram': [[serialize_fraction(x) for x in row] for row in data['gram']],
        'linear_correction': [serialize_poly(p) for p in certificate['linear']],
        'meaning': 'Analytic inequalities certify the exact fixed-point limit. Finite iterates are approximations with explicit tails.',
    }
    (ROOT / 'EXAMPLE_CERTIFICATE.json').write_text(json.dumps(cert_output, indent=2) + '\n')
    results['example'] = {k: cert_output[k] for k in
                          ['configuration_dimension', 'epsilon_power_two_exponent',
                           'physical_time_per_source_time', 'curvature_error_upper_power_two']}
    results['status'] = 'PASS: exact scoped checks; no physical implementation or universal trajectory run'
    results['runtime_seconds'] = time.monotonic() - started
    (ROOT / 'results.json').write_text(json.dumps(results, indent=2) + '\n')
    print(json.dumps({'checks': results['checks'], 'example': results['example'],
                      'status': results['status'], 'runtime_seconds': results['runtime_seconds']}, indent=2))
    return results


if __name__ == '__main__':
    run()
