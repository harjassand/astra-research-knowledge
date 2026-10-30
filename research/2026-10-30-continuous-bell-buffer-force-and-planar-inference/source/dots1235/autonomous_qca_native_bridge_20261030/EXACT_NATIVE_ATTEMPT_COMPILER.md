# Exact clean native compiler for a finite local attempted-update channel
2026-10-30. New derivation. This is a clean-channel/schedule lemma, NOT a noisy asynchronous threshold theorem.

## 1. Input and physical resources

Let {Phi_a} be finitely many CPTP channels on fixed finite patches R_a of a two-dimensional finite-dimensional cell lattice. Include in R_a EVERY register read or written by the update: quantum DATA, current classical control, old-control buffers, and every marching-soldier clock entering its guard. The controller does not inspect an external live guard during acquisition. Instead Phi_a itself is the complete attempted-update channel: it dephases the designated classical fields, evaluates validity, and either performs the intended buffered brickwork update/increment or its stipulated rejected-attempt action. On valid classical fields this is the intended rule. The finite channel is defined on the full Hilbert space, including invalid/coherent control values.

Install one finite native hub for each translate/type a, private workspace W_a and a finite clock/monitor. Its ready-state LOAD is unconditional at a fixed rate; the QCA guard is not a LOAD enable. This differs explicitly from the old LOCC request-controlled LOAD. Each cell has owner tags and finite monitors; its QCA payload is distinct from these tags. All dimensions, footprint diameters, overlaps and rates are constants. A two-site Hamiltonian acts on a hub and one resource; a hub-only operation can use a fixed owned tag as its second-site guard. A fixed finite-radius planar layout is allowed. Strict nearest-neighbor geometry requires a separately specified constant-size routing/port layout; no regrouping silently supplies absent couplers.

Choose a Stinespring unitary U_a on payload(R_a) and W_a with W_a initially zero. It can be synthesized EXACTLY into a finite hub/resource gate list when arbitrary fixed two-qudit gates are allowed: swap each resource payload into a designated private hub slot, apply the finite unitary on the grouped hub, and swap the payload slots back. The hub is large but fixed; its environment slot retains the dilation output. No physical dephasing/erasure of that slot occurs before the terminal. If a restricted hardware gate alphabet only approximates U_a, that fixed synthesis error is an additional local error and is not silently zero.

## 2. Actual native alphabet and forest

Use the I,A_i,C_t,B_(j0,l),Q_i,R_(parent,j) machine of the accepted rollback construction, with its actual two-site acquisition/verification/cleanup/failed-test edges and separately resolved complete onsite resets. Substitute the new finite gate list, recomputing its lengths and all finite-path constants. No old numerical Lyapunov coefficient is retained.

- LOAD initializes W at I->A0. Acquisition owns the FULL R_a before COMMIT.
- C_t executes the coherent Stinespring prefix.
- A watchdog C_t->B_(t,t) preserves W and the prefix frame. The inverse rail coherently restores DATA AND W before clean abort at B_0.
- SUCCESS C_L->Q0 erases all W basis labels with equal resolved rates. This is the actual dilation discard.
- Malformed masks use the same ownership-deleted forest components and distinct failed-test leaves. Dirty retirement has bounded R_a support.
- No live-prefix release/reacquisition or W refresh occurs in C/B/R.

For each ownership mask set V=I at the least index of each connected forward-path component and extend by its present unitary edges. B_l uses the same V_l; R inherits its parent. I/A/Q have identity frame. The product F of these local direct-sum unitaries is well-defined on the full Hilbert space; actually owned payload supports of different nontrivial factors are disjoint. All nominal Hamiltonians become controller-only in this forest frame.

The physical good-history projector is the corresponding prefix of W=0 in every consistent ordinary sector and zero in failed-test sectors. Its frame version is controller/workspace-only, independent of QCA payload. Every individual nominal Kraus and Hamiltonian preserves each good range; each complete retirement maps its owner's entire space into its good range. These statements use only unitarity of each payload gate, not energy decrease, Pauli structure or idempotence.

