#!/usr/bin/env python3
"""Exact independent compressed joint posterior and sampler-bridge verifier.

No peer code imported or executed. Target exp bounds and symmetric output
checking are from our already owned independent checker, not author routines.
"""
from copy import deepcopy
from datetime import datetime, timezone
from fractions import Fraction as Q
from hashlib import sha256
from pathlib import Path
import argparse
import json
import math
import sys
import time

OWN = Path(__file__).resolve().parent
ROOT = OWN.parents[4]
sys.path.insert(0, str(OWN.parent / "algorithm_review"))
import independent_posterior_verifier as independent


def need(ok, reason):
    if not ok:
        raise ValueError(reason)


def choose(n, k):
    return math.comb(n, k) if 0 <= k <= n else 0


def sector_table(N):
    table = []
    for b in range(N // 2 + 1):
        r = N - 2 * b + 1
        row = [Q(r * (choose(N - k, b) - choose(N - k, b - k - 1)),
                 (k + 1) * 2 ** (N - k)) for k in range(N + 1)]
        need(min(row) >= 0, "sector column has negative mass")
        table.append(row)
    need(all(sum(row[k] for row in table) == 1 for k in range(N + 1)),
         "sector columns not physical probability vectors")
    multiplicities = [choose(N, b) - choose(N, b - 1) for b in range(N // 2 + 1)]
    need(sum((N - 2 * b + 1) * d for b, d in enumerate(multiplicities)) == 2 ** N,
         "physical multiplicities do not sum to Hilbert dimension")
    return table, multiplicities


def verify(model):
    format_name = model["format"]
    need(format_name in ("FILTERED_SECTOR_GIBBS_CERTIFIED_V1",
                         "FILTERED_SECTOR_GIBBS_CERTIFIED_SCALING_V1"),
         "unsupported filtered output format")
    rounded_bridge = format_name == "FILTERED_SECTOR_GIBBS_CERTIFIED_SCALING_V1"
    N = model["N"]
    need(type(N) is int and 2 <= N <= (64 if rounded_bridge else 16),
         "outside independent finite-output scope")
    alpha, delta, h, epsilon = map(independent.rational,
                                  (model["alpha"], model["delta"], model["h"], model["epsilon"]))
    need(alpha >= 0 and 0 <= delta <= 1 and 0 < epsilon < 1, "invalid promised parameters")
    weights = list(map(independent.rational, model["isotropic_weights"]))
    fhat = list(map(independent.rational, model["filter_values"]))
    need(len(weights) == len(fhat) == N + 1 and min(weights) >= 0 and sum(weights) == 1
         and min(fhat) > 0, "invalid positive K mixture/filter data")
    A, multiplicities = sector_table(N)
    sector = [sum(x * w for x, w in zip(row, weights)) for row in A]
    logs = [-delta * Q((2 * t - N) ** 2, 4 * N) + h * Q(2 * t - N, 2)
            for t in range(N + 1)]
    peak = max(logs)
    f = [independent.independent_exp_minus(peak - x) for x in logs]
    e = [independent.independent_exp_minus(alpha * Q(b * (N + 1 - b), N))
         for b in range(N // 2 + 1)]
    target, candidate = [], []
    for b, multiplicity in enumerate(multiplicities):
        r = N - 2 * b + 1
        for t in range(b, N - b + 1):
            target.append((multiplicity * e[b][0] * f[t][0],
                           multiplicity * e[b][1] * f[t][1]))
            candidate.append(sector[b] * fhat[t] / r)
    need(len(candidate) == model["joint_certificate_entries"], "wrong physical joint entry count")
    target_normalizer = sum(a for a, _ in target), sum(b for _, b in target)
    candidate_normalizer = sum(candidate)
    need(target_normalizer[0] > 0 and candidate_normalizer > 0, "invalid joint normalization")
    target = [independent.interval_divide(v, target_normalizer) for v in target]
    joint = sum(max(abs(q / candidate_normalizer - a), abs(q / candidate_normalizer - b))
                for q, (a, b) in zip(candidate, target)) / 2
    need(joint <= independent.rational(model["target_vs_ideal_joint_TV_upper"]),
         "independently acquired joint posterior exceeds certificate")

    raw = {}
    for k in range(N + 1):
        for u in range(N - k + 1):
            raw[k, u] = weights[k] * Q(choose(N - k, u), (k + 1) * 2 ** (N - k)) * sum(fhat[u:u + k + 1])
    raw_normalizer = sum(raw.values())
    need(raw_normalizer == candidate_normalizer, "K-filter branch disintegration does not match joint state")
    p = {key: mass / raw_normalizer for key, mass in raw.items()}
    delivered = {(b["k"], b["u"]): independent.rational(b["probability"]) for b in model["branches"]}
    need(len(delivered) == len(model["branches"]) and min(delivered.values()) >= 0
         and sum(delivered.values()) == 1, "invalid or duplicated delivered branch law")
    need(all(key in raw for key in delivered), "invalid physical branch type")
    need(all(x.denominator & (x.denominator - 1) == 0 for x in delivered.values()),
         "delivered branch weights not finite-bit dyadics")
    outer = sum(abs(p[key] - delivered.get(key, Q(0))) for key in raw) / 2
    inner = preparation = Q(0)
    rank_bits = model["uniform_rank_bits"]
    need(type(rank_bits) is int and rank_bits == 128, "filtered sampler uses exactly128 rank bits")
    max_inner = 0
    for branch in model["branches"]:
        k, u, block = branch["k"], branch["u"], branch["Dicke_model"]
        need(type(k) is int and type(u) is int and block["n"] == k,
             "conditional physical type mismatch")
        need(independent.rational(block["delta"]) == delta * Q(k, N)
             and independent.rational(block["h"]) == h - delta * Q(2 * u - (N - k), N),
             "wrong Gaussian block parameters")
        population, receipt = independent.verify_symmetric(block)
        Zblock = sum(fhat[u:u + k + 1])
        # Load-bearing bridge: actual output versus EXACT fhat conditional,
        # rather than reusing its true-exponential block certificate.
        block_error = sum(abs(q - fhat[u + ell] / Zblock)
                          for ell, q in enumerate(population)) / 2
        mass = delivered[k, u]
        weighted_error = mass * block_error
        # Scaling version raises EACH exact weighted bridge term to the
        # next160-bit dyadic, then sums; this is an upper bound even when
        # the exact terms have mutually large denominators. Never lower-round.
        inner += independent.dyadic_ceil(weighted_error, 160) if rounded_bridge else weighted_error
        _, phase = independent.phase_parameters(k, block["node_weight_bits"])
        density = Q(8 * k, 2 ** block["density_bits"])
        preparation += mass * (Q(choose(N, k) + choose(N - k, u), 2 ** (rank_bits + 1))
                               + phase + density)
        max_inner = max(max_inner, receipt["fair_bits"])
    for actual, name in [(outer, "outer_rounding_TV"), (inner, "block_population_TV"),
                         (preparation, "finite_preparation_TV_upper")]:
        need(actual == independent.rational(model[name]), "exact bridge budget mismatch: " + name)
    stored_joint = independent.rational(model["target_vs_ideal_joint_TV_upper"])
    total = stored_joint + outer + inner + preparation
    need(total == independent.rational(model["total_target_trace_distance_upper"]) <= epsilon,
         "whole final composed trace guarantee fails")
    outer_bits = max(x.denominator.bit_length() - 1 for x in delivered.values())
    need(model["outer_sampling_bits"] == outer_bits and model["max_inner_sampling_bits"] == max_inner
         and model["predetermined_random_bits_per_sample"] == outer_bits + 2 * rank_bits + max_inner,
         "whole fixed fair-bit budget inconsistent")
    need(model["branch_count"] == len(delivered) and model["dense_matrix_formed"] is False,
         "implementation evidence schema inconsistent")
    return {"N": N, "physical_joint_entries": len(candidate), "verified_blocks": len(delivered),
            "independent_joint_TV_upper": independent.encode(independent.dyadic_ceil(joint, 192)),
            "composed_trace_bound": model["total_target_trace_distance_upper"],
            "block_bridge_TV_positive": inner > 0,
            "block_bridge_method": "160-bit upward rounding of each exact weighted term" if rounded_bridge else "exact rational sum",
            "branch_and_joint_normalizers_equal_exact": True,
            "predetermined_fair_bits": outer_bits + 2 * rank_bits + max_inner}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--certificate", type=Path, action="append")
    ap.add_argument("--output", type=Path, default=OWN / "FILTERED_N8_N16_VERIFY.json")
    args = ap.parse_args()
    paths = args.certificate or [ROOT / ("work/cycle6/c03_s01/implementation/filtered_N" + str(n) + ".json")
                                 for n in (8, 16)]
    start = time.perf_counter()
    cases, inputs, controls = [], [], []
    for path in paths:
        raw = path.read_bytes()
        packet = json.loads(raw)
        model = packet["model"]
        receipt = verify(model)
        receipt["source_sha256"] = sha256(raw).hexdigest()
        for sample in packet.get("samples", []):
            need(sample["random_bits_consumed"] == receipt["predetermined_fair_bits"],
                 "sample bit-count metadata inconsistent")
            for density in sample["local_density_matrices"]:
                independent.verify_local_density(density)
        cases.append(receipt)
        inputs.append({"path": str(path.resolve()), "sha256": sha256(raw).hexdigest(), "bytes": len(raw)})
        # A zeroed nonzero bridge is rejected, demonstrating the critical term
        # is actually reacquired, not inferred from the child exp certificate.
        if model["N"] == 8:
            bad = deepcopy(model)
            bad["block_population_TV"] = independent.encode(Q(0))
            try:
                verify(bad)
            except ValueError as error:
                controls.append({"zeroed_phat_to_actual_block_bridge": "REJECTED", "reason": str(error)})
            else:
                raise ValueError("omitted block bridge accepted")
    result = {"status": "PASS independent exact joint posterior AND actual hierarchy bridge",
              "utc": datetime.now(timezone.utc).isoformat(), "inputs": inputs, "cases": cases,
              "controls": controls, "code_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
              "method": "different exp engine; exact acquired rational A_bk and physical d_b; no peer imports/execution or LP rerun; every rounded block compared directly to fhat conditional",
              "wall_seconds": time.perf_counter() - start,
              "limits": "finite delivered outputs, not a polynomial simplex runtime or uniform-success theorem; hardware preparation unclaimed"}
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": result["status"], "N": [x["N"] for x in cases],
                      "blocks": sum(x["verified_blocks"] for x in cases),
                      "wall_seconds": result["wall_seconds"]}, indent=2))


if __name__ == "__main__":
    main()
