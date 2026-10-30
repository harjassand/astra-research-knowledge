# Finite head-margin allocation as a max-plus cycle test
Status: new personally derived abstraction of the concrete holey-head construction, unreviewed. This is a verifiable sufficient criterion, not a statement that weak reversibility automatically satisfies it.

Suppose an ACTUAL finite-head surrogate has already earned a shifted-profile comparison using a Metzler Hurwitz matrix G(s), including nonzero-shift slack or exact shifts. Let R(s)=(-G(s))^-1>=0, with finite leading powers rho_ij of its nonzero entries. These powers come from exact finite algebra, not an assumed global Lyapunov function.

The shifted-profile comparison must hold for EVERY new profile R(s)s^a selected below, not only for a previously tested forcing. In the concrete setting, fixed factor-2 slack on nonzero shifts and positive rational-Puiseux/power profiles give this uniformly for each fixed chosen exponent vector; zero corrected shifts remain exact.

Choose positive forcing h_j(s)=s^(a_j), and set v=R h. Positivity prevents leading cancellation, so

    degree v_i = d_i=max_j(rho_ij+a_j).

Suppose the TRUE omitted tail-return operator has an earned entrywise bound with exponent epsilon_ij in EVERY fixed polynomially enlarged weight (1+s)^d phi(s), with factorial/phase entrance shifts included; constants may depend on d. Equivalently its action on terminal (1+s_terminal)^d phi(s_terminal) is bounded by C_d s^(epsilon_ij+d)phi(s). This is essential for nonlocal returns with unbounded terminal residual; a phi-only norm bound is insufficient. The finite-birth renewal estimate supplies precisely this stronger contract. The resulting extra head forcing is at most C s^max_j(epsilon_ij+d_j). It is absorbed by the deliberately selected head margin h_i whenever

    a_i > max_(j,k)(epsilon_ij+rho_jk+a_k).                 (1)

Only rows with actual incoming error are constrained. Running-cost forcing adds inequalities a_i>kappa_i for its earned fixed exponents.

Let T_ik=max_j(epsilon_ij+rho_jk), ignoring absent edges. The strict difference constraints a_i>a_k+T_ik are feasible exactly when every directed cycle of this finite weighted graph has negative total weight. Necessity follows by summing around a cycle. Sufficiency follows by choosing a small common positive slack below the negative maximum cycle mean, then taking longest-path potentials after adding that slack; no positive cycles remain. Adding a common constant to all a_i preserves (1) and can satisfy any fixed running-cost lower bounds.

Thus the margin placement itself can be selected by finite algebra and a finite weighted-cycle test. It is not necessary to insist on unit negative forcing in every phase. This matters because only particular fast-active phases may physically enter the problematic tail, and those phases can often support a much larger margin without amplifying the slow-head profile by the same amount.

Concrete check: in HOLEY_HEAD_NONBALANCED_ACTUAL_CLOSURE_V2.md, choosing a_i=2 on active head phases and0 on inactive phases yields v_i=O(s^2). All actual tail entrances originate in active phases. The base-residual tail/profile calculation bounds their extra forcing by s^(2alpha+o(1)), while inactive phases receive no direct tail error. Thus the selected margins pass with room to spare for alpha<1/43. A uniform unit forcing would not justify the same crude error estimate.

Limitations remain explicit: G must genuinely be Hurwitz with valid shift comparison; the return-error bounds must be earned for the actual process; any boundary cap must have its real incoming forcing controlled. A nonnegative weighted cycle is a failure of this sufficient construction, not proof of transience. No claim is made that an arbitrary weakly reversible network has the required negative cycles.
