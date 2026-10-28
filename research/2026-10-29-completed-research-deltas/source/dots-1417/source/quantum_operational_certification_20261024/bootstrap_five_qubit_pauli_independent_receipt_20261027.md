# Independent five-qubit transfer receipt (27 October 2026)

## Scope and hypotheses

This receipt verifies the Pauli-code transfer component, not the warm learner's promised high-confidence success rate. It uses the exact supported causal-comb equality from `explicit_online_random_dimension_reduction_compiler_20261027.md` and the common-latent-frame/record disintegration in `streaming_bures_recovery_persistent_frame_20261027.md` §§3–5.

**Common support is mandatory:** the SAME frame, initialized for the entire predetermined horizon, must include every warm, programme-data, and carrier call. The owner confirms the quaternion-family bound `k=min(s,8R)` using `coherent_encoder_bures_bridge_20261027/COHERENT_ENCODER_UNRESTRICTED_RECOVERY.md` §2 (anchor rank R, full family rank at most 4R, common output support at most 8R). This report has not independently re-proved that upstream support theorem. A seed-only `2R` bound is not an acceptable substitute.

Condition mathematically on the common Haar frame U and pre-transfer warm record h. Freeze the selected seed isometry V_h and strict-TP decoder D_h, but continue updating (never freezing/resetting/measuring) the quantum frame through **every** source call. The conditional logical seed channel is a fixed CPTP qubit channel. Independent private uniform Paulis before V_h and inverse Paulis after D_h make each carrier a Pauli channel

`P_(U,h)(rho) = sum_(a=I,X,Y,Z) q_a(U,h) a rho a`, `p(U,h)=1-q_I(U,h)`.

The carrier noise is iid **conditional on U,h** because the physical source is stationary and independently reset, the exact frame comb equals a common-U product source on its whole supported operator space, and the private keys are independent. Entangled carrier inputs do not change this channel-factorization statement. It is not an empirical consequence of a marginal holdout. A fixed hidden mixture is not replaced by a product of its averaged channel.

## Code and exact recursion

Use stabilizers `XZZXI, IXZZX, XIXZZ, ZXIXZ`; logical Paulis are `XXXXX, ZZZZZ`. The 15 single-qubit nonidentity errors have all 15 distinct nonzero syndromes. Correct with that single-qubit Pauli, and use identity for zero syndrome. Every weight-zero or weight-one error is corrected exactly. Any Pauli error, followed by this recovery and ideal decoding, is a logical Pauli: its corrected residual centralizes the stabilizer, and its logical class is determined by anticommutation with logical Z and X. Syndrome records are discarded/kept private.

For independent carriers of total nonidentity probability p, the logical error probability therefore satisfies

`p' <= Pr(number of carrier errors >= 2) <= sum_(i<j) Pr(error_i and error_j) = 10 p^2`.

This bound is insensitive to arbitrary X/Y/Z bias. At the next concatenation level, disjoint corrected blocks are independent conditional on U,h and have a common logical Pauli distribution (possibly with changed bias). Thus

`p_L <= (10 p)^(2^L)/10`.

For `p <= p0 < 1/20`, it suffices to bound `p_L <= (10p0)^(2^L)/10`, which decays doubly exponentially in L. Each logical transfer uses exactly `5^L` source-carrier calls. The proof presumes trusted local code encoding, syndrome recovery, seed maps and private Pauli controls; their finite inaccuracies require a separate complete implementation budget. No noisy-gate fault-tolerance theorem is being claimed.

## Complete reference and bank cost

For a qubit Pauli channel with nonidentity mass p_L,

`||P_L-id||diamond = 2 p_L`.

Upper bound: triangle inequality on the Pauli mixture. Lower bound: input half a Bell state; the four Paulis give orthogonal Bell states. Consequently this bound holds for a transferred qubit entangled with any outside system, including the previously emitted programme datum, the other two reference qubits, and all prior bank elements.

Prepare each programme input locally with its three coherent reference qubits; make its data-source call **first** and immediately process that physical output through the SAME frame. Encode each reference qubit into a concatenated codeword, and send every physical codeword qubit by V_h → source → same frame → D_h, with independent private Pauli twirls. After local code recovery, the intended three-reference-qubit programme sample differs from its ideal same-U sample by at most `6p_L` in unhalved trace norm, by three channel replacements. One can encode before or after the data call provided no reference is bypassed to the receiver.

