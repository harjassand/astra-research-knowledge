# Exact boundary of the capacitated-matching inventory property

Independent ordinary graph lemma; not a recurrence theorem and not acceptance of the new compound-seed code.

For a finite simple undirected graph G and integer capacities x>=0, let ν_G(x) be the maximum number of edges in an integer capacitated matching (an edge may be used repeatedly, with incident multiplicities bounded by x). For any enabled edge uv, insertion/removal gives

    1 <= ν_G(x)-ν_G(x-e_u-e_v) <= 2.

The lower bound follows by appending uv to a matching after removal. For the upper bound, remove the at most two matching edges needed to free one copy of u and v.

## Theorem

The following are equivalent:

1. For every x and every enabled graph edge uv, removing one copy at each endpoint lowers ν_G by exactly one.
2. Every connected component containing an edge is complete bipartite.
3. G has neither an induced triangle nor an induced four-vertex path P4.

Isolated vertices are irrelevant.

**(2) implies (1).** On a complete bipartite component, arbitrary integer counts can be matched up to the smaller total shore count, so ν=Σ_components min(L,U). Removing an edge lowers both totals in its component by one and hence lowers ν by exactly one.

**(1) excludes triangles and induced P4.** On a triangle put capacities (1,1,2), all other capacities zero. The two unit-capacity vertices can each be matched to the double-capacity vertex, giving ν=2. Removing the edge between the unit vertices leaves only the third vertex, giving ν=0. On an induced path 1--2--3--4 put one particle at each path vertex and zero elsewhere. Initially ν=2; remove one copy at 2 and 3 and only nonadjacent endpoints remain, so ν=0.

**(3) implies (2).** In a connected component choose an edge uv. A shortest path of length at least three would contain an induced P4, so every vertex is within distance two of u. If a vertex w is at distance two from u via a and is not adjacent to v, the path v--u--a--w is induced (triangle-freeness excludes v--a), a contradiction. Hence every vertex is in N(u) or N(v). These neighborhoods are disjoint and individually independent by triangle-freeness. If l in N(v) and r in N(u) are nonadjacent, l--v--u--r is an induced P4 (the cases l=u or r=v already have the edge). Therefore all cross edges are present, proving the component complete bipartite.

## Dynamical relevance and limit

For a general hub graph, `R=A+ν_G(x_sat)` retains an internally positive activity notion. But a reverse arm `hub -> A+X_free` at either witness decreases ν by two and increases A by only one, hence decreases R despite A=0. Scaling the P4 witness to counts M gives a decrement channel at order M² without a positive A factor. The compound-seed proof's A-dependent bad-forward-rate bound therefore fails for this matching inventory.

The graph condition is **sharp for this universal one-Lipschitz hub-removal property only**. It does not classify stable networks, all usable activity inventories, all sampled-time constructions, or the largest family admitting a corrector. A particular network may omit the offending reverse arm or admit a different inventory. The separate constructor's conservative UNKNOWN remains appropriate.
