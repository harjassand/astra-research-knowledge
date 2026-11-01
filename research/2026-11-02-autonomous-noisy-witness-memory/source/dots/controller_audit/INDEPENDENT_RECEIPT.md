# Independent witness-controller audit — 2026-11-01

## Finding

**Conditional mathematical PASS for the stated ideal graph-local controller's extensive drift, enlarged ground subsystem, and linear protected distance.** No counterexample found to those claims. This is not a lifetime theorem, physical jump-synthesis result, or certification of numerical hardware constants. The parent boundary/coherent-noise consumer is outside this receipt.

Audited author file: `producer-workspace/TANNER_WITNESS_DOWNHILL_CONTROLLER.md`, SHA256 `9f04d241d3dfd5d62fe3457f98c550d5edfc6644e75261aa3435357759f619ef`.

The imports must be narrowed to the sufficiently-large-degree LZ quantum Tanner family, with simultaneous robust primal and dual constituent codes and the required Ramanujan square complex. The advertised radius is explicit **conditional on those family constants**, not a certificate for a supplied finite Tanner instance. Projector support, not merely flipped-witness support, must be used for parent interaction/noise incidence accounting.

## Primary-source and orientation gate

No governing PDFs were actually present alongside the author file, and filename searches under shared/scratch/tmp found none. I read the supplied access-stop ledger first, then opened only the permitted direct arXiv PDFs:

