# Independent audit: holey fast graph, corrected head, and actual return feedback

Reviewed 2026-10-30. Sources: `HOLEY_HEAD_ACTUAL_RETURN_CLOSURE_CANDIDATE.md`, `exact_holey_head_shift_slack.py`, its JSON, and the original leading-script/kernel helper.

**Verdict: the strengthened phase-offset/slack/active-forcing construction passes this audit as a local actual head–tail certificate. The modified-fast extreme-composition F estimate also checks out.** This is not a separate whole-global-proof review or a general/novelty claim.

## 1. Original fixture limitations, now explicitly repaired

Reproduced `HOLEY_HEAD_EXACT_LEADING.json` byte-for-byte. Its absorption helper omits immigration/activation hazards and has rows summing to one. It is the birth-SUPPRESSED fast/clearing kernel, not the actual zero-birth substochastic kernel. However it entrywise dominates the latter, because the actual zero-birth event additionally requires no competing birth along the same fast/clearing path. The current candidate labels this correctly.

The original frozen tilted inverse by itself was not a physical shifted-profile certificate: its profile grew as r^2, with an extra r^alpha in the hole phase, and the small Schur gap did not automatically absorb arbitrary fixed-shift errors. The new eta normalization and factor-two gain slack are substantive repairs, not merely a renamed original calculation.

## 2. Exact algebra and two-scale positivity

Reproduced `HOLEY_HEAD_SHIFT_SLACK_EXACT.json` byte-for-byte. Also checked directly from the constructed matrix:

- dimension 21;
- every entry has Laurent t exponents between -1 and 1;
- the active leading block is independent of t;
- its determinant is exactly 14644694986260480000 > 0;
- its inverse is entrywise nonnegative.

The Schur expansion is exact through the retained z order: the formal inverse recursion uses the invertible constant active block, and truncated multiplication retains every contribution through that order. The subset-DP determinant sign counts previously chosen columns greater than the newly chosen column, which is the correct permutation inversion sign. Thus the displayed z^2 determinant term and z^0 Cramer numerator terms are exact, not fitted asymptotics.

The full row-scaled matrix is polynomial in z and Laurent polynomial in t. Its full determinant has t degree bounded in absolute value by 21; replacing a column by the row-scaled forcing does not increase this bound. Multiplying the Schur determinant or Cramer numerator by the active determinant recovers the corresponding full polynomial, whose active leading determinant is a positive constant. Therefore a positive z-degree gap beats any possible t-degree advantage along t=z^-alpha when 0<alpha<1/43. The reported leading terms then genuinely determine the signs; lexicographic leading terms are not being used without a two-scale justification.

All inactive profiles are asymptotic to positive constants times r^2. The active block remains a nonsingular M-matrix for large r: it is a Z-matrix converging to its stable leading block. Its inverse is nonnegative, the transferred inactive coupling is nonnegative, and its right-hand forcing is positive. Active profiles are positive and O(r^2). This also proves eventual positivity of the full inverse solution, not just positivity of the inactive determinant.

## 3. The corrected coordinate really absorbs physical shifts

The script's source B=r+g_N-eta is correct for r=s+eta. Every compressed gain uses the destination eta as well, including the terminal phase after an exterior clearing. Eta is not claimed to be a tail invariant.

For rational alpha each profile is rational in a root of r. Eventual positivity gives v_j(r+ell)/v_j(r)=1+O(1/r). The extra analytic tilt has fixed-shift ratio 1+o(1). Consequently factor two bounds the exact gamma/tilt/profile gain ratio for every nonzero corrected shift, while a zero corrected shift changes no argument at all. This proves the displayed suppressed-return head inequalities with physical forcing r^2 phi on active phases and phi on inactive phases.

The source's scalar obstruction is genuine: at A=2,C=1 the triangle has no enabled fast source and clearing is disabled. Activation occurs at rate 2B, changes s by +1, and beats the rate-one neutral immigration with probability 2B/(1+2B). The new matrix mechanism is therefore doing work that a uniform scalar first-up estimate cannot do.

## 4. Actual tail accessibility and weighted return estimate

Every shell N>=4 reaches clearing. If A>=3, clearing is enabled. If A=0, the pure-C source can jump directly to A=3. If A=1 or 2 and A<3, then for N>=4 either pure C or the A+2C source is enabled and its edge to 3A increases A to at least three. Thus the finite-fiber accessibility hypothesis really holds above this head; the isolated N=3 hole is kept inside the finite head.

