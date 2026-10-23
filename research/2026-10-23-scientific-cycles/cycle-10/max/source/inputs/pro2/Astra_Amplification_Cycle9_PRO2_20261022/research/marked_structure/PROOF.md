# Actual marked vertices in chordless width-two atoms

Contributor: `/root/cycle8_structural_scope`, Cycle9, 22 October 2026.
This is a marked structural interface theorem using the completed native
Cycle8 atom proof. It changes neither the original support nor matrix actions.
It does not grant simultaneous guarantees at several marked vertices.

## 1. Scope and source

Let G be a finite simple two-connected chordless graph of treewidth at most
two and maximum degree at most four. A vertex v is actually specified in the
input and has degree two or three in G. It is not a convenient port chosen
after seeing a coloring. Use the exact loaded grammar H8 and its completed
four-color guarantee families from Cycle8.

Read actual `cycle8_pro2/PROOF.md`,
`cycle8_pro2/research/structural_scope/ALL_CHORDLESS_ATOMS.md`, and
`cycle8_pro2/src/atom_normal_form.py`. The latter currently chooses a
convenient port pair. Its current implementation cannot be cited as if it
made an arbitrary marked vertex a port. The lemmas below describe the actual
required changes or contexts.

The only nontriangle atoms in this class are triangle-free, by the received
chordless-atom argument. C3 is a separate explicit case in Section 5.

## 2. Every degree-three marked vertex can be a real H8 terminal

**Theorem 1.** If deg_G(v)>=3, then there is an original nonadjacent vertex w
such that G has a support-preserving H8 expression with terminals v,w. In
particular this applies to the requested degree-three marked roots. No new
leaf or edge is attached to v.

**Proof.** Choose an actual edge vu incident to v and protect it during the
Cycle8 degree-two suppression. This gives an ordinary edge-rooted TTSP
expression. The protected edge has only parallel ancestors. After flattening
them, chordlessness gives exactly one other branch H, so

    G=P(edge vu,H).

Its actual terminal load at v is deg_H(v)=deg_G(v)-1>=2. Follow the v-terminal
side of the ordinary expression H. At a series node, that side belongs to
exactly one child and its load is unchanged. A single-edge leaf has load
one, so the traversal cannot end at a leaf while retaining load at least
two. It therefore reaches a parallel node N with v as one terminal; write
its other terminal as w.

The exact complement C_N is TTSP by the Cycle8 ancestor-context formulas.
The whole original graph is the parallel join of the at least two children
of N and C_N. These give at least three internally disjoint nonempty v-w
branches. If vw were an edge, paths through two other branches would form
a cycle chorded by vw. Hence v,w are nonadjacent. Every simple v-w path
lies within one branch; closing it through another branch shows that it
is induced, since G is chordless.

Normalize this ordinary expression by the already-proved binary rules:
edge+edge becomes path2; edge+module becomes a left extension;
module+edge becomes a right extension; module+module remains series; parallel
has only non-edge children. This is a decomposition of actual original
edges, not permission to add a stub. It preserves v as an outer terminal,
all original vertex IDs, and every actual degree budget. QED.

This also proves port eligibility for degree-four vertices, but their
attachment budget is zero and H8 correctly treats them as saturated. The
degree-three port remains active and retains its actual color/support/flag
record. It does not have an arbitrary prescribed neighbor-color profile.

### Concrete preparation change

Allow the protected edge in the Cycle8 normalizer to be an input edge incident
to v. In H, select the terminal-side child at each series node until the first
parallel node, rather than selecting an arbitrary parallel descendant.
Reroot there with its exact complement, then run the unchanged support-
preserving normalization. This has the same asymptotic preparation cost as
the native operation: linear graph/expression work under the degree cap,
with canonical sorting charged separately as in the actual implementation.

## 3. A real degree-two vertex need not be an eligible terminal

**Counterexample.** Let G=K_(2,3), with hubs a,b and middle vertices v,w,z.
Mark the actual degree-two vertex v. The graph is simple, two-connected,
chordless, of maximum degree three, and of treewidth at most two. A width-two
decomposition has bags {a,b,v}, {a,b,w}, {a,b,z} joined in a path.

The only vertices nonadjacent to v are w and z. If the second terminal is w,
the simple terminal path

    v-a-z-b-w

has both v-b and a-w as chords. For second terminal z, interchange w,z.
Therefore no nonadjacent second terminal makes every simple terminal path
induced. That property is necessary for H8 membership, so v cannot be an
H8 terminal under any rerooting of this unchanged graph.

The structural hypotheses are direct. Deleting one hub leaves a star and
deleting one middle vertex leaves a four-cycle, so there is no cut vertex.
All cycles use the only two hubs and hence have length four, with no chords.
The above bags prove the width bound. This is a failure of the arbitrary-
marked-terminal ansatz, not a coloring or recovery lower bound on K_(2,3).

## 4. Universal marked-midpoint representation for degree two

**Theorem 2.** Let deg_G(v)=2, with neighbors a,b, and assume G is not C3.
Then ab is not an edge and there is an H8 expression H for the exact graph
G-v, with terminals a,b, such that

    G=P(path2(a,v,b), H).

