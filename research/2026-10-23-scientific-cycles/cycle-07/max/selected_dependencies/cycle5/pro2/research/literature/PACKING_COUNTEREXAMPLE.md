# A maximal square-independent recoloring set can miss the whole obstruction

This is an elementary applicability counterexample derived in Cycle5. It
does not rule out a suitably targeted recoloring set.

For n>=2 form a caterpillar with spine vertices v_1,...,v_n, path edges
v_i v_(i+1), and one leaf u_i adjacent to each v_i. This is a tree with
maximum degree three. Give v_i color i mod 2 and all u_i color2. This is a
proper acyclic three-coloring.

Let S={u_1,...,u_n}. For i!=j,

    dist_G(u_i,u_j)=|i-j|+2 >= 3.

Hence S is independent in the square G^2. It is maximal there because every
remaining vertex is a spine vertex v_i adjacent to u_i. Nevertheless, S has
no vertex in the bichromatic 0/1 spine component. Recoloring S with color3
leaves that n-vertex component unchanged. Its coordinate recovery constant
therefore diverges by the inherited cut-flow lower theorem.

This disproves the implication

    maximal square-independent set -> fragmentation of old bichromatic trees.

It remains false even with treewidth one and maximum degree three. Radius-two
domination of the full graph is not a hitting property inside each induced
bichromatic subgraph.

## Correct conditional recoloring lemma

Let c be a proper acyclic k-coloring of a graph of maximum degree Delta.
Suppose S is independent in G^2 and, after deleting S, every component
induced by any two old colors has at most K vertices. Recolor all vertices
of S with a new color. Then this is a proper acyclic (k+1)-coloring with all
bichromatic components of size at most max(K,Delta+1).

Proof. Old-color components are the stipulated induced subgraphs of G-S,
and deletion preserves acyclicity. For a fixed old color a, every a-colored
vertex has at most one neighbor in S, because two such neighbors would be
at distance two and contradict square independence. A path using only a and
the new color therefore cannot contain two vertices of S; each component is
a star centered at one S vertex, or a single vertex. Such stars have at most
Delta+1 vertices. Properness follows from independence of S and properness
of c on G-S. This proves the lemma.

The real obligation is finding S that simultaneously fragments all old
bichromatic trees. Maximality alone does not prove this; the caterpillar
shows precisely where that inference fails. No universal existence theorem
for such an S is claimed here.
