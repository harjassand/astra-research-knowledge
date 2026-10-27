#!/usr/bin/env python3
"""Finite Hermite algebra checks for the owned vector construction."""
import json
import math
from pathlib import Path
import numpy as np


def add(p, q, c=1.):
    r = dict(p)
    for k, v in q.items():
        r[k] = r.get(k, 0.) + c * v
        if r[k] == 0:
            r.pop(k)
    return r


def scale(p, c):
    return {k: c * v for k, v in p.items() if c * v != 0}


def act(p, axis, creation=False):
    r = {}
    for ix, v in p.items():
        n = ix[axis]
        if creation or n:
            jx = list(ix)
            jx[axis] += 1 if creation else -1
            jx = tuple(jx)
            r[jx] = r.get(jx, 0.) + math.sqrt(n + 1 if creation else n) * v
    return r


def div(v, d):
    r = {}
    for i in range(d):
        r = add(r, act(v[i], d + i, True))
    return r


def rowdiv(M, d):
    return [div(row, d) for row in M]


def grad(p, d, source=False):
    return [act(p, i if source else d + i) for i in range(d)]


def sym(M):
    return [[scale(add(M[i][j], M[j][i]), .5) for j in range(len(M))] for i in range(len(M))]


def norm(p):
    return math.sqrt(sum(v * v for v in p.values()))


def mnorm(M):
    return math.sqrt(sum(norm(p) ** 2 for row in M for p in row))


def ninv(p, d, power=1):
    return {ix: v / sum(ix[d:]) ** power for ix, v in p.items() if sum(ix[d:])}


def transfer(p, C, d):
    r = {}
    for i in range(d):
        for j in range(d):
            r = add(r, act(act(p, j), d + i, True), C[i, j])
    return r


def solve_potential(R, C, d):
    s = div(rowdiv(R, d), d)
    eta = {}
    for ix, value in s.items():
        m, k = sum(ix[d:]), sum(ix[:d])
        term = {ix: -value / m}
        eta = add(eta, term)
        for j in range(1, k + 1):
            term = scale(transfer(term, C, d), -1. / (m + j))
            eta = add(eta, term)
    return grad(ninv(eta, d), d)


def hodge(R, d):
    phi = scale(ninv(div(rowdiv(R, d), d), d, 2), -1)
    u = grad(phi, d)
    du = [grad(p, d) for p in u]
    w = [add(a, b) for a, b in zip(rowdiv(R, d), grad(div(u, d), d))]
    dw = [grad(p, d) for p in w]
    J = [[{} for _ in range(d)] for _ in range(d)]
    for i in range(d):
        for j in range(d):
            skew = add(dw[i][j], dw[j][i], -1)
            skew = {ix: v / (sum(ix[d:]) + 2) for ix, v in skew.items()}
            J[i][j] = add(add(scale(R[i][j], -1), du[j][i], -1), skew)
    return u, J


def simple_divergence_inverse(R, C, d):
    """Alternative gauge: u=delta J0, (NZ+2+delta C DG)J0=-R."""
    J0 = [[{} for _ in range(d)] for _ in range(d)]
    for i in range(d):
        for j in range(d):
            for ix, value in R[i][j].items():
                m, k = sum(ix[d:]), sum(ix[:d])
                term = {ix: -value / (m + 2)}
                J0[i][j] = add(J0[i][j], term)
                for ell in range(1, k + 1):
                    term = scale(transfer(term, C, d), -1. / (m + ell + 2))
                    J0[i][j] = add(J0[i][j], term)
    u = rowdiv(J0, d)
    du = [grad(p, d) for p in u]
    dgu = [grad(p, d, True) for p in u]
    source = [[{} for _ in range(d)] for _ in range(d)]
    for i in range(d):
        for j in range(d):
            for k in range(d):
                source[i][j] = add(source[i][j], dgu[j][k], C[i, k])
    F = sym([[add(add(add(R[i][j], J0[i][j]), du[j][i]), source[i][j]) for j in range(d)] for i in range(d)])
    assert norm(div(rowdiv(F, d), d)) < 1e-9
    w = rowdiv(F, d)
    dw = [grad(p, d) for p in w]
    J = [[{} for _ in range(d)] for _ in range(d)]
    for i in range(d):
        for j in range(d):
            skew = add(dw[i][j], dw[j][i], -1)
            skew = {ix: v / (sum(ix[d:]) + 2) for ix, v in skew.items()}
            J[i][j] = add(add(J0[i][j], F[i][j], -1), skew)
    return u, J


