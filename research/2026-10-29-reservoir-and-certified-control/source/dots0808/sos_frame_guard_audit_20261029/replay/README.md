# Acquired-bank frame optimization → actual finite guarded payload
2026-10-29. Scientific model computation, not hardware. Independent review pending.

## Outcome and strongest comparison

On the existing permanent-one-axis acquisition history, optimizing the empirical frame-task objective yields a materially more useful code than deploying the final coarse-net Hedge distribution. It does NOT identify the full frame, and does NOT outperform an equally informed ordinary optimizer: the certified candidates are precisely the output of ordinary24-start SLSQP, with an additional SOS global lower certificate. Removing certification leaves identical candidates and identical operational yield. A separately executed24-start Nelder–Mead baseline performs almost identically.

Predeclared one-attempt guard:35 logical payload qubits;155 one-qubit service slots; correct up to6 bad slots; abort at first failed validation; cap1400 native calls. Matching uses C2,s1/3; completed six-state uses C1.5,s0.4. Both have R1 and accepted-subnormalized soundness bound1/128 under the earlier private-role/trusted-control/retirement assumptions. No source-dependent guard tuning was performed.

| Acquired candidate policy | Test | Acceptance | Expected native calls | Expected accepted payload / calls |
|---|---|---:|---:|---:|
| SOS-certified ordinary SLSQP | six-state |0.3508147863|239.3421983|0.0513010978|
| Ordinary Nelder–Mead | six-state |0.3459792045|237.9611003|0.0508876121|
| Final old Hedge distribution | six-state |0.0109274792|83.6291252|0.0045733083|
| Uniform old net | six-state |9.22e−21|7.2116482|4.48e−20|
| SOS-certified ordinary SLSQP | matching |0.0423112406|139.3736520|0.0106253470|
| Ordinary Nelder–Mead | matching |0.0404649337|137.6798978|0.0102867064|
| Final old Hedge distribution | matching |8.85e−6|38.4825046|8.05e−6|
| Uniform old net | matching |4.34e−44|3.3171676|4.58e−43|

The roughly11.2× six-state yield improvement over old Hedge is a valid *narrow* comparison. It is an empirical-optimization gain, not an SOS-specific operational gain. SLSQP and Nelder–Mead use the same acquired information. The additional SOS deliverable is an exact global empirical-objective certificate, not a certificate of future physical behavior.

## Same acquired data, actual retained bath, no extra training

Inputs are unchanged copies from `quaternion_oracle_controller_20261029`: the29,916-probe integer coefficient bank, the three frozen certified rational quaternions, the completed60,000-round history and replayed final Hedge checkpoint. The history also contains30,084 source service calls; **all60,000 calls are charged**, not only probes. No new training records or hidden-frame fit enter candidate generation.

The benchmark starts each counterfactual policy from the ACTUAL final training bath, not the original initial bath or a maximally mixed replacement. Reconstructing final Hedge probabilities from the sufficient bank agrees with the replay checkpoint to4.72e−14; final bath agrees exactly. Input source state is preserved in `maps_and_fixture.npz`.

The declared evaluator continues source index1: the fixed one-axis hidden collective J_z⊗Z_M plus0.37 I⊗X_M Hamiltonian for time0.8. This is the original permanent-one-axis policy, not a favorable policy selected after looking at results. Hidden frame/source matrices are used ONLY for source-model evaluation. Every reported candidate policy is predeclared from the bank or original comparator. This does not predict an unknown future source or prove stationarity from data.

Offline optimization is paid ONCE before this frozen-candidate guard; its latency is not charged as a worst-case online-padding delay before every call. A fixed candidate may be public and the source may know it: model-free guard soundness still relies on the current test/service role and Pauli/test keys being private. Future yield remains contingent on the declared stationary continuation, and this benchmark makes no online FTPL performance claim.

Full-frame identifiability is deliberately absent: independent rotations about each hidden local z axis leave this full-joint source invariant. Useful code performance is therefore the target, not Euclidean error to a unique hidden frame.

Charging the full acquisition once, the SLSQP/SOS-six-state one-attempt accepted-payload ratio is0.0002038289 per source call, versus0.00000636549 for old Hedge. These are single-operation cost ratios. No repeated-attempt or amortized throughput claim is made, and no retry of the same unknown payload after abort is assumed. Such a claim would require actual post-attempt memory-channel propagation and a suitable workload/payload model.

## Ordinary optimizer and compute budget

`ordinary_optimization.py` imports no source matrix or hidden frame. It reruns exactly the candidate-generating24-start SLSQP already used by the SOS procedure (four coordinate starts plus20 fixed-seed random starts), then rationalizes the quaternion. All three rational candidates are identical to the certified files. Certification is not what finds a better candidate here.

The separate function-only Nelder–Mead comparison receives a predeclared equal *monomial-pass* budget: one analytic value+gradient evaluation in this implementation evaluates five35-term monomial sums, so NM receives at most five times that evaluation count, split over the same24 starts. All starts/results and limits are reported, not selected by physical performance. SLSQP takes508,423,436 value+gradient calls; NM uses2520,2112,2160 function calls. Per-edge observed runtimes are approximately0.07–0.09 seconds for both on this host. This accounting is not a claim of universally identical CPU/hardware cost, and failed-to-converge NM runs are retained. The exact global lower certificates remain additional SLSQP/SOS work, not granted to ordinary optimizers.

