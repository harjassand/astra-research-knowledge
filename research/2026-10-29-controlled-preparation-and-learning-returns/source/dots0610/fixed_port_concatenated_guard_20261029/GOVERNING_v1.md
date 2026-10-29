# Fixed four-spin-port gap-free guarded recovery via verified concatenation
2026-10-29. New compiler/composition, awaiting independent review. Conventional coding ingredients are explicitly attributed; no new random-code existence or channel-capacity theorem is claimed.

## 1. Objective and physical scope
The preceding n=4log2B construction varies source size. Here the source port is FIXED at four physical spins, preserving one logical qubit per native service through the reviewed four-spin encoder/permutation-orbit/total decoder. The source has arbitrary retained memory and a fixed unknown full-joint collective frame. There is no occupation-gap premise. The same three-edge online learner acts on the actual interleaved sequence, rather than predicting a separately chosen future channel.

We construct a finite outer qubit code of constant rate and linear native-fault tolerance using an explicitly generated/verified small stabilizer code concatenated with the received full-field quantum Reed-Solomon/CSS outer code. Endpoint storage/gates, private controls, complete source-port isolation, record retirement, generation cost and online-learning arithmetic are paid resources. This is a source-exposure-rate theorem for this structured fixed-port process with guarded abort, NOT unassisted memoryless capacity, a total-computation-rate advantage or a hardware threshold.

## 2. Uniform finite inner-code generation
Let B=2^h, h>=5, ell=16h, k=h and r=ell-k=15h. Work in V=GF(2)^(2ell) with symplectic form [(x,z),(x',z')]=x.z'+z.x'. Sample independent isotropic generators sequentially. Given S_j of dimension j, compute a GF2 basis of S_j^perp and draw a uniform linear combination using dim(S_j^perp) fair bits. Reject if the vector lies in S_j; otherwise adjoin it. The membership rejection probability is2^(2j-2ell), at most2^(-2h-2). Each accepted vector is uniform in S_j^perp minus S_j. Every ordered isotropic basis has the same probability, and every r-dimensional isotropic subspace has the same number of ordered bases. Thus the final S is uniform over isotropic r-subspaces. This proof does not replace uniform sampling by a short random Clifford walk.

For each fixed nonzero v, symplectic transitivity and counting give

 Pr[v in S^perp]=(2^(ell+k)-1)/(2^(2ell)-1) <2^(-15h+1).

Verify the candidate by enumerating EVERY nonidentity Pauli label of weight<h and rejecting the entire code if any has zero syndrome against S. This stronger purity check excludes even low-weight stabilizers, and guarantees quantum distance at least h. It is not an estimated random-distance test.

The volume is at most sum_{w<=h} binom(16h,w)3^w. Taking x=1/48 in (1+3x)^(16h), this sum is <=48^h(17/16)^(16h)<(48e)^h<144^h<2^(8h). A union bound therefore makes code rejection probability beta0<2^(-7h+1). Reuse ONE accepted inner code for all B blocks; independent per-block random codes are not necessary for this conservative distance product.

With at most R code candidates and L_bit attempts per generator, a finite generation abort bound is beta_code<=beta0^R+Rr2^(-L_bit), using the looser rejection<=1/2 bound. All candidate verification is classical and occurs before using an unknown payload. Successful code acceptance is exact; rejected/aborted runs do not deploy an unchecked code. Low-weight verification has O(B^8 poly(h)) bit cost and a deterministic finite cap, not a free oracle. Larger exponents are polynomial but practically material.

## 3. Actual Clifford encoder and total inner decoder
Reuse the received `learned_pauli_algebra_compiler_20261029/algebra_compiler_v1.py`, copied unchanged as `received_algebra_compiler_v1.py`. On isotropic S it produces an actual H,S,CX,SW circuit U mapping its binary span to Z on the first r ancillas. The code is DEFINED by the inverse actual circuit:

 E_in|psi>=U†(|0>^r tensor |psi>).

