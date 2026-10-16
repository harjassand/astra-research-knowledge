# Conditional gate-level interface and a calibration obstruction

2026-10-15. Separate bounded extension candidate; not an amendment to the completed weak-pulse theorem. No general noisy-controller or hardware claim.

## Results

1. Full-Pauli gate characters can qualify bounded correction gadgets under an additional **actual conjugation-covariance** premise. Additive frame dependence and deletion stability alone do not imply that the zero character is correct.
2. If the qualified elementary gates of gadget b have integrated actions a_e, the joint subset strength for faulty gadgets is p_b = sum_{e in b} a_e^2. No independence of actual gadget faults is asserted.
3. Ordinary fine stabilizer measurement, classical lookup and Pauli feedforward implement a different full-input channel from the completed coarse correction. Their per-Pauli-orbit transitions agree, so the universal support/common-decoder proof transfers under the stated support and record assumptions.
4. A multiplicative calibration error in a conjugated Clifford drive can be entirely in the zero Fourier character. An exact rational example below excludes a generic claim that independent Pauli frames qualify coherent gate errors.

## A. Precise sufficient gate interface

Fix an exogenous primitive schedule and its geometrically clean completed gadgets. A gadget has at most a constant m qualified quantum gate slots and bounded full reserved support, including ancillas and frame operations. Slots within one gadget are sequential. During a clean slot no other operation acts on its memory/ancilla support, except its specified intended gate and noise. Overlapping clean gadgets have disjoint reserved memory supports; their bath may be shared. Nonclean and pending gadgets remain arbitrary local gadgets charged by the existing conflict/pending certificate.

Each selected gate e has a private independent uniform full Pauli frame T_e on its ENTIRE data-plus-ancilla gate support. Ignore Pauli phases. In a common interaction-picture dilation its error Hamiltonian is genuinely

    V_{e,T}(t) = T_e^dagger V_e(t) T_e,

where V_e has arbitrary bath coefficients, is supported on that gate's memory support, and is independent of T_e. This formula is meant in the correctly compiled gate interaction coordinates, not asserted for arbitrary laboratory drive errors. The intended final gate C_e is Clifford. All remaining terms in the common dilation are independent of the selected frame seeds. They include arbitrary bath dynamics and operations on disjoint memory supports. The entire frame/compiler/reset/measurement/control implementation must admit the additive, deletion-stable common-dilation hypothesis of the subset-character lemma. Deleting a selected interaction cannot leave its seed in another Hamiltonian term, record-dependent control, initialization, schedule or readout. Endogenous outcomes stay inside this dilation, and their effects are summed, never conditioned and normalized for the moment proof.

Let a_e = integral sup_T ||V_{e,T}(t)|| dt. A bath-only part can instead be assigned to the frame-independent background. For mathematical simplicity take finite-dimensional bath or the bounded-interaction version of the established Duhamel lemma. Only completed frames that have actually been undone at the observation horizon are selected; pending frame prefixes are charged, not quietly dropped.

A sufficient atomic illustration of the compiler convention is: apply input T, implement the SAME core C with fixed error C W, then apply output C T^dagger C^dagger. The ideal net is C, and the actual net is C T^dagger W T. The output correction is a Pauli because C is Clifford. This illustration requires exact/qualified wrappers and frame-independent core error W. Unlike covariant recompilation of the drive, it holds the actual noisy physical core fixed for all seeds.

There is a concrete finite-duration realization of the same sufficient premise. Let the fixed ideal local gate path be C_e(t), with endpoint Clifford C_e; its Hamiltonian acts on the gate memory support and is bath-independent. Let the actual fixed core add local memory-bath V_e^lab(t), independent of its private frame. Apply T_e before this core and C_e T_e^dagger C_e^dagger afterward. Inside the slot use the local moving frame D_e(t)=C_e(t)T_e. The ideal drive cancels against the moving-frame derivative, and the error becomes

    T_e^dagger [C_e(t)^dagger V_e^lab(t) C_e(t)] T_e.

The bracket is seed-independent, has the same operator norm, and stays on the same memory support. Arbitrary shared-bath-only terms are unchanged. Disjoint-memory remote operations commute with D_e(t); for disjoint simultaneous clean cores the moving frames commute on memory even if their errors share a bath. The endpoint wrapper restores the ideal C_e, and the remaining error Pauli is transported by that Clifford. At the finitely many gate boundaries use the exact intended circuit transitions. This gives the required local interaction coordinates and conjugation covariance without splitting the full shared-bath propagator into per-gate channels or reordering bath factors.

Thus multiplicative calibration error of the FIXED physical core can qualify under this convention. The counterexample below applies to the different compiler that changes the physical noisy drive with the frame. The fixed-core construction still assumes exact/qualified wrappers and fixed, seed-independent core noise/control; hidden dependence through timing, a controller, other pulses or a leaked frame fails the premise. A physical implementation must also verify the common-dilation additive/deletion condition across the entire circuit, rather than infer it from isolated-gate process tomography.

