# A four-query local decoder from degree-four 2-tree completions

Contributor: /root/degree4_structure, 22 October 2026 Australia/Brisbane.
This is a bounded structural contribution to the owner's four-versus-five
question. The main theorem below covers genuine 2-trees of maximum degree four
and their subgraphs. It does not cover every partial 2-tree of maximum degree
four: adding a 2-tree completion can violate the degree cap. The full owner's
question remains open from this contribution alone.

## 1. Precise constructive theorem

Let H be a 2-tree of maximum degree at most four on n>=3 vertices, supplied
with a construction starting from a triangle and repeatedly adding a new vertex
adjacent to the two ends of an existing edge. Let G be any known subgraph of H
on the same vertex set. Every diagonal is free. There is an explicitly
constructible rational n-by-4 query block X with all row norms at most one and
an explicit linear local decoder L such that, for every real symmetric D
supported on G and every action error E,

    ||L(DX+E)-D||_2 <= ||L(DX+E)-D||_F <= 20 ||E||_F.

The cap is on the ENTIRE query row. Noise is absolute Frobenius noise on the
ENTIRE observed block; no independence, relative-error or noiseless-action
hypothesis is used. Preparation and decoding require O(n) fixed-size arithmetic
operations with the supplied construction. Four operator actions still have
their actual acquisition cost. All local maps have fixed rational coefficients.
The proof holds for all real coefficients; the supplied executable uses exact
Fraction arithmetic on actual finite inputs.

The query budget is sharp in the worst case for this subclass, conditional on
the accepted all-design three-query squared-path lower theorem in the owner's
unchanged predecessor source, because the subclass contains every P_n^2.
The upper proof below is elementary and independent of that inherited lower.
Historical originality of this four-query operation is not established.

## 2. Local graph structure and the exceptional book

The graph induced by the neighbors of a vertex in a 2-tree is a tree: at the
vertex's creation its two neighbors are adjacent, and each subsequent neighbor
adds a leaf to this link. Thus a degree-four vertex has a four-vertex tree as
its link, either a path P4 or a star K1,3.

The star case forms a three-page book: adjacent apices u,v with three common
neighbors a,b,c. Both apices have degree four. In any graph of treewidth at
most two containing this book and with maximum degree four, each component
outside the book meets at most one of a,b,c. Otherwise an outside path between
two pages completes the K4-minus-one-edge on u,v and those pages to a K4 minor.
Outside attachment to an apex is forbidden by its saturated degree. A 2-tree
is 2-connected, so a genuine 2-tree containing this book must be exactly the
five-vertex book.

That finite exception has a three-star-color coordinate decoder: give the
apices colors0,1 and every page color2, pad a fourth query by zero. Every
diagonal is isolated in its own-color reading. Read each apex-page edge from
its page endpoint and the apex edge from either apex. The selected cells are
distinct, giving the standard Frobenius constant sqrt(2).

For every other genuine 2-tree in the theorem, no edge belongs to three
triangles. The graph of triangles joined across their common edges is a tree:
each newly added triangle attaches to the unique existing triangle at its
parent edge. Its running-intersection property follows from the construction.

## 3. Six-vector palette, four directions

Give the root triangle colors0,1,2 and signs+1. For each added vertex w on edge
uv, assign the missing color. The parent edge lies in exactly one earlier
triangle; let z be its third vertex. Then w and z have the same color. Set

    s_w = -s_z.

This assigns opposite signs to the same-color opposite vertices of every
diamond (two triangles sharing an edge). There is no inconsistency because
the triangle adjacency is a tree and each new vertex is assigned once.

Equivalently, for a fixed color contract each connected set of triangles
containing the same vertex of that color. The quotient is a tree whose edges
join the opposite vertices of diamonds. The signs are its bipartition. This
description makes the graph-adapted consistency condition explicit.

Set

    x_v = (e_{color(v)}, s_v)/2 in R4.

These six possible rational rows have squared norm1/2, within the total cap.
At a degree-four vertex the link is P4, whose proper two-coloring has two
vertices of each color. Each same-color pair forms the opposite vertices of
a diamond and therefore has opposite signs. At a degree-three vertex the
link is P3, and its repeated-color pair likewise has opposite signs.

## 4. Local row maps and their exact inverse bound

For vertex v let M_v have as rows x_v and all x_w for neighbors w. A coefficient
row d_v acts as M_v^T d_v. If deg(v)<=3, these rows are linearly independent.
If deg(v)=4, M_v has rank four and a one-dimensional coefficient kernel.

The pseudoinverse of M_v^T has norm at most4. To see this for degree three,
temporarily omit the division by2 in the query rows. Use the own-color
coordinate to read the diagonal a and the singleton other-color coordinate
to read r. The duplicated other-color coefficients p,q obey

    p+q = y_B,
    p-q = y_4 - s_v a - s_single r,

after ordering the pair by its signs. The inverse's four rows have squared
norms1,1,1,1, so its Frobenius norm is2. Restoring the query division by2
gives norm at most4. Lower-degree cases have an immediate coordinate left
inverse of norm at most2. A degree-four neighborhood contains one of the
full-rank four-row configurations just analyzed; adding a row cannot reduce
the smallest nonzero singular value of the full-column-rank matrix.

