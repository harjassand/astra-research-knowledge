#!/usr/bin/env python3
"""Independent, bounded challenge of exact_residual.py.

This file does not change the checker.  Exact comparisons exercise the
input-to-dyadic and integer-kernel boundary; small floating polar computations
are explicitly diagnostic.  Run under python -O to ensure assertions do not
form part of the admission gate.
"""
from __future__ import annotations

from fractions import Fraction as F
from math import isqrt
from pathlib import Path
import gzip
import hashlib
import json
import sys
import tempfile
import time

import numpy as np
from scipy.sparse import csr_matrix, csc_matrix

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import exact_residual as er


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


def q(cert, key):
    return er.jf(cert[key])


def rejected(fn, *args):
    try:
        fn(*args)
    except (ValueError, TypeError, IndexError, OverflowError, ZeroDivisionError) as exc:
        return {"exception": type(exc).__name__, "message": str(exc)}
    raise RuntimeError("malformed/unsafe input was accepted")


def independent_root_bracket(x, bits):
    """Integer bisection rather than the checker's integer-square-root path."""
    x = F(x)
    den = 1 << bits
    low, high = 0, 1
    while high * high * x.denominator < x.numerator * den * den:
        high *= 2
    while high - low > 1:
        mid = (low + high) // 2
        if mid * mid * x.denominator <= x.numerator * den * den:
            low = mid
        else:
            high = mid
    if high * high * x.denominator == x.numerator * den * den:
        return F(high, den), F(high, den)
    if low * low * x.denominator == x.numerator * den * den:
        return F(low, den), F(low, den)
    return F(low, den), F(high, den)


def exact_scalar_checks():
    roots = 0
    cases = [F(0), F(1), F(4, 9), F(2), F(3, 7), F(1, 10**80),
             F(10**80, 3), F(17**2, 23**2)]
    cases += [F(i, j) for i in range(1, 30, 3) for j in range(1, 21, 4)]
    for x in cases:
        for bits in (0, 1, 7, 32, 100):
            lo, hi = er.sqrt_interval(x, bits)
            need(0 <= lo <= hi and lo * lo <= x <= hi * hi,
                 "square-root interval fails squared endpoint check")
            need(hi - lo <= F(1, 1 << bits), "square-root interval too wide")
            need((lo, hi) == independent_root_bracket(x, bits),
                 "independent rational bisection disagrees")
            roots += 1
    rounded = 0
    for num in range(-81, 82):
        for den in range(1, 18):
            x = F(num, den)
            z = er.round_fraction(x)
            need(abs(x - z) <= F(1, 2), "nearest rounding error")
            if abs(x - z) == F(1, 2):
                need(z > x, "signed tie was not upward")
            for bits in (0, 3, 80):
                upper = er.up(x, bits)
                need(0 <= upper - x < F(1, 1 << bits), "upper rounding failed")
            rounded += 1
    return {"exact_root_cases": roots, "signed_nearest_rounding_cases": rounded,
            "upper_rounding_cases": rounded * 3}


def mm_text(n, records):
    return ("%%MatrixMarket matrix coordinate real symmetric\n"
            "% synthetic bounded audit fixture\n"
            f"{n} {n} {len(records)}\n" +
            "".join(f"{i+1} {j+1} {s}\n" for i, j, s in records))


def write_pair(directory, stiffness, mass, n=3):
    for name, recs in (("bcsstk08.mtx.gz", stiffness), ("bcsstm08.mtx.gz", mass)):
        (directory / name).write_bytes(gzip.compress(mm_text(n, recs).encode("ascii"), mtime=0))


