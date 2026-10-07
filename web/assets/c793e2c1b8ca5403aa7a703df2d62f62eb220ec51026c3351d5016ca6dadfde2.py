"""Independent finite generator checks and an observed-flips-only diagnostic.

No theorem is inferred from these fixtures.  Matrix checks use the entire
continuous-time generator, separately from the proposed two-state quotient.
"""
from __future__ import annotations

import itertools
import json
import math
import time
from fractions import Fraction
from pathlib import Path

import numpy as np

OUT = Path(__file__).with_name("learning_acquisition_check.json")


def all_states(n):
    return np.array(list(itertools.product((-1, 1), repeat=n)), dtype=int)


def generator(states, potentials):
    """Construct heat-bath generator from an explicit potential table."""
    n = states.shape[1]
    index = {tuple(x): a for a, x in enumerate(states)}
    rates = np.zeros((len(states), n))
    L = np.zeros((len(states), len(states)))
    for a, x in enumerate(states):
        for i in range(n):
            y = x.copy()
            y[i] *= -1
            b = index[tuple(y)]
            q = 1 / (1 + math.exp(potentials[a] - potentials[b]))
            rates[a, i] = q
            L[a, b] = q
        L[a, a] = -sum(rates[a])
    pi = np.exp(potentials - max(potentials))
    pi /= sum(pi)
    return L, rates, pi


def count_covariance(L, rates, pi, horizon):
    """Evaluate exact count second-moment integral via a symmetric eigensolve."""
    root = np.sqrt(pi)
    S = root[:, None] * L / root[None, :]
    assert np.max(np.abs(S - S.T)) < 1e-11
    eigenvalues, Q = np.linalg.eigh(S)
    integral = np.empty_like(eigenvalues)
    for j, lam in enumerate(eigenvalues):
        if abs(lam * horizon) < 1e-7:
            integral[j] = horizon ** 2 / 2
        else:
            integral[j] = (math.expm1(lam * horizon) - lam * horizon) / lam ** 2
    coeff = Q.T @ (root[:, None] * rates)
    moments = 2 * coeff.T @ (integral[:, None] * coeff)
    mean_rate = pi @ rates
    cov = moments - np.outer(mean_rate, mean_rate) * horizon ** 2
    cov[np.diag_indices_from(cov)] += mean_rate * horizon
    return cov, mean_rate


def parity_cov(k, tau, horizon):
    r = (1 - tau ** 2) / 2
    return r * tau ** 2 * (horizon / k + math.expm1(-k * horizon) / k ** 2)


def gadget(x):
    a, b, c, s, e = x
    return Fraction(a*b + a*c + a*b*s - a*c*s + e*b - e*c - e*b*s - e*c*s, 2)


