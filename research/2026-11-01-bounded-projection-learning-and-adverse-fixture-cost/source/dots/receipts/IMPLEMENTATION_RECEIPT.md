# Independent scientific implementation receipt — 2026-11-01

## Reviewed bytes

- `bounded_projection_receiver.py`: SHA256 e7bdd3f4e7a5ccca0aef6a0469ec7a5b5c00dd47139b73fd208bbc54f79b8fdf
- `test_bounded_projection_receiver.py`: SHA256 33582c789f7b70e381024a5990d8aa3384c43e65c426bbea50ae15fe8896c744
- Shared exact-arithmetic and binary-adapter helpers in `receiver.py`: SHA256 0239083a1841439c1909278b1d54f61dd2135d6e1c02031472e2216d9ffd6d0d

Compared against main construction 4dd9265425b1ef0f78c487602c63e6cd8d78b429c1cf7bc67155981e8ad1632f, rounded solver 972ee67b866093f791d11e8081d379bbdf27037f80549b92c8d29d690ca3640b, and binary scheduler 10cb212745356dff1f6b2d06a78fc26ad45979c3d87eaa1e6d0ba1b7fa7d217f.

## Result

No scientific correctness bug or unearned hidden-vector access found in this bounded review. Ran `python test_bounded_projection_receiver.py` in the construction directory: **all seven tests passed**. This is independent execution/review of constructor-authored tests, not a claim that those tests were independently designed.

## Formula and interface checks

1. The receiver accesses its adapter only through scalar Gram-pair means. Hidden fixture coordinates occur in the test oracle and validation, not in prediction, proposal generation, witness choice, or acceptance. No general readout is requested.
2. Dictionary successor descriptors append the action on the right, matching v_(wa)=T_a v_w. Reverse dual order is explicitly `adjoints[a] for a in reversed(word)`. Correction uses backward state at l-i, and residual products use exactly the first l-i dual residuals.
3. PSD-repaired `A=Ghat+m alpha I` is used for convex projection only. The residual quadratic and DWR correction correctly use RAW `G`, `K`, `HH`, with inflation 4B^2 alpha. The data certificate is (B+2lB^2)alpha. Root enclosures are outward exact rational, with the prescribed eta; the empty word uses its raw self-return. Output clipping is sound.
4. `_witness` scans only forward/reverse-adjoint prefixes, skips existing and repeated candidate descriptors, and uses repaired-objective value minus EXACT empirical FW gap minus (B+4)B^2 alpha. It retains only a lower bound exceeding lambda/2. The public request loop rejects duplicates and enforces the finite descriptor ceiling independently of data.
5. Precision b, alpha, W/W1/E/Jmax, beta and per-job failure allocation match the scheduler. Required shot counts use the identical integer-log formula. Canonical unordered-pair keys include the precision epoch. Shared cached means impose symmetry exactly; unchanged epochs do not resample old pairs. The rank-three test crosses a precision epoch and verifies common shot denominators and pair/epoch uniqueness.
6. The generic optimizer uses the specified rounded fixed step, exact signed l1-ball linear oracle, fixed dyadic grid, exact recomputed FW gap, and explicit cap. Toward-zero rounding and the final feasibility check preserve the coefficient ball. The exact Schur PSD helper correctly handles zero pivots; `sqrt_upper` uses exact integer square roots and outward dyadic rounding.
7. Optional active-face proposals are restricted to m<=4. They use ONLY acquired scalar matrices and vectors, with a constant-size enumeration and rational linear solves. A proposal is rounded to the same grid and accepted ONLY if its independently recomputed exact FW gap is <=delta. Therefore correctness does not rely on the proposal solver finding the true optimum. An unsuccessful feasible proposal may initialize the fallback instead of zero; the full-domain objective-range descent/cap proof remains valid from any feasible grid point. Constant-size inversion here is a numerical proposal mechanism, not an assumption of a well-conditioned hidden basis or a new inverse-Gram source-precision requirement.
8. Source failures, invalid means, failed PSD/radicand/gap/cap conditions, absent witnesses, and budget refusals latch permanently through the public request path. Subsequent requests fail before new source calls. Binary calibration checks the entire required episode budget before starting a mean. The optimizer likewise refuses an unaffordable proof cap before executing fallback steps.

## What execution establishes—and does not

The three end-to-end scientific fixtures used **validated emulated scalar means** lying within their prescribed entrywise tolerances and on attainable common n-shot binary grids. They executed ZERO physical episodes and did not draw their theoretical sample budgets. They reached dictionaries of sizes 2, 2, and 3, using 27, 18, and 66 emulated means respectively. Tests checked actual scalar error against the certificate, retained expansion, repeated-task reuse, an additional unseen task without reacquisition, and exact feasible/dyadic coefficients with certified FW gaps. One fixture has actual nonselfadjoint rotation labels paired with verified adjoints and reachable Gram determinant approximately 4e-24. It does not force retention of that near-duplicate pair; the separate constructor stress diagnostic is the imposed-dictionary test.

The other tests exercise PSD failure, unexpected source failure, unaffordable binary calibration, and unaffordable generic FW, including subsequent no-retry latching. No astronomical source loop or optimization loop was executed. The full generic rounded-FW convergence path is supported by the analytical receipt and prior exact step checks, NOT by a completed large-cap run in these seven tests.

The default per-solve optimizer budget is finite (10,000), so this executable is explicitly a budgeted receiver that can return refusal/UNKNOWN. In particular small active-face proposals are not a generic large-dictionary solver. The executable must not be described as demonstrating successful unlimited-budget acquisition on arbitrary instances, or as making the enormous theoretical calibration budget practical.

Episode/descriptor-control fields are source-adapter counters; they are not measurements of stationary preparation duration, energy, or physical wall-clock cost. Work counters are partial operation diagnostics, not a measured bit-operation ledger. Those costs remain the explicit parameters of the theorem, and zero-source emulator execution establishes no physical timing advantage.

## Explicit adapter/label restrictions

Two interface restrictions remain rather than being silently covered by this receipt. First, canonical pair sorting requires mutually orderable labels; the constructor's hashability/uniqueness checks alone do not enforce this. Homogeneous string/integer labels used by the tests are supported. Arbitrary mixed, nonorderable labels can trigger a latched Python comparison failure; supporting them would require canonicalization by supplied label indices.

Second, `_mean` checks rational type and [-1,1] range but does NOT verify that an arbitrary custom adapter's value lies on the claimed n-shot binary grid. The finite-bit implementation receipt therefore covers the native BinaryMeanAdapter and the reviewed conforming validated emulator, or another adapter satisfying the same explicit report/denominator contract—not an unrestricted rational-valued adapter. A possible narrow validation is requiring `(value*shots+shots)/2` to be integral. No code change was made in this review. An arbitrary custom adapter must also earn its statistical mean-error/unbiasedness contract; grid validation alone could not establish that physical premise.

## Closure

The reviewed implementation faithfully realizes the audited scalar formulas with optional independently gap-checked constant-size proposals and explicit budget refusal. No historical cache/loading/security experiments, remote changes, hidden-state training interface, or physical sampling claim entered this review. The bounded scientific implementation audit is closed; no further polishing or testing is required for this receipt.