## 3. Exact instrument identities

On a clean fully owned C_L source, let U_a(|psi> tensor |0>)=sum_s K_(a,s)|psi> tensor |s>. The separately resolved terminal channel has DATA Kraus K_(a,s), with sum_s K_(a,s)^dagger K_(a,s)=I. Consequently its unresolved DATA action is exactly Phi_a, also when the input is entangled with all other cells, bath and reference. A clean abort has DATA action Id, since inverse-prefix evolution restores both DATA and workspace before any discard.

The source clock projectors and complete scalar losses do not resolve W. Clock/tag monitors resolve no payload or W value. Thus clean inter-terminal evolution, after forest conjugation, acts only on the controller process. The terminal map factors as a clock transition times Phi_a. Summing the dilation output label s makes the terminal effect scalar on DATA. This proves DATA-independent probabilities for the COARSE record of terminal/abort types and times. It does NOT assert that a particular workspace-erasure outcome has DATA-independent probability.

Starting with a clean controller state independent of the logical input, the nominal channel is therefore a probability-weighted family of compositions of the Phi_a's at terminal times, interspersed with identity aborts and a final local forest dressing. The coarse schedule can have quantum-controller correlations and need not be Poisson or independent between hubs. Its law is independent of the QCA input. If one keeps the terminal environment labels, use the corresponding fixed Stinespring instruments and retain those labels; do not replace their joint state with a fresh independent bath. Summing labels is used only to establish the schedule marginal.

## 4. Linearization and causality

Two updates with intersecting full footprints cannot both be committed at once. The first terminal occurs while its full footprint remains owned. A later overlapping transaction cannot commit until those tags have actually been released. Every other update during that committed interval has disjoint full footprint and commutes with the pending channel. Hence its complete channel can be linearized at the terminal time; no stale read is introduced.

The compiled channel includes the guard computation AFTER ownership. It is therefore exactly an atomic attempted Phi_a on the current linearized payload state, rather than an update chosen from a pre-acquisition snapshot. On valid QCA clock fields, whatever algebraic valid-interleaving theorem the chosen asynchronous rule establishes applies to the terminal sequence. This does not establish that the proposed asynchronous rule's own finite-clock repair and recursive correctness theorem is complete.

## 5. Service is finite, not instantaneous

For any fixed hub the actual full-Hilbert finite path first retires malformed controllers, clears/parks its finitely many competing owners, loads zero workspace, acquires R_a, follows the finite C rail and takes SUCCESS. All outcomes are retained. Monitors and all background terms intersecting the finite path patch are included in its norm budget. This is the same structural finite-instrument proof as in the accepted explicit rollback machine, with NEW generator constants. It gives fixed T_s,p_s>0 for at least one complete fresh attempted channel, uniformly over arbitrary starting controller/quantum states. It is not a constant instantaneous hazard and not a proof that every algorithmic attempt is accepted by the marching guard.

A fair nominal native schedule is thus plausible from an actual finite-path bound, rather than an exogenous clock assumption. Converting its delays to the particular recursive asynchronous theorem and proving a joint local fault-path norm are separate obligations, treated in the companion note.

## Sources and boundary

Physical machine: `producer-workspace/EXTENDED_MACHINE_AND_OPERATOR_PROOF.md` (73e1b695d260dc3821ea39c4241bd33730cf5b393bf478c6ca512fbb4c9ab34b), and `ACTUAL_SUCCESS_SERVICE_AND_GLOBAL_ASSEMBLY.md` (b3cbf9b11cbfc41a8c4f130527711f7875235dbc046bbda8fec8717bdc6eb810). Its LOCC-specific FIFO/service semantics are NOT imported; only the verified finite native forest/reset architecture and proof method are substituted above.

This note supplies no ideal encoded initialization, no noiseless program registers, no automatic continuous-noise threshold and no ideal endpoint forest inversion. A universal operational theorem must pay these interfaces separately.
