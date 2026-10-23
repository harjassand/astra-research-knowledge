# Independent challenge: one-root stars can compose into bounded spiders

Scope: Cycle10 Pro2 root's proposed replacement for the theta-only interface.
This review reads the exact Cycle9 PROOF.md (Sections 2.2–2.3 and 4–5),
CONTINUATION.txt and FAILED_APPROACHES.md. It does not rerun the completed
atom closure, the 66-case projection, or an old receiving calculation.

## Verdict

The proposed all-depth gluing argument is valid under the hypotheses below.
The root's distinction between one-root realizability and simultaneous
independent roots is preserved: each new block receives only ONE prescribed
root and ONE requested permutation of its actual rooted coloring. Its other
cut vertices keep the colors and profiles produced by that coloring. The
extra control at one outgoing site is imposed on that site's CHILD block,
not by recoloring the present block.

This is an independent internal argument check, not historical-priority or
external-acceptance evidence. The native construction and its original-action
receiver are the root's separate obligations.

## 1. Exact abstract hypotheses

Let the graph be assembled along a tree of edge-disjoint nontrivial blocks.
Each shared vertex belongs to exactly two blocks and has degree two within
each. Distinct block adjacencies use distinct shared vertices. Every block
admits a star coloring with colors {0,1,2,3}. Furthermore, at any ACTUALLY
specified shared vertex r, its block has a realizable star-four coloring
with the following one-root guarantee:

1. Its two neighbors have distinct colors, so |N(r)|=2.
2. At most one color lies in F(r), where a neighbor color b belongs to F(r)
   iff the b-colored neighbor has a further neighbor of color color(r).

The coloring may be permuted globally within that one block. There is no
assumption that two root guarantees can be realized simultaneously in a
block, or that neighbor colors can be independently chosen at all marks.

The root block only needs an unrooted star-four coloring. Choose it once.
Every nonroot block will be colored once using its one actual parent cut.

## 2. Local admission with an optional forbidden channel

Suppose the already colored parent block has cut r of color a and neighbor
support P, a nonempty subset of the other three colors with |P|<=2. The
child is optionally required to avoid one color f in P at its root.

If |P|=1, send the child's two distinct root-neighbor colors to the two
colors outside P and {a}. Then the parent and child have no common channel.
The optional forbidden channel is automatically avoided.

If |P|=2, let c be the sole other color outside P and {a}. Choose
b in P, with b!=f if f was specified. Send the child's two root-neighbor
colors to b,c, and send its possible flagged color to c. Such a permutation
fixing the root exists because the child has distinct root-neighbor colors
and at most one flag. The intersection with P is exactly {b}, and b is
unflagged. The optional forbidden channel is absent from the child support.

Thus every admitted parent profile and every one-channel request has a
realizable extension. This is not an arbitrary-boundary assertion; the
child chooses from its actual rooted coloring by a single permutation.

### Meaning of an unflagged common channel

In the child, the root has exactly one b-neighbor u. The other root neighbor
has color c outside the pair {a,b}. Since b is unflagged, u has no other
a-neighbor. Consequently the child's entire component in pair {a,b} is
the isolated edge r-u. This uses actual flags, not merely a bound on their
cardinality detached from the neighbor support.

## 3. The one-message invariant

Each nonroot block shares at most one neighbor color with its parent at the
root. If there is one, the preceding paragraph identifies the exact edge
r-u through which that inherited pair enters the block. If u is another
cut vertex, request that the child block attached at u avoid color(r).
That is a valid optional forbidden channel: r is a neighbor of u in the
current block, so color(r) is in the current N(u).

There is at most one such outgoing request in a block, because there is at
most one inherited pair and that pair is exactly one edge. Other outgoing
children receive no forbidden-channel request. At u the next child is
colored by Section 2, which always admits this request. If u is not a cut,
the inherited pair already stops. A degree-three/four vertex inside a block
cannot be a cut of the stated class; no nonexistent child is assumed there.

This proves by induction on the block tree that all choices exist at every
depth. Multiple outgoing cuts do not demand multiple root profiles from the
current block. They demand separate one-root colorings from separate actual
child blocks, with distinct vertices already fixed by the parent.

## 4. Global two-color component proof

Fix an unordered pair {a,b} and a nontrivial component T of the final graph
induced by that pair. Let B be the shallowest block containing an edge of T.
The intersection with B is one local bichromatic star. It cannot comprise
two disconnected local components joined outside B: the block adjacency is
a tree, and returning to B through a different cut would require a cycle
in that adjacency tree.

