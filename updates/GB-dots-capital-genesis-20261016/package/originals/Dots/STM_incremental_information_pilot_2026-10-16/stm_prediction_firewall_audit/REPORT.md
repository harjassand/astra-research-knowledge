# Independent STM phase-one predictive-firewall audit

Date: 2026-10-16 UTC

## Decision

**PASS for phase-one training and development selection using the unchanged submitted code below, subject to root authorization.** No implementation correction was required. This is **not permission or a PASS for held-out evaluation**. The held-out evaluator is intentionally outside this phase and has not been reviewed or executed.

The numerical estimand is prediction of recorded image-localization labels on the compatible serialized-new-image proxy subset. Interpretation as endpoint information immediately before already-triggered physical scans remains conditional on documented logger timing/freshness semantics. This audit neither proves physical freshness nor validates current gain, d as elapsed time, complete physical action logging, scan savings, or safety.

## Access boundary and preservation

Read frozen PROTOCOL_v1.1.md, submitted audit/features/train source and tests, hardened-reader definitions, and audit-only gate metadata. Used diagnostic episode 00000 exclusively as an inert schema template through safe_reader, replacing its image grids, coordinates, actions, currents, d, states, rewards and terminal flags with synthetic values in original tests. No newly acquired episode contents, test labels, test outcomes, test distributions, plots, or examples were read. Test-label files were inspected through filesystem metadata only, not opened. No active implementation file was edited and no downloads were performed.

Preserved submitted source is in `submitted/`. Audited SHA-256:

- audit.py: 4747c982b688cabad721d64a1e57ee11f55d45a5aa47b5628073df17f868c100
- features.py: 31aaeb869f66217c76db6c734231cfe231b3d640236b203235684df48535950d
- train.py: 7c36cbe6bd793fdb60b41fb53650088158789b6366f07c58efe3d70d0a767450

Active hashes were rechecked after tests and remained identical. This is a code/synthetic audit, not independent replication of the selected-episode compatibility audit.

## Checks and evidence

### Feature whitelist and timing: PASS

The builder exports only p, g-minus-p, prior measured disagreement and history. History contains only executed six-action vectors, stored start/end requests, d and current. Routing is separate. The feature function directly reads these fields and does not receive an info/state object wholesale. Both continuous targets use identical inputs.

p and prior disagreement update only after the current row is assembled and labeled. Same-row new coordinates change labels but leave current predictors unchanged. The same coordinates legitimately become the next interval's anchor. Current-row forward/back disagreement is not a feature; prior measured disagreement is. Goal is reset-defined, with no cross-episode stitching.

All fixed maps match the frozen formulas and ordering: 382 shared A inputs, 457 A+C inputs, 585 A+F inputs; float64; linear quantiles; population standard deviation; complete action aggregates and B16; latest/aggregate/concatenated d summaries; signed current numerical nA; unscaled-MAD descriptors; trace-length-normalized spike counts; per-trace normalization before concatenation. d is nonnegative radial displacement, not cumulative travel; nonmonotone traces are accepted. No feature learning occurs.

### Prefix preservation and anchor recovery: PASS

Original tests construct two reused-image steps followed by a fresh boundary, then a reused step and a fresh boundary. Rows retain histories of lengths 3 and 2 and use the correct preceding measured positions. Changing an early current changes current arms while preserving A; changing early d changes the shared A prefix identically across arms. Missing-trace and ambiguous/copied-boundary mutations suppress dependent rows, then establish a new measured anchor before subsequent rows become eligible. History resets only at recognized boundaries or invalid intervals; it is not truncated to latest action.

### Prohibited inputs: PASS

Original builder tests vary rewards, state, next-state, post-scan destination distance and routing IDs without changing feature records. Extending a synthetic episode beyond an earlier scan leaves that earlier row and label unchanged. Same-row label mutations and previous-row anchor mutations have the expected clock-specific effects. Submitted tests additionally inject all enumerated prohibited keys, including terminal fields, done, images, image extents, future length/actions, episode/time/regime IDs, hashes, audit flags, label values and post-scan disagreement; resulting features remain identical.

The auditor does inspect schema/normal-completion flags and future image identity/hash consistency for eligibility, as distinct from predictors. The whole-episode compatibility gate intentionally rejects malformed or contradictory records. No schema exclusions occurred in the reported selected corpus, so its normal-completion validation removed no selected episode. Audit-only information is not passed into model matrices. This does not remove the protocol's explicitly acknowledged proxy-subset selection limitation.

