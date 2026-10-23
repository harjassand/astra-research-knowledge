#!/usr/bin/env python3
"""Exact native fan-out check for the changed geometry in matched powers."""
import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import resource
import time
import traceback
from reciprocal_checks import ident, native, quarter_root, lump, vm, power, tv, write


def run():
    n, m, alpha, eta = 2, 16, F(1, 2), F(1, 4)
    b, e, p, t = F(1, 4), F(1, 64), F(1, 2), F(1, 8)
    q = [b]+[e/m]*m+[1-b-e]
    pi = [t]+[p/m]*m+[1-p-t]
    Q = [[F(0) for _ in q] for _ in q]
    for j in range(1, m+1):
        Q[0][j], Q[j][0] = F(1, m), F(1)
    Q[-1][-1] = F(1)
    blocks = [[0], list(range(1, m+1)), [m+1]]
    ql, pil = [b, e, q[-1]], [t, p, pi[-1]]
    W, G, Lfull, Cfull, _, _ = native(q, pi, Q, eta, alpha)
    GL = lump(G, blocks)
    assert GL == [[b, e, q[-1]], [t/W[1], 1-(1-p)/W[1], pi[-1]/W[1]],
                  [t/W[-1], e, 1-t/W[-1]-e]]
    records = []
    for kappa in [F(1, 2), F(1, 4)]:
        L = ident(len(q))
        screens = []
        for i in range(len(q)):
            for j in range(len(q)):
                if i != j and Q[i][j]:
                    S = quarter_root(q[j]/q[i])**int(4*eta)*quarter_root(Q[j][i]/Q[i][j])**int(4*kappa)
                    rp = pi[j]*Q[j][i]/(pi[i]*Q[i][j])
                    L[i][j] = Q[i][j]*min(F(1), S)*min(F(1), rp/S)
                    if i == 0:
                        screens.append(S)
            L[i][i] = 1-sum(L[i][j] for j in range(len(q)) if j != i)
        sigma = F(1) if kappa != eta else F(1, 2)
        assert screens == [sigma]*m
        C = [[(F(i == j)+alpha*G[i][j]+(1-alpha)*L[i][j])/2
              for j in range(len(q))] for i in range(len(q))]
        for P in [L, C]:
            assert all(sum(row) == 1 and min(row) >= 0 for row in P)
            assert all(pi[i]*P[i][j] == pi[j]*P[j][i]
                       for i in range(len(q)) for j in range(len(q)))
        if kappa == eta:
            assert L == Lfull and C == Cfull
        LL, CL = lump(L, blocks), lump(C, blocks)
        assert LL == [[1-sigma, sigma, F(0)], [sigma/n**2, 1-sigma/n**2, F(0)],
                      [F(0), F(0), F(1)]]
        a, c = alpha*q[-1]/2, (alpha*e+(1-alpha)*sigma)/2
        v, dl = a+c, alpha*(1-p)/(2*W[1])+(1-alpha)*sigma/(2*n**2)
        for i in blocks[1]:
            assert sum(C[i][j] for j in blocks[1]) == 1-dl
            assert C[i][i] < 1-dl
        law = q[:]
        checks = []
        for horizon in range(1, 17):
            law = vm(law, C)
            if horizon in [2, 4, 8, 16]:
                quotient = vm(ql, power(CL, horizon))
                assert [sum(law[i] for i in block) for block in blocks] == quotient
                error = tv(law, pi)
                assert error == tv(quotient, pil)
                lower = b*c/v*(1-(1-v)**(horizon//2))*(1-dl)**horizon-p
                upper = p+t+e+b*c/v+b*(1-v)**horizon
                assert lower <= error <= upper
                checks.append({'horizon': horizon, 'TV': error, 'lower': lower, 'upper': upper})
        records.append({'kappa': kappa, 'screen': sigma, 'local_quotient': LL,
                        'leaf_block_hold': 1-dl, 'individual_leaf_diagonal': C[1][1], 'checks': checks})
    ordinary, law = [], q[:]
    for horizon in range(1, 17):
        law = vm(law, G)
        if horizon in [2, 4, 8, 16]:
            error = tv(law, pi)
            lower, upper = p-(horizon+1)*e, p+t+e/(1-b)+b**(horizon+1)
            assert lower <= error <= upper
            ordinary.append({'horizon': horizon, 'TV': error, 'lower': lower, 'upper': upper})
    return {'q': q, 'pi': pi, 'Q': Q, 'eta': eta, 'kappas': [F(1, 2), F(1, 4)],
            'alpha': alpha, 'blocks': blocks, 'n_scale': n, 'm': m, 'b': b,
            'KL_rational_upper': F(5, 2)+F(17, 47)}, {'status': 'PASS', 'native_states': len(q),
                'arithmetic': 'exact rational', 'records': records, 'ordinary': ordinary,
                'scope': 'finite native geometry and full-block identities, not asymptotic evidence'}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output-dir', type=Path, required=True)
    args = ap.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    wall, cpu = time.perf_counter(), time.process_time()
    try:
        inp, result = run()
        resources = {'wall_seconds': time.perf_counter()-wall, 'cpu_seconds': time.process_time()-cpu,
                     'peak_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                     'scope': 'body excluding serialization; not discovery cost',
                     'inference_token_monetary_discovery_cost': 'unknown'}
        write(args.output_dir/'FANOUT_INPUTS.json', inp)
        write(args.output_dir/'FANOUT_CHECKS.json', result)
        write(args.output_dir/'FANOUT_RESOURCES.json', resources)
        print(json.dumps({'status': 'PASS', 'hybrid_sandwiches_and_native_lumping': 8,
                          'ordinary_sandwiches': 4, 'resources': resources,
                          'deterministic_sha256': {n: hashlib.sha256((args.output_dir/n).read_bytes()).hexdigest()
                              for n in ['FANOUT_INPUTS.json', 'FANOUT_CHECKS.json']}}, indent=2))
    except Exception:
        write(args.output_dir/'FANOUT_FAILED.json', {'traceback': traceback.format_exc()})
        raise


if __name__ == '__main__':
    main()
