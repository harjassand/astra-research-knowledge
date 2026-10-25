"""Acquire inverse balance equations from forward-only response interactions.

New research implementation, 2026-10-25. This file is standalone and uses exact
rational arithmetic. It assumes a fixed, square, linear response oracle. It
does not infer linearity, physical accessibility, or absence of measurement
noise. Unknown coordinate supports are searched; no chain ordering is supplied
to the learner. Ordinary sparse recovery and sparse elimination are legitimate
equally informed alternatives. See ACQUIRED_INVERSE_RELATIONS.md for proofs.
"""
from __future__ import annotations

from collections import Counter
from fractions import Fraction as F
from itertools import combinations
from math import comb
from pathlib import Path
import cProfile
import json
import random
import time


def dot(x, y):
    return sum((a*b for a, b in zip(x, y) if a and b), F(0))


def matvec(a, x):
    return [dot(row, x) for row in a]


def transpose(a):
    return [list(row) for row in zip(*a)]


def eye(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]


def sparse_apply(rows, x):
    return [sum((v*x[j] for j, v in row.items() if x[j]), F(0))
            for row in rows]


def dense(rows):
    n = len(rows)
    return [[row.get(j, F(0)) for j in range(n)] for row in rows]


def encode(x):
    if isinstance(x, F):
        return str(x)
    if isinstance(x, dict):
        return {str(k): encode(v) for k, v in x.items()}
    if isinstance(x, (tuple, list)):
        return [encode(v) for v in x]
    return x


def bits(values):
    return max((max(abs(x.numerator).bit_length(), x.denominator.bit_length())
                for x in values), default=0)


def measured(function):
    p = cProfile.Profile()
    start = time.perf_counter()
    p.enable()
    value = function()
    p.disable()
    counts = Counter()
    for entry in p.getstats():
        c = entry.code
        if (hasattr(c, 'co_filename') and c.co_filename.endswith('fractions.py')
                and c.co_name in ('_add', '_sub', '_mul', '_div')):
            counts[c.co_name] += entry.callcount
    return value, dict(Fraction_arithmetic_calls=dict(counts),
                      total_Fraction_arithmetic_calls=sum(counts.values()),
                      wall_seconds=time.perf_counter()-start,
                      exclusion='Integer modular arithmetic counted separately; gcd/bit operations, comparisons, storage and loop overhead not included in Fraction totals.')


