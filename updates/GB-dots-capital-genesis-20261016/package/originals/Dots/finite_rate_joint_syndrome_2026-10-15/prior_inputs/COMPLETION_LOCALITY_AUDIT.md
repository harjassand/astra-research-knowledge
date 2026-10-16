# Independent audit: global-character completion-time locality

Date: 2026-10-15.

## Verdict

PASS under the strong clean-reservation, bath-independent-correction, conjugation/deletion-stable whole-dilation, and no-local-logical hypotheses in the revised SUBSET_MOMENT_AND_LOCALITY_PROOF.md. Together with SUBSET_CHARACTER_AUDIT.md, this closes the two quantum interfaces required by the separate subset-moment contour argument. It does not establish general controller robustness, a chronological small-error instrument, or fault tolerance of arbitrary continuous interactions.

The audit checked the revised treatment of unfinished frame wrappers and endogenous measurement records. A separate exact test, check_memory_only_reorder.py, verifies the central algebra with crossing noncommuting shared-bath pulses and intervening completed-correction projectors.

## 1. Physical wrappers and deletion stability

The valid physical order for a selected pulse is: complete its exact correction circuit, insert its ideal stabilizer frame, run its finite local pulse, and remove the frame. The whole memory/private-ancilla/frame support is reserved for the fixed interval. During a clean interval every other memory operation is disjoint from this entire reserved support, not just from the center vertex or the smaller error patch.

Consequently the held frame commutes with all intervening remote memory operations and with bath-only operations. Moving the frame algebraically through the physical sequence conjugates only its own error Hamiltonian, leaving remote terms unchanged. For an ideal frame g, the resulting pulse terms are g V_i g†, and the start/end wrappers cancel. Setting this pulse coupling to zero therefore removes all dependence on g from the complete dilated circuit.

This reasoning does not require generic correction gates to be stabilizer covariant: the correction finishes before its own frame is inserted. It does require actual ideal frame insertion/removal and excludes an uncharged frame-dependent control or ancilla leak. If wrappers have finite implementation dynamics, those dynamics must themselves be qualified; they cannot silently be omitted from the model.

The relocation of a clean correction to its stipulated start uses the prior finite-duration interface's stronger assumptions: each correction gate is identity on the shared bath, private working ancillas are not accessed by remote operations, and intervening operations have disjoint reserved memory/ancilla supports. Therefore those gates commute with remote bath-coupled pulses as joint operators. Composite isolated-channel bath independence alone would not suffice. No bath-coupled error pulse is serialized or moved as a channel.

## 2. Pending frames and legitimate conditioning

The revised note correctly transforms only geometrically clean pulses that have fully completed, including frame removal, by the fixed deterministic horizon. A pending wrapper has no matching undo yet and can retain direct frame dependence. Its actual prefix is charged as bad; it is not given an artificial small-action completion label.

Other frame seeds and exogenous primitive schedule/noise variables may be fixed as unselected parameters, with bounds proved uniformly and then averaged. Conditional on these parameters, a pending-frame-dependent unitary is simply part of the unselected background as far as a selected clean frame is concerned. Clean disjointness still prevents hidden dependence on selected frames.

Endogenous measurement/dilation outcomes are different. They remain in the one common dilation and are summed at the CP-effect level; they must not be normalized and conditioned upon in the moment proof. The source now says this explicitly. Resolving an individual outcome gives an unnormalized subeffect, not a new uniform conditional probability theorem.

## 3. Memory-only reordering is exact

Expand each clean pulse interaction into patch Paulis with bath/auxiliary operator coefficients. In a chronological Dyson monomial, a factor belonging to pulse i is

chi_P(g_i) P_Ai tensor B_P(t).

The full monomial is a tensor product of its ordered memory-factor product and its ordered auxiliary-factor product. Move only the memory factors from pulse i to that pulse's completion. Every memory operation crossed during the move is disjoint by the clean-reservation hypothesis, so the commutations are exact. Preserve the chronological order among factors of the same pulse.

The bath/auxiliary factors stay in their original chronological order. In particular one must not regroup all coefficients of pulse i together or move the joint tensor factors as units. Shared-bath commutators are fully retained. Intervening correction projectors also commute when their full physical supports are disjoint; mere vertex separation would be insufficient.

