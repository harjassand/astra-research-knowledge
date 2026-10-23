# Cycle6: an all-depth three-query construction on recursive series-parallel networks

Owner: Astra PRO2. Date: 22 October 2026.

## 1. The precise new claim and its limits

The construction below gives three coordinate actions with a dimension-independent
operator error bound on a class of arbitrarily deep, nonuniform series-parallel
networks of maximum degree four. The class admits branching and odd series
composition, including arbitrarily large chordless two-connected atoms. The
proof supplies the global boundary-mass invariant that was missing from a
local-piece argument. It does **not** color every degree-four partial two-tree.
In particular, even series composition is not a permitted production of this
construction. Section 7 gives an actual exponentially growing counterexample
to the most direct extension to that production.

The recovery contract is unchanged: G is known before the design is chosen;
D is any real symmetric matrix supported on G with arbitrary free diagonal;
each row of X has total Euclidean norm at most one; Y=DX+E has arbitrary absolute
Frobenius noise; the output error is the operator norm. All actions are on the
full original graph. No reduced action oracle or distributional noise model is
assumed.

For the base construction, the new all-size bounds are

    q=3,  maximum bichromatic tree order <=13,
    ||Dhat-D||_2 <=5 ||E||_F.                                  (1)

The same class contains cycles, which exclude every two-column real design for
exact recovery. Thus its worst-case exact and dimension-independent stable query
counts are both three. This does not improve the established three-query forest
constant sqrt(2), or imply a practical runtime advantage over any application
incumbent. The full treewidth-two, degree-four question remains four versus five.

## 2. A supplied graph grammar, with no recognition assumption hidden

Each network has two distinct ordered terminals s,t of degree one. Apart from
these terminals, different inputs to a production have disjoint vertices.

* L: a path of two edges, s-u-t.
* P_b, with 2<=b<=B: take b child networks, identify their left terminals at a
  and their right terminals at z, add new vertices s,t and edges sa,zt.
* S_l, with odd l>=3: concatenate l child networks in series, identifying the
  right terminal of each with the next left terminal. The outer terminals are
  those of the first and last child.

The main degree-four theorem uses B=3. There is no restriction on the recursion
depth, the number of nodes, the branching choices, the odd series lengths, or
the relative sizes of the children. A supplied construction expression is part
of the input. Validating its incidence and constructing the graph and colors is
charged. Recognition of an arbitrary graph as belonging to this grammar is not
provided for free.

Every produced graph is simple. Child terminals are nonadjacent, so P_b creates
no repeated edge. Its two join vertices have degree b+1 and its new terminals
have degree one. S_l creates degree-two join vertices. Thus Delta<=B+1. All
productions are series and parallel compositions of paths, proving treewidth at
most two. These claims also follow from the usual width-two decomposition of
a two-terminal series-parallel construction; the construction expression is
retained as a certificate rather than a graph-name assertion.

All base paths and all produced terminal paths have at least two edges. Every
simple terminal path is induced: this holds for a path, is preserved by series
composition, and at P_b a terminal path traverses exactly one child, with a new
edge at either end. There are no edges between different child interiors and
no edge az. Every cycle either lies in a child or consists of a terminal path
in each of two parallel children. Such a cycle has no chord. Consequently all
produced graphs are chordless and triangle-free. Removing the two exterior
degree-one vertices at a P_b node leaves a two-connected network: after deletion
of any vertex, every surviving part of a child meets at least one of a,z, since
every vertex lies on a simple terminal path, and the other child supplies a
connection. A two-connected chordless graph has no clique cutset: an adjacent
two-vertex cut would give two internally disjoint paths outside its shared
edge, making that edge a chord; singleton cuts and larger cliques are absent.
Thus the construction supplies unbounded chordless atoms, not merely a chain of
bounded local pieces. Its exterior stubs are retained in the actual support.

## 3. The coloring operation

