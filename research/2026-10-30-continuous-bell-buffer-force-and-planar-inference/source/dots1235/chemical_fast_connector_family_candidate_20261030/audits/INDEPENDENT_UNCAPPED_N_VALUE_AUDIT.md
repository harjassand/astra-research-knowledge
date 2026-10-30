# Independent end-to-end audit: uncapped N-directed actual value

Reviewed 2026-10-30. Source: `UNCAPPED_N_DIRECTED_VALUE_CANDIDATE.md`, using corrected `N_DIRECTED_RESET_WALK_V2.md` and the independently audited strict-power clearing theorem.

**Verdict: passes this child-level audit on the amended source.** The proof earns a finite actual stopped-cost value and its pointwise generator identity uniformly in the unbounded hidden fiber. It no longer treats a neutral bad immigration as a physical exit. This review does not independently certify a separate global-recurrence synthesis or novelty.

## 1. Independent nonexplosion and scalar geometry

For 1+N+B the fast generator is zero. If B<q, positive activation drift is O(1+N); if A<m it is O(1+B). In the complementary region, falling factorials are bounded below by fixed multiples of A^m and B^q. Since m>=2 and q>m, C AB-c'A^mB^q is bounded above; thus LV_1<=CV_1. Finite sublevels and finite-state localization prove global nonexplosion independently of recurrence.

The H formula and all residual increments check out. N=r+H(B)>=r, activation is neutral, only designated immigrations increase r by h, and designated clearings decrease it by h. The source's first-event bounds therefore apply uniformly in arbitrary high B and hidden composition when r is large. No small inactive shell enters this domain.

## 2. Reset-law conditioning is genuinely controlled

At every fully specified fast-stage input, clearing before either birth has probability >=1/2 for large r. Its output inverse moment is <=Cp(r) by the actual clearing compensator. Therefore its subprobability kernel satisfies the relative bound

    K_D[(1+A_after)^-m] <=2Cp(r) K_D[1].

The terminal low phase and the downward-exit classification are determined by the pre-clearing B, not by the newly sampled A_after. Decompose a selected terminal branch over its final clearing-stage inputs and apply this relative inequality before normalization. The bound is preserved even if the final phase/branch is rare. This supplies admissible fresh low laws at new levels, with constants uniform over the preceding history. It does not assert an inverse-moment bound after observing A_after.

The corrected reset-walk probability argument is valid with joint kernels. It proves O(beta) escape for an arbitrary fresh low law and O(p) for the fresh B0 law followed by compulsory immigration. Fast-episode entrance indexing gives the bounded expected number of runs without illicit post-output conditioning. For the new section, activation from b=1 lands directly on S and stops repair; the normalized low-return assertion is correctly restricted to b>=2.

## 3. Weighted repair is an actual finite-cost construction

The repair input family consists of pointwise fast states and admissible fresh low laws; it must not be read as a pointwise bound for every observed low composition. A repair round composes the fast-to-low transition with its ensuing low walk. The neutral fast-to-low leg can have mass one, but is internal to that round, not a purported small continuation.

After this composition, only the following require further repair:

- a downward exit, with weight ratio O(r^-alpha h);
- a bad active state, whose probability is O(p) from fast processing or O(beta) from the fresh low walk, with maximal weight ratio O(r^alpha h).

A low upward wrap lands directly on S and contributes terminal weight of the same small weighted order. All coefficients tend to zero because alpha h<epsilon and epsilon may be taken below 1, hence below (m-1+epsilon)/m. The strict-power exponent furnished by the startup proof already has this property.

Each composed round has bounded expected duration at its fixed residual: there are geometrically bounded fast stages and bounded expected low-reset runs, with low holding rates bounded below by immigration. Its expected running phi-cost is <=Cphi(r). Truncating at a finite number of rounds gives a normalized value inequality M_n<=C+rho M_(n-1), with rho<1/2 after fixing a sufficiently large threshold. All constants can be fixed before increasing that threshold. Monotone passage to the limit earns finite terminal weight and finite accumulated running cost.

This also proves actual termination, rather than assuming it. The running cost is bounded below by a positive constant above threshold. Global nonexplosion prevents infinitely many round-ending reaction events in finite time. Thus a nonterminating repair would accumulate infinite cost, contradicting the finite expectation. Neutral bad immigrations are genuinely continued by this construction.

## 4. Sharp R0 and R1 estimates

