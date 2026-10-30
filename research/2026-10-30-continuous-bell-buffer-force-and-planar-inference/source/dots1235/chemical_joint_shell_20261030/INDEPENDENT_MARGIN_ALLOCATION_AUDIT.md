# Independent audit: finite head-margin allocation

Reviewed 2026-10-30. Source: `FINITE_HEAD_MARGIN_ALLOCATION_PRINCIPLE.md`.

The finite max-plus criterion is correct, provided the operator and shift assumptions apply to the new profiles, as specified below. This is a sufficient verification device, not an automatic weak-reversibility sign theorem.

## Algebra and strict cycle feasibility

For R>=0 with positive leading coefficients on its nonzero entries and h_k=s^{a_k}, no leading cancellation occurs in v_i=sum_k R_ik h_k. Its degree is exactly max_k(rho_ik+a_k). If each actual error entry acts on such polynomially weighted terminal data with exponent epsilon_ij, the forcing degree in row i is bounded by max_j,k(epsilon_ij+rho_jk+a_k). Strict separation from a_i absorbs its constant and any subpower factor at sufficiently large s.

Put T_ik=max_j(epsilon_ij+rho_jk), omitting absent contributions, and orient an edge k->i of weight T_ik. Summing a_i>a_k+T_ik around a directed cycle proves necessity of negative cycle weight. Conversely, if all cycles are strictly negative, choose a small positive common edge slack so all cycle sums remain nonpositive (indeed negative). Add a zero-weight super-source edge to every vertex and take longest-path potentials. There is no positive cycle, so these potentials are finite and satisfy the non-strict constraints with the added slack, hence the original strict constraints. If the graph has no cycles, any positive slack works. Raising all a_i by one common constant preserves every difference inequality and meets finitely many running-cost lower bounds.

## Required profile-uniform assumptions

1. Changing the forcing changes v. A shifted-profile comparison checked only for a previous particular inverse vector is insufficient. The comparison must hold for every selected profile R(s)s^a, or be reverified after selection. A fixed nonzero-jump gain slack and positive rational-Puiseux/power profiles provide this in the concrete setting because their fixed-shift ratios tend to one. Exact zero corrected shifts remain exact.

2. A nonlocal return operator can land at an unbounded terminal residual. Therefore a bound in factorial weight phi alone does not justify pulling out the initial factor s^{d_j}. One must require the entrywise error estimate with the same exponent epsilon_ij in every fixed polynomially enlarged weight s^d phi (constants and thresholds may depend on d), or directly require E_ij[phi(.) (1+.)^d](s)<=C_d phi(s)(1+s)^{epsilon_ij+d}. The finite-birth expansion supplies this stronger property; it should be explicit in the abstract contract.

3. The error entries must already incorporate physical head-entry shifts and any source entrance rate powers, as the source states. Otherwise the extra factorial power from a positive entrance shift must be added.

With these requirements, the concrete active/inactive forcing choice is a legitimate example of the criterion's logic. It does not show every coefficient choice or every head has a feasible negative-cycle graph, and failure of this sufficient test does not establish transience.

### Repair verification and final verdict

Re-read the amended source: it now explicitly requires shifted-profile comparison for every newly selected profile and the same error exponent in every fixed polynomially enlarged terminal weight, with an equivalent moment bound. These resolve the two qualifications raised during review. A common upward shift of all forcing exponents may also ensure all profile degrees are nonnegative, if only nonnegative enlargement powers are intended. The finite max-plus sufficient criterion therefore **passes this scoped audit**. No automatic network-level sign or recurrence conclusion follows.

Reviewed source hash:
4b89628958713a3976d3f067676411c4254e53c38a0c08b03cc5db86df26a167  chemical_joint_shell_20261030/FINITE_HEAD_MARGIN_ALLOCATION_PRINCIPLE.md
