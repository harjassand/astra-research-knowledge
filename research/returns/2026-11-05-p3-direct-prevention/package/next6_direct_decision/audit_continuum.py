#!/usr/bin/env python3
"""Deterministic synthetic diagnostics, not physical or generic-oracle execution.

Independent-bit formulas are the strongest ordinary reference for this subclass.
The generic theorem is not benchmarked against a deliberately weak simulator.
"""
from __future__ import annotations

import hashlib
import json
import math
import platform
import time
from pathlib import Path

import numpy as np
import scipy
import mpmath as mp
from scipy.integrate import quad_vec
from scipy.linalg import solve
from scipy.optimize import minimize

ROOT = Path(__file__).resolve().parent


def product_objective(q, rates, controls, *, h=None):
    """Return p*M, its gradient and optional directional Hessian by quadrature."""
    q, rates, controls = map(np.asarray, (q, rates, controls))
    n = len(q)
    logp = float(np.log(q).sum())
    p = math.exp(logp)
    a = 1.0 - p
    scale = float(np.dot(controls * rates, 1.0 - q))

    def integrand(s):
        t = s / scale
        e = np.exp(-controls * rates * t)
        factors = q + (1.0 - q) * e
        prod = math.exp(float(np.log(factors).sum()))
        value = max(prod - p, 0.0)
        w = rates * (1.0 - q) * e / factors
        grad = -t * prod * w
        out = np.r_[value, grad]
        if h is not None:
            w_h = float(np.dot(w, h))
            second = t*t*prod*(w_h*w_h + float(np.dot(h*h, rates*w-w*w)))
            out = np.r_[out, second]
        return out / (a * scale)

    value, err = quad_vec(integrand, 0.0, np.inf,
                          epsabs=2e-12, epsrel=2e-11, limit=600)
    return {
        "objective": float(value[0]),
        "gradient": np.asarray(value[1:n+1]),
        "directional_hessian": None if h is None else float(value[-1]),
        "quadrature_estimated_norm_error": float(err),
        "target_probability": p,
        "log_target_probability": logp,
    }


def explicit_objective(q, rates, controls):
    n = len(q)
    size = 1 << n
    pi = np.empty(size)
    Q = np.zeros((size, size))
    for x in range(size):
        bits = np.array([(x >> i) & 1 for i in range(n)])
        pi[x] = np.prod(np.where(bits, q, 1.0-q))
        for i in range(n):
            Q[x, x ^ (1 << i)] = controls[i]*rates[i]*(1.0-q[i] if bits[i] else q[i])
        Q[x, x] = -Q[x].sum()
    target = size - 1
    safe = np.arange(size-1)
    mean = solve(-Q[np.ix_(safe, safe)], np.ones(size-1), assume_a="gen")
    M = float(pi[safe] @ mean / (1.0-pi[target]))
    return pi[target]*M, pi, Q


def greedy_linear_minimizer(gradient, costs, budget, cap):
    controls = np.ones_like(gradient)
    remain = float(budget)
    for j in np.argsort(gradient / costs):
        if gradient[j] >= 0 or remain <= 0:
            break
        add = min(cap-1.0, remain / costs[j])
        controls[j] += add
        remain -= costs[j]*add
    return controls