R0 applies only to a fresh clearing-reset law at B0, as the amended source explicitly states. Partition its first composed round into same-level section returns, downward branches, and upward/bad branches. Same-level terminal weight is exactly phi(r). A downward branch has subsequent expected weight <=Cphi(r-h)<=phi(r) at large r. The first two masses sum to at most one. The remaining branches have total mass O(p), and their future weight is <=Cphi(r+h). Therefore

    E phi(r_S)<=[1+Cp(r)r^(alpha h)]phi(r).

The coefficient one is not replaced by an arbitrary constant, which is essential for the later small section drift. An arbitrary observed B0 composition does not enjoy this estimate; it is covered by the separate initial repair bound.

From B=2q-1, intervening activations preserve the downward clearing residue. The first clearing before immigration is therefore down. Immigration before that clearing has probability O(p), using the uniformly bounded stage count. Applying the already earned fast/fresh-low repair bounds gives R1 exactly as stated, and its normalized return weight tends to zero.

From an arbitrary low state, before the first fast entry the only events are immigrations and a possible final activation. There are at most q such low events; their mean duration is bounded. The residual can increase by at most h before the fast state or S is reached. This proves the worst-case initial r^(alpha h) factor without assuming a fresh moment law.

## 5. Pointwise section-return contraction

At every S state B=q, N=r+m. The pointwise hazard inequality lambda_T>=c r^{-(m-1)}lambda_D holds wherever clearing is enabled and trivially elsewhere. Integrating until the first connector event gives P_T>=c r^{-(m-1)}P_D, while strict clearing gives P_D=1-o(1) and P_I<=Cp.

All three first connector events preserve r. Conditional on clearing-first, the output law is fresh and R0 applies. Conditional on activation-first, the input to R1 is a fully specified arbitrary composition, for which R1 is uniform. Conditional on immigration-first, the pointwise fast repair bound applies. Consequently

    E phi(r_next)/phi(r)
      <=1-P_T(1-o(1))+Cp(r)r^(alpha h)
      <=1-c r^{-(m-1)}.

The error is smaller than the negative term precisely because alpha h<epsilon. This inequality is conditional on the full incoming section state, not on an invented pointwise fresh-A moment estimate.

The same result for Psi=(1+r)^(m-1)phi must be obtained by repeating the branch proof, as the source does. One must NOT append a generic O(1/r) multiplicative error to the final small-drift inequality, which could overwhelm r^{-(m-1)}. Same-level returns keep the exact coefficient one for Psi; only the already rare or downward branches use fixed-shift ratios. Thus the polynomial enlargement preserves the needed drift order.

## 6. Real-time cost and the actual generator identity

The expected phi-running cost in a section-return cycle is <=Cphi(r): the first fast connector race has a finite uniform mean, and all three branches have the earned repair-cost bounds at the unchanged initial residual. For Psi, section drift is at most -cphi. Telescoping at finitely many actual section returns, using nonnegative terminal weight, and then monotone convergence bounds the sum of expected phi(r) over cycles by C Psi(r_initial). This pays the real-time cost, not merely the number of jumps in an instantaneous trace.

The lower bound phi>=1 above threshold makes the expected number of section cycles finite. Each repair is an actual finite-duration stopping construction, so threshold arrival follows almost surely and its expected accumulated cost is finite. Arbitrary-state initial repair adds at most the stated r^(alpha h) factor. Hence the displayed uniform upper bound on W_r is earned.

With W_r=0 at r<=r0, ordinary first-jump decomposition is now justified and gives LW_r=-phi(r) above threshold. Finitely many outgoing targets have finite values, so no regularity assumption or infinite generator sum is hidden. Only constant-rate immigration can cross upward from the exterior threshold strip, and its target r lies in a fixed finite band. The hidden-fiber-uniform upper bound therefore gives a globally bounded positive threshold defect. The first-holding lower bound follows from total physical rate <=C(1+N+B)^(m+q).

## Verdict and scope

The amended repair and pointwise-section construction closes the actual neutral-bad continuation gap identified in the original fresh-section note. It supplies an uncapped N-directed value, but normlikeness of that value alone is correctly not asserted. Combining it with a complementary residual is a separate synthesis. Fixed positive coefficients and the stated homogeneous/pure-complex graph contract remain essential hypotheses.

## Reviewed source hashes
8e638fe1c219848b553cd921eba916b3de919c7eee41ea8c75bcc99bb8ab214d  chemical_joint_shell_20261030/UNCAPPED_N_DIRECTED_VALUE_CANDIDATE.md
7d462ffb21e2ab248bbd7c95024efae6a995b2e8d8eb70bcaac920fbd9e09483  chemical_joint_shell_20261030/N_DIRECTED_RESET_WALK_V2.md