class SparseElimination:
    """Complete-pivot sparse Gaussian elimination, retaining an executable tape.

    Markowitz fill heuristic; arbitrary nonsingular rational square matrices
    are allowed. The transpose solve is the reverse linear computation of the
    forward solve. Neither sparsity discovery nor elimination is claimed new.
    """
    def __init__(self, rows):
        self.n = len(rows)
        a = [{j: F(v) for j, v in row.items() if v} for row in rows]
        active_r = set(range(self.n))
        active_c = set(range(self.n))
        self.steps = []
        self.fill_entries_created = 0
        self.max_bits = bits(v for row in a for v in row.values())
        while active_r:
            col_count = Counter(j for i in active_r for j in a[i])
            candidates = [(max(0, len(a[i])-1)*max(0, col_count[j]-1),
                           len(a[i])+col_count[j], i != j, i, j)
                          for i in active_r for j in a[i]]
            if not candidates:
                raise ValueError('singular learned balance operator')
            _, _, _, r, c = min(candidates)
            pivot = a[r][c]
            tail = {j: v for j, v in a[r].items() if j != c}
            multipliers = {}
            for i in sorted(active_r-{r}):
                v = a[i].pop(c, F(0))
                if not v:
                    continue
                m = v/pivot
                multipliers[i] = m
                for j, u in tail.items():
                    old = a[i].get(j, F(0))
                    new = old-m*u
                    if new:
                        if not old:
                            self.fill_entries_created += 1
                        a[i][j] = new
                    else:
                        a[i].pop(j, None)
            self.steps.append(dict(row=r, column=c, pivot=pivot,
                                   tail=tail, multipliers=multipliers))
            self.max_bits = max(self.max_bits, bits(
                [pivot]+list(tail.values())+list(multipliers.values())))
            a[r] = {}
            active_r.remove(r)
            active_c.remove(c)
        self.calls = Counter()

    def solve(self, b):
        self.calls['solve'] += 1
        work = [F(v) for v in b]
        rhs = []
        for step in self.steps:
            u = work[step['row']]
            rhs.append(u)
            for i, m in step['multipliers'].items():
                work[i] -= m*u
        x = [F(0)]*self.n
        for step, u in zip(reversed(self.steps), reversed(rhs)):
            x[step['column']] = (u-sum((v*x[j] for j, v in step['tail'].items()), F(0)))/step['pivot']
        return x

    def solve_transpose(self, z):
        self.calls['solve_transpose'] += 1
        adjoint_x = [F(v) for v in z]
        adjoint_rhs = []
        for step in self.steps:
            w = adjoint_x[step['column']]/step['pivot']
            adjoint_rhs.append(w)
            for j, v in step['tail'].items():
                adjoint_x[j] -= v*w
        out = [F(0)]*self.n
        for step, w in zip(reversed(self.steps), reversed(adjoint_rhs)):
            out[step['row']] = w-sum((m*out[i] for i, m in step['multipliers'].items()), F(0))
        return out

    def artifact(self):
        return dict(n=self.n, steps=self.steps,
                    fill_entries_created=self.fill_entries_created,
                    retained_scalar_count=sum(1+len(s['tail'])+len(s['multipliers']) for s in self.steps),
                    maximum_factor_bit_length=self.max_bits,
                    method='Complete pivot Gaussian elimination; Markowitz ordering computed from learned entries.')

    @classmethod
    def load(cls, artifact):
        obj = cls.__new__(cls)
        obj.n = artifact['n']
        obj.steps = []
        for s in artifact['steps']:
            obj.steps.append(dict(row=int(s['row']), column=int(s['column']),
                                  pivot=F(s['pivot']),
                                  tail={int(j): F(v) for j, v in s['tail'].items()},
                                  multipliers={int(j): F(v) for j, v in s['multipliers'].items()}))
        obj.fill_entries_created = artifact['fill_entries_created']
        obj.max_bits = artifact['maximum_factor_bit_length']
        obj.calls = Counter()
        return obj


class ForwardBalanceSource:
    """Supplied nonreciprocal local balance model, exposing ONLY H=A^{-1}.

    Exact software control, not experimental discovery of a physical network.
    The learner only calls n/apply/cost. The reference rows are exposed solely
    to independent controls and the full-source incumbent.
    """
    def __init__(self, n=32, seed=814, parameter=F(0)):
        self.n = n
        rng = random.Random(seed)
        self.permutation = list(range(n))
        rng.shuffle(self.permutation)
        parameter = F(parameter)
        self.lower = [-F(2+i % 5, 7)*(1+parameter/2) for i in range(n-1)]
        self.upper = [-F(1+(3*i) % 7, 11)*(1-parameter/3) for i in range(n-1)]
        self.diag = [F(1)+parameter**2+(abs(self.lower[i-1]) if i else 0)
                     +(abs(self.upper[i]) if i < n-1 else 0) for i in range(n)]
        self.pivots = list(self.diag)
        self.multipliers = []
        for i in range(1, n):
            m = self.lower[i-1]/self.pivots[i-1]
            self.multipliers.append(m)
            self.pivots[i] -= m*self.upper[i-1]
        self.calls = 0
        self.max_bits = 0
        self.max_input_bits = 0

    def _solve(self, forcing):
        b = [forcing[self.permutation[i]] for i in range(self.n)]
        for i in range(1, self.n):
            b[i] -= self.multipliers[i-1]*b[i-1]
        b[-1] /= self.pivots[-1]
        for i in reversed(range(self.n-1)):
            b[i] = (b[i]-self.upper[i]*b[i+1])/self.pivots[i]
        out = [F(0)]*self.n
        for i, j in enumerate(self.permutation):
            out[j] = b[i]
        return out

    def apply(self, forcing):
        self.calls += 1
        self.max_input_bits = max(self.max_input_bits, bits(forcing))
        out = self._solve(forcing)
        self.max_bits = max(self.max_bits, bits(out))
        return out

    def reference_rows(self):
        rows = [{} for _ in range(self.n)]
        for i, j in enumerate(self.permutation):
            rows[j][j] = self.diag[i]
            if i:
                rows[j][self.permutation[i-1]] = self.lower[i-1]
            if i < self.n-1:
                rows[j][self.permutation[i+1]] = self.upper[i]
        return rows

    def cost(self):
        return dict(native_forward_calls=self.calls, transpose_calls=0,
                    vector_width=self.n, returned_scalar_entries=self.calls*self.n,
                    maximum_input_rational_bit_length=self.max_input_bits,
                    maximum_output_rational_bit_length=self.max_bits)


