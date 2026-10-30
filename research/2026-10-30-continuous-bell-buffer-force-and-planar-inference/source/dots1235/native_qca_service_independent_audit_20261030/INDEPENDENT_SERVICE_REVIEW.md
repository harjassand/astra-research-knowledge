# Independent review: actual generic-payload two-SUCCESS service and finite local witness
2026-10-30. Reviewer: `challenge_live_busy_energy`.

## Verdict and exact source
**Scoped PASS with the two completing precisions below** for the actual full-Hilbert two-SUCCESS service/witness instantiation in:

`autonomous_qca_native_bridge_20261030/ACTUAL_GENERIC_TWO_SUCCESS_WITNESS_SUBSTITUTION.md`

SHA-256 `ca214266295eab2797bde54f10ca33a5b2ef4c9e33c5be6fa6dfabbead8b7a61`.

The exact compiler source read is `EXACT_NATIVE_ATTEMPT_COMPILER.md`, SHA `2b2279a5ce72a0a8a89baf2ccd935f58272a4e00f9ecc104784f3e4a8d7310de`. Both are copied in `reviewed_sources/`; actual reset/monitor/polynomial and rollback dependencies are hashed separately.

The completing precisions, confirmed by the author, are:

1. Park the TARGET h as well as each already cleared competitor while later competitors are being cleared. The target's LOAD/I-watchdog are released only at its designated LOAD step. Parking is actual record selection with all losses charged, not a physical halt.
2. For the probability proof, use a freshly proved one-SUCCESS full-state effect p1 at T1, then two consecutive successful-window CP instruments. This gives T2=2T1 and p2>=p1^2 without independence or delicate early-first-SUCCESS bookkeeping. The source's m2 remains a valid finite reachability bound; no unverified direct multi-event numerical constant is needed.

This earns the actual new contract

    alpha I<=Z_h<=I,
    (L0^rec-J_h^kill)^*Z_h<=-r Z_h

with fresh finite support/constants for the declared generic onsite-only Stinespring/rollback machine. It supplies the formerly conditional service input of the CP cavity/norm theorem. The earlier conditional cavity receipt SHA `7161a260a9eba75a1af661e85e2c50ebd939d9a3c05610e35235d4a67f449e4c` is unchanged.

It does NOT prove ideal asynchronous-QCA semantics of a serviced box, success of the payload's marching guard, bounded dirty-leading damage, recursive progress or universality. DATA-independent coarse timing is certified only under the CLEAN input condition in section 6, not for arbitrary dirty clocks.

## 1. The new generator is actually specified; old LOCC waiting is absent
Each hub has one fixed finite attempted CPTP channel on its complete locked read/write footprint. Every variable algorithmic guard/control field is part of that payload. LOAD is a fixed positive-rate complete onsite I-to-A0 reset with W=0, UNCONDITIONAL on those fields. No Alice/Bob split, FIFO, request/reply, cache purge, pending external program or classical intersite transport is retained. Thus an invalid algorithmic guard cannot block the physical service path; it is evaluated inside the finite attempted channel, which may reject semantically while still physically completing.

The Stinespring unitary is a finite exact circuit on grouped hub/resource factors. Full workspace initialization at LOAD/COMMIT, unitary finite gates, coherent inverse rollback and complete equal-rate resolved SUCCESS erasure realize the channel. Enlarged finite hub slots used by an exact synthesis are priced hardware, not a hidden instantaneous nonlocal dissipator. The circuit acts as identity on the monitor registers. A restricted approximate gate alphabet or absent coupler would need its own specification/error charge and is not certified by this ideal exact-synthesis statement.

Every named physical reset is onsite on a COMPLETE hardware site and identity on the external bath. Prefix watchdog is identity on W and enters the equal-prefix rollback copy; it does not erase a nonzero prefix. All erased workspace labels, including zero, are separate channels with equal source intensity. The resulting summed losses are diagonal in clock/control and scalar on erased W. Every ordinary clock/tag basis state belongs to the explicit finite alphabet; no unused binary encoding is assumed to have an exit.

