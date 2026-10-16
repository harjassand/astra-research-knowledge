# Selected-endpoint readout-sensitivity diagnostic

## Result

The selected equal-check-rate Toom endpoint previously labeled a failure becomes a success under BOTH predeclared alternative syndrome-only recoveries. The sweep endpoint remains a success with an identical recovery under all three policies. This establishes recovery-policy dependence of this selected comparison; it does not establish a memory-method advantage, an unbiased failure probability, a threshold, or irreversible logical information loss.

Only two prescribed trajectories were replayed: L=32, alpha=0.001, T=5, seed=101, sweep beta=1 and Poisson-Toom beta=4. Both reproduced EVERY legacy nontiming output field before any alternative readout was evaluated. The accumulated error E and exact syndrome S were then persisted. Each decoder subprocess received S only; E was used later to score the selected recovery. No extra seeds, times or parameter choices were searched.

| Endpoint | Decoder | Global fallback | Logical mask | Recovery faces | Closed residual faces |
|---|---|---:|---:|---:|---:|
|Sweep beta1|D0|No|0|6858|1140|
|Sweep beta1|D1|No|0|6858|1140|
|Sweep beta1|D2|No|0|6858|1140|
|Toom beta4|D0|Yes|7|387336|389582|
|Toom beta4|D1|Yes, unresolved union only|0|10858|3338|
|Toom beta4|D2|No|0|10654|3134|

Mask7 means three nonzero homology coordinates under frozen D0. Every listed recovery satisfies boundary(R)=S, and every scored E+R is closed. The D1 result is especially informative: retaining already-valid strict local fills and applying the SAME tensor fallback only to the combined unresolved syndrome eliminates the selected failure, without enlarging the strict local cutoff.

Independent extraction of the lone strict-ineligible Toom component finds 16 edges, 15 vertices, a consistent lift, and per-axis spans/wrapped diameters [1,1,2,4]. The strict L/8=4 rule excludes equality at 4; D2 accepts this injective box. Thus the switch was caused by a small width-4 component, not macroscopic winding. D1 still invokes fallback for that component alone and succeeds. Details: phase4_ineligible_geometry.json.

## Policies fixed before replay

D0 is unchanged: if every syndrome component has a consistent lift and strict ambient wrapped infinity diameter<L/8, fill each by the deterministic box prism; otherwise discard partial fills and apply H to the whole syndrome.

D1 uses exactly the D0 component eligibility test and exactly the same local prism, but retains eligible component fillings. It applies H once to the UNION of all unresolved components. Individually winding components must remain combined: they may bound jointly while neither bounds alone.

D2 uses the same component traversal, integer lift and local prism. A component qualifies if its lift is consistent and each vertex-coordinate span max−min is strictly less than L, so its coordinate box injects into the torus. It applies H once to the union of remaining components. It does not choose among recoveries using E, previous homology, trajectory history or success scores.

For both alternatives, removing already-filled component boundaries from total S leaves a boundary, so H can fill the combined remainder. All-strict-eligible inputs produce exactly the same recovery as D0. Thus these alternatives agree with D0 on the original certificate's good-case inputs; extending a complete theorem statement beyond this agreement remains a separate proof-review question.

## Validation

- Independent release gate passed before replay: 181 direct D0/D1/D2 cases, 5150 D0 regression cases, plus source review of component eligibility and combined fallback.
- A separate deterministic harness exhausts 786432 D1/D2 single-face cases at L16, including every periodic seam, verifies exact equality with D0, recovery boundary and zero residual homology.
- The original selftests pass in the instrumented binary. No geometry, physical dynamics, RNG, rate or D0 logical-scoring change was introduced.
- Both replay records match every prior nontiming field before alternatives. D0 readout scores also reproduce the saved trajectory scores.
- Independent Python boundary/scoring code checks persisted E,S,R after each recovery; the decoder executable additionally asserts boundary(R)=S. A separate verifier then checked all persisted hashes, boundaries and logical parities for all six recoveries at cuts 0, 1 and 31; all passed.

The source and binary are separate simulator_readouts.cpp and simulator_readouts. Original source/binaries and all prior raw results are preserved. readouts.patch records the precise instrumentation/policy diff. PHASE4_SHA256SUMS pins the new source/binary; PHASE4_ENDPOINT_SHA256SUMS pins both exact endpoints and all six recovery artifacts.

## Resources and reproducibility

Exactly two replays and six readout evaluations completed in6.0757 aggregate CPU seconds (runner plus children),6.0705 wall seconds. Maximum child RSS was108268KiB (105.7MiB), runner RSS83100KiB (81.2MiB), under the45CPU-second cap and1GiB per-process address-space limit. Even their separate high-water sum is below1GiB. No cap, schema or invariant failure occurred.

phase4_manifest.json freezes the selection, policies, caps and model scope. phase4_legacy_regression.json records the matched legacy fields. phase4_replays.jsonl, phase4_readout_results.json and phase4_resources.json contain raw outputs. Versioned sparse endpoint/recovery JSON artifacts specify geometry and index ordering. run_phase4.py reproduces the exact selected diagnostic after gate/hash verification and overwrites only phase4 output artifacts.

This is a SELECTED FAILED-ENDPOINT diagnostic, not a random sample for estimating performance. Do not replace the historical phase3 D0 failure count with these selected outcomes or pool them as independent trials. The model is still an ideal instantaneous Pauli process with perfect final readout; this says nothing about finite coherent gates, shared baths, reservoir engineering or a perturbed-generator theorem. No additional experiment follows automatically.
