# Bell-diagonal mass to compiled subsystem preservation
Date: 2026-10-29. Status: new derivation and reproducible finite checks; independent review pending. No priority, hardware, or generic-capacity claim.

## What changes
The v1 compiler assumed samples from a promised Pauli subspace, with uniformity/excitation sufficient to identify its complete support. Complete identification is unnecessary for an approximate one-shot preservation guarantee. For **any stationary CPTP channel**, coherent process off-diagonals included, Bell samples plus a mixed-gauge Clifford encoder give a directly certifiable entanglement-fidelity guarantee. No Kraus list, environment reconstruction, or distribution over an exponentially large error set is acquired. The positive-rate condition is still highly structural: sampled errors must span a symplectic subspace with a nontrivial complementary subsystem. Generic samples exhaust the physical space and leave zero logical qubits.

This is a conventional noiseless-subsystem/stabilizer mechanism made operational, not a claim to a new quantum error correction principle. Its role in Astra is to bypass an interface-specific full-reference-row normalization obstruction by compiling the **actual logical decoder**, rather than representing the same expensive polar operator with compact labels.

## Interface and exact identity
Use Hermitian n-qubit Paulis P_v, v in F_2^(2n), with Tr(P_v P_w)=d delta_vw, d=2^n. A stationary CPTP map has Kraus expansions K_r=sum_v c_rv P_v and positive process matrix chi_vw=sum_r c_rv conjugate(c_rw). Trace preservation gives sum_v chi_vv=1. Prepare n trusted Bell pairs, send one half through the channel, and perform n trusted Bell measurements: the label v has probability p_v=chi_vv. This assertion does not require Pauli-diagonal noise.

Let U be any **actually synthesized** Clifford, and split its output into t gauge qubits G and k=n-t logical qubits L. Implement

  Enc(rho)=U†[(I_G/2^t) tensor rho]U,
  Dec(sigma)=Tr_G[U sigma U†].

Write U P_v U†=phase_v Q_g(v) tensor Q_l(v). Define T_U={v:l(v)=0}. Then the induced logical channel has exactly

  Fe(Dec o E o Enc, I_L/2^k) = sum_{v in T_U} p_v.                 (1)

Proof: its Kraus operators are (1/sqrt(d_G)) <i|U K_r U†|j>, for r,i,j. Fe is the sum of squared Kraus traces divided by d_L². Every term with nonidentity logical Pauli has zero logical trace. For the remaining terms, summing i,j yields Hilbert-Schmidt orthogonality of distinct gauge Paulis: Tr(Q_g Q_h†)=d_G delta_gh. Thus all process off-diagonals cancel and the remaining sum is precisely (1). Equivalently, the recovered logical process matrix is a partial trace over gauge Pauli coefficients.

This proof does not assert that the whole logical channel is Pauli-diagonal. Fidelity is entanglement fidelity on the maximally mixed logical state; it is not a dimension-free diamond-norm guarantee on arbitrary payloads. A subsequent logical Pauli twirl would make the corrected channel Pauli and turn 1-Fe into half-diamond distance, but requires shared fresh trusted logical Pauli controls and changes the protocol. See the addendum below.

## Learning and compiling an error algebra
Given sampled labels, compute their binary span S. If dim S=m and its restricted symplectic form has rank 2a, the radical has dimension b=m-2a. Symplectic elimination with elementary H,S,CNOT,SWAP produces U such that

  U span{P_s:s in S} U† = M_(2^a) tensor Diag_(2^b) tensor I_(2^k),
  t=a+b, k=n-a-b.

The implementation in algebra_compiler_v1.py updates binary rows at each actual gate; no dense U is required in the scalable path. At each step it maps a nonzero pivot to Z_t, maps a symplectic partner to X_t when present, and clears their columns in all remaining rows. Remaining commuting pivots become Z on successive qubits. There are O(n²) gates and polynomial binary classical processing (the simple pair-search implementation is not optimized). Decoding uses U; encoding uses its gatewise inverse, with S† available as S³. SWAP is three CNOTs when required. Mixing t gauge qubits requires t private unbiased classical bits and computational-basis preparation, or Bell pairs with one half discarded. The random bits are not needed by the decoder.

