"""Exact finite checks of the determinant-tail theorems.

All pass criteria are Fraction inequalities. Exponentials in Poisson tails
are enclosed by rational Taylor bounds. Auxiliary probabilities are algebra,
not a sensor model. No acquisition/LP algorithm is claimed as executed here.
"""
from fractions import Fraction as F
from math import comb, factorial
from pathlib import Path
import json
import random
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'p1_next' / 'code'))
from native_source import NativeSource, determinant, jsonable


def gram(factors):
    return [[sum((x*y for x, y in zip(a, b)), F(0))
             for b in factors] for a in factors]


def coefficients(b, g):
    n = len(g)
    den, num = {}, {}
    for mask in range(1 << n):
        s = [i for i in range(n) if mask >> i & 1]
        sub = [[b[i][j] for j in s] for i in s]
        augmented = [[b[i][j] + g[i]*g[j] for j in s] for i in s]
        den[mask] = determinant(sub)
        num[mask] = determinant(augmented) - den[mask]
        assert den[mask] >= 0 and num[mask] >= 0
    assert den[0] == 1 and num[0] == 0
    return den, num


def evaluate(coeff, u, degree=None):
    answer = F(0)
    for mask, value in coeff.items():
        if degree is not None and mask.bit_count() > degree:
            continue
        term = value
        for i, dose in enumerate(u):
            if mask >> i & 1:
                term *= dose
        answer += term
    return answer


def rational_hazard(q, r):
    if r == 0:
        return F(1)
    terms = [q**j / factorial(j) for j in range(r+1)]
    return terms[-1] / sum(terms, F(0))