The former outer program/capture registers are removed, not left in arbitrary blocking states. The old service proof's FIFO/transport steps and numerical constants therefore play no role here.

## 2. Exhaustive structural clearing path on dirty inputs
Let k bound full resource footprints, L bound the NEW finite gate lists, and d bound resource owner incidence. For target h the patch contains h, all owners incident to R_h, and every resource of those owners. There are at most

    n_c=1+k(d-1)

owner hubs and n_c k resource sites. Include every boundary-crossing nominal Hamiltonian and every ordinary reset loss touching this patch in the finite norm budget. The exterior is retained, not frozen.

ClearOwner(g) is available from every phase and requires NO acquisition:

- I/A/Q/R: take its actual complete nonprefix watchdog or direct dirty abort into Q0.
- C_t: take its prefix watchdog into B_(t,t). If its ownership mask is consistent, follow at most L inverse unitary edges to B_(t,0), then the clean abort reset. If inconsistent, an actual failed ownership test has a distinct R leaf and a complete dirty abort.
- Initial B_(j0,l): the same consistent inverse route or inconsistent failed-test route applies. A missing ownership edge is never assumed to connect a disconnected rail to zero.
- At Q0, turn each own o tag into z, reset z to free, verify all k not-own predicates, then take READY to I. Other owners' labels count as not-own and do not obstruct these tests.

Each step is an actual edge/reset in the inherited explicit table. The source's

    M_clear=L+3k+4

is conservative: the consistent C route costs at most one watchdog, L inverse edges, one abort, at most 2k cleanup steps, k verification edges and one READY; the inconsistent route replaces the long inverse traversal by a failed-test edge and reset. The bound covers arbitrary workspace, coherent payload, and malformed ownership states because the nonzero gate blocks are unitary on the ENTIRE workspace/payload space. It does not presume W=0 or a valid QCA history.

Clear h, then every direct competitor. After clearing EACH owner, including h, select no LOAD and no I-watchdog emission until that owner is meant to run again. Their anticommutator losses remain charged. Other nominal I refresh/monitor actions do not leave its ready state. Clearing never acquires a resource; hence later clearing cannot reblock target resources. Every owner capable of holding a tag on R_h belongs to this finite competitor set. Outside owners may change other resources from free to their own tags, but they cannot create a cleared owner's own tag or obstruct its not-own verification. No recursively expanding blocker patch is needed.

At the end every R_h resource is free and h is ready with initialized workspace. Run unconditional LOAD, k acquisitions, COMMIT, the L forward gates, and SUCCESS. The conservative NEW one-success selected-word length is

    m1<=n_c M_clear+k+L+3.                         (2.1)

Competitors remain parked only as an event subset during this finite word. The physical generator is never replaced by an externally stopped competitor generator.

## 3. Actual finite-monitor probability: all hypotheses are transferred afresh
I checked the actual monitor/reset theorem, not merely its previous LOCC conclusion. For the new machine:

- selected Hamiltonian clock blocks are unique gU blocks with U unitary on the full payload/workspace;
- forward and inverse rail indices are distinct, and each failed test has its distinct leaf, so no selected leading block is cancelled by another;
- selected reset intensities are strictly positive on ALL erased workspace inputs;
- complete erasure losses are scalar on W, preventing dark reset vectors;
- the actual finite monitor Hamiltonian/reset alphabet resolves clock/tag labels only, never payload or W;
- all main terms act as identity on monitors;
- all selected states/edges and all local/boundary losses are in the new finite physical patch/norm budget.

Use the NEW m1, monitored-site/clock alphabet, incident no-jump bound B, minimum selected Hamiltonian amplitude g_min and minimum selected reset rate kappa_min in the explicit formulas of `ACTUAL_RESET_INSTRUMENT_TAIL.md`. The LOAD rate, even if weak, enters these values. A previously derived coefficient cannot be retained after changing it.

