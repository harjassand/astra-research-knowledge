# Native observe–delay–commit adapter for a classical Gács rule

2026-10-30. Concrete physical adapter and deterministic clean-cycle implication. A complete strong-trajectory/inclusive-norm theorem is not yet claimed.

## Governing primary contract

Gács 2024, Definition 7.19, permits represented dwell periods between T_low and T_high except local rare events. A transition must use a neighborhood snapshot from the interval (sigma_1, sigma_2 - T_low/2]. Theorem 7.3 realizes this with a finite classical clock that samples before committing. Thus copying and buffering are explicitly classical; no quantum DATA is inserted into Cur, Prev, or sampled neighborhood registers.

## Physical registers and operation

Each classical site x has a visible classical register X_x, a private snapshot S_x, finite mode/timer registers, and the usual native ownership tags. The representation is pi=the visible X_x register. The ideal transition table Tr includes the source's time-marking bit so each represented commit really changes Det.

A cycle is:

1. **OBSERVE.** Arm a one-shot native channel that copies all visible states X_y in the fixed neighborhood of x to S_x. It locks the entire read footprint, uses controlled read-only copies rather than moving the source registers, explicitly pinches the read labels at its terminal, and releases all tags on cleanup. The read-only compiler supplied in READ_ONLY_CLASSICAL_CLOCK_COMPILER.md gives the relevant exact algebra. S_x is a declared persistent payload/output register, not workspace erased by cleanup.
2. **DELAY.** After snapshot cleanup, an onsite timer traverses n stages at fixed rate. Neighbor locks are NOT held during this delay. No visible X changes in this phase.
3. **COMMIT.** When the timer has finished, an actual resolved onsite jump writes Tr(S_x).Det to X_x and writes a fresh fair Rand bit using two equal-rate leaves. This jump is enabled only while x's local resource tag is free, so it cannot overwrite a register held by another site's snapshot. It resets the cycle mode for the next observation. Registers X_x, S_x, its own tag and the commit control are grouped within the finite local site dimension. A finite clear/commit path gives service when readers temporarily hold its tag.

All interactions used for remote classical reads are two-site controlled unitaries. All timer, commit, randomization and cleanup operations are onsite resolved resets. No quantum source data, external clock pulse, instantaneous generator substitution, or multisite jump is required. A continuous perturbation may damage these registers; this construction has not declared them reliable.

## Serializable observation

While the read transaction holds its complete footprint, all relevant visible labels are frozen against nominal writes. Consequently the successful copy has a common neighborhood value at an actual time sigma_read in that interval. Its terminal snapshot is not assembled from unprotected reads at unrelated times. The visible state X_x stays unchanged until the later COMMIT.

Only a copy of classical labels is retained. The raw physical nominal X registers stay diagonal in their declared basis. Under coherent perturbations, a new analysis must use the explicit read pinching and local bad-box accounting rather than postulate a classical stochastic trajectory.

## Timing margins

Choose a finite analysis period T AFTER choosing all physical read/write circuits and their finite service constants. Require:

    observation plus cleanup <= T/16,
    post-observation Erlang timer in [T/2, 3T/4],
    tag-free commit service <= T/16.

Then every good cycle has represented dwell in [T/2, 7T/8], hence in [T/2,T]. Also

    sigma_commit - sigma_read >= T/2 >= T_low/2,
    T_low = T/2.

The common snapshot therefore lies in Definition 7.19's required observation interval. The spare T/8 allows conservative endpoint/cleanup conventions. Use a timer mean, for example, 5T/8 and sufficiently many stages n; its probability of leaving [T/2,3T/4] is exponentially small in n. Its physical jump rate is n/(5T/8), a finite chosen constant. The service exceptions are bounded by new actual finite-path constants C exp(-r T/16). Timer and service choices are all fixed independently of computation size; the subsequent allowable perturbation strength may need to be extremely small.

A commit blocked by a reader is not assumed instantaneous. The existing native clearing-word argument must be rerun for the commit's actual enabled tag-free leaf, including the new local registers and readers. A parked reader has released its tags. A live reader can be cleared in the known finite way. Thus the structural finite-path hypothesis is available, but no numerical old witness coefficient is transplanted.

## Why the source uses two switches after an arbitrary observation time

An arbitrary time a may fall inside a partially completed or previously damaged cycle. Its first subsequent commit can use a stale snapshot. The second commit is based on a fresh observe–delay–commit cycle, provided no new marked defect appears. This is consistent with Definition 7.19's use of sigma_1 and sigma_2, and with the native two-SUCCESS freshness principle. One must not certify the first stale commit from a fresh-service bound alone.

## Remaining proof obligation

Per-cycle nominal tails do not by themselves prove the strong trajectory axioms for systems of disjoint deterministic or stopping-time-selected windows. The actual target statement must charge each failed Definition 7.19 condition to finitely many enlarged local service/timer/noise boxes and verify their joint inclusive norm estimate. In particular:

* all malformed local modes must reach a fresh complete cycle with an all-state instrument bound;
* the local witnesses must remain valid with the actual tag-free commit rule;
* timer outcomes, snapshot pinching, and visible-state noise must be represented in one common nominal CP expansion;
* the Gács deterministic damage witnesses must be applied only after that physical representation is established.

The adapter gives a specific native operation to prove, rather than assuming an already reliable asynchronous control computer. It still does not attach a quantum gate to a repaired classical history or prove active-wire waiting protection.
