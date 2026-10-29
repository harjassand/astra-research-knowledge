# Acquired: a uniform check-soundness bridge for recursive passive-memory codes

The constructed operation is an explicit local binary retraction for the RX/RZ replacements of **Balasubramanian–Davydova–Lin, arXiv:2605.10943v1**. Two disjoint layer projections halve one CSS sector's stabilizer weight; the transposed repetition inclusion is nonexpanding in the other sector. A local face/path homotopy pays every correction and lifted-generator cost. Alternating the steps gives a uniform polynomial check-soundness bound at every replacement depth.

The governing all-level argument is [RETRACTION_PROOF.md](RETRACTION_PROOF.md). With its explicit constant A, paired-step bound

`g_k(M) <= A(1+A)M + A^2 g_(k-1)(floor(M/2))`

is dominated by `K M^p`, where `p=ceil(log2(2A^2))` and `K=max(seed_check_bound,2A(1+A))`. The full Pauli stabilizer uses `2K M^p`. Constants depend on the fixed replacement parameter and source degree bounds, not system size or recursion depth.

Using the **existing Yin–Lucas stability theorem**, this pays a zero-temperature ground-band stability consequence for the source's bounded-density finite-range R3 embedding. Graph shells can conservatively be bounded by O(r^3), using dimension parameter 4 in its lemma. The consequence is a size-independent sufficiently-small perturbation threshold in that theorem's weighted local norm, a constant ground-band gap and exponentially-in-distance small doublet splitting. The primary's unperturbed thermal-storage theorem is an independent import; no perturbed-bath lifetime follows from the new bridge.

The exact finite construction uses a planar [[5,1,2]] seed, yielding 5 -> 60 -> 1336 qubits at ell=3, one logical qubit throughout. `check_retraction.py` verifies the complete cochain/retraction/homotopy matrix identities, both disjoint projections and the cost orientation on all vectors of the two replacements; 0.1683 s reported after imports. An ell=5 one-step subdivision control verifies the multi-edge rays/face telescope; 0.00445 s. These are algebraic consumers. They do not acquire the primary's random spatial embedding, nor replace its much larger fixed ell by 3 or 5.

The same-input ordinary method is exact GF(2) stabilizer elimination plus established stability theorems. Ordinary elimination already classifies/fills finite stabilizers in polynomial time. The added result is the explicit size-independent support-count bound needed for the stability application, not a demonstrated finite computational speedup or a new general gap theorem. Historical priority of this particular composition has not been established by the bounded primary screen.

Unacquired: useful numerical perturbation threshold, finite-temperature lifetime with coherent Hamiltonian errors and an actual bath, native bounded multi-spin interactions, efficient initialization/readout, practical code size/packing and hardware advantage. The primary's illustrative random-embedding constants are enormous (section 3.4 reports lambda about 5.4e24 and ell=(2alpha+1)lambda with alpha=1000). This is a foundational mathematical bridge, not a manufactured passive memory or a civilization-level success claim.

No external scientific repositories, protected chats or shared intake were modified. No physical operation, paid compute, agent spawn, formal goal, automation, purchase or outreach occurred. Initial choice was protected from the other sol24 proposals; inherited context means it was not a blind comparison.
