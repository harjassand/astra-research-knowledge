#!/usr/bin/env python3
"""Numerical diagnostics for exact algebra in e2_alternative.txt.

These calculations are floating point. They do not certify new positive
capacity points. The exact obstructions in the report are algebraic.
"""
import json
import math
from pathlib import Path

import numpy as np


def brentq(fn, low, high):
    # Bisection is adequate for these diagnostic thresholds.
    flo, fhi = fn(low), fn(high)
    assert flo * fhi < 0
    for _ in range(60):
        middle = (low + high) / 2
        fmid = fn(middle)
        if flo * fmid <= 0:
            high, fhi = middle, fmid
        else:
            low, flo = middle, fmid
    return (low + high) / 2


def ndtr(x):
    return .5 * math.erfc(-x / math.sqrt(2))


def expit(x):
    y = np.exp(-abs(x))
    return np.where(x >= 0, 1 / (1 + y), y / (1 + y))


def i0e(x):
    return float(np.i0(x)) * math.exp(-abs(x))


def entropy(prob):
    p = np.asarray(prob, dtype=float)
    p = p[p > 0]
    return float(-np.dot(p, np.log2(p)))


def h2(p):
    return entropy([p, 1 - p])


def rail_channel(eta, d, nu=1):
    gain = 1 + (1 - eta) * nu
    tau = eta / gain
    a = tau
    b = (1 - tau) * (gain - 1)
    z = a + d * b
    success = z / gain ** (d + 1)
    depol = a / z
    q0 = depol + (1 - depol) / d**2
    q1 = (1 - depol) / d**2
    ic = (2 * success - 1) * math.log2(d)
    ic -= success * entropy([q0] + [q1] * (d**2 - 1))
    return dict(eta=eta, d=d, success=success, depol=depol,
                coherent_information_per_D_uses=ic, rate_per_use=ic / d)


def gaussian_noise_min(eta, kappa, nu=1):
    if kappa <= eta:
        excess = kappa * (1 - eta) * nu / eta
    else:
        excess = kappa - eta + (1 - eta) * nu
    return (1 - kappa) / 2 + excess


def gaussian_noise(eta, kappa, w, nu=1):
    u = kappa / (eta * w)
    return (w * eta * abs(u - 1)
            + w * (1 - eta) * (2 * nu + 1) + abs(w - 1)) / 2


def hard_gkp_error(spacing, variance):
    ratio = spacing / math.sqrt(variance)
    if ratio >= 1.4:
        # Use survival functions to avoid subtraction from one.
        vals = []
        for j in range(100):
            term = ndtr(-(2 * j + .5) * ratio) - ndtr(-(2 * j + 1.5) * ratio)
            vals.append(term)
            if term < 1e-19:
                break
        return 2 * sum(vals)
    bias = 0.0
    for j in range(100):
        odd = 2 * j + 1
        term = (-1)**j / odd * math.exp(-odd**2 * math.pi**2 / (2 * ratio**2))
        bias += term
        if abs(term) < 1e-19:
            break
    return .5 - 2 / math.pi * bias


