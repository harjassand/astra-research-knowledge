# Narrow composition gate: refreshed private frames in the scheduled exact-correction memory theorem

Date: 2026-10-15. Conditional composition audit. It changes the homogeneous pulse-effect budget in the existing scheduled finite-duration theorem; it does not prove a new contour theorem, qualify noisy Clifford compilation, or yield a fully autonomous continuous-noise memory.

Target source: ../prior_inputs/SCHEDULED_FINITE_DURATION_MEMORY_THEOREM.md. Effect input: DIRECT_FOURIER_INDEPENDENT_AUDIT.md. Support input: ../prior_inputs/SUBSET_MOMENT_AND_LOCALITY_PROOF.md and its completion-locality audit.

## 1. Exact model amendment

Retain the source theorem's original geometric attempt/start clocks, external Pauli-noise clocks, reserved patches, fixed TOTAL gadget duration tau, exact completed bath-independent correction FIRST, subsequent identity-target weak-noise interval, completed frame removal, fresh resets, pending/dirty/conflict classification, and final decoder.

The initial private uniform frame can be the SAME bounded stabilizer subgroup G_i used by that theorem. Choose m bounded independent generator bits whose uniform values push forward to the uniform group. Redundancy is allowed but gives a looser union bound. Full-Pauli frames are another option only if their full support and all other source requirements are actually covered; replacing the group is not needed for the direct effect proof.

During the weak pulse, each chosen frame generator receives independent Poisson updates, of rates at least gamma>0, independent of every initial frame seed, the original geometric record, the quantum input, and the other selected internal streams. Track the cumulative current frame exactly and remove its exact inverse by the original fixed completion time. Updates are ideal instantaneous operations whose entire support lies inside the SAME reservation. They add no latency, failure rate, interaction tail, resource conflict, or geometric operation outside that reservation.

There is one explicit count amendment: the source assumes a fixed bounded number of ideal frame operations per attempted gadget. Internal Poisson refreshes have an unbounded random count but are almost surely finite on every bounded interval, at fixed bounded rates per generator. The correction circuit still has its bounded gate count. This count change does not enter the geometric flags because the ideal internal updates stay inside the unchanged fixed patch and duration; it is not permission to ignore a real finite-duration or faulty implementation.

Require the ACTUAL compiled common dilation to have

 H_{g,eta}(t)=H_0(t)+sum_selected i Ad(g_i eta_i(t))[V_i(t)]

(up to the consistent inverse-conjugation convention), with no selected seed or update-path dependence anywhere else. The laboratory coupling cannot follow the private compiler frame in an uncharged way. Other protected operations, controller records, bath interactions and final maps must preserve this same private/additive dependence. Exact tracking does not itself prove that interface for a physical controller.

Assume uniform action bound a as before, pointwise ||V_i(t)||<=J, at most m initial generator bits per pulse, and duration at most tau for its error interval. Using the actual shorter error duration improves the formula but tau is a valid conservative bound.

## 2. The essential conditioning separation

Let h contain ONLY the source theorem's geometric primitives: attempt/start clocks, external-noise clocks, and all variables needed for the original conflict/dirty/pending classification. Keep all original h-dependent quantities unchanged.

Let eta denote the selected pulses' PRIVATE internal refresh histories. These histories are exogenous in the physical model but must NOT be conditioned away in the finite-rate quantum bound. For fixed h and fixed unselected seeds/refresh histories, the new bound is

 E_eta sum_{chi: chi_i!=0 for all i in S} sum_alpha
      K_{h,eta,chi,alpha}^dagger K_{h,eta,chi,alpha}
 <=p_new^|S| I.                                          (1)

The refresh average is inside the quantum effect. Alpha contains genuine dilation outcomes, summed without normalization. Equivalently eta and its probability weight are part of the complete actual Kraus index.

The source's phrase 'conditional on all exogenous primitives' must therefore be specialized to h, not reinterpreted to include eta. Conditioning on a rare no-refresh trajectory would generally lose the finite-rate improvement. The packet lemma only needs a uniform subset effect conditional on h, so its input remains satisfied by (1).

