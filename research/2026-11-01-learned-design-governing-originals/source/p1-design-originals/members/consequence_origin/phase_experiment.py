"""Finite synthetic check of the acquisition-to-phase-sampling construction.

The learner receives only the trajectory, the known graph/beta, and a field range.
True h is used only by the synthetic experiment and the final validation scorer.
No claim of physical acquisition, formal interval arithmetic, or novelty is made.
"""
from __future__ import annotations

import argparse
import json
import math
import time
from pathlib import Path

import numpy as np
from scipy.optimize import brentq
from scipy.special import expit, logsumexp
from scipy.stats import beta as beta_distribution


def complete_graph(n):
    return [tuple(j for j in range(n) if j != i) for i in range(n)]


def trajectory(adj, beta, true_h, steps, rng):
    """Observe every attempt; no reset and no equilibration are used."""
    n = len(adj)
    degree = len(adj[0])
    assert all(len(a) == degree for a in adj)
    spins = np.ones(n, dtype=np.int8)
    neighbour_sum = np.full(n, degree, dtype=np.int16)
    zvals = np.arange(-degree, degree + 1, 2)
    probs = expit(2 * beta * zvals + 2 * true_h)
    count = np.zeros(degree + 1, dtype=np.int64)
    plus = np.zeros(degree + 1, dtype=np.int64)
    sites = rng.integers(n, size=steps, dtype=np.uint8)
    uniforms = rng.random(steps)
    outcomes = np.empty(steps, dtype=np.uint8)
    contexts = np.empty(steps, dtype=np.int8)
    magnetisation = n
    phase_changes = 0
    min_magnetisation = n
    previous_phase = 1
    flips = 0
    for t in range(steps):
        i = int(sites[t])
        z = int(neighbour_sum[i])
        c = (z + degree) // 2
        y = int(uniforms[t] < probs[c])
        outcomes[t] = y
        contexts[t] = z
        count[c] += 1
        plus[c] += y
        new = 2 * y - 1
        difference = new - int(spins[i])
        if difference:
            flips += 1
            spins[i] = new
            magnetisation += difference
            for j in adj[i]:
                neighbour_sum[j] += difference
        phase = 1 if magnetisation >= 0 else -1
        phase_changes += int(phase != previous_phase)
        previous_phase = phase
        min_magnetisation = min(min_magnetisation, magnetisation)
    return dict(sites=sites, outcomes=outcomes, contexts=contexts,
                count=count, plus=plus, zvals=zvals,
                phase_changes=phase_changes, flips=flips,
                minimum_magnetisation=min_magnetisation)


def fit_bias(zvals, counts, plus, beta, field_range, delta):
    def score(h):
        return float(np.sum(plus - counts * expit(2 * beta * zvals + 2*h)))

    def log_likelihood(h):
        eta = 2 * beta * zvals + 2*h
        return float(np.sum(plus * eta - counts * np.logaddexp(0, eta)))

    low, high = -field_range, field_range
    if score(low) <= 0:
        estimate = low
    elif score(high) >= 0:
        estimate = high
    else:
        estimate = brentq(score, low, high, xtol=1e-13)
    grid = np.linspace(low, high, 801)
    log_mix = float(logsumexp([log_likelihood(h) for h in grid]) - math.log(len(grid)))
    threshold = log_mix + math.log(delta)
    def root(h):
        return log_likelihood(h) - threshold
    ci_low = low if root(low) >= 0 else brentq(root, low, estimate, xtol=1e-13)
    ci_high = high if root(high) >= 0 else brentq(root, estimate, high, xtol=1e-13)
    return dict(estimate=estimate, confidence_interval=[ci_low-1e-10, ci_high+1e-10],
                confidence_rule="finite likelihood mixture; continuous parameter; numerical roots",
                mixture_points=len(grid), delta=delta, log_mixture=log_mix,
                score_at_estimate=score(estimate))


def adjacency_masks(adj):
    return [sum(1 << j for j in a) for a in adj]


