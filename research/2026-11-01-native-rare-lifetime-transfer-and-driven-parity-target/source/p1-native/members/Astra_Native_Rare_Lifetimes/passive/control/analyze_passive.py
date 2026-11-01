"""Exact local-interface audit and finite-state evaluation of the passive run.

The acquisition simulator passes only actual state changes/timestamps to its
observer. This file receives the resulting counts and exposure quotas. Truth
parameters below are used for validation after fitting, never for acquisition.
Floating linear solves are diagnostic evaluations, with residuals reported.
"""
from fractions import Fraction as F
from pathlib import Path
import json
import math
import numpy as np
from scipy.linalg import solve

HERE = Path(__file__).resolve().parent


def clip(x, lo, hi):
    return min(hi, max(lo, x))


def fit(counts, R, n):
    """All calculations here are rational. No true parameter enters."""
    q = [clip(F(k, R), F(81, 181), F(100, 181))
         for k in counts[:2*n-1]]
    odds = []
    for i in range(n):
        for right in range(2 if i+1 < n else 1):
            rate = q[2*i+right]
            odds.append((1-rate)/rate if i % 2 == 0 else rate/(1-rate))
    a = [clip(odds[2*i], F(9, 10), F(11, 10)) for i in range(n)]
    b = [clip(odds[2*i+1]/odds[2*i], F(9, 10), F(11, 10))
         for i in range(n-1)]
    alpha = []
    for i in range(n-1):
        nu = F(counts[2*n-1+i], R)
        raw = nu if i % 2 else nu*odds[2*i+1]*odds[2*(i+1)]
        alpha.append(clip(raw, F(1, 2), F(1)))
    return a, b, alpha


def bit(x, i):
    return (x >> i) & 1


def model(a, b, alpha):
    """Return exact product weights and exact aggregate generator rows."""
    n = len(a)
    rows, weights = [], []
    for x in range(1 << n):
        w = F(1)
        for i in range(n):
            if bit(x, i):
                w *= a[i]
        for i in range(n-1):
            if bit(x, i) and bit(x, i+1):
                w *= b[i]
        weights.append(w)
        row = {}
        for i in range(n):
            r = a[i]
            if i > 0 and bit(x, i-1):
                r *= b[i-1]
            if i+1 < n and bit(x, i+1):
                r *= b[i]
            rate = F(1)/(1+r) if bit(x, i) else r/(1+r)
            y = x ^ (1 << i)
            row[y] = row.get(y, F(0)) + rate
        for i in range(n-1):
            old = bit(x, i) + 2*bit(x, i+1)
            if old == 2:
                continue
            v = F(1)
            if bit(x, i):
                v *= a[i]
            if bit(x, i+1):
                v *= a[i+1]
            if i > 0 and bit(x, i-1) and bit(x, i):
                v *= b[i-1]
            if bit(x, i) and bit(x, i+1):
                v *= b[i]
            if i+2 < n and bit(x, i+1) and bit(x, i+2):
                v *= b[i+1]
            nxt = ((3, 0, 2, 1) if i % 2 else (1, 3, 2, 0))[old]
            y = (x & ~(3 << i)) | (nxt << i)
            row[y] = row.get(y, F(0)) + alpha[i]/v
        row[x] = -sum(row.values())
        rows.append(row)
    return weights, rows


def contexts(n):
    result = []
    for i in range(n):
        for right in range(2 if i+1 < n else 1):
            mask, pattern = 1 << i, (1 if i % 2 == 0 else 0) << i
            if i > 0:
                mask |= 1 << (i-1)
            if i+1 < n:
                mask |= 1 << (i+1)
                pattern |= right << (i+1)
            result.append((mask, pattern, 1 << i))
    for i in range(n-1):
        mask, pattern = 3 << i, 0
        if i % 2 == 0:
            pattern = mask
            if i > 0:
                mask |= 1 << (i-1)
            if i+2 < n:
                mask |= 1 << (i+2)
        result.append((mask, pattern, 3 << i))
    return result


