# Root receiving review of the separate equilibrium fluctuation theorem

30 October 2026. Actual-file review, not a review of a synopsis.

Reviewed input: `record_geometry/EQUILIBRIUM_DENSITY_CURRENT_GEOMETRY.md`.
SHA-256: `a51c985b179d24a03a5395378cf0d3142f86344dbc602359198ddfe44fbe599e`.
The exact reviewed file and input record are retained beside this review.

## Decision and actual scope

Accept the stated joint functional central limit theorem at its actual clean
ring interface: canonical stationary occupancy with a fair bit, or the stated
bounded-density initial-law extension with the required initial-field limit;
alpha_N in [0,1] tending to alpha; gamma_N tending to infinity and gamma_N/N
tending to zero. The theorem is not being extended to arbitrary hidden phase
amplitudes or zero external clock by this review. In particular, the new root
zero-clock large-deviation theorem for fixed alpha<1 does not itself prove a
zero-clock fluctuation theorem, and this CLT does not prove the singular full
spatial action at alpha=1.

No substantive correction was needed. The authored file's statement that
independent review was pending is historical after this actual receipt; it is
retained rather than silently rewritten.

## Reconstructed checks

1. **Canonical cancellation.** The coefficient sum for Delta G is exactly
   zero. Covariances for disjoint bonds are identical under the canonical law;
   subtracting their common value leaves only bounded-overlap terms. Thus
   Var(sum Delta G_i a_i)=O(1/N), not merely a pointwise O(1) bound. The density
   defect therefore has squared L2 norm O(N^2).

2. **Clock coercivity.** The macroscopic reversible form dominates the sign
   form. For an odd source R, its inverse-energy norm is at most
   ||R||_2^2/(2N^2 gamma_N), even though native and clock generators need not
   commute. This follows from the variational definition and projection onto
   the odd component. The native form is nonnegative. The stationary reversible
   maximal additive-functional inequality makes the integrated defect vanish
   uniformly on compact times. This step really uses gamma_N -> infinity.

3. **Density bracket.** Its activity part converges by the same canonical
   variance bound and stationarity. In the odd part, discrete summation by parts
   bounds N sum Delta G_i Delta K_i delta_i by O(1/N). Thus no hidden temporal
   mixing premise is used for the deterministic bracket limit.

4. **Actual current martingale.** For an active jump,
   (1+alpha u delta) delta(delta-alpha u)=(1-alpha^2)delta^2.
   This independently verifies the displayed density/current cross bracket.
   The total-current bracket is c(1-alpha^2)A/N. Canonical equal-time activity
   control makes both integrated brackets converge. Their jumps vanish, so
   the vector martingale functional CLT has the stated Gaussian limit, jointly
   with the initial field. Vanishing cross brackets imply independence in
   this Gaussian limit; finite-N independence is not asserted.

5. **Actual elapsed time.** The clock martingale correction to total current
   has normalized mean bracket O(gamma_N/N). The remaining clock occupation
   has inverse-energy bound alpha_N^2 gamma_N/(2N). Both vanish in the paid
   clock window. This is a proof for actual elapsed time, not the event-pair
   occupation clock in the separate trace construction.

6. **Spatial reconstruction and topology.** Exact continuity gives the
   discrete-antiderivative formula with the displayed plus sign. The Fourier
   maximal bound grows at most as 1+k^4+k^2/gamma_N. Its H^-3 weighted sum is
   finite, giving compact containment in a weaker space; finite-coordinate
   tightness then supports the stated H^-5 field topology. The same estimates
   control approximation of the discrete antiderivatives.

7. **Endpoint and records.** Alpha=1 is allowed here because the positive
   external clock makes every needed exchange orientation accessible, and the
   proof uses sign coercivity rather than uniform native ellipticity. A fixed
   recorded u or sigma with canonical visible occupancy has density two
   against the stationary joint law, so the small-error transfer is valid.
   A complete retained occupancy record does not generally have this bounded
   density; no such transfer is accepted. Full future conditional generator
   laws remain required.

## Scientific consequence and provenance

The result supplies a genuine additional distinction: ordinary equilibrium
density OU fluctuations coexist with a tunable harmonic-current Brownian
variance s chi(m)(1-alpha^2). At the closed-gate endpoint that harmonic current
vanishes at the fluctuation scale, while density fluctuations remain ordinary
under the stronger clock/initializer interface. Nonconstant integrated currents
are reconstructed from density differences and are generally not Brownian.

The inverse-energy and martingale framework is established Kipnis--Varadhan
machinery. Root read the primary 1985 announcement,
https://www.numdam.org/article/AST_1985__132__65_0.pdf, including its inverse-form
condition and martingale approximation, and checked the finite-chain scaling
actually used here. This review establishes internal mathematical acceptance,
not historical priority, an apparatus, or finite-data experimental confidence.

No extra fixture was run for this review; the needed checks are algebra,
initial-law transfer, topology and asymptotic estimates.
