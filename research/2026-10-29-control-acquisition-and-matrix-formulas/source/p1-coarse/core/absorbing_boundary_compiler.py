"""Observed absorption closes a boundary certificate without a source norm gap.

Exact integer-RNG trajectories, rational confidence/certificate acceptance.
Private source: countably infinitely many reachable slow states, norm exactly 1.
Learner inputs: categorical counts, common symmetric Markov source class,
exact boundary preparation and nonintrusive boundary/alive/absorbed reports.
"""
from pathlib import Path
from fractions import Fraction as F
from math import lcm, factorial
import argparse
import json
import random
import sys
import time
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'branches' / 'physical'))
from rational_linalg import Mat, diag, psd
from multiboundary_positive_events import (
    source_fixture, binomial_interval, sqrt_upper, dominate, dumpable,
    word_prediction, compare_words,
)


class InfiniteAbsorbingInstrument:
    """No hidden IDs leave this backend.

    Boundary j couples to a fast state by epsilon=1/500 and to every slow
    state (j,n), n>=0, by w_n=2^(-21-n). Slow state n stays with probability
    1-eta_n, eta_n=2^(-10-n), returns with probability w_n, and dies otherwise.
    """
    def __init__(self, seed=2026102831):
        self.boundary = [a.extract(range(3), range(3)) for a in source_fixture()]
        self.fast_stay = [F(1, 4), F(1, 3), F(2, 5)]
        self.epsilon, self.slow_mass = F(1, 500), F(1, 2**20)
        self.rng = np.random.default_rng(seed)
        self.bits = random.Random(seed + 100)

    def slow_excursion(self, boundary, horizon):
        level = 0
        while self.bits.getrandbits(1) == 0:
            level += 1
        for step in range(2, horizon + 1):
            if self.bits.getrandbits(10 + level) == 0:
                return (boundary if self.bits.getrandbits(11) == 0 else -1), step
        return -2, horizon

    def acquire(self, mode, start, trials, horizon=32, batch=200000):
        assert trials > 0 and horizon >= 2
        probabilities = self.boundary[mode].a[start] + [self.epsilon, self.slow_mass]
        den = lcm(*(x.denominator for x in probabilities))
        cdf = np.cumsum(np.array([int(p*den) for p in probabilities], dtype=np.int64))
        first, final = np.zeros(3, dtype=np.int64), np.zeros(3, dtype=np.int64)
        parity = np.zeros((2, 3), dtype=np.int64)
        durations = np.zeros(horizon + 1, dtype=np.int64)
        first_alive = first_dead = dead = pending = steps = 0
        fast_den = lcm(self.epsilon.denominator, self.fast_stay[start].denominator)
        fast_return = int(self.epsilon*fast_den)
        fast_live = int((self.epsilon+self.fast_stay[start])*fast_den)
        last_terminal = None
        for begin in range(0, trials, batch):
            size = min(batch, trials-begin)
            category = np.searchsorted(cdf, self.rng.integers(0, den, size=size), side='right')
            # Boundary 0..2, fast 3, slow 4, absorbed 5.
            terminal = np.where(category < 3, category, -1).astype(np.int64)
            duration = np.ones(size, dtype=np.int64)
            for k in range(3):
                first[k] += int(np.count_nonzero(category == k))
            first_alive += int(np.count_nonzero((category == 3) | (category == 4)))
            first_dead += int(np.count_nonzero(category == 5))
            active = np.flatnonzero(category == 3)
            for step in range(2, horizon+1):
                if not len(active):
                    break
                out = self.rng.integers(0, fast_den, size=len(active))
                returned = out < fast_return
                alive = (out >= fast_return) & (out < fast_live)
                duration[active] = step
                terminal[active[returned]] = start
                parity[step % 2, start] += int(np.count_nonzero(returned))
                active = active[alive]
            terminal[active] = -2
            for index in np.flatnonzero(category == 4):
                state, stop = self.slow_excursion(start, horizon)
                terminal[index], duration[index] = state, stop
                if state >= 0:
                    parity[stop % 2, state] += 1
            for k in range(3):
                final[k] += int(np.count_nonzero(terminal == k))
            dead += int(np.count_nonzero(terminal == -1))
            pending += int(np.count_nonzero(terminal == -2))
            durations += np.bincount(duration, minlength=horizon+1)
            steps += int(duration.sum())
            last_terminal = int(terminal[-1])
        returned, even = int(parity.sum()), int(parity[0].sum())
        assert int(first.sum()) + first_alive + first_dead == trials
        assert int(final.sum()) + dead + pending == trials
        assert int(final.sum()) == int(first.sum()) + returned
        assert steps == sum(k*int(x) for k, x in enumerate(durations))
        return dict(mode=mode, start_boundary=start, trials=trials, horizon=horizon,
            first_step_boundary_counts=first.tolist(), first_step_alive_outside=first_alive,
            first_step_absorbed=first_dead, excursion_return_counts_even_odd=parity.tolist(),
            returned_or_pending=returned+pending, even_returned_or_pending=even+pending,
            absorbed_before_boundary_return=dead, pending_alive_at_censor=pending,
            terminal_boundary_counts=final.tolist(), duration_histogram=durations.tolist(),
            last_terminal_boundary_or_absorbed_or_pending=last_terminal,
            logical_trials=trials, primitive_applications=steps, categorical_observations=steps,
            fresh_reset_execution_upper_bound=trials,
            preparations_with_known_boundary_reuse=trials-int(final[start])+int(last_terminal == start))

    def direct_program(self, word, start, end, trials=10000):
        """Endpoint-only comparator: hidden updates may stop, all steps charged."""
        first_tables = {}
        for mode in range(2):
            for j in range(3):
                probabilities = self.boundary[mode].a[j]+[self.epsilon, self.slow_mass]
                den = lcm(*(p.denominator for p in probabilities))
                cumulative, total = [], 0
                for p in probabilities:
                    total += int(p*den)
                    cumulative.append(total)
                first_tables[mode, j] = (den, cumulative)
        counts = [0]*4
        last_boundary = None
        for _ in range(trials):
            state = ('boundary', start, 0)
            for mode in word:
                kind, j, level = state
                if kind == 'absorbed':
                    continue
                if kind == 'boundary':
                    den, cdf = first_tables[mode, j]
                    u = self.bits.randrange(den)
                    outcome = next((k for k, threshold in enumerate(cdf) if u < threshold), 5)
                    if outcome < 3:
                        state = ('boundary', outcome, 0)
                    elif outcome == 3:
                        state = ('fast', j, 0)
                    elif outcome == 4:
                        level = 0
                        while self.bits.getrandbits(1) == 0:
                            level += 1
                        state = ('slow', j, level)
                    else:
                        state = ('absorbed', j, 0)
                elif kind == 'fast':
                    den = lcm(self.epsilon.denominator, self.fast_stay[j].denominator)
                    u = self.bits.randrange(den)
                    if u < int(self.epsilon*den):
                        state = ('boundary', j, 0)
                    elif u >= int((self.epsilon+self.fast_stay[j])*den):
                        state = ('absorbed', j, 0)
                elif self.bits.getrandbits(10+level) == 0:
                    state = ('boundary', j, 0) if self.bits.getrandbits(11) == 0 else ('absorbed', j, 0)
            last_boundary = state[1] if state[0] == 'boundary' else 3
            counts[last_boundary] += 1
        interval = binomial_interval(counts[end], trials)
        return dict(word=list(word), start_boundary=start, end_boundary=end, trials=trials,
                    endpoint_boundary_or_outside_counts=counts, confidence_interval=interval,
                    primitive_applications=trials*len(word), categorical_observations=trials,
                    preparations_with_known_boundary_reuse=trials-counts[start]+int(last_boundary == start))


