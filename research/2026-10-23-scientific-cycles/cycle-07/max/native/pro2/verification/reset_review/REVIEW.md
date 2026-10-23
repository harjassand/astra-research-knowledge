# Focused independent review of terminal-color resets

Reviewer: `cut_balance_challenge`, Cycle6 PRO2. This bounded review concerns
the owner's new three-color construction on a supplied recursive two-terminal
network. It does not investigate the entire degree-four partial-two-tree class.
The contract retains free diagonals, coordinate query rows of norm one,
absolute Frobenius action noise and operator output error.

## Verdict

The parallel-reset construction is correct, including its K=13 component
bound and C=5 operator-noise guarantee for maximum parallel arity three.
Arbitrary odd series composition also preserves this bound. The proof needs
a distinction between reset identities at a **parallel node** and inequalities
valid throughout the grammar: a series node need not have L_AC=1.
The proposed even-series coloring extension fails as claimed, with an
explicit exponentially growing bichromatic tree. That failure is for this
specified coloring rule, not for every design on the same graphs.

## 1. Network and color definitions

Every network has distinct ordered terminals s,t, each of graph degree one.
A leaf is the three-vertex path s-u-t. For a desired ordered pair of distinct
terminal colors (A,B), with C the third color, its word is (A,C,B).

P_b, for b in {2,3}, takes b otherwise vertex-disjoint child networks, identifies
all their left terminals as a and all their right terminals as z, and adds
new outer terminals s,t with edges sa and zt. Assign

    c(s)=A, c(a)=B, c(z)=C, c(t)=B,

and recursively color each child with ordered terminal colors (B,C).

At a series node with 2k+1 children, identify consecutive child terminals and
color their ordered terminal pairs alternately

    (A,B),(B,A),(A,B),...,(A,B).

Only the identified terminal vertices are shared. Every constituent vertex
and edge remains otherwise distinct.

These constructions preserve simplicity and terminal degree one. A separated
child cannot have a terminal-to-terminal edge, so identifying child terminal
pairs in parallel creates no duplicate edge. A P_b junction has degree b+1,
a series junction has degree two, and old internal degrees do not change.
Thus the base grammar has maximum degree at most four. The construction is
series-parallel: parallel composition, series composition and adding pendant
outer edges are its defining operations. Equivalently, adding a virtual edge
between the two terminals maintains a width-two decomposition, which can be
composed along the child terminal pairs. Triangle-freeness also follows for
the path-leaf grammar: joins cannot create a triangle because parallel
children have no terminal edge and series joins occur at a cut vertex.

## 2. Boundary profiles and separation

For a colored network with terminal colors (A,B), define

    L_AB = order of the AB component containing s,
    L_AC = order of the AC component containing s,
    R_AB = order of the AB component containing t,
    R_BC = order of the BC component containing t.

Isolated vertices count as components of order one in this bookkeeping.
A network is separated if no bichromatic component contains both terminals.
Because their colors differ, only the AB pair could contain both, but the
all-pair formulation is convenient when relabeling children.

The leaf has profile

    (L_AB,L_AC,R_AB,R_BC)=(1,2,1,2),

is properly colored, acyclic, and separated.

## 3. Exact parallel recurrences