def exact_loader_checks():
    stiffness = [(0, 0, "0.3"), (1, 0, "-0.7"), (1, 1, "1.4"),
                 (2, 0, "0"), (2, 1, "0.11"), (2, 2, "-3.2")]
    receipts = []
    with tempfile.TemporaryDirectory(prefix="astra_residual_audit_") as tmp:
        directory = Path(tmp)
        for label, masses in (("rational_square_masses", ["4", "9", "25"]),
                              ("irrational_cross_mass_roots", ["2", "3", "5"])):
            write_pair(directory, stiffness, [(i, i, m) for i, m in enumerate(masses)])
            ai, meta = er.load_exact_generalized(directory)
            den, scale = er.AD, int(meta["scale"])
            need(scale > 0 and scale & (scale - 1) == 0, "normalization is not a power of two")
            need(ai.dtype == np.int64 and (ai != ai.T).nnz == 0, "loader symmetry/type")
            rows = [F(0)] * 3
            target_rows = [F(0)] * 3
            for i, j, value in stiffness:
                root_lo, root_hi = independent_root_bracket(F(masses[i]) * F(masses[j]), 170)
                source = F(value) / scale
                a, b = sorted((source / root_lo, source / root_hi))
                dyadic = F(int(ai[i, j]), den)
                err = max(abs(a - dyadic), abs(b - dyadic))
                bound = max(abs(a), abs(b))
                rows[i] += err
                target_rows[i] += bound
                if i != j:
                    rows[j] += err
                    target_rows[j] += bound
            independent_tau = max(rows)
            need(independent_tau <= q(meta, "tau"), "published tau misses finer exact source enclosure")
            need(max(target_rows) <= 1, "source normalization bound failed")
            actual_absrows = max(sum(abs(int(x)) for x in ai.toarray()[i, :]) for i in range(3))
            need(q(meta, "M") == F(actual_absrows, den), "dyadic operator norm row bound mismatch")
            for name, digest in meta["input_sha256"].items():
                need(hashlib.sha256((directory / name).read_bytes()).hexdigest() == digest,
                     "source hash does not match read bytes")
            receipts.append({"case": label, "scale": scale, "tau": meta["tau"],
                             "independent_tau_upper": er.fj(independent_tau)})

        half = "0.000000000116415321826934814453125"  # exactly 2^-33
        write_pair(directory, [(0, 0, half), (1, 1, "-" + half)],
                   [(0, 0, "1"), (1, 1, "1")], n=2)
        ai, meta = er.load_exact_generalized(directory)
        need(ai.toarray().tolist() == [[1, 0], [0, 0]], "source signed half-way rounding")
        need(q(meta, "tau") == F(1, 2 * er.AD), "half-way source allowance")
        receipts.append({"case": "positive_and_negative_exact_halfway", "tau": meta["tau"]})

        bad = {}
        variants = {
            "nonpositive_mass": [(0, 0, "4"), (1, 1, "0"), (2, 2, "25")],
            "missing_mass": [(0, 0, "4"), (2, 2, "25")],
            "offdiagonal_mass": [(0, 0, "4"), (1, 0, "1"), (2, 2, "25")],
            "duplicate_mass": [(0, 0, "4"), (0, 0, "4"), (2, 2, "25")],
            "finite_root_precision_rejection": [(i, i, "1e-100") for i in range(3)],
        }
        for label, mass in variants.items():
            write_pair(directory, stiffness, mass)
            bad[label] = rejected(er.load_exact_generalized, directory)
        write_pair(directory, stiffness + [(0, 1, "1")], [(i, i, "1") for i in range(3)])
        bad["unexpected_upper_triangle"] = rejected(er.load_exact_generalized, directory)
    return {"valid_source_cases": receipts, "rejected_source_cases": bad}


