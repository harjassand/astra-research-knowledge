#!/usr/bin/env python3
"""A fully deterministic small S4 Frobenius-witness fixture.

The polynomial X^4-X-1 has Galois group S4: its reduction at 2 is
irreducible and a reduction with cycle type (3,1) excludes C4 and D4.
The 4-cycle excludes A4. This fixture does not check a zero-free theorem.
"""
from pathlib import Path
from math import isqrt
import json

def trim(f):
    while f and not f[-1]:
        f.pop()
    return f

def remainder(f, g, p):
    f = trim([x % p for x in f])
    while len(f) >= len(g):
        c = f[-1] * pow(g[-1], -1, p) % p
        shift = len(f) - len(g)
        for i, t in enumerate(g):
            f[i + shift] = (f[i + shift] - c * t) % p
        trim(f)
    return f

def gcd(f, g, p):
    f, g = trim([x % p for x in f]), trim([x % p for x in g])
    while g:
        f, g = g, remainder(f, g, p)
    if f:
        inv = pow(f[-1], -1, p)
        f = [v * inv % p for v in f]
    return f

def multiply(f, g, modulus, p):
    product = [0] * max(0, len(f) + len(g) - 1)
    for i, x in enumerate(f):
        for j, y in enumerate(g):
            product[i + j] = (product[i + j] + x * y) % p
    return remainder(product, modulus, p)

def power(f, exponent, modulus, p):
    out = [1]
    while exponent:
        if exponent & 1:
            out = multiply(out, f, modulus, p)
        f = multiply(f, f, modulus, p)
        exponent >>= 1
    return out

def prime(p):
    return p >= 2 and all(p % q for q in range(2, isqrt(p) + 1))

def cycle_type(f, p):
    n = len(f) - 1
    derivative = [i * f[i] % p for i in range(1, len(f))]
    if len(gcd(f, derivative, p)) > 1:
        return None
    y = [0, 1]
    counts, degrees = {}, {}
    for k in range(1, n + 1):
        y = power(y, p, f, p)
        difference = y[:] + [0] * max(0, 2 - len(y))
        difference[1] = (difference[1] - 1) % p
        degree = len(gcd(f, difference, p)) - 1
        degrees[k] = degree
        residual = degree - sum(d * c for d, c in counts.items() if k % d == 0)
        assert residual >= 0 and residual % k == 0
        counts[k] = residual // k
    cycle = tuple(sorted(k for k, c in counts.items() for _ in range(c)))
    assert sum(cycle) == n
    return cycle, degrees

f = [-1, -1, 0, 0, 1]
targets = {(1, 1, 1, 1), (1, 1, 2), (2, 2), (1, 3), (4,)}
found = {}
for p in range(2, 5000):
    if not prime(p):
        continue
    result = cycle_type(f, p)
    if result is None:
        continue
    cycle, degrees = result
    if cycle not in found:
        found[cycle] = {"prime": p, "cycle_type": cycle, "gcd_degrees": degrees}
    if targets <= found.keys():
        break
assert targets <= found.keys()
assert found[(4,)]["prime"] == 2
assert (1, 3) in found
payload = {"status": "finite_fixture_only_not_zero_free_validation",
           "polynomial": "X^4-X-1", "polynomial_discriminant": -283,
           "galois_group": "S4", "first_witnesses": list(found.values())}
Path(__file__).with_name("frobenius_fixture.json").write_text(json.dumps(payload, indent=2) + "\n")
for cycle in sorted(found):
    print(f"cycle {cycle}: ell={found[cycle]['prime']}")
