"""New work: acquired, history-aware evaluators for uncertain response tasks.

Numerical optimization proposes procedures. Rational post-verification proves
their bounds. Every past full response and coordinate enclosure is available.
No native transpose, exact response, or desired task answer is used by the
learner. Source-aware reference computations are separate controls.
"""
from fractions import Fraction as F
from pathlib import Path
from collections import Counter
import json
import time

import numpy as np

from acquired_inverse_relations import (SparseElimination, bits, dense, dot,
    encode, eye, measured, sparse_apply, transpose)
from certified_response_instrument import CertifiedBalanceInstrument, dyadic, sqrt_upper


def fmatrix(a):
    return [[F(v) for v in row] for row in a]


def floats(a):
    return np.array([[float(v) for v in row] for row in a], dtype=float)


def mm(a, b):
    bt = transpose(b)
    return [[dot(row, col) for col in bt] for row in a]


def sub(a, b):
    return [[x-y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def inner(a, b):
    return sum((dot(ar, br) for ar, br in zip(a, b)), F(0))


def nuclear_upper(a, precision=32):
    """A floating SVD proposes factors; exact arithmetic verifies a bound.

    ||A||_* <= (||P||_F^2+||Q||_F^2)/2
                 + sqrt(min(shape(A)))*||A-P Q^T||_F.
    The statement needs no guarantee about the numerical SVD.
    """
    af = floats(a)
    u, s, vt = np.linalg.svd(af, full_matrices=False)
    p = [[dyadic(x, precision) for x in row] for row in u*np.sqrt(s)]
    q = [[dyadic(x, precision) for x in row] for row in vt.T*np.sqrt(s)]
    residual = sub(a, mm(p, transpose(q)))
    factor_energy = (inner(p, p)+inner(q, q))/2
    residual_frobenius = sqrt_upper(inner(residual, residual))
    bound = factor_energy+sqrt_upper(F(min(af.shape)))*residual_frobenius
    return dict(bound=bound, proposed_left_factor=p, proposed_right_factor=q,
                factor_energy=factor_energy, residual_frobenius_upper=residual_frobenius,
                numerical_singular_values=[float(v) for v in s],
                maximum_residual_bit_length=bits(v for row in residual for v in row),
                floating_SVD_calls=1, factor_rounding_bits=precision)


def unit_proposal(x, precision=26):
    """Exactly rational vector with certified Euclidean norm at most one."""
    v = [dyadic(a, precision) for a in x]
    norm = sqrt_upper(dot(v, v))
    if not norm:
        raise ValueError('zero proposed experiment')
    out = [a/norm for a in v]
    assert dot(out, out) <= 1
    return out


def decode_record(record):
    return dict(input=[F(x) for x in record['input']],
                response=[F(x) for x in record['response']],
                coordinate_error_bound=F(record['coordinate_error_bound']),
                requested_error=F(record['requested_error']),
                requested_accuracy_met=bool(record['requested_accuracy_met']),
                sweeps=int(record['sweeps']))


class AcquiredUncertainty:
    def __init__(self, rows, factor, rho, records):
        self.rows = rows
        self.n = len(rows)
        self.factor = factor
        self.rho = F(rho)
        self.records = list(records)
        self.bf = floats(dense(rows))
        self.solver_counts = Counter()
        self.refresh()

    def refresh(self):
        self.inputs = transpose([r['input'] for r in self.records])
        self.responses = transpose([r['response'] for r in self.records])
        self.errors = [r['coordinate_error_bound'] for r in self.records]
        self.residuals = transpose([[a-b for a, b in zip(sparse_apply(self.rows, r['response']), r['input'])]
                                    for r in self.records])
        self.ff = floats(self.inputs)
        self.cf = floats(self.residuals)
        self.df = np.array([float(e) for e in self.errors])

    def append(self, record):
        self.records.append(record)
        self.refresh()

    def task(self, w):
        w = fmatrix(w)
        # M=B^{-T} W; tr(W^T B^{-1}) = tr(M).
        m = transpose([self.factor.solve_transpose(col) for col in transpose(w)])
        nominal = sum((m[i][i] for i in range(self.n)), F(0))
        return dict(W=w, M=m, nominal=nominal)

    def propose(self, task, sign=1, iterations=1600, beta=0.7):
        """Two-block ADMM proposes dual multipliers, never a proof of optimality.

        U is residual-coordinate multiplier; V=B^T U. Minimize
        ||M-U F^T||_* + <C,U>/rho + sum_j delta_j ||B^T U_j||_1/rho.
        X and S form one separable block, U the other. Feasible dual upper
        certificates exist for EVERY U, irrespective of ADMM convergence.
        """
        start = time.perf_counter()
        m = floats(task['M'])*sign
        f, b = self.ff, self.bf
        c = self.cf/float(self.rho)
        d = self.df/float(self.rho)
        n, q = f.shape
        # Historical least-squares projection is a legitimate retained baseline.
        projection = m @ np.linalg.pinv(f.T)
        u = projection.copy()
        x = m-u@f.T
        s = b.T@u
        d1, d2 = np.zeros_like(x), np.zeros_like(s)
        eg, pg = np.linalg.eigh(b@b.T)
        ek, pk = np.linalg.eigh(f.T@f)
        denominator = eg[:, None]+ek[None, :]
        if np.min(denominator) <= 0:
            # Positive B B^T makes the exact system positive; numerical failure
            # is a failed proposal, not grounds to alter a certificate.
            return [np.zeros_like(u), projection], dict(failed='Numerical normal system is not positive.', iterations=0)
        best = u.copy()
        def objective(v):
            return float(np.sum(np.linalg.svd(m-v@f.T, compute_uv=False))
                         +np.sum(c*v)+np.sum(d[None, :]*np.abs(b.T@v)))
        best_value = objective(best)
        objective_evaluations = 1
        for step in range(1, iterations+1):
            left, singular, right = np.linalg.svd(m-u@f.T-d1, full_matrices=False)
            x = (left*np.maximum(singular-1/beta, 0))@right
            value = b.T@u-d2
            s = np.sign(value)*np.maximum(np.abs(value)-d[None, :]/beta, 0)
            rhs = (m-x-d1)@f+b@(s+d2)-c/beta
            u = pg@((pg.T@rhs@pk)/denominator)@pk.T
            r1, r2 = x+u@f.T-m, s-b.T@u
            d1 += r1
            d2 += r2
            if step % 40 == 0 or step == iterations:
                value = objective(u)
                objective_evaluations += 1
                if value < best_value:
                    best, best_value = u.copy(), value
        self.solver_counts['ADMM_iterations'] += iterations
        self.solver_counts['floating_SVD_calls'] += iterations+objective_evaluations
        self.solver_counts['floating_eigendecompositions'] += 2
        self.solver_counts['floating_pseudoinverses'] += 1
        return [np.zeros_like(u), projection, best], dict(
            iterations=iterations, floating_SVD_calls=iterations+objective_evaluations,
            floating_eigendecompositions=2, floating_pseudoinverses=1,
            numerical_best_scaled_objective=best_value,
            numerical_primal_residual=float(np.hypot(np.linalg.norm(r1), np.linalg.norm(r2))),
            wall_seconds=time.perf_counter()-start,
            interpretation='Optimization proposal only. No computed optimality or duality gap is asserted.')

    def certify(self, task, multipliers, sign=1, precision=30):
        u = [[dyadic(v, precision) for v in row] for row in multipliers]
        target = [[sign*v for v in row] for row in task['M']]
        residual = sub(target, mm(u, transpose(self.inputs)))
        nuclear = nuclear_upper(residual)
        # Sparse B^T U, preserving every coordinatewise history enclosure.
        q = len(self.records)
        v = [[F(0)]*q for _ in range(self.n)]
        for i, row in enumerate(self.rows):
            for j, coefficient in row.items():
                for k in range(q):
                    v[j][k] += coefficient*u[i][k]
        noise = sum((self.errors[k]*sum((abs(v[i][k]) for i in range(self.n)), F(0))
                     for k in range(q)), F(0))
        offset = inner(u, self.residuals)
        residual_bound = self.rho*nuclear['bound']
        bound = sign*task['nominal']+offset+residual_bound+noise
        return dict(bound=bound, residual_coordinate_multipliers=u,
                    historical_offset=offset, model_uncertainty_term=residual_bound,
                    observation_uncertainty_term=noise, nuclear_certificate=nuclear,
                    unresolved_task_coefficient=residual, sign=sign,
                    records_used=q, multiplier_rounding_bits=precision,
                    maximum_multiplier_bit_length=bits(x for row in u for x in row),
                    meaning='Upper bound on sign*<W,H>, conditional on the one retained all-input calibration event.')

    def interval(self, task, previous=None, iterations=1600):
        endpoints, proposals, all_costs = [], [], []
        for sign in (1, -1):
            candidates, solver = self.propose(task, sign, iterations=iterations)
            # Numerical ranking only chooses a candidate; validity does not
            # depend on that ranking. Include the old valid multiplier so a
            # failed search cannot worsen a retained certificate.
            def score(u):
                a = sign*floats(task['M'])-u@self.ff.T
                return (float(self.rho)*np.linalg.svd(a, compute_uv=False).sum()
                        +np.sum(u*self.cf)+np.sum(self.df[None, :]*np.abs(self.bf.T@u)))
            chosen = min(candidates, key=score)
            current, cost = measured(lambda: self.certify(task, chosen, sign))
            all_costs.append(cost)
            if previous is not None:
                old = previous['upper_certificate' if sign == 1 else 'negative_lower_certificate']
                # Padding an old certificate with zero multipliers changes none
                # of its exact arithmetic, so reuse its proven numeric bound.
                if old['bound'] <= current['bound']:
                    old = dict(old)
                    old['residual_coordinate_multipliers'] = [row+[F(0)]*(len(self.records)-len(row))
                                                             for row in old['residual_coordinate_multipliers']]
                    old['records_used'] = len(self.records)
                    old['reused_previous_bound'] = True
                    current = old
            endpoints.append(current)
            proposals.append(solver)
        upper, neg_lower = endpoints
        lower = -neg_lower['bound']
        assert lower <= upper['bound'], 'Inconsistent certified operator set or implementation failure.'
        return dict(lower=lower, upper=upper['bound'], center=(lower+upper['bound'])/2,
                    radius=(upper['bound']-lower)/2, upper_certificate=upper,
                    negative_lower_certificate=neg_lower, numerical_search=proposals,
                    exact_verification_costs=all_costs)


def spectral_minimax_controls():
    """Exact adversarial transcript controls, independent of response fixtures."""
    sigma = [F(7), F(3), F(1)]
    rho = F(2, 5)
    results = []
    for eta in (F(0), F(1, 20), F(2, 5), F(3, 5)):
        for k in range(4):
            radius = rho*sum(sigma[k:], F(0))+min(eta, rho)*sum(sigma[:k], F(0))
            diagonal = [min(eta, rho) if i < k else rho for i in range(3)]
            witness_value = dot(sigma, diagonal)
            assert witness_value == radius
            assert all(diagonal[i] <= eta for i in range(k))
            results.append(dict(eta=eta, queries=k, exact_minimax_radius=radius,
                                plus_minus_witness_diagonal=diagonal,
                                every_queried_full_response_can_be_reported_as_zero=True))
    # All bounded errors can be systematic; repetition need not average away.
    systematic = dict(unknown_values=[F(-1, 20), F(1, 20)],
                      repeated_reports=[F(0)]*100, error_bound=F(1, 20),
                      remaining_radius_after_100_repeats=F(1, 20))
    return dict(diagonal_cases=results, systematic_error_control=systematic,
                amplitude_control='If input amplitude is unlimited while absolute error stays fixed, scaling a query can remove the noise floor. The theorem explicitly assumes ||x||_2<=1.',
                scope='Deterministic worst-case algorithms over the spectral-norm ball, not a stochastic-noise or randomized-query lower bound; extra histories can shrink the set.')


def run():
    root = Path(__file__).resolve().parent
    saved = json.loads((root/'certified_response_instrument_results.json').read_text())
    results = []
    for case in saved['preselected_cases']:
        rows = [{int(j): F(v) for j, v in row.items()} for row in case['proposed_model']['rows']]
        factor = SparseElimination.load(case['proposed_model']['factor'])
        records = [decode_record(r) for r in case['all_observations']]
        knowledge = AcquiredUncertainty(rows, factor, F(case['calibration']['rho']), records)
        source = CertifiedBalanceInstrument(mass=F(case['mass']))
        n = source.n
        # Held-out scientific quantities are specified independently of outputs.
        tasks = [('mean_local_static_response', [[F(i == j, n) for j in range(n)] for i in range(n)]),
                 ('spatial_static_response_contrast', [[F((1 if i % 4 < 2 else -1) if i == j else 0, n)
                                                       for j in range(n)] for i in range(n)])]
        workloads = []
        for name, w in tasks:
            task, construction_cost = measured(lambda: knowledge.task(w))
            interval = knowledge.interval(task)
            steps = [dict(stage='All retained observations, before new queries', interval=interval)]
            # Same budget and requested precision in both damping regimes.
            target = F(1, 10**4)
            calls_before = source.counts['forward_queries']
            for step in range(4):
                if interval['radius'] <= target:
                    break
                ap = floats(interval['upper_certificate']['unresolved_task_coefficient'])
                am = floats(interval['negative_lower_certificate']['unresolved_task_coefficient'])
                _, _, vt = np.linalg.svd((ap-am)/2, full_matrices=False)
                forcing = unit_proposal(vt[0])
                record = source.query(forcing, requested_error=F(1, 10**8))
                knowledge.append(record)
                interval = knowledge.interval(task, previous=interval)
                steps.append(dict(stage='New residual-directed unit-energy experiment',
                                  query=record, interval=interval))
            workloads.append(dict(name=name, W=w, task_construction_cost=construction_cost,
                                  predeclared_absolute_error_target=target,
                                  maximum_new_queries=4, requested_new_response_accuracy=F(1, 10**8),
                                  stages=steps, target_met=interval['radius'] <= target,
                                  new_native_queries=source.counts['forward_queries']-calls_before,
                                  no_native_transpose=True))
            print('case', case['mass'], name, 'radius', float(steps[0]['interval']['radius']),
                  '->', float(interval['radius']), 'calls', source.counts['forward_queries']-calls_before,
                  flush=True)
        # Independent exact source-aware answer: never passed to the evaluator.
        actual_rows = [{int(j): F(v) for j, v in row.items()}
                       for row in case['full_source_controls']['actual_rows']]
        reference = SparseElimination(actual_rows)
        truth = transpose([reference.solve(v) for v in eye(n)])
        for workload in workloads:
            exact_value = inner(workload['W'], truth)
            checks = [s['interval']['lower'] <= exact_value <= s['interval']['upper'] for s in workload['stages']]
            assert all(checks)
            workload['separate_full_source_control'] = dict(exact_answer=exact_value,
                                                           all_reported_intervals_contain_truth=True,
                                                           final_actual_center_error=abs(exact_value-workload['stages'][-1]['interval']['center']))
        results.append(dict(mass=F(case['mass']), calibration_failure_bound=F(case['calibration']['failure_probability_bound']),
                            acquired_rho=knowledge.rho, original_acquisition_cost=case['instrument_cost'],
                            new_instrument_cost=source.cost(), local_numerical_search_counts=dict(knowledge.solver_counts),
                            workloads=workloads, retained_final_observations=knowledge.records,
                            comparison='A conventional optimal-recovery method given the same acquired B, rho and complete history may use this exact dual and obtains the same bounds. Source-code access permits a direct sparse solve and requires no learning.'))
    output = dict(construction='History-aware acquired evaluators and generated residual-directed experiments under certified numerical error',
                  spectral_minimax_controls=spectral_minimax_controls(), preselected_cases=results,
                  restrictions=['Linearity and fixed source are supplied interface contracts.',
                                'Every source numerical error is certified from supplied software coefficients, not measured physical calibration.',
                                'Optimization is numerical search; each returned bound is verified with rational arithmetic.',
                                'The experiment selector is a heuristic for the complete historical uncertainty set, not a claim of globally optimal adaptive design.',
                                'The new experiment budget is Euclidean norm at most one; this is not a lower bound for unlimited-amplitude native calls.'])
    (root/'acquired_uncertain_operations_results.json').write_text(json.dumps(encode(output), indent=2))
    return output


if __name__ == '__main__':
    run()
