# Four original actions on chordless degree-four partial two-trees, including bridges

Pro2, 23 October 2026. A new theorem relative to the exact Cycle10 checkpoint.
This is an internally checked mathematical construction, not a claim of
historical priority, external acceptance, or application speedup.

## 1. Contract, theorem, and dependencies

The finite simple support G is known before choosing the real n-by-q matrix X.
The unknown D is an arbitrary real symmetric matrix on the ORIGINAL support,
including an arbitrary diagonal. Every WHOLE row of X has Euclidean norm at
most one. The observations are all original Y=DX+E, with arbitrary absolute
Frobenius noise E. The output must equal D when E=0, and its operator error
must have a constant independent of graph size. Preparation, actions, precision,
residual certification and sparse output are part of the operation.

**Theorem 1.** Every finite chordless graph G of treewidth at most two and
maximum degree at most four admits a constructively obtained proper coordinate
four-color design X and its canonical least-squares inverse satisfying

    ||Dhat-D||op <= ||Dhat-D||F <= 3 sqrt(2) ||E||F.

Disconnected graphs and isolated vertices are included. Chordless means that
no cycle has a chord; triangles are permitted. There is no limit on the number
of bridges, block depth, number of attachments, atom size, or path length.
Every original vertex and edge is retained in every action and in the output.
The implementation starts from n and the original edge list. It does not need
a favorable root, a supplied decomposition, or actions on a reduced graph.

The same proof gives the slightly stronger sufficient squared constant

    2L = 3 beta+1+sqrt((3 beta-1)^2+8 beta),
    beta=(3+sqrt(5))/2,

which is strictly less than 18. Neither expression is claimed to be the sharp
operator inverse norm. On bridgeless inputs the accepted stronger squared
constant 3+sqrt(5) remains available; this theorem does not replace it with 18.
The native finite component certificates may also give stronger instance bounds.

Four is the worst-case uniformly stable COORDINATE minimum on this class,
even allowing signed unequal one-coordinate row amplitudes: the Cycle9 chains
of K_(2,4) are bridgeless chordless members and already exclude three-coordinate
uniform stability. That lower theorem is preserved, not reproved here. It does
not exclude arbitrary real three-column designs on this subclass. On the full
class tw<=2, Delta<=4, arbitrary-real q3 is excluded and q5 is sufficient;
arbitrary-real q4 remains open because nonchordless blocks are not covered here.

The exact constructive dependencies are:

* The accepted H8 semantic realization and intrinsic marked normalizer in the
  unchanged Cycle8/9 sources embedded through the exact Cycle10 ZIP.
* The Cycle10 degree-two marked-root guarantee, its one-message block gluing
  theorem, and the arm-at-most-two spider Poincare inequality.
* The new degree-three projection, with all 18 literal witnesses in
  sources/DEGREE3_PROJECTION.json, and the intrinsic reduction below.
* The new bridge-leaf classification and quantitative extension lemma proved
  in Sections 4-7. A finite receiving example is not their all-size proof.

The fixed H8 certificate is 982,625 bytes with SHA256
63f4cdfd7ccc3b3159782a28a144a199422a315975aa207e5d144e8659e53525.
No inherited closure search or old scientific receiving suite was rerun.

## 2. An actually specified degree-three root has a missing channel

**Lemma 2.** Let B be a two-connected chordless graph with tw(B)<=2 and
Delta(B)<=4. For every actually specified degree-three vertex r, there is a
constructive star-four coloring c such that the colors of its three actual
neighbors occupy at most two colors. Consequently a color z distinct from
c(r) is missing from its neighbor support. One global permutation can map
c(r) and z to any two prescribed distinct colors.

Choose any actual incident edge rv. Subdivide that edge temporarily with w.
Subdivision preserves two-connectivity, chordlessness and the maximum-degree
bound. It preserves treewidth two: attach the bag {r,v,w} to a bag containing
r,v in a width-two decomposition, then remove the original edge. Apply the
accepted degree-two marked normalizer at w. Its network after deleting w is
exactly H=B-rv, with ordered terminal degrees (2,d), d=deg_B(v)-1 in {1,2,3}.
Every terminal-to-terminal path in H is induced, because adding the original
edge closes it into a cycle of the chordless original graph. Thus the accepted
normalizer coverage theorem and fixed H8 families apply. The temporary vertex
is only a preparation device: it is not a row of X or an action coordinate.

