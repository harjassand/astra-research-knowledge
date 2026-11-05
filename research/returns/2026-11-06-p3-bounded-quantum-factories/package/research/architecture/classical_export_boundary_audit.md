# Classical-only export: failed boundary and audited repetition-five repair

5 November 2026. This audit concerns the new repetition-code controller, not
the accepted static-tree history-erasure theorem or earlier quantum sources.

## The original fresh-suffix assertion is false

A fresh fault-tolerant descent cannot be declared correct uniformly over
arbitrary incoming correctable gauges merely because every descent extended
rectangle is good. Standard extended-rectangle correctness moves a decoder
relative to the rectangle after its leading EC; a faulty leading EC need not
preserve the previous decoded value when it also meets an incoming error.

Concrete example: a two-level repetition word has level-one children

    a=001, b=000, c=111.

Their decoded values are (0,0,1), so recursive majority is zero. In a's fresh
leading EC, copy its first zero into the first voter buffer; one outgoing
source-wire X fault then flips that source before its other two copies. The
voters see (0,0,1), (1,0,1), (1,0,1), and emit 011. Its decoded value is one;
a clean trailing EC makes it 111. All later gates may be fault-free. The
parent now reads (1,0,1) and emits one although every descent extended
rectangle has at most one physical fault. Thus the original tag misses it.

This does not disprove classical-only export under its full physical fault
model. It invalidates the proposed uniform arbitrary-gauge interface and
shows why the decoder boundary must include the private preparation tail.

## Provisional private-tail proposal: superseded, not an earned theorem

The following was a proposed repair, retained as research history. Its
complete ownership and validity proof was not finished. The final operation
does not rely on it; the audited repetition-five construction below replaces
this route. In particular, this section must not be cited as a sufficient
private-tail theorem.

After protected encoded fanout, give each intended raw output its own final
complete EC and subsequent descent. Include these final ECs in the protected
prefix's logical error budget. Their physical gates and the later descents
are disjoint across output copies. Use fresh leading corrections where
necessary to keep each private region closed under its own extended
rectangles; account for their fixed additional gadget size.

For the top descent k to k-1, mark the output whenever any level-(k-1)
rectangle in its final private EC or its next descent is bad. There are only
a fixed number of such rectangles for this scale. At the next scale, include
the kept output's own final level-(k-1) EC together with the next descent,
and continue. At the bottom, mark ordinary physical faults. These are
private staircase regions rather than a suffix independent of arbitrary
incoming gauges.

The needed deterministic invariant is stronger and appropriate: if the
level-(j-1) rectangles of a level-j final EC are all good, its effective
classical EC is fault-free and its child decoded labels are all the same.
This is an EC validity statement; the common value need not be identified
with the earlier input before a faulty boundary. In the logical-prefix
hybrid, that common value is the intended b. A good next descent preserves
it. The kept output's final EC supplies the same invariant one scale down.

This is why the entire private final EC is included in the tag: lower-scale
gauge errors are generated inside its private region and are no longer
silently treated as arbitrary free incoming errors. Extended-rectangle
truncation is still required when correction gadgets overlap.

If the number of counted level-j rectangles per scale is at most a fixed
g_export, the usual support witness bounds give

    q_export <= g_export sum_j p_j <= 2 g_export p.

The tag regions are disjoint across outputs, so joint tag probabilities have
the needed local-stochastic bound. Tags may correlate with old accessible
records; this is allowed by the accepted tree theorem. What is unnecessary
and false is requiring them to be a fresh suffix independent of every
incoming gauge.

Do not condition the original noise distribution on logical prefix success.
Instead retain a coupled hybrid: on the charged prefix failure event replace
the encoded outputs by canonical codewords for the intended logical bits;
on success keep the actual physical states and gauges. The total cq change
is at most the prefix discrepancy. Keep the original private fault-support
tags in this coupling. Their unconditional joint bounds are unchanged.

## Status of the superseded proposal

The proposal would have required a completed private-tail validity induction,
closed physical ownership of extended rectangles, and an enlarged fixed
g_export. Those requirements are no longer needed by the final route.

## Final audited repair: strict repetition five

The corrected `control/classical_only_export.md` replaces repetition three
by five, performs two successive refresh rounds per EC, and does not share
ECs between adjacent rectangles. A refresh uses five separate voter
workspaces and sequential source-lane copies. One source/copy fault affects
only one lane across voters; an internal voter fault affects only its own
output. With one pre-existing bad lane and one new source fault, at least
three of five inputs remain correct. This is exactly the spare margin
missing from the failed construction.

Two refresh rounds have both required base properties: arbitrary-input
validity with one fault, and correctness with one incoming error plus one
fault. The corrected induction includes input-selective normalization and
common-value CNOT copying. Thus the first good copy of an invalid source
chooses one valid value and supplies that same value to its target; future
copies preserve it. It does not assume an ideal decoded value for invalid
data. This property makes all voters see one consistent coarse input word.

The hierarchical invariant is deliberately strict: at least four of five
children are regular of the intended value, with only one arbitrary child.
It is stronger than merely having the desired recursive-majority answer.
The simultaneous induction on validity, regular-input correctness, and
common-value copying is sound under the stated fixed lane/voter routing
incidence. Unshared lower rectangles have disjoint physical fault supports,
so a bad upper rectangle requires two bad lower rectangles and the stated
quadratic recursion follows.

## Direct physical decoder avoids the earlier boundary problem

Every protected copy is consumed by its own fresh physical majority-five
tree. A tag depends only on fresh faults: tag a parent for a faulty voter
or at least two tagged/faulty-edge children, using all five children rather
than consulting which old child is exceptional. Therefore

    q_(h+1) <= v + 10(q_h+e)^2,  q_0=0.

For s=max(v,e)<=1/200, q_h<=2s is invariant because s+90s²<=2s.
An untagged node of a strict regular subtree has at least three correct
received bits: at most one old exceptional child and at most one fresh
tag/edge fault are excluded. Its clean majority returns the intended bit.
This proof is uniform over all admitted strict gauges and old records.
Disjoint fresh decoder trees give the required LS pool. The prefix failure
is added by coupling, without conditioning the suffix noise law.

This direct physical tree uses ordinary noisy gates and growing classical
resources. It inserts neither an ideal decoder nor a growing quantum code.

## Independent review of the local exhaustive receipt

`control/verify_classical_ec.py` correctly checks all 32 input words, both
refreshes, sequential row copies into five private voter columns, and every
nonempty outgoing-wire flip subset at each abstract reset, copy and voter
operation. Its 16,352 arbitrary-input validity cases and 6,132
one-incoming-error-plus-one-fault cases match the program's enumeration.
The source-wire pivot case that broke repetition three is explicitly
covered by the copy-gate output subsets.

Abstracting a voter by its truth table plus arbitrary private output flips
is adequate here: all of its internal gates and buffers are private, so
one internal fault can change only that voter's returned bit. The native
MAJ5 formula is independently checked on all 32 inputs. Idle faults commute
to the preceding wire-use fault representative; an initial source idle
adds at most a second bad lane, which clean majority-five corrects. No
additional large test suite is needed for this deterministic base claim.

The final repair passes this audit. Its fixed classical threshold still
depends on the complete finite gadget/routing count, and the positive
quantum-fabric rate alone does not establish that classical threshold.
