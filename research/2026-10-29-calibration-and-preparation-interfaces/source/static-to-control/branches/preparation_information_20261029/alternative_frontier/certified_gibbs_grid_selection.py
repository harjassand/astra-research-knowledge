#!/usr/bin/env python3
"""Certified finite 1D Gibbs-grid selection.

The default histogram is a deterministic arithmetic fixture, not acquired
native data. HiGHS proposes an LP solution. Fraction arithmetic repairs and
checks a feasible primal, a feasible dual, numerical intervals, and the
coefficient-relaxation loss. General-dimensional construction is in the note.

Usage:
  python certified_gibbs_grid_selection.py --output certificate.json
  python certified_gibbs_grid_selection.py --verify certificate.json
  python certified_gibbs_grid_selection.py --counts 2,4,8,16,18,10,4,2
"""
import argparse
import json
import math
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix


def atan_reciprocal_interval(q, terms=32):
    s = sum((F((-1) ** k, (2 * k + 1) * q ** (2 * k + 1))
             for k in range(terms)), F(0))
    nxt = F((-1) ** terms, (2 * terms + 1) * q ** (2 * terms + 1))
    return min(s, s + nxt), max(s, s + nxt)


def outward_dyadic(lo, hi, bits=80):
    scale = 1 << bits
    return (F((lo*scale).__floor__(), scale),
            F((hi*scale).__ceil__(), scale))


@lru_cache(maxsize=None)
def pi_interval(terms=32):
    a, b = atan_reciprocal_interval(5, terms)
    c, d = atan_reciprocal_interval(239, terms)
    return outward_dyadic(16*a-4*d, 16*b-4*c, bits=96)


@lru_cache(maxsize=None)
def exp_nonnegative_interval(lo, hi, terms=48):
    assert 0 <= lo <= hi
    # Positive Taylor lower sum; the upper remainder is a geometric majorant.
    terms = max(terms, hi.__ceil__() + 2)
    sl = sh = tl = th = F(1)
    for k in range(1, terms + 1):
        tl *= lo / k
        th *= hi / k
        sl += tl
        sh += th
    first_omitted = th * hi / (terms + 1)
    ratio_bound = hi / (terms + 2)
    assert ratio_bound < 1
    return outward_dyadic(sl, sh+first_omitted/(1-ratio_bound))


@lru_cache(maxsize=None)
def log_positive_interval(x, terms=48):
    assert x > 0
    # Scale into [1,2), then use 2 atanh(z); |z| <= 1/3.
    y, power = x, 0
    while y < 1:
        y *= 2
        power -= 1
    while y >= 2:
        y /= 2
        power += 1

    def unit_interval(t):
        z = (t - 1) / (t + 1)
        s = 2 * sum((z ** (2*k + 1) / (2*k + 1)
                     for k in range(terms)), F(0))
        tail = 2 * z ** (2*terms + 1) / (
            (2*terms + 1) * (1 - z*z))
        return s, s + tail

    a, b = unit_interval(y)
    l2, u2 = unit_interval(F(2))
    if power >= 0:
        return outward_dyadic(a+power*l2, b+power*u2)
    return outward_dyadic(a+power*u2, b+power*l2)


def dyadic_nearest(x, bits=44):
    return F(round(float(x) * (1 << bits)), 1 << bits)


def dyadic_floor_nonnegative(x, bits=36):
    return F(max(0, math.floor(float(x) * (1 << bits))), 1 << bits)


def intervals_for_grid(m, A, tau):
    pl, pu = pi_interval()
    dl = [[2*pl*min(abs(i-j), m-abs(i-j))/m
           for j in range(m)] for i in range(m)]
    du = [[2*pu*min(abs(i-j), m-abs(i-j))/m
           for j in range(m)] for i in range(m)]
    cl = [[F(1) for _ in range(m)] for _ in range(m)]
    cu = [[F(1) for _ in range(m)] for _ in range(m)]
    for i in range(m):
        for j in range(m):
            cl[i][j], cu[i][j] = exp_nonnegative_interval(
                A*dl[i][j]/tau, A*du[i][j]/tau)
    return pl, pu, dl, du, cl, cu


