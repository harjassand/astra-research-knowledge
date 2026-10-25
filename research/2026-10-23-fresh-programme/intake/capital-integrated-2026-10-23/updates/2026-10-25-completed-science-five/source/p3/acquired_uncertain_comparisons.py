"""Equally informed retained projection, plus a full-source algebra control.

The projection baseline receives the same B, rho and every uncertain response.
The full-source control has stronger access and is labeled accordingly. Neither
is forced to discard correlations or repeat already retained source queries.
"""
from fractions import Fraction as F
from pathlib import Path
import json
import time
import numpy as np

from acquired_inverse_relations import SparseElimination, encode, measured
from acquired_uncertain_operations import AcquiredUncertainty, decode_record, fmatrix, floats


def selected_inverse_diagonal(rows):
    """Exact selected inversion after obtaining the path ordering from rows.

    This is conventional tridiagonal LDU/selected inversion, not a discovery.
    Source entries are visible only to this explicitly stronger-access control.
    """
    n = len(rows)
    adjacent = [set(j for j, v in row.items() if j != i and v) for i, row in enumerate(rows)]
    for i in range(n):
        for j in adjacent[i]:
            assert i in adjacent[j]
    assert all(len(a) <= 2 for a in adjacent)
    first = next(i for i, a in enumerate(adjacent) if len(a) == 1)
    order, previous, current = [], None, first
    while current is not None:
        order.append(current)
        following = adjacent[current]-({previous} if previous is not None else set())
        assert len(following) <= 1
        previous, current = current, next(iter(following), None)
    assert len(order) == n
    diagonal = [rows[i][i] for i in order]
    lower = [rows[order[i+1]][order[i]] for i in range(n-1)]
    upper = [rows[order[i]][order[i+1]] for i in range(n-1)]
    pivots = list(diagonal)
    for i in range(1, n):
        pivots[i] -= lower[i-1]*upper[i-1]/pivots[i-1]
    inverse_diagonal = [F(0)]*n
    inverse_diagonal[-1] = 1/pivots[-1]
    for i in reversed(range(n-1)):
        inverse_diagonal[i] = 1/pivots[i]+upper[i]*lower[i]*inverse_diagonal[i+1]/pivots[i]**2
    out = [F(0)]*n
    for i, j in enumerate(order):
        out[j] = inverse_diagonal[i]
    return dict(diagonal=out, obtained_order=order, pivots=pivots,
                no_source_response_queries=True,
                operation='Conventional selected inversion on the supplied sparse path source.')


def run():
    root = Path(__file__).resolve().parent
    instruments = json.loads((root/'certified_response_instrument_results.json').read_text())
    operations = json.loads((root/'acquired_uncertain_operations_results.json').read_text())
    cases = []
    for ci, co in zip(instruments['preselected_cases'], operations['preselected_cases']):
        rows = [{int(j): F(v) for j, v in row.items()} for row in ci['proposed_model']['rows']]
        all_records = [decode_record(r) for r in co['retained_final_observations']]
        outputs = []
        for workload in co['workloads']:
            final = workload['stages'][-1]['interval']
            q = final['upper_certificate']['records_used']
            factor = SparseElimination.load(ci['proposed_model']['factor'])
            knowledge = AcquiredUncertainty(rows, factor, F(ci['calibration']['rho']), all_records[:q])
            task = knowledge.task(fmatrix(workload['W']))
            start = time.perf_counter()
            u = floats(task['M'])@np.linalg.pinv(knowledge.ff.T)
            proposal_time = time.perf_counter()-start
            certificate, cost = measured(lambda: knowledge.certify(task, u))
            radius = certificate['model_uncertainty_term']+certificate['observation_uncertainty_term']
            center = task['nominal']+certificate['historical_offset']
            truth = F(workload['separate_full_source_control']['exact_answer'])
            assert center-radius <= truth <= center+radius
            outputs.append(dict(task=workload['name'], records_used=q,
                                additional_native_queries=0, numerical_pseudoinverse_calls=1,
                                numerical_proposal_seconds=proposal_time,
                                certificate=certificate, certified_radius=radius, center=center,
                                exact_verification_cost=cost,
                                ADMM_search_radius=F(final['radius']),
                                ADMM_minus_projection_radius=F(final['radius'])-radius,
                                comparison='Same learned law, norm certificate and all observations. Opposite multiplier reuses the same norm/noise bound for the lower endpoint.'))
        actual = [{int(j): F(v) for j, v in row.items()} for row in ci['full_source_controls']['actual_rows']]
        selected, selected_cost = measured(lambda: selected_inverse_diagonal(actual))
        checks = []
        for workload in co['workloads']:
            w = fmatrix(workload['W'])
            value = sum((w[i][i]*selected['diagonal'][i] for i in range(len(w))), F(0))
            assert value == F(workload['separate_full_source_control']['exact_answer'])
            checks.append(dict(task=workload['name'], exact_value=value))
        cases.append(dict(mass=F(ci['mass']), equal_information_retained_projection=outputs,
                          stronger_access_source_control=dict(selected_inverse=selected,
                                                              construction_cost=selected_cost, tasks=checks,
                                                              distinction='This control reads supplied source coefficients; it is not a forward-only learner with the same observation record. It demonstrates why source code must not be artificially hidden from an incumbent that legitimately has it.')))
        print('comparison mass',ci['mass'], 'projection gaps',
              [float(o['ADMM_minus_projection_radius']) for o in outputs],
              'source Fraction ops',selected_cost['total_Fraction_arithmetic_calls'], flush=True)
    result = dict(cases=cases,
                  unexecuted_alternative='Hutchinson/Hutch++ may also use every retained observation, the acquired inverse and a residual control variate. Their randomized guarantees are discussed in the proof note; no runtime or superiority claim against an unexecuted implementation is made.')
    (root/'acquired_uncertain_comparisons_results.json').write_text(json.dumps(encode(result), indent=2))
    return result


if __name__ == '__main__':
    run()
