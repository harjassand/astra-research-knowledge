# A genuinely reused-programme controller, and its discriminating question

30 October 2026. C. Previous ROOT28/ROOT29 files remain frozen.

The native source is N_U(X)=U(X tensor I_r/r)U*, logical qubit, unknown
isometric U, fresh memoryless junk. Persistent physical registers are
P0 (target), P1 and P2; the known retained controller memory is one qubit M.
Initially prepare two ordinary programme calls on known logical inputs
(for example0 and+) and M=+. No programme flag or source inverse exists.

One uniform cell is, in chronological order:

1. Known controlled-SWAP01, controlled by the old known M.
2. The canonical known Pauli isometry V(a,b):M -> A3,M',R,
   with a^2+3b^2=1. It is the exact ROOT28 memory port, not a filter.
3. One ORDINARY forward N_U call on A3, producing physical P3.
4. Controlled-SWAP01 by M' (post-echo), controlled-SWAP13 by R
   (interaction with the NEW physical source output), then
   controlled-SWAP12 by M' (stored physical transfer).
5. Known H on M'; discard P3 and R; retain P0,P1,P2,M'.

P1 is physically used both before and after the source call. P3 is
physically used before it is discarded. Thus neither the newest-only
holding-time commutation nor the previous two-carrier disposal bound
settles this cell. Its exact all-r recurrence is in the preceding
permutation-memory interface; a new-wire discard is just the same cycle
trace with d=3, or a known final wire exchange/relabel if that old API's
d=1 convention is used.

In source-port order(M',A3,R), the nonzero amplitudes, given old M=c,
are

    (m=c, A=c,   R=c):      2b/sqrt2,
    (m=c, A=1-c, R=1-c): (a+b)/sqrt2,
    (m=1-c,A=1-c,R=c):   (b-a)/sqrt2.

After the final H, the amplitude for new M=j is the corresponding raw
coefficient times (-1)^(m j)/2. The physical wire permutation of that
path is

    g = (12)^m (13)^R (01)^(m+c).

This completely specifies the known staged circuit, its relative phases
and the source input. We select ONE exact nontrivial port, a=11/14,
b=5/14, inherited as a known rational isometry from ROOT28. No parameter
scan is planned. The all-order question is whether this actual recurrent
controller retains the original logical data long enough to use rare
matching junk. It is not a Q=3 decoder fit.

At a=b=+/-1/2 the input A3 is an independent Bell half; at a=-b it is
also an independent Bell half after exchanging the known ports. Those
cases reduce to preacquired programmes and do not escape the ordinary
whole-programme barrier. For a!=+/-b the source can have a genuinely
payload-correlated input. Fixed-parameter conclusions must NOT be
extrapolated to r-dependent tuning toward the independent-query points.

The proposed discriminator is a causal DISTINCT-LIVE-TAG process. Before
any live-tag collision, every original logical qubit stays attached to
its own junk tag; known physical permutations only move the tagged
carriers. Sorting tag identities for analysis factors out the original
logical input. It is untouched until its carrier is discarded. Source
logical data can be traced in this reduced position/controller process
because future controls do not act on it before a collision.

Only six arrangements of the three distinct live tags and M are needed:
a12-dimensional quantum walk, not a classical sector approximation.
Append one fresh distinct tag, apply the staged circuit, and trace the
discarded tag. Distinct discarded labels are different Kraus outcomes;
retain all position coherences compatible with the SAME discarded label.
Relabel the two surviving nontarget tags canonically. If the target tag
is discarded, that is absorption. The exact Kraus and a positive
Lyapunov/lifetime certificate, if they exist, will decide this family.

A finite lifetime at fixed(a,b) can bound the probability of any live-tag
collision BEFORE data loss by3 E(lifetime)/r, plus initial collisions.
That would be a uniform-ALL-horizons failure, with an explicit parameter
bill, not an unqualified stationary state or a finite-order generator.
It would not prohibit an r-dependent long-lived controller or a different
echo that retains a useful protected mode.
