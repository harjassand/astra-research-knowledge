#!/usr/bin/env python3
"""Markov burst/reset and reversible-write-cost diagnostics.

The q, alpha model is an effective post-selection incorporation process, not
an empirical fit to a particular polymerase. The run-reset calculation is exact
for the stated renewal policy. The example values are illustrative only.
"""
from math import log2


def h2(p: float) -> float:
    if p in (0.0, 1.0):
        return 0.0
    return -p * log2(p) - (1.0 - p) * log2(1.0 - p)


def stationary_markov(q: float, alpha: float) -> dict[str, float]:
    """Stationary error-chain cluster and equilibrium-register work terms.

    q = P(E_i=1), alpha = P(E_{i+1}=1 | E_i=1).
    Wrong bases are uniform among the other 3 choices, independently given E.
    The register reference is initially uniform over equal-energy 4-letter
    sequences. Work units are kBT*ln(2) per reported bit.
    """
    if not (0.0 < q < 1.0 and 0.0 <= alpha < 1.0):
        raise ValueError("require 0<q<1 and 0<=alpha<1")
    beta = q * (1.0 - alpha) / (1.0 - q)
    if beta > 1.0:
        raise ValueError("alpha is incompatible with a stochastic stationary chain")
    assert abs(q - ((1.0 - q) * beta + q * alpha)) < 1e-12
    h_rate = (1.0 - q) * h2(beta) + q * h2(alpha)
    iid_bits = 2.0 - h2(q) - q * log2(3.0)
    corr_bits = h2(q) - h_rate
    write_bits = 2.0 - q * log2(3.0) - h_rate
    assert abs(write_bits - iid_bits - corr_bits) < 1e-12
    return {
        "q": q,
        "alpha": alpha,
        "beta": beta,
        "cluster_start_rate": q * (1.0 - alpha),
        "mean_cluster_length": 1.0 / (1.0 - alpha),
        "cluster_tail_ge_10": alpha ** 9,
        "error_entropy_rate_bits": h_rate,
        "iid_register_write_bound_bits_per_site": iid_bits,
        "error_correlation_excess_bits_per_site": corr_bits,
        "total_register_write_bound_bits_per_site": write_bits,
    }


def reset_after_run(q: float, alpha: float, m: int) -> dict[str, float]:
    """Exact renewal quantities if m consecutive errors are clipped and retried.

    A burst begins after a correct base with probability beta. Within a burst,
    each next base is wrong with probability alpha. On reaching length m, the
    last m bases are excised and the same segment is retried from a clean state.
    A terminal accepted burst therefore has length 0,...,m-1.
    """
    if m < 2:
        raise ValueError("m must be at least 2")
    beta = q * (1.0 - alpha) / (1.0 - q)
    reset_prob = beta * alpha ** (m - 1)
    accepted_prob = 1.0 - reset_prob
    # Unnormalised terminal-episode probabilities; reset attempts are geometric.
    masses = {ell: beta * (1.0 - alpha) * alpha ** (ell - 1)
              for ell in range(1, m)}
    out_length_num = (1.0 - beta) + sum(mass * (ell + 1)
                                          for ell, mass in masses.items())
    error_num = sum(ell * mass for ell, mass in masses.items())
    cluster_num = sum(masses.values())
    q_after = error_num / out_length_num
    cluster_rate = cluster_num / out_length_num
    resets_per_output = reset_prob / out_length_num
    extra_insertions_per_output = m * resets_per_output
    return {
        "beta": beta,
        "per_episode_reset_probability": reset_prob,
        "accepted_episode_probability": accepted_prob,
        "terminal_output_length_numerator": out_length_num,
        "post_reset_error_rate_before_MMR": q_after,
        "post_reset_cluster_rate": cluster_rate,
        "reset_events_per_output_base": resets_per_output,
        "extra_dNTP_insertions_per_output_base": extra_insertions_per_output,
        "copy_insertions_per_output_base": 1.0 + extra_insertions_per_output,
        "max_accepted_error_run": m - 1,
    }


def uncorrected_long_run_errors(q: float, alpha: float, m: int) -> float:
    """Error fraction in runs of length >=m in the no-reset Markov process."""
    return q * alpha ** (m - 1) * (m - (m - 1) * alpha)


def illustrative_costs(q: float, alpha: float, m: int, flank: int,
                       copy_attempt: float, reset_setup: float,
                       mmr_setup: float, mmr_per_base: float,
                       sitewise_setup: float) -> dict[str, float]:
    """Compare a reset+patch design to a same-raw-channel sitewise editor.

    Costs are arbitrary kBT units, not measured biological parameters.
    The baseline makes one first-pass copy and performs one replacement per
    initial mismatch. The candidate pays failed m-base reset insertions,
    resets, one MMR setup per surviving run, and patch synthesis. Patches are
    assumed not to overlap; epsilon=0 is the idealized perfect-repair case.
    """
    base = stationary_markov(q, alpha)
    reset = reset_after_run(q, alpha, m)
    q0 = q * alpha ** (m - 1) * (m - (m - 1) * alpha)
    # Exact expression above is long-run error mass left in unreset runs >=m.
    # The candidate clips all such runs; MMR repairs every accepted run <m.
    patched_bases = reset["post_reset_error_rate_before_MMR"] + flank * reset["post_reset_cluster_rate"]
    candidate_cost = (
        copy_attempt * reset["copy_insertions_per_output_base"]
        + reset_setup * reset["reset_events_per_output_base"]
        + mmr_setup * reset["post_reset_cluster_rate"]
        + mmr_per_base * patched_bases
    )
    sitewise_cost = (
        copy_attempt * (1.0 + q)
        + sitewise_setup * q
        + mmr_per_base * q
    )
    return {
        "no_reset_long_run_error_fraction_if_MMR_limit_is_m_minus_1": q0,
        "candidate_expected_patched_bases_per_output": patched_bases,
        "candidate_fuel_units_per_output": candidate_cost,
        "sitewise_fuel_units_per_output": sitewise_cost,
        "candidate_minus_sitewise_fuel": candidate_cost - sitewise_cost,
    }


def main() -> None:
    q, alpha, m = 0.01, 0.99, 3
    for label, a in (("iid", q), ("bursty", alpha), ("isolated-errors", 0.0)):
        row = stationary_markov(q, a)
        print(label)
        for key, value in row.items():
            print(f"  {key}={value:.12g}")
    reset = reset_after_run(q, alpha, m)
    print("run-reset policy; m=3")
    for key, value in reset.items():
        print(f"  {key}={value:.12g}")
    costs = illustrative_costs(q, alpha, m, flank=25,
                               copy_attempt=1.0, reset_setup=5.0,
                               mmr_setup=4.0, mmr_per_base=1.0,
                               sitewise_setup=4.0)
    print("illustrative cost comparison; arbitrary kBT units")
    for key, value in costs.items():
        print(f"  {key}={value:.12g}")


if __name__ == "__main__":
    main()
