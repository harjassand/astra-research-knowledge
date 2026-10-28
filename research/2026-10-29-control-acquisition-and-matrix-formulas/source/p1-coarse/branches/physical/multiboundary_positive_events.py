"""Three-boundary positive-event acquisition; no hidden IDs in its receipts.

Native trajectories use integer transition probabilities.  All certificate
arithmetic, confidence endpoint acceptance, and hidden-source checks are exact.
Floating point only proposes confidence and semidefinite endpoints.
"""
from fractions import Fraction as F
from pathlib import Path
from math import ceil, floor, factorial, isqrt, lcm, log, log1p
from functools import lru_cache
import argparse
import json
import time
import numpy as np
from scipy.linalg import eigh
from scipy.optimize import brentq
from rational_linalg import Mat, diag, zeros, norm2, psd

ROOT = Path(__file__).resolve().parent


def sqrt_upper(x, scale=10**14):
    assert x >= 0
    n = (x.numerator*scale*scale + x.denominator-1)//x.denominator
    y = isqrt(n)
    if y*y < n:
        y += 1
    out = F(y, scale)
    assert out*out >= x
    return out


def inverse(a):
    n = a.rows
    assert a.cols == n
    x = [row[:] + [F(j == k) for k in range(n)]
         for j, row in enumerate(a.a)]
    for j in range(n):
        pivot = next(k for k in range(j, n) if x[k][j])
        x[j], x[pivot] = x[pivot], x[j]
        d = x[j][j]
        x[j] = [v/d for v in x[j]]
        for k in range(n):
            if k != j:
                d = x[k][j]
                x[k] = [u-d*v for u, v in zip(x[k], x[j])]
    ans = Mat([row[n:] for row in x])
    assert a*ans == diag(*([1]*n))
    return ans


def power(a, n):
    assert n >= 0
    out = diag(*([1]*a.rows))
    while n:
        if n & 1:
            out = out*a
        a = a*a
        n //= 2
    return out


def floats(a):
    return np.array([[float(x) for x in row] for row in a.a])


def dominate(q, r):
    """Propose using eigensolver, accept only exact rational PSD inequality."""
    assert psd(r) and r.det() > 0
    top = max(0.0, float(eigh(floats(q), floats(r), eigvals_only=True)[-1]))
    quantum = F(1, 10**10)
    value = F(ceil(top/float(quantum)), 10**10)
    while not psd(value*r-q):
        value += quantum
    return value


@lru_cache(maxsize=None)
def log_bounds(z, terms=24):
    """Rational enclosure using binary scaling and the atanh series."""
    assert z > 0
    shift = 0
    while z < 1:
        z *= 2
        shift -= 1
    while z > 2:
        z /= 2
        shift += 1
    t = (z-1)/(z+1)
    t2 = t*t
    monomial = t
    lower = F(0)
    for k in range(terms):
        lower += 2*monomial/(2*k+1)
        monomial *= t2
    upper = lower + 2*monomial/((2*terms+1)*(1-t2))
    if shift:
        lo2, hi2 = log_bounds(F(2), terms)
        lower += shift*(lo2 if shift >= 0 else hi2)
        upper += shift*(hi2 if shift >= 0 else lo2)
    return lower, upper


def kl_lower(phat, p):
    assert 0 <= phat <= 1 and 0 < p < 1
    result = F(0)
    if phat:
        result += phat*log_bounds(phat/p)[0]
    if phat != 1:
        result += (1-phat)*log_bounds((1-phat)/(1-p))[0]
    return result


def kl_float(phat, p):
    if phat == 0:
        return -log1p(-p)
    if phat == 1:
        return -log(p)
    return phat*log(phat/p)+(1-phat)*(log1p(-phat)-log1p(-p))