Use three colors. For a network with prescribed distinct terminal colors (A,B),
let C be the third color.

* L receives the word A,C,B.
* At P_b set c(a)=B, c(z)=C, c(s)=A, c(t)=B, and color every child with ordered
  terminal colors (B,C).
* At S_l set the junction colors to A,B,A,B,...,A,B. Thus the child terminal
  colors alternate (A,B),(B,A),...,(A,B). The parity restriction makes the last
  child's ordered colors identical to the parent's.

The rule uses no optimization, numerical fit, or precision selection. It is
linear in the supplied expression and the output graph. Every edge is proper.

### Separation and acyclicity

Inductively, no bichromatic component meets both terminals. This is immediate
for L, whose path uses all three colors. At P_b, a bichromatic path between a
and z would have to traverse a whole child, which induction forbids. Hence
children can merge components at a or at z, but cannot connect those two join
vertices in any color pair. This excludes both a new bichromatic cycle and a
bichromatic path between the new s,t. At a series node, no child transmits
between its terminals; therefore a bichromatic component cannot pass through
a child to two consecutive series junctions. It meets at most one junction,
and the union remains a forest in each color pair. Acyclicity and separation
hold at every depth, independent of the mass bounds proved next.

## 4. The global boundary-mass invariant

For a network colored with terminal colors (A,B), denote by

    x = size of the {A,B} component at s,
    u = size of the {A,C} component at s,
    v = size of the {A,B} component at t,
    y = size of the {B,C} component at t.

Isolated retained terminal vertices have size one. All four quantities are
actual component sizes. Separation ensures that none of the components counted
at one terminal is also counted at the other terminal for the same pair.

The base vector is (x,u,v,y)=(1,2,1,2). For a P_b production, label each child's
four quantities relative to its own ordered colors (B,C). Direct union of
vertex sets gives

    u'=1,  v'=1,
    x'=2+sum_i(u_i-1),
    y'=2+sum_i(v_i-1).                                      (2)

The two possible new components at a and z which do not contain an exterior
terminal have orders

    1+sum_i(x_i-1),  1+sum_i(y_i-1),                         (3)

respectively. All other components are inherited unchanged. The subtraction
counts the shared terminal once; no independence or norm estimate is involved.

At an odd series production, the four outer masses are inherited from the first
or last child in the same relative slots. A component newly closed at a junction
is the union of one boundary component on each of its two neighboring children,
with their shared vertex counted once. No component can reach a second junction.

More generally suppose supplied leaf modules are properly and acyclically colored,
satisfy separation, have terminal degree one, maximum component order K0, and all
four boundary masses at most beta, where beta>=2. This mass statement does not
by itself impose a graph class on the modules: to retain the earlier support
claims, they must also be simple series-parallel networks of maximum degree
at most B+1; chordlessness and induced terminal paths are additionally required
if those structural conclusions are wanted. The path leaves satisfy all of
these conditions. Set

    R = 2+B(beta-1),
    K = max(K0, 1+B(R-1)).                                  (4)

The following simultaneous inequalities are closed under both productions:

    u,v <= beta;   x,y <= R;   all component orders <= K.     (5)

Indeed, (2) sets the low slots u,v to one and bounds the high slots by R. The
two orders in (3) are at most 1+B(R-1). A series node copies the outer slots.
Its new internal component has order at most 2R-1, which is at most 1+B(R-1)
because B>=2. In fact one high and one low slot meet, giving R+beta-1, but that
refinement is unnecessary. The unchanged child components already satisfy K.
Induction on the finite construction expression proves (5) for every size and
depth. This is the global reset: a parallel step sets both low slots to one,
and the permitted series steps cannot exchange low and high slots.

For L, beta=2,K0=2 and B=3 give R=5,K=13, proving the component claim in (1).
For B=2 alone the same argument gives R=4,K=7. These constants are certified
upper bounds, not asserted optimal.

### Optional arbitrary path leaves

