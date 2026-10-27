"""Finite normalized-Hermite checks for the joint Gaussian Stein gauge.

This verifies polynomial identities, not a sampler or continuous-law TV bound.
Run only this owned file. Requires numpy for the independent matrix diagnostic.
"""
from __future__ import annotations
import json
import math
from pathlib import Path
import numpy as np

TOL = 1e-10


def add(*polys):
    out = {}
    for p in polys:
        for k, v in p.items():
            out[k] = out.get(k, 0.0) + v
    return {k: v for k, v in out.items() if abs(v) > 1e-13}


def scale(p, c):
    return {k: c * v for k, v in p.items() if abs(c * v) > 1e-13}


def derivative(p, j):
    out = {}
    for k, v in p.items():
        if k[j]:
            q = list(k)
            q[j] -= 1
            out[tuple(q)] = math.sqrt(k[j]) * v
    return out


def divergence_slot(p, j):
    out = {}
    for k, v in p.items():
        q = list(k)
        q[j] += 1
        out[tuple(q)] = math.sqrt(k[j] + 1) * v
    return out


def norm2(p):
    return sum(v * v for v in p.values())


def total_norm2(polys):
    return sum(norm2(p) for p in polys)


def max_error(p):
    return max((abs(v) for v in p.values()), default=0.0)


def source_adjoint_inverse(R, d, ng, mz):
    """R entries have fixed source degree ng and noise degree mz.

    Returns u[d], Jg[d,d], Jz[d,d].  Row divergence is used.
    """
    N = ng + mz
    dr = [add(*(divergence_slot(R[i][j], d + j)
                 for j in range(d))) for i in range(d)]
    s = add(*(divergence_slot(dr[i], d + i) for i in range(d)))
    phi = scale(s, -1 / ((mz + 2) * (N + 2)))
    u = [derivative(phi, d + i) for i in range(d)]
    # w is the orthogonal divergence-free part of delta_Z R.
    w = [add(dr[i], scale(derivative(s, d + i), -1 / (mz + 2)))
         for i in range(d)]
    B = [[scale(add(derivative(w[i], d + j),
                    scale(derivative(w[j], d + i), -1)),
                1 / (mz + 2)) for j in range(d)] for i in range(d)]
    Jg = [[scale(derivative(u[i], j), -1)
           for j in range(d)] for i in range(d)]
    Jz = [[add(scale(R[i][j], -1),
               scale(derivative(u[j], d + i), -1), B[i][j])
           for j in range(d)] for i in range(d)]
    return u, Jg, Jz


def compositions(n, k):
    if k == 1:
        yield (n,)
    else:
        for j in range(n + 1):
            for q in compositions(n - j, k - 1):
                yield (j,) + q


def identity_trial(d, ng, mz, seed):
    rng = np.random.default_rng(seed)
    ks = [g + z for g in compositions(ng, d)
          for z in compositions(mz, d)]
    R = [[{} for _ in range(d)] for _ in range(d)]
    for i in range(d):
        for j in range(i, d):
            p = {k: float(rng.normal()) for k in ks}
            R[i][j] = p
            R[j][i] = dict(p)
    rn = total_norm2([p for row in R for p in row])
    R = [[scale(p, 1 / math.sqrt(rn)) for p in row] for row in R]
    u, Jg, Jz = source_adjoint_inverse(R, d, ng, mz)
    err_div = 0.0
    err_linear = 0.0
    err_center = 0.0
    for i in range(d):
        du = add(*(divergence_slot(Jg[i][j], j) for j in range(d)),
                 *(divergence_slot(Jz[i][j], d+j) for j in range(d)))
        err_div = max(err_div, max_error(add(du, scale(u[i], -1))))
        err_center = max(err_center,
            max((abs(v) for k,v in u[i].items() if sum(k[d:]) == 0),
                default=0.0))
        for j in range(d):
            # sym[J_Z + (D_Zu)^T] = -R.
            lij = add(Jz[i][j], derivative(u[j], d+i))
            lji = add(Jz[j][i], derivative(u[i], d+j))
            e = add(scale(add(lij,lji), .5), R[i][j])
            err_linear = max(err_linear, max_error(e))
    du2 = total_norm2([derivative(u[i], j)
                      for i in range(d) for j in range(2*d)])
    jg2 = total_norm2([p for row in Jg for p in row])
    jz2 = total_norm2([p for row in Jz for p in row])
    assert err_div < TOL, (d, ng, mz, err_div)
    assert err_linear < TOL, (d, ng, mz, err_linear)
    assert err_center == 0.0
    assert du2 <= 1 + TOL
    assert jg2 <= .25 + TOL
    assert jz2 <= (2 + math.sqrt(2))**2 + TOL
    return dict(d=d, source_degree=ng, noise_degree=mz,
                divergence_error=err_div, linear_error=err_linear,
                conditional_mean_error=err_center,
                full_Du_norm=math.sqrt(du2),
                Jg_norm=math.sqrt(jg2), Jz_norm=math.sqrt(jz2))


