# Independent review: native pause adapter and stopped-memory receiving interfaces

2026-10-30. Reviewer `producer-workspace/audit_topology_free_noise`.

## Decision and exact acceptance boundary

**Scoped PASS after the corrections recorded below.** This is acceptance of (i) the actual structurally clean PAUSE/retire/live-PARK adapter, (ii) its separate all-state NORMAL-or-QUIESCENT event-service witness, and (iii) the BUSY horizon and explicitly restricted stopped-instrument receiving lemmas. It is **not** acceptance of a noisy asynchronous computation, adapter-defect healing, truthful repair epochs, a reliable DONE mechanism, computational progress, or an autonomous quantum handoff.

The adapter changes the generic rollback attempt compiler: it inhibits LOAD and adds PARK and quiescent milestones. The BUSY/stopped lemmas instead use the separately accepted unified idempotent memory with its actual fixed witnesses. These two scoped results cannot be composed merely by attaching PAUSE to that memory; the changed memory service/drift would have to be earned. All earlier memory/recipient whole receipts remain unchanged.

Exact frozen sources in `autonomous_quantum_handoff_20261030`:

- `NATIVE_PAUSE_RETIRE_AND_LIVE_ACK_ADAPTER.md`: ADAPTER_HASH.
- `ACTUAL_BUSY_HORIZON_AND_JOINT_CUT.md`: `4aacc24fb8e0754844a69ed47fab9ac0dca9a221939e98f0bae000b6415ffe88`.
- `TWO_STOPPED_INSTRUMENTS_RECEIVING_LEMMA.md`: STOPPED_HASH.

The 21 imported dependency hashes and their snapshots were checked. Initial review bytes and final reviewed bytes are preserved separately. The SWAP/router note and its persistent-mode obstruction are contextual companions, not a whole router/controller acceptance in this receipt.

## 1. Physical adapter: no erased live native prefix

Every owner whose full read/write footprint meets x is included, not just an owner whose final gate writes x. Each requester has a separate pause bit at the incident hub. Old LOAD, retirement, READY and workspace resets preserve these new fields; new guards are actual onsite source resolutions with the full losses retained. Old erasers cannot accidentally release a request. Including the added fields in the finite actual monitor basis is essential for the later finite-path proof.

A held pause inhibits new LOAD but does not abort a live C/B prefix by erasing its workspace. Existing acquisition, computation, rollback, dirty retirement and cleanup remain actual operations. PARK is a new phase with identity forest, no DATA Hamiltonian and NOT-CLAIM on every resource. It does not retain an invisible live-prefix claim. Old o/z cleanup therefore removes orphan tags even in malformed PARK. Unparking is a complete W reset to Q0, followed by real cleanup/verification; no direct PARK-to-I shortcut exists.

The exact PARK-good convention is W=0 with tags unrestricted. This is legitimate because its frame is identity, like Q0, and it claims no resource. A complete QUIESCENT W reset maps its entire source into that range. Pause-bit operations, phase monitors and cleanup preserve the range; PARK-to-Q0 resets into the inherited Q0-good range for every mask. Requiring no-own tags in PARK-good would be wrong for the given milestone: an onsite W reset cannot clear remote tags. Tags that remain can block availability but are not a retained PARK quantum prefix.

The request rail is actual two-site reversible acquisition followed by an onsite irreversible commitment. Before commitment, reverse bit changes are harmless because no DATA erasure has been authorized. After commitment the adapter holds every incident bit through live verification and ERASE/HOLD. Each verification edge tests the current actual PARK phase, not a remembered ACK. An already verified owner cannot nominally leave PARK while that requester's bit remains one. Thus earlier checks cannot become stale during later checks.

CLEAR also admits a finite actual realization: for one bit, use distinct adapter intermediate labels E0,E1 with two-site edges from (C_j,bit=0) to (E0,bit=0), and from (C_j,bit=1) to (E1,bit=0). Separate onsite resolved transitions E_s to C_(j+1) discard the source bit label. Reverse motion before the onsite commit is harmless; after it the old edge is inaccessible. Repeating this fixed number of times clears only this requester's bits, without an elementary remote dissipator. All added labels and losses are finite and must be included in the service constants.

The ERASE jump itself is onsite on the declared DATA/write set at x. Its authority is a proven source inclusion from the clean structural rail, not a many-owner elementary projector. The structural adapter range contains the rail/pause prefix constraints and actual PARK predicates for already verified owners. Within that range, ERASE sees every incident native forest equal to identity and no incident live DATA Hamiltonian. Quantum coherence among allowed rail positions does not change these operator source-range inclusions. The transition to HOLD is irreversible; RELEASE cannot revisit ERASE, and a later cycle passes through fresh CLEAR/acquisition/verification.

Overlapping repairs retain separate bits. One release cannot unpause an owner while another requester holds a bit. No global all-ready operation is introduced. Each grouped site, rail, coupling and footprint degree remains fixed-size; this is not elementary-qubit locality or a free long-range control bus.