An H8 signature is (a,b,dL,NL,FL,dR,NR,FR). The terminal colors/degrees are
exact, NL and NR upper-bound neighbor-color support, and FL,FR upper-bound
far-repeat flags. A flag b at the left means that some b-neighbor has another
neighbor of color a. Start with an actual star coloring of H realizing a target.
Restoring the original edge rv preserves the star property exactly when

    a != b,
    b not in FL,
    a not in FR,
    not (b in NL and a in NR),

where for necessity the sets are the actual supports/flags. A new bichromatic
P4 must contain the newly restored edge. If it is an end edge, one of the two
flag exclusions applies; if it is the middle edge, the last exclusion applies.
These exhaust all positions. Properness is exactly a!=b. Applying the same
conditions to upper bounds is sufficient and downward closed.

The root's restored neighbor support is contained in NL union {b}. The new
literal projection chooses an old realizable target with this union of size
at most two in EVERY relevant family. The complete family list is

    2,4,12,14,19,24,26,30,31,33,40,44,45,52,53,54,62,63.

For each, the saved row identifies the exact old target index, all eight target
entries, actual degrees, edge-closing predicates, and a missing color. A separate
standard-library-only checker verifies all 18 rows against the bound source.
The inherited semantic theorem then realizes the chosen target at every network
normalizing to that family. This finite projection plus the all-size normalizer
coverage, not six successful test graphs alone, proves Lemma 2.

src/degree3_atom.py expands the old transition witnesses, maps colors back to
the ORIGINAL IDs, restores the original edge, and checks the actual original
star coloring and neighbor multiplicities. In the native degree-three-to-four
case the actual profile can have a nonzero far flag. No stronger all-unflagged
claim is used. The proof and complete local source are also preserved under
research/degree3_interface/.

## 3. One qualified entry in a whole bridgeless module

Delete every bridge of G. Its resulting connected components are called
modules; singleton modules are kept. Nontrivial modules are bridgeless and
have minimum internal degree at least two. Contracting them yields a forest,
because any cycle of quotient bridges would put each of those edges on a
cycle of G. Multiple quotient edges between the same two modules are excluded
for the same reason. Root each quotient tree.

For a nontrivial nonroot module M, let r be the ACTUAL endpoint of its one
incoming bridge. Its internal degree is two or three: the incoming bridge
uses one unit of the full degree budget. Furthermore r belongs to just one
nontrivial atom of M. Membership in two atoms would already contribute at
least two plus two internal neighbors, leaving no bridge budget.

Root M's actual atom tree at the unique atom containing r. If r has degree
two, use the accepted marked-root star-four coloring: its two neighbors have
distinct colors, so one of the three nonroot colors is missing. If r has
degree three, use Lemma 2. A triangle is covered by the degree-two case. The
root color and one missing neighbor color can be mapped to two prescribed
distinct colors by one global permutation of this actual root atom coloring.

