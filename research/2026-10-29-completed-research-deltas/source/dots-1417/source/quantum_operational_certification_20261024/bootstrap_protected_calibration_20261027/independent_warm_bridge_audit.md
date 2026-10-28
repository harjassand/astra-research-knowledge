# Independent warm-seed and protected-calibration bridge audit

27 October 2026. Reviewer: `producer-workspace/audit_bootstrap_warm_bridge`. **PASS within the stated mathematical/trusted-control scope.** This is a separate internal proof audit, not external peer review, a hardware result, or a novelty assessment. Frozen files and their hashes are in `independent_warm_bridge_receipt.json`.

## Received scope and selective imports

I read the complete bootstrap proof and selectively checked the actual six-bank positive-risk/confidence proof, coherent Gamma support/rank/contraction/risk/net proof, exact private-framed comparator proof, and explicit online compiler. I verified the compiler's canonical hash against its independent receipt. The separately enumerated five-qubit module is imported from `../bootstrap_five_qubit_pauli_independent_receipt_20261027.md`; I did not duplicate its exhaustive Pauli classification. The root's latent-good-event note supplies a complementary composition check, not a premise of this audit.

The imported six-bank confidence result is pointwise in a fixed virtual frame, not conditioned on every exposed record. Its finite statistical arithmetic is deterministic; actual approximate quantum controls are charged only in the later whole-process comparison. The coherent support proof legitimately uses the union of four anchor environment supports and physical output supports: `rank Gamma <= 4R`, `rank J_x <= 4R`, and common output dimension `k=min(s,8R)`. A seed-only support bound would be wrong but is not used. The support applies also to off-diagonal reference blocks, so the compiler's arbitrary-operator/reference/causal law applies to entangled source calls.

## 1. Warm acquisition and validation

For a fixed decoder the true loss quadratic has spectrum in [0,1]. At a global minimizing pair the minimizing x is an eigenvector. Therefore its loss increase at chord distance h is at most h². Signed-face rounding and normalization give h²<=3/m0²<=Delta; no nonsmooth optimized-loss differentiation is used. There is a candidate with optimum loss at most ell_*+Delta.

The six-state input bank ranks are bounded by `min(4R,k)`, and all banks use the SAME persistent frame. With `m_w=Delta²/96`, `eta_w=Delta²/8`, and `gamma_w=Delta`, the two additive risk terms sum to Delta. The multiplicative excess is at most Delta because true loss is at most one. The union over K candidates uses the stated logarithm `log(12 D_w K/beta_t)`. Thus with probability at least `1-beta_t`, the distinguished candidate has loss at most `ell_*+3Delta <= p0-Delta`.

All decoders are fixed before fresh holdouts. Conditional on U and the complete training record, a holdout mismatch has mean `2p_j/3`; independent reset calls and private random six-label inputs justify Hoeffding. For radius Delta/2 in p, the mismatch radius is Delta/3, so `2 exp(-2v Delta²/9)` and the displayed v give failure at most beta_v/K. No independence between candidate training records is required.

On validation event V, every accepted candidate has p<=p0. On T intersect V at least the distinguished candidate passes. Consequently the SINGLE union event `abort OR (accept AND p>p0)` lies in `T^c union V^c` and has mass at most beta_t+beta_v. One must not sum separate abort and false-accept bounds and lose an extra beta_v; the proof does not. The unconditional theorem includes replacement outputs upon abort. Its optional acceptance-conditioned ratio correctly divides by an acceptance lower bound.

## 2. Causal chronology and independent errors

Warm banks, holdouts, each Gamma datum, EVERY carrier codeword output, and final payload outputs enter one compiler initialized with the entire predetermined horizon H. Its memory is retained through quantum measurement and classical computation. The exact compiler supports adaptive linking, not merely parallel-product input identities. U is only a latent decomposition; after observing warm records its posterior need not be Haar.

For each fixed U,w, the selected seed decoder and encoder are fixed and each fresh reset call has the same local channel. Independent private Pauli frames therefore give a tensor power of a fixed Pauli channel as a COMPLETE map. Entanglement with other codeword qubits, stored Gamma data, or prior source environments does not invalidate tensor factorization of the channels. Averaging over U,w afterward generally produces correlated channels; this average is nowhere replaced by a tensor power of its marginal. The theorem does not infer iid noise from a holdout.

The sender first makes the Gamma data call, while I,A remain local, then encodes and sends all three references through actual seed calls. No original reference is transported around N. Receiver-local retained frame memory and local coherent sender storage are trusted and explicitly charged; neither transports the unknown payload around N. Controlled known anchors, not a controlled unknown source, prepare Gamma. The private key interface is an additional paid classical resource.

