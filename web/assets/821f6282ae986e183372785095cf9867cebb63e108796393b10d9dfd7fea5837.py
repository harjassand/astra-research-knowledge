"""Exact scalar checks for the variance-dual counterattack note.

This script checks the dimension-symbolic equalities used for the full
traceless frame and the universal 1->2 cloner. It does not optimize over
channels, search for a counterexample, or certify the all-Q inequality.
Run with Python 3 and SymPy 1.14.
"""

import sympy as sp


d = sp.symbols("d", integer=True, positive=True)
r = d**2 - 1
lam_cloner = sp.Rational(1, 2) * (d + 2) / (d + 1)
beta_full_frame = d * (d - 1)
support_full_frame = d - 1

# For a tau-orthonormal basis of traceless Hermitians, Q=I_H0 has trace r.
# The pure-state variance infimum is beta=d(d-1), so the variance dual has
# normalized-trace cost r-beta=d-1. The Haar rank-one POVM attains this.
assert sp.simplify(r - beta_full_frame - support_full_frame) == 0

# The universal symmetric cloner marginal is lambda_cloner on H0; its
# factor-two target 2 Phi-I has eigenvalue 1/(d+1), and its Dirichlet trace
# equals beta/2. This is an exact equality control, not a counterexample.
assert sp.simplify(2 * lam_cloner - 1 - 1 / (d + 1)) == 0
assert sp.simplify(r * (1 - lam_cloner) - beta_full_frame / 2) == 0
assert sp.simplify(2 * r * lam_cloner - r - support_full_frame) == 0

for dimension in range(2, 13):
    assert sp.simplify((r - beta_full_frame - support_full_frame).subs(d, dimension)) == 0
    assert sp.simplify((r * (1 - lam_cloner) - beta_full_frame / 2).subs(d, dimension)) == 0

print("symbolic_dimension", d)
print("full_traceless_rank", r)
print("full_frame_variance_gap", beta_full_frame)
print("full_frame_support", support_full_frame)
print("cloner_H0_eigenvalue", lam_cloner)
print("cloner_target_2Phi_minus_I_eigenvalue", sp.simplify(2 * lam_cloner - 1))
print("cloner_Dirichlet_trace_equals_beta_over_2", sp.simplify(r * (1 - lam_cloner)))
print("all_exact_identities_passed_for_integer_dimensions_2_to_12")