def infer(receipts, exponent=F(12)):
    """No hidden matrix, dimension, tail model, spectral gap or norm cap input."""
    identity, modes = diag(1, 1, 1), []
    for mode in range(2):
        group = [next(x for x in receipts if x['mode'] == mode and x['start_boundary'] == j)
                 for j in range(3)]
        n = group[0]['trials']
        assert all(x['trials'] == n for x in group)
        observed = [x['first_step_boundary_counts'] for x in group]
        arrays = [[[F(0)]*3 for _ in range(3)] for _ in range(4)]
        for j in range(3):
            for k in range(j, 3):
                count = observed[j][j] if j == k else observed[j][k]+observed[k][j]
                total = n if j == k else 2*n
                lo, hi = binomial_interval(count, total, exponent)
                center = F(count, total)
                for u, v in [(j, k), (k, j)]:
                    for array, value in zip(arrays, (center, lo, hi, max(center-lo, hi-center))):
                        array[u][v] = value
        t, lower, upper, radius = map(Mat, arrays)
        row_intervals, row_error, r_up, even_up, absorption_lo = [], [], [], [], []
        for j, record in enumerate(group):
            lo, hi = binomial_interval(sum(observed[j]), n, exponent)
            row_intervals.append((lo, hi))
            row_error.append(max(abs(lo-sum(t.a[j])), abs(hi-sum(t.a[j]))))
            r_up.append(binomial_interval(record['returned_or_pending'], n, exponent, upper_only=True)[1])
            even_up.append(binomial_interval(record['even_returned_or_pending'], n, exponent, upper_only=True)[1])
            absorption_lo.append(binomial_interval(record['absorbed_before_boundary_return'], n, exponent)[0])
        kp = max(min(absorption_lo), min(1-row_intervals[j][1]-r_up[j] for j in range(3)))
        km = min(2*lower[j, j]+absorption_lo[j] for j in range(3))
        assert kp > 0 and km > 0
        local_inverse = (1/kp+1/km)/2
        q_true = max(even_up) + max(r_up)**2*local_inverse
        error_op = max(sum(row) for row in radius.a)
        q_estimated = (sqrt_upper(q_true)+error_op*sqrt_upper(local_inverse))**2
        budget = identity-t.T*t
        assert psd(budget) and budget.det() > 0
        theta = dominate(q_estimated*identity, budget)
        uncertainty = diag(*row_error)
        for j in range(3):
            for k in range(j+1, 3):
                edge = Mat([F(l == j)-F(l == k) for l in range(3)])
                uncertainty = uncertainty+radius[j, k]*(edge*edge.T)
        zeta = dominate(uncertainty, budget)
        unstructured_zeta = dominate(error_op*identity, budget)
        cap_t = max(hi for _, hi in row_intervals)
        assert cap_t < 1
        modes.append(dict(mode=mode, model=t, kernel_lower=lower, kernel_upper=upper,
            entry_radius=radius, row_mass_intervals=row_intervals,
            excursion_return_row_upper=r_up, even_excursion_return_row_upper=even_up,
            observed_absorption_row_lower=absorption_lo,
            boundary_schur_plus_lower=kp, boundary_schur_minus_lower=km,
            local_boundary_inverse_dissipation_upper=local_inverse,
            true_galerkin_form_operator_upper=q_true, operator_error_upper=error_op,
            proposed_form_operator_upper=q_estimated, budget=budget, theta_squared=theta,
            structured_uncertainty_form=uncertainty, structured_correction_noise_zeta=zeta,
            correction_noise_zeta=unstructured_zeta,
            true_kernel_norm_upper=cap_t, robust_galerkin_theta_squared=q_true/(1-cap_t**2)))
    remainder = 2*max(m['theta_squared'] for m in modes)
    noise = max(m['structured_correction_noise_zeta'] for m in modes)
    unstructured_noise = max(m['correction_noise_zeta'] for m in modes)
    return dict(modes=modes, global_source_norm_cap_input=None,
        uniform_signed_remainder_bound=remainder,
        uniform_correction_noise_bound=unstructured_noise,
        uniform_all_word_bound=remainder+unstructured_noise,
        uniform_structured_correction_noise_bound=noise,
        uniform_structured_all_word_bound=remainder+noise,
        robust_galerkin_uniform_dynamical_bound=2*max(m['robust_galerkin_theta_squared'] for m in modes))


