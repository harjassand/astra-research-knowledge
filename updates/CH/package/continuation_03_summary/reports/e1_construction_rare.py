#!/usr/bin/env python3
"""Finite, physical-cutoff checks for the E1 rare pure-seed construction.

No faithfulness conclusion can be drawn from these finite matrices. Input
cutoffs prepare actual normalized finite states; the output overflow is an
erasure flag and is never postselected away. Floating-point diagnostics only.
"""
import argparse
import json
import math
from pathlib import Path

import numpy as np


def entropy(a):
    vals = np.linalg.eigvalsh((a + a.conj().T) / 2.0)
    if vals.min() < -3e-12:
        raise ValueError(f"Not positive: {vals.min()}")
    vals = vals[vals > 1e-16]
    return float(-np.dot(vals, np.log2(vals)))


def output_blocks(eta, nu, seeds, max_output):
    """P_M Phi(|seed_i><seed_j|) P_M from exact loss/amp Kraus."""
    dim_input = seeds.shape[1]
    num = seeds.shape[0]
    b = (1.0 - eta) * nu
    gain = 1.0 + b
    tau = eta / gain
    dim = max_output + 1
    blocks = np.zeros((num, num, dim, dim), dtype=complex)
    for lost in range(dim_input):
        jj = np.arange(dim_input - lost)
        loss = np.array([
            math.exp((math.lgamma(int(j) + lost + 1)
                      - math.lgamma(lost + 1) - math.lgamma(int(j) + 1)
                      + lost * math.log1p(-tau) + int(j) * math.log(tau)) / 2)
            for j in jj
        ])
        lv = seeds[:, lost:] * loss
        for added in range(dim):
            length = min(dim_input - lost, dim - added)
            if length <= 0:
                continue
            amp = np.array([
                math.exp((math.lgamma(j + added + 1)
                          - math.lgamma(j + 1) - math.lgamma(added + 1)
                          + added * math.log(b)
                          - (j + added + 1) * math.log(gain)) / 2)
                for j in range(length)
            ])
            vv = lv[:, :length] * amp
            sl = slice(added, added + length)
            for ii in range(num):
                for kk in range(ii, num):
                    blocks[ii, kk, sl, sl] += np.outer(vv[ii], vv[kk].conj())
    for ii in range(num):
        for kk in range(ii):
            blocks[ii, kk] = blocks[kk, ii].conj().T
    return blocks


def flagged_blocks(blocks, seeds):
    num, _, dim, _ = blocks.shape
    full = np.zeros((num, num, dim + 1, dim + 1), dtype=complex)
    full[:, :, :dim, :dim] = blocks
    gram = seeds @ seeds.conj().T
    for ii in range(num):
        for kk in range(num):
            full[ii, kk, dim, dim] = gram[ii, kk] - np.trace(blocks[ii, kk])
    return full


def coherent_information(blocks, probability):
    probs = np.array([1.0 - probability, probability])
    dim = blocks.shape[-1]
    bob = sum(probs[ii] * blocks[ii, ii] for ii in range(2))
    joint = np.empty((2 * dim, 2 * dim), dtype=complex)
    for ii in range(2):
        for kk in range(2):
            joint[ii * dim:(ii + 1) * dim, kk * dim:(kk + 1) * dim] = (
                math.sqrt(probs[ii] * probs[kk]) * blocks[ii, kk]
            )
    return entropy(bob) - entropy(joint)


def kernel_diagnostic(eta, nu, probability_ratio, cutoff):
    """Exact finite polynomial kernel norm and its vacuum dark-mass bound."""
    b = (1 - eta) * nu
    gain = 1 + b
    tau = eta / gain
    beta2 = 1 - tau
    alpha2 = eta / gain**2
    q = tau / b
    nn = np.arange(cutoff + 1)
    pp = probability_ratio**nn
    pp /= pp.sum()
    moment = float(np.dot(pp, q**nn))
    derivative = float(np.dot(nn[1:] * pp[1:], q**(nn[1:] - 1)))
    norm = derivative + moment / beta2
    numerator = float(np.dot(nn[1:] * pp[1:], alpha2**(nn[1:] - 1))) / gain
    return dict(cutoff=cutoff, probability_ratio=probability_ratio,
                dilation_q=q, kernel_norm_squared=norm,
                vacuum_dark_mass_lower_bound=numerator / norm)


