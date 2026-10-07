#!/usr/bin/env python3
"""Integer/Fraction-only verifier for the saved N=72 Hankel witness."""
from fractions import Fraction
from math import comb
from pathlib import Path
import json

CERT = Path(__file__).with_suffix(".json")
# Keep certificate and verifier names paired despite the verifier prefix.
CERT = CERT.with_name("axial_hankel_N72_delta81_50_exact.json")
D_BITS = 256
D = 1 << D_BITS
RANGE_SQUARES = 10
TAYLOR_ODD = 35
TAYLOR_EVEN = 34
N = 72


def floor_f(x: Fraction) -> int:
    return x.numerator // x.denominator


def ceil_f(x: Fraction) -> int:
    return -((-x.numerator) // x.denominator)


def exp_interval(distance: int) -> tuple[int, int]:
    x = Fraction(9 * distance * distance, 400)
    y = x / (1 << RANGE_SQUARES)
    assert y <= Fraction(1, 16)
    term = Fraction(1)
    odd = even = term
    for r in range(1, TAYLOR_ODD + 1):
        term *= -y / r
        odd += term
        if r <= TAYLOR_EVEN:
            even += term
    assert 0 < odd <= even
    lo, hi = floor_f(odd * D), ceil_f(even * D)
    for _ in range(RANGE_SQUARES):
        lo = (lo * lo) // D
        hi = ceil_f(Fraction(hi * hi, D))
    return lo, hi


def main() -> None:
    cert = json.loads(CERT.read_text())
    assert cert["status"] == "CERTIFIED_NEGATIVE"
    assert cert["N"] == N and cert["delta"] == "81/50"
    e = cert["scale_exponents_e_i"]
    z = [Fraction(int(a), int(b)) for a, b in cert["z_rational"]]
    assert len(e) == len(z) == 36 and z[-1] == 1
    v = [z[i] * (1 << e[i]) for i in range(36)]
    coeff = {k: Fraction(0) for k in range(1, N)}
    for i in range(36):
        for j in range(36):
            k = i + j + 1
            coeff[k] += v[i] * v[j] / comb(N, k)

    cache = {d: exp_interval(d) for d in range(36)}
    lo_total = hi_total = 0
    for k in range(1, N):
        c = coeff[k]
        if not c:
            continue
        lo, hi = cache[abs(k - 36)]
        if c > 0:
            lo_total += floor_f(c * lo)
            hi_total += ceil_f(c * hi)
        else:
            lo_total += floor_f(c * hi)
            hi_total += ceil_f(c * lo)

    recorded = [int(x) for x in cert["quadratic_interval_scaled_numerators"]]
    assert [lo_total, hi_total] == recorded
    assert hi_total < 0
    assert Fraction(hi_total, D) < Fraction(-1, 3000)
    print("PASS: exact rational replay proves v^T(H1/72!)v in")
    print(f"[{lo_total}/{D}, {hi_total}/{D}] < -1/3000")
    print("No floating-point operation is used by this verifier.")


if __name__ == "__main__":
    main()