def malformed_input_checks():
    n = 3
    ai = csr_matrix((n, n), dtype=np.int64)
    vi = np.zeros((n, 1), dtype=np.int64)
    vi[0, 0] = er.VD
    gi = np.array([1, 0, 0], dtype=np.int64)
    base = [ai, vi, [0], [], gi, 1, F(0)]
    variants = {}
    def variant(name, position, value):
        args = base.copy()
        args[position] = value
        variants[name] = args
    variant("negative_tau", 6, F(-1, 7))
    variant("nonfinite_tau", 6, float("nan"))
    variant("floating_nonzero_numerator", 0, csr_matrix(np.diag([2.0**-30, 0, 0])))
    variant("nonsymmetric_operator", 0, csr_matrix(np.array([[0, er.AD, 0], [0, 0, 0], [0, 0, 0]], dtype=np.int64)))
    variant("wrong_sparse_format", 0, csc_matrix(ai))
    variant("fractional_diagonal", 2, [F(1, 2)])
    variant("floating_integral_diagonal", 2, [0.0])
    variant("boolean_diagonal", 2, [False])
    variant("out_of_range_diagonal", 2, [1 << 64])
    variant("diagonal_length", 2, [0, 0])
    variant("fractional_probe", 4, np.array([1.5, 0, 0]))
    variant("short_probe", 4, gi[:1])
    variant("long_probe", 4, np.array([1, 0, 0, 0], dtype=np.int64))
    variant("zero_probe", 4, np.zeros(3, dtype=np.int64))
    variant("fractional_probe_denominator", 5, F(3, 2))
    variant("boolean_probe_denominator", 5, True)
    variant("zero_probe_denominator", 5, 0)
    variant("negative_probe_denominator", 5, -1)
    variant("floating_basis", 1, vi.astype(float))
    variant("rank_deficient_basis", 1, np.zeros((3, 1), dtype=np.int64))
    duplicate = csr_matrix((np.array([0, 0], dtype=np.int64), np.array([0, 0]),
                            np.array([0, 2, 2, 2])), shape=(3, 3))
    variant("duplicate_csr_records", 0, duplicate)
    result = {name: rejected(er.certify_krylov, *args) for name, args in variants.items()}
    two_basis = np.eye(3, dtype=np.int64)[:, :2] * er.VD
    for name, off in (("zero_offdiagonal", [0]), ("negative_offdiagonal", [-1]),
                      ("fractional_offdiagonal", [F(3, 2)]), ("offdiagonal_length", [])):
        result[name] = rejected(er.certify_krylov, ai, two_basis, [0, 0], off, gi, 1, 0)
    dense_basis = np.eye(3, dtype=np.int64) * er.VD
    result["dense_negative_tau"] = rejected(er.certify_dense, ai, dense_basis, [0, 0, 0], -1)
    result["dense_fractional_diagonal"] = rejected(er.certify_dense, ai, dense_basis, [0, F(1, 2), 0], 0)
    return result


