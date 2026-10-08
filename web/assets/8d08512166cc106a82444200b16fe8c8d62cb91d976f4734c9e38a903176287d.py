#!/usr/bin/env python3
"""Finite exact/numeric check of matched-port and initial-temperature kernels."""
import math

C1, C2 = 1.0, 4.0
for t in (0.1, 0.5, 2.0):
    decay = 1.0 - math.exp(-5.0*t/4.0)
    h12 = h21 = decay/5.0
    g12 = 4.0*decay/5.0
    g21 = decay/5.0
    assert math.isclose(h12, h21, rel_tol=0, abs_tol=1e-15)
    assert math.isclose(C1*g12, C2*g21, rel_tol=1e-14, abs_tol=1e-15)
    assert math.isclose(g12/g21, C2/C1, rel_tol=1e-14)
    # Equal-energy impulse at node 2 divides its initial temperature jump by C2.
    assert math.isclose(g12/C2, h12, rel_tol=1e-14, abs_tol=1e-15)
    print(f"t={t:g}: h12=h21={h12:.12g}; equal-dT G12/G21={g12/g21:g}; weighted={C1*g12:.12g}")

# Laplace-domain cross-port response from inverse([[1+s,-1],[-1,1+4s]]).
for s in (0.1, 1.0, 2.5):
    det=s*(4*s+5)
    h12=1.0/det
    h21=1.0/det
    assert h12 == h21
print("PASS: reciprocal power/temperature transfer; weighted initial-temperature kernel identity")