## 2. Clean history, dirty history and the two preserved counterexamples

On a clean native history, an owner active when the stable pause is committed has at most one in-flight transaction. It completes its actual Stinespring attempted channel or rolls back to identity before PARK; the workspace is never discarded through an incomplete clean prefix. All dilation environments remain retained. The number of leading straddlers is the bounded union of incident full-footprint owners, not a new charge per detector read.

For an initially dirty owner, the first actual retirement can have arbitrary bounded-footprint action and remains an inherited charged event. Initial or fault-entered PARK certifies present physical DATA inactivity, not that a clean historical retirement occurred. A later W reset can restore a present mechanical certificate without retroactively making the prior history harmless.

The review found and preserves two distinct failures:

1. With a stricter no-own-PARK certificate, two W milestones can occur before orphan tag cleanup. They do not establish that stricter certificate. The corrected unrestricted-tag PARK convention resolves this.
2. An arbitrary malformed adapter already at ERASE with p=0 can erase x while a neighboring owner has a clean live C prefix. Owner-only SUCCESS counts do not heal that adapter. In an exact two-qubit example, a CNOT DATA-to-W prefix sends |1,0> to |1,1>; resetting DATA sends it to |0,1>, wholly outside the prefix good range. Two earlier owner SUCCESS events do not prevent a later occurrence in the same box.

Accordingly, global owner no-creation and box-end mechanical goodness are conditional on structurally good adapters, or on a separately earned adapter-healing instrument. The all-state event tail below is not an adapter-healing theorem. Keeping a malformed adapter in the charged bad-region history until actual repair is an obligation of the receiving clock-damage proof. It cannot simply be declared healed at the next owner good box.

Caller RELEASE truth and epoch freshness are likewise not solved. A legal release signal can still be semantically wrong. No immutable finite flag, correct global DONE bit, repeat-proof request protocol or clock-repair completion is inferred. Arbitrary initially malformed erase clocks at every site are not an admitted free startup.

## 3. Fresh actual NORMAL-or-QUIESCENT service

The counted event is **ordinary C_L SUCCESS or the new QUIESCENT milestone**. An abort is not substituted for an attempted Phi_h. The quiescent event is explicitly DATA identity, with scalar complete effect on PARK with a held pause; it is not computational progress.

At a nonzero pause mask, select the actual finite monitor word that preserves that mask, follows the real full-alphabet retirement/cleanup/verification route and reaches PARK, then records one complete quiescent gain. Starting in malformed PARK uses its actual W reset. At zero mask, select the real normal-service route, retiring/parking competitors and acquiring the full footprint before the actual C terminal. A paused competitor is NOT-CLAIM and can have its orphan tags cleared; no fictitious resource release is required.

Every new pause/adapter label is monitored in this word. Bounded background Hamiltonians, caller fields and complete reset losses are retained. Selecting constant-label monitor outcomes is a real nominal instrument event with positive finite probability, not perfect freezing. The complete W outcome bundle is summed; an arbitrary starting workspace/reference/bath state is not projected onto a favorable normalized outcome. The ordered leading terms are products of actual nonzero clock edges and unitary payload legs, with finite diagonal-label monitoring and bounded losses. Compact finite alphabets give a uniform one-window effect `A_1^*(I)>=p_1 I` after enlarging the fixed patch and recomputing its constants.

Two windows then give `(A_1 composed A_1)^*(I)>=p_1^2 I` by positivity. This handles arbitrary conditional states after the first hit, not independence. The actual two-hit analysis counter, with complete losses and second gain deleted, has a genuine CP/TNI survival contraction. The imported anchored finite-support polynomial is applied to this modified killed generator, giving a positive local witness and fixed exponential event tail. Separated protected patches require the enlarged monitor/adapter support coloring and corresponding fixed packing constants.

This establishes an event-service disjunction. On a structurally good adapter region, the first owner refresh restores mechanical goodness and the second provides a clean ordinary attempt or genuine quiescent milestone, with nominal goodness then preserved. Without that structural premise, the event tail remains meaningful but the deterministic semantic consequence does not follow. No accepted clock increment or useful computational throughput is asserted.

## 4. BUSY horizon: the exact full-Hilbert cut

For the unchanged unified memory, the accepted physical singleton witness obeys `exp(theta M)<=G<=exp(Theta M)`, commutes the individual BUSY masks and has full-Hilbert drift `L^*G<=-lambda G log G+rho N G`. The admitted clean or certified warm initial moment and `max(nu_0,rho/lambda)<theta b-gap` give a uniform moment barrier.

