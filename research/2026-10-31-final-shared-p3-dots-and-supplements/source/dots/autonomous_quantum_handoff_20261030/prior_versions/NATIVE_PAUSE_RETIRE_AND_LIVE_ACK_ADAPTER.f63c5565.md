# Native PAUSE/retire/live-ACK adapter for a paused quantum boundary
2026-10-30. New actual local construction for the QCA boundary-port interface. This is a nominal clean-instrument/structural support lemma, not a complete clock-epoch or noisy-QCA theorem. Existing compiler sources remain unchanged.

## 1. What the adapter must prevent

A classical PAUSE bit is not permission to erase DATA while a native C/B prefix still owns it. Likewise a cached ACK from a previous repair cannot authorize a new erase. The proposed adapter uses fresh structural reservations and reads the ACTUAL parked engine phase; it has no reusable cached ACK bit.

Let x be a DATA cell to be erased during a declared repair. Let H(x) be EVERY native owner whose FULL read/write footprint contains x, not merely owners whose final gate writes x. Its size d is fixed. Work with the exact generic Stinespring/rollback compiler in `autonomous_qca_native_bridge_20261030/EXACT_NATIVE_ATTEMPT_COMPILER.md`.

For each incident pair (x,h), add a private pause-reservation bit p_(x,h) at hub h. Hub h has only boundedly many such bits. Every old LOAD/retirement/READY/workspace reset is extended by identity on these new pause fields, with their actual source labels separately resolved when used as guards; no old eraser clears them implicitly. Include the finite pause/adapter labels in the actual onsite reset-timer monitoring basis. This adds only fixed monitor channels at fixed degree. Its LOAD source is changed to require ALL its pause bits zero. This is a real private onsite guard; remove neither the complete loss nor the resolved LOAD outcomes. All already active A/C/B/R/Q dynamics remain unchanged.

Add one PARK_h engine phase, with no acquisition or DATA payload edges. The final Q verification/READY channel enters PARK_h instead of I whenever some pause bit is one. An I engine whose LOAD is inhibited follows its actual I-watchdog/retirement and Q cleanup to PARK. PARK may return only through a complete onsite W-reset to Q0 when ALL pause bits are zero. It does not jump directly to I: fresh cleanup/verification is retained after a malformed parked state. Label monitors remain on. PARK is declared NOT-CLAIM on every resource, so the existing local o/z cleanup removes any orphan own tags even on a malformed parked source. Its hub phase remains PARK during this cleanup. PARK has no DATA prefix or DATA Hamiltonian.

A crucial service correction is required: a genuinely paused hub cannot satisfy the old unconditional two-SUCCESS-attempt witness. Add a separately named complete onsite **QUIESCENT milestone** on PARK with some pause bit held. Its separately W/p-resolved jumps reset W to zero, preserve PARK and the actual pause mask, and are DATA identity. The coarse milestone has scalar effect kappa_Q P_(PARK,paused). It is NOT called an execution of the original Phi_h. The modified cavity/service event is explicitly ordinary C_L SUCCESS OR this quiescent milestone, with the receiver distinguishing the two types. It supplies mechanical refresh/observable parked service while actual computational progress remains a separate classical-controller condition. If the receiver insists on two original Phi_h attempts in every paused box, this adapter is incompatible with that premise; one must not claim the old witness unchanged.

The new history convention is EXPLICIT: F_PARK=I and the PARK-good projector is |W=0><W=0| tensor I_DATA,tags,pause. It does NOT require no-own tags. This is the same identity-frame convention as Q0: orphan tags may block availability but are not a quantum prefix in PARK. Each QUIESCENT gain maps its full source into this good range, even before tag cleanup; request-bit operations, phase/bit monitors and NOT-CLAIM tag cleanup preserve it. PARK->Q0 performs the complete W reset and hence enters the inherited Q0-good range for every tag configuration. Other nominal terms cannot create PARK badness because they do not change its W. These are unconditional OWN-PARK range facts. The extended ALL-owner no-creation statement additionally requires the adapter structural-good ranges of section 3: otherwise a malformed erase clock can reset DATA through another owner's clean live C prefix. On the joint structurally good owner/adapter range, the old forest proof plus the new PARK cases and the live-ACK erase-source inclusion prove nominal invariance. Individual owner-good ranges are NOT globally invariant on arbitrary malformed adapter states.

