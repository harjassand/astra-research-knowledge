"""Synthetic real-trajectory interface and independent population audit.

The learner receives only executed action counts and terminal binary reads.
The native device is a hidden, order-dependent finite transducer. Its model
is used only by the generator and the separately labelled population audit.
KT/OPE is an established method, not claimed as a new algorithm here.
"""
from pathlib import Path
from fractions import Fraction
from math import comb, factorial, log, sqrt, ceil
import hashlib
import json
import numpy as np
from scipy.special import gammaln
from scipy.stats import binom

ROOT = Path(__file__).resolve().parent
RECORDS = ROOT / "controller_learning_records"
RECORDS.mkdir(exist_ok=True)
T = 64
N = 131072
L = 4096
BETA = 0.01
SEED = 202610290601


def actual_episodes(n, seed, probability_numerator=None):
    """One fresh hidden parameter per prepared episode, retained within it.

    A0: x <- 2x+z+1 mod 7. A1: x <- 3x+2z+1 mod 7.
    z is hidden and frozen, x initially zero. These maps need not commute.
    A terminal binary sensor has success probability 19/20 when both the
    count window and hidden endpoint gate hold, and 1/20 otherwise.
    The action RNG uses finite integer choices; no continuous policy draw.
    """
    rng = np.random.default_rng(seed)
    z = rng.integers(0, 3, size=n, dtype=np.uint8)
    state = np.zeros(n, dtype=np.uint8)
    counts = np.zeros(n, dtype=np.uint8)
    packed = np.zeros((n, T // 8), dtype=np.uint8)
    for t in range(T):
        if probability_numerator is None:
            selector = rng.integers(0, 2*t+2, size=n)
            action = selector < (2*counts.astype(np.int64)+1)
        else:
            selector = rng.integers(0, L, size=n)
            action = selector < probability_numerator
        counts += action.astype(np.uint8)
        packed[:, t//8] |= action.astype(np.uint8) << (t % 8)
        state = np.where(action, 3*state+2*z+1, 2*state+z+1) % 7
    gate = ((counts >= 44) & (counts <= 52)
            & np.isin(state, [0, 1, 3]))
    readout = (rng.integers(0, 20, size=n) < np.where(gate, 19, 1))
    # Private selector draws and hidden z/state are not supplied to learner.
    return packed, counts, readout.astype(np.uint8)


def conditional_population_response():
    """Independent audit: uniform action words conditional on their count.

    The recursion is a positive averaging recursion, avoiding enormous
    word multiplicities. It is not used to select the empirical policy.
    """
    g = np.zeros(T+1)
    for z in range(3):
        dist = np.zeros((T+1, 7))
        dist[0, 0] = 1
        map0 = (2*np.arange(7)+z+1) % 7
        map1 = (3*np.arange(7)+2*z+1) % 7
        for t in range(1, T+1):
            nxt = np.zeros_like(dist)
            for k in range(t+1):
                if k < t:
                    nxt[k, map0] += (t-k)/t * dist[k]
                if k > 0:
                    nxt[k, map1] += k/t * dist[k-1]
            dist = nxt
        assert np.max(np.abs(dist.sum(axis=1)-1)) < 1e-13
        g += dist[:, [0, 1, 3]].sum(axis=1)/3
    return 0.05 + 0.9*((np.arange(T+1)>=44)
                           & (np.arange(T+1)<=52))*g


def exact_kt_checks():
    checks = []
    for t in [1, 2, 3, 8, 16, 32, 64]:
        largest = Fraction(0)
        for k in range(t+1):
            qword = Fraction(factorial(2*k)*factorial(2*(t-k)),
                             4**t*factorial(k)*factorial(t-k)*factorial(t))
            target = Fraction(k**k*(t-k)**(t-k), t**t)
            ratio = target/qword
            assert ratio*ratio <= 4*(t+1)
            largest = max(largest, ratio)
        endpoint = Fraction(4**t, comb(2*t, t))
        assert largest == endpoint
        checks.append({"T": t, "exact_max_ratio": str(largest),
                       "max_ratio_float": float(largest)})
    return checks


def lower_bound_checks():
    rows = []
    for n in [4096, 16384, 65536, 262144]:
        r = ceil(sqrt(n))
        centers = np.arange(ceil(n/8), n//4+1, 2*r+1)
        masses = [binom.cdf(int(m+r), n, m/n)
                  - binom.cdf(int(m-r-1), n, m/n) for m in centers]
        assert len(centers) >= 4
        assert min(masses) >= 0.75
        assert np.all(np.diff(centers)>2*r)
        delta = 0.2
        kl = -0.5*log(1-4*delta*delta)
        assert kl <= (8/3)*delta*delta
        rows.append({"n": n, "boxes": len(centers),
                     "boxes_over_sqrt_n": len(centers)/sqrt(n),
                     "minimum_target_box_probability": min(masses),
                     "chebyshev_guarantee": 1-n/(4*r*r)})
    return rows


def main():
    actions, counts, reads = actual_episodes(N, SEED)
    np.savez_compressed(RECORDS / "kt_bank.npz", actions=actions,
                        counts=counts, reads=reads)
    assert np.array_equal(np.unpackbits(actions, axis=1, bitorder="little")
                          .sum(axis=1), counts)
    k = np.arange(T+1)
    qcount = np.exp(gammaln(T+1)-gammaln(k+1)-gammaln(T-k+1)
                    +gammaln(k+0.5)+gammaln(T-k+0.5)
                    -2*gammaln(0.5)-gammaln(T+1))
    assert abs(qcount.sum()-1) < 1e-12
    observed_counts = np.bincount(counts, minlength=T+1)
    observed_rewards = np.bincount(counts, weights=reads, minlength=T+1)
    # All policy selection uses only actual count/readout records.
    pgrid = np.arange(L+1)/L
    pmfs = binom.pmf(k[None, :], T, pgrid[:, None])
    estimates = pmfs @ (observed_rewards/(N*qcount))
    chosen_index = int(np.argmax(estimates))
    chosen_p = float(pgrid[chosen_index])
    C = 2*sqrt(T+1)
    x = log(2*(L+1)/BETA)
    radius = sqrt(2*C*x/N)+2*C*x/(3*N)
    regret_bound = 2*radius+T/L
    lower_value = max(0, float(estimates[chosen_index])-radius)
    upper_half = min(1, float(estimates[L//2])+radius)

    # Separate audit after selection; hidden model is not in the learner.
    coefficients = conditional_population_response()
    population_values = pmfs @ coefficients
    population_chosen = float(population_values[chosen_index])
    population_best = float(population_values.max())
    pop_error = np.max(np.abs(estimates-population_values))
    assert pop_error <= radius  # This seeded run passes; not the confidence proof.
    assert population_best-population_chosen <= regret_bound

    validation_n = 65536
    va, vc, vr = actual_episodes(validation_n, SEED+1, chosen_index)
    np.savez_compressed(RECORDS / "fresh_selected_deployment.npz",
                        actions=va, counts=vc, reads=vr)
    validation_mean = float(vr.mean())
    validation_radius = sqrt(log(2/BETA)/(2*validation_n))

    # Noncommutation/order sensitivity at equal counts, independently checked.
    def endpoint(word, z=0):
        s = 0
        for a in word:
            s = ((3*s+2*z+1) if a else (2*s+z+1)) % 7
        return s
    order_witness = {"word_01_endpoint": endpoint([0, 1]),
                     "word_10_endpoint": endpoint([1, 0]),
                     "same_action_counts": True}
    assert endpoint([0, 1]) != endpoint([1, 0])

    output = {
        "status": "synthetic samples; established KT/OPE method; no apparatus claim",
        "T": T, "N": N, "grid_denominator": L, "bank_beta": BETA,
        "seed": SEED, "chosen_p": chosen_p,
        "estimated_value": float(estimates[chosen_index]),
        "uniform_value_radius": radius,
        "certified_global_regret": regret_bound,
        "certified_selected_value_lower": lower_value,
        "certified_improvement_over_p_half": lower_value-upper_half,
        "population_chosen_value": population_chosen,
        "population_best_grid_value": population_best,
        "population_best_grid_p": float(pgrid[np.argmax(population_values)]),
        "population_grid_regret": population_best-population_chosen,
        "population_p_half_value": float(population_values[L//2]),
        "population_deterministic_values": [float(population_values[0]),
                                             float(population_values[-1])],
        "largest_grid_estimation_error": float(pop_error),
        "minimum_type_sample_count": int(observed_counts.min()),
        "KT_bound": C, "uniform_action_worst_ratio": 2**T,
        "ordinary_comparator": "KT policy-bank method itself is established; same-interface tie",
        "independent_selected_deployment": {
            "N": validation_n, "mean": validation_mean,
            "hoeffding_radius": validation_radius, "beta": BETA,
            "inside_population_interval_this_run":
                abs(validation_mean-population_chosen) <= validation_radius},
        "physical_ledger": {
            "baseline_preparations": N+validation_n,
            "native_calls": (N+validation_n)*T,
            "terminal_reads": N+validation_n,
            "recorded_action_ids": (N+validation_n)*T,
            "integer_selector_draw_calls": (N+validation_n)*T,
            "terminal_noise_integer_draw_calls": N+validation_n,
            "controller_counter_resets": N+validation_n,
            "random_bit_count": "not measured; integer-generator calls are not bit cost",
            "physical_time": "not supplied by synthetic model"},
        "exact_KT_checks": exact_kt_checks(),
        "learning_lower_packing_checks": lower_bound_checks(),
        "order_witness": order_witness,
        "key_failure": {"q": 0.5, "p": 0.75,
                         "joint_support_mismatch_mass": 0.25},
        "frozen_bit_failure": {"variance_of_repeated_mean": 0.25,
                               "independent_mean_variance_would_be": 0.25/N}
    }
    hashes = {}
    for path in sorted(RECORDS.glob("*.npz")):
        hashes[path.name] = {"sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                             "bytes": path.stat().st_size}
    output["raw_records"] = hashes
    (ROOT / "CONTROLLER_LEARNING_CHECKS.json").write_text(
        json.dumps(output, indent=2)+"\n")
    print(json.dumps({key: output[key] for key in [
        "chosen_p", "certified_global_regret",
        "certified_improvement_over_p_half", "population_chosen_value",
        "population_grid_regret", "largest_grid_estimation_error",
        "physical_ledger"]}, indent=2))


if __name__ == "__main__":
    main()
