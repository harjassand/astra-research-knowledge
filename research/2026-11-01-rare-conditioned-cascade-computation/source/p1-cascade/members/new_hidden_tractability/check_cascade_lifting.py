"""Targeted independent checks of conditional threshold lifting.

The root-owned event_time_compiler is imported, not modified. This check attacks
the rectangular driver preimage (including cyclic influence and zero rates),
and integrates full two-node timed-path laws for one-sided model error. It also
preserves two assumption counterexamples. Numerical quadrature is evidence,
not a proof of total variation; the ordinary proof is in CASCADE_LIFTING_PROOF.txt.
"""

from __future__ import annotations

import itertools
import json
import math
from pathlib import Path
import sys

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'new_rare_event'))
from event_time_compiler import LocalRate, make_event_time_factor, thresholds_from_bins


def independent_held_bins(rates, thresholds, bins, deadline):
    dt = deadline / bins
    cumulative = np.zeros(len(rates))
    failed = np.zeros(len(rates), dtype=bool)
    output = np.full(len(rates), bins)
    for j in range(bins):
        lambdas = np.array([r.at_state(failed) for r in rates])
        cumulative += dt * lambdas
        new = (~failed) & (thresholds < cumulative)
        output[new] = j
        failed[new] = True
    return output


def rectangular_preimage():
    rates = [LocalRate((2,), np.array([0.4, 4.0])),
             LocalRate((0,), np.array([0.0, 3.0])),
             LocalRate((1,), np.array([0.05, 5.0]))]
    n, bins, deadline = len(rates), 3, 0.7
    factors = [make_event_time_factor(i, r, bins, deadline) for i, r in enumerate(rates)]
    mass = 0.0
    assignments = 0
    draws = 0
    rng = np.random.default_rng(41093)
    for values in itertools.product(range(bins + 1), repeat=n):
        log_p = sum(float(f.values[tuple(values[j] for j in f.scope)]) for f in factors)
        if not np.isfinite(log_p):
            continue
        mass += math.exp(log_p)
        assignments += 1
        for _ in range(20):
            thresholds, _ = thresholds_from_bins(rates, np.array(values), bins, deadline, rng)
            returned = independent_held_bins(rates, thresholds, bins, deadline)
            assert np.array_equal(returned, values)
            draws += 1
    assert abs(mass - 1) < 1e-13
    return {'nodes': n, 'bins': bins, 'cyclic_parent_graph': True,
            'zero_baseline_rate_present': True, 'positive_assignments_checked': assignments,
            'conditional_driver_draws_checked': draws, 'normalization_error': abs(mass - 1),
            'all_reconstructed_drivers_return_original_bin_assignment': True}


def path_quadrature(rates, deadline, order=96):
    """Two irreversible nodes: rates (a,b,c,d), where b>=a and d>=c.

    a=node1 initially, b=node1 after2; c=node2 initially, d=node2 after1.
    Returns positive quadrature cell masses for full timed paths. Within a
    channel the quadrature cells agree across models, allowing a TV integral.
    """
    a, b, c, d = rates
    nodes, weights = np.polynomial.legendre.leggauss(order)
    u, w = (nodes + 1) / 2, weights / 2
    t = deadline * u
    one1 = w * deadline * a * np.exp(-(a + c) * t - d * (deadline - t))
    one2 = w * deadline * c * np.exp(-(a + c) * t - b * (deadline - t))
    first = deadline * u[:, None]
    second = first + (deadline - first) * u[None, :]
    jacobian = deadline * (deadline - first)
    quadrature = w[:, None] * w[None, :] * jacobian
    both12 = quadrature * a * d * np.exp(-(a + c) * first - d * (second - first))
    both21 = quadrature * c * b * np.exp(-(a + c) * first - b * (second - first))
    return {'none': np.array([math.exp(-(a+c)*deadline)]),
            'only1': one1, 'only2': one2,
            'both12': both12.ravel(), 'both21': both21.ravel()}


def conditional_path_tv():
    truth = np.array([1.0, 7.0, 2.0, 9.0])
    zeta = 0.02
    lower = truth * np.array([1-zeta, 1-0.3*zeta, 1-0.7*zeta, 1-zeta])
    bound = 1 - (1-zeta) ** 2
    cases = []
    for deadline in [1e-5, 0.1, 2.0, 10.0]:
        p = path_quadrature(truth, deadline)
        q = path_quadrature(lower, deadline)
        assert abs(sum(a.sum() for a in p.values()) - 1) < 2e-12
        assert abs(sum(a.sum() for a in q.values()) - 1) < 2e-12
        for event, channels in [('both', ['both12', 'both21']),
                                ('node1', ['only1', 'both12', 'both21']),
                                ('any', ['only1', 'only2', 'both12', 'both21'])]:
            p_cells = np.concatenate([p[name] for name in channels])
            q_cells = np.concatenate([q[name] for name in channels])
            p_event, q_event = float(p_cells.sum()), float(q_cells.sum())
            assert q_event <= p_event * (1+1e-12)
            assert q_event / p_event >= (1-zeta)**2 - 1e-12
            tv = float(np.abs(p_cells/p_event-q_cells/q_event).sum()/2)
            assert tv <= bound + 1e-12
            cases.append({'deadline': deadline, 'event': event,
                          'true_event_probability': p_event,
                          'model_event_probability_ratio': q_event/p_event,
                          'quadrature_path_total_variation': tv})
    return {'one_sided_fraction_error': zeta, 'proved_tv_bound': bound, 'cases': cases,
            'scope': '96-point positive quadrature on each timed-path stratum; analytic theorem separately proved.'}


def assumption_failures():
    # Non-attractive rate: node1 fires at .1 and shuts node2 off. Held input
    # still allows node2 to fire at .5 in the same unit bin.
    inhibitory_true_times = [0.1, None]
    inhibitory_held_times = [0.1, 0.5]

    # Exactly one failure is not upward. A small one-sided rate change can
    # bias its route by exp(zeta*T), defeating an n*zeta conditional TV bound.
    zeta, deadline = 0.01, 1000.0
    p_log = np.array([math.log(-math.expm1(-deadline))-deadline] * 2)
    q_log = np.array([math.log(-math.expm1(-(1-zeta)*deadline))-deadline,
                      math.log(-math.expm1(-deadline))-(1-zeta)*deadline])
    p = np.exp(p_log-p_log.max()); p /= p.sum()
    q = np.exp(q_log-q_log.max()); q /= q.sum()
    route_tv = float(np.abs(p-q).sum()/2)
    assert route_tv > 0.49 and route_tv > 2*zeta
    return {'nonattractive_counterexample': {
                'initial_rates': [1.0, 1.0], 'node2_rate_after_node1': 0.0,
                'thresholds': [0.1, 0.5], 'bin_width': 1.0,
                'true_failure_times': inhibitory_true_times,
                'held_failure_times': inhibitory_held_times,
                'delayed_event_subset_fails': True},
            'nonupward_counterexample': {
                'true_independent_rates': [1.0, 1.0],
                'lower_independent_rates': [1-zeta, 1.0],
                'deadline': deadline, 'event': 'exactly one node fails',
                'true_route_probability': p.tolist(), 'lower_model_route_probability': q.tolist(),
                'route_marginal_total_variation': route_tv,
                'invalid_unrestricted_n_zeta_bound': 2*zeta}}


def main():
    result = {'rectangular_driver_preimage': rectangular_preimage(),
              'one_sided_conditional_path_law': conditional_path_tv(),
              'assumption_counterexamples': assumption_failures()}
    Path(__file__).with_name('cascade_lifting_results.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
