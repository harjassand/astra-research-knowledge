# Independent selected-endpoint readout-sensitivity audit

## Scope

A separate instrumentation/readout version; old dynamics versions and prior results are immutable. Only the two selected L32,alpha.001,T5,seed101 endpoints may be replayed: sweep beta1 and Toom beta4. The selection follows observed failure, so this is a diagnostic, not an unbiased performance experiment or permitted seed search.

## Source review

Diff readouts.patch leaves event evolution, random streams and rates unchanged. Endpoint persistence happens after the final independently gathered syndrome check, before D0 recovery. JSON format4d-memory-endpoint-v1 records L,kappa,alpha,T,seed,method,beta,index convention and sparse E/S. Recovery accepts only geometry, syndrome and frozen policy; the hidden chain E is used solely by separate post-recovery scoring. Persisted files require content hashes and independent E-boundary validation after replay.

D0 preserves the original all-or-nothing fallback. D1 retains each strict-local filling and applies H once to the COMBINED unresolved syndrome. That combined syndrome is a boundary because the original S is a boundary and each removed local component has its explicit filling. It is therefore valid to apply H jointly even if individual unresolved components have winding.

D2 uses the same prism but allows a component only when its integer vertex lift is consistent and max−min<L in EVERY coordinate. These conditions make the full coordinate box injective in the periodic lattice. They exclude winding cycles and over-wide boxes separately; using wrapped diameter alone would not suffice. The remaining components are combined before H, as in D1. On all-strict-eligible inputs all three policies use identical local fills.

None of these policies is minimum-weight or maximum-likelihood. D2 defines an intentionally different final decoder; it does not alter the actual trajectory or retrospectively rewrite earlier results.

## Frozen phase4 hashes

Source90b056735e1a8ce1c8fcc8ffdcf5afb2129a40c5170010f0834514e96d89ef34.
Executabled8446b68cca4c6a9b9d44b743dff0ec5d3d9cebe4cb34f0fe83421ae9702b0c6.

## Deterministic test results

181 external cases PASS: independent recovery-boundary checks for all policies, strict-eligible equality, wide seam-crossing contractible disks, winding-loop pairs plus disjoint local components, preservation of local fills, and rejection of a consistent staircase component with lift span>=L.

D0 full external suite PASS on5,150 cases. The builder standalone harness passes786,432 D1/D2 single-face cases atL16, including seams and exact equality withD0. The replay runner was reviewed: both original non-timing endpoint records must match before any alternative evaluation; each decoder process receives onlyS; persistedE is checked and scored separately.

## Gate PASS:2026-10-15 21:07 UTC

Approve only the two named replays and their six frozen readout evaluations, under45CPU seconds/1GiB. No further seeds or parameter search. Source/binary hashes and all older hashes are pinned; verify endpoint/recovery content hashes after completion. Replay comparison remains a prerequisite to alternative evaluation, not a claim already established before replay.

## Completed diagnostic:2026-10-15 21:09 UTC

Both authorized replays match every pre-existing non-timing field before alternative evaluation. Two replays and six readouts completed in6.07567 aggregate CPU seconds, with108,268KiB maximum child RSS and83,100KiB runner maximum RSS, below the stated45CPU-second/1GiB limits. All six original/new source and binary hashes rechecked unchanged.

Independent tuple-cell verification of persisted files confirms all content hashes, boundary(E)=S for both endpoints, boundary(R)=S for all six recoveries, and closed residual homology matching reported scores at three different cuts0,1,31. Results: sweep is success underD0/D1/D2 with the same6,858-face recovery. Toom is failure(mask7) underD0, success(mask0) underD1 andD2. D1 still uses fallback but only for combined unresolved components; D2 uses no fallback on this endpoint.

Independent component extraction finds8,733 Toom syndrome components and exactly one strict-ineligible component:16edges,15vertices, consistent integer lift, coordinate diameters and lift spans[1,1,2,4]. Its diameter equals the strict cutoffL/8=4; it has no winding and its injective box is accepted byD2. Thus the D0 full-syndrome fallback was triggered by a small contractible component at the boundary of the preset cutoff.

This is a concrete final-readout sensitivity diagnosis, not an unbiased new failure probability, evidence of intrinsic information loss, a performance ranking, or a changed claim about coherent errors. Prior raw results remain valid for their originally fixedD0 policy and are not rewritten.
