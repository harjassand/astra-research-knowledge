#!/usr/bin/env python3
"""Independent, read-only replay checks for the acquired-kinetics packet.

The source snapshot remains untouched. All NPZ inputs are opened with
allow_pickle=False. This checker recomputes the tensor enclosures with an
exactly checked high-precision local alpha witness and builds one full-state
comparator certificate using integer-scaled exact arithmetic.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import resource
import sys
import time
from fractions import Fraction as F
from pathlib import Path

import mpmath as mp
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
REPLICA = ROOT / "replica"
sys.path.insert(0, str(REPLICA))

import certify as certmod
import full_reference as fullmod
from model import Compiler, discover_partition, from_transcript


def load_case(name: str):
    tr = json.loads((REPLICA / f"{name}_transcript.json").read_text())
    model = from_transcript(18, tr)
    groups, partition = discover_partition(model)
    c = Compiler(model, groups)
    with np.load(REPLICA / f"{name}.npz", allow_pickle=False) as archive:
        arrays = [np.array(archive[str(i)], copy=True) for i in range(c.B)]
    old = json.loads((REPLICA / f"{name}.json").read_text())
    return tr, c, arrays, old, partition


def load_model_case(name: str):
    tr = json.loads((REPLICA / f"{name}_transcript.json").read_text())
    model = from_transcript(18, tr)
    groups, partition = discover_partition(model)
    return tr, Compiler(model, groups), partition


def exact_alpha_witness(c: Compiler, bits: int = 112, dps: int = 100):
    """Solve K u=1 numerically, then certify the dyadic u and alpha exactly."""
    block = next(b for b, group in enumerate(c.groups) if c.model["target"] in group)
    K = c.refraw[block]
    mp.mp.dps = dps
    M = mp.matrix(
        [
            [mp.mpf(K[i, j].numerator) / K[i, j].denominator for j in range(len(K))]
            for i in range(len(K))
        ]
    )
    proposal = mp.lu_solve(M, mp.matrix([1] * len(K)))
    den = 1 << bits
    u_int = [int(mp.nint(proposal[i] * den)) for i in range(len(K))]
    u = [F(value, den) for value in u_int]
    if min(u) <= 0:
        raise ArithmeticError("local alpha witness has a nonpositive entry")
    delta = max(
        abs(sum(F(K[i, j]) * u[j] for j in range(len(K))) - 1)
        for i in range(len(K))
    )
    if delta >= 1:
        raise ArithmeticError("local alpha witness residual is not below one")
    alpha = (1 - delta) / max(u)
    if any(F(K[i, j]) > 0 for i in range(len(K)) for j in range(len(K)) if i != j):
        raise ArithmeticError("local killed generator is not a Z-matrix")
    return alpha, {
        "target_block": block,
        "local_states": len(K),
        "dyadic_bits": bits,
        "u_numerators": [str(value) for value in u_int],
        "u_denominator": str(den),
        "u_min": str(min(u)),
        "u_max": str(max(u)),
        "residual_infinity": str(delta),
        "alpha_lower": str(alpha),
        "alpha_lower_float": float(alpha),
        "exact_checks": {
            "all_u_positive": True,
            "exact_Ku_minus_one_infinity_lt_one": True,
            "all_offdiagonals_nonpositive": True,
        },
        "validity_argument": (
            "For the irreducible killed-generator M-matrix K, exact Ku >= "
            "(1-delta)1 and u>0 imply K^{-1}1 <= u/(1-delta). Thus the "
            "row-sum norm of K^{-1} is at most max(u)/(1-delta), so "
            "lambda_min(K) >= (1-delta)/max(u)."
        ),
    }


def tensor_replay(name: str, alpha_cache: dict[str, tuple[F, dict]]):
    t0 = time.perf_counter()
    tr, c, V, old, partition = load_case(name)
    old_alpha = F(old["alpha_lower"])

    naive, naive_data = certmod.certify(c, V, return_data=True)
    na_rr = certmod.dot_sums(c, naive_data["residual"], naive_data["residual"], same=True)

    key = "A" if name == "reverse_A" else "B"
    if key not in alpha_cache:
        alpha_cache[key] = exact_alpha_witness(c)
    alpha, witness = alpha_cache[key]
    original_alpha_bound = certmod.alpha_bound
    try:
        certmod.alpha_bound = lambda _c, bits=46: (alpha, {
            "reference_residual": witness["residual_infinity"],
            "reference_max_trial": witness["u_max"],
            "reference_local_states": witness["local_states"],
            "witness_bits": witness["dyadic_bits"],
        })
        fresh, data = certmod.certify(c, V, return_data=True)
    finally:
        certmod.alpha_bound = original_alpha_bound

    rr = certmod.dot_sums(c, data["residual"], data["residual"], same=True)
    old_lower = data["L"] / c.Z
    old_upper = (data["L"] + rr / old_alpha) / c.Z
    old_lower_matches = old_lower == F(old["lower"])
    old_upper_matches = old_upper == F(old["upper"])
    if not old_lower_matches or not old_upper_matches:
        raise AssertionError(f"stored endpoints do not follow from the stored alpha: {name}")
    old_alpha_rec = old_alpha <= alpha
    if not old_alpha_rec:
        raise AssertionError(f"new exact alpha witness does not validate stored alpha: {name}")

    stat = (REPLICA / f"{name}.npz").stat()
    return {
        "name": name,
        "source_transcript_queries": {
            "energy": tr["energy_queries"],
            "reverse_relaxation": tr["reverse_clock_queries"],
        },
        "partition": partition["selected"],
        "witness": {
            "arrays": [list(a.shape) for a in V],
            "coefficients": sum(a.size for a in V),
            "npz_bytes": stat.st_size,
            "npz_sha256": hashlib.sha256((REPLICA / f"{name}.npz").read_bytes()).hexdigest(),
        },
        "source_reported_interval": {
            "lower": old["lower"], "upper": old["upper"], "ratio": old["ratio_float"],
            "alpha_lower": old["alpha_lower"],
        },
        "fresh_platform_alpha_replay": {
            "lower": naive["lower"], "upper": naive["upper"], "ratio": naive["ratio_float"],
            "alpha_lower": naive["alpha_lower"],
            "lower_exact_matches_source": F(naive["lower"]) == F(old["lower"]),
            "upper_exact_matches_source": F(naive["upper"]) == F(old["upper"]),
            "source_minus_replay_lower_exact": str(F(old["lower"]) - F(naive["lower"])),
            "source_minus_replay_upper_exact": str(F(old["upper"]) - F(naive["upper"])),
            "source_minus_replay_lower_float": float(F(old["lower"]) - F(naive["lower"])),
            "source_minus_replay_upper_float": float(F(old["upper"]) - F(naive["upper"])),
            "source_minus_replay_ratio": old["ratio_float"] - naive["ratio_float"],
            "certificate_seconds": naive["seconds"],
            "recomputed_residual_squared": str(na_rr),
        },
        "exact_high_precision_alpha_recertification": {
            "lower": fresh["lower"], "upper": fresh["upper"], "ratio": fresh["ratio_float"],
            "ratio_exact": str(data["U"] / data["L"]),
            "alpha_lower": str(alpha),
            "old_alpha_le_new_exact_alpha": old_alpha_rec,
            "stored_lower_rebuilt_exactly": old_lower_matches,
            "stored_upper_rebuilt_exactly_from_old_alpha": old_upper_matches,
            "fresh_certificate_seconds": fresh["seconds"],
            "alpha_witness": witness,
        },
        "wall_seconds": time.perf_counter() - t0,
    }


def exact_full_certificate(c: Compiler, v_int: np.ndarray, bits: int, alpha: F):
    """Evaluate the complete 2^n residual and source contractions as integers."""
    if F(c.model["kappa"]) != 1:
        raise ValueError("this checker is scoped to the canonical kappa=1 case")
    n = c.model["n"]
    dims = [len(p) for p in c.prob]
    N = math.prod(dims)
    if len(v_int) != N:
        raise ValueError("full-state witness length mismatch")

    strides = [math.prod(dims[b + 1 :]) for b in range(len(dims))]
    block_masks = []
    for b, group in enumerate(c.groups):
        block_masks.append([
            sum(int(c.bits[b][a, s]) << node for s, node in enumerate(group))
            for a in range(dims[b])
        ])
    flip_stride = [strides[c.loc[i][0]] * (1 << c.loc[i][1]) for i in range(n)]

    block_denoms = [sum(mass) for mass in c.mass]
    rho_denom = math.prod(block_denoms)

    cross_count = len(c.cross)
    cross_weights = []
    for code in range(1 << cross_count):
        value = F(1)
        for e, (_b, s, _d, t, g) in enumerate(c.cross):
            equal = (code >> e) & 1
            value *= (g if equal else F(1)) / min(F(1), g)
        cross_weights.append(value)
    w_denom = math.lcm(*(x.denominator for x in cross_weights)) if cross_weights else 1
    w_num_table = [int(w * w_denom) for w in cross_weights]

    energy_neighbors = {
        i: sorted(j if i == a else a for a, j in c.model["edges"] if i == a or i == j)
        for i in range(n)
    }
    clock_contexts = c.model.get("clock_contexts", {})
    contexts = {i: sorted(set(energy_neighbors[i]) | set(clock_contexts.get(i, []))) for i in range(n)}
    rate_fractions = {}
    for i in range(n):
        for xi in (0, 1):
            for code in range(1 << len(contexts[i])):
                bits_by_node = {node: (code >> p) & 1 for p, node in enumerate(contexts[i])}
                cc = clock_contexts.get(i, [])
                if "clock_tables" in c.model:
                    clock_code = sum(bits_by_node[node] << p for p, node in enumerate(cc))
                    prefactor = F(c.model["clock_tables"][i][clock_code])
                else:
                    prefactor = F(c.model["nu"][i])
                ratio = F(c.model["fields"][i]) ** (1 - 2 * xi)
                for j in energy_neighbors[i]:
                    same = xi == bits_by_node[j]
                    t = F(c.model["edges"][tuple(sorted((i, j)))])
                    ratio *= 1 / t if same else t
                rate_fractions[i, xi, code] = prefactor * ratio / (1 + ratio)
    q_denom = math.lcm(*(q.denominator for q in rate_fractions.values()))
    rate_nums = {
        key: int(value * q_denom) for key, value in rate_fractions.items()
    }

    v_denom = 1 << bits
    b_num = energy_num = residual_num = z_num = 0
    for state in range(N):
        local = [(state // stride) % dim for stride, dim in zip(strides, dims)]
        xmask = 0
        rho_num = 1
        for b, a in enumerate(local):
            xmask |= block_masks[b][a]
            rho_num *= c.mass[b][a]

        cross_code = 0
        for e, (b, s, d, t, _g) in enumerate(c.cross):
            xb = (xmask >> c.groups[b][s]) & 1
            xd = (xmask >> c.groups[d][t]) & 1
            if xb == xd:
                cross_code |= 1 << e
        w_num = w_num_table[cross_code]

        Vx = int(v_int[state])
        raw_num = 0
        for i in range(n):
            context_code = sum(((xmask >> node) & 1) << p for p, node in enumerate(contexts[i]))
            xi = (xmask >> i) & 1
            q_num = rate_nums[i, xi, context_code]
            raw_num += q_num * (Vx - int(v_int[state ^ flip_stride[i]]))
        raw_num += ((xmask >> c.model["target"]) & 1) * Vx * q_denom

        b_num += rho_num * w_num * Vx
        energy_num += rho_num * w_num * Vx * raw_num
        residual_gap_num = q_denom * v_denom - raw_num
        residual_num += rho_num * w_num * w_num * residual_gap_num * residual_gap_num
        z_num += rho_num * w_num

    b = F(b_num, rho_denom * w_denom * v_denom)
    energy = F(energy_num, rho_denom * w_denom * q_denom * v_denom * v_denom)
    residual_sq = F(
        residual_num,
        rho_denom * w_denom * w_denom * q_denom * q_denom * v_denom * v_denom,
    )
    Z = F(z_num, rho_denom * w_denom)
    if Z != c.Z:
        raise AssertionError("exact full-state normalization disagrees with source compiler")
    lower_unnormalized = 2 * b - energy
    upper_unnormalized = lower_unnormalized + residual_sq / alpha
    return {
        "states": N,
        "full_state_dyadic_bits": bits,
        "q_common_denominator_bits": q_denom.bit_length(),
        "weight_common_denominator": str(w_denom),
        "rho0_common_denominator_bits": rho_denom.bit_length(),
        "normalizer": str(Z),
        "L_unnormalized": str(lower_unnormalized),
        "residual_squared_exact": str(residual_sq),
        "alpha_lower": str(alpha),
        "lower": str(lower_unnormalized / Z),
        "upper": str(upper_unnormalized / Z),
        "ratio": float(upper_unnormalized / lower_unnormalized),
        "ratio_exact": str(upper_unnormalized / lower_unnormalized),
        "exact_identity": True,
        "scope": "full 2^18-state rational residual and source contraction from acquired transcript",
    }


def full_state_comparator(alpha_cache):
    t0 = time.perf_counter()
    phase = {}
    phase_start = time.perf_counter()
    tr, c, partition = load_model_case("reverse_matched_full")
    tr_b = json.loads((REPLICA / "reverse_B_transcript.json").read_text())
    same_transcript = (
        tr["weights"] == tr_b["weights"]
        and tr["reverse_rates"] == tr_b["reverse_rates"]
    )
    if not same_transcript:
        raise AssertionError("matched full-state model did not receive the B transcript")
    alpha, alpha_witness = alpha_cache["B"]
    phase["transcript_model_reconstruction_seconds"] = time.perf_counter() - phase_start

    # build_full imports certify.alpha_bound locally, so patch that source
    # function (the same exactly checked witness used for the tensor path).
    original_alpha = certmod.alpha_bound
    try:
        certmod.alpha_bound = lambda _c, bits=46: (alpha, {
            "reference_residual": alpha_witness["residual_infinity"],
            "reference_max_trial": alpha_witness["u_max"],
            "reference_local_states": alpha_witness["local_states"],
        })
        phase_start = time.perf_counter()
        data = fullmod.build_full(c)
        phase["full_state_setup_seconds"] = time.perf_counter() - phase_start
    finally:
        certmod.alpha_bound = original_alpha

    b = data["rp"] * data["w"]
    x = np.zeros_like(b)
    r = b.copy()
    z = fullmod.apply_Cinv(c, data, r)
    p = z.copy()
    rz = r @ z
    history = []
    pcg_start = time.perf_counter()
    directed_cert_seconds = 0.0
    for it in range(1, 13):
        ap = fullmod.apply_A(data, p)
        step = rz / (p @ ap)
        x += step * p
        r = b - fullmod.apply_A(data, x)
        if it % 2 == 0:
            proposal = x / data["rp"]
            cert_start = time.perf_counter()
            rounded = fullmod.certify_full(data, proposal, bits=18)
            directed_cert_seconds += time.perf_counter() - cert_start
            history.append({"iteration": it, "source_interval_ratio": rounded.get("ratio_float")})
            if rounded.get("valid") and rounded["ratio_float"] <= 1.05:
                break
        z = fullmod.apply_Cinv(c, data, r)
        new_rz = r @ z
        p = z + (new_rz / rz) * p
        rz = new_rz

    u = x / data["rp"]
    dyadic_bits = 18
    v_int = np.rint(u * (1 << dyadic_bits)).astype(np.int64)
    if int(v_int.min()) <= 0:
        raise ArithmeticError("rounded full-state response is not positive")
    cert_start = time.perf_counter()
    source_float_certificate = fullmod.certify_full(data, v_int.astype(float) / (1 << dyadic_bits), bits=dyadic_bits)
    directed_cert_seconds += time.perf_counter() - cert_start
    phase["pcg_seconds_including_directed_checks"] = time.perf_counter() - pcg_start
    phase["directed_float_certificate_seconds"] = directed_cert_seconds
    phase_start = time.perf_counter()
    exact = exact_full_certificate(c, v_int, dyadic_bits, alpha)
    phase["exact_rational_full_certificate_seconds"] = time.perf_counter() - phase_start
    if exact["ratio"] > 1.05:
        raise AssertionError("fresh exact full-state comparator missed the shared 5% interval target")

    old_source = json.loads((REPLICA / "reverse_matched_full.json").read_text())
    stat = (REPLICA / "reverse_matched_full_transcript.json").stat()
    return {
        "method": "full-state PCG using acquired local preconditioner, independently rationally recertified",
        "matched_transcript_equals_reverse_B": same_transcript,
        "partition": partition["selected"],
        "queries": {"energy": tr["energy_queries"], "reverse_relaxation": tr["reverse_clock_queries"]},
        "iterations": it,
        "iteration_history": history,
        "source_reported_full_certificate": old_source,
        "fresh_directed_float_full_certificate": source_float_certificate,
        "fresh_exact_rational_full_certificate": exact,
        "states": data["N"],
        "full_response_vector_bytes": v_int.nbytes,
        "npz_witness_bytes": 0,
        "transcript_bytes": stat.st_size,
        "phase_seconds": phase,
        "process_peak_rss_bytes": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        "wall_seconds": time.perf_counter() - t0,
    }


def main():
    alpha_cache = {}
    tensors = [tensor_replay(name, alpha_cache) for name in [
        "reverse_A", "reverse_B", "reverse_matched_tensor"
    ]]
    full = full_state_comparator(alpha_cache)
    outputs = {
        "runtime": {
            "python": sys.version.split()[0],
            "numpy": np.__version__,
            "scipy": __import__("scipy").__version__,
            "sympy": __import__("sympy").__version__,
            "mpmath": mp.__version__,
            "thread_environment": {
                "OPENBLAS_NUM_THREADS": os.environ.get("OPENBLAS_NUM_THREADS"),
                "OMP_NUM_THREADS": os.environ.get("OMP_NUM_THREADS"),
            },
        },
        "tensor_replays": tensors,
        "matched_full_state_comparator": full,
        "process_peak_rss_bytes": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        "scope": "fresh exact residual certificates from acquired transcripts; no private fixture truth",
    }
    out = HERE / "fresh_replay_results.json"
    out.write_text(json.dumps(outputs, indent=2) + "\n")
    failed_audit = json.loads((HERE / "audit_reverse_failure.json").read_text())
    endpoint_differences = {
        "original_unmodified_audit": {
            "file": "audit_reverse_failure.json",
            "returncode": failed_audit["returncode"],
            "failure_site": "audit.py exact lower/upper endpoint equality assertion",
            "audit_reverse_py_sha256": hashlib.sha256((REPLICA / "audit_reverse.py").read_bytes()).hexdigest(),
            "source_snapshot_audit_reverse_py_sha256": hashlib.sha256((ROOT / "source_snapshot" / "audit_reverse.py").read_bytes()).hexdigest(),
        },
        "per_tensor_witness": [
            {
                "name": item["name"],
                "lower_exactly_equal": item["fresh_platform_alpha_replay"]["lower_exact_matches_source"],
                "upper_exactly_equal": item["fresh_platform_alpha_replay"]["upper_exact_matches_source"],
                "source_minus_replay_lower_exact": item["fresh_platform_alpha_replay"]["source_minus_replay_lower_exact"],
                "source_minus_replay_upper_exact": item["fresh_platform_alpha_replay"]["source_minus_replay_upper_exact"],
                "source_minus_replay_lower_float": item["fresh_platform_alpha_replay"]["source_minus_replay_lower_float"],
                "source_minus_replay_upper_float": item["fresh_platform_alpha_replay"]["source_minus_replay_upper_float"],
                "source_ratio_minus_replay_ratio": item["fresh_platform_alpha_replay"]["source_minus_replay_ratio"],
                "new_exact_alpha_recertification_rebuilds_stored_upper": item["exact_high_precision_alpha_recertification"]["stored_upper_rebuilt_exactly_from_old_alpha"],
            }
            for item in tensors
        ],
        "interpretation": (
            "The source audit remains a FAIL. Fresh platform alpha regeneration changes the exact upper endpoints. "
            "A separate exact local supersolution witness proves each stored scalar alpha is conservative and "
            "rebuilds the saved upper endpoint from the saved tensor response; this does not retroactively pass the original audit."
        ),
    }
    (HERE / "audit_reverse_endpoint_differences.json").write_text(json.dumps(endpoint_differences, indent=2) + "\n")
    print(json.dumps({
        "output": str(out),
        "tensor": [
            {"name": x["name"], "ratio": x["exact_high_precision_alpha_recertification"]["ratio"],
             "stored_upper_rebuilt": x["exact_high_precision_alpha_recertification"]["stored_upper_rebuilt_exactly_from_old_alpha"]}
            for x in tensors
        ],
        "full": {"iterations": full["iterations"], "ratio": full["fresh_exact_rational_full_certificate"]["ratio"],
                 "seconds": full["wall_seconds"]},
        "peak_rss_bytes": outputs["process_peak_rss_bytes"],
    }, indent=2))


if __name__ == "__main__":
    main()
