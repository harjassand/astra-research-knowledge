"""Finite diagnostic for the analytic proof in pure_quantum_lower.md.

These checks do not prove the theorem or settle novelty. They test the exact
multinomial normalization, eigenvalue lower bound, projection tail bound,
Stinespring entanglement-fidelity identity, and Schmidt-tail bottleneck bound.
Only numpy and the Python standard library are used.
"""

from __future__ import annotations

import itertools
import json
import math
from pathlib import Path

import numpy as np


def occupations(q: int, n: int):
    return [m for m in itertools.product(range(n + 1), repeat=q) if sum(m) <= n]


def probabilities(q: int, n: int, radius: float):
    occ = occupations(q, n)
    S = min(radius * radius, 0.25)
    r2 = S / q
    log_norm = -n * math.log1p(S / n)
    p = []
    for m in occ:
        k = sum(m)
        log_falling = sum(math.log1p(-j / n) for j in range(k))
        p.append(math.exp(log_norm + log_falling + k * math.log(r2)
                          - sum(math.lgamma(j + 1) for j in m)))
    return occ, np.array(p), S, r2


def random_channel_kraus(rng, input_dim: int, output_dim: int, environment: int):
    z = (rng.standard_normal((output_dim * environment, input_dim))
         + 1j * rng.standard_normal((output_dim * environment, input_dim)))
    v, _ = np.linalg.qr(z)
    return [v[j * output_dim:(j + 1) * output_dim, :]
            for j in range(environment)]


def apply_channel(kraus, rho):
    return sum(k @ rho @ k.conj().T for k in kraus)


def trace_distance(a, b):
    return 0.5 * np.abs(np.linalg.eigvalsh(a - b)).sum()


def audit_spectra():
    max_norm_error = 0.0
    min_lower_ratio = math.inf
    min_falling_ratio = math.inf
    min_overlap_ratio = math.inf
    max_tail_excess = 0.0
    cases = 0
    rng = np.random.default_rng(84310)
    for q in (1, 2, 3):
        for n in range(1, 13):
            for radius in (0.03, 0.2, 0.5, 2.0):
                occ, p, S, r2 = probabilities(q, n, radius)
                cases += 1
                max_norm_error = max(max_norm_error, abs(p.sum() - 1))
                c0 = (1 - S) * math.exp(-S)
                for K in range(n + 1):
                    bound = math.exp(-S + K * math.log(r2 / math.e)
                                     - math.lgamma(K + 1))
                    covered = [p[i] for i, m in enumerate(occ) if sum(m) <= K]
                    min_lower_ratio = min(min_lower_ratio, min(covered) / bound)
                for k in range(n + 1):
                    log_ratio = sum(math.log1p(-j / n) for j in range(k)) + k
                    min_falling_ratio = min(min_falling_ratio, math.exp(log_ratio))
                for _ in range(4):
                    theta = rng.uniform(0, 2 * math.pi, q)
                    phi = rng.uniform(0, 2 * math.pi, q)
                    inner = abs((1 + (r2 / n)
                                 * np.exp(1j * (phi - theta)).sum())
                                / (1 + S / n)) ** n
                    min_overlap_ratio = min(min_overlap_ratio, inner / c0)

                # Test the upper bound for arbitrary full-ball norms,
                # not merely the small lower-bound torus.
                for s in (min(0.001, radius * radius / 4),
                          radius * radius / 2, radius * radius):
                    theta = s / (n + s)
                    bp = np.array([math.comb(n, k) * theta ** k
                                   * (1 - theta) ** (n - k)
                                   for k in range(n + 1)])
                    for K in range(n):
                        tail = bp[K + 1:].sum()
                        bound = math.exp((K + 1) * math.log(radius * radius)
                                         - math.lgamma(K + 2))
                        max_tail_excess = max(max_tail_excess, tail - bound)
    assert max_norm_error < 2e-12
    assert min_lower_ratio >= 1 - 2e-12
    assert min_falling_ratio >= 1 - 2e-12
    assert min_overlap_ratio >= 1 - 2e-12
    assert max_tail_excess < 2e-12
    return {
        "cases": cases,
        "max_probability_normalization_error": max_norm_error,
        "min_eigenvalue_lower_bound_ratio": min_lower_ratio,
        "min_falling_factorial_lower_bound_ratio": min_falling_ratio,
        "min_pairwise_overlap_lower_bound_ratio": min_overlap_ratio,
        "max_binomial_tail_bound_excess": max_tail_excess,
    }


