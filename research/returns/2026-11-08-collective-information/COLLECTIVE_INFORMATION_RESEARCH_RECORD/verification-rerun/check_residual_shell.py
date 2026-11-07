"""Finite algebra diagnostic only; no claim of physical validation or priority."""

from pathlib import Path
import json
import math
import numpy as np


def invroot(a, tolerance=1e-10):
    values, vectors = np.linalg.eigh((a + a.T) / 2)
    keep = values > tolerance
    return (vectors[:, keep] / np.sqrt(values[keep])) @ vectors[:, keep].T


def symmetric_generator(q, probability):
    root = np.sqrt(probability)
    a = root[:, None] * (-q) / root[None, :]
    assert np.max(np.abs(a - a.T)) < 2e-10
    return (a + a.T) / 2


def exponential(a, time):
    values, vectors = np.linalg.eigh((a + a.T) / 2)
    assert min(values) > -1e-8
    return (vectors * np.exp(-time * np.maximum(values, 0))) @ vectors.T


def transfer_partition(m, pair_weight):
    state = np.zeros((m + 1, 2))
    state[0, 0] = 1
    state[1, 1] = 1
    for length in range(1, m):
        following = np.zeros_like(state)
        for count in range(length + 1):
            for previous in (0, 1):
                for bit in (0, 1):
                    following[count + bit, bit] += (
                        state[count, previous] * pair_weight ** (previous * bit)
                    )
        state = following
    return state.sum(axis=1)


