# Retained-trajectory context acquisition: cost and interface gate

2026-10-24. Bounded audit of `../RETAINED_CONTEXT_ACQUISITION.md`, using its
literal root refinement. No external source or physical platform was checked.

## What the refinement removes, and what it still supplies

The protocol genuinely removes a full-system initializer from the acquisition
loop: it follows one existing field, exposes only noisy site-labeled reads,
uses a deterministic public control schedule, records first visits to local
context/mode rows, and stops at a finite cap with `UNKNOWN` on incomplete
coverage. It no longer needs a context sampler, a reset, or a hidden random
controller word. It still assumes the native local bits are a sufficient
Markov state, the physical graph/range and target support are known, and the
site/mode response law is complete. Those promises remain physical structure;
the read stream does not prove that no omitted local memory exists.

The honest clock/read interface requires a global hold (or an equivalent
verified local hold for every cell in `C`) while each repeated pre-read is
taken. The hold has positive latency and cost and must prevent uncontrolled
cell evolution during the read sequence. Each pulse needs a defined
pre-read/parallel-update/post-read boundary and site-addressable modes. A
finite neighborhood cannot be assembled from serial reads if the field
continues evolving between them. A persistent hidden cell, asynchronous
background dynamics during hold, or a shared bath variable that affects
several updates breaks the supplied Markov/product-kernel contract.

No context index is given to the learner: it computes the bit string from
actual repeated reads. The data source must not separately return an exact
configuration label, mode response table, or hidden transition-noise draw.
The schedule itself is deterministic and public, so it creates no random
controller key and requires no selector-key erasure. The calibration records
and any data-dependent stopping time are still information: either keep them
as explicit shared calibration information or pad acquisition to `T_max` if
constant public duration is required. Padding costs its extra reads/holds and
updates. This timing issue does not create a reset key, but it must not be
silently omitted from the acquisition transcript.

## Probability and coverage audit

For a fixed bit, the conditional read-error bound `e_s<1/2` for every history
is enough for the Hoeffding-Azuma majority tail, even with dependent errors;
the field must actually remain fixed during those reads. A mere marginal
error bound would not suffice. With at most
`T_max (|C|+|B|)` majority decisions, the first term of (1) is a valid union
bound. On the event all majority decisions are correct, each first visit to a
row `(i,a,z)` is selected before its fresh update noise. The Bernoulli
martingale concentration for the first `m` visits is then valid without
conditioning on eventual completion. The note correctly charges incomplete
coverage as `UNKNOWN` and does not divide the error guarantee by a presumed
success probability.

This is an unconditional failure-and-return guarantee, not a uniform
finite-time acquisition guarantee. With no lower bound on the chance of
visiting each context/mode row, `T_max` may be exceeded with probability one;
the rare-context cost is not bounded by graph degree or finite row count.
Using the same explored trajectory across multiple rounds is legitimate under
the fresh conditional Markov update law, but cannot manufacture a context
that the public schedule never reaches. The fixed schedule must enumerate
every required mode at every trained site; merely alternating two global
modes is sufficient only when those are the full control set. Context row
identification still comes from the pre-read, not a supplied context oracle.

There is an acquisition-side record caveat: “stop when all rows are full” has
a data-dependent completion time. If time is observable, it can reveal
information about row visitation even if raw reads are later discarded. This
does not undermine the downstream all-history contraction proof when the
learned table/mode choice is treated as fixed shared calibration, but it is a
real output of acquisition and belongs in the record contract. Fixed-time
padding removes that timing output at added cost.

## Explicit ledger and geometry

At the stated cap, the acquisition ledger includes at least

    T_max synchronous rounds,
    T_max (|C|+|B|) r raw sensor reads,
    the corresponding clock-hold latency/energy,
    every actual site-update pulse and its switching energy,
    O(M log(m+1)) bits of row counts plus context/control metadata,
    majority, row-index, interval, mode-selection and validation computation,

where `M=|B||U|2^d` is the full required table size. If sensors operate in
parallel, raw-read count is still paid even when wall time is only `r` read
slots; if they are serial, hold time scales with `r(|C|+|B|)`. The apparatus
must specify which case. Likewise, `T_max|C|` update events is the correct
count only if the pulse can update just `C` while holding the rest. If a native
clock pulse updates the entire system, charge all updated cells (or report the
physical system-size cost). Guard preparation later costs `k|B|` native
updates only under site-selective operation; an all-system pulse costs the
whole active system per round. Future task sensors on `A` are paid task costs,
not hidden acquisition or reset-free measurements.

The root refinement's volume warning is material. On a bounded-degree graph
of degree `Delta`, a radius-`R` ball can have size exponential in `R` (tree
growth). For a fixed-dimensional lattice it is polynomial, `O(R^D)`. The
finite-cone bound requires, for target error `epsilon`, approximately

    k >= log(2|F|/epsilon)/(-log q),
    R >= rH - 1 + log(2|F|/epsilon)/(-log q).

Thus bounded degree alone does not imply polynomial total acquisition or
preparation cost in horizon/accuracy. Any such cost claim additionally needs
polynomial volume growth (or a specified smaller geometry), and the concrete
per-site control/read/clock cost. The mathematical TV certificate remains
valid at any finite volume where the acquisition succeeds.

## Matched controls and remaining value

The strongest ordinary comparator retains the exact same read stream, row
counts and confidence allocation, then fits the same local tables and selects
the same minimum-row-sum Dobrushin modes. It ties the operation and certificate;
there is no algorithmic advantage from calling the result an acquired
procedure. A full-initialization comparator can bypass the guard only if it
has a separately supplied capability to initialize the same target directly;
otherwise compare against initializing the same reference and applying the
same deterministic guard. Acquisition is initializer-free, but calibration
still consumes the long-lived native trajectory, sensing and update resources
above. Its advantage is specifically reduced dependence on external starts,
conditional on row coverage and the supplied local physical structure.

Verdict: the retained-trajectory change is a real removal of a costly
initialization resource, not a context-oracle substitution. Its key unsupplied
gates are reachable row coverage, synchronized hold/read/update hardware,
site-selective update accounting, and native-variable completeness. Keep
missing contexts as `UNKNOWN`, the learner's same-data tie as the live
algorithmic control, and geometry/volume costs explicit.