S is contained in T_U, so (1) gives Fe >= p(S). In exact support cases, the corrected logical channel is the identity, even for coherent Kraus combinations, since every Kraus factors as B_r tensor I_L. For approximate support, mixed gauge is load-bearing.

### Pure-gauge counterexample
For one gauge and one logical qubit take V=|0><0| tensor X + |1><1| tensor I. Its diagonal process mass on logical-identity Paulis is 1/2. Pure gauge |0> produces logical X and Fe=0; mixed gauge yields Fe=1/2 exactly. Therefore a pure-sector encoder cannot inherit (1) merely from full-input Bell data. With exact algebra support pure gauge remains valid; it is the approximate mass transfer that fails.

### Distribution-free mass coverage, not exact support learning
Let D=2n. Fix epsilon,delta in (0,1), t_batch=ceil(log((D+1)/delta)/epsilon). Draw (D+1)t_batch iid Bell labels, divided into D+1 batches, updating the span. At most D batches can increase its dimension. Hence some batch contains no innovation. Conditional on the preceding history, if current outside mass exceeds epsilon, the chance that a whole batch lies in the current span is at most (1-epsilon)^t_batch <= delta/(D+1). A union bound over batches shows final outside mass is at most epsilon with probability at least1-delta: otherwise monotonicity makes every earlier outside mass exceed epsilon, contradicting the inevitable no-innovation batch except on the bounded failure event.

Thus O((n/epsilon) log(n/delta)) samples suffice for approximate coverage, regardless of minimum nonzero error probability. There is no uniform finite guarantee of finding *every* rare generator. If an a priori support dimension bound m is known, D can be replaced by m. One can terminate at the first no-innovation batch, retaining the same union bound over at most D+1 batches. Generic p can force k=0; this is not a useful universal-rate code. Small rare outliers can unnecessarily increase span rank; robust subspace selection at fixed rate is a separate unsolved optimization obligation here.

For a frozen trained U, fresh held-out Bell labels can validate membership in the larger corrected set T_U directly, rather than the smaller training span. With zero failures among h iid holdouts, outside mass >epsilon is rejected with failure probability at most exp(-h epsilon). Reusing holdouts adaptively requires a union bound or an anytime-valid rule. General failure counts permit exact binomial confidence intervals. No laboratory samples have been acquired in this work.

### Optional affine shift
A deterministic unknown Pauli need not cost a gauge qubit. Choose one initial sampled label v0, learn the span of differences v+v0, and apply the known Pauli P_v0† to the channel output before U. Left multiplication shifts process labels (phases are irrelevant to their probabilities). The same argument applies to the shifted distribution. Conditional on the first sample, subsequent labels remain iid; the batch proof is unchanged. This is elementary Pauli-frame correction, not a new mechanism.

## Actual encoded-row factorization and normalization
For exact algebra support and a fixed computational gauge basis vector j, write C_j=U†(|j> tensor I_L). Each error satisfies

  U P_s C_j = (B_s |j>) tensor I_L,
  U [P_s C_j]_s = [B_s |j>]_s tensor I_L.

The unknown physical Kraus combinations likewise factor. The decoder extracts the logical tensor factor directly; it does not invert or block-encode the first factor. **Do not infer the reference row has norm1.** For uniform Pauli gauge algebras its row norm can still grow exponentially. The scientific escape is that no polar transform of that row is needed. A binary label map is sufficient for actual Clifford synthesis because the algebra is Pauli-generated. This does not extend the fixed-defect Schur compiler to generic extensive Schur sectors.

## Acquisition, calibration, and resource restrictions
- Channel calls must have the same stationary map; probe/payload drift or memory is not controlled by this theorem.
- Requires n trusted retained reference qubits, Bell preparation/measurement and arbitrary physical Clifford controls with enough connectivity/routing. Does not learn an unknown tensor-product basis or an unknown non-Clifford embedding.
- Bell preparation/readout uses O(n) ideal elementary operations; compiler encoder/decoder O(n²) before routing. For adversarial gate errors, diamond errors add, so total control error must be budgeted; constant per-gate error cannot silently be held fixed while n grows.
- If acquired Bell distribution q is known within total variation zeta of p, the coverage guarantee transfers as Fe >=1-epsilon-zeta. This requires actual calibration, not presumed clean probes.
- If implemented encoding/decoding composite differs from ideal by half-diamond distance eta_ctrl, entanglement-fidelity loss is at most eta_ctrl. All preparations and randomization are part of that implementation budget.
- No tomography cost is hidden: stored span at most2n binary rows of length2n, plus the emitted O(n²) gate list. Dense matrices in v2 are small validation fixtures only.

