# Ordinary-acquired flagged helper pays for coherent encoder calibration

28 October 2026. Constructive conditional theorem and finite checks; not hardware or a universal capacity detector. This extends the received grouped-reference bootstrap to a fixed multi-use HERALDED helper with a different physical output type and an independently retained frame. The older bootstrap already supplied the grouped FIFO, whole-bank comparison, and coherent learner; those are not claimed as new. The missing work here is the ordinary TNI startup substitution and the two-typed-frame composition.

## 1. Two source interfaces, neither supplied as a protected link

The raw source is a stationary independently reset CPTP map `N:L(C^p)->L(C^s)`. Two known input interfaces use DISJOINT raw calls:

* **Data:** the received calibrated quaternion family `E_x=N Ad(V_x)`, `V_x=(sum_(i=0)^3 x_i E_i)V0`, real `x in S^3`. The known relative controlled-anchor phases and coherent preparation circuits are supplied. Each anchor Choi rank is at most the supplied `R_D`. Put `K_D=min(s,8R_D)`. All data outputs, including coherent anchor off-diagonal blocks and every eventual `E_x` output, lie in one unknown common `K_D`-support.
* **Helper:** a FIXED known coherent isometry `V_H:C^2->(C^p)^tensor c` followed by `c` independent raw calls, with the entire output retained. Write `H=N^tensor c Ad(V_H):C^2->(C^s)^tensor c`. A supplied valid encoded-BLOCK Choi-rank bound is `R_H`; put `s_H=s^c`, `K_H=min(s_H,2R_H)`. Every helper output lies in its unknown common `K_H`-support. No unknown block encoder is acquired here.

For the helper assume that SOME unknown receiver-local CP TNI map `D_0` satisfies

`D_0 H(rho)=a_0 rho`, `a_0>=A+Delta`,

where rational `1/2<A<1`, `0<Delta<=1-A` are public. Choose rational `U>0`, `U/A<3/4`, with certified strict slack

`2(1-A)+A h_4(U/A)<1`, `h_4(q)=h_2(q)+q log_2(3)`.

The unknown helper receiver/support basis is NOT furnished. This is an existence-and-margin promise used by ordinary acquisition, not an observed-postselection condition. A near-zero comparator can instead use the received regret inequality, but its resulting public `A,U` must satisfy the same entropy slack. No positive-capacity source is asserted to admit this fixed helper.

Block rank is a real cost. If only a raw Choi-rank bound `R_raw` is known, the safe bound is `R_H<=R_raw^c`, because the block has at most `R_raw^c` product Kraus operators after the known encoder. It can grow exponentially in `c`. The data-anchor bound alone does NOT bound a helper whose inputs lie outside the anchor input span. All ranks must describe the actual promised source/control model, not an ideal nearby low-rank model.

## 2. Typed frame lemma: no identification of incompatible output spaces

Initialize TWO independent known causal frame processors:

`T_D` on `s`-dimensional DATA outputs, with reduced dimension `K_D` and declared horizon `H_D`;

`T_H` on `s^c`-dimensional WHOLE HELPER outputs, with reduced dimension `K_H` and declared horizon `H_H`.

Their initial private memories are product states. A helper block's `c` physical outputs are held and assembled before ONE helper-frame step. They never pass through the data processor. Each memory persists and is updated only on its own type; it is not reset, exposed, swapped for a classical alignment, or identified with the other memory.

Here is the actual reference-preserving proof. Let unknown support inclusions be `W_D:C^(K_D)->C^s`, `W_H:C^(K_H)->C^(s^c)`. The received causal compiler gives for each type `t` and every operator `Y_t`, not only a density or product state,

`T_t Ad_(W_t^tensor H_t)(Y_t)=integral Ad_(U_t^tensor H_t)(Y_t) dU_t`.

Expand an arbitrary joint operator `X` on all reduced D slots, all reduced H slots and an arbitrary untouched reference `Z` as `sum_ab E_a^D tensor E_b^H tensor X_ab^Z` in matrix-unit bases. Apply the two identities term by term. Exactly,

