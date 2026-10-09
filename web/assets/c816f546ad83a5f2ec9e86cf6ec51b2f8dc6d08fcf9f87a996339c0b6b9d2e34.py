"""Independent exact Fraction Sturm audit of two exposed depth certificates.

No SymPy or originating replay code is used. Inputs are fixed by the
exposed SCALAR_DEPTH_CERTIFICATE: delta=1/100, r=3 or 5.
"""
from fractions import Fraction as F
from functools import reduce
import hashlib
import json
import sys
from math import gcd, lcm
from pathlib import Path


def trim(p):
    p = list(p)
    while p and p[-1] == 0:
        p.pop()
    return p


def primitive(p):
    p = trim(p)
    if not p:
        return p
    den = reduce(lcm, (a.denominator for a in p), 1)
    nums = [a.numerator * (den // a.denominator) for a in p]
    content = reduce(gcd, (abs(a) for a in nums), 0)
    return [F(a // content) for a in nums]  # Positive scaling preserves signs.


def remainder(p, q):
    p = trim(p)
    while p and len(p) >= len(q):
        shift = len(p) - len(q)
        factor = p[-1] / q[-1]
        for j, a in enumerate(q):
            p[j + shift] -= factor * a
        p = trim(p)
    return p


def evaluate(p, x):
    y = F(0)
    for a in reversed(p):
        y = y * x + a
    return y


def variations(sequence, x):
    vals = [evaluate(p, x) for p in sequence]
    signs = [1 if a > 0 else -1 for a in vals if a]
    return sum(a != b for a, b in zip(signs, signs[1:]))


def sturm(p):
    p = primitive(p)
    derivative = primitive([F(i) * p[i] for i in range(1, len(p))])
    seq = [p, derivative]
    while len(seq[-1]) > 1:
        nxt = primitive([-a for a in remainder(seq[-2], seq[-1])])
        if not nxt:
            break
        seq.append(nxt)
    return seq


def polynomial(r, m, gamma):
    p = [F(0)] * max(4, 2 * m + 3)
    for j, a in enumerate([F(2) + gamma, F(-4), F(2)]):
        p[2 * m + j] += F(2**m) * a
    for j, a in enumerate([-(3 + gamma) * (r + 1), 4 * (r + 1), 2 * r * (3 + gamma), -8 * r]):
        p[j] += a
    return trim(p)


gamma = F(1, 800)
lower, upper = (3 + gamma) / 4, F(1)
cases = []
for r, claimed in [(3, 11), (5, 12)]:
    attempts = []
    for m in range(claimed + 1):
        p = polynomial(r, m, gamma)
        seq = sturm(p)
        vl, vu = variations(seq, lower), variations(seq, upper)
        assert vl >= vu
        endpoints = [evaluate(p, lower), evaluate(p, upper)]
        positive = all(a > 0 for a in endpoints)
        roots = vl - vu
        accepted = positive and roots == 0
        assert accepted == (m == claimed)
        assert len(p) - 1 <= max(3, 2 * m + 2)
        if m == 0:
            assert len(p) - 1 == 3 and p[-1] == -8 * r
        attempts.append({
            "m": m, "degree": len(p) - 1,
            "endpoint_values": [str(a) for a in endpoints],
            "sturm_variations": [vl, vu], "distinct_roots_in_interval": roots,
            "accepted": accepted,
            "rational_coefficients_ascending": [str(a) for a in p],
            "primitive_sturm_sequence": [[str(a) for a in z] for z in seq],
        })
    cases.append({"r": r, "delta": "1/100", "gamma": str(gamma),
                  "interval": [str(lower), str(upper)], "depth": claimed,
                  "leaves": 2**claimed, "attempts": attempts})

result = {
    "status": "EXACT_EXPOSED_DEPTH_CERTIFICATES_PASS",
    "scope": "Two fixed exposed interval certificates, independently reconstructed with Fraction Sturm arithmetic",
    "cases": cases,
    "minor_degree_correction": "For m=0, degree is 3; the correct uniform bound is max(3,2m+2)",
    "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
}
out = Path(__file__).with_name("EXPOSED_DEPTH_CERT_AUDIT.json")
if out.exists() and "--write" not in sys.argv:
    assert json.loads(out.read_text()) == result
else:
    out.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({"status": result["status"], "cases": [(r["r"], r["depth"], r["leaves"]) for r in cases], "degree_correction": result["minor_degree_correction"]}, indent=2))
