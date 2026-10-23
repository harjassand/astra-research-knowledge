# Four coordinate actions on an all-depth series/parallel grammar

Astra PRO2, Cycle7, 22 October 2026. Principal construction and integration:
the owner. Focused independent obligations and their actual records are in
`verification/` and `research/`. This is a new theorem relative to the received
checkpoint, with no claim of historical priority or external acceptance.

## 1. The operation and its exact scope

Let H be the following class of supplied two-terminal expressions. A module
has distinct, nonadjacent ordered terminals s,t, each of degree one. Different
child occurrences have disjoint vertices before the specified identifications.

* A leaf is a path of any integer edge length at least two.
* S_l, for any l>=2, concatenates l children by identifying consecutive terminals.
  Both series parities are admitted.
* P_b, b in {2,3}, identifies the left terminals of b children at a, and their
  right terminals at z, then adds fresh terminal leaves s,t and edges sa,zt.

An input expression can be a directed acyclic description with repeated child
IDs. Each occurrence means a distinct copy. The expanded output size is charged.
The expression describes the actual original support; it is not permission to
remove the exterior stubs, replace observations, or freely recognize an arbitrary
graph as a member. If the given support has other vertex labels, a supplied
isomorphism or a checked expansion-to-support map is also necessary.

**Theorem 1 (constructive star-four design).** Every finite expression in H has
a proper star coloring with four colors. It can be constructed by a fixed finite
transition certificate using O(p+n+m) combinatorial work and storage, where p
charges the read/normalized description and expanded occurrences, and n,m are the
actual output vertex and edge counts. There is no bound on depth, series length,
number of branchings, or path-leaf length. No arbitrary boundary-color assignment
is promised.

**Theorem 2 (full-action recovery).** Let G be the expanded support, let D be any
real symmetric matrix whose off-diagonal nonzeros are allowed only on G, with
an arbitrary free diagonal, and set X_i=e_{c(i)} in R^4 for the constructed
coloring. For all real E in R^(n x 4), the supplied canonical least-squares
decoder applied to Y=DX+E satisfies

    ||Dhat-D||F <= sqrt(2) ||E||F,
    ||Dhat-D||op <= sqrt(3/2) ||E||F.

The first bound and its weaker operator consequence were the initially
checked certificate. The sharper operator bound follows from the recovered
Cycle2 direct-decoder quadratic estimate and the action projection identity,
as proved in Section 8 and `research/OPERATOR_BOUND_ADDENDUM.md`. The actual
saved receiving records keep their original valid squared bound 2 unchanged.

Every probe row has Euclidean norm exactly one, across all four directions
together. No distribution, relative-noise bound, known coefficient, spectral
normalizer, or reduced-action oracle is used. Noiseless reconstruction is exact.

The full class tw(G)<=2, Delta(G)<=4 still has the inherited q3 lower and q5
upper; arbitrary-real q4 on that full class remains open. H is a strict
subclass. The graph obstruction in Section 10 identifies a missing structural
interface even among chordless two-connected atoms.

## 2. Graph properties are part of the construction

Every member is connected, simple, triangle-free, chordless, series-parallel,
and has maximum degree at most four. Its two terminals retain degree one,
remain distinct and nonadjacent, and every simple terminal-to-terminal path is
induced. These statements follow together by induction.

A path leaf has all these properties. A series join identifies leaves from
disjoint children and creates a degree-two articulation vertex. Cycles remain
inside one child, and a terminal path is a concatenation of induced child paths
with no cross-edges. At a parallel join, a and z each have degree b+1<=4 after
the stubs are added; every old internal vertex retains its degree. There is no
edge az because child terminals were nonadjacent, and distinct interiors cannot
create duplicate edges. A cycle is either internal to a child or is the union
of one a-z path in each of two children. Those paths are induced, have length
at least two, and have no cross-edges or az edge. Thus the cycle has no chord
and length at least four. A new terminal path passes through one child and the
two stubs and is induced. The same productions are ordinary series/parallel
operations, proving the series-parallel and width-two claims. This proof uses
the induced-terminal-path invariant; chordlessness of children alone would not
justify the parallel step for arbitrary externally chosen terminals.

