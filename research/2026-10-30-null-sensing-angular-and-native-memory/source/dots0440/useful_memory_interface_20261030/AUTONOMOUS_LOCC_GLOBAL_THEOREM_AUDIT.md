# Independent integrated audit: autonomous bilateral global-energy theorem
2026-10-30. Scoped PASS, with the explicit radius and hardware clarifications below.

## Audited object and verdict

Audited frozen AUTONOMOUS_LOCC_GLOBAL_ENERGY_THEOREM.md, SHA256

    02d6535fc45b5b4187b575b0dc37aba088f4c2c3e5d8ba7d51773a2ca40c5146

against the frozen architecture, the FIFO clarification/universal-word proof, the marked-emission moment proof, the Bell-target common-span identities, and the reviewed deterministic GPT density/confinement contract.

**PASS in the stated broader stochastic local-instrument/classical-channel model.** The construction supplies an autonomous noisy classical-message mechanism, not merely a semantic promise of syndrome acquisition. The parameter order is noncircular. Arbitrary initial finite controller/channel states are legitimately handled by marking every hub initially and suppressing early commit attempts relative to watchdogs. The theorem does not require a pre-encoded Bell-state initializer.

This verdict does NOT supply a native two-site-Hamiltonian/onsite-reset implementation, a relativistic communication-carrier model, bare-state loading, or arbitrary-input protection of the enlarged two-sided Bell-target space.

## 1. Protocol and finite service

The unconditional response dequeue in FIFO_PROTOCOL_CLARIFICATION_AND_WORD_PROOF.md is necessary and present in the integrated theorem. ACKs are used only in FLUSH_WAIT, DATA only in READ_WAIT, and all other replies are discarded. The invalid wait-only receiver would deadlock with full FIFOs and a held Alice reply.

The G+1 purge is sound from arbitrary finite queue/worker contents after a master reset. At most G old replies can exist or be generated. At least one acknowledged SYNC is current; strict FIFO order and one-response-before-next-request worker processing then exclude all old READ/DATA. Current leftover SYNC/ACK traffic cannot imitate a new DATA result.

The fixed service word is more than a no-deadlock assertion. The clarification bounds the total number of possible progress transitions before COMMIT by an N-independent L. Every complete round-robin cycle before COMMIT makes progress, hence L+1 cycles force COMMIT. Its final commit is deliberately withheld until the last word letter. Quantum outcomes affect payloads, not the packet-operation budget. A fixed positive-probability Poisson-clock event therefore supplies uniform service from arbitrary controller/channel states.

No Bob or distributed lock is omitted by accident: the declared Bob primitive reads his CURRENT full local syndrome and applies the table/mask atomically. Alice's nominal operations only measure commuting stabilizers. Once that primitive is decomposed into finite gates, this exact justification no longer applies and a local exclusion/prefix compiler is required.

## 2. Unmarked semantics and spoil accounting

An actual Alice DATA fault can invalidate a cached reply and therefore marks every incident hub. Controller/channel faults mark the affected finite set of hubs. A subsequent LOCAL master watchdog clears its cache and forces the full purge before any further commit; this makes mark clearing sound without resetting remote queues instantaneously.

A marked Bob commit cannot make another hub's Alice cache stale: it changes Bob only, and other hubs read Bob at their own commit. Thus controller taint does not branch through nominal corrections. The marked commit may still create a bounded relative Pauli error, which is charged.

Controller-only faults must receive nonzero support mass even if their immediate DATA action is identity. The integrated theorem does this. It pays for a successful clock word whose actual implementation was spoiled. A fixed fault can spoil only a bounded number of packed candidate/hub tests; fresh later word trials contain a watchdog and purge, so old packet corruption does not spoil arbitrarily many later successful words without another fault.

The packed inequality

    kappa_p U <= C_res D+c_Q Q+M_clock

therefore has the required interpretations. Candidate resolution counts either a clean energy-decreasing bounded move, a charged bad mask/service interruption, or a missing private clock word. There is no assumed independent scheduler replacing the actual machine.

## 3. Arbitrary initial classical states: why the boundary factor is sufficient

Starting every analytical mark at one correctly covers any initial master phase/cache/queue/worker corruption. Before its first watchdog, a hub can perform bad local commits, but they are dominated by its independent commit-attempt clock. After its watchdog, arbitrary old remote contents are handled by the actual FIFO purge.

The independently verified Feynman–Kac estimate is

    E_1 exp(theta K(A))
       <= [mu/(mu-v)] exp[a v |A|/(mu-v)],
    v=lambda(exp(theta)-1), mu>v.

It is uniform over arbitrary selected time sets and all initial physical controller contents because the mark domination concerns actual clock records, not their data-dependent transitions. Setting all marks to one at each queried window is a valid worst-case bound, not an independence assumption between windows.

After spatial coloring and all Holder/support-weight dilations, the logarithm of the initial-state factor is proportional to

    N log[mu/(mu-v_effective)].

This tends to zero with lambda/mu. Thus a small but fixed bad-support fraction q can dominate the early uncontrolled commits with an exp(-cN) tail, even when every controller begins corrupted. A large watchdog rate makes the service word unlikely but does not make its probability zero. The subsequent smaller physical-noise threshold can absorb its enlarged service time.

