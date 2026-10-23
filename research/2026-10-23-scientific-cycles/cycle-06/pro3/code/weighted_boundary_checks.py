#!/usr/bin/env python3
"""Frozen exact-rational diagnostics for the Cycle6 weighted boundary theorem.

Standard library only. No finite calculation proves the asymptotic theorem.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import resource
import time
import traceback


def identity(n):
    return [[F(int(i == j)) for j in range(n)] for i in range(n)]


def mm(a, b):
    return [[sum((a[i][k]*b[k][j] for k in range(len(b))), F(0))
             for j in range(len(b[0]))] for i in range(len(a))]


def vm(v, a):
    return [sum((v[i]*a[i][j] for i in range(len(v))), F(0))
            for j in range(len(a[0]))]


def power(a, n):
    z = identity(len(a))
    while n:
        if n & 1:
            z = mm(z, a)
        n //= 2
        if n:
            a = mm(a, a)
    return z


def add(a, b):
    return [x+y for x, y in zip(a, b)]


def tv(a, b):
    return sum((abs(x-y) for x, y in zip(a, b)), F(0))/2


def exact_ldl(a):
    n = len(a)
    assert all(a[i][j] == a[j][i] for i in range(n) for j in range(n))
    lower, diag = identity(n), []
    for j in range(n):
        pivot = a[j][j]-sum((lower[j][k]**2*diag[k] for k in range(j)), F(0))
        assert pivot > 0, ('nonpositive exact pivot', j, str(pivot))
        diag.append(pivot)
        for i in range(j+1, n):
            lower[i][j] = (a[i][j]-sum(
                (lower[i][k]*lower[j][k]*diag[k] for k in range(j)), F(0)))/pivot
    assert [[sum((lower[i][k]*diag[k]*lower[j][k] for k in range(n)), F(0))
             for j in range(n)] for i in range(n)] == a
    return diag


def native(q, pi, Q, screen_ratio, alpha):
    n = len(q)
    assert sum(q) == sum(pi) == 1 and min(q+pi) > 0
    assert all(sum(row) == 1 and min(row) >= 0 for row in Q)
    assert all(Q[i][j] == Q[j][i] for i in range(n) for j in range(n))
    W = [pi[i]/q[i] for i in range(n)]
    G, L = identity(n), identity(n)
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            G[i][j] = q[j]*min(F(1), W[j]/W[i])
            if Q[i][j]:
                r_eta = screen_ratio[i][j]
                assert r_eta > 0 and r_eta**2 == q[j]/q[i]
                L[i][j] = Q[i][j]*min(F(1), r_eta)*min(F(1), pi[j]/pi[i]/r_eta)
        G[i][i] = 1-sum(G[i][j] for j in range(n) if i != j)
        L[i][i] = 1-sum(L[i][j] for j in range(n) if i != j)
    C = [[(F(int(i == j))+alpha*G[i][j]+(1-alpha)*L[i][j])/2
          for j in range(n)] for i in range(n)]
    for P in [G, L, C]:
        assert all(sum(row) == 1 and min(row) >= 0 for row in P)
        assert all(pi[i]*P[i][j] == pi[j]*P[j][i]
                   for i in range(n) for j in range(n))
    return W, G, L, C


def absorbed(P, A, E):
    idx = A+E
    return idx, [[P[x][y] if x in A else F(int(x == y)) for y in idx] for x in idx]


def transform(P, idx, roots):
    return [[P[i][j]*F(roots[idx[i]], roots[idx[j]])
             for j in range(len(idx))] for i in range(len(idx))]


def full_return_check(q, C, A, B, n=16, N=5):
    size = len(q)
    living = [q[x] if x in A else F(0) for x in range(size)]
    initial_boundary = [q[x] if x in B else F(0) for x in range(size)]
    accounted = vm(initial_boundary, power(C, n))
    hit_masses = [sum(initial_boundary)]
    for j in range(1, N+1):
        move = vm(living, C)
        hit = [move[x] if x in B else F(0) for x in range(size)]
        living = [move[x] if x in A else F(0) for x in range(size)]
        accounted = add(accounted, vm(hit, power(C, n-j)))
        hit_masses.append(sum(hit))
    accounted = add(accounted, vm(living, power(C, n-N)))
    direct = vm(q, power(C, n))
    assert accounted == direct
    assert sum(hit_masses)+sum(living) == 1
    return {'n': n, 'N': N, 'hit_masses': hit_masses, 'residual_mass': sum(living),
            'direct_law': direct, 'exact_identity': True}


def weighted_checks():
    roots = [4, 3, 2, 1, 5, 6]
    q = [F(x*x, 91) for x in roots]
    pi = [F(x, 100) for x in [1, 1, 1, 2, 45, 50]]
    Q = [[F(0) for _ in roots] for _ in roots]
    for i in range(6):
        Q[i][i] = F(3, 8)
        Q[i][(i-1) % 6] = Q[i][(i+1) % 6] = F(1, 4)
        Q[i][(i+3) % 6] = F(1, 8)
    screen = [[F(roots[j], roots[i]) for j in range(6)] for i in range(6)]
    A, B = [0, 1, 2], [3, 4, 5]
    b = sum(q[x] for x in A)
    alphas = [F(1, 2), F(91, 153), F(3, 4), F(9, 10)]
    definitions = [(a, 'canonical') for a in alphas]+[(F(3, 4), 'r_b_plus_one')]
    cases, returns = [], []
    hit_count = 0
    for alpha, weight_kind in definitions:
        beta = 1-alpha
        r_b = alpha*(1-b)/beta
        boundary_weight = max(F(1), r_b) if weight_kind == 'canonical' else r_b+1
        delta = max(F(0), beta*boundary_weight-alpha*(1-b))
        W, G, L, C = native(q, pi, Q, screen, alpha)
        assert max(W) == F(91, 50) < 2
        assert [i for i in range(6) if W[i] < F(1, 2)] == A
        if weight_kind == 'canonical':
            returns.append({'alpha': alpha, **full_return_check(q, C, A, B)})
            assert delta == max(F(0), beta-alpha*(1-b))
        for mask in range(8):
            E = [B[i] for i in range(3) if mask & (1 << i)]
            e = sum((q[x] for x in E), F(0))
            idx, PE = absorbed(C, A, E)
            _, GE = absorbed(G, A, E)
            _, LE = absorbed(L, A, E)
            weights = [F(1) if x in A else boundary_weight for x in idx]
            assert all(sum(row) <= 1 and min(row) >= 0 for row in PE)
            assert all(PE[i][j] == (F(int(i == j))+alpha*GE[i][j]+beta*LE[i][j])/2
                       for i in range(len(idx)) for j in range(len(idx)))
            LM, PM = transform(LE, idx, roots), transform(PE, idx, roots)
            local_columns = [sum(LM[i][j] for i in range(len(idx))) for j in range(len(idx))]
            local_weighted_rows = [sum(weights[j]*LM[i][j] for j in range(len(idx)))
                                   for i in range(len(idx))]
            assert max(local_columns) <= 2
            assert all(local_weighted_rows[i] <= (1+boundary_weight if x in A else boundary_weight)
                       for i, x in enumerate(idx))
            global_columns = [sum(q[x]*GE[i][j]/q[y] for i, x in enumerate(idx))
                              for j, y in enumerate(idx)]
            global_weighted_rows = [sum(weights[j]*GE[i][j] for j in range(len(idx)))
                                    for i in range(len(idx))]
            for i, x in enumerate(idx):
                assert global_columns[i] <= (2*b if x in A else 1+b)
                if x in E:
                    assert global_columns[i] == 1+b
                assert global_weighted_rows[i] == (b+boundary_weight*e if x in A else boundary_weight)
            gamma = F(1, 2)+(1+delta+alpha*boundary_weight*e)  # p=2
            slack = [[gamma*weights[i]*int(i == j)-sum(
                (PM[i][k]*weights[k]*PM[j][k] for k in range(len(idx))), F(0))
                      for j in range(len(idx))] for i in range(len(idx))]
            pivots = exact_ldl(slack)
            hits = []
            for N in [1, 2, 5, 12]:
                initial = [q[x] if x in A else F(0) for x in idx]
                law = vm(initial, power(PE, N))
                actual = sum((law[i] for i, x in enumerate(idx) if x in E), F(0))
                living = [q[x] if x in A else F(0) for x in range(6)]
                independently_counted = F(0)
                for _ in range(N):
                    move = vm(living, C)
                    independently_counted += sum((move[x] for x in E), F(0))
                    living = [move[x] if x in A else F(0) for x in range(6)]
                assert actual == independently_counted
                squared_bound = b*e*gamma**N/boundary_weight
                assert actual**2 <= squared_bound
                hits.append({'N': N, 'actual_first_hit_mass': actual,
                             'squared_holder_bound': squared_bound, 'exact_identity': True})
                hit_count += 1
            cases.append({'alpha': alpha, 'weight_kind': weight_kind, 'r_b': r_b,
                          'boundary_weight': boundary_weight, 'delta': delta, 'E': E,
                          'gamma': gamma, 'positive_LDL_pivots': pivots,
                          'local_columns': local_columns, 'local_weighted_rows': local_weighted_rows,
                          'global_columns': global_columns, 'global_weighted_rows': global_weighted_rows,
                          'first_hit_checks': hits})
    inputs = {'q': q, 'pi': pi, 'Q': Q, 'eta': F(1, 2), 'p': 2, 'h': F(1, 2),
              'A': A, 'B': B, 'alphas': alphas, 'additional_weight': 'r_b+1 at alpha=3/4',
              'horizons': [1, 2, 5, 12], 'KL_admission': 'max W=91/50<2<exp(1)'}
    return inputs, {'energy_certificates': len(cases), 'first_hit_identities': hit_count,
                    'full_return_identities': len(returns), 'cases': cases, 'returns': returns}


def crossing_checks():
    b, p, m, ell_proxy, alpha = F(1, 4), F(1, 256), 16, 4, F(3, 4)
    e = p/(m*ell_proxy**2)
    q = [b, e, 1-b-e]
    pi = [p/m**2, p, 1-p-p/m**2]
    Q = [[F(0), F(1), F(0)], [F(1), F(0), F(0)], [F(0), F(0), F(1)]]
    screen = [[F(1) for _ in range(3)] for _ in range(3)]
    screen[0][1], screen[1][0] = F(1, 128), F(128)
    W, G, L, C = native(q, pi, Q, screen, alpha)
    assert W[0] < 1 < W[2] < W[1] == 256
    KL_rational_upper = 1/q[2]-1+8*p
    assert KL_rational_upper < 1
    sigma = F(1, 128)
    explicit_L = [[1-sigma, sigma, F(0)],
                  [sigma/m**2, 1-sigma/m**2, F(0)], [F(0), F(0), F(1)]]
    explicit_G = [[b, e, q[2]],
                  [pi[0]/W[1], 1-(1-p)/W[1], pi[2]/W[1]],
                  [pi[0]/W[2], e, 1-pi[0]/W[2]-e]]
    assert L == explicit_L and G == explicit_G
    f = (1-alpha)*sigma/2
    a, c = alpha*q[2]/2, f+alpha*e/2
    v = a+c
    leaf_escape = alpha*(1-p)/(2*m*ell_proxy**2)+f/m**2
    assert C[0][1] == c and C[0][2] == a and 1-C[0][0] == v
    assert 1-C[1][1] == leaf_escape
    checks = []
    for n in [8, 16, 32, 64]:
        law = vm(q, power(C, n))
        error = tv(law, pi)
        lower = b*c/v*(1-(1-v)**(n//2))*(1-leaf_escape)**n-p
        upper = 1-pi[2]+e+b*c/v+b*(1-v)**n
        assert lower <= error <= upper
        ordinary_law = vm(q, power(G, n))
        ordinary_error = tv(ordinary_law, pi)
        ordinary_lower, ordinary_upper = p-(n+1)*e, 1-pi[2]+e/(1-b)+b**(n+1)
        assert ordinary_lower <= ordinary_error <= ordinary_upper
        checks.append({'horizon': n, 'hybrid_TV': error, 'hybrid_lower': lower,
                       'hybrid_upper': upper, 'ordinary_TV': ordinary_error,
                       'ordinary_lower': ordinary_lower, 'ordinary_upper': ordinary_upper})
    inputs = {'q': q, 'pi': pi, 'Q': Q, 'alpha': alpha, 'eta': F(1, 2),
              'b': b, 'p': p, 'm': m, 'ell_proxy': ell_proxy, 'horizons': [8, 16, 32, 64],
              'scope': 'exact finite identity fixture, not an asymptotic-policy data point'}
    return inputs, {'native_formula_equalities': True, 'KL_rational_upper': KL_rational_upper,
                    'sigma': sigma, 'root_exit': v, 'leaf_escape': leaf_escape,
                    'hybrid_sandwiches': len(checks), 'ordinary_sandwiches': len(checks), 'checks': checks}


def serialize(x):
    if isinstance(x, F):
        return str(x)
    if isinstance(x, dict):
        return {str(k): serialize(v) for k, v in x.items()}
    if isinstance(x, (tuple, list)):
        return [serialize(v) for v in x]
    return x


def write_json(path, obj):
    path.write_text(json.dumps(serialize(obj), sort_keys=True, indent=2)+'\n')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output-dir', type=Path, required=True)
    args = ap.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    wall, cpu = time.perf_counter(), time.process_time()
    try:
        wa, wb = weighted_checks()
        ca, cb = crossing_checks()
        elapsed, process = time.perf_counter()-wall, time.process_time()-cpu
        inputs = {'weighted_boundary': wa, 'one_crossing': ca}
        result = {'status': 'PASS', 'arithmetic': 'exact fractions; no floating positivity',
                  'weighted_boundary': wb, 'one_crossing': cb,
                  'scope': 'finite identities and energy diagnostics; not proof of asymptotic limit'}
        write_json(args.output_dir/'EXACT_INPUTS.json', inputs)
        write_json(args.output_dir/'WEIGHTED_CHECKS.json', result)
        resources = {'wall_seconds': elapsed, 'cpu_seconds': process,
                     'peak_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                     'scope': 'diagnostic body excluding result serialization',
                     'inference_token_monetary_discovery_cost': 'unknown'}
        write_json(args.output_dir/'CHECK_RESOURCES.json', resources)
        output = {'status': 'PASS', 'energy_certificates': wb['energy_certificates'],
                  'first_hit_identities': wb['first_hit_identities'],
                  'full_return_identities': wb['full_return_identities'],
                  'one_crossing_sandwiches': cb['hybrid_sandwiches'],
                  'ordinary_sandwiches': cb['ordinary_sandwiches'], 'resources': resources,
                  'deterministic_sha256': {name: hashlib.sha256((args.output_dir/name).read_bytes()).hexdigest()
                      for name in ['EXACT_INPUTS.json', 'WEIGHTED_CHECKS.json']}}
        print(json.dumps(output, indent=2))
    except Exception:
        write_json(args.output_dir/'FAILED_CHECK.json', {'traceback': traceback.format_exc(),
                   'wall_seconds': time.perf_counter()-wall, 'cpu_seconds': time.process_time()-cpu})
        raise


if __name__ == '__main__':
    main()