def connected_sets(adj, cutoff):
    n = len(adj)
    masks = adjacency_masks(adj)
    current = {1 << i for i in range(n)}
    result = set(current)
    for size in range(2, cutoff + 1):
        nxt = set()
        for mask in current:
            boundary = 0
            for i in range(n):
                if (mask >> i) & 1:
                    boundary |= masks[i]
            boundary &= ~mask
            while boundary:
                bit = boundary & -boundary
                boundary -= bit
                nxt.add(mask | bit)
        result.update(nxt)
        current = nxt
    return sorted(result, key=lambda m: (m.bit_count(), m))


def make_polymers(adj, beta, h, sign, cutoff):
    n = len(adj)
    neighbourhood = adjacency_masks(adj)
    polys = []
    for mask in connected_sets(adj, cutoff):
        size = mask.bit_count()
        boundary_edges = sum(1 for i in range(n) if (mask >> i) & 1
                             for j in adj[i] if not ((mask >> j) & 1))
        closed = mask
        for i in range(n):
            if (mask >> i) & 1:
                closed |= neighbourhood[i]
        weight = math.exp(-2*beta*boundary_edges - 2*sign*h*size)
        polys.append((mask, closed, weight, size, (mask & -mask).bit_length()-1))
    return polys


def certificate(adj, beta, max_abs_h):
    n = len(adj)
    delta = max(map(len, adj))
    lap = np.diag([len(a) for a in adj]).astype(float)
    for i, a in enumerate(adj):
        lap[i, list(a)] = -1
    # This is a numerical consistency check; the paper calls for certified inertia.
    lam2 = float(np.linalg.eigvalsh(lap)[1])
    b = lam2 / 2
    a = 2*beta*b - 2*max_abs_h
    r = delta**2 * math.exp(-a)
    s = math.exp(-a)/(1-r) if r < 1 else math.inf
    theta = (delta+1)*math.exp(-a)/(1-r)**2 if r < 1 else math.inf
    return dict(laplacian_gap=lam2, expansion_lower_bound=b, activity_exponent=a,
                r=r, s=s, theta=theta,
                accepted=(r < 1 and theta < 1 and s <= .25),
                spectral_verification="floating eigenvalues; no formal rounding certificate")


class PolymerSampler:
    def __init__(self, polymers, n, theta, accuracy, rng, allowed=None):
        self.n, self.rng = n, rng
        allowed = (1 << n)-1 if allowed is None else allowed
        self.polys = [p for p in polymers if p[0] & ~allowed == 0]
        self.cdf = np.cumsum([p[2] for p in self.polys])
        self.weight = float(self.cdf[-1]) if self.polys else 0.0
        self.rate = n + self.weight
        self.steps = math.ceil(self.rate / (1-theta) * math.log(2*n/accuracy))
        self.attempts = 0

    def sample(self):
        occupied = 0
        representatives = {}
        for _ in range(self.steps):
            u = self.rng.random()*self.rate
            if u < self.n:
                vertex = int(u)
                dying = representatives.pop(vertex, 0)
                occupied ^= dying
            else:
                index = int(np.searchsorted(self.cdf, u-self.n, side="right"))
                mask, closed, weight, size, rep = self.polys[index]
                if not (closed & occupied):
                    representatives[rep] = mask
                    occupied |= mask
        self.attempts += self.steps
        return occupied


def binomial_interval(successes, trials, delta, mixing_error):
    lo = 0.0 if successes == 0 else float(beta_distribution.ppf(delta/2, successes, trials-successes+1))
    hi = 1.0 if successes == trials else float(beta_distribution.ppf(1-delta/2, successes+1, trials-successes))
    return [max(0.0, lo-mixing_error), min(1.0, hi+mixing_error)]


