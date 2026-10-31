# Independent executable calibration review

## Verdict and binding

PASS for the conservative fixed-sample affine-innovation calibrator. I read the complete implementation and test harness, reran all 17 supplied tests, and added/executed independent arithmetic, histogram, recovery and malformed-input checks. No defect was found. This is not an authentication verifier, an empirical validation of the iid mechanism, or an implemented downstream quantum simulation.

Exact sources:
- `calibrate_affine_innovations.py`, SHA-256 `ef36b3b08fc024aa083418ec6aa6c612f749243aa9e42261d3e525772570dc1f`.
- `test_affine_calibration.py`, SHA-256 `9a6bb612e35d85f9e9fe941ea966fa82ad4d409d1bd96f2b294455bf52506fdc`.
- Read scope companion `CALIBRATION_EXECUTABLE_SCOPE.md`, SHA-256 `2dc3e8f9bb1a0f4b5d19bf0e7dba3ef3aafda4070cd1c23d4935c77035af9f76`.

The mathematical receiver remains the separately reviewed 14,390-byte source SHA `546c90eb5e3efc087e4dc90d559017623772c6f426bdf58c20ccdbddba3172bf`. This executable implements a more conservative rational sufficient confidence schedule, not the exact logarithmic radius formula.

## Actual code checks

The public `calibrate` entry validates square invertible integer-bit F, injective G with 1<=k<=n, integer offset, and controllability. It computes the first full-rank horizon by successively concatenating G,FG,...; this is polynomial binary arithmetic. Row-matrix/low-bit label orientation is consistent. General redundant or zero-noise coordinate laws are rejected rather than assigned an invalid eta equality.

Each supplied pair has two exact n-bit integer labels. The residual y+Fx+beta is decoded by elimination over G. Because mechanism validation established column independence, a pivot exists at each recovery step; remaining inconsistent equations detect residuals outside im G. A malformed externally supplied G to the low-level helper is not a separate public calibrated interface.

Budgets use exact integers, rational strings or Fraction values, rejecting binary floats and booleans. N is a positive integer; p_slots is a nonnegative integer; radius and model tolerance are positive, delta is in (0,1), and b,T are nonnegative. The confidence exponent is the least j with 2^-j<=delta, using integer comparisons and boundary corrections rather than floating logarithms.

The guard N radius^2>=2(D+j), D=2^k, implies the required sign-union error bound: writing x=N radius^2/2, e^-x<=2^-floor(x), so 2^D e^-x<=2^-j<=delta. The integer ceiling and equality boundary are safe. It is deliberately stronger than a condition using ln 2, not an incorrect substitution of logarithm bases.

The sparse histogram computes observed-symbol absolute deviations exactly and adds (D-number_observed)/D for missing symbols. The result is exactly ||p_hat-u||_1, including zero counts. Upper=min(2,eta_hat+radius) and the target min(1/(4m),epsilon_model/C) are rational. PASS includes equality and implies the deterministic theorem's requirements on the single good statistical event. `model_error_upper_if_good` is populated only on PASS, and `model_promise_verified` is always false.

## Statistical and interface limits

The code checks that exactly N pairs were supplied; it cannot prove N or budgets were chosen before observation, that every clock event was recorded, or that observations have the claimed iid law. A caller can select data, repeatedly run the routine until PASS, or submit a change-only list of the correct length. Those operations do not gain the stated confidence merely because the routine executes. The scope companion expressly states these historical/protocol obligations and the need for a separate confidence allocation under repeated testing. `trajectory_pairs` constructs adjacent pairs only; it is not a detector of missed events.

No verifier for a saved result object is implemented. Mutating an output dictionary does not create a new certified statistic; a consumer must rerun the routine on the actual mechanism, data and budgets or provide a separately earned record-verification layer. The current function returns computed results, not a signed/authenticated certificate. This is not a defect under its declared API, but packaging must not describe it as a tamper-proof output verifier.

The supplied balanced one-bit transcript has positive probability under p=(9/10,1/10), despite that law lying outside the accepted eta target. Its PASS is intentionally retained. It illustrates permitted rare false acceptance, not posterior model truth. The code's statement of unconditional training confidence and false model-promise flag are correct. The supplied b, exact centering, known clock, and downstream control algebra are not verified here.

## Executed independent evidence

All 17 supplied tests passed, including exact thresholds, insufficient N, controllability, off-image data, all-tick self-loops, exhaustive small injective recovery and the rare misleading PASS example.

Independent script `test_calibration_independent.py` has SHA-256 `04dcba9e8342b790b0209ebb93236dcf896948e506492a2e50c71df289afdd0e`; result `calibration_independent_checks.json` has SHA-256 `0257a7ff5b81ecd31300e3ae96bff035976dd5c24744d5bb6502e10c203b3031`. It passed:
- 11,041 exact confidence-exponent checks, including 1,000-bit dyadic boundaries;
- 62 malformed public-input cases rejected;
- 60 sparse-versus-dense histogram comparisons with random complete affine pairs and offsets;
- 1,558 valid recoveries and 216 off-image rejections across all full-column-rank matrices through n=3;
- all four conservative cost rows checked for both sufficiency and minimal integer ceiling under their stated guard;
- no mutation of caller inputs.

These are finite checks supplementing the algebraic proof, not empirical confirmation of arbitrary sampling promises.

## Cost and consequence

The implementation uses polynomial mechanism/recovery arithmetic per supplied record and sparse histogram storage; it does not enumerate all 2^n source states or all 2^D sign tests. It nevertheless processes the full explicit N-record input. It is not a streaming sampler, hardware observer or compact verifier of an unobserved giant dataset.

The read and independently checked cost file `calibration_sample_cost_examples.json`, SHA-256 `d64fb369b53b88a9236e7d29d7e5d446536027531762f87f41e4d7c61181d07e`, gives 489,982,526 sufficient records even in its first m=k=1, b^2 T=0.01, epsilon_model=0.1 example. Larger displayed examples reach billions and beyond. These are conservative sufficient bounds, not lower bounds or demonstrated throughput. They make practical acquisition efficiency emphatically unearned; inverse-square calibration cost can dominate the later logarithmic numerical-precision overhead.

Final scope: reviewed executable arithmetic for one fixed-N statistical protocol under a known affine mechanism, composing with the separate mathematical robustness theorem. No new general learner, truth validator, optional-stopping guarantee, quantum simulator, practical advantage or novelty claim. Frozen author sources were not edited.
