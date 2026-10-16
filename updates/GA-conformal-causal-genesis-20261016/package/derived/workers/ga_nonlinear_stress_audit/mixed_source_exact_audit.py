#!/usr/bin/env python3
"""Exact receiving audit of the reserve-floor falsifier; standard library only."""
from pathlib import Path
from fractions import Fraction as F
from math import factorial
import hashlib
import json
from exact_audit import variable, add, mul, powp, scale, deriv, j1

HERE = Path(__file__).resolve().parent
INPUT = HERE.parent / "ga_sharp_invention/MIXED_SOURCE_CONTINUATION.md"
checks = []


def check(name, condition, detail=None):
    if not condition:
        raise RuntimeError("FAILED: " + name)
    checks.append({"name": name, "status": "PASS", "detail": detail})


def circular_moment(m, n=0):
    if m % 2 or n % 2:
        return F(0)
    p, q = m // 2, n // 2
    return F(factorial(2 * p) * factorial(2 * q),
             4 ** (p + q) * factorial(p) * factorial(q) * factorial(p + q))


def phase_average(poly, extra_sin_power=0):
    # f=sin(x+y),g=-sin(x+y): a=b=cos(x+y),c=d=-cos(x+y).
    out = {}
    for (ka, kb, kc, kd, ks), v in poly.items():
        val = v * (-1) ** (kc + kd) * circular_moment(ka + kb + kc + kd, extra_sin_power)
        out[ks] = out.get(ks, F(0)) + val
    return {k: v for k, v in out.items() if v}


def main():
    a, b, c, d, s = [variable(i) for i in range(5)]
    sigma1 = add(scale(mul(powp(s, 2), b), -3), scale(powp(b, 3), F(1, 2)))
    sigma2 = add(scale(powp(s, 3), 3), scale(mul(powp(s, 2), a), 7),
                 scale(mul(s, powp(a, 2)), 5), scale(powp(a, 3), F(1, 2)))
    pairing = add(mul(sigma1, c), mul(sigma2, d))
    gap = add(j1(add(a, s), b, c, add(d, s)), scale(powp(s, 4), -2))
    G = add(gap, scale(mul(powp(s, 3), a), -5), scale(pairing, -1))
    W = add(deriv(sigma1, 1), deriv(sigma2, 0))
    source = phase_average(W, extra_sin_power=2)  # g*f_xy=sin(x+y)^2
    stress = phase_average(pairing)
    check("phase field is rank-one valued", phase_average(add(mul(a, d), scale(mul(b, c), -1))) == {})
    check("exact source X_s", source == {2: F(2), 0: F(3, 8)})
    check("exact stress pairing is minus source", stress == {k: -v for k, v in source.items()})
    check("exact target Jensen energy", phase_average(gap) == {2: F(1), 0: F(3, 4)})
    check("exact full reserve", phase_average(G) == {2: F(3), 0: F(9, 8)})
    gradient_quadratics = [mul(x, y) for i, x in enumerate([a, b, c, d]) for y in [a, b, c, d][i:]]
    M4 = add(*[powp(x, 2) for x in gradient_quadratics])
    R = add(powp(a, 2), powp(c, 2), powp(d, 2))
    check("exact M4 mean", phase_average(M4) == {0: F(15, 4)})
    check("exact R mean", phase_average(R) == {0: F(3, 2)})
    floor = phase_average(scale(add(M4, mul(powp(s, 2), R)), F(1, 128)))
    difference = {k: source.get(k, F(0)) - floor.get(k, F(0)) for k in set(source) | set(floor)}
    check("source exceeds floor for every real s", difference == {2: F(509, 256), 0: F(177, 512)})
    check("G homogeneous quartic gives exact compact scaling", all(sum(k) == 4 for k in G))
    check("mixed-source concentration exponent vanishes", F(2) + F(1, 2) - F(1) - F(3, 2) == 0)
    check("quartic concentration exponent vanishes", F(2) - 4 * F(1, 2) == 0)
    check("quadratic-background concentration exponent vanishes", F(2) - 2 * F(1, 2) - 2 * F(1, 2) == 0)
    receipt = {"schema": "independent-mixed-source-continuation-audit/1", "status": "PASS",
               "scope": "Exact reserve-floor falsifier and scaling exponents; local-null-stress classification proved in the addendum.",
               "checks": checks,
               "source_minus_floor": {str(k): str(v) for k, v in difference.items()},
               "input_sha256": hashlib.sha256(INPUT.read_bytes()).hexdigest(),
               "self_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
               "own_polynomial_library_sha256": hashlib.sha256((HERE / 'exact_audit.py').read_bytes()).hexdigest()}
    (HERE / "MIXED_SOURCE_AUDIT_RECEIPT.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps({"status": receipt["status"], "checks": len(checks),
                      "source_minus_floor": receipt["source_minus_floor"]}, indent=2))


if __name__ == "__main__":
    main()
