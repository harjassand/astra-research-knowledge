# Focused independent challenge: four directions on a forest prism

Reviewer: `/root/degree4_structure`.
Scope: the owner's proposed four-color operation on `Q = T Cartesian-product K2`.
This is a proof review of a distinct receiving use of the branching
counterexample in PROOF.md, not an independent full recovery programme.

## Reviewed statement and disposition

Let T be any finite forest, root each component, and let d(v) be vertex depth.
Write a=(0,2,1,3), with all subscripts read modulo four. Color the two copies of
v by

    c(v,0) = a[d(v)],
    c(v,1) = a[d(v)+2].

The proposed coloring is a proper four-star-coloring of Q for every forest T,
without a degree bound. The review accepts this exact all-size statement.
Coordinate query rows X_(v,l)=e_(c(v,l)) have norm exactly one. The usual
star-component decoder consequently satisfies

    ||Dhat-D||_2 <= ||Dhat-D||_F <= sqrt(2) ||E||_F

for every symmetric D on this known support, with free diagonal and arbitrary
absolute Frobenius action noise. Below is a direct proof of the required
coloring and decoder estimate, including the absence of unwanted connections
between levels and layers.

## Explicit pair table

For an edge from a parent at depth d to a child at depth d+1, the unordered
color pairs are:

| d mod 4 | Layer 0 parent-child pair | Layer 1 parent-child pair | Rung at depth d |
|---|---|---|---|
| 0 | {0,2} | {1,3} | {0,1} |
| 1 | {1,2} | {0,3} | {2,3} |
| 2 | {1,3} | {0,2} | {0,1} |
| 3 | {0,3} | {1,2} | {2,3} |

Every edge has different endpoint colors, so the coloring is proper.

There are only six unordered pairs of four distinct colors. The table
partitions all pairs into two disjoint types:

1. Pairs {0,1} and {2,3} occur on rungs only. Rungs are a matching, because
   each vertex belongs to exactly one rung. Their bichromatic components
   therefore consist of single edges and isolated vertices.
2. The remaining four pairs occur on tree edges only. A component of one of
   these pairs cannot change layers: the only edges between layers are rungs,
   and no rung has that color pair. Fix a layer and one such pair. The table
   assigns that pair to a unique lower-depth residue r modulo four. Its edges
   therefore lie only between levels (r+4j,r+4j+1). Different such level pairs
   have disjoint vertex sets and no connecting edge of the fixed color pair.
   Within a single level pair, every child has exactly one parent. Consequently
   distinct parents' edge sets are vertex-disjoint stars.

These two cases exhaust every bichromatic subgraph. In particular, a vertex
cannot join two stars by acting as a child for one occurrence of a color pair
and a parent for another: the next possible lower-depth occurrence is four
levels later, not one level later. No component can bypass this restriction by
crossing a rung, because rung pairs and tree-edge pairs are disjoint.

## Direct decoder and actual noise norm

Proper coloring isolates every diagonal:

    Y[v,c(v)] = D[v,v] + E[v,c(v)].

For a star in the bichromatic subgraph for colors a,b, with center u and leaves
w_1,...,w_s, each leaf row isolates the corresponding edge:

    Y[w_j,c(u)] = D[w_j,u] + E[w_j,c(u)].

Read the edge from that leaf entry and use the same estimate in both symmetric
positions. For a one-edge star, choose either endpoint deterministically.
Each selected observation cell is used for only one coefficient: for a fixed
row and target color, the row lies in exactly one component of the associated
two-color subgraph; if it is used as a leaf, that component gives one edge.
Diagonal cells are distinct from all these cells by proper coloring.

Writing E_diag and E_edge for these disjoint selected cells therefore gives

    ||Dhat-D||_F^2
      = sum_diag |E_diag|^2 + 2 sum_edges |E_edge|^2
      <= 2 ||E||_F^2.

This elementary decoder already proves the stated bound without a global
inverse or a probability/noise-independence assumption. An owner implementation
may instead use all readings in each star: its edge coefficient observation
matrix consists of an identity matrix from the leaves and a row of ones from
the center, so its Gram matrix is I + 11^T. Its smallest eigenvalue is at least
one. Distinct star blocks use disjoint observation cells, which proves the same
global sqrt(2) bound. For a one-edge block the Gram eigenvalue is two, but the
uniform estimate does not require exploiting that improvement.

## Support, construction and scope

Q has 2|V(T)| vertices, |V(T)|+2|E(T)| edges and maximum degree Delta(T)+1.
Each tree component's root rung starts a width-one decomposition. For each
parent p and child v, add bags

    {(p,0),(p,1),(v,0)},
    {(p,1),(v,0),(v,1)}.

Attach the first bag to an existing bag containing the parent rung and attach
the second to the first. The second bag contains the child rung for later
attachments. These bags cover every new square and satisfy running
intersection, proving treewidth at most two. Thus Delta(T)<=3 puts Q inside the
owner's exact treewidth-two, degree-four support class. Isolated components of
T cause no exception: their prisms are single rungs.

Rooting, depth residues, rows and bichromatic component preparation require
O(|V(T)|) work from an adjacency-list representation. Decoding likewise uses
O(|V(T)|) arithmetic operations. Four coordinate actions have their actual
acquisition cost. The exact-real noise bound above does not itself certify
floating arithmetic; an implementation must charge any additional arithmetic
error. The owner owns the numerical source and execution for this operation.

The positive result applies to the highly branching family that defeated the
bounded-bandwidth shortcut. It demonstrates that unbounded bandwidth is not a
four-query obstruction. It does not establish a three-query lower bound for
forest prisms, and does not resolve four versus five for all partial 2-trees of
maximum degree four. Historical originality is not assessed by this focused
review.

## Review cost and exclusions

This review used the explicit four-residue table and direct all-size proofs.
No numerical trial, optimizer, source replay, paid compute or precision sweep
was run. Reading, reasoning, proof authoring, messaging and service overhead
are real additional costs but were not separately metered. The computational
timings in RESULT.json concern the earlier degree-four 2-tree decoder only and
must not be attributed to this new prism operation.

No counterexample was found in the stated forest-prism class. The dangerous
join mechanisms requested by the owner are excluded individually above; the
proof does not extrapolate from a finite graph test.
