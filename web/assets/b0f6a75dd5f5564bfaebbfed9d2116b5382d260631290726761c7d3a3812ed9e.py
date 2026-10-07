"""Exact algebra audit for the component-weight counterexample.

The script checks only the volume-weight and power formulas. The dynamical
entropy inputs are imported as exact, already-derived Sol/translation facts
from the baseline proof and are stated explicitly in INITIAL.txt.
"""
import sympy as sp

Vs, V0, L, nu, a = sp.symbols("V_s V_0 L nu a", positive=True)
V = Vs + L**3 * V0
p = Vs / V
H = sp.simplify(p * a)
W = 4 * nu * Vs * a**2
rhs_volume = sp.simplify(4 * nu * V * H**2)
rhs_topological_lower = 4 * nu * V * a**2

assert sp.simplify(H - Vs * a / V) == 0
assert sp.factor(W - rhs_volume) == 4 * nu * Vs * a**2 * L**3 * V0 / V
assert sp.factor(W - rhs_topological_lower) == -4 * nu * a**2 * L**3 * V0
assert sp.simplify(W / V - 4 * nu * p * a**2) == 0

print("component mass p = V_s/(V_s + L^3 V_0)")
print("volume entropy H = p a")
print("power W = 4 nu V_s a^2")
print("claimed volume-entropy RHS = 4 nu V_s^2 a^2/(V_s + L^3 V_0)")
print("W - volume-entropy RHS = 4 nu V_s a^2 L^3 V_0/(V_s + L^3 V_0) > 0")
print("W - topological-entropy RHS (using h_top >= a) = -4 nu a^2 L^3 V_0 < 0")
print("normalized power W/V = 4 nu p a^2 -> 0 as L -> infinity")