def fixture_event_probabilities(source, mode, start, horizon, levels=16):
    """Exact truth enclosures, for checker only; not used by learner."""
    terms = [(source.epsilon, source.fast_stay[start])]
    terms += [(source.slow_mass/2**(n+1), 1-F(1, 2**(10+n))) for n in range(levels)]
    returned = even = pending = F(0)
    for coupling, stay in terms:
        pending += coupling*stay**(horizon-1)
        for length in range(2, horizon+1):
            prob = coupling**2*stay**(length-2)
            returned += prob
            if length % 2 == 0:
                even += prob
    tail = source.slow_mass/2**levels
    boundary_mass = sum(source.boundary[mode].a[start])
    absorbed_hi = 1-boundary_mass-returned-pending
    return {'returned_or_pending': (returned+pending, returned+pending+tail),
            'even_returned_or_pending': (even+pending, even+pending+tail),
            'absorbed': (absorbed_hi-tail, absorbed_hi), 'pending': (pending, pending+tail)}


def source_program_enclosure(source, word, start, end, levels=12):
    """Omitted branch entries are killed; union bound encloses their influence."""
    boundary, fast = [F(j == start) for j in range(3)], [F(0)]*3
    slow = [[F(0)]*levels for _ in range(3)]
    for mode in word:
        next_b = [sum(source.boundary[mode][j, k]*boundary[k] for k in range(3))
                  +source.epsilon*fast[j]
                  +sum(source.slow_mass/2**(n+1)*slow[j][n] for n in range(levels)) for j in range(3)]
        next_f = [source.epsilon*boundary[j]+source.fast_stay[j]*fast[j] for j in range(3)]
        next_s = [[source.slow_mass/2**(n+1)*boundary[j]+(1-F(1, 2**(10+n)))*slow[j][n]
                   for n in range(levels)] for j in range(3)]
        boundary, fast, slow = next_b, next_f, next_s
    return boundary[end], min(F(1), boundary[end]+len(word)*source.slow_mass/2**levels)


