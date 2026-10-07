"""Owned bounded regularization fixture; all posterior arithmetic is rational.

The existing owned rational Jacobi core is imported without running its main.
The fixture is one admitted execution capped at 30 seconds in total. It checks
an endpoint rank-one n=2 target and a rank-three atomic n=6 target. It does not
prove the universal complexity theorem or expand another worker's code scope.
"""
from fractions import Fraction as F
from math import comb
from pathlib import Path
import datetime, importlib.util, json, signal, time

HERE = Path(__file__).resolve().parent
CORE = HERE.parent / "rational_jacobi.py"
spec = importlib.util.spec_from_file_location("owned_frozen_jacobi", CORE)
jacobi = importlib.util.module_from_spec(spec)
spec.loader.exec_module(jacobi)

def rank(A):
    A = [r[:] for r in A]
    nr, nc = len(A), len(A[0])
    r = 0
    for c in range(nc):
        p = next((i for i in range(r, nr) if A[i][c]), None)
        if p is None:
            continue
        A[r], A[p] = A[p], A[r]
        q = A[r][c]
        A[r] = [x / q for x in A[r]]
        for i in range(nr):
            if i != r and A[i][c]:
                q = A[i][c]
                A[i] = [x - q*y for x, y in zip(A[i], A[r])]
        r += 1
        if r == nr:
            break
    return r

def solve(A, b):
    n = len(A)
    M = [A[i][:] + [b[i]] for i in range(n)]
    for j in range(n):
        p = next(i for i in range(j, n) if M[i][j])
        M[j], M[p] = M[p], M[j]
        q = M[j][j]
        M[j] = [x / q for x in M[j]]
        for i in range(n):
            if i != j:
                q = M[i][j]
                M[i] = [x - q*y for x, y in zip(M[i], M[j])]
    return [row[-1] for row in M]

def inverse(A):
    n = len(A)
    cols = [solve(A, [F(int(i == j)) for i in range(n)]) for j in range(n)]
    return jacobi.tr(cols)

def positive_ldl(A):
    n = len(A)
    L = jacobi.ident(n)
    D = []
    for j in range(n):
        q = A[j][j] - sum((L[j][k]**2 * D[k] for k in range(j)), F(0))
        assert q > 0
        D.append(q)
        for i in range(j + 1, n):
            L[i][j] = (A[i][j] - sum((L[i][k]*L[j][k]*D[k] for k in range(j)), F(0))) / q
    return D

