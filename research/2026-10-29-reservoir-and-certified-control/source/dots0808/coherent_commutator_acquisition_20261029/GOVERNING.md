# One-call coherent commutator-Gram acquisition
2026-10-29. Construction and boundaries; not a recovery or hardware-advantage claim.

## 1. Acquired object and exact source contract

S is the same D-dimensional system before/after one ordinary opaque source call; M contains all retained source memory. The complete source is a CPTP map with Kraus Kα:S⊗M→S⊗M′. No controlled implementation of Kα, inverse source call, source purification access or bath reconstruction is assumed. On one chosen pair let P_j=σ_a⊗σ_b⊗I_rest, j=(a,b)∈{x,y,z}². They are known Hermitian unitaries.

Prepare fresh control C uniformly in its nine labels, a fresh plus flag F, and fresh S maximally mixed I_D/D independent of current M. A trusted maximally entangled S:R pair realizes this while retaining the reference R outside the source. M may remain entangled with arbitrary earlier reference Q. Both C and F and all trusted references must be isolated from source access throughout the call. The same complete source Kα must act on all control branches: no leaked external label-dependent operation or uncharged control-window disturbance is allowed. The ordinary source may interact arbitrarily with S, infer information from S, and retain memory; that is included in Kα.

Define Δαj=Kα(P_j⊗I_M)−(P_j⊗I_M′)Kα and

H_jk(σ_M)=(1/(2D)) Σα Tr[(I_D⊗σ_M) Δαj† Δαk].

H is Hermitian PSD. If a true twisted swap T*=(I+Σ_j C*_j P_j)/2 commutes with every full-joint Kα, then H vec(C*)=0 for every actual memory state. C* is real and represents a rotation in SO(3), with squared norm3. Conversely, kernel membership for a single encountered σ can reflect unoccupied memory sectors; it does NOT certify a full-joint symmetry or future channel. No occupation-gap premise has been acquired by changing data representation.

## 2. Actual circuit, both outcomes, full memory

Before the source apply P_j only on flag0. After the same ordinary source call apply P_j only on flag1. Read F in its ± basis, retaining C. These are two known branch-controlled Pauli multiplexors, not controlled source calls. Branchα,j has target-memory amplitude

Aαj,±=(Kα P_j ± P_j Kα)/2.

With C uniform, the isometry into C adds factor1/√9. This circuit differs from a direct same-control sandwich: multiplying its minus branch by a j-dependent P_j would change inter-label coherences. Therefore the new acquisition identity is proved here rather than imported from a single-involution checker.

After tracing S and its fresh reference, the complete CP maps from M to C⊗M′ are

J_±(σ)=(1/(36D)) Σ_{α,j,k}|j><k|⊗Tr_S[(KαP_j±P_jKα)(I_D⊗σ)(KαP_k±P_kKα)†].

One explicit Kraus family is

Lαuv,±=(1/(6√D)) Σ_j |j>⊗<u|(KαP_j±P_jKα)|v>,

where u,v range over a system basis. The maps extend by identity to any earlier reference Q. Summing both outcomes gives a trace-preserving instrument because it is obtained from the stated source CPTP map and trusted pre/post unitaries. Neither branch alone is normalized. No independent bath reset or factorization of the output C:M′:Q is assumed.

If both outcomes and C are discarded, the retained memory/reference output is exactly the ordinary source marginal Tr_S N((I_D/D)⊗σ_MQ). This follows because diagonal control branches have P_j(I_D/D)P_j=I_D/D before the call and target-only unitaries vanish under the final system trace. Conditioning on a flag outcome or retaining C does NOT have this unchanged marginal. Thus unconditioned acquisition costs one ordinary mixed-input bath update, rather than a hidden extra source interaction.

Tracing M′ gives exactly

ρ_C,minus = H(σ)^T/18,     p_minus=Tr(H)/18.

The transpose is in the fixed j-label basis: output element jk is Tr[Δ_j(I⊗σ)Δ_k†]/(36D)=H_kj/18. For complex Gram matrices omitting the transpose is wrong. H^T is PSD; the known real C* remains its kernel vector as well. p_minus can vanish, notably for the identity source. The total probability and the plus branch are paid, not discarded from resource counts.

## 3. What coherent data do NOT provide

The normalized minus state is H^T/Tr H and lies in its RANGE, not its kernel. It does not prepare the unknown rotation/encoder. A kernel can have dimension>1, may contain non-SO(3) vectors and can change on unoccupied memory sectors. A normalized real coefficient vector also does not automatically supply a deterministic programmable gate or physical frame.

For an arbitrary pre-existing control density matrix ρ_C independent of current M, the reduced minus map is (1/2)ρ_C∘H^T (entrywise product), not Hρ_CH and not a kernel filter. In particular inserting a coefficient state does not automatically perform a coherent gradient or spectral projection. Postselecting the output control onto its uniform vector after input |c> instead gives probability c†Hc/18; this consumes/projectively disturbs the coefficient register and does not implement a reusable unknown program. The full CP instrument retains its backaction on M.

Successive acquisitions with retained source memory generally yield correlated C registers and history-dependent H(σ_t); they are NOT iid copies of one density operator. Density-matrix exponentiation, quantum PCA or independent-copy kernel-learning interfaces cannot be assumed for free. Under a genuine fixed full-joint commuting-swap promise there is a shared dark vector, but producing it still requires a proved algorithm, resources and SO(3) compatibility. No gap-free purification is supplied.

**Sample versus oracle:** the physical output H^T/18 is a quantum record, not a coherent block-encoding of H with its inverse. Its preparation includes an opaque CPTP source and uncontrolled retained memory. No repeatable purification oracle, inverse source Stinespring U†, controlled unknown evolution, amplitude amplification, QSVT or gap-free density-matrix purification follows from this acquisition. Any such downstream interface must be built and paid separately.

