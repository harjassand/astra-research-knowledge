# Independent known-model local-admission compiler audit

31 October 2026. Reviewer: challenge_graph_profile_compiler. **PASS for the exact known-model structural/acquisition operation and its research implementation.** This is separate from physical calibration, a consumer threshold theorem, or a quantum gate backend.

## Source binding

Full files read and independently hash-checked:

- `acquire_local_admission.py`: `a7bc4e513cb4de03a3ef5c504bae75b7b464cb4985a9a683cd560f9d439136f8`.
- `KNOWN_MODEL_COMPILER_SPEC.md`: `8f6bd49d59e91672096f2c8d9fcd8aecd02e130ded7ddacf66911bc485f47fef`.
- `test_acquire_local_admission.py`: `b3a2789fd9c610e4d376e0c0f2ab464a150658bb3d51930b9c5b402e6c608272`.

The received mathematical sources remain the frozen occupation proof `0b0bd7ff...` and resource corollary `403e1421...`, with their separate independent reviews. No new physical source theorem is inferred from executable tests.

## 1. Exact parser and external binding

The JSON loader rejects duplicate keys, floating-point tokens and nonfinite numeric constants. The model parser requires exact field sets, canonical coprime integer rational pairs with positive denominators, strict nonboolean integer indices, positive loss bounds, nonnegative injection and control bounds, and valid lowercase SHA-256 strings. Unknown generator fields and source-creating coupling syntax are rejected, not treated as zero. Pauli words have sorted unique in-range qubits and explicit XYZ labels; identity words are outside this interface.

Parallel identical signed Pauli words are combined before norm/support acquisition, so actual exact cancellations do not spuriously create fanout. Nonidentical words are bounded by the sum of absolute coefficients, a safe LCU norm bound rather than an asserted exact operator norm.

Verification recomputes the entire deterministic record from a separately supplied external specification. Canonical JSON comparison distinguishes booleans, integers, floats, strings, extra fields and changed hashes. Changing the requested budget, consumer ID, target Hamiltonian, evidence identifier or full schedule cannot be accepted against the original external specification by substituting a certificate's own easier task.

The check binds identifiers, not their underlying truth. It does not inspect the control-evidence document, authenticate a threshold contract, or prove that a device follows the declared generator. Model and integrated Hamiltonian control-error assumptions remain externally acquired premises.

## 2. Always-on support and complete schedule

Every system qubit must have a sorted interval partition of the full positive duration, with no gap, overlap or omitted final idle. A global constant unwanted Pauli term is assigned to every location touching its support. Its entire support must fit within each such patch. This correctly rejects an always-on two-qubit term that would cross separately scheduled patches at any time; it cannot disappear merely because a different gate is being executed.

For each source and each assigned location, the code sums absolute merged coefficients to acquire c_li. The maximum is the actual per-source local c bound. The maximum number of distinct assigned sources is g, the maximum actual location duration is tau, and the maximum declared integrated mismatch is epsilon_ctl. A source's assigned intervals must not overlap, even when it couples weakly to two separate simultaneous patches. Sequential reuse is admitted. Multiple terms within one actual joint patch are allowed and their norm sum is charged.

Intended target terms are restricted to their stated patches and are source independent. Their LCU action is recorded but not executed. Idle is explicit; perfect reset/preparation/measurement are not accepted as magic operations. This acquisition result alone therefore does not certify a universal fault-tolerant gate set or its gadgets.

## 3. Graph acquisition and unequal loss

For an explicit graph every supplied source and unique unordered edge is read. The incident hopping bound is sum(|Re h|+|Im h|), which safely bounds the true complex edge magnitude. Normalizing by the minimum positive loss lower bound gives beta and gamma=1-2beta. No hidden spectral-norm calculation is assumed.

For actual unequal losses lambda_i>=lambda_min, the weighted adjoint acquires the extra nonpositive term -sum(lambda_i-lambda_min) u_i n_i V/(1+u_i). Hence the common-minimum-loss proof applies conservatively. Replacing actual injection by its largest upper bound is also conservative. This receiving step does not need stationarity or equal loss rates.

The known uniform open-chain mode defines the entire graph by a finite program. It correctly uses maximum degree 0, 1 or 2 for n=1, n=2 or n>=3 (and zero incident weight when hopping vanishes). Its zero explicit-inspection counters do not claim that a million unknown independently supplied entries were checked. Independent tests compared this mode to fully materialized graphs for n=1 through 8 and reproduced all derived parameters and certificate fields. The logical graph size is reported separately from actual inspected input size.

## 4. Rational admission and exceptional branches

For c>0 and gamma>0, the implemented radius is exactly
R0=gamma lambda_min/[8 c g(1+a tau)], capped by 1/(2epsilon_ctl) when nonzero. The program requires R>=2. The no-control exponent is at most 1/4; the combined exponent is at most 3/4. The exact Taylor-tail certificates used in the tests prove exp(1/4)<9/7 and exp(3/4)<17/8: after terms through degree 8, the remaining positive terms are bounded by the degree-9 term divided by 1-x/10.