`(T_D tensor T_H tensor id_Z) Ad_(W_D^tensor H_D tensor W_H^tensor H_H tensor I_Z)(X)`

`= integral integral Ad_(U_D^tensor H_D tensor U_H^tensor H_H tensor I_Z)(X) dU_D dU_H`.  (1)

Conjugating input/output labels by the known chronological wire permutations puts (1) into any fixed interleaving of the two types. Each imported processor is causal on the FULL physical operator space; each restricted typed process is therefore a causal comb. Equality (1) is equality of their Choi operators/causal combs, so linking arbitrary external preparation channels, measurements, classical feed-forward, reference-carrier encodings and source channels preserves equality by linearity of the link contraction. It is NOT inferred from matching one-use marginals or dimensions.

Support factorization is also complete: if all Kraus ranges of a channel lie in `range W_t`, then the channel is `Ad_(W_t) E_(t,0)` on every operator and under every reference extension. For the helper this follows from `supp H(I/2)`; for coherent data it follows from the span of all anchor Kraus ranges. The reset-source contract on disjoint raw calls supplies the product of these source maps for correlated/adaptive inputs. Unknown source memory across calls would invalidate this step.

Thus the ENTIRE physical protocol, with private frame memories untested, has an exact virtual representation using TWO independent initial Haar coordinates `U_D,U_H`. Conditional on these and the frozen helper warm record, helper carriers see one stationary channel in the H-coordinate, while all data samples and payloads see their family in the D-coordinate. Measurements may steer actual processor memory; the comb identity includes this. Later conditioning can correlate the latent coordinates, so estimates below are pointwise in both coordinates and the warm record, then averaged. Neither coordinate is measured or implemented.

There is no physical conversion `C^(K_H)->C^(K_D)`: the helper decoder outputs a logical qubit in the known laboratory basis. That is the type of a Gamma reference wire, NOT the type of a data output. Transporting that qubit identically in complete norm preserves its correlations with a separately framed data register. This is the required interface between the two spaces.

## 3. Paid ordinary helper acquisition

Use the received `ordinary_heralded_tni_bures_acquisition_20261027.md` in the H-frame. Each of its ordinary six-state loss preparations costs one WHOLE helper call, hence `c` raw uses, and retains no sender reference through those uses. Set

`m_H=min{1/16,Delta^2/32,U/35}`,
`d_H=2K_H`, `r_H=min(d_H,3R_H)`, `D_H=nextpow2(d_H r_H)`,
`N_W=ceil[(80D_H/m_H) log(12D_H/beta)]`.                 (2)

The actual acquired state is `T_Hloss=[2 sigma_H tensor I-J_H]/3`, prepared as the ordinary six-state mixture, not by querying a protected Choi state. A physical Bures estimate `tau` and ONE acceptance-constrained TNI SDP learn a feasible `D_hat_H`; the estimate's marginal supplies acceptance, so no second output bank or instrument grid is needed. On one latent pre-data event `G`, with `Pr(G^c)<=beta`,

`a>=A`, `u=a-F_e(D_hat_H H)<=U`.                        (3)

Freeze this learned decoder in the SAME continuing H-frame. Complete failure by the maximally mixed replacement, emit `g in {success,failure}`, and privately Pauli-twirl the WHOLE instrument. Its exact joint law in the virtual frame is

`w(success,I)=a-u`, `sum_(P!=I)w(success,P)=u`,
`w(failure,P)=(1-a)/4` for every Pauli `P`.              (4)

The flags are thereby input-independent even when the raw success effect was input-dependent. Conditional on `U_H` and the warm record, the joint Pauli/flag law is iid on later helper uses, including inputs entangled with data and each other. No source bill is divided by `a`; failures remain in the code. The event includes all calibration/solver aborts if any; there is no acceptance-conditioned confidence normalization.

Equation (2) is the ideal exact-reference estimator count. We choose the received permitted accounting route that charges ALL finite quantum implementation discrepancies to the SINGLE final process budget `nu` below. Hence no extra beta/2 replacement is silently assumed; alternatively its confidence-scale route must change the logarithm and must not be charged again. SDP/eigenvalue arithmetic already explicitly allocated within the acquired estimator must not be double-debited.

