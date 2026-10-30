# Physical classical command port and fresh one-way windows

2026-10-30. Concrete adapter, a conditional clean-window lemma, and precise open semantic obligations. No complete noisy quantum controller is claimed.

## 1. Do not turn Gács's history decoder into hardware by notation

Definition 19.5 chooses a latest suitable time in the recent history, with a damage-free condition. This is an analysis decoder. Its conditions are not a supplied local error detector. An actuator must instead execute an actual read operation on actual registers.

## 2. Actual observer operation

Fix a colony size Q and the source's finite alphabets. A command observer uses a native read-only transaction to acquire the full fixed colony footprint, copy its visible structural fields and its Util/Payload packages into private hub registers, and release the tags. The read controls never move or write the source labels. The observer then executes the finite classical decoding table alpha* and a syntactic Safe test on its copied snapshot. All this is a finite CPTP map: read pinching is explicit, classical computation is reversible with discarded workspace, and its output is a finite command register.

One conservative Safe test requires a full member domain with the prescribed Addr pattern and sibling relations, no wrap through the work-period boundary, and every observed Age in the middle interval [Q+1,U-Q-2]. It also runs the source's bounded-error package decoder and rejects a nonaccepted package. Rejecting means NO COMMAND, not erasing quantum DATA.

A fixed Q can require an enormous but finite hub dimension and full read footprint. This is not a constant independent of the selected source level. A recursively implemented higher-level observer would require a separate distributed implementation; it cannot be collapsed into a growing physical hub.

## 3. Conditional clean-window soundness lemma

Let t_read be an actual successful snapshot linearization time. Assume the underlying represented classical trajectory satisfies the source robust-medium rules, and assume:

* the fixed colony is covered by a domain of member cells belonging to the same work period at t_read;
* the source rectangle I x (t_read-2T_star-split_t,t_read] in Lemma 20.1 is damage-free;
* a sufficiently recent switching time exists, as required in Definition 19.5;
* the actual observer snapshot passes Safe and its own native transaction is clean.

Then the observer's decoded command is the command in the source's decoded macrocell at t_read.

Proof. Lemma 20.1 gives error-free current Util/Payload packages. Take the latest colony switching time before t_read. The relevant packages have not changed since that switch. The assumed damage-free history and same-work-period domain make that switch admissible in Definition 19.5. Current finite package decoding therefore agrees with the history decoder. The native read is a serializable snapshot, not a collection of inconsistent values from different instants. The statement does not claim that Safe alone verifies the hypotheses.

This deliberately uses the stronger no-lower-damage window, not merely the absence of higher damage. Extending it to a single lower-level island requires using the full Present Attribution/Healing analysis, including its cases for growth, doomed colonies and healing wakes. That extension is open here.

## 4. Conditional availability, without postselecting on future cleanliness

Inside an undamaged full colony, sibling ages differ by at most one along a neighboring step and decrease away from its center. Choose a central age band strictly farther than 2Q and the source's fixed boundary margins from the work-period ends. If the center advances n ages through that band, Corollary 16.5 bounds its elapsed duration below by

    L_safe >= (n-Delta-3) p1 T_low.

For the actual source parameters the band and n must be checked against U and Q; no numerical universal window is inserted. Throughout a valid such band, a conservative Safe snapshot exists.

If L_safe exceeds a chosen native service window, two fresh successful observer attempts give a valid command except the actual no-service event. A possibly stale first attempt is discarded. This is an inclusion of events,

    {safe band lasts L, but no fresh accepted observation}
        subset {fewer than two required clean completions within L},

not an illicit probability bound conditioned on future damage-freeness. The actual all-state instrument estimate can apply at the band's stopping-time start in the nominal marked-record process. A signed-noise version still needs the common cavity expansion.

The observer's locks delay visible writes. The source cannot be treated as an unaffected CCA while this is happening. The observe–delay–commit adapter therefore includes observers among all owners in its finite service budgets, and final writes still wait for FREE. Establishing the resulting joint primitive-medium strong-trajectory contract remains necessary.

## 5. A useful command design: virtual schedule, not raw completion input

For a predetermined quantum circuit, let the classical target computation issue BEFORE -> ARM -> RUN -> AFTER for each unrolled module. It advances its virtual program independently of unprotected quantum completion bits. A bounded-duration RUN is charged bad if the native quantum service does not finish in time. Quantum measurement/feedforward can be internalized only in explicitly compiled finite local modules, or must be included as actual protected classical circuit operations; a general free decoder is not added.

ARM refreshes only the module's classical one-use latch and workspace, not the incoming unknown DATA. A successful RUN performs T_g exactly once and records local completion. If an earlier damaged command ran g before its legitimate activation, the later valid T_g overwrites its output bank. If that earlier run touched a live incoming bank, it remains a quantum fault and is not 'repaired' by resetting a flag.

Keep idle native controllers refreshing. Compile all DATA-moving payload edges controlled on a hub predicate F initialized to zero. The source's remote classical labels are read-only controls; F is computed before any DATA motion. On clean guard-false histories every DATA edge is physically identity, but ownership, monitors, watchdogs and refresh continue. Thus a malformed old controller is not parked indefinitely until a future quantum input arrives. A corrupted F or dirty prefix is still a marked local quantum fault. This avoids claiming that inactive hardware is fault-free.

Freshness must cover the full actual controller footprint and its neighbors as required by the native forest/cavity theorem. Merely seeing a command value twice is not a proof of freshness.

## 6. The inactive-bank erasure fact

Fix the legitimate good production and consumption events of a wire bank. Before production, any prior contents of that bank are overwritten by the producer's output reset. After consumption, the bank is a disposable zero register. Therefore bad activity strictly outside its live interval has no direct quantum channel to the later logical state, except through other explicitly retained bad ports/bath interactions.

This does not excuse a controller error that persists into a later live interval, nor an incorrect command that prevents the legitimate production/consumption event. An actual service/repair witness must charge those situations. The point is to remove accumulation from old erased resource contents, not to assume away late control errors.

## 7. Still-open central contract

The remaining desired theorem is not just a reliable classical output theorem. It must prove that the actual observer, latch, native transaction and Gács repair together yield an exact good open quantum circuit, with only a bounded-incidence set of ports opened by each charged bad box, AND that live-wire waiting errors receive a finite local-time accounting or a proved protected-memory handoff. The safe-snapshot lemma above is one concrete portion of that contract. The full contract has not been proved.