def propose_lp(counts, dlow, clow):
    m, n = len(counts), sum(counts)
    nv = m*m + m
    c = np.zeros(nv)
    c[:m*m] = [float(x) for row in dlow for x in row]
    er, ec, ev = [], [], []
    for i in range(m):
        for j in range(m):
            idx = i*m+j
            er.extend([i, m+j])
            ec.extend([idx, idx])
            ev.extend([1.0, 1.0])
    for j in range(m):
        er.append(m+j); ec.append(m*m+j); ev.append(-1.0)
    eq = coo_matrix((ev, (er, ec)), shape=(2*m, nv)).tocsr()
    rhs = np.r_[np.array(counts, dtype=float)/n, np.zeros(m)]
    ur, uc, uv, pairs = [], [], [], []
    for i in range(m):
        for j in range(m):
            if i == j:
                continue
            row = len(pairs)
            pairs.append((i, j))
            ur.extend([row, row])
            uc.extend([m*m+i, m*m+j])
            uv.extend([1.0, -float(clow[i][j])])
    ub = coo_matrix((uv, (ur, uc)), shape=(len(pairs), nv)).tocsr()
    result = linprog(c, A_ub=ub, b_ub=np.zeros(len(pairs)),
                     A_eq=eq, b_eq=rhs, bounds=(0, None), method="highs")
    if not result.success:
        raise RuntimeError(result.message)
    return result, pairs


def repair_probabilities(raw_p, clow):
    m = len(raw_p)
    # A tiny strictly positive rational floor avoids a spurious numerical zero.
    integers = [max(1, round(float(x) * (1 << 36))) for x in raw_p]
    total = sum(integers)
    p0 = [F(k, total) for k in integers]
    lam = F(0)
    for i in range(m):
        for j in range(m):
            if i == j:
                continue
            v = p0[i] - clow[i][j]*p0[j]
            if v > 0:
                slack = (clow[i][j]-1)/m
                lam = max(lam, v/(v+slack))
    p = [(1-lam)*x + lam/m for x in p0]
    return p, lam


def repair_transport(raw_t, a, p):
    m = len(a)
    t = [[dyadic_floor_nonnegative(raw_t[i*m+j])
          for j in range(m)] for i in range(m)]
    rows = [sum(row) for row in t]
    cols = [sum(t[i][j] for i in range(m)) for j in range(m)]
    theta = F(1)
    for want, have in list(zip(a, rows)) + list(zip(p, cols)):
        if have > 0:
            theta = min(theta, want/have)
    t = [[theta*x for x in row] for row in t]
    ar = [a[i]-sum(t[i]) for i in range(m)]
    pr = [p[j]-sum(t[i][j] for i in range(m)) for j in range(m)]
    assert all(x >= 0 for x in ar+pr)
    residual_mass = sum(ar)
    for i in range(m):
        for j in range(m):
            x = min(ar[i], pr[j])
            t[i][j] += x
            ar[i] -= x
            pr[j] -= x
    assert all(x == 0 for x in ar+pr)
    return t, theta, residual_mass


def repair_dual(result, pairs, dlow, clow, m):
    alpha = [dyadic_nearest(x) for x in result.eqlin.marginals[:m]]
    beta = [dyadic_nearest(x) for x in result.eqlin.marginals[m:]]
    z = [[F(0) for _ in range(m)] for _ in range(m)]
    for (i,j), raw in zip(pairs, result.ineqlin.marginals):
        z[i][j] = min(F(0), dyadic_nearest(raw))
    for j in range(m):
        q = sum(z[j][k] for k in range(m) if k != j)
        q -= sum(clow[i][j]*z[i][j] for i in range(m) if i != j)
        beta[j] = max(beta[j], q)
    for i in range(m):
        alpha[i] = min(alpha[i], min(dlow[i][j]-beta[j]
                                     for j in range(m)))
    return alpha, beta, z