This is stronger than assuming sparse initial controller faults, but it relies on the exact finite state space: every basis state has a specified transition/cleanup interpretation, all packets occupy counted finite slots, and the watchdog resets the ENTIRE master cache/phase/counter. It does not tolerate an arbitrary initial modification of the nominal transition generator itself.

## 4. Parameter choices are not circular

A valid explicit order is:

1. Fix the code, finite local tables, FIFO layout/capacities, footprint incidence, and deterministic GPT constants.
2. Choose final radius budgets and small source/bad-mass/miss fractions z0,q,m satisfying the energy margin. The contraction constants a,A,B depend on the deterministic GPT geometry/persistence counts, not on the clock-word probability.
3. Fix the Chernoff exponent and ALL moment dilations. Choose lambda/mu sufficiently small to make the initial mark boundary term less than the allotted q exponent and satisfy mu>v_effective. Keep all attempt rates positive.
4. At these fixed rates determine the finite service word duration T0 and probability p0. Choose the number of trials J so the actual-clock miss fraction is below m; set T=J T0.
5. Only now choose epsilon sufficiently small that the primitive/marked-emission term epsilon b1(T,theta) fits the remaining q budget. If faulty operations are obtained by thinning, choose their rates so the declared good clocks retain positive rates.

Every quantity remains independent of N. The thresholds can be extraordinarily poor; no claim of practicality follows. In particular one must not fix an epsilon threshold before choosing the potentially enormous service window.

## 5. Source, first exit, and logical class

The physical Bell source must supply the stated COMMON positive-record relative-support majorant. A good source record has a representative E with |E|<=z0N. A minimum same-syndrome representative R has |R|<=|E|; if 2z0N<d, E+R is a stabilizer, not merely a zero-syndrome error. This initializes the correct logical class without any encoded factory.

Inside a window, every clean move decreases U globally, regardless of whether later reduced weight would leave the small-error radius. Every charged bad edge changes U by at most twice its support mass. Therefore the within-window energy cap is available BEFORE invoking the first-exit contradiction. The active-density packing only needs the safe window-start representative. This avoids circular use of confinement.

At a first crossing of rN, the preceding canonical representative has weight at least rN-s and is still within confinement, contradicting the established energy cap. Along every subsequent local edge, |R|+|f|+|R'|<d makes the zero-syndrome difference a stabilizer. The theorem therefore controls the relative logical class; low energy alone would not suffice.

**Radius clarification.** If r is used separately for X and Z sectors and final recovery uses a total physical representative, require explicitly

    (r_X+r_Z)N<d/2.

A conservative equal-radius choice is 4rN<d, in addition to each canonical-edge bound 2rN+s<d and confinement cutoffs. The integrated theorem's final instruction to choose the combined representative inside the common recovery radius supplies this requirement, but the earlier per-sector inequality alone would not. This is a choice of smaller fixed constants, not a new theorem assumption.

## 6. Coherent records and output meaning

The entire good event depends on positive source/fault/clock records and their common support envelopes. Each such record controls every Pauli/matrix-unit coefficient history; retained-bath coherence is not replaced by sampled Pauli errors. The final relative recovery factors the SAME pure logical Bell target from the entire safe span, including coherent common-syndrome gauges and arbitrary controller/bath correlations.

The unconditional union bound over the source failure and actual bad windows is legitimate without temporal independence. The factorization then gives target trace error at most twice the bad-instrument mass. The gauge-input-to-constant-Bell diamond formulation is appropriate when the instrument bounds are uniform. An arbitrary-logical identity channel on the enlarged two-party target space would not follow.

Raw physical Bell pairs already lie in W. Source errors, sparse missing/replaced pairs and their support law must still be declared; high average pair fidelity alone is insufficient. This removes the encoded initializer and common-syndrome computation, not the physical entanglement source or acquisition synchronization cost.

## 7. Exact hardware/LOCC qualifications

- **Nominal LOCC versus adversarial bath.** The nominal implementation uses local quantum instruments and classical messages. Arbitrary kicks accessing an entangled bath shared across laboratories can make the total faulty channel non-LOCC in the resource-theory sense. The robustness theorem allows those adversarial interactions; it must not count them as a free LOCC implementation resource. Strict LOCC hardware uses local baths with classical-only channel faults and shared classical randomness, a subclass covered by the support proof.
- **Communication is a declared primitive.** A FIFO hop is an explicitly granted finite-rate stochastic CLASSICAL channel with finite storage/backpressure. The proof does not derive it from a spacetime-local relativistic carrier, instantaneous long-distance access, or the native two-site quantum hardware. Every delayed packet must occupy a counted slot.
- **Quantum instrument arity changed.** Alice's local check instrument and Bob's current-syndrome/table/Pauli commit are atomic bounded-body CPTP jumps. A two-site Hamiltonian/onsite-reset realization is still a separate compiler problem, including local exclusion, unfinished prefixes, abort/reset safety and the classical purge.
- **Endpoints remain charged.** Signed-resource teleportation/swap is an actual encoded use bridge only with its full finite-latency physical-mask stage and controlled recipient seam. Bare loading/output and arbitrary-delay mask delivery are not granted by this memory theorem.

Subject to these precise interpretations and radius choices, the integrated theorem is technically supported by the audited construction. No stronger native-hardware, geometric, universality, or comparative-performance conclusion is certified here.
