#!/usr/bin/env python3
"""Cycle7 exact-rational checks; standard library, no stochastic experiment.

Matrix utilities follow the unchanged Cycle6 diagnostic conventions. Native
proposal handling, reverse-Jensen checks and both asymmetric fixtures are new.
Finite PASS is a diagnostic, not proof of an asymptotic theorem.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as F
import hashlib
import json
from math import isqrt
from pathlib import Path
import resource
import time
import traceback


def ident(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]


def mm(a, b):
    return [[sum((a[i][k]*b[k][j] for k in range(len(b))), F(0))
             for j in range(len(b[0]))] for i in range(len(a))]


def vm(v, a):
    return [sum((v[i]*a[i][j] for i in range(len(v))), F(0))
            for j in range(len(a[0]))]


def power(a, n):
    out = ident(len(a))
    while n:
        if n & 1:
            out = mm(out, a)
        n //= 2
        if n:
            a = mm(a, a)
    return out


def tv(a, b):
    return sum((abs(x-y) for x, y in zip(a, b)), F(0))/2


def add(a, b):
    return [x+y for x, y in zip(a, b)]


def quarter_root(x):
    a, b = isqrt(isqrt(x.numerator)), isqrt(isqrt(x.denominator))
    assert F(a, b)**4 == x, ('not a rational fourth power', str(x))
    return F(a, b)


def sqrt_ratio(x):
    a, b = isqrt(x.numerator), isqrt(x.denominator)
    assert F(a, b)**2 == x
    return F(a, b)


def ldl(a):
    n = len(a)
    assert all(a[i][j] == a[j][i] for i in range(n) for j in range(n))
    lower, ds = ident(n), []
    for j in range(n):
        pivot = a[j][j]-sum((lower[j][k]**2*ds[k] for k in range(j)), F(0))
        assert pivot > 0, ('nonpositive rational LDL pivot', j, str(pivot))
        ds.append(pivot)
        for i in range(j+1, n):
            lower[i][j] = (a[i][j]-sum(
                (lower[i][k]*lower[j][k]*ds[k] for k in range(j)), F(0)))/pivot
    assert [[sum((lower[i][k]*ds[k]*lower[j][k] for k in range(n)), F(0))
             for j in range(n)] for i in range(n)] == a
    return ds


def energy_slack(T, input_coeff, output_weights):
    return [[input_coeff[i]*int(i == j)-sum(
        (T[i][k]*output_weights[k]*T[j][k] for k in range(len(T))), F(0))
             for j in range(len(T))] for i in range(len(T))]


def native(q, pi, Q, eta, alpha, kind='full'):
    n = len(q)
    assert sum(q) == sum(pi) == 1 and min(q+pi) > 0
    assert all(sum(row) == 1 and min(row) >= 0 for row in Q)
    assert all(bool(Q[i][j]) == bool(Q[j][i]) for i in range(n) for j in range(n))
    assert (eta*4).denominator == 1
    W = [pi[i]/q[i] for i in range(n)]
    G, L, acc, ratios = ident(n), ident(n), ident(n), ident(n)
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            G[i][j] = q[j]*min(F(1), W[j]/W[i])
            if Q[i][j]:
                rq, rp = q[j]*Q[j][i]/(q[i]*Q[i][j]), pi[j]*Q[j][i]/(pi[i]*Q[i][j])
                first_ratio = rq if kind == 'full' else q[j]/q[i]
                s = quarter_root(first_ratio)**int(4*eta)
                acc[i][j] = min(F(1), s)*min(F(1), rp/s)
                ratios[i][j] = rq
                L[i][j] = Q[i][j]*acc[i][j]
        G[i][i] = 1-sum(G[i][j] for j in range(n) if i != j)
        L[i][i] = 1-sum(L[i][j] for j in range(n) if i != j)
    C = [[(F(i == j)+alpha*G[i][j]+(1-alpha)*L[i][j])/2
          for j in range(n)] for i in range(n)]
    for P in [G, L, C]:
        assert all(sum(row) == 1 and min(row) >= 0 for row in P)
        assert all(pi[i]*P[i][j] == pi[j]*P[j][i]
                   for i in range(n) for j in range(n))
    return W, G, L, C, acc, ratios


def absorb(P, A, E):
    idx = A+E
    return idx, [[P[x][y] if x in A else F(x == y) for y in idx] for x in idx]


def transform(P, idx, q):
    return [[P[i][j]*sqrt_ratio(q[idx[i]]/q[idx[j]])
             for j in range(len(idx))] for i in range(len(idx))]


def full_return(q, C, A, B, n=10, N=3):
    size = len(q)
    alive = [q[x] if x in A else F(0) for x in range(size)]
    hit0 = [q[x] if x in B else F(0) for x in range(size)]
    accounted = vm(hit0, power(C, n))
    masses = [sum(hit0)]
    for j in range(1, N+1):
        move = vm(alive, C)
        hit = [move[x] if x in B else F(0) for x in range(size)]
        alive = [move[x] if x in A else F(0) for x in range(size)]
        accounted = add(accounted, vm(hit, power(C, n-j)))
        masses.append(sum(hit))
    accounted = add(accounted, vm(alive, power(C, n-N)))
    assert accounted == vm(q, power(C, n))
    assert sum(masses)+sum(alive) == 1
    return {'n': n, 'N': N, 'hit_masses': masses, 'residual': sum(alive),
            'full_original_return_identity': True}


def finite_energy(q, pi, Q, eta, alpha, w, A, E, horizons):
    b, e = sum(q[x] for x in A), sum((q[x] for x in E), F(0))
    W, G, L, C, acc, rq = native(q, pi, Q, eta, alpha)
    idx, PE = absorb(C, A, E)
    _, LE = absorb(L, A, E)
    _, GE = absorb(G, A, E)
    LM, PM = transform(LE, idx, q), transform(PE, idx, q)
    weights = [F(1) if x in A else w for x in idx]
    aux = [[(Q[y][x] if x in A else F(0)) if x != y else
            (L[x][x] if x in A else F(1)) for y in idx] for x in idx]
    auxcols = [sum(aux[i][j] for i in range(len(idx))) for j in range(len(idx))]
    assert max(auxcols) <= 2
    coeffs = [[LM[i][j]**2/aux[i][j] if aux[i][j] else F(0)
               for j in range(len(idx))] for i in range(len(idx))]
    assert all(aux[i][j] or LM[i][j] == 0
               for i in range(len(idx)) for j in range(len(idx)))
    for i, x in enumerate(idx):
        for j, y in enumerate(idx):
            if x in A and x != y and Q[x][y]:
                assert coeffs[i][j] == Q[x][y]*acc[x][y]**2/rq[x][y]
    if eta == F(1, 2):
        H = w
    else:
        assert eta == F(3, 4)
        H = F(4, 27)*w**3 if w <= F(3, 2) else w-1
    local_rows = [sum(weights[j]*coeffs[i][j] for j in range(len(idx)))
                  for i in range(len(idx))]
    assert all(local_rows[i] <= (1+H if x in A else w)
               for i, x in enumerate(idx))
    local_pivots = ldl(energy_slack(LM, [2*(1+H) if x in A else 2*w for x in idx], weights))
    gc = [sum(q[x]*GE[i][j]/q[y] for i, x in enumerate(idx))
          for j, y in enumerate(idx)]
    gr = [sum(weights[j]*GE[i][j] for j in range(len(idx))) for i in range(len(idx))]
    for i, x in enumerate(idx):
        assert gc[i] <= (2*b if x in A else 1+b)
        assert gr[i] == (b+w*e if x in A else w)
        if x in E:
            assert gc[i] == 1+b
    delta = max(F(0), (1-alpha)*H-alpha*(1-b))
    gamma = F(1, 2)+(1+delta+alpha*w*e)  # p=2
    pivots = ldl(energy_slack(PM, [gamma*z for z in weights], weights))
    assert all(PE[i][j] == (F(i == j)+alpha*GE[i][j]+(1-alpha)*LE[i][j])/2
               for i in range(len(idx)) for j in range(len(idx)))
    hits = []
    for N in horizons:
        initial = [q[x] if x in A else F(0) for x in idx]
        absorbed = vm(initial, power(PE, N))
        actual = sum((absorbed[i] for i, x in enumerate(idx) if x in E), F(0))
        alive = [q[x] if x in A else F(0) for x in range(len(q))]
        counted = F(0)
        for _ in range(N):
            move = vm(alive, C)
            counted += sum((move[x] for x in E), F(0))
            alive = [move[x] if x in A else F(0) for x in range(len(q))]
        assert actual == counted
        bound2 = b*e*gamma**N/w
        assert actual**2 <= bound2
        hits.append({'N': N, 'first_hit': actual, 'holder_squared': bound2})
    return {'eta': eta, 'alpha': alpha, 'w': w, 'E': E, 'H': H, 'delta': delta,
            'gamma': gamma, 'auxiliary_columns': auxcols, 'powered_weighted_local_rows': local_rows,
            'local_all_vector_LDL': local_pivots, 'mixture_all_vector_LDL': pivots,
            'global_density_columns': gc, 'global_weighted_rows': gr, 'hits': hits,
            'max_absorbed_local_counting_column': max(sum(LM[i][j] for i in range(len(idx)))
                                                     for j in range(len(idx)))}


def asymmetric_fixture():
    q = [F(i**4, 4676) for i in range(1, 8)]
    pi = [F(x, 6104) for x in [1, 1, 1, 1, 100, 1000, 5000]]
    Q = [[F(0) for _ in q] for _ in q]
    for i in range(1, 7):
        Q[i][0], Q[0][i] = F(1, 4), F(1, 64)
        j = 1+i % 6
        Q[i][j], Q[j][i] = F(1, 16), F(1, 256)
    for i in range(7):
        Q[i][i] = 1-sum(Q[i])
    W = [pi[i]/q[i] for i in range(7)]
    assert max(W) < 2
    A, B = [1, 2, 3, 4], [0, 5, 6]
    assert A == [i for i in range(7) if W[i] < F(1, 2)]
    qcols = [sum(Q[i][j] for i in range(7)) for j in range(7)]
    assert max(qcols) > 2
    assert F(1, 16)**6 != F(1, 256)**6  # cycle criterion: Q nonreversible
    b = sum(q[i] for i in A)
    canonical = max(F(1), 3*(1-b))
    definitions = [(F(1, 2), F(1, 2), F(1)), (F(1, 2), F(3, 4), canonical),
                   (F(1, 2), F(3, 4), canonical+1), (F(3, 4), F(1, 2), F(1)),
                   (F(3, 4), F(3, 4), F(4, 3)), (F(3, 4), F(3, 4), F(2))]
    cases, returns, done = [], [], set()
    for eta, alpha, w in definitions:
        if (eta, alpha) not in done:
            C = native(q, pi, Q, eta, alpha)[3]
            returns.append({'eta': eta, 'alpha': alpha, **full_return(q, C, A, B)})
            done.add((eta, alpha))
        for mask in range(8):
            E = [B[i] for i in range(3) if mask & (1 << i)]
            cases.append(finite_energy(q, pi, Q, eta, alpha, w, A, E, [1, 3, 7]))
    inputs = {'q': q, 'pi': pi, 'Q': Q, 'theta': F(1, 2), 'p': 2, 'h': F(1, 2),
              'A': A, 'B': B, 'cases': definitions, 'horizons': [1, 3, 7],
              'KL_admission': 'max(pi/q)<2<exp(1)', 'Q_counting_columns': qcols,
              'nonreversible_cycle_products': [F(1, 16)**6, F(1, 256)**6]}
    return inputs, {'cases': cases, 'returns': returns,
                    'local_all_vector_certificates': len(cases),
                    'mixture_all_vector_certificates': len(cases),
                    'first_hit_identities': 3*len(cases), 'full_return_identities': len(returns)}


def lump(P, blocks):
    out = []
    for block in blocks:
        rows = [[sum(P[x][y] for y in dst) for dst in blocks] for x in block]
        assert all(row == rows[0] for row in rows)
        out.append(rows[0])
    return out


def fanin_fixture():
    m, scale, b, alpha = 16, 2, F(1, 4), F(1, 2)
    e, p, t = b/m, F(1, scale), F(1, scale**3)
    q = [e]*17+[1-b-e]
    pi = [t/m]*16+[p, 1-p-t]
    Q = [[F(0) for _ in q] for _ in q]
    for i in range(m):
        Q[i][m], Q[m][i] = F(1), F(1, m)
    Q[-1][-1] = F(1)
    blocks = [list(range(m)), [m], [m+1]]
    ql, pil = [b, e, q[-1]], [t, p, pi[-1]]
    assert F(5, 2)+F(17, 47) < 3
    checks, ordinary = [], []
    for eta in [F(1, 4), F(1, 2)]:
        for kind in ['q_only', 'full']:
            W, G, L, C, _, _ = native(q, pi, Q, eta, alpha, kind)
            sigma = F(1) if kind == 'q_only' else quarter_root(F(1, m))**int(4*eta)
            GL, LL, CL = lump(G, blocks), lump(L, blocks), lump(C, blocks)
            assert LL == [[1-sigma, sigma, F(0)], [sigma/scale**2, 1-sigma/scale**2, F(0)],
                          [F(0), F(0), F(1)]]
            assert GL == [[b, e, q[-1]], [t/W[m], 1-(1-p)/W[m], pi[-1]/W[m]],
                          [t/W[-1], e, 1-t/W[-1]-e]]
            a, c = alpha*q[-1]/2, (alpha*e+(1-alpha)*sigma)/2
            v, dl = a+c, alpha*(1-p)/(2*W[m])+(1-alpha)*sigma/(2*scale**2)
            assert 1-CL[1][1] == dl
            law = q[:]
            for horizon in range(1, 17):
                law = vm(law, C)
                if horizon in [2, 4, 8, 16]:
                    quotient = vm(ql, power(CL, horizon))
                    assert [sum(law[i] for i in block) for block in blocks] == quotient
                    assert tv(law, pi) == tv(quotient, pil)
                    lower = b*c/v*(1-(1-v)**(horizon//2))*(1-dl)**horizon-p
                    upper = p+t+e+b*c/v+b*(1-v)**horizon
                    error = tv(law, pi)
                    assert lower <= error <= upper
                    checks.append({'eta': eta, 'kind': kind, 'horizon': horizon,
                                   'sigma': sigma, 'native_equals_quotient_TV': error,
                                   'lower': lower, 'upper': upper})
            if eta == F(1, 4) and kind == 'full':
                law = q[:]
                for horizon in range(1, 17):
                    law = vm(law, G)
                    if horizon in [2, 4, 8, 16]:
                        error = tv(law, pi)
                        lower, upper = p-(horizon+1)*e, p+t+e/(1-b)+b**(horizon+1)
                        assert lower <= error <= upper
                        ordinary.append({'horizon': horizon, 'TV': error, 'lower': lower, 'upper': upper})
    energy = finite_energy(q, pi, Q, F(1, 2), alpha, F(1), blocks[0], [m], [1, 3, 7])
    assert [i for i in range(len(q)) if pi[i]/q[i] < F(51, 100)] == blocks[0]
    assert energy['max_absorbed_local_counting_column'] == 5 > 2
    inputs = {'q': q, 'pi': pi, 'Q': Q, 'n_scale': scale, 'm': m, 'b': b,
              'alpha': alpha, 'etas': [F(1, 4), F(1, 2)], 'blocks': blocks, 'energy_h': F(51, 100),
              'horizons': [2, 4, 8, 16], 'KL_rational_upper': F(5, 2)+F(17, 47),
              'scope': '18 native states; exact finite identities, not asymptotic data'}
    return inputs, {'hybrid_native_lumping_and_sandwiches': checks, 'ordinary': ordinary,
                    'old_column_premise_counterexample_and_new_energy': energy}


def ser(x):
    if isinstance(x, F):
        return str(x)
    if isinstance(x, dict):
        return {str(k): ser(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [ser(v) for v in x]
    return x


def write(path, obj):
    path.write_text(json.dumps(ser(obj), sort_keys=True, indent=2)+'\n')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output-dir', required=True, type=Path)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    wall, cpu = time.perf_counter(), time.process_time()
    try:
        ai, ar = asymmetric_fixture()
        fi, fr = fanin_fixture()
        resources = {'wall_seconds': time.perf_counter()-wall, 'cpu_seconds': time.process_time()-cpu,
                     'peak_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                     'scope': 'diagnostic body excluding serialization; not discovery cost',
                     'inference_token_monetary_discovery_cost': 'unknown'}
        result = {'status': 'PASS', 'arithmetic': 'exact rational; no floating positivity',
                  'asymmetric_energy': ar, 'fanin': fr,
                  'scope': 'finite operator/lumping/first-hit checks; no inferred asymptotic limit'}
        write(args.output_dir/'EXACT_INPUTS.json', {'asymmetric_energy': ai, 'fanin': fi})
        write(args.output_dir/'RECIPROCAL_CHECKS.json', result)
        write(args.output_dir/'CHECK_RESOURCES.json', resources)
        print(json.dumps({'status': 'PASS', 'local_all_vector_certificates': 49,
                          'mixture_all_vector_certificates': 49, 'first_hit_identities': 147,
                          'full_return_identities': 4, 'native_lumping_and_hybrid_sandwiches': 16,
                          'ordinary_sandwiches': 4, 'old_counting_column_counterexample': '5>2',
                          'resources': resources,
                          'deterministic_sha256': {n: hashlib.sha256((args.output_dir/n).read_bytes()).hexdigest()
                              for n in ['EXACT_INPUTS.json', 'RECIPROCAL_CHECKS.json']}}, indent=2))
    except Exception:
        write(args.output_dir/'FAILED_CHECK.json', {'traceback': traceback.format_exc(),
                    'wall_seconds': time.perf_counter()-wall, 'cpu_seconds': time.process_time()-cpu})
        raise


if __name__ == '__main__':
    main()