The resulting rational bound E/(R-1) and looser linear envelope are correct. PASS is the comparison to the supplied consumer amplitude budget, not an internally chosen universal threshold. Nonpositive gamma, R<2 or a bound above budget produce a truthful NOT_ADMITTED record, not a mathematical impossibility finding.

When c=0, all unwanted source-dependent couplings are absent or cancel identically. The source decouples from system evolution even if initially correlated and even if its transport violates the occupation criterion. The ordinary Hamiltonian first-insertion bound epsilon_ctl is then valid without a transport restriction. This does not waive any schedule, target, model-input or control-bound premise. I explicitly tested this branch with a strongly supercritical source and nonzero small control error.

Arbitrary initial finite-source/system/reference correlations are within the received proof; arbitrary correlated incoming loss/injection fields are not. The loss/injection channels must have the initialized Markov dilation specified by the model.

## 5. Record validity versus actual admission

`verify_certificate` means exact consistency with the external specification, including truthful NOT_ADMITTED output. `verify_admitted` additionally requires PASS. CLI verification exits 1 on invalid records; `--require-admitted` also exits 1 for valid NOT_ADMITTED records. Malformed input exits 2. Without that flag, producing or verifying a truthful negative admission record may correctly exit 0. This distinction is explicit and tested through real subprocess calls.

The functions are not model-learning algorithms or experimental-history validators. Bound evidence identifiers do not convert average infidelity or arbitrary channel estimates into the required integrated patch-supported Hamiltonian discrepancy.

## 6. Independent execution

I called the supplied test `main()` directly, so its file-writing main block did not run and author artifacts were preserved. All 93 supplied checks passed, including six actual CLI exit tests. I then ran 149 additional checks in `check_acquisition_independent.py`:

- every integer input leaf was challenged with boolean and floating aliases;
- certificates for valid altered task/location identifiers were rejected against the original external input;
- symbolic chains and explicit tables agreed for n=1..8;
- always-on cross-patch exposure was rejected;
- the decoupled c=0 branch remained valid with supercritical transport;
- both saved fixture certificates independently verified as admitted.

The resulting check output is `local_admission_independent_checks.json`. Finite tests support the implementation audit; the all-location amplitude theorem is supplied by the separately reviewed mathematical proof.

The reported four-source and million-source-program amplitude values are rational sufficient bounds, not experiment results. Explicit graph parsing is linear in graph input size; schedule/support assignment and rational arithmetic have ordinary polynomial costs in their actual input and bit sizes. No exponential Hilbert-space table is built. The program does not implement the physical loss, injection, intended gates, calibration, decoder or threshold consumer. Benchmark wall times and raw-norm comparator failure are not evidence of practical superiority over the strongest ordinary methods.

## Verdict

Accept the source-bound known-model compiler, strict external-task recomputation, and supplied-input structural/rational admission. Retain the conditional physical premises, explicit/succinct graph distinction, initialized-field restriction, and consistency-versus-PASS distinction in downstream use. No generic local-operator framework or unreceived extension is accepted by this receipt.

## Saved artifact bindings

`explicit_fixture_input.json`: `d806d085ab44b37b8cc666d1ed97da5fe679952ef18c13caa3f2e069b4b3bd5a`

`explicit_fixture_certificate.json`: `f8dc26930b6577b54879b26ca5e5d6326451f0b633900228c5e5fc9d09f809c5`

`million_source_fixture_input.json`: `4715f25f3245cc65749bb2dc87126cab28ab5f7bfa8404e0798a825e46952158`

`million_source_fixture_certificate.json`: `d2a3716f868ab57c7d641eef14e18465f77ffb0b891f5335477f01433550eac3`

`local_admission_test_results.json`: `7c484d37625bf570a5708790b869605f2b9d448dea6973ed12b70f05a53c02cf`

`check_acquisition_independent.py`: `19083bc7ce01d2397e436f8b4e11426e316ce9e5a7340c6e20aef60849a59fba`

`local_admission_independent_checks.json`: `d29497016e0b38f1a5e9425076cd5fc8942d56fe83143301d20ebeced7b54976`


## Final specification-only binding

After the whole review, the author added the explicit benchmark boundary that timers begin from parsed specifications and exclude fixture construction, JSON I/O and physical calibration. I read that paragraph and verified final `KNOWN_MODEL_COMPILER_SPEC.md` SHA-256 `9e1cac0147e4986d48bb5cee2e29cfeac52f7c7a50dd5d8ed23aeca670da69f5`. This strengthens, rather than changes, the cost qualifications above. Code `a7bc4e51...`, tests `b3a2789f...` and saved certificates are unchanged. The PASS binds this final specification as well; no complete end-to-end timing claim is inferred.