def closed_path_check():
    n = 5
    states = list(itertools.product((-1, 1), repeat=n))
    models = {
        "independent_fields": lambda x: sum(x),
        "parity_hyperedge": lambda x: math.prod(x),
        "degree_three_gadget": gadget,
    }
    tau = Fraction(1, 2)
    activity = (1 - tau*tau) / 4
    checked = 0
    edges = {}
    rng = np.random.default_rng(880314)
    for name, potential in models.items():
        derivatives = {}
        for x in states:
            for i in range(n):
                y = list(x)
                y[i] *= -1
                delta = potential(tuple(y)) - potential(x)
                assert abs(delta) == 2
                derivatives[(x, i)] = delta
        model_edges = []
        for i in range(n):
            for j in range(i):
                varying = False
                for x in states:
                    y = list(x)
                    y[j] *= -1
                    if derivatives[(x, i)] != derivatives[(tuple(y), i)]:
                        varying = True
                if varying:
                    model_edges.append([j, i])
        edges[name] = model_edges
        for length in (2, 4, 6, 8, 12):
            for repeat in range(300):
                x = states[int(rng.integers(len(states)))]
                half = list(rng.integers(0, n, size=length//2))
                word = half + half
                rng.shuffle(word)
                state = list(x)
                value = Fraction(1)
                for i in word:
                    new = state.copy()
                    new[i] *= -1
                    delta = potential(tuple(new)) - potential(tuple(state))
                    # A potential increment +2 has rate (1+tau)/2.
                    value *= (1 + tau * Fraction(delta)/2) / 2
                    state = new
                assert tuple(state) == x
                assert value == activity ** (length//2)
                checked += 1
    assert len(edges["independent_fields"]) == 0
    assert len(edges["parity_hyperedge"]) == 10
    assert len(edges["degree_three_gadget"]) == 8
    return {"exact_closed_paths": checked, "gadget_states": 32, "dependency_edges": edges}


def matrix_checks():
    worst = 0.0
    checked = 0
    for k in range(2, 8):
        states = all_states(k)
        for tau in (0.2, -0.6, 0.8):
            theta = math.atanh(tau)
            pot = theta * np.prod(states, axis=1)
            L, rates, pi = generator(states, pot)
            for horizon in (0.1, 0.7, 2.0):
                cov, mean = count_covariance(L, rates, pi, horizon)
                predicted = parity_cov(k, tau, horizon)
                r = (1-tau*tau)/2
                expected = np.full((k, k), predicted)
                expected[np.diag_indices(k)] += r*horizon
                err = max(np.max(np.abs(cov-expected)), np.max(np.abs(mean-r)))
                assert err < 2e-12, (k, tau, horizon, err)
                worst = max(worst, float(err))
                checked += 1
    states = all_states(6)
    groups = ((0, 1, 2), (3, 4))
    taus = (0.6, -0.4)
    pot = sum(math.atanh(t) * np.prod(states[:, g], axis=1) for g, t in zip(groups, taus))
    L, rates, pi = generator(states, pot)
    cov, mean = count_covariance(L, rates, pi, 0.4)
    expected = np.zeros((6, 6))
    for g, t in zip(groups, taus):
        for i in g:
            for j in g:
                expected[i, j] = parity_cov(len(g), t, 0.4)
            expected[i, i] += (1-t*t)*0.4/2
    expected[5, 5] = 0.2
    err = float(np.max(np.abs(cov-expected)))
    assert err < 2e-12
    gadget_states = all_states(5)
    tau = 0.5
    theta = math.atanh(tau)
    potential = np.array([theta * float(gadget(x)) for x in gadget_states])
    Lg, qg, pg = generator(gadget_states, potential)
    mean_g = pg @ qg
    rate_cov = qg.T @ (pg[:, None] * qg) - np.outer(mean_g, mean_g)
    assert np.max(np.abs(mean_g - (1-tau*tau)/2)) < 1e-12
    active_cov = []
    for i in range(5):
        for j in range(i):
            # Compute the mixed derivative independently from the potential table.
            prob_active = 0.0
            for a, x in enumerate(gadget_states):
                xi = x.copy(); xi[i] *= -1
                xj = x.copy(); xj[j] *= -1
                xij = xi.copy(); xij[j] *= -1
                c = (gadget(x)-gadget(xi)-gadget(xj)+gadget(xij))/4
                if c != 0:
                    prob_active += pg[a]
            predicted_rate_cov = tau*tau*(1-tau*tau)/4 * prob_active
            assert abs(rate_cov[i,j]-predicted_rate_cov) < 1e-12
            active_cov.append([j,i,float(rate_cov[i,j]),prob_active])
    return {"full_generator_cases": checked+2, "largest_absolute_error": max(worst, err),
            "gadget_stationary_rate_covariance": active_cov}


def metastability_checks():
    """Exact rational gate identities and Chernoff inequalities."""
    gates = 0
    tails = 0
    for n in range(2, 12, 2):
        for x in itertools.product((-1, 1), repeat=n):
            m = sum(x)
            if m > 0:
                for i in range(n):
                    m_next = m - 2*x[i]
                    assert abs(m_next)-abs(m) == -2*x[i]
                    gates += 1
    for n in range(2, 62, 2):
        for tau in (Fraction(1,5), Fraction(1,2), Fraction(4,5)):
            p = (1+tau)/2
            tail = sum(Fraction(math.comb(n,a))*p**a*(1-p)**(n-a)
                       for a in range((n+2)//2+1))
            bound = (1+tau)/(1-tau) * (1-tau*tau)**(n//2)
            assert tail <= bound
            tails += 1
    return {"exact_identical_gate_checks": gates, "exact_binomial_chernoff_checks": tails}


def flips_only_diagnostic():
    """One continuous Gillespie path; no failed attempts are generated/stored."""
    rng = np.random.default_rng(5423087)
    n = 18
    groups = [list(range(0, 3)), list(range(3, 7)), list(range(7, 10)), list(range(10, 12))]
    taus = [0.65, -0.8, 0.7, -0.6]
    group_of = [-1] * n
    for a, g in enumerate(groups):
        for i in g:
            group_of[i] = a
    spins = np.ones(n, dtype=int)
    parities = np.ones(len(groups), dtype=int)
    rates = np.full(n, 0.5)
    for a, g in enumerate(groups):
        rates[g] = (1-taus[a]*parities[a])/2
    now = 0.0
    total_events = 0
    sample_trace = []
    next_time = float(rng.exponential(1 / sum(rates)))
    def advance(end, counts=None):
        nonlocal now, next_time, total_events
        while next_time <= end:
            now = next_time
            draw = float(rng.random()) * float(sum(rates))
            i = int(np.searchsorted(np.cumsum(rates), draw))
            spins[i] *= -1
            if counts is not None:
                counts[i] += 1
            a = group_of[i]
            if a >= 0:
                parities[a] *= -1
                rates[groups[a]] = (1-taus[a]*parities[a])/2
            total_events += 1
            if len(sample_trace) < 20:
                sample_trace.append([now, i])
            next_time = now + float(rng.exponential(1 / sum(rates)))
        now = end
    # A finite diagnostic, not the theorem's conservative sample bound.
    # Public bounds, not actual hidden group sizes/amplitudes, set the threshold.
    K, tau_lower, tau_upper = 4, 0.6, 0.8
    M, block, gap = 200000, 0.3, 1.0
    advance(20.0)
    samples = np.zeros((M, n), dtype=int)
    for a in range(M):
        advance(now + gap)
        advance(now + block, samples[a])
    empirical = np.cov(samples, rowvar=False, ddof=0)
    truth = np.zeros((n, n), dtype=bool)
    predicted = np.zeros((n, n), dtype=float)
    for g, tau in zip(groups, taus):
        for i in g:
            for j in g:
                if i != j:
                    truth[i, j] = True
                    predicted[i, j] = parity_cov(len(g), tau, block)
    minimum_signal = min(parity_cov(len(g), tau, block) for g, tau in zip(groups, taus))
    public_signal_lower = (1-tau_upper**2)/2 * tau_lower**2 * (
        block/K + math.expm1(-K*block)/K**2)
    threshold = public_signal_lower/2
    recovered = empirical > threshold
    np.fill_diagonal(recovered, False)
    correct = bool(np.array_equal(recovered, truth))
    assert correct, (np.argwhere(recovered != truth), threshold)
    max_nonedge = float(np.max(empirical[~truth & ~np.eye(n, dtype=bool)]))
    min_edge = float(np.min(empirical[truth]))
    return {
        "seed": 5423087, "n": n, "groups": groups, "taus": taus,
        "sample_blocks": M, "block_time": block, "between_block_gap": gap,
        "physical_time": now, "actual_flip_events": total_events,
        "failed_attempt_records": 0, "all_edges_correct": correct,
        "expected_minimum_signal": minimum_signal, "threshold": threshold,
        "public_bounds": {"K":K,"tau_lower":tau_lower,"tau_upper":tau_upper},
        "public_signal_lower": public_signal_lower,
        "threshold_uses_hidden_parameters": False,
        "largest_nonedge_covariance": max_nonedge,
        "smallest_edge_covariance": min_edge,
        "largest_entrywise_covariance_error": float(np.max(np.abs((empirical-predicted)[~np.eye(n,dtype=bool)]))),
        "first_twenty_actual_flips": sample_trace,
        "status": "finite diagnostic; conservative theorem bounds not run",
    }


if __name__ == "__main__":
    start = time.perf_counter()
    report = {"closed_path_obstruction": closed_path_check(), "generator_identity": matrix_checks(),
              "metastability_lower_bound": metastability_checks()}
    report["continuous_path_diagnostic"] = flips_only_diagnostic()
    report["wall_seconds"] = time.perf_counter() - start
    OUT.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({key: value for key, value in report.items() if key != "continuous_path_diagnostic"}, indent=2))
    print(json.dumps({key:value for key,value in report["continuous_path_diagnostic"].items() if key != "first_twenty_actual_flips"}, indent=2))