Any path of length at least two can be colored with distinct terminal colors,
no transmitted pair, and component order at most four. For endpoints 0,1, use
0,2,1 for length two and 0,2,0,1 for length three. For length l>=4, color positions
0,...,l-2 by 012 periodically, choose position l-1 different from position l-2
and from 1, and append 1. The periodic prefix already contains all three colors.
The last two positions can enlarge a two-vertex bichromatic prefix component
by at most two vertices. Relabel the three colors for any ordered distinct
terminal colors. Thus beta=K0=4 is valid, and (4) gives K=31 for B=3.
This is an explicit optional enlargement, with a weaker error constant sqrt(61).
It is not a retuning of a completed strip result.

## 5. Recovery operation, proof for all real D and E, and exact query minimum

Take X_i=e_{c(i)} in R^3. Each row has norm exactly one. The cell (i,c(i)) of DX
is D_ii because the coloring is proper. For each color pair, the other selected
cells on a bichromatic tree T are its unsigned vertex-edge incidence action.
Choose one color's sign +1 and the other's -1, sign the observations, and project
them to zero mean. Root T arbitrarily. For a child edge e with subtree S of size
a in a component of size N, its reconstructed coefficient is

    w_e = sigma_child * [ sum_{i in S} f_i - (a/N) sum_{i in T} f_i ].   (6)

Keep the diagonal cells directly. Formula (6) is the exact least-squares inverse
of the tree incidence action; in a noiseless valid action it recovers every
coefficient, including the arbitrary free diagonal. The supplied production
code uses the inherited exact rational implementation unchanged.

For completeness, the operator error bound does not require a floating solver.
Fix a vertex and root one incident bichromatic tree there. Its incident branches
partition the other N-1 vertices. A signed sum of edge errors has a coefficient
vector equal to +1 or -1 on each branch and zero at the root. Mean projection
does not increase its Euclidean norm, so the absolute edge-error row sum from
this component is at most sqrt(N-1) times its selected action-noise norm. At a
vertex, distinct opposite colors use disjoint action cells. Adding the independent
diagonal cell and applying Cauchy-Schwarz bounds each absolute matrix row sum by
sqrt(1+r(K-1))||E||_F, with r<=2. Symmetry bounds the operator norm by this maximum
row sum. Hence K=13 gives 5||E||_F; K=31 gives sqrt(61)||E||_F. A graph-specific
smaller certificate uses 1+max_i sum_{T containing i}(|T|-1), and the inherited
cut and Frobenius certificates may be smaller still. The implementation keeps
the smallest proved bound and does not replace a stronger inherited one.

For a numerical decoder with supported symmetric output and rigorously bounded
residual Rnum=Dhat X-PY, where P is the described orthogonal action projection,
the allowance becomes C(||E||_F+||Rnum||_F). Rounding in residual evaluation must
be included. Perturbed acquisition X+deltaX adds D deltaX, requiring its own norm
bound; no such bound follows from the row cap. The coordinate rows use exact
0/1 entries. The saved receiving test is rational throughout, so its arithmetic
residual is exactly zero and no solver success flag substitutes for proof.

Finally, any support containing a cycle on k vertices excludes two real queries.
Restrict D to the k cycle edges and k free diagonal entries, giving dimension 2k.
For a k-by-2 design of rank two, symmetry forces X^T(DX) symmetric, a nonzero
linear constraint on the 2k output coordinates. Thus the action rank is at most
2k-1. For rank at most one, all output rows lie in a common at-most-one-dimensional
row space, so the rank is at most k. In either case a nonzero supported D lies in
the kernel. Extend it by zero outside the cycle. Every P_b network contains a
cycle, so q=3 is the sharp worst-case exact and stable count for this class.
This lower allows arbitrary graph-adapted real designs, unlike the failure in
the next section.

## 6. Charged construction and ordinary comparisons