## 3. A local certificate for star coloring

A proper coloring is a star coloring when it has no bichromatic path on four
distinct vertices. Equivalently, every two-color component containing an edge
is a star. In a proper coloring, call edge uv bad when u has another neighbor
colored c(v) and v has another neighbor colored c(u). Then the coloring is star
if and only if no edge is bad.

Indeed a bichromatic four-vertex path has a bad middle edge. Conversely, choose
the two other neighbors witnessing a bad edge. They are distinct from its
endpoints and from each other: a common witness would have to have both unequal
endpoint colors. They form a bichromatic four-vertex path. This elementary
criterion is a local restatement of the classical star-color condition; it is
not claimed as new. A closely related primary formulation is the in-coloring
orientation characterization in Albertson et al., Lemma 3.2 [1].

This local criterion supplies the stronger invariant used here. Instead of
allowing large bichromatic trees and carrying their masses, we prevent their
extension past a star. In this grammar the stronger invariant is realizable.
It is not realizable with four colors on every partial two-tree: the inherited
P7-squared exclusion remains relevant to the broader question.

## 4. Exact boundary signature and composition

For a star-colored module let u_s,u_t be the unique terminal neighbors. They
may coincide on a two-edge path. Record

    sigma=(a,b,p,q,f,g)
          =(c(s),c(t),c(u_s),c(u_t),f,g),
    f=[u_s has a neighbor other than s colored a],
    g=[u_t has a neighbor other than t colored b].

Here a!=p and b!=q; a and b may agree. The flags are Boolean existence
statements. They are not assertions that terminal colors are freely selectable.
Every state used below has an actual realizing coloring.

### 4.1 Binary series

Take sigma1=(a1,b1,p1,q1,f1,g1) and sigma2=(a2,b2,p2,q2,f2,g2).
They can be identified at t1=s2 only if b1=a2. The resulting coloring is star
exactly when

    not (q1=p2 and (g1 or f2)).                         (S)

The output signature is

    (a1,b2,p1,q2,f1,g2).                              (S-out)

Only the joined vertex gains neighbors. Its two neighbors are distinct because
the interiors are disjoint and child terminals are nonadjacent. The first
junction edge has far-end flag g1 and new junction-end flag [q1=p2]; the second
has far-end flag f2 and the same new flag. All other edges retain the neighbor
colors at both endpoints. This proves the exact rejection rule. The neighbors
of the outer terminals are not the join, and their neighbor-color lists are
unchanged, even if a child's terminal neighbors coincide. Therefore their
recorded flags remain f1,g2.

### 4.2 Stubbed parallel composition

Let the b child signatures be (C,D,p_i,q_i,f_i,g_i). Their terminal colors must
agree across children at each identified end. Give the new exterior terminals
colors A,B, requiring A!=C and B!=D. The union is star exactly when, for every i,

    not (f_i and (p_i=A or some j!=i has p_j=p_i)),      (P-left)
    not (g_i and (q_i=B or some j!=i has q_j=q_i)).      (P-right)

Its output signature is

    (A,B,C,D, [some i:p_i=A], [some i:q_i=B]).          (P-out)

Only a and z acquire neighbors. Every old child edge incident to a retains
far-end flag f_i. At a its other-side flag is exactly the collision condition
in P-left. This proves the left rule, and the right rule is identical. The
fresh stub edges have a degree-one endpoint and cannot be bad. Interior edges
retain their endpoint neighbor colors. Even if one child interior vertex is
adjacent to both terminals, a and z are distinct and retain colors C,D, so
its flags are unchanged. The new terminal flags are precisely P-out.

### 4.3 Exactness and limitations of the interface

Restricting any valid output coloring to the child copies gives admitted child
states satisfying these formulas. Conversely, any selected realizable child
states satisfying them can be realized independently and glued; the bad-edge
criterion proves the resulting whole coloring valid. Thus the transition is
exact for the set of attainable signatures, not merely a local sufficient rank
test. No terminal-neighbor identity or remote connectivity bit is missing under
the stated hypotheses. This conclusion is specific to star coloring and these
degree-one, nonadjacent terminals with disjoint interiors. It is not a state
compression theorem for general acyclic colorings, adjacent ports, shared
interiors, or ports of higher degree.