The finite-graph estimate, common (B)_4 factor, and p<1 cap yield uniform birth probability s^{-3+o(1)} before head descent and zero-birth stopping time s^{-4+o(1)}. The corrected terminal head data satisfy H<=C s^{2+alpha}phi(s), because eta<=1. In weight psi=s^{2+alpha}phi, the first-birth renewal norm is s^{-3+alpha+o(1)} and the full return norm is bounded. Hence returns with at least one birth contribute at most s^{-1+2alpha+o(1)}phi(s), exactly as claimed.

The running-cost assertion can be justified without a hidden interchange of limits. A single no-birth/first-birth attempt has expected phi-cost <=s^{-4+o(1)}phi(s). The full cost has a global phi-weighted bound by renewal. Expand that cost equation for any fixed K with K(3-alpha)>4: the first K terms retain the s^{-4+o(1)} bound because their residuals differ only by O(K), and the remaining term is <=s^{-K(3-alpha)+o(1)}phi(s). This proves the stated full-tail cost bound. A weaker polynomial bound would already suffice for the head margin.

The renewal construction proves finiteness and stopped nonexplosion before defining the tail value. First-jump decomposition gives the exact physical LW=-phi in the tail. No stationary distribution, equilibrium replacement, or full-chain recurrence is assumed.

## 5. Why omitted births are paid at the correct phases

All H=5 head-to-tail entrances originate at N=4 or 5, and every such phase is fast-active with eta=0. The entrance events are N=4 activation, N=5 activation, and N=5 immigration. Their original s increments are 0, 0, and -1, respectively; their rates are O(s). Thus there is no omitted positive entrance weight exponent.

Multiplying the true >=1-birth return error by the entrance rate gives s^{2alpha+o(1)}phi(s), and the running-cost contribution is smaller. This is o(s^2 phi(s)) for the chosen alpha. It is absorbed precisely where the matrix supplied the stronger s^2 forcing. Inactive phases have no direct tail entrances, so their phi-sized margin suffers no such error. Birth-suppressed domination pays the zero-birth part, and the weighted estimate pays the remaining actual paths. This proves a true local head–tail feedback inequality, not merely a frozen-kernel matrix sign.

## 6. Modified-fast extreme-composition F estimate

This estimate can be checked directly, rather than inferred from the old fast graph. Near the pure-C endpoint, the source 3C has two outgoing channels, to A+2C and 3A. Their factorial jump ratios tend uniformly to zero as A/N tends to zero and N grows, giving a negative order-N^3 contribution. Potentially positive reverse terms have boundary powers at least (A/N)^{1-alpha} or (A/N)^{3-3alpha}; these tend to zero for alpha<1. Near pure A, the 3A outgoing channels analogously give negative order N^3, while the opposing mixed and pure-C source contributions have boundary powers at least (C/N)^{2-2alpha} and (C/N)^{3-3alpha}.

Falling-factorial estimates remain uniform when the small coordinate is bounded: use enabled-source conditions and replace shifted small counts by their count plus a fixed constant. The resulting finite-count corrections are lower order than N^3. Thus fixed endpoint cones and a uniform -cN^3(B)_4 F margin exist. The low-B connector function and its clearing-return error are unchanged, and that error still has exponent 3-delta<3. Immigration/activation remain lower order. The modified graph is one strongly connected linkage, so balanced high-B negativity follows from the same primal bulk lemma after decreasing alpha if necessary.

## 7. Interface and scope

The tail extension's polynomial profile bound is enough for the previously proved cap-collar comparison. On the outer collar N~(log s)^p, B-s=g_N supplies a negative order (log s)^{1+p} factorial separation that beats every polynomial interface factor, while the original r-value vanishes there. Threshold definitions can be extended arbitrarily on the finite exceptional head/low-s set without changing these conclusions.

The present audit establishes the new local actual-return construction and checks the modified-fast endpoint premise. It does not independently reassemble or claim novelty for a full global theorem on the modified network. The original network's frozen reviewed bundle was not edited or used to skip these new obligations.

## Reviewed source hashes
be782212437b88ee191afaa8ca6438cc639dccfad44fca11cdb7adcd16914f89  chemical_joint_shell_20261030/HOLEY_HEAD_ACTUAL_RETURN_CLOSURE_CANDIDATE.md
4912eee940c8167673f961a7e0cb5900202f5220bdafc9134d2278367a118ce0  chemical_joint_shell_20261030/exact_holey_head_shift_slack.py
fac4c4e591407fcc5ac9675bcfd73fd6a685edeb835536cf1c3d4cacece88320  chemical_joint_shell_20261030/HOLEY_HEAD_SHIFT_SLACK_EXACT.json
1a2345f3eb40e35915517b7efd7d6f95dd57691fe4d77595423ccbc72db3b9b4  chemical_joint_shell_20261030/test_holey_head_return_matrix.py
