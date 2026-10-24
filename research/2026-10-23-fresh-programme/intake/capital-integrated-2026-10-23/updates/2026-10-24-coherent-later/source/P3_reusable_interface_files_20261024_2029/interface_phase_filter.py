"""New Pro3 work: phase-dependent partial gates and correlated entrance laws.

The source-level action below evaluates compact free kernels and performs exact
Bayesian entrance updates given first-event densities. The test supplies those
densities using small expanded active-block references, and compares the full
event/entrance result against an independently expanded global CTMC. It does not
claim that expanded reference evaluation is the compact Volterra solver.

Dependencies: numpy, scipy. No historical Astra helper is imported.
"""
from dataclasses import dataclass
from itertools import product
import json
import numpy as np
from scipy.linalg import expm


@dataclass(frozen=True)
class Gate:
    target: tuple
    rate: float
    reset: tuple = ()  # pairs (global site index, deterministic new bit)


@dataclass(frozen=True)
class Phase:
    support: tuple
    gates: tuple


def binary_transition(alpha, beta, t):
    lam = alpha + beta
    if lam == 0:
        return np.eye(2)
    p = alpha / lam
    e = np.exp(-lam * t)
    return np.array([[1-p+p*e, p*(1-e)],
                     [(1-p)*(1-e), p+(1-p)*e]])


def check_source(alpha, beta, phase):
    n = len(alpha)
    assert len(beta) == n and np.min(alpha) >= 0 and np.min(beta) >= 0
    assert len(set(phase.support)) == len(phase.support)
    assert all(0 <= i < n for i in phase.support)
    for gate in phase.gates:
        assert len(gate.target) == len(phase.support)
        assert all(v in (0, 1) for v in gate.target) and gate.rate >= 0
        assert len(dict(gate.reset)) == len(gate.reset)
        assert all(0 <= i < n and v in (0, 1) for i, v in gate.reset)


def compact_kernel(alpha, beta, phase, t):
    """K_ij(t), with cost linear in active support for a fixed gate count."""
    check_source(alpha, beta, phase)
    trans = [binary_transition(alpha[i], beta[i], t) for i in phase.support]
    m = len(phase.gates)
    K = np.ones((m, m))
    for l, P in enumerate(trans):
        for i, gi in enumerate(phase.gates):
            for j, gj in enumerate(phase.gates):
                K[i, j] *= P[gi.target[l], gj.target[l]]
    return K * np.array([g.rate for g in phase.gates])[None, :]


def compact_source_terms(alpha, beta, phase, factors, t):
    """b_rj(t) for R product components; factors shape R x n x 2."""
    R = len(factors)
    b = np.ones((R, len(phase.gates)))
    for l, i in enumerate(phase.support):
        predicted = factors[:, i, :] @ binary_transition(alpha[i], beta[i], t)
        for j, gate in enumerate(phase.gates):
            b[:, j] *= predicted[:, gate.target[l]]
    return b * np.array([g.rate for g in phase.gates])[None, :]


def entrance_update(alpha, beta, phase, weights, factors, mark, t, densities):
    """Update from an observed (time, mark).

    densities[r,j] is the first-event density from product component r. It can
    be obtained from f_r + f_r*K = b_r through the existing event-action method.
    This update does not expand configurations and does not increase R.
    """
    gate = phase.gates[mark]
    likelihoods = np.asarray(densities)[:, mark]
    normalizer = float(np.dot(weights, likelihoods))
    if normalizer <= 0:
        raise ValueError('Observation has zero density under the supplied model')
    next_weights = weights * likelihoods / normalizer
    next_factors = np.empty_like(factors)
    pinned = dict(zip(phase.support, gate.target))
    pinned.update(dict(gate.reset))
    for i in range(len(alpha)):
        if i in pinned:
            next_factors[:, i, :] = 0
            next_factors[:, i, pinned[i]] = 1
        else:
            next_factors[:, i, :] = factors[:, i, :] @ binary_transition(alpha[i], beta[i], t)
    return next_weights, next_factors, normalizer


def expanded_generator(alpha, beta):
    n = len(alpha)
    states = list(product((0, 1), repeat=n))
    lookup = {s: k for k, s in enumerate(states)}
    Q = np.zeros((2**n, 2**n))
    for k, s in enumerate(states):
        for i in range(n):
            new = list(s); new[i] = 1-new[i]
            rate = alpha[i] if s[i] == 0 else beta[i]
            Q[k, lookup[tuple(new)]] += rate
            Q[k, k] -= rate
    return states, lookup, Q


def expand_product(factors):
    out = np.array([1.0])
    for f in factors:
        out = np.kron(out, f)
    return out


