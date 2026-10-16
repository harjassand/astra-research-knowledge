# Independent support/probability audit: qualified noisy correction cores

2026-10-15 21:00 UTC. Separate audit of SCHEDULED_QUALIFIED_CORE_MEMORY_THEOREM.md. Earlier delivered theorems and packets were not changed. Read the gate-interface construction, its independent quantum audit, and the syndrome-refinement audit; those quantum results are inputs here, not inferred from this composition.

## Result

The whole-parent support and local-stochastic composition closes under the explicit qualified-core, fresh-resource, protected-record, and fixed-schedule premises. It does not require a zero-character gadget channel to factor as C_ref tensor a bath map. Its required fact is the much weaker per-record Pauli-orbit transition. Quantum-failed gadgets must be charged over their entire interval, including omission at the original start. The displayed parent count and p_g budget correctly implement that requirement.

Two precision issues raised in review are material premises: (1) genuinely fresh per-attempt ancillas and local syndrome records, excluding inherited record corruption; (2) an exogenous selected-frame set, unaffected by endogenous abort timing. The first was explicitly added and checked. Final status of the second is recorded in the resolution addendum below.

## 1. Zero-character refined transitions

For a selected elementary slot, the imported full-quantum-support Pauli-character identity sets its net error Pauli to identity when its character is zero. This includes extraction ancillas, not just data. In a fixed unnormalized physical record, the remaining quantum gates are consequently the intended gates, with ordered auxiliary coefficients. The protected classical-record condition is needed here: an identity-on-quantum error cannot be allowed to flip a record and thereby choose a different subsequent gate.

For a geometrically clean all-zero-character gadget, move only its memory/private-ancilla factors to its parent start across operations on disjoint memory resources. Preserve all bath factor order. The record values in this algebra are fixed genuine values; this is not a claim that the physical controller sees its record early. Fresh preparation and exact readout contract the private ideal circuit to the refined Kraus factor L_s=Q_(j(s))R_s, with possible scalar and bath filtering.

Every measured check is a code stabilizer and its joint labels determine the sweep decision. Thus R_s E V_code is zero or E V_code for any Pauli orbit, and the surviving Q_(j(s)) is the same sweep correction used by the original envelope. This is enough for the original update F at the moved start in every term. The refined channel may dephase syndrome coherences and its zero-character subchannel may be trace-decreasing; neither fact obstructs this termwise statement.

Fresh ancillas only at time zero would not suffice after an arbitrary bad gadget using the same resources. The added per-attempt reset and private-record premises prevent that propagation loophole. A corrupted prior record cannot choose a new intended branch in an otherwise zero-character gadget. Allowed shared-bath coefficients can retain quantum correlations but cannot introduce unqualified memory feedforward.

## 2. Nonzero characters mark an entire attempt

If any selected gate character is nonzero, discard the assumption of an ideal correction for the whole parent gadget. Expand every actual memory operation in its fixed patch throughout its declared interval into data Paulis with ordered ancillary coefficients. This includes intended extraction gates and measurement/reset/feedforward factors. It is unnecessary to locate a single effective post-correction fault.

At the parent start the actual expansion has no distinguished C or L_s. The reference envelope still uses its original independent clock and the atomic map

    G_b(eta)=sat_(S_b)(F_b(eta)).

Outside the full changed-coordinate stencil S_b, F_b is identity. Inside it saturation is one. Therefore G_b(eta)>=eta for every binary eta. It is monotone. This preserves support for an omitted correction without changing the physical chain or factoring a bad channel through C. Treat the two operations as an atomic envelope update; its fictitious intermediate F_b value need not dominate physical support.

Each subsequent local Pauli term can create syndrome only within the full allowed local birth patch and is paid for at its actual time. The same applies to geometrically bad and pending prefixes. No gates or memory tails may occur outside the reserved interval. A persistent bath may affect later declared gadgets, but that later interaction must be charged or qualified at its own declared memory patch/time.

Long conflict components and large numbers of Dyson terms do not enlarge an individual event support. Every finite Dyson monomial has a finite local event history, and the guard certificate is universal over all admitted histories and times. Norm convergence then extends corrected linear identities to the whole Kraus operator. This is not a physical random-Pauli mixture.

## 3. Retrospective classification is legitimate

The quantum-good/bad choice depends on final global Fourier labels. That does not make physical actions anticipatory: the classification is used only to construct an endpoint support expansion and a Kraus-record predicate. For one fixed h,chi, it supplies deterministic allowed histories. Zero-character gadgets have exact orbit transitions at starts; other gadgets have arbitrary bounded events over their intervals and omitted start corrections.

The chosen Fourier variables themselves, however, must be fixed from exogenous h. Their completion cannot depend on a generated quantum record. A geometrically clean attempt therefore must execute its fixed padded slot/wrapper-completion schedule independently of endogenous outcomes. If a modeled logical abort is admitted, it must be represented inside that same fixed qualified dilation and must still uncompute all selected wrappers. An outcome-dependent unfinished wrapper cannot be removed from the Fourier set after postselection. This is separate from charging its data effects as a marked whole gadget.

## 4. Gadget subset probabilities and full-interval counts

