"""Finite arithmetic diagnostic for the CRT field corner; not a general proof."""
import json
from pathlib import Path


def degree(p):
    return p.bit_length() - 1


def divmod_poly(a, b):
    q = 0
    while a and degree(a) >= degree(b):
        shift = degree(a) - degree(b)
        q ^= 1 << shift
        a ^= b << shift
    return q, a


def mul(a, b):
    result = 0
    while b:
        if b & 1:
            result ^= a
        a <<= 1
        b >>= 1
    return result


def mod(a, p):
    return divmod_poly(a, p)[1]


cases = [(1, 0b11), (2, 0b111), (3, 0b1011), (4, 0b10011)]
results = []
for d, f in cases:
    q = 1 << d
    order = q - 1
    modulus = (1 << order) | 1
    h, rem = divmod_poly(modulus, f)
    assert rem == 0
    inv = next(v for v in range(1, q) if mod(mul(h, v), f) == 1)
    e = mod(mul(h, inv), modulus)
    assert mod(mul(e, e), modulus) == e
    embed = lambda v: mod(mul(e, v), modulus)
    images = {embed(v) for v in range(q)}
    assert len(images) == q
    assert embed(1) == e
    for a in range(q):
        for b in range(q):
            assert embed(a ^ b) == embed(a) ^ embed(b)
            assert embed(mod(mul(a, b), f)) == mod(mul(embed(a), embed(b)), modulus)
    results.append({"d": d, "q": q, "cyclic_order": order,
                    "minimal_polynomial_bits": f, "corner_idempotent_bits": e,
                    "field_addition_pairs_checked": q*q,
                    "field_multiplication_pairs_checked": q*q,
                    "status": "FINITE_CHECK_PASSED"})

out = {"scope": "F2 CRT field corner for four specified finite fields only; no group witness or measurable conjugacy tested",
       "results": results}
Path(__file__).with_name("corner_diagnostic.json").write_text(json.dumps(out, indent=2) + "\n")
print(json.dumps(out))
