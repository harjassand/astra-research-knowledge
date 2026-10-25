"""Acquire a complete implicit presentation of a rectangular response map.

New 2026-10-25 work. Learn sparse relations C*y=D*f from interactions with a
fixed linear H:f->y. Neither H nor a hidden-state model must be invertible.
The learned C is checked for invertibility; this is an obtained property of
the retained presentation. Kernel representations and implicit sparse system
identification have substantial antecedents; see the accompanying proofs.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations
from math import comb
from pathlib import Path
import json
import random

from acquired_inverse_relations import (ForwardBalanceSource, ModularFilter,
    SparseElimination, bits, dense, dot, encode, eye, fit_exact_columns, matvec, measured,
    sparse_apply, transpose)


def nullspace(matrix, columns):
    """Exact right nullspace, with a canonical unit value per free coordinate."""
    a = [[F(v) for v in row] for row in matrix]
    rank, pivots = 0, []
    for j in range(columns):
        p = next((i for i in range(rank, len(a)) if a[i][j]), None)
        if p is None:
            continue
        a[rank], a[p] = a[p], a[rank]
        scale = a[rank][j]
        a[rank] = [v/scale for v in a[rank]]
        for i in range(len(a)):
            if i != rank and a[i][j]:
                scale = a[i][j]
                a[i] = [v-scale*w for v, w in zip(a[i], a[rank])]
        pivots.append(j)
        rank += 1
    result = []
    for j in range(columns):
        if j in pivots:
            continue
        v = [F(0)]*columns
        v[j] = F(1)
        for r, p in enumerate(pivots):
            v[p] = -a[r][j]
        result.append(v)
    return result


class RowBasis:
    def __init__(self, n):
        self.n, self.pivots, self.rows = n, [], []

    def add(self, v):
        residual = list(v)
        for p, row in zip(self.pivots, self.rows):
            a = residual[p]
            if a:
                residual = [u-a*w for u, w in zip(residual, row)]
        p = next((i for i, v in enumerate(residual) if v), None)
        if p is None:
            return False
        scale = residual[p]
        self.pivots.append(p)
        self.rows.append([v/scale for v in residual])
        return True


class RectangularTransportSource:
    """16 actuator inputs, 12 measured responses, rank 6; exact software control.

    Unknown actuation incidence and unknown nonreciprocal output balance.
    The learner receives only dimensions and forward response actions.
    The construction is not evidence that arbitrary hidden environments have
    sparse equations on their visible ports.
    """
    def __init__(self):
        self.n, self.m = 16, 12
        self.base = ForwardBalanceSource(self.m, parameter=F(1, 6))
        input_order = list(range(self.n))
        random.Random(622).shuffle(input_order)
        self._d = [{} for _ in range(self.m)]
        for i, measured in enumerate(self.base.permutation):
            a, b = input_order[2*(i//2):2*(i//2)+2]
            scale = F(1) if i % 2 == 0 else F(2, 3)
            self._d[measured] = {a: scale, b: -scale/3}
        self.calls = 0
        self.max_input_bits = self.max_output_bits = 0

    def apply(self, x):
        self.calls += 1
        self.max_input_bits = max(self.max_input_bits, bits(x))
        y = self.base._solve(sparse_apply(self._d, x))
        self.max_output_bits = max(self.max_output_bits, bits(y))
        return y

    def reference_response(self, x):
        return self.base._solve(sparse_apply(self._d, x))

    def cost(self):
        return dict(native_forward_calls=self.calls, native_transpose_calls=0,
                    input_width=self.n, output_width=self.m,
                    returned_scalar_entries=self.m*self.calls,
                    maximum_input_rational_bit_length=self.max_input_bits,
                    maximum_output_rational_bit_length=self.max_output_bits)


def validate_presentation(source, c, d, probes=5, alphabet=257, seed=3102):
    rng = random.Random(seed)
    records = []
    for _ in range(probes):
        f = [F(rng.randrange(alphabet)-alphabet//2, alphabet) for _ in range(source.n)]
        y = source.apply(f)
        residual = [a-b for a, b in zip(sparse_apply(c, y), sparse_apply(d, f))]
        records.append(dict(input=f, response=y, residual=residual))
        if any(residual):
            return dict(status='COUNTEREXAMPLE', records=records), False
    return dict(status='ACCEPTED_RANDOMIZED_PRESENTATION', records=records,
                alphabet=alphabet, probes=probes,
                fixed_candidate_false_accept_bound=F(1, alphabet**probes)), True


def acquire_presentation(source, support_budget=5, alphabet=2**61, seed=3101):
    """Enumerate local linear circuits in the input-output behavior.

    q=s experiments preserve all coordinate-subset ranks of size <=s almost
    surely for a fixed H, or with the stated finite-alphabet union bound.
    A complete learned presentation exists if such local relations span m
    independent output coefficient rows. No supplied inverse, support, rank or
    actuation incidence is used. Exponential support search is explicitly paid.
    """
    n, m = source.n, source.m
    rng = random.Random(seed)
    forcings = [[F(rng.randrange(alphabet)-alphabet//2, alphabet) for _ in range(n)]
                for _ in range(support_budget)]
    responses = [source.apply(f) for f in forcings]
    joint = [y+f for y, f in zip(responses, forcings)]
    joint_rows = transpose(joint)
    mod = ModularFilter([v for row in joint for v in row])
    modular = [[mod.cast(v) for v in row] for row in joint]
    basis = RowBasis(m)
    circuits = []
    relations = []
    statistics = Counter()
    completed = False
    for size in range(1, support_budget+1):
        for support in combinations(range(m+n), size):
            support_set = frozenset(support)
            # Supersets of already found circuits are not minimal circuits.
            # All relations in a support are spanned by its minimal circuits.
            if any(circuit <= support_set for circuit in circuits):
                statistics['nonminimal_supports_skipped'] += 1
                continue
            statistics['supports_examined'] += 1
            minor = [[modular[t][j] for j in support] for t in range(size)]
            if mod.nonsingular(minor):
                statistics['certified_modular_independence'] += 1
                continue
            statistics['exact_nullspaces_computed'] += 1
            kernel = nullspace([[row[j] for j in support] for row in joint], size)
            if not kernel:
                continue
            circuits.append(support_set)
            statistics['sample_circuits_found'] += 1
            for coefficients in kernel:
                c = {j: v for j, v in zip(support, coefficients) if j < m and v}
                d = {j-m: -v for j, v in zip(support, coefficients) if j >= m and v}
                if basis.add([c.get(j, F(0)) for j in range(m)]):
                    relations.append(dict(output_coefficients=c, input_coefficients=d,
                                          support=support, coefficients=coefficients))
                    if len(relations) == m:
                        completed = True
                        break
            if completed:
                break
        if completed:
            break
    statistics.update(mod.counts)
    record = dict(n=n, m=m, support_budget=support_budget,
                  training_inputs=forcings, training_responses=responses,
                  selected_relations=relations, statistics=dict(statistics),
                  training_rank_preservation_failure_bound=min(F(1), F(sum(k*comb(n+m, k) for k in range(1, support_budget+1)), alphabet)))
    c = [r['output_coefficients'] for r in relations]
    d = [r['input_coefficients'] for r in relations]
    if not completed:
        if not relations:
            record.update(status='UNKNOWN_NO_LOCAL_RELATIONS', source_cost=source.cost())
            return record, None
        cert, accepted = validate_presentation(source, c, d)
        record.update(status='ACQUIRED_PARTIAL_PRESENTATION' if accepted else 'FAILED_FRESH_PRESENTATION_CHECK',
                      C_rows=c, D_rows=d, output_row_rank=len(relations),
                      all_outputs_determined=False, certificate=cert,
                      source_cost=source.cost())
        return record, None
    factor = SparseElimination(c)
    cert, accepted = validate_presentation(source, c, d)
    record.update(status='ACQUIRED_COMPLETE_PRESENTATION' if accepted else 'FAILED_FRESH_PRESENTATION_CHECK',
                  C_rows=c, D_rows=d, C_factor=factor.artifact(),
                  factorization_arithmetic='Included in the measured acquisition total.', certificate=cert,
                  source_cost=source.cost())
    return record, (c, d, factor) if accepted else None


def compile_observation_query(record, observation_rows):
    """Obtain O*H=G whenever the requested rows O lie in rowspan(C).

    A complete presentation is unnecessary. Relations C*H=D suffice. Failure
    means the requested operation is not entailed by the retained relations;
    it does not mean no future acquisition could obtain it.
    """
    m, n = record['m'], record['n']
    c = [{int(j): F(v) for j, v in row.items()} for row in record['C_rows']]
    d = [{int(j): F(v) for j, v in row.items()} for row in record['D_rows']]
    crows = [[row.get(j, F(0)) for j in range(m)] for row in c]
    weights, actions = [], []
    for obs in observation_rows:
        alpha = fit_exact_columns(crows, [obs.get(j, F(0)) for j in range(m)])
        if alpha is None:
            return dict(status='UNKNOWN_OUTSIDE_ACQUIRED_OBSERVABLE_SPAN')
        action = {}
        for a, row in zip(alpha, d):
            for j, v in row.items():
                action[j] = action.get(j, F(0))+a*v
        weights.append(alpha)
        actions.append({j: v for j, v in action.items() if v})
    return dict(status='ACQUIRED_QUERY_ACTION', weights=weights, G_rows=actions,
                observations=observation_rows, input_dimension=n, native_calls=0)


class RetainedResponse:
    """An acquired executable H and H^T, requiring zero native actions."""
    def __init__(self, record):
        self.m, self.n = record['m'], record['n']
        self.c = [{int(j): F(v) for j, v in row.items()} for row in record['C_rows']]
        self.d = [{int(j): F(v) for j, v in row.items()} for row in record['D_rows']]
        self.factor = SparseElimination.load(record['C_factor'])

    def apply(self, f):
        return self.factor.solve(sparse_apply(self.d, f))

    def adjoint(self, z):
        v = self.factor.solve_transpose(z)
        out = [F(0)]*self.n
        for i, row in enumerate(self.d):
            for j, a in row.items():
                out[j] += a*v[i]
        return out


def compile_port_inverse(c, d, penalty, observations, data, n):
    """KKT compiler for C*y=D*f; no rank assumption on D or H."""
    m = len(c)
    total = 2*m+n
    rows = [{} for _ in range(total)]
    rhs = [F(0)]*total

    def add(i, j, value):
        rows[i][j] = rows[i].get(j, F(0))+value
        if not rows[i][j]:
            rows[i].pop(j)

    for obs, value in zip(observations, data):
        for i, a in obs.items():
            rhs[i] += a*value
            for j, b in obs.items():
                add(i, j, a*b)
    for i, row in enumerate(c):
        for j, a in row.items():
            add(m+n+i, j, a)
            add(j, m+n+i, a)
        for j, a in d[i].items():
            add(m+n+i, m+j, -a)
            add(m+j, m+n+i, -a)
    for i, p in enumerate(penalty):
        assert p > 0
        add(m+i, m+i, p)
    factor = SparseElimination(rows)
    solution = factor.solve(rhs)
    assert sparse_apply(rows, solution) == rhs
    y, f = solution[:m], solution[m:m+n]
    assert sparse_apply(c, y) == sparse_apply(d, f)
    return dict(response=y, forcing=f, multiplier=solution[m+n:],
                generated_equations=rows, rhs=rhs,
                executable_tape=factor.artifact(), exact_KKT_residual_zero=True)


def run():
    root = Path(__file__).resolve().parent
    source = RectangularTransportSource()
    (record, model), acquisition_ops = measured(lambda: acquire_presentation(source))
    assert model is not None
    acquisition_cost = source.cost()
    c, d, factor = model
    retained = RetainedResponse(encode(record))
    n, m = source.n, source.m
    # Full-source reference is separate; no acquisition query is charged for
    # this inspection because it is explicitly not available to the learner.
    h = transpose([source.reference_response(v) for v in eye(n)])
    hrank = RowBasis(n)
    for row in h:
        hrank.add(row)
    assert len(hrank.rows) == 6
    # The two operative identities are checked on every basis coordinate in
    # this known-answer control, separately from randomized source acquisition.
    for v in eye(n):
        assert retained.apply(v) == matvec(h, v)
    for z in eye(m):
        assert retained.adjoint(z) == matvec(transpose(h), z)
    z = [F((7*i) % 13-6, 9) for i in range(m)]
    adjoint, adjoint_ops = measured(lambda: retained.adjoint(z))
    dense_adjoint, dense_ops = measured(lambda: matvec(transpose(h), z))
    assert adjoint == dense_adjoint
    observations = [{0: F(1), 7: F(1, 3)}, {4: F(1)}, {9: F(1), 11: F(-1, 2)}]
    data = [F(2, 5), F(-3, 7), F(1, 6)]
    penalty = [F(1+i % 4, 9) for i in range(n)]
    task, task_ops = measured(lambda: compile_port_inverse(c, d, penalty, observations, data, n))
    actual_response = source.reference_response(task['forcing'])
    assert actual_response == task['response']
    # The acquired semantics itself supplies a whole-task stationarity test.
    residual = [a-y for a, y in zip(sparse_apply(observations, task['response']), data)]
    dual = [F(0)]*m
    for row, r in zip(observations, residual):
        for j, a in row.items():
            dual[j] += a*r
    gradient = [a+p*f for a, p, f in zip(retained.adjoint(dual), penalty, task['forcing'])]
    assert not any(gradient)
    # Strong equally informed observation-space solve, with the same model.
    def observation_space():
        pcols = [retained.adjoint([row.get(i, F(0)) for i in range(m)]) for row in observations]
        gram = [[F(i == j)+sum((a*b/p for a, b, p in zip(pcols[i], pcols[j], penalty)), F(0))
                 for j in range(len(observations))] for i in range(len(observations))]
        small = SparseElimination([{j: v for j, v in enumerate(row) if v} for row in gram])
        coefficients = small.solve(data)
        forcing = [sum((coefficients[j]*pcols[j][i] for j in range(len(observations))), F(0))/penalty[i]
                   for i in range(n)]
        return dict(forcing=forcing, response=retained.apply(forcing))
    standard, standard_ops = measured(observation_space)
    assert standard['forcing'] == task['forcing']
    result = dict(construction='Acquired complete input-output relations and reusable semantics without a square or invertible response',
                  acquisition=record, acquisition_arithmetic=acquisition_ops,
                  known_answer_control=dict(response_rows=m, input_columns=n, rank=6,
                                            all_basis_forward_and_adjoint_checks_exact=True,
                                            true_microscopic_equations_not_required_to_match=True),
                  new_adjoint=dict(input=z, output=adjoint, arithmetic=adjoint_ops,
                                   dense_arithmetic=dense_ops, native_calls=0),
                  new_inverse_task=dict(observations=observations, data=data, penalty=penalty,
                                        generated=task, arithmetic=task_ops,
                                        exact_total_gradient_zero=True,
                                        equally_informed_observation_solve=standard,
                                        equally_informed_observation_arithmetic=standard_ops,
                                        native_calls=0),
                  acquisition_source_cost_frozen=acquisition_cost,
                  transfer_condition='Same fixed observable response H. No unobserved physical intervention is inferred from the equation presentation.',
                  limitations=['Sparse relations among visible inputs/outputs need not survive elimination of hidden variables.',
                               'The q=s statement assumes complete exact output vectors and a fixed linear response; it is not a scalar-query theorem.',
                               'Exhaustive circuit search has combinatorial arithmetic cost.',
                               'Behavioral kernel representations, implicit sparse identification and elimination compilation are antecedents; no historical novelty established by this experiment.'])
    (root/'acquired_relational_semantics_results.json').write_text(json.dumps(encode(result), indent=2))
    print(json.dumps(dict(status=record['status'], cost=acquisition_cost,
                          supports_examined=record['statistics']['supports_examined'],
                          relations_retained=len(record['selected_relations']),
                          C_nonzeros=sum(map(len, c)), D_nonzeros=sum(map(len, d)),
                          response_rank=6, adjoint_ops=adjoint_ops['total_Fraction_arithmetic_calls'],
                          dense_adjoint_ops=dense_ops['total_Fraction_arithmetic_calls'],
                          task_ops=task_ops['total_Fraction_arithmetic_calls'],
                          standard_observation_ops=standard_ops['total_Fraction_arithmetic_calls']), indent=2))
    return result


if __name__ == '__main__':
    run()