def main():
    m, kappa, collective_strength = 6, 1000.0, 4.0
    pair_weight = 1.005
    x = ((np.arange(2**m)[:, None] >> np.arange(m)) & 1).astype(int)
    counts = x.sum(axis=1)
    residual = -math.log(pair_weight) * (x[:, :-1] * x[:, 1:]).sum(axis=1)
    collective = -collective_strength * (np.arange(m + 1) - m / 2) ** 2 / m
    energy = residual + collective[counts]
    probability = np.exp(-energy)
    probability /= probability.sum()
    z = np.bincount(counts, weights=np.exp(-residual), minlength=m + 1)
    partition_error = float(np.max(np.abs(z - transfer_partition(m, pair_weight))))
    assert partition_error < 2e-12

    fast = np.zeros((2**m, 2**m))
    slow = np.zeros_like(fast)
    bare_plus, bare_minus, insertion = (np.zeros(m + 1) for _ in range(3))
    for state in range(2**m):
        k = counts[state]
        shell_weight = math.exp(-residual[state]) / z[k]
        for site in range(m):
            target = state ^ (1 << site)
            neighbor_sum = sum(x[state, j] for j in (site - 1, site + 1) if 0 <= j < m)
            mobility = 1.0 + 0.17 * neighbor_sum
            bare = mobility * math.exp(-(residual[target] - residual[state]) / 2)
            slow[state, target] = bare * math.exp(-(collective[counts[target]] - collective[k]) / 2)
            if x[state, site] == 0:
                bare_plus[k] += shell_weight * bare
                insertion[k] += shell_weight * math.exp(-(residual[target] - residual[state]))
            else:
                bare_minus[k] += shell_weight * bare
        for site in range(m - 1):
            if x[state, site] != x[state, site + 1]:
                target = state ^ (1 << site) ^ (1 << (site + 1))
                fast[state, target] = kappa * math.exp(-(residual[target] - residual[state]) / 2)
    for q in (fast, slow):
        np.fill_diagonal(q, -q.sum(axis=1))

    insertion_error = float(np.max(np.abs(insertion[:-1] - np.arange(1, m + 1) * z[1:] / z[:-1])))
    edge_flux_error = float(np.max(np.abs(z[:-1] * bare_plus[:-1] - z[1:] * bare_minus[1:])))
    assert insertion_error < 2e-12 and edge_flux_error < 2e-12

    coarse_probability = np.bincount(counts, weights=probability, minlength=m + 1)
    phi = np.sqrt(probability)[:, None] * (counts[:, None] == np.arange(m + 1))
    phi /= np.sqrt(coarse_probability)[None, :]
    assert np.linalg.norm(phi.T @ phi - np.eye(m + 1)) < 1e-12
    _, _, vh = np.linalg.svd(phi.T, full_matrices=True)
    psi = vh[m + 1 :].T
    f = symmetric_generator(fast, probability)
    b = symmetric_generator(slow, probability)
    a00 = phi.T @ b @ phi
    a11 = psi.T @ (f + b) @ psi
    coupling = psi.T @ b @ phi
    d_exact = float(np.linalg.norm(invroot(a11) @ coupling @ invroot(a00), 2))
    cc = float(np.linalg.norm(coupling @ invroot(a00), 2) ** 2)
    fast_values = np.linalg.eigvalsh(psi.T @ f @ psi)
    gamma = float(min(fast_values))
    d_bound = math.sqrt(cc / gamma)
    assert d_exact <= d_bound + 1e-10

    coarse_q = -a00 * np.sqrt(coarse_probability)[None, :] / np.sqrt(coarse_probability)[:, None]
    transient = counts < m
    micro_q = (fast + slow)[np.ix_(transient, transient)]
    micro_h = np.linalg.solve(-micro_q, np.ones(sum(transient)))
    micro_tau = float(probability[transient] @ micro_h / sum(probability[transient]))
    coarse_h = np.linalg.solve(-coarse_q[:m, :m], np.ones(m))
    coarse_tau = float(coarse_probability[:m] @ coarse_h / sum(coarse_probability[:m]))
    lifetime_ratio = micro_tau / coarse_tau
    assert lifetime_ratio >= 1 - 1e-9
    assert lifetime_ratio <= 1 / (1 - d_bound**2) + 1e-9

    # Perturb plus and minus bare rates independently, then reconstruct one
    # reversible learned mass. This deliberately does not preserve true pi.
    rng = np.random.default_rng(1207)
    eta = 0.001
    plus_hat = bare_plus * (1 + rng.uniform(-eta, eta, m + 1))
    minus_hat = bare_minus * (1 + rng.uniform(-eta, eta, m + 1))
    z_hat = np.ones(m + 1)
    for k in range(m):
        z_hat[k + 1] = z_hat[k] * plus_hat[k] / minus_hat[k + 1]
    mass_hat = z_hat * np.exp(-collective)
    mass_hat /= mass_hat.sum()
    learned_q = np.zeros_like(coarse_q)
    for k in range(m + 1):
        if k < m:
            learned_q[k, k + 1] = plus_hat[k] * math.exp(-(collective[k + 1] - collective[k]) / 2)
        if k > 0:
            learned_q[k, k - 1] = minus_hat[k] * math.exp(-(collective[k - 1] - collective[k]) / 2)
    np.fill_diagonal(learned_q, -learned_q.sum(axis=1))
    h = symmetric_generator(learned_q, mass_hat)
    mass_ratio = mass_hat / coarse_probability
    c = np.sqrt(coarse_probability)[:, None] * (-learned_q) / np.sqrt(coarse_probability)[None, :]
    c = mass_ratio[:, None] * c
    assert np.max(abs(c - c.T)) < 1e-11
    dm = float(np.max(abs(mass_ratio - 1)))
    dc = float(np.linalg.norm(invroot(a00) @ (c - a00) @ invroot(a00), 2))
    delta = max(dm, dc)
    observed_error = 0.0
    for time in np.logspace(-5, 6, 121):
        learned = exponential(h, time) * np.sqrt(mass_ratio)[None, :] / np.sqrt(mass_ratio)[:, None]
        observed_error = max(observed_error, float(np.linalg.norm(exponential(a00, time) - learned, 2)))
    assert observed_error <= 8 * delta / (1 - delta) + 1e-9

    output = {
        "scope": "finite algebra diagnostic; not a proof of general claims or physical validation",
        "sites": m,
        "partition_transfer_error": partition_error,
        "positive_insertion_error": insertion_error,
        "coarse_edge_flux_error": edge_flux_error,
        "exact_relative_offdiagonal_norm": d_exact,
        "variance_gap_bound": d_bound,
        "microscopic_mean_lifetime": micro_tau,
        "coarse_mean_lifetime": coarse_tau,
        "mean_lifetime_ratio": lifetime_ratio,
        "mean_lifetime_ratio_upper_bound": 1 / (1 - d_bound**2),
        "mass_error": dm,
        "relative_form_error": dc,
        "mass_metric_observed_operator_error": observed_error,
        "mass_metric_operator_bound": 8 * delta / (1 - delta),
        "sampled_times": 121,
    }
    destination = Path(__file__).with_name("RESIDUAL_SHELL_CHECK.json")
    destination.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
