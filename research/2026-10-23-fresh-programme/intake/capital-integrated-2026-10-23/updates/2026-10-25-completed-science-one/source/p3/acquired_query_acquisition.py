"""Compile optimal additional experiments from acquired laws AND raw history.

New 2026-10-25 construction. For a fixed exact linear response H, retain C H=D
and every queried pair U,V=H U. All consistent completions have the form
H0+N Z T, where N spans ker(C), T annihilates U, and Z is arbitrary. A new
linear functional <W,H> requires rank(N^T W T^T) extra full-vector forward
queries in the deterministic worst case over this completion class. The code
constructs that many queries, computes the answer, and retains the new pairs.

This is optimal conditional on precisely the retained information; it is not
a randomized or scalar-oracle lower bound, and does not exclude extra priors.
"""
from fractions import Fraction as F
from pathlib import Path
import json

from acquired_inverse_relations import (SparseElimination, dot, encode, eye,
    fit_exact_columns, matvec, measured, sparse_apply, transpose)
from acquired_relational_semantics import RowBasis, nullspace
from acquired_relational_controls import MatrixResponse


def rref(a, right=None):
    """Return reduced row system, same transformed RHS, and pivot columns."""
    a = [[F(v) for v in row] for row in a]
    b = [[F(v) for v in row] for row in right] if right is not None else None
    n = len(a[0]) if a else 0
    rank, pivots = 0, []
    for j in range(n):
        p = next((i for i in range(rank, len(a)) if a[i][j]), None)
        if p is None:
            continue
        a[p], a[rank] = a[rank], a[p]
        if b is not None:
            b[p], b[rank] = b[rank], b[p]
        v = a[rank][j]
        a[rank] = [x/v for x in a[rank]]
        if b is not None:
            b[rank] = [x/v for x in b[rank]]
        for i in range(len(a)):
            if i == rank or not a[i][j]:
                continue
            v = a[i][j]
            a[i] = [x-v*y for x, y in zip(a[i], a[rank])]
            if b is not None:
                b[i] = [x-v*y for x, y in zip(b[i], b[rank])]
        pivots.append(j)
        rank += 1
    return a[:rank], b[:rank] if b is not None else None, pivots