Every clean path entering PARK through the ordinary Q/READY route has moreover actually retired, erased W and removed its own tags. No live prefix is released or discarded. An arbitrary malformed PARK state with W!=0 is PHYSICALLY DATA-inactive but is mechanically bad until the complete QUIESCENT reset; its initial unknown correlations are not asserted to be a protected input. PARK with W0 and orphan tags is mechanically good under the declared convention, while its tag cleanup remains an actual availability obligation.

## 2. A fresh bounded native reservation rail at x

At resource cell x put a separate finite adapter clock. All its pre-erase Hamiltonians act only on classical reservation/clock fields, not on QCA DATA. No interparty coherent bus is involved; this is an on-chip hub/resource gadget.

The clean cycle is:

1. **CLEAR.** Clear any own p_(x,h) bits through a dedicated cleanup/verification rail before admitting a new cycle. This does not erase DATA. In the clean supplied initialization they are already zero. An orphan request is an availability issue, not authority for a reset.
2. **REQUEST ACQUISITION.** For a fixed ordering h_1,...,h_d, use the actual two-site Hermitian edges

       (A_j,p_(x,h_(j+1))=0) <-> (A_(j+1),p_(x,h_(j+1))=1).

   Other hub fields are unchanged. These edges are between x's adapter and one hub. Reversibility before commitment is allowed: no DATA reset has yet been authorized.
3. **COMMIT PAUSE.** At A_d an onsite resolved clock jump enters V_0. The d pause bits remain one. No acquisition/reversal edge out of V can clear them. After this actual commitment every incident h has LOAD disabled until this adapter's release rail clears its own bit. Other requesters have separate bits.
4. **LIVE VERIFICATION.** Use two-site edges V_j<->V_(j+1) guarded by the ACTUAL phase PARK_(h_(j+1)). The bits remain held. A verified owner cannot nominally leave PARK because p_(x,h)=1. Therefore earlier verifications cannot become stale during later checks. There is no ACK message that can survive from another epoch.
5. **ERASE.** At V_d take an irreversible onsite phase transition to the erase source and apply the declared complete source-resolved onsite reset of DATA x (and only the stipulated small write set at x). Then enter HOLD. All incident owners remain parked and all pause reservations remain held.
6. **RELEASE.** Only on an actual caller-supplied release authorization does a separate release rail clear p_(x,h_1),...,p_(x,h_d), using two-site edges. It cannot revisit the erase source. At its end it enters DONE, and a new cycle must return through CLEAR and fresh request acquisition/live verification. A continuously asserted input is not an instruction to repeat the erase indefinitely.

The ordinary finite reset-monitor construction can be applied to these finite rails to obtain actual positive service on a held request/release interval. For the modified owner event, a finite actual word either follows the ordinary unpaused transaction route or retires/clears into PARK and takes the separately named quiescent milestone. The finitely many pause-mask cases can be resolved at the start; their changes are suppressed only in the selected finite record, with every real loss retained. This supports a fresh union-event witness, not the old two-Phi witness. It is not an atomic multi-owner test. No numerical resolvent from a different alphabet is transplanted. The adapter dimension, incident hub bits, gate count and monitor resources are constants for fixed original footprint degree.

All multi-owner conditions are implemented by this sequential native rail plus held reservations. The DATA-reset jump itself is onsite at x; it does not inspect a remote all-ready projector. Thus there is no forbidden many-site elementary dissipator or global all-ready operation.

## 3. Exact quiescence and quantum boundary consequence

The adapter structural-good range is the span of the clean reachable reservation/phase configurations: acquisition bits match the acquisition index; V/HOLD retain every own reservation; each already verified owner is parked; release/cleanup cannot revisit the erase source; a new cycle restarts through fresh cleanup/acquisition. This is a joint finite local predicate on the adapter, pause bits and incident owner phases, not merely its private clock value. The source-range proof and the finite graph diagnostic establish its nominal invariance jointly with clean owner histories. It is NOT asserted for arbitrary initial malformed clocks.

Starting from this consistent adapter range, a source in V_d/HOLD implies:

- every p_(x,h)=1;
- every incident h is in PARK;
- every such owner has actually completed retirement before PARK;
- no such owner can start another transaction while x holds its reservation.

These are source-range inclusions on the actual joint Hilbert space, not claims that all clocks are classical trajectories. Coherent reversible rail positions are allowed. The final resolved commitment and reset have the stated source ranges.