def family(n):
    j = np.arange(n, dtype=float)
    q = .35 + .48*((j*.6180339887498949+.17) % 1.0)
    rates = .5 + 1.5*((j*.4142135623730951+.43) % 1.0)
    costs = .75 + .5*((j*.7320508075688772+.31) % 1.0)
    cap = 3.0
    budget = .7*float(costs.sum())
    controls = np.full(n, 1.7)
    initial = product_objective(q, rates, controls)
    best_gap = math.inf
    best = None
    max_err = initial["quadrature_estimated_norm_error"]
    iterations = 0
    start = time.monotonic()
    for it in range(1000):
        current = product_objective(q, rates, controls)
        max_err = max(max_err, current["quadrature_estimated_norm_error"])
        s = greedy_linear_minimizer(current["gradient"], costs, budget, cap)
        gap = float(current["gradient"] @ (controls-s))
        if gap < best_gap:
            best_gap = gap
            best = (controls.copy(), current, gap)
        iterations = it+1
        if gap <= 2e-5*current["objective"]:
            break
        gamma = 2.0/(it+2.0)
        controls = (1.0-gamma)*controls + gamma*s
    controls, final, gap = best

    # Strong ordinary reference: a nonlinear optimizer on the same factorized
    # quadrature, not a global Markov trajectory simulator.
    cache = {}
    def both(x):
        key = tuple(x)
        if key not in cache:
            cache.clear()
            cache[key] = product_objective(q, rates, x)
        return cache[key]
    opt = minimize(lambda x: both(x)["objective"], controls,
                   jac=lambda x: both(x)["gradient"], method="SLSQP",
                   bounds=[(1.0, cap)]*n,
                   constraints=[{"type":"ineq",
                                 "fun":lambda x: budget - float(costs @ (x-1.0)),
                                 "jac":lambda x: -costs}],
                   options={"ftol":1e-12,"maxiter":1500})
    ordinary = product_objective(q, rates, opt.x)
    p = final["target_probability"]
    R = 2.0*(cap+1.0)*float(rates.sum())
    g = float(rates.min()/R)
    return {
        "N": n,
        "global_states": str(1 << n),
        "target_probability": p,
        "log10_target_probability": final["log_target_probability"] / math.log(10),
        "uniform_control_p_times_mean": initial["objective"],
        "fw_p_times_mean": final["objective"],
        "fw_duality_gap": gap,
        "fw_relative_gap": gap/final["objective"],
        "fw_iterations": iterations,
        "ordinary_SLSQP_p_times_mean": ordinary["objective"],
        "ordinary_SLSQP_success": bool(opt.success),
        "ordinary_SLSQP_message": str(opt.message),
        "fw_excess_over_ordinary_relative": final["objective"]/ordinary["objective"]-1.0,
        "improvement_vs_equal_allocation_factor": initial["objective"]/final["objective"],
        "physical_mean_at_fw": final["objective"]/p,
        "normalized_gap_certificate": g,
        "common_uniformizer": R,
        "used_budget": float(costs @ (controls-1.0)),
        "budget": budget,
        "control_min": float(controls.min()),
        "control_max": float(controls.max()),
        "max_quadrature_estimated_norm_error": max_err,
        "elapsed_seconds": time.monotonic()-start,
        "controls": controls.tolist(),
        "q": q.tolist(),
        "rates": rates.tolist(),
        "costs": costs.tolist(),
    }


