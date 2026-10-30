# Preparation baseline: Bergamaschi–Liu arXiv:2411.04405v1
2026-10-30. Primary theorem/algorithm inspection and an independently derived interface analysis. No claim that the paper already solves native noisy-controller initialization.

## Bottom line

This is a genuine encoded-Bell factory, not merely error correction of an already encoded state. Its physical output, AFTER its classical Pauli feedforward, is an encoded Bell state with a usable residual error-seed envelope. The remaining obstacle is operational: the factory assumes away the noisy quantum waiting time needed to calculate that feedforward. Starting our ordinary zero-syndrome autonomous controller before the frame is known is not a justified substitute.

## 1. Compact primary-source contract

[Primary HTML](https://arxiv.org/html/2411.04405); [PDF](https://arxiv.org/pdf/2411.04405). Inspected Sections 1.1, 2, 3, 4, 5 and Appendix B, including Figure 4.

Theorem 5.1 uses O(ell nT) qubits, depth O(ell²), and local-stochastic Pauli noise. Its failure bound is nT(p/p*)^{Omega(min(T,d))}; conditional residual noise is O(sqrt(p)). The factory starts from product states, builds the alternating Tanner graph by CZ gates, measures its bulk in X, and applies Rec(s). Figure 4 computes a minimum-weight bulk error matching meta-checks, then any boundary Pauli matching the corrected full boundary/Bell stabilizers. Equations 24–25 describe the actual corrected boundary as Rep(P)|Phi_L>, with syndrome residuals and separately bounded logical residuals. Rep is analytical, not an implemented ideal recovery. Lemma 5.5 supplies the fixed-subset tail. Footnote 1 assumes instantaneous classical computation and no associated quantum waiting noise. The stated baseline decoding time is at most T exp(n); Theorem 1.2 supplies efficiency only given an efficient repeated-measurement preparation decoder. Corollary 1.5 defers feedforward through a shallow Clifford circuit ending in measurement, not through an arbitrary dissipative memory.

## 2. Exact handoff state: the distinction that matters

Here and below, statements are deductions for composition with our memory, not additional claims attributed to the paper.

Write Phi_L for the k-pair encoded Bell target. Let e_partial denote any relocated Pauli fault on the two unmeasured boundary blocks and let P denote the bulk Pauli error. On a successful preparation branch, the physical state after the applied feedforward has the form

    |output(P,s)> proportional to e_partial Rep(P)|Phi_L>.

The syndrome components in Rep are ordinary physical Pauli errors. They have not been physically removed by an ideal decoder. On the good factory event, the separate logical residual factors are trivial. Therefore the correct memory input is a noisy encoded state, not the exact Enc(Phi) initialization in the frozen theorem.

Before feedforward, the corresponding physical state is

    Rec(s)^dagger e_partial Rep(P)|Phi_L>

up to a phase. Rec(s) may have extensive support and nonzero code syndrome even when P=0. Its being a known-in-principle Pauli frame does not make the actual zero-syndrome energy small. It is not generally only a logical Pauli, and it cannot simply be ignored by the autonomous recovery generator.

This observation avoids two false shortcuts:

1. Calling Rep an ideal recovery and therefore asserting an exactly encoded output.
2. Calling Rec a harmless logical frame and enabling the unchanged native controller on the pre-feedforward boundary.

## 3. A constructive initial-error-seed extension of the native proof

Suppose the actual corrected factory supplies a positive good-event ensemble with failure mass eta_prep and, for each CSS sector, a residual Pauli support E0 satisfying a uniform fixed-subset estimate

    Pr[S subset supp(E0), good_prep] <= q^|S|.        (I)

The bound may instead have a fixed prefactor C0; for nonempty S this can be absorbed into a larger constant multiple of q. It is enough to use the UNNORMALIZED good-event ensemble. No conditioning on an individual rare measurement string is necessary.

For a fixed memory-graph set W of m sites and alpha in (0,1], a union over subsets of size ceil(alpha m) gives

    Pr[|supp(E0) intersect W| >= alpha m, good_prep]
       <= 2^m q^(alpha m) = (2 q^alpha)^m.            (II)

This is exactly the fresh-density estimate needed when the native backward witness chain reaches the initialization boundary. Replace the old assertion that the initial representative is empty by this explicit initial-seed terminal alternative. All later physical blocks retain their original actual fault/service certificates. An initial terminal contributes one additional slice; its rooted connected-animal entropy is already of the required bounded-degree form. No physical ideal recovery is inserted.

If E0 is not the chosen sectorwise minimum representative, introduce ONE identity/D0-only initialization cap: include supp(E0) and the separately minimum-syndrome endpoint representatives. Local same-syndrome replacement and their minimum physical weight bound each cap component by a fixed multiple of its E0 seed count. Small cap components differ only by stabilizers. A cutoff-bad cap component is already a dense initial-seed witness bounded by (II). This is an analytical gauge reduction, not a gate or an extra waiting interval.

The resulting candidate extension has the form

    error <= 2 eta_prep + C n(1+t) exp(-c n),

with a new fixed threshold including q and with clean controller/lock initialization still explicitly required. For two Bell boundaries, pair matched positions into columns as in BELL_INTERFACE_AUDIT.md. Summing over which member of each column is occupied changes q to at most 2q and does not require independence between boundaries.

Later native noise can retain correlations with the factory's classical error label if the physical-record moment estimates remain uniform on the permitted joint initial states. One must establish this from those actual uniform contracts; merely saying that a marginal output is local-stochastic does not automatically supply an arbitrary correlated-bath initialization theorem.

## 4. Fidelity versus one-off factory space

For Tanner d=Theta(n), matching exponentially small end-to-end initialization failure requires min(T,d)=Theta(n), hence T=Theta(n) and O(n²) factory qubits at fixed ell. A logarithmic T gives a polynomially small initialization failure, which may be entirely adequate operationally but becomes a polynomial error floor in a claimed exp(-cn) end-to-end channel. Exponentially long subsequent storage cannot repair an already wrong logical Bell resource.

The retained resource still occupies only 2n data qubits after discarding the factory bulk. Thus a one-off superlinear factory is compatible with a constant-rate STORAGE device, but not with a claim of constant total preparation-hardware overhead or an automatically high resource-production throughput. Both should be accounted separately.

## 5. The actual classical-latency obstruction

Rec(s) must first be calculated from newly obtained noisy measurement data. Its minimum-weight bulk inference is not the native GPT syndrome-descent algorithm and does not acquire an efficiency guarantee merely because GPT corrects low-reduced-weight data errors.

During that calculation, the live boundary is in the extensive frame described in Section 2. The native zero-syndrome controller can therefore be far outside its small-component basin. Leaving it off accumulates ordinary physical noise for the entire decoding latency. Leaving it on invokes an unproved high-energy initialization claim. The published constant quantum depth does not distinguish these two problems because its computational waiting time is stipulated to contribute no noise.

The following are genuine possible bridges, each requiring new evidence:

- A preparation decoder and distributed implementation with a certified bounded noisy waiting budget, including quantum storage before feedforward.
- A locally implementable frame-covariant native generator, driven by a sufficiently reliable compatible syndrome target, whose stability is proved even while the frame information is still being decoded. A bare statement that the frame is Pauli does not construct this.
- A separate protected boundary buffer or repeated-measurement preparation architecture, with its own full noisy-control/latency theorem.
- For purely CLASSICAL end results, consume the boundary immediately through a shallow Clifford/measurement workload and postpone classical frame correction. This does not initialize a long-lived live quantum memory and is therefore a different useful interface.

Precomputed tables do not erase runtime dependence on s; unlimited instantaneous table lookup would itself be an additional control resource. Even an efficient polynomial-time decoder would not solve quantum waiting by itself.

## 6. Noise-model boundary and a promising but unproved stronger route

The quoted output envelope is for random Pauli errors. Our native guarantee allows arbitrary local CPTP Poisson kicks with a retained common bath. A finite-depth Clifford factory does not automatically Pauli-twirl those kicks: after Kraus expansion, different Pauli branches can remain coherent and bath-correlated.

There is a plausible direct bridge worth attempting, rather than assuming stochastic Pauli reduction. The factory clustering proof relates a bad mismatch component to a positive density of ACTUAL fault-supported sites. With bounded-depth bounded-range circuits, each primitive CPTP event expands into Pauli terms on a common bounded light cone. One could seek a fixed physical-record event, common to every compatible Pauli term, whose complement gives the initial-seed certificate (I) in CP-effect form, or append the factory's rooted cluster witnesses directly to the native spacetime animal. Exogenous fault-location tails would then be counted once, not once per Pauli branch.

This requires a written common-span/positive-record proof and constants for the factory circuit; it is not established solely by Theorem 5.1's stochastic Pauli statement. Crucially, even such an extension would leave the runtime classical feedforward and physical handoff/clean-controller preparation obligations from Section 5.

## 7. Exact status

**Available:** a constructive strong ordinary encoded-Bell factory under its own noise/control model; a physical residual-state description suitable for initial-seed analysis; and the elementary way its fixed-subset envelope can terminate our memory's backward chain.

**Not available from this paper alone:** noisy finite-rate classical feedforward during live quantum waiting, initialization of our native controller from arbitrary factory boundary frames, or the common retained-bath arbitrary-CPTP factory theorem.

No priority claim and no implication that standard single-shot QEC already performs preparation are made.

## 8. Checked follow-up: Appendix B efficiency and success-event normalization

### Efficiency is inherited, not instantiated for Tanner

Appendix B reconstructs the repeated-measurement syndrome history from the measured cluster string by subtracting cumulative teleportation-frame syndromes (its equations 59–63), then invokes the supplied repeated-measurement Frame function. Its hypothesis is a fault-tolerant STATE-INITIALIZATION protocol with physical residual output, not merely a decoder for low-weight errors on an existing code state. Accordingly, this inspection found no polynomial-time Tanner preparation decoder furnished by that reduction alone. If one is supplied independently, the parity preprocessing is efficient and the reduction preserves that property; the physical waiting-time premise remains to be paid regardless of polynomial complexity.

### Use a subnormalized good measure in INITIAL_SEED_SLAB.md

Let G be the intersection of the factory's no-spanning-cluster and no-logical-residual events. Its failure mass is charged separately. For either sector, the detailed clustering estimate before Bayes normalization gives

    Pr[S subset supp(Rep_sector), G]
      <= A(p) q0^|S|,
    q0=(p/p1)^(1/2),
    A(p)=1/[1-(p/p1)^(1/4)].

This follows by restricting the event on the left of the unnormalized fixed-subset estimate to G. No division by Pr(G) is needed. For every nonempty S, taking q=A(p)q0 gives an LS-shaped upper bound q^|S| whenever A>=1. In the required small-p regime A is a fixed bounded constant. For S empty the good measure has mass at most one.

Thus the generating-function estimate used by INITIAL_SEED_SLAB.md becomes

    E[1_G z^{|E0 intersect W|}]
       <= [1+q(z-1)]^{|W|},   z>=1,

provided the residual representation and any boundary/handoff faults have first been included in E0 with a valid fixed-subset envelope. This is the cleanest way to combine the initializer with the native proof. The complete probability bound then adds Pr(G^c) once; it never treats a normalized rare conditional factory state as a fresh free initialization.

If one prefers a normalized law conditioned on G, its nonempty-subset bound carries A(p)/Pr(G), not exactly q0^|S|. When Pr(G)>=1/2, that prefactor can again be absorbed into a fixed enlargement of q; the literal unrenormalized expression q0^|S| should not be asserted. The paper's asymptotic O(sqrt(p)) formulation tolerates this constant adjustment in the reliable-factory regime.

When combining additional dependent local-stochastic boundary or handoff errors, do not assume independence. A conservative union/Hölder argument still gives a positive-power effective noise rate: if two support sets have LS parameters q1,q2, their union has parameter at most sqrt(q1)+sqrt(q2). Sharper rates require a joint fault witness. Any sufficiently small positive-power rate suffices for the initial seed slab; retaining the exact square-root exponent is not essential to the composition.
