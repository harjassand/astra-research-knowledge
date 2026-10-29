"""Compile an exact dyadic register/copy contract and actual graph catalogue.

This program does not execute a stochastic path or acquire physical controls.
The only transcendental relaxations used are ln2>=1/2 and exp(-x)<=2^-floor(x).
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import resource
import struct
import sys
import time
from fractions import Fraction as F

from controller import FAIR_BITS_PER_ATTEMPT, WALK_LENGTH, neighbor


def fraction(x: F) -> dict:
    return {"numerator": str(x.numerator), "denominator": str(x.denominator),
            "decimal_diagnostic": format(float(x), ".17g")}


def pow2(exponent: int) -> F:
    return F(1 << exponent) if exponent >= 0 else F(1, 1 << (-exponent))


def compile_packet(side: int, q: int, horizon_bits: int, latency: int,
                   out: Path) -> dict:
    if side < 2 or q < 1 or horizon_bits < 0 or latency < 1:
        raise ValueError("bad contract parameters")
    n = side * side
    h = (n + 63) // 64
    lower = (9 * n + 1023) // 1024
    initial = n // 256
    if h <= q:
        raise ValueError("the required first-exit level must exceed q")
    if latency > (1 << horizon_bits):
        raise ValueError("copy readout latency must be within the horizon")
    coefficient = 3 * (F(1, 64) + F(25, 32) ** WALK_LENGTH)
    if not coefficient < F(1, 8):
        raise AssertionError("the literal spectral inequality failed")
    lam = F(1, 1024 * ((1 << q) - 1))
    horizon = 1 << horizon_bits
    prefactor = F(n) * (1 + lam) * horizon
    reg_general = min(F(1), (1 << q) * prefactor * pow2(-(n // 256)))
    copy_excursion = F(n) * (F(17, 16) + lam) * horizon * pow2(lower + q - h)
    copy_forgetting = n * pow2(-(15 * latency // 16))
    copy_total = min(F(1), reg_general + copy_excursion + copy_forgetting)

    out.mkdir(parents=True, exist_ok=True)
    graph_file = out / "GRAPH_CATALOGUE.u32le"
    inverse = (1, 0, 3, 2, 5, 4, 7, 6)
    graph_start = time.perf_counter()
    column_counts = [[0] * n for _ in range(8)]
    sha = hashlib.sha256()
    loops = 0
    checks = 0
    with graph_file.open("wb") as stream:
        for vertex in range(n):
            row = []
            for ticket in range(8):
                target = neighbor(side, vertex, ticket)
                column_counts[ticket][target] += 1
                if neighbor(side, target, inverse[ticket]) != vertex:
                    raise AssertionError("a literal affine inverse failed")
                loops += int(target == vertex)
                checks += 1
                row.append(target)
            data = struct.pack("<8I", *row)
            stream.write(data)
            sha.update(data)
    if any(x != 1 for column in column_counts for x in column):
        raise AssertionError("a named graph direction was not a permutation")
    graph_seconds = time.perf_counter() - graph_start
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if sys.platform != "darwin":
        rss *= 1024
    return {
        "status": "EXACT_CONTRACT_COMPILED_NO_TRAJECTORIES",
        "scope": "classical graph-local retained bit and frozen-source buffered copy",
        "not_claimed": ["native recursive quantum decoder", "Euclidean finite-range wiring",
                        "noisy terminal majority implementation", "hardware performance",
                        "a new generic majority/expander theorem"],
        "inputs": {"side": side, "sites_per_register": n, "q": q,
                   "lambda_upper": fraction(lam), "initial_wrong_upper": initial,
                   "horizon": str(horizon), "horizon_bits": horizon_bits,
                   "copy_readout_latency": latency,
                   "fixed_clock_rate_interval": ["15/16", "17/16"],
                   "fixed_atomic_graph_range_source": WALK_LENGTH,
                   "fixed_atomic_graph_range_copy": WALK_LENGTH + 1},
        "exact_universal_inequality": {"3_times_rho_plus_sigma_squared": fraction(coefficient),
                                      "upper": "1/8", "strict": True},
        "levels": {"source_first_exit": h, "copy_excursion_lower": lower},
        "bounds": {"retained_bit_failure": fraction(reg_general),
                   "copy_source_failure": fraction(reg_general),
                   "copy_excursion_failure": fraction(copy_excursion),
                   "copy_initial_forgetting_failure": fraction(copy_forgetting),
                   "total_buffered_copy_failure": fraction(copy_total)},
        "actual_graph_acquisition": {"path": graph_file.name, "sha256": sha.hexdigest(),
                                     "vertices": n, "incidences": checks,
                                     "loop_incidences": loops, "bytes": graph_file.stat().st_size,
                                     "inverse_checks": checks, "eight_permutations_checked": True,
                                     "seconds": graph_seconds,
                                     "spectral_premise": "named all-moduli standard theorem; no numeric eigenfit"},
        "nominal_resource_contract": {"persistent_bits_retained": n,
                                      "persistent_bits_source_plus_copy": 2 * n,
                                      "noiseless_persistent_bits": 0,
                                      "internal_global_clock": False,
                                      "fair_bits_per_attempt": FAIR_BITS_PER_ATTEMPT,
                                      "endpoint_reads_per_attempt": 3,
                                      "source_attempt_rate_nominal": n,
                                      "source_plus_copy_attempt_rate_nominal": 2 * n,
                                      "source_plus_copy_attempt_rate_upper": fraction(F(17, 16) * 2 * n),
                                      "expected_source_plus_copy_attempts_over_horizon_upper": str(F(17, 16) * 2 * n * horizon),
                                      "expected_nominal_fair_bits_over_horizon_upper": str(F(17, 16) * FAIR_BITS_PER_ATTEMPT * 2 * n * horizon),
                                      "terminal_decoder": "ideal mathematical global majority; noisy acquisition not granted",
                                      "physical_routing": "atomic expander channels range16 restoration/range17 copy admitted; no serial-message implementation acquired",
                                      "input_preparation": "sparse initial source error contract; noisy physical loading not acquired"},
        "cost": {"peak_rss_bytes": rss, "trajectories": 0, "state_samples": 0,
                 "physical_experiments": 0, "exact_integer_graph_checks": checks}}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--side", type=int, default=256)
    parser.add_argument("--q", type=int, default=1)
    parser.add_argument("--horizon-bits", type=int, default=128)
    parser.add_argument("--latency", type=int, default=256)
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    start = time.perf_counter()
    packet = compile_packet(args.side, args.q, args.horizon_bits, args.latency, args.output)
    packet["cost"]["total_seconds_after_imports_before_serialization"] = time.perf_counter() - start
    (args.output / "REGISTER_CONTRACT.json").write_text(json.dumps(packet, indent=2) + "\n")
    print(json.dumps({"status": packet["status"], "n": args.side ** 2,
                      "failure_upper_diagnostic": packet["bounds"]["total_buffered_copy_failure"]["decimal_diagnostic"],
                      "seconds": packet["cost"]["total_seconds_after_imports_before_serialization"]}))


if __name__ == "__main__":
    main()
