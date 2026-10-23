# Cost and error accounting

This checkpoint uses Python3.12.14 on the supplied Linux x86_64 CPU runtime.
The new executable source requires only the Python standard library. It uses
exact Fraction arithmetic, integer tents, graph traversal and rational linear
algebra. No GPU, install, paid compute, eigensolver, numerical optimization or
precision sweep was used.

## Distinct observed computation

| Activity | Body wall seconds | Body CPU seconds | Peak RSS bytes |
|---|---:|---:|---:|
| Seven exact witness constructions, including n4012 | 1.716356064 | 1.716238879 | 30,760,960 |
| Independent verification of all seven, plus four tamper checks | 1.530646674 | 1.530533601 | 31,256,576 |
| Root direct decoder exact fixtures | 0.002169369 | 0.002167276 | 12,058,624 |
| Local-color obstruction supporting check | 0.041286724 | 0.041286433 | 9,699,328 |
| Initial palette check, later strengthened | 0.003677298 | 0.003659517 | 9,306,112 |
| Strengthened palette check | 0.004164432 | 0.004132510 | 9,437,184 |
| Independent decoder-constant examples | 0.000159976 | 0.000156734 | 9,043,968 |
| **Distinct body subtotal** | **3.298460537** | **3.298174950** | **31,256,576 maximum** |

Stage/per-case timers are contained in these bodies and are not added again.
In particular, the n4012 witness construction1.670694673s and receiving check
1.481536362s are subsets of the first two rows. Imports/process creation,
source reading, execution-service latency and authoring are excluded from
these body timers. Parallel elapsed time is not their sum.

Machine-readable records are `results/cost_ledger.json`, the individual
`results/*.json`, and `witnesses/PRODUCER_RECEIPT.json`. An isolated package
replay, ZIP construction and private delivery have separate receipts. They
are not additional discoveries or silently included in this subtotal.

## Failed approaches and other observed work

The first analytical candidate compressed an arbitrary star-color palette
using simplex vectors. A replicated-star counterexample killed its premise;
the stronger all-palette version is preserved. The second candidate used
local palette omission to allow rowwise unmixing. The classical41-vertex graph
proves this repair cannot cover treewidth two. Both are scientific failures
that determine the next choice; neither involved a hidden parameter sweep.

The initial palette check was rerun once to strengthen its exact local-frame
Gram verification. Both times are charged above. The main witness producer
ran once, and the separate receiving checker ran once. There were no failed
new numerical runs. The supplied incoming q3 diagnostic scripts and original
NIST calculations were not replayed.

Scoped literature work used13 calls totaling41.9s reported access latency;
the local-color contributor used3 calls totaling6.7s; the palette contributor
used one primary read taking3.3s. These **51.9 seconds** of observed contributor
source-access latency exclude root's additional primary reads and all reading,
interpretation and authoring. Failed direct PDF retrievals and one irrelevant
arXiv identifier opened and discarded are preserved in `notes/literature.md`.
They support no scientific conclusion. Root's source extraction/hash equality
check is recorded in the incoming SOURCE_RECEIPT, about0.120763990s measured
scope. Those provenance costs are separate from scientific calculation.

Proof development, mathematical challenge, source interpretation, model
inference, token price, service overhead, monetary cost and energy are not
fully exposed or metered. They are **unknown additional costs**, not zero.
The elapsed investigation is not equated to the sum of small program timers.

## Actual operation costs

The positive algorithm is given a known graph G and a proposed separator S.
It validates that G-S is a forest and constructs its root/depth coloring.
The abstract traversal and sparse decoding take O(n+e) work/storage, e=|E(G)|.
The supplied Python implementation also canonicalizes with sorting, costing
O(e log(e+1)+s log(s+1)) in addition to traversal; it does not claim a linear
implementation of those sorts. Constructing a dense seed or retaining a dense
measured action block costs O(n(s+3)) storage/time, and reading/transferring it
must be counted when required by the action interface.

The query bill is **s+3 actual actions**, regardless of how inexpensive the
local decoder is. Sparse input action simulation in the fixture source is
ordinary explicit arithmetic, not a free physical or computational oracle.
Finding a small or minimum feedback vertex set is outside the supplied-input
contract. There is no uncharged separator optimization. A later spectrum or
CDF computation has its own cost and is not delivered by this decoder.

The lower witness operation is O(m) rational arithmetic/storage for fixed s,
with polynomial dependence on s in the straightforward implementation.
Rational numerator/denominator growth is not a unit-cost bit guarantee. The
independent checker pays for every action entry and all input binding; a
floating solver status is never the acceptance condition.

## Error boundary

Every supplied fixture input is an exact rational matrix. Each row energy is
checked exactly, all support entries are explicit, and actions are evaluated
by exact arithmetic. No coefficient rounding is introduced and no separately
rounded operator is silently substituted. The rational tent bound is distinct
from the stronger analytic sine-mode bound.

The positive theorem allows arbitrary action error E, including correlation
and components that are not themselves an action of a supported matrix.
The seed entries0,1 are exactly representable. Finite-arithmetic rounding in
averaging separator-edge reads needs a separately certified output allowance;
PROOF.md gives a Frobenius sum-of-radii bound. Supported operator input error
tau adds directly; unsupported input error may cost as much as C*tau*sqrt(n)
under only an operator-norm bound. Approximate support is not covered for free.

## Preserved historical costs and stop boundaries

The incoming squared-path and fan trial arms took654s and744s elapsed,
respectively. The fan arm's24s administrative overrun is preserved, not erased.
Their numerical bodies, blind review, and relocated producer replays remain
in the copied incoming records and are not charged as new discoveries here.
Owner acceptance was a reading/proof-assessment operation, not another replay.

The unchanged prior owner ZIP includes every original input, failed route and
receipt. The NIST dense proposal plus verification1.675848413s before shared
conversion and width9/1074 remains the practical incumbent. The prior common
completion producer39.019276241s and its independent replay remain a cost
defeat for that stored-input task. These outputs and families differ from the
new structural theorem, so their times and widths are not a matched speedup
comparison. The closed molecular family and its fixed-family floor remain
closed; no new task in that programme was undertaken.

## Delivery accounting

The immutable archive is saved privately and transported through the same
agent-readable Page. Ordered base64 text chunks remain below700000 characters,
with per-part SHA256/length, archive SHA256 and a strict reconstruction script.
The new archive's delivery receipt records actual upload/readback results and
post-archive costs, avoiding a self-referential ZIP digest. Upload and readback
do not imply independent receiver reconstruction or scientific integration.

## Completed receiving preparation

One isolated delivery replay passed all five new check programs from a different
working directory. Its wrapper took1.693582829s, child CPU1.672239s, with maximum
child peak RSS31,391,744 bytes. Individual process times overlap this wrapper
and are not added again. It did not regenerate witnesses or replay historical
science. The receipt is delivery_receipts/portability.json.

One multi-file source edit was rejected before changing files because the patch
attempted delete-and-add on the same path. The unchanged state was inspected,
and a corrected update succeeded. Its reported0.5s tool latency is separate
from numerical costs; the failure changed no theorem or witness.
