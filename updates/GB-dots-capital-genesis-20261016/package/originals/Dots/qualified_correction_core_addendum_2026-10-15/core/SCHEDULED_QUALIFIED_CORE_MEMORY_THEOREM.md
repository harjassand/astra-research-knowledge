# Scheduled memory with qualified noisy Clifford cores

Date: 2026-10-15. Status: separate composed theorem with independent internal gate-interface and support/probability reconstruction completed under the exact premises and named imports. See GATE_INTERFACE_AUDIT.md and SCHEDULED_CORE_SUPPORT_PROBABILITY_AUDIT.md. Does not amend the previously delivered overlapping-pulse theorem or packets. This is not a generic noisy-circuit threshold, external validation, or physical implementation qualification.

## 1. Conditional conclusion

Under the exact gate-interface, refinement, geometry and record hypotheses below, sufficiently small external-noise ratio nu/kappa, duration ratio kappa*tau, and qualified-gadget strength

    p_g = sup_b sum_(e in gadget b) a_e^2

give the same type of pointwise recovered-memory bound for sufficiently large compatible L:

    ||Gamma_(L,T)-Id_logical tensor Lambda_(L,T)||_diamond
       <= min(2, A L^4(1+kappa*T) exp(-cL))             (1)

for every deterministic readout T and some CPTP auxiliary/bath comparison map Lambda_(L,T). The input includes an arbitrary finite persistent bath and arbitrary untouched reference. Trace the output bath for the ordinary joint-input memory comparison; fix an independent input bath state for a logical-only channel.

The ideal correction target is now the syndrome-REFINED instrument C_ref, not equality to the original coarse completed channel on arbitrary syndrome coherences. Its transitions on encoded Pauli orbits are the same. Geometrically clean and quantum-good are different notions throughout.

## 2. Required model, with resources still ideal

Independent exogenous rate-kappa Poisson attempts start fixed-total-duration tau gadgets. Every attempt has a fixed bounded reservation P_b covering all data/check/ancilla supports, exact wrappers, gate cores, measurement, record access, feedforward, and reset operations over [s_b,s_b+tau]. Fixed padded timing bounds the number m of quantum slots, including branch-dependent identity slots. All actual memory actions, including those of a failed or aborted gadget, remain inside its declared patch AND interval. No delayed uncharged memory tail is allowed.

Geometrical conflicts, external-noise dirtiness, and pending status are functions of the full exogenous primitive record h. A gadget is geometrically clean/completed only if its whole reservation is disjoint from every other memory/ancilla operation during its interval, contains no external noise, and finishes all wrappers by T. Sharing a persistent bath between disjoint-memory gadgets is allowed. Nonclean and pending attempts, including scheduling skips/aborts caused by geometrical conflicts, are charged as arbitrary local attempts. Every geometrically clean gadget retains its fixed padded slot schedule and completes/uncomputes ALL its selected frames regardless of endogenous outcomes. Its selected-frame set is therefore a function of h alone. A quantum-dependent omission or abort of an intended correction action is allowed only INSIDE that same fixed qualified dilation, with identity padding, completed wrappers, and the guaranteed intended refined action on the all-zero-character branch. Otherwise an actual scheduling skip/abort is restricted to geometrically bad attempts and charged there. Unfinished outcome-dependent wrappers cannot be selected on the basis of favorable later characters. Initial ancillas are actually reset and there are no in-flight attempts at time zero. In addition, EVERY geometrically clean completed attempt must actually receive fresh private ancillas and correctly initialized local syndrome/lookup records, with all prior correlations or corruption removed. Its intended branch is determined by its own protected syndrome-extraction records; a prior failed gadget's retained record cannot silently select or modify an otherwise zero-character correction. Reset/discard of working ancillas and records is an exact local operation within the declared reservation, and unused reset/measurement environments are discarded. If records are retained for output, their fixed finite-dimensional output scope is explicitly included; no unbounded external record register or unqualified cross-gadget feedback is covered.

Each selected quantum slot obeys the EXACT fixed-core compilation and conjugation-covariance hypotheses of GATE_INTERFACE_AND_OBSTRUCTION.md. Its intended endpoint C_e is Clifford on its whole quantum data-plus-ancilla gate support. Independent private full-Pauli input/output wrappers qualify a fixed seed-independent core. In one common local interaction-picture dilation, the selected error terms have actual form

    V_(e,T_e)(t)=T_e^dagger V_e(t) T_e,
    a_e=integral sup_(T_e) ||V_(e,T_e)(t)|| dt.