For distinct gadgets J, an assignment choosing one nonzero elementary character in each uses distinct elementary slots. The joint effect theorem bounds that assignment by the product of its a_e^2 values. Summing all assignments gives

    effect(all M_b=1, b in J)
      <= product_b sum_(e in b) a_e^2 I
      <= p_g^|J| I.

Repeatedly counting outcomes with multiple nonzero slots is harmless for this upper bound. The elementary indices are those of the fixed padded schedule; no outcome-selected slot list is substituted. The effect sum includes all endogenous physical/dilation outcomes. Fixing unselected independent seeds is allowed during a uniform bound and averaging them afterward preserves it.

The full exogenous h includes external noise as well as starts. Hence the strong complete-primitive packet lemma applies. No additional conditioning on normalized quantum outcomes is used. Nonselected geometric-bad/pending attempts have mark zero and are already charged by base flags.

A bad parent [s,s+tau] can place an arbitrary birth in slab [t,t+Delta] only if

    s in [t-tau,t+Delta].

The omitted correction at s in the slab is included in this same window. Count every parent location whose full allowed birth patch OR skipped-start stencil intersects the guard. Before any clean selection the candidate mean is at most kappa N(Delta+tau). This is the required interval count; a completion-only test could miss early marked-gadget events.

On one packet color class, candidate-parent sets are disjoint, so one witness from each flag is a distinct parent. Conditional subset bounds and independent complete primitive packets give

    P(all B_v on a separated set J) <= (d0+p_g mu_int)^|J|.

No independence between actual M_b labels is required. A largest class of the fixed Q-coloring yields q=(d0+p_g mu_int)^(1/Q) for arbitrary finite sets. The enlarged packet must include all full gadget/record/reset supports and the conflict partner windows. Its temporal window remains bounded by [t-2tau,t+Delta+tau]. With kappa tau<=1 and Cb>=1 this gives fixed degree in coarse units.

N,D,F,Q must be recomputed for this implementation. The theorem correctly refuses to reuse numerical pulse-only constants. Sectorwise analysis followed by a union bound needs no cross-sector independence.

## 5. Budget algebra and final CP step

Put x=kappa tau and y=nu/kappa. Using the looser candidate mean N(Cb+2x), the contributions beyond delta_ideal are

    F y(Cb+2x)+Nx[2D(Cb+2x)+1]+Np_g(Cb+2x).

Their difference from A0 y+B0 x+C0 p_g is the nonnegative quantity

    2(1-x)[F y+2NDx+Np_g]

for 0<=x<=1. Thus all constants in the conservative recipe check. The sharper mean N(Cb+x) would improve only the marked-parent term. The original start rate in slow/fast flags remains kappa; no selected completion process is treated as Poisson. The correct threshold is q_star^Q, not the prior iid-death marginal tolerance. Geometry/Q precede b, and physical ratios/strength follow the selected b.

For fixed h,chi define G using the robust no-escape predicate for BOTH sectors and all possible full-interval bad-gadget births. G is independent of input amplitudes, bath coefficients, analysis couplings and physical Kraus index alpha. Every term in a selected record is corrected by the same decoder. Its recovered Kraus operator is therefore I_logical tensor an auxiliary operator even though individual zero-character gadgets need not factor as channels.

Summing the complete global Kraus family on G produces a CP trace-nonincreasing good map. Summing its complement produces a CP bad map. Uniform subset/escape estimates over joint input states bound the bad effect; the standard bath-effect completion gives the claimed joint-input diamond estimate, with sector and factor-two constants absorbed. No signed Pauli term is selected as a probability event and no selected map is normalized.

The existing correlated contour, cold-field and zero-exterior torus replay argument applies unchanged to these enlarged flags. Whole-slab coverage and local accumulated-homology invariance still require only bounded actual event supports, which the whole-interval construction supplies.

## Boundaries

This qualifies only cores obeying the actual fixed-core conjugation and whole-dilation deletion hypotheses. Exact/protected wrappers, reset, measurement, records, lookup, timing and final recovery remain premises unless separately qualified. There is no extension to generic control errors or arbitrary shared-bath dynamics capable of corrupting protected records. The statement remains pointwise at each deterministic T; retrospective characters do not create a physical all-times Pauli trajectory.

## Resolution and final verdict — 2026-10-15 21:01 UTC

Verified the amended Section 2. Every geometrically clean attempt retains the fixed padded schedule and completes/uncomputes all selected frames regardless of generated outcomes. The selected set is explicitly h-measurable. A quantum-dependent omission of intended correction action is admitted only inside the same qualified dilation with identity padding, completed wrappers and correct all-zero-character action; other scheduling skips/aborts are restricted to geometric-bad attempts. Favorable-character selection of unfinished wrappers is explicitly forbidden.

The per-attempt fresh ancilla/local-record preparation, exact local reset/discard, fixed finite retained-output scope, and exclusion of inherited cross-gadget record steering were also verified in that section.

FINAL PASS for the conditional whole-gadget support/probability composition. No outstanding support, counting, conditioning or CP-selection clarification remains from this audit. The independent quantum gate/refinement results and original deterministic contour/memory imports remain named premises; this does not certify broader physical controls.
