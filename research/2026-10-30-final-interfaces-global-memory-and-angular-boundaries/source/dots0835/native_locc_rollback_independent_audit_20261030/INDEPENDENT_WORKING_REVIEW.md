# Native LOCC integration: independent working review

2026-10-30. This is a working audit, NOT a whole-theorem acceptance receipt. Author sources remain in development. The earlier challenge ledger and source snapshots are preserved.

## Findings already established

1. **The local operator repair is coherent.** The explicit I/A/C/B/Q/R claim table preserves every good range term by term. The rollback copy uses the forward forest value at the same remaining prefix, and the C-to-B watchdog has equal source/target frame. The R leaves must keep all claims. A live C/B/R(C/B) component cannot release and reacquire its actual owned DATA before a complete Q0 reset.
2. **Dirty Bob does not create an unbounded semantic infection.** A dirty reset acts only on DATA actually tagged to that owner, not on every DATA factor in its declared worst-case footprint. Another mechanically clean committed Bob engine owns its entire raw-read footprint, so its snapshot is disjoint from that action. An acquiring engine has not yet taken its snapshot. This is the load-bearing reason Bob-to-Bob propagation is absent.
3. **The one-ghost FIFO allowance survives only with the new I guard.** Alice cannot enqueue HOLD or process a new request while a live engine is present. A malformed C+HOLD either overwrites HOLD at terminal or preserves it through abort; it cannot export both. Quantum phase coherence does not circumvent this: the actual enqueue gain projects onto I, eliminating its C alternative. Pending REQUEST survives rollback.
4. **Delayed dirty Alice retirement is a real new mark birth.** A malformed acquisition state can obtain a resource after a neighboring clean Alice read, then execute only part of its read circuit before dirty retirement. Partial ancilla entanglement/reset can change an Alice stabilizer. Therefore clearing Bob at an earlier watchdog/purge cannot exclude a later stale cache. The actual dirty Alice retirement must set new Bob marks.
5. **Arbitrary native initialization is excluded.** Initially malformed engines can each emit one fast DATA-changing reset at zero external fault rate. Slow SUCCESS rates do not suppress dirty aborts. A concrete sufficient initialization is engine I, W/P initialized, owner tags free, Bob master FLUSH_SEND(0)/cache empty. Arbitrary FIFO/Alice worker classical contents then remain behind the actual first purge. Arbitrary initial Bob WANT needs an additional physical bootstrap mechanism and is not silently included.

## Probability interfaces under review

### Actual retirement

The full alphabet has an explicit path to an actual complete reset: I/A/Q/R have a direct watchdog, C can take the equal-frame prefix watchdog, consistent B can reverse to zero, and inconsistent B has a distinct failed-test R leaf. This covers disconnected malformed rollback rails. The imported finite-rate monitor argument must be applied with the NEW alphabet, path length and incident norm constants; no old matrix or numerical tail constant is reused. Its output is an integrated-window full-Hilbert effect contraction, not an instantaneous hazard.

### Count versus occupancy

The previous ancestor-cell theorem bounds occupied distinct owner/time cells. It does not by itself bound the number of bad DATA resets inside a cell. A useful new route is to count distinct primitive roots with a charged descendant in the observation window. Each root has a bounded number of descendants. For each distinct root choose only one actual descendant path, of depth at most two. Unique canonical ancestors forbid shared Alice intermediate nodes between distinct roots. Consecutive selected intervals at any owner are separated by its actual T reset. This avoids falsely multiplying a shared-parent survival probability.

For a deterministic valid family of these intervals, a buffered witness color captures at least 1/P of their total duration. The noisy killed product witness gives exponential decay in that duration, at fixed multiplicative costs per interval and per prescribed local gain/root insertion. Normalize a selected reset gain by its bounded intensity and complete it to a CPTP map only for this upper bound; do not replace the physical generator by a Poisson-CPTP reset-attempt process.

Integrating an intermediate Alice reset time produces a kernel proportional to age times exp(-beta age), which is integrable. Distinct-root Poisson factorial moments can therefore bound the COUNT MGF. The author's exact lemma is still being checked. One constant correction already requested: direct, zero-edge selected roots can affect another path's larger Lyapunov support, so they too must carry the insertion comparison constant.

### Useful service

The prior two-RETIREMENT certificate does NOT transfer: clean rollback/watchdog aborts are now nonzero. Count actual SUCCESS terminals instead. The prospective construction is a passive record latch counting the first two actual SUCCESS gains. A full-state positive one-SUCCESS window bound gives full alive-latch contraction in two windows; the anchored local polynomial then gives joint shortfall tails. Semantic validity still requires excluding or charging primitive and dirty-Alice service spoils. Marginal success probabilities do not justify independent coins across owners.

The favorable service word must retain every physical Hamiltonian and every no-jump loss. Parking competitors means selecting no-LOAD/no-I-watchdog records, not silently using the halted generator. Each native quantum read macro must be executed through its real monitored gates and reset gains; the atomic read primitive is not reintroduced.

## Scope retained

The noise is exogenous sparse Poisson CPTP kicks, with retained bath, bounded physical support/incidence and actual separately recorded nominal reset channels. No continuous coherent-noise theorem is imported. Quantum gates are onsite/two-site on fixed-dimensional grouped sites within a laboratory; measured classical transport is separately declared. Output remains locally forest-framed and then ideally decoded. No bare arbitrary-time DATA output, universal computation, or completed native Bell-buffer threshold is certified by this working note.