They are additive in selected seeds and deletion-stable in the SAME whole dilation. All gate supports and branch-uniform action bounds are included. Shared-bath terms can be noncommuting; bath factors are never rearranged. All uncharged memory interactions are excluded. Fixed-core covariance, not isolated calibration fidelity or the words 'Pauli twirl', is the hypothesis. Compiler-following drive errors can violate it, as the source's exact obstruction shows.

Ancilla initialization/reset, frame wrappers, final measurement, record transmission/storage, classical lookup, and branch selection remain exact or independently qualified resources. Protected classical records are stable: error Hamiltonians and bath-only dynamics cannot flip/coherently mix them; only the specified ideal record/lookup operations can write them. Record-controlled coefficients are block diagonal in their genuine record basis. A fresh slot frame is independent of prior records and inaccessible thereafter. All branches fit one padded, fixed-timing, deletion-stable common dilation. Nonlinear classical lookup is not claimed qualified by the Clifford argument.

The ideal gadget implements refined Kraus operators

    L_s=Q_(j(s)) R_s,  sum_s R_s=I,
    Pi_j=sum_(s:j(s)=j) R_s,

where R_s are joint projectors of bounded commuting code stabilizers determining the sweep decision. For the sweep rule, measuring its eight incident checks provides this refinement. The full data/check/ancilla implementation must be included in the actual reservation geometry. The identity C_ref=C D_R acknowledges extra syndrome dephasing; it is not assumed equal to C on cross-syndrome operators.

Only gates in geometrically clean FULLY COMPLETED gadgets have their frames selected for the global Fourier transform. Fix seeds of all other gadgets as unselected parameters, prove uniformly, and average them. Condition probability estimates on exogenous clocks/noise only, never on normalized generated outcomes. Endogenous measurement/controller/dilation outcomes remain in the common dilation and are summed at the CP-effect level. Individual unnormalized records may be fixed ONLY for support algebra.

## 3. Global quantum-failure subsets

For a selected gadget b let

    M_b=1 if at least one of its gate characters chi_e is nonzero,
    M_b=0 otherwise.

For unselected geometric-bad/pending gadgets set M_b=0 as a bookkeeping convention; they are already charged by the base flags. M_b is a label of the complete end-of-experiment Kraus representation, not a causal indication available to a controller.

The gate-level global effect bound, summed over every physical outcome, gives for distinct selected gates S

    effect(all chi_e!=0 for e in S) <= product_(e in S) a_e^2 I.

For distinct gadgets J, union over one nonzero-character gate per gadget. The chosen gates are distinct because their parents are distinct. Therefore

    effect(M_b=1 for all b in J)
       <= product_(b in J) [sum_(e in b) a_e^2] I
       <= p_g^|J| I.                                 (2)

This holds conditional on the full exogenous h, uniformly in unselected independent seeds and all initial joint states. Average those seeds afterward. A common gate action a gives p_g<=m a^2. No independence between actual gadget failures or conditional bound after another character is asserted.

## 4. Deterministic support: two distinct cases

### A. Geometrically clean with every gate character zero

In the global Pauli/Dyson expansion, full-Pauli conjugation fixes one memory Pauli per gate character. For zero character that Pauli is identity on the ENTIRE quantum gate support, including extraction ancillas. Intended gates therefore remain exactly the intended gates in each unnormalized physical record. Protected classical records ensure no identity-on-quantum-support error secretly changes a syndrome bit and hence the later chosen feedforward.

After fixing a legitimate physical record for algebra, move only this zero-character gadget's memory/private-ancilla factors back to its original start across disjoint-memory operations. Keep every bath coefficient at its original position in the chronological auxiliary product. No shared-bath channel is commuted, no causal record is made available early, and no equality of physical CPTP circuits is claimed. Protected block-diagonal record controls let their fixed record values select the same intended branch during this support algebra.

Contract the ideal prepared/read-out private ancillas in that record. The memory factor is the intended refined L_s, possibly with a scalar record coefficient and bath filtering. For any encoded Pauli orbit E V_code, R_s E V_code is either zero or E V_code; its surviving branch is Q_j E V_code, exactly the original sweep transition. Thus the original F_b envelope update at the start is valid TERM BY TERM. Refinement removes/selects terms but adds no new support.