### Equal inputs, weights, budgets, choices and selection: PASS

Every arm receives bit-identical A including every d summary and trace-length descriptor. Finite-current validation is shared across arms; current values do not change A. All nine fitted candidates use the same train rows, normalized inverse eligible-row-count episode weights, estimator settings and seeds. One ExtraTrees model predicts both coordinates; the HGB choice fits two independently modeled coordinates with the same hyperparameters and weights. Those two coordinate estimators are one candidate choice, not a second selection opportunity.

There are exactly three candidates per arm and two deterministic baselines. No extra real-data seed, fit, transform, classifier, stack or sweep is introduced. Development selection minimizes macro-episode Euclidean endpoint error; ties within 1e-9 select the predeclared candidate order. No development refitting exists. The empirical radius uses development episode maxima and linear 90th percentile. Baseline requested endpoint equals latest end_nm, not summed requests or endpoint minus start.

Original synthetic unequal-episode tests verify equal total episode training weights and macro rather than pooled selection weighting, including tie-boundary behavior. Synthetic fitting for serializer tests does not use pilot outcomes and does not constitute additional pilot model choices.

### Numeric snapshots: PASS at implementation level

ExtraTrees snapshots explicitly reproduce sklearn's float32 predictor conversion before threshold traversal and accumulate stored numerical leaf values. HGB snapshots use numerical thresholds and leaf values, coordinate baselines and predictor order. Inputs must be finite; no missing or categorical route is required by this protocol. JSON round trips are nonexecutable and do not use pickle.

Independent tests probe random synthetic out-of-sample inputs plus exact internal thresholds, adjacent float64 representable values on both sides, and float32-rounded thresholds. ExtraTrees and HGB original-vs-frozen predictions agree at rtol=atol=1e-12. Submitted synthetic roundtrip tests also pass. Production train.py checks each actual candidate against its frozen snapshot on development before saving it; an exception stops the run without substitution. Production fits were not yet performed during this audit, so their successful checks and final immutable lock remain completion evidence for phase one.

### Seal and sequence: PASS for phase one only; later evaluator pending

The test label directory is mode0700 and label file mode0400. Modeling load_split rejects anything other than train/development before file access. Test labels are outside the sanitized input directory. The code contains no test-loading/scoring entry point. This is procedural and write protection, not cryptographic or separate-OS-user isolation: the same account can technically read the file, so the no-access instruction remains essential.

Training requires the explicit root-approval token and audit report path; orchestration must supply approval only after the reviewed gate is PASS. Each fit output directory must be empty; model files and lock files use exclusive creation. The final lock records schema hash, code hashes, candidate parameters, selected candidates, development radii, model hashes, input hashes, versions, protocol hash and audit-report hash. The training code records the audit-report digest rather than independently enforcing every gate; that enforcement is owned by the root-approved audited workflow.

Before any held-out use: verify final successful fit lock and unchanged code/model/schema hashes; review a one-use evaluator, its authority boundary, fixed three-block membership, classification support gating, all five selected/baseline metrics and same-hyperparameter comparisons, and refusal to overwrite/retry a burned result without explicit invalidation/amendment. No PASS for these unimplemented or unreviewed evaluation steps is implied here.

## Eligibility metadata reviewed

The recorded audit status is PASS; no systemic schema failure and no schema exclusions. Eligible train:120 episodes/384 boundaries; development:39/72; test:60/100. Development episode1501 was excluded because its shared-image component touches burned episode1500. These are permitted audit counts, not scores. The exact-hash connected-component implementation includes both image directions, transitive links and excluded-schema graphs; it keeps earliest within-split duplicates and excludes burned/cross-split components.

## Test record

- Original independent test suite:10/10 PASS (`test_independent_firewall.py`, `test_results.txt`).
- Preserved submitted feature/training suite:12/12 PASS (`submitted_features_results.txt`).
- Initial construction-only test failure was an auditor fixture dtype mismatch: float64 bytes were initially placed in float32 template nodes. Fixed the synthetic helper to preserve each inert node's dtype. No submitted code was altered, no pilot result was evaluated, and no failure was hidden by changing the implementation.

No mathematical feature-leakage blocker was found in the audited phase-one code. Physical scan semantics remain the frozen protocol's explicit conditional interpretation.
