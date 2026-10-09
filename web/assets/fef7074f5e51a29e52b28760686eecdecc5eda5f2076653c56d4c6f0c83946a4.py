#!/usr/bin/env python3
"""Markov burst/reset and reversible-write-cost diagnostics.

The q, alpha model is an effective post-selection incorporation process, not
an empirical fit to a particular polymerase. The run-reset calculation is exact
for the stated renewal policy. The example values are illustrative only.
"""
from math import lgamma, log, log2


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


def work_bits_per_site(q: float, alpha: float) -> float:
    """Reversible work lower bound in bits/site for the uniform-register model."""
    row = stationary_markov(q, alpha)
    return row["total_register_write_bound_bits_per_site"]


def max_cluster_tail_at_work(q: float, budget_bits: float, m: int) -> dict[str, float]:
    """Sharp max P(L>=m) in the homogeneous first-order Markov class.

    Positive clustering means alpha>=q. Work is monotone increasing with alpha
    there, so bisection gives the exact Markov-class frontier. The bound is a
    reversible-work lower bound for a randomized equal-energy output register,
    not a prediction for an autonomous biological copier.
    """
    if m < 1:
        raise ValueError("m must be positive")
    iid = work_bits_per_site(q, q)
    if budget_bits < iid - 1e-12:
        raise ValueError("budget is below the independent-channel work bound")
    high_work = 2.0 - q * log2(3.0)
    if budget_bits >= high_work:
        alpha_max = 1.0
    else:
        lo, hi = q, 1.0
        for _ in range(100):
            mid = (lo + hi) / 2.0
            if work_bits_per_site(q, mid) <= budget_bits:
                lo = mid
            else:
                hi = mid
        alpha_max = lo
    return {
        "iid_work_floor_bits_per_site": iid,
        "work_budget_bits_per_site": budget_bits,
        "max_alpha_in_Markov_class": alpha_max,
        "max_cluster_tail_ge_m": alpha_max ** (m - 1),
        "max_mean_cluster_length": float("inf") if alpha_max == 1.0 else 1.0 / (1.0 - alpha_max),
    }


def latent_bad_blocks(q: float, bad_fraction: float, block_length: int,
                      run_length: int) -> dict[str, float]:
    """Stationary block-mode counterexample to exponential cluster suppression.

    Independently for each block, choose a bad mode with probability
    `bad_fraction`; in that mode every site is wrong. In the good mode, errors
    are iid Bernoulli(q0), where q0 preserves the marginal error rate q. A
    uniform random block phase makes the bi-infinite process stationary. Wrong
    base identities are assumed iid uniform among the three alternatives.

    The block entropy is computed exactly from its probability mass function.
    `excess_correlation_bits_per_site` is the extra equilibrium-register write
    bound over an iid error channel with the same q. The controller's finite
    phase/mode reset and chemical implementation are not included.
    """
    lam = bad_fraction
    b = block_length
    m = run_length
    if not (0.0 < q < 1.0 and 0.0 < lam < q and q < 1.0):
        raise ValueError("require 0 < bad_fraction < q < 1")
    if not (1 <= m <= b):
        raise ValueError("require 1 <= run_length <= block_length")
    q0 = (q - lam) / (1.0 - lam)
    p_all = lam + (1.0 - lam) * q0 ** b
    h_block = -p_all * log2(p_all)
    ln2 = log(2.0)
    # Every non-all-one error word has probability
    # (1-lambda) q0^k (1-q0)^(B-k); sum by Hamming weight.
    for k in range(b):
        log_count = (lgamma(b + 1) - lgamma(k + 1) - lgamma(b - k + 1)) / ln2
        log_word_probability = (log2(1.0 - lam) + k * log2(q0)
                                + (b - k) * log2(1.0 - q0))
        layer_probability = 2.0 ** (log_count + log_word_probability)
        h_block -= layer_probability * log_word_probability
    h_rate = h_block / b
    iid_error_entropy = h2(q)
    write_floor = 2.0 - q * log2(3.0) - iid_error_entropy
    excess = iid_error_entropy - h_rate
    # Exact m-window event under a uniform random block phase. A window that
    # crosses one boundary splits into independent suffix/prefix events.
    p_m_lower = lam * (b - m + 1) / b
    p_m_exact = ((b - m + 1) * (lam + (1.0 - lam) * q0 ** m)
                 + sum((lam + (1.0 - lam) * q0 ** k)
                       * (lam + (1.0 - lam) * q0 ** (m-k))
                       for k in range(1, m))) / b
    return {
        "q": q,
        "bad_mode_fraction": lam,
        "good_mode_error_probability": q0,
        "block_length": float(b),
        "run_length": float(m),
        "error_entropy_rate_bits_per_site": h_rate,
        "iid_error_entropy_bits_per_site": iid_error_entropy,
        "excess_correlation_bits_per_site": excess,
        "iid_uniform_register_copy_floor_bits_per_site": write_floor,
        "excess_as_fraction_of_iid_copy_floor": excess / write_floor,
        "all_error_window_probability_lower_bound": p_m_lower,
        "all_error_window_probability_exact": p_m_exact,
        "iid_all_error_window_probability": q ** m,
    }