The resulting net memory Pauli E_i is supported in the original error patch A_i. Its frame character is the product of the characters of its constituent factors, which is exactly the character of E_i. Hence taking the global Fourier coefficient chi_i selects precisely the net-pulse condition character(E_i)=chi_i.

For finite-dimensional integrable Hamiltonians the Dyson expansion converges absolutely in operator norm. The local Pauli expansion has finitely many coefficients per interaction, and the finite-horizon finite-event construction permits the indicated regrouping and passage to the limit. This is an algebraic support-history rearrangement, not a causal simulation or independent-pulse channel factorization.

## 4. Quotienting by patch stabilizers

If two patch Paulis have the same detected character, their product centralizes the full stabilizer group. Detection completeness and absence of a logical Pauli on A_i make their product a code stabilizer supported in A_i, up to phase. Fix one patch representative P_(i,chi) for each nonempty character and P_(i,0)=I.

At the relocated completion point in any expanded history, the preceding memory operator is a Pauli orbit E V_code, possibly annihilated earlier by an incompatible correction projector. For every surviving history, a patch stabilizer M_i acts as a scalar sign on that full logical orbit. Thus E_i=P_(i,chi_i) M_i can be replaced by P_(i,chi_i), with the sign absorbed into the auxiliary coefficient.

This replacement is on each history term, not an assertion that the whole state has a single syndrome or that a general zero-character channel is bath-only. Different monomials may have different intermediate histories and bath coefficients. They nevertheless all lie in the same allowed support family specified by the primitive schedule and final global characters.

Therefore clean nonzero characters add one allowed patch Pauli at completion; zero characters add no support. Arbitrary bad operations retain their charged support and physical ordering. Pending prefixes are never completed fictitiously. The rest of the evolution must itself admit the stated local-operation/support representation; the arbitrary H_0 allowed by the norm lemma alone does not establish this locality assumption.

## 5. Dilation records and global good maps

Genuine record-dependent pulse operators are allowed only through one common controlled dilation satisfying the same conjugation, support, norm, and deletion hypotheses. A physical record may influence later allowed couplings; a final mathematical Fourier label is not an available control signal. Keeping the auxiliary coefficients in chronological order preserves all allowed causal record dependencies.

For the selected completed frames, the Fourier transformation is a unitary change of Kraus representation of their independent private-frame average. Resolving frame-independent physical output records and discarding ancillas preserves completeness. A final global Fourier tuple is therefore a legitimate CP-instrument index even when it has no online local realization.

A fixed input-independent good predicate on schedule and global characters can select a CP trace-nonincreasing subchannel. If the deterministic certificate corrects every supported Pauli history, the same decoder acts as scalar logical identity on every term. Their coherent sum therefore has Kraus form I_logical tensor B, with all bath interference retained. The established TNI completion then applies once the separate probability module bounds the bad effect uniformly on joint inputs.

No iid domination, chronological small conditional mark bound, or online character readout is used. The crossing echo obstruction is consistent with this result: its intermediate conditional branch can involve both open patches, while the global termwise history assigns each net memory factor to its own completion.

## 6. Exact check

check_memory_only_reorder.py uses two stabilized memory qubits and one shared bath qubit. Four interleaved rotations use memory X/Y factors and noncommuting bath X/Y/Z factors. A completed reset correction on C occurs after A begins, and another reset on A occurs after A completes but before C completes.

The script checks exact equality between:

- the full Fourier coefficient of the chronological physical products; and
- the sum of monomials with memory factors grouped at their completions while bath factors remain B_3 B_2 B_1 B_0.

All 16 correction/character records agree exactly. All 64 initial-full-syndrome/record cases follow the predicted correction/representative-Pauli output orbit. The script passes using rational SymPy arithmetic. This supplements, rather than replaces, the general argument.

## Final scope

The quantum gates are closed for this explicitly restricted reserved-patch model. The separate classical subset-to-contour result, fixed-duration geometry, pending-boundary accounting, and common-decoder hypotheses are still required for a memory theorem. General faulty controllers, overlapping memory supports within a nominally clean pulse, exposed frame labels, noisy wrappers, unrestricted measurement feedback, and arbitrary continuous memory interactions are not covered.