def exponential_interval(q, minimum_degree=0):
    assert q >= 0
    if not q:
        return F(1), F(1)
    degree = max(minimum_degree, 96, 2*(q.numerator // q.denominator)+20)
    term = F(1)
    partial = term
    for j in range(1, degree+1):
        term *= q / j
        partial += term
    following = term*q/(degree+1)
    remainder = following/(1-q/(degree+2))
    return partial, partial+remainder


def poisson_tail_interval(q, k):
    if k == 0:
        return F(1), F(1)
    if not q:
        return F(0), F(0)
    lower, upper = exponential_interval(q, k-1)
    partial = sum((q**j/factorial(j) for j in range(k)), F(0))
    lo, hi = max(F(0), 1-partial/lower), min(F(1), 1-partial/upper)
    assert F(0) <= lo <= hi <= F(1)
    return lo, hi


def check_truncations(b, g, u, source=None):
    den, num = coefficients(b, g)
    d, a = evaluate(den, u), evaluate(num, u)
    value = a/d
    n = len(g)
    q = sum((u[i]*b[i][i] for i in range(n)), F(0))
    energy = sum((u[i]*g[i]*g[i] for i in range(n)), F(0))
    kappa = max(b[i][i] for i in range(n))
    G = max(map(abs, g))
    for mask in den:
        size = mask.bit_count()
        assert den[mask] <= kappa**size
        if size:
            assert num[mask] <= size*size*G*G*kappa**(size-1)
    if source is not None:
        raw = source.response(u)
        assert raw == source.independent_response(u)
        assert raw-F(3, 2)-source.c0 == value
    rows = []
    for r in range(n+1):
        dr, nr = evaluate(den, u, r), evaluate(num, u, r)
        approximation = nr/dr
        error = value-approximation
        hazard = rational_hazard(q, r)
        assert F(0) <= error <= value*hazard <= energy*hazard
        if r:
            assert value <= approximation/(1-hazard)
        if r == n:
            assert error == 0
        tail = poisson_tail_interval(q, r)
        # Checking against the LOWER endpoint is stronger than using the
        # computed enclosure's upper endpoint; only the analytic theorem is
        # claimed for all sources.
        assert error <= energy*tail[0]
        if hazard:
            assert hazard <= tail[0]
        assert F(0) <= (d-dr)/d <= poisson_tail_interval(q, r+1)[0]
        assert F(0) <= (a-nr)/d <= value*tail[0]
        rows.append({'degree': r, 'error': error, 'exact_rational_bound': energy*hazard,
                     'relative_rational_factor': hazard})
    return {'n': n, 'q_actual': q, 'energy_actual': energy, 'F': value,
            'truncations': rows}, den, num


def fresh_sources():
    rng = random.Random(108210901)
    fixtures = []
    checked = 0
    for n in range(1, 8):
        for variant in range(4):
            rank = variant
            scale = (F(0), F(1, 4), F(1), F(4))[variant]
            factors = [[scale*F(rng.randrange(-3, 4), 3) for _ in range(rank)]
                       for _ in range(n)]
            g = [F(rng.randrange(-5, 6), 5) for _ in range(n)]
            if n > 1:
                g[-1] = F(0) if variant % 2 == 0 else F(1, 10**7)
            b = gram(factors)
            source = NativeSource([[gi]+bi for gi, bi in zip(g, factors)], F(7, 8))
            weights = [rng.randrange(1, 10) for _ in range(n)]
            u = [F(w, 5*sum(weights)) for w in weights]
            result, _, _ = check_truncations(b, g, u, source)
            result.update({'variant': variant, 'rank_fixture': rank,
                           'signed_weak_or_dark_couplings': g})
            fixtures.append(result)
            checked += n+1
    return fixtures, checked


def large_diagonal_cases():
    rows = []
    for n in (20, 100):
        for q in (F(1, 5), F(1), F(4), F(16)):
            lam = q/n
            energy = F(1, 5)
            value = energy/(1+lam)
            for r in (1, 2, 4, 8, 12):
                dr = sum((F(comb(n, j))*lam**j for j in range(r+1)), F(0))
                nr = energy*sum((F(comb(n-1, j))*lam**j for j in range(r)), F(0))
                approximation = nr/dr
                error = value-approximation
                bound = value*rational_hazard(q, r)
                assert F(0) <= error <= bound
                assert error <= energy*poisson_tail_interval(q, r)[0]
                rows.append({'n': n, 'q': q, 'degree': r, 'error': error,
                             'relative_bound': bound,
                             'bound_fraction_used': error/bound if bound else F(0)})
    return rows


def projector_sharpness_cases():
    rows = []
    for n in (20, 100, 1000):
        for q in (F(1, 5), F(1), F(4)):
            lam = q/(n-1)
            for r in (1, 2, 4, 8, 12):
                terms = [F(comb(n-1, j))*lam**j for j in range(r+1)]
                fraction = terms[-1]/sum(terms, F(0))
                limiting_bound = rational_hazard(q, r)
                assert F(0) < fraction <= limiting_bound
                rows.append({'n': n, 'q': q, 'degree': r,
                             'exact_error_fraction': fraction,
                             'dimension_uniform_bound': limiting_bound,
                             'bound_fraction_used': fraction/limiting_bound})
    # A small rational Gram factor independently realizes the same family.
    for n in (3, 6):
        projection = [[F(int(i == j))-F(1, n) for j in range(n)] for i in range(n)]
        assert gram(projection) == projection
        g = [F(1)]*n
        source = NativeSource([[F(1)]+row for row in projection], F(1))
        result, _, _ = check_truncations(projection, g, [F(1, 5*n)]*n, source)
        assert result['F'] == F(1, 5)
    return rows


def path_sign_pair(m):
    g = [F(int(i in (0, m-1))) for i in range(m)]
    plus = [[F(int(i == j)) + (F(1, 4) if abs(i-j) == 1 else F(0))
             for j in range(m)] for i in range(m)]
    minus = [row[:] for row in plus]
    minus[-1][-2] = minus[-2][-1] = -F(1, 4)
    return plus, minus, g


def sparse_twins():
    rows = []
    for m in range(2, 9):
        k = m-1
        plus, minus, g = path_sign_pair(m)
        dp, np = coefficients(plus, g)
        dm, nm = coefficients(minus, g)
        # Exact coefficient equality on every proper support proves the
        # finite algebraic proper-support identity for these saved matrices.
        assert dp == dm
        full = (1 << m)-1
        for mask in range(full):
            assert np[mask] == nm[mask]
        assert np[full] != nm[full]
        t = F(1, 5*m)
        u = [t]*m
        fp = evaluate(np, u)/evaluate(dp, u)
        fm = evaluate(nm, u)/evaluate(dm, u)
        gap = abs(fp-fm)
        qsum = F(2, 5)
        tail = poisson_tail_interval(qsum, k)
        bound = max(fp, fm)*tail[0]
        assert gap > 0 and gap <= bound
        assert gap <= F(1, 5)*tail[0]
        expected = abs(4*(-1)**(m-1)*F(1, 4)**(m-1)*t**m/evaluate(dp, u))
        assert gap == expected
        old = F(1, 5)*F(1, 5)**k/(1+F(1, 5))
        rows.append({'m': m, 'support_order': k, 'gap_exact': gap,
                     'new_uniform_bound_interval': (F(1, 5)*tail[0], F(1, 5)*tail[1]),
                     'old_neumann_bound': old,
                     'new_upper_below_old': F(1, 5)*tail[1] < old})
    return rows


def wrong_poisson_guard():
    wrong = poisson_tail_interval(F(1, 2), 1)
    correct = poisson_tail_interval(F(1), 1)
    assert wrong[1] < F(1, 2) < correct[0]
    return {'Bernoulli_success_probability': F(1, 2),
            'false_mean_matched_Poisson_tail': wrong,
            'valid_lambda_trace_Poisson_tail': correct,
            'guard': 'Domination uses log(1+lambda), then trace, not sum p.'}


def ray_obstruction_check():
    plus = NativeSource([[F(1)], [F(0)], [F(1)], [F(0)]], F(1))
    minus = NativeSource([[F(0)], [F(1)], [F(0)], [F(1)]], F(1))
    checks = 0
    for edge in range(3):
        for dose in (F(0), F(1, 100), F(1, 10), F(1, 5)):
            u = [F(0)]*4
            u[edge] = u[edge+1] = dose/2
            assert plus.response(u) == minus.response(u) == F(5, 2)+dose/2
            checks += 1
    gap = plus.response([F(1, 5), F(0), F(0), F(0)])-minus.response([F(1, 5), F(0), F(0), F(0)])
    assert gap == F(1, 5)
    return {'finite_ray_amplitude_checks': checks, 'unseen_vertex_gap': gap,
            'scope': 'Finite illustration; arbitrary adaptive-query proof is in inference_ray_obstruction.md.'}


def main():
    fixtures, truncation_checks = fresh_sources()
    diagonal = large_diagonal_cases()
    sharpness = projector_sharpness_cases()
    twins = sparse_twins()
    result = {'status': 'passed',
              'scope': ('Exact finite algebra/source checks of determinant truncation '
                        'and sparse-twin bounds. No finite-noisy acquisition executed; '
                        'no physical or whole-proof audit claim.'),
              'fresh_source_fixtures': len(fixtures),
              'fresh_truncation_checks': truncation_checks,
              'large_diagonal_truncation_checks': len(diagonal),
              'projector_sharpness_checks': len(sharpness),
              'small_projector_native_source_fixtures': 2,
              'sparse_twin_cases': len(twins),
              'fixtures': fixtures, 'large_diagonal_cases': diagonal,
              'projector_sharpness_cases': sharpness,
              'sparse_twins': twins, 'invalid_domination_guard': wrong_poisson_guard(),
              'ray_obstruction': ray_obstruction_check()}
    path = Path(__file__).with_name('inference_determinant_tail_results.json')
    path.write_text(json.dumps(jsonable(result), indent=2)+'\n')
    print(json.dumps({'status': 'passed', 'fresh_fixtures': len(fixtures),
                      'fresh_truncations': truncation_checks,
                      'large_diagonal_truncations': len(diagonal),
                      'projector_sharpness_checks': len(sharpness),
                      'sparse_twins': len(twins), 'output': str(path)}, indent=2))


if __name__ == '__main__':
    main()
