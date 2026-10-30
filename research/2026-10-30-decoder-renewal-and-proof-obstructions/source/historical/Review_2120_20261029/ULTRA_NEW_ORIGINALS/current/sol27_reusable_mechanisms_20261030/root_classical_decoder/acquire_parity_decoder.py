"""Ordinary iid exhaustive acquisition vs paid repeated-environment acquisition.

Classical SIMULATION of flags and phase labels, not quantum/source execution.
Consumers receive only sample records; the secret is confined to fixture creation
and post-acquisition validation. The iid algorithm is an informed ordinary
incumbent (all parity correlations via Walsh transform), not a naive baseline.
"""
from __future__ import annotations
import argparse
import json
import math
from pathlib import Path
import time
import numpy as np


def parity(y: int, secret: int) -> int:
    return (int(y) & int(secret)).bit_count() & 1


def compile_decoder(secret: int, n: int) -> dict:
    support = [i for i in range(n) if secret >> i & 1]
    return {
        "classical_bits_little_endian": [(secret >> i) & 1 for i in range(n)],
        "reversible_circuit": (
            [["CX", f"flag_{i}", "work"] for i in support]
            + [["CZ", "work", "physical"]]
            + [["CX", f"flag_{i}", "work"] for i in reversed(support)]
        ),
        "initial_work_bit": 0,
        "discard_after": [f"flag_{i}" for i in range(n)] + ["work"],
    }


def iid_acquire(n: int, flags: np.ndarray, labels: np.ndarray) -> tuple[int, dict]:
    # Signed histogram and exact integer Walsh-Hadamard transform. Finite
    # sample scores are exact integers; no source probabilities are queried.
    start = time.perf_counter()
    scores = np.zeros(1 << n, dtype=np.int64)
    np.add.at(scores, flags, 1 - 2 * labels.astype(np.int64))
    width = 1
    while width < len(scores):
        v = scores.reshape(-1, 2 * width)
        a = v[:, :width].copy()
        b = v[:, width:].copy()
        v[:, :width] = a + b
        v[:, width:] = a - b
        width *= 2
    secret = int(np.argmax(scores))
    best = int(scores[secret])
    ties = int(np.count_nonzero(scores == best))
    return secret, {
        "acquisition_seconds": time.perf_counter() - start,
        "source_calls": len(flags), "parities_scored": 1 << n,
        "score_storage_bytes": scores.nbytes,
        "temporary_arrays_charged_separately": True,
        "best_integer_score": best, "number_of_maximizers": ties,
    }


def solve_binary(n: int, equations: list[tuple[int, int]]) -> tuple[int | None, int]:
    pivots: dict[int, tuple[int, int]] = {}
    inconsistent = False
    for row, label in equations:
        row, label = int(row), int(label)
        while row:
            pivot = row.bit_length() - 1
            if pivot not in pivots:
                pivots[pivot] = (row, label)
                break
            old_row, old_label = pivots[pivot]
            row ^= old_row
            label ^= old_label
        if row == 0 and label:
            inconsistent = True
    if inconsistent or len(pivots) < n:
        return None, len(pivots)
    secret = 0
    for pivot in sorted(pivots):
        row, label = pivots[pivot]
        bit = label ^ parity(row ^ (1 << pivot), secret)
        secret |= bit << pivot
    return secret, len(pivots)


