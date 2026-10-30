# Exact physical DATA-term classification for a finite native shutoff
2026-10-30. Structural addendum for the separately constructed recipient bridge. This is not that bridge's acceptance and does not assume instantaneous coupling deletion.

## Physical generator, not its dressed description

On every ownership mask and malformed engine state, the ONLY nominal terms acting nontrivially on physical DATA are the forward C payload Hamiltonian edges and inverse B payload Hamiltonian edges whose U_t has a DATA factor. It is harmless and simpler to scale down ALL C/B payload bundles, including workspace-only gates.

Each such bundle is the full Hermitian pair

    H_(h,t)=g_t |next><previous| tensor U_t(P)
                       tensor 1_(actual resource tag=o_h) + h.c.

The physical gate support is a grouped hub plus one resource. A finite ramp multiplies the ENTIRE Hermitian pair by a bounded real envelope a_(h,t)(u) going from one to zero over a declared fixed interval. This stays a valid local Hamiltonian at every time; no directed non-Hermitian half edge is removed.

Every other nominal term is physical DATA identity:

- acquisition/unacquisition, Q verification, o/z cleanup and failed-test Hamiltonians act only on hub clocks/workspaces where stated and resource TAGS;
- finite label monitors act only on controller/tag/monitor registers;
- LOAD, COMMIT, SUCCESS, rollback/dirty/nonprefix retirement, READY and workspace refresh are actual ONSITE hub reset instruments;
- z->free resets are resource-TAG identity-on-payload instruments;
- measured classical messages, including syndrome-pointer export, act only on their classical/controller registers.

In particular a dirty partial-reset instrument is a bounded DATA instrument in the FOREST REPRESENTATION, but its PHYSICAL Kraus operator is still hub-local tensor I_DATA. Tracing/resetting an entangled workspace does not secretly add a physical DATA generator. Every separately resolved outcome preserves any fixed linear DATA error module through its retained controller coefficients; no normalized-postselection invariance claim is needed.

## FREE/ACTIVE support condition

FREE_h is `(I or Q_i) and no own o_h/z_h tags`; ACTIVE_h=I-FREE_h. It is DATA-independent and commutes the forest unitary. Every nominal term except LOAD is noncreating for each ACTIVE_h; every Hamiltonian preserves it exactly. All C/B payload bundles vanish on FREE_h, including their adjoints.

Consequently, with LOAD disabled, every nominal physical DATA action is confined to the fixed union of R_h over the initially active owners in each initial activity sector. A finite C/B ramp preserves that condition term by term. The physical reset/cleanup/classical terms do not create new DATA support outside this union. Initial coherent superpositions of small active-owner sets are treated by the span of the corresponding bounded Pauli-support modules, not by sampling a classical owner pattern.

A bounded physical insertion can affect only the bounded set of ACTIVE projectors whose supports it meets. Its new nominal DATA support is therefore confined to the corresponding bounded union of R_h. This is the precise owner-cone premise used by a finite-time norm-Duhamel support expansion; it is not a stochastic fault-parent interpretation for continuous noise.

After the ramp reaches zero, the entire old nominal physical generator is DATA-free. Any remaining physical DATA perturbation is the explicitly bounded endpoint noise or endpoint operation, not an uncharged fast old payload Hamiltonian.

## Drain mode and rates

The actual FREE return lemma keeps the I watchdog and needs no I-only absorbing state. If a separate endpoint mode removes ONLY the I watchdog as well, FREE remains invariant and its return path still exists: an I state with no own tags is already FREE; an I state with own tags can clear them directly because I claims nothing. This statement does NOT authorize removing the A/C/B retirement or cleanup machinery needed by the drain. In particular a consistent partially acquired A_i can get stuck if both acquisition and its nonprefix watchdog are removed.

Mechanical/semantic debt healing is a different predicate: removing I watchdog while also omitting an I workspace refresh may leave an idle W-dirty history flag uncleared. Do not promote FREE return into full history-debt healing under that changed generator without checking it. The current-debt contract should be established before any such optional mode change, or the required refresh must remain.

The ramp and LOAD-disable control are explicit endpoint premises whose finite physical realization, timing and faults belong to the recipient/port construction. The raw operator lemma ensures nonincrease under removal or nonnegative rescaling of nominal bundles, but does not by itself implement a perfect global control signal.

## Module boundary still owed by the port

A sparse ACTIVE tail makes the physical forest a bounded-support operator relative to the dressed state because F_h=I on FREE_h. To conclude an actual signed Bell-resource module, the drain must ALSO preserve the correct relative logical class/small-error span from its native stochastic source, retain its finite-time noise errors, and then combine the bounded forest support with that span. Low U alone is insufficient. The separate port author is responsible for that canonical-span and recipient composition; no automatic native-old promotion is made here.
