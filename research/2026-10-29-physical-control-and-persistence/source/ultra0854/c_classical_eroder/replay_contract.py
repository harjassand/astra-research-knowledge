"""Independent finite scalar/transport consumer; no producer code imports.

The all-volume proof and ordinary spectral/Finner imports remain analytical
premises, rather than conclusions from this finite replay.
"""
import hashlib
import json
from pathlib import Path
import time
from fractions import Fraction as F


def parse(obj):
    return F(int(obj["numerator"]), int(obj["denominator"]))


def p2(k):
    return F(1 << k) if k >= 0 else F(1, 1 << (-k))


def main():
    start = time.perf_counter()
    root = Path(__file__).resolve().parent
    result = json.loads((root / "REGISTER_CONTRACT.json").read_text())
    x = result["inputs"]
    n, q = x["sites_per_register"], x["q"]
    assert n == x["side"] ** 2
    lam = parse(x["lambda_upper"])
    assert lam == F(1, 1024 * (2 ** q - 1))
    T, latency = int(x["horizon"]), x["copy_readout_latency"]
    assert T == 2 ** x["horizon_bits"] and 0 < latency <= T
    h, lower = (n + 63) // 64, (9 * n + 1023) // 1024
    assert h > q
    assert h == result["levels"]["source_first_exit"]
    assert lower == result["levels"]["copy_excursion_lower"]
    assert x["initial_wrong_upper"] == n // 256

    spectral = 3 * (F(1, 64) + F(25, 32) ** 16)
    assert spectral < F(1, 8)
    assert parse(result["exact_universal_inequality"]["3_times_rho_plus_sigma_squared"]) == spectral
    rmin, rmax = F(15, 16), F(17, 16)
    a, d = rmax / 8, rmin * F(7, 8)
    assert a == F(17, 128) and d == F(105, 128)
    assert d - 2 * a == F(71, 128) > F(1, 2)
    assert 2 * lam * (2 ** q - 1) == F(1, 512)
    # The proof's ln2>=1/2 relaxation is now purely rational.
    assert F(3, 256) * F(1, 2) - F(1, 512) == F(1, 256)
    copy_positive = (rmax + rmin / 2) / 512 + lam * (2 ** q - 1)
    copy_negative = rmin * F(9, 1024) / 2
    assert copy_positive == F(130, 32768)
    assert copy_negative - copy_positive == F(5, 32768) > 0

    source = min(F(1), 2 ** q * n * (1 + lam) * T * p2(-(n // 256)))
    excursion = n * (rmax + lam) * T * p2(lower + q - h)
    forgetting = n * p2(-(15 * latency // 16))
    total = min(F(1), source + excursion + forgetting)
    for name, expected in [("retained_bit_failure", source),
                           ("copy_source_failure", source),
                           ("copy_excursion_failure", excursion),
                           ("copy_initial_forgetting_failure", forgetting),
                           ("total_buffered_copy_failure", total)]:
        assert parse(result["bounds"][name]) == expected, name

    graph = root / result["actual_graph_acquisition"]["path"]
    content = graph.read_bytes()
    assert len(content) == 32 * n
    assert hashlib.sha256(content).hexdigest() == result["actual_graph_acquisition"]["sha256"]
    report = {"status": "PASS_FINITE_ARITHMETIC_AND_TRANSPORT",
              "producer_imports": False, "graph_bytes_checked": len(content),
              "graph_reacquired": False, "new_graph_or_noise_cases": 0,
              "new_trajectories": 0, "all_volume_theorem_replaced_by_replay": False,
              "clock_calibration_interval": [str(rmin), str(rmax)],
              "branching_birth_rate": str(a), "branching_death_rate": str(d),
              "branching_exponential_drift": str(d - 2 * a),
              "copy_exponential_drift_margin_per_n": str(copy_negative - copy_positive),
              "total_failure_exact": [str(total.numerator), str(total.denominator)],
              "seconds_after_imports": time.perf_counter() - start}
    (root / "REPLAY.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: report[k] for k in ["status", "seconds_after_imports"]}))


if __name__ == "__main__":
    main()