At any cut w on this local star, an outgoing child contributes either no
edge in this pair or exactly one edge w-z, by the local admission rule.
In the latter case, if z is itself a cut, the one-message invariant forbids
this pair in its outgoing child. There is no path inside the first child
past z, because its pair component is already the isolated edge w-z.

Therefore T is the local base star with at most one pendant edge added at
each of its vertices. At an original leaf this produces an arm of length
two. An extension at the center merely supplies one additional arm of length
one. If the base star is a single edge, extensions at both ends give P4,
which is still a spider with arms of length at most two after centering at
one internal endpoint. No vertex can receive two extra child edges because
each cut belongs to exactly two blocks. Thus every T is a tree and, more
specifically, such a spider. This also proves global acyclicity.

Potential overlooked case checked: a local star whose center is the parent
root is harmless. If its pair enters from the parent then Section 2 would
force its child-local component to be an edge; otherwise it may be a base
star for a new global component. The proof chooses the shallowest block
with an edge, so it does not silently presume every star starts at a block
root or every cut is a local leaf.

## 5. Recovery consequence and scope

Set X_i=e_color(i). Properness isolates the free diagonal; the actual
full-action cells for each color pair are unsigned tree incidence systems.
Each spider has center o and disjoint arms of length <=2. For every arm
with values x,y relative to o,

    x^2+y^2 <= ((3+sqrt(5))/2) * (x^2+(y-x)^2).

Summing, then replacing the center value by the variance-minimizing mean,
gives the incidence inverse bound from Cycle9. Disjoint original action
cells and symmetric duplication give

    ||Dhat-D||op <= ||Dhat-D||F <= sqrt(3+sqrt(5)) ||E||F.

This requires all original action cells and the canonical exact LS inverse.
Any numerical residual, probe error or action assembly error is additional,
as in the inherited theorem. The argument does not create a reduced-action
oracle or a performance comparison.

For a connected bridgeless graph of maximum degree four, every cut belongs
to exactly two nontrivial blocks of degree two there: each incident block
contributes at least two to the original degree. Thus the incidence and
degree hypotheses follow intrinsically in that class. A bridge can have
local degree one and permits more incident pieces, so bridges are outside
this argument until handled explicitly.

The Cycle9 one-mark theorem supplies the rooted hypothesis for each
nontriangle two-connected chordless tw<=2,Delta<=4 atom. C3 has the same
root guarantee by three distinct vertex colors: distinct root neighbors and
zero far flags. The atom theorem also supplies the unrooted root block.
These are dependencies, not newly reverified claims here.

This does not settle all degree-four partial two-trees, does not prove any
arbitrary-real four-query lower, and does not erase the star-four gluing
obstruction. It explicitly permits P4/P5 two-color components.

## 6. Checks against likely failure modes

* A flag on the common channel would invalidate the isolated-edge assertion.
  The permutation places the possible flag on the NEW channel instead.
* Two inherited common channels would require two outgoing requests and
  could invalidate the invariant. The rule deliberately admits at most one.
* A request to avoid both parent neighbor colors is not assumed when |P|=2;
  only one is forbidden, leaving the other available.
* A vertex shared by three blocks could receive several extensions and
  invalidate the simple spider proof. This incidence is excluded and cannot
  occur in the bridgeless Delta4 application.
* The construction never asks a parent block to realize two marked-root
  profiles. Its already determined local profiles are read, not reset.
* The base local component may have an extended center as well as leaves.
  That adds an arm of length one and preserves the spider estimate.

## 7. Bounded exact diagnostic and costs

`check_channel_transition.py` checks the new 30 orbit-representative local
admission cases. This is a small exact diagnostic of Section 2, not the
all-depth proof and not a replay of the accepted 66-family atom certificate.
Its source, literal witness permutations and body wall/CPU/RSS are saved.
Source reading, analytical challenge, drafting and integration costs remain
unknown. No application speedup, discovery-time claim, or external acceptance
is inferred from the diagnostic.

## 8. Earlier theta-only line, preserved but not used

Before receiving the broader proposal, this reviewer found a plausible
theta-specific 3-color-forest construction after removing one hub per block.
At incoming path2 marks, periodic-three coloring of an outgoing arm fails
the endpoint avoidance requirement exactly when its length from the retained
hub is 2 mod3. Replacing that endpoint by its grandparent's color fixes it;
the flips are nonadjacent and every vertex has at most one flipped child.
This would again make base-color components spiders. The broader one-message
theorem has a stronger receiving class and does not need this alternative.
No implementation, finite sweep or independent acceptance of that unused
theta-specific sketch is claimed here. Its reasoning cost is unknown.
