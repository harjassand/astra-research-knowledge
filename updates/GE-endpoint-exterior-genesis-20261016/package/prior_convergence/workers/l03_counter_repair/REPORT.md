# L03 counter repair: bounded completion, ambiguous history

**Status:** exact finite-patch counterexample plus a conditional existence lemma. This does not establish recursive repair, a scalable fault threshold, or quantum-data recovery.

## Finding

A quarantined patch always has at least one tile-valid completion when the true clean counter state is in the decoder's candidate set and the exterior guard collar is trusted and held fixed. A nearest-completion rule changing at most `k` counters exists for any `k` counter faults: the true state is a candidate at Hamming distance at most `k`, so a minimizer is also at distance at most `k` from the observation. Its counter discrepancy from the true state is therefore supported on at most `2k` sites. This is a finite-support statement; it does not show that every selected tile-valid completion is a reachable controller history or that quantum operations are recovered.

Exact recovery is already ambiguous at `k=2`, even with a fixed 4x4 patch and a fault-free, frozen exterior. On a 6x6 torus with `q=8`, take the all-zero clean state A and state B obtained by one legal even-tile gate at coordinates `(2,2),(2,3),(3,2),(3,3)`. Let the observed counters be one on `(2,2),(2,3)` and zero elsewhere. This observation is two onsite counter faults from either history: two false advances from A or two false rollbacks from B. A and B agree on the entire perimeter of the patch `x,y ∈ {1,2,3,4}`. Exhaustive enumeration of every residue assignment within two edits of the observation, checking every tile on the torus, finds exactly two valid completions: A and B. The quantum data histories differ by the gate channel `K` on that tile. No counter-only decoder with this boundary can determine whether that operation occurred.

For this particular ambiguity, choosing either completion can be charged as at most one missing or spurious tile-gate packet, supported on the tile. This is a gate-debt description only; no inverse of a general CPTP channel is assumed and no quantum data are restored.

## Whole-tile count edits cannot realize the witness repair

Suppose a forward or inverse ghost count edit has the same counter action as a tile gate: it adds `+1` or `-1` modulo `q` to all four counters of one 2x2 tile. Partition sites into the four coordinate-parity classes `(x mod 2,y mod 2)` and let `Σ_ab` be the sum of counters in each class modulo `q`. Every tile contains exactly one site from each class. Therefore every sequence of whole-tile count edits changes `(Σ_00,Σ_01,Σ_10,Σ_11)` by `(m,m,m,m)` for some `m`; pairwise differences are invariant.

For the observed midpoint the class sums are `(1,1,0,0)`. Reaching A requires delta `(q-1,q-1,0,0)` and reaching B requires `(0,0,1,1)`. Neither is diagonal modulo `q` (in particular for `q=8`), so neither completion can be reached by any number of whole-tile forward/inverse count edits, even if intermediate edits may leave the patch. Thus the current atomic gate-count mechanism cannot implement this collective repair. A patch write that changes counters independently could repair the tile-valid surface in at most two writes in this example, but it is a new counter-only primitive and breaks the existing rule that counter progress is inseparable from the quantum gate jump. It must be specified and charged separately.

## Boundary and scope conditions

The existence lemma needs a trusted exterior assignment for all constraints crossing the patch boundary, and the guard collar must be frozen while the completion is computed and installed. In this controller, tile validity alone reads a 2x2 support, while the gate guard can read a 4x4 box; the quarantine must include that full gate-read support. If neighboring counters can advance during repair, the saved boundary is stale and the lemma does not apply. A larger finite patch does not remove the two-history ambiguity: the witness histories agree everywhere outside the single tile, so any patch boundary surrounding it sees identical counters.

The enumerated completions are valid under the local predicates from the modified crossed-plaquette table. The general nearest-completion argument guarantees a local compatible counter assignment only. It does not prove that arbitrary minimizers are clean-reachable, that a selected counter phase can continue without spreading future disagreement, or that protected identity/EC can be maintained while the patch waits. Those are separate gates. The results do not transfer to the original `AsyncR` model.

## Exact artifact

`patch_completion_check.py` exhaustively enumerates all patch assignments within two counter edits of the constructed observation. `PATCH_COMPLETION_RESULTS.json` records the two completions, distances, frozen perimeter, class sums, and the full-tile edit obstruction. Run it from the repository root with:

```sh
python3 research/2026-10-16-convergence-genesis-v1/workers/l03_counter_repair/patch_completion_check.py
```

This uses the same local validity predicate as `s01_controller_repair/TRANSITION_TABLE.md`; it does not modify or import the s01/s06 worker code. The two-fault deadlocks and pair-repair false positives in `s06_controller_adversary/PAIR_REPAIR_RESULTS.json` remain consistent with this result: broadening the repair region supplies compatible completions, but does not identify the intended history or make the existing atomic count edits sufficient.
