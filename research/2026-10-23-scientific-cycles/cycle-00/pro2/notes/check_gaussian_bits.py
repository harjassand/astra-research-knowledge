"""Bounded adversarial diagnostics for the integer Box--Muller module.

Decimal reference values are diagnostic only; verification in gaussian_bits.py
uses integer intervals and does not trust these reference values.
"""
from __future__ import annotations

from decimal import Decimal, localcontext
import hashlib
import importlib.util
import json
from pathlib import Path
import random
import resource
import struct
import tempfile
import time
from unittest.mock import patch

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("gaussian_bits", ROOT / "src" / "gaussian_bits.py")
gb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gb)


def dec_pi():
    # Independent Gauss--Legendre reference, not used by the certificate.
    a, b, t, p = Decimal(1), Decimal(1) / Decimal(2).sqrt(), Decimal(1) / 4, Decimal(1)
    for _ in range(12):
        a_next, b_next = (a + b) / 2, (a * b).sqrt()
        t -= p * (a - a_next) ** 2
        a, b, p = a_next, b_next, 2 * p
    return (a + b) ** 2 / (4 * t)


def dec_sincos(x):
    # Direct argument, independent of the production quadrant reduction.
    sin_term, cos_term = x, Decimal(1)
    sine, cosine = sin_term, cos_term
    for k in range(1, 100):
        sin_term *= -(x * x) / ((2 * k) * (2 * k + 1))
        cos_term *= -(x * x) / ((2 * k - 1) * (2 * k))
        sine += sin_term
        cosine += cos_term
    return sine, cosine


def contains(interval, value):
    return Decimal(interval[0]) / gb.Q <= value <= Decimal(interval[1]) / gb.Q


def expect_reject(action, label, records):
    try:
        action()
    except (ValueError, FileExistsError, gb.ProbeGenerationFailure) as exc:
        records.append({"case": label, "status": "rejected", "exception": type(exc).__name__})
    else:
        raise AssertionError("checker accepted " + label)