Geometry, clean selection and pending classification are functions of h alone. They must not depend on selected refresh outcomes or quantum/dilation outcomes. The rate improvement is invalid for a model in which waiting for an update changes the completion time or its reserved support.

## 3. Homogeneous effective pulse budget

Define

 B(J,gamma,tau)=1/2{exp(-gamma tau)
       [cosh(d tau)+(gamma/d)sinh(d tau)]-1},
 d=sqrt(gamma^2+4J^2),

 p_new=min{1,m B(J,gamma,tau)},
 p_eff=min{1,a^2,m B(J,gamma,tau)}.                       (2)

The direct Fourier proof gives (1) with p_new. Independently, the source action-squared theorem still applies conditional on each fixed eta, because the selected INITIAL frames remain independent and additive, and conjugation preserves the integrated action. Its uniform a^(2|S|) bound survives averaging eta. Both bounds hold for the SAME complete global character family. For every selected subset cardinality r,

 effect<=min{1,a^(2r),[mB]^r} I=p_eff^r I.                (3)

This is a HOMOGENEOUS minimum of uniform bounds. No product of heterogeneous per-pulse minima is asserted; that requires an additional hybrid subset proof.

A looser usable budget is p_new<=min{1,(m/2)[exp(2J^2 tau/gamma)-1]}. At fixed finite rate and sufficiently small J, the exact B has leading behavior J^2[tau/gamma-(1-exp(-2gamma tau))/(2gamma^2)]. A bound that is worse than a^2 need not be used.

## 4. Completion-support proof survives the internal updates

For support algebra only, fix h, a complete eta history, the initial full frame characters chi, and an unnormalized ordinary dilation record. On a finite interval eta has finitely many ideal jumps almost surely. In the exact toggling representation each inserted memory Pauli from pulse i is multiplied by its initial-frame character and an eta-dependent sign. The sign changes its auxiliary coefficient, not its memory support or its character as a function of the INITIAL private frame.

The same completion-time memory-only regrouping is therefore valid under the existing clean reservations. Every pulse's net local Pauli has its original initial-frame character chi_i. The existing stabilizer-detection/no-local-logical argument replaces zero-character contributions by identity support and nonzero characters by their fixed local representatives, up to scalar syndrome signs. Bath coefficients are never moved or regrouped into independent local channels.

No new intermediate support birth is created by the ideal frame updates in this toggling representation: they are exactly tracked and canceled by the actual completed inverse. This assertion uses the full compiled identity, not a claim that an uncompensated physical Pauli jump is harmless. Pending or failed wrappers remain charged bad as in the source.

The resulting support certificate and no-escape predicate G(h,chi) are uniform over eta. Thus one may condition eta for this deterministic support argument but MUST average it for (1). The good CP subchannel then sums all eta records with the SAME G(h,chi); every such good record remains logical identity tensor a bath map after decoding.

## 5. Coarse budget substitution, without changing geometry

Keep the source quantities exactly as defined there:

 Delta=Cb/kappa,
 d0=delta_ideal+2DN kappa^2 tau(Delta+2tau)
       +F nu(Delta+2tau)+N kappa tau,
 mu=kappa N(Delta+2tau).

The same full-primitive packet argument, now using (3) conditional on h, yields

 q=(d0+p_eff mu)^(1/Q),
 d0+p_eff mu<=q_star^Q.                                 (4)

The simplified sufficient recipe becomes

 delta_ideal+A0(nu/kappa)+B0(kappa tau)+C0 p_eff
 <=q_star^Q,

with A0,F,N,D,B0,C0,Q and all support guards unchanged. No refresh-count term is silently added to or subtracted from d0. That is justified only by the exact zero-duration, geometry-independent internal-update premise.

The existing contour, stopped-torus replay, whole-slab support/homology and actual-good-CP completion arguments then give precisely the source theorem's recovered joint-input lifetime conclusion under its remaining premises. This is substitution into an audited proof chain, not an independent reconstruction of its imported contour theorems.

## 6. Scope boundary

This audit qualifies a finite-rate strengthening of the exact-correction-first, private identity-noise-pulse model. It does not extend to a noisy Clifford core merely by inserting moving frames; its actual compiler covariance/dilation and control timing need separate qualification. It does not qualify finite-duration update gates, noisy initial/final frames, corrupt frame records, controller feedback that reads private seeds, or correlated update streams. It does not cover arbitrary uncharged continuous data coupling outside the stipulated pulses.

