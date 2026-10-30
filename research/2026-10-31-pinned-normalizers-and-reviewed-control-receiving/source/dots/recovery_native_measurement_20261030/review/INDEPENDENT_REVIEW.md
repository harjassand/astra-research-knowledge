# Independent review: destructive CSS measurement
2026-10-30. Reviewed candidate SHA256 `1008c6622d2c5d489b27f913de4dd7ff7a5a47d381dfb93d35da44f7f2e7efd1`; original V1 hash `7222850b9d9f54e270712ff24ab66b4c28199b19bd574c101f4e60568e55051c`.

## Verdict
**Scoped PASS with the binding branch-dependent repair below** for complete terminal reduced whole-bank Z/X or Bell measurement into protected internal classical registers, conditional on the already-reviewed FT/cavity/native radius contracts. Not a noiseless physical detector, arbitrary-accuracy raw-bit ingress, universal native processor, or practical advantage. The supplied same-coefficient KL proof is valid in the restricted local-isometry capture model but must not be extended blindly to a consumed DATA register later reused as interacting bath.

### Checked load-bearing steps
1. Bottom-up tower is a forward construction, not a false time reversal of resets. Exact fixed polynomial-code encoder, constant number of child-level preparation/identity/refresh modules, and final arbitrary-input totalization supply the required coherent good module. Bad towers are arbitrary qudit symbols, not classical flips. Updated field-to-bit sanitizer closes the bad-symbol alphabet gap. Every tower stage is a prefix-free spacetime module, so the joint OR sieve gives a uniform O(x0) bad-record floor. This does not evade the raw-ingress lower bound.
2. Fixed padded GPT scans require only the actual finite orbit-minimizing tables, integer U descent and the separately accepted decoding radius. At most O(N) nonterminal full scans occur. The claim is polynomial circuitry, not a fictitious constant-time RAM decoder. The exact code-zero sector removes an unknown baseline. Half distance alone is NOT a substitute for the GPT radius.
3. Corrected-word projectors intertwine every admitted coordinate-local error with logical outcome projectors. For the local-isometry capture model, KL then supplies the claimed two-sided identity, including phases and reference coherences. A separate Steane test in this directory checked 106 Pauli-basis errors on one doubled DATA/record coordinate, 11,236 ordered cross pairs, and all logical/output indices: largest residual 5.55e-17. This is algebra evidence, not a Tanner gadget or numerical threshold certification.
4. The record and protected-processing predicates are physically disjoint. The exact cardinality and mixed sieve, not probability independence, gives the stated b. Polynomial overhead for exponentially small error is correctly acknowledged.

## Binding repair: rank-one branches, not one outcome-independent auxiliary
Consumed DATA and reversible work contain the outcome even in a perfect implementation. If these systems remain an interacting bath during the polynomial protected computation, it is not justified to keep treating every coefficient as an error supported on a few original DATA coordinates. Thus the candidate's equations (4)-(6), and its outcome-independent Gram coefficient in section 7, are restricted to the local-isometry capture model. The general shared-bath receiving proof should instead use the following stronger and simpler rank-one argument.

The complete logical Z basis and the complete logical Bell basis consist of rank-one projectors. Good histories preserve the corrected outcome for each basis input; the final protected output-dephasing circuit is part of the good computation. In the common logical chart the good map therefore has the form

    G(rho_LB)=sum_z |z><z|_O tensor K_z(<z|rho_LB|z>),

where K_z are signed auxiliary maps and may depend on z. This statement follows from outcome intertwining on ket and bra, plus actual final encoded dephasing. It does not require K_z=K or an outcome-independent bath. The reference is untouched.

Write actual Phi=G+B, ||B||_diamond<=b. Since Phi is TP,

    ||diag_z(K_z*(I)-I_B)||_infinity <= b.

For any positive joint input, the diagonal blocks rho_zz are positive and their traces sum to one. After tracing auxiliary output, the complete trace norm of the good-map trace defect is at most b, uniformly with a reference. The bad contribution costs at most b. Thus the candidate's reduced-instrument bound epsilon_in+2b holds without any equal-coefficient assumption. Rank-one completeness is important; a partial nondestructive observable requires an additional surviving-logical-subspace channel proof.

This correction must govern the text wherever it asserts one common auxiliary coefficient despite retained outcome garbage.

## Optional positive full-auxiliary repair for a subsequent composition proof
This review identifies, but does not certify the complete native teleportation/feedforward receiving theorem. There is a useful channel-level construction:

Define P on channels by measuring the INPUT logical basis virtually, retaining its label z, applying the channel, and projecting its OUTPUT logical classical label onto the same z, retaining all actual auxiliaries. This is a CP superchannel with a trace-nonincreasing postprocessing, hence complete-norm contractive on channel differences. It fixes the branch-diagonal good map G. Therefore Phi_pos=P(Phi) is CP/TNI, ||Phi_pos-G||<=b and ||Phi-Phi_pos||<=2b.

Each branch of Phi_pos is exactly rank-one input measurement followed by a CP/TNI outcome-conditioned auxiliary map. Its missing trace effect is positive. The wrong-output event vanishes on G and has probability at most b on every input basis/bath state, so each branch deficit has operator norm at most b. Replacing that deficit with any fixed auxiliary state produces a CPTP branch completion and costs at most b. Consequently a full-output-and-auxiliary, outcome-conditioned measurement comparator can be within 3b, assuming the declared input/output charts are genuine CP embeddings/compressions and the good branch identity holds with the retained systems.

This is an analytical channel repair, not a physical input measurement, postselection or bath reset. In particular it does NOT imply an outcome-independent environment. A receiver must still check that its subsequent protected feedforward/memory theorem tolerates the resulting outcome-conditioned auxiliary states and preserves reference behavior. No end-to-end teleportation acceptance is issued here.

## Critical additional condition for FULL retained-output claims
The proposed later addendum FULL_OUTCOME_CONDITIONED_INSTRUMENT.md at SHA2080c6618f258dcc794ea8e4fd40ea6bfe2e511db56c93f2aa9aa1b18788903a has a blocker as written: a coherent copy to a RETAINED garbage register is not dephasing of the complete retained output. For example |+> maps to (|00>+|11>)/sqrt(2), not a classical mixture. Tracing that copy establishes the REDUCED claim, but cannot establish the full-output branch-diagonal map (1).

To use the otherwise correct branchwise positive CP/TNI repair of that addendum, install an ACTUAL protected logical erasure/dephasing channel: copy the outcome to an encoded ancilla and apply an actual FT logical reset/replacement to that ancilla, including all finite physical reset errors and work erasures in the full rectangle count. The nominal replacement must act as R tensor Id on the modeled retained bath; its inaccessible Markov reset reservoir is NOT part of that retained bath. The accepted finite CP-divisible replacement primitive can supply precisely such an interface, but it must be stated and instantiated. A unitary dilation retaining every reset reservoir would again retain coherence and requires a coherent measurement-isometry formulation instead.

Subject to this real-erasure condition, common protected input/output module charts, and the deterministic good branch intertwining, equations (3)-(6) of that addendum are correct: each A_z is CP/TNI; the direct-sum diamond norm is at most max_z ||A_z-K_z||; G_pos stays in the protected module; and comparison directly with G+B yields 2b without a number-of-outcomes factor. This reviewer does not accept the full retained-output claim before the actual erasure condition is incorporated.
