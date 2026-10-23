# Cycle6 result: stable recovery through arbitrary recursive depth

The principal new result is a **three-query, uniformly stable reconstruction
operation for an explicit recursive class of chordless series-parallel supports**.
The class has maximum degree four, arbitrary recursion depth and uneven branching,
and admits odd series composition. Its sharp worst-case exact and stable query
count is three. The full degree-four partial-two-tree question remains four
versus five.

## New all-size theorem

Start from a path of length two. Repeatedly permit either:

1. Two or three terminal-degree-one children in parallel, with a fresh terminal
   edge at each side.
2. Any odd number, at least three, of children joined in series.

The operation takes this construction expression as supplied input. For distinct
terminal colors (A,B), a parallel node colors its children's terminals (B,C),
where C is the third color. An odd series node alternates its junction colors
A,B,A,B,...,A,B. This yields proper acyclic three-coloring with no bichromatic
terminal connection.

The four actual boundary masses satisfy two distinct bounds: low slots are at
most two and high slots at most five. Parallel steps reset the low slots to one;
odd series steps copy them without exchanging their roles. The resulting global
component bound is 13, independent of every recursion parameter. The inherited
coordinate least-squares decoder then gives

    X_i=e_color(i),  ||X_i||=1,
    ||Dhat-D||_op <=5||E||_F

for every supported real symmetric D with free diagonal and every absolute
Frobenius action error E. This is an all-depth induction, not an extrapolation
from the finite fixtures. A cycle dimension argument excludes every real
two-column exact design on these cyclic supports, making three sharp.

The operation is outside both the forest and exact-one-subdivision controls:
it has cycles and can have adjacent degree-four vertices. It does not assert
the best possible noise constant, historical originality, or a physical speedup.

The general module form is reusable. If supplied separated leaf modules have
maximum bichromatic component K0 and all terminal masses at most beta>=2, and
the maximum parallel arity is B>=2, the same induction gives

    R=2+B(beta-1),
    K<=max(K0,1+B(R-1)).

Their graph-class hypotheses must be checked separately. For arbitrary path
leaves of length at least two, the saved explicit three-color path rule has
K0=beta=4, giving K<=31 and operator constant sqrt(61) at B=3.

## Actual receiving calculations

The saved inputs are new supports, sparse coefficients with free diagonal,
three complete original action columns, and nonzero rational observation noise.
The decoder source is inherited unchanged from Cycle5. No coefficient was
discarded, no reduced observation substituted, and no floating solver used.

| Receiving use | n | m | Max degree | Actual largest bichromatic tree | Strongest supplied operator constant squared |
|---|---:|---:|---:|---:|---:|
| Uneven branching with odd series, length-two leaves | 359 | 484 | 4 | 9 | 17 |
| Same operation with path lengths 2, 3, 8 and 17 | 218 | 245 | 4 | 11 | 19 |

Both recover the noiseless arbitrary-coefficient input exactly. On the noisy
input, both have exact projected-action residual zero. The first noise norm
squared is 86167/994009 and the actual error has certified operator upper
65/997 from its exact absolute row sums. The second noise norm squared is
52374/994009 and its corresponding actual error upper is 6859/98703. These
are checks on the saved instances; the all-real guarantee rests on the proof.
The row/cut/Frobenius certificates are all evaluated and the strongest retained.

## A decisive failure, not a universal impossibility

The obvious extension to two-child series composition swaps low and high
boundary slots. For the explicit recursion

    Q0=path2,
    Qh=P2(S2(Q(h-1),path2), S2(Q(h-1),path2)),

the same coloring strategy remains proper, acyclic and terminal-separated but
has a boundary component of exactly 2^h vertices. Its supports are actual
triangle-free series-parallel graphs with maximum degree three. A branch cut
has Gamma=2^(h-2)-2^(-h). The full materialized h=8 support has 1788 vertices,
2042 edges and a 256-vertex bichromatic tree. The saved exact symmetric witness
has a unit edge coefficient and action norm squared 256/16383, proving an
inverse constant at least sqrt(16383/256) for this design.