The zero-character gadget need not be a normalized good CPTP channel. It need not equal C_ref tensor one bath channel on arbitrary inputs. Per-record Pauli-orbit transitions are precisely what the common-decoder proof requires.

### B. Geometrically clean but M_b=1, or geometrically bad/pending

Charge the ENTIRE reserved interval and patch. Expand its actual local Kraus/interaction memory factors, including intended extraction gates, measurement factors, feedforward and reset effects, into data Paulis with ordered ancillary/bath coefficients. Do not retain an assumed ideal C or refined L_s for this gadget. Wrong syndrome outcomes/feedforward and omitted correction are admitted within its full bounded reservation.

At its parent start the physical expansion has no distinguished ideal correction. Let F_b be the reference ideal envelope update and let S_b contain every vertex that F_b can change. Use the ATOMIC auxiliary update

    sat_(S_b) composed with F_b.

Its output is >= the pre-update envelope for every binary input. The fictitious intermediate F_b state need not contain actual support. This reference update pays for the omitted correction without inserting a noninvertible C into the actual quantum history.

At every actual local factor throughout [s_b,s_b+tau], saturate the syndrome support of the whole allowed local data patch. All such births are covered by the single full-interval parent flag. There is no factor proportional to the number of Pauli expansion terms and no contraction of a long conflict cluster into one bounded fault. Finite gates or convergent finite-dimensional local interaction expansions are handled termwise, then by norm convergence.

The final result is a set of supported Pauli histories with exact original sweep transitions at zero-character clean starts, omitted ideal transitions at all other starts, and arbitrary bounded local events throughout charged gadget intervals. One common decoder must correct EVERY admitted history in a good schedule, including their coherent sums.

## 5. Full-interval coarse flags and the correct budget

Run the coarse construction per CSS sector, counting both sectors' starts/noise whenever they can affect its guard; union their escape events at the end. Recompute the fixed guard, conflict incidence D, candidate location count N, external-noise location count F, packet graph and coloring Q for the full extraction/wrapper/ancilla gadget. Fix the coarse geometry and Q before choosing b. Write Delta=Cb/kappa, Cb>=1, and x=kappa*tau<=1.

Let delta_ideal contain ONLY slow-clock and fast-word failures at the unchanged original start rate. The geometric/base marginal has the conservative bound

    d0=delta_ideal
        +2DN kappa^2 tau(Delta+2tau)
        +F nu(Delta+2tau)
        +N kappa tau.                                (3)

Here the terminal event is local: guarded candidate parents whose starts lie in [t-tau,t+Delta] INTERSECT [T-tau,T]. It is empty in other slabs. Startup incurs no term under the reset/no-in-flight convention; other conventions need additional explicit costs.

A quantum-failed gadget can cause a birth at ANY time of its interval and can omit its correction AT START. Consequently for slab [t,t+Delta] its parent candidate window is

    s_b in [t-tau,t+Delta],                           (4)

clipped to nonnegative actual starts. A completion-only window is insufficient. Count all parent locations whose allowed full-gadget birth patch or skipped-start stencil intersects the guard. The expected number of candidates is at most

    mu_int=kappa N(Delta+tau)
          <=kappa N(Delta+2tau).                     (5)

On a separated color class, candidate-parent sets and complete primitive packets are disjoint. Applying (2), union over one marked parent per flag, and averaging independent primitive packets gives the full-primitive local-stochastic bound. For every finite set W of coarse spacetime sites,

    P(B_v=1 for every v in W) <= q^|W|,
    q=[d0+p_g mu_int]^(1/Q).                         (6)

Thus the sufficient condition is d0+p_g mu_int<=q_star^Q, where q_star is the correlated-death contour tolerance. The count N may be larger than in previous pulse-only models; identical symbols do NOT authorize reusing their numerical constants.

With the conservative second bound in (5), an easy sufficient recipe is

    delta_ideal+A0(nu/kappa)+B0(kappa*tau)+C0 p_g
         <=q_star^Q,
    A0=F(Cb+2), B0=N[2D(Cb+2)+1], C0=N(Cb+2).          (7)

