"""Exact 2x2 witness: arbitrary Kraus slicing misses a fixed classical mode."""
import json
import sympy as sp

I = sp.eye(2)
Z = sp.diag(1, -1)
P0 = sp.diag(1, 0)
P1 = sp.diag(0, 1)
P = (P0, P1)

def tau(A):
    return sp.trace(A) / 2

def phi(A):
    return P0 * A * P0 + P1 * A * P1

def canonical(effects, A):
    out = sp.zeros(2)
    for E in effects:
        p = tau(E)
        out += tau(E * A) / p * E
    return sp.simplify(out)

# A full-domain symmetric broadcaster: measure the input in Z and prepare
# the same basis state at both receivers. Its two marginals are phi.
def gamma(A, B):
    return sp.simplify(sum((sp.trace(Q * A) * sp.trace(Q * B) * Q for Q in P), sp.zeros(2)))

assert sp.simplify(gamma(Z, I) - phi(Z)) == sp.zeros(2)
assert sp.simplify(gamma(I, Z) - phi(Z)) == sp.zeros(2)
assert sp.simplify(phi(Z) - Z) == sp.zeros(2)

# Receiver slicing in the pointer basis gives CP branches Lambda_y(A)=Gamma(A⊗P_y),
# effects E_y=phi(P_y), and canonical Psi=phi o pinching o phi=phi.
branch_effects = [gamma(I, Q) for Q in P]
psi_pointer = canonical(branch_effects, Z)
assert psi_pointer == Z

# The same channel also has the random-unitary Kraus family I/sqrt(2), Z/sqrt(2).
# Both effects are I/2; the canonical EB channel is then replacement and loses Z.
random_effects = [I / 2, I / 2]
psi_random = canonical(random_effects, Z)
assert psi_random == sp.zeros(2)

energy = lambda T, H: sp.simplify(tau(H * H) - tau(H * T(H)))
E_phi = energy(phi, Z)
E_psi_random = energy(lambda A: canonical(random_effects, A), Z)
E_psi_pointer = energy(lambda A: canonical(branch_effects, A), Z)
assert E_phi == 0 and E_psi_random == 1 and E_psi_pointer == 0

# Choi witness that the random-unitary branchwise residuals 2 Lambda_y-P_y^EB
# are not CP: J(Id)-J(Tr(.)I/4) has eigenvalues 7/4,-1/4,-1/4,-1/4.
Omega = sp.Matrix([1, 0, 0, 1])
J_id = Omega * Omega.T
J_replace_branch = sp.eye(4) / 4
branch_residual_spectrum = sorted((2 * J_id / 2 - J_replace_branch).eigenvals().keys())
assert branch_residual_spectrum == [-sp.Rational(1, 4), sp.Rational(7, 4)]

print(json.dumps({
    "dimension": 2,
    "field": "exact rationals",
    "channel": "Z dephasing; symmetric measure-copy broadcaster supplied",
    "Phi_Z": str(phi(Z)),
    "random_unitary_effects": [str(E) for E in random_effects],
    "canonical_EB_on_Z_from_random_unitary_effects": str(psi_random),
    "canonical_EB_on_Z_from_broadcaster_pointer_slices": str(psi_pointer),
    "Dirichlet_energy_Phi_Z": str(E_phi),
    "Dirichlet_energy_random_EB_Z": str(E_psi_random),
    "Dirichlet_energy_pointer_EB_Z": str(E_psi_pointer),
    "random_branch_residual_choi_eigenvalues": [str(x) for x in branch_residual_spectrum],
    "status": "arbitrary Kraus basis fails; supplied-broadcaster pointer basis succeeds in this example"
}, indent=2))
