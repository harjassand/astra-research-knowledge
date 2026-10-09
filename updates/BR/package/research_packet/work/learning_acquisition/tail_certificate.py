"""Acquired scalar LTI FIR tail certificate; classical recurrence corollary.

Run: python3 work/learning_acquisition/tail_certificate.py
No system-order or pole-radius estimation is performed. These are supplied
promises. Numerical runs are diagnostics, not interval-arithmetic certificates.
Sequence convention: g_k=C A**k B, observed at physical time k+1 after a
zero-state unit impulse at time 0. An arbitrary direct-feedthrough tap D is
excluded and must be estimated separately or the degree cap increased by one.
"""
from fractions import Fraction as F
from math import ceil, comb, log
from pathlib import Path
import json
import random
import time
import numpy as np


def weights(d, r):
    """Positive formula; exact for Fraction input, no subtractive cancellation."""
    return [r ** (d-j) * sum(F(comb(m, d-1-j), 1) /
            (1-r) ** (m+1) for m in range(d-1-j, d)) for j in range(d)]


def coefficient_bound(d, rho, k, initial_abs):
    return sum(initial_abs[j] * comb(k, j) * comb(k-j-1, d-j-1)
               * rho ** (k-j) for j in range(d))


def polynomial(roots):
    p = [F(1)]
    for root in roots:
        q = [F(0)] * (len(p)+1)
        for i, a in enumerate(p):
            q[i] -= root*a
            q[i+1] += a
        p = q
    return p


def recur(p, initials, horizon):
    d = len(initials)
    g = list(initials)
    while len(g) < horizon:
        k = len(g)-d
        g.append(-sum(p[j]*g[k+j] for j in range(d)))
    return g


def exact_tail_upper(estimates, b, d, rho, s):
    """Exact certificate for rational observations and deterministic error bars."""
    if len(estimates) < d*s:
        raise ValueError("Need at least d*s observations")
    w = weights(d, rho**s)
    offset = len(estimates)-d*s
    return sum(w[j]*(abs(estimates[offset+r+j*s])+b)
               for r in range(s) for j in range(d))


def exact_checks():
    rng = random.Random(91241)
    inequalities = equalities = 0
    for d in range(1, 9):
        rho = F(3, 4)
        w = weights(d, rho)
        assert sum(w) == (((1+rho)/(1-rho))**d-1)/2
        for _ in range(16):
            roots = [F(rng.randrange(-9, 10), 12) for _ in range(d)]
            initial = [F(rng.randrange(-20, 21), 20) for _ in range(d)]
            g = recur(polynomial(roots), initial, 35)
            for k in range(d, 35):
                assert abs(g[k]) <= coefficient_bound(d, rho, k, list(map(abs, initial)))
                inequalities += 1
        eps = [F(j+1, d) for j in range(d)]
        initial = [(-1)**(d-1-j)*eps[j] for j in range(d)]
        g = recur(polynomial([rho]*d), initial, 35)
        for k in range(d, 35):
            assert g[k] == coefficient_bound(d, rho, k, eps)
            equalities += 1
        assert sum(weights(d, F(1, 2*d))) <= 1
    # Exact acquired-data certificates with arbitrary bounded rational noise.
    # All true tail terms here are positive from d onward, so the infinite
    # reference tail is itself a rational number from the sharpness formula.
    certificates = 0
    for d in range(1, 6):
        rho, noise = F(3, 4), F(1, 1000)
        s = stride_for(d, float(rho))
        eps = [F(j+1, d) for j in range(d)]
        initial = [(-1)**(d-1-j)*eps[j] for j in range(d)]
        h = 2*d*s
        g = recur(polynomial([rho]*d), initial, h)
        exact_tail = sum(a*w for a, w in zip(eps, weights(d, rho))) - sum(g[d:])
        measured = [v+(-1)**j*noise for j, v in enumerate(g)]
        assert 0 <= exact_tail <= exact_tail_upper(measured, noise, d, rho, s)
        certificates += 1
    return dict(exact_rational_inequalities=inequalities,
                exact_sharpness_equalities=equalities,
                exact_weight_sum_identities=8, exact_decimation_bounds=8,
                exact_noisy_infinite_tail_certificates=certificates)


