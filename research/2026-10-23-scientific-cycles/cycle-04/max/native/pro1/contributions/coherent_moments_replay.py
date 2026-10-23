#!/usr/bin/env python3
"""Finite exact normal-form checks of the infinite-bath moment identities.

This checks operator expressions in the inherited F_uv,K_uv algebra, not a
reflecting bath approximation. The infinite series and drift theorem are proved
in coherent_moments.md. No finite check count certifies those limits.
"""
import argparse
from fractions import Fraction as F
import importlib.util
import json
from pathlib import Path
import platform
import resource
import sys
import time


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--representation', type=Path, default=Path(__file__).resolve().parents[1] / 'representation/exact_representation.py')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    wall, cpu = time.perf_counter(), time.process_time()
    spec = importlib.util.spec_from_file_location('inherited_fock_rep', args.representation)
    rep = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = rep
    spec.loader.exec_module(rep)
    add, mul, scale, star = rep.add, rep.mul, rep.scale, rep.adjoint
    I, R, S, ig = rep.ONE, rep.ROOT, rep.S[1], rep.I_G
    sub = lambda x, y: add(x, scale(y, -1))
    comm = lambda x, y: sub(mul(x, y), mul(y, x))
    C = lambda x: add(*(mul(mul(rep.S[a], x), star(rep.S[a])) for a in (1, 2)))
    D = sub(star(S), S)
    records = []
    for alpha, beta, q, g in [(F(3, 5), F(4, 5), F(1, 3), F(1, 10)), (F(12, 13), F(5, 13), F(2, 5), F(-1, 8))]:
        a, r = (1-q)/2, q/(1-q)
        assert alpha*alpha+beta*beta == 1 and g*g <= q*a
        rho = [[rep.G(q), ig*g, rep.G()], [-ig*g, rep.G(a), rep.G()], [rep.G(), rep.G(), rep.G(a)]]
        V = rep.port_matrix(alpha, beta)
        def T(x):
            return add(*(scale(mul(mul(star(V[b][j]), x), V[b][i]), rho[i][j])
                         for i in range(3) for j in range(3) for b in range(3) if rho[i][j]))
        assert T(I) == I
        Fk = [S]
        for k in range(6):
            Fk.append(C(Fk[-1]))
        first = add(scale(S, beta*beta+alpha*alpha*a), scale(Fk[1], alpha*alpha*q),
                    scale(R, ig*alpha*alpha*g), scale(mul(S, R), -ig*alpha*beta*q),
                    scale(sub(I, mul(S, star(S))), -alpha*beta*g))
        assert T(S) == first
        assert rep.trace_stationary(T(S)) == rep.G(-F(5, 6)*alpha*beta*g)
        for k in range(1, 6):
            delta = sub(Fk[k-1], Fk[k])
            rhs = add(scale(Fk[k], beta*beta), scale(Fk[k+1], alpha*alpha*q),
                      scale(Fk[k-1], alpha*alpha*(1-q)),
                      scale(add(mul(delta, star(S)), mul(S, delta)), -alpha*beta*g))
            assert T(Fk[k]) == rhs
        for N in range(5):
            B = add(*(scale(Fk[k], r**k) for k in range(N+1)))
            lhs = sub(B, T(B))
            rhs = add(scale(S, alpha*alpha*a), scale(mul(S, R), ig*alpha*beta*q),
                      scale(R, -ig*alpha*alpha*g), scale(comm(D, B), alpha*beta*g),
                      scale(sub(Fk[N], Fk[N+1]), alpha*alpha*q*r**N))
            assert lhs == rhs
            comm_rhs = add(I, mul(S, S),
                           scale(add(mul(B, star(S)), mul(S, B)), -(1-r)),
                           scale(add(mul(Fk[N], star(S)), mul(S, Fk[N])), -r**(N+1)))
            assert comm(D, B) == comm_rhs
        records.append({'alpha':str(alpha),'beta':str(beta),'q':str(q),'g':str(g),
                        'first_moment':'passed','hierarchy_k_1_to_5':'passed',
                        'finite_resolvent_N_0_to_4':'passed','finite_commutator_N_0_to_4':'passed'})
    beta = F(1, 512)
    alpha2 = 1-beta*beta
    q = F(1, 2)-3*beta*beta/32
    a = (1-q)/2
    g = beta/8
    nu = alpha2*(1-2*q)-8*beta*beta*g*g/a-beta**4*g*g*q/(alpha2*a*a)
    assert nu > beta*beta/8
    payload = {
        'scope':'Finite exact infinite-bath normal-form identities; not the proof of the infinite series or asymptotic communication.',
        'records':records,
        'fixed_seed':{'beta':str(beta),'q':str(q),'g':str(g),'a':str(a),
                      'nu_exact':str(nu),'nu_float':float(nu),
                      'nu_over_beta_squared_float':float(nu/(beta*beta)),
                      'proved_rational_comparison':'nu > beta^2/8'},
        'resources':{'wall_seconds':time.perf_counter()-wall,'cpu_seconds':time.process_time()-cpu,
                     'max_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                     'python':platform.python_version(),'discovery_cost':'not independently metered'}
    }
    out = json.dumps(payload, indent=2)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(out)
    print(out, end='')


if __name__ == '__main__':
    main()
