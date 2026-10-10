# Uniform PPT powers and bistochastic sequences

9 October 2026. Integrated research edition preserving the earlier theorem, its finite mapping-cone criterion, and the new arbitrary-map criterion. These are proof candidates with focused internal mathematical checks. Formal verification, external certification and priority are not established.

## Main results and limits

1. For each fixed d, every PPT completely positive map on M_d has an entanglement-breaking power at one common finite exponent N(d). The more general theorem applies to any closed convex semialgebraic CP mapping cone whose every member has some finite EB power. Non-trace-preserving maps are included.
2. For a CP mapping cone, eventual EB of every member is equivalent to the vanishing of every invariant-corner cross transfer. This gives a finite exact algebraic test for algebraically presented semialgebraic cones, and a terminating search for the common exponent after a positive test.
3. For an arbitrary CP map Phi on M_d, put L=lcm(1,...,d). Eventual EB is equivalent to nilpotence of the cross transfer at every proper invariant corner of Phi^L. Testing its d^2-th power gives one finite real-algebraic criterion. Exact algebraic input can therefore be decided, with an algebraic negative certificate or a terminating least-index search on a positive answer.
4. A negative certificate can be converted into one fixed pure qubit-ancilla input whose output is NPT at every serial iterate. This supplement preserves the reviewed core unchanged. Entanglement may decay to zero, so it gives no robust storage or positive-capacity guarantee.

5. New in this edition: for each fixed d, every sufficiently long arbitrary serial word of bistochastic PPT channels is EB. Both unitality and trace preservation are required for every factor. This is a newly completed proof candidate, developed after the preserved reviews; it has not received an additional independent review.

No PPT-square result, practical numerical exponent, efficient algorithm, noisy-tomography classifier, tensor-power distillability result or unrestricted nonunital nonstationary-composition theorem is claimed. The earlier common-power theorem and the new bistochastic word theorem have distinct scopes.

## Reading order

- filter_closed_uniformity/FULL_SEMIALGEBRAIC_MAPPING_CONE_UNIFORMIZATION.md is the complete uniform-power proof and PPT corollary. Its WHOLE_CLAIM_REVIEW.md preserves the focused check, including the pointwise PPT input chain.
- filter_closed_uniformity/FINITE_OBSTRUCTION_AND_DECIDABILITY.md is the mapping-cone finite criterion. Its supporting boundary and source records are included.
- general_cp_eventual_eb/FINITE_CRITERION.md is the arbitrary-map theorem. FINITE_CRITERION_REVIEW.md preserves the targeted continuation of the same mathematical review. It checks Sections 1–4; source comparison and later scope consequences are identified separately.
- general_cp_eventual_eb/FIXED_PURE_QUBIT_WITNESS.md proves the later pure-input refinement. NONFAITHFUL_BOUNDARY_EXAMPLE.md gives a rational qutrit family showing exact-input discontinuity.
- nonstationary_ppt/BISTOCHASTIC_VARYING_WORD_THEOREM.md contains the new full sequence proof. Its load-bearing steps are a moving-support rank plateau, a largest-margin anchor usable from either direction, and the published transitive-space product theorem. BISTOCHASTIC_PRIMARY_COMPARISON.md and NONSTATIONARY_SOURCE_PROVENANCE.md credit the exact inputs.
- nonstationary_ppt/MOVING_SUPPORT_AND_NORMALIZATION.md preserves the rectangular positive split and the exact same-dimension equivalence of unrestricted CP and CPTP word bounds. Neither removes the nonunital gap.
- nonstationary_ppt/COMPACT_SEMIALGEBRAIC_NIL_COUNTEREXAMPLE.md closes one tempting abstract shortcut for the unrestricted varying-sequence gate. It is not a CP-channel counterexample. The convex bilinear square-zero barrier explains why its nonlinear product cannot simply be copied into convex algebra coordinates.

Primary-source comparisons are deliberately narrow. Park arXiv:2608.13551v2 Section 1.2 explicitly leaves a map-independent bound open. The arbitrary-map comparison distinguishes faithful-channel, unital-channel, restricted-zero-eigenspace and qubit results. Source versions, inspected locations and downloaded-byte hashes are recorded; no third-party full texts are bundled.

## Reproduction and preservation

Run the Python scripts in their respective folders. NumPy is needed for verify_kraus_word_bootstrap.py; SymPy is needed for the two general_cp_eventual_eb scripts; verify_nil_semigroup.py uses only the standard library. The new verify_bistochastic_anchors.py uses NumPy and checks 9 unequal-word cases containing 482 Kraus words, including the explicit positive decompositions for both anchor directions. Saved JSON results preserve the bounded checks and their limitations. None is a numerical substitute for a universal proof.

PACKAGE_VALIDATION.json records the checks performed while assembling this edition. MANIFEST.json gives SHA-256 and byte counts for every other bundled file. The reviewed arbitrary-map core retains SHA-256 1437f7755136344d1261ee7768b6ede48670dd744c9890e27b1c619f3007ae78. Both review reports are copied byte-for-byte. References in them to privately retained source PDFs identify provenance; those PDFs are intentionally absent.