## Conventional comparator and unresolved significance
This is standard noise-algebra/noiseless-subsystem structure and symplectic stabilizer elimination with task-specific Bell acquisition. An equally informed conventional learner can implement the same algorithm. It proves that Astra's full-reference normalization barrier is not a universal operational barrier and removes the earlier uniform/excitation assumption for *approximate* mass coverage. It does not establish a comparative speedup over conventional adaptive QEC, positive capacity under broad unrestricted noise, an unknown-frame discovery algorithm, optimal protected rate, or a practical fault-tolerant device architecture.

Conventional stabilizer codes can correct error sets that do not act trivially on a common subsystem; this algorithm deliberately does not exploit that stronger Knill-Laflamme possibility. Particularly, taking a linear span of rare outliers can destroy all logical rate even when a standard sparse-error correcting code performs well. A serious next mechanism must preserve high-probability error geometry rather than indiscriminately close it into an algebra.

## Reproduction and evidence
Run `python coherent_mixed_gauge_v2.py`. The four n=2..4 coherent random-isometry CPTP checks agree with (1) to below2e-16; the pure-gauge counterexample is included. These are checks, not the proof. `algebra_compiler_v1.py` includes an n=128 binary fixture and small dense operator-factor tests; no exponential matrices are used in that large fixture. No independent review completed yet.

## Primary-source context (not novelty clearance)
- Knill, Laflamme, Viola, Theory of Quantum Error Correction for General Noise, PRL84 (2000), https://arxiv.org/abs/quant-ph/9908066 : conventional subsystem foundations; bibliographic/source verification still to be completed before precise reliance.
- Wagner et al., Learning Logical Pauli Noise in Quantum Error Correction, PRL130200601(2023), https://arxiv.org/abs/2209.09267 and https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.130.200601 . Primary abstract retrieved 2026-10-29: logical Pauli channel estimation from syndrome data for stabilizer/subsystem/data-syndrome codes; this is a strong task-specific learning comparator, not the same input interface.
- Learning Noise-Robust Stabilizer Structure via Bell Sampling, https://arxiv.org/abs/2610.03307 . October2026 abstract retrieved via https://quics.umd.edu/publications/learning-noise-robust-stabilizer-structure-bell-sampling . Its finder-verifier response to corrupted samples is directly relevant to the outlier/rank failure. No theorem from it is imported here without reading its governing arguments.
- Cotler, Gong, Kannan, Noisy Quantum Learning Theory, https://arxiv.org/abs/2512.10929 ; https://www.nature.com/articles/s41467-026-73693-x . Primary abstract retrieved: ideal Bell/SWAP learning primitives can lose advantages under uncorrected acquisition noise. Here trusted acquisition is explicit, not a solved hardware interface.

## Logical twirl addendum: dimension-free payload guarantee
Choose a fresh uniform k-qubit Pauli Q (2k classical bits), apply Q before the ideal encoder, and apply Q† after the ideal decoder. The sender and receiver need the same key (stored locally for a memory, or a reliable shared classical link for communication); the stationary channel must not depend on the key. Average over and then discard that key. The logical channel becomes its Pauli twirl, whose identity probability is unchanged Fe. For a Pauli channel, its half-diamond distance to identity is exactly1-Fe: the upper bound follows from convexity, and the matching lower bound from a maximally entangled input producing orthogonal Bell errors. Therefore (1), with this extra implemented randomization, gives a dimension-free all-payload error bound p(T_U complement), plus acquisition/control budgets. This is ordinary randomized compiling, explicitly paid here. It is an averaged channel guarantee, not a per-key claim. Without this operation the earlier Fe-only scope remains governing.

Source check update: the original quant-ph/9908066 abstract was fetched directly and confirms the subsystem/operator-algebra foundation. Tang–Steckmann2610.03307 is v2, revised2026-10-05. The links and abstracts are context only; the current derivation is self-contained.