The actual monitor Gramian has a positive minimum eigenvalue on every positive finite window. Its flush handles monitors initially entangled with one another, DATA, the exterior, bath and reference. Once conditioned on the full allowed timing pattern, the normalized clock instrument has the stated O(B epsilon_window) error; it is not divided by a rare timing probability. Summing the label-conditioned paths is a complete instrument comparison, not a separate error multiplied by the number of possible clock labels.

The one-event proof can treat an early h SUCCESS as genuine success immediately. All other unwanted transitions, including parked LOAD/watchdog jumps, are controlled by the same projected-path/no-jump construction with their full losses retained. The new finite word therefore gives constants T1<infinity,p1>0 such that the actual instrument A1 for at least one h SUCCESS in a T1 window satisfies

    A1^*(I)>=p1 I                                (3.1)

on every physical input and reference extension. No algorithmic ACCEPT outcome or specific workspace-erasure outcome is selected. All such outcomes are retained.

Nominal external bath evolution is uncoupled from the apparatus and is retained as a bath-only CPTP factor; arbitrary initial bath correlations are allowed. Boundary-crossing system terms are already in B. The claim is nominal service, not a trajectory construction in a generator whose reset channels may have been cancelled by generic noise; the separately proved CP cavity is what legitimately restores those instruments in the noisy norm argument.

## 4. Two SUCCESS events by CP composition, and the actual killed counter
The map A1 includes the full nominal evolution to the window endpoint conditioned only on at least one real SUCCESS. From (3.1), positivity gives

    (A1 composed A1)^*(I)
       =A1^*(A1^*(I))>=p1 A1^*(I)>=p1^2 I.

This event has at least one SUCCESS in each of two consecutive windows, hence at least two in their union. It does not assume independent attempts, a Poisson success process or a reset to a fixed joint DATA/bath state between windows. Its second bound is uniform on the arbitrary conditional state left by the first window.

Consequently take

    T2=2T1,    p2=p1^2>0.

Attach the actual passive classical alive counter {0,1}: SUCCESS takes 0 to 1 and leaves 1 at 1. Delete the designated SUCCESS gain from counter source 1, retaining its complete loss. This is the CP/TNI killed instrument for fewer than two SUCCESS events. Starting at 1 needs only one more and is covered by the same conservative p2,T2 bound. The counter is an analytical record annotation with no physical feedback or ideal preparation operation on the apparatus. Its event effect is block diagonal in the classical counter; the construction extends the operator inequality on the alive counter space without postulating a completed absorbing sector.

The actual new killed generator K_(h,2) therefore obeys

    exp(T2 K_(h,2)^*)I<=(1-p2)I.                  (4.1)

The longer explicit m2 bound in the source is consistent with legal reachability; (4.1) is independently earned by the cleaner two-window argument, so no informal claim that an early first event always preserves a preselected two-event word is required.

## 5. Fresh finite-support witness; no controller-only or old-matrix shortcut
The complete deleted gain intensity is bounded by a fixed nu I, determined by the actual SUCCESS rate. Thus

    K_(h,2)^*I>=-nu I,
    a I<=int_0^T2 exp(t K_(h,2)^*)I dt<=T2 I,
    a=(1-exp(-nu T2))/nu>0.

The exact integral has drift at most -p2 I. Its nonlocality is handled by the accepted anchored finite-support polynomial construction, applied to THIS new generator and alive counter.

Every ordinary local adjoint annihilates I away from its support; the sole nonunital contribution is the local deleted second-SUCCESS gain at h/counter. Track that anchor in every polynomial iterate. The local Taylor norm bounds use only the new finite-range/per-site nominal norm budget, not an extensive generator norm. For arbitrary fixed T2 the short-step telescoping construction uses finitely many finite-degree local polynomials and the exact derivative identity K*F_j=O_j-I. It never applies an extensive K to a small approximation error.

The nominal bath-only generator acts trivially on these system/counter observables, so unbounded bath evolution introduces no new polynomial support or norm term. All resulting inequalities extend by identity on the bath/reference.