At the moment an owner's first stable pause reservation is committed, it has at most ONE in-flight transaction. All later LOAD is disabled. If that transaction is clean, it either completes exactly its original Phi_h once, or cleanly rolls back to identity. It may not be silently erased because PAUSE arrived. If it was dirty, its first complete retirement can have arbitrary bounded R_h DATA action, charged as an inherited mechanical boundary fault. Thereafter it is good and parked. This is the actual leading-prefix contribution that the clock-frontier port count must include.

Consequently, before DATA x is erased, every native owner that could act on x has ended its current quantum transaction. Resetting x cannot cut an uncompleted clean Stinespring prefix in half. The set of pre-pause straddling operations is at most one per incident full-footprint owner, with their actual dilation environments retained. For a region, count the union of boundary incident owners rather than a fresh charge per repeated detector read.

Combined with an independently proved bounded number of legal marching increments crossing a frozen classical frontier, these operations define finitely many ACTUAL quantum boundary ports. Arbitrary internal erasure/rejoin dynamics can be absorbed into the open boundary comb; it is not replaced by an instantaneous Pauli fault or ordered gate-fault fiction. The boundary comb/damage theorem remains the receiving worker's obligation.

## 4. Freshness and overlaps

**No stale ACK:** there is no stored ACK used as reset authority. Each cycle commits its own pause bits and then tests current PARK phases while those bits prevent departure. A previous DONE or old message cannot skip the current V rail. A new RESET is unreachable nominally except through that rail.

**Overlapping repairs:** p_(x,h) and p_(y,h) are distinct. Hub h remains parked until ALL held requests release. One cell's release cannot unpause h while another cell retains a bit. Per-cell reset authorization has bounded fan-in and needs no system-wide all-ready barrier.

**Caller epochs are NOT solved:** HOLD deliberately does not autonomously clear its reservations. An old or corrupted caller release signal could let a repair region unfreeze before its CLOCK repair is semantically complete. A correct caller must either supply an actual fresh release/epoch protocol, or guard release by a separately proved present-state validity test on its declared boundary. The earlier clock-frontier note explicitly leaves that issue open; this adapter does not assume it away. Its no-stale-ACK claim concerns native quantum quiescence, not truth of a higher-level repair completion message.

If the caller withdraws a request after pause commitment, the adapter still completes its current retire/verify/erase-to-HOLD cycle; cancellation cannot release a live quantum prefix. If that erase is not desired, a separate explicitly armed abort-to-release path may be added BEFORE the irreversible erase source. It must not be confused with undoing DATA after erasure.

## 5. Corruption and exact scope under the cavity expansion

A physical fault can create a false V_d, clear a held pause bit, corrupt PARK or spoof a release. No finite classical flag is immutable under the admitted noise. Such a branch is a BAD adapter/controller rectangle. Its DIRECT DATA write remains confined to x (or the declared fixed small write set); its reservation changes affect only H(x), and any interrupted native history is charged to those owners' full bounded footprints. Full generic hub SWAP compilation must not turn a read-only large clock detector into a large hidden DATA write.

This structural bounded direct-write statement does NOT bound all later algorithmic propagation of a bad pause/release; the actual clock damage induction must do that. Nor does it assert a uniform multi-fault norm theorem merely from a clean adapter. To use the existing CP-cavity machinery, enlarge the protected patch to include the adapter, its pause bits, all incident native owner-history/forest supports and its reset channels; recompute finite actual return/service witnesses for the NORMAL-or-QUIESCENT union event of this modified generator, and prove the receiver permits the quiescent alternative. Constants and boxes remain finite at fixed degree, but that substitution and the caller's damaged-epoch analysis must be written before whole acceptance.

Initialization is either clean adapter phase/CLEAR with its declared bits, or an explicitly charged bad preparation region. Arbitrary malformed initial erase clocks at every site can cause extensive damage and are not free startup.

This adapter provides the missing actual PAUSE-to-quantum-quiescence leg, with live fresh ACK and bounded native straddlers. It does not provide a reliable classical epoch, a global reset of a quantum codeblock, a decoder/re-encoder, a fresh entangled gate resource, a quantum rewind, or a full autonomous-QCA threshold.


## 6. Completing the fresh normal-or-quiescent witness

The added actual label monitors are important: merely wishing the request bits constant during a proof path would not suppress their coherent native acquisition edges. Use the accepted projected finite-monitor-word argument with every new pause/adapter label and all background losses included.

