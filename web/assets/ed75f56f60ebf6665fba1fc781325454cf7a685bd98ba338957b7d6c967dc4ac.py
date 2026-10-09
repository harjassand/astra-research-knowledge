#!/usr/bin/env python3
"""Finite Curie-Weiss check of an exact global-symmetry move.

This is a diagnostic, not a proof of a molecular result. It compares the
conductance of the positive-magnetization cut for single-spin Metropolis
updates and for a 50/50 mixture with the global spin-flip symmetry.
"""

from math import comb, exp, log


def logsumexp(values):
    peak = max(values)
    return peak + log(sum(exp(v - peak) for v in values))


def energy(n, coupling, magnetization):
    return -coupling * magnetization * magnetization / (2.0 * n)


def local_cross_probability(n, beta, coupling, magnetization):
    """Probability local Metropolis leaves m>0, given m>0."""
    if magnetization <= 0:
        return 0.0
    # From positive m, a one-spin update can reach m<=0 only at m=1 (odd n)
    # or m=2 (even n).
    if n % 2:
        if magnetization != 1:
            return 0.0
        plus_count = (n + magnetization) // 2
        target = magnetization - 2
        proposal = plus_count / n
    else:
        if magnetization != 2:
            return 0.0
        plus_count = (n + magnetization) // 2
        target = magnetization - 2
        proposal = plus_count / n
    delta = energy(n, coupling, target) - energy(n, coupling, magnetization)
    return proposal * min(1.0, exp(-beta * delta))


def evaluate(n, beta, coupling, group_refresh_probability=0.5):
    mags = list(range(-n, n + 1, 2))
    log_weights = [
        log(comb(n, (n + m) // 2)) - beta * energy(n, coupling, m)
        for m in mags
    ]
    normalizer = logsumexp(log_weights)
    probs = [exp(w - normalizer) for w in log_weights]
    pi = dict(zip(mags, probs))
    positive_mass = sum(p for m, p in pi.items() if m > 0)

    # Exact flow across A={m>0} under the local update.
    local_flow = sum(
        pi[m] * local_cross_probability(n, beta, coupling, m)
        for m in mags
        if m > 0
    )
    local_phi = local_flow / positive_mass

    # A uniform draw from G={identity, global flip} is the conditional orbit
    # refresh. It flips with probability 1/2 and is always accepted.
    augmented_phi = (1.0 - group_refresh_probability) * local_phi + group_refresh_probability / 2.0

    # Check detailed balance for the one-dimensional lumped birth-death chain.
    max_db_local = 0.0
    max_db_augmented = 0.0
    for m in mags:
        for step in (-2, 2):
            target = m + step
            if target < -n or target > n:
                continue
            count = (n + m) // 2
            proposal = (count / n) if step == -2 else ((n - count) / n)
            delta = energy(n, coupling, target) - energy(n, coupling, m)
            accept = min(1.0, exp(-beta * delta))
            p_forward_local = proposal * accept

            target_count = (n + target) // 2
            reverse_proposal = (target_count / n) if step == 2 else ((n - target_count) / n)
            reverse_delta = energy(n, coupling, m) - energy(n, coupling, target)
            p_reverse_local = reverse_proposal * min(1.0, exp(-beta * reverse_delta))

            # Symmetry flip is a deterministic involution at magnetization level.
            p_forward_symmetry = 0.5 if target == -m else 0.0
            p_reverse_symmetry = 0.5 if m == -target else 0.0

            # Local chain is reversible; the global-flip kernel is checked
            # separately below because its jump need not be a single-spin edge.
            max_db_local = max(
                max_db_local,
                abs(pi[m] * p_forward_local - pi[target] * p_reverse_local),
            )
            p_forward = (1.0 - group_refresh_probability) * p_forward_local + group_refresh_probability * p_forward_symmetry
            p_reverse = (1.0 - group_refresh_probability) * p_reverse_local + group_refresh_probability * p_reverse_symmetry
            max_db_augmented = max(
                max_db_augmented,
                abs(pi[m] * p_forward - pi[target] * p_reverse),
            )

    # Check all global-flip pairs, including states not connected by a local edge.
    for m in mags:
        target = -m
        lhs = pi[m] * group_refresh_probability / 2.0
        rhs = pi[target] * group_refresh_probability / 2.0
        max_db_augmented = max(max_db_augmented, abs(lhs - rhs))

    return local_phi, augmented_phi, max_db_local, max_db_augmented


def main():
    beta_coupling = 2.0
    print("n,betaJ,local_positive_cut_conductance,with_global_flip_conductance,max_DB_local,max_DB_mixture")
    for n in (8, 16, 32, 48, 64, 96, 128):
        local_phi, augmented_phi, db_local, db_augmented = evaluate(
            n, beta=1.0, coupling=beta_coupling, group_refresh_probability=0.5
        )
        print(
            f"{n},{beta_coupling:.1f},{local_phi:.12g},{augmented_phi:.12g},"
            f"{db_local:.3g},{db_augmented:.3g}"
        )


if __name__ == "__main__":
    main()