For a real candidate rotation C with ||vec C||²=3, projecting the uniform-input minus record onto |vec C/√3> has *joint* probability vec(C)^T H vec(C)/54. If δ(C)=(1/(2D))ΣαTr[(I⊗σ)[Kα,T(C)]†[Kα,T(C)] for T(C)=(I+ΣC_jP_j)/2, then vec(C)^T H vec(C)=4δ(C), so the record test probability is2δ(C)/27. A direct known-T(C) coherent commutator flag test on mixed data has minus probabilityδ(C)/2. Thus this record query has only4/27 of that one-query sensitivity, not an automatic one-call advantage. Its potential value would be retaining a quantum record for a later choice of query, under a proved control/receiver contract. Normalizing by p_minus without paying the waiting/correlation cost would be misleading.

An elementary limitation is the identity source: H=0 gives no minus states, though every frame is valid. Near identity, quantum Gram acquisition can be arbitrarily rare. Distinguishing a nearly degenerate common kernel from another orientation retains information/spectral-resolution issues. Retaining quantum coherences may enable a different downstream algorithm, but no advantage over equally informed adaptive classical measurements has been established. The local object is only9-dimensional, so avoiding classical output alone is not an asymptotic speedup argument.

## 4. Controls and paid resources

Abstract cost per attempt: one ordinary source call, one fresh nine-level coherent control, one fresh flag, known pre/post multiplexed Paulis, flag readout, and fresh I_D/D data (or maximally entangled data-reference preparation). Source-memory dimensions do not enter the controller circuit. The control is two qutrit labels: each pre/post multiplexor decomposes into one Pauli selection on each of the two target spins. No global source inverse, channel tomography or bath readout is needed.

A conservative qubit compilation uses two2-qubit qutrit encodings00,01,10, one flag and one reusable clean work qubit. For each of two targets, three Pauli values and two windows there is one addressed three-control Pauli:12 total. Compute AND of two controls into work, Toffoli from work and third control to target, uncompute; basis-conjugate target for Y or Z. This uses36 exact Toffolis, hence216 CNOT and324 one-qubit gates using the earlier reviewed6-CNOT/9-single Toffoli. Open controls require44 extra X gates across this particular label encoding; target Y/Z conjugations add16 singles. The control uniform states each use one Ry and one negative-controlled Ry:4 CNOT+10 singles together. Flag preparation/readout adds2 H. For a pair-only D4 source, two data-reference Bell pairs add2 CNOT+2 H. Total sufficient budget:222 CNOT+398 single-qubit gates per attempt, plus state preparation/reset, readout, routing/idle and noise costs. These counts are a compositional upper bound from known primitive circuits, not an optimized native-device implementation or a claim this entire qubit-level compilation was simulated here. The dense acquisition simulation executes the specified9-level controls directly.

Pair-only peak with Bell references is10 qubits (data2, reference2, label4, flag1, work1); a four-spin source with full mixed input needs four data plus four reference qubits, hence14. Classical mixed-state preparation can trade reference qubits/Bell gates for fresh trusted random bits and discarded preparation records; correlations with old source memory cannot be silently introduced. Finite precision, terminal operations and isolation require their own noise budgets. N1041 collective-dephasing protection of a dual-rail FLAG does not protect these nine coherent LABELS or arbitrary target-control errors.

## 5. Executed checks

`check_instrument.py` constructs actual full control/flag/source pre/post matrices and evaluates both outcomes while retaining an entangled memory/reference state. It independently constructs the explicit CP Kraus formula and compares complete C:M′:Q outputs, not just flag probabilities.

Fixtures: a random three-Kraus nonunital joint channel; a two-Kraus genuinely nonunital twisted-collective channel built from collective damping and noncommuting memory couplings; identity. Full-output differences are below1.1e−16, H-transpose identity below4.9e−17. The twisted-SO(3) kernel residual is2.2e−16. Wrongly dropping transpose causes differences0.02–0.04. Nonzero retained control-memory correlations are directly observed. Identity produces exactly zero minus probability. `check_obstructions.py` additionally shows that a true kernel coefficient input still has minus probability0.2373, while postselecting its control onto uniform makes the joint probability vanish; hence the unmodified control channel is not a spectral filter. Dephasing the flag gives false minus probability1/2 even for the identity source, and label dephasing destroys the twisted kernel. These are numerical consistency checks of exact identities, not interval certificates, hardware data or statistical acquisition guarantees.

## 6. Governing Astra source and freshness

Astra plugin search was attempted first and failed with `published_refresh_failed`: runtime/version mismatch, prior snapshot not certified current. GitHub fallback fetched N1041 packet at pinned revision3882c05cc803ff107b4d89f4010090ed41c3a392 and the complete governing source `research/2026-10-23-fresh-programme/intake/capital-integrated-2026-10-23/updates/2026-10-26-coherent-check-flag/source/p1/originals/DECOHERENCE_FREE_COHERENT_CHECK_FLAG.md`. Its intact SHA256 is c5dca84b0bd857dfee66c09f1f32124126b8090269f10db4839641127c177e24; copied as received_N1041_proof.md. The pinned source was read completely, not assumed current or compatible from its title.

The reused premise is known-control bracketing around one complete opaque source including all memory. N1041's source-specific teleportation/forbidden effects, dual-rail collective-noise protection, numerical assertions and physical capabilities are NOT transferred. Its correction scope expressly requires isolated fresh coherence, a full joint error budget rather than per-Kraus substitution, and paid control/readout operations. This construction has its own full-instrument proof above. No historical priority claim for coherent commutator interferometry, Gram-state preparation or quantum learning is made.
