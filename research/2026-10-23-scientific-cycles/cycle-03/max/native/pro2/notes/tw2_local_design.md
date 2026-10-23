# Local palette compression is blocked by the classical sharp star-color graph

Contributor: `/root/tw2_local_design`; 22 October 2026 Australia/Brisbane.
Task: test the proposed repair of dense compression by a star coloring in which
all closed neighborhoods contain at most five colors. This is a local lemma,
not a parallel investigation of general dense five-query recovery.

## Result

The repair is impossible. There is a 41-vertex outerplanar graph of treewidth
at most two such that **every star coloring, with arbitrarily many total colors,
has a closed neighborhood containing at least six distinct colors**.

This is a strengthened observation from the very graph in Albertson, Chappell,
Kierstead, Kündgen and Ramamurthi (2004), Theorem 6.3. It does not introduce a
new graph or establish historical novelty. Their proof already contains the
mechanism; replacing its global five-color assumption by a local five-color
assumption works because the common apex sees the entire central path.

## Explicit graph

Take an apex `v` and path `u_1,...,u_8`, with every `u_j` adjacent to `v`.
For each `j`, take a disjoint four-vertex path `H_j` and join all four of its
vertices to `u_j`. There are `1+8+8*4=41` vertices and `15+8*7=71` edges.

A width-two tree decomposition is explicit: use the seven central bags
`{v,u_j,u_(j+1)}` in path order; for each `j` attach a path of three bags
`{u_j,h_(j,k),h_(j,k+1)}`, `k=1,2,3`, to any central bag containing `u_j`.
Every edge lies in a bag, every bag has size three, and the bags containing
any vertex induce a connected subtree. Thus the graph has treewidth at most
two. It contains triangles, so the treewidth is exactly two. This is also
exactly the paper's `G_3` construction, stated there to be outerplanar.

## Full proof of the local obstruction

A star coloring is proper and has no two-colored path on four distinct vertices.
Assume for contradiction that every closed neighborhood uses at most five colors.

The closed neighborhood of `v` contains `v` and all eight path vertices. Properness
makes the color of `v` distinct from every color on that path. The central path
therefore uses at most four colors.

Call a path vertex redundant when its color occurs at least twice on the path.
Two adjacent path vertices must both be redundant. Indeed, if the redundant
vertices formed an independent set in the eight-vertex path, there could be at
most four of them. Thus there would be at least four nonredundant vertices,
using at least four distinct singleton colors. There is at least one redundant
vertex, since eight vertices use at most four colors; its color is different
from every singleton color. That would require at least five colors, a
contradiction.

Choose adjacent redundant vertices `u_j,u_(j+1)`. Relabel their colors as `2,3`
and the apex color as `1`; properness makes these three labels distinct.
Color `1` cannot occur on `H_j`: if a vertex `h` of `H_j` had color `1`, a
second central-path vertex `u_l` with color `2` would give the two-colored
four-vertex path `h,u_j,v,u_l`. The four vertices are distinct. Likewise color
`1` is absent from `H_(j+1)`. Properness excludes color `2` from `H_j` and
color `3` from `H_(j+1)`.

If color `3` occurred at some `h` in `H_j` and color `2` occurred at some `h'`
in `H_(j+1)`, then `h,u_j,u_(j+1),h'` would be a two-colored four-vertex path.
Therefore either `H_j` contains neither color `1,2,3`, or `H_(j+1)` contains
none of these three colors.

Every star coloring of a four-vertex path uses at least three colors: a proper
two-coloring of that path is itself a forbidden two-colored `P_4`. The chosen
attached path thus uses at least three colors different from `1,2,3`.
The closed neighborhood of its center `u_j` or `u_(j+1)` contains the whole
attached path, the center, the adjacent selected central-path vertex and the
apex. It uses at least six distinct colors. Contradiction.

The general six-star-color upper bound for treewidth two makes six sharp for
this local palette parameter on this graph. Its proof is unnecessary for the
negative conclusion.

## Consequence for query compression; exact limitation

Suppose a recovery scheme first assigns one vector to each color, then recovers
**all color aggregates in each row using only that row's measured action**,
and finally applies star-color direct recovery. If a closed neighborhood has
`s` colors, its `s` row aggregates are independent scalar unknowns: each
neighbor color has at least one permitted incident edge and the own-color
aggregate is the free diagonal. The row measurement is a linear map from
`R^s` to `R^q`. Exact full aggregate recovery requires `q>=s`, regardless of
conditioning or the number of global colors. Therefore no such five-query
local-unmixing implementation covers all treewidth-two supports.

This does **not** exclude a five-query dense scheme which jointly decodes rows,
uses graph-adapted continuous vectors without full local aggregate recovery,
or only recovers selected coefficients by local functionals. It also does not
exclude a restricted family that avoids this graph. No general four/five-query
operator lower bound is proved.

## Modest generalization of the same observation

Let `G_t` be exactly the recursive construction in Theorem 6.3: `G_1=K_1`,
`G_2=P_4`; for `t>=3`, take a clique of size `t-2` complete to a path of length
`2*(binom(t,2)+1)`, and attach a copy of `G_(t-1)` universally to each path
vertex. The paper proves clique number `t`, treewidth `t-1`, and global star
chromatic number `binom(t+1,2)`.

The same graph also forces local closed-neighborhood star color count at least
`binom(t+1,2)`, even with unbounded global palette. To prove this, suppose the
local count is at most `B-1`, where `B=binom(t+1,2)`, and write `b=binom(t,2)`.
A vertex of the apex clique sees the whole apex clique and path, so the path
uses at most `B-1-(t-2)=b+1` colors. Its length is `2(b+1)`, forcing adjacent
redundant vertices by the same counting argument. Each attached copy at those
vertices avoids all `t-2` apex colors, and one avoids both selected center
colors, by the same two-colored paths. That copy needs at least `b` distinct
colors by the established global lower bound for `G_(t-1)`. The closed
neighborhood of its center then contains at least `b+t=B` colors, a
contradiction. The general star upper bound supplies equality. Base cases
are immediate. This is a consequence of the established construction, not a
claimed new historical theorem.

## Sources and observed costs

Primary source personally read: Albertson et al., *Coloring with no 2-colored
P4's*, Electronic Journal of Combinatorics 11 (2004), R26, Theorems 6.1, 6.3.
DOI https://doi.org/10.37236/1779 . Full text:
https://www.combinatorics.org/ojs/index.php/eljc/article/viewFile/v11i1r26/pdf/ .
The relevant construction and proof are on page 10 of the PDF (printed page 10;
zero-based PDF page 9), around retrieved lines 414-452.

Three web calls had displayed latencies 2.3, 2.0 and 2.4 seconds, total 6.7
seconds. A first broad narrow-topic search returned mainly irrelevant results;
none is used as evidence. The two subsequent calls read the primary source.
No original benchmark, incoming obstruction replay, optimization, installs,
paid resources, or further agent delegation occurred. The simple exact graph
check is separately metered in results/tw2_local_design_check.json. Proof
construction, authoring, model inference cost, monetary cost and energy were
not separately metered and are not zero.