def audit_channels():
    rng = np.random.default_rng(543083)
    q, n, radius = 2, 3, 0.5
    occ, p, S, _ = probabilities(q, n, radius)
    dim = len(occ)
    rho = np.diag(p)
    # Grid size n+1 makes the phase average exactly diagonal.
    phases = [2 * math.pi * np.array(theta) / (n + 1)
              for theta in itertools.product(range(n + 1), repeat=q)]
    states = [np.sqrt(p) * np.exp(1j * np.array(occ) @ theta)
              for theta in phases]
    phase_average = sum(np.outer(v, v.conj()) for v in states) / len(states)
    assert np.linalg.norm(phase_average - rho) < 2e-12
    c0 = (1 - S) * math.exp(-S)
    records = []
    for contamination in (1e-8, 1e-4, 0.2):
        noisy = random_channel_kraus(rng, dim, dim, 3)
        kraus = ([math.sqrt(1 - contamination) * np.eye(dim)]
                 + [math.sqrt(contamination) * k for k in noisy])
        errors, distances, env = [], [], []
        for v in states:
            original = np.outer(v, v.conj())
            decoded = apply_channel(kraus, original)
            errors.append(1 - np.vdot(v, decoded @ v).real)
            distances.append(trace_distance(original, decoded))
            env.append(np.array([np.vdot(v, k @ v) for k in kraus]))
        avg_error = float(np.mean(errors))
        fe = float(sum(abs(np.trace(rho @ k)) ** 2 for k in kraus))
        avg_env = np.mean(env, axis=0)
        identity_error = abs(fe - np.vdot(avg_env, avg_env).real)
        converse = 1 - (2 * math.sqrt(max(0, avg_error)) + avg_error) / c0
        assert identity_error < 2e-12
        assert max(np.array(errors) - np.array(distances)) < 2e-12
        assert fe >= converse - 2e-12
        records.append({"contamination": contamination,
                        "average_infidelity": avg_error,
                        "average_trace_distance": float(np.mean(distances)),
                        "entanglement_fidelity": fe,
                        "lemma_lower_bound": converse,
                        "environment_identity_error": identity_error})

    bottlenecks = []
    for Q in (1, 2, 4):
        # Encoder needs enough environment dimensions for an isometry.
        encoder = random_channel_kraus(rng, dim, Q, dim)
        decoder = random_channel_kraus(rng, Q, dim, 2)
        kraus = [dk @ ek for dk in decoder for ek in encoder]
        fe = float(sum(abs(np.trace(rho @ k)) ** 2 for k in kraus))
        spectral = float(np.sort(p)[-Q:].sum())
        assert fe <= spectral + 2e-12
        # Explicit decoded reference-output state has a decomposition into
        # vectors whose Schmidt coefficient matrices have rank at most Q.
        for k in kraus:
            target_matrix = np.diag(np.sqrt(p)) @ k.T
            assert np.linalg.matrix_rank(target_matrix, tol=1e-12) <= Q
        bottlenecks.append({"Q": Q, "entanglement_fidelity": fe,
                            "top_Q_spectral_mass": spectral,
                            "composite_kraus_rank_bound": Q})
    return {"stinespring": records, "bottlenecks": bottlenecks}


def main():
    result = {"status": "passed; finite diagnostic only",
              "spectra": audit_spectra(), "channels": audit_channels()}
    out = Path(__file__).with_name("pure_quantum_lower_check.json")
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
