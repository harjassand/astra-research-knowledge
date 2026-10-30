# Independent review: approximate finite gates received by target-gate cavities
30 October 2026. Frozen source: sources/ROOT_APPROXIMATE_GATE_CAVITIES.md, SHA256 5b2ca82a9f1760d3f41d6eac93808c8946385eac08b719e3fb39ab8098a3f2ac. Governing cavity acceptance is the parent directory's INDEPENDENT_REVIEW.md.

## Verdict

**PASS for the modified target-gate cavity expansion and inclusive bound product_(j in S)(x+delta_j), under the finite fixed-schedule contract.** This receives an actually supplied finite-duration onsite reset from arbitrary dirty correlated targets into an exact-target fault expansion. It does not grant an exact physical reset, an unencoded noiseless detector, arbitrary adaptive/autonomous operation, or a complete threshold theorem.

## 1. Selected isolated slots really can be replaced

In the original cavity, a selected gate block has its intended local time-dependent generator and no coupling to its complement throughout that location. The complementary generator acts as identity on the selected block. Their propagators therefore factor, including for nonunital intended dynamics. Moving the entire intended channel G_j to the end of its location does not move it past an operation acting on that block: such an operation would violate the active-block disjointness premise.

At a later location using the same physical site, the earlier endpoint channel remains before the later dynamics. Simultaneously active selected locations have disjoint blocks, so their endpoint factors commute whenever their ordering is immaterial. Thus repeated-site slots are temporal channel insertions, not an illicit commutation of generator projections from different times.

Replacing the factored G_j by CPTP U_j leaves the complementary generator unchanged. Trace preservation makes the partial trace of the selected intended generator zero, even when it is nonunital. The modified cavity is consequently CPTP. It isolates the exact target at every selected location and preserves the accepted linear fault-class support argument.

The strictly layered disjoint-block case is directly covered. A more general fixed schedule must retain the declared location duration and an unambiguous endpoint ordering; a refinement to constant active partitions is permissible only with its resource overhead counted. No assertion for overlapping autonomous interactions follows.

## 2. Exact expansion and its signs

At each selected slot U_j=G_j-Delta_j. Multilinearity in those finite wire-channel insertions gives the displayed expansion over A subset R. In the inclusive alternating sum put R=A union B with disjoint A,B. Its sign is (-1)^(|R|+|A|)=(-1)^|B|, proving AG1 exactly. It is not a stochastic mixture.

The modified empty cavity is the actual channel; Möbius inversion therefore reconstructs that channel exactly. In each exact fault map, every location outside the declared fault set is its target U_j. Approximation residuals at other locations are allowed as arbitrary fault maps, rather than being hidden in ideal locations.

## 3. Fixed Delta insertions preserve the local derivative bound

For fixed A, first isolate A throughout their location intervals. Remove only their independent intended generators and insert Delta_j at the corresponding endpoint. The remaining generator is still a valid complementary cavity generator, with identity on the temporarily isolated A blocks. Further cavity choices on the remaining active blocks, and their convex interpolation, stay CPTP.

All evolutions between the fixed Delta insertions are therefore diamond contractions. Each fixed slot contributes its norm delta_j once. Mixed differentiation in the remaining location variables does not differentiate these fixed slots. It distributes derivative insertions across the intervening temporal segments; once their times are specified, the segment is determined. Thus the same ordered set-partition argument applies with no extra factorial or number-of-segments penalty.

Fixed-A projections are contractions and cannot introduce dependence on a system block absent from an original noise term. The derivative incidence estimate and root partition sum are unchanged. Hence the inner finite difference is bounded by product_A delta_j times x^|S\A|. Summing over A gives the exact product bound in AG2. This proof remains complete-norm uniform over arbitrary dirty-target/bath/reference correlations.

If x=0, the statement follows by the zero-noise limit (or direct product-slot expansion). No division by x is needed at that endpoint.

## 4. Finite reset is an actual approximate preparation, not fresh purity

The specified reset map R is CPTP and idempotent. Its bounded generator kappa(R-I) gives

 G_R=exp(-kappa tau_R)I+(1-exp(-kappa tau_R))R.

The complete norm inequality ||I-R||_diamond<=2 gives delta_R<=2exp(-kappa tau_R). This applies to initially entangled dirty targets, since R acts on the target while retaining the other systems. The supplied dissipative reset primitive is an explicit entropy-removal resource.

The order of choices is noncircular: fix a positive target strength, choose a finite reset duration to bound its residual, then fix the resulting maximum actual location duration and choose a sufficiently small positive eta. Data idles during long preparation must be included among locations with their actual durations. The error law receives both finite reset residuals and physical perturbations during the interval; it does not assume independence between them.

Resetting a known-state target does not reconstruct an unknown raw symbol erased during ingress. The prior raw-latch limitation remains unaffected.

## 5. Independent finite regression

check_approximate_cavities.py uses two physical sites at two successive layers (four locations), with a finite damping-to-zero reset at each first-site slot and an approximate finite rotation at each second-site slot. It computes all modified cavities, their exact isolated-slot expansions, and AG1 for every nonempty required set, at three perturbation rates including zero.

The 48 modified cavities are CPTP within floating-point tolerance; isolated-slot expansion residual is below5.5e-16 and AG1 residual below1.6e-15. Each of the45 inclusive bounds is checked with the Hermiticity-preserving dual certificate ||Tr_output |J(map)||_infinity, a valid diamond upper bound. Its largest ratio to the asserted product bound is0.999984 in the zero-noise rotation case, and less than0.564 at the nonzero tested rates.

The unnormalized Choi nuclear norm alone gives a looser dimension-dependent upper bound and exceeds the claimed bound in some cases. This is not a violation: the sharper valid dual certificate is below the bound. Both diagnostics are retained in the JSON rather than suppressing the loose result. Finite tests corroborate identities and constants; the all-size argument is sections1–4 above.

## Preserved scope

Accepted: exact-target signed fault classes and product local-noise strength x+delta for approximate finite intended gates, including supplied finite dirty-target reset.

Still separate: a physically available gate set and timing controller; actual fault-tolerant gadget correctness and overlapping-rectangle receiving; exact final detector qualification; unknown-input acquisition; infinite/unbounded bath extensions; autonomous scheduling; practical advantage; historical novelty. No external state was changed.
