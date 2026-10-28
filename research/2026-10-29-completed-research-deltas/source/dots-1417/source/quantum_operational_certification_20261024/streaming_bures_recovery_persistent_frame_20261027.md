# Streaming Bures recovery with a retained quantum frame

27 October 2026. New corollary candidate; independent receiving required. This changes the chronology/resource interface of the received one-shot Bures theorem. It does **not** declare its old fresh-bank/no-reuse statements wrong: the new ingredient is a persistent receiver quantum-frame memory implementing causal random dimension reduction. A measured decoder matrix alone still cannot align a future physical datum.

## Governing inputs and compiler gate

1. `direct_cptp_bures_bridge_20261027/DIRECT_CPTP_BURES_RISK_RECOVERY.md`: the received ordinary-six-state, full-CPTP Bures-risk learner with polynomial tomography/SDP processing.
2. `direct_cptp_bures_bridge_20261027/PRIVATE_FRAMED_COMPLETE_OPTIMALITY.md` and its independent audit: the received exact product-fidelityproducer-workspace/privately framed collective comparator and expected-risk transfer.
3. `causal_random_dimension_reduction_extension_20261027.md` and its independent receipt: an exact causal TP family on ALL physical input operators, equal on a common k-support to one Haar-common-frame channel.
4. **Explicit online compiler:** `explicit_online_random_dimension_reduction_compiler_20261027.md` and its separate independent receipt must be received before this note's polynomial-gate version is promoted. The existence theorem in item 3 ALREADY proves the statistical/chronological corollary with a finite but potentially exponential generic memory-channel implementation. An efficient full-Schur transform alone does not by itself certify an efficient causal dilation.

The compiler interface required below is precise. For a predetermined horizon H, it supplies receiver-local known isometries receiving one s-register and persistent memory, emitting one k-register immediately, with the following exact-reference law for every unknown fixed isometry W:C^k->C^s and every operator X on `(C^k)^tensor H`:

`T_H(Ad_(W^tensor H) X) = integral Ad_(U^tensor H)(X) dU`.       (1)

Its prefix maps must obey full arbitrary-input causality, not only promised-input consistency. The finite implementation must approximate the WHOLE interactive process (or have per-step diamond errors summing to the allocated budget) and use `poly(H,k,log s,log(1/nu))` known gates and workspace. It may retain growing quantum memory; it must not measure/disclose paths that are required coherently. Neither the source inverse nor a controlled source nor a protected encoder programme is supplied.

## 1. Operational theorem

Let `E:L(C^2)->L(C^s)` be stationary and independently reset. A valid integer upper bound R>=1 on its normalized Choi rank is supplied. The accuracy parameters obey `0<gamma,epsilon<=1`. Define

`a=f_opt(E)=max_(D CPTP:C^s->C^2) F_e(D E)`, `ell_*=1-a`.

For a fixed integer M>=1, each logical payload receives an independent private uniform Pauli BEFORE E, and the inverse Pauli after recovery. Keys are independent of source/calibration/payload and are not exported to the tested logical output. Let

`delta^*_(frame,M)(E)=2(1-a^M)`                              (2)

be the received exact optimum against arbitrary key-dependent collective physical CPTP decoders, arbitrary independent pre-datum calibration, and full source knowledge. This comparator concerns one use of E per logical qubit with no rate-changing cross-use encoder, sender/receiver quantum bypass, extra payload-dependent source query, or postselection.

Set, for s>=2,

`k=min(s,2R)`, `r=min(R,k)`, `D=2^ceil(log2(kr))`,

`n=ceil[30720 D(log(2D)+1) M/(gamma epsilon)]`, `N=6n`.       (3)

There is a PRE-DATUM ordinary calibration using N source calls, followed by M sequential future payload calls, whose recovered logical block satisfies

`||Lambda_actual,M-id||diamond
 <=min{2,(1+gamma)delta^*_(frame,M)(E)+epsilon}`.             (4)

All norms are unhalved. Total source calls are exactly N+M under this cap. In particular:

* The M payloads need not coexist in receiver storage.
* Calibration is measured and its feasible decoder SDP is solved BEFORE the first payload arrives.
* No new training bank is acquired per payload.
* The persistent quantum frame is retained/updated at EVERY payload; the classical decoder alone is not reused on an unaligned physical output.
* The given M determines the total complete-error target and training accuracy. An infinite horizon at the same nonzero error budget is not asserted.

If the explicit compiler interface is received, known gates/classical processing are polynomial in `R,M,1/(gamma epsilon),log s` and precision parameters, subject to the supplied trusted source/control implementation costs. The exact source cap is

`N=O(R^2 log(2R) M/(gamma epsilon))`.                        (5)

