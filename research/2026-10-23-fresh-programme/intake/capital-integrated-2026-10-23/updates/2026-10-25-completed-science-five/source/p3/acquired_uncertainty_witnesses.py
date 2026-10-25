"""Constructive limits and counterexample experiments from uncertain history.

No hidden response matrix or task answer is used to construct the witnesses.
They are feasible alternatives in the explicitly retained spectral-ball/box
model K, not necessarily in every additional physical or source-code class.
"""
from fractions import Fraction as F
from pathlib import Path
import json
import numpy as np

from acquired_inverse_relations import (SparseElimination, bits, dot, encode,
    eye, matvec, measured, transpose)
from acquired_relational_semantics import nullspace
from certified_response_instrument import CertifiedBalanceInstrument, dyadic, sqrt_upper
from acquired_uncertain_operations import (AcquiredUncertainty, decode_record,
    floats, fmatrix, inner, mm, sub, unit_proposal)


def gram_operator_upper(frame):
    k = len(frame[0])
    gram_error = sub(mm(transpose(frame), frame), eye(k))
    return sqrt_upper(F(1)+sqrt_upper(inner(gram_error, gram_error)))


def obtain_alternatives(knowledge, task, rounding_bits=44):
    """Searches a feasible center and a full-history-invisible perturbation.

    The exact nullspace is obtained from the actual forcing history. A floating
    SVD proposes a polar factor, but exact Gram residuals bound its norm.
    """
    n = knowledge.n
    # Numerical interpolation is only a proposal. Exact checks follow.
    r0f = knowledge.cf@np.linalg.pinv(knowledge.ff)
    r0 = [[dyadic(v, 48) for v in row] for row in r0f]
    center_norm = sqrt_upper(inner(r0, r0))  # >= spectral norm
    if center_norm >= knowledge.rho:
        return dict(obtained=False, reason='Proposed center has no certified spectral-ball slack.',
                    center_frobenius_upper=center_norm)
    center_responses, slacks = [], []
    for record in knowledge.records:
        f = record['input']
        rf = matvec(r0, f)
        y0 = knowledge.factor.solve([a+b for a, b in zip(f, rf)])
        error = max(abs(a-b) for a, b in zip(y0, record['response']))
        slack = record['coordinate_error_bound']-error
        if slack < 0:
            return dict(obtained=False, reason='Proposed center fails a retained observation enclosure.',
                        failed_record=len(slacks), signed_slack=slack)
        center_responses.append(y0)
        slacks.append(slack)
    null_rows = nullspace(transpose(knowledge.inputs), n)
    d = len(null_rows)
    if not d:
        return dict(obtained=False, reason='No exactly unobserved forcing direction remains; this witness constructor does not exploit observation noise.')
    null_basis = transpose(null_rows)
    nf = floats(null_basis)
    qf, _ = np.linalg.qr(nf, mode='reduced')
    coefficients = np.linalg.lstsq(nf, qf, rcond=None)[0]
    rational_coefficients = [[dyadic(v, rounding_bits) for v in row] for row in coefficients]
    v = mm(null_basis, rational_coefficients)
    # Every column of V annihilates the entire history, exactly.
    annihilation = mm(transpose(v), knowledge.inputs)
    assert all(a == 0 for row in annihilation for a in row)
    m = floats(task['M'])
    left, _, right = np.linalg.svd(m@floats(v), full_matrices=False)
    j = [[dyadic(a, rounding_bits) for a in row] for row in left@right]
    perturbation = mm(j, transpose(v))
    norm_bound = gram_operator_upper(j)*gram_operator_upper(v)
    scale = (knowledge.rho-center_norm)/norm_bound
    signed_half_gap = scale*inner(task['M'], perturbation)
    if signed_half_gap < 0:
        j = [[-a for a in row] for row in j]
        perturbation = [[-a for a in row] for row in perturbation]
        signed_half_gap = -signed_half_gap
    # <M,R0> is the center's task correction; no true answer is supplied.
    center_value = task['nominal']+inner(task['M'], r0)
    assert scale > 0 and signed_half_gap >= 0
    return dict(obtained=True, center_residual_operator=r0,
                perturbation_left_factor=j, perturbation_right_factor=v,
                perturbation_scale=scale, center_frobenius_upper=center_norm,
                perturbation_operator_norm_upper=norm_bound,
                certified_residual_norm_upper=center_norm+scale*norm_bound,
                minimum_historical_box_slack=min(slacks),
                every_past_full_response_exactly_unchanged_by_perturbation=True,
                unobserved_forcing_dimension=d, records_used=len(knowledge.records),
                minus_task_value=center_value-signed_half_gap,
                plus_task_value=center_value+signed_half_gap,
                information_radius_lower_bound=signed_half_gap,
                exact_nullspace_basis=null_basis,
                maximum_nullspace_bit_length=bits(a for row in null_basis for a in row),
                maximum_perturbation_bit_length=bits(a for row in perturbation for a in row),
                interpretation='H_plus/minus = B^{-1}(I+R0 +/- scale*J*V^T). Both belong to the full retained set K. Their existence lower-bounds any deterministic estimator on this recorded history, regardless of its computation.')