The mark v is the original midpoint of the displayed original length-two
path. The loads of H are deg_G(a)-1 and deg_G(b)-1, each in {1,2,3}; both
are active ports. This representation exists for every specified degree-two
vertex, including the K_(2,3) counterexample above.

**Proof.** If ab were an edge, a,v,b would form a triangle. The received
two-connected chordless triangle lemma would then force G=C3, excluded here.
Thus a,b are nonadjacent.

Suppress v in the auxiliary graph, replacing its two-edge path by a formal
edge ab. This is a minor and remains two-connected and of treewidth at most
two, by the Cycle8 suppression proof. Protect that formal edge and construct
an ordinary edge-rooted TTSP expression. Its parallel siblings, excluding
the distinguished formal edge, form an ordinary TTSP network H whose edges
are exactly those of G-v. There can now be several siblings: the auxiliary
graph need not be chordless, and the native normalizer's one-sibling test
must NOT be applied here. Join all siblings in parallel when necessary.

Return to the original graph by replacing the distinguished formal edge with
the original path a-v-b. No new edge is included in the final support or in
any matrix action. This gives exactly G=P(path2(a,v,b),H), with disjoint
interiors and nonadjacent terminals.

Every a-b path in H, closed through the original a-v-b path, is a cycle of
G. Consequently it is induced. Also H has no terminal edge ab. Its ordinary
TTSP expression therefore normalizes into H8 by the received induced-path
normalization theorem. The actual H terminal degrees are the original degrees
minus the one edge incident to v, so they are between one and three. The final
parallel sums equal the original degrees, at most four. QED.

The formal suppression edge is an auxiliary representation device that is
removed before constructing the design; it is not an added physical/matrix
edge, a queried coefficient, or a reduced-action observation. The inverse
continues to use every original edge of G and all original actions.

### Exact marked profile from the two active ports

Give the two H terminals actual colors A,B and the marked midpoint color Z,
where Z differs from both A and B. Suppose an actual valid star coloring of
H is supplied and the actual parallel join with this path2 coloring passes
the H8 merge tests. Let N_a,N_b be the actual neighbor-color supports at the
two H ports. The full original graph then has the following exact one-port
record at v:

    color(v)=Z, degree(v)=2,
    N_v={A,B},
    F_v=({A} if Z in N_a else empty)
        union ({B} if Z in N_b else empty).

The formula is direct: the other neighbors of a and b are exactly their H
neighbors. It remains valid when A=B, but the actual merge tests must still
be passed; in that case a far-end repeat at either side would combine with
the two equally colored neighbors of v and be rejected.

If H is supplied by a Cycle8 upper-bound target rather than an exact profile,
replace N_a,N_b by their certified upper bounds to obtain an upper bound for
F_v. Neighbor colors A,B and degree two remain exact. Actual realizability
comes from the existing child guarantee and a valid path2/parallel witness,
not from a syntactic mask alone. All relabelings are global color permutations.

This gives a finite genuine receiving operation on the old H8 families:
take an actual active-load family for H, use a valid path2 parallel witness,
and project the resulting realization to the original marked midpoint.
Nonemptiness is inherited from the complete degree-admissible H8 parallel
closure. It need not supply every imaginable rooted profile or independently
qualify a second mark in the same atom.

### Preparation and actual inputs

The auxiliary graph has one fewer vertex and one fewer edge. The protected-
edge suppression and extraction of all nonformal siblings use linear graph/
expression work under the degree cap. Normalize H and retain the actual path2
with mark v. The output still names precisely the original support. Sorting,
expression validation, expanded output, bit costs, and the actual full matrix
actions must be charged by an implementation. No old closure search is needed.

## 5. Triangle and simultaneous-mark limits

For C3, every marked vertex has degree two. The ordinary three-color triangle
coloring has two distinct neighbor colors and empty far-end flag set at the
mark. This is an explicit exceptional rooted profile; it does not belong to
the nonadjacent-terminal H8 grammar.

Theorems 1 and 2 qualify **one actual marked vertex at a time**. They do not
say that separately selected profiles at two or more different vertices of
the same atom have a common realizing coloring. That compatibility is a real
global condition. In particular, applying the one-mark theorem independently
at two cut vertices of a central atom is not a valid gluing proof.

The root's new Cycle9 multi-attachment obstruction must be assessed at that
stronger simultaneous-mark contract. The present structural lemmas neither
override it nor convert any star-color obstruction into an arbitrary-real
four-query impossibility. The full width-two degree-four recovery question
and the choice of a weaker stable representation remain separate.

## 6. What was received and what changed

The received Cycle8 normal form, complement rerooting, induced-path lemma,
and active-port color/support/flag guarantees are used concretely here.
They yield two different correct marked interfaces: an actual degree-three
terminal and a distinguished original path2 midpoint for degree two. The
K_(2,3) counterexample proves that combining these into an alleged universal
terminal-root interface would be false.

This is structural mathematical progress, not a benchmark advantage or a
claim of historical novelty. No completed old finite suite was rerun.
