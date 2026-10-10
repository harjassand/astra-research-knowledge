#!/usr/bin/env python3
"""Reproduce E1 Gaussian-seed cat obstruction and entropy-metric checks.

This is numerical support for the analytic derivation in e1_construction.txt.
It is not an interval certificate or a quantum-capacity solver.
Dependencies: Python standard library and NumPy. No source-repository edits.
"""
import json
import math
from pathlib import Path

import numpy as np


def pure_seed(eta, nu, s):
    a = 1.0 - eta
    v = 2.0 * nu + 1.0
    cross = math.sqrt(eta * (v * v - 1.0))
    q = eta * s + a * v
    p = eta / s + a * v
    w2 = q * p
    t = math.sqrt(max(0.0, 1.0 - 1.0 / w2))
    vq = np.array([[a * s + eta * v, cross], [cross, v]])
    vp = np.array([[a / s + eta * v, -cross], [-cross, v]])
    proj_q = (vq @ vp - np.eye(2)) / (w2 - 1.0)
    proj_p = (vp @ vq - np.eye(2)) / (w2 - 1.0)
    half_inv_q = np.linalg.inv(vq) @ (
        np.eye(2) - t / (1.0 + t) * proj_q
    )
    half_inv_p = np.linalg.inv(vp) @ (
        np.eye(2) - t / (1.0 + t) * proj_p
    )
    cb = np.array([eta / (2.0 * q * (1.0 + t)),
                   eta / (2.0 * p * (1.0 + t))])
    ce = a / 2.0 * np.array([half_inv_q[0, 0], half_inv_p[0, 0]])
    numerator = eta * eta - a * a * v * v - a * a * (v * v - 1.0) / t
    k = numerator / (2.0 * (1.0 + t) * w2)
    closed_difference = k * np.array([1.0 / s, s])
    return cb, ce, closed_difference


def gaussian_entropy(lam):
    n = max(0.0, (lam - 1.0) / 2.0)
    return 0.0 if n == 0.0 else ((n + 1.0) * math.log(n + 1.0)
                                - n * math.log(n)) / math.log(2.0)


def entropy_metric(eta, nu, s, c):
    """Mixed Gaussian seed: local binary Holevo curvature in nats/dq^2.

    Input covariance is c*diag(s,1/s), c>1. Displacement difference is dq.
    Curvature is the relative-entropy/BKM curvature, not SLD QFI/8.
    """
    a = 1.0 - eta
    v = 2.0 * nu + 1.0
    cross = math.sqrt(eta * (v * v - 1.0))
    q = eta * c * s + a * v
    p = eta * c / s + a * v
    wb = math.sqrt(q * p)
    vq = np.array([[a * c * s + eta * v, cross], [cross, v]])
    vp = np.array([[a * c / s + eta * v, -cross], [-cross, v]])
    kk = vq @ vp
    tr = float(np.trace(kk))
    det = float(np.linalg.det(vq) * np.linalg.det(vp))
    lp2 = (tr + math.sqrt(max(0.0, tr * tr - 4.0 * det))) / 2.0
    lm2 = det / lp2
    lp, lm = math.sqrt(lp2), math.sqrt(lm2)
    proj = (kk - lm2 * np.eye(2)) / (lp2 - lm2)

    def f(lam):
        return lam * math.log((lam + 1.0) / (lam - 1.0)) / 2.0

    fmat = np.linalg.inv(vq) @ (f(lp) * proj + f(lm) * (np.eye(2) - proj))
    kb = eta * f(wb) / (4.0 * q)
    ke = a * fmat[0, 0] / 4.0
    sld_b = eta / (4.0 * q)
    sld_e = a * np.linalg.inv(vq)[0, 0] / 4.0
    ic = gaussian_entropy(wb) - gaussian_entropy(lp) - gaussian_entropy(lm)
    return dict(c=c, eta=eta, nu=nu, s=s, lambda_E_small=lm,
                seed_Ic_bits=ic, BKM_B=kb, BKM_E=ke,
                BKM_difference=kb-ke, SLD_over_8_difference=sld_b-sld_e)


def critical_eta(nu, s):
    v = 2.0 * nu + 1.0

    def numerator(eta):
        a = 1.0 - eta
        w2 = (eta * s + a * v) * (eta / s + a * v)
        t = math.sqrt(1.0 - 1.0 / w2)
        return eta * eta - a * a * v * v - a * a * (v * v - 1.0) / t

    lo, hi = v / (v + 1.0) + 1e-10, 1.0 - 1e-6
    for _ in range(90):
        mid = (lo + hi) / 2.0
        if numerator(mid) > 0.0:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2.0


def binary_entropy(x):
    if x <= 0.0 or x >= 1.0:
        return 0.0
    return (-x * math.log(x) - (1.0-x) * math.log1p(-x)) / math.log(2.0)