def source_checks(source, receipts, certificate):
    checks = []
    for m in certificate['modes']:
        mode = m['mode']
        assert all(m['kernel_lower'][j, k] <= source.boundary[mode][j, k] <= m['kernel_upper'][j, k]
                   for j in range(3) for k in range(3))
        assert psd(m['structured_correction_noise_zeta']*m['budget']-m['structured_uncertainty_form'])
        assert psd(m['theta_squared']*m['budget']-m['proposed_form_operator_upper']*diag(1, 1, 1))
        for j in range(3):
            record = next(r for r in receipts if r['mode'] == mode and r['start_boundary'] == j)
            events = fixture_event_probabilities(source, mode, j, record['horizon'])
            flags = [events['returned_or_pending'][1] <= m['excursion_return_row_upper'][j],
                     events['even_returned_or_pending'][1] <= m['even_excursion_return_row_upper'][j],
                     m['observed_absorption_row_lower'][j] <= events['absorbed'][0]]
            assert all(flags)
            checks.append(dict(mode=mode, boundary=j, event_probability_enclosures=events, checks=flags))
    return checks


def run(trials=2_000_000, horizon=32, replay=False):
    started, source = time.perf_counter(), InfiniteAbsorbingInstrument()
    raw_path = ROOT/'results'/'ABSORBING_BOUNDARY_RAW_RECEIPTS.json'
    if replay:
        raw = json.loads(raw_path.read_text())
        assert raw['trials_per_action_boundary'] == trials and raw['censor_horizon'] == horizon
        receipts = raw['receipts']
    else:
        receipts = []
        for mode in range(2):
            for j in range(3):
                receipt = source.acquire(mode, j, trials, horizon)
                receipts.append(receipt)
                print(json.dumps({'mode': mode, 'boundary': j, 'steps': receipt['primitive_applications'],
                                  'returned_or_pending': receipt['returned_or_pending']}), flush=True)
        raw_path.write_text(json.dumps(dict(trials_per_action_boundary=trials, censor_horizon=horizon,
                                           receipts=receipts), indent=2)+'\n')
    certificate = infer(receipts)
    checks = source_checks(source, receipts, certificate)
    wa, wb = (0,)*10+(1,)*10, (1,)*10+(0,)*10
    comparison = compare_words(certificate, wa, wb, 0, 2)
    direct_path = ROOT/'results'/'ABSORBING_BOUNDARY_DIRECT_RECEIPTS.json'
    if direct_path.exists():
        direct_raw = json.loads(direct_path.read_text())
        direct = direct_raw['receipts']
        for receipt in direct:
            receipt['confidence_interval'] = tuple(F(x) for x in receipt['confidence_interval'])
    else:
        direct_source = InfiniteAbsorbingInstrument(seed=2026102837)
        direct = [direct_source.direct_program(word, 0, 2) for word in [wa, wb]]
        raw_direct = [dict(x, confidence_interval=[str(y) for y in x['confidence_interval']]) for x in direct]
        direct_path.write_text(json.dumps({'receipts': raw_direct}, indent=2)+'\n')
    direct_interval = (direct[0]['confidence_interval'][0]-direct[1]['confidence_interval'][1],
                       direct[0]['confidence_interval'][1]-direct[1]['confidence_interval'][0])
    direct_costs = {key: sum(r[key] for r in direct) for key in ['primitive_applications',
                    'categorical_observations', 'preparations_with_known_boundary_reuse']}
    programs = []
    for word, start, end in [((), 0, 0), ((0,), 0, 1), ((1,), 1, 2), (wa, 0, 2), (wb, 0, 2),
                             ((0, 1)*10, 0, 2), ((1, 0)*10, 0, 2), ((0,)*100, 0, 0), ((1,)*100, 2, 2)]:
        prediction = word_prediction(certificate, word, start, end)
        truth = source_program_enclosure(source, word, start, end)
        assert all(prediction[key][0] <= truth[0] <= truth[1] <= prediction[key][1]
                   for key in ['source_interval', 'robust_galerkin_source_interval'])
        programs.append(dict(word=list(word), start=start, end=end, source_truth_enclosure=truth,
                             prediction=prediction, check_passed=True))
    # Each action: 12 entry tails, 6 row-mass tails, 9 event tails. An unused
    # absorption upper endpoint does not consume a tail in the good event.
    tail_count = 58  # 54 acquisition tails plus four fresh direct-comparator tails
    assert tail_count/sum((F(12**k, factorial(k)) for k in range(60)), F(0)) < F(1, 1000)
    costs = {name: sum(r[name] for r in receipts) for name in ['logical_trials', 'primitive_applications',
        'categorical_observations', 'fresh_reset_execution_upper_bound', 'preparations_with_known_boundary_reuse']}
    output = dict(date='2026-10-28',
        source_contract='Common symmetric substochastic Markov operators on a finite or countable state space; exact boundary preparations; nonintrusive boundary/alive/irreversibly-absorbed reports.',
        fixture_norm='Exactly one, infinitely many reachable slow states, no eigenvector of eigenvalue one; no global source norm cap enters inference.',
        fixture_hidden_definition_checker_only=dict(boundary_matrices=source.boundary, fast_diagonal=source.fast_stay,
            fast_coupling=source.epsilon, slow_total_coupling_per_boundary=source.slow_mass,
            slow_coupling='w_n=2^(-21-n)', slow_exit='eta_n=2^(-10-n)', n_range='all integers n>=0'),
        trials_per_action_boundary=trials, censor_horizon=horizon, confidence_exponent=12,
        confidence_tail_count=tail_count, joint_failure_probability_upper=F(1, 1000),
        certificate=certificate, receipts=receipts, independent_source_event_checks=checks,
        all_tested_exact_checks_passed=True, order_comparison=comparison, program_checks=programs, costs=costs,
        direct_endpoint_comparator=dict(receipts=direct, difference_interval=direct_interval,
            order_resolved=direct_interval[0] > 0, costs=direct_costs,
            scope='Same infinite source and boundary interface; this two-program answer has no all-word reuse guarantee.'),
        simulation_seconds_diagnostic=time.perf_counter()-started,
        execution_scope='Software integer-RNG trajectories; no laboratory operation or sensor warranty acquired.',
        strong_existing_route='Positive interval propagation around the acquired true Galerkin residual, using identical counts and the same boundary interface.')
    path = ROOT/'results'/'ABSORBING_BOUNDARY_RESULTS.json'
    path.write_text(json.dumps(dumpable(output), indent=2)+'\n')
    print(json.dumps(dumpable(dict(uniform_all_word_bound=certificate['uniform_structured_all_word_bound'],
        true_galerkin_dynamical_bound=certificate['robust_galerkin_uniform_dynamical_bound'],
        order_comparison=comparison, costs=costs, results=str(path.relative_to(ROOT))))), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--trials', type=int, default=2_000_000)
    parser.add_argument('--horizon', type=int, default=32)
    parser.add_argument('--replay', action='store_true')
    args = parser.parse_args()
    run(args.trials, args.horizon, args.replay)