class AcquiredKnowledge:
    def __init__(self, m, n, c, d, inputs, outputs):
        self.m, self.n = m, n
        self.c = [[F(row.get(j, 0)) for j in range(m)] for row in c]
        self.d = [[F(row.get(j, 0)) for j in range(n)] for row in d]
        self.inputs = [[F(v) for v in f] for f in inputs]
        self.outputs = [[F(v) for v in y] for y in outputs]
        self.rebuild()

    def rebuild(self):
        self.c_reduced, self.d_reduced, self.output_pivots = rref(self.c, self.d)
        if len(self.output_pivots) != len(self.c):
            raise ValueError('retained relation rows must be independent')
        self.output_free = [i for i in range(self.m) if i not in self.output_pivots]
        self.N_columns = nullspace(self.c, self.m) if self.c else eye(self.m)
        # Keep every observed pair; extract a basis only for computations.
        basis = RowBasis(self.n)
        self.input_basis, self.response_basis = [], []
        for f, y in zip(self.inputs, self.outputs):
            assert matvec(self.c, y) == matvec(self.d, f)
            if basis.add(f):
                self.input_basis.append(f)
                self.response_basis.append(y)
        _, _, self.input_pivots = rref(self.input_basis)
        self.input_free = [j for j in range(self.n) if j not in self.input_pivots]
        self.T_rows = nullspace(self.input_basis, self.n) if self.input_basis else eye(self.n)
        # Standard nullspace construction has identity on the free coordinates.
        assert [[row[j] for j in self.input_free] for row in self.T_rows] == eye(len(self.input_free))
        assert [[col[i] for col in self.N_columns] for i in self.output_free] == eye(len(self.output_free))
        u_pivots = [[v[i] for v in self.input_basis] for i in self.input_pivots]
        self.input_factor = SparseElimination([{j: v for j, v in enumerate(row) if v} for row in u_pivots]) if u_pivots else None
        self.ambiguity_dimension = len(self.output_free)*len(self.input_free)

    def base_action(self, f):
        """A particular consistent H0 f, without forming the dense H0 matrix."""
        coefficients = self.input_factor.solve([f[i] for i in self.input_pivots]) if self.input_factor else []
        y = [F(0)]*self.m
        for i in self.output_free:
            y[i] = sum((a*v[i] for a, v in zip(coefficients, self.response_basis)), F(0))
        for row, rhs, pivot in zip(self.c_reduced, self.d_reduced, self.output_pivots):
            y[pivot] = dot(rhs, f)-sum((row[i]*y[i] for i in self.output_free), F(0))
        return y

    def missing_coefficient(self, w):
        """A=N^T W T^T, coefficient of the still-unknown free matrix Z."""
        return [[sum((a*dot(row, t) for a, row in zip(ncol, w)), F(0))
                 for t in self.T_rows] for ncol in self.N_columns]

    def base_functional(self, w):
        total = F(0)
        for j in range(self.n):
            column = [row[j] for row in w]
            if any(column):
                f = [F(i == j) for i in range(self.n)]
                total += dot(column, self.base_action(f))
        return total

    def acquire_functional(self, source, w, allow_law_shortcut=True):
        """No candidate/source revalidation: existing all-input law certificate
        covers adaptive task choice, and each new response is retained exactly.
        """
        # Try a cheap acquired-law contraction before reconstructing the full
        # completion calculus. This is a standard consequence of C*H=D, and
        # any equally informed structured programme can use it.
        if allow_law_shortcut and self.c:
            law_coefficients = []
            for column in transpose(w):
                alpha = fit_exact_columns(self.c, column)
                if alpha is None:
                    break
                law_coefficients.append(alpha)
            if len(law_coefficients) == self.n:
                value = sum((a*self.d[i][j] for j, alpha in enumerate(law_coefficients)
                             for i, a in enumerate(alpha)), F(0))
                return dict(value=value, weight=w, proof='W=C^T L, hence <W,H>=<L,D>.',
                            law_coefficients_by_input_column=law_coefficients,
                            additional_forward_queries=0, records=[],
                            ambiguity_dimension_before=self.ambiguity_dimension,
                            ambiguity_dimension_after=self.ambiguity_dimension,
                            deterministic_worst_case_query_lower_bound=0,
                            selected_procedure='Direct contraction with acquired law; raw history remains retained.')
        a = self.missing_coefficient(w)
        column_basis = RowBasis(len(self.output_free))
        independent_columns = []
        for col in transpose(a) if a else []:
            if column_basis.add(col):
                independent_columns.append(col)
        rank = len(independent_columns)
        coefficient_columns = [fit_exact_columns(independent_columns, col) for col in transpose(a)] if a else []
        assert all(v is not None for v in coefficient_columns)
        factors_b = transpose(coefficient_columns) if rank else []
        value = self.base_functional(w)
        records = []
        before = source.cost()['native_forward_calls']
        old_dimension = self.ambiguity_dimension
        new_query_noise_amplifier_l1 = F(0)
        for avec, bvec in zip(independent_columns, factors_b):
            f = [F(0)]*self.n
            for j, v in zip(self.input_free, bvec):
                f[j] = v
            assert matvec(self.T_rows, f) == bvec
            scale = max(F(1), max(map(abs, f), default=F(0)))
            f = [v/scale for v in f]
            assert matvec(self.T_rows, f) == [v/scale for v in bvec]
            y = source.apply(f)
            predicted = self.base_action(f)
            free_residual = [y[i]-predicted[i] for i in self.output_free]
            contribution = scale*dot(avec, free_residual)
            new_query_noise_amplifier_l1 += scale*sum(map(abs, avec), F(0))
            value += contribution
            records.append(dict(input=f, response=y, base_response=predicted,
                                missing_output_coordinates=free_residual,
                                coefficient=avec, input_normalization=scale,
                                contribution=contribution))
        # Updating mid-factorization would change H0 and double-count terms.
        self.inputs.extend(r['input'] for r in records)
        self.outputs.extend(r['response'] for r in records)
        self.rebuild()
        assert source.cost()['native_forward_calls']-before == rank
        assert not any(v for row in self.missing_coefficient(w) for v in row)
        assert self.base_functional(w) == value
        return dict(value=value, weight=w, missing_coefficient=a,
                    rank_factor_output_columns=independent_columns,
                    rank_factor_input_rows=factors_b,
                    additional_forward_queries=rank, records=records,
                    ambiguity_dimension_before=old_dimension,
                    ambiguity_dimension_after=self.ambiguity_dimension,
                    input_absolute_coordinate_limit=1,
                    new_query_componentwise_noise_amplifier=new_query_noise_amplifier_l1,
                    noise_amplifier_scope='If retained laws/history were exact and only each new response coordinate has error <=sigma, the scalar error is <=sigma times this number. This is not a noisy acquisition theorem for the learned laws or old history.',
                    deterministic_worst_case_query_lower_bound=rank,
                    lower_bound_scope='Deterministic exact answers for every rational linear H in the unrestricted consistent-completion class, using rational full-vector forward queries. Extra structural or coefficient bit-size promises, source-code access, and randomized bounded-error algorithms are outside this lower bound.')

    def artifact(self):
        return dict(m=self.m, n=self.n, C=self.c, D=self.d,
                    all_inputs=self.inputs, all_outputs=self.outputs,
                    output_relation_rank=len(self.output_pivots), observed_input_rank=len(self.input_basis),
                    input_basis=self.input_basis, response_basis=self.response_basis,
                    N_columns=self.N_columns, T_rows=self.T_rows,
                    input_pivots=self.input_pivots, input_free=self.input_free,
                    output_pivots=self.output_pivots, output_free=self.output_free,
                    ambiguity_dimension=self.ambiguity_dimension,
                    input_factor=self.input_factor.artifact() if self.input_factor else None)