def true_context_rates(a, b, alpha):
    n = len(a)
    rates = []
    for i in range(n):
        for right in range(2 if i+1 < n else 1):
            r = a[i]*(b[i] if right else 1)
            rates.append(F(1)/(1+r) if i % 2 == 0 else r/(1+r))
    rates.extend(alpha[i] if i % 2 else alpha[i]/(a[i]*a[i+1]*b[i])
                 for i in range(n-1))
    return rates


def exact_audit(a, b, alpha, weights, rows):
    n = len(a)
    incoming = [F(0)]*(1 << n)
    for x, row in enumerate(rows):
        assert sum(row.values()) == 0
        for y, rate in row.items():
            incoming[y] += weights[x]*rate
    assert all(v == 0 for v in incoming)
    tests = 0
    rates = true_context_rates(a, b, alpha)
    for (mask, pattern, flip), expected in zip(contexts(n), rates):
        for x, row in enumerate(rows):
            if x & mask == pattern:
                assert row.get(x ^ flip, F(0)) == expected
                tests += 1
    # Exact reconstruction from rational intensities, with a common exposure
    # denominator chosen solely for this algebraic audit (not for the run).
    common = math.lcm(*(q.denominator for q in rates))
    counts = [int(q*common) for q in rates]
    assert fit(counts, common, n) == (a, b, alpha)
    return {"exact_stationarity": True,
            "exact_selected_aggregate_intensity_checks": tests,
            "exact_factor_identification": True}


def dense_model(weights, rows):
    Z = sum(weights)
    pi = np.array([float(w/Z) for w in weights])
    Q = np.zeros((len(rows), len(rows)))
    for x, row in enumerate(rows):
        for y, q in row.items():
            Q[x, y] = float(q)
    return pi, Q


def evaluate(pi, Q, mask, pattern, s=F(1, 40), g=F(1, 2)):
    nstates = len(pi)
    A = np.array([x for x in range(nstates) if x & mask == pattern])
    B = np.array([x for x in range(nstates) if x & mask != pattern])
    p = pi[A].sum()
    killed = -Q[np.ix_(B, B)]
    h = solve(killed, np.ones(len(B)))
    M = pi[B] @ h / (1-p)
    u = solve(killed + float(s)*np.eye(len(B)), Q[np.ix_(B,A)].sum(axis=1))
    r = float(s) + (pi[A] @ (Q[np.ix_(A,B)] @ (1-u)))/p
    R = 1/(p*r) - 1/float(s)
    sf = 1+float(s/g)
    lo, hi = R/((1-p)*sf), R*sf/(1-p)
    assert lo <= M <= hi
    return {"p": p, "mean_from_stationary_outside": M,
            "killed_solve_max_relative_residual": float(np.max(abs(killed@h-1))),
            "screened_r": r, "screened_R": R,
            "screened_mean_interval": [lo, hi]}