def repetition_cond_entropy(error, m):
    # Pairs of complementary BSC error patterns share a syndrome.
    if error == .5:
        return 1.0
    w = np.arange(m // 2 + 1, dtype=float)
    logcomb = math.lgamma(m + 1) - np.asarray([math.lgamma(x + 1) for x in w])
    logcomb -= np.asarray([math.lgamma(m - x + 1) for x in w])
    loga = w * math.log(error) + (m - w) * math.log1p(-error)
    logb = (m - w) * math.log(error) + w * math.log1p(-error)
    logtotal = np.logaddexp(loga, logb)
    post = expit(loga - logb)
    with np.errstate(divide='ignore', invalid='ignore'):
        terms = np.where(post > 0, -post * np.log2(post), 0)
        terms += np.where(post < 1, -(1 - post) * np.log2(1 - post), 0)
    return float(np.dot(np.exp(logcomb + logtotal), terms))


def repetition_scan(variance):
    best = (-float('inf'), None)
    lengths = [1, 3, 5, 7, 11, 15, 23, 31, 47, 63, 95, 127, 191, 255, 383, 511, 767, 1023]
    for ratio in np.linspace(1, 5, 161):
        px = hard_gkp_error(math.sqrt(math.pi) * ratio, variance)
        pz = hard_gkp_error(math.sqrt(math.pi) / ratio, variance)
        for m in lengths:
            parity_x = -math.expm1(m * math.log1p(-2 * px)) / 2
            ic = 1 - h2(parity_x) - repetition_cond_entropy(pz, m)
            if ic / m > best[0]:
                best = (ic / m, dict(rectangular_ratio=float(ratio), m=m,
                                    px=px, pz=pz, inner_ic=ic))
    return dict(variance=variance, best_scanned_rate=best[0], parameters=best[1])


def thermal_kernel(q, s, cutoff=140):
    n = np.arange(cutoff)
    annihilation = np.diag(np.sqrt(np.arange(1, cutoff)), 1)
    # i times the anti-Hermitian displacement generator is Hermitian.
    values, vectors = np.linalg.eigh(1j * s * (annihilation.T - annihilation))
    displacement = (vectors * np.exp(-1j * values)[None, :]) @ vectors.conj().T
    thermal = (1 - q) * q**n
    operator = (displacement * thermal[None, :]) @ displacement
    numerator = abs(operator)**2
    root = np.sqrt(thermal)
    kernel = float(np.sum(numerator / (root[:, None] + root[None, :])**2))
    weighted = float(np.sum(numerator / (root[:, None] * root[None, :])))
    t = math.sqrt(q)
    c = 2 * (1 - t) * (1 + q) / (t * (1 + t))
    exact_weighted = math.exp(c * s * s)
    acoef = 4 * (1 + q) / (1 - q)
    bcoef = 2 * (1 + q)**2 / (t * (1 - q))
    exact_diag = .25 * math.exp((bcoef - acoef) * s * s) * i0e(bcoef * s * s)
    diag = float(np.sum(np.diag(numerator) / (4 * thermal)))
    return dict(q=q, displacement=s, cutoff=cutoff, kernel=kernel,
                diagonal_lower=diag, diagonal_formula=exact_diag,
                weighted_upper=weighted / 4, weighted_formula=exact_weighted / 4,
                weighted_identity_relative_error=abs(weighted / exact_weighted - 1),
                diagonal_identity_relative_error=abs(diag / exact_diag - 1))


def main():
    output = {}
    output['status'] = 'floating_point_diagnostics_not_capacity_certificates'
    output['rail_table'] = [rail_channel(e, d) for e in [.75, .751, .76, .7841, .8, .85, .9, .95]
                            for d in [2, 3, 8]]
    output['rail_p_half_threshold_D2'] = brentq(lambda e: rail_channel(e, 2)['success'] - .5, .75, .95)
    output['rail_ic_zero_threshold_D2'] = brentq(lambda e: rail_channel(e, 2)['coherent_information_per_D_uses'], .8, .999)
    output['gaussian_noise_checks'] = []
    for eta in [.75, .751, .7841, .8]:
        for kappa in [.50001, .6, .8, 1.0]:
            # Include exact breakpoints as well as a broad logarithmic scan.
            wvalues = np.r_[np.logspace(-5, 5, 10001), 1., kappa / eta]
            observed = min(gaussian_noise(eta, kappa, w) for w in wvalues)
            formula = gaussian_noise_min(eta, kappa)
            output['gaussian_noise_checks'].append(dict(eta=eta, kappa=kappa,
                sampled_minimum=observed, formula=formula, difference=observed-formula))
    output['repetition_scan'] = [repetition_scan(v) for v in [.30, .34, .3535533905932738, 1/math.e, .4, .45, .49]]
    output['thermal_kernel_checks'] = [thermal_kernel(.5, s) for s in [0, .25, .5, 1., 1.5, 2., 3., 4.]]
    output['thresholds'] = dict(preamp_standard=1-1/(2*math.e),
        large_bias_gkp_variance=1/(2*math.sqrt(2)),
        unweighted_collision_eta=.75,
        weighted_kernel_theta_gate=(2+math.sqrt(2))/4)
    result_path = Path(__file__).with_name('diagnostics.json')
    result_path.write_text(json.dumps(output, indent=2) + '\n')
    print(json.dumps({k: output[k] for k in ['status', 'rail_p_half_threshold_D2',
                'rail_ic_zero_threshold_D2', 'thresholds', 'repetition_scan']}, indent=2))
    print('maximum thermal identity relative error', max(max(r['weighted_identity_relative_error'],
          r['diagonal_identity_relative_error']) for r in output['thermal_kernel_checks']))
    print('saved', result_path)


if __name__ == '__main__':
    main()