## 3. Whole-bank comparison and warm failure

The ideal comparator has the same warm U,w distribution, supplies ideal reference transport, and continues even on histories where the physical protocol would abort. This is a comparison channel, not an implementable free link. On accepted good histories the conditional complete reference-transport discrepancy is at most `6 n_Gamma p_L <= nu_ref`. The good/bad event depends only on pre-payload variables. On the rest, two normalized channels differ by at most two. Integrating gives `2(beta_t+beta_v)+nu_ref` without conditional-success normalization.

The common-U representation is taken only after linking all physical frame steps. Replacing reference-transport channels in that virtual process is legitimate; deleting frame steps in a physical circuit and resetting the frame would not be. For fixed U,w the ideal future Gamma bank is iid Gamma_U even on warm abort histories. Its downstream expected-risk bound is uniform in those variables, so correlation of the good event with U cannot skew the ideal comparator into a worse target. The actual noisy bank need not retain the low rank. The same globally CPTP learner acts on both banks, but its rank-based theorem is invoked only on the ideal bank.

Actual finite-control errors are compared at the whole interactive-process level and add nu_fin. The actual approximate frame is not assigned a fictional exact U. This includes errors in warm acquisition: no unproved beta-scale confidence event is asserted for the approximate implementation.

## 4. Global risk and exact comparator

The coherent tomography allocation yields `m<=gamma e/512`: its sampling and arithmetic terms are each at most `gamma e/1024`. Together with `eta<=gamma e/16`, the positive-risk inequality gives additive local loss `e/2=epsilon/(4M)`. The feasible learned decoder is retained in its own continuing frame; there is no fresh recovery factor.

For every U,w,g the fidelity f of the selected family encoder/decoder obeys `f<=a*=1-ell_*`. Conditional payload channels are tensor powers of the privately twirled fixed channel; their mixture has identity-Pauli mass E f^M. The pointwise inequalities

`a^M-f^M <= M a^(M-1)(a-f)` and `M a^(M-1)(1-a)<=1-a^M`

transfer expected one-use regret to `2[1-E f^M] <= (1+gamma)2[1-a^M]+epsilon/2` without assuming independent learned errors. The exact collective-decoder fidelity tensorization has a positive SDP dual; its product certificate is valid, including key-dependent decoder families via the Bell lower bound. Optimizing over fixed family encoders or randomizing their pre-payload choice cannot beat the best a*. This is the specified private-framed comparator, not a generic unframed diamond optimum or a cross-use payload encoder.

Finally, `2(epsilon/32+epsilon/32)+epsilon/8+epsilon/4=epsilon/2`. Adding the ideal learner's epsilon/2 proves the claimed epsilon. The bound is on logical payload outputs only; keys, records, syndromes and frame memory are not exported.

## 5. Source, local computation and storage accounting

The deterministic source cap is `K(6n_w+v)+n_Gamma(1+3*5^L)+M`. It counts all candidates and all carrier calls, including failed holdout candidates, with no retry or normalized postselection. For fixed p0 and Delta, n_w is O(R² log(R/beta_t)), K is constant, and n_Gamma is O(R² log R M/(gamma epsilon)). The factor `5^L=O(log(n_Gamma/nu_ref)^(log_2 5))` is necessary and explicitly retained in the soft-O cap.

The compiler's cost is polynomial in the ENTIRE H,k,log(s),log(1/nu_fin), not merely n_Gamma. The finite encoder net and full-CPTP SDPs are polynomial for the fixed three-dimensional family; actual supplied physical preparation/control costs are separate. Known learned decoders are synthesized feasibly, and all seed uses and M final uses enter the gate/error cap. No polynomial-in-log-input-dimension synthesis of an arbitrary encoder is claimed.

Storage includes warm quantum banks until measured, the full reduced Gamma bank and learner workspace, sender codewords/references, and the long-lived compiler memory (which can grow with H and log s). Logical dimension k registers should of course be embedded into ceil(log2 k) qubits; unrounded log k storage expressions are asymptotic dimension shorthand. The construction is not a constant-memory streaming decoder or an indefinite-horizon reusable physical decoder. Waiting-time/local-memory errors require the stated uniform complete implementation budget; no unknown hardware error suppression follows from warm validation.

## Evidence and limits

`independent_warm_bridge_checks.py` passed exact-rational warm/budget identities, 9,200 scalar batch-regret cases, nine coding-cap allocations, and a shared-latent-mixture negative control. These checks complement the analytic proof above and do not execute high-dimensional Schur/CG, purification or fault-tolerant hardware. No required mathematical edit was identified in this reviewed scope. Final receipt binds the precise proof snapshot; later changes require a new hash and relevant recheck.
