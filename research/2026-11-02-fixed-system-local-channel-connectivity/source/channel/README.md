# Local-channel connectivity of the 3D thermal-code region

1 November2026. Internally reviewed specified-state result, with explicit channel resources and limits.

## Strongest completed statement
For the actual recursive 3D memory code, an open low-temperature domain of sufficiently weak generic quantum perturbations is connected in both directions to the normalized ground-code projector P0/2 by physical local CPTP BLOCK circuits. Their total causal range is polylogarithmic for fixed inverse-polynomial accuracy. Individual gates have approximate local reverses on the specified source states, with the corrected accumulated-error bound.

This is a statement about local structure and state conversion, not another simulator constant. It is not a full phase classification: separation from product-state phases, a complete invariant classification, and full MKS all-annulus exponential clustering are not established here.

The ground-connection theorem is MEMORY ONLY. Finite-temperature endpoint connectivity has a separately stated bounded-density qubit-bath extension. No arbitrary bath dimension, inaccessible reservoir or unbounded-density layout is silently included.

## How the physical-resource gap was repaired
The first construction retained polylogarithmically many Poisson-record bits per root. That is useful mathematically but is not bounded-density ancillary hardware on the unchanged lattice. The independent audit rejected that stronger interpretation.

The final proof uses those independent records ONLY to establish physical restricted covariance bounds. It then extends the Ma–Khemani–Sang local-variation argument with microscopic perturbation cores. Each final gate erases and recovers an actual physical data block using its target-state Petz map, with fresh disposable environment inside that gate. No persistent growing work register remains between gates.

The commuting cooling leg reaches beta_max=O(log(N/epsilon)); elementary syndrome counting and contractivity then replace the cold Gibbs state by P0/2. Generic noncommuting perturbations are removed before this cooling step, so no finite-temperature weak-V theorem is extrapolated to beta→infinity.

## Costs and error floors
- These are standard local BLOCK-channel maps, not a claim of polylogarithmic native elementary-gate runtime.
- Target marginals are not free oracles. Offline construction may use the independently earned ideal encoder plus tomography, with consistent full-rank estimates and charged conditioning/precision. The conservative cost is exp(polylog(N/epsilon)).
- This locality result is distinct from the earlier POLYNOMIAL global ideal thermal encoder. Neither complexity claim should be substituted for the other.
- If G counts local recovery block gates, endpoint error is O(epsilon+G eta_n); common-layer local-reversibility error is O(epsilon+G² eta_n). G does not count elementary synthesis gates.
- Offline state-source error includes its full intrinsic floor beta N eta_n+sqrt(delta_tw,n)+delta_tw,n, and must be below the tomography tolerance. All cutoff/finite-size conditions remain explicit.
- Fresh ancillas, erasure and entropy export are allowed resources of the channel model. The maps are not autonomous energy-conserving hardware.

## Logical and physical limits
The new maps provide SPECIFIED-STATE connectivity and local reversibility. Their encoding frame is not automatically the fixed-decoder thermal-overwrite frame used in the exact-H lifetime theorem. No lifetime transfer to these new maps is claimed without that comparison. The earlier ideal encoder retains its own separately proved reference-safe logical guarantee.

Generic noisy physical preparation/release/readout remains open. This result does not contradict the driven energy counterexample: local phase conversion may use controls and entropy export, and phase connectivity is not immunity to arbitrary nonthermal driving.

## Read first
1. FIXED_SYSTEM_MKS_REPAIR.md: corrected standard-system proof.
2. INDEPENDENT_FIXED_SYSTEM_REPAIR_AUDIT.md: final diff/hash binding and corrections.
3. auxiliary/: earlier enlarged-work representation, physical geometry/covariance derivations and the audit that found its resource gap.
4. prerequisites/ideal_encoder/: the independently reviewed code, host gap, sampler and filtered-parent ingredients.
5. tests/root_petz_and_layer_checks.py: finite channel-plumbing checks, not an actual-code phase simulation.

The test confirms consistency-based Petz trace preservation and the reduced-state conditioning bound. It also exhibits the common-prefix error that motivated the G² local-reversibility correction: disjoint channels can erase a correlation, so a sequential-prefix estimate cannot simply be pulled backward by commutation.

## Predecessors and interpretation
Ma–Khemani–Sang supplies the local-interaction-variation/recovery framework; Xun–Cao–Watanabe supplies closely related classical-gauge local-channel architecture and Poisson-record machinery. The actual entangled quantum-code binding, physical correlation input and corrected fixed-system construction are the content assessed here. Source links and conditions are retained in the proofs; no exhaustive novelty or priority claim is made.

This is additional scientific understanding of the constructed thermal region. It is not a usable quantum memory, experimental demonstration, peer-reviewed result, favourable hardware threshold or civilisation-level breakthrough.