## 4. Public flagged reference code and coherent learner budgets

Fix rational `eta>0`, `A'=A-eta>1/2`, `U'=U+eta<3A'/4`, and certified rational constants `h_*<1`, `R_c>0`, `xi>0` with

`2(1-A')+A' h_4(U'/A')<=h_*`, `R_c+h_*+xi<=1`.

For each observed flag string, the decoder admits exactly the joint types whose success fraction is at least `A'` and success-nonidentity fraction is at most `U'`. Conditional on that flag string, the number of admitted errors is at most `(n+1)^8 2^(n h_*)`. The received conditional-type/collision proof consequently gives the uniform ensemble fixed-code complete-error bound `2 F_n`, where

`F_n=4 exp(-2n eta^2)+2(n+1)^8 2^(-n xi)`.              (5)

It is an expectation of fixed-code diamond bounds, including arbitrary reference-correlated inputs and code-dependent inputs, not a guarantee for each sampled code. The complete decoder covers ALL flags/syndromes, with identity fallback when no representative exists. This is not erasure postselection and does not use `H(flag,Pauli)`.

For `M>=1`, `0<epsilon,gamma<=1`, put

`e=epsilon/(8M)`, `beta=epsilon/8`, `delta_ref=epsilon/4`, `nu<=epsilon/4`,
`d_D=8K_D`, `r_D=min(4R_D,d_D)`, `D_D=nextpow2(d_D r_D)`, `L_D=log(2D_D)+1`,
`n_Gamma=ceil[20480D_D L_D/(gamma e)]`,
`a_eig^2<=gamma e/4096`, `eta_opt<=gamma e/8`.           (6)

The received coherent learner's expected Bures bound is then `m_D<=gamma e/256`; its feasible global quaternion-net/full-CPTP-SDP optimizer obeys

`E ell(x_hat,D_hat_D)<=(1+gamma)ell_*+e`,
`ell_*=min_(x,D CPTP)[1-F_e(D E_x)]`.                   (7)

There is no Gamma high-confidence bad event to charge: (7) is an expected-risk theorem. `D_hat_D` is synthesized and later used in the SAME continuing D-frame. The source net-size factor is absent; all net SDPs and their arithmetic are real classical costs.

There are `Q=3n_Gamma` reference qubits (two anchor-control bits and one Bell half per sample). Double `n_c` from `max(2,ceil(6/R_c))` until outward certified intervals prove BOTH

`4 exp(-2n_c eta^2)<=delta_ref/[8(Q+1)]`,
`2(n_c+1)^8 2^(-n_c xi)<=delta_ref/[8(Q+1)]`.           (8)

Set `k_c=floor(R_c n_c)`, `B=ceil(Q/k_c)`; then `k_c>=3` and `k_c>=R_c n_c/2`. One shared exact uniform stabilizer descriptor is sampled with the received capped sampler, `J=ceil(log_4(4n_c/delta_ref))`, so `beta_gen<=n_c 4^(-J)<=delta_ref/4`. On generation failure use a fixed replacement and do not retry for free. Its one-time debit and the B reference blocks satisfy

`2 beta_gen+2B F_(n_c)<=delta_ref`.                    (9)

All parameters/horizons are fixed BEFORE warmup; no favorable training record determines an unbounded refinement or call cap. Public entropy/log tests use outward rational arithmetic. Warm abort, sampler failure and early stopping can use fewer calls, with harmless fixed padding if equality of caps is desired.

## 5. Physical data-first schedule and exact raw-call ledger

Declare `H_D=n_Gamma+M`, `H_H=N_W+n_c B` before initializing the two frames. Warm the helper first, freeze its instrument, sample/communicate the code descriptor and compile the relevant circuits. No unknown final payload has yet arrived.