def integer_kernel_and_exact_polar_checks():
    rng = np.random.default_rng(2026102102)
    kernel_cases = 0
    for n in range(1, 9):
        for k in sorted({1, n}):
            raw = rng.integers(-1000, 1001, size=(n, n), dtype=np.int64)
            ai = csr_matrix(raw + raw.T)
            vi = rng.integers(-10000, 10001, size=(n, k), dtype=np.int64)
            diag = rng.integers(-1000, 1001, size=k, dtype=np.int64)
            off = rng.integers(1, 1000, size=k - 1, dtype=np.int64)
            er.check_int64_dot_bounds(ai, vi, diag, off)
            j = np.diag(diag) + np.diag(off, 1) + np.diag(off, -1)
            need(np.array_equal((ai @ vi).astype(object), ai.toarray().astype(object) @ vi.astype(object)),
                 "sparse integer kernel differs from Python arbitrary precision")
            need(np.array_equal((vi.T @ vi).astype(object), vi.astype(object).T @ vi.astype(object)),
                 "Gram kernel differs from Python arbitrary precision")
            vj = vi * diag[None, :]
            if k > 1:
                vj[:, 1:] += vi[:, :-1] * off[None, :]
                vj[:, :-1] += vi[:, 1:] * off[None, :]
            need(np.array_equal(vj.astype(object), vi.astype(object) @ j.astype(object)),
                 "tridiagonal kernel differs from Python arbitrary precision")
            kernel_cases += 1

    near = (1 << 33) - 1
    ai = csr_matrix(np.diag([near, -near]).astype(np.int64))
    vi = np.eye(2, dtype=np.int64) * er.VD
    er.check_int64_dot_bounds(ai, vi, [near, -near])
    need(np.array_equal((ai @ vi).astype(object), ai.toarray().astype(object) @ vi.astype(object)),
         "near-limit product mismatch")
    overflow = {
        "operator_product": rejected(er.check_int64_dot_bounds,
            csr_matrix(np.array([[(1 << 34)]], dtype=np.int64)),
            np.array([[er.VD]], dtype=np.int64), [0]),
        "residual_subtraction": rejected(er.check_int64_dot_bounds,
            csr_matrix(np.array([[(1 << 33)]], dtype=np.int64)),
            np.array([[er.VD]], dtype=np.int64), [-(1 << 33)]),
        "gram_product": rejected(er.check_int64_dot_bounds,
            csr_matrix((1, 1), dtype=np.int64), np.array([[(1 << 32)]], dtype=np.int64), [0]),
        "cancellation_does_not_waive_guard": rejected(er.check_int64_dot_bounds,
            csr_matrix(np.array([[(1 << 34), -(1 << 34)], [-(1 << 34), (1 << 34)]], dtype=np.int64)),
            np.array([[er.VD], [er.VD]], dtype=np.int64), [0]),
    }

    # The last omitted coupling is allowed by the Lanczos recurrence and must
    # not be charged as a first-column residual.
    aint = np.array([[er.AD // 8, er.AD // 16, 0],
                     [er.AD // 16, -er.AD // 8, 3 * er.AD // 32],
                     [0, 3 * er.AD // 32, er.AD // 4]], dtype=np.int64)
    ai = csr_matrix(aint)
    vi = np.eye(3, dtype=np.int64)[:, :2] * er.VD
    diag, off = [er.AD // 8, -er.AD // 8], [er.AD // 16]
    cert = er.certify_krylov(ai, vi, diag, off, np.array([1, 0, 0], dtype=np.int64), 1, 0)
    for key in ("gamma", "polar_distance", "r0", "r", "xi", "z", "completion_error", "start0"):
        need(q(cert, key) == 0, f"exact retained recurrence incorrectly charged {key}")

    exact_cases = 0
    # Column-scaled coordinate frames have exactly known polar factor Q=[e1,e2].
    # Every post-polar residual in this test is a rational number.
    for offsets in ((1, -1), (7, -12), (-er.VD // 2, er.VD // 4)):
        vi = np.eye(3, dtype=np.int64)[:, :2] * er.VD
        vi[0, 0] += offsets[0]
        vi[1, 1] += offsets[1]
        gi = np.array([3, -4, 0], dtype=np.int64)
        cert = er.certify_krylov(ai, vi, diag, off, gi, 7, 0)
        gram_squared = sum(F(int(vi[i, i])**2 - er.VD**2, er.VD**2)**2 for i in range(2))
        need(q(cert, "gamma")**2 >= gram_squared, "Gram budget below exact Frobenius norm")
        distance_squared = sum(F(o, er.VD)**2 for o in offsets)
        need(q(cert, "polar_distance")**2 >= distance_squared, "polar Frobenius distance failed")
        start_squared = (F(int(vi[0, 0]), er.VD) - F(3, 5))**2 + F(4, 5)**2
        need(q(cert, "start0")**2 >= start_squared, "exact intended-probe distance failed")
        need(q(cert, "probe_norm2") == F(25, 49), "intended probe denominator was not respected")
        need(q(cert, "r") >= 0 and q(cert, "z") >= 0, "negative polar residual budget")
        exact_cases += 1
    return {"python_integer_kernel_cases": kernel_cases + 1,
            "overflow_rejections": overflow, "exact_polar_cases": exact_cases,
            "allowed_last_coupling": "3/32 with zero completion error"}


def small_polar_diagnostics():
    rng = np.random.default_rng(2026102103)
    excess = {key: -float("inf") for key in ("gamma", "polar_distance", "r", "z", "start0", "start_effect")}
    count = 0
    for n in (2, 4, 7, 10):
        for k in sorted({1, min(3, n), n}):
            for unused in range(3):
                raw = rng.normal(size=(n, n))
                a = (raw + raw.T) * (0.01 / n)
                aint = np.rint(a * er.AD).astype(np.int64)
                ai = csr_matrix(aint)
                a = aint.astype(float) / er.AD
                basis, _ = np.linalg.qr(rng.normal(size=(n, k)), mode="reduced")
                vi = np.rint((basis + rng.normal(size=(n, k)) * 0.0002) * er.VD).astype(np.int64)
                diag = np.rint(rng.normal(size=k) * 0.01 * er.AD).astype(np.int64)
                off = np.rint(rng.uniform(0.001, 0.01, size=k - 1) * er.AD).astype(np.int64)
                gi = rng.integers(-100, 101, size=n, dtype=np.int64)
                cert = er.certify_krylov(ai, vi, diag, off, gi, 17, F(1, 10**12))
                v = vi.astype(float) / er.VD
                g = v.T @ v
                vals, vecs = np.linalg.eigh(g)
                polar = v @ ((vecs / np.sqrt(vals)) @ vecs.T)
                j = (np.diag(diag) + np.diag(off, 1) + np.diag(off, -1)).astype(float) / er.AD
                intended = gi.astype(float) / np.linalg.norm(gi.astype(float))
                values = {
                    "gamma": np.linalg.norm(g - np.eye(k), "fro"),
                    "polar_distance": np.linalg.norm(polar - v, "fro"),
                    "r": np.linalg.norm((a @ polar - polar @ j)[:, :-1], "fro"),
                    "z": abs(j[-1, -1] - polar[:, -1] @ a @ polar[:, -1]),
                    "start0": np.linalg.norm(v[:, 0] - intended),
                    "start_effect": np.sqrt(max(0.0, 1 - (intended @ polar[:, 0])**2)),
                }
                for key, value in values.items():
                    budget = float(q(cert, "start_error" if key == "start_effect" else key))
                    excess[key] = max(excess[key], float(value - budget))
                    need(value <= budget + 2e-12, "floating polar diagnostic exceeded exact budget: " + key)
                count += 1
    return {"cases": count, "max_measured_minus_certified": excess,
            "diagnostic_tolerance": 2e-12,
            "scope": "Floating eigendecomposition is diagnostic only; exact checker and algebra supply the guarantee."}


def main():
    wall, cpu = time.perf_counter(), time.process_time()
    sections = {}
    for name, fn in (("scalar_exact", exact_scalar_checks),
                     ("source_exact", exact_loader_checks),
                     ("malformed_rejections", malformed_input_checks),
                     ("integer_and_exact_polar", integer_kernel_and_exact_polar_checks),
                     ("floating_polar_diagnostics", small_polar_diagnostics)):
        st, sc = time.perf_counter(), time.process_time()
        sections[name] = fn()
        sections[name]["wall_seconds"] = time.perf_counter() - st
        sections[name]["cpu_seconds"] = time.process_time() - sc
    receipt = {"status": "PASS", "checker_sha256": hashlib.sha256(Path(er.__file__).read_bytes()).hexdigest(),
               "test_source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
               "sections": sections, "wall_seconds": time.perf_counter() - wall,
               "cpu_seconds": time.process_time() - cpu, "peak_rss_bytes": er.rss_bytes(),
               "python_optimize": sys.flags.optimize,
               "scope": "Independent bounded input, arithmetic, overflow and polar-budget challenge; not a full-matrix experiment."}
    output = ROOT / "results" / "exact_residual_projection_agent_audit.json"
    output.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
