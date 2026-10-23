# Cycle7 focused primary comparison and a finite star-port interface

Contributor: /root/cycle7_focused_literature. 22 October 2026.
Scope: bounded literature obligation and a local interface lemma; root owns
the global construction and recovery theorem.

## Decision

No matching theorem for uniformly bounded-component acyclic four-coloring of
all chordless / triangle-free series-parallel degree-four supports was identified
in this additional focused search. This is not a literature-wide absence,
historical novelty, or open-problem claim. The native Cycle6 comparisons remain
unchanged. In particular, no edge-coloring result was converted to four vertex
coordinate directions.

A useful established alternative certificate is the star/in-coloring
characterization below. It produces a finite realizable port signature for the
owner's terminal-degree-one grammar. It does not prove that all required
production combinations admit a signature or that star four-coloring holds.

## Primary source checked

Michael O. Albertson, Glenn G. Chappell, H. A. Kierstead, Andre Kundgen and
Radhika Ramamurthi, *Coloring with no 2-colored P4's*, EJC 11 (2004), R26:
https://www.combinatorics.org/ojs/index.php/eljc/article/download/v11i1r26/pdf

Section 3, Definition 3.1 and complete Lemma 3.2 proof were read. A proper
coloring is a star coloring iff its edges can be oriented so every bichromatic
three-vertex path points toward its middle. The generic acyclic-orientation
bound in Theorem 3.3 is k*Delta+1, hence nine for k=2,Delta=4; it does not supply
four colors. Source retrieval refs: turn198view2 and turn199view0.

The scope of Robert Janczewski and Michal Malafiejski, *On Efficient Coloring
of Chordless Graphs* (2009), was checked at its native PDF:
https://journals.agh.edu.pl/dmms/article/download/544/401/1195

Its Corollaries 4-5 give 2-degeneracy and ordinary three-colorability. These do
not assert acyclicity or bounded two-color component mass. The ordinary proper
two-coloring of C4 already shows the distinction. Relevant source refs:
turn198view0 and turn199view1. No dependence on this paper's structural proof
is introduced into the owner's theorem.

## Exact local form of the star condition

For a proper coloring c, define
    mult(u,b) = number of neighbors of u whose color is b.
The coloring is star iff there is no edge uv such that
    mult(u,c(v)) >= 2 AND mult(v,c(u)) >= 2.                 (1)

Proof: if (1) holds, choose a neighbor w!=v of u colored c(v) and a neighbor
z!=u of v colored c(u). Properness and the two different endpoint colors ensure
w,u,v,z are four distinct vertices. They form a bichromatic P4. Conversely,
the middle edge of any bichromatic P4 has both multiplicities at least two.
This is a local restatement of the established star condition, not a priority
claim or a new whole-graph coloring theorem.

## A finite terminal-degree-one signature

Assume a supplied module is already properly star colored, has two distinct
degree-one terminals s,t, and has no terminal edge. Record
    (c(s), c(t), c(a), c(b), epsilon_s, epsilon_t),
where a is s's unique neighbor, b is t's unique neighbor, and
    epsilon_s = [mult(a,c(s)) >= 2],
    epsilon_t = [mult(b,c(t)) >= 2].
The terminals may have equal colors; their physical vertices stay distinct.
For q colors there are at most q^2*(q-1)^2*4 signatures, at most 576 for q=4.
This is a bound on individual signatures, not on all subsets used by a DP.

Under series identifications and parallel identifications with fresh exterior
stubs, only the incident multiplicities at the identified vertices change.
For an old edge from a join vertex to a child interior, the far-end condition
in (1) is exactly the saved epsilon bit. Its join-end condition is computed by
counting the known neighbor colors, including any fresh stub. No other old
edge gains a changed endpoint neighborhood. A newly added exterior stub edge
has a degree-one endpoint, so cannot itself violate (1). Its new epsilon bit
is computed from the other incident neighbor colors at its join vertex.

Thus these signatures give exact acceptance/rejection and updated port states
for these operations, provided the pieces already have valid star colorings,
their interiors are disjoint, terminal colors agree at every identification,
and the structural simplicity/degree rules of the grammar hold. Parallel
children may have their two terminals adjacent to the same internal vertex
(as on a path2 leaf); the definition still applies, since the two terminal
vertices are not identified with each other. Series endpoints retain their
original neighbor conditions. These observations account for every affected
edge, so the interface can be composed at arbitrary depth without omitting
a new bichromatic P4.