def main():
    h = json.loads((HERE / "passive_native_history.json").read_text())
    n, R, counts, D = h["n"], h["R"], h["counts"], h["truth_denominator"]
    truth = tuple([F(v, D) for v in h[key]]
                  for key in ("truth_a", "truth_b", "truth_alpha"))
    fitted = fit(counts, R, n)
    tw, tr = model(*truth)
    fw, fr = model(*fitted)
    audit = exact_audit(*truth, tw, tr)
    audit["fitted_model"] = exact_audit(*fitted, fw, fr)
    rates = true_context_rates(*truth)
    eta = F(1, 50)
    Aconst = F(181, 81)
    u = float(Aconst*(3*n-2)*eta)
    alpha_log = -math.log1p(-float(eta)) + 2*float(Aconst*eta)
    v = u+alpha_log
    logfactor = 3*u+(2/math.sqrt(3))*v
    factor = math.exp(logfactor)
    cal_failure = 2*(3*n-2)*math.exp(-R*float(eta)**2/9)
    rate_errors = [float(abs(F(k,R)/theta-1)) for k,theta in zip(counts,rates)]
    parameter_log_errors = [[abs(math.log(float(y/x))) for x,y in zip(xs,ys)]
                            for xs,ys in zip(truth,fitted)]
    exact_weight_log_max = max(abs(math.log(float(y/x))) for x,y in zip(tw,fw))
    gamma = F(729,1729)
    p0 = float(gamma**4)
    delta_exp = .001
    g = .5
    logCn = .5*n*math.log(2)+.5*(2*n-1)*math.log(11/9)
    horizon = max(4*R/p0, 8/(g*p0)*(math.log((3*n-2)/delta_exp)+logCn))
    pit, Qt = dense_model(tw,tr)
    pif, Qf = dense_model(fw,fr)
    targets = {}
    for name,mask,pattern in (("all_eight_ones",(1<<n)-1,(1<<n)-1),
                              ("first_six_ones",(1<<6)-1,(1<<6)-1)):
        true_eval = evaluate(pit,Qt,mask,pattern)
        fit_eval = evaluate(pif,Qf,mask,pattern)
        mean_ratio = fit_eval["mean_from_stationary_outside"]/true_eval["mean_from_stationary_outside"]
        lo,hi = fit_eval["screened_mean_interval"]
        transfer_interval = [lo/factor,hi*factor]
        assert transfer_interval[0] <= true_eval["mean_from_stationary_outside"] <= transfer_interval[1]
        targets[name] = {"true":true_eval,"fitted":fit_eval,
                         "fitted_to_true_mean_ratio":mean_ratio,
                         "certified_true_mean_interval_on_calibration_event":transfer_interval}
    # Useful failure: aggregating both flip directions and taking a naive
    # heatbath ratio is inconsistent in this driven architecture.
    _, flat = model([F(1)]*3,[F(1)]*2,[F(1)]*2)
    naive_ratio=flat[0][2]/flat[2][0]  # site1, both neighbors0
    assert naive_ratio == F(1,3)
    out = {
        "scope":"One seeded numerical interface check; theorem assumes exact ordered event observations and ideal native CTMC law.",
        "n":n,"quota_per_context":R,"contexts":3*n-2,
        "observed_elapsed_time":h["completed_time"],
        "actual_observed_state_changes":h["actual_observed_state_changes"],
        "hidden_source_proposals_charged_as_simulation_work":h["hidden_source_proposals_for_diagnostic_cost_only"],
        "all_exposure_quotas_complete":all(x==R for x in h["exposures"]),
        "eta":float(eta),"calibration_failure_upper_bound":cal_failure,
        "max_observed_context_rate_relative_error":max(rate_errors),
        "all_rates_inside_stated_simultaneous_event":max(rate_errors)<=float(eta),
        "parameter_log_error_maxima_a_b_alpha":[max(z) for z in parameter_log_errors],
        "global_weight_log_error_actual":exact_weight_log_max,
        "global_weight_log_error_upper_bound_u":u,
        "stationary_flow_log_error_upper_bound_v":v,
        "log_mean_transfer_factor":logfactor,"mean_transfer_factor":factor,
        "fitted_rational_a":[str(v) for v in fitted[0]],
        "fitted_rational_b":[str(v) for v in fitted[1]],
        "fitted_rational_alpha":[str(v) for v in fitted[2]],
        "exact_audit":audit,
        "naive_aggregate_flip_ratio_failure":{"actual_ratio":str(naive_ratio),"true_heatbath_odds":"1"},
        "completion_horizon":{"context_stationary_mass_lower_bound":p0,
                              "failure_allowance":delta_exp,"walltime_upper_bound":horizon,
                              "expected_full_event_upper_bound":(3*n-2)*horizon},
        "targets":targets,
        "limitations":["The confidence interval is intentionally broad at this small acquisition budget.",
                       "The source simulator uses a seeded PRNG and floating timestamps; it is a diagnostic realization.",
                       "Full ordered state changes with no missed events are an input assumption.",
                       "The known alternating cycle architecture and known unit heatbath time scale are required.",
                       "No practical superiority over fully informed conventional CTMC likelihood or rare-event solvers is claimed."]}
    (HERE/"passive_results.json").write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({k:out[k] for k in ("n","observed_elapsed_time","actual_observed_state_changes",
          "hidden_source_proposals_charged_as_simulation_work","max_observed_context_rate_relative_error",
          "calibration_failure_upper_bound","mean_transfer_factor","targets")},indent=2))


if __name__ == "__main__":
    main()
