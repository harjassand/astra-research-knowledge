"""Train/held-out scalar reference certificate for the exact observation channel.

Inputs are charged calibration records. The iid/range/domination contracts
are assumptions supplied with the data, not inferred from empirical fits.
The built-in demo uses declared finite tapes and is a software diagnostic.
"""
from __future__ import annotations

from fractions import Fraction as F
from pathlib import Path
import argparse
import json
import math
import random
import time

from covariance_codec import fs, log_interval


def sqrt_upper(x: F, bits: int = 40) -> F:
    assert x >= 0
    scale = 1 << bits
    scaled = x * scale * scale
    k = math.isqrt(scaled.numerator // scaled.denominator)
    if F(k * k) < scaled:
        k += 1
    answer = F(k, scale)
    assert answer * answer >= x
    return answer


def divergence_interval(a: F, b: F, bits: int) -> tuple[F, F]:
    assert a >= 0 and b > 0
    if a == b:
        return F(0), F(0)
    if a == 0:
        return b, b
    lo, hi = log_interval(a / b, bits)
    return max(F(0), a * lo - a + b), a * hi - a + b


def certify(raw: dict, bits: int = 48) -> dict:
    alpha, beta = F(raw["alpha"]), F(raw["beta"])
    threshold, C, epsilon = F(raw["classifier_threshold"]), F(raw["domination_C"]), F(raw["epsilon"])
    delta, k = F(raw["confidence_delta"]), int(raw["outputs_k"])
    t0, t1 = F(raw["T0"]), F(raw["T1"])
    training = [F(x) for x in raw["training"]]
    validation = [F(x) for x in raw["validation"]]
    assert 0 < alpha <= threshold < beta and C >= 1 and 0 < delta < 1
    assert k >= 1 and 0 < epsilon <= 1 and 0 < t0 < t1
    assert training and validation and all(alpha <= a <= beta for a in training + validation)
    def label(a):
        return int(a > threshold)
    means, counts = [], []
    for j in (0, 1):
        values = [a for a in training if label(a) == j]
        counts.append(len(values))
        means.append(sum(values, F(0)) / len(values) if values else alpha)
        assert alpha <= means[-1] <= beta
    intervals = [divergence_interval(a, means[label(a)], bits) for a in validation]
    empirical_low = sum((v[0] for v in intervals), F(0)) / len(validation)
    empirical_up = sum((v[1] for v in intervals), F(0)) / len(validation)
    R0 = (beta - alpha) ** 2 / (2 * alpha)
    for lo, hi in intervals:
        assert 0 <= lo <= hi
        # Roundoff interval width is separately paid; exact risk is <=R0.
        assert hi <= R0 + F(1, 1 << (bits - 4))
    _, log_delta_upper = log_interval(1 / delta, bits)
    confidence = R0 * sqrt_upper(log_delta_upper / (2 * len(validation)))
    risk_upper = empirical_up + confidence
    W = 1 / t0 - 1 / t1
    criterion = 4 * W * epsilon * epsilon / (k * C)
    tv_sq = k * C * risk_upper / (4 * W)
    return {
        "status": "CERTIFIED_UNDER_IID_RANGE_DOMINATION_CONTRACT" if risk_upper <= criterion else "UNKNOWN",
        "confidence_failure_probability": fs(delta),
        "retained_dimension": 2, "fixed_binary_bits": 1,
        "training_draws": len(training), "validation_draws": len(validation),
        "training_bin_counts": counts, "classifier_threshold": fs(threshold),
        "codebook_covariances": [fs(m) for m in means],
        "range_loss_upper_R0": fs(R0),
        "empirical_risk_interval": {"lower": fs(empirical_low), "upper": fs(empirical_up)},
        "confidence_radius_upper": fs(confidence), "reference_risk_upper": fs(risk_upper),
        "reference_risk_threshold": fs(criterion), "uniform_TV_squared_upper": fs(tv_sq),
        "epsilon": fs(epsilon), "k": k, "C": fs(C), "W": fs(W),
        "precision_bits": bits,
        "source_assumptions": ["training independent of fresh iid validation under mu",
                               "declared field range alpha<=A<=beta for the whole source",
                               "dP_v/dmu<=C for all target parameters"],
        "sampler_status": "IDEAL_GAUSSIAN_DECODER; DIGITAL_CONTINUOUS_OUTPUT_NOT_IMPLEMENTED",
    }


def demo() -> dict:
    values = ["1/2", "3/5", "9/10", "1"]
    training_tape, validation_tape = random.Random(42), random.Random(2048)
    return {
        "alpha": "1/2", "beta": "1", "classifier_threshold": "3/4",
        "domination_C": "2", "epsilon": "1/4", "confidence_delta": "1/20",
        "outputs_k": 3, "cap_L": "8", "T0": "1", "T1": "2",
        "training": [values[training_tape.getrandbits(2)] for _ in range(32)],
        "validation": [values[validation_tape.getrandbits(2)] for _ in range(512)],
        "fixture_reference_values": values,
        "fixture_note": "Independent fixed pseudorandom tapes exercise the software; physical source/iid certification not claimed.",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path)
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("acquired_decoder_certificate.json"))
    args = parser.parse_args()
    target = args.output.resolve()
    assert target.is_relative_to(Path(__file__).resolve().parent)
    assert not target.exists(), "Preserve existing results; choose a new output path"
    started = time.perf_counter()
    raw = json.loads(args.input.read_text()) if args.input else demo()
    result = certify(raw)
    check = {"scope": "NOT_A_PHYSICAL_SOURCE_RUN"}
    if "fixture_reference_values" in raw:
        means = [F(x) for x in result["codebook_covariances"]]
        threshold = F(raw["classifier_threshold"])
        exact = [divergence_interval(F(x), means[int(F(x) > threshold)], 48)
                 for x in raw["fixture_reference_values"]]
        exact_low = sum((x[0] for x in exact), F(0)) / len(exact)
        exact_up = sum((x[1] for x in exact), F(0)) / len(exact)
        assert exact_up <= F(result["reference_risk_upper"])
        check.update({"exact_fixture_reference_risk_interval": {"lower": fs(exact_low), "upper": fs(exact_up)},
                      "confidence_upper_covers_fixture_true_risk": True})
    for x in [F(0), F(1, 9), F(2), F(2000, 13)]:
        assert sqrt_upper(x) ** 2 >= x
    assert divergence_interval(F(0), F(1, 2), 48) == (F(1, 2), F(1, 2))
    record = {"input": raw, "certificate": result, "checks": check,
              "local_seconds": time.perf_counter() - started, "backend_energy_tokens": "UNKNOWN"}
    target.write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps({"output": str(target), "status": result["status"], "D": 2, "binary_bits": 1,
                      "draws": result["training_draws"] + result["validation_draws"], "k": result["k"],
                      "TV_upper_approx": math.sqrt(float(F(result["uniform_TV_squared_upper"]))),
                      "confidence_failure_probability": result["confidence_failure_probability"],
                      "codebook_covariances": result["codebook_covariances"],
                      "true_fixture_risk_upper_approx": float(F(check["exact_fixture_reference_risk_interval"]["upper"])),
                      "local_seconds": record["local_seconds"]}, indent=2))


if __name__ == "__main__":
    main()
