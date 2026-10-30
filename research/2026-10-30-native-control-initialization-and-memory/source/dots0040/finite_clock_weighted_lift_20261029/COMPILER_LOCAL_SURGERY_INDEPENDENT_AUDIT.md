# Independent audit of conditional local surgery for the one-body-reset compiler
2026-10-30. Auditor: cp_clean_overlap. This audit does NOT supply the raw bad-token reset charge; it checks the reduction conditional on that charge and the stated monomial gauge.

## Verdict
No hidden O(t kappa) good/bad coherence term or extra animal-size factor was found. The local-surgery reduction is sound conditional on its explicit structural inputs, provided buffered supports include the full gauge/light-cone footprint and the gauge flags are used consistently. The positive diagonal bad blocks cost O(t kappa) and are paid by raw bad-reset loss; the cross blocks are only O(t kappa nu), producing O(t^2 kappa nu^2) clean-side cost after Young's inequality.

## 1. Stronger flag simplification in the chosen gauge
Let U be the occupancy-preserving guarded monomial completion. In gauge coordinates, the combined flag is exactly
C'_h=U^* C_h U=Q_h-G_h R_h,
where R_h=|ref_h><ref_h| is the fixed good excited reference-label projector. If a neighbor is occupied, G_h=0 and C'_h=Q_h. If all neighbors are ready, U_h maps R_h to the physical good Stinespring projector E_h, while every other nontrivial guarded unitary is on disjoint data support. Hence U^*G_hE_hU=G_hR_h.

Thus the gauged C'_h are PURE AUXILIARY projectors, not data-dependent projectors. In particular all hypothetical data-only Phi_h commute with every C'_j. The guarded good-reference coherence in B_h changes ready<->ref only when neighboring auxiliaries are ready, so B_h and sqrt(B_h) commute with every flag. The circuit generators Z_h therefore preserve every mask block, exactly.

This identity removes a possible ambiguity in writing d_h=(I-Phi_h^*)V_ext: d_h may depend on remote flags through animal weights, but Phi_h never changes those flags. On a clean buffered local region they are commuting spectators, so the legal-range algebra applies without pretending d_h is globally clock-independent.

## 2. Zero-drive diagonal algebra and cross-mask scaling
At nu=0, B_h=Q_h, sqrt(B_h)=Q_h, and Z_h has jumps Q_h K_hs. Such maps preserve the joint syndrome/auxiliary-label diagonal algebra. The physical Hamiltonian vanishes at nu=0. By the monomial-gauge assumption, each conjugated raw reset is a partial monomial map on that same joint sector algebra, so its adjoint preserves diagonal observables. Consequently BOTH L_0 Z_h(0)V_ext and Z_h(0)L_0 V_ext are diagonal. Their cross block between any diagonal masks P_X and Q_X is exactly zero.

The required square-root estimate is valid for the explicit B_h, rather than generic positive-matrix continuity. The only off-diagonal block is the ready/ref two-dimensional block, whose small eigenvalue is O(nu^2), off-diagonal entry O(nu), and large eigenvalue 1+O(nu^2). Its square root differs from Q_h by O(nu). Blocked-ready sectors have square root nu sqrt(f_m), while blocked/dark excited sectors differ from identity by O(nu^2). Finite fixed local dimensions give a uniform bound
||sqrt(B_h(nu))-Q_h||<=C nu,
||Z_h(nu)-Z_h(0)||_cb<=C nu.
The gauged raw generator changes from its nu=0 value only through an O(kappa nu) local Hamiltonian. Hence every local commutator cross block is O(kappa nu), not O(kappa), in the local relative-animal norm.

A buffered P_X clean block is the legal direct-clock calculation because masks cannot be created by raw resets, Z preserves masks, and all local intermediate supports are inside the buffer. Remote flags remain spectators. One must retain this buffer through each composed local term; using only the bare center star would be insufficient for a gauge-expanded reset.

## 3. Relative form estimate and bad support
For a local commutator term acting on f_A, all factors of f_A outside its physical syndrome/token light cone commute with the term. The inside factors have fixed condition ratio depending only on the bounded number of affected check/token vertices, theta, and token multiplicity R. Since P_X,Q_X commute f_A, the cross estimate gives
±t(P_X M_A Q_X+Q_X M_A P_X)
 <=delta Q_X f_A+C_delta kappa t^2 nu^2 P_X f_A
with the kappa normalization chosen consistently (equivalently rescale the first term by kappa).
The positive bad diagonal block is bounded by C kappa t Q_X f_A. Raw V_ext and raw L_phys V_ext already have their independently supplied negative drift, so these estimates are needed only for the t-commutator correction, not for an uncontrolled raw term.

