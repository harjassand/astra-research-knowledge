# Independent bridge-interface challenge

Pro2 bounded contributor, 23 October 2026. This is a conditional global-interface
lemma and a decisive failure of an omitted condition. It does not prove the
degree-three rooted atom hypothesis, historical novelty, or an all-real lower.

## 1. Intrinsic incidence and the necessary local obligation

Delete every bridge from a connected finite simple graph of maximum degree
four. The resulting connected components, including isolated vertices, form
the vertices of a quotient tree; the original bridges are its edges. Two
different quotient vertices cannot be joined by two bridges, since the two
paths through their connected components would put both edges on a cycle.

Every nonsingleton component M is connected and bridgeless, and has minimum
degree at least two. Root the quotient tree. The endpoint r in a nonsingleton
child M of its incoming bridge has degree two or three within M, because the
bridge consumes one unit of the original degree budget. Moreover r lies in
exactly one nontrivial block of M. Membership in two nontrivial blocks would
already contribute local degrees at least two plus two, leaving no bridge.

Thus the new local obligation really is one marked root of degree two or
three in one atom. It is not several independent marks in a block, nor a
choice of a convenient root after observing the support. If a rooted atom
coloring has an absent nonroot neighbor color, then global permutation maps
the root and that absent color to any two prescribed DISTINCT colors. The
root's neighbors do not change when other blocks of M are colored at their
other cuts; r is not such a cut in M.

This verifies the interface needed by the root investigator's stronger route,
conditional on the actual degree-three missing-color theorem and its native
realization. A mere list of successful endpoint profiles does not prove that
all actual degree-three roots reduce to those profiles.

## 2. Module hypotheses and actual bridge rule

Suppose every nonsingleton component M is assigned an actual proper
four-coloring such that:

1. Each bichromatic component with an edge is a spider with arms at most two.
2. At its actual incoming bridge endpoint r, if the parent endpoint has color
   p and r has color a, then p is absent among the colors of all neighbors
   of r INSIDE M. The two colors a,p are distinct.

The root component needs only condition 1. A singleton has no internal edges.
Each whole query row is the corresponding coordinate vector, as in the
unchanged recovery contract.

When selecting the endpoint color on an outgoing bridge u-v, require:

- color(v) differs from color(u), so the original bridge is proper;
- if u is the incoming bridge endpoint of its own component, color(v) also
  differs from that component's parent endpoint color;
- at every singleton child component, impose the same second requirement
  on all its outgoing bridges.

There are at most two forbidden colors when selecting color(v), so at least
two choices remain. Once this actual endpoint color is chosen, a genuine
one-root missing-color guarantee in the child can be permuted to that root
color and the required missing parent color. Different bridge-deleted
components are vertex-disjoint, and hence such permutations do not change
any previously colored vertex.

The second requirement is essential even when all module entry colors are
missing locally; Section 5 gives an exact failure family without it.

## 3. No collision and exact global component classification

Fix a pair of colors {a,b}. Consider a bridge u-v directed from a parent
component to a child component, with endpoint colors a,b. At v there is
no internal child edge in this pair by condition 2 (or because the child is
a singleton). There is also no outgoing bridge in the pair at v, because
the bridge rule forbids the color a at each forward endpoint. Thus v is a
LEAF of this entire bichromatic component.

This observation concerns the actual original vertex v. It does not stop at
a convenient normalizer boundary, and it includes the case that v has both
an internal degree-two atom and a further bridge at the same vertex. The
incoming bridge and that outgoing bridge cannot form a two-edge continuation.

Every global component with nonbridge edges therefore has such edges in
exactly one bridge-deleted component M. Otherwise the quotient-tree route
between two components contributing nonbridge edges would enter a child
through a bridge and then continue internally or through another bridge,
contrary to the leaf conclusion. Within M it is exactly one of its local
bichromatic spiders S. A second disconnected local component cannot reconnect
outside M, because the quotient is a tree and all departures end at leaves.

