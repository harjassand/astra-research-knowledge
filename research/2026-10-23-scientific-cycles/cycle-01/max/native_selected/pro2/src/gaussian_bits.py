"""Exact integer-interval Box--Muller probe generation and replay.

The probability model is iid uniform 64-bit words. os.urandom is an
implementation source for those words, not a mathematical proof of entropy.
All transcendental enclosures and coupling-error bounds below use integer
arithmetic. No binary floating-point or Decimal transcendental is trusted.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import random
import resource
import struct
import time

import numpy as np

BITS = 64
N = 1 << BITS
PRECISION = 112
Q = 1 << PRECISION
PROBE_BITS = 40
DENOMINATOR = 1 << PROBE_BITS
LOG_TERMS = 48
TRIG_TERMS = 18
VERSION = "astra-integer-box-muller-v1"


def _ceildiv(a: int, b: int) -> int:
    if b <= 0:
        raise ValueError("positive denominator required")
    return -((-a) // b)


def _ceilsqrt(a: int) -> int:
    if a < 0:
        raise ValueError("nonnegative radicand required")
    q = math.isqrt(a)
    return q + (q * q != a)


def _rat(a: int, b: int = 1) -> tuple[int, int]:
    return a * Q // b, _ceildiv(a * Q, b)


def _add(a, b):
    return a[0] + b[0], a[1] + b[1]


def _neg(a):
    return -a[1], -a[0]


def _sub(a, b):
    return a[0] - b[1], a[1] - b[0]


def _mul(a, b):
    p = (a[0] * b[0], a[0] * b[1], a[1] * b[0], a[1] * b[1])
    return min(p) // Q, _ceildiv(max(p), Q)


def _scale(a, k: int):
    return (a[0] * k, a[1] * k) if k >= 0 else (a[1] * k, a[0] * k)


def _divint(a, k: int):
    return a[0] // k, _ceildiv(a[1], k)


def _fracscale(a, numerator: int, denominator: int):
    lo, hi = _scale(a, numerator)
    return lo // denominator, _ceildiv(hi, denominator)


def _sqrt(a):
    if a[0] < 0:
        raise ValueError("sqrt enclosure has negative lower endpoint")
    return math.isqrt(a[0] * Q), _ceilsqrt(a[1] * Q)


def _atan_inverse(q: int, terms: int = 48):
    # Alternating power series, with an explicit absolute next-term remainder.
    lo = hi = 0
    for k in range(terms):
        term = _rat((-1) ** k, (2 * k + 1) * q ** (2 * k + 1))
        lo += term[0]
        hi += term[1]
    rem = _ceildiv(Q, (2 * terms + 1) * q ** (2 * terms + 1))
    return lo - rem, hi + rem


PI = _sub(_scale(_atan_inverse(5), 16), _scale(_atan_inverse(239), 4))


def _two_atanh(x):
    if not (0 <= x[0] <= x[1] and 3 * x[0] <= Q and x[1] <= _ceildiv(Q, 3)):
        raise ValueError("atanh argument outside the admitted range")
    x2 = _mul(x, x)
    power = x
    total = (0, 0)
    for k in range(LOG_TERMS):
        total = _add(total, _divint(power, 2 * k + 1))
        power = _mul(power, x2)
    total = _scale(total, 2)
    # True x <= 1/3. Sum_{k=L}^inf 2 x^(2k+1)/(2k+1)
    # <= 9/[4(2L+1)3^(2L+1)].
    rem = _ceildiv(9 * Q, 4 * (2 * LOG_TERMS + 1) * 3 ** (2 * LOG_TERMS + 1))
    return total[0], total[1] + rem


LN2 = _two_atanh(_rat(1, 3))


def _log_midpoint(j: int):
    # u=(j+1/2)/2^64 = p/2^65. Reduce u=2^(-k) z, 1<=z<2.
    p = 2 * j + 1
    top = 1 << (p.bit_length() - 1)
    k = BITS + 1 - (p.bit_length() - 1)
    x = _rat(p - top, p + top)
    return _sub(_two_atanh(x), _scale(LN2, k))


def _sin_cos_midpoint(h: int):
    # theta=pi*(2h+1)/2^64. Reduce to |x|<=pi/4 by a nearest pi/2 multiple.
    p = 2 * h + 1
    quadrant = (p + (N >> 2)) // (N >> 1)
    remainder = p - quadrant * (N >> 1)
    x = _fracscale(PI, remainder, N)
    if max(abs(x[0]), abs(x[1])) > Q:
        raise RuntimeError("Taylor argument did not lie in [-1,1]")
    x2 = _mul(x, x)
    k = TRIG_TERMS
    cp = _rat((-1) ** k, math.factorial(2 * k))
    sp = _rat((-1) ** k, math.factorial(2 * k + 1))
    for k in range(TRIG_TERMS - 1, -1, -1):
        cp = _add(_mul(cp, x2), _rat((-1) ** k, math.factorial(2 * k)))
        sp = _add(_mul(sp, x2), _rat((-1) ** k, math.factorial(2 * k + 1)))
    sp = _mul(x, sp)
    cr = _ceildiv(Q, math.factorial(2 * TRIG_TERMS + 2))
    sr = _ceildiv(Q, math.factorial(2 * TRIG_TERMS + 3))
    c = cp[0] - cr, cp[1] + cr
    s = sp[0] - sr, sp[1] + sr
    return [(c, s), (_neg(s), c), (_neg(c), _neg(s)), (s, _neg(c))][quadrant % 4]


def _nearest_dyadic(a):
    # Round the rational centre of the enclosure to denominator 2^40, ties even.
    num = (a[0] + a[1]) * DENOMINATOR
    den = 2 * Q
    q, r = divmod(num, den)
    if 2 * r > den or (2 * r == den and q % 2):
        q += 1
    fixed_value = q * (Q // DENOMINATOR)
    error = max(abs(a[0] - fixed_value), abs(a[1] - fixed_value))
    if not -(1 << 63) <= q < (1 << 63):
        raise OverflowError("probe numerator does not fit int64")
    return q, error


def _pair(j: int, h: int):
    if not (0 < j < N and 0 <= h < N):
        raise ValueError("radial cell j=0 is excluded; both words must be uint64")
    radial = _sqrt(_scale(_log_midpoint(j), -2))
    cosine, sine = _sin_cos_midpoint(h)
    x = _mul(radial, cosine)
    y = _mul(radial, sine)
    xi, ex = _nearest_dyadic(x)
    yi, ey = _nearest_dyadic(y)

    # U lies in [j/N,(j+1)/N]. A universal Holder bound handles the cell at 1:
    # |sqrt(-2ln U)-sqrt(-2ln U0)| <= sqrt(1/j).
    radial_cell = _ceilsqrt(_ceildiv(Q * Q, j))
    # Sharper derivative bound for b=(j+1)/N<1, using -ln b >= 1-b.
    b_gap = N - j - 1
    if b_gap:
        rmin_lower = math.isqrt((2 * b_gap * Q * Q) // N)
        if rmin_lower:
            derivative_bound = _ceildiv(Q * Q, 2 * j * rmin_lower)
            radial_cell = min(radial_cell, derivative_bound)
    # The angular midpoint error is <=pi/N, and the unit circle is 1-Lipschitz.
    angular_cell = _ceildiv(radial[1] * PI[1], N * Q)
    cell_error = radial_cell + angular_cell
    pair_midpoint_error = _ceilsqrt(ex * ex + ey * ey)
    return (xi, yi), cell_error + pair_midpoint_error, (cell_error + ex, cell_error + ey)


def _fraction(numerator: int, denominator: int):
    d = math.gcd(numerator, denominator)
    return {"numerator": str(numerator // d), "denominator": str(denominator // d)}


class ProbeGenerationFailure(RuntimeError):
    pass


def _construct(raw: bytes, n: int, s: int, source: str):
    if n < 1 or s < 1:
        raise ValueError("n and s must be positive")
    count = n * s
    pairs = (count + 1) // 2
    if len(raw) != 16 * pairs:
        raise ValueError("incorrect bit-source length")
    words = list(struct.iter_unpack("<QQ", raw))
    excluded = [i for i, (j, _) in enumerate(words) if j == 0]
    if excluded:
        raise ProbeGenerationFailure("excluded radial zero cells at pair indices " + repr(excluded))
    out = np.empty(count, dtype=np.int64)
    pair_error_squared = 0
    column_error_squared = [0] * s
    largest_pair_error = 0
    for index, (j, h) in enumerate(words):
        values, bound, components = _pair(j, h)
        pair_error_squared += bound * bound
        largest_pair_error = max(largest_pair_error, bound)
        for component in (0, 1):
            flat_index = 2 * index + component
            if flat_index < count:
                out[flat_index] = values[component]
                column_error_squared[flat_index % s] += components[component] ** 2
    out = out.reshape(n, s)
    global_radius = _ceilsqrt(pair_error_squared)
    column_radii = [_ceilsqrt(x) for x in column_error_squared]
    column_norm_squares = [sum(int(x) ** 2 for x in out[:, j]) for j in range(s)]
    norm_scale = (Q // DENOMINATOR) ** 2
    column_norm_lowers = [math.isqrt(x * norm_scale) for x in column_norm_squares]
    global_norm_lower = math.isqrt(sum(column_norm_squares) * norm_scale)
    if global_norm_lower == 0 or any(x == 0 for x in column_norm_lowers):
        raise ProbeGenerationFailure("stored probe block has a zero column norm")
    cert = {
        "schema": VERSION,
        "n": n,
        "s": s,
        "pair_count": pairs,
        "flattening": "row-major n-by-s; columns are probes",
        "source": source,
        "source_model": "iid independent uniform 64-bit words; entropy assumption is not verified by replay",
        "continuous_coupling": "independent uniforms in the saved bit cells, followed by ideal Box-Muller",
        "probe_denominator": str(DENOMINATOR),
        "interval_precision_bits": PRECISION,
        "log_terms": LOG_TERMS,
        "trig_terms": TRIG_TERMS,
        "bits_sha256": hashlib.sha256(raw).hexdigest(),
        "probe_ints_raw_le_sha256": hashlib.sha256(out.astype("<i8", copy=False).tobytes()).hexdigest(),
        "excluded_radial_zero_cell_count": 0,
        "exception_probability_upper": _fraction(pairs, N),
        "excluded_cell_failure_bound": _fraction(pairs, N),
        "frobenius_radius_numerator": str(global_radius),
        "frobenius_radius_denominator": str(Q),
        "normalized_cdf_slack": _fraction(min(global_radius, global_norm_lower), global_norm_lower),
        "global_normalized_cdf_slack": _fraction(min(global_radius, global_norm_lower), global_norm_lower),
        "column_frobenius_radii": [_fraction(x, Q) for x in column_radii],
        "column_cdf_slacks": [_fraction(min(r, q), q) for r, q in zip(column_radii, column_norm_lowers)],
        "per_column_normalized_cdf_slack": [_fraction(min(r, q), q) for r, q in zip(column_radii, column_norm_lowers)],
        "largest_pair_error": _fraction(largest_pair_error, Q),
        "norm_lower_numerator": str(global_norm_lower),
        "norm_lower_denominator": str(Q),
        "pi_interval_numerators": [str(PI[0]), str(PI[1])],
        "ln2_interval_numerators": [str(LN2[0]), str(LN2[1])],
        "constants_denominator": str(Q),
        "randomness_status": "deterministic fixture only; no statistical coverage claimed" if source.startswith("fixture:") else "statistical coverage conditional on the stated iid-bit model",
    }
    return out, cert


def generate_probe_block(n: int, s: int, directory, *, seed=None):
    """Persist bits once, then return (int64 probes, 2**40, certificate).

    Existing bit/probe/certificate files are never overwritten or redrawn.
    A supplied seed is an explicitly non-probabilistic deterministic fixture.
    """
    start_wall, start_cpu = time.perf_counter(), time.process_time()
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    paths = [directory / x for x in ("gaussian_bits.bin", "gaussian_probe_ints.npy", "gaussian_probe_certificate.json")]
    if any(p.exists() for p in paths):
        raise FileExistsError("probe files already exist; verify them instead of redrawing")
    pairs = (n * s + 1) // 2
    if seed is None:
        raw = os.urandom(16 * pairs)
        source = "os.urandom"
    else:
        rng = random.Random(seed)
        raw = b"".join(struct.pack("<QQ", rng.getrandbits(BITS), rng.getrandbits(BITS)) for _ in range(pairs))
        source = "fixture:" + str(seed)
    with paths[0].open("xb") as f:
        f.write(raw)
    try:
        probes, cert = _construct(raw, n, s, source)
    except ProbeGenerationFailure as exc:
        failure = {"schema": VERSION, "status": "generation_failed_no_redraw", "reason": str(exc), "n": n, "s": s,
                   "bits_sha256": hashlib.sha256(raw).hexdigest(), "exception_probability_upper": _fraction(pairs, N)}
        paths[2].write_text(json.dumps(failure, indent=2) + "\n")
        raise
    with paths[1].open("xb") as f:
        np.save(f, probes, allow_pickle=False)
    cert["probe_file_sha256"] = hashlib.sha256(paths[1].read_bytes()).hexdigest()
    cert["generation_resources"] = {"wall_seconds": time.perf_counter() - start_wall,
                                    "cpu_seconds": time.process_time() - start_cpu,
                                    "peak_process_rss_bytes_linux": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024}
    paths[2].write_text(json.dumps(cert, indent=2) + "\n")
    return probes, DENOMINATOR, cert


def verify_probe_block(directory, *, expected_n=None, expected_s=None, expected_bits_sha256=None):
    """Replay all exact interval calculations; optionally pin receiving identity."""
    start_wall, start_cpu = time.perf_counter(), time.process_time()
    directory = Path(directory)
    cert = json.loads((directory / "gaussian_probe_certificate.json").read_text())
    if cert.get("schema") != VERSION or "status" in cert:
        raise ValueError("unsupported or unsuccessful probe certificate")
    n, s = cert["n"], cert["s"]
    if expected_n is not None and n != expected_n:
        raise ValueError("n disagrees with receiver contract")
    if expected_s is not None and s != expected_s:
        raise ValueError("s disagrees with receiver contract")
    raw = (directory / "gaussian_bits.bin").read_bytes()
    if expected_bits_sha256 is not None and hashlib.sha256(raw).hexdigest() != expected_bits_sha256:
        raise ValueError("bits disagree with receiver-pinned identity")
    reproduced, expected = _construct(raw, n, s, cert["source"])
    file_bytes = (directory / "gaussian_probe_ints.npy").read_bytes()
    if hashlib.sha256(file_bytes).hexdigest() != cert["probe_file_sha256"]:
        raise ValueError("probe file digest mismatch")
    supplied = np.load(directory / "gaussian_probe_ints.npy", allow_pickle=False)
    if supplied.dtype != np.dtype("int64") or supplied.shape != (n, s) or not np.array_equal(supplied, reproduced):
        raise ValueError("stored dyadic probes differ from exact replay")
    for key, value in expected.items():
        if cert.get(key) != value:
            raise ValueError("certificate field differs from replay: " + key)
    return {"status": "PASS", "schema": VERSION, "n": n, "s": s,
            "bits_sha256": expected["bits_sha256"],
            "external_bits_identity_pinned": expected_bits_sha256 is not None,
            "replay_scope": "exact integer enclosures and data binding; not verification of source entropy",
            "wall_seconds": time.perf_counter() - start_wall,
            "cpu_seconds": time.process_time() - start_cpu,
            "peak_process_rss_bytes_linux": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=["generate", "verify"])
    parser.add_argument("directory")
    parser.add_argument("--n", type=int)
    parser.add_argument("--s", type=int)
    parser.add_argument("--seed", type=int)
    parser.add_argument("--expected-bits-sha256")
    args = parser.parse_args()
    if args.operation == "generate":
        if args.n is None or args.s is None:
            parser.error("generate requires --n and --s")
        _, _, result = generate_probe_block(args.n, args.s, args.directory, seed=args.seed)
    else:
        result = verify_probe_block(args.directory, expected_n=args.n, expected_s=args.s,
                                    expected_bits_sha256=args.expected_bits_sha256)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
