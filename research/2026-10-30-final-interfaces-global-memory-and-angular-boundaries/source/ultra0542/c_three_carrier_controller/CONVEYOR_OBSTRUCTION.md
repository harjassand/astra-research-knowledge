# The newest-only reference conveyor is still spent-carrier disposal

This is the first failed controller in this assignment, preserved before
the genuinely reused-P1 attempt. It is a whole causal-family observation,
not a parameter fit. Known memory may be unbounded and need not reset.

Initial physical programmes B1(oldest), B2(newest) may come from ANY
known entangled two-input preparation, independently of the target B0.
In cell t=1,...,m, control ONLY B0 and newest B_(t+1) by their SWAP sectors
and arbitrary known memory isometries; forward the resulting logical
input to obtain B_(t+2); discard oldest B_t. All known references may be
retained and used. The final processor is arbitrary on B0,B_(m+1),
B_(m+2) and all known memory. The literal auxiliary query count is m+2.

Every older carrier is never physically used after the cell in which
it was newest. Its eventual partial trace commutes backwards across
all subsequent memory-only processing and source calls, even when it
is entangled with that memory:

    Tr_B (id_B tensor Phi)(X)=Phi(Tr_B X).

Therefore B_(t+1)'s discard can occur immediately after its last physical
use, for t<m. The first m-1 cells are EXACTLY the accepted spent-carrier
class. Only the final cell can use its additionally retained controlled
programme. Extra holding time is not physical reuse.

The initial B1, which is never controlled, can similarly be traced at
the start. Complete trace preservation of its source call leaves a
KNOWN input/memory state for the one remaining initial programme;
entangled source inputs do not leave hidden U information in known
memory when that physical output is completely traced.

To bound the terminal resource it is enough to consider the native
subfamily U=V tensor I_r, V an unknown qubit unitary in a known physical
embedding. All-A prefixes leave the target untouched, and all older
outputs are completely traced without physical interaction. Iterating
the same complete trace identity removes EVERY earlier source V from
the known memory, leaving ONE current V-query programme prepared on a
known possibly entangled state, followed by the final fresh call.
Normalizing the all-A branch uses only its U-independent probability;
unbounded known memory does not become extra free unitary queries.

The strongest ordinary TWO-query adaptive qubit-unitary inverse bound
is near.7500. Actual primary2109.08202v3 Section6 states its two-query
primal/dual bounds are rigorously certified through four decimals;
2401.10137v3 Table2 displays the sequential qubit n2 entry.7500 and
the corresponding unitary/isometry port. We conservatively import only
the rational upper bound beta=4/5, not a claimed exact.75 equality.
Each N_(V tensor I_r) call is simulated by one V call and known mixed
junk, so this terminal port applies with arbitrary known memory and
final processing. Source texts/precise read windows are bound in the
handoff; no numerical solver value is silently made a proof.

The previous exact first-cross argument applies to the m-1 spent
prefix cells. If p is the all-A survival probability, every first B
prefix erases the reference, the terminal all-A resource has fidelity
at most beta, and all prefix cross insertions contribute at most
sqrt(m-1)/r. Thus on this native subfamily's Haar-V average,

    Fe <=1/4+(beta-1/4)p+sqrt(m-1)/r
       <=4/5+sqrt(m-1)/r.

For any uniform all-U error epsilon<1/5 this implies

    m-1 >=r^2(1/5-epsilon)^2.

This rules out the newest-only conveyor despite all known references
and a strong terminal processor. It does not cover any cell that
physically reuses the old carrier before its discard, the reused-P1
family in PROOF.md, other S3/S4 controls, or a general three-carrier
approximate inverse. The subsequent genuine reuse attempt was analysed
separately rather than presenting this simpler obstruction as its result.