def all_sector_single_photon(eta, nu, d):
    """Exact all-output-sector coherent information for I_one-photon/d.

    No output sector is postselected or erased. Sectors above M are omitted
    only from the numerical sum, with a geometric upper tail bound.
    """
    b = (1.0 - eta) * nu
    gain = 1.0 + b
    tau = eta / gain
    mean = d * b + eta
    variance_upper = (d + 1) * b * gain + 1.0
    cutoff = int(math.ceil(mean + 14.0 * math.sqrt(variance_upper) + 80.0))
    ic = 0.0
    total_probability = 0.0
    last_vac = 0.0
    last_one = 0.0
    for photons in range(cutoff+1):
        log_dim = (math.lgamma(photons+d) - math.lgamma(photons+1)
                   - math.lgamma(d))
        log_vac = (log_dim + photons * math.log(b)
                   - (photons+d) * math.log(gain))
        wvac = math.exp(log_vac)
        wone = wvac * photons / (b*d)
        weight = (1.0-tau) * wvac + tau*wone
        total_probability += weight
        ratio_dims = 0.0 if photons == 0 else photons / (photons+d-1.0)
        beta = (1.0-tau) + tau * photons / (b*d)
        plus = (ratio_dims / d * ((1.0-tau)
                 + tau/b*(photons+d-1.0)) / beta)
        # Difference of the conditional B and RB entropies, with log dim
        # cancelled analytically to avoid exponentially large dimensions.
        conditional_ic = -binary_entropy(plus)
        if plus > 0.0:
            conditional_ic -= plus * math.log2(ratio_dims)
        if plus < 1.0:
            conditional_ic -= (1.0-plus) * math.log2(d-ratio_dims)
        ic += weight * conditional_ic
        last_vac, last_one = wvac, wone
    ratio_vac = b/gain * (cutoff+d) / (cutoff+1.0)
    ratio_one = b/gain * (cutoff+d) / cutoff
    tail_bound = ((1.0-tau) * last_vac * ratio_vac / (1.0-ratio_vac)
                  + tau * last_one * ratio_one / (1.0-ratio_one))
    asymptotic = (-(1.0-tau) * math.log2(d) - binary_entropy(tau)
                  - tau * math.log2(b/gain))
    return dict(eta=eta, nu=nu, d=d, cutoff=cutoff,
                Ic_bits_per_block=ic, Ic_bits_per_mode=ic/d,
                summed_probability=total_probability,
                omitted_tail_probability_bound=tail_bound,
                omitted_Ic_absolute_bound=tail_bound*math.log2(d),
                asymptotic_Ic_bits=asymptotic)


def sparse_shell_upper_bound(eta, nu, d, photons):
    b = (1.0-eta)*nu
    gain = 1.0+b
    tau = eta/gain
    upper = (gaussian_entropy(2.0*b+1.0)
             + eta*photons*math.log2(1.0+1.0/b)
             - (1.0-tau)*photons*math.log2(d/photons))
    return dict(eta=eta, nu=nu, d=d, photons=photons,
                exact_analytic_Ic_upper_bound_bits=upper)


def main():
    rng = np.random.default_rng(20261010)
    max_error = 0.0
    for _ in range(1000):
        eta = rng.uniform(0.4, 0.95)
        nu = rng.uniform(0.1, 3.0)
        s = math.exp(rng.uniform(-5.0, 5.0))
        cb, ce, closed = pure_seed(eta, nu, s)
        max_error = max(max_error, float(np.max(np.abs(cb-ce-closed))))
    assert max_error < 1e-9, max_error

    s_values = [1e-8, 1e-4, 0.1, 1.0, 10.0, 1e4, 1e8]
    thresholds = [dict(s=s, eta_Chernoff=critical_eta(1.0, s)) for s in s_values]
    eta_limit = math.sqrt(17.0) / (1.0 + math.sqrt(17.0))
    smooth = [entropy_metric(0.76, 1.0, 1.0, 1.0+eps)
              for eps in [1e-2, 1e-4, 1e-6, 1e-8]]
    anti_near = []
    for eta in [0.75, 0.76, 0.7818, 0.7841, 0.8, eta_limit+1e-3]:
        cb, ce, closed = pure_seed(eta, 1.0, 1e-6)
        anti_near.append(dict(eta=eta, s=1e-6,
                             C_B_per_dq2=float(cb[0]),
                             C_E_per_dq2=float(ce[0]),
                             difference=float(closed[0])))
    output = dict(
        status="NUMERICAL_SUPPORT_NOT_INTERVAL_CERTIFICATION",
        independent_covariance_vs_closed_formula_max_absolute_error=max_error,
        random_cases=1000,
        nu_1_asymptotic_gaussian_seed_cat_threshold=eta_limit,
        thresholds=thresholds,
        near_antidegradable_chernoff=anti_near,
        smoothing_entropy_metric=smooth,
        all_output_sector_single_photon=[
            all_sector_single_photon(eta, 1.0, d)
            for eta in [0.75, 0.76, 0.7841, 0.8, 0.85, 0.9]
            for d in [2, 4, 16, 64, 256, 1024]
        ],
        photon_sparse_uniform_shell_upper_bounds=[
            sparse_shell_upper_bound(eta, 1.0, 1000*k, k)
            for eta in [0.75, 0.76, 0.7841, 0.8]
            for k in [1, 4, 16, 64]
        ],
    )
    destination = Path(__file__).with_name("e1_construction_checks.json")
    destination.write_text(json.dumps(output, indent=2)+"\n")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
