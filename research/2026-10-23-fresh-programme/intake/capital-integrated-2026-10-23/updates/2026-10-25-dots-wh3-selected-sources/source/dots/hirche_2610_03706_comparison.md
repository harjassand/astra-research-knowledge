# Primary-paper comparison and receiving use

Primary source: Christoph Hirche, *Quantum estimation, channel orders, and private capacity*, arXiv:2610.03706v1, 2 October 2026, https://arxiv.org/html/2610.03706v1.

Read governing proofs: Proposition 3.5 / Eq. (3.18); Theorem 3.2 / Appendix A.1; Section 2.2 / Eq. (2.12); Proposition 3.4 / Appendix A.2; Theorem 5.1. The coherent-qubit integral must be credited as prior. The smoothed criterion has a finite reference test dimension d_B²; this is not an unsmoothed-reference cutoff. Section 6 leaves the unsmoothed-to-signed-lift implication open generally.

## Independent comparison with our retained constructions

Our SLD-to-BKM identity used auxiliary tau_s=diag(1,s)/(1+s) and the off-diagonal tangent H tensor X. Change variables t=1/(1+s). Then dt=−ds/(1+s)², and our measure ds/[4(1+s)²] becomes dt/4. The two block baselines are identical after relabeling. This identifies the integral ingredient exactly, not just conceptually. Our notes should call it a rederivation/use of an existing construction.

For completeness, the positive experiment can be checked directly. Set S_t=diag(tσ,(1−t)σ) and Ω_t=S_t+h sqrt(t(1−t))[[0,H],[H,0]]. Congruence by S_t^−1/2 gives [[I,hK],[hK,I]], K=σ^−1/2 H σ^−1/2. Its eigenvalues are 1±hλ_j(K), so h||K||≤1 guarantees positivity. The trace is one because the perturbation is off diagonal. If H_R=0, the complete CR marginals of Ω_t and S_t are equal. This directly explains both the operational positivity of the forward bridge and why it does not furnish the missing reverse Umegaki realization.

The conditional gauge remains a separate step in our argument. For arbitrary input baseline σ and tangent H, let L=Omega_(σ_R)^−1(H_R) and H0=H−Omega_σ(I tensor L). Then H0_R=0, and the output conditional SLD deficit equals the full SLD norm of the channel image of H0. The channel commutes with this reference-only gauge. Applying the prior integral pointwise and integrating BKM along a segment proves our quantitative conditional sufficiency for every coefficient c≥0.

Our reverse construction in `universal_conditional_sld_equivalence.md` is different: it uses a saturated numerator reference and finite resolvent filters converging to a point kernel. Its pair has unequal reference marginals. Nothing in the coherent-qubit integral alone supplies that reverse realization. Conversely, neither argument produces a physical equal-reference Umegaki witness for a general quantum channel from an arbitrary conditional witness. That remains the previously isolated positivity problem.

For coefficient c=1, raw and conditional comparisons coincide by cancellation of the common reference divergence. For c≠1, they do not. A raw coefficient below one is impossible with arbitrary untouched references: encode the entire distinction in the reference while keeping the transmitted system fixed. The raw ratio is then exactly one. Conditional subtraction is therefore essential to our quantitative statements, not a notational difference.

The distinction between a signed observable estimator and a physical state transformation is decisive. A Hermiticity-preserving lift that reproduces means and dominates quadratic costs need not send positive inputs to positive outputs. Accordingly, even a finite-dimensional certificate for such a lift cannot be silently reused as the positive geometry needed for the equal-reference witness problem. A stronger premise may be finitely testable without making the weaker unsmoothed order finitely testable.

## Why the W3 entropy target does not follow

Our present target compares W3 with a one-half retained fixed-equilibrium entropy, not with its complementary output. At the self-complementary endpoint, receiver/environment comparison reduces to equality between isometrically equivalent outputs. It then says nothing quantitative about contraction relative to the identity channel or the product equilibrium I3/3 tensor ρ_R.

More concretely, the desired statement is

D((W3 tensor id)ρ || I3/3 tensor ρ_R)
 ≤ (1/2)D(ρ || I3/3 tensor ρ_R).

A receiver-versus-environment ordering supplies no factor 1/2 in this expression. A private-capacity conclusion concerns optimized classical-message advantages and cannot be substituted for this pointwise entropy inequality. Thus the reviewed results neither invalidate nor subsume the rank-four family certificate, nor settle the unrestricted W3 target.

## Priority and confidence boundary

The coherent-qubit integral is prior and should not be claimed as our new theorem. The conditional gauge, reverse filter, sharp coefficient applications, and positive-realization question must be compared separately, with their exact quantifiers retained. This review checks the relevant finite-dimensional mechanisms and non-transfer; it is not a blanket validation of every capacity claim in the source or of unrelated claims in N675.