All additional edges are pendant original bridges attached to vertices of S.
Every such bridge adds a different new leaf. Thus the classification is:

    one Cycle10 arm-at-most-two spider core
    + pendant bridge leaves attached to its actual vertices.

There are at most 4-deg_M(v) bridge leaves at v. In particular each vertex
of a nonsingleton core has at most two. The result need not itself be an
arm-two spider: bridge leaves at internal arm vertices can introduce more
than one branching vertex, and a bridge leaf beyond an arm endpoint extends
an arm to length three. Reusing the old short-arm constant without another
argument would be unjustified.

A component containing only bridges is a star. After entering any child
vertex it stops; hence all its edges have a common parent vertex. The degree
cap bounds this star's order by five. Acyclicity is preserved in both cases.

There are no competing messages at one child root. Each bridge-deleted
component has one incoming bridge; a forbidden parent color is tested only
at that actual entry vertex. The rooted missing-color condition inside the
module is singular, not a family of independent root prescriptions.

## 4. A safe component-order bound

For a nontrivial spider core, choose a center with a arms, b of length two.
If a>=2, then b<=a<=4, its order is 1+a+b, its center has internal degree at
least a, and every other vertex has internal module degree at least two.
There can therefore be at most

    (4-a) + 2(a+b)

pendant bridge leaves. The full component order is at most

    (1+a+b)+(4-a)+2(a+b) = 5+2a+3b <= 25.

For a single-edge core the two internal module degrees are each at least
two, so its order after attachments is at most six. A path of length two
can be centered at its middle and is covered by a=2,b=0. A singleton core
contributes only bridges and is covered by the star case. Thus K<=25 is a
valid graph-size-independent bound, conditional on the module hypotheses.

This count uses the actual degree budget in addition to the core geometry.
It is not an assertion that bounded diameter alone controls cut mass. The
root investigator may obtain a better direct inverse bound for this shape;
that separate analysis is not assumed here.

## 5. Missing entry color alone fails on a native bridge family

Take k disjoint triangles with vertices (v_i,a_i,b_i), and join consecutive
v_i by original bridges. This graph is chordless, width two, and has maximum
degree four. Its bridge-deleted components are the triangles. Give v_i color
i mod 2, a_i color 2, and b_i color 3. Every triangle is properly star colored.
At every child entry v_i, its parent endpoint color (i-1) mod 2 is ABSENT
among the two internal neighbor colors {2,3}.

Nevertheless, the entire sequence of bridges is a bichromatic 0/1 path
on k vertices. The omitted bridge rule allows color(v_(i+1)) to equal
color(v_(i-1)); it is precisely the forbidden entry-vertex continuation.

For a cut with a vertices on the left and d on the right, define signed
divergence 1/a on one side and -1/d on the other. The path-incidence inverse
gives a supported symmetric D using only these original bridge coefficients,
zero diagonal and zero triangle coefficients. Its cut coefficient has absolute
value one, and its FULL original action satisfies

    ||DX||F^2 = 1/a+1/d,  ||D||op>=1.

The design's inverse squared constant is at least ad/(a+d), diverging along
balanced cuts. The exact k=9 diagnostic has 27 vertices, 35 original edges,
cut 4/5, action norm squared 9/20 and inverse squared lower 20/9.

The same graph admits the complete bridge rule: color v_i=i mod3; for each
noninitial triangle color a_i,b_i with the two colors other than color(v_i)
and color(v_(i-1)); use colors2,3 in the initial triangle. Its actual
bichromatic components have order at most three. The diagnostic checks both
colorings and the full original-action witness. The failure excludes only
the rule omitting the entry-vertex prohibition, not all four-color designs
or any arbitrary-real recovery method.

## Scope and cost

This contributor challenges only the new bridge interface. The original
Cycle10 theorem, table closure and receiving suites were read but not rerun.
The degree-three atom guarantee and the final recovery norm are separate
obligations owned by the parent investigator. One exact new diagnostic is
timed; reasoning, source reading, authoring and integration totals are unknown.
