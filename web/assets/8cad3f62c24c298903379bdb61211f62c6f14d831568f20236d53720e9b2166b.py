#!/usr/bin/env python3
"""Costed arithmetic composition of frozen N64 output with collective decay.

No compiler, solver, simulation, peer code import or new quantum assumption.
Acquires target positive sums using our already owned different exp engine.
The physical channel is an explicitly imported ideal-bath theorem.
"""
from datetime import datetime, timezone
from fractions import Fraction as Q
from hashlib import sha256
from pathlib import Path
import json
import math
import signal
import sys
import time

OWN = Path(__file__).resolve().parent
ROOT = OWN.parents[4]
sys.dont_write_bytecode = True
sys.path.insert(0, str(OWN.parent / "algorithm_review"))
import independent_posterior_verifier as independent


def need(ok, message):
    if not ok:
        raise ValueError(message)


def enc(value):
    return independent.encode(value)


def positive_sum(x, degree):
    total = term = Q(1)
    for k in range(1, degree + 1):
        term *= x / k
        total += term
    return total


def main():
    began = time.perf_counter()
    def timeout(signum, frame):
        raise TimeoutError("declared10s owned arithmetic cap reached")
    signal.signal(signal.SIGALRM, timeout)
    signal.setitimer(signal.ITIMER_REAL, 10)
    try:
        source = OWN.parent / "filtered_review/source_snapshots/scaling_N64.json"
        raw = source.read_bytes()
        need(sha256(raw).hexdigest() == "4fafd8807baadcdb8ea26958393ae50bd75b47218769826bf2ff29d128ba7118",
             "N64 delivered output does not match frozen independently accepted pin")
        model = json.loads(raw)["model"]
        N = model["N"]
        alpha, delta, h = map(independent.rational, (model["alpha"], model["delta"], model["h"]))
        need((N, alpha, delta, h) == (64, Q(3), Q(1), Q(1, 3)), "wrong saved fixture")
        eps = independent.rational(model["total_target_trace_distance_upper"])
        logs = [-delta * Q((2 * t - N) ** 2, 4 * N) + h * Q(2 * t - N, 2)
                for t in range(N + 1)]
        peak = max(logs)
        f = [independent.independent_exp_minus(peak - x) for x in logs]
        zlo = zhi = blo = bhi = clo = chi = Q(0)
        records = []
        for b in range(N // 2 + 1):
            multiplicity = math.comb(N, b) - (math.comb(N, b - 1) if b else 0)
            j = Q(N, 2) - b
            emit_max = j * (j + 1) + Q(N % 2, 4)
            elo, ehi = independent.independent_exp_minus(alpha * Q(b * (N + 1 - b), N))
            masslo = multiplicity * elo * sum(f[t][0] for t in range(b, N - b + 1))
            masshi = multiplicity * ehi * sum(f[t][1] for t in range(b, N - b + 1))
            zlo += masslo
            zhi += masshi
            blo += b * masslo
            bhi += b * masshi
            clo += emit_max * masslo
            chi += emit_max * masshi
            records.append({"b": b, "physical_multiplicity": multiplicity,
                            "spin_dimension": N - 2 * b + 1,
                            "unnormalized_mass_interval": [enc(masslo), enc(masshi)]})
        need(zhi >= zlo > 0, "invalid target positive normalization")
        beta_interval = blo / zhi, bhi / zlo
        C_interval = clo / zhi, chi / zlo
        # D=half trace norm: observable RANGE times eps, not twice that.
        beta_error = Q(N, 2) * eps
        Jmax = Q(N, 2)
        C_error = Jmax * (Jmax + 1) * eps
        beta_actual_lower = beta_interval[0] - beta_error
        C_actual_upper = C_interval[1] + C_error
        # Small rational bounds, directed after charging the actual-output error.
        beta = Q((16 * beta_actual_lower).numerator // (16 * beta_actual_lower).denominator, 16)
        C = Q(-((-C_actual_upper.numerator) // C_actual_upper.denominator))
        need(0 < beta <= beta_actual_lower and C >= C_actual_upper, "simple bounds not conservative")
        ratio = 2 * N * C / (beta * beta)
        # Every finite positive Taylor sum lies STRICTLY below exp(x), x>0.
        tau = next(s for s in range(1, 101) if positive_sum(Q(s, 2), 64) > ratio)
        degree = next(m for m in range(65) if positive_sum(Q(tau, 2), m) > ratio)
        T = positive_sum(Q(tau, 2), degree)
        need(T > ratio, "Taylor onset inequality not strict")
        witness_upper = 2 * C / T - beta * beta / N
        need(witness_upper < 0, "collective witness not strictly negative")
        theorem = ROOT / "work/cycle6/c07_s02/phase2/COLLECTIVE_DECAY_ENTANGLEMENT.txt"
        prior_audit = ROOT / "work/cycle6/c05_s03/revisions/19_collective_decay_fresh_proof_audit.txt"
        theorem_raw, prior_audit_raw = theorem.read_bytes(), prior_audit.read_bytes()
        for name, data in [("SOURCE_COLLECTIVE_DECAY_ENTANGLEMENT.txt", theorem_raw),
                           ("SOURCE_COLLECTIVE_DECAY_FRESH_AUDIT.txt", prior_audit_raw)]:
            destination = OWN / name
            if destination.exists():
                need(destination.read_bytes() == data, "previous owned source pin would change")
            else:
                destination.write_bytes(data)
        posterior = OWN.parent / "filtered_review/FILTERED_FINAL_ALL4_VERIFY.json"
        final_manifest = OWN.parent / "filtered_review/FINAL_CHECKS_MANIFEST.json"
        library = OWN.parent / "algorithm_review/independent_posterior_verifier.py"
        result = {"utc": datetime.now(timezone.utc).isoformat(),
                  "status": "PASS exact costed onset for the actual unconditioned compiled N64 ensemble under the stated ideal collective bath",
                  "N": N, "alpha": enc(alpha), "delta": enc(delta), "h": enc(h),
                  "input_sha256": sha256(raw).hexdigest(), "input_path": str(source),
                  "input_trace_distance_upper": enc(eps),
                  "target_beta_interval": [enc(x) for x in beta_interval],
                  "target_C_interval": [enc(x) for x in C_interval],
                  "beta_observable_range_error": enc(beta_error),
                  "C_observable_range_error": enc(C_error),
                  "actual_beta_lower_before_simple_rounding": enc(beta_actual_lower),
                  "actual_C_upper_before_simple_rounding": enc(C_actual_upper),
                  "simple_actual_beta_lower": enc(beta), "simple_actual_C_upper": enc(C),
                  "dimensionless_onset_tau": tau, "time_statement": "Gamma*t >= tau suffices, including equality; all later times also satisfy the strict witness",
                  "log_argument_upper": enc(ratio), "positive_Taylor_degree": degree,
                  "positive_Taylor_argument": enc(Q(tau, 2)), "positive_Taylor_lower": enc(T),
                  "strict_Taylor_margin": enc(T - ratio),
                  "linear_witness": "W_beta=J_+J_--(2*beta/N)(J_z+N/2)+(beta^2/N)I",
                  "linear_witness_upper_at_and_after_tau": enc(witness_upper),
                  "target_joint_entries": sum(x["spin_dimension"] for x in records),
                  "spin_sectors": records,
                  "source_pins": {str(p): sha256(p.read_bytes()).hexdigest()
                                  for p in (theorem, prior_audit, posterior, final_manifest, library)},
                  "method": "Independent outward rational exponentials; positive joint-mass moment sums; directed trace-distance observable-range correction; exact simple rational rounding; strictly lower positive Taylor exponential bound",
                  "scope": "Unconditioned actual output density of the frozen finite product sampler, with its phase/subset/local rounding errors already included. Arbitrary actual initial coherences allowed by imported bath theorem. Entanglement means failure of full separability, not a claim for every conditioned draw, stronger multipartite depth, priority, simulation or hardware realization.",
                  "declared_arithmetic_cap_seconds": 10,
                  "no_compiler_or_LP_rerun": True,
                  "code_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
                  "wall_seconds": time.perf_counter() - began}
        need(result["wall_seconds"] < 10, "arithmetic cap exceeded before export")
        (OWN / "COMPILED_N64_ONSET_CERTIFICATE.json").write_text(json.dumps(result, indent=2) + "\n")
        print(json.dumps({"status": result["status"], "beta_lower": str(beta), "C_upper": str(C),
                          "tau": tau, "Taylor_degree": degree,
                          "target_beta_display": [float(x) for x in beta_interval],
                          "target_C_display": [float(x) for x in C_interval],
                          "witness_upper_display": float(witness_upper),
                          "wall_seconds": result["wall_seconds"]}, indent=2))
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)


if __name__ == "__main__":
    main()
