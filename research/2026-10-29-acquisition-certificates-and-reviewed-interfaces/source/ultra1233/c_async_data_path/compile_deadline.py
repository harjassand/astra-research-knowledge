"""Exact finite scalar receiver; no stochastic path/real-number oracle."""
import argparse
from fractions import Fraction as F
import json
from pathlib import Path
import time


def frac(x):
    return {"numerator": str(x.numerator), "denominator": str(x.denominator),
            "decimal_diagnostic": format(float(x), ".17g")}


def ceildiv(a, b):
    return -((-a) // b)


def acquire(M, B, q, precision_bits, horizon):
    if min(M, B, q, precision_bits) < 1 or horizon < 0:
        raise ValueError("positive discrete parameters and nonnegative horizon")
    N = (B + 1) * M + 1
    width = 2 * (16 * M - 1).bit_length()
    C = 2 * M * q
    W = M * (M + 1) // 2
    lam = F(1, 16 * N * (C + 1) * width)
    Lambda = N * lam
    p_cover = F(M, 1 << (width // 2))
    assert p_cover <= F(1, 16)
    assert Lambda * width == F(1, 16 * (C + 1))
    # Completely rational relaxations of the logarithmic moment bound.
    log_mgf_upper = (-F(1, 2 * (C + 1)) + p_cover / (C + 1)
                     + 2 * Lambda * width)
    rate = F(5, 16 * (C + 1))
    assert log_mgf_upper <= -rate
    single_rounds = ceildiv(16 * (W + (C + 1) * precision_bits), 5)
    roots = ceildiv(horizon, width) + 1
    paid_bits = precision_bits + (roots - 1).bit_length()
    uniform_rounds = ceildiv(16 * (W + (C + 1) * paid_bits), 5)
    return {
        "status": "EXACT_DEADLINE_OR_EDIT_RECEIVER",
        "inputs": {"capacity": M, "packet_bits": B, "fault_support_bits": q,
                   "clock_rate_interval": ["1/2", "2"],
                   "requested_tail_bits": precision_bits,
                   "all_input_acceptance_horizon": horizon},
        "controller": {"physical_noisy_bits": N, "noiseless_persistent_bits": 0,
                       "persistent_counters": 0, "history_tape_bits": 0,
                       "nearest_neighbor_stage_local": True,
                       "largest_nominal_support_bits": 2 * B + 3,
                       "nominal_maps": M + 1,
                       "per_bit_nominal_diamond_norm_density_upper": 12,
                       "physical_atomicity_and_hardware": "NOT_ACQUIRED"},
        "noise": {"per_bit_rate_upper": frac(lam), "total_rate_upper": frac(Lambda),
                  "future_dependent_fault_labels": True,
                  "positive_independent_fault_support_streams_required": True,
                  "signed_bath_flags_admitted": False},
        "queue_contract": {"capacity": M, "all_tag_states_valid": True,
                           "edits_per_q_bit_fault_upper": 2 * q,
                           "initial_ghost_packets_upper": M,
                           "prefix_invariant": "d(O Q_T,Q_0 I)<=2q F(T)",
                           "initially_empty_and_drained": "d(O,I)<=2q F(T)"},
        "schedule_workload": {"fixed_analysis_window": width, "initial_upper": W,
                              "fault_work_increase_upper": C,
                              "coverage_failure_upper": frac(p_cover),
                              "dominating_arrival_mean_upper": frac(F(1, 8)),
                              "exponential_drift_rate": frac(rate),
                              "mean_empty_epoch_time_upper_fixed_start": frac(F(8 * W * width, 7)),
                              "global_window_boundaries_are_physical_clock": False},
        "single_start": {"rounds": single_rounds,
                         "time_with_one_alignment_window": width * (single_rounds + 1),
                         "tail_upper": frac(F(1, 1 << precision_bits))},
        "all_future_selected_starts": {"candidate_fixed_boundaries": roots,
                                       "paid_tail_bits": paid_bits,
                                       "rounds": uniform_rounds,
                                       "latency_upper": width * (uniform_rounds + 1),
                                       "union_tail_upper": frac(F(roots, 1 << paid_bits)),
                                       "requested_tail_upper": frac(F(1, 1 << precision_bits))},
        "interpretation": {"delivery": "deadline OR packet edited by an explicitly counted fault",
                           "empty_epoch": "hitting time; not guaranteed empty at the final observation",
                           "acceptance": "causal local capture/commit; scalar false notifications not excluded",
                           "protected_logical_stream": "NOT_ACQUIRED",
                           "unknown_logical_qubit_decoder": "NOT_ACQUIRED"}}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--capacity", type=int, default=3)
    parser.add_argument("--packet-bits", type=int, default=2)
    parser.add_argument("--q", type=int, default=2)
    parser.add_argument("--precision-bits", type=int, default=20)
    parser.add_argument("--horizon", type=int, default=1024)
    args = parser.parse_args()
    start = time.perf_counter()
    out = acquire(args.capacity, args.packet_bits, args.q, args.precision_bits, args.horizon)
    out["actual_acquisition"] = {"seconds_after_imports": time.perf_counter() - start,
                                 "trajectories": 0, "state_samples": 0,
                                 "real_transcendental_oracles": 0,
                                 "work": "constant many integer/rational operations on O(p+log M+log q+log horizon) bit operands; output probabilities themselves have O(p+log horizon) bits; no state enumeration"}
    path = Path(__file__).resolve().parent / "DEADLINE.json"
    path.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({"status": out["status"], "lambda": str(out["noise"]["per_bit_rate_upper"]),
                      "uniform_latency": out["all_future_selected_starts"]["latency_upper"],
                      "seconds": out["actual_acquisition"]["seconds_after_imports"]}))


if __name__ == "__main__":
    main()