## 4. Why the completion charge does not introduce W^2
For each bounded local support X and each nearby bad flag j, complete an animal A meeting X by a fixed connected patch joining its point of intersection to the entire R-token bundle at j. The added size is bounded independently of |A| and total volume. The weight ratio and source multiplicity are therefore bounded constants. The target is paid by D_j^bad, conditional on the supplied strict raw-token decrement.

When summing over X, a fixed j belongs to only boundedly many buffered X because the first-order commutator decomposition has bounded local incidence. Thus all Q_X f_A bad-side terms sum to C sum_j D_j^bad, WITHOUT an extra |A| factor. The clean-side Young remainder, by contrast, is summed over X that meet A and therefore contributes exactly one |A| factor, i.e. C t^2 nu^2 W_ext. There is no second sum over distant correction hubs.

The same fixed-patch argument applies to Q_X d_h: d_h is a sum of bounded local animal differences, so only animals meeting h's fixed footprint occur; completing to a nearby bad token bundle has bounded multiplicity and ratio. It pays missing clean service in dirty blocks without treating hypothetical clean updates as actual dirty resets.

## 5. Augmented coverage
AUGMENTED_FLAG_COVERAGE.md's three-way split is valid. Total-sparse animals give the vacuum O(N) term. Flag-dense animals have at least eta|A|/(2R) distinct occupied token bundles and are charged directly to D_bad by completing one such bundle; duplication of flags into R identical bits causes no independence assumption. Remaining animals are syndrome-dense, so the original component-container rich/poor proof applies after enlarging the fixed footprints and its constants. Added occupied tokens cannot worsen completion ratios. Arbitrary flag configurations are never incorrectly subjected to FGL syndrome confinement.

The constants and parameter choices must be recomputed after enlarging footprints and choosing R. In particular the new component cutoff and container expansion constants are not automatically identical to the original data-only values. This is a fixed-geometry adjustment, not a volume dependence.

## 6. Conditional conclusion and limits
Given (i) the actual raw bad-reset operator charge, (ii) the exact monomial gauge/flag identities, and (iii) bounded-depth local credit construction, local surgery gives the desired full physical first-order drift. The finite-depth inverse-circuit remainder is HP, identity-annihilating, and local, so the augmented local-orbit bound costs only C kappa t^2 W_ext. Choosing t sufficiently small compared with nu^2 times the actual augmented coverage constants closes that remainder. The already proved local Stinespring perturbation lemma then applies to the CP-dressed augmented observable.

This audit does not replace a proof of the raw bad-token charge, does not equate dirty reset channels with Phi_h, and does not certify a native two-site implementation. Its conclusion is a conditional validation of the claimed local-surgery interface for the actual simple compiler, not a numerical extrapolation from the 18-dimensional fixture.

## Addendum: the explicit XOR/Pauli gauge earns the raw-charge input
After the preceding audit, MONOMIAL_BAD_RESET_CHARGE.md supplied the missing raw-charge derivation for the explicit simple compiler. I checked that derivation as follows.

On the excited-label space, use
U_exc=(sum_s F_s tensor |s><s|)(sum_s Pi_s tensor X_label^s),
with sufficiently many labels for the complete local consulted syndrome and reference excited label0. Both factors are unitary. The second is a syndrome-controlled label permutation; the first is a label-controlled Pauli. Applied to reference label0, their product yields sum_s F_s Pi_s tensor |s>, the required Stinespring isometry. Both factors normalize the joint syndrome/label diagonal algebra, so the full guarded product does too. Its guard and depth preserve bounded physical support and occupancy.

Each gauged physical reset therefore sends each fixed joint syndrome/label sector to one such sector (up to a degeneracy-space unitary), and exactly one physical reset label is nonzero on that source sector. Thus the raw adjoint preserves the diagonal algebra exactly; no pinching or classical approximation is required.

No physical reset creates a previously zero combined flag: an occupied neighbor of the reset source was already flagged by the illegal edge; a ready neighbor remains ready; a good isolated occupied nonneighbor is unaffected in its physical data/label sector. Its own flag is cleared. Conjugation preserves these exact source-subspace inclusions.

Consequently R>k_reset unary tokens make every bad reset remove at least R-k_reset occupied augmented vertices net, with bounded total flip size. Enlarging the finite local reset footprint to a clique permits direct application of the already proved full-animal monotonicity lemma. Completing any animal containing the h-token bundle by the full actual changed set D has bounded size and preimage multiplicity and a uniform positive weight ratio. This proves the required D_h^bad charge to ALL animals containing the bundle.

Accordingly the raw-charge hypothesis is now earned for the specifically engineered XOR/Pauli monomial simple compiler, subject only to the original SSF/geometry assumptions already stated elsewhere. The surgery audit does not identify a remaining raw bad/bad or good/bad coherence gap. This conclusion is specific to the engineered monomial completion and does not extend automatically to an arbitrary Stinespring completion.