For s=1 use a fixed maximally mixed logical replacement; it attains the comparator without calibration.

## 2. Actual chronology

1. Initialize the causal frame processor with horizon H=N+M and common-support bound k. A Kraus decomposition with at most R terms proves `rank E(I_2)<=2R`; no physical support basis is given or learned for free.
2. Prepare n independent ordinary outputs for each of the six trusted Pauli eigenstates. After EACH source call, feed its s-register to the next frame step and store the emitted k-register in its labelled homogeneous bank. Keep the processor's persistent quantum memory untouched except for its prescribed updates.
3. With all N calibration outputs emitted, perform the received random purification/Bures tomography separately on the six homogeneous k-dimensional banks. Solve the certified feasible full-CPTP decoder SDP and compile its decoder D_h. All this occurs before payload arrival. The measured classical record h can be processed normally; the quantum frame memory is NOT discarded or measured.
4. For payload j=1,...,M, apply its fresh private input Pauli, use E ONCE, feed the physical output to frame step N+j, apply the SAME learned D_h to the newly emitted k-output, then undo that payload's Pauli. Release the logical output immediately. Update and retain the frame memory for the next use.
5. At the stated horizon discardproducer-workspace/privately retain the internal memory according to the output specification. It is never part of the compared logical output. Continuing beyond M requires a newly stated accuracy/horizon budget, not an assertion of free indefinite reuse.

Training storage is N reduced registers, not N+M simultaneously stored physical registers. Persistent frame memory remains a quantum resource and may be as costly as a coherent encoding of past physical data. This is not a claim of low memory or a small practical latency: the direct learner still waits for all N calibration outputs before serving payloads.

## 3. Why training measurements do not destroy future alignment

Mathematically write `E=Ad_W E_0` and `E_U=Ad_U E_0`. For fixed W, (1) is equality of causal channels on arbitrary operators, including untouched references. Linking in ordinary calibration preparations, their measurements, and h-controlled later decoders preserves that equality. Thus the EXACT reference experiment is operationally equivalent to:

* choose one mathematical Haar U;
* supply all six iid training banks from E_U;
* condition on their record h;
* apply E_U to every later payload, in the SAME U-frame.

The real apparatus never samples, measures or exports U. The decomposition is a proof device for the whole process. Measuring a calibration output can steer the actual receiver memory; the causal identity already accounts for that steering. Replacing the memory by a classical U estimate or independently resetting it would not satisfy (1).

For fixed U the training law h is independent of arbitrary future payload/reference states and their private keys. Hence the learned strict-TP D_h defines the same local logical channel

`Lambda_(U,h)=D_h E_U`

on every future slot, with `0<=f_(U,h):=F_e(Lambda_(U,h))<=a` pointwise. The final logical process is a mixture of tensor powers; it is NOT the tensor power of an averaged marginal. No external source environment or coherent input reference was accessed.

## 4. Global privately framed error, including correlations

After averaging the private per-payload keys, let `P_(U,h)` be the Pauli twirl of Lambda_(U,h). The exact-reference logical process is

`Gamma_M = E_(U,h) [P_(U,h)]^tensor M`,                     (6)

so its total identity-Pauli weight is `E f_(U,h)^M`, not `(E f_(U,h))^M`. The received Pauli identity gives

`||Gamma_M-id||diamond=2[1-E f_(U,h)^M]`.                   (7)

The direct Bures proof supplies an expected local loss guarantee. With

`m:=E(delta_Bures)<=gamma epsilon/(384M)`,

`eta_SDP<=gamma epsilon/(32M)`,

and backward eigensolver error squared `<=gamma epsilon/(6144M)`, its exact-reference loss bound is

`E(1-f_(U,h)) <= (1+gamma)(1-a)+epsilon/(4M)`.               (8)

These are precisely the received finite allocations associated with n in (3). No high-confidence event, beta penalty or confidence-copy logarithm is necessary.

For 0<=f<=a<=1,

`a^M-f^M <= M a^(M-1)(a-f)`,

`M a^(M-1)(1-a)<=1-a^M`.

Combining with (8) gives

`2[1-E f^M] <= (1+gamma)2(1-a^M)+epsilon/2`.                (9)

This uses nonnegative pointwise regret a-f; it does not assume that training-induced errors on different payloads are independent after averaging. Equation (2) is the exact collective comparator, not the looser union benchmark `2M ell_*`.

### Optional interactive use of the recovered ports

Equation (6) defines a classical mixture of complete Pauli-error sequences, with input-independent sequence probabilities. For any causal external experiment that supplies later logical states based on earlier recovered outputs, the all-identity sequence gives exactly the ideal experiment and all other sequences contribute trace distance at most two. Thus its distinguishing distance is at most the same right side of (7). A parallel Bell input attains (7). This statement concerns testing/using the SAME recovered ports; it does not enlarge the source/encoding comparator by granting extra source calls, changed coding rate or additional bypass systems.