Given an expression of length p, graph construction and coloring cost O(p+n+m)
arithmetic and storage. The supplied implementation is iterative, so it does
not impose a Python recursion-depth restriction on the mathematical class.
Preparation checks the actual graph, degree, properness, bichromatic forests,
and exact cut/row certificates. It takes O(nq+m) arithmetic and storage for fixed
q=3. Decoding has the same arithmetic order. If D is explicitly sparse, acquiring
its three actions is O(n+m) arithmetic; for an external action oracle its actual
three-call cost must be added instead. Rational bit complexity is not asserted
linear. Recognition, graph extraction, physical acquisition, and any downstream
spectral calculation are separate charged operations.

Ordinary controls remain: the three-query forest operation has constant sqrt(2);
the exact one-subdivision operation has three star colors for a three-colorable
original graph; the established general degree-four operation uses five full-spark
coordinates. The new family includes cycles and, at depth two, adjacent vertices
of degree four, so it is neither a forest nor an exact one-subdivision. This is
not by itself a historical novelty claim. The primary literature comparison is
in research/literature and RESULT.md. No NIST, molecular, application-time or
physical-performance improvement is claimed.

## 7. A decisive failure of the direct even-series extension

Allow a two-child series node with terminal colors (A,B), choose its shared
vertex color C, and color the children with (A,C),(C,B). Its two left boundary
slots are exchanged: parent x=child_left u, parent u=child_left x. The two right
slots are exchanged analogously. Separation and acyclicity still hold, but the
low/high invariant is no longer closed.

This is not just a failed inequality. Let Q0=L. For h>=1, let Qh be P_2 of two
copies of S_2(Q_(h-1),L), using precisely the color rules above. All supports are
actual simple triangle-free series-parallel graphs of maximum degree three.
If x_h is the {A,B} component size at the left outer terminal, the exact update is

    x_0=1,  x_h=2+2(x_(h-1)-1)=2x_(h-1),  hence x_h=2^h.     (7)

Thus this natural extension has exponentially growing bichromatic trees despite
properness, acyclicity, no terminal transmission, and uniformly bounded local
pieces. The inherited bounded-degree cut lower gives an inverse constant at least
sqrt((2^h-1)/6). The new script also emits an exact cut witness for the actual
finite failed design, with no floating singular-value assertion.

Equation (7) closes this specific unmodified extension. It does not exclude a
different coloring of Qh, recoloring, a different finite state, four coordinates,
or an arbitrary real design. The example is a failed design family, not a hard
graph family for all designs. It identifies the next precise obligation: handle
general series parity and separator states without allowing a high mass to feed
back into a low slot before the next branching step.

For h>=2 the specified left boundary tree consists of one hub, its terminal
leaf, and two branches of size 2^(h-1)-1. A branch cut therefore has

    Gamma = ((2^(h-1)-1)(2^(h-1)+1))/2^h
          = 2^(h-2)-2^(-h).                                 (8)

The cut's signed divergence, uniform with values 1/a and -1/b on the two sides,
gives a supported symmetric witness with a unit coefficient on that edge and
action norm squared 1/a+1/b. Thus the inverse lower is sqrt(Gamma), stronger
than the coarse degree bound above. At h=8 the actually materialized support
has n=1788,m=2042, and the checked exact lower squared is 16383/256. Symbolic
all-size counts are n_h=7*2^h-4 and m_h=8*2^h-6; enormous graphs were not built.

## 8. Dependencies and scientific status

The old degree-free cut theorem, coordinate decoder and exact source chain are
preserved. The proof above restates the row certificate needed for the new
operation, so its stability assertion can be checked without a hidden prior
lemma. The bounded theta-interface contribution independently identifies forced
transmission and invalid equal-terminal states; it is integrated as a constraint
on the broader frontier, not silently promoted to a full atom construction.
Internal proof review, exact executable verification, historical originality,
efficient implementation, and physical usefulness remain separate claims.