def count_gas(polys, n, theta, samples, accuracy, delta, rng):
    allowed = (1 << n)-1
    log_z = 0.0
    log_lo = 0.0
    log_hi = 0.0
    stages = []
    attempts = 0
    for v in range(n):
        sampler = PolymerSampler(polys, n, theta, accuracy, rng, allowed)
        successes = sum(not (sampler.sample() & (1 << v)) for _ in range(samples))
        p = successes / samples
        ci = binomial_interval(successes, samples, delta/n, accuracy)
        if ci[0] <= 0:
            raise RuntimeError("Inconclusive probability interval; acquire more digital samples")
        log_z -= math.log(p)
        log_lo -= math.log(ci[1])
        log_hi -= math.log(ci[0])
        stages.append(dict(vertex=v, successes=successes, trials=samples, p=p, interval=ci))
        attempts += sampler.attempts
        allowed &= ~(1 << v)
    return dict(log_z=log_z, interval=[log_lo, log_hi], stages=stages,
                digital_update_attempts=attempts)


def phase_acceptance(polys, n, theta, sign, samples, accuracy, delta, rng):
    threshold = n//2 if sign == 1 else (n+1)//2-1
    sampler = PolymerSampler(polys, n, theta, accuracy, rng)
    successes = sum(sampler.sample().bit_count() <= threshold for _ in range(samples))
    return dict(estimate=successes/samples,
                interval=binomial_interval(successes, samples, delta, accuracy),
                digital_update_attempts=sampler.attempts)


