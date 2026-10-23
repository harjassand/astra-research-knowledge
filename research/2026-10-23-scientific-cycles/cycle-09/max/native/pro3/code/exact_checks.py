#!/usr/bin/env python3
"""Cycle8 exact native checks. Standard library only; no simulations.

Matrix utility conventions descend from Cycle7 reciprocal_checks.py.
The distorted scalar envelope, current fixtures, moving-mismatch geometry,
and bounded-asymmetry checks are new. Finite PASS is not an asymptotic proof.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as F
import hashlib
import itertools
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


def rational_power(x, exponent):
    exponent = F(exponent)
    if exponent.denominator == 1:
        return x**exponent.numerator
    assert exponent.denominator in (2, 4)
    a, b = isqrt(x.numerator), isqrt(x.denominator)
    if exponent.denominator == 4:
        a, b = isqrt(a), isqrt(b)
    root = F(a, b)
    assert root**exponent.denominator == x, ('not an exact rational root', x, exponent)
    return root**exponent.numerator


def ldl(a):
    size = len(a)
    assert all(a[i][j] == a[j][i] for i in range(size) for j in range(size))
    low, ds = ident(size), []
    for j in range(size):
        pivot = a[j][j]-sum((low[j][k]**2*ds[k] for k in range(j)), F(0))
        assert pivot > 0, ('nonpositive exact LDL pivot', j, pivot)
        ds.append(pivot)
        for i in range(j+1, size):
            low[i][j] = (a[i][j]-sum(
                (low[i][k]*low[j][k]*ds[k] for k in range(j)), F(0)))/pivot
    assert [[sum((low[i][k]*ds[k]*low[j][k] for k in range(size)), F(0))
             for j in range(size)] for i in range(size)] == a
    return ds


def energy_slack(T, input_coeff, output_weight):
    return [[input_coeff[i]*int(i == j)-sum(
        (T[i][k]*output_weight[k]*T[j][k] for k in range(len(T))), F(0))
        for j in range(len(T))] for i in range(len(T))]


def native(q, pi, Q, eta, kappa, alpha):
    size = len(q)
    assert sum(q) == sum(pi) == 1 and min(q+pi) > 0
    assert all(sum(row) == 1 and min(row) >= 0 for row in Q)
    assert all(bool(Q[i][j]) == bool(Q[j][i])
               for i in range(size) for j in range(size))
    W = [pi[i]/q[i] for i in range(size)]
    G, L, acc, rq, screens = [ident(size) for _ in range(5)]
    for i in range(size):
        for j in range(size):
            if i == j:
                continue
            G[i][j] = q[j]*min(F(1), W[j]/W[i])
            if Q[i][j]:
                ratioQ = Q[j][i]/Q[i][j]
                rq[i][j] = q[j]*ratioQ/q[i]
                rp = pi[j]*ratioQ/pi[i]
                screens[i][j] = rational_power(q[j]/q[i], eta)*rational_power(ratioQ, kappa)
                acc[i][j] = min(F(1), screens[i][j])*min(F(1), rp/screens[i][j])
                L[i][j] = Q[i][j]*acc[i][j]
        G[i][i] = 1-sum(G[i][j] for j in range(size) if j != i)
        L[i][i] = 1-sum(L[i][j] for j in range(size) if j != i)
    C = [[(F(i == j)+alpha*G[i][j]+(1-alpha)*L[i][j])/2
          for j in range(size)] for i in range(size)]
    for P in (G, L, C):
        assert all(sum(row) == 1 and min(row) >= 0 for row in P)
        assert all(pi[i]*P[i][j] == pi[j]*P[j][i]
                   for i in range(size) for j in range(size))
    return W, G, L, C, acc, rq, screens


def absorb(P, A, E):
    idx = A+E
    return idx, [[P[x][y] if x in A else F(x == y) for y in idx] for x in idx]


def transform(P, idx, q):
    return [[P[i][j]*rational_power(q[idx[i]]/q[idx[j]], F(1, 2))
             for j in range(len(idx))] for i in range(len(idx))]


def full_return(q, C, A, B, n=8, N=3):
    size = len(q)
    alive = [q[x] if x in A else F(0) for x in range(size)]
    hit = [q[x] if x in B else F(0) for x in range(size)]
    accounted = vm(hit, power(C, n))
    masses = [sum(hit)]
    for j in range(1, N+1):
        move = vm(alive, C)
        hit = [move[x] if x in B else F(0) for x in range(size)]
        alive = [move[x] if x in A else F(0) for x in range(size)]
        tail = vm(hit, power(C, n-j))
        accounted = [x+y for x, y in zip(accounted, tail)]
        masses.append(sum(hit))
    residual = vm(alive, power(C, n-N))
    accounted = [x+y for x, y in zip(accounted, residual)]
    assert accounted == vm(q, power(C, n))
    assert sum(masses)+sum(alive) == 1
    return {'n': n, 'N': N, 'hit_masses': masses, 'residual_mass': sum(alive),
            'full_original_return_identity': True}


def energy_case(q, pi, Q, ratio, eta, kappa, alpha, w, A, E):
    b, e = sum(q[x] for x in A), sum((q[x] for x in E), F(0))
    W, G, L, C, acc, rq, screens = native(q, pi, Q, eta, kappa, alpha)
    idx, PE = absorb(C, A, E)
    _, LE = absorb(L, A, E)
    _, GE = absorb(G, A, E)
    LM, PM = transform(LE, idx, q), transform(PE, idx, q)
    weights = [F(1) if x in A else w for x in idx]
    aux = [[(Q[y][x] if x in A else F(0)) if x != y else
            (L[x][x] if x in A else F(1)) for y in idx] for x in idx]
    auxcols = [sum(aux[i][j] for i in range(len(idx))) for j in range(len(idx))]
    assert max(auxcols) <= 2
    assert all(aux[i][j] or LM[i][j] == 0
               for i in range(len(idx)) for j in range(len(idx)))
    coeff = [[LM[i][j]**2/aux[i][j] if aux[i][j] else F(0)
              for j in range(len(idx))] for i in range(len(idx))]
    for i, x in enumerate(idx):
        for j, y in enumerate(idx):
            if x in A and x != y and Q[x][y]:
                assert coeff[i][j] == Q[x][y]*acc[x][y]**2/rq[x][y]
    # theta=1/2, p=2, |kappa-eta|=eta, A=log(ratio), so U=w*ratio.
    assert abs(kappa-eta) == eta
    U = w*ratio
    if eta == F(1, 2):
        tau, H, scalar_regime = F(0), U, 'tau_zero_supremum'
    else:
        assert eta == F(3, 4)
        tau = F(2, 3)
        H = F(4, 27)*U**3 if U*tau <= 1 else U-1
        scalar_regime = 'interior' if U*tau < 1 else 'endpoint'
    rows = [sum(weights[j]*coeff[i][j] for j in range(len(idx)))
            for i in range(len(idx))]
    assert all(rows[i] <= (1+H if x in A else w) for i, x in enumerate(idx))
    lpivots = ldl(energy_slack(LM, [2*(1+H) if x in A else 2*w for x in idx], weights))
    gc = [sum(q[x]*GE[i][j]/q[y] for i, x in enumerate(idx))
          for j, y in enumerate(idx)]
    gr = [sum(weights[j]*GE[i][j] for j in range(len(idx))) for i in range(len(idx))]
    for i, x in enumerate(idx):
        assert gc[i] <= (2*b if x in A else 1+b)
        assert gr[i] == (b+w*e if x in A else w)
        if x in E:
            assert gc[i] == 1+b
    delta = max(F(0), (1-alpha)*H-alpha*(1-b))
    gamma = F(1, 2)+1+delta+alpha*w*e
    ppivots = ldl(energy_slack(PM, [gamma*z for z in weights], weights))
    assert all(PE[i][j] == (F(i == j)+alpha*GE[i][j]+(1-alpha)*LE[i][j])/2
               for i in range(len(idx)) for j in range(len(idx)))
    hits = []
    for N in (1, 3, 7):
        init = [q[x] if x in A else F(0) for x in idx]
        absorbed = vm(init, power(PE, N))
        hit = sum((absorbed[i] for i, x in enumerate(idx) if x in E), F(0))
        alive = [q[x] if x in A else F(0) for x in range(len(q))]
        independently_counted = F(0)
        for _ in range(N):
            move = vm(alive, C)
            independently_counted += sum((move[x] for x in E), F(0))
            alive = [move[x] if x in A else F(0) for x in range(len(q))]
        assert hit == independently_counted
        bound_squared = b*e*gamma**N/w
        assert hit**2 <= bound_squared
        hits.append({'N': N, 'first_hit': hit, 'holder_squared_bound': bound_squared})
    return {'ratio': ratio, 'eta': eta, 'kappa': kappa, 'alpha': alpha, 'w': w,
            'E': E, 'U': U, 'tau': tau, 'H': H, 'scalar_regime': scalar_regime,
            'positive_part': delta, 'gamma': gamma, 'auxiliary_columns': auxcols,
            'powered_weighted_rows': rows, 'local_all_vector_LDL': lpivots,
            'mixture_all_vector_LDL': ppivots, 'global_density_columns': gc,
            'global_weighted_rows': gr, 'first_hit_checks': hits}


def energy_checks():
    q = [F(i**4, 979) for i in range(1, 6)]
    pi = [F(x, 5503) for x in (1, 1, 1, 500, 5000)]
    A, B = [0, 1, 2], [3, 4]
    assert max(pi[i]/q[i] for i in range(5)) < 2
    assert A == [i for i in range(5) if pi[i]/q[i] < F(1, 5)]
    fixtures, cases, returns = [], [], []
    for ratio in (F(17, 16)**4, F(3, 2)**4):
        Q = [[F(0) for _ in q] for _ in q]
        edges = [(0, 1), (1, 2), (2, 0), (0, 3), (0, 4)]
        for x, y in edges:
            Q[x][y], Q[y][x] = 1/(8*ratio), F(1, 8)
        for x in range(5):
            Q[x][x] = 1-sum(Q[x])
        assert Q[0][1]*Q[1][2]*Q[2][0] != Q[1][0]*Q[2][1]*Q[0][2]
        assert all(max(Q[y][x]/Q[x][y], Q[x][y]/Q[y][x]) == ratio
                   for x, y in edges)
        fixtures.append({'ratio': ratio, 'q': q, 'pi': pi, 'Q': Q,
                         'theta': F(1, 2), 'p': 2, 'h': F(1, 5),
                         'A_low': A, 'B': B,
                         'KL_admission': 'max(pi/q)<2 implies KL<log(2)<1',
                         'nonreversible_proposal_cycle': edges[:3]})
        for eta in (F(1, 2), F(3, 4)):
            for kappa in (F(0), 2*eta):
                for alpha in (F(1, 2), F(3, 4)):
                    C = native(q, pi, Q, eta, kappa, alpha)[3]
                    returns.append({'ratio': ratio, 'eta': eta, 'kappa': kappa,
                                    'alpha': alpha, **full_return(q, C, A, B)})
                    for w in (F(1), F(2)):
                        for mask in range(4):
                            E = [B[i] for i in range(2) if mask & (1 << i)]
                            cases.append(energy_case(q, pi, Q, ratio, eta, kappa, alpha, w, A, E))
    assert len(cases) == 128 and len(returns) == 16
    assert {r['scalar_regime'] for r in cases} == {'tau_zero_supremum', 'interior', 'endpoint'}
    assert any(r['positive_part'] == 0 for r in cases)
    assert any(r['positive_part'] > 0 for r in cases)
    return fixtures, {'status': 'PASS', 'cases': cases, 'full_returns': returns,
                      'local_all_vector_certificates': 128,
                      'mixture_all_vector_certificates': 128,
                      'first_hit_identities': 384, 'full_return_identities': 16}


def lump(P, blocks):
    out = []
    for block in blocks:
        rows = [[sum(P[x][y] for y in dst) for dst in blocks] for x in block]
        assert all(row == rows[0] for row in rows)
        out.append(rows[0])
    return out


def entropy_upper(pi, q):
    """KL <= sum_{W>1} pi ceil(log2 W), because log(2)<1."""
    integers = []
    upper = F(0)
    for px, qx in zip(pi, q):
        W, k = px/qx, 0
        while F(2)**k < W:
            k += 1
        integers.append(k)
        upper += px*k
    return upper, integers


def tree_fixture(sign):
    ratio, M, J, scale = F(9, 4), 3, 2, 4
    b, p, eta = F(1, 64), F(1, 16), F(1, 2)
    mismatch_kappa = F(2) if sign == 'expansion' else F(0)
    z = M*ratio**(-4) if sign == 'expansion' else F(1, M)
    levels = [list(itertools.product(range(M), repeat=d)) for d in range(J+1)]
    labels = [label for group in levels for label in group]
    pos = {x: i for i, x in enumerate(labels)}
    core = len(labels)
    Q = [[F(0) for _ in range(core+1)] for _ in range(core+1)]
    # This same native undirected tree is oriented by progress levels below.
    for d in range(J):
        for parent in levels[d]:
            for child_symbol in range(M):
                child = parent+(child_symbol,)
                x, y = pos[parent], pos[child]
                Q[x][y], Q[y][x] = F(1, 2*M), ratio/(2*M)
    for x in range(core+1):
        Q[x][x] = 1-sum(Q[x])
    progress = levels if sign == 'expansion' else levels[::-1]
    blocks = [[pos[x] for x in group] for group in progress]+[[core]]
    qt = [b*z**i for i in range(J+1)]
    pt = [p*F(scale)**(-2*(J-i)) for i in range(J+1)]
    qt.append(1-sum(qt))
    pt.append(1-sum(pt))
    q, pi = [F(0)]*(core+1), [F(0)]*(core+1)
    for i, block in enumerate(blocks):
        for x in block:
            q[x], pi[x] = qt[i]/len(block), pt[i]/len(block)
    bound, ints = entropy_upper(pi, q)
    assert bound < 1
    assert len(q) == 14
    for x in range(core):
        for y in range(core):
            if x != y and Q[x][y]:
                assert max(Q[y][x]/Q[x][y], Q[x][y]/Q[y][x]) == ratio
    return {'sign': sign, 'ratio': ratio, 'M': M, 'depth': J, 'scale': scale,
            'b': b, 'p': p, 'eta': eta, 'mismatch_kappa': mismatch_kappa,
            'z': z, 'q': q, 'pi': pi, 'Q': Q, 'blocks': blocks,
            'q_levels': qt, 'pi_levels': pt, 'labels': labels+[('core',)],
            'KL_exact_rational_upper': bound, 'KL_ceil_log2_weights': ints,
            'p_scope': 'Finite rational identity fixture; not the asymptotic p(n,V) allocation'}


def tree_checks():
    fixtures, records = [], []
    for sign in ('coalescence', 'expansion'):
        inp = tree_fixture(sign)
        fixtures.append(inp)
        q, pi, Q, blocks = [inp[k] for k in ('q', 'pi', 'Q', 'blocks')]
        qt, pt = inp['q_levels'], inp['pi_levels']
        scale, J, p, b, z = [inp[k] for k in ('scale', 'depth', 'p', 'b', 'z')]
        f = F(1, 2) if sign == 'expansion' else inp['ratio']/(2*inp['M'])
        for kappa in (inp['mismatch_kappa'], inp['eta']):
            sigma = F(1) if kappa != inp['eta'] else (
                F(8, 27) if sign == 'expansion' else F(2, 3))
            for alpha in (F(1, 2), F(3, 4)):
                W, G, L, C, acc, rq, screens = native(q, pi, Q, inp['eta'], kappa, alpha)
                GL, LL, CL = [lump(P, blocks) for P in (G, L, C)]
                for i in range(J):
                    assert LL[i][i+1] == f*sigma
                    assert LL[i+1][i] == f*sigma/scale**2
                    for x in blocks[i]:
                        for y in blocks[i+1]:
                            if Q[x][y]:
                                assert screens[x][y] == sigma
                for i in range(J+1):
                    expected = 1-f*sigma*int(i<J)-f*sigma*int(i>0)/scale**2
                    assert LL[i][i] == expected
                Wleaf = pt[J]/qt[J]
                assert Wleaf == max(W)
                dleaf = alpha*(1-p)/(2*Wleaf)+(1-alpha)*f*sigma/(2*scale**2)
                assert all(sum(C[x][y] for y in blocks[J]) == 1-dleaf for x in blocks[J])
                if len(blocks[J]) > 1:
                    assert all(C[x][x] < 1-dleaf for x in blocks[J])
                # Marked-path chain kills EVERY global attempt and local backward move.
                marked = [[F(0) for _ in range(J+1)] for _ in range(J+1)]
                c, g = (1-alpha)*f*sigma/2, alpha/2
                for i in range(J):
                    marked[i][i] = 1-c-g-(c/scale**2 if i else 0)
                    marked[i][i+1] = c
                marked[J][J] = 1
                native_law, ordinary_law = q[:], q[:]
                checks = []
                for horizon in range(1, 17):
                    native_law, ordinary_law = vm(native_law, C), vm(ordinary_law, G)
                    if horizon not in (4, 8, 16):
                        continue
                    quotient = vm(qt, power(CL, horizon))
                    assert [sum(native_law[x] for x in block) for block in blocks] == quotient
                    error = tv(native_law, pi)
                    assert error == tv(quotient, pt)
                    H = horizon//(2*J)
                    hazards = [c+g+(c/scale**2 if i else 0) for i in range(J)]
                    exact_stage = [c/hz*(1-(1-hz)**H) for hz in hazards]
                    per_window = F(1)
                    for value in exact_stage:
                        per_window *= value
                    # Rational conservative alternative to exp[-(c+g)H] in the proof.
                    E = c+g+c/scale**2
                    rational_stage_bound = c/E*(1-(1-(c+g))**H)
                    assert all(value >= rational_stage_bound for value in exact_stage)
                    lower = b*rational_stage_bound**J*(1-dleaf)**horizon-p
                    assert error >= lower
                    marked_capture = vm([b]+[F(0)]*J, power(marked, J*H))[J]
                    assert marked_capture >= b*per_window
                    assert quotient[J] >= marked_capture*(1-dleaf)**horizon
                    sq = sum(qt[1:J+1])
                    ordinary_bound = sum(pt[:J+1])+sq/(1-b)+b**(horizon+1)
                    ordinary_error = tv(ordinary_law, pi)
                    assert ordinary_error <= ordinary_bound
                    checks.append({'horizon': horizon, 'TV': error,
                        'terminal_probability': quotient[J], 'finite_capture_TV_lower': lower,
                        'marked_capture_by_JH': marked_capture, 'window_capture': b*per_window,
                        'rational_stage_lower': rational_stage_bound,
                        'ordinary_TV': ordinary_error, 'ordinary_upper': ordinary_bound})
                records.append({'sign': sign, 'kappa': kappa, 'alpha': alpha,
                    'sigma': sigma, 'forward_proposal': f, 'G_quotient': GL,
                    'L_quotient': LL, 'C_quotient': CL, 'terminal_escape': dleaf,
                    'terminal_union_size': len(blocks[J]),
                    'one_terminal_native_diagonal': C[blocks[J][0]][blocks[J][0]],
                    'checks': checks})
    assert len(records) == 8
    return fixtures, {'status': 'PASS', 'native_states_each': 14, 'records': records,
        'native_kernel_configurations': 8, 'native_lumping_TV_checks': 24,
        'capture_and_retention_checks': 24, 'ordinary_full_return_upper_checks': 24,
        'scope': 'Exact finite native identities and inequalities, not asymptotic rate evidence'}


def normalize(x):
    if isinstance(x, F):
        return str(x)
    if isinstance(x, dict):
        return {str(k): normalize(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [normalize(v) for v in x]
    return x


def write(path, value):
    path.write_text(json.dumps(normalize(value), indent=2, sort_keys=True)+'\n')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    assert __debug__, 'Assertions must not be disabled'
    args.output_dir.mkdir(parents=True, exist_ok=True)
    start_wall, start_cpu = time.perf_counter(), time.process_time()
    try:
        ei, er = energy_checks()
        energy_time = {'wall_seconds': time.perf_counter()-start_wall,
                       'cpu_seconds': time.process_time()-start_cpu}
        tree_wall, tree_cpu = time.perf_counter(), time.process_time()
        ti, tr = tree_checks()
        resources = {'energy_body': energy_time,
            'tree_body': {'wall_seconds': time.perf_counter()-tree_wall,
                          'cpu_seconds': time.process_time()-tree_cpu},
            'total_body': {'wall_seconds': time.perf_counter()-start_wall,
                           'cpu_seconds': time.process_time()-start_cpu},
            'peak_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            'scope': 'Current exact diagnostic bodies only, excluding serialization and replay',
            'inference_tokens_monetary_total_discovery_cost': 'unknown',
            'stochastic_runs': 0}
        write(args.output_dir/'EXACT_INPUTS.json', {'energy': ei, 'tree': ti})
        write(args.output_dir/'EXACT_RESULTS.json', {'energy': er, 'tree': tr})
        write(args.output_dir/'EXACT_RESOURCES.json', resources)
        report = {'status': 'PASS',
            'energy_certificates_each_kind': er['local_all_vector_certificates'],
            'first_hit_identities': er['first_hit_identities'],
            'full_return_identities': er['full_return_identities'],
            'native_tree_configurations': tr['native_kernel_configurations'],
            'native_tree_TV_checks': tr['native_lumping_TV_checks'],
            'resources': resources,
            'deterministic_sha256': {name: hashlib.sha256((args.output_dir/name).read_bytes()).hexdigest()
                         for name in ('EXACT_INPUTS.json', 'EXACT_RESULTS.json')}}
        write(args.output_dir/'RUN_SUMMARY.json', report)
        print(json.dumps(report, indent=2))
    except Exception:
        write(args.output_dir/'FAILED_RUN.json',
              {'traceback': traceback.format_exc(),
               'elapsed_wall_seconds': time.perf_counter()-start_wall,
               'elapsed_cpu_seconds': time.process_time()-start_cpu,
               'scope': 'Preserve failure; do not silently overwrite'})
        raise


if __name__ == '__main__':
    main()

