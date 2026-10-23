# Failures and revisions that affect continuation

## Scientific routes closed or corrected

1. **Treating a KL-only exponential sample-cost law as new.** The focused primary-source search showed that Block–Polyanskiy already establishes the exponential accuracy scale. The coefficient-one calculation is retained as an independently proved baseline/specialization, not promoted as a new entropy barrier.

2. **Using the obsolete proceedings tail lemma.** The old Lemma 27 omits a boundary term. The authors corrected it in arXiv v3. A Bernoulli diagnostic in the literature notes violates the old statement. The current proofs use independently derived valid tail and clipped-excess inequalities. This is an upstream correction, not a newly claimed Astra correction.

3. **Assuming a local reversible update preserves proposal-start finite-time TV performance.** Stationary variance and Dirichlet ordering do not imply this. The explicit fixed-KL three-state construction disproves the uniform guarantee, including both matched-global-call cycle orders. The operation is closed under its proved assumptions; no more synthetic cases are needed to establish the same fact.

4. **Promoting SIR over ordinary IMH.** The strongest finite-support same-budget comparator dominates ordinary SIR in every convex f-divergence. SIR is used only to prove approximate warmness; the actual finite-state initializer is pure IMH. No advantage is manufactured by weakening that comparator.

5. **Treating approximate warmness as a full mixing theorem.** A bad-mass/good-density decomposition alone supplies no convergence rate. Section 6 of PROOF.md supplies an explicit reversible lazy-mixture rate, and records its poor exponential cost. A fitted training loss is also not a population-KL certificate.

6. **Expecting a doubly exponential joint-KL obstruction from the same funnel.** Reverse KL bounds the stationary entrance mass from below. Reversibility then forces a compensating local escape rate. The independent funnel note proves the limitation and supplies a valid singly exponential lower family. Making the global exit still smaller does not overcome the local escape.

7. **Nested-exponential upper bound by truncating the initial density first.** This valid but weak route became unnecessary after the principal switched to smoothing an indicator. The first direct core proof gave coefficient (sqrt(K)+sqrt(J))^2; better outside-mass accounting gave K+J; an independent fixed-anchor refinement changed the product BR into M(B+1)+R and gave max(K,J). The current theorem is in JOINT_KL.md. PROOF.md Section 8 preserves the earlier continuation seed and is superseded by the new file.

8. **Losing half the lower coefficient by looking only at the first lazy step.** Binomial subordination retains the non-lazy exponential coefficient. A skewed but fixed symmetric path proposal then raises the class lower bound from (1-alpha)J/2 to (1-alpha)J. The proof does not require a reducible endpoint kernel.

9. **Assuming both deterministic cycle orders have the same joint-KL lower construction.** For GL, the original first-cycle injection is b^2/2, not b/2. With b proportional to epsilon that is insufficient. The independent note records the weaker sqrt(epsilon) parameterization instead. The positive joint-KL theorem is explicitly limited to the lazy random mixture.

10. **Claiming complete sharpness.** Only 0<J<=K has matching upper/lower leading exponent K. The remaining J>K interval is max(K,(1-alpha)J) through J. No numerical optimization or small-chain demonstration closes that interval.

## Recovery and execution issues

- The original B3 source was not present in scratch. Its exact private persistent identity was recovered; a restricted download failed and the unchanged authorized helper succeeded with network permission. An ambiguous README suffix was corrected to the exact main archive member. Neither issue changed any scientific result.
- `mpmath` was unavailable in both queried Python environments. The principal used the standard-library Decimal module, consistent with the independent arithmetic, with separately coded general MH and multinomial SIR routines. No package installation was required. Matplotlib was available in the supplied runtime; its default read-only cache path fell back to a temporary directory. The completed figure was visually inspected.
- An OpenReview retrieval hit a verification/403 response; the original NeurIPS source was used. Some arXiv URLs failed in one search service while the primary PDFs were accessible through authorized retrieval. Public source identities and failed download receipts are retained.
- The principal replay, higher-precision check, cross-implementation comparison and joint-KL event checks passed on their first recorded scientific execution. Their rounded arithmetic is not a formal interval certificate.

## Historical operations remain closed

B3's pISO correction, the failed full halo inference and the diffusion metadata-admission failure retain their frozen inputs and decisions in the exact original archive. The Gaussian conditional sampler and scoped R3/anMC recipient rejection are preserved. None of these was rerun or reused as claimed adoption. No protected owner's construction was transferred by the restoration instruction.