For common slot action a replace p_g by m a^2. The marked-gadget contribution is not added as an independent Poisson process, and geometry-clean attempts are not assumed quantum-good. The temporal packet windows remain bounded, for example inside [t-2tau,t+Delta+tau], so Q stays fixed under x<=1.

## 6. Contours, actual-record good map, and completion

The local-stochastic contour theorem applies to (6), using joint distinct-sink bounds rather than iid domination. Its deterministic Toom contour existence, edge/sink and enumeration imports remain SST arXiv:2202.10999v1 Theorem 7/Lemmas 13-14 and HT arXiv:2212.08437v2 Lemma 9.15. The stopped torus witness is copied through an injective coarse patch with zero exterior flags; this preserves the subset probability class. The original uniform forcing, whole-slab cover and bounded-event homology argument use the full-interval births of Section 4B. No new propagation mechanism is introduced by refinement or by a zero-character bath filter.

Define G(h,chi) as the fixed robust no-escape predicate built from actual exogenous records and actual GLOBAL gate characters, including every allowed full-interval bad-gadget birth and omitted start. It does not depend on the initial state, an auxiliary coupling, or a choice of favorable Pauli coefficients. Every Pauli term of every selected good record is corrected by the same decoder.

After recovery, sum the complete actual global Kraus family with indicator 1_G. The index alpha includes ordinary physical/dilation outcomes, recovery outcomes, and the unselected frame-seed averaging weights; alternatively integrate those seeds explicitly. This gives a CP trace-nonincreasing Good=Id_logical tensor Lambda_g and a CP complementary Bad map. All small-probability estimates sum endogenous outcomes before comparing effects; none normalizes a selected branch.

Equation (6) and the contour/torus estimate imply a uniform bad effect of order L^4(1+kappa*T)exp(-cL). Trace preservation makes its effect I_logical tensor D_B. Complete Lambda_g by a CP bath map with effect D_B. Twice the bad-effect norm proves (1), with the two CSS-sector factor absorbed into A.

## 7. Scope and missing physical qualifications

This extension qualifies only noisy Clifford cores obeying the ACTUAL fixed-core conjugation/deletion structure, with full quantum-support Pauli frames and protected ideal classical records. It does not qualify arbitrary errors in measurement, reset, lookup, records, clocks, wrappers or timing. Nor does it cover frame-following calibration errors merely because their isolated magnitude is small.

It remains a Poisson-start scheduled finite-duration model. It is not a physical time-independent Lindbladian realization, finite autonomous-controller theorem, general noisy-circuit threshold, useful quantitative threshold, leakage theorem, or historical priority claim. The fixed final decoder and encoded initialization remain ideal. The bound is pointwise at each deterministic T, not an adaptive stopping-time guarantee or a claim that actual coherent intermediate states trace a Pauli-homology path.

For fixed physical nu,tau,p_g, the rate-dependent part of (7) cannot be tuned independently to zero: its unconstrained minimum is 2sqrt(A0 B0 nu tau), subject to admissible kappa. The remaining budget must also cover C0 p_g. Failure of this conservative sufficient test does not establish a device impossibility.

## 8. Dependencies and audit targets

- Gate covariance, full-Pauli character correctness and gadget subset effects: GATE_INTERFACE_AND_OBSTRUCTION.md and GATE_INTERFACE_AUDIT.md.
- Refined-instrument transfer: ../refinement/SYNDROME_REFINEMENT_TRANSFER_AUDIT.md.
- Local-stochastic probability/counting and torus transfer: ../../overlapping_weak_pulses_2026-10-15/classical/SUBSET_BOUND_CONTOUR_BRIDGE.md and ../../overlapping_weak_pulses_2026-10-15/classical/INDEPENDENT_AUDIT.md.
- Prior support/forcing/common-decoder and contour dependencies: ../../coherent_memory_packet_2026-10-15/STATUS.md.

The independent composition audit is SCHEDULED_CORE_SUPPORT_PROBABILITY_AUDIT.md. It verifies Section 4A's unnormalized termwise refined transition with bath filtering, Section 4B's whole-interval replacement and omitted-start envelope, Section 5's full-interval candidate count, actual per-attempt reset, and the exogenous selected-frame set with completed padded wrappers. No remaining internal support/probability clarification is identified within these premises. None of these statements claims a quantum channel factorization of a clean gadget.