The full independent proof, including the shared-neighbor and equal-terminal
cases, is `verification/port_interface/PROOF.md`. The finite graph enumerations
there check implementations of the lemma; the argument above gives its
all-size validity.

## 5. Four realizable guarantee families

Color labels are 0,1,2,3. Canonicalize the first four entries by first-occurrence
order and leave the two bits unchanged. A family guarantee means that **every**
listed state, and every permutation of its color labels, can be realized on
the module. It need not be the complete attainable-state set. A family label is
not a syntactic graph category and does not prescribe a module's vertex count.

The four canonical families are as follows. Entries are (a,b,p,q,f,g).

```
A (2):
001111  012200

B (4):
001200  011201  012010  012300

C (9):
001200  001211  011000  011200  011210
012000  012001  012301  012310

D (15):
001201  001210  001211  011000  011001
011010  011200  011210  011211  012000
012001  012011  012301  012310  012311
```

These digit strings encode six separate single-digit entries, not numbers.
The machine-readable lists and each colored witness are in
`results/general_star_certificate.json`, 115,016 bytes, SHA256
`b0ffc8e13badf6faedff7dd821407549e3f4745f7de8a15e6cd765e5163e8fb4`.

A two-edge path realizes precisely family A up to color permutations: equal
terminal colors give both flags one, distinct terminal colors give both zero.
A three-edge path realizes precisely family B. For path colors (a,p,q,b), its
flags are [q=a] and [p=b], and the coloring is star exactly when these two
equalities do not both hold. The displayed B states are all the resulting
canonical patterns. Direct independent enumeration gives 36 proper/star
labeled four-colorings for path2 and 108 proper, 96 star colorings for path3.

## 6. The complete closed transition certificate

The following tables assign a guaranteed parent family for every possible
child-family combination. Series is ordered; parallel children are unordered.

| S2 | A | B | C | D |
|---|---|---|---|---|
| A | C | B | A | A |
| B | B | A | A | A |
| C | A | A | A | A |
| D | A | A | A | A |

| P2 child classes | Parent | P3 child classes | Parent |
|---|---|---|---|
| AA | C | AAA | C |
| AB | D | AAB | D |
| AC | C | AAC | C |
| AD | C | AAD | C |
| BB | A | ABB | A |
| BC | A | ABC | A |
| BD | A | ABD | D |
| CC | A | ACC | A |
| CD | A | ACD | C |
| DD | A | ADD | C |
| — | — | BBB | A |
| — | — | BBC | A |
| — | — | BBD | A |
| — | — | BCC | A |
| — | — | BCD | A |
| — | — | BDD | A |
| — | — | CCC | A |
| — | — | CCD | A |
| — | — | CDD | A |
| — | — | DDD | B |

There are 16+10+20=46 cases. For **every requested state of every parent
family**, the JSON gives colored child states realizing it. These total 200
witness rows. This is an explicit finite mathematical certificate, not a
floating solver status, sampled graph pattern, or bound on recursion depth.

For example, P3(C,C,C)->A has these witnesses. To obtain parent
(0,0,1,1,1,1), choose children

    (1,1,0,2,0,0), (1,1,0,2,0,0), (1,1,2,0,0,0).

To obtain parent (0,1,2,2,0,0), choose all three children

    (2,2,1,0,0,0).

Each belongs to the C orbit. The incoming flags are zero, so repeated join
neighbor colors are allowed; the output flags follow exactly from P-out.
This illustrates why requiring every port to reset to zero, or requiring
distinct terminal colors in every child, would be an unnecessary and sometimes
false intermediate invariant.

`verification/port_interface/verify_general_certificate.py` independently pins
the four family lists, enumerates the actual leaves, demands all 46 cases and
all required output rows exactly once, checks each child's family orbit, and
evaluates S/P directly with integer labels and Boolean flags. It imports no
producer. Its first gate passed all 200 rows. For readability,
`research/FINITE_WITNESSES.txt` renders every witness from the actual JSON in
compact literal form. The checker and these finite rows discharge the full
finite obligation; no optimization or unverifiable success flag is part of the
theorem's premise.

