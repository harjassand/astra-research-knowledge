#!/usr/bin/env python3
"""Reproduce the exact K12 log-concavity and Hurwitz obstructions."""
import json
from pathlib import Path
import sympy as sp
from check_shape import coefficients, graph

a = coefficients(graph(12, [1] * 66))
assert a == [1, 66, 4455, 207900, 5457375, 58939650, 108056025]
assert a[1] ** 2 < a[0] * a[2]
c = list(reversed(a))
H = sp.Matrix(6, 6, lambda i, j: c[2*j-i+1]
              if 0 <= 2*j-i+1 < len(c) else 0)
minors = [int(H[:k, :k].det()) for k in range(1, 7)]
assert minors[4] == -808578408339264245760000
out = {
    "K12_coefficients": a,
    "a1_squared": a[1] ** 2,
    "a0_times_a2": a[0] * a[2],
    "Hurwitz_matrix": [[int(x) for x in H.row(i)] for i in range(6)],
    "Hurwitz_leading_minors": minors,
}
Path(__file__).with_name("exact_certificates.json").write_text(
    json.dumps(out, indent=2) + "\n")
print("PASS: K12 violates ordinary log-concavity and Hurwitz stability.")