All remaining atoms of M are handled by the unchanged Cycle10 rule. At a cut
r' the local degrees are two and two. The child takes one actual marked
coloring with distinct root-neighbor colors and at most one flagged channel.
It can be permuted to share at most one parent neighbor channel, unflagged in
the child. That shared component is precisely an isolated edge r'-u. If u is
a cut, the next child is asked to avoid color(r') at u. This is one genuine
request to the NEXT coloring, not several independently chosen profiles in
one already colored atom. The accepted permutation argument handles it.

The inherited gluing theorem requires only an arbitrary star-four coloring
of its root atom; it never required that root itself have degree two. Thus
the new root qualification is compatible with it. Every bichromatic component
inside M remains an arm-at-most-two spider. No other atom meets the entry r,
so its missing neighbor color is unchanged by the rest of the internal gluing.
The root module of a quotient tree needs no bridge qualification and uses
the same inherited operation with a convenient degree-two atom root.

This realizes the single entry interface. There is no assertion that several
arbitrary marks in M can be qualified independently, and no coloring of M is
revised in response to later children.

## 4. The complete bridge rule

Process modules in quotient-tree order. If a child module's entry vertex r
has parent endpoint u, first choose c(r)!=c(u). For a nontrivial child, apply
Section 3 and map its actual missing neighbor color to c(u). Thus

    c(u) is absent among all colors of neighbors of r INSIDE its module.

For a singleton child this condition is vacuous. At every outgoing bridge
v-w from an already colored module, choose c(w) distinct from c(v). Impose
one additional prohibition when v is this module's own entry vertex:

    c(w) != color of this module's parent bridge endpoint.

This is also imposed at every singleton nonroot module, where its only vertex
is its entry. There are at most two forbidden colors, so four colors always
provide a choice. The nontrivial child coloring is subsequently permuted to
the chosen root color and its parent's color as missing channel. Modules
are vertex-disjoint, so this never recolors a previously fixed original vertex.

**Leaf invariant.** On each directed bridge u-r, the child endpoint r is a
leaf in the COMPLETE global component of the pair {c(u),c(r)}. No internal
child edge continues it because c(u) is missing there. No outgoing bridge
at r continues it because of the additional prohibition. This proves the
invariant on the actual original graph, including two bridges meeting at
one degree-two entry. It is not a claim about a normalizer-only boundary.

## 5. All-depth component classification

Fix two colors. A global component containing a nonbridge edge contains
nonbridge edges from exactly one module. Otherwise its path through the
quotient tree would enter a child through a bridge and continue internally
or through another bridge, contradicting the leaf invariant. Within that
module it contains exactly one local pair component: two distinct local
components cannot reconnect by leaving and returning through a quotient tree.

The global component is therefore one inherited spider core with additional
pendant original bridge leaves at its core vertices. Each core vertex has
internal module degree at least two, so at most TWO such leaves attach to it.
No new pendant vertex receives another edge in this pair. A component with
only bridges is a star, by the same child-leaf invariant. Both types are trees.
This proves proper acyclic coloring and prevents accumulation with quotient
depth, module branching, or atom size.

The new components need not themselves be arm-two spiders. A bridge may extend
a length-two arm or branch at an internal arm vertex. Reusing the old constant
without paying for these extensions would be invalid.

A useful additional combinatorial bound is component order at most 25. If
a nontrivial spider core has a arms, b of length two, where 2<=a<=4 and b<=a,
its order is 1+a+b. Its center has at most 4-a pendant bridge leaves and its
other a+b vertices at most two each. Hence its full order is at most

    (1+a+b)+(4-a)+2(a+b)=5+2a+3b<=25.

A single-edge core extends to at most six vertices; a bridge-only star has
at most five. The inverse bound below uses a quantitative energy argument,
not diameter or this finite component-order count alone.

## 6. A reusable quantitative pendant-extension theorem

**Lemma 3.** Let a core tree T with at least two vertices satisfy

    sum_v (x_v-mean_T x)^2 <= beta sum_uv (x_u-x_v)^2

for all real x, with beta>=1. Attach at most a new pendant vertices at each
ORIGINAL core vertex, without attaching further edges to the new vertices.
The extended tree has Poincare constant at most

    L(a,beta) = ((a+1)beta+1
               +sqrt(((a+1)beta-1)^2+4a beta))/2.

Proof. Put c=mean_T x, delta_v=x_v-c, and eta_l=y_l-x_parent(l) for each new
leaf. Let U be core edge energy and V=sum_l eta_l^2. The mean of the extended
tree minimizes squared distance to constants, so its variance is bounded by
evaluation at c. If a_v<=a leaves meet v, this gives

    Var <= sum_v(1+a_v)delta_v^2 + 2 sum_l delta_parent(l) eta_l + V
        <= (a+1)beta U + 2 sqrt(a beta U V) + V.

The second step is the core inequality and Cauchy-Schwarz. The last expression
is the quadratic form of

    Q = [[(a+1)beta, sqrt(a beta)], [sqrt(a beta),1]]

at (sqrt(U),sqrt(V)). Its largest eigenvalue is L(a,beta), proving the claim.
For a singleton core the component is a star, and evaluation at its center
directly bounds variance by edge energy, with constant one. An edgeless
component has no edge inverse. QED.

For an arm-two spider, the inherited anchored-arm quadratic gives
beta=(3+sqrt(5))/2. Namely x^2+y^2 <= beta[x^2+(y-x)^2] on each two-edge arm;
summing over arms and minimizing over constants yields the core Poincare bound.
Here a=2 by the actual full degree budget. The exact two-by-two Sylvester test
gives Q<9I, because

    9-3beta>0,
    det(9I-Q)=72-26beta=33-13sqrt(5)>0.

The latter follows from 33^2>13^2*5. Thus every global bichromatic tree has
Poincare constant at most nine, uniformly over all graph sizes and depths.

**General bridge composition principle.** Sections 3-6 do not fundamentally
need chordlessness. They apply to any bridge-deleted modules with actual
q-color acyclic realizations, uniformly bounded pair-tree Poincare constant
beta, a missing neighbor color at the one actual entry, and at most a outgoing
bridge leaves per original core vertex. For q>=3 the bridge rule is feasible,
and the global matrix inverse squared constant is at most max(1,2L(a,beta)).
The hypotheses must be supplied and proved for that module family; arbitrary
operator stability of a module alone does not imply the stronger pair-tree
Poincare hypothesis. The separation of a root interface from its quantitative
inverse is the reusable structural consequence of this construction.

## 7. Canonical least squares on the full original actions

Set X_i=e_(c(i)) in R^4. Each whole row has norm exactly one. Properness isolates
D_ii in action cell (i,c(i)). For an unordered color pair, selected cells
consist of unsigned incidence B times the coefficients on the actual edges
of each pair tree. Distinct trees and diagonal cells use disjoint action cells.

Multiplying vertex observations and edge coordinates by bipartition signs
converts unsigned incidence to oriented incidence without changing singular
values. Its nonzero squared singular values are the positive tree Laplacian
eigenvalues. Poincare constant at most nine therefore bounds the squared
Euclidean norm of the edge LS inverse by nine. The decoder signs observations,
projects away the one constant mode, and takes subtree sums; it is exactly
the canonical LS inverse, not an uncharged exact-consistency assumption.

For every real noise matrix E, summing the disjoint action budgets gives

    ||Dhat-D||F^2
      <= ||diagonal noise||_2^2 + 18 sum_components ||component noise||_2^2
      <= 18 ||E||F^2.

The factor two is the two occurrences of each symmetric offdiagonal entry.
Operator norm is no larger than Frobenius norm. Injectivity of incidence on
tree edges and diagonal separation prove exact noiseless reconstruction.
Unused action cells are discarded orthogonally, but ALL original actions
are acquired and every input cell remains in the absolute noise budget.

For a supported numerical output W let Pi be orthogonal projection onto the
original supported action range and let R=WX-Pi Y. A verified bound on R gives

    ||W-D||op <= 3 sqrt(2) (||E||F+||R||F).

Acquisition, coefficient conversion and assembly errors must enter E or receive
separate rigorous allowances. Probe perturbation adds D deltaX, which the row
budget alone cannot bound. The saved receivers use exact Fraction arithmetic;
their projected residual is exactly zero. Their RAW observation residual need
not vanish and is separately saved. No floating success status is a certificate.

## 8. A decisive failure without the second bridge condition

Take k disjoint triangles (v_i,a_i,b_i) and bridge consecutive v_i. Color
v_i=i mod2, a_i=2, b_i=3. These are actual chordless width-two degree-four
supports, and every incoming bridge color is missing from the internal
neighbors of v_i. Every local triangle is star colored. Nevertheless the
bridges form one bichromatic path on k vertices.

Cut that path into a and d vertices. Put signed divergence 1/a on one side,
-1/d on the other, then invert the path incidence. The cut edge coefficient
has absolute value one, all triangle coefficients and diagonal are zero, and
the FULL ORIGINAL action satisfies

    ||DX||F^2=1/a+1/d,  ||D||op>=1.

The design's squared inverse constant is at least ad/(a+d), unbounded for
balanced cuts. This excludes exactly the missing-color-only bridge rule.
The additional outgoing prohibition removes this propagation. The actual
27-vertex k=9 input has an exact saved witness with cut4/5, action squared
9/20 and inverse squared lower20/9; its complete-rule receiver has largest
component three. It is not an obstruction to every coloring or dense design.

## 9. Algorithm, checks, and limits

src/bridge_recovery.py finds bridges and their forest iteratively, retains
original IDs, invokes one qualified actual root per nontrivial module, and
uses the unchanged Cycle10 rule inside modules. It validates the resulting
original proper/acyclic coloring, every bridge child-leaf condition, one-core
classification, pendant degree cap, and component shape. Preparation takes
O(n+m log m) arithmetic in this native Python realization, plus one charged
fixed certificate load and the new 18-row projection check. Reading input and
writing sparse output count. The coloring, LS preparation and each decode
take O(nq+m) arithmetic after normalization; rational bit costs are additional.
The algorithm is not a complete recognizer of all graphs outside its guaranteed
class. Any accepted graph is nevertheless accompanied by an actual validated
stable-design certificate.

The new 49-vertex/61-edge receiver covers a degree-three entry adjacent to a
degree-four vertex, multi-atom modules, multiple actual outgoing marks, same-
entry bridges and bare branching bridge vertices. The new 27-vertex/35-edge
receiver uses the exact failed-rule support. Both use original free-diagonal
rational matrices and nonzero rational noise; all original action cells and
reconstructed coefficients are saved. A separate three-isolated-vertex branch
check validates the newly included direct-sum entry point. Independent checking
has a separate source and receipt; finite checks do not prove the all-size scope.

The inspected ordinary comparisons and their exact scope are in COMPARISON.md.
This is not a first use of coloring compression or substitution, and no direct
assembly/AD cost or original NIST/molecular incumbent has been beaten. Internal
proof/check status, historical originality, efficient implementation and useful
physical performance remain separate claims.