def coeff_mixture_bound(clow, chigh):
    m = len(clow)
    lam = F(0)
    for i in range(m):
        for j in range(m):
            if i == j:
                continue
            err = chigh[i][j]-clow[i][j]
            if err == 0:
                continue
            slack = (clow[i][j]-1)/m
            lam = max(lam, err/(err+slack))
    return lam


def verify_exact(a, p, transport, alpha, beta, z, dl, du, cl):
    m = len(a)
    assert sum(a) == sum(p) == 1
    assert all(x > 0 for x in p)
    assert all(x >= 0 for row in transport for x in row)
    assert all(sum(transport[i]) == a[i] for i in range(m))
    assert all(sum(transport[i][j] for i in range(m)) == p[j]
               for j in range(m))
    for i in range(m):
        for j in range(m):
            assert p[i] <= cl[i][j]*p[j]
            assert alpha[i]+beta[j] <= dl[i][j]
            assert z[i][j] <= 0
    for j in range(m):
        q = sum(z[j][k] for k in range(m) if k != j)
        q -= sum(cl[i][j]*z[i][j] for i in range(m) if i != j)
        assert -beta[j]+q <= 0
    primal = sum((transport[i][j]*du[i][j]
                  for i in range(m) for j in range(m)), F(0))
    dual = sum((a[i]*alpha[i] for i in range(m)), F(0))
    assert primal >= dual
    return primal, dual


def serialize(x):
    if isinstance(x, F):
        return str(x)
    if isinstance(x, list):
        return [serialize(y) for y in x]
    if isinstance(x, dict):
        return {k:serialize(v) for k,v in x.items()}
    return x


def decode_vector(x):
    return [F(y) for y in x]


def decode_matrix(x):
    return [decode_vector(row) for row in x]


def create(counts, A, tau, b):
    m, n = len(counts), sum(counts)
    assert m >= 2 and n > 0 and A >= 0 and tau > 0 and b > 0
    assert all(isinstance(k, int) and k >= 0 for k in counts)
    pl, pu, dl, du, cl, cu = intervals_for_grid(m, A, tau)
    result, pairs = propose_lp(counts, dl, cl)
    a = [F(k,n) for k in counts]
    p, pmix = repair_probabilities(result.x[m*m:], cl)
    t, shrink, residual = repair_transport(result.x[:m*m], a, p)
    alpha, beta, z = repair_dual(result, pairs, dl, cl, m)
    primal, dual = verify_exact(a,p,t,alpha,beta,z,dl,du,cl)
    cmix = coeff_mixture_bound(cl,cu)
    eta = primal-dual+pu*cmix
    logs = [log_positive_interval(x) for x in p]
    energies = [[tau*(logs[0][0]-hi), tau*(logs[0][1]-lo)]
                for lo,hi in logs]
    energies[0] = [F(0),F(0)]
    _, eg = exp_nonnegative_interval(
        2*A*(pl/m+b)/tau, 2*A*(pu/m+b)/tau)
    kappa_upper = min(pu, pu/m + pu*min(F(1),(eg-1)/2))
    receipt = {
        "scope":"Deterministic 1D arithmetic fixture; no native observations or iid/entropy certification.",
        "dimension":1, "counts":counts, "A":A, "tau":tau,
        "m":m, "N_histogram":n, "smoothing_mean_displacement_bound":b,
        "pi_interval":[pl,pu], "distance_lower":dl, "distance_upper":du,
        "ratio_lower":cl, "ratio_upper":cu,
        "empirical_probabilities":a, "selected_probabilities":p,
        "primal_transport":t, "dual_row":alpha, "dual_column":beta,
        "dual_ratio":z, "primal_cost_upper":primal, "dual_cost_lower":dual,
        "inner_primal_dual_gap":primal-dual,
        "coefficient_mixture_bound":cmix,
        "total_outer_optimization_error_upper":eta,
        "probability_repair_mixture":pmix,
        "transport_shrink":shrink,"transport_residual_mass":residual,
        "energy_intervals":energies,
        "grid_plus_smoothing_error_upper":kappa_upper,
        "representation":{
            "grid":"x_i = 2 pi i/m in the calibrated native coordinate",
            "potential":"v_i = -tau log(p_i/p_0); V(q)=min_i(v_i+A d_T(q,x_i))",
            "smoothing":"Periodic Gaussian convolution with standard deviation b in d=1; subtract value at zero.",
            "evaluation_scope":"Log and grid intervals supplied. Smooth convolution is represented but not evaluated here; its interval quadrature and force evaluation require their own tolerance/node budget."
        },
        "floating_proposal":{
            "solver":"scipy.optimize.linprog(method=highs)",
            "objective":float(result.fun),
            "iterations":int(result.nit),
            "status":str(result.message)
        },
        "certificate_status":"All primal/dual/ratio/marginal checks passed using exact Fraction arithmetic."
    }
    return receipt