Maintain a sender FIFO in order `(I1,I2,A)` for each Gamma sample and a receiver bank of data registers. If the FIFO has `r<k_c` entries, prepare `g=min(samples left,ceil((k_c-r)/3))` new Gamma samples. For EACH sample prepare the known control superposition and logical Bell pair, apply known controlled anchors, send ONLY the data through N once, enter the output into the next D-frame step and store its emitted data register. Its three reference qubits remain coherently at the sender and join the FIFO.

Whenever at least `k_c` reference qubits are queued, encode the first `k_c` using the stabilizer code. Send all `n_c` carriers through the learned helper: each carrier uses the known `c`-rail encoder, `c` raw reset calls, whole-block assembly, the next H-frame step, the learned success/failure receiver, and independent private Pauli input/output frames. Keep flags, decode the entire carrier block, label/store the recovered reference qubits at the receiver, and discard syndrome environments. Continue until all samples are prepared; send a final partial FIFO block with known zero padding if necessary.

A reference triple may straddle code blocks. The FIFO never exceeds `k_c+2`; after a full block at most two entries remain. Exactly `B=ceil(3n_Gamma/k_c)` blocks suffice, with no triple-rounding factor. Every actual reference is eventually CONSUMED in a paid noisy helper transmission; there is no protected quantum link, supplied entanglement pair, source inverse, environment readout, or out-of-band quantum relocation. Trusted sender/receiver LOCAL memory is still necessary and paid.

Run the coherent learner only after its full reconstructed bank has arrived. For each later logical payload: use a fresh private Pauli, the selected data encoder, N ONCE, the next D-frame step, the learned full-CPTP D-frame decoder, and inverse Pauli. Do not use the H-frame on a data output. The exact raw-source cap is

`N_raw=c N_W+n_Gamma+c n_c ceil(3n_Gamma/floor(R_c n_c))+M`  (10)

`<=c N_W+(1+6c/R_c)n_Gamma+c n_c+M`.

For fixed helper entropy margins, `n_c=O(log((n_Gamma+1)/epsilon))`. The reference transport is constant-rate in source calls rather than a polylogarithmic cost PER reference. The `c` multiplier applies to warm acquisition AND every reference carrier; it never applies to the single-use data or payload slots.

## 6. Complete-bank transfer and final guarantee

Work in (1)'s exact double-coordinate representation; fix `U_D,U_H` and the entire warm record. On `G`, the learned helper satisfies (3)-(5). For each sampled descriptor, compare its ACTUAL decoded reference channels with identity on the SAME logical FIFO wires, including stored data and future preparations as arbitrary external references/testers. For every block the uniform fixed-code diamond bound is valid on the entire reference-correlated operator space. Sum the B bounds and average the code descriptor. The shared code's qualities may be correlated; independence of qualities is never used. Its one sampler failure costs at most `2 beta_gen`.

This replacement occurs ONLY in the virtual causal comparison. No actual helper source/frame steps are physically deleted, and neither frame memory is reset. The fact that old data can be entangled with currently transmitted reference inputs is exactly what complete norm and the typed-comb identity cover. In the ideal comparison the returned bank is precisely `Gamma_(U_D)^tensor n_Gamma`, independent of the helper code descriptor conditional on the coordinates and warm history. Helper flags may be discarded, or matched to the exact-reference input-independent flag law in the comparison; private Pauli keys, syndrome environments, source environments and frame memories are not tested outputs.

Define the ideal comparison on bad warm histories too by supplying this exact Gamma bank and running the prescribed feasible learner, with dummy metadata when necessary. The ideal learner guarantee is uniform in both coordinates/history. The one bad warm event costs at most `2 beta`; (9) costs at most `delta_ref` on good histories. Therefore the full reconstructed-bank/learning/deployment transfer costs ONLY

`2 beta+delta_ref`.                                    (11)

The actual reconstructed bank need not be iid or low rank. The same globally CPTP learner is applied to both experiments, and contractivity transfers (11); no low-rank tomography theorem is applied directly to a contaminated actual bank. Extra flag leakage/marginal specifications must be explicitly paid if retained; the theorem below discards all calibration and helper side records.

