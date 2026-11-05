# Separately audited extension: projected-Y formulation

Status: provisional mathematical extension, separately checked by the first internal adversarial auditor (INDEPENDENT_REVIEW.md), but not formally or externally verified. The second and third auditors did not review this extension; their reviews of the unrestricted theorem are not additional endorsements of this document. This does not assert equality of unrestricted and restricted optima at a fixed level.

For the natural Eq. (17) nearest-neighbor objective, use n>=3; its n=2 truncation is not a valid general gap lower bound. Rai Appendix D Eq. (115)-(116) replaces Y by Q_(n-1)YQ_(n-1), where Q_(n-1) is the complement of the open-chain ground projector. Its dual has

    rho_n >= 0,
    Tr rho_n h_1 = 1,
    Q_(n-1) [Tr_1 rho_n - Tr_n rho_n] Q_(n-1) = 0.

This is weaker than full LTI. Nevertheless, every observable h_i, h_i^2, and {h_i,h_j} contained in n-1 sites annihilates the open-chain ground space on both sides. Therefore O=Q_(n-1) O Q_(n-1), and the projected marginal equality gives the one-step translation identity for every energy moment used in the completeness proof. Iterating gives every fitting translated first and second moment. A pair already spanning all n sites has only one placement and needs no translation identity.

The proof in PROOF_CANDIDATE.md uses no other consequence of full LTI. Thus it applies to these restricted-dual feasible operators as well. The positive-definite identity witness gives strict dual Slater feasibility, and the open-chain second-moment bound makes the dual infimum finite. The same nearly-optimal-witness argument is valid.

## Literal indexing difference in the source

Eq. (17) sums j=2,...,n-1. By contrast the printed general-range expressions in Appendix D use j<1+n-k. With nearest-neighbor k=2, the literal sum ends at n-2. These formulas differ by one level, and this must not be hidden.

For the literal Appendix D version, require n>=4 and put L=n-1>=3 and sigma_L=Tr_last rho_n. Its objective is exactly the natural L-site objective h_1^2+sum_(j=2)^(L-1){h_1,h_j}. The projected marginal condition on rho_n supplies all required translated first and second energy moments on sigma_L. Apply the ground-space projection and boundary repair on these L sites. This yields

    gamma_cert,n >= Delta_(n-1) - O(sqrt(log n/n)).

Telescoping of its primal still provides gamma_cert,n <= Delta_N for all sufficiently large N. Together these force convergence to the same periodic thermodynamic limit. Monotonicity of the restricted hierarchy is unnecessary for this conclusion. If one uses the Eq. (17) indexing with projected Y instead, the lower comparison is with Delta_n rather than Delta_(n-1).

## Relation to a further reduced hierarchy

The same observation suggests enforcing only translation invariance of the needed energy moments, rather than the full projected marginal equality. This gives a polynomial number of linear constraints and a primal divergence in the span of h_i, h_i^2, and {h_i,h_j}. It still retains a d^n-dimensional PSD cone. Its convergence is a corollary of the moment-based proof, but practical performance and the precise relationship to earlier low-parameter quadratic gap criteria require separate study. No practical advantage is established here.
