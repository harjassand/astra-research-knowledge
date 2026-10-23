# Cycle5 result: cut balance and a reduction of the four-color frontier

The four-versus-five question for treewidth at most two and maximum degree
at most four remains open. This checkpoint supplies two all-size results:
a degree-free characterization of stable proper-coordinate recovery, and
a constructive reduction that removes arbitrarily long triangle strips
from the unresolved four-coloring problem. The native Cycle4 archive is
embedded unchanged.

## Strongest result

For a supplied proper coordinate design X_v=e_c(v), every bichromatic
component must be a tree. For each edge, split that tree into a,b vertices;
write Gamma=max ab/(a+b), M=max min(a,b), and r for the maximum number of
neighbor colors. The exact incidence least-squares decoder L satisfies

    max(1,sqrt(Gamma)) <= rho = ||L||_(F->operator)
        <= sqrt(1+4rM) <= sqrt(1+8rGamma).

The decoder is optimal in worst deterministic noise for this fixed design.
For fixed q, uniform stability is equivalent to acyclicity and uniformly
bounded Gamma, with NO graph-degree restriction. Large components with many
small branches are allowed. A balanced cut, rather than component diameter,
is the error mechanism. This extends the earlier bounded-degree criterion;
within degree-four graphs it does not remove the need to bound component size.

The proof uses an exact covariance matrix of subtree-sum errors and a bound
on the number of nonzero entries per column of an oriented error matrix.
The lower is the exact cut-flow indistinguishability witness, valid for
nonlinear exact decoders too. It does not lower-bound arbitrary real designs.

## Explicit operation and the distinction between output norms

A supplied hub with arbitrarily many arms of length at most L has a two-query
operation with operator error constant sqrt(1+4L). Two is its minimum exact
and stable query count for fixed L when an edge is allowed. The worst constant
is Theta(sqrt L). The ordinary three-query forest operation has constant
sqrt2 and remains the stronger noise comparator.

The actual exact receiving use has33 arms of length12,397 vertices and396
edges. Its maximum degree is33. It gives

    q=2, Gamma=4620/397, M=12, certified operator constant=7.

On that same admitted design, a saved alternating ramp on two arms proves
that every exact Frobenius-output decoder needs constant at least
sqrt(325/3), approximately10.4083. More generally the Frobenius lower grows
as L while the optimal operator constant grows as sqrt L. This is a real
norm-contract distinction, not a solver timing or a new Delta4 lower.

The saved double-star counterexample has two hubs with32 leaves each:
n=66, diameter3, central coefficient1, leaf coefficients-1/33, and
||DX||F^2=2/33. It proves inverse>=sqrt(33/2). The all-size family shows
that well-conditioned local stars can lose stability when joined. Its
unbounded degree and specified-coordinate scope are explicit.

## The selected four-color problem is structurally smaller

Every maximal edge-connected triangle union in a partial two-tree is an
actual2-tree, with outside connected pieces attached through cliques of size
at most two. The inherited degree-four2-tree classification implies that
every such triangle component with at least30 vertices is a squared path.
Its interior is saturated, leaving only two endpoint pairs as ports.

The new boundary extension accepts arbitrary distinct colors on both ordered
endpoint pairs. Six-step transitions on12 states join them to a period-nine
core, producing bichromatic trees of order at most16 and no bichromatic path
between opposite ends. All144 transition witnesses are saved. A strict
two-vertex gap for each color pair supplies the all-size separation argument.

Delete interiors of all long triangle strips, retaining their endpoint
edges. The reduced graph has triangle components of order at most29.
Any acyclic four-coloring of the reduced graph with component bound K
extends to the original graph with bound65K. Thus the universal coordinate
existence question is equivalent to the same question with all triangle
components bounded. The required coloring of the reduced graph is an
unsolved input; this is not a universal four-query implementation.

The owner's additional attachment lemma bounds cut mass directly:

    Gamma_final <= max((1+A)Gamma_base, A, B/4),

when each old vertex receives at most A new vertices in rooted tree
attachments and detached trees have order at most B. Distinct attachments
have disjoint new vertices except for their old root. This permits unbounded
old components, and shows exactly what local insertion must control.

## Actual receiving calculation on the new mixed support

The contributor's new two-strip-plus-square graph has99 vertices and194
edges, reduces to8 vertices and6 edges, and has reduced component bound2.
The extended four-coloring has maximum component order9.

The owner received those actual colors and support into the global decoder,
formed synthetic exact actions including free diagonals, added deterministic
rational noise, and recovered both noiseless and noisy outputs. No reduced
action cells were substituted for the original operator. The measured
global data are:

| Quantity | Exact value |
| --- | --- |
| Reduced Gamma | 1/2 |
| Original Gamma | 20/9 |
| Largest new attachment at one old vertex and pair | 7 |
| Largest detached tree | 5 |
| Attachment theorem's Gamma upper | 7 |
| New cut certificate's squared operator constant | 49 |
| Better inherited row certificate's squared constant | 20 |

The accepted per-input bound is sqrt20, the minimum of certified bounds.
The new cut theorem is not promoted as a conditioning improvement on this
bounded-degree fixture. Its benefit is the degree-free information criterion
and the justified composition rule. The boundary reset changes the set of
supports that can be reconstructed from a supplied reduced coloring.

## Comparators and limits

The full class still has an all-real three-query obstruction and a five-query
upper through a fixed full-spark palette on a17-color square coloring. The
ordinary five-coordinate banded isometry has constant1 on its own banded
class; it is not asserted to cover every current support. Exact one-subdivision
of a partial2tree already has a classical three-color star construction;
we do not relabel that established operation as a new four-query advance.

Construction and decoding are linear arithmetic in a supplied representation;
finding the missing reduced coloring, input conversion, action acquisition,
bit cost, numerical residual and downstream inference remain chargeable.
No NIST, molecular, physical-runtime or energy advantage is established.

Analytic focused reviews accepted the cut theorem, strip theorem and new
attachment lemma. Independent exact checkers verify the transition witnesses
and stored operator calculations without importing producer code. Their
receipts and scope are in verification/ and research/cut_balance_review/.
These establish internal correctness of the stated arguments and concrete
data, not historical originality, external acceptance or Max integration.

## Continuation decision

Keep the full question active. Work next on boundary extension states for
chordless/triangle-free two-terminal atoms and their composition with bounded
triangle pieces. Track whether a bichromatic component meets a boundary and
how much mass can accumulate at that boundary; a reset must be proved through
arbitrary depth. A primary-source structural corollary supplies a degree-two
vertex away from an adjacent boundary in clique-cutset-free atoms larger
than12 vertices, but reinsertion still needs the missing coloring invariant.

Do not optimize the constants16,30,65 or rerun larger fixtures by default.
The meaningful question is whether the remaining interface states close, or
whether an actual graph family forces growth for all coordinate four-colorings.
Such a negative would still leave arbitrary real four-column designs open.