def binomial_interval(x, n, exponent=F(12), upper_only=False):
    """Fixed-n KL-Chernoff interval. Each retained tail costs exp(-exponent)."""
    assert isinstance(x, int) and 0 <= x <= n and n > 0
    phat = F(x, n)
    quantum = F(1, 10**12)
    target = float(exponent/n)
    if x == n:
        hi = F(1)
    elif x == 0:
        hi = min(F(1), exponent/n)
    else:
        proposal = brentq(lambda p: kl_float(float(phat), p)-target,
                          float(phat), 1-1e-15, xtol=1e-15)
        hi = F(ceil(proposal/float(quantum)), 10**12)
        while n*kl_lower(phat, hi) < exponent:
            hi += quantum
    if upper_only:
        return F(0), hi
    if x == 0:
        lo = F(0)
    elif x == n:
        lo = max(F(0), 1-exponent/n)
    else:
        proposal = brentq(lambda p: kl_float(float(phat), p)-target,
                          1e-15, float(phat), xtol=1e-15)
        lo = F(floor(proposal/float(quantum)), 10**12)
        while lo > 0 and n*kl_lower(phat, lo) < exponent:
            lo -= quantum
    return lo, hi


def source_fixture():
    l0, l1 = diag(F(1, 10), F(1, 10), F(1, 10)), diag(F(1, 10), F(1, 10), F(1, 10))
    for mode, j, k, weight in [(0, 0, 1, F(9, 10)), (0, 1, 2, F(1, 20)),
                               (1, 1, 2, F(9, 10)), (1, 0, 2, F(1, 20))]:
        edge = Mat([F(q == j)-F(q == k) for q in range(3)])
        if mode == 0:
            l0 = l0 + weight*(edge*edge.T)
        else:
            l1 = l1 + weight*(edge*edge.T)
    boundary = [diag(1, 1, 1)-F(1, 5)*l for l in [l0, l1]]
    matrices = []
    for t in boundary:
        a = [[F(0) for _ in range(6)] for _ in range(6)]
        for j in range(3):
            for k in range(3):
                a[j][k] = t[j, k]
            a[j][j+3] = a[j+3][j] = F(1, 500)
            a[j+3][j+3] = [F(1, 4), F(1, 3), F(2, 5)][j]
        matrices.append(Mat(a))
    assert boundary[0]*boundary[1] != boundary[1]*boundary[0]
    for a in matrices:
        assert a == a.T
        assert all(min(row) >= 0 and sum(row) <= F(99, 100) for row in a.a)
        # Strict diagonal dominance proves positivity exactly; row sums prove cap.
        assert all(a[j, j] > sum(abs(a[j, k]) for k in range(6) if k != j)
                   for j in range(6))
    return matrices


