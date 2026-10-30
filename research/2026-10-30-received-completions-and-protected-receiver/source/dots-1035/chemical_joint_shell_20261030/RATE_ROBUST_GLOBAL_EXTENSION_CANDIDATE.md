# Unreviewed extension: a common global certificate under bounded rate interventions

Status: personally derived extension, NOT YET REVIEWED. The separately bundled base candidate must not be treated as already proving this stronger statement.

## Proposed theorem and exact scope
Fix the SAME reaction graph as JOINT_GLOBAL_FOSTER_CANDIDATE.md. For every reaction e, fix 0<m_e<=M_e<infinity. Permit its coefficient to be an arbitrary time-homogeneous function k_e(A,C,B) in [m_e,M_e], multiplying the usual falling-factorial mass-action source rate. The coefficients need not be continuous, lumpable, independent of hidden composition, or mutually coordinated.

Claim under review: one finite normlike function V, depending only on the coefficient intervals, satisfies a global Foster inequality for EVERY such generator. Consequently each resulting homogeneous finite-rate CTMC is nonexplosive and every closed class is positive recurrent with all exponential total-population moments. The positive reaction graph is unchanged, so weak reversibility still makes communicating classes closed.

Generator inequalities can also be interpreted under adapted time-dependent controls, but stationary recurrence/moment statements are made ONLY for time-homogeneous generators. No exponential mixing-rate or uniform-in-time moment claim is asserted.

## 1. Uniform bulk alpha is earned, not assumed
The finite killed-generator lemma used in the bulk proof is uniform over a compact positive coefficient box. If it were not, choose alpha_n→0, coefficients k_n in the box and simplex points z_n with nonnegative dissipation. Pass to convergent coefficient and simplex subsequences. Positive terms are O(alpha_n) uniformly by weighted AM-GM. The limiting support cannot contain a killed vertex. A fixed directed path from that support to killing has a first edge leaving the support; its negative term divided by alpha_n tends to infinity in magnitude. Its coefficient stays bounded below. This contradicts the positive O(alpha_n) budget.

There are only finitely many proper complex supports. Choose one sufficiently small alpha for all of them and all coefficient choices; compactness supplies the fixed-alpha margin. The falling-factorial comparison errors are uniform as well. Thus the SAME primal factorial bulk function works pointwise for every state-dependent coefficient choice.

## 2. Replace the low-phase function by an actually controlled finite Poisson value
At B<4, only immigration and activation occur and B reaches4 or more in at most4 jumps. Define F there as the supremum, over allowed coefficient controls, of terminal V0 plus the running V0 cost until that exit. At B>=4 retain F=V0.

C is unchanged during this finite excursion, so F=C!^alpha f_B(A). The backward Bellman recursion is

    f_b(a)=max_(u in {m_I,M_I},v in {m_T,M_T})
      [(a!b!)^alpha+u f_(b+1)(a+1)+v ab f_(b+3)(a+2)]/(u+v ab).

The endpoint maximization is valid because the expression is separately linear-fractional in each positive coefficient, with derivative of fixed sign when the other coefficient is held fixed. At b=0 only immigration remains.

The value is finite, F>=V0, F<=poly(A)V0, and L_k F<=−V0 at every low phase for every admissible coefficient choice. The same exact return asymptotics remain uniform:

    f_b(a)=((a+2)!(b+3)!)^alpha[1+O(a^(alpha−1))], b=1,2,3;
    f_0(a)=((a+3)!4!)^alpha[1+O(a^−delta)],
    delta=min(1−alpha,3alpha)>0.

Indeed activation dominates immigration by a factor of order a at b>=1, uniformly over the coefficient box. The b=0 holding cost changes only its bounded prefactor. Thus actual clearing-return feedback is still O(A^(3−delta)) relative to the factorial scale. No coefficient derivatives are used.

Fast inward drift at A/(A+C) near0 or1 remains uniform: the extreme pure-C creation channel and pure-A depletion channel retain positive lower coefficients, while all opposing rates have the required boundary count factor and bounded upper coefficients. The two extreme-composition F inequalities therefore hold uniformly. In balanced high-B states the uniform bulk theorem applies.

## 3. Controlled first trace already has the required scope
The r=N−h_B trace was proved with arbitrary adapted coefficients in compact positive intervals. Actual connector coefficients in A>=epsilon N remain in such intervals after dividing by (N)_1 or (N)_3. Hidden fast transitions preserve N,B and therefore contribute zero to the r-value. The off-cone positive-rate upper bounds remain uniform.

## 4. The actual complementary trace also admits uniform controls
On its fixed composition head, all endpoint row policies have the same positive graph and degrees. Exact positive Schur exponents are unchanged. The affine policy-improvement lemma therefore makes the up/tail/time bounds common for all controls, not merely for fixed coefficients.

On a conservative N-shell, the explicit W_N(a)=(a+N^(3/4))^(−3) absorption proof is uniform over the coefficient box: near a=0, creation drift is bounded below by cN^3, total rate is at most CN^3, and clearing is at least c(a)_3. The same Taylor estimate gives Q_k W_N<=−c_0 for every allowed instantaneous generator. Stopped Dynkin yields the controlled absorption bound C N^(−9/4)/(B)_4. Summing the competing-birth risk over decreasing N is unchanged.

Hence the complementary s-trace has the same uniformly controlled first-up O(1/s) and polynomial-time estimates. Define W_s as the SUPREMUM stopped-cost value, rather than the uncontrolled expectation. The first-jump epsilon-policy argument now gives L_k W_s<=−phi_s for every allowed row. Its threshold leakage is still at most C AB.

## 5. Global coupling is uniform
All three ingredients F,W_r,W_s are now common functions. Every comparison in the base global proof uses only coefficient-box constants, finite polynomial degrees and fixed entropy gaps. The same sum V=F+W_r+W_s therefore gives the claimed uniform Foster conclusion if the extension passes whole-proof review.

## Why this is materially stronger, and why it is still restricted
This would cover all positive constant-rate choices on the graph and arbitrary bounded state-dependent multiplicative perturbations, including adversarial dependence on conservative composition. It does not assume exact lumpability, phase equilibrium, or a common Lyapunov barrier; that barrier is constructed from the trace bounds.

It remains a theorem for this reaction graph/structural mechanism, not arbitrary weakly reversible networks. Removing coefficient lower bounds or changing the finite-head exit-order inequalities can invalidate it. No novelty clearance is claimed, and the extension is presently unreviewed.
