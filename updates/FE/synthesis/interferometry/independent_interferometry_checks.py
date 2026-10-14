#!/usr/bin/env python3
"""Independent mathematical checks; no experimental or CaOH+ simulation claims.

Run with Python >=3.10, numpy, scipy. This program does not import producer code.
All paths are command-line supplied or relative to this file.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import platform
from fractions import Fraction
from pathlib import Path

import numpy as np
import scipy
from scipy.integrate import quad
from scipy.linalg import expm


X = np.array([[0, 1], [1, 0]], complex)
Y = np.array([[0, -1j], [1j, 0]], complex)
Z = np.diag([1., -1.]).astype(complex)
I2 = np.eye(2, dtype=complex)


def wave(Ea, Eb, s, x):
    a, b = np.exp(0.5j*s), np.exp(-0.5j*s)
    cp = (a*Ea-b*Eb)/(2j*math.sin(s))
    cm = (-b*Ea+a*Eb)/(2j*math.sin(s))
    return cp*np.exp(1j*x)+cm*np.exp(-1j*x), abs(cp)**2+abs(cm)**2


def pulse(theta, E):
    h = np.array([[0., np.conj(E)], [E, 0.]], complex)
    return expm(-0.5j*theta*h)


def order_vectors(p, s, q=0.):
    theta = 2*math.asin(math.sqrt(p))
    states = []
    for x in (s/2+q, -s/2+q):
        f1, _ = wave(1., 1j, s, x)
        f2, _ = wave(1j, 1., s, x)
        states.append(pulse(theta, f2)@pulse(theta, f1)@np.array([1., 0.]))
    return states


def completion_vectors(pa, pb, zs, zl):
    qa, qb = 1-pa, 1-pb
    # Two orthogonal outcome sectors, each of dimension two. Inner products are
    # <vB|P_s|vA>=zs and <vB|P_l|vA>=zl, fixing all branch outcome probabilities.
    a = np.array([math.sqrt(pa), 0., math.sqrt(qa), 0.], complex)
    b = np.array([np.conj(zs)/math.sqrt(pa),
                  math.sqrt(max(0., pb-abs(zs)**2/pa)),
                  np.conj(zl)/math.sqrt(qa),
                  math.sqrt(max(0., qb-abs(zl)**2/qa))], complex)
    return a, b


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--source-dir', type=Path)
    ap.add_argument('--replay-dir', type=Path)
    ap.add_argument('--output', type=Path, default=Path(__file__).with_name('independent_results.json'))
    args = ap.parse_args()
    rng = np.random.default_rng(1431)
    result = {'status': 'INTERNAL MATHEMATICAL CHECKS; NO PHYSICAL VALIDATION',
              'runtime': {'python': platform.python_version(), 'numpy': np.__version__,
                          'scipy': scipy.__version__}, 'groups': {}}

    # Closed-form inverse and matrix exponential are independent of producer
    # linear solve and hand-coded rotation. Exercise multiple conditioning regimes.
    errors = dict(interpolation=0., energy=0., equal_intensity=0., unitary_formula=0.)
    for s in (.1, .4, .78, 1.2, 1.57, 2.2, 3.0):
        for _ in range(30):
            ea, eb = rng.normal(size=2)+1j*rng.normal(size=2)
            va, e = wave(ea, eb, s, s/2)
            vb, _ = wave(ea, eb, s, -s/2)
            formula = (abs(ea)**2+abs(eb)**2-2*math.cos(s)*np.real(ea*np.conj(eb)))/(2*math.sin(s)**2)
            errors['interpolation'] = max(errors['interpolation'], abs(va-ea), abs(vb-eb))
            errors['energy'] = max(errors['energy'], abs(e-formula))
        for x in rng.uniform(-12, 12, 100):
            f1, _ = wave(1., 1j, s, x)
            f2, _ = wave(1j, 1., s, x)
            errors['equal_intensity'] = max(errors['equal_intensity'], abs(abs(f1)**2-abs(f2)**2))
    for p in (.001, .01, .03, .1, .3, .49):
        va, vb = order_vectors(p, .78)
        target = 1-2*p*p+2j*p*(1-p)
        errors['unitary_formula'] = max(errors['unitary_formula'], abs(np.vdot(vb, va)-target))
    assert max(errors.values()) < 1e-11
    result['groups']['independent_field_and_unitary_checks'] = errors

    # Adaptive integration of the entire spatially dependent unitary, not a
    # point-packet interpolation or the producer's Gauss-Hermite rule.
    sigma, p, s = .03, .03, .78
    def integrand(q):
        va, vb = order_vectors(p, s, q)
        return np.vdot(vb, va)*math.exp(-q*q/(2*sigma*sigma))/(math.sqrt(2*math.pi)*sigma)
    re, err_re = quad(lambda q: integrand(q).real, -10*sigma, 10*sigma, epsabs=1e-12, epsrel=1e-12)
    im, err_im = quad(lambda q: integrand(q).imag, -10*sigma, 10*sigma, epsabs=1e-12, epsrel=1e-12)
    assert abs(re-.9981841219781635) < 1e-7 and abs(im-.05809073) < 1e-7
    result['groups']['adaptive_finite_width'] = {'L_real': re, 'L_imag': im,
        'reported_quadrature_error_real': err_re, 'reported_quadrature_error_imag': err_im,
        'excluded_gaussian_tail_bound': math.erfc(10/math.sqrt(2)),
        'limitation': 'floating diagnostics, not rigorous interval quadrature or CaOH+ prediction'}

    # Construct every sampled disk point explicitly, including both extremal
    # signs; these are physical normalized dilation vectors, not a loose norm test.
    worst = 0.
    for _ in range(300):
        pa, pb = rng.uniform(.02, .98, size=2)
        zs = rng.uniform(0., 1.)*math.sqrt(pa*pb)*np.exp(1j*rng.uniform(-math.pi, math.pi))
        radius = math.sqrt((1-pa)*(1-pb))
        for frac in (0., .3, 1.):
            zl = frac*radius*np.exp(1j*rng.uniform(-math.pi, math.pi))
            a, b = completion_vectors(pa, pb, zs, zl)
            err = max(abs(np.vdot(a, a)-1), abs(np.vdot(b, b)-1),
                      abs(np.vdot(b[:2], a[:2])-zs), abs(np.vdot(b, a)-(zs+zl)))
            worst = max(worst, err)
    assert worst < 1e-13
    result['groups']['sharp_erasure_disk'] = {'constructed_cases': 900, 'max_error': worst}

    pa = pb = .99
    a, b = completion_vectors(pa, pb, .99, -.01)
    full = float(np.vdot(b, a).real)
    assert abs(full-.98) < 1e-14
    result['groups']['postselection_countermodels'] = {
        'perfect_survivors': {'survival_each_branch': .99, 'conditional_overlap': 1.,
                             'full_overlap': full, 'full_X_failure': (1-full)/2},
        'rank_one_residual': {}}
    d, t, r = 8, 1., 1.
    L = ((d-1)+np.exp(-1j*r*t))/d
    pfull = (1-L.real)/2
    assert pfull > 0
    result['groups']['postselection_countermodels']['rank_one_residual'] = {
        'd': d, 'H': '0', 'R': '|0><0|', 'Rcap': 1., 'Lambda': 1., 't': t,
        'reset': 'I/d', 'erase_rule': 'projector |0><0| at final time',
        'erasure_probability': 1/d, 'conditional_X_failure': 0.,
        'full_X_failure': float(pfull), 'actual_residual_operator_norm': r,
        'sharp_completion_upper_X_failure': 1/d,
        'naive_discarded_record_norm_certificate': 0.}

    # Full controlled GKSL generator. Each branch's internal map is identity,
    # while the environmental mark destroys branch coherence.
    gamma, duration = .7, .4
    jump = math.sqrt(gamma)*np.kron(Z, I2)
    n = 4
    ld = np.kron(jump.conj(), jump)-.5*(np.kron(np.eye(n), jump.conj().T@jump)
                                              +np.kron((jump.conj().T@jump).T, np.eye(n)))
    rho = np.kron(np.ones((2, 2))/2, np.diag([.6, .4]))
    final = (expm(duration*ld)@rho.reshape(-1, order='F')).reshape((n, n), order='F')
    observed = 2*np.trace(final[:2, 2:])
    analytic = math.exp(-2*gamma*duration)
    assert abs(observed-analytic) < 1e-13
    result['groups']['identical_channel_marginals_different_cross_block'] = {
        'branch_channels': 'both exactly identity at every t',
        'same_jump_choice': {'J_A': 'sqrt(gamma) I', 'J_B': 'sqrt(gamma) I', 'overlap': 1.},
        'opposite_jump_choice': {'J_A': 'sqrt(gamma) I', 'J_B': '-sqrt(gamma) I',
                               'gamma': gamma, 't': duration, 'observed_overlap': float(observed.real),
                               'analytic_overlap': analytic},
        'meaning': 'mathematical shared-environment countermodel, not measured scattering rate'}

    # A common atomic energy phase mixes cat labels. Model an ideal cat by
    # CNOT encoding into orthogonal motion branches, then undo that encoding.
    # This keeps the erroneous unrecombined motion, which a label-only model loses.
    cnot = np.zeros((4, 4), complex)
    for anc in (0, 1):
        for motion in (0, 1):
            cnot[2*anc+(motion^anc), 2*anc+motion] = 1.
    encode = np.kron(cnot, I2)
    theta = 2*math.asin(math.sqrt(.03))
    ua = pulse(theta, 1j)@pulse(theta, 1.)
    ub = pulse(theta, 1.)@pulse(theta, 1j)
    conditional = np.zeros((4, 4), complex)
    conditional[:2, :2], conditional[2:, 2:] = ua, ub
    conditional = np.kron(I2, conditional)
    init = np.kron(np.array([1., 1.])/math.sqrt(2), np.array([1., 0., 0., 0.]))
    chi = .8
    mixed = np.kron(expm(-.5j*chi*X), np.eye(4))
    psi = encode@conditional@mixed@encode@init
    amp = psi.reshape((2, 4))
    rho_anc = amp@amp.conj().T
    measured = 2*rho_anc[0, 1]
    ideal = np.vdot(ub@np.array([1., 0.]), ua@np.array([1., 0.]))
    expected = ideal.real+1j*math.cos(chi)*ideal.imag
    assert abs(measured-expected) < 1e-13
    result['groups']['common_atomic_mixing_without_scalar_visibility'] = {
        'chi_scenario_not_dynamic_prediction': chi,
        'ideal_overlap': [float(ideal.real), float(ideal.imag)],
        'measured_qubit_coherence': [float(measured.real), float(measured.imag)],
        'real_quadrature_retention': 1., 'imaginary_quadrature_retention': math.cos(chi),
        'limitation': 'orthogonal spatial-branch toy, no CaOH+ material parameters',
        'blank_control': 'UA=UB implies no order-odd signal under the same common background'}

    # Exact finite-envelope scope counterexample to promoting a carrier-field
    # intensity identity to a pointwise spacetime identity. No apparatus length,
    # lifetime or rate is inferred from this dimensionless construction.
    a, b, delay, kx = 1., -2., .1, .39
    def intensities(time):
        gplus = math.exp(-(time-delay)**2/4)
        gminus = math.exp(-(time+delay)**2/4)
        f1 = a*gplus*np.exp(1j*kx)+b*gminus*np.exp(-1j*kx)
        f2 = b*gplus*np.exp(1j*kx)+a*gminus*np.exp(-1j*kx)
        return abs(f1)**2, abs(f2)**2
    envelope_error = 0.
    maximum_difference = 0.
    for time in np.linspace(-6., 6., 501):
        i1, i2 = intensities(time)
        formula = (a*a-b*b)*(math.exp(-(time-delay)**2/2)-math.exp(-(time+delay)**2/2))
        envelope_error = max(envelope_error, abs(i1-i2-formula))
        maximum_difference = max(maximum_difference, abs(i1-i2))
    integrated_difference, err = quad(lambda time: intensities(time)[0]-intensities(time)[1], -10., 10., epsabs=1e-12)
    assert envelope_error < 1e-13 and maximum_difference > .1 and abs(integrated_difference) < 1e-12
    result['groups']['finite_envelope_intensity_scope'] = {
        'dimensionless_delay': delay, 'beam_amplitudes': [a, b], 'kx': kx,
        'maximum_pointwise_intensity_difference': maximum_difference,
        'closed_form_identity_max_error': envelope_error,
        'integrated_fluence_difference': integrated_difference,
        'meaning': 'finite counterpropagating envelopes break instantaneous carrier identity; integrated fluence equality at fixed x survives'}

    # A harmonic Gaussian mixture can have nonzero log-overlap quartic response.
    # L(eps)=exp(-eps^2) cosh(eps^2/2), hence d^4 log L(0)=3 exactly.
    mean_variance = (Fraction(1)+Fraction(3))/2
    mean_squared_variance = (Fraction(1)+Fraction(9))/2
    fourth_log_coefficient = mean_squared_variance/8-mean_variance**2/8
    assert fourth_log_coefficient*math.factorial(4) == 3
    result['groups']['harmonic_mixture_quartic_countermodel'] = {
        'variance_values': [1, 3], 'weights': [.5, .5],
        'L': '0.5 exp(-epsilon^2/2)+0.5 exp(-3epsilon^2/2)',
        'log_L': '-epsilon^2+log(cosh(epsilon^2/2))',
        'fourth_log_derivative_at_zero': 3,
        'exact_rational_quartic_coefficient': str(fourth_log_coefficient),
        'status': 'exact symbolic identity; a nonzero fourth connected signal alone does not certify anharmonicity'}

    # Finite variable-history domination check. The proof in the note is uniform
    # and not limited to these sampled conditional probability trees.
    qstar, steps, checked = .2, 8, 0
    min_slack = 1.
    for _ in range(20):
        paths = {(): 1.}
        for j in range(steps):
            new = {}
            for hist, prob in paths.items():
                pz = qstar+(1-qstar)*rng.uniform(0, 1)
                new[hist+(0,)] = prob*(1-pz)
                new[hist+(1,)] = prob*pz
            paths = new
        for k in range(steps):
            actual = sum(v for h, v in paths.items() if sum(h) <= k)
            comparison = sum(math.comb(steps, j)*qstar**j*(1-qstar)**(steps-j) for j in range(k+1))
            min_slack = min(min_slack, comparison-actual)
            assert actual <= comparison+1e-13
            checked += 1
    result['groups']['memory_safe_erasure_failure_count'] = {'history_trees': 20,
        'lower_tail_checks': checked, 'minimum_slack': min_slack,
        'proof_scope': 'predeclared finite N; every conditional failure probability lower bounded'}

    N = 102729
    q_exact = -math.expm1(math.log(.9)/N)
    q_approx = -math.log(.9)/N
    n_zero = math.ceil(math.log(.05)/math.log1p(-1e-6))
    result['groups']['cost_and_survival_arithmetic'] = {
        'C_and_R_scenarios': [.52, .03], 'completed_two_setting_trials': N,
        'exact_independent_loss_ceiling_for_90pct_survival': q_exact,
        'source_first_order_loss_ceiling': q_approx,
        'first_order_overstatement': q_approx-q_exact,
        'zero_loss_trials_for_95pct_one_sided_1e_minus6_bound': n_zero,
        'five_sigma_completed_rate_minutes_at_assumed_50_Hz': N/50/60,
        'Hoeffding_one_sided_fixed_N_alpha_2p87e_minus7_coefficient': 2*math.log(1/2.87e-7),
        'scope': 'planning arithmetic; actual signal, reset independence, attempt rate, systematic error and loss remain unacquired'}

    if args.source_dir and args.replay_dir:
        old = json.loads((args.source_dir/'results.json').read_text())
        new = json.loads((args.replay_dir/'results.json').read_text())
        changes = []
        def compare(a, b, path=''):
            if isinstance(a, dict) and isinstance(b, dict):
                assert a.keys() == b.keys()
                for k in a: compare(a[k], b[k], path+'/'+k)
            elif isinstance(a, list) and isinstance(b, list):
                assert len(a) == len(b)
                for i, (aa, bb) in enumerate(zip(a, b)): compare(aa, bb, path+'/'+str(i))
            elif a != b:
                changes.append({'path': path, 'source': a, 'replay': b,
                                'absolute_difference': abs(a-b) if isinstance(a, (int, float)) and isinstance(b, (int, float)) else None})
        compare(old, new)
        maxdiff = max((v['absolute_difference'] or 0. for v in changes), default=0.)
        result['producer_replay'] = {'source_sha256': hashlib.sha256((args.source_dir/'results.json').read_bytes()).hexdigest(),
            'replay_sha256': hashlib.sha256((args.replay_dir/'results.json').read_bytes()).hexdigest(),
            'differences': changes, 'maximum_numeric_absolute_difference': maxdiff,
            'finite_width_independent_overlap_difference': abs((re+1j*im)-complex(new['noncommuting_control_scenarios'][1]['pure_ground_finite_width']['L_real'], new['noncommuting_control_scenarios'][1]['pure_ground_finite_width']['L_imag']))}
        assert maxdiff < 1e-10
        assert result['producer_replay']['finite_width_independent_overlap_difference'] < 1e-10
    args.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
