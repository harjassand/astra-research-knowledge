# L03 follow-up: exact B(P), distance-four, and two-repair interleavings

**Finding.** The bounded checks below support the candidate's small-pattern behavior on the stated surfaces. They do not establish an arbitrary clean-state theorem, an asymptotic fault threshold, or recovery of quantum data. A trusted, frozen exterior is essential for any patch-completion claim, and the existing tile-gate count actions cannot enact the counter-only repairs in the ambiguity witness.

## Exhaustive L4 two-fault check

For `q=8`, the exact scan covers every clean state reachable from zero on `L=4` with maximum counter height at most 3 (46 states), every distinct pair of faulty sites, and each of the 49 choices of non-original residues. This is 270,480 observed states. For each state it checks singleton counter repairs; if no correct singleton exists, it checks the invalid tile containing both faults and enumerates all one- or two-counter `B(P)` writes whose full distance-two tile-overlap moat is valid.

| Outcome | Count |
|---|---:|
| Correct singleton available | 190,992 |
| No correct singleton, so B(P) checked | 79,488 |
| False singleton | 0 |
| No correct singleton and no common enabled B(P) | 0 |
| B(P) outputs checked | 80,688 |
| Invalid B(P) output | 0 |
| Valid B(P) output not equal to the clean assignment or one-tile forward/inverse gate debt | 0 |
| States with multiple B(P) outputs at a common tile | 1,200 |

Thus every scanned two-fault state had either a correct singleton repair or at least one enabled common-tile `B(P)`. The scan also finds nondeterministic B outputs in 1,200 states, so this is an existence result for the enumerated cases, not a unique decoder. The output classification compares the final counter surface with its generating clean history. A B write itself edits counters independently; it does not apply the quantum gate `K`.

The completed-run receipt is [L4_TWO_FAULT_RESULTS.json](L4_TWO_FAULT_RESULTS.json). Reproduce the scan with:

```sh
python3 research/2026-10-16-convergence-genesis-v1/workers/l03_counter_repair/replay_l4_two_fault.py
```

## Connected supports through four sites

For each listed clean history, every connected changed-site support of size 1–4 and all `q=8` substitutions were checked against every tile predicate. “Non-gate alternatives” are valid counter assignments not equal to one whole-tile forward or inverse count jump from the supplied clean state.

| L | Clean history | Supports checked | Substitutions checked | Valid alternatives | Non-gate alternatives |
|---:|---|---:|---:|---:|---:|
| 4 | zero | 860 | 1,551,452 | 8 | 0 |
| 4 | reachable max-spread state, heights 2–3 | 860 | 1,551,452 | 4 | 0 |
| 6 | zero | 2,124 | 3,944,556 | 18 | 0 |
| 6 | all even tiles fired once | 2,124 | 3,944,556 | 18 | 0 |
| 6 | uniform height 9, after counter wrap | 2,124 | 3,944,556 | 18 | 0 |
| 6 | greedy high-gradient history, heights 32–34 | 2,124 | 3,944,556 | 6 | 0 |

Within these supplied surfaces, every connected valid alternative supported on at most four changed counters was a whole-tile gate-count debt. For a support of at most four sites that is disconnected in the graph joining sites that share a tile, the affected-tile constraints factor across its components. Each component is itself a connected alternative of size at most four; the enumerations therefore rule out an additional disconnected alternative in these same supplied states. This is a finite statement about the listed counter surfaces only.

The script and full matrices/results are in [run_distance4_selected.py](run_distance4_selected.py) and [DISTANCE4_SELECTED_RESULTS.json](DISTANCE4_SELECTED_RESULTS.json). Replay with:

```sh
python3 research/2026-10-16-convergence-genesis-v1/workers/l03_counter_repair/run_distance4_selected.py
```

## Two simultaneous B(P) repairs

On an `L=8`, all-zero `q=8` clean surface, I placed two `0→1` counter faults inside each of two distinct even tiles. The check exhausts all 4,320 choices of tile pair and two-site supports. In 2,016 states both B triggers were initially enabled. For each such state it enumerates every first B output, recomputes the second guard and its options, then checks both orders, `P` then `Q` and `Q` then `P`.

All 2,016 states remained repairable in either order; neither second guard was disabled in any branch. Each second trigger still had two options. The check covered 8,064 final branches per order (16,128 total); every final counter surface was globally tile-valid and was the zero state or a union of zero, one, or two forward even-tile gate-count debts. This gives exact interleaving safety for this specific all-zero, same-parity, `0→1` two-cluster family. It does not cover arbitrary residues, odd tiles, nonuniform clean histories, three or more repairs, or unbounded schedules.

The replay script and result are [interleaving_check.py](interleaving_check.py) and [INTERLEAVING_RESULTS.json](INTERLEAVING_RESULTS.json). Run:

```sh
python3 research/2026-10-16-convergence-genesis-v1/workers/l03_counter_repair/interleaving_check.py
```

## Consequences and limits

The exact trusted-collar ambiguity and parity-class edit invariant remain decisive. In the `L=6` witness in [REPORT.md](REPORT.md), the observed midpoint is two counter faults from both the zero history and a history after one legal tile gate. They agree on the fixed 4×4 patch boundary, and exhaustive completion enumeration gives exactly those two valid assignments within two counter edits. Each completion requires two individual counter writes from the midpoint. No sequence of whole-tile `+1/-1` count edits reaches either completion: every such edit shifts all four coordinate-parity class sums equally, while the required midpoint deltas are unequal across classes. Thus a repair that selects either assignment needs an additional counter-only mechanism; it is a ghost counter repair unless the controller explicitly adds and accounts for that mechanism. It does not rewind or reapply `K`, and it does not recover the quantum state.

The general nearest-completion existence argument needs the true clean assignment to remain among the candidates and all boundary values used by crossing tile constraints to be trusted and frozen while the patch is solved and installed. The quarantine must contain the full controller read support, including the 4×4 gate-guard support. The boundary cannot resolve the two-history ambiguity, because the histories differ only by the interior tile operation and agree outside it. No result here proves that a selected completion is reachable, that repairs compose safely beyond the enumerated family, or that counter validity protects quantum data while a patch is quarantined. These checks apply only to the modified crossed-plaquette rule, not the original `AsyncR` model.
