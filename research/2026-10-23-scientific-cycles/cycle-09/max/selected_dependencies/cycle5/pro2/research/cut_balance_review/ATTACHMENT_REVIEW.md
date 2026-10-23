# Focused review: cut-mass-preserving rooted attachments

Reviewer: `cut_balance_challenge`, Cycle5 PRO2. The root requested this
additional bounded review of PROOF.md Section5 after the two prior reviews.
No numerical experiment or earlier fixture was replayed for this review.

## Verdict and precise attachment convention

The transfer bound is correct. Fix one color pair. Start with its old
bichromatic forest. Attach trees whose new vertices are disjoint except for
sharing their old root, and add detached trees. Equivalently, after deleting
all old edges, every component containing a new edge is a tree and contains
at most one old vertex. This explicit convention prevents overlapping pieces
from silently creating a cycle or joining old components.

Let A bound the total number of new vertices rooted at any one old vertex
for this fixed color pair, let B bound the order of every detached tree,
and put W=1+A. Then

    Gamma_final <= max(W Gamma_old, A, B/4).

The hypothesis must bound total attached mass per root, not just the size of
each individual piece when arbitrarily many pieces can attach to that root.
No bound on the size or maximum degree of an old tree is required.

## Proof checked

Every final edge is of one of the following three kinds.

1. An old edge cuts an old component into a,b vertices. Every old vertex has
   between one and W vertices assigned to it after attachment, including
   itself, so the final cut sizes satisfy a'<=Wa, b'<=Wb. The harmonic mass
   h(x,y)=xy/(x+y) has partial derivatives y^2/(x+y)^2 and x^2/(x+y)^2,
   both positive. It is homogeneous of degree one. Consequently

       h(a',b') <= h(Wa,Wb) = W h(a,b) <= W Gamma_old.

2. An edge in an attached tree has a side away from its old root containing
   only vertices assigned to that root. That side has at most A vertices.
   Since h(x,y)<=min(x,y), this cut's mass is at most A.

3. An edge of a detached N-vertex tree has h(a,b)<=N/4<=B/4, by
   4ab<=(a+b)^2.

These exhaust the edges. The attachment convention preserves acyclicity
and prevents mergers of different old components, proving the claim.
Isolated old vertices cause no exception: their new edges fall under case2,
and the old edgeless forest has Gamma_old=0.

## Application to the triangle-strip transfer

The already reviewed strip extension gives, for each color pair, a local
component of order at most16 meeting the old graph in either no vertex,
one vertex, or exactly the endpoints and edge of one retained end pair.
In the last case, deleting that retained edge splits the local tree into
two trees, each attached to just one old endpoint. There cannot be another
path between these endpoints because the local component is acyclic.
Distinct strip interiors are disjoint. Thus the attachment convention above
holds simultaneously for all strips.

The conservative incidence bound of four strips at an old vertex and16
vertices per incidence gives A=64. Detached components have B=16. Therefore

    Gamma_G <= max(65 Gamma_R,64,4) = max(65 Gamma_R,64).

This argument is independent of any bound on old bichromatic component
order, so it is stronger than a size-only transfer statement in that respect.
It does not solve the missing reduced-graph coloring problem, establish a
new all-real-design lower, or claim improved conditioning on every input.

## Receiving values and comparison scope

The saved root receiving record reports A=7, B=5 and Gamma_R=1/2. Substitution
in the proved inequality gives

    max(8*(1/2),7,5/4)=7.

Its reported actual Gamma_G=20/9 is consistent with the transfer. This review
checks the theorem and this substitution; it does not replace the separate
exact fixture checker establishing the recorded A, B and Gamma values.
The saved99-vertex record labels49 and20 as *squared* operator constants.
The new cut-oriented upper is therefore7, whereas the stronger inherited
certificate on that input is sqrt(20). The transfer theorem should not be
presented as a conditioning improvement on that fixture.

## Observed cost and status

This review read the root proof and the receiving record labels, then checked
the algebra and decomposition argument. Local source-access calls reported
about0.3s outer latency apiece; no mathematical computation body was executed
or timed. Reasoning, writing, messages and service/inference costs are
unmetered and unknown, not zero. Internal proof acceptance is distinct from
historical originality, external acceptance and practical performance.