def fit_exact_columns(columns, target):
    """Solve overdetermined Xc=target exactly; None if inconsistent/dependent."""
    k, q = len(columns), len(target)
    a = [[columns[j][i] for j in range(k)]+[target[i]] for i in range(q)]
    r = 0
    for j in range(k):
        p = next((i for i in range(r, q) if a[i][j]), None)
        if p is None:
            return None
        a[r], a[p] = a[p], a[r]
        v = a[r][j]
        a[r] = [z/v for z in a[r]]
        for i in range(q):
            if i != r and a[i][j]:
                v = a[i][j]
                a[i] = [z-v*w for z, w in zip(a[i], a[r])]
        r += 1
    if any(row[-1] for row in a[r:]):
        return None
    return [a[j][-1] for j in range(k)]


class ModularFilter:
    """Nonzero (k+1)-minor rules out k-column rational fit; no false rejection.

    Modular rank comparison alone would be UNSOUND when support rank drops
    modulo p. We use an augmented minor of size strictly greater than k.
    Zero minors go to exact rational fitting. Denominator invertibility checked.
    """
    def __init__(self, observations, prime=2147483647):
        self.prime = prime
        self.counts = Counter()
        for v in observations:
            if v.denominator % prime == 0:
                raise ValueError('choose another prime: observed denominator vanishes')

    def cast(self, x):
        self.counts['field_inverse'] += 1
        self.counts['field_multiply'] += 1
        return (x.numerator % self.prime)*pow(x.denominator, -1, self.prime) % self.prime

    def nonsingular(self, a):
        a = [list(row) for row in a]
        n, p = len(a), self.prime
        for j in range(n):
            r = next((i for i in range(j, n) if a[i][j] % p), None)
            if r is None:
                return False
            a[r], a[j] = a[j], a[r]
            if j+1 == n:
                return True
            pinv = pow(a[j][j], -1, p)
            self.counts['field_inverse'] += 1
            for i in range(j+1, n):
                if not a[i][j]:
                    continue
                m = a[i][j]*pinv % p
                self.counts['field_multiply'] += 1
                for h in range(j+1, n):
                    a[i][h] = (a[i][h]-m*a[j][h]) % p
                    self.counts['field_multiply'] += 1
                    self.counts['field_subtract'] += 1
        return True


