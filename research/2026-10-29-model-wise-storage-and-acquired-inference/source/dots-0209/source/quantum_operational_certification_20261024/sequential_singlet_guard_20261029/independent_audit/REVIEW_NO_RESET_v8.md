# Independent review: no-reset acquisition-to-guard continuity v8
2026-10-29 UTC. Reviewer: `review_current_channel_symmetry`.
Disposition: **accepted as the declared conditional-on-one-acquisition-history mathematical continuity fixture**, with its source-stage switch, paid resources and existing soundness boundaries. This does not establish training-average yield, confidence-stopping completion, unchanged acquisition dynamics during deployment, hardware performance or practical superiority.

All governing programs, results, dependencies and checks are hash-bound in RECEIPT_NO_RESET_v8.json. The complete million-call acquisition plus guard program was rerun; its printed JSON matches the author's stored output byte for byte. Independent checks are in check_noreset_complete.py/.json.

## 1. Counter-only frame fit and actual quantum-memory carry
Source inspection confirms that final frames are fitted from `old.sums/1000000 - old.Jembed`. The sums contain only actual probe-setting/output counter updates. The identity embedding Jembed is a fixed 16-by-9 basis-inclusion matrix: it has ones at row4a+b, column3(a-1)+b-1 for a,b=1,2,3 and zeros elsewhere. It is not an inferred environment model or a source-dependent truth array. Our independent check reconstructs this matrix from scratch and verifies exact equality.

The final frame fit uses the smallest right singular vector followed by the specified signed proper-rotation projection. It does not consume old.O, the true-frame diagnostic, occupation matrices, bath vector, future guard acceptance or an exact-operator frame. Independently recomputing the fit from final counters and the known embedding gives exactly the same candidate matrices. The basis of the four-qubit singlet encoder is computed from known total-spin operators, not from source parameters.

The learning simulator itself uses the declared known source generator to produce one million actual sequential product-probe outcomes and conditional bath updates; that is its simulation role. Its final normalized bath vector is passed into the guard as sigma=|bath_final><bath_final|. There is no replacement by an initial state, maximally mixed state, learned bath estimate or fresh reset. Independent carry residual is exactly zero. The state is nontrivial, approximately

    [[0.46724274, -0.05350929 - 0.49604810 i],
     [-0.05350929 + 0.49604810 i, 0.53275726]].

This simulator knowledge is not available to the physical learner or guard. The learner compiles the counter-derived frame; the physical guard samples roles and test preparations, observes test outcomes, and decodes its outer syndrome. Source Kraus operators, bath state and virtual fault labels remain evaluator-only objects.

## 2. What continues, and what changes at the stage boundary
The QUANTUM bath is not reset. However the SOURCE SELECTION RULE deliberately changes: during training, the next unitary is chosen from previous output parity; during guard, the unperturbed source always uses acquisition unitary0, with the predeclared lab-Z burst alternative. The final sampled acquisition parity is1, so blindly continuing the old parity rule would have selected unitary1 for the next call. V8 explicitly selects unitary0 instead.

This is a declared causal source fixture and is consistent with the model-free guard. It is not a prediction of the future environment from an occupation estimate, nor a claim of unchanged parity-controlled dynamics across stages. The independent check verifies Ugood equals old.Us[0]. The same complete guard source map is used by both roles at each current call index, and the burst is scheduled independently of the hidden current role. No bath-reset interpretation is needed or permitted.

Conditioning on a completed training record freezes the candidate frame and the source-memory state. The guard theorem holds for every such frozen frame and memory input, so their correlation through the training history is harmless. A new user payload may be introduced independently of that memory for the product-input statement; arbitrary initial payload–memory correlation instead invokes the separately reviewed accepted memory-filter ideal. No acquisition confidence certificate is required for guard soundness, though it matters for a separate claimed learning guarantee or yield promise.

## 3. Yield is conditional on this training record
The million-call acquisition is ONE sampled history. The subsequent DP computes exact-in-floating-arithmetic future guard probabilities conditioned on that history's candidate frame and final bath state. These are not averages over every possible million-call acquisition record and not lower bounds on training-average acceptance.