Take the real complete-loss CP/TNI compression to P_B=1_(M<=bN). Since G commutes P_B, removed outgoing gains are positive and the same subnormalized scalar-Jensen bound applies. Every fixed-body system leg changes only a bounded number of full BUSY predicate supports, even for distant moving partners. Its outgoing source lies in M>=bN-K and has exponentially small mass. Finite-system-leg boundary Cauchy--Schwarz gives the stated actual-versus-BUSY-killed horizon estimate. Bath coefficient maps are norm controlled by the joint cb bound; bath-only dynamics commute the cut and require no unbounded global norm estimate.

These are comparisons for the admitted encoded/ready or certified warm input family, uniformly with logical reference. They are not a diamond bound on arbitrary unprepared full-system inputs. There is no classical first-exit trajectory assigned to coherent clocks.

The alternative common cut P=P_C P_B also closes without cross-witness commutation. P_C and P_B commute, but F_C need not commute P_B and G need not commute P_C. From the two unconditional output bounds, the bad mass is at most delta. For sigma=P rho P, the exact equation is

`sigma'=K_P sigma + P L(rho-P rho P) P`.

Bath-only terms give zero remainder. The bounded system-touching generator sum costs O(N); hence the remainder norm is at most `2 C N sqrt(delta)`. Variation of constants through the actual CP/TNI K_P propagator and final gentle compression yields the stated polynomial(N)(1+t)^(3/2) exponential comparison. No product of witnesses, restricted-drift transfer, or CP domination is used.

## 5. Actual stopped instruments: repaired terminal contract

A final classical record cannot reconstruct an earlier quantum state. The trigger must be a declared actual terminal CP instrument at its physical time, with retained records and an alive/no-trigger direct-sum description. Its nominal controller actions must preserve the fixed memory representation; DATA sensing/backaction is physical and must meet the stated perturbation contract. No fictional nominal SUCCESS record is attached to arbitrary signed HP noise.

Commuting trigger source effects with the respective witness and cut suffices to subtract a positive loss from each alive moment inequality. It does **not** imply a terminal output predicate or logical identity. The review's explicit unitary counterexample has K* K=I commuting every witness/cut, but changes ready to BUSY and flips the logical qubit. The post-terminal bad-BUSY mass is one and logical trace error is two.

The corrected output theorem therefore additionally requires actual terminal intertwiners for P_C and P_B, and identity on the logical factor in the declared canonical module. The output representation is the fixed native forest/canonical/BUSY representation (or declared fixed physical wire relabeling), not a terminal-dependent coordinate choice hiding a logical operation. The concrete sufficient case is identity on all protected/native memory factors and an actual controller/bath instrument only.

Under that contract, compare the actual stopped instrument separately to its canonical-killed and BUSY-killed versions. Both are positive and retain no-trigger-by-H. The latter has zero bad-BUSY output mass, so the former's bad mass is bounded by the sum of the two comparison errors. Apply the physical BUSY cutoff positively to the canonical comparison only **after** this transfer. The cutoff preserves its common outer logical module and commutes its forest; it need not commute its proof witness. Gentle compression gives the advertised unnormalized stopping-safe correctable span, with a finite number of square roots reducing only the exponent.

If only source-effect commutation is available, the valid conclusion is instead an alive/preterminal safe-input comparison, followed by the SAME real terminal map contractively. There is no automatic post-terminal BUSY, canonical-module or ordinary-decoder conclusion. Future receiving dynamics, mode switching and protection must be physically supplied and separately proved. The instrument is not a noiseless quantum holding register. Trigger probability, semantic truth, fixed-bank readiness and normalized rare-postselection fidelity are not guaranteed; conditioning on mass p can cost error/p.

## 6. Independent checks and final scope

The review independently extended the actual inherited I/A/C/B/Q/R label table with PARK and fixed pause masks, rather than collapsing retirement to a black box. It checked 70,380 states per mask and 1,874,112 directed edges: structural no-creation under the corrected PARK convention, held-PARK phase invariance, and reachability of no-own parked/ready targets from every label state (maximum fixture path 17). It also identifies 5,776 milestone cases that would not heal a hypothetical strict no-own-PARK certificate.

The clean reservation graph rerun checks 1,416 states, 6,265 edges and all 24 erase sources, including fresh verification across repeat cycles and overlaps. Its abstraction of native retirement is supplemented by the actual-table test above; neither finite check replaces the full workspace-unitary or finite monitored-path argument.

Independent matrix counterexamples preserve both invalid terminal-effect reasoning and malformed prefix erasure. The joint-cut algebra fixture verifies the projected derivative identity despite nonzero cross-witness commutators. Numerical fixtures are supporting finite algebra/label evidence, not empirical thresholds or whole QCA simulations.

The resulting scoped statements are useful physical/analytic interfaces. The unresolved adapter-healing event, classical damaged-epoch induction, legal frontier increment count, full quantum boundary-comb correctness, receiver/consumer causal order and computational progress remain explicit receiving obligations. Nothing in this receipt changes the earlier accepted memory or continuous quantum-recipient whole theorems.