This lemma does **not** show existence of a closed nonempty set of realizable
states for every admitted expression. That finite closure is the root's
remaining constructive task if it chooses star colorings on this subclass.
It does not imply a four-query theorem for all partial two-trees: the preserved
P7-squared obstruction already excludes that stronger star requirement there.
Bounded larger bichromatic trees remain admissible for the full target.

## Forced boundary and degree checks are retained

For K2,4 with equal endpoint colors A, all four internal vertices need colors
other than A. Each has epsilon=true at both incident sides. Any repeated
internal color makes (1) fail on an incident edge. Four different colors other
than A would be required, impossible with q=4. With different terminal colors,
the usual three-color star coloring remains available.

K2,4 itself has degree four at its two terminals. It is not an admitted
terminal-degree-one module, and attaching exterior stubs there would give
degree five. The local condition still checks this boundary counterexample,
but the terminal signature must not be silently used with a false degree-one
interface. The same distinction applies to forced transmissions in theta atoms.

## Receiving consequence, conditional on a constructed coloring

A supplied proper star coloring gives two-color star forests, so the existing
coordinate decoder applies. In the degree-four setting their orders are at
most five. The inherited stronger star recovery bound (sqrt2 under the native
absolute Frobenius action-noise convention) remains the relevant comparator;
the coarser size/row bound is unnecessary where that sharper theorem applies.
Obtaining a four-color star design through the finite port states would
therefore be a complete recovery consequence on its proved support class,
once actual coloring construction, original actions and decoding are charged.
No such all-class result is claimed by this literature/interface note.

### Self-contained verification of the sharper star decoder bound

For a two-color star with k edges, its unsigned vertex-edge incidence matrix
B has Gram matrix B^T B = I_k + 11^T. Therefore its smallest singular value
is at least one (sqrt2 for a single edge). The least-squares edge error vector
has Euclidean norm at most the Frobenius/Euclidean norm of its selected noise
cells. Different two-color components use disjoint action cells, and the
proper-color diagonal cells are also disjoint. The squared Frobenius norm of
a symmetric off-diagonal error matrix is twice the squared Euclidean norm of
its distinct edge coefficients. Consequently the canonical decoder obeys

    ||Dhat-D||op <= ||Dhat-D||F <= sqrt2 ||E||F.

This proof applies to every supplied proper star coloring, any number of
colors and any maximum degree. It is the applicable inherited comparator,
not a claim that this note invented star recovery or its optimal constant.
It uses the canonical least-squares decoder on the complete original action.
Floating residuals/acquisition errors still require the owner's usual explicit
allowances. The root's proposed finite automaton must establish a nonempty
realizable state family on every admitted expression before invoking this
consequence; finite successful graphs alone would not establish that premise.

## Search boundary and excluded hits

Six web calls, sixteen search entries, five opens. Both search engines were
used; the stronger engine filled sparse initial coverage. Search terms
targeted chordless/minimally-2-connected/2-sparse vertex star coloring,
triangle-free series-parallel degree-four supports, and terminal interfaces.
No broad survey or old fixture replay was performed.

Several returned titles concerned edge coloring, circular coloring (historically
also called star coloring), or ordinary proper coloring. They do not meet the
query contract. The Xidian-hosted 2015 r-acyclic PDF request timed out; the
complete proof was not read or relied on. Cycle6 had already rejected using
cycle-color counts or arbitrary long bichromatic paths as mass control.

Existing notes for subdivision, tree-partition, I,F-partition, CAI, long strips,
prisms, Laakso comparisons and the P7-squared obstruction were read and retained,
not rerun as new scientific checks. This bounded search cannot establish
historical priority of a new root construction.

## Costs

Observed awaited web-call time: 18.331 seconds (Date.now around each tool call).
First recorded source-reading clock: 2026-10-22 02:21:17 UTC; last retrieval/
assessment checkpoint: 02:23:44 UTC. These timestamps are a work envelope,
not aggregate model compute or a discovery cost. Source reading, inference,
mathematical assessment, authoring and service overhead were not separately
metered. No numerical experiment, package install, paid resource, external
write or scientific replay occurred. CALLS.json contains exact queries and
the individual observed intervals.

