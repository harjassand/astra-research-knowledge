#!/usr/bin/env python3
"""Reproduce the finite-block selected-entry failure and the repaired bound."""
from math import sqrt

# The exact bad 3x3 example from the N175 proof's retained failure.
delta, D, rho = 1.0, 1e6, 0.1
selected = delta * D ** (-3 / 4)
cross_column = -rho * delta
F = selected + cross_column
op_norm = delta * sqrt(D ** (-3 / 2) + 1)  # E is one nonzero row.
print("selected-entry toy")
print(f"selected={selected:.10g}, cross_column={cross_column:.10g}, F={F:.10g}")
print(f"||E||_2={op_norm:.10g} (< 2 delta = {2*delta:g})")
assert selected > 0 and F < 0 and op_norm < 2 * delta

# A conservative dimension-aware bound for the repaired local expansion.
p, C, b, rho, eps = 4, 3.0, 1.0, 0.01, 0.01
q = sqrt(p - 1) * rho
err = C*q + eps*(1+q) + rho*C*(1+q) + rho*eps*(1+q)
print("\nfull-matrix repair bound, normalized by a")
print(f"p={p}, C={C}, b={b}, rho={rho}, eps={eps}")
print(f"worst-case |F/a - z B_21| <= {err:.10g}; signed leading margin b={b:g}")
assert err < b