def strict_inverse_norm(n, lam):
    a = math.sqrt(1 - lam**2)
    # Log-sum-exp avoids cancellation/underflow at moderately high degree.
    terms_j, terms_u = [], []
    for q in range(n+1):
        lj = (math.lgamma(n+1)-math.lgamma(q+1)-math.lgamma(n-q+1)
              + 2*q*math.log(abs(lam/a)) - 2*math.log(a)
              - 2*math.log(q+1)-2*math.log(q+2))
        terms_j.append(lj)
        terms_u.append(lj + math.log(q+1))
    def lse(xs):
        z = max(xs)
        return z + math.log(sum(math.exp(x-z) for x in xs))
    return math.exp(.5*lse(terms_j)), math.exp(.5*lse(terms_u))


def scalar_affine_trial(n, m, lam):
    a = math.sqrt(1-lam**2)
    R = [[{(n,m): 1.0}]]
    u, jg, jz = source_adjoint_inverse(R, 1, n, m)
    L = add(scale(derivative(u[0],0),lam),
            scale(derivative(u[0],1),a),
            scale(jg[0][0],lam), scale(jz[0][0],a))
    e = max_error(add(L, scale(R[0][0],a)))
    assert e < TOL
    return e


def main():
    trials = [identity_trial(d,n,m,1000+d*100+n*10+m)
              for d in (1,2,3) for n in (0,1,3,7)
              for m in (0,1,2,5)]
    affine_errors = [scalar_affine_trial(n,m,lam)
                     for n in (0,1,5,20,100) for m in (0,1,5)
                     for lam in (.1,.4,.8,.99)]
    comparison = []
    for lam in (.1,.4,.8):
        a = math.sqrt(1-lam**2)
        for n in (1,10,50,100,250,1000):
            j, u = strict_inverse_norm(n,lam)
            # For R=H_n(G), full gauge inverse is exactly division by a.
            N = n
            cu = -1/((N+2)*a)
            cg = math.sqrt(n)/((N+2)*a)
            cz = -(n+1)/((N+2)*a)
            comparison.append(dict(lam=lam, n=n, strict_J=j,
                strict_u=u, full_u=abs(cu),
                full_Du=abs(cu)*math.sqrt(n+1),
                full_J=math.hypot(cg,cz)))
    out = dict(identity_trials=trials,
               maximum_affine_linear_error=max(affine_errors),
               comparison=comparison,
               scope="Finite polynomial identity/norm diagnostics only")
    path = Path(__file__).with_name("hermite_results.json")
    path.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps(dict(trials=len(trials),
        max_divergence_error=max(t['divergence_error'] for t in trials),
        max_linear_error=max(t['linear_error'] for t in trials),
        maximum_affine_linear_error=max(affine_errors),
        output=str(path)),indent=2))
    for row in comparison:
        if row['n'] in (10,100,1000):
            print(json.dumps(row))


if __name__ == "__main__":
    main()