For genuine record-dependent feedforward, use a fixed padded list of gate slots per gadget, with each classical branch selecting a core Clifford (possibly identity) in that slot. Its fresh frame is independent of every past record, and the action/support bound is uniform over branches. Keep the record as an explicit register of the common dilation. The controlled ideal path and its controlled output wrapper cancel branchwise; the residual interaction is still conjugation by the same fresh Pauli on the quantum gate support, with record-controlled coefficients. Ideal classical records must remain stable and be accessed only by the specified exact controller. They are protected classical registers, NOT arbitrary mutable subsystems of the persistent bath: neither error terms nor bath-only dynamics may flip or coherently mix their values. Record-controlled coefficients are block-diagonal in the genuine record basis. Only the specified ideal recording/lookup operations may write these registers. Otherwise an identity-on-data error could corrupt a stored syndrome, select wrong feedforward and defeat zero-character correctness. This is not obtained by fixing or postselecting record values in the probability argument. If variable branch timing, support, missing slots, or a controller's access to old frame seeds prevents a single padded deletion-stable dilation, this interface has not been established.

## B. Character locality and zero-character correctness

Expand each local interaction into memory Paulis tensored with bath operators. Every Dyson monomial from gate e acquires the conjugation character of the ordered product P_e of its memory Pauli factors. Full-Pauli conjugation has one distinct character per memory Pauli, and its trivial character contains only scalar multiples of identity on the entire gate support. Therefore Fourier character chi_e fixes P_e, including P_e = I for chi_e = 0. Transport from the gate interaction picture to the physical endpoint conjugates P_e by C_e and is still a Pauli.

This is a termwise statement about the full joint Kraus expansion. Move only the gate's memory Pauli factors to the gate endpoint across disjoint-memory operations; retain every bath coefficient in its original chronological order. Sequential later gates in the same gadget are not crossed by this move. Shared-bath noncommutativity therefore causes no invalid reordering. Summing terms with the same global characters and genuine physical records need not produce independent gate channels.

If every selected gate in a clean gadget has zero character, its memory factors are exactly the intended quantum gates. Any ideal measurement branch still supplies its intended measurement Kraus factor; bath coefficients may depend on the genuine syndrome record. This gives ideal per-branch memory action with bath filtering, not a normalized good CPTP channel or a common bath-channel tensor factor on arbitrary inputs.

If any selected gate has nonzero character, charge the WHOLE bounded gadget, including its ancilla interactions, possible wrong outcome/feedforward, and possible missing ideal correction. Do not replace this by a single post-correction fault without an additional propagation/interface proof. The existing arbitrary-local-bad-gadget support certificate must cover these histories at their actual intervals.

## C. Exact gadget subset bound

The global subset-character lemma supplies, for every set S of selected elementary gates and every joint input/reference,

    sum_{chi: chi_e != 0 for all e in S} K_chi^dagger K_chi
        <= (product_{e in S} a_e^2) I.

Physical dilation outcomes are included and summed. Characters are global Kraus labels; they are not generally causal records or available controller signals.

Let B_b be the event that gadget b has at least one nonzero gate character. For distinct clean gadgets b in J, use a union bound over choosing one bad gate e_b from each gadget. The gate assignments are disjoint. Hence, also as an operator-effect bound,

    effect(intersection_{b in J} B_b)
       <= product_{b in J} (sum_{e in b} a_e^2) I.

Thus p_b = sum_e a_e^2, or p <= m a^2 for a common action a. This is the same joint-subset interface used by the finite-pulse contour argument, not sequential Bernoulli domination. Combine only with a classical contour/support theorem that accepts these subset moments, the full gadget support and timing, and conflict/pending flags. A conditional bound after observing another global character is neither needed nor claimed.

On a fixed input-independent set of support-certified good records, the universal decoder yields Kraus I_logical tensor B_record. The aggregate good map is trace-nonincreasing. A uniform bad effect <= epsilon I allows the established bath-only CP completion and logical diamond bound <= 2 epsilon. Normalizing individual good record maps would invalidate this step.

## D. Refined syndrome instruments

Let the original completed correction have Kraus Q_j Pi_j, including the inactive branch, with Pi_j functions of commuting code stabilizers. Choose a bounded local full syndrome family R_s satisfying sum_s R_s = I and Pi_j = sum_{s:j(s)=j} R_s. The implementable refined target has Kraus Q_{j(s)} R_s. In general it is NOT the original full-input channel: fine measurement dephases coherences within a coarse Pi_j branch.