## 5. Finite errors, memory and implementation costs

Allocate a TOTAL interactive implementation error `nu<=epsilon/2`. Include:

* all N probe preparation/source-control inaccuracies;
* all H=N+M causal-frame updates, with per-step errors whose telescoping sum is within its allocation;
* six purification channels, bounded Clifford seed generation and any other learner-record errors not already charged to m/eta;
* all M compiled decoder uses and all 2M input/output Pauli operations;
* coefficient, feasibility and synthesis errors according to the received finite SDP contracts, without double-counting errors already in m/eta.

Per-step diamond control is sufficient under arbitrary retained memory/references and adaptive use: apply a hybrid argument and contractivity at each replacement. The final complete-error discrepancy is at most nu, not nu/2. Equation (9) therefore proves (4). Approximate implementations are NOT asserted to have a literal latent U; the ideal-process analysis is transferred after the complete error budget is established.

The causal-existence construction gives the coarse Hilbert-space memory bound `dim M_h<= (sk)^h`, hence at most `h log2(sk)` memory qubits, plus encodingproducer-workspace/workspace. The explicit compiler may supply better structure; its ACTUAL memory/gate cap must be used once received. In any case the memory persists from calibration through the last payload and grows with N+M. Purely local physical-output storage and lifetime, coherent control, classical decoder description, private key delivery/storage, reset stationarity and gate precision are all resources. This is no practical fault-tolerance or generic-noise scalability claim; R itself may be exponential in physical qubit count.

The pre-noise Pauli control requires a sender or trusted controller and a private key interface to the decoder. It cannot be retroactively applied to an already noise-corrupted datum. Both the proposed method and its strongest conventional comparator receive the same interface.

## 6. Record scope and fair comparison

Only logical outputs are required by (4). One may also retain the downstream TRAINING record h with the ideal identity channel carrying the SAME h law: h is generated before payload arrival, and the factorization in Section 3 makes it input/reference-independent. The private-frame cq lemma then gives the same averaged complete-error bound. This is not a good-quality guarantee for EVERY particular h; rare records can be bad. For finite implementations, do NOT use a generic cq triangle that silently changes the ideal record law and doubles its debit. Split nu into key-blind processor error nu_proc and frame-gate error nu_frame. Apply the private-frame cq identity DIRECTLY to the actual key-blind CPTP block with its actual pre-payload h law: its exact-private-frame cq error equals twice its unrecorded Bell loss. That Bell loss differs from the exact-reference value by at most nu_proc/2, so its complete-error increase is at most nu_proc. Comparing imperfect versus exact frame gates on this SAME actual block and record law adds at most nu_frame. Thus the advertised total nu=nu_proc+nu_frame still suffices.

Do not export the frame processor's internal quantum memory, its coherent Young path, or payload-dependent internal records. They are not the training record covered above. Do not export private Pauli keys. Do not normalize a postselected branch. No source-drift robustness follows from source stationarity, and no claim is made for decoder reuse after the quantum frame memory is reset/lost.

The equally informed conventional alternative is the SAME Bures state tomography and full decoder SDP, with the same quantum-frame memory and ordinary controls. This construction is such a conventional measured-data recovery learner equipped with a stronger receiver memory protocol, not a claimed learning-speed separation or a first unknown-noise recovery result.

## 7. Difference from the frozen one-shot boundary

The older batch theorem required the entire calibration-plus-payload batch to arrive before one collective reduction. It therefore correctly prohibited applying its learned classical decoder to future independently reduced physical data. The present protocol implements a different causal receiver: its quantum state continuously carries the frame through time. It lets the training finish first and serves future payloads one at a time. It neither clones a consumed programme nor assumes a classical physical support alignment.

For a per-payload marginal objective rather than a global M-use objective, an initial bank with `O_tilde(R^2/(gamma epsilon_local))` calls yields the received local expected loss on EVERY subsequent slot within the compiled horizon. Global complete error accumulates, and (3) pays the 1/M local-accuracy demand explicitly. No claim that a fixed finite bank gives an M-independent global error indefinitely is made.

## Evidence/status

`streaming_bures_recovery_persistent_frame_check.py/.json` verifies the scalar expected-regret transfer, deterministic count scaling, shared-mixture versus product-of-average distinction, and private Pauli-sequence tester decomposition. It does not execute the quantum frame/purification circuits. The statistical corollary follows from received Bures/comparator proofs plus the received causal existence theorem. Polynomial online gate efficiency remains gated on the separate explicit compiler receipt; this note cannot supply that receipt by assertion.
