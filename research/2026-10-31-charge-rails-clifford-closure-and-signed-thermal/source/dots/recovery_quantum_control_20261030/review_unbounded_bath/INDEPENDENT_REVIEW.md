# Independent review: common unbounded free-bath CP cavities
30 October 2026. Scoped PASS for the stated common-base, bounded-perturbation cavity extension. This is not a whole infinite-bath native-device receipt.

Frozen source: frozen_sources/ROOT_UNBOUNDED_FREE_BATH.md SHA256 25ead9254477707014505c1d91ba62e8e3e4143fe9fff09fd546caf10be904a5. The superseded 0389ce72 version is not this binding target. The final source includes the intended-block and convex-averaging clarifications requested during audit.

## 1. Exact interpretation of measurability and domain
Read 'strongly measurable on trace class' as pointwise strong measurability: t maps to K(t)rho is trace-norm measurable for every trace-class rho. Together with a measurable integrable bound on ||K(t)||_cb, this suffices. Operator-norm/CB-Bochner measurability of the map-valued family is not required.

The bath and finite system give a separable trace-class Banach space. Products K(t)x(t) with strongly measurable x(t) are strongly measurable by approximation with simple vectors and the pointwise bounded-operator property. The common free semigroup is strongly continuous and completely contractive. Thus every time-ordered Dyson integrand is strongly measurable and has an integrable scalar norm majorant. Its strong integral defines a bounded linear predual map. The same construction applies to each finite reference ampliation and yields bounds independent of reference dimension. The maps' adjoints are normal because they have these trace-class preduals.

For merely measurable nonautonomous K, this establishes the usual mild evolution. It does NOT assert norm differentiability of V_t, differentiability on every input state, or invariance of D(B_0) under arbitrary time-dependent perturbations. No such assertion is needed. In the autonomous case the bounded-perturbation generator has domain D(B_0); in the nonautonomous argument all formulas can and should be read as mild/Dyson identities on the entire trace class.

## 2. Reduced cavities really converge in complete norm
C_R and E_R intertwine the common bath semigroup. Therefore the compressed actual short propagator and the bounded-perturbation reduced propagator have exactly the same zero and first Dyson terms. Each remaining order-r term has complete norm at most h^r/r!, even though the free semigroup need not be norm continuous. The strong integrals are first defined pointwise; the uniform ampliation majorant then proves the complete-norm bound. This does not require integrating V_t in operator norm.

Hence IB1 holds. On a partition, Q_i is CP/TP (or CP/TNI), while ||W_i||_cb<=exp(h_i). Composition of the mild propagators and telescoping yield an error bounded by the stated conservative exp(2h_total) sum_i h_i^2. Absolute continuity of the integral of the scalar majorant permits max_i h_i to tend to zero at fixed finite device and horizon. CP and TP/TNI are closed under this complete-norm limit. The resulting reduced propagator therefore has the required positivity on the entire trace class.

This argument neither bounds nor approximates ||B_0|| and does not assume a finite-energy initial bath. It also does not exchange an infinite-system/thermodynamic limit with the partition limit. Each physical system here has finitely many finite-dimensional sites; the bath may be infinite.

## 3. Restoring gates and averaging interpolation
For actual cavity restoration, R must be a union of current disjoint intended gate blocks. Otherwise an intended gate crossing R need not split into the stated tensor complement. The final source explicitly imposes this condition. Trace annihilation of an isolated intended CPTP generator gives its zero reduced contribution, while complement intended gates are unchanged. Tensoring the restored independent intended evolution is CP/TP and leaves the same free bath base.

The final interpolation proof correctly uses convex averages of exact cavity maps over the SAME subinterval with fixed weights. Such an average is CP/TNI and has the same zero/first Dyson terms as the desired averaged bounded perturbation. The same remainder/partition argument then proves the interpolated propagator CP/TNI. A common integrable bound for the finitely many cavity perturbations suffices.

The earlier time-fraction concatenation wording was unsafe without extra care for nonautonomous merely measurable K; it has been removed. If optional time-dependent convex weights are used, bounded simple approximations converging almost everywhere also converge in weighted L1 against the common perturbation bound. Variation of constants then gives convergence in complete norm. Fixed interpolation parameters, which suffice for the claimed local law, avoid even that extension.

## 4. Parameter variation and absence of a volume exponential
All parameter dependence is in bounded polynomial K_z. Common-base variation of constants follows by regrouping the strong Dyson integrals, with integrable scalar majorants justifying Fubini. Difference quotients and higher parameter derivatives consequently converge in complete norm although V_t itself need not be norm differentiable. The ordered-partition derivative formula uses exact interpolated CP/TNI propagators between bounded insertions.

Those intervening maps have complete norm at most one. Bath-only terms are annihilated by every processor cavity difference; B_0 has no parameter derivative at all. The remaining derivative support/count estimate is exactly the already accepted finite-system local one. Its per-site incident norm and support cutoff q give the unchanged rooted-partition fault strength. No exp(h_total) belongs in that estimate: the exponential above is only a fixed-device existence/convergence majorant used to establish the exact CP interpolants. It is not an operational resource cost and is not carried through the fault calculation.

Uniformity is established over all finite reference ampliations, as claimed. Any larger normal reference extension must be interpreted via its trace-class/normal extension, not assumed from a nonnormal map. Finite-dimensional system matrix-unit expansions remain finite even when their bath coefficient maps act on an infinite Hilbert space.

## 5. Tests and exact stopping boundary
Replayed check_reduced_product.py: all 44 finite-dimensional consistency cases pass the certified envelope. Saved source_replay.json. The test checks spectral-superoperator error against a proved complete-norm majorant; it does not optimize a diamond norm or simulate an infinite bath. No monotonicity of actual approximation error in partition count is inferred. Fast bath oscillations can make coarse partitions accidentally closer than intermediate ones; the rejected monotonic-error claim is not revived.

Accepted extension: a supplied common bath-only C0 CPTP semigroup with possibly unbounded generator; finite-system bounded strongly measurable perturbations with integrable complete norm; actual CP/TP or CP/TNI propagation on every subinterval; and the existing local HP/support/incident assumptions. Individual perturbations need not be CP or centered in the TNI formulation.

Not accepted: unbounded system-bath interaction operators, an unspecified arbitrary unbounded total generator, domains inferred from low-energy intuition, thermodynamic-system limits, native warm/logical identities automatically transferred to infinite baths, microscopic reset-reservoir realizations, novelty, or practical improvement. Finite resets, system-only cuts and later factory/receiver arguments can use this lemma only after ALL their own common-chart, normal-coefficient, source and moment hypotheses have been independently checked for the extended setting. No prior finite-bath device receipt is silently broadened.