def correlated_scalar_audit():
    """High precision non-product check of the new short scalar interface."""
    mp.mp.dps = 90
    n = 3
    rates = [mp.mpf("0.8"), mp.mpf("1.2"), mp.mpf("1.6")]
    controls = [mp.mpf("1.3"), mp.mpf("2.7"), mp.mpf("1.8")]
    fields = [mp.mpf("-12"), mp.mpf("-11"), mp.mpf("-13")]
    interactions = {(0,1):mp.mpf("0.7"), (1,2):mp.mpf("-0.4")}
    size = 1 << n
    W = []
    Q = mp.matrix(size,size)
    for x in range(size):
        bits = [(x >> i) & 1 for i in range(n)]
        energy = sum(fields[i]*bits[i] for i in range(n))
        energy += sum(j*bits[i]*bits[k] for (i,k),j in interactions.items())
        W.append(mp.exp(energy))
        for i in range(n):
            logit = fields[i]
            for (j,k),coupling in interactions.items():
                if j == i: logit += coupling*bits[k]
                if k == i: logit += coupling*bits[j]
            q = 1/(1+mp.exp(-logit))
            Q[x,x^(1<<i)] = controls[i]*rates[i]*(1-q if bits[i] else q)
        Q[x,x] = -sum(Q[x,j] for j in range(size) if j != x)
    Z = sum(W)
    pi = [w/Z for w in W]
    p = pi[-1]
    a = 1-p
    R = 8*sum(rates)
    # Conservative influence bound tanh(|J|/4) <= |J|/4.
    row_bound = max(sum(abs(j)/4 for pair,j in interactions.items() if i in pair) for i in range(n))
    g = min(rates)*(1-row_bound)/R
    P = mp.eye(size)+Q/R
    PA = P[:size-1,:size-1]
    K = mp.eye(size-1)-PA
    v = mp.matrix([1]*(size-1))
    mean_steps = mp.lu_solve(K,v)
    f = p/a*sum(pi[i]*mean_steps[i] for i in range(size-1))
    nu = mp.mpf("0.02")
    xi = nu*g/64
    L = int(mp.ceil(mp.log(4/(g*xi),2)))
    k = int(mp.ceil(L/g))
    p_gate = xi/(2*k)
    assert p < p_gate
    survived = (PA**k)*v
    z = sum(P[size-1,i]*survived[i] for i in range(size-1))
    discrepancy = abs(f-1/z)
    assert z >= g/4
    assert discrepancy <= nu/4
    return {"N":n,"interacting":True,"precision_decimal_digits":mp.mp.dps,
            "target_probability":str(p),"normalized_gap_lower_bound":str(g),
            "potential_updates_after_exit":k,"rare_gate":str(p_gate),
            "exact_high_precision_p_R_times_mean":str(f),
            "short_no_return_probability":str(z),
            "scalar_reciprocal":str(1/z),
            "scalar_approximation_error":str(discrepancy),
            "theorem_error_allowance":str(nu/4),
            "note":"Deterministic high-precision matrix check; conditional sampler and operating coins were not executed."}


def main():
    rng = np.random.default_rng(6951307)
    small = []
    for n in (2, 3, 4, 5, 6, 7):
        q = rng.uniform(.3, .8, size=n)
        rates = rng.uniform(.5, 2.0, size=n)
        controls = rng.uniform(1.0, 3.0, size=n)
        h = rng.uniform(-1.0, 1.0, size=n)
        value = product_objective(q, rates, controls, h=h)
        explicit, pi, Q = explicit_objective(q, rates, controls)
        R = 8.0*float(rates.sum())
        g = float(rates.min()/R)
        mismatch = abs(value["objective"] - explicit)
        homogeneity = abs(float(controls @ (-value["gradient"])) - value["objective"])
        second_norm = R*value["directional_hessian"]
        second_bound = 2.0*float(np.max(np.abs(h)))**2 / g
        assert mismatch <= 2e-10
        assert homogeneity <= 2e-10
        assert second_norm >= -1e-10 and second_norm <= second_bound
        assert np.all(value["gradient"] <= 1e-12)
        small.append({
            "N":n, "explicit_p_times_mean":float(explicit),
            "product_p_times_mean":value["objective"],
            "absolute_cross_representation_error":mismatch,
            "homogeneity_error":homogeneity,
            "normalized_directional_hessian":second_norm,
            "theorem_directional_hessian_bound":second_bound,
            "max_detailed_balance_error":float(np.max(np.abs(pi[:,None]*Q-(pi[:,None]*Q).T))),
        })
    results = []
    for n in (8, 16, 32, 64, 128):
        out = family(n)
        results.append(out)
        print(json.dumps({k:out[k] for k in ("N","target_probability","fw_relative_gap",
                     "improvement_vs_equal_allocation_factor","physical_mean_at_fw")}), flush=True)
    record = {
        "scope":"Floating deterministic synthetic audit; no physical service, no general correlated sampler, no conservative confidence schedule executed.",
        "small_identity_checks":small,
        "correlated_short_scalar_identity":correlated_scalar_audit(),
        "growing_family":results,
        "environment":{"python":platform.python_version(), "numpy":np.__version__,
                       "scipy":scipy.__version__, "platform":platform.platform()},
        "source_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    (ROOT/"continuum_execution.json").write_text(json.dumps(record,indent=2)+"\n")


if __name__ == "__main__":
    main()
