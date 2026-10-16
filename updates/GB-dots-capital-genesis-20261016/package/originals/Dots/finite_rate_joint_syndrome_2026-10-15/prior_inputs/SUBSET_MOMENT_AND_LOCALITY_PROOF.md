# Global subset-character moments and completion-time support locality

Date: 2026-10-15. Status: independent derivation of the global-character construction. This note proves the quantum moment and support interfaces under explicit hypotheses. It does not assert a chronological character instrument or a conditional small-error bound, which the crossing echo disproves. The classical use of joint-subset moments is a separate module.

## 1. Full-joint subset moment lemma

Fix a finite horizon, a realized exogenous schedule, and a finite-dimensional closed-system dilation. All frames are independent uniform variables g_i in finite groups G_i, independent of the initial input. On the full memory/bath/dilation Hilbert space suppose

    H_g(t)=H_0(t)+sum_i V_{i,g_i}(t),

with self-adjoint integrable terms. The only dependence on g_i is its displayed term. Put

    a_i=integral sup_{g_i} ||V_{i,g_i}(t)|| dt.

Let U_g(T,0) be the full propagator. Frame-independent prescribed unitary interventions may be included through a piecewise propagator; their operator norm is one. Instruments, reset, and genuine record-dependent control require a fixed frame-independent dilation with independent initial ancillas. The hypothesis must remain true after any selected terms are set to zero. In particular no control, initial state, schedule, final projection, or hidden frame readout may retain additional dependence on a deleted frame.

For finite abelian G_i define full-horizon Fourier Kraus operators

    K_chi=E_g conjugate(chi(g)) U_g.

For every subset S of pulse indices,

    sum_{chi: chi_i != 0 for every i in S} K_chi^dagger K_chi
       <= product_{i in S} a_i^2 I.                       (1)

This is a full joint-operator inequality, uniform in reference systems, initial bath state, and initial memory-bath correlations. Shared-bath commutators and overlapping intervals are allowed.

### Proof without factorial loss

In the Hilbert-space-valued L2 space of frame tuples, let E_i average g_i and Q_i=I-E_i. They are commuting orthogonal projections. For selected indices introduce independent real interpolation parameters z_i in [0,1]: replace V_{i,g_i} by z_i V_{i,g_i}. For every real z the propagator U_z remains unitary.

Multivariate fundamental calculus expands U_1 into the integral of its full mixed derivative plus boundary terms each having some selected z_i=0. Such a boundary term is independent of g_i and is killed by Q_i. Thus, with Q_S=product_i Q_i,

    Q_S U_1=Q_S integral_[0,1]^S partial_S U_z dz.          (2)

For m=|S|, the mixed Duhamel derivative is a sum over the m! possible chronological orders of one insertion of each selected V_i. In a fixed ordering the integrand is a product of m selected V_i factors separated by unitary full propagators at that same z. Its norm is bounded by the product of the insertion norms. The ordering domains are disjoint simplices whose union is the product of the m insertion-time intervals, up to measure-zero ties. Consequently

    ||partial_S U_z||
       <= integral_product_times product_i ||V_{i,g_i}(t_i)|| dt_i
       <= product_i a_i.                                 (3)

There is no m! loss: it would arise only from bounding every simplex separately by the whole time cube. Integrable finite-dimensional Hamiltonians justify the derivatives by Duhamel/Dyson convergence; bounded step approximations and dominated convergence give the same result if desired.

For every vector psi, including an untouched reference, use Minkowski's inequality and orthogonal projection contraction in (2):

    ||Q_S U_g psi||_L2(g)
       <= integral_[0,1]^S ||partial_S U_z(g) psi||_L2(g) dz
       <= product_i a_i ||psi||.

Parseval identifies the squared left side with the expectation of the left-hand effect in (1). Since the bound holds for every psi, (1) follows. The projection formulation requires only independent finite frame variables; characters additionally use the abelian group structure.

Summing any frame-independent dilation-output Kraus indices preserves (1). Thus tracing unused ancillas, or resolving genuine physical records in a frame-independent basis, leaves a complete global character/record Kraus instrument with the same effect bound. Frame-dependent physical feedback must be part of the dilation and preserve deletion stability; it cannot be justified merely by saying the Hamiltonian was additive before feedback.

## 2. Extra locality hypotheses for a memory application

Equation (1) alone gives no local support statement. For each geometrically clean completed pulse i impose:

1. The entire correction/error/randomizer/private-ancilla reservation interval and support are fixed by the primitive schedule. During its error interval, every other memory operation has disjoint support from its reserved memory patch; sharing the persistent bath is allowed.
2. Its actual completed correction occurs before its error pulse. If a finite correction circuit is moved to the original start, its gatewise bath independence and legal adjacent commutations are independently justified exactly as in COMPOSED_POST_ERROR_INTERFACE.md. No bath-coupled pulse is moved as a channel.
3. In the toggling-frame representation every memory-coupled error term belonging to pulse i has form

       V_{i,g_i}(t)=(g_i tensor I) V_i(t)(g_i^dagger tensor I),

   with V_i(t) supported on its fixed error patch A_i tensor the bath. Bath-only terms may instead be included in H_0. All other terms are independent of g_i. The physical held-frame wrappers must truly yield this representation; the reserved frame support excludes an uncharged intersecting memory operation.
4. G_i is a subgroup of code stabilizers detecting the full syndrome of patch-A_i Paulis. There is no logical Pauli supported in A_i.
5. Other bad/pending operations remain at their physical times and have their fixed allowed memory supports. All operations on or across a clean reserved memory patch during its error interval belong to its stipulated local pulse; otherwise it is not clean. Pending pulses at the deterministic endpoint are charged as bad and never completed fictitiously.

These conditions concern the full physical/dilated circuit, not merely isolated reduced pulse channels. An uncharged g_i-dependent controller interaction violates the algebraic and locality premises.

### Which frame variables are transformed

For the finite-duration application, Fourier-transform ONLY the frames of geometrically clean pulses that have fully completed, including frame removal, by the fixed deterministic horizon. Classification is a function of the exogenous geometry/noise schedule. Fix all other frame seeds and exogenous primitive schedule/noise variables as unselected parameters, prove the bounds uniformly in them, and average them afterward. Genuine endogenous measurement/dilation outcomes stay inside the common dilation and are summed at the effect level; they are not conditioned and normalized in the moment proof. Individual record subeffects may be retained unnormalized. A pending wrapper has not canceled and can carry additional frame dependence at the endpoint; its frame is therefore not treated as a selected small-action character. Its actual prefix remains an arbitrary charged bad operation.

The restricted physical sequence is: exact bath-independent correction circuit; completed application of an ideal stabilizer frame; finite weak local memory-bath pulse; completed frame removal. The whole fixed-duration correction/frame/pulse support is reserved. Remote operations during an active clean frame are disjoint from its full memory-frame support, although they may share the bath. Toggling then conjugates exactly its own pulse terms and leaves all remote memory/bath-only terms unchanged. This derives the additive representation without assuming generic correction gates are pointwise stabilizer covariant. Frame application/removal errors require a separate qualification.

Genuine record-dependent pulse coefficients must be represented by the same fixed common-dilation Hamiltonian under all deletion/interpolation settings. A controlled bath/record operator with a uniform operator bound is allowed. A collection of separately calibrated branch models that silently changes the controller when a coupling is deleted is not sufficient. Final Fourier labels remain unavailable to the controller.

## 3. Global Fourier labels control local completion-time Pauli histories

Under Section 2, fix the primitive schedule and a frame-independent physical/dilation Kraus record alpha. Expand the full propagator or record map in its convergent chronological Dyson expansion, and expand each local interaction factor in a memory-Pauli basis with auxiliary/bath operator coefficients. Bad operations may have arbitrary such coefficients. Keep correction projectors and prescribed correction Paulis as explicit memory factors.

A factor from clean pulse i has the form

    chi_P(g_i) P_Ai tensor B_P(t),

where chi_P is its stabilizer conjugation character. The bath factors may be noncommuting and shared across all pulses. None is rearranged.

For each expansion monomial, move ONLY the memory Pauli factors belonging to pulse i to its completion time. Each intervening memory operation is disjoint by cleanliness, so these memory commutations are exact. Their order relative to one another remains their original chronological order. The auxiliary/bath product remains in the original chronological order throughout.

This is a rearrangement of tensor-factor algebra within a monomial, NOT serialization of the pulse's joint channel. One must not regroup its bath coefficients into an independent per-pulse map. Crossing pulses with noncommuting bath terms are covered precisely because only their commuting memory factors are moved.

The resulting net memory Pauli E_i is supported on A_i, and its character is the product of the characters of that pulse's factors. Averaging the global monomial against chi_i therefore selects exactly

    character_Gi(E_i)=chi_i.                              (4)

This remains true for arbitrarily many insertions from one pulse and for bath-only insertions. Pulse zero-character contributions need not have a perturbatively small amplitude.