def numerical_diagnostics():
    rng = random.Random(70320261021)
    radial = [1, 2, 3, gb.N // 1024, gb.N // 2 - 1, gb.N // 2, gb.N - 2, gb.N - 1]
    angular = [0, gb.N // 8 - 1, gb.N // 8, gb.N // 4 - 1, gb.N // 4,
               gb.N // 2 - 1, gb.N // 2, 3 * gb.N // 4, gb.N - 1]
    pairs = [(j, h) for j in radial for h in angular]
    pairs += [(rng.randrange(1, gb.N), rng.randrange(gb.N)) for _ in range(100)]
    max_pair_ratio = Decimal(0)
    max_component_ratio = Decimal(0)
    with localcontext() as ctx:
        ctx.prec = 120
        pi = dec_pi()
        assert contains(gb.PI, pi)
        assert contains(gb.LN2, Decimal(2).ln())
        for j, h in pairs:
            u0, v0 = Decimal(2 * j + 1) / (2 * gb.N), Decimal(2 * h + 1) / (2 * gb.N)
            radius = (-2 * u0.ln()).sqrt()
            sine, cosine = dec_sincos(2 * pi * v0)
            assert contains(gb._log_midpoint(j), u0.ln())
            cos_i, sin_i = gb._sin_cos_midpoint(h)
            assert contains(cos_i, cosine)
            assert contains(sin_i, sine)
            values, bound, components = gb._pair(j, h)
            stored = [Decimal(x) / gb.DENOMINATOR for x in values]
            exact_midpoint = [radius * cosine, radius * sine]
            # Check all four cell corners; the proof separately covers the interior.
            tests = [exact_midpoint]
            for u_num in (j, j + 1):
                u = Decimal(u_num) / gb.N
                r = (-2 * u.ln()).sqrt()
                for v_num in (h, h + 1):
                    v = Decimal(v_num) / gb.N
                    sin_v, cos_v = dec_sincos(2 * pi * v)
                    tests.append([r * cos_v, r * sin_v])
            for ideal in tests:
                errors = [abs(a - b) for a, b in zip(ideal, stored)]
                error = sum(x * x for x in errors).sqrt()
                pair_ratio = error * gb.Q / bound
                assert pair_ratio <= 1, (j, h, str(pair_ratio))
                max_pair_ratio = max(max_pair_ratio, pair_ratio)
                for e, b in zip(errors, components):
                    ratio = e * gb.Q / b
                    assert ratio <= 1, (j, h, str(ratio))
                    max_component_ratio = max(max_component_ratio, ratio)
    return {"pair_count": len(pairs), "midpoint_and_corner_vectors_checked": 5 * len(pairs),
            "decimal_precision": 120,
            "maximum_pair_error_over_certified_bound": str(max_pair_ratio),
            "maximum_coordinate_error_over_certified_bound": str(max_component_ratio),
            "status": "PASS", "scope": "independent numerical diagnostics, not a replacement proof"}


def binding_diagnostics():
    records = []
    with tempfile.TemporaryDirectory(prefix="astra_gaussian_test_") as temp:
        root = Path(temp)
        work = root / "fixture"
        _, _, cert = gb.generate_probe_block(8, 4, work, seed=20261021)
        bits_hash = cert["bits_sha256"]
        receipt = gb.verify_probe_block(work, expected_n=8, expected_s=4, expected_bits_sha256=bits_hash)
        assert receipt["status"] == "PASS"
        records.append({"case": "exact_replay_with_pinned_identity", "status": "PASS"})
        before = {p.name: p.read_bytes() for p in work.iterdir()}
        expect_reject(lambda: gb.generate_probe_block(8, 4, work, seed=33), "generation_refuses_existing_files", records)
        assert before == {p.name: p.read_bytes() for p in work.iterdir()}
        expect_reject(lambda: gb.verify_probe_block(work, expected_n=9), "receiver_dimension_mismatch", records)
        expect_reject(lambda: gb.verify_probe_block(work, expected_bits_sha256="0" * 64), "receiver_bits_identity_mismatch", records)

        bits_path = work / "gaussian_bits.bin"
        raw = bytearray(bits_path.read_bytes())
        raw[1] ^= 1
        bits_path.write_bytes(raw)
        expect_reject(lambda: gb.verify_probe_block(work, expected_bits_sha256=bits_hash), "changed_bit_source", records)
        bits_path.write_bytes(before[bits_path.name])

        array_path = work / "gaussian_probe_ints.npy"
        array = np.load(array_path, allow_pickle=False)
        array[0, 0] += 1
        np.save(array_path, array, allow_pickle=False)
        cert_path = work / "gaussian_probe_certificate.json"
        modified = json.loads(before[cert_path.name])
        modified["probe_file_sha256"] = hashlib.sha256(array_path.read_bytes()).hexdigest()
        cert_path.write_text(json.dumps(modified))
        expect_reject(lambda: gb.verify_probe_block(work), "changed_probe_with_updated_file_hash", records)
        array_path.write_bytes(before[array_path.name])
        cert_path.write_bytes(before[cert_path.name])

        modified = json.loads(before[cert_path.name])
        modified["global_normalized_cdf_slack"] = {"numerator": "0", "denominator": "1"}
        cert_path.write_text(json.dumps(modified))
        expect_reject(lambda: gb.verify_probe_block(work), "understated_coupling_slack", records)
        cert_path.write_bytes(before[cert_path.name])
        assert gb.verify_probe_block(work)["status"] == "PASS"

        odd = root / "odd_fixture"
        _, _, odd_cert = gb.generate_probe_block(3, 1, odd, seed=337)
        assert odd_cert["pair_count"] == 2
        assert gb.verify_probe_block(odd)["status"] == "PASS"
        records.append({"case": "odd_coordinate_count_last_component_discarded", "status": "PASS"})

        # A mock source forces the rare rejection branch. This is not random data.
        abort = root / "zero_cell_mock"
        raw_zero = struct.pack("<QQ", 0, 59)
        with patch.object(gb.os, "urandom", return_value=raw_zero):
            expect_reject(lambda: gb.generate_probe_block(2, 1, abort), "mock_zero_radial_cell", records)
        assert (abort / "gaussian_bits.bin").read_bytes() == raw_zero
        assert json.loads((abort / "gaussian_probe_certificate.json").read_text())["status"] == "generation_failed_no_redraw"
        assert not (abort / "gaussian_probe_ints.npy").exists()
        expect_reject(lambda: gb.generate_probe_block(2, 1, abort, seed=9), "abort_is_not_silently_redrawn", records)
    return records


def main():
    start_wall, start_cpu = time.perf_counter(), time.process_time()
    result = {"schema": "astra-gaussian-module-diagnostics-v1", "numerical": numerical_diagnostics(),
              "binding_and_abort": binding_diagnostics(),
              "resources": {"wall_seconds": time.perf_counter() - start_wall,
                            "cpu_seconds": time.process_time() - start_cpu,
                            "peak_process_rss_bytes_linux": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024},
              "probability_scope": "no Monte Carlo coverage claim; all generated probe blocks here are fixtures or mocks"}
    destination = Path(__file__).with_name("gaussian_bits_diagnostics.json")
    destination.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