Resolve the finitely many initial local pause-mask sectors by actual monitor outcomes. In a nonzero-mask sector choose the finite word keeping that mask present, retire the owner's current I/A/C/B/R history through its actual available path, clear its own o/z tags, verify Q and enter PARK. One complete QUIESCENT gain then occurs with positive probability. Own-tag clearance needs no neighboring ownership erasure; another owner acquiring an already released resource does not invalidate the no-own test. Starting in PARK uses its actual W-reset milestone; arbitrary old W is not declared good before that gain. If no pause bit is present, choose the original finite normal-service word (including competitor retirement/parking as needed), while the actual local monitor word keeps the relevant pause labels zero. All request-cell background Hamiltonians and finite reset losses remain in the norm budget.

Each prescribed path has a nonzero ordered leading amplitude from the actual two-site H edges and complete resolved gains. Finite monitoring windows and bounded retained losses give a strictly positive effect lower bound on its full source sector. The selected constant-label records are genuine nominal records, not perfect physical freezing or an external feedback operation. Finitely many phase/ownership/pause sectors cover the local Hilbert space; summing their positive instrument effects yields a one-hit instrument A_1 with A_1^*(I)>=p_1 I in a fixed T_1 window, uniformly over arbitrary starting local/bath/reference state. An early ordinary SUCCESS or QUIESCENT gain already satisfies this one-hit event; no workspace outcome is selected. Positivity then gives (A_1 composed A_1)^*(I)>=p_1^2 I for two consecutive windows. Take T_*=2T_1 and p_*=p_1^2. This handles arbitrary conditional states after the first hit without an independence assumption or a fragile preselected two-event path. All constants are recomputed for this alphabet; none are old numerical values.

Attach the actual two-hit analysis counter to these gains, retain all losses, and delete the second hit. The positive killed propagator contracts its full alive space over T_* by at least p_*. Applying the already proved finite-support anchored polynomial to THIS generator yields a local positive witness alpha I<=Z<=I with K^*Z<=-r Z, with fixed enlarged support. For buffered separated owners the corresponding product construction is the same CP argument; the finite packing constants are recalculated. This is the interface required by the existing nominal-cavity mixed-box bound.

The all-state EVENT TAIL and the deterministic SEMANTICS must be kept separate. The fresh witness bounds failure of two union gains from arbitrary local states, but those owner gains do NOT heal an independently malformed adapter clock. The deterministic consequence is only on a STRUCTURALLY GOOD adapter region (or after a separately earned adapter-healing instrument): an owner refreshed by the union event remains mechanically good and the box contains either a fresh ordinary attempted channel or a real certified quiescent milestone. It does not imply an accepted logical clock increment. A receiver must recognize a legitimately paused box as quiescent and must charge a corrupted or semantically unauthorized pause/release in its clock-damage induction. This change of the good-box meaning is indispensable, not a notational relabeling of an idle loop as computation.


## 7. Preserved malformed-adapter counterexample and remaining healing obligation

Take an initially malformed adapter already at its erase source with its pause bits zero. Let an incident owner h be in a clean live C prefix. The onsite adapter erase can fire and change DATA x without first retiring h. This breaks h's history-good range. Moreover, h can have completed two ordinary SUCCESS events earlier in the same box before beginning this C prefix. Thus the old owner-only two-hit condition does NOT imply end-of-box mechanical goodness when an unhealed adapter is present. Suppressing adapter events on a selected service word proves an event probability lower bound; it does not remove this other nominal branch from the good event.

A two-qubit exact fixture demonstrates the mechanism: U=CNOT_(DATA->W), initial |1,0>, good prefix U|1,0>=|1,1>. Reset DATA to |0> gives |0,1>, orthogonal to the good range U(I_DATA tensor |0><0|_W)U^*. This is not harmless classical metadata damage.

Therefore no inclusive dirty-leading theorem for the MODIFIED paused machine is claimed yet. To obtain one, the receiver must either retain structural adapter defects in its charged bad-region history until an actual fresh retirement/seal is completed, or enlarge the good-box event by an actual adapter-healing instrument BEFORE the owner refresh. The caller/clock-damage proof must specify that mechanism. Merely adding owner milestones or declaring the adapter initially charged does not prove it healed at the next good box.

The accepted old generic compiler/cavity results remain unchanged. What this note presently earns is the actual structurally clean quiescence adapter, its independent all-state union-event service interface, and the precise additional adapter-healing obligation for noisy whole composition.