A causal hybrid over all `3 n_Gamma` reference transfers proves bank preparation error at most

`6 n_Gamma p_L`.

There is no dimension penalty and no assumption that the three references are initially independent. Conditional independence belongs to channel noise, not to the data. The joint programmed bank remains a mixture over the SAME U,h, not an iid bank after those variables are averaged. Any subsequent fixed or h-controlled CPTP learner contracts this trace-norm error. If downstream processing is itself interactive, use the corresponding causal-process hybrid. The programme-data calls are ideal source uses on both sides of this comparison; their own physical source noise is part of the target programme, not counted as transfer error.

Total calls for this bank component are `n_Gamma (1+3*5^L)`, plus warm/validation calls. Include all of these in the frame horizon and gate precision allocation.

## Warm acceptance caveats

1. A mean-risk warm bound does not imply `p(U,h)<=p0` for every h or every latent U compatible with acceptance. Even conditioning on h alone leaves a posterior mixture over U. State a good event `G={(U,h):p(U,h)<=p0}` and prove the required probability separately.
2. If unconditional bad mass is at most beta, an unconditioned TP experiment pays at most `2 beta` in complete error in addition to the good-event transfer bound. For an accepted normalized experiment, the relevant penalty is `2 Pr(G^c | A)`, bounded only by `2 beta/Pr(A)` from an unconditional guarantee. This may be large when acceptance is rare.
3. Ordinary validation on the frozen seed is conditionally iid in the exact same-U model. Conditional binomial tail bounds can be integrated over U,h to bound *false acceptance*; this is legitimate under the theorem's reset/common-frame assumptions. Such validation does not certify those physical assumptions for correlated hardware, and its additional calls/frame updates must be included in the horizon.
4. Actual finite implementations need not possess a literal U decomposition. Charge their **whole interactive process** discrepancy nu separately using a causal hybrid. For unconditioned TP output this adds nu. Conditioning on acceptance can amplify discrepancies by an inverse acceptance probability; simply writing '+nu' for a normalized accepted branch is not justified. Safer: specify a TP protocol with a retained accept/reject flag and defined failure output, or establish an explicit conditioned comparison with an acceptance lower bound.
5. Private twirl keys and internal frame memory must not be exported as part of the compared output; releasing them is outside the simple averaged Pauli-channel claim. This receipt discards syndrome records; retaining classical syndromes requires stating their ideal cq law explicitly, rather than silently adjoining them to the identity output. The pre-transfer warm record may be retained with its actual, input-independent law and treated as a cq label.

**Correlated counterexample:** apply `I^tensor5` with probability 1-p and `X^tensor5` with probability p. Every one-qubit marginal has error p, but the code has logical-X error p, not at most `10p²` when p<1/10. A marginal holdout cannot rule this out.

## Executable evidence

`bootstrap_five_qubit_pauli_independent_check_20261027.py` exhaustively classifies all 1024 phase-free Pauli errors by syndrome, correction and logical class, asserts every weight-0/1 correction, and writes the complete multivariate logical enumerator to the matching `.json`. It also checks exact-rational biased channels, the full denominator-20 probability simplex, three concatenation levels, a fixed-latent mixture versus the incorrect product-of-average construction, and the correlated counterexample. This is a classical finite code check, not execution of the frame compiler, warm learner, or quantum circuit.

### Executed result

The script completed successfully: 1024 Pauli errors and 1771 exact-rational simplex channels passed. The weight-w logical-I counts for w=0,...,5 are `(1,15,0,60,135,45)`; each nonidentity logical class has counts `(0,0,30,70,90,66)`. At biased p=0.04, the first three concatenated errors were `0.0146228314864, 0.00206959860038, 0.0000426357188819`, beneath bounds `0.016, 0.00256, 0.000065536`. The shared-latent half-identity/half-pure-X(p=0.04) mixture has logical error `0.0073789952`, versus the incorrect product-of-average result `0.0038423872`.
