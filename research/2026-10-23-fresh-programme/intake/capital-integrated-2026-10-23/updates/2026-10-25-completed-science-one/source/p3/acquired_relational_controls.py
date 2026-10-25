"""Meaningful failures and partial operations for acquired relation semantics."""
from fractions import Fraction as F
from pathlib import Path
import json
import random

from acquired_inverse_relations import (ModularFilter, SparseElimination, bits,
    dot, encode, eye, fit_exact_columns, matvec, sparse_apply, transpose)
from acquired_relational_semantics import acquire_presentation, compile_observation_query


class MatrixResponse:
    def __init__(self, h):
        self.h = h
        self.m, self.n = len(h), len(h[0])
        self.calls = 0
        self.max_input_bits = self.max_output_bits = 0
        self.max_input_amplitude = F(0)

    def apply(self, f):
        self.calls += 1
        self.max_input_bits = max(self.max_input_bits, bits(f))
        self.max_input_amplitude = max(self.max_input_amplitude, max(map(abs, f), default=F(0)))
        y = matvec(self.h, f)
        self.max_output_bits = max(self.max_output_bits, bits(y))
        return y

    def cost(self):
        return dict(native_forward_calls=self.calls, native_transpose_calls=0,
                    input_width=self.n, output_width=self.m,
                    returned_scalar_entries=self.calls*self.m,
                    maximum_input_rational_bit_length=self.max_input_bits,
                    maximum_output_rational_bit_length=self.max_output_bits,
                    maximum_input_absolute_coordinate=self.max_input_amplitude)


def run():
    # Low output rank alone does not obtain the input-facing functional.
    # More input directions than all seven retained acquisition observations;
    # the incomplete examples cannot secretly be fully tomographed by those data.
    input_dimension = 19
    v = [F(i+2, i+3) for i in range(input_dimension)]
    low = MatrixResponse([[a*x for x in v] for a in (F(1), F(2), F(3))])
    low_record, low_model = acquire_presentation(low, support_budget=2, seed=4101)
    assert low_model is None
    assert low_record['status'] == 'ACQUIRED_PARTIAL_PRESENTATION'
    assert low_record['output_row_rank'] == 2
    assert all(not row for row in low_record['D_rows'])
    unavailable = compile_observation_query(low_record, [{0: F(1)}])
    assert unavailable['status'] == 'UNKNOWN_OUTSIDE_ACQUIRED_OBSERVABLE_SPAN'
    # An incomplete model can nevertheless support nonzero new operations.
    h = [[F(2) if j == 3 else F(0) for j in range(input_dimension)],
         v, [F((j+3)**2+1, j+5) for j in range(input_dimension)]]
    partial = MatrixResponse(h)
    partial_record, partial_model = acquire_presentation(partial, support_budget=2, seed=4102)
    assert partial_model is None
    assert partial_record['status'] == 'ACQUIRED_PARTIAL_PRESENTATION'
    assert partial_record['output_row_rank'] == 1
    query = compile_observation_query(partial_record, [{0: F(3, 2)}])
    assert query['status'] == 'ACQUIRED_QUERY_ACTION'
    assert query['G_rows'] == [{3: F(3)}]
    rejected = compile_observation_query(partial_record, [{1: F(1)}])
    assert rejected['status'] == 'UNKNOWN_OUTSIDE_ACQUIRED_OBSERVABLE_SPAN'
    # New exact regularized control task on the acquired observable only.
    target, alpha = F(5, 7), F(1, 4)
    g = [query['G_rows'][0].get(j, F(0)) for j in range(input_dimension)]
    forcing = [a*target/(alpha+dot(g, g)) for a in g]
    observed = dot(g, forcing)
    gradient = [a*(observed-target)+alpha*f for a, f in zip(g, forcing)]
    assert not any(gradient)
    assert F(3, 2)*matvec(h, forcing)[0] == observed
    task = dict(target=target, regularizer=alpha, acquired_row=g,
                forcing=forcing, observable_response=observed,
                stationarity_exact=True, native_queries=0,
                other_outputs_not_reconstructed=True)
    # A modular support rank drop must not reject a true rational relation.
    prime = 2147483647
    columns = [[F(prime), F(2*prime)]]
    rhs = [F(1), F(2)]
    mod = ModularFilter(columns[0]+rhs, prime)
    minor = [[mod.cast(columns[0][i]), mod.cast(rhs[i])] for i in range(2)]
    assert not mod.nonsingular(minor)
    assert fit_exact_columns(columns, rhs) == [F(1, prime)]
    # General pivot/transpose tape checks, including permutations and fill.
    rng = random.Random(5150)
    matrices = 0
    right_hand_sides = 0
    for n in range(2, 8):
        for case in range(3):
            a = [[F(rng.randrange(-3, 4)) for _ in range(n)] for _ in range(n)]
            for i in range(n):
                a[i][i] += 10*n
            # Independent row/column permutations make symmetric pivoting insufficient.
            pr, pc = list(range(n)), list(range(n))
            rng.shuffle(pr)
            rng.shuffle(pc)
            a = [[a[i][j] for j in pc] for i in pr]
            factor = SparseElimination([{j: v for j, v in enumerate(row) if v} for row in a])
            for b in eye(n):
                assert matvec(a, factor.solve(b)) == b
                assert matvec(transpose(a), factor.solve_transpose(b)) == b
                right_hand_sides += 1
            matrices += 1
    singular_rejected = False
    try:
        SparseElimination([{0: F(1), 1: F(2)}, {0: F(2), 1: F(4)}])
    except ValueError:
        singular_rejected = True
    assert singular_rejected
    result = dict(low_rank_obstruction=dict(acquisition=low_record, attempted_query=unavailable,
                                           conclusion='Only output-null relations were acquired; the dense input-facing functional remains unobtained.'),
                  useful_partial_model=dict(acquisition=partial_record, available_query=query,
                                            unavailable_query=rejected, new_task=task),
                  modular_rank_drop_control=dict(prime=prime, fitted_coefficient=F(1, prime),
                                                 correctly_not_rejected=True),
                  elimination_controls=dict(matrices=matrices, basis_right_hand_sides=right_hand_sides,
                                            forward_and_transposed_residuals_exactly_zero=True,
                                            singular_matrix_rejected=singular_rejected))
    (Path(__file__).resolve().parent/'acquired_relational_controls_results.json').write_text(json.dumps(encode(result), indent=2))
    print(json.dumps(dict(low_rank_status=low_record['status'], acquired_output_rank=low_record['output_row_rank'],
                          low_rank_missing_operation=unavailable['status'],
                          useful_partial_status=partial_record['status'],
                          new_operation=query['status'], new_optimal_forcing=str(forcing[3]),
                          exact_matrix_controls=matrices, basis_right_hand_sides=right_hand_sides), indent=2))
    return result


if __name__ == '__main__':
    run()
