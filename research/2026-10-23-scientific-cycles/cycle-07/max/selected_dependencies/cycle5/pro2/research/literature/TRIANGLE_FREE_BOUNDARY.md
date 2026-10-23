# A finite exceptional boundary for triangle-free clique-cutset atoms

This is a derived structural corollary of the explicit bad-triple description
in Trotignon–Vuskovic, arXiv:1407.6531v2, Lemma5.2. It is not an independent
replacement proof of their classification, nor a four-color extension lemma.

## Statement

Let G be a finite simple triangle-free, 2-connected, series-parallel graph,
with no clique cutset and maximum degree at most four. If |V(G)|>12, then
for every pair x,y with x=y or xy an edge, there exists a degree-two vertex
outside N[x] union N[y].

All degree conditions refer to G itself. "Series-parallel" here means no K4
subdivision as a subgraph, equivalent to the K4-minor-free support class.
Absence of a clique cutset is essential to the invoked source lemma. The
statement does not apply indiscriminately to all triangle-free supports.

## Exact dependency from the primary source

Write the desired property as the (x,y)-property. If it fails then either
(G,x,x), (G,y,y), or (G,x,y) is a bad triple in the source's terminology.
For a bad triple with at least five vertices, Lemma5.2 supplies a nonempty
tree T on the vertices outside N[x] union N[y]. The other vertices besides
x,y are b auxiliary degree-two vertices, each adjacent to exactly one of
x,y and one vertex of T. Every leaf of T needs at least two such attachments;
each degree-two T vertex needs at least one. If T is a singleton it needs
at least three attachments.

For distinct x,y the source restricts to xy an edge, so b<=deg(x)+deg(y)-2.
For x=y, b<=deg(x). These are the only source properties needed below.

## Counting proof

Assume |T|>=2. Let L be its leaf count, Q the number of its degree-two
vertices, and H its number of vertices of degree at least three. The tree
degree sum gives

    H <= L-2.

The attachment obligations give

    b >= 2L+Q.

Consequently

    |T|=L+Q+H <= 2L+Q-2 <= b-2.

For x!=y, b<=6, and therefore

    |G|=2+b+|T| <= 2b <=12.

For x=y, b<=4, and

    |G|=1+b+|T| <=2b-1 <=7.

If |T|=1, the separate totals are |G|=b+3<=9 for distinct x,y, and
|G|=b+2<=6 for x=y. The cases |G|<5 are already below twelve. Thus failure
of the (x,y)-property always forces |G|<=12, proving the statement.

## Scientific role and limits

This bounds exceptional atoms for a possible reducibility argument: a
large triangle-free atom has a low-degree vertex away from a specified
edge boundary. It does not show that deleting/reinserting this vertex
preserves a bounded-component acyclic four-coloring; neighbor color and
component-size states still need to be controlled. It also does not show
that an arbitrary graph-adapted real four-query design is stable.

No graph enumeration or numerical experiment was used. No historical
originality is claimed for the corollary or source structure.