def approximate_cholesky(A, bits):
    n = len(A)
    L = [[F(0) for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(i + 1):
            q = A[i][j] - sum((L[i][k]*L[j][k] for k in range(j)), F(0))
            if i == j:
                assert q > 0
                lo, hi = jacobi.sqrt_dyadic_interval(q, bits)
                L[i][j] = (lo + hi) / 2
            else:
                L[i][j] = jacobi.round_dyadic(q / L[j][j], bits)
    assert L[0][0] == 1
    return L

def populations(n, nodes, weights):
    return [sum((w * comb(n, k) * x**k * (1-x)**(n-k)
                 for x, w in zip(nodes, weights)), F(0)) for k in range(n + 1)]

def fixture(n, atoms, epsilon, tau):
    start = time.monotonic()
    m, d = n // 2, n // 2 + 1
    eta = epsilon / 8
    u = [sum((w*x**l for x, w in atoms), F(0)) for l in range(n + 1)]
    assert u[0] == 1
    ur = [(1-eta)*u[l] + eta/F(l+1) for l in range(n + 1)]
    H0 = [[u[i+j] for j in range(d)] for i in range(d)]
    H = [[ur[i+j] for j in range(d)] for i in range(d)]
    oldrank = rank(H0)
    assert oldrank < d
    hpivots = positive_ldl(H)
    A = [[ur[i+j+1] for j in range(m)] for i in range(m)]
    v = [ur[i+m+1] for i in range(m)]
    s = sum((x*y for x, y in zip(v, solve(A, v))), F(0))
    K = [[ur[i+j+1] if (i, j) != (m, m) else s for j in range(d)] for i in range(d)]
    assert rank(K) == m
    positive_ldl([[H[i][j]-K[i][j] for j in range(d)] for i in range(d)])
    Lr = approximate_cholesky(H, 96)
    LL = jacobi.mm(Lr, jacobi.tr(Lr))
    # This exact support certificate protects the actual rounded factor.
    support = [[(1+tau)*LL[i][j]-K[i][j] for j in range(d)] for i in range(d)]
    support_pivots = positive_ldl(support)
    Linv = inverse(Lr)
    Jr = jacobi.mm(jacobi.mm(Linv, K), jacobi.tr(Linv))
    M = [[x/(1+tau) for x in row] for row in Jr]
    out = jacobi.diagonalize(M, tau)
    nodes = [out['T'][i][i] for i in range(d)]
    assert all(0 <= x <= 1 for x in nodes)
    endpoint = min(range(d), key=lambda i: nodes[i])
    assert nodes[endpoint] <= tau
    nodes[endpoint] = F(0)
    weights = out['weights']
    assert all(w >= 0 for w in weights) and sum(weights) == 1
    target = populations(n, [x for x, w in atoms], [w for x, w in atoms])
    regtarget = [(1-eta)*p + eta/F(n+1) for p in target]
    recovered = populations(n, nodes, weights)
    assert all(p >= 0 for p in recovered) and sum(recovered) == 1
    regerror = sum((abs(a-b) for a, b in zip(recovered, regtarget)), F(0))/2
    totalerror = sum((abs(a-b) for a, b in zip(recovered, target)), F(0))/2
    regularization_cost = sum((abs(a-b) for a, b in zip(regtarget, target)), F(0))/2
    assert regularization_cost <= eta
    assert regerror <= epsilon/8
    assert totalerror <= epsilon/4
    return {
        'n': n, 'atoms': [[str(x), str(w)] for x, w in atoms],
        'epsilon': str(epsilon), 'eta': str(eta), 'tau': str(tau),
        'original_gram_rank': oldrank, 'regularized_gram_rank': rank(H),
        'dimension': d, 'min_H_pivot': str(min(hpivots)),
        'min_support_pivot': str(min(support_pivots)),
        'nodes': [str(x) for x in nodes], 'weights': [str(w) for w in weights],
        'posterior_regularization_TD': str(regularization_cost),
        'posterior_quadrature_TD': str(regerror),
        'posterior_original_TD': str(totalerror),
        'posterior_original_TD_float_for_display': float(totalerror),
        'exact_positivity': True, 'exact_weight_sum': True,
        'exact_radau_endpoint0': True, 'posterior_budget_pass': True,
        'rotations': out['rotations'], 'refinements': out['refinements'],
        'max_output_bitlength': out['max_output_bitlength'],
        'seconds': time.monotonic() - start,
    }

class TimeCap(Exception):
    pass

def timeout(signum, frame):
    raise TimeCap('Admitted total 30-second fixture cap reached')

if __name__ == '__main__':
    admitted = time.monotonic()
    rows = []
    result = {
        'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'admitted_total_seconds': 30,
        'scope': 'two owned atomic regularization fixtures, exact rational posterior; no generic frontend or physical execution claim',
        'old_core': str(CORE), 'fixtures': rows,
    }
    signal.signal(signal.SIGALRM, timeout)
    signal.setitimer(signal.ITIMER_REAL, 30)
    try:
        for n, atoms in [(2, [(F(1, 2), F(1))]),
                         (6, [(F(0), F(1, 5)), (F(1, 3), F(1, 2)), (F(1), F(3, 10))])]:
            row = fixture(n, atoms, F(1, 8), F(1, 2**22))
            rows.append(row)
            print(json.dumps({k: row[k] for k in ['n', 'original_gram_rank', 'regularized_gram_rank', 'posterior_original_TD_float_for_display', 'rotations', 'seconds']}), flush=True)
        result['status'] = 'PASS'
        result['all_passed'] = True
    except Exception as err:
        result['status'] = type(err).__name__
        result['error'] = str(err)
        result['all_passed'] = False
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        result['total_seconds'] = time.monotonic() - admitted
        HERE.joinpath('atomic_fixture.json').write_text(json.dumps(result, indent=2))
        print(json.dumps({k: result[k] for k in ['status', 'all_passed', 'total_seconds']}), flush=True)
    if not result['all_passed']:
        raise SystemExit(1)