Thus the stabilizer phases are induced by U, not assumed from unsigned binary labels. Encoder inverse gates are reversed, with S replaced by S† (or three S gates). The checker tracks exact Pauli conjugation in the convention i^phase X^x Z^z: H adds2x_j z_j and swaps x_j,z_j; S adds x_j and replaces z_j by z_j+x_j; CX and SW have their actual binary conjugation with no extra phase in this convention. Dense checks compare these rules with the actual circuit matrices. Receiving review caught a tensor-order/table-order mismatch in the first dense fixture; reversal of measured tensor indices is now explicit and a locally scrambled code checks that the original symmetry cannot mask it.

Let u=floor((h-1)/2). Enumerate all Pauli errors of weight<=u, conjugate each through U, and record its ancilla X syndrome plus its h-qubit logical Pauli. Verified distance makes the logical correction unambiguous; our stronger purity check actually makes all these syndromes distinct. On the received ell-qubit block: apply U, measure the first r ancillas and pack the classical syndrome as sum_j outcome_j*2^j (wire0 is the least-significant TABLE bit, independently of tensor-array indexing), and apply the inverse recorded logical Pauli to the remaining h wires. For unlisted syndromes apply identity (or any declared fixed correction). Discard all measured ancillas/records under the trusted retirement scope. ALL outcomes have a defined output; there is no postselected decoding success assumption.

This corrects the linear span of all weight<=u errors by the Knill-Laflamme condition, including coherent errors entangled with retained source memory. A phase difference between errors with a common syndrome affects only discarded syndrome/environment amplitudes, not the corrected logical state. It cannot simply be dropped in a physical simulation; the provided phase-aware checks retain it. Sparse lookup avoids storing all2^(15h) syndromes: only the enumerated low-weight representatives are needed, with a default for every other outcome.

## 4. Concatenation and the constructive correction guarantee
The received GF(B) full-field CSS/GRS code has B symbols, B/2 logical symbols, and corrects t_out=B/8 arbitrary symbol errors. It has explicit finite-field generation, binary Clifford encoding and total syndrome decoding. Encode its h-qubit symbols with the SAME verified [[16h,h,>=h]] inner code. The concatenated block has

 N=16hB native one-logical-qubit service slots,
 K_payload=hB/2 logical qubits.

Use the actual two-stage total decoder: inner decoders on all B blocks, then the received total outer decoder. Let

 t=t_out(u+1)=(B/8)ceil(h/2).

Any Pauli error of weight<=t has at most t_out inner blocks with more than u errors. Inner decoding corrects all other blocks; its residual is an arbitrary h-qubit error only on those at most t_out blocks. The outer decoder therefore corrects it. The same concatenated recovery corrects the entire error span: syndrome measurement and correction linearity/Knill-Laflamme apply to superpositions and source-memory coefficients, not merely the sampled Pauli labels used in tests. Interspersed native source-memory operations do not enlarge support on untouched service slots.

In particular t>=N/256. The decoder's guarantee is deliberately conservative; it is not an assertion that this two-stage decoder achieves half the full product minimum distance. No independent-error distribution is assumed. Inner and outer circuits and endpoint ancillas are separate from the four-spin source interface and their noise is not silently corrected for free.

## 5. Finite guard on one fixed physical port
For n0=4, d0=2, A0=2^4/d0=8, C0=(4+2)/(4-1)=2. Use the received gap-free rational three-edge learner with

 p=1/3 (learning), s=2/9 (service), a=4/9 (matching validation),
 J=N, T=9N, b=floor(t/4).

Sample the current candidate privately BEFORE its independent role; update experts only from actual learning records. Every service handles exactly ONE of the N native qubits using the same fixed four-spin port. Complete the Jth service before evaluating cap exhaustion, including on call T. Stop on b+1 validation failures or a sampler abort. After stopping, use only the reviewed mathematical zero-loss extension in the proof, not extra physical source calls.

For arbitrary source noise, the orbit/matching hazard ratio is C0 s/a=1. The previous three-role arbitrary-memory guard and the constructive outer correction therefore give

 (1/2)||A_acc-id_payload tensor B_acc||diamond
 <=Pr[Bin(t+b+1,1/2)<=b]
 <=exp(-3t/16)<=exp(-3N/4096).                         (1)

For the Hoeffding bound use t-b+1>=3t/4 and t+b+1<=3t/2 for t>=4. Learning rounds are neutral, and the finite cap only discards branches. B_acc is the actual accepted coarse-memory instrument under the reviewed retirement convention.