At P_b the child relative color triple is (A',B',C')=(B,C,A).
The outer-terminal boundary profiles are

    L_AC = 1,
    R_AB = 1,
    L_AB = 2 + sum_i (L_AC(child_i)-1),
    R_BC = 2 + sum_i (R_AB(child_i)-1).                    (1)

The possible new closed components at the two shared child terminals have
orders

    BC component at a: 1 + sum_i (L_AB(child_i)-1),
    AC component at z: 1 + sum_i (R_BC(child_i)-1).         (2)

Other components remain internal to one child. Equations (1)--(2) account
for every pair: AB touches only a, AC touches only z, and BC has components
at both a and z. The latter remain separate because no child has a BC path
between its two terminals. Each merged component is a union of trees sharing
one root, so it remains a tree. The new pendant edges do not create cycles.
The outer right terminal is isolated in AB, proving separation of the parent.

Throughout the path-leaf grammar, including odd series nodes, the invariant is

    L_AC <= 2,   R_AB = 1,
    L_AB <= 5,   R_BC = 2.                               (3)

At an actual P node the stronger equalities L_AC=R_AB=1 hold.
Equation (1) preserves (3). Equation (2) bounds closed new components by

    1+3(5-1)=13,    1+3(2-1)=4.

The boundary components have order at most five. Hence every bichromatic
component has order at most13 at every parallel depth.

## 4. Odd series composition

A bichromatic component cannot cross two distinct series junctions: that
would require a terminal-to-terminal bichromatic path in the child between
those junctions. This is forbidden by separation. Thus any new component
at a junction consists of exactly a right boundary component of one child
and a left boundary component of the next, identified at their common root.
Their union is a tree and its order is the sum of their orders minus one.

Because the desired ordered terminal pair alternates, the two possible
junction component orders have relative form

    R_AB(previous) + L_AB(next) - 1,
    R_BC(previous) + L_AC(next) - 1.                      (4)

By (3), these are at most five and three. Components internal to a child
keep their previous bound13. The outer boundary components are exactly those
of the first and last children, since they cannot pass through a child to
its next junction. With an odd number of children, those first and last
children have the same ordered terminal colors (A,B) as the parent. Thus
(3), acyclicity, separation and K<=13 all persist.

The assertion "all internal nodes have L_AC=1" would be false. For example,
a series node whose first child is a leaf has L_AC=2. The correct induction
uses (3) globally and the stronger equalities only at P nodes. This is a
wording correction to the proof invariant, not a failure of the construction.

## 5. Stable recovery and exact query minimum

The admitted coordinate design has exactly three columns and row norm one.
The inherited coordinate theorem gives, for r<=2 and K<=13,

    ||Dhat-D||op <= sqrt(1+r(K-1)) ||E||F <= 5 ||E||F.

The original-support global incidence decoder and residual allowance apply.
This does not assert that5 is the optimal condition constant, or that these
three actions outperform a higher-query design under total physical costs.

For any graph containing a cycle on l vertices, two arbitrary real query
columns cannot identify every supported symmetric matrix with free diagonal.
Restrict D to the l cycle diagonals and l cycle edges: this gives2l free
coefficients and only2l possibly nonzero action entries. If the restricted
query block X is nonzero, every action Y=DX obeys the nonzero linear relation

    x_1^T y_2 - x_2^T y_1 = 0,

from symmetry. Hence the action rank is at most2l-1. If X is zero, the rank
is zero. A nonzero kernel follows in either case. All other rows of the
full action vanish for this restricted D, so extra graph vertices supply no
missing information. This argument permits graph-adapted dense real rows;
it does not rely on the coordinate restriction or on full column rank of X.

Therefore the worst-case exact and dimension-independent stable query count
of this grammar is exactly three whenever it includes a P node and hence a
cycle. A particular leaf-only series tree may have a smaller exact minimum.

## 6. Supplied leaf-module generalization

The same argument works when leaves are supplied properly acyclic three-
colored, separated two-terminal modules, with terminal degree one, maximum
bichromatic component order K0 and all four boundary masses at most beta.
Assume beta>=2 and maximum parallel arity B>=2. Relabel module colors to
match any desired distinct ordered terminal pair. Put

    R = 2+B(beta-1),
    K = max(K0, 1+B(R-1))
      = max(K0, 1+B+B^2(beta-1)).                         (5)

The invariant becomes

    L_AC,R_AB <= beta,    L_AB,R_BC <= R.

Parallel nodes reset the low slots to one, create high slots of size at
mostR, and create closed components of size at most1+B(R-1). Odd series
nodes inherit boundary profiles and their junction components have order at
mostR+beta-1<=2R-1<=1+B(R-1), since B>=2 and R>=beta. Thus (5) covers the
whole grammar with arbitrary odd-series and parallel depth. The support
maximum degree is max(supplied-module maximum degree,B+1), and the graph
remains series-parallel if the supplied modules are two-terminal SP modules.
A module's good coloring alone does not prove it is series-parallel.

## 7. Exact failure of the proposed even-series rule

For two children, choose the global terminal pair (A,B), junction color C,
and child pairs (A,C),(C,B). This is still proper, acyclic and separated,
but it swaps the profile slots:

    L_AB(S2)=L_AC(first),   L_AC(S2)=L_AB(first),
    R_AB(S2)=R_BC(second), R_BC(S2)=R_AB(second).           (6)

Let Q0 be the path leaf and let

    Q_h = P_2(two copies of S2(Q_(h-1), path leaf)).

Write x_h=L_AB(Q_h). Equations (1) and (6) give

    x_0=1,   x_h=2+2(x_(h-1)-1)=2x_(h-1)=2^h.

The graph remains simple, triangle-free, series-parallel, and has maximum
degree at most three. Its exact counts are

    n_h=7*2^h-4,   m_h=8*2^h-6.

Properness, acyclicity and absence of terminal transmission survive; only
uniform component size fails. The inherited bounded-degree cut theorem
therefore gives the specified coloring an operator inverse lower

    rho >= sqrt((2^h-1)/6).

There is a more explicit cut for h>=2. The left boundary tree consists of a
root hub, one terminal leaf, and two branches each of order2^(h-1)-1.
One branch cut has sides2^(h-1)-1 and2^(h-1)+1, so its cut mass is

    Gamma_cut = 2^(h-2)-2^(-h).

The exact signed-divergence cut witness yields rho>=sqrt(Gamma_cut).
This is a failure of the chosen even-series profile rule. It does not prove
that these graphs lack a better three-coloring, a better three-query real
design, or a stable decoder for a different design.

## 8. Small independent diagnostic and scope

`independent_reset_check.py` imports no producer module and uses only integer
arithmetic. Its first and only run checked three newly generated examples:

| Case | Vertices | Edges | Maximum degree | Largest bichromatic tree | Boundary profile |
|---|---:|---:|---:|---:|---|
| Two-level ternary parallel reset | 19 | 26 | 4 | 13 | (2,1,1,2) |
| Odd series with a leaf at its left boundary | 23 | 30 | 4 | 13 | (1,2,1,2) |
| Even-series failure Q3 | 52 | 58 | 3 | 8 | (8,1,1,4) |

Every example passed properness, acyclicity, terminal-degree and no-transmission
checks. Full edges and colors are saved in RESULT.json. The second example
makes the stronger internal-reset wording failure concrete. These finite
checks supplement the all-size recurrences; they do not prove them by size
extrapolation. No old suite, physical matrix action or application benchmark
was run in this review.

Internal correctness, historical priority, external acceptance and practical
usefulness remain separate. The result supplies a real uniform operation on
a recursive support class; it does not resolve all maximum-degree-four
partial two-trees or weaken the applicable five-query full-class comparator.

### Representation-reading cost caveat

For a graph-size linear construction claim, odd series nodes should have at
least three children, or unary nodes must be normalized while charging the
supplied expression length. Arbitrarily many unary S1 nodes can encode the
same graph and must not be read for free. The substantive operation count
is linear in the supplied expression plus the materialized graph and fixed
leaf-module data; actual actions and decoder work remain additional.