## Actual CP instruments, not scalar rescaling

For each frame tuple W, use the reviewed8-CNOT Bell-label four-spin singlet isometry E=W E0 and complete decoder D(ρ)=E†ρE+|0><0|Tr[(I−EE†)ρ]. The canonical logical gauge is the Bell-label one throughout this new benchmark; no uncontrolled change of reset target occurs.

Completed service applies private logical Pauli pads before E and inverses AFTER the complete decoder. The averaged memory channel is T(σ)=Tr_S U((EE†/2)⊗σ)U†. Its completed identity-Pauli CP branch is built from all decoder Kraus operators; the complement is CP. Six-state preparations/readouts are passed through the actual E,U,D, including leakage-reset contributions, not replaced by a failure coefficient alone.

Raw matching tests prepare each of the three pair-singlet states in the candidate frame and accept only exact full-state survival. Their averaged pass/fail maps are built directly. For their conservative ledger we retain the raw scalar good branch BσB†, B=(1/2)Tr_code U, and bad=T−good. The completed logical Pauli service contains that good subbranch plus positive additional identity terms, so this conservative raw ledger remains valid with cheap logical pads; physical permutation routing is not needed for this four-spin comparison. The complete-memory inequalities H_bad≤2F_matching and H_bad,completed≤1.5F_six are checked as operator inequalities, as are CP/TP and all effects.

For old Hedge/uniform, all27³ frame tuples are averaged with exact declared independent edge probabilities. The frame tuple is independently sampled and its classical key retired on every call, before the private role coin. SOS/SLSQP and NM use their fixed bank-derived tuples. Candidate distributions do not get chosen by source truth.

`build_compare.py` executes a finite1400-step matrix-state DP, tracking service count, bad-count bucket0…6/overflow and the full2×2 retained bath. It records acceptance, validation/cap abort, expected calls and accepted overflow mass. Trace conservation is checked numerically. This is not a memoryless binomial model. Reported probabilities are floating numerical evaluations, not directed-rounded interval certificates.

The source-model conditional memory-effect eigenvalues are also reported. In this fixed one-axis model, raw effects are nearly scalar; the SLSQP/SOS raw bad weight is0.01030909 versus Hedge0.03901451, completed bad weight0.00678093 versus0.02956726. These are uniform-over-current-memory diagnostics for the declared source, not acquired unknown-future certificates.

## Complete outer recovery and circuit resources

The actual received GF32 CSS/GRS outer code has31 symbols,155 physical qubit slots,35 logical payload qubits and corrects6 arbitrary symbol errors. At most6 bad native qubit slots hit at most6 symbols. Prior QEC-span reasoning extends this to coherent errors entangled with source memory; no iid noise assumption is required.

`sample_complete_decoder.py` constructs all completed joint-memory Pauli CP branches from the actual source and all15 reset-decoder Kraus operators. Their identity branch and total map agree with the DP within8.1e−16. Across300 independently simulated counterfactual single attempts, each initialized at the same actual final training bath,111 accept. Every accepted actual error ledger is fed through the received finite-field total syndrome decoder; all35-qubit logical residuals vanish, with at most5 native faults among accepted trials. Within each trial the bath is continuously retained and updated. This is not300 successive deployed attempts with bath reset, nor large dense quantum-state simulation. Exact model DP—not these samples—supplies the reported acceptance/yield.

A temporary implementation error used the pre-Fourier phase-syndrome index despite the received `decoded_error` already swapping the first-register X/Z labels. The first corrected-error assertion caught it; the accepted script now uses dx[:s] exactly as the governing outer decoder specifies. No initial failed run is represented as evidence of recovery.

`control_budget.py` compiles the actual31-symbol outer binary encoder/inverse and verifies its action on all binary Pauli basis labels. It charges16 CNOT per full service or six-state test (8 encode+8 decode),4 CNOT per raw matching preparation/readout, and the actual outer circuit, with outer inverse only on acceptance. Four physical learned-frame one-qubit gates per endpoint direction, private Pauli controls, initial states, resets/readouts, routing, storage and calibration remain additional.155 protected buffer qubits are required, plus active source/test ancillas. These are ideal-control counts, not noisy-hardware feasibility claims. The outer compiler and eight-CNOT endpoint help all candidate optimizers and test families equally.

## Reproduction and dependencies

Run `ordinary_optimization.py`, `build_compare.py`, `sample_complete_decoder.py`, `control_budget.py` with Python, NumPy and SciPy (OPENBLAS_NUM_THREADS=1 used here). Frozen model/data, outputs and gates are included. Received external proof/code dependency hashes are recorded separately. Do not rerun `inputs/capture_one_axis.py` to generate new training; it is provenance only. Source candidate generation, source evaluation, CP validation, finite DP and classical outer decoding are distinguished, and no Capital/GitHub publication is claimed by this packet.