This closes the unmodified even-series extension. A better coloring of the same
graphs, four coordinates, and arbitrary real designs remain possible.

## Boundary exclusions that constrain the larger programme

The distinct chordless contributor supplies actual proofs and code, included
under research/chordless:

- For nonadjacent two-terminal joins, a bichromatic cycle occurs precisely when
  both pieces transmit in the same pair. Exact connectivity and mass updates
  must be retained together.
- K_(2,4) excludes equal prescribed terminal colors in an acyclic four-color
  extension. An arbitrary-boundary extension invariant is therefore false.
- Theta(2,2,2,L) with equal terminal colors forces all three available channels
  to transmit, even as L grows. Discarding small exceptions does not justify
  universal resetting of every channel.
- For every cap K>=2, an explicit colored C_(2K+1) minus a remote degree-two
  vertex has cap K but cannot be reinserted without recoloring or exceeding K.
  The received remote-degree-two corollary alone cannot justify that induction.

The theta result keeps its stronger free-boundary three-color comparator; its
four-color theorem is valuable for prescribed boundary states, not a query gain.

## Primary comparison and status

Color compression and substitution recovery are established sparse-Hessian
methods. Gebremedhin, Pothen, Tarafdar and Walther, *Efficient Computation of
Sparse Hessians using Coloring and Automatic Differentiation*, describe the
star/direct and acyclic/substitution framework:
https://www.cs.purdue.edu/homes/apothen/Papers/hessian-coloring-joc.pdf
The new contribution here is the all-depth mass invariant and its stated norm
guarantee on this grammar, not the invention of graph-colored recovery.

Wood, *Acyclic, Star and Oriented Colourings of Graph Subdivisions* (2005),
Lemma 3 supplies star-three colors for the exact one-subdivision of a
three-colorable graph:
https://dmtcs.episciences.org/articles/344/download
It is a stronger ordinary control on that subclass but does not cover the full
new grammar with adjacent degree-four vertices. The generic partial-two-tree
acyclic-three coloring provides exact identification without controlling mass.
The inherited five-query full-spark operation remains the general stable control,
and the three-query forest operation retains its smaller constant sqrt(2).

The primary 2026 Proposition 4.4 of Benitez-Bobadilla et al. exhibits P7^2 as
not star-four-colorable:
https://arxiv.org/pdf/2606.25168
Thus demanding star four-coloring would already overconstrain the full target.
This does not exclude bounded larger bichromatic trees. The Laakso recursion
has a similar first gadget but replaces every edge, unlike this grammar; its
metric results are not imported as coloring results. Focused primary notes and
the exact search costs are retained in research/literature. No matched prior
theorem was identified in those bounded searches; historical priority is unknown.

The independent mathematical reviewer accepted the all-depth induction, the
cycle query lower, and the even-series counterexample. A separate no-producer-
import checker verifies the saved receiving inputs and rational outputs. These
are internal proof and implementation checks, not external acceptance or Max's
integration. Receipt and integration are recorded separately in delivery.

## Decision

Keep the coordinate structural programme active. Stop the cap-only reinsertion
and unmodified even-series rules under their proved failures. The next precise
task is to find a boundary-state transition, potentially using the fourth color,
that handles both series parities without feeding an unbounded high mass back
into a low slot before branching. It must then be checked against forced
equal-terminal transmissions in actual chordless atoms. More vertices or a
precision sweep cannot answer that obligation.

No original NIST calculation or closed thermal, TPV, half-cell, molecular,
desalination or GUIDE operation was rerun. Protected programmes remain untouched.
The Cycle5 99-vertex receiving operation retains squared constant 20; its weaker
49 certificate was not substituted. The exact unchanged predecessor is preserved
by SOURCE_PREDECESSOR.json and its verified readable private transport.