def repeated_acquire(n: int, flags: np.ndarray, ones: np.ndarray, repeats: int) -> tuple[int | None, dict]:
    start = time.perf_counter()
    # Each record is a held-flag block's one count, not a source probability.
    equations = [(int(y), int(z > repeats // 2)) for y, z in zip(flags, ones)]
    secret, rank = solve_binary(n, equations)
    return secret, {
        "acquisition_seconds": time.perf_counter() - start,
        "source_calls": int(len(flags) * repeats),
        "independent_environment_holds": len(flags),
        "repeats_per_hold": repeats, "coefficient_rank": rank,
        "abort": secret is None,
    }


def run_case(n: int, eta: float, delta: float, seed: int) -> dict:
    rng = np.random.default_rng(seed)
    secret = int(rng.integers(0, 1 << n))
    bias = 1 - 2 * eta
    # Hoeffding uniform over every parity; known eta/delta are supplied metadata.
    count = math.ceil(32 * ((n + 1) * math.log(2) + math.log(1 / delta)) / bias**2)
    start = time.perf_counter()
    flags = rng.integers(0, 1 << n, size=count, dtype=np.int64)
    truth = np.array([parity(int(y), secret) for y in flags], dtype=np.uint8)
    labels = truth ^ (rng.random(count) < eta)
    iid_draw_time = time.perf_counter() - start
    learned_iid, iid = iid_acquire(n, flags, labels)
    iid["simulated_sample_generation_seconds"] = iid_draw_time
    iid["matches_fixture_secret"] = learned_iid == secret
    iid["decoder"] = compile_decoder(learned_iid, n)

    blocks = n + math.ceil(math.log2(2 / delta))
    repeats = math.ceil(2 * math.log(2 * blocks / delta) / bias**2)
    repeats += (repeats + 1) % 2  # next odd integer, for unambiguous majority
    start = time.perf_counter()
    held_flags = rng.integers(0, 1 << n, size=blocks, dtype=np.int64)
    held_truth = np.array([parity(int(y), secret) for y in held_flags], dtype=np.uint8)
    ones = rng.binomial(repeats, np.where(held_truth, 1 - eta, eta))
    repeated_draw_time = time.perf_counter() - start
    learned_repeat, repeated = repeated_acquire(n, held_flags, ones, repeats)
    repeated["simulated_sample_generation_seconds"] = repeated_draw_time
    repeated["matches_fixture_secret"] = learned_repeat == secret
    if learned_repeat is not None:
        repeated["decoder"] = compile_decoder(learned_repeat, n)

    # The fixed-error control deliberately violates fresh noise per repeated
    # call, preserving the same marginal error eta but often corrupting equations.
    frozen_errors = rng.random(blocks) < eta
    frozen_ones = repeats * (held_truth ^ frozen_errors).astype(np.int64)
    learned_frozen, frozen = repeated_acquire(n, held_flags, frozen_ones, repeats)
    frozen["same_per_call_error_marginal"] = eta
    frozen["noise_held_fixed_within_each_block"] = True
    frozen["matches_fixture_secret"] = learned_frozen == secret

    return {"n": n, "eta": eta, "delta": delta, "fixture_seed": seed,
            "iid_noisy_walsh": iid, "repeated_environment": repeated,
            "fixed_error_control": frozen,
            "analytic_payload_entanglement_fidelity_if_secret_correct": 1 - eta,
            "analytic_payload_entanglement_fidelity_if_wrong": 0.5}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    start = time.perf_counter()
    cases = [run_case(n, 0.1, 0.01, 4100 + n) for n in (8, 12, 16, 20)]
    result = {
        "scope": "classical simulated sample acquisition and literal decoder gate-list construction",
        "quantum_source_calls_executed": 0, "quantum_gates_executed": 0,
        "device_or_hardware_runs": 0, "cases": cases,
        "wall_seconds": time.perf_counter() - start,
        "claims_excluded": ["LPN hardness evidence", "practical quantum advantage",
                            "availability of repeat-environment apparatus", "generic robust Clifford learner"],
    }
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"output": str(args.output), "wall_seconds": result["wall_seconds"],
                      "cases": [{"n": x["n"],
                         "iid_calls": x["iid_noisy_walsh"]["source_calls"],
                         "iid_seconds": x["iid_noisy_walsh"]["acquisition_seconds"],
                         "iid_correct": x["iid_noisy_walsh"]["matches_fixture_secret"],
                         "repeat_calls": x["repeated_environment"]["source_calls"],
                         "repeat_correct": x["repeated_environment"]["matches_fixture_secret"],
                         "fixed_error_abort": x["fixed_error_control"]["abort"]}
                         for x in cases]}, indent=2))


if __name__ == "__main__":
    main()