For every encoded Pauli orbit E V_code, exactly one R_s is identity on that orbit and all others annihilate it. The surviving branch applies the same Q_j E as the coarse instrument. In an arbitrary coherent Pauli expansion of a bad gadget, apply this fact term by term in each physical record. Refinement only selects the surviving terms of that record; it creates no new transition or memory support. Completeness is recovered by summing all records. Thus any certificate with one common decoder for EVERY admitted Pauli term transfers to this refined instrument. No assumption that actual bad errors are incoherent Pauli mixtures is needed.

This independently confirms the refinement candidate at ../refinement/SYNDROME_REFINEMENT_TRANSFER_CANDIDATE.md. Its separate audit at ../refinement/SYNDROME_REFINEMENT_TRANSFER_AUDIT.md checks the concrete sweep refinement and support. The refinement argument itself does not qualify noisy extraction. Its complete support, duration, ancilla use and record handling must be counted anew.

## E. Exact counterexample: the drive error follows the compiler

Let C = (I - i X)/sqrt(2), the intended Clifford Rx(pi/2), and E = (99 I - 20 i X)/101. For frame g in {I,X,Y,Z}, compile ideal core g C g^dagger and actual core g C E g^dagger. Surround the core by input g and output g^dagger. Every ideal logical circuit is C; every actual logical circuit is C E. This describes a relative drive overrotation whose axis/sign follows the compiled ideal drive.

Consequently K_0 = C E and every nontrivial Fourier coefficient vanishes. The zero-character branch is not the ideal gate. Exactly ||E-I||^2 = 4/101, while ideal and actual outputs on |0> have trace-norm distance 40/101. A continuous model with an arbitrarily small frame-independent logical X error satisfies additive/deletion stability but has the same failure. The subset moment theorem remains true, even trivially, because all nonzero-character probabilities are zero; the missing premise is character-local correctness.

The exact checker ../checks/core/check_gate_obstructions.py verifies the four frame identities, all Fourier coefficients, norm identity, output distance, and the separate coarse-versus-fine measurement counterexample. It also verifies the positive fixed-core compiler on the SAME C E: K_0=(99/101)C, K_X= -i(20/101)C X, other characters zero, and bad effect (400/10201)I. It executes only local self-authored algebra.

## F. Resources still assumed ideal or separately qualified

- Initial ancilla preparation/reset. A preparation can be modeled as ideal preparation followed by a separately qualified weak interaction only if such a physical premise is supplied. This does not establish a noisy reset theorem.
- Final projective measurement and transmission/storage of its classical outcome. Circuit gate qualification alone does not qualify detector confusion, lost bits or corrupted measurement records.
- Classical syndrome lookup and branch selection. Lookup can be nonlinear and its reversible dilation may contain non-Clifford gates. Treating it as an exact frame-independent classical resource is explicit here; the Clifford argument does not qualify it.
- Quantum Pauli feedforward pulses can be gate slots under the same strong premises. Selecting the wrong pulse because of a controller fault is a distinct fault model.
- Frame wrappers and their timing. They must be exact resources or separately certified. Recursive appeals to randomizing every wrapper do not close an implementation proof.
- Ancilla frames. Twirling data alone leaves zero-character ancilla errors that can corrupt syndrome extraction.
- Frame/record privacy and compiler covariance. A simple sufficient convention removes frames before exact measurement. Compiling frames through measurement requires correct unmasking before lookup and a common dilation with no forbidden seed leakage. Mere equality of reduced ideal memory channels is insufficient.

These are substantial remaining physical primitive tests. The note supplies a sufficient mathematical interface and an exact obstruction, not a generic qualification of noisy correction circuits.

## G. Provenance

The mechanisms are applications of established Pauli randomization, randomized compiling and syndrome projection. Relevant primary sources include Wallman and Emerson, arXiv:1512.01098; Winick et al., arXiv:2212.07500 (persistent environments and frame leakage); Beale and Wallman, arXiv:2304.06599 (randomized compiling for subsystem measurements) and arXiv:2306.13752 (logical randomized compiling). The measurement-paper abstract establishes relevant scope, but its detailed hypotheses have not been matched to this note's common-dilation/covariance requirements. No claim that its theorem automatically supplies the missing measurement/controller interface is made. Novelty of the composed interface is unassessed.

Primary links: https://arxiv.org/abs/1512.01098 ; https://arxiv.org/html/2212.07500 ; https://arxiv.org/abs/2304.06599 ; https://arxiv.org/abs/2306.13752 .

## Independent review

The separate audit GATE_INTERFACE_AUDIT.md passes this interface after the protected-record and padded-slot clarifications. Its independently authored ../checks/core/check_fixed_core_independent.py verifies a two-error-segment fixed-core compiler. The whole-gadget skipped-correction/support classical module remains a separate input, not a result of this quantum gate note.