Define eta(A,B)=eta(B,C)=eta(C,A)=+1 and reverse signs on reversed color pairs.
At a degree-four vertex the unnormalized kernel row c_v has zero diagonal and

    c_vw = eta(color(v),color(w)) s_w

on each of its four neighbors. Its squared norm is4. The group sums vanish
because each same-color pair has opposite signs, and the fourth-coordinate
sum is two plus signs and two minus signs. This proves the kernel formula.

For actual noiseless data decompose each row orthogonally as

    d_v = r_v + rho_v c_v,

where r_v is the minimum-norm local coefficient solution. Set rho_v=0 at
vertices of degree at most three. Then

    ||r||_F <= 4 ||DX||_F,
    ||D||_F^2 = ||r||_F^2 + 4 sum_{v high} rho_v^2.

## 5. Symmetry, odd cycles and a bounded local decoder

Put z_v=rho_v/s_v at high (degree-four) vertices, and z_v=0 at low vertices.
For an edge vw define from the known local particular rows

    g_vw = eta(color(v),color(w)) s_v s_w (r_wv-r_vw).

For a high-high edge, symmetry of D gives g_vw=z_v+z_w. For a high-low edge
it gives g_vw=z_v. These are unit-magnitude, negative connection gains; an
unbalanced generic-gain Cheeger claim is not being used.

Each high vertex v has a triangle through it. If it has any low neighbor w,
recover z_v=g_vw. Otherwise choose a triangle v,u,w (all its vertices are high)
and recover

    z_v = (g_vu+g_vw-g_uw)/2.

This is an exact local formula. The choices can be deterministic by vertex
indices. Recover rho_v=s_v z_v, add rho_v c_v to each particular row, and
orthogonally project the result onto symmetric supported matrices. For G a
proper subgraph of H, additionally zero the forbidden coefficients. Both
projections are contractions in Frobenius norm and preserve the true D.

For arbitrary noisy data, let delta r be the difference between the computed
local particular rows and the noiseless ones. Fixed local pseudoinverses give

    ||delta r||_F <= 4||E||_F.

Edge differences satisfy

    sum_edges |delta g_vw|^2 <= 2||delta r||_F^2.

In the triangle formula, Cauchy gives

    |delta z_v|^2 <= (3/4)(|delta g_vu|^2+|delta g_vw|^2+|delta g_uw|^2).

Any edge can occur in the chosen triangles of at most four vertices: its two
endpoints and at most two common neighbors. A high-low direct anchor edge is
used by at most its high endpoint and does not occur in an all-high triangle.
Therefore

    sum_high |delta z_v|^2 <= 3 sum_edges |delta g_vw|^2
                             <= 6||delta r||_F^2.

Every delta r_v is orthogonal to c_v, since both local particular solutions
are chosen in the orthogonal complement of the same kernel. Before final
symmetrization the reconstruction error consequently has squared Frobenius
norm at most

    ||delta r||_F^2 + 4 sum |delta z_v|^2
       <= 25||delta r||_F^2 <= 400||E||_F^2.

This proves the announced constant20, including arbitrary correlated action
noise. Finite local rank alone would not supply this estimate; the unit gain,
triangle recovery and bounded reuse of measurements are the global obligations.

## 6. What this subclass actually contains

The class of genuine 2-trees with maximum degree four is particularly narrow:
it consists of squared paths P_n^2, the five-vertex three-page book, and the
six-vertex three-sun (a triangle with one new vertex on each edge).

Proof: the book case was handled above. Otherwise the triangle dual is a tree.
If a dual triangle has three neighboring triangles, its three vertices already
have degree four. Each neighboring triangle has two of these saturated
vertices, so it cannot have any further neighboring triangle. Connectedness
forces the complete graph to be the three-sun. In every other case the triangle
dual is a path T1,...,Tk.

Along this path each vertex lies in a consecutive interval of triangles and
its degree is one plus the interval length. For k>=4, the unique T1-only
vertex has degree2. The vertex removed at T2-to-T3 must be an original T1
vertex: removing the newly introduced T2 vertex would give three triangles
sharing the same edge. Thus this second vertex has degree3. The last end
similarly has a degree2 and a degree3 vertex, distinct from the first two.
For every 2-tree, sum_v(4-deg(v))=6. These four end vertices use all six units,
so every other vertex lies in exactly three triangles. The bags are therefore
forced to have the form {v_i,v_(i+1),v_(i+2)}, giving P_n^2. k<=3 is direct.

Consequently the most useful general receiving class is symmetric bandwidth-two
supports with a supplied ordering, including subgraphs of the squared path.
The accepted all-design three-query obstruction plus this decoder settles that
class's worst-case stable minimum at four. The broad degree-four partial-2-tree
class still includes branching supports with no degree-preserving completion.