def propose_distinguishing_query(knowledge, witness):
    perturbation = mm(witness['perturbation_left_factor'], transpose(witness['perturbation_right_factor']))
    columns = [knowledge.factor.solve(col) for col in transpose(perturbation)]
    response_difference_shape = transpose(columns)
    _, _, vt = np.linalg.svd(floats(response_difference_shape), full_matrices=False)
    forcing = unit_proposal(vt[0])
    shift = [witness['perturbation_scale']*a for a in matvec(response_difference_shape, forcing)]
    center_forcing = [a+b for a, b in zip(forcing, matvec(witness['center_residual_operator'], forcing))]
    center_response = knowledge.factor.solve(center_forcing)
    minus = [a-b for a, b in zip(center_response, shift)]
    plus = [a+b for a, b in zip(center_response, shift)]
    separation = max(abs(a-b) for a, b in zip(plus, minus))
    return dict(input=forcing, predicted_minus_response=minus, predicted_plus_response=plus,
                response_infinity_separation=separation,
                sufficient_coordinate_error_for_disjoint_reporting_boxes=separation/2,
                reasoning='A coordinate enclosure smaller than half this separation cannot contain both alternatives after this query.')


def known_answer_controls():
    controls = []
    for eta in (F(0), F(1, 20)):
        n = 3
        rows = [{i: F(1)} for i in range(n)]
        records = [dict(input=v, response=v, coordinate_error_bound=eta,
                        requested_error=max(eta, F(1, 10**12)), requested_accuracy_met=True, sweeps=0)
                   for v in eye(n)]
        knowledge = AcquiredUncertainty(rows, SparseElimination(rows), F(2, 5), records)
        weights = [F(7), F(3), F(1)]
        w = [[weights[i] if i == j else F(0) for j in range(n)] for i in range(n)]
        task = knowledge.task(w)
        interval = knowledge.interval(task, iterations=200)
        exact_radius = eta*sum(weights)
        assert interval['radius'] >= exact_radius
        assert float(interval['radius']-exact_radius) < 1e-8
        controls.append(dict(eta=eta, exact_radius=exact_radius,
                             certified_interval=interval, known_sharp_alternatives='H=I +/- eta*I'))
    # Repeating the same bounded-error report cannot reveal an exact zero.
    structural = dict(reported_matrix=[[F(1), F(0)], [F(0), F(1)]],
                      alternative_one=[[F(1), F(0)], [F(0), F(1)]],
                      alternative_two=[[F(1), F(1, 1000)], [F(0), F(1)]],
                      coordinate_error_bound=F(1, 1000),
                      all_unit_input_reports_of_first_alternative_can_mask_second=True,
                      meaning='A zero coupling and a small nonzero coupling remain compatible; arbitrary exact structural sparsity is not acquired from finite bounded-error evidence.')
    source = CertifiedBalanceInstrument(n=8, mass=F(1, 100), max_sweeps=1)
    record = source.query([F(1)]*8, requested_error=F(1, 10**20))
    assert not record['requested_accuracy_met']
    assert record['coordinate_error_bound'] > record['requested_error']
    return dict(diagonal_minimax_controls=controls, noisy_zero_control=structural,
                deliberate_solver_budget_failure=dict(record=record, cost=source.cost(),
                                                       honest_unmet_precision_reported=True))