## 7. All-depth proof and construction

Induct over the normalized finite expression with leaves path2/path3 and nodes
S2/P2/P3. Label a leaf by its A or B guarantee. At an internal node the table
selects its parent label from its child labels. For any requested parent state,
the corresponding witness specifies a realizable state for each child. The
induction hypotheses realize those children; Section 4 proves the joined
coloring star with the exact desired signature. Global color permutations
preserve all predicates. Parallel witnesses can be reassigned to the
corresponding actual child order, while series order is retained. This proves
the guarantee for every label at every depth. Choosing any root state yields
the desired coloring.

Every integer length l>=2 can be written l=2a+3b with a>=0 and b in {0,1}.
Use b=0 for even l and b=1 for odd l. Thus an arbitrary path leaf splits into
path2/path3 segments, with segment endpoints identified at existing path
vertices. This changes no graph vertex or edge. Every S_l associates into
binary series joins, again with no graph change. The one-segment cases need
no unary node. These normalizations prove the theorem for the entire stated
grammar, including both series parities and arbitrary path leaves.

The executable `src/star_recovery.py` first normalizes and labels nodes
bottom-up, then uses explicit stacks to expand the actual graph and realize
the requested states top-down. Its fixed certificate lookup and at most 24
color-permutation trials per node are size-independent constants. It preserves
the original child order when applying unordered parallel cases. Stack-based
traversal avoids a hidden language recursion-depth restriction. It validates
topological child IDs, admitted arities and integer path lengths. The separate
actual-graph star check evaluates the bad-edge condition on every edge.

For a compressed DAG expression, output expansion can be exponential in its
description length and is charged as such. Unreachable listed path descriptions
are also normalized by this simple implementation; their normalization work is
part of p. A caller wanting to avoid that work may first prune unreachable nodes
and must charge the pruning. No claim is made of linear work in a compressed
description when the actual graph is exponentially larger.

## 8. Recovery and its uniform error proof

Fix the constructed proper coordinate coloring. The diagonal entry D_ii appears
alone in action cell (i,c(i)). For each unordered color pair, the corresponding
off-diagonal edge coefficients map to the selected action cells by the unsigned
vertex-edge incidence matrix of the bichromatic graph. Different pairs/components
and diagonal cells are disjoint. Unused cells contain only noise.

Every nontrivial two-color component is a k-edge star. Its incidence matrix B
has

    B^T B = I_k + 11^T.

For k>=2 its smallest singular value is one; for k=1 it is sqrt(2). Thus the
least-squares edge error has Euclidean norm at most the norm of its selected
noise cells. The squared Frobenius norm of a symmetric off-diagonal matrix
counts each distinct edge twice. Diagonal errors count once. Summing the
disjoint noise cells gives

    ||Dhat-D||F^2
      = sum_i diagonal_error_i^2 + 2 sum_edges edge_error^2
      <= 2 ||E||F^2.

The operator norm is at most the Frobenius norm, giving first the weaker
operator bound sqrt(2). This bound
does not grow with star degree, component count, graph size, or recursion depth.
The current graph degree bound also gives component order at most five, but
that weaker size fact is unnecessary for the sharper sqrt(2) estimate. The
bound is a valid uniform certificate, not claimed to be the exact operator
inverse norm of every graph.

### The stronger triangle-free operator bound

For any supplied star coloring choose a direct exact inverse T that reads each
edge from one leaf's isolated action cell and each diagonal from its own-color
cell. These cells are distinct. For a unit vector z, let w_i=z_i^2. The squared
Frobenius dual norm of E -> z^T T(E) z is

    Q_G(w)=sum_i w_i^2 + 4 sum_edges w_i w_j.

The preserved Cycle2 forest proof bounds this by shifting mass between
nonadjacent positive-weight vertices until its support is a clique. That
argument requires only triangle-freeness: along each shift Q is convex, so
one endpoint does not decrease it; a final clique has size at most two. Its
value is 1+2ab<=3/2. Hence ||T||_(F->op)<=sqrt(3/2).

