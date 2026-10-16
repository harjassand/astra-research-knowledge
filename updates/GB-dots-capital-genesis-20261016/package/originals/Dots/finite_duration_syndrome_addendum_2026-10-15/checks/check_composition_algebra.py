#!/usr/bin/env python3
"""Exact symbolic checks; no simulation or physical-realization claim.
Run: python check_composition_algebra.py
"""
import json
import sympy as s

I = s.eye(2)
Z = s.diag(1, -1)
# Basis |memory,bath>: |00>, |01>, |10>, |11>.
V = s.Matrix([[1,0,0,0], [0,1,0,0], [0,0,0,1], [0,0,1,0]])
Z_B = s.kronecker_product(I, Z)
Z_AZ_B = s.kronecker_product(Z, Z)
assert V.H * V == s.eye(4)
assert V * V == s.eye(4)
physical = V.H * Z_B * V
incorrectly_serialized = Z_B * (V.H * V)
assert physical == Z_AZ_B
assert physical != incorrectly_serialized
plus_zero = s.Matrix([1,0,1,0]) / s.sqrt(2)
minus_zero = s.Matrix([1,0,-1,0]) / s.sqrt(2)
assert physical * plus_zero == minus_zero
assert incorrectly_serialized * plus_zero == plus_zero
assert (plus_zero.H * minus_zero)[0] == 0
# Exact trace norm between pure output densities equals 2.
rho_difference = minus_zero * minus_zero.H - plus_zero * plus_zero.H
trace_distance_norm = sum(abs(eigenvalue) * multiplicity
                          for eigenvalue, multiplicity in rho_difference.eigenvals().items())
assert trace_distance_norm == 2

A, B, C, nu, tau, kappa, d = s.symbols('A B C nu tau kappa d', positive=True)
f = A * nu / kappa + B * kappa * tau
k_star = s.sqrt(A * nu / (B * tau))
f_star = 2 * s.sqrt(A * B * nu * tau)
assert s.simplify(s.diff(f, kappa).subs(kappa, k_star)) == 0
assert s.simplify(f.subs(kappa, k_star) - f_star) == 0
assert s.diff(f, kappa, 2) == 2 * A * nu / kappa**3
# Exact global nonnegative square certificate, for every positive kappa.
square = (s.sqrt(A * nu / kappa) - s.sqrt(B * kappa * tau))**2
assert s.simplify(f - f_star - square) == 0
assert s.simplify((f + C*d**2).subs(kappa, k_star) - (f_star+C*d**2)) == 0
# If kappa*tau <= 1 is the only extra constraint:
# k_star is admissible iff A*nu*tau <= B; otherwise f decreases up to 1/tau.
assert s.simplify((k_star*tau)**2 - A*nu*tau/B) == 0
assert s.simplify(f.subs(kappa, 1/tau) - (A*nu*tau+B)) == 0
assert s.simplify(s.diff(f, kappa).subs(kappa, 1/tau) - tau*(B-A*nu*tau)) == 0

# Verify the composed conservative budget algebra exactly.
N, F, D, Cb, x, y, p = s.symbols('N F D Cb x y p', positive=True)
raw = F*y*(Cb+2*x) + N*x*(2*D*(Cb+2*x)+1) + N*p*(Cb+2*x)
upper = F*(Cb+2)*y + N*(2*D*(Cb+2)+1)*x + N*(Cb+2)*p
slack = 2*(1-x)*(F*y+2*N*D*x+N*p)
assert s.simplify(upper-raw-slack) == 0

print(json.dumps({
    'sympy_version': s.__version__,
    'exact_checks_passed': True,
    'physical_echo_matrix': physical.tolist(),
    'incorrect_serialization_matrix': incorrectly_serialized.tolist(),
    'witness_output_trace_norm': str(trace_distance_norm),
    'optimal_rate': str(k_star),
    'unconstrained_minimum': str(f_star),
    'constraint': 'kappa*tau <= 1',
    'optimizer_admissibility': 'A*nu*tau <= B',
    'otherwise_constrained_minimum': 'A*nu*tau+B',
    'budget_upper_minus_raw': str(slack),
}, indent=2, default=str))