def run():
    root = Path(__file__).resolve().parent
    instruments = json.loads((root/'certified_response_instrument_results.json').read_text())
    saved = json.loads((root/'acquired_uncertain_operations_results.json').read_text())
    cases = []
    for instrument_case, history_case in zip(instruments['preselected_cases'], saved['preselected_cases']):
        rows = [{int(j): F(v) for j, v in row.items()} for row in instrument_case['proposed_model']['rows']]
        factor = SparseElimination.load(instrument_case['proposed_model']['factor'])
        all_records = [decode_record(r) for r in history_case['retained_final_observations']]
        outcomes = []
        for workload in history_case['workloads']:
            old_interval = workload['stages'][-1]['interval']
            q = old_interval['upper_certificate']['records_used']
            knowledge = AcquiredUncertainty(rows, factor, F(instrument_case['calibration']['rho']), all_records[:q])
            task = knowledge.task(fmatrix(workload['W']))
            witness, construction_cost = measured(lambda: obtain_alternatives(knowledge, task))
            item = dict(task=workload['name'], witness=witness, construction_cost=construction_cost,
                        achieved_interval_radius=F(old_interval['radius']),
                        predeclared_target=F(workload['predeclared_absolute_error_target']))
            if witness['obtained']:
                assert witness['information_radius_lower_bound'] <= F(old_interval['radius'])
                item['current_evidence_proves_target_unattainable_in_K'] = witness['information_radius_lower_bound'] > item['predeclared_target']
                item['upper_to_lower_radius_ratio'] = float(item['achieved_interval_radius']/witness['information_radius_lower_bound'])
            outcomes.append(item)
            print('witness', history_case['mass'], workload['name'],
                  'obtained', witness['obtained'],
                  'lower', float(witness.get('information_radius_lower_bound', 0)),
                  'upper', float(item['achieved_interval_radius']), flush=True)
        # One actual information intervention generated by the final witness.
        intervention = None
        if outcomes[-1]['witness']['obtained']:
            witness = outcomes[-1]['witness']
            plan, plan_cost = measured(lambda: propose_distinguishing_query(knowledge, witness))
            source = CertifiedBalanceInstrument(mass=F(history_case['mass']))
            record = source.query(plan['input'], requested_error=F(1, 10**8))
            eta = record['coordinate_error_bound']
            admitted = {}
            for label in ('minus', 'plus'):
                error = max(abs(a-b) for a, b in zip(plan['predicted_'+label+'_response'], record['response']))
                admitted[label] = error <= eta
            assert plan['response_infinity_separation'] > 2*eta
            assert not all(admitted.values())
            knowledge.append(record)
            # New procedure is verified from all old data and this one result.
            interval = knowledge.interval(task)
            intervention = dict(plan=plan, plan_construction_cost=plan_cost, actual_record=record,
                                alternative_survives_new_record=admitted,
                                reporting_boxes_proved_disjoint=True,
                                all_history_interval_after_query=interval, source_cost=source.cost(),
                                note='At least one exhibited alternative is excluded. This need not halve the whole compatible set or make the target attainable.')
        cases.append(dict(mass=F(history_case['mass']), outcomes=outcomes,
                          one_witness_generated_intervention=intervention,
                          scope='Limits concern the retained norm-ball and observation-box set K. Additional physical restrictions, source-code access, or other supplied structural knowledge can shrink K further.'))
        # Preserve the scientific objects before independent controls. A prior
        # development run reached both cases but failed on nested cProfile.
        (root/'acquired_uncertainty_witnesses_results.json').write_text(json.dumps(encode(dict(cases=cases)), indent=2))
    controls = known_answer_controls()
    result = dict(construction='Acquired counterexamples distinguish missing information from failed procedure search',
                  cases=cases, controls=controls,
                  preceding_failed_execution=dict(reason='Nested cProfile raised ValueError: Another profiling tool is already active, while entering the independent controls.',
                                                  completed_but_not_retained_before_failure='Four witness constructions and two separating-query executions; recreated by the successful run.',
                                                  extra_native_forward_queries=2, extra_returned_response_scalars=64,
                                                  restriction='Detailed timing from the failed run was unavailable; it is not included in successful-run arithmetic totals.'))
    (root/'acquired_uncertainty_witnesses_results.json').write_text(json.dumps(encode(result), indent=2))
    return result


if __name__ == '__main__':
    run()
