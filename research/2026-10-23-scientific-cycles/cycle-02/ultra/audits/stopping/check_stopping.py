#!/usr/bin/env python3
"""Finite falsification checks for the exact stopping-method obstruction.

The theorem is in PROOF.txt. This script checks actual small density matrices,
not only the scalar-tail relaxation, then verifies the joint-tail tangent bound
with a finite LP. All large-N rows use exact finite classical formulas.
"""
import itertools
import json
import math
import os
from pathlib import Path
import resource
import sys
import time
import warnings

import numpy as np
import scipy
from scipy.optimize import linprog


def tensor(items):
    x = np.ones((1, 1))
    for item in items:
        x = np.kron(x, item)
    return x


def entropy(eigenvalues):
    a = np.asarray(eigenvalues)
    a = a[a > 1e-13]
    return float(-np.dot(a, np.log(a)))


def stop_laws(d, n, w):
    a = 1.0 / d
    g = np.array([(1 - a) * a**k for k in range(n)] + [a**n])
    p = np.array([
        (1 - a) * sum(w[h] * a ** (k-h) for h in range(k+1))
        for k in range(n)
    ] + [sum(w[h] * a ** (n-h) for h in range(n+1))])
    ratio = np.cumsum(np.asarray(w) * d ** np.arange(n+1))
    return p, g, ratio


def dense_case(d, n, w):
    v = np.zeros(d*d)
    v[::d+1] = 1/math.sqrt(d)
    phi = np.outer(v, v)
    chi = np.diag(np.diag(phi))
    rho = sum(w[h] * tensor([phi]*h + [chi]*(n-h)) for h in range(n+1))
    sigma = tensor([chi]*n)
    proj = [tensor([phi]*h + [np.eye(d*d)]*(n-h)) for h in range(n+1)]
    effects = [proj[k] - proj[k+1] for k in range(n)] + [proj[n]]
    actual_p = np.array([np.trace(e @ rho).real for e in effects])
    actual_g = np.array([np.trace(e @ sigma).real for e in effects])
    p, g, ratio = stop_laws(d, n, w)
    live = p > 0
    classical_d = float(p[live] @ np.log(p[live]/g[live]))
    er = n*math.log(d) - entropy(np.linalg.eigvalsh(rho))
    assert np.max(np.abs(actual_p-p)) < 1e-11
    assert np.max(np.abs(actual_g-g)) < 1e-11
    assert np.max(np.abs(p-g*ratio)) < 1e-11
    assert abs(classical_d-er) < 1e-10
    return {
        "D": d, "N": n, "weights": [float(x) for x in w],
        "stopping_law": p.tolist(), "geometric_comparator": g.tolist(),
        "monotone_likelihood": ratio.tolist(),
        "relative_entropy_by_physical_spectrum": er,
        "relative_entropy_by_stopping_record": classical_d,
        "max_physical_probability_error": float(np.max(np.abs(actual_p-p))),
    }


def joint_lp(d, n, r, w):
    p, g, ratio = stop_laws(d, n, w)
    cells = np.array(list(itertools.product(range(n+1), repeat=r)), dtype=int)
    thresholds = cells[np.any(cells > 0, axis=1)]
    # Rectangular joint-tail constraints include zero thresholds as I.
    matrix = np.array([np.all(cells >= i, axis=1).astype(float) for i in thresholds])
    bounds = np.array([d ** (-float(np.sum(i))) for i in thresholds])
    objective = np.prod(ratio[cells], axis=1)
    fit = linprog(-objective, A_ub=matrix, b_ub=bounds,
                  A_eq=np.ones((1,len(cells))), b_eq=np.ones(1),
                  bounds=(0,None), method="highs")
    assert fit.success, fit.message
    maximum = -float(fit.fun)
    assert abs(maximum-1) < 1e-9
    p_prod = np.prod(p[cells], axis=1)
    g_prod = np.prod(g[cells], axis=1)
    live = p_prod > 0
    relative = float(p_prod[live] @ np.log(p_prod[live]/g_prod[live]))
    single_live = p > 0
    single = float(p[single_live] @ np.log(p[single_live]/g[single_live]))
    assert abs(relative-r*single) < 1e-10
    moment_rows=[]
    for alpha in [0.5,2.0]:
        moment=objective**alpha
        fit_alpha=linprog(-moment,A_ub=matrix,b_ub=bounds,
                         A_eq=np.ones((1,len(cells))),b_eq=np.ones(1),
                         bounds=(0,None),method="highs")
        assert fit_alpha.success,fit_alpha.message
        achieved=-float(fit_alpha.fun)
        comparator=float(g_prod@moment)
        assert abs(achieved-comparator)<1e-8
        moment_rows.append({"alpha":alpha,"LP_max":achieved,
                            "geometric_comparator_value":comparator})
    return {"D":d, "N":n, "copies":r, "LP_cells":len(cells),
            "LP_joint_tail_constraints":len(thresholds),
            "max_joint_likelihood_expectation": maximum,
            "product_relative_entropy":relative,
            "copies_times_single":r*single,
            "Renyi_likelihood_moment_LPs":moment_rows,
            "scope":"LP checks scalar joint-tail implication only; dense cases bind physical inputs"}