Choose a patch representative P_{i,chi_i} of each nonempty character, with P_{i,0}=I. By detection completeness and no local logical,

    E_i=P_{i,chi_i} M_i up to phase,

where M_i is a code stabilizer supported on A_i. At the completion-time point in a particular Pauli history, the current memory factor is E V_code. Hence M_i acts as a scalar sign on that entire logical subspace. Absorb this sign and any Pauli phase into the chronological auxiliary coefficient. Replace E_i by P_{i,chi_i}.

Thus each term in a fixed GLOBAL Fourier/physical record has a legal support history with:

- exact clean corrections at their justified original starts, before their own pulses;
- omitted/bad corrections and arbitrary bad-gate Pauli terms charged by the existing flags;
- one representative patch Pauli at each clean completed pulse with nonzero chi_i;
- no added memory support at zero-character clean completions;
- all pending-prefix operations kept and charged without fictional completion.

The full Fourier Kraus operator may be a coherent sum of these histories with complicated interleaved bath coefficients. No positive Pauli mixture is asserted. Every history in the sum shares the same allowed support record (primitive schedule plus global chi), so a universal common-decoder certificate can cover them simultaneously.

Memory projectors at unrelated correction starts remain valid in this rearrangement: their FULL physical supports are included in the reserved patches, so they commute with the memory factors being moved whenever they lie inside a clean pulse interval. Moving a factor across a merely vertex-disjoint but support-overlapping check would not be justified.

## 4. Good CP subchannel without a causal character instrument

Let G(h,chi) be a fixed input-independent support predicate of the primitive schedule h and the final global character tuple chi. It must certify every expansion history just described. It may not depend on an initial state, a favorable bath coefficient, or a state-dependent coupling construction.

The full-horizon Fourier transform is a unitary change of Kraus representation over the independently averaged private frames. Consequently the operators K_{h,chi,alpha} form a legitimate COMPLETE Kraus family even though chi has no causal local interpretation at pulse completions.

Select good records directly in that family:

    Good(X)=integral dP(h) sum_{chi,alpha} 1_G(h,chi)
                 K_{h,chi,alpha} X K_{h,chi,alpha}^dagger.

This is CP and trace-nonincreasing. On a universally correctable record, the common decoder sends each expanded memory history to scalar logical identity; summing its chronological bath coefficients gives I_logical tensor B_{h,chi,alpha}. Thus Good=Id_logical tensor Lambda_g.

If a separate classical argument uses (1), uniformly conditional on h, to bound the probability of G^c by epsilon for every initial joint input, then the existing TNI-good-map completion gives joint-input recovered diamond error at most 2epsilon. No chronological character instrument and no iid Bernoulli domination have been manufactured. The quantum proof needs only a final Kraus representation, an input-independent good predicate, and a uniform bad-effect estimate.

Genuine causal controllers cannot use these final Fourier labels unless their physical availability is separately implemented. A full-horizon mathematical Kraus decomposition does not provide an online control signal.

## 5. Scope and relation to the crossing echo

The exact crossing echo satisfies the pulse-conjugation structure, so its global characters may obey (1) while violating every proposed small chronological conditional bound. There is no contradiction. Its first completed pulse's intermediate character branch has support on both open memory patches; the valid locality statement instead groups memory factors across the full experiment and assigns each net pulse Pauli at its own completion in a TERM-BY-TERM support history.

The separate classical module must therefore use genuine joint-subset moments, not reuse the prior conditional-instrument proof or assert a fresh iid reference mark coupling. Likewise a global support-history rearrangement does not establish a causal local-channel factorization.

This note establishes the two quantum gates: full-joint subset moments and global-character support locality under the stated conditions. It does not qualify pulse controls, characterize arbitrary coherent continuous interactions, or validate hardware error rates. The Hamiltonian deletion-stability and strict reserved-memory cleanliness assumptions remain substantive.

## Independent audit status

The subset moment lemma passed independent review in SUBSET_CHARACTER_AUDIT.md. Completion-time support locality passed independent review in COMPLETION_LOCALITY_AUDIT.md, including the distinction between exogenous conditioning and endogenous record subeffects. The supplementary exact check_memory_only_reorder.py verifies 16 operator identities and 64 syndrome-history cases. These checks corroborate the universal algebraic proof; they are not numerical lifetime tests. The crossing-echo causal-record counterexample was independently checked in INDEPENDENT_CROSSING_AUDIT.md.