def check(d, seed):
    rng = np.random.default_rng(seed)
    R = [[{} for _ in range(d)] for _ in range(d)]
    for i in range(d):
        for j in range(i, d):
            p = {}
            for _ in range(25):
                ix = tuple(int(x) for x in rng.integers(0, 3, size=2*d))
                if sum(ix[:d]) <= 4 and sum(ix[d:]) <= 3:
                    p[ix] = float(rng.normal())
            R[i][j] = R[j][i] = p
    C = rng.normal(size=(d, d)) / (4*d)
    C = (C + C.T) / 2
    u = solve_potential(R, C, d)
    dgu = [grad(p, d, True) for p in u]
    source = [[{} for _ in range(d)] for _ in range(d)]
    for i in range(d):
        for j in range(d):
            for k in range(d):
                source[i][j] = add(source[i][j], dgu[j][k], C[i,k])
    ss = sym(source)
    eff = [[add(R[i][j], ss[i][j]) for j in range(d)] for i in range(d)]
    uh, J = hodge(eff, d)
    du = [grad(p, d) for p in u]
    lhs = sym([[add(add(J[i][j], du[j][i]), source[i][j]) for j in range(d)] for i in range(d)])
    defect = [[add(lhs[i][j], R[i][j]) for j in range(d)] for i in range(d)]
    dj = rowdiv(J, d)
    out = {
        'dimension': d, 'seed': seed, 'residual_norm': mnorm(R),
        'full_equation_error': mnorm(defect),
        'divergence_error': math.sqrt(sum(norm(add(dj[i], u[i], -1))**2 for i in range(d))),
        'potential_consistency_error': math.sqrt(sum(norm(add(uh[i], u[i], -1))**2 for i in range(d))),
        'conditional_centering_by_z_degree': all(sum(ix[d:]) >= 1 for p in u for ix in p),
    }
    assert out['full_equation_error'] < 1e-9
    assert out['divergence_error'] < 1e-9
    assert out['potential_consistency_error'] < 1e-9
    us, Js = simple_divergence_inverse(R, C, d)
    ds = [grad(p, d) for p in us]
    dgs = [grad(p, d, True) for p in us]
    ls = [[add(Js[i][j], ds[j][i]) for j in range(d)] for i in range(d)]
    for i in range(d):
        for j in range(d):
            for k in range(d):
                ls[i][j] = add(ls[i][j], dgs[j][k], C[i,k])
    ls = sym(ls)
    errs = [[add(ls[i][j], R[i][j]) for j in range(d)] for i in range(d)]
    divs = rowdiv(Js, d)
    out['simple_gauge_equation_error'] = mnorm(errs)
    out['simple_gauge_divergence_error'] = math.sqrt(sum(norm(add(divs[i], us[i], -1))**2 for i in range(d)))
    assert out['simple_gauge_equation_error'] < 1e-9
    assert out['simple_gauge_divergence_error'] < 1e-9
    return out


if __name__ == '__main__':
    results = [check(d, seed) for d in [1,2,3] for seed in [91023, 91024]]
    path = Path(__file__).resolve().parent / 'vector_checks.json'
    path.write_text(json.dumps(results, indent=2) + '\n')
    print(json.dumps(results, indent=2))
