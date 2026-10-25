"""Obtain a precision/cost interface and compile costed response experiments.

Exact quantized Jacobi supplies a source-derived, input-uniform accuracy bound
at a known iteration budget. A discrete optimizer allocates that budget to a
task's certified rank-one remainder. This is new code, not a recovered file.
"""
from fractions import Fraction as F
from pathlib import Path
from collections import Counter
from itertools import product
import json
import numpy as np

from acquired_inverse_relations import (SparseElimination, bits, dot, encode,
    measured, sparse_apply, transpose)
from certified_response_instrument import CertifiedBalanceInstrument, dyadic, sqrt_upper
from acquired_uncertain_operations import (AcquiredUncertainty, decode_record,
    fmatrix, floats, inner, mm, sub)


def ceiling_dyadic(x, precision=80):
    x = F(x)
    scale = 1 << precision
    return F(-((-x.numerator*scale)//x.denominator), scale)


def power_upper(x, t):
    """Upward exact dyadic exponentiation; no unbounded denominator cascade."""
    out, base = F(1), ceiling_dyadic(x)
    while t:
        if t & 1:
            out = ceiling_dyadic(out*base)
        base = ceiling_dyadic(base*base)
        t //= 2
    return out


def nearest_dyadic(x, precision):
    scale = 1 << precision
    # This is exact rational rounding, including negative numbers.
    numerator = (2*x.numerator*scale+x.denominator)//(2*x.denominator)
    return F(numerator, scale)


class QuantizedJacobiInstrument:
    def __init__(self, mass, n=32, precision=40):
        source = CertifiedBalanceInstrument(n=n, mass=mass)
        self._rows, self.n, self.margin = source._rows, n, source.margin
        self.contraction = max(sum((abs(v) for j, v in row.items() if j != i), F(0))/abs(row[i])
                               for i, row in enumerate(self._rows))
        assert F(0) <= self.contraction < 1
        self.precision = precision
        self.rounding_error = F(1, 1 << (precision+1))
        self.counts = Counter()
        self.maximum_state_bits = self.maximum_intermediate_bits = 0
        self.maximum_input_bits = 0
        self.records = []

    def uniform_error(self, sweeps):
        # Supplied source condition, independently checked, guarantees this
        # for EVERY ||f||_infinity<=1, before observing its response.
        return power_upper(self.contraction, sweeps)/self.margin+self.rounding_error/(1-self.contraction)

    def contract(self):
        off = sum(len(row)-1 for row in self._rows)
        return dict(dimension=self.n, checked_dominance_margin=self.margin,
                    checked_Jacobi_contraction=self.contraction,
                    fixed_fractional_bits=self.precision,
                    input_contract='Rational coordinates with ||f||_infinity<=1; executed inputs also satisfy ||f||_2<=1.',
                    uniform_error_formula='alpha^t/mu + 2^(-p-1)/(1-alpha)',
                    Fraction_arithmetic_calls_per_sweep=2*off+2*self.n,
                    integer_quantizations_per_sweep=self.n,
                    final_residual_Fraction_arithmetic_calls=2*(off+self.n)+self.n+1,
                    optimization_cost_unit='Jacobi sweeps. Query overhead, rational arithmetic and integer quantization are reported separately; sweep optimality is not a wall-time optimality claim.')

    def query(self, f, sweeps):
        f = [F(a) for a in f]
        assert len(f) == self.n and max(map(abs, f)) <= 1 and sweeps >= 0
        self.maximum_input_bits = max(self.maximum_input_bits, bits(f))
        y = [F(0)]*self.n
        for _ in range(sweeps):
            next_y = []
            for i, row in enumerate(self._rows):
                value = (f[i]-sum((a*y[j] for j, a in row.items() if j != i), F(0)))/row[i]
                self.maximum_intermediate_bits = max(self.maximum_intermediate_bits, bits([value]))
                next_y.append(nearest_dyadic(value, self.precision))
            y = next_y
            self.maximum_state_bits = max(self.maximum_state_bits, bits(y))
        residual = [a-b for a, b in zip(f, sparse_apply(self._rows, y))]
        uniform = self.uniform_error(sweeps)
        residual_bound = max(map(abs, residual))/self.margin
        enclosure = min(uniform, residual_bound)
        self.counts['native_forward_queries'] += 1
        self.counts['Jacobi_sweeps'] += sweeps
        self.counts['integer_quantizations'] += self.n*sweeps
        record = dict(input=f, response=y, coordinate_error_bound=enclosure,
                      uniform_prequery_coordinate_error=uniform,
                      exact_residual_coordinate_error=residual_bound,
                      requested_error=uniform, requested_accuracy_met=True,
                      sweeps=sweeps, exact_residual=residual,
                      source_kind='Exact fixed-precision quantized Jacobi under a checked diagonal-dominance contract.')
        self.records.append(record)
        return record

    def cost(self):
        return dict(counts=dict(self.counts), input_width=self.n, output_width=self.n,
                    returned_response_scalars=self.n*self.counts['native_forward_queries'],
                    maximum_state_rational_bit_length=self.maximum_state_bits,
                    maximum_intermediate_rational_bit_length=self.maximum_intermediate_bits,
                    maximum_input_rational_bit_length=self.maximum_input_bits,
                    native_transpose_queries=0)


def obtain_menu(source, rho, gain):
    modes = []
    # Ratios fixed independently of either source's measured responses.
    for ratio in (F(3, 4), F(1, 4), F(1, 16), F(1, 64)):
        target = rho*ratio
        floor = gain*source.rounding_error/(1-source.contraction)
        if floor >= target:
            modes.append(dict(available=False, target_residual_error=target,
                              reason='Fixed quantization floor exceeds this requested accuracy.'))
            continue
        hi = 1
        while gain*source.uniform_error(hi) > target:
            hi *= 2
        lo = 0
        while lo+1 < hi:
            mid = (lo+hi)//2
            if gain*source.uniform_error(mid) <= target:
                hi = mid
            else:
                lo = mid
        modes.append(dict(available=True, sweeps=hi,
                          coordinate_error=source.uniform_error(hi),
                          residual_error=gain*source.uniform_error(hi),
                          target_residual_error=target))
    return modes


def allocate(weights, rho, modes, budget, desired_error=None, overhead=F(0)):
    """Exact discrete optimization of this declared rank-one certificate.

    Returns the smallest sweep cost attaining the target, if one fits budget;
    otherwise returns the largest certified improvement within the budget.
    The convex-history information class need not have this exact minimax value.
    """
    options = [(0, rho, -1)]+[(m['sweeps'], m['residual_error'], j)
                             for j, m in enumerate(modes) if m['available']]
    frontier = {0: (F(0), [])}
    transitions = 0
    for weight in weights:
        next_frontier = {}
        for cost, (gain, assignment) in frontier.items():
            for c, eta, j in options:
                if cost+c > budget:
                    continue
                new_gain = gain+weight*(rho-eta)
                transitions += 1
                if cost+c not in next_frontier or new_gain > next_frontier[cost+c][0]:
                    next_frontier[cost+c] = (new_gain, assignment+[j])
        frontier, best_gain = {}, F(-1)
        for cost in sorted(next_frontier):
            value = next_frontier[cost]
            if value[0] > best_gain:
                frontier[cost] = value
                best_gain = value[0]
    baseline = overhead+rho*sum(weights, F(0))
    admissible = [(c, gain, a) for c, (gain, a) in frontier.items()
                  if desired_error is not None and baseline-gain <= desired_error]
    if admissible:
        cost, gain, assignment = min(admissible, key=lambda v: v[0])
    else:
        cost, (gain, assignment) = max(frontier.items(), key=lambda item: item[1][0])
    return dict(sweeps=cost, assigned_mode_per_term=assignment,
                guaranteed_error_upper=baseline-gain, target_attained=bool(admissible),
                source_queries=sum(j >= 0 for j in assignment), exact_DP_transitions=transitions,
                retained_frontier_points=len(frontier), budget=budget,
                scope='Exact optimum of the displayed positive rank-one error bound over the supplied precision menu, not global optimality over all historical-information algorithms or wall time.')


def factor_remainder(a, precision=32):
    u, singular, vt = np.linalg.svd(floats(a), full_matrices=False)
    n = len(a)
    reconstruction = [[F(0)]*n for _ in range(n)]
    terms, weights = [], []
    for k in range(len(singular)):
        s = max(F(0), dyadic(singular[k], 40))
        left = [dyadic(v, precision) for v in u[:, k]]
        right = [dyadic(v, precision) for v in vt[k]]
        nl = sqrt_upper(dot(left, left))
        nr = sqrt_upper(dot(right, right))
        if not nr or not s:
            terms.append(dict(coefficient=[F(0)]*n, query=[F(0)]*n, weight=F(0)))
            weights.append(F(0))
            continue
        query = [v/nr for v in right]
        coefficient = [s*nr*v for v in left]
        assert dot(query, query) <= 1
        weight = s*nr*nl
        weights.append(weight)
        terms.append(dict(coefficient=coefficient, query=query, weight=weight))
        for i in range(n):
            for j in range(n):
                reconstruction[i][j] += coefficient[i]*query[j]
    residual = sub(a, reconstruction)
    remainder_nuclear_bound = sqrt_upper(F(n))*sqrt_upper(inner(residual, residual))
    return dict(terms=terms, weights=weights, reconstruction_remainder_nuclear_upper=remainder_nuclear_bound,
                statement='Each rank-one term is exact rational; numerical SVD success is not required for the bound.')


def diagonal_controls():
    weights = [F(7), F(3), F(1)]
    rho = F(2, 5)
    modes = [dict(available=True, sweeps=1, residual_error=F(1, 5)),
             dict(available=True, sweeps=3, residual_error=F(1, 20))]
    tests = []
    for budget in range(8):
        plan = allocate(weights, rho, modes, budget)
        enumeration = []
        for choices in product((-1, 0, 1), repeat=3):
            cost = sum(modes[j]['sweeps'] for j in choices if j >= 0)
            if cost <= budget:
                value = sum((w*(rho if j < 0 else modes[j]['residual_error']) for w, j in zip(weights, choices)), F(0))
                enumeration.append(value)
        assert plan['guaranteed_error_upper'] == min(enumeration)
        tests.append(dict(budget=budget, plan=plan, independent_exhaustive_optimum=min(enumeration)))
    return tests


def new_task_reuse(knowledge, actual_source_rows):
    """New off-diagonal response task, with an equally informed data-only tie.

    At this point all 32 input directions have been covered. A retaining
    tomography method legitimately obtains the same zero-new-query capability.
    This test establishes transfer of procedures, not a query advantage.
    """
    n = knowledge.n
    w = [[F(int(j == (i+7) % n), n) for j in range(n)] for i in range(n)]
    task = knowledge.task(w)
    u = floats(task['M'])@np.linalg.pinv(knowledge.ff.T)
    certificate, certificate_cost = measured(lambda: knowledge.certify(task, u))
    radius = certificate['model_uncertainty_term']+certificate['observation_uncertainty_term']
    center = task['nominal']+certificate['historical_offset']
    assert len(knowledge.records) == n

    def direct_retainer():
        # F is square and is checked invertible by exact elimination. For a
        # complete forcing frame, V F^T = W removes the unknown H completely.
        frows = [{j: a for j, a in enumerate(row) if a} for row in knowledge.inputs]
        ffactor = SparseElimination(frows)
        v = [ffactor.solve(row) for row in w]  # each V row is W row * F^{-T}
        assert mm(v, transpose(knowledge.inputs)) == w
        direct_center = inner(v, knowledge.responses)
        direct_radius = sum((knowledge.errors[j]*sum((abs(v[i][j]) for i in range(n)), F(0))
                             for j in range(n)), F(0))
        return dict(center=direct_center, radius=direct_radius, estimator_weights=v,
                    factor=ffactor.artifact(), additional_native_queries=0,
                    learned_B_or_rho_used=False,
                    interpretation='Exact interval from all 32 response boxes alone, sharp for unrestricted operators with this invertible forcing matrix.')

    data_only, data_only_cost = measured(direct_retainer)
    reference = SparseElimination(actual_source_rows)
    new_response_errors = []
    for record in knowledge.records[22:]:
        actual_response = reference.solve(record['input'])
        error = max(abs(a-b) for a, b in zip(actual_response, record['response']))
        assert error <= record['coordinate_error_bound']
        new_response_errors.append(error)
    exact = F(0)
    for j in range(n):
        column = reference.solve([F(i == j) for i in range(n)])
        exact += sum((w[i][j]*column[i] for i in range(n)), F(0))
    assert center-radius <= exact <= center+radius
    assert data_only['center']-data_only['radius'] <= exact <= data_only['center']+data_only['radius']
    return dict(task='Mean response across a previously unqueried sensor/actuator pairing',
                W=w, additional_native_queries=0, all_history_certificate=certificate,
                certificate_cost=certificate_cost, result=dict(center=center, radius=radius),
                equally_informed_data_only_retainer=data_only, data_only_construction_cost=data_only_cost,
                independent_source_reference=exact,
                independent_new_response_enclosure_control=dict(checked_records=len(new_response_errors),
                                                                all_enclosures_valid=True,
                                                                actual_coordinate_errors=new_response_errors),
                consequence='A new, non-diagonal task is answered from retained full responses. Ordinary retaining tomography ties this operation once the complete input span is acquired.')


def run():
    root = Path(__file__).resolve().parent
    instruments = json.loads((root/'certified_response_instrument_results.json').read_text())
    operations = json.loads((root/'acquired_uncertain_operations_results.json').read_text())
    witnesses = json.loads((root/'acquired_uncertainty_witnesses_results.json').read_text())
    cases = []
    for ci, co, cw in zip(instruments['preselected_cases'], operations['preselected_cases'], witnesses['cases']):
        rows = [{int(j): F(v) for j, v in row.items()} for row in ci['proposed_model']['rows']]
        factor = SparseElimination.load(ci['proposed_model']['factor'])
        records = [decode_record(r) for r in co['retained_final_observations']]
        records.append(decode_record(cw['one_witness_generated_intervention']['actual_record']))
        knowledge = AcquiredUncertainty(rows, factor, F(ci['calibration']['rho']), records)
        source = QuantizedJacobiInstrument(mass=F(ci['mass']))
        absolute_row_sums = [sum(map(abs, row.values()), F(0)) for row in rows]
        residual_gain = sqrt_upper(dot(absolute_row_sums, absolute_row_sums))
        menu, menu_cost = measured(lambda: obtain_menu(source, knowledge.rho, residual_gain))
        workload = co['workloads'][-1]
        task = knowledge.task(fmatrix(workload['W']))
        # Use the strongest inexpensive retained projection, rather than pay
        # for ADMM after its negligible benefit was exposed.
        u = floats(task['M'])@np.linalg.pinv(knowledge.ff.T)
        base, base_cost = measured(lambda: knowledge.certify(task, u))
        decomposition, decomposition_cost = measured(lambda: factor_remainder(base['unresolved_task_coefficient']))
        overhead = base['observation_uncertainty_term']+knowledge.rho*decomposition['reconstruction_remainder_nuclear_upper']
        budget = 2*max(m['sweeps'] for m in menu if m['available'])
        plan, plan_cost = measured(lambda: allocate(decomposition['weights'], knowledge.rho, menu, budget,
                                                    desired_error=F(1, 10**4), overhead=overhead))
        center = task['nominal']+base['historical_offset']
        error = overhead
        executed = []
        for term, mode_index in zip(decomposition['terms'], plan['assigned_mode_per_term']):
            if mode_index < 0:
                error += knowledge.rho*term['weight']
                continue
            mode = menu[mode_index]
            record, cost = measured(lambda: source.query(term['query'], mode['sweeps']))
            residual_center = [a-b for a, b in zip(sparse_apply(rows, record['response']), record['input'])]
            center += dot(term['coefficient'], residual_center)
            actual_eta = residual_gain*record['coordinate_error_bound']
            assert actual_eta <= mode['residual_error']
            error += term['weight']*actual_eta
            executed.append(dict(mode_index=mode_index, record=record, execution_cost=cost,
                                 residual_error_upper=actual_eta))
        assert error <= plan['guaranteed_error_upper']
        # Reference truth is read only after construction and execution.
        truth = F(workload['separate_full_source_control']['exact_answer'])
        assert center-error <= truth <= center+error
        result = dict(mass=F(ci['mass']), all_prior_records_used=len(records),
                      source_contract=source.contract(), obtained_precision_menu=menu,
                      menu_construction_cost=menu_cost, base_history_certificate=base,
                      base_certificate_cost=base_cost, certified_rank_one_decomposition=decomposition,
                      decomposition_cost=decomposition_cost, discrete_plan=plan,
                      discrete_plan_cost=plan_cost, executed=executed,
                      result_interval=dict(center=center, radius=error, lower=center-error, upper=center+error),
                      source_cost=source.cost(),
                      separate_reference_check=dict(true_answer=truth, contained=True,
                                                     actual_center_error=abs(center-truth)),
                      fairness='Every observation from acquisition, both earlier task runs, and the separating experiment is retained. The precision menu is obtained from checked source coefficients inside the instrument, not inferred from favorable observed convergence.')
        for item in executed:
            knowledge.append(item['record'])
        actual_rows = [{int(j): F(v) for j, v in row.items()} for row in ci['full_source_controls']['actual_rows']]
        result['retained_observations_after_operation'] = knowledge.records
        result['genuinely_new_task_reuse'] = new_task_reuse(knowledge, actual_rows)
        cases.append(result)
        (root/'certified_precision_design_results.json').write_text(json.dumps(encode(dict(cases=cases)), indent=2))
        print('precision plan',ci['mass'],'modes',[(m['sweeps'],float(m['residual_error'])) for m in menu if m['available']],
              'calls',plan['source_queries'],'sweeps',plan['sweeps'],'guarantee',float(plan['guaranteed_error_upper']),
              'actual_certificate',float(error), flush=True)
    controls = diagonal_controls()
    final = dict(cases=cases, exact_discrete_controls=controls,
                 distinction='The ideal variable-precision minimax theorem and the exact optimum of this finite certificate family are different claims. Native widths, full history, arithmetic and conditioning are not discarded.')
    (root/'certified_precision_design_results.json').write_text(json.dumps(encode(final), indent=2))
    return final


if __name__ == '__main__':
    run()