def expand_mixture(weights, factors):
    return sum((w * expand_product(mu) for w, mu in zip(weights, factors)),
               np.zeros(2**factors.shape[1]))


def active_reference_densities(alpha, beta, phase, factors, t):
    """Small-reference oracle ONLY: expands the active block, not the main claim."""
    A = list(phase.support)
    states, lookup, Q = expanded_generator(alpha[A], beta[A])
    B = np.zeros((len(states), len(phase.gates)))
    for j, g in enumerate(phase.gates):
        B[lookup[g.target], j] += g.rate
    H = Q - np.diag(B.sum(axis=1))
    propagator = expm(t * H)
    return np.array([expand_product(mu[A]) @ propagator @ B for mu in factors])


def global_reference_step(alpha, beta, phase, law, mark, t):
    states, lookup, Q = expanded_generator(alpha, beta)
    hazards = np.zeros((len(states), len(phase.gates)))
    for k, s in enumerate(states):
        for j, g in enumerate(phase.gates):
            if tuple(s[i] for i in phase.support) == g.target:
                hazards[k, j] = g.rate
    killed = Q - np.diag(hazards.sum(axis=1))
    entered = (law @ expm(t * killed)) * hazards[:, mark]
    result = np.zeros_like(law)
    for k, s in enumerate(states):
        new = list(s)
        for i, v in phase.gates[mark].reset:
            new[i] = v
        result[lookup[tuple(new)]] += entered[k]
    normalizer = result.sum()
    return result / normalizer, normalizer


def run_checks():
    alpha = np.array([0.08, 0.18, 0.05, 0.0825])
    beta = np.array([0.12, 0.12, 0.05, 0.0675])
    phases = [
        Phase((0, 1), (Gate((1, 1), 1.3, ((0, 0),)), Gate((0, 0), 0.4))),
        Phase((1, 2, 3), (Gate((1, 1, 1), 1.1, ((2, 0),)), Gate((0, 0, 0), 0.6))),
    ]
    weights = np.array([0.5, 0.5])
    probabilities = np.array([[0.9, 0.8, 0.95, 0.9], [0.2, 0.1, 0.05, 0.1]])
    factors = np.stack([1-probabilities, probabilities], axis=-1)
    law = expand_mixture(weights, factors)
    records = [(0, 0.7, 0), (1, 0.6, 0), (0, 0.45, 1), (1, 0.8, 1)]
    errors = []
    log_compact = log_reference = 0.0
    witness = None
    for step, (q, t, mark) in enumerate(records):
        phase = phases[q]
        densities = active_reference_densities(alpha, beta, phase, factors, t)
        weights, factors, p = entrance_update(alpha, beta, phase, weights, factors, mark, t, densities)
        law, p_ref = global_reference_step(alpha, beta, phase, law, mark, t)
        errors.append({'step': step+1, 'density_error': abs(p-p_ref),
                       'posterior_l1_error': float(np.abs(expand_mixture(weights, factors)-law).sum()),
                       'mixture_width': len(weights)})
        log_compact += np.log(p); log_reference += np.log(p_ref)
        if step == 0:
            marginals = np.einsum('r,rni->ni', weights, factors)
            correlated = np.dot(weights, factors[:, 2, 1]*factors[:, 3, 1])
            independent = marginals[2, 1]*marginals[3, 1]
            f_true = active_reference_densities(alpha, beta, phases[1], factors, 0.6)
            true_next = np.dot(weights, f_true[:, 0])
            naive_next = active_reference_densities(alpha, beta, phases[1], marginals[None, :, :], 0.6)[0, 0]
            witness = {
                'posterior_weights': weights.tolist(),
                'inactive_pair_both_active': float(correlated),
                'product_of_inactive_marginals': float(independent),
                'inactive_pair_covariance': float(correlated-independent),
                'next_mark_density_correlated': float(true_next),
                'next_mark_density_independent_replacement': float(naive_next),
                'density_relative_error_from_discarding_correlation': float((naive_next-true_next)/true_next)
            }
    assert max(e['posterior_l1_error'] for e in errors) < 1e-12
    assert abs(log_compact-log_reference) < 1e-12
    return {'status': 'new scientific implementation; small expanded numerical references',
            'checks': errors, 'joint_log_density_error': abs(log_compact-log_reference),
            'correlation_witness': witness,
            'scope': 'Compact kernels and entrance updates are implemented. Small-reference active-block exponentials supply the test densities; the file does not claim a new general certified Volterra discretization.'}


if __name__ == '__main__':
    result = run_checks()
    print(json.dumps(result, indent=2))
    with open('interface_phase_filter_results.json', 'w') as handle:
        json.dump(result, handle, indent=2)