def verify_file(path):
    x = json.loads(path.read_text())
    A, tau = F(x["A"]), F(x["tau"])
    m = x["m"]
    # Recompute all transcendental interval constructions, rather than trust
    # the saved intervals as premises.
    pl,pu,dl,du,cl,cu = intervals_for_grid(m,A,tau)
    assert serialize([pl,pu]) == x["pi_interval"]
    for key, value in [("distance_lower",dl),("distance_upper",du),
                       ("ratio_lower",cl),("ratio_upper",cu)]:
        assert serialize(value) == x[key]
    primal,dual = verify_exact(
        decode_vector(x["empirical_probabilities"]),
        decode_vector(x["selected_probabilities"]),
        decode_matrix(x["primal_transport"]),
        decode_vector(x["dual_row"]), decode_vector(x["dual_column"]),
        decode_matrix(x["dual_ratio"]), dl,du,cl)
    assert primal == F(x["primal_cost_upper"])
    assert dual == F(x["dual_cost_lower"])
    cmix = coeff_mixture_bound(cl,cu)
    assert cmix == F(x["coefficient_mixture_bound"])
    assert primal-dual+pu*cmix == F(x["total_outer_optimization_error_upper"])
    p = decode_vector(x["selected_probabilities"])
    logs = [log_positive_interval(v) for v in p]
    energies = [[tau*(logs[0][0]-hi),tau*(logs[0][1]-lo)]
                for lo,hi in logs]
    energies[0] = [F(0),F(0)]
    assert serialize(energies) == x["energy_intervals"]
    return {"verified":True, "m":m,
            "primal_cost_upper":float(primal),
            "dual_cost_lower":float(dual),
            "total_outer_optimization_error_upper":float(primal-dual+pu*cmix)}


def main():
    if not __debug__:
        raise RuntimeError("Exact certificate checks require Python assertions enabled.")
    ap = argparse.ArgumentParser()
    ap.add_argument("--counts", default="2,4,8,16,18,10,4,2")
    ap.add_argument("--A", default="1")
    ap.add_argument("--tau", default="1")
    ap.add_argument("--b", default="1/20")
    ap.add_argument("--output", type=Path)
    ap.add_argument("--verify", type=Path)
    args = ap.parse_args()
    if args.verify:
        print(json.dumps(verify_file(args.verify), indent=2))
        return
    counts = [int(s) for s in args.counts.split(",")]
    result = create(counts,F(args.A),F(args.tau),F(args.b))
    if args.output:
        args.output.write_text(json.dumps(serialize(result),indent=2)+"\n")
    print(json.dumps({
        "scope":result["scope"], "m":result["m"],
        "primal_cost_upper":float(result["primal_cost_upper"]),
        "dual_cost_lower":float(result["dual_cost_lower"]),
        "inner_primal_dual_gap":float(result["inner_primal_dual_gap"]),
        "coefficient_mixture_bound":float(result["coefficient_mixture_bound"]),
        "total_outer_optimization_error_upper":
            float(result["total_outer_optimization_error_upper"]),
        "selected_probabilities":[float(v) for v in result["selected_probabilities"]],
        "certificate_status":result["certificate_status"]
    },indent=2))


if __name__ == "__main__":
    main()