Let `a_*=1-ell_*` and let the benchmark be the received omniscient SAME one-use encoder-family optimum, allowing arbitrary collective physical decoders but no cross-use payload encoder or extra payload-dependent calls:

`delta^*_(family,M)=2[1-a_*^M]`.

For the ideal learner, every realized fidelity `f<=a_*`; private per-payload Pauli frames give output discrepancy `2[1-E f^M]`. The elementary bounds `a_*^M-f^M<=M a_*^(M-1)(a_*-f)` and `M a_*^(M-1)(1-a_*)<=1-a_*^M`, together with (7), imply

`||Lambda_ideal-id||diamond<=(1+gamma)delta^*_(family,M)+2M e`.

Now add (11) and the SINGLE paid finite WHOLE interactive discrepancy `nu`. Since `2M e+2 beta+delta_ref+nu<=epsilon`,

`||Lambda_actual-id||diamond<=min{2,(1+gamma)delta^*_(family,M)+epsilon}`.  (12)

All norms are unhalved. This is an averaged complete-output theorem, not a good-realized-code/record assertion, and not an unframed generic diamond-optimality claim. For one use it has the received Bell-risk interpretation. The final family receiver is reusable only with the preserved D-frame and within the declared horizon/accuracy budget, not as a bare physical-space classical decoder forever.

## 7. Every non-source resource remains paid

* **Frames:** separate `poly(H_D,K_D,log s,log(1/nu_D))` and `poly(H_H,K_H,c log s,log(1/nu_H))` known gate/arithmetic/workspace bills under the received explicit causal compiler. A coarse logical memory bound is `O(H_D(log s+log K_D)+H_H(c log s+log K_H))` qubits, plus the actual compiler's polynomial encoding/workspace. The memories and their idle noise persist for the whole real chronology, including code construction and classical optimization. No claimed dimension-only compression erases this cost.
* **Helper warmup:** `N_W` reduced helper outputs plus local conjugate states, purification/finite-Clifford tomography, one finite-feasible TNI SDP, and known-matrix instrument synthesis are paid. The source scaling is `c O(R_H^2 log(R_H/beta) max(Delta^-2,U^-1))`. Actual rank/output truncation is not inferred from a small observed error.
* **Code:** one uniform descriptor, finite capped generation, sender communication of that descriptor, known dense stabilizer encoding/syndrome circuits, per-block flags, private keys and receiver compilation are paid. For an encountered flag string the brute-force representative table costs `4^n_c poly(n_c)` work/storage; processing B strings costs at most B times this, or cached distinct-string tables with their own memory. Enumerating every possible flag string in advance would cost `8^n_c` and is unnecessary. This is polynomial in `n_Gamma/epsilon` only for FIXED public margins, with potentially absurd exponent; it is not a practical or uniform-small-gap decoder.
* **Memory/latency:** sender FIFO/codeword memory is `O(k_c+n_c)` logical qubits plus `c`-rail preparation workspace; receiver transient carrier memory is `O(n_c log K_H+c log s)` plus decoding workspace. The coherent bank is `n_Gamma(log K_D+3)` qubits plus learner workspace. A block incurs `c n_c` raw-source calls before reference delivery. A triple may wait through two blocks; all earlier data remain stored until the bank is processed. Calibration and all its compilation finish before unknown payload arrival. Later payloads cost one raw use each plus local decoding/frame latency, not zero latency.
* **Gamma controls/optimizer:** `n_Gamma` Bell/control preparations, all calibrated relative phases, random purification, finite-Clifford measurements, `O(eta_opt^(-3/2))` known quaternion-net SDPs, finite feasibility/optimization arithmetic, and final receiver synthesis are retained from the coherent bridge. Supplied encoder circuits may themselves be large; charge actual gate counts rather than claim polynomial in `log p`.
* **Keys and finite faults:** outside warmup there are `2(n_c B+M)` private Pauli random bits and corresponding pre/post operations. Key distribution/storage is a paid private CLASSICAL control interface. Set a deterministic cap on EVERY gate, classical compilation, source-control preparation, storage interval, frame update, syndrome/readout and receiver application. Allocate `nu` by per-step complete-channel/strategy errors whose sum is within its budget. The two processors' errors add; they are not one free frame. Errors already assigned to eigenvalue/SDP precision or sampler bad mass are not charged again. Unknown drift/correlated hardware faults are not inferred iid or corrected away; they require the promised uniform interactive error bound.