class BoundaryInstrument:
    """Hidden states remain internal; receipts contain boundary IDs or outside."""
    def __init__(self, matrices, boundary_size=3, seed=2026102807):
        self.matrices = matrices
        self.r = boundary_size
        self.rng = np.random.default_rng(seed)

    def acquire(self, mode, start_boundary, n, depth, tail_weight, batch=200000):
        a = self.matrices[mode]
        hidden_count = a.rows
        denominator = lcm(*(x.denominator for row in a.a for x in row))
        cdf = np.array([[int(x*denominator) for x in row] for row in a.a], dtype=np.int64).cumsum(axis=1)
        mix_den = tail_weight.denominator
        mix_total = depth*mix_den+tail_weight.numerator
        first_counts = np.zeros(self.r+1, dtype=np.int64)
        lengths_hist = np.zeros(depth+1, dtype=np.int64)
        outside_hist = np.zeros(depth+1, dtype=np.int64)
        pen_inside_hist = np.zeros(depth+1, dtype=np.int64)
        event_hist = np.zeros(depth+1, dtype=np.int64)
        terminal_counts = np.zeros(self.r+1, dtype=np.int64)
        last_terminal_report = None
        live_random_draws = 0
        for begin in range(0, n, batch):
            size = min(batch, n-begin)
            labels = np.minimum(self.rng.integers(mix_total, size=size)//mix_den, depth)
            lengths = 2*labels+2
            lengths_hist += np.bincount(labels, minlength=depth+1)
            state = np.full(size, start_boundary, dtype=np.int8)
            active = np.ones(size, dtype=bool)
            terminal = np.full(size, -1, dtype=np.int8)
            for step in range(1, 2*depth+3):
                idx = np.flatnonzero(active & (step <= lengths))
                old = state[idx]
                live = old < hidden_count
                live_idx = idx[live]
                draws = self.rng.integers(denominator, size=live_idx.size)
                live_random_draws += int(live_idx.size)
                if live_idx.size:
                    state[live_idx] = np.sum(draws[:, None] >= cdf[old[live]], axis=1)
                # Absorbed trajectories are computationally skipped but charged below.
                if step == 1:
                    reports = np.where(state < self.r, state, self.r)
                    first_counts += np.bincount(reports, minlength=self.r+1)
                    active = state >= self.r
                    terminal[~active] = state[~active]
                    outside_hist += np.bincount(labels[active], minlength=depth+1)
                pen = active & (step == lengths-1)
                failed = pen & (state < self.r)
                pen_inside_hist += np.bincount(labels[failed], minlength=depth+1)
                terminal[failed] = state[failed]
                active[failed] = False
                final = active & (step == lengths)
                success = final & (state == start_boundary)
                event_hist += np.bincount(labels[success], minlength=depth+1)
                terminal[final] = np.where(state[final] < self.r, state[final], self.r)
                active[final] = False
            assert np.all(terminal >= 0)
            terminal_counts += np.bincount(terminal, minlength=self.r+1)
            last_terminal_report = int(terminal[-1])
        # One initial transition, remaining scheduled transitions after outside,
        # minus the final transition when the penultimate boundary report rejects.
        charged_ops = n+sum(int(x)*(2*k+1) for k, x in enumerate(outside_hist))-int(sum(pen_inside_hist))
        charged_reads = n+sum(int(x)*(1 if k == 0 else 2) for k, x in enumerate(outside_hist))-int(sum(pen_inside_hist))
        return {'mode': mode, 'start_boundary': start_boundary, 'trials': n,
                'first_step_boundary_or_outside_counts': first_counts.tolist(),
                'mixture_length_histogram': lengths_hist.tolist(),
                'first_outside_length_histogram': outside_hist.tolist(),
                'penultimate_inside_rejections_by_length': pen_inside_hist.tolist(),
                'positive_events_by_length': event_hist.tolist(),
                'positive_events': int(sum(event_hist)),
                'terminal_boundary_or_outside_counts': terminal_counts.tolist(),
                'known_returns_to_requested_boundary': int(terminal_counts[start_boundary]),
                'primitive_applications': charged_ops,
                'categorical_boundary_observations': charged_reads,
                'logical_trials': n,
                'fresh_reset_execution_upper_bound': n,
                'resets_with_boundary_reuse': n-int(terminal_counts[start_boundary])+int(last_terminal_report == start_boundary),
                'sampling_group_final_reports_equal_requested': int(last_terminal_report == start_boundary),
                'independently_initialized_sampling_groups': 1,
                'simulation_live_transition_rng_draws': live_random_draws}

    def direct_word(self, word, n, start_boundary=0, end_boundary=0, batch=200000):
        """Equally informed direct endpoint route; no hidden-state shortcut."""
        states = self.matrices[0].rows
        denominators = [lcm(*(x.denominator for row in a.a for x in row))
                        for a in self.matrices]
        cdfs = [np.array([[int(x*d) for x in row] for row in a.a], dtype=np.int64).cumsum(axis=1)
                for a, d in zip(self.matrices, denominators)]
        endpoints = np.zeros(self.r+1, dtype=np.int64)
        live_draws = 0
        last_report = None
        for begin in range(0, n, batch):
            size = min(batch, n-begin)
            state = np.full(size, start_boundary, dtype=np.int8)
            for mode in word:
                idx = np.flatnonzero(state < states)
                old = state[idx]
                draw = self.rng.integers(denominators[mode], size=idx.size)
                live_draws += int(idx.size)
                state[idx] = np.sum(draw[:, None] >= cdfs[mode][old], axis=1)
            report = np.where(state < self.r, state, self.r)
            endpoints += np.bincount(report, minlength=self.r+1)
            last_report = int(report[-1])
        return {'word': list(word), 'start_boundary': start_boundary, 'end_boundary': end_boundary,
                'trials': n, 'logical_trials': n,
                'endpoint_boundary_or_outside_counts': endpoints.tolist(),
                'target_returns': int(endpoints[end_boundary]),
                'primitive_applications': n*len(word),
                'categorical_boundary_observations': n,
                'fresh_reset_execution_upper_bound': n,
                'resets_with_boundary_reuse': n-int(endpoints[start_boundary])+int(last_report == start_boundary),
                'simulation_live_transition_rng_draws': live_draws}


def combine_receipts(first, second):
    assert first['mode'] == second['mode'] and first['start_boundary'] == second['start_boundary']
    out = {'mode': first['mode'], 'start_boundary': first['start_boundary']}
    for key in first:
        if key in out:
            continue
        out[key] = ([int(x)+int(y) for x, y in zip(first[key], second[key])]
                    if isinstance(first[key], list) else first[key]+second[key])
    return out


def dumpable(x):
    if isinstance(x, F):
        return {'fraction': str(x), 'diagnostic': float(x)}
    if isinstance(x, Mat):
        return dumpable(x.a)
    if isinstance(x, dict):
        return {k: dumpable(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [dumpable(v) for v in x]
    return x


def infer(receipts, depth, source_cap, exponent=F(12)):
    """Receipts and the stated access contract are the only learner inputs."""
    r = 3
    identity = diag(1, 1, 1)
    tail = 1/(1-source_cap*source_cap)
    normalizer = depth+tail
    modes = []
    for mode in range(2):
        group = [next(x for x in receipts if x['mode'] == mode and x['start_boundary'] == j)
                 for j in range(r)]
        n = group[0]['trials']
        assert all(x['trials'] == n for x in group)
        observed = [x['first_step_boundary_or_outside_counts'] for x in group]
        t = [[F(0) for _ in range(r)] for _ in range(r)]
        lower = [[F(0) for _ in range(r)] for _ in range(r)]
        upper = [[F(0) for _ in range(r)] for _ in range(r)]
        radius = [[F(0) for _ in range(r)] for _ in range(r)]
        for j in range(r):
            for k in range(j, r):
                count = observed[j][j] if j == k else observed[j][k]+observed[k][j]
                total = n if j == k else 2*n
                lo, hi = binomial_interval(count, total, exponent)
                center = F(count, total)
                rad = max(center-lo, hi-center)
                for q, s in [(j, k), (k, j)]:
                    t[q][s], lower[q][s], upper[q][s], radius[q][s] = center, lo, hi, rad
        t, lower, upper, radius = Mat(t), Mat(lower), Mat(upper), Mat(radius)
        budget = identity-t.T*t
        assert psd(budget) and budget.det() > 0
        delta_op = max(sum(row) for row in radius.a)
        q_diagonal_upper = []
        for x in group:
            _, hi = binomial_interval(x['positive_events'], n, exponent, upper_only=True)
            q_diagonal_upper.append(normalizer*hi)
        q_trace = sum(q_diagonal_upper, F(0))
        q_proposal = (sqrt_upper(q_trace)+delta_op*sqrt_upper(tail))**2
        theta_squared = dominate(q_proposal*identity, budget)
        zeta = dominate(delta_op*identity, budget)

        # Stronger, still same-data correction uncertainty: preserve correlation
        # between diagonal and off-diagonal errors through observed row masses.
        row_intervals, row_radii = [], []
        for j in range(r):
            lo, hi = binomial_interval(sum(observed[j][:r]), n, exponent)
            row_intervals.append((lo, hi))
            proposed_row = sum(t.a[j])
            row_radii.append(max(abs(lo-proposed_row), abs(hi-proposed_row)))
        uncertainty_form = diag(*row_radii)
        for j in range(r):
            for k in range(j+1, r):
                edge = Mat([F(q == j)-F(q == k) for q in range(r)])
                uncertainty_form = uncertainty_form+radius[j, k]*(edge*edge.T)
        structured_zeta = dominate(uncertainty_form, budget)

        # Equally informed robust Galerkin comparator. The true T has nonnegative
        # entries and row masses bounded by these observed confidence intervals.
        true_kernel_cap = max(hi for _, hi in row_intervals)
        assert true_kernel_cap < 1
        galerkin_theta_squared = q_trace/(1-true_kernel_cap*true_kernel_cap)
        modes.append({'mode': mode, 'model': t, 'kernel_lower': lower,
                      'kernel_upper': upper, 'entry_radius': radius,
                      'row_mass_intervals': row_intervals,
                      'operator_error_upper': delta_op,
                      'galerkin_form_diagonal_uppers': q_diagonal_upper,
                      'galerkin_form_trace_upper': q_trace,
                      'proposed_form_operator_upper': q_proposal,
                      'budget': budget, 'theta_squared': theta_squared,
                      'correction_noise_zeta': zeta,
                      'structured_uncertainty_form': uncertainty_form,
                      'structured_correction_noise_zeta': structured_zeta,
                      'true_kernel_norm_upper': true_kernel_cap,
                      'robust_galerkin_theta_squared': galerkin_theta_squared})
    remainder = 2*max(m['theta_squared'] for m in modes)
    noise = max(m['correction_noise_zeta'] for m in modes)
    structured_noise = max(m['structured_correction_noise_zeta'] for m in modes)
    return {'modes': modes, 'mixture_tail_weight': tail,
            'mixture_normalizer': normalizer,
            'uniform_signed_remainder_bound': remainder,
            'uniform_correction_noise_bound': noise,
            'uniform_all_word_bound': remainder+noise,
            'uniform_structured_correction_noise_bound': structured_noise,
            'uniform_structured_all_word_bound': remainder+structured_noise,
            'robust_galerkin_uniform_dynamical_bound': 2*max(m['robust_galerkin_theta_squared'] for m in modes)}


def trajectories(modes, word, start_boundary=0, end_boundary=0):
    cin = Mat([F(j == start_boundary) for j in range(3)])
    cout = Mat([F(j == end_boundary) for j in range(3)])
    alpha = [cin]
    for i in word:
        alpha.append(modes[i]['model']*alpha[-1])
    beta = [None]*(len(word)+1)
    beta[-1] = cout
    for t in range(len(word)-1, -1, -1):
        beta[t] = modes[word[t]]['model']*beta[t+1]
    return cin, cout, alpha, beta


def correction_radius(coefficients, modes):
    radius = F(0)
    for c, mode in zip(coefficients, modes):
        r = mode['entry_radius']
        for j in range(3):
            radius += abs(c[j, j])*r[j, j]
            for k in range(j+1, 3):
                radius += abs(c[j, k]+c[k, j])*r[j, k]
    return radius


def word_prediction(certificate, word, start_boundary=0, end_boundary=0):
    modes = certificate['modes']
    cin, cout, alpha, beta = trajectories(modes, word, start_boundary, end_boundary)
    coeff = [zeros(3, 3), zeros(3, 3)]
    forward_budget = backward_budget = F(0)
    for t, i in enumerate(word):
        coeff[i] = coeff[i]+beta[t+1]*alpha[t].T
        r = modes[i]['budget']
        forward_budget += modes[i]['theta_squared']*(alpha[t].T*r*alpha[t])[0]
        backward_budget += modes[i]['theta_squared']*(beta[t+1].T*r*beta[t+1])[0]
    remainder = 2*sqrt_upper(forward_budget*backward_budget)
    radius = correction_radius(coeff, modes)
    point = (cout.T*alpha[-1])[0]
    lo_state, hi_state = cin, cin
    for i in word:
        lo_state = modes[i]['kernel_lower']*lo_state
        hi_state = modes[i]['kernel_upper']*hi_state
    # With positive source matrices, hidden excursions only add positive paths;
    # the true Galerkin prediction is a lower bound on the source response.
    gal_lo = (cout.T*lo_state)[0]
    gal_hi = (cout.T*hi_state)[0]+certificate['robust_galerkin_uniform_dynamical_bound']
    return {'word': list(word), 'start_boundary': start_boundary, 'end_boundary': end_boundary,
            'model_prediction': point,
            'finite_word_remainder_bound': remainder,
            'aggregated_correction_interval_radius': radius,
            'source_interval': (max(F(0), point-remainder-radius),
                                min(F(1), point+remainder+radius)),
            'correction_coefficients': coeff,
            'robust_galerkin_source_interval': (max(F(0), gal_lo), min(F(1), gal_hi))}


def truth(a, word, start_boundary=0, end_boundary=0):
    cin = Mat([F(j == start_boundary) for j in range(a[0].rows)])
    cout = Mat([F(j == end_boundary) for j in range(a[0].rows)])
    x = cin
    for i in word:
        x = a[i]*x
    return (cout.T*x)[0]


def exact_source_check(a, certificate, receipts, depth):
    """Uses hidden matrices only after inference, to check the synthetic receipt."""
    v = Mat([[F(j == k) for k in range(3)] for j in range(6)])
    p = v*v.T
    outside = diag(*([1]*6))-p
    tail = certificate['mixture_tail_weight']
    normalizer = certificate['mixture_normalizer']
    checked = []
    for i, mode in enumerate(certificate['modes']):
        source = a[i]
        true_t = v.T*source*v
        delta = true_t-mode['model']
        d_gal = outside*source*v
        d_prop = source*v-v*mode['model']
        resolvent = inverse(diag(*([1]*6))-source*source)
        q_gal = d_gal.T*resolvent*d_gal
        q_prop = d_prop.T*resolvent*d_prop
        mixture = zeros(3, 3)
        for k in range(depth+1):
            term = d_gal.T*power(source, 2*k)*d_gal
            path = v.T*source*outside*power(source, 2*k)*outside*source*v
            assert path == term
            mixture = mixture+(tail if k == depth else 1)*term
        assert psd(mixture-q_gal)
        for j in range(3):
            assert mixture[j, j] <= mode['galerkin_form_diagonal_uppers'][j]
            for k in range(3):
                assert mode['kernel_lower'][j, k] <= true_t[j, k] <= mode['kernel_upper'][j, k]
            lo, hi = mode['row_mass_intervals'][j]
            assert lo <= sum(true_t.a[j]) <= hi
        ident = diag(1, 1, 1)
        assert psd(mode['galerkin_form_trace_upper']*ident-q_gal)
        assert psd(mode['proposed_form_operator_upper']*ident-q_prop)
        assert psd(mode['theta_squared']*mode['budget']-q_prop)
        pi = mode['structured_uncertainty_form']
        assert psd(pi-delta) and psd(pi+delta)
        true_r = ident-true_t*true_t
        assert psd(mode['robust_galerkin_theta_squared']*true_r-q_gal)
        checked.append({'mode': i, 'true_boundary_matrix': true_t,
                        'true_galerkin_source_form': q_gal,
                        'true_proposed_source_form': q_prop,
                        'true_mixed_event_probabilities': [mixture[j, j]/normalizer for j in range(3)],
                        'all_inequalities_exact': True})
    return checked


def compare_words(certificate, word_a, word_b, start_boundary=0, end_boundary=0):
    a = word_prediction(certificate, word_a, start_boundary, end_boundary)
    b = word_prediction(certificate, word_b, start_boundary, end_boundary)
    difference = a['model_prediction']-b['model_prediction']
    coeff_difference = [x-y for x, y in zip(a['correction_coefficients'], b['correction_coefficients'])]
    radius = (a['finite_word_remainder_bound']+b['finite_word_remainder_bound']
              +correction_radius(coeff_difference, certificate['modes']))
    interval = (difference-radius, difference+radius)
    alo, ahi = a['robust_galerkin_source_interval']
    blo, bhi = b['robust_galerkin_source_interval']
    return {'program_a': a, 'program_b': b, 'model_difference': difference,
            'shared_data_difference_interval': interval,
            'shared_data_order_resolved': interval[0] > 0 or interval[1] < 0,
            'two_uniform_bound_order_resolved': abs(difference) > 2*certificate['uniform_all_word_bound'],
            'two_structured_uniform_bound_order_resolved': abs(difference) > 2*certificate['uniform_structured_all_word_bound'],
            'robust_galerkin_difference_interval': (alo-bhi, ahi-blo),
            'robust_galerkin_order_resolved': alo > bhi or blo > ahi}


def run(initial_trials=10_000_000, maximum_trials=20_000_000):
    if initial_trials <= 0 or maximum_trials < initial_trials:
        raise ValueError('Require 0 < initial_trials <= maximum_trials')
    started = time.monotonic()
    sources = source_fixture()
    source_cap, depth, exponent = F(99, 100), 4, F(12)
    tail = 1/(1-source_cap*source_cap)
    instrument = BoundaryInstrument(sources)
    # Two fixed inference checkpoints, 12 distinct kernel entries with two
    # tails, six row masses with two tails, six one-sided event probabilities.
    confidence_tail_count = 2*(12*2+6*2+6)
    assert sum((F(12**k, factorial(k)) for k in range(70)), F(0)) > 1000*confidence_tail_count
    receipts = []
    stages = []
    primary_words = ((0,)*10+(1,)*10, (1,)*10+(0,)*10)
    previous_n = 0
    for target_n in dict.fromkeys([initial_trials, maximum_trials]):
        added = target_n-previous_n
        for mode in range(2):
            for boundary in range(3):
                fresh = instrument.acquire(mode, boundary, added, depth, tail)
                if previous_n:
                    index = mode*3+boundary
                    receipts[index] = combine_receipts(receipts[index], fresh)
                else:
                    receipts.append(fresh)
                (ROOT/'MULTIBOUNDARY_RAW_RECEIPTS.json').write_text(json.dumps(
                    {'seed': 2026102807, 'depth': depth, 'source_cap': str(source_cap),
                     'target_trials_at_current_checkpoint': target_n,
                     'receipts': receipts}, indent=2)+'\n')
                print('acquired', target_n, mode, boundary,
                      'events', receipts[mode*3+boundary]['positive_events'], flush=True)
        certificate = infer(receipts, depth, source_cap, exponent)
        check = exact_source_check(sources, certificate, receipts, depth)
        comparisons = []
        for count in [10, 15, 20, 25, 30]:
            comparison = compare_words(certificate, (0,)*count+(1,)*count, (1,)*count+(0,)*count,
                                       start_boundary=0, end_boundary=2)
            for key in ['program_a', 'program_b']:
                item = comparison[key]
                exact = truth(sources, item['word'], item['start_boundary'], item['end_boundary'])
                item['checker_exact_source_response'] = exact
                lo, hi = item['source_interval']
                glo, ghi = item['robust_galerkin_source_interval']
                assert lo <= exact <= hi and glo <= exact <= ghi
                actual_correction = F(0)
                for i, coeff in enumerate(item['correction_coefficients']):
                    true_t = check[i]['true_boundary_matrix']
                    delta = true_t-certificate['modes'][i]['model']
                    actual_correction += sum((coeff[j, k]*delta[j, k]
                                              for j in range(3) for k in range(3)), F(0))
                assert abs(exact-item['model_prediction']-actual_correction) <= item['finite_word_remainder_bound']
                assert abs(exact-item['model_prediction']) <= certificate['uniform_all_word_bound']
                item['checker_exact_signed_correction'] = actual_correction
            exact_difference = (comparison['program_a']['checker_exact_source_response']
                                -comparison['program_b']['checker_exact_source_response'])
            comparison['checker_exact_source_difference'] = exact_difference
            lo, hi = comparison['shared_data_difference_interval']
            glo, ghi = comparison['robust_galerkin_difference_interval']
            assert lo <= exact_difference <= hi and glo <= exact_difference <= ghi
            comparisons.append(comparison)
        self_return = compare_words(certificate, (0,)*10+(1,)*10, (0, 1)*10)
        self_return['checker_exact_source_difference'] = truth(sources, (0,)*10+(1,)*10)-truth(sources, (0, 1)*10)
        stage = {'trials_per_action_and_boundary': target_n,
                 'receipts': [dict(x) for x in receipts], 'certificate': certificate,
                 'independent_hidden_source_checks': check,
                 'same_count_program_comparisons': comparisons,
                 'self_return_diagnostic': self_return,
                 'costs': {key: sum(x[key] for x in receipts) for key in
                           ['logical_trials', 'primitive_applications', 'categorical_boundary_observations',
                            'fresh_reset_execution_upper_bound', 'resets_with_boundary_reuse',
                            'simulation_live_transition_rng_draws']}}
        stages.append(stage)
        print('stage', target_n, 'global', float(certificate['uniform_all_word_bound']),
              'structured', float(certificate['uniform_structured_all_word_bound']),
              'pair', [float(x) for x in comparisons[0]['shared_data_difference_interval']],
              'galerkin_pair', [float(x) for x in comparisons[0]['robust_galerkin_difference_interval']], flush=True)
        previous_n = target_n
        if comparisons[0]['shared_data_order_resolved']:
            break

    # Fresh direct endpoint data for the primary pair, at a fixed 10k each.
    direct = [instrument.direct_word(w, 10_000, start_boundary=0, end_boundary=2) for w in primary_words]
    direct_intervals = [binomial_interval(x['target_returns'], x['trials'], exponent) for x in direct]
    for record, interval in zip(direct, direct_intervals):
        record['confidence_interval'] = interval
        assert interval[0] <= truth(sources, record['word'], record['start_boundary'], record['end_boundary']) <= interval[1]
    direct_gap = (direct_intervals[0][0]-direct_intervals[1][1],
                  direct_intervals[0][1]-direct_intervals[1][0])
    final_costs = stages[-1]['costs']
    direct_costs = {key: sum(x[key] for x in direct) for key in
                    ['logical_trials', 'primitive_applications', 'categorical_boundary_observations',
                     'fresh_reset_execution_upper_bound', 'resets_with_boundary_reuse']}
    result = {'date': '2026-10-28', 'source_matrices_checker_only': sources,
              'physical_state_count_not_given_to_learner': True,
              'boundary_dimension': 3, 'future_action_count': 2,
              'explicit_access_contract': 'Reset at each of three boundary states; exact nonintrusive categorical report of boundary ID or outside; iid Markov evolution; symmetric nonnegative substochastic primitives; warranted norm cap.',
              'source_norm_warranty': source_cap, 'depth': depth,
              'chernoff_exponent': exponent,
              'joint_inference_failure_probability_upper': F(1, 1000),
              'confidence_tail_count_including_both_fixed_checkpoints': confidence_tail_count,
              'confidence_arithmetic': 'Every nontrivial KL endpoint accepted using exact rational lower bounds for logarithms; no floating-point confidence acceptance.',
              'reset_policy': 'One initial reset per action/boundary sampling group; reuse state after every terminal report equal to that requested boundary; otherwise reset before next trial.',
              'absorbed_path_cost_policy': 'Backend may skip deterministic cemetery updates; all scheduled operations and reads remain charged unless an observed boundary predicate rejects.',
              'stages': stages,
              'direct_endpoint_comparator': {'receipts': direct, 'difference_interval': direct_gap,
                     'order_resolved': direct_gap[0] > 0 or direct_gap[1] < 0,
                     'joint_failure_probability_upper': F(1, 1000), 'costs': direct_costs,
                     'compiler_to_direct_operation_ratio': F(final_costs['primitive_applications'], direct_costs['primitive_applications']),
                     'scope': 'Fresh endpoint trials using the same boundary access and source; solves this one pair, does not acquire an all-word reusable certificate.'},
              'all_exact_witness_checks_passed': True,
              'simulation_seconds_diagnostic': time.monotonic()-started,
              'simulation_scope': 'Software-generated integer-RNG trajectories. No physical apparatus or source warranty was acquired. Extra boundary preparation/readout access is a premise.'}
    out = ROOT/'MULTIBOUNDARY_POSITIVE_EVENTS_RESULTS.json'
    out.write_text(json.dumps(dumpable(result), indent=2)+'\n')
    print('saved', out, 'elapsed', result['simulation_seconds_diagnostic'],
          'direct_gap', [float(x) for x in direct_gap], flush=True)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--initial-trials', type=int, default=10_000_000)
    parser.add_argument('--maximum-trials', type=int, default=20_000_000)
    args = parser.parse_args()
    run(args.initial_trials, args.maximum_trials)