def stride_for(d, rho):
    if rho == 0:
        return 1
    s = max(1, ceil(log(2*d)/(-log(rho))))
    while rho**s > 1/(2*d):
        s += 1
    return s


def tail_upper(estimates, b, d, rho, s):
    """Uses trailing d*s samples; valid on simultaneous coefficient event."""
    w = np.array(weights(d, rho**s), dtype=float)
    window = np.abs(estimates[-d*s:]).reshape(d, s) + b
    return float(np.sum(w[:, None] * window))


def identify(impulse, d, rho, eta, sigma, delta, seed, max_epochs=8):
    """Actual simulated repeated reset/impulse observations, streamed by run.

    Estimator sees only returned observations; known impulse is simulator/evaluator.
    Fresh N_m resets at each doubled horizon, all acquisitions fully charged.
    """
    rng = np.random.default_rng(seed)
    s = stride_for(d, rho)
    v = float(s*sum(weights(d, rho**s)))
    total_observations = resets = 0
    rows = []
    for epoch in range(max_epochs):
        h = d*s*2**epoch
        delta_m = delta/2**(epoch+1)
        b = eta/(4*(h+v))
        n = max(1, ceil(2*sigma*sigma/(b*b)*log(2*h/delta_m)))
        total = np.zeros(h)
        truth = impulse(np.arange(h))
        for _ in range(n):
            # This generates every charged sensor observation, no mean shortcut.
            total += truth+rng.normal(0, sigma, h)
        estimate = total/n
        total_observations += n*h
        resets += n
        tail = tail_upper(estimate, b, d, rho, s)
        contiguous_tail = tail_upper(estimate, b, d, rho, 1)
        error_cert = h*b+tail
        exact_head_error = float(np.sum(np.abs(estimate-truth)))
        # Diagnostic reference, finite summation to 20000 only; not proof of tail.
        tail_20000 = float(np.sum(np.abs(impulse(np.arange(h, 20000)))))
        rows.append(dict(epoch=epoch, horizon=h, resets=n,
                         sensor_observations=n*h, b=b, acquired_tail_bound=tail,
                         contiguous_tail_bound=contiguous_tail,
                         certified_error=error_cert,
                         observed_head_max_error=float(np.max(np.abs(estimate-truth))),
                         diagnostic_error_to_20000=exact_head_error+tail_20000))
        if error_cert <= eta:
            return dict(status="NUMERICAL_CERTIFICATE_DIAGNOSTIC",
                        stride=s, degree_cap=d, radius_bound=rho,
                        target=eta, sigma=sigma, failure_probability=delta,
                        total_sensor_observations=total_observations,
                        total_resets=resets, rows=rows)
    return dict(status="UNKNOWN_BUDGET_EXHAUSTED", rows=rows,
                total_sensor_observations=total_observations, total_resets=resets)


def main():
    start = time.perf_counter()
    report = {"status": "INTERNAL_DIAGNOSTIC_CLASSICAL_COROLLARY_NO_NOVELTY_CLAIM",
              "algebra": exact_checks(), "experiments": {}}
    cases = {
      "near_unit_scalar_declared_degree_3": lambda k: .05*.95**k,
      "signed_two_poles": lambda k: .1*(-.9)**k+.005*.95**k,
      "repeated_pole_transient": lambda k: ((k+1)*(k+2)/2)*.05**3*.95**k,
    }
    for name, impulse in cases.items():
        runs = [identify(impulse, 3, .95, .1, 1e-4, .01, seed)
                for seed in range(6)]
        report["experiments"][name] = runs
    report["elapsed_seconds"] = time.perf_counter()-start
    output = Path(__file__).with_name("diagnostics.json")
    output.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({"algebra": report["algebra"], "elapsed_seconds": report["elapsed_seconds"],
       "experiments": {name: {"runs": len(runs), "statuses": sorted(set(r["status"] for r in runs)),
         "final_horizons": sorted(set(r["rows"][-1]["horizon"] for r in runs)),
         "total_observations": sorted(set(r["total_sensor_observations"] for r in runs)),
         "max_diagnostic_error": max(r["rows"][-1]["diagnostic_error_to_20000"] for r in runs)}
       for name, runs in report["experiments"].items()}}, indent=2))


if __name__ == "__main__":
    main()
