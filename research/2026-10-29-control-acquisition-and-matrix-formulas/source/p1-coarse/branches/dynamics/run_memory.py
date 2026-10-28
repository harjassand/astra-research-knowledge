"""Synthetic passive-memory acquisition with a rigorous analytic error formula.

The LP is a numerical proposal. A separate high-precision interval evaluation
checks every retained weight, mass and sample residual before the analytic
certificate is reported. Dense trajectories are diagnostics, not proof.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import mpmath as mp
import numpy as np
from scipy.optimize import linprog


ROOT = Path(__file__).resolve().parent


def tail(m):
    q = 0.25
    n = m + 1
    return q**n * (n*n/(1-q) + 2*n*q/(1-q)**2 + q*(1+q)/(1-q)**3)


def step(times, rates, weights):
    return (-np.expm1(-np.outer(np.asarray(times), rates))) @ weights


def impulse(times, rates, weights):
    return np.exp(-np.outer(np.asarray(times), rates)) @ (weights*rates)


def iv_step(t, rates, weights):
    # All stored floats are treated as their exact binary rational values.
    z = mp.iv.mpf(0)
    for rate, weight in zip(rates, weights):
        if weight:
            z += mp.iv.mpf(float(weight)) * (-mp.iv.expm1(-mp.iv.mpf(float(rate))*mp.iv.mpf(float(t))))
    return z


def interval_bounds(z):
    # float conversion alone is nearest-rounded; nextafter makes it outward.
    return np.nextafter(float(z.a), -np.inf), np.nextafter(float(z.b), np.inf)


def main():
    mp.mp.dps = 70
    mp.iv.dps = 50
    M, Lambda, T, requested = 1.0, 100.0, 10000.0, 0.01
    sensor_eta = 1e-8
    t0 = requested/(12*M*Lambda)
    edges = [t0]
    while edges[-1] < T:
        edges.append(min(2*edges[-1], T))
    B = len(edges)-1
    m = 2
    while 32*M*B*tail(m) > requested/3:
        m += 1

    times = []
    max_timing_error = mp.mpf(0)
    for a, b in zip(edges[:-1], edges[1:]):
        for j in range(m+1):
            ideal = (mp.mpf(a)+mp.mpf(b))/2 + (mp.mpf(b)-mp.mpf(a))/2*mp.cos(mp.pi*j/m)
            actual = float(ideal)
            max_timing_error = max(max_timing_error, abs(mp.mpf(actual)-ideal))
            times.append(actual)
    times = np.array(sorted(set(times)))
    assert len(times) == B*m+1

    rng = np.random.default_rng(1716)
    source_rates = np.exp(rng.uniform(np.log(1e-10), np.log(99.0), 128))
    source_weights = rng.uniform(0.2, 1.0, len(source_rates))
    source_weights = source_weights/source_weights.sum()*0.95
    # Actual measured centers: interval-computed source plus a declared error.
    centers = []
    source_roundoff = 0.0
    for i, t in enumerate(times):
        lo, hi = interval_bounds(iv_step(t, source_rates, source_weights))
        center = (lo+hi)/2 + sensor_eta*0.5*math.sin(i*1.741)
        source_roundoff = max(source_roundoff, abs(center-lo), abs(center-hi))
        centers.append(center)
    centers = np.asarray(centers)
    assert source_roundoff <= sensor_eta

    fits = []
    accepted = None
    for ngrid in [256, 512, 1024, 2048]:
        rates = np.geomspace(requested/(1000*M*T), Lambda, ngrid)
        A = -np.expm1(-np.outer(times, rates))
        # Variables are nonnegative weights and the nonnegative max residual.
        lhs = np.vstack([np.column_stack([A, -np.ones(len(times))]),
                         np.column_stack([-A, -np.ones(len(times))]),
                         np.r_[np.ones(ngrid), 0.0][None, :]])
        rhs = np.r_[centers, -centers, M]
        obj = np.r_[np.zeros(ngrid), 1.0]
        fit = linprog(obj, A_ub=lhs, b_ub=rhs, bounds=(0, None), method='highs',
                      options={'primal_feasibility_tolerance': 1e-9,
                               'dual_feasibility_tolerance': 1e-9})
        if not fit.success:
            fits.append({'grid': ngrid, 'success': False, 'message': fit.message})
            continue
        weights = np.maximum(fit.x[:-1], 0.0)
        # Make the positive mass constraint hold even after binary rounding.
        if weights.sum() > M*(1-1e-12):
            weights *= M*(1-2e-12)/weights.sum()
        keep = weights > 0
        model_rates, model_weights = rates[keep], weights[keep]
        residual = 0.0
        for t, c in zip(times, centers):
            lo, hi = interval_bounds(iv_step(t, model_rates, model_weights))
            residual = max(residual, abs(lo-c), abs(hi-c))
        mass_iv = sum((mp.iv.mpf(float(w)) for w in model_weights), mp.iv.mpf(0))
        _, mass_upper = interval_bounds(mass_iv)
        assert mass_upper <= M
        timing_error = np.nextafter(float(max_timing_error), np.inf)
        # Each true/model derivative bound is M*Lambda.
        eta = sensor_eta + M*Lambda*timing_error
        residual_ideal = residual + M*Lambda*timing_error
        error = (2*M*Lambda*t0 + B*(32*M*tail(m)+2*m*math.sqrt(2*m)*(eta+residual_ideal)))
        error = np.nextafter(error*(1+1e-12), np.inf)
        info = {'grid': ngrid, 'success': True, 'lp_proposed_residual': float(fit.x[-1]),
                'retained_modes': int(keep.sum()), 'validated_residual_upper': residual,
                'validated_mass_upper': mass_upper, 'analytic_l1_upper': error,
                'target_met': bool(error <= requested)}
        fits.append(info)
        if error <= requested:
            accepted = (model_rates, model_weights, info)
            break
    if accepted is None:
        raise RuntimeError(f'No certified model found: {fits}')
    model_rates, model_weights, info = accepted

    # Dense diagnostic is deliberately separate from the analytic certificate.
    dense = np.r_[0, np.geomspace(t0/100, T, 30000)]
    difference = np.abs(impulse(dense, source_rates, source_weights)-impulse(dense, model_rates, model_weights))
    l1_diagnostic = float(np.trapezoid(difference, dense))
    source_step = step(dense, source_rates, source_weights)
    model_step = step(dense, model_rates, model_weights)

    # All bounded-input certificate can be reused for a near worst-case sign input.
    # Reversed impulse-error signs maximize the selected terminal convolution
    # in the continuum. This is checker-only and not supplied to the learner.
    signed_difference = impulse(dense, source_rates, source_weights)-impulse(dense, model_rates, model_weights)
    sign_changes = int(np.count_nonzero(np.diff(np.signbit(signed_difference))))

    # Analytic early-experiment obstruction with exactly known DC gain.
    tau, U, obstruction_eta = 100.0, 1.0, 1e-5
    a = 4*obstruction_eta/(U*tau)
    future_time = 2*math.log(2)/a
    future_step_gap = math.exp(-a*future_time/2)-math.exp(-a*future_time)
    summary = {
        'source_class': 'positive relaxation mixture, supplied M and upper rate, no lower rate',
        'M': M, 'Lambda': Lambda, 'T': T, 'requested_l1_error': requested,
        'source_modes_checker_only': len(source_rates), 'source_min_rate_checker_only': float(source_rates.min()),
        'blocks': B, 'degree': m, 'scalar_readings': len(times),
        'physical_wait': T, 'prepared_step_trajectories': 1,
        'sensor_error_contract': sensor_eta, 'checked_source_center_error_upper': source_roundoff,
        'maximum_command_timing_error': float(max_timing_error),
        'fits_in_order_all_charged': fits,
        'analytic_guarantee': 'every exogenous input bounded by U has finite-horizon output error <= U*analytic_l1_upper',
        'dense_l1_diagnostic_not_certificate': l1_diagnostic,
        'dense_step_sup_diagnostic_not_certificate': float(np.max(np.abs(source_step-model_step))),
        'checker_near_worst_input_sign_changes': sign_changes,
        'obstruction': {'early_experiment_duration': tau, 'eta': obstruction_eta, 'input_amplitude': U,
                        'rate_a': a, 'rate_b': a/2, 'common_transcript_gap_bound': U*a*tau/2,
                        'later_time': future_time, 'later_step_gap': future_step_gap},
        'scope': 'Synthetic execution; analytic proof plus interval-validated node errors. No physical device, no inferred source class, no priority or comparative-speedup claim.'
    }
    (ROOT/'RESULTS.json').write_text(json.dumps(summary, indent=2)+'\n')
    np.savez_compressed(ROOT/'DATA.npz', times=times, centers=centers, source_rates=source_rates,
                        source_weights=source_weights, model_rates=model_rates, model_weights=model_weights,
                        edges=np.asarray(edges))
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