It retains private initial frames, exogenous starts, fixed reservations/endpoints, exact local tracking/inversion, perfect initialization/readout and all other source idealizations. The added Poisson randomization is internal to each scheduled pulse. The original unscheduled autonomous stabilizer-dephasing proposal remains a different model and is not proved by this composition.

Verdict: the homogeneous substitution a^2 -> p_eff is valid under the explicit model amendment and h/eta conditioning separation above. No heterogeneous-minimum rule or broader physical control theorem is claimed.

## 7. Optional bounded-update-count implementation, with character-only flags

To retain a deterministic bounded count of ideal frame operations, execute at most M internal generator updates per pulse and then stop updating, while still performing the exact final inverse of the ACTUAL current frame at the original completion time. The initial full uniform frame and fixed laboratory coupling remain unchanged. There are at most M plus the initial/final frame operations per pulse. This is still an ideal instantaneous-control model, not a finite-duration update-gate qualification.

Couple it mathematically to the uncapped proposed internal Poisson streams. Let O_i be the latent event that their total number over the pulse interval exceeds M. If the total mean is lambda_i=tau_i sum_j gamma_ij, then

 rho_i=P(O_i)=P(Poisson(lambda_i)>M).

Keep the ACTUAL fault predicate character-only: M_i=1 exactly when chi_i is nonzero. Do NOT declare overflow itself a fault. Even on overflow, the capped protocol has exact tracking/inversion and the same initial-character completion support identity. Thus its existing G(h,chi) decoder predicate remains valid without dummy births or new full-interval flags.

For the selected joint character event, partition the private clock sample space by the exact subset F of selected pulses which overflow. Sum/drop the character constraints on pulses in F; Parseval turns that sum into averaging their initial bits. Condition their clocks and those averaged initial-bit values as unselected baseline parameters. This only enlarges a positive effect.

On the remaining pulses' nonoverflow restriction, the capped and uncapped processes agree. In a reference process keep the fixed F pulses capped, but uncap the remaining selected pulses using their same independent proposed streams. Drop the remaining nonoverflow restriction positively. The direct Fourier bound is uniform in the fixed capped F background and gives (mB) to the number of remaining selected pulses. Integrating the independent overflow streams contributes at most rho to the number in F, where rho uniformly bounds rho_i. Summing F yields

 effect(all actual capped chi_i!=0 on S) <=(rho+mB)^|S| I.

Independently, for EVERY fixed capped update history the selected initial frames retain their private additive dependence and action bound a. The original action-squared proof therefore bounds the SAME character event by a^(2|S|), after averaging all capped paths. Consequently the valid HOMOGENEOUS capped budget is

 p_cap=min{1,a^2,rho+mB}.                                 (5)

The distinction is important: if one instead explicitly declares an overflow to be a bad event even with chi_i=0, the old a^2 bound no longer controls that enlarged event. A conservative budget for that DIFFERENT composite flag is min{1,rho+min(a^2,mB)}. Equation (5) relies on retaining the character-only decoder predicate, which the exact capped tracking/inversion permits.

No heterogeneous per-pulse minimum is asserted. With the exact capped implementation, substitute p_cap for p_eff in (4) and its simplified recipe. The source completion-parent count mu, support guards and all coarse constants remain unchanged. The latent overflow partition is internal analysis of the private update average and remains excluded from geometric h. No physical access to latent unexecuted proposals is assumed.

## 8. Conditional handoff contract and provenance

For a standalone handoff retain both source files:

- ../prior_inputs/SCHEDULED_FINITE_DURATION_MEMORY_THEOREM.md
- ../prior_inputs/SCHEDULED_THEOREM_INDEPENDENT_AUDIT.md

The source conclusion, all geometric constants and contour tolerance, and its named published imports are dependencies of this composition. The present audit verifies the new effect/support interface and parameter substitution only. The prior internal reconstruction is not external validation, formal certification, a useful numerical threshold, or implementation qualification. No canonical source theorem has been edited by this work.