def exhaustive_distribution(adj, beta, h):
    """Scorer only: explicitly charges 2^n states, never used by the learner."""
    n = len(adj)
    states = ((np.arange(1 << n)[:, None] >> np.arange(n)) & 1)*2-1
    energy = h*states.sum(axis=1).astype(float)
    for i, ns in enumerate(adj):
        for j in ns:
            if i < j:
                energy += beta * states[:, i] * states[:, j]
    log_z = float(logsumexp(energy))
    p = np.exp(energy-log_z)
    return dict(phase_plus=float(p[states.sum(axis=1)>=0].sum()),
                mean_activation=float(p @ ((states.sum(axis=1)/n+1)/2)),
                log_partition=log_z, enumerated_states=1 << n), p


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--observations", type=int, default=10000000)
    parser.add_argument("--count-samples", type=int, default=1500)
    parser.add_argument("--seed", type=int, default=49203)
    parser.add_argument("--n", type=int, default=9)
    parser.add_argument("--beta", type=float, default=.55)
    parser.add_argument("--true-h", type=float, default=.08)
    parser.add_argument("--field-range", type=float, default=.2)
    args = parser.parse_args()
    out = Path(__file__).resolve().parent
    rng = np.random.default_rng(args.seed)
    adj = complete_graph(args.n)
    beta, true_h, prior_range = args.beta, args.true_h, args.field_range
    started = time.perf_counter()
    data = trajectory(adj, beta, true_h, args.observations, rng)
    acquisition_seconds = time.perf_counter()-started
    np.savez_compressed(out/"phase_observations.npz", sites=data["sites"],
                        outcomes=data["outcomes"], contexts=data["contexts"])
    fit = fit_bias(data["zvals"], data["count"], data["plus"], beta, prior_range, .05)
    hhat = fit["estimate"]
    cert = certificate(adj, beta, max(map(abs, fit["confidence_interval"])))
    print(json.dumps(dict(stage="acquired", observations=args.observations,
                          phase_changes=data["phase_changes"], fit=fit,
                          certificate=cert, seconds=acquisition_seconds)), flush=True)
    if not cert["accepted"]:
        raise RuntimeError("Learned uncertainty does not certify the polymer mechanism")
    n = len(adj)
    cutoff = n//2  # Exact truncation for this small consistency check.
    records = {}
    logs, log_intervals = {}, {}
    for sign in [1, -1]:
        polymers = make_polymers(adj, beta, hhat, sign, cutoff)
        count = count_gas(polymers, n, cert["theta"], args.count_samples, 1e-6, .01, rng)
        accept = phase_acceptance(polymers, n, cert["theta"], sign,
                                  args.count_samples, 1e-6, .01, rng)
        logs[sign] = sign*hhat*n + count["log_z"] + math.log(accept["estimate"])
        log_intervals[sign] = [sign*hhat*n + count["interval"][0] + math.log(accept["interval"][0]),
                               sign*hhat*n + count["interval"][1] + math.log(accept["interval"][1])]
        records[str(sign)] = dict(polymer_types=len(polymers), count=count, acceptance=accept)
        print(json.dumps(dict(stage="phase_counted", sign=sign, log_weight=logs[sign],
                              log_interval=log_intervals[sign])), flush=True)
    alpha = float(expit(logs[1]-logs[-1]))
    alpha_interval = [float(expit(log_intervals[1][0]-log_intervals[-1][1])),
                      float(expit(log_intervals[1][1]-log_intervals[-1][0]))]
    truth, ptrue = exhaustive_distribution(adj, beta, true_h)
    learned, plearned = exhaustive_distribution(adj, beta, hhat)
    field_lo, _ = exhaustive_distribution(adj, beta, fit["confidence_interval"][0])
    field_hi, _ = exhaustive_distribution(adj, beta, fit["confidence_interval"][1])
    true_in_ci = fit["confidence_interval"][0] <= true_h <= fit["confidence_interval"][1]
    degree = max(map(len, adj))
    rest = np.arange(-(degree-1), degree, 2)
    exact_site_influence = float(np.max(expit(2*beta*(rest+1)+2*hhat)
                                        - expit(2*beta*(rest-1)+2*hhat)))
    # An intentionally weaker comparator: empirical physical magnetisation would
    # stay in the initial phase. The strongest conventional comparator uses the
    # very same conditional MLE and polymer calculation, hence is identical.
    result = dict(
        status="finite synthetic consistency check; no novelty or physical validation",
        seed=args.seed, graph=f"complete graph K{n}", n=n, beta=beta, true_h_for_scoring=true_h,
        observation_count=args.observations, acquisition_seconds=acquisition_seconds,
        site_flips=data["flips"], physical_phase_changes=data["phase_changes"],
        minimum_physical_magnetisation=data["minimum_magnetisation"],
        context_counts=data["count"].tolist(), plus_counts=data["plus"].tolist(),
        fit=fit, true_field_in_confidence_interval=bool(true_in_ci), certificate=cert,
        one_site_classical_bound=max(map(len, adj))*math.tanh(beta), cutoff=cutoff,
        truncation_tail=0.0, phase_records=records,
        estimated_plus_phase_weight=alpha, counting_confidence_interval=alpha_interval,
        scoring_true_stationary=truth, scoring_fitted_stationary=learned,
        scoring_field_interval_implied_phase_interval=[field_lo["phase_plus"],field_hi["phase_plus"]],
        scoring_field_interval_implied_mean_interval=[field_lo["mean_activation"],field_hi["mean_activation"]],
        fitted_exact_one_site_row_sum=degree*exact_site_influence,
        end_to_end_004_accuracy_certified=False,
        actual_model_total_variation=float(np.abs(ptrue-plearned).sum()/2),
        conservative_model_tv_bound=n*max(abs(hhat-fit["confidence_interval"][0]),
                                        abs(hhat-fit["confidence_interval"][1])),
        numerical_count_error=abs(alpha-learned["phase_plus"]),
        conventional_retaining_comparator="identical conditional MLE plus ordinary polymer solver",
        exact_small_comparator="full-state stationary calculation of the fitted model; same uncertainty",
        total_seconds=time.perf_counter()-started)
    (out/"phase_results.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({k:result[k] for k in ["estimated_plus_phase_weight", "counting_confidence_interval",
          "scoring_true_stationary", "scoring_fitted_stationary", "actual_model_total_variation",
          "numerical_count_error", "physical_phase_changes", "total_seconds"]}), flush=True)


if __name__ == "__main__":
    main()
