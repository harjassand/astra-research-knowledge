"""Independent true-filter model certificates for frozen peer deliveries.

No peer code is imported/executed. This certifies the actual rational K weights,
excluding conditional-block, phase, local-preparation and sampling errors.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import signal
import time
from decimal import Decimal, localcontext

from axial_acquisition import sector_matrix, matvec, spin_dimensions
from filtered_sector import (interval_sum, positive_interval_product,
                             positive_normalize, interval_TV_upper)
from fast_scalar_enclosure import exp_negative_interval


def acquired_model_posterior(N, alpha, delta, h, bits, w):
    """Independent scalar acquisition; previous physical-sector formula."""
    H = abs(h) * N / 2
    fiv = []
    for t in range(N + 1):
        m = F(2 * t - N, 2)
        fiv.append(exp_negative_interval(H + delta * m * m / N - h * m, bits))
    civ = []
    for b in range(N // 2 + 1):
        lo, hi = interval_sum(fiv[b:N - b + 1])
        civ.append((lo / (N - 2 * b + 1), hi / (N - 2 * b + 1)))
    riv = [exp_negative_interval(alpha * b * F(N + 1 - b, N), bits)
           for b in range(len(civ))]
    raw = [positive_interval_product(r, c) for r, c in zip(riv, civ)]
    dims = spin_dimensions(N)
    target, target_Z = positive_normalize([(lo * D, hi * D) for (lo, hi), D in zip(raw, dims)])
    Aw = matvec(sector_matrix(N), w)
    candidate, candidate_Z = positive_normalize([(a * lo, a * hi) for a, (lo, hi) in zip(Aw, civ)])
    return {"target_sector_intervals": target, "candidate_sector_intervals": candidate,
            "TV_upper": interval_TV_upper(target, candidate)}


def interval_TV_lower(a, b):
    if len(a) != len(b):
        raise ValueError("matching interval vectors required")
    return sum((max(F(0), x[0] - y[1], y[0] - x[1])
                for x, y in zip(a, b)), F(0)) / 2


def main():
    def wall_limit(signum, frame):
        raise TimeoutError("declared10second repaired model certificate cap exceeded")
    signal.signal(signal.SIGALRM, wall_limit)
    signal.alarm(10)
    started, assertions, records = time.perf_counter(), 0, []

    def check(condition):
        nonlocal assertions
        assertions += 1
        assert condition

    def frac(record):
        return F(int(record["numerator"]), int(record["denominator"]))

    frozen_path = Path(__file__).with_name("FROZEN_MODEL_WEIGHT_INPUTS.json")
    frozen_raw = frozen_path.read_bytes()
    frozen = {r["N"]: r for r in json.loads(frozen_raw)["cases"]}
    # A high-precision decimal comparison is diagnostic evidence; containment
    # is proved by the directed integer recurrence and geometric-tail argument.
    scalar_diagnostic_cases = 0
    for bits in [8, 32, 96, 160]:
        for x in [F(0), F(1, 16), F(1, 3), F(17, 3), F(33), F(1000)]:
            lo, hi = exp_negative_interval(x, bits)
            check(0 <= lo <= hi <= 1 and hi - lo <= F(1, 1 << bits))
            with localcontext() as ctx:
                ctx.prec = 180
                dx = Decimal(x.numerator) / Decimal(x.denominator)
                value = (-dx).exp()
                dlo, dhi = [Decimal(t.numerator) / Decimal(t.denominator) for t in [lo, hi]]
                check(dlo <= value <= dhi)
            scalar_diagnostic_cases += 1
    lo, hi = exp_negative_interval(F(1 << 256), 160)
    check(lo == 0 and hi == F(1, 1 << 162))

    for N in [8, 16, 32, 64]:
        fixture = frozen[N]
        path = Path(fixture["original_source"])
        model = fixture["model"]
        alpha, delta, h, eps = [frac(model[k]) for k in ["alpha", "delta", "h", "epsilon"]]
        check(alpha == 3 and delta == 1 and h == F(1, 3))
        w = [frac(x) for x in model["isotropic_weights"]]
        check(len(w) == N + 1 and min(w) >= 0 and sum(w) == 1)
        bits = max(96, 2 * N + 32)
        cert = acquired_model_posterior(N, alpha, delta, h, bits, w)
        lower = interval_TV_lower(cert["target_sector_intervals"], cert["candidate_sector_intervals"])
        upper = cert["TV_upper"]
        check(0 <= lower <= upper < eps)
        bad_w = [F(int(k == 0)) for k in range(N + 1)]
        bad = acquired_model_posterior(N, alpha, delta, h, bits, bad_w)
        bad_lower = interval_TV_lower(bad["target_sector_intervals"], bad["candidate_sector_intervals"])
        check(bad_lower > F(1, 100))
        check(bad_lower <= bad["TV_upper"])
        record = {"N": N, "alpha": str(alpha), "delta": str(delta), "h": str(h),
                  "epsilon": str(eps), "source": str(path),
                  "source_sha256": fixture["original_source_sha256"],
                  "source_bytes": fixture["original_source_bytes"], "precision_bits": bits,
                  "own_true_filter_model_TV_lower": str(lower),
                  "own_true_filter_model_TV_upper": str(upper),
                  "own_true_filter_model_TV_upper_float": float(upper),
                  "wrong_K0_model_TV_lower": str(bad_lower),
                  "wrong_K0_model_TV_lower_float": float(bad_lower),
                  "sampler_block_phase_preparation_errors_included": False}
        if N > 16:
            record["peer_source_reported_compile_seconds"] = model["compile_seconds"]
            record["peer_source_reported_total_trace_upper"] = model["total_target_trace_distance_upper"]
            record["peer_source_reported_joint_entries"] = model["joint_certificate_entries"]
            record["peer_source_reported_branches"] = model["branch_count"]
            record["peer_source_reported_cached_zero_field_rules"] = model["cached_zero_field_rules"]
            record["peer_source_reported_draw_bits"] = model["predetermined_random_bits_per_sample"]
        records.append(record)

    result = {"status": "PASS", "assertions": assertions,
              "elapsed_seconds_shared_machine": time.perf_counter() - started,
              "wall_cap_seconds": 10,
              "scalar_diagnostic_cases": scalar_diagnostic_cases,
              "scalar_interval_source": "owned directed-integer Taylor/reciprocal/square algorithm",
              "owned_frozen_input_sha256": hashlib.sha256(frozen_raw).hexdigest(),
              "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "independent_actual_peer_model_certificates": records,
              "scope": "actual rational weights vs TRUE scalar-filter intervals, full physical trace metric",
              "peer_optimizer_or_sampler_executed": False,
              "generic_LP_or_iid_backend_executed": False,
              "hardware_preparation": "NOT_EXECUTED"}
    signal.alarm(0)
    Path(__file__).with_name("scaling_model_checks.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": result["status"], "assertions": assertions,
                      "elapsed_seconds_shared_machine": result["elapsed_seconds_shared_machine"],
                      "own_model_errors": [{"N": r["N"], "upper": r["own_true_filter_model_TV_upper_float"],
                                             "wrong_K0_lower": r["wrong_K0_model_TV_lower_float"]}
                                            for r in records]}, indent=2))


if __name__ == "__main__":
    main()