def conditional_counterexample():
    # Actual globally A:B-separable local-Bell state, ordered A1,B1,A2,B2.
    local_bells=np.zeros((2,2,2,2))
    for a,b in itertools.product(range(2),repeat=2):
        local_bells[a,b,a,b]=0.5
    psi=local_bells.reshape(-1)
    rho=np.outer(psi,psi)
    v=np.array([1.0,0.0,0.0,1.0])/math.sqrt(2)
    phi=np.outer(v,v)
    first=float(np.trace(np.kron(phi,np.eye(4))@rho))
    both=float(np.trace(np.kron(phi,phi)@rho))
    assert abs(first-0.25)<1e-12 and abs(both-0.25)<1e-12
    conditional=4*both/first
    assert conditional>2
    return {"first_Bell_success":first,"both_Bell_successes":both,
            "second_success_given_first":both/first,
            "M1_on_first_success":2,
            "conditional_expected_M2_on_first_success":conditional,
            "unconditional_expected_M1":2*first,
            "unconditional_expected_M2":4*both,
            "verdict":"Fixed-horizon bound holds; supermartingale property fails",
            "provenance":"Principal reviewer supplied counterexample; replay independently contracts its physical state",
            "optional_time_claim":"UNPROVED, not inferred"}


def uniform_row(d, n):
    a=1.0/d
    m=math.log(d)
    k=np.arange(n+1)
    p=(1-a**k)/n
    p[-1]/=(1-a)
    logg=k*(-m)+math.log1p(-a)
    logg[-1]=-n*m
    live=p>0
    logs=np.zeros(n+1)
    logs[live]=np.log(p[live])-logg[live]
    er=float(p[live]@logs[live])
    mean=float(p@k)
    h=er-(n+1)*m/2+math.log(n)
    c=-math.log1p(-a)+m/(d-1)
    constant=min(2*d-m, m/(1-d**(-0.5))**2)
    if d==2:
        constant=min(constant,2-m)
    b=(n+1)*m/2
    assert abs(float(np.sum(p))-1)<1e-12
    assert -1e-9<=h<=c+1e-9
    assert er<=b+1e-9
    return {"D":d,"N":n,"return_half_trace":(1-a**n)/n,
            "mean_stopping_length":mean,"stopping_entropy":entropy(p),
            "ER_exact":er,"mean_Bell_supply":b,"EC_lower":b-constant,
            "EC_minus_ER_lower":b-constant-er,
            "conditional_stock_entropy":h,"conditional_entropy_upper":c,
            "log_likelihood_variance":float(p@((logs-er)**2)),
            "scope":"EC bound inherited from audited Restore witness and established MC additivity"}


def main():
    started=time.perf_counter()
    cpu=time.process_time()
    rng=np.random.default_rng(20261022)
    dense=[]
    for d,n in [(2,1),(2,2),(2,3),(2,4),(3,1),(3,2)]:
        uniform=np.array([0.0]+[1/n]*n)
        dense.append(dense_case(d,n,uniform))
        w=rng.dirichlet(np.ones(n+1))
        dense.append(dense_case(d,n,w))
    lps=[]
    for d,n,r in [(2,2,2),(2,3,2),(3,2,2),(2,2,3)]:
        lps.append(joint_lp(d,n,r,rng.dirichlet(np.ones(n+1))))
    rows=[uniform_row(d,n) for d in [2,3,4] for n in [2,8,32,128,512,2048]]
    swapping=conditional_counterexample()
    rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    rss_bytes=int(rss if sys.platform=="darwin" else rss*1024)
    result={"status":"PASS", "date":"2026-10-22", "seed":20261022,
            "dense_physical_cases":dense, "joint_tail_LPs":lps,
            "uniform_inventory_rows":rows,
            "conditional_supermartingale_counterexample":swapping,
            "observed_cost":{"body_wall_seconds":time.perf_counter()-started,
                             "body_CPU_seconds":time.process_time()-cpu,
                             "peak_process_RSS_bytes":rss_bytes,
                             "full_scientific_cost":"UNKNOWN",
                             "python":sys.version,"numpy":np.__version__,
                             "scipy":scipy.__version__,
                             "OMP_NUM_THREADS":os.environ.get("OMP_NUM_THREADS"),
                             "OPENBLAS_NUM_THREADS":os.environ.get("OPENBLAS_NUM_THREADS")},
            "limitations":["Finite checks do not prove universal inequalities",
                            "No convex-roof optimization was performed",
                            "The test is a mathematical converse observation, not an LOCC implementation",
                            "No claim of experimental access or historical novelty"]}
    path=Path(__file__).resolve().parent/"RESULT.json"
    path.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"status":"PASS","dense_physical_cases":len(dense),
                      "joint_tail_LPs":len(lps),"large_uniform_rows":len(rows),
                      "body_wall_seconds":result["observed_cost"]["body_wall_seconds"],
                      "result":str(path)},indent=2))


if __name__=="__main__":
    main()