Under the fixed hidden full-joint collective-algebra promise, the actual-history learner gives expected cumulative edge loss<=3L_T. Matching failure<=raw Bell loss and orbit correlated-input closure imply expected validation failures<=a*8*3*L_T=(32/3)L_T. Since b+1>t/4>=N/1024, Markov and private role-coin shortage give

 Pr[accept]>=1-exp(-N/4)-(32768/3)L_T/N
              -beta_sampler-beta_code.                (2)

The exact tighter form uses (32/3)L_T/(b+1). With epsilon=T^(-1/4), the rational net and dyadic learning rate, L_T=O(sqrt(T logT)), so rejection tends to zero at O(sqrt(logN/N)), plus declared finite sampling/generation budgets. Arbitrary noise retains only(1) and may always reject. These are proof bounds, not a claim of favorable finite constants or a large executed quantum experiment.

The payload/native physical-qubit source-exposure ratio at the cap is EXACTLY

 (hB/2)/(4*9N)=1/1152.

This now holds for ONE FIXED four-spin port as block length grows. Expected accepted payload multiplies that ratio by readiness. The total time/classical cost is not constant-rate: exact expert arithmetic and O(B^8 poly(h)) code verification may dominate. Quantum buffering is O(N) bare protected-output wires plus encoded/outer ancillas and references when used. The source must not later revisit these trusted buffers; otherwise the port model changes. A resource-first version additionally pays clean reference storage and teleportation, not a self-bootstrapping local-memory claim.

## 6. Executed evidence and comparison
`construct_inner.py` executes exact GF2 isotropic sampling, exhaustive distance verification, received Clifford compilation and sparse total-decoder tables. The C++ fast verifier has128-bit syndromes; when r>128 the driver uses an explicit arbitrary-integer Python exhaustive fallback rather than truncating. Cases h2,3,4,5 were constructed; h5 is [[80,5,>=5]], checked against130,354,980 low-weight Paulis, with2118 decoder Clifford gates (1699 CX). The seed is reproducibility machinery, not a physical fair-randomness source. `check_phase_decoder.py` checks exact uniform-flag multiplicities at n3,k1 and dense five-qubit phase/QEC/coherent-memory fixtures. `check_concatenated.py` uses the ACTUAL h5 generated inner circuit/table and received GF32 outer binary circuit and syndrome decoder, testing adversarially concentrated and dispersed native Pauli errors at the declared radius. Large dense quantum-state execution is not claimed.

The strongest fixed-four-spin alternative uses the SAME one-logical-qubit singlet code with full-path computational/Hadamard survival testing and bare logical Pauli pads. At n4 the full singlet dimension is2, equal to the code dimension, so there is NO d/K penalty. The same gap-free learner transfers with A0=8, witness coefficient2, the SAME concatenated code and the SAME asymptotic rate/availability orders, without physical permutations. Matching-only tests bypass encoder/decoder endpoints but require their independent calibration; full-path tests include those endpoints and may better detect their faults. Thus fixed-port closure is a successful use of existing coding machinery, not an established advantage over an equally informed conventional full-path alternative.

## Primary prior art and governing sources
- Ouyang, *Concatenated quantum codes can attain the quantum Gilbert–Varshamov bound*, arXiv:1004.1127v6, sectionsII.2–II.3: stabilizer normalizer distance and concatenation of inner stabilizer codes with quantum GRS outer codes. https://arxiv.org/html/1004.1127 . Our conservative reused-inner-code union bound is proved above, not represented as this paper's sharper GV theorem.
- Hamada, *Concatenated Quantum Codes Constructible in Polynomial Time: Efficient Decoding and Error Correction*, arXiv:quant-ph/0610195v4, sectionsIV–V: constructive concatenation, finite-field coordinate interfaces and staged syndrome decoding. https://arxiv.org/html/quant-ph/0610195 . Efficient constructive quantum concatenation predates this work; no coding novelty is claimed.
- Actual Astra dependencies: received algebra compiler; outer_grs_distillation_20261028/GOVERNING_WRAPPER_v1.md and grs_wrapper_v1.py; compiled_payload_outer_bridge_20261029/direct_outer_checks_v1.py and governing integrated theorem; four-spin Bell-label encoder; permutation-orbit CP memory theorem; independently reviewed gap-free learner and three-role readiness theorem.
