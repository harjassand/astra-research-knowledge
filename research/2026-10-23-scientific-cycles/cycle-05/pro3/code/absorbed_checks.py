#!/usr/bin/env python3
"""Exact, frozen checks of Cycle5's absorbed first-hit operation.

Python standard library only. These checks do not prove an asymptotic theorem.
"""
from __future__ import annotations
import argparse
from decimal import Decimal, localcontext
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import resource
import time


def ident(n):
    return [[F(int(i == j)) for j in range(n)] for i in range(n)]


def mm(a, b):
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), F(0))
             for j in range(len(b[0]))] for i in range(len(a))]


def vm(v, a):
    return [sum((v[i] * a[i][j] for i in range(len(v))), F(0))
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


def positive_ldl(a):
    """Exact LDL certificate; every pivot must be positive, no tolerance."""
    n = len(a)
    assert all(a[i][j] == a[j][i] for i in range(n) for j in range(n))
    lower = ident(n)
    diag = []
    for j in range(n):
        d = a[j][j] - sum((lower[j][k] ** 2 * diag[k] for k in range(j)), F(0))
        assert d > 0, ('nonpositive exact pivot', j, str(d))
        diag.append(d)
        for i in range(j + 1, n):
            lower[i][j] = (a[i][j] - sum(
                (lower[i][k] * lower[j][k] * diag[k] for k in range(j)), F(0))) / d
    reconstructed = [[sum((lower[i][k] * diag[k] * lower[j][k]
                           for k in range(n)), F(0)) for j in range(n)] for i in range(n)]
    assert reconstructed == a
    return diag


def native():
    roots = [4, 3, 2, 1, 5, 6]
    q = [F(a * a, 91) for a in roots]
    pi = [F(a, 100) for a in [1, 1, 1, 2, 45, 50]]
    w = [a / b for a, b in zip(pi, q)]
    Q = [[F(0) for _ in roots] for _ in roots]
    for x in range(6):
        Q[x][x] = F(3, 8)
        Q[x][(x + 1) % 6] = F(1, 4)
        Q[x][(x - 1) % 6] = F(1, 4)
        Q[x][(x + 3) % 6] = F(1, 8)
    G, L = ident(6), ident(6)
    for x in range(6):
        for y in range(6):
            if x == y:
                continue
            G[x][y] = q[y] * min(F(1), w[y] / w[x])
            r = q[y] / q[x]
            L[x][y] = Q[x][y] * min(F(1), r) * min(F(1), (pi[y] / pi[x]) / r)
        G[x][x] = 1 - sum(G[x][y] for y in range(6) if y != x)
        L[x][x] = 1 - sum(L[x][y] for y in range(6) if y != x)
    assert sum(q) == sum(pi) == 1 and min(q + pi) > 0
    assert max(w) == F(91, 50) < 2  # KL <= log(max W) < log 2 < 1.
    assert all(Q[x][y] == Q[y][x] for x in range(6) for y in range(6))
    for P in [Q, G, L]:
        assert all(sum(row) == 1 and min(row) >= 0 for row in P)
    for P in [G, L]:
        assert all(pi[x] * P[x][y] == pi[y] * P[y][x]
                   for x in range(6) for y in range(6))
    A = [i for i in range(6) if w[i] < F(1, 2)]
    B = [i for i in range(6) if i not in A]
    assert A == [0, 1, 2] and B == [3, 4, 5]
    return roots, q, pi, w, Q, G, L, A, B


def absorbed(P, A, E):
    idx = A + E
    out = [[(P[x][y] if x in A else F(int(x == y))) for y in idx] for x in idx]
    return idx, out


def transformed(P, idx, roots):
    # D_i/D_j = sqrt(q_i/q_j) = roots_i/roots_j exactly.
    return [[P[i][j] * F(roots[idx[i]], roots[idx[j]]) for j in range(len(idx))]
            for i in range(len(idx))]


def rationalize(x):
    if isinstance(x, F):
        return str(x)
    if isinstance(x, dict):
        return {str(k): rationalize(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [rationalize(v) for v in x]
    return x


def decimal_constants():
    with localcontext() as ctx:
        ctx.prec = 80
        one = Decimal(1)
        r0 = (-one).exp()
        lo, hi = Decimal('0.5'), Decimal('0.9')
        for _ in range(280):
            mid = (lo + hi) / 2
            value = mid * (((1-mid)/mid) * (1-mid).ln()).exp()
            if value < r0:
                lo = mid
            else:
                hi = mid
        c = (lo+hi)/2
        b = 1-r0
        offsets = [Decimal(-2), Decimal(-1), Decimal(0), Decimal(1)]
        return {'precision': 80, 'definition': 'F(c)=exp(-1), K=1, alpha=1/2',
                'c_star': str(c), 'reciprocal': str(1/c),
                'crossover_s': str(b.ln()/c),
                'critical_amplitudes': [{'s':str(s), 'amplitude':str(max(one,b*(-c*s).exp()))}
                                        for s in offsets],
                'status': 'Decimal illustrations; not interval or theorem certificates'}


def run():
    roots, q, pi, w, Q, G, L, A, B = native()
    b = sum(q[x] for x in A)
    cases = []
    identity_count = 0
    for alpha in [F(1, 2), F(1, 8)]:
        beta = 1-alpha
        C = [[(F(int(x == y)) + alpha*G[x][y] + beta*L[x][y])/2
              for y in range(6)] for x in range(6)]
        assert all(sum(row) == 1 and min(row) >= 0 for row in C)
        assert all(pi[x]*C[x][y] == pi[y]*C[y][x] for x in range(6) for y in range(6))
        delta = max(F(0), beta*F(1,4)-alpha*(1-b))
        CA = [[C[x][y] for y in A] for x in A]
        CAB = [[C[x][y] for y in B] for x in A]
        for mask in range(8):
            E = [B[i] for i in range(3) if mask & (1 << i)]
            e = sum((q[x] for x in E), F(0))
            idx, PE = absorbed(C, A, E)
            _, GE = absorbed(G, A, E)
            _, LE = absorbed(L, A, E)
            assert all(sum(row) <= 1 and min(row) >= 0 for row in PE)
            assert all(PE[i][j] == (F(int(i == j))+alpha*GE[i][j]+beta*LE[i][j])/2
                       for i in range(len(idx)) for j in range(len(idx)))
            LG = transformed(LE, idx, roots)
            PM = transformed(PE, idx, roots)
            local_rows = [sum(row) for row in LG]
            local_cols = [sum(LG[i][j] for i in range(len(idx))) for j in range(len(idx))]
            assert all(local_rows[i] <= (F(5,4) if x in A else F(1)) for i,x in enumerate(idx))
            assert max(local_cols) <= 2
            global_rows = [sum(row) for row in GE]
            global_cols = [sum(q[x]*GE[i][j]/q[y] for i,x in enumerate(idx)) for j,y in enumerate(idx)]
            for i,x in enumerate(idx):
                assert global_rows[i] == (b+e if x in A else 1)
                assert global_cols[i] <= (2*b if x in A else 1+b)
                if x in E:
                    assert global_cols[i] == 1+b
            gamma = F(1,2) + (1 + delta + alpha*e)  # p=2
            MMT = mm(PM, [list(row) for row in zip(*PM)])
            energy_slack = [[gamma*int(i==j)-MMT[i][j] for j in range(len(idx))]
                            for i in range(len(idx))]
            pivots = positive_ldl(energy_slack)
            horizons = []
            for N in [1,2,5,12]:
                start = [q[x] if x in A else F(0) for x in idx]
                final_absorbed = vm(start, power(PE,N))
                hit = sum((final_absorbed[i] for i,x in enumerate(idx) if x in E), F(0))
                survivor = [q[x] for x in A]
                independently_counted = F(0)
                for _ in range(N):
                    arrival_B = vm(survivor,CAB)
                    independently_counted += sum((arrival_B[B.index(y)] for y in E),F(0))
                    survivor = vm(survivor,CA)
                assert hit == independently_counted
                assert hit**2 <= b*e*gamma**N
                identity_count += 1
                horizons.append({'N':N,'first_hit_mass':hit,'squared_bound':b*e*gamma**N,
                                 'squared_margin':b*e*gamma**N-hit**2})
            cases.append({'alpha':alpha,'E':E,'b':b,'e':e,'Delta':delta,'Gamma':gamma,
                          'G_density_columns':global_cols,'G_row_masses':global_rows,
                          'L_transformed_rows':local_rows,'L_transformed_columns':local_cols,
                          'exact_LDL_positive_pivots':pivots,'horizons':horizons})
        # Independent full law vs first-hit decomposition with original full C after each hit.
        n,N = 16,5
        direct = vm(q,power(C,n))
        initial_B = [q[x] if x in B else F(0) for x in range(6)]
        reconstructed = vm(initial_B,power(C,n))
        survivor = [q[x] for x in A]
        for j in range(1,N+1):
            arrival = vm(survivor,CAB)
            full_arrival = [arrival[B.index(x)] if x in B else F(0) for x in range(6)]
            propagated = vm(full_arrival,power(C,n-j))
            reconstructed = [a+c for a,c in zip(reconstructed,propagated)]
            survivor = vm(survivor,CA)
        residual = [survivor[A.index(x)] if x in A else F(0) for x in range(6)]
        reconstructed = [a+c for a,c in zip(reconstructed,vm(residual,power(C,n-N)))]
        assert reconstructed == direct
        assert sum(direct) == 1
        cases.append({'alpha':alpha,'full_return_decomposition':{'n':n,'N':N,
                     'exact_equality':True,'direct_law':direct,'residual_mass':sum(residual)}})
    inputs={'q':q,'pi':pi,'W':w,'Q':Q,'G':G,'L_eta1':L,'A':A,'B':B,
            'h':F(1,2),'K':1,'eta':1,'c':F(1,2),'theta':F(1,2),'p':2,
            'admission':'max W=91/50<2<exp(1) => D(pi||q)<1',
            'alphas':[F(1,2),F(1,8)],'boundary_sets':'all eight subsets of B',
            'first_hit_horizons':[1,2,5,12]}
    result={'status':'all exact assertions passed',
            'absorption_identities':identity_count,'energy_PSD_certificates':16,
            'full_return_decompositions':2,'cases':cases,'constants':decimal_constants(),
            'limitations':'Finite algebra/identity diagnostics only. No asymptotic inference or sampler timing.'}
    return rationalize(inputs),rationalize(result)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--inputs',type=Path,required=True)
    parser.add_argument('--resources',type=Path,required=True)
    args=parser.parse_args()
    wall=time.perf_counter(); cpu=time.process_time()
    inputs,result=run()
    metrics={'wall_seconds':time.perf_counter()-wall,'cpu_seconds':time.process_time()-cpu,
             'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
             'body_scope':'native exact construction, checks, Decimal constants; excludes output writes',
             'active_inference_cost':'unknown','complete_discovery_cost':'unknown'}
    for path,data in [(args.inputs,inputs),(args.output,result),(args.resources,metrics)]:
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':result['status'],'metrics':metrics,
                      'output_bytes':args.output.stat().st_size,
                      'output_sha256':hashlib.sha256(args.output.read_bytes()).hexdigest()}))


if __name__=='__main__':
    main()