def validate_inverse(source, rows, *, seed=719, probes=5, alphabet=257):
    rng = random.Random(seed)
    records = []
    for _ in range(probes):
        f = [F(rng.randrange(alphabet)-alphabet//2, alphabet) for _ in range(source.n)]
        y = source.apply(f)
        residual = [a-b for a, b in zip(sparse_apply(rows, y), f)]
        records.append(dict(forcing=f, response=y, residual=residual))
        if any(residual):
            return dict(status='COUNTEREXAMPLE', records=records,
                        candidate_frozen_before_probes=True), False
    return dict(status='ACCEPTED_RANDOMIZED_IDENTITY', records=records,
                candidate_frozen_before_probes=True, alphabet=alphabet,
                probes=probes, fixed_candidate_false_accept_bound=F(1, alphabet**probes)), True


def acquire_sparse_inverse(source, max_support=3, *, seed=711,
                           alphabet=2**61, validation_probes=5):
    rng = random.Random(seed)
    n = source.n
    forcings, responses = [], []
    rejected = [set() for _ in range(n)]
    fitted = [None]*n
    stages = []
    statistics = Counter()
    validation_attempts = 0
    for budget in range(1, max_support+1):
        # One extra experiment beyond the largest fitted row support prevents
        # generic interpolation by arbitrary equally sized wrong supports.
        while len(forcings) < budget+1:
            f = [F(rng.randrange(alphabet)-alphabet//2, alphabet) for _ in range(n)]
            forcings.append(f)
            responses.append(source.apply(f))
        yrows, frows = transpose(responses), transpose(forcings)
        mod = ModularFilter([v for row in yrows+frows for v in row])
        ym = [[mod.cast(v) for v in row] for row in yrows]
        fm = [[mod.cast(v) for v in row] for row in frows]
        stage_start = Counter(statistics)
        for i in range(n):
            if fitted[i] is not None:
                pred = [sum((a*yrows[j][t] for j, a in fitted[i].items()), F(0))
                        for t in range(len(forcings))]
                if pred == frows[i]:
                    continue
                rejected[i].add(tuple(sorted(fitted[i])))
                fitted[i] = None
            for k in range(1, budget+1):
                for support in combinations(range(n), k):
                    if support in rejected[i]:
                        continue
                    statistics['supports_examined'] += 1
                    minor = [[ym[j][t] for j in support]+[fm[i][t]] for t in range(k+1)]
                    if mod.nonsingular(minor):
                        rejected[i].add(support)
                        statistics['certified_modular_rejections'] += 1
                        continue
                    statistics['exact_fits_attempted'] += 1
                    coefficients = fit_exact_columns([yrows[j] for j in support], frows[i])
                    if coefficients is None:
                        # A rank-deficient fit may become identifiable after a
                        # later experiment. Do not cache it as an impossible support.
                        statistics['exact_rejections'] += 1
                        continue
                    fitted[i] = {j: c for j, c in zip(support, coefficients) if c}
                    break
                if fitted[i] is not None:
                    break
        statistics.update(mod.counts)
        stages.append(dict(support_budget=budget, training_queries=len(forcings),
                           fitted_rows=sum(v is not None for v in fitted),
                           stage_statistics=dict(statistics-stage_start)))
        if all(row is not None for row in fitted):
            validation_attempts += 1
            cert, accepted = validate_inverse(source, fitted, seed=seed+101+validation_attempts,
                                             probes=validation_probes+validation_attempts-1)
            stages[-1]['validation'] = cert
            if accepted:
                return dict(status='ACQUIRED_INVERSE_EQUATIONS', n=n,
                            rows=fitted, training_forcings=forcings, training_responses=responses,
                            stages=stages, statistics=dict(statistics),
                            certificate=cert, source_cost=source.cost(),
                            adaptive_validation_false_accept_budget=F(257, 256*257**validation_probes),
                            training_input_alphabet=alphabet,
                            generic_acquisition_failure_union_bound=min(F(1), F(n*sum((k+1)*comb(n, k) for k in range(1, budget+1)), alphabet)),
                            finding_assumption='For high-probability acquisition: fixed invertible source with inverse rows at most this support budget. Certificate soundness does not require that promise.'), fitted
            for rec in cert['records']:
                forcings.append(rec['forcing'])
                responses.append(rec['response'])
        # If no candidate fits, increasing the budget is a computational choice;
        # it is NOT a proof that the source has no other useful representation.
    return dict(status='NO_INVERSE_IN_SEARCH_BUDGET', n=n, rows=fitted,
                training_forcings=forcings, training_responses=responses,
                stages=stages, statistics=dict(statistics), source_cost=source.cost()), None


def run():
    n = 32
    source = ForwardBalanceSource(n)
    (record, rows), acquisition_ops = measured(lambda: acquire_sparse_inverse(source))
    assert rows is not None
    acquisition_cost = source.cost()
    assert rows == source.reference_rows()
    factor, factor_ops = measured(lambda: SparseElimination(rows))
    artifact = factor.artifact()
    loaded = SparseElimination.load(encode(artifact))
    new_vectors = [[F(((i+3)*(k+5)) % 19-9, 7+k) for i in range(n)] for k in range(2)]
    operations = []
    for k, z in enumerate(new_vectors):
        forward, forward_ops = measured(lambda: loaded.solve(z))
        adjoint, adjoint_ops = measured(lambda: loaded.solve_transpose(z))
        assert sparse_apply(rows, forward) == z
        assert matvec(transpose(dense(rows)), adjoint) == z
        operations.append(dict(task_id=k, input=z, forward=forward, adjoint=adjoint,
                               forward_arithmetic=forward_ops, adjoint_arithmetic=adjoint_ops,
                               forward_and_transpose_balance_residuals_exactly_zero=True,
                               native_calls_after_reload=0))
    # Matched native API, including full vector width: dense forward tomography.
    tomography_source = ForwardBalanceSource(n)
    h, tomography_ops = measured(lambda: transpose([tomography_source.apply(v) for v in eye(n)]))
    dense_adjoint, dense_adjoint_ops = measured(lambda: matvec(transpose(h), new_vectors[0]))
    assert dense_adjoint == operations[0]['adjoint']
    assert all(v for row in h for v in row)
    # A source-aware incumbent gets the supplied local equations immediately.
    source_factor, source_factor_ops = measured(lambda: SparseElimination(source.reference_rows()))
    assert source_factor.solve_transpose(new_vectors[1]) == operations[1]['adjoint']
    # Failure of identification with one experiment: two different inverse
    # operators, both 1-sparse per row, fit exactly the same all-ones pair.
    ambiguity = dict(forcing=[F(1), F(1)], response=[F(1), F(1)],
                     inverses=[eye(2), [[F(0), F(1)], [F(1), F(0)]]])
    for a in ambiguity['inverses']:
        assert matvec(a, ambiguity['response']) == ambiguity['forcing']
    # A training-only model can interpolate a poorly exciting observation.
    f = [F(1)]*n
    y = source._solve(f)
    wrong = [{i: f[i]/y[i]} for i in range(n)]
    assert sparse_apply(wrong, y) == f
    poor_source = ForwardBalanceSource(n)
    poor_cert, poor_pass = validate_inverse(poor_source, wrong, seed=512)
    assert not poor_pass
    # General complete pivot control: no nonzero diagonal is required.
    offdiag = [{1: F(2)}, {0: F(3)}]
    off = SparseElimination(offdiag)
    assert off.solve([F(5), F(7)]) == [F(7, 3), F(5, 2)]
    assert off.solve_transpose([F(5), F(7)]) == [F(7, 2), F(5, 3)]
    result = dict(construction='Unknown-support inverse equations from exact forward responses',
                  source_scope='Supplied exact nonreciprocal permuted nearest-neighbour balance software. Full-state forcing and readout. Not physical evidence.',
                  acquisition=record, acquisition_arithmetic=acquisition_ops,
                  learned_equations_match_reference=True,
                  elimination_tape=artifact, factorization_arithmetic=factor_ops,
                  new_task_operations=operations,
                  tomography=dict(source_cost=tomography_source.cost(), arithmetic=tomography_ops,
                                  stored_dense_scalars=n*n, first_new_adjoint_arithmetic=dense_adjoint_ops,
                                  exact_same_answer=True),
                  source_aware_incumbent=dict(native_learning_queries=0,
                                             factorization_arithmetic=source_factor_ops,
                                             same_sparse_solver_and_adjoint=True),
                  controls=dict(one_query_ambiguity=ambiguity,
                                training_fit_fresh_identity_failure=poor_cert,
                                complete_pivot_zero_diagonal_control=True),
                  retained_structure=dict(equation_nonzeros=sum(len(row) for row in rows),
                                          factor_scalars=artifact['retained_scalar_count'],
                                          native_source_cost_frozen=acquisition_cost),
                  limitations=['Exhaustive support search is combinatorial, not an efficient general sparse recovery algorithm.',
                               'Native vector width, exact precision, modular work, acquisition and factor construction are charged.',
                               'Full source access supplies equations directly; no discovery advantage claimed against that incumbent.',
                               'Elimination and transposed solve generation are established algorithms, not a newly invented algebraic solver.'])
    path = Path(__file__).resolve().parent/'acquired_inverse_relations_results.json'
    path.write_text(json.dumps(encode(result), indent=2))
    print(json.dumps(dict(status=record['status'], source_cost=acquisition_cost,
                          supports_examined=record['statistics']['supports_examined'],
                          exact_fits=record['statistics']['exact_fits_attempted'],
                          Fraction_operations=acquisition_ops['total_Fraction_arithmetic_calls'],
                          modular_operations={k: v for k, v in record['statistics'].items() if k.startswith('field_')},
                          factor_scalars=artifact['retained_scalar_count'],
                          fill=artifact['fill_entries_created'],
                          adjoint_Fraction_operations=operations[0]['adjoint_arithmetic']['total_Fraction_arithmetic_calls'],
                          dense_adjoint_Fraction_operations=dense_adjoint_ops['total_Fraction_arithmetic_calls']), indent=2))
    return result


if __name__ == '__main__':
    run()