def universal_run_tail_envelope(q: float, excess_correlation_bits: float,
                                run_length: int) -> dict[str, float]:
    """A non-sharp stationary-process bound on run tails from q and entropy.

    For q<=1/2, the entropy rate h=h2(q)-c is at most
    G_q(s)=H(E_i|E_{i-1}), where s=P(0,1)=P(1,0) is the run-start density.
    Inverting the increasing branch of G_q gives a lower bound on s. The
    mass-transport identity q=s E[L] and Markov's inequality then bound
    P(L>=m | run start) <= q/(m s). This is universal but generally loose.
    """
    if not (0.0 < q <= 0.5):
        raise ValueError("require 0 < q <= 1/2")
    if run_length < 1:
        raise ValueError("run_length must be positive")
    if not (0.0 <= excess_correlation_bits <= h2(q) + 1e-12):
        raise ValueError("correlation excess must be between zero and h2(q)")
    h_rate = max(0.0, h2(q) - excess_correlation_bits)

    def pair_conditional_entropy(s: float) -> float:
        return ((1.0 - q) * h2(s / (1.0 - q))
                + q * h2(1.0 - s / q))

    lo, hi = 0.0, q * (1.0 - q)
    for _ in range(100):
        mid = (lo + hi) / 2.0
        if pair_conditional_entropy(mid) >= h_rate:
            hi = mid
        else:
            lo = mid
    start_rate_lower = hi
    tail_upper = (1.0 if start_rate_lower == 0.0 else
                  min(1.0, q / (run_length * start_rate_lower)))
    return {
        "error_entropy_rate_bits_per_site": h_rate,
        "run_start_rate_lower_bound": start_rate_lower,
        "run_tail_upper_bound": tail_upper,
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
    frontier = max_cluster_tail_at_work(q, work_bits_per_site(q, q) + 0.01, m=10)
    print("Markov-class work/cluster frontier; 0.01 extra bits/site")
    for key, value in frontier.items():
        print(f"  {key}={value:.12g}")
    reset = reset_after_run(q, alpha, m)
    print("run-reset policy; m=3")
    for key, value in reset.items():
        print(f"  {key}={value:.12g}")
    block = latent_bad_blocks(q=0.01, bad_fraction=0.001,
                              block_length=1000, run_length=10)
    print("stationary latent bad-block counterexample")
    for key, value in block.items():
        print(f"  {key}={value:.12g}")
    run_bound = universal_run_tail_envelope(
        q=block["q"],
        excess_correlation_bits=block["excess_correlation_bits_per_site"],
        run_length=10,
    )
    print("universal conditional run-tail envelope for block example")
    for key, value in run_bound.items():
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
