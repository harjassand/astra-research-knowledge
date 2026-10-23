# Critical check of the parameterized action separation

Focused analytic addendum, `/root/cycle8_port_lemma`, Cycle9, 22 October 2026.
The principal owner proposed and authors the general theorem and operation.
This review checks its lower bounds and the extension of the parity proof;
no numerical work is performed here.

## 1. Correct intrinsic scope

Fix an integer p>=2. Consider connected graphs with at least one block,
every block K_{p,k_B} for an integer k_B>=p+1. Require all cut vertices to be
in the k_B-side (the middle side) and to belong to exactly two blocks. Hubs
are the p vertices of within-block degree k_B, middles have within-block
degree p. The inequality k_B>=p+1 makes that distinction intrinsic. Suppressing
the degree-two cut nodes again gives a tree of blocks.

A decomposition with bags consisting of all p hubs and one middle has width
p. Joining block decompositions through shared middles preserves width at
most p. The graphs remain triangle-free for every p. However, when p>=3
they are generally **not chordless**: K3,3 supplies a six-cycle with chords.
Only the p=2 case recovers the chordless atom setting. That is a substantive
extension of the graph class and must be stated, not silently carried over.

## 2. Positive operation and control

Give the p hubs of each block distinct common labels 0,...,p-1. Color middle
vertices by p or p+1 according to the same outgoing block-depth parity rule
used in PARITY_AND_CUT_REVIEW.md. For a fixed hub label h and one middle
label, the induced component has exactly the same spider description: a
parent hub, its middle neighbors, and at most one child h-hub beyond each
shared middle. The other p-1 hub labels are absent from this pair. Thus every
arm still has at most two edges, independently of p, k_B and block-tree depth.

The already proved component Poincare inequality and orthogonal action-cell
argument give p+2 unit-coordinate actions with

    ||error||op <= ||error||F <= sqrt(3+sqrt5) ||E||F.

A stronger-conditioning star control uses 2p+1 actions. Color all middles
2p. Give even-depth hubs labels 0,...,p-1 and odd-depth hubs labels p,...,2p-1.
Each shared middle has 2p pairwise different neighbor colors. For any fixed
hub label, it belongs to at most one incident block. Every two-color
component is therefore a star, and the inherited triangle-free LS bounds
are operator sqrt(3/2), Frobenius sqrt2. Both schemes use actual whole-row
norm one and all original actions. The action/conditioning comparison is
valid for every graph in the class, not only the obstruction below.

## 3. Star-color lower on a bounded-degree hard subfamily

Take a central block K_{p,2p} and attach p further K_{p,2p} blocks, one at
each of p distinct central middles. Each identification uses a middle in
the attached block. No other vertices are shared. The resulting graph has

    number_of_blocks = p+1,
    n = 3p(p+1)-p = 3p^2+2p,
    m = 2p^2(p+1),
    maximum_degree = 2p,
    treewidth <= p.

Assume a star coloring with at most 2p colors. Within any K_{p,2p} block,
if two hubs share a color, no two middles can share a color: otherwise those
four vertices form a bichromatic C4 and hence contain a bichromatic P4.
The 2p middles would then use 2p distinct colors, all disjoint from at least
one hub color, impossible with 2p colors. Therefore all p hubs are rainbow.

Each middle has the p distinct hub colors as its neighbor support N. If
its own color occurs at another middle, each hub has that other neighbor
of the same color, so F=N. If its color is unique among the middles, F is
empty. These are the only possibilities for its root hazard.

At a shared middle, both incident block supports have size p and avoid the
shared root's color. They lie inside at most 2p-1 remaining colors, so their
intersection is nonempty. If either root color repeats in its block, F=N
on that side and the exact gluing condition fails. Thus a shared middle
must have a unique middle color in **both** incident blocks.

The central block would therefore need p specified middles each with a
unique color. Its p rainbow hub colors leave at most p colors for all 2p
middles. At most p-1 middle colors can occur exactly once: if p were unique,
those p colors would each be used once and no color would remain for the
other p middle vertices. Contradiction.

So the graph has no star coloring with 2p colors. The construction in
Section 2 gives one with 2p+1 colors, proving star chromatic number exactly
2p+1 on this explicit bounded-degree graph. For p=2 it is precisely the
sixteen-vertex, three-K2,4 obstruction. The argument does not rely on one
chosen palette, local template, numerical solver or arbitrary prescribed
boundary colors.

## 4. Uniform coordinate lower at p+1 queries

Take a path of b=2m blocks, all K_{p,2p}. Any exact unit-coordinate design
with p+1 colors must be proper and acyclic; the respective equal-color-edge
and alternating-cycle kernels prove those necessities with a free diagonal.

If two hubs in one block shared a color, acyclicity would force all 2p
middles to have distinct colors, again requiring at least 2p+1 colors.
This exceeds p+1. Hence the p hubs use p distinct colors and all middles
use the one remaining color. Shared middles propagate this common middle
color along the entire block path. Every other color labels exactly one
hub per block.

Fix one such hub color. Its component with the middle color is a tree with

    N = (2p)b+1 = 4pm+1

vertices. Deleting the edge from the m-th hub to the next shared middle
splits it into a=2pm and b'=2pm+1 vertices. The inherited exact cut witness
therefore gives

    rho^2 >= Gamma_{p,m}
           = 2pm(2pm+1)/(4pm+1),

which diverges as m grows for each fixed p. Coefficients outside this one
bichromatic component are zero, so the witness uses the full original
matrix/action space without an omitted-action assumption.

For row-scaled signed coordinate probes X=W C with |w_v|<=1, a zero weight
already loses its free diagonal. Otherwise let alpha=min|w_v|. The diagonal
witness gives rho>=alpha^-1; congruence-transforming the cut witness gives
rho>=alpha sqrt(Gamma_{p,m}). Hence

    rho >= Gamma_{p,m}^{1/4}.

The proof and exact noise convention are the same as Section 6 of
PARITY_AND_CUT_REVIEW.md. Thus p+2 is the minimum uniformly stable coordinate
query count on this family, including signed/unequal row amplitudes. It is
not a lower for arbitrary real dense designs. The p+1 coordinate design
still gives exact identification on each finite graph; uniform conditioning
is what fails.

## 5. Consequence and remaining limits

The same intrinsic class separates the stronger star requirement from the
actual stable-coordinate objective:

    uniform stable coordinate count = p+2,
    worst-case star-color count       = 2p+1.

The hard star example and the diverging p+1 chain both lie in the bounded-
degree subfamily with all k_B=2p. The positive p+2 and 2p+1 operations also
cover unbounded k_B under the stated incidence restriction. This is a genuine
parameterized action separation, not just a larger fixture of the p=2 rule.
It does not imply superiority in overall cost: the 2p+1 construction has
the stronger noise constant, and acquisition and numerical costs remain paid.

No historical originality, external acceptance or arbitrary-real query
optimality is asserted. Native recognition, exact reconstructed actions,
implementation complexity and independent receiving checks remain separately
owned verification obligations. No search or numerical experiment was run
for this review, and total inference/authoring cost is unknown.
