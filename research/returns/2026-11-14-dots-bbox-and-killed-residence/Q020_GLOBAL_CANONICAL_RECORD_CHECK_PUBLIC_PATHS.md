# Independent check of the global erase/bootstrap/grow construction

This checks geometry, reconstruction and stopping logic. It does NOT independently establish the magnetic contour, strip partition or hole-envelope bounds invoked by the congestion calculation.

## Deterministic classification on a torus
Avoid assigning a boundingbox to an already-winding component. Select original augmented components in a fixed deterministic torus-root order. For each, explore a deterministic connected prefix with integer lifts, stopping as soon as either span reaches400. If exploration exhausts the component first, both spans are<400; no nonzero torus winding can have occurred inside this box because400<L/2. This is an erodable component. If the threshold is reached first, the connected prefix is a valid locally lifted seed, including when the FULL original component winds. Each new adjacent vertex increases either span by at mostone, so the threshold is reached exactly400 and the other span is at most400.

This removes any reliance on a global lift of a winding original component. The root and exploration order need not be separately decoded in the congestion injection: their determinism defines the path; the geometric overwrite record plus S,T recover the initial configuration.

## Full erased history and overwrite reconstruction
Let T be the full union of previously erased ORIGINAL components and x'=x\T. Their original nonadjacency gives exact factorization w(x)=w(T)w(x'), using weights relative to all-minus. At an addition edge let U be the explicitly overwritten region (including any originally-plus scheduled sites), and z the pre-edge configuration. Then

    z outside U = x' outside U,
    S = x' intersect U,
    x = (z outside U) union S union T.

This remains true when T crosses U, or portions of T have been regrown. Factorization is performed in ORIGINAL x, not after restoring T to the current state. Unchanged exterior original spins are retained in z outsideU. There is no unrecorded collection of outside bits.

For a fixed geometric record,U is reconstructed from the old rectangle, extension direction/witness and progress. Multiple compatible original exploration prefixes or marked components only overcount S; they do not require extra hidden spin records. Original prefix vertices form a connected subset of S spanning the bootstrap box; after bootstrap its fixed seed continues to span400columns throughout prewrapgrowth.

## First-hit and edge multiplicity
Check target membership after EVERY nonnull addition, including midrow, before wrapping, and midcolumn. A scheduled already-plus site is a no-op, not a native transition. Erosion cannot reach majority; growth cannot hit all-minus. If no large original component occurs, erosion terminates at all-minus. Otherwise a completed400×L cylinder can be thickened to width800, which guarantees majority, so earlier stopping is always possible.

Every site is deleted at mostonce and added at mostonce: total actual path length<=2n. A phase may not silently omit current across another phase on the same undirected edge; phase currents are summed. The fourphase record envelope is deliberately much larger than the concrete bootstrap16n^3 and prewrap/cylinder4n^2 counts. An additional explorationseedroot is unnecessary for injection because S,T already reconstructx. Even paying an extra factor n would still fit the present10^446 congestion target, but that slack is not a substitute for a valid record mapping.

## Last-row wrapping seam
Do NOT directly replace the partial lastrow configuration by the full periodic cylinder. Cut the periodic seam and retain the planar-strip comparison through height1600. For each seam bond with binary endpoint occupanciesa,b,

    P_open-P_periodic = a+b-|a-b| = 2ab,
    E_periodic = E_open -16 B,

where B counts plus-plus seam bonds. Since S subset U, B(S)<=B(U), hence

    E_periodic(S)-E_periodic(U)
      >= E_open(S)-E_open(U).

Thus the open-boundary deletion ratio is a conservative upper bound during the final partial row. Its opened energy remains bounded by6415.96, and the marked width400 strip estimate through height1600 applies. Only AFTER complete wrap may the full-cylinder partition bound take over. Exterior plus spins separately improve the deletion comparison.

## Physical-time interface
The congestion uses c=w*q with native rate-one-per-site heatbath transitions. Bootstrap additions have at leasttwo plus neighbors; prewrap/cylinder additions have at leastone, including the initial protuberance; all native inverse-rate factors remain explicit. The killed spectral inequality gives a uniform mean-duration bound only after the source note's logarithmic stationary-mass factor is included; no discrete-time n factor is silently removed.

## Executed finite evidence
canonical_global_check.py/json tested2856 randomL9 tori with threshold3, including winding fullcomponents. It checked38100actual transitions,5457original smallcomponent erasures,7383records where erasedT crossedU, and769completedwrap cases. Every reconstruction/factorization, first-hit termination, neighbor-count premise and length<=2n assertion passed.1062paths reachedall-minus and1794majority. Elapsed time was not separately instrumented. These checks support implementation reasoning but do not prove large-system entropy bounds or the complete congestion theorem.

No global reconstruction obstruction was found. The final theorem still depends on independently established static hull/strip/cylinder envelopes and their stated scope.

## Fresh adversarial pass: explicit repairs and stronger bookkeeping
The overwrite progress index must count SCHEDULED positions, including already-plus no-ops, not merely the number of actual flips. Otherwise a decoder might need unknown original spins to recover U. With the prescribed geometry-only row/column fill order, scheduled progress is sufficient and has the stated polynomial bound. Actual path length still counts only nonnull transitions and remains<=2n.

For the last-wraprow seam opening, retain the original seed in the initial<=400-high seed rectangle, away from the selected opening seam. Its horizontal-spanning connected prefix survives opening, even if other original components split. Therefore the marked prewrap partition premise is not lost at wrapping.

A deliberately broader record envelope100n^4 can be used. Anchor n, old dimensions atmostn, witness/local offset atmost2n, scheduled progress atmostn, and32direction/local flags give64n^4 possible bootstrap descriptors. This is a conservative envelope, not a claim that all these choices occur independently. Prewrap/cylinder records fit inside it. Then log[(2n)(100n^4)]<80 atn2560000. With the separately asserted static bounds, bootstrap logload<878+32+1+1+80=992; prewrap<184+8+16+17+1+80=306; cylinder<446+80+17+1+80=624; erosion<944. Summing four phases is strictly belowe1000, with substantial slack. These numbers are CONDITIONAL on the static bounds and must not be presented as an independent proof of them.

No hidden rate correction was found: bootstrapk>=2 yieldsinverseheatbathrate<2<e; growthk>=1 yieldsinverse<1+e15.96<e17; erodek<=2 usesitsdisplayedinversebound. All are physical rate-one-per-site quantities.

If the combined congestion theorem really establishesrho<=e1000, the source spectral lemma gives uniform killed meanM<2.2e7 e1000. With independently certifiedlambda_a<1e-7 andp_core_exit<1e-450, the outside renewal correction is<2.2e-450 e1000 (approximately4.4e-16). The core excess<1.087e-7 then dominates. This would complete a quantitative occupation numerator reduction, NOT compute capacity, establish efficient relative rare-event sampling, or yield a civilization-level capability by itself.