def load_partial_history(record):
    inputs = [[F(v) for v in f] for f in record['training_inputs']]
    outputs = [[F(v) for v in y] for y in record['training_responses']]
    for sample in record['certificate']['records']:
        inputs.append([F(v) for v in sample['input']])
        outputs.append([F(v) for v in sample['response']])
    c = [{int(j): F(v) for j, v in row.items()} for row in record['C_rows']]
    d = [{int(j): F(v) for j, v in row.items()} for row in record['D_rows']]
    return AcquiredKnowledge(record['m'], record['n'], c, d, inputs, outputs)


def run():
    root = Path(__file__).resolve().parent
    prior = json.loads((root/'acquired_relational_controls_results.json').read_text())
    record = prior['useful_partial_model']['acquisition']
    knowledge, load_ops = measured(lambda: load_partial_history(record))
    n, m = knowledge.n, knowledge.m
    v = [F(i+2, i+3) for i in range(n)]
    h = [[F(2) if j == 3 else F(0) for j in range(n)],
         v, [F((j+3)**2+1, j+5) for j in range(n)]]
    source = MatrixResponse(h)
    initial = knowledge.artifact()
    assert len(knowledge.inputs) == 7
    assert len(knowledge.input_basis) == 7
    for f, y in zip(knowledge.inputs, knowledge.outputs):
        assert knowledge.base_action(f) == y
    tasks = []
    # Different previously unspecified aggregate response functionals.
    weights = [[[F(((i+2)*(j+3)+5*task) % (13+task)-6, 7+task)
                 for j in range(n)] for i in range(m)] for task in range(2)]
    for task_id, w in enumerate(weights):
        before = knowledge.artifact()
        # Equally informed data-only comparison retains every same pair. It
        # may also adopt the acquired laws and tie the full learner exactly.
        data_only = AcquiredKnowledge(m, n, [], [], knowledge.inputs, knowledge.outputs)
        data_a = data_only.missing_coefficient(w)
        data_rank = RowBasis(len(data_a))
        for column in transpose(data_a):
            data_rank.add(column)
        result, ops = measured(lambda: knowledge.acquire_functional(source, w))
        expected = sum((dot(wrow, hrow) for wrow, hrow in zip(w, h)), F(0))
        assert expected == result['value']
        tasks.append(dict(task_id=task_id, result=result, arithmetic=ops,
                          prior_knowledge=before,
                          exact_dense_reference_value=expected,
                          same_history_data_only_missing_rank=len(data_rank.rows),
                          equally_informed_retainer_with_acquired_laws=result['additional_forward_queries']))
    # A new functional in the learned observable span needs no new experiment.
    final_weight = [[F(0)]*n for _ in range(m)]
    final_weight[0] = [F((3*j) % 11-5, 8) for j in range(n)]
    generic_final, generic_final_ops = measured(
        lambda: knowledge.acquire_functional(source, final_weight, allow_law_shortcut=False))
    final, final_ops = measured(lambda: knowledge.acquire_functional(source, final_weight))
    assert final['additional_forward_queries'] == 0
    assert final['value'] == sum((dot(a, b) for a, b in zip(final_weight, h)), F(0))
    assert final['value'] == generic_final['value']
    assert knowledge.ambiguity_dimension > 0
    # An actual completion witness: same old observations/laws, different
    # unqueried aggregate answer before acquisition. Fixed-transcript witness,
    # not a source allowed to adapt to the random certification probes.
    old = load_partial_history(record)
    a = old.missing_coefficient(weights[0])
    j = next(j for j in range(len(a[0])) if any(row[j] for row in a))
    avec = [row[j] for row in a]
    output_direction = [sum((v[k]*a0 for v, a0 in zip(old.N_columns, avec)), F(0)) for k in range(m)]
    input_row = old.T_rows[j]
    delta = [[u*v for v in input_row] for u in output_direction]
    assert not any(v for row in old.c for v in [dot(row, output_direction)])
    assert all(not any(matvec(delta, f)) for f in old.inputs)
    changed_functional = sum((dot(wrow, drow) for wrow, drow in zip(weights[0], delta)), F(0))
    assert changed_functional == dot(avec, avec) > 0
    # Preserve the first full-vector task response as well: with one of the
    # two planned queries, a nonzero alternative still changes the functional.
    first_query = tasks[0]['result']['records'][0]['input']
    transformed_first = matvec(old.T_rows, first_query)
    unresolved_directions = nullspace([transformed_first], len(old.T_rows))
    vmissing = next(v0 for v0 in unresolved_directions if any(matvec(a, v0)))
    amissing = matvec(a, vmissing)
    odir = [sum((col[i]*a0 for col, a0 in zip(old.N_columns, amissing)), F(0)) for i in range(m)]
    irow = [sum((z*t[j] for z, t in zip(vmissing, old.T_rows)), F(0)) for j in range(n)]
    after_one_delta = [[u*v0 for v0 in irow] for u in odir]
    assert all(not any(matvec(after_one_delta, f)) for f in old.inputs+[first_query])
    after_one_change = sum((dot(wr, dr) for wr, dr in zip(weights[0], after_one_delta)), F(0))
    assert after_one_change == dot(amissing, amissing) > 0
    result = dict(construction='Optimal marginal acquisition of new linear response functionals from learned laws and the complete retained interaction history',
                  initial_knowledge=initial, initialization_arithmetic=load_ops,
                  tasks=tasks, final_zero_query_task=final, final_zero_query_arithmetic=final_ops,
                  generic_zero_query_task=generic_final,
                  generic_zero_query_arithmetic=generic_final_ops,
                  final_knowledge=knowledge.artifact(), additional_source_cost=source.cost(),
                  ambiguity_witness=dict(output_direction=output_direction, input_row=input_row,
                                         preserves_all_prior_pairs_and_laws=True,
                                         changes_first_new_functional_by=changed_functional),
                  one_query_lower_bound_control=dict(output_direction=odir, input_row=irow,
                                                     preserves_prior_history_and_first_full_vector_task_response=True,
                                                     changes_requested_functional_by=after_one_change),
                  probability_accounting='Only the earlier acquired relation certificate is probabilistic. On its event all subsequent exact acquisition plans and answers are valid for adaptive tasks; no per-task probability charge.',
                  distinction='The data-only rank comparison does not handicap an informed retaining method: a retainer using the same learned C,D ties the optimal query count. The contribution is the obtainable representation and compiled strategy.')
    (root/'acquired_query_acquisition_results.json').write_text(json.dumps(encode(result), indent=2))
    print(json.dumps(dict(initial_ambiguity=initial['ambiguity_dimension'],
                          tasks=[dict(id=t['task_id'], queries=t['result']['additional_forward_queries'],
                                      same_history_without_law_rank=t['same_history_data_only_missing_rank'],
                                      with_law_retainer_queries=t['equally_informed_retainer_with_acquired_laws'],
                                      value=str(t['result']['value']),
                                      remaining_ambiguity=t['result']['ambiguity_dimension_after'],
                                      Fraction_ops=t['arithmetic']['total_Fraction_arithmetic_calls']) for t in tasks],
                          final_new_task_queries=final['additional_forward_queries'],
                          direct_law_zero_query_Fraction_ops=final_ops['total_Fraction_arithmetic_calls'],
                          generic_zero_query_Fraction_ops=generic_final_ops['total_Fraction_arithmetic_calls'],
                          final_ambiguity=knowledge.ambiguity_dimension,
                          total_additional_calls=source.calls), indent=2))
    return result


if __name__ == '__main__':
    run()