## 8. AD(0.4), the honest baseline, and scope

For amplitude damping `d=2/5`, the fixed two-rail helper `|0>->|01>`, `|1>->|10>` uses `c=2`. Its support is the vacuum plus one-excitation subspace and its encoded Choi rank is exactly `R_H=3`; the safe unspecialized raw-rank bound would be `2^2=4`. There exists an unknown-to-learner success decoder with `a_0=3/5,u_0=0`. Choose `A=11/20`, `Delta=1/20`, `U=1/1000`. Ordinary acquisition learns a qualifying instrument; it is NOT handed the parity filter or unknown output rotation. Known dual-rail input preparation remains supplied.

For example `eta=1/1000`, `h_*=93/100`, `R_c=1/50`, `xi=1/50` are conservative valid public code constants: the expanded entropy bound is below `.925<.93`, and their sum is `.97<=1`. The receiver-flag code therefore transports the Gamma references despite the received COMPLETE one-use qubit CPTP pre/post Pauli-entropy optimum being `1.016023193904...>1` for the raw AD(0.4) source. The better known ideal dual-rail erasure entropy `.8` is not silently substituted for the more conservative acquired `A,U` certificate.

This example says the helper acquisition/transport promise can hold where every single-use qubit unflagged Pauli seed fails. It does not make the quaternion optimization nontrivial for a bare two-dimensional input (input unitaries can be absorbed into unrestricted recovery), nor does it determine AD capacity. The theorem's useful near-optimal family objective concerns generic supplied higher-dimensional encoder families satisfying its separate data/control/rank contract.

**Direct payload coding is simpler for communication.** Once the SAME helper is acquired, transmit M unknown logical qubits directly through its conditional-flag code. With code block length `n_P`, `k_P=floor(R_c n_P)`, and transport target `epsilon/2` in place of `delta_ref`, the same stopping/sampler rule gives

`N_raw,direct=c[N_W+n_P ceil(M/k_P)]`,
`||Lambda_direct-id||diamond<=2 beta+epsilon/2+nu<=epsilon`.

It needs no Gamma bank, controlled anchors, data frame or global encoder optimizer. Its asymptotic payload rate is `R_c/c`, with block latency `c n_P`. The optional Gamma route buys a near-optimal reusable ONE-USE family encoder/receiver (with preserved frame), and potentially useful later one-use port rate/latency when `ell_*` is small; it does not guarantee this and does not outperform a positive-rate helper code for general communication merely by matching a noisy benchmark. If `ell_*>0`, its M-use bound may saturate at two. Both protocols pay local controls, memories, rank promises, reset assumptions and all source calls.

The equally informed conventional learner can run exactly this tomography/SDP/code construction. This is not a quantum-learning speed separation, a universal positive-capacity detector, protection against unqualified hardware noise, a novelty assertion about Schur compression/QEC, or a published result.

## 9. Evidence and receiving boundary

`heralded_typed_reference_checks.py/.json` tests the two-type arbitrary-operator identity with different physical/reduced dimensions and complex support rotations; explicit reference-correlated non-Hermitian operators; known data-first/flag-code complete-channel contractions; the AD block rank/entropy example; exact FIFO labels, ceilings, raw-call factors and rational error budgets; and finite log-domain block choices. These are finite mathematical diagnostics, not sampled collective tomography, execution of astronomical dictionaries, a frame circuit or hardware.

The typed-frame proof received a separate local review while under construction. The final manuscript requires its hash-bound independent receiving before promotion. Imported received sources are unchanged: ordinary heralded acquisition; flagged conditional-entropy coding; block-reference entropy bootstrap; coherent unrestricted-recovery bridge; explicit causal frame compiler and its receipts. No external publish, push or upload is part of this work.