def optimized_kernel_diagnostic(eta, nu, probability_ratio, cutoff):
    """E3's entangled multiplier, with independently derived exact norm."""
    b = (1 - eta) * nu
    gain = 1 + b
    tau = eta / gain
    beta2 = 1 - tau
    radius = (eta - b) / b
    s0 = gain * (eta - b) / eta
    kappa2 = (eta - b)**2 / eta
    nn = np.arange(cutoff + 1)
    pp = probability_ratio**nn
    pp /= pp.sum()
    moment = float(np.dot(pp, radius**nn))
    derivative = float(np.dot(nn[1:] * pp[1:], radius**(nn[1:] - 1)))
    norm = moment / s0**2 + 4 * beta2 * derivative / s0
    numerator = beta2 / gain * float(np.dot(nn[1:] * pp[1:],
                                             kappa2**(nn[1:] - 1)))
    return dict(cutoff=cutoff, probability_ratio=probability_ratio,
                optimized_moment_radius=radius, kernel_norm_squared=norm,
                vacuum_dark_mass_lower_bound=numerator / norm)


def check_wronskian(eta=.76, nu=1., cutoff=7):
    """Finite coefficients of an infinite entangled kernel cancel exactly.

    The contraction against polynomial input has only finitely many nonzero
    terms, despite the kernel's infinite e^(txy) factor.
    """
    b = (1 - eta) * nu
    gain = 1 + b
    beta = math.sqrt(1 - eta / gain)
    alpha = math.sqrt(eta) / gain
    gamma = math.sqrt(b / gain)
    t = -beta * gamma / alpha
    lam = alpha / gamma + beta * t
    kappa = lam * gamma
    rng = np.random.default_rng(1107)
    f = rng.normal(size=cutoff+1) + 1j*rng.normal(size=cutoff+1)
    f /= np.linalg.norm(f)
    g = rng.normal(size=cutoff+1) + 1j*rng.normal(size=cutoff+1)
    g /= np.linalg.norm(g)
    max_b = 2 * cutoff - 1
    h = np.zeros((cutoff+1, max_b+1), dtype=complex)
    for nn in range(cutoff+1):
        for jj in range(cutoff+1):
            lost, added = jj+1, jj+nn
            if lost <= cutoff and added <= max_b:
                h[lost, added] += (f[nn] * lam**nn * t**jj / math.factorial(jj)
                                  * math.sqrt(math.factorial(lost)
                                              * math.factorial(added)
                                              / math.factorial(nn)))
            lost, added = jj, jj+nn-1
            if nn >= 1 and added <= max_b:
                h[lost, added] -= (beta * f[nn] * nn * lam**(nn-1) * t**jj
                                  / math.factorial(jj)
                                  * math.sqrt(math.factorial(lost)
                                              * math.factorial(added)
                                              / math.factorial(nn)))

    def contract(seed):
        vv = np.zeros(max_b+1, dtype=complex)
        for mm in range(max_b+1):
            for lost in range(cutoff+1):
                for added in range(mm+1):
                    nn = mm+lost-added
                    if lost <= nn <= cutoff:
                        vv[mm] += (h[lost, added] * seed[nn]
                                   * math.sqrt(math.comb(nn, lost)
                                               * math.comb(mm, added))
                                   * alpha**(mm-added) * beta**lost * gamma**added
                                   / math.sqrt(gain))
        return vv

    ff = np.array([f[nn]/math.sqrt(math.factorial(nn))
                   for nn in range(cutoff+1)])
    gg = np.array([g[nn]/math.sqrt(math.factorial(nn))
                   for nn in range(cutoff+1)])
    fd = np.arange(1, cutoff+1) * ff[1:]
    gd = np.arange(1, cutoff+1) * gg[1:]
    wr = np.convolve(gd, ff) - np.convolve(gg, fd)
    predicted = np.array([beta/math.sqrt(gain) * wr[mm] * kappa**mm
                          * math.sqrt(math.factorial(mm))
                          for mm in range(max_b+1)])
    # Independent norm check: directly sum normalized two-mode Fock
    # coefficients of the entire exp(txy) kernel, rather than its moments.
    direct_norm = 0.
    for nn in range(cutoff+1):
        for lost in range(101):
            added = lost+nn-1
            if added < 0:
                continue
            logfactor = (math.lgamma(lost+1)+math.lgamma(added+1)
                         - math.lgamma(nn+1)-2*math.lgamma(lost+1))
            value = (math.exp(logfactor)*abs(t)**(2*(lost-1))
                     * lam**(2*(nn-1)) * (lost*lam-beta*nn*t)**2)
            direct_norm += abs(f[nn])**2*value
    radius = (eta-b)/b
    s0 = 1-t*t
    moment = sum(abs(f[nn])**2*radius**nn for nn in range(cutoff+1))
    derivative = sum(nn*abs(f[nn])**2*radius**(nn-1)
                     for nn in range(1, cutoff+1))
    moment_norm = moment/s0**2+4*beta**2*derivative/s0
    return dict(seed_kernel_max_abs=float(abs(contract(f)).max()),
                second_seed_wronskian_max_error=float(abs(contract(g)-predicted).max()),
                second_seed_contraction_norm_squared=float(np.vdot(predicted, predicted).real),
                direct_Fock_norm_squared=float(direct_norm),
                moment_norm_squared=float(moment_norm),
                norm_relative_error=float(abs(direct_norm/moment_norm-1)))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-cutoff", type=int, default=28)
    parser.add_argument("--output-cutoff", type=int, default=50)
    parser.add_argument("--eta", type=float, default=.76)
    args = parser.parse_args()
    n = np.arange(args.input_cutoff + 1)
    trials = []
    # Distinct non-Gaussian infinite-tail ansatz, truncated for physical tests.
    for ratio in [.25, 5/12, .6, .8]:
        for cubic in [.31, math.sqrt(2)]:
            amp = ratio**(n / 2) * np.exp(1j * cubic * n**3)
            amp /= np.linalg.norm(amp)
            for shift in [None, .3, math.pi]:
                other = (np.eye(1, len(n), 0).reshape(-1).astype(complex)
                         if shift is None else amp * np.exp(1j * shift * n))
                seeds = np.array([amp, other])
                raw = output_blocks(args.eta, 1, seeds, args.output_cutoff)
                blocks = flagged_blocks(raw, seeds)
                vals = [{"probability": p, "Ic_bits": coherent_information(blocks, p)}
                        for p in [.5, .1, .01, .001, 1e-5]]
                trials.append(dict(eta=args.eta, probability_ratio=ratio,
                                   cubic_phase=cubic, phase_shift=shift,
                                   input_mean=float(np.dot(n, abs(amp)**2)),
                                   overflow=float(blocks[0, 0, -1, -1].real),
                                   results=vals))
    diagnostics = [kernel_diagnostic(.75, 1, x, cutoff)
                   for x in [.25, 5/12, .6]
                   for cutoff in [10, 20, 40, 80, 160]]
    optimized = [optimized_kernel_diagnostic(.75, 1, x, cutoff)
                 for x in [.25, .5, .6]
                 for cutoff in [10, 20, 40, 80, 160]]
    out = dict(status="FLOATING_POINT_DIAGNOSTIC_NOT_CAPACITY_CERTIFICATE",
               parameters=vars(args), trials=trials,
               exact_kernel_diagnostics=diagnostics,
               optimized_kernel_diagnostics=optimized,
               wronskian_coefficient_check=check_wronskian())
    dest = Path(__file__).with_name("e1_construction_rare_checks.json")
    dest.write_text(json.dumps(out, indent=2) + "\n")
    best = max((r["Ic_bits"], t["probability_ratio"], t["cubic_phase"],
                t["phase_shift"], r["probability"])
               for t in trials for r in t["results"])
    print(json.dumps(dict(output=str(dest), best_Ic_and_parameters=best,
                          wronskian_coefficient_check=out["wronskian_coefficient_check"],
                          optimized_kernel_diagnostics=optimized), indent=2))


if __name__ == "__main__":
    main()