- [LZ, v3](https://arxiv.org/pdf/2208.05537): definitions, §2.7, Theorem 12, proof of Theorem 13, Lemma 18 Claim 1.
- [Gu–Pattison–Tang, v1](https://arxiv.org/pdf/2206.06557): decoder overview; not used as the extensive-move premise.
- [Dinur–Hsieh–Lin–Vidick, v1](https://arxiv.org/pdf/2206.07750): construction overview and robustness theorem location; not substituted for LZ's square-qubit construction.

LZ places X checks at V00,V11, with local check space CA⊗CB; Z checks are at V01,V10 with local check space CA-perp⊗CB-perp. Therefore X-error witnesses belong at V01,V10, with kernel CA⊗F2^B + F2^A⊗CB. Z-error witnesses belong at V00,V11, with both constituent codes dualized. Shared strip labels agree. LZ's active-set threshold is 2^-12 δ² ε³ κ_rob |V00|, and its Claim 1 supplies the needed first-removal covering bound. Large enough fixed Δ and the source's robust-code/expansion hypotheses are essential. D-H-L-V's own code instead has edge qubits; its construction cannot silently replace this square-qubit instance.

No denied source, alternate, mirror, external communication, publication, or hardware action was used. No source-access block remains for this audit. Full independent reproving of the imported expansion theorem was not attempted.

## Independent reconstruction of the static bound

This is not an inference from logarithmic parallel rounds. Let a terminating fast sequence have increments xi and decrement at least (1-ε)|xi|. Write Ri for the number of coordinates removed at step i and Ai for added coordinates. Then Ri≥(1-ε/2)|xi| and Ai≤ε|xi|/2. Summing and using termination gives sum Ai≤ε|Z|/[2(1-ε)].

Let fi count ORIGINAL coordinates first removed at step i. These partition the original support. Ri-fi counts removals of coordinates previously added, including re-added original coordinates. Every such removal can be charged to a previous addition, so sum(Ri-fi)=sum Ai. If fi≤(1-3ε/2)|xi|, then Ri-fi≥ε|xi| and consequently

sum_bad fi ≤ [(1-3ε/2)/ε] sum Ai
           ≤ [(1-3ε/2)/(2(1-ε))]|Z| < |Z|/2.

Thus the good first-removal sets cover more than half the initial support. Each good xi has initial overlap at least fi, hence initial gain > (1-3ε)|xi| > |xi|/2 for ε<1/6. All first-removal sets assigned to the same vertex lie in its Δ²-coordinate view, and are disjoint. Therefore at least |Z|/(2Δ²) distinct vertices initially admit improving moves. Repeated visits to one vertex cannot inflate this count.

The explicit basin's norm argument is sound: starting norm t, robustness bounds accumulated added decomposition norm by |Z|/[κ_rob Δ(1-ε)]; the elementary inequality |Z|≤Δ t gives intermediate norm ≤At, A=1+1/[κ_rob(1-ε)]. Active vertices in any one partition are at most that norm. This proves continued applicability by induction, without assuming a terminating sequence in order to prove its existence.

For a joint Pauli representative of weight r, at most 2r check views in one sector are touched. Virtual repairs introduce at most 2Δ²r witness flips. At most 2(1+2Δ²)r local difference codewords remain; each uses at most 2Δ strips. Thus t≤4Δ(1+2Δ²)r. Substituting |V00|=n/Δ² gives precisely the author's R_n. Take the minimum of the two sector constants and a strict safety factor. All quantities count enlarged-system Pauli weight, while n is original data-qubit count; total register count is 5n, so linearity is preserved.

## Incompatibility and constant check

Writing d=Δ², j repairs alter at most dj mismatch coordinates. Each coordinate lies in four candidate views. Thus at most 4dj candidate vertices change their local mismatch input. Combining |Z'|≥z-dj with the compatible bound gives

N_mismatch ≥ max(0,z/(2d)-(1/2+4d)j).

With M=d+1 and C=1/2+4d,

Mj+z ≤ (M+2dC)[j+max(0,z/(2d)-Cj)],
M+2dC=8d²+2d+1≥2d.

Repair and mismatch events at the same vertex remain distinct event types; each has one selected local update, not one full-rate event per possible codeword. This establishes the claimed K. The accompanying exact-rational script checks 640,000 scalar instances; the displayed algebra is the proof, not the finite test.

## Local operators, coherence, and physical meaning

Compatibility is measurable by the constant-size commuting observables S_h times the corresponding witness-Z parity, for a basis h of the local check space. The block j_v is one minus their simultaneous +1 projector. Mismatch uses only the two witness Z values at each coordinate. Hence all potential terms commute even across CSS sectors. Actual syndrome values lie in the image of H_v, including when redundant check coordinates are retained, so the repair equation is solvable.

A repair changes only its own compatibility block, lowering Mj by M and changing mismatch by at most d. A direct kernel update preserves compatibility. At other-partition vertices, distributing the row/column words preserves each touched kernel and XORs exactly x into mismatch; cancellation of overlapping row/column flips is harmless. No distant syndrome or maintained global decomposition is queried.

Choose deterministic local tie-breaking using compatibility discrepancy for repairs and the local mismatch for reductions. For each pattern, Pi is a projector on these local commuting observables and T is the fixed witness Pauli. On each joint spectral sector,

D[sqrt(kappa) T Pi]^*(exp(aW))
 = kappa Pi [exp(a W_after)-exp(aW)].

All enabled updates are downhill; their summed diagonal eigenvalue therefore obeys the claimed bound. Since this is an operator inequality in a common spectral decomposition, it holds on arbitrary superpositions, including arbitrary gauge coherences. A classical-mixture assumption is unnecessary. Off-basin sectors do not acquire a drift bound from this argument.

**Locality caution:** T flips at most 2d witness qubits, but Pi can involve additional nearby witnesses and physical check supports. The jump J=T Pi must be charged its complete bounded neighborhood. The b≤2d descent-path bound concerns the Pauli correction product, not a claim that the dissipator has only 2d support. There is no measured-history or full-syndrome oracle hidden here, but neither is synthesis by noisy bounded-arity hardware established.

## Ground subsystem and distance

Independently checked, also by the companion algebra audit: fix the order of controlled-X and controlled-Z gates. U is a Clifford on independent five-qubit blocks, with the specified two layers. On copy agreement, conjugation of each original CSS check attaches exactly its relevant witness parity. Thus W=0 equals U(C_original⊗K_aux) as a subspace, not just on classical witness assignments. The two free equality-pair qubits per data site are gauge. Witness Z phase faults commute with U and act only in this gauge; witness flips generally do NOT and remain modeled physical faults.

Define the enlarged gauge group by conjugating the original stabilizer group and the equality-pair gauge groups. A dressed logical Pauli conjugates to an original nontrivial logical times an auxiliary Pauli. A weight-w enlarged Pauli has at most 5w total support after conjugation, so its data component cannot be such a logical unless 5w≥d_original. This proves the stated conservative distance. It does not, by itself, prove that every trajectory of noisy jumps preserves logical information.

The barrier deduction is valid with its explicit conditions: if W<r/b and each step lowers W by at least one, the total correction support is <r; its intermediate radius stays below 2r. If the initial and accumulated correction remain below logical distance, their ground-preserving product is gauge, contradicting minimality of r. Use a reduced-weight radius with 2r inside both the drift basin and distance bound. Defining quantum boundary shells and proving leakage remains the separate consumer's responsibility.

## Acceptance limits

Accepted: conditional ideal-controller construction, local spectral drift, static extensive rate, basin algebra, ground subsystem, conservative protected distance. Not accepted from this receipt: arbitrary-family applicability, a practical Δ, explicit useful threshold/lifetime, fault-tolerant encoding or final decoding, hardware implementation, noisy reset locality, thermal realization, or advantage over a matched active decoder. No novelty claim is assessed.

## Flat-component join clarification (parent follow-up)

The parent clarified that the earlier sources had been read through web tools, not saved beside the file; the missing-file observation is not a source omission by the author. The direct permitted PDF reads above remain the evidence actually inspected in this branch.

For a region whose every joint-syndrome label s admits a chosen Pauli representative E_s of weight at most r_*, compare an edge T:s→t to these representatives. E_t† T E_s preserves the enlarged ground subspace and has weight at most 2r_*+b, where b bounds the update Pauli's support. If this is below protected distance, that product is gauge. Thus the corrected edge has identity protected-logical action; any closed path has only gauge holonomy. The syndrome-only projector convention makes its conditional factor protected-logical trivial as well. This supplies the algebraic flatness join, **conditional on representative existence throughout the admitted component**. Low W on all labels globally is not sufficient; a disconnected high-radius label may have low W. Use a component seeded by correctable states and a cutoff below the barrier shell to justify confinement, with a b-wide boundary margin for one-step jumps.

A useful optional strengthening from the independent algebra check: U has one data qubit per disjoint five-qubit block. A weight-w enlarged Pauli occupies at most w blocks, so its decoded *data* component has weight at most w. Thus the same reasoning yields d_enlarged ≥ d_original, although the stated d_original/5 bound is already valid and needs no strengthening for acceptance.

Companion files: `ALGEBRA_RECEIPT.md`, `check_clifford.py`, `clifford_results.json`. The five-qubit matrix checks are executable local consistency tests, not numerical proofs of an asymptotic family theorem.