As a simpler intermediate structural bound, any 2-tree construction prefix
has total degree deficit6. It has at least two degree-two vertices, proved by
removing the last added vertex and inducting; for at least four vertices they
can be chosen nonadjacent (the three-vertex initial triangle is harmless).
Thus at most four prefix vertices have degree<=3. Every vertex with a future
neighbor belongs to that set, giving a construction frontier of size<=4.
For a partial 2-tree with a supplied 2-tree completion missing delta edges,
the analogous prefix count is at most6+2delta, giving pathwidth<=6+2delta.
Neither frontier bound, by itself, is a noise-stability theorem.

## 7. Structural approaches explicitly ruled out

Low-degree anchors need not be within bounded distance. In P_n^2 only the
first two and last two vertices have degree<=3, while central distance to them
is unbounded. The exact n=100 check gives distance24. A finite rooted tree with
root degree4 and three children at each later internal vertex has all internal
vertices of degree4 and an arbitrarily deep degree-four core; forest treewidth
does not force that core to have bounded pathwidth.

A deep saturated tree also need not have a degree-four 2-tree completion.
Take an internal vertex all four of whose neighbors already have degree4.
In a 2-tree its neighbor link must be a tree, requiring new edges between
currently nonadjacent neighbors. Every such new edge violates the degree cap.

Even adding 2-connectedness does not force bounded bandwidth or bounded
pathwidth. Let T_h be the complete rooted binary tree of height h, and form
Q_h=T_h square K2: vertices are (v,0),(v,1); include each rung
(v,0)(v,1), and both copies of every edge of T_h. Then Q_h has
n=2(2^(h+1)-1) vertices and maximum degree4. It is 2-connected for h>=1:
after deleting one vertex, the other layer is a connected copy of T_h, and
each surviving vertex in the affected layer is connected to it by its rung.
It has treewidth exactly2: start with the root rung and attach a four-cycle
for each child along its parent's existing rung. A four-cycle has a width2
decomposition containing both its opposite rungs in bags, and gluing these
decompositions along a bag containing the shared rung preserves width2.
The graph contains a cycle, so width1 is impossible. Its diameter is2h+1.
For any labeling with bandwidth b, the path between the vertices labeled1
and n has at most2h+1 edges, so n-1 <= b(2h+1). Thus its minimum bandwidth
is at least [2(2^(h+1)-1)-1]/(2h+1), which diverges. No claim about four-query
recovery follows from this counterexample. In particular, it is not an
all-design query lower bound. The independent pathwidth assertion can be
seen by contracting all rungs to recover T_h, whose pathwidth is unbounded;
the elementary bandwidth bound above already defeats the bounded-bandwidth
shortcut without relying on that additional standard tree fact.

There is a useful but conditional planar expansion observation. Removing all
vertices on triangles or quadrilaterals leaves induced girth at least five.
For any subset S of remaining degree-four vertices, planarity gives
|E(S)|<=(5/3)|S|, hence at least(2/3)|S| edges leave S. This is a uniform
Dirichlet expansion statement, and would support unit-gain energy estimates.
It does NOT automatically control arbitrary bounded unequal endpoint gains.

Explicit weighted-gain failure: use the depth-H rooted tree with four children
at the root and three at later internal vertices. Give edge p-to-child the
energy (z_child-z_parent/2)^2; set z_v=2^(-depth(v)) on internal vertices and
zero at boundary leaves. All interior edge energies vanish. Boundary energy
is (4/3)(3/4)^H, while the root amplitude is one and total squared amplitude
remains bounded. Both endpoint coefficients remain between1/2 and1. Thus a
bounded gain ratio plus tree expansion is insufficient. The decoder above
avoids this failure by proving exact unit-magnitude negative gains.

## 8. Source, costs and comparisons

decoder.py validates an actual 2-tree construction and its degree bound,
constructs the signs and six-vector rational palette, computes fixed local
pseudoinverses, and implements the triangle/anchor decoder. check.py was run
once, with exact noiseless and deterministic-noise tests on P_32^2, P_128^2,
the three-sun and book. RESULT.json records all squared norms and the exact
local inverse-trace checks. This is producer-side execution, not independent
verification or a finite substitute for the proof above.

Observed computation body:0.037431175 seconds wall,0.037432581 seconds CPU,
peak RSS10878976 bytes. Imports, source reading, mathematical development,
authoring, messaging and service/inference overhead are additional and not
fully measured. No optimizer, precision sweep, old scientific replay, package
installation or paid compute was used. No failed computational run was omitted.
The rejected structural premises above affected the construction and are
retained. The early pathwidth<=4 argument was sharpened by the classification.

The five-query full-spark construction remains the comparator for all degree-
four supports. On the narrower bandwidth-two class, a stronger five-query
comparator is periodic coordinate rows with period five: every closed band
neighborhood has distinct coordinates, yielding rowwise Frobenius constant1
after symmetrization. The new theorem uses one fewer action with the conservative
bound20. It establishes no conditioning or end-to-end runtime improvement over
that five-query operation. Four actions, supplied ordering/construction,
O(n) query/preparation/decoding work, action error and arithmetic error all count.
The actual implementation uses exact rationals; a floating implementation must
bound its additional local arithmetic error. No NIST or molecular advantage
is claimed, and no historical-originality claim is made.
