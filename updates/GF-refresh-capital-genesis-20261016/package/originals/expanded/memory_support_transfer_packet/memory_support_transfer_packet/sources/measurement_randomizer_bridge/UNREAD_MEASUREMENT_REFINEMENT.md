# Unread exact syndrome measurements suffice for the extra measurement cells

Date: 2026-10-15. Verdict: **PASS.** This is a separate scope refinement of DETERMINISTIC_MEASUREMENT_CELL_COROLLARY.md. The actual recorded-instrument theorem in REPORT.md is unchanged.

## 1. Exact resource assumption

Suppose the extra syndrome-measurement boundaries implement the exact NONSELECTIVE channel

    D_G(X) = sum_s P_s X P_s

on the full retained memory plus persistent bath, with P_s acting on memory and identity on bath. Each boundary uses a fresh reservoir, and no discarded reservoir subsequently interacts with the retained memory, persistent bath, controller, or other resources that can feed back into them. No later operation, timing choice, correction decision, or acceptance criterion uses the extra outcomes.

The device need not expose any readout. If it does expose a noisy readout that is entirely ignored, readout fidelity is irrelevant to this theorem provided the stipulated exact full-joint channel and no-feedback condition actually hold. This does not relax the original exact correction-controller assumptions or the final decoder assumptions.

An initial nonselective D_G after the completed exact correction supplies the entering sector label in the proof. Alternatively, an already-qualified exact correction/premeasurement may supply the initial sector and its intended deterministic shift. One cannot simply invent an entering label without either this actual pinching or another proved sector-preparation/refinement property.

## 2. Fixed latent-record dilation

Choose the same canonical measurement-copy Stinespring isometry at every interpolation value:

    W_G = sum_s P_s tensor |s>_E.

It satisfies W_G^dagger W_G=I and Tr_E(W_G X W_G^dagger)=D_G(X). Give each boundary a distinct fresh E. A fixed unitary extension with E initialized in a fixed pure state exists and is independent of every noise-deletion parameter.

Keep these environments untouched only in the mathematical dilation; they need not be readable or physically stored as protected controller bits. Physical disposal or processing in an isolated external reservoir is immaterial if the composed channel on retained systems is the same and no information or interaction returns. Thus a convenient dilation can retain orthogonal labels even when the apparatus never reads them.

Let u_(i,0),...,u_(i,M_i) denote the latent basis labels of these distinct reservoirs. Define fixed output-environment projectors

    Q_(i,l) = 1[u_(i,l) != u_(i,l-1)].

They are diagonal in one environment basis and commute, including adjacent comparisons that share one label. They are theoretical Kraus predicates, NOT observed syndrome flags or accessible controller signals.

## 3. Deletion-nullness is an operator identity

When a cell's own perturbation V_(i,l) is deleted, every remaining operation during that clean cell preserves the G_i sector. In particular, remote operations on disjoint full memory reservations may act arbitrarily on the common bath but commute with the memory projectors. Consequently

    P_t U_(cell,deleted) P_s = 0 whenever t != s.

This holds for all retained input vectors, including arbitrary bath/reference correlations, and for every other real interpolation parameter. The subsequent evolution is identity on the chosen copied-record environments. Therefore, in the complete fixed dilation,

    Q_(i,l) U_(z_i,l=0) W_initial = 0.

No observation of u_(i,l), physical comparison circuit, normalized conditioning, or readout accuracy is needed. The deletion-null detector lemma is an operator statement about commuting output projectors, so it applies to these environment projectors exactly as it applied to observed records.

## 4. Same positive effects, now explicitly unobserved

Resolve the final environment in the fixed latent-record basis. The resulting Kraus family A_(u,beta) is a COMPLETE Kraus representation of the ACTUAL unread channel:

    Phi(X) = sum_(u,beta) A_(u,beta) X A_(u,beta)^dagger.

For a selected set C of cells, the positive latent-event effect obeys

    sum_(u: all selected changes occur) sum_beta A^dagger A
       <= product_(c in C) a_c^2 I.

For latent parent label b_i=OR_l 1[u_(i,l)!=u_(i,l-1)], the same commuting union bound gives

    F_R <= product_(i in R) p_i I,
    p_i = min{1, sum_l a_(i,l)^2}.

Equal cells of total weak duration tau_i with ||V_i||<=J_i give p_i<=min{1,J_i^2 tau_i^2/M_i}. These are effects of a chosen unobserved Kraus decomposition. They are not experimentally logged fault frequencies, heralding probabilities available to a controller, or small normalized chronological conditional probabilities.

## 5. Support and recovered channel

For each fixed latent environment record, its Kraus operator contains exactly the same chain of sector projectors as the outcome-resolved instrument. Under the full-footprint condition

    Pauli(A_i) intersect Centralizer(G_i)
       subset phase times S_code,

the same memory-only chronological regrouping applies. A latent good parent has no cell syndrome changes; each cell's net Pauli is then a stabilizer and creates no additional support on an encoded Pauli orbit. Latent bad parents are conservatively charged over their bounded parent support. Shared-bath coefficients remain in physical chronology.

For an input-independent common-decoder good predicate G(h,u), sum the corresponding ACTUAL-channel Kraus maps. This defines a genuine TNI CP subchannel even though nobody observes u. The support certificate makes its decoded map logical identity tensor a bath/auxiliary CP map. Its CP complement is bounded by the latent bad effect. The source's CP completion and subset-to-contour argument therefore gives the same recovered-channel conclusion. The controller never needs to know which summand occurred.

This is the same logical status as the original unobserved global Fourier Kraus labels, with a simpler canonical measurement-environment realization. It is a channel decomposition used to prove correctness, not a claim that an unperformed environmental measurement is part of the implemented protocol.

## 6. Non-negotiable boundaries

- Exact backaction on the FULL joint memory-bath channel is required. An isolated data marginal, favorable input calibration, or poor/noisy readout record does not establish D_G tensor identity on the bath or its correlations.
- No discarded-reservoir reinteraction or feedback is allowed in the stated construction. For example, a CNOT from |+> data to a fresh |0> environment produces a dephased data marginal when the environment is ignored; a second CNOT can erase that information and restore |+>. The boundary marginal alone therefore does not justify an irreversible channel composition.
- The extra outcomes must not control future operations. Ignoring a noisy record is allowed; acting on it introduces a new controller channel requiring qualification.
- Exact nonselective pinching is stronger than a finite-time finite-rate dephasing semigroup. For one Pauli S, exp[t gamma(Ad S-I)] retains coherence by exp(-2gamma t) and is not the exact complete pinching at finite gamma t. This refinement removes a readout requirement, not the exact-QND-backaction requirement.
- Measurement support, fresh ancillary resources, duration, and reset/no-tail requirements still count in the total reservation. The total geometric duration theta remains distinct from weak-noise duration tau. No hardware cost or noisy-measurement theorem is obtained by discarding outcomes.
- Pending boundary operations remain charged pending. Missing endpoint channels cannot be inserted fictitiously.

Conclusion: the extra repeated detector readouts may be omitted entirely. Exact nonselective syndrome backaction with fresh isolated reservoirs suffices for the same latent joint-effect and common-decoder proof, while all original correction and geometric qualifications remain.

Independent follow-up audit: PASS. The independent measurement-effect auditor separately checked the canonical dilation, shared-label commutation, uniform deletion identity, and unchanged latent good-CP/common-decoder argument. No additional obstruction was found under the stated full-joint-channel and no-reinteraction hypotheses.