Let L be the full supported symmetric action map and Pi the Frobenius-orthogonal
projection onto range(L). Its canonical least-squares inverse R equals T Pi,
since T is exact on that range. Pi is a contraction, so
||R||_(F->op)<=sqrt(3/2). All grammar graphs are triangle-free, completing the
stronger assertion of Theorem 2. The full argument and exact recovered native
source are in `research/OPERATOR_BOUND_ADDENDUM.md` and `sources/cycle2_selected/`.
The focused independent review accepted this proof without a numerical rerun.
Sharpness for the LS decoder is not asserted. The saved weaker certificate
and actual action/output records remain unchanged.

The inherited `src/coordinate_decoder.py` performs the same least-squares map
on a tree by signing the two vertex parts, subtracting the mean, and summing
subtrees. It is included unchanged. Its general preparation routine also prints
older trace/row bounds; the new star proof is what supplies the squared bound 2.
No numerical discrepancy is hidden by replacing that routine's printed bound.

A direct star formula provides independent receiving verification. If y_0 is
the center observation and y_1,...,y_k are leaf observations, then

    d_hat_i = y_i + (y_0-sum_j y_j)/(k+1).

It is the solution of (I+11^T)d=y_leaf+y_0 1. The independent receiving checker
uses this formula instead of importing or rerunning the producer decoder.

### Actual computational and numerical boundary

Coloring, graph validation, preparation, and decoding require O(p+nq+m)
arithmetic/storage for fixed q=4. Four actual full actions must be acquired.
For the saved explicit sparse matrices, `action` accumulates each diagonal once
and each edge twice into the appropriate columns; those real operations are
timed. For another matrix-action source, its own four-query acquisition cost
must be paid. The theorem does not furnish the action oracle.

Exact rational arithmetic is used for the saved receiving records. Arithmetic
operation counts are not bit-complexity bounds. With floating arithmetic let
P be the orthogonal projector onto the full supported symmetric action range,
and suppose a supported symmetric candidate has independently bounded residual
R_num=Dhat X-PY. Relative to the exact decoder output Dstar, the sharper inverse
bound gives ||Dhat-Dstar||op<=sqrt(3/2)||R_num||F. Consequently

    ||Dhat-D||op <= sqrt(3/2)(||E||F+||R_num||F).

Assembly/acquisition errors must be included in E or paid separately, and a
finite-precision realization X+deltaX introduces D deltaX, which the row cap
alone cannot bound. In the exact saved operations R_num is exactly zero.

## 9. A real representation boundary and receiving change

Let L=path2, A=S2(L,L), C=P2(L,L), B=P3(L,A,C), and G=P2(A,B).
The actual graph G has 17 vertices, 20 edges, and maximum degree four. The
exact three-color port propagation yields no star state. A distinct direct
checker enumerated all 49,320 labeled proper three-colorings and found zero
star colorings. The new theorem supplies a star-four coloring, so its star
chromatic number is exactly four. This is a finite representation-specific
proof, not a lower bound against all acyclic three-colorings, arbitrary real
three-column designs, or nonlinear exact recovery algorithms.

The new operation was also received on the identical labeled Q8 support saved
by Cycle6: 1,788 vertices and 2,042 edges. The old unmodified even-series
three-color rule had inverse squared constant at least 16383/256, witnessed
by a supported matrix with action norm squared 256/16383. The new four-color
design has a recorded uniform inverse squared upper bound 2 on that support,
strengthened to 3/2 by the triangle-free addendum. Applied
to the same old cut matrix, its new four-column action has exact squared norm
2499892216/268402689 and reconstructs exactly. The old action was read from
its pinned native record, not replayed as new science. This is a receiving
repair of the failed rule, with one additional query fully charged. It is not
a universal impossibility for three queries and not a runtime comparison with
the best other design on Q8.

The root and independent receiving records also cover a 59-vertex mixed
expression containing arbitrary path leaves, both series parities, and all
four guarantee labels. Exact free diagonals, edges, nonzero rational noise,
full observations, outputs and projected-action equalities are saved. The
universal proof above supplies the all-noise claim; those instances check the
actual construction and implementation on the received inputs.