The new witness can be normalized to

    alpha I<=Z_h<=I,
    K_(h,2)^*Z_h<=-r Z_h,
    alpha=a/(3T2),  r=p2/(3T2),                  (5.1)

or any more conservative positive bounds supplied by the same construction. Supports, degrees and constants can be extremely poor but depend only on the fixed new alphabet, unitary circuit, rates and bounded nominal geometry. They are uniform in N. Z_h may act on DATA on dirty sectors; no false controller-only closure is required.

Enlarge each cavity patch to include that actual witness, its complete hardware sites/monitors and the declared buffered footprint. Nominal finite-range bounded geometry gives bounded patch volume/incidence and buffered packing. For packed witnesses, no nominal term touches two, so the exact product killed drift follows. These are precisely the service inputs used by the separately accepted CP-cavity theorem.

## 6. Clean coarse schedule law is true; arbitrary dirty timing independence is false
On the CLEAN forest range, every nominal Hamiltonian/prefix watchdog is controller-only, a clean abort is DATA identity, and an unresolved clean terminal is a controller transition tensor the fixed attempted channel Phi_h. Completeness of the Stinespring Kraus family makes its coarse source effect scalar on DATA. Monitors resolve no W or DATA. Since the attempted guard is internal to Phi_h and does not enable LOAD/acquisition, it changes the attempted-channel result but not the clock-path law.

Therefore, from a CLEAN forest-factorized controller initialization independent of the QCA input, the marginal coarse SUCCESS/abort types-and-times law is DATA independent. The schedule may remain correlated across controllers and non-Poisson. Individual workspace-erasure outcomes generally ARE DATA dependent. If those environment labels are retained, they remain in the joint Stinespring output; summing them for a coarse probability does not authorize replacing the bath by an independent state.

The all-state service inequality (3.1)/(4.1) is strictly weaker than all-state timing independence. A dirty coherent-prefix example demonstrates the distinction. Let clock states C0,C1 be coupled by

    H=(|C1><C0|+|C0><C1|) tensor Z_DATA,

with terminal reset from C1 at rate kappa, and start the clock in (|C0>+i|C1>)/sqrt(2). For DATA Z eigenvalues +1 and -1, the derivative of C1 population is respectively -1-kappa/2 and +1-kappa/2. Hence subsequent coarse terminal-time distributions differ. Actual finite label monitors do not remove this initial derivative difference. Such a product state is not the specified clean forest-factorized prefix input.

The author explicitly confirms this clean restriction. The cavity norm proof needs only a uniform positive service effect from dirty states, not their DATA-independent timing. Leading dirty retirement/semantic correctness must still be charged by a separate theorem.

## 7. Independent diagnostics and remaining scope
`check_generic_paths.py` uses the explicit rollback transition alphabet and an independently implemented clearing/one-/two-success path selector with unconditional LOAD. It verifies:

- 66,825 initial clock/tag configurations;
- 133,650 target-owner paths;
- 4,366,314 selected legal transitions;
- maximum ClearOwner length 11, one-SUCCESS length 26 and direct two-SUCCESS length 41;
- no acquisition in any clearing route, and all conservative source bounds.

This is an exhaustive finite basis-label eligibility diagnostic, not a probability proof for coherent workspace/DATA or a many-body QCA simulation. Those conclusions use sections 2–5. `check_dirty_timing.py` separately verifies the dirty coherent-prefix timing counterexample, so the clean scheduling scope is not inferred from the service bound.

The new service contract plus the unchanged CP cavity/mixed-box theorem now earns the stated physical signed-box NORM locality for this actual generic payload compiler (with its stated noise assumptions). The separate weighted-incidence receipt broadens only the noise partner geometry, with Q<=1.

No automatic algorithmic guard acceptance, dirty-leading correctness, asynchronous leading-rectangle/progress theorem, encoded initialization, final physical output, practical rate or universality claim is approved. Primary inclusive fault-path methods remain the standard AGP/Terhal–Burkard comparator; the present acceptance is an actual finite native-service substitution, not a novelty claim for the resummation.