Likewise, the 1000 guard trajectories are alternative simulated continuations from that same conditional starting state; they are not 1000 sequential physical operations each beginning at the same bath without resets. The source-generator simulation can fork a mathematical initial state to evaluate conditional probabilities. This does not grant the proposed physical protocol an ability to restore an unknown bath state.

The unchanged confidence-stopping limitation is correctly preserved: the conservative acquisition stop has not fired. A million calls here produce a candidate whose guard happens to have useful yield in the declared fixture. No confidence-complete common-algebra discovery or arbitrary-noise high-yield theorem follows.

## 4. Independent guard and code checks
The same design is retained before evaluating the new frame: C=6, s=1/7, b=0, t=6,155 qubit services grouped into31 GF(32) symbols, [[31,7,13]]_32 code,35 payload qubits and cap1400. Therefore the already-reviewed ideal accepted-subnormalized bound remains exactly1/128. Grouping and trace-dual Z conventions are unchanged; no alphabet mismatch reappears.

The independent check explicitly constructs the actual minus product-singlet and plus fixed-four-qubit-seed preparation for every pair in the newly learned frame. Their complete pass/fail memory maps agree with the author's projector-form test maps to below6.2e-16. Thus the changed frame does not introduce an unpriced access to a singlet projector state.

An independently organized matrix-state DP, with explicit bath matrix axes and a terminal service bucket, gives:

- Good continuation: acceptance0.775765692602868; accepted >6-fault mass1.4741717235881846e-12; abort0.22423430739795885; cap abort0.00011843454950395189; expected957.4809003757351 guard calls.
- Predeclared burst: acceptance0.013702727465348258; accepted >6-fault mass1.3731832036579217e-5; abort0.9862972725350685; cap abort1.716311592006435e-6; expected482.3938639325302 guard calls.

The largest compared difference from author DP results is5.69e-13. These decimal values are reproducible mathematical floating results, not interval-certified or measured laboratory probabilities. The universal1/128 guarantee comes from the theorem, not from trusting a tiny simulated tail.

The whole author rerun reproduces its sampled trajectories and actual selected-ledger decoding. The phrase64 decoded ledgers means the first50 nonzero accepted good-source ledgers plus14 nonzero accepted burst ledgers, not every good-source accepted ledger. The source document correctly uses that selection wording. Independent field checks again exhaust160 trace-dual identities and decode36 additional spread/random/clustered patterns, including30 inner-coordinate faults confined to six outer symbols. These checks use the actual total finite-field decoder, not a fault-count correction oracle. Full32^31-dimensional amplitudes remain unsimulated.

## 5. Costs, dependencies and accepted change
The charged acquisition budget is1,000,000 full-array native calls, not1m at each diagnostic checkpoint. Guard consumes at most1400 additional calls. Each stage's full preparation/readout and source duration must be counted. The155-qubit trusted endpoint buffers, private pads and permanently retired keys, four-qubit encoder/decoder and signed-seed controls, routing/role padding, outer Clifford gates and exact classical decoder remain genuine required resources. The arbitrary-noise guard does not protect those endpoint buffers by itself.

The new fixture differs from v5 in learner, source generator, frame accuracy and starting bath state. Its reduction in simulated acquisition call count is not an isolated sample-efficiency comparison. Lower good-source acceptance is accurately reported rather than concealed. No performance superiority over direct encoded 2-design validation, authentication/traps or equally informed conventional QEC is established.

The code imports the reviewed retained-memory acquisition program and its source-generation NPZ; these are explicit dependencies, not silently regenerated inaccessible assets. The imported exact-source arrays generate the synthetic source and independent diagnostics, whereas the compiled learned frame uses only its observable counters. Hashes of all these dependencies are in the receipt.

Accepted progress: one actual no-reset simulated learning trajectory now feeds its acquired frame AND actual final quantum bath state into the already-reviewed guarded finite operation, without a stage-boundary quantum reset or confidence-completion fiction. This closes that continuity/wiring loop within the declared ideal-control source-generator model. It does not solve generic unknown-noise learning, availability, physical calibration or practical implementation.