## 10. The grammar has a genuine missing degree-load interface

Every generated full network has an even number of degree-three vertices and
an even number of degree-four vertices: a series join creates degree two,
whereas each P2 creates exactly two degree-three vertices and each P3 creates
exactly two degree-four vertices. Old internal degrees stay fixed.

If deleting the two outer terminal leaves leaves a two-connected cyclic core,
the top production must be P_b. A top series production leaves an articulation
even after deleting those two leaves. The two top join vertices therefore have
degree b in the core. Removing them leaves exactly b nonempty connected child
interiors, each contributing exactly one incident edge at each join. All
degree-four core vertices are inherited inside children, so their count is even.

For L>=2, construct A_L from three branch vertices a,b,c: two internally
disjoint length-two paths a-b, two such paths a-c, and one length-L path b-c,
with all interiors disjoint. It has n=L+6, m=L+8, degrees 4,3,3 at a,b,c and
degree two elsewhere. It is simple, triangle-free, chordless, two-connected,
series-parallel and clique-cutset-free, with an explicit width-two decomposition.
There is exactly one degree-four vertex. Thus it cannot be a cyclic core of
the grammar, regardless of where the two exterior terminal leaves are attached.
The complete structural proof and small exact check are in
`research/grammar_scope/PROOF.md` and `RESULT.json`.

This is not graph hardness for recovery. The eight-vertex A_2 already has an
explicit ordinary star-three coloring. The failure is the degree-one port
representation: its productions create paired degree loads. The current
construction does include the core theta(2,2,2,L) for L>=4, using
P2(path(L-2),P3(path2,path2,path2)), so it does not simply discard the old
forced-transmission examples. It still chooses admissible ports and colors;
it does not solve the false arbitrary-equal-terminal assignment problem.

## 11. Comparators, dependencies, and continuation

Star-color compression and sparse-Hessian substitution are established [1,2].
The inverse analysis uses their ordinary coordinate incidence operation, not
a newly claimed recovery method. The new checkpoint contribution is the
realizable closed all-depth port construction, its all-parity/arbitrary-path
extension, and the actual receiving repair of a previously failing support.
Bounded primary searches did not establish historical novelty.

The inherited three-query forest design retains its sharper operator constant
sqrt(3/2) and Frobenius constant sqrt(2). The completed
odd-series grammar retains its three-query constant 5 for path2 leaves (and
its stated larger path-leaf guarantee); four queries do not dominate a lower
query count. The five-query full-spark construction remains the full-class
stable control. No NIST, molecular, physical, or downstream application speed
advantage is claimed. The Cycle5 99-vertex squared constant 20 is unchanged.

The selected next structural question is to replace the degree-one port by
actual degree-load signatures, beginning with loads (2,1) that generate A_L,
and determine whether a closed star-four interface covers a meaningfully wider
class of chordless degree-four SP atoms. Such a state must record multiplicities
and far-end flags, enforce the degree budget before joining, and provide actual
realizations. It may fail and must not be promoted to an arbitrary-boundary
theorem. Even a positive chordless result would leave triangle-containing
partial two-trees and the full arbitrary-real q4 question separate. This is
the next owned question, not an unexecuted theorem claimed in this return.

## References

[1] M. O. Albertson, G. G. Chappell, H. A. Kierstead, A. Kündgen, R. Ramamurthi,
*Coloring with no 2-colored P4's*, Electronic Journal of Combinatorics 11 (2004),
R26, especially Definition 3.1 and Lemma 3.2.
https://www.combinatorics.org/ojs/index.php/eljc/article/download/v11i1r26/pdf

[2] A. H. Gebremedhin, A. Pothen, A. Tarafdar, A. Walther,
*Efficient computation of sparse Hessians using coloring and automatic
differentiation*, INFORMS Journal on Computing. Primary author copy:
https://www.cs.purdue.edu/homes/apothen/Papers/hessian-coloring-joc.pdf

Primary-reading/search scopes and exclusions are retained in
`research/literature/FINDINGS_AND_STAR_PORTS.md` and the unchanged predecessor.
