# Polynomial acquisition of the exact cover inventory (separate compiler addendum)

**Candidate; independent review pending.** The frozen eleven-file cover theorem
is preserved byte-identically under `frozen_cover_source/`. This addendum removes
its exponential subset enumeration; it does not change its CTMC class, function,
profile constants, inequalities, or stationary conclusions. No new graph-algorithm
novelty is claimed. The derivation is self-contained; no external source is used.
In particular the parent's inaccessible Citeseer maximum-clique source is not
retried, mirrored, read or cited as verified.

## 1. Exact finite circuit, acquired from the graph

Let G be the nonempty satellite graph satisfying the frozen theorem's condition:
no induced triangle plus isolate and no induced P4 plus isolate. For every vertex
v form its anti-neighborhood U_v=V\(N(v) union {v}). The induced graph on U_v contains
no triangle or P4, because v would be the isolated vertex in the forbidden pattern.

Every connected triangle-free and P4-free graph with at least one edge is complete
bipartite. Here is an elementary proof. A shortest odd cycle in a nonbipartite
triangle-free graph has length at least five and is chordless; its first four
vertices form an induced P4. Thus the graph is bipartite. If a connected bipartite
graph omits a cross-shore edge, a shortest path between those two vertices has odd
length at least three, and its first four vertices induce a P4. Contradiction.
Singleton components are isolated vertices. Ordinary BFS two-coloring plus all
cross-pair checks therefore acquires each U_v's biclique components and isolates.
No decomposition is supplied as input.

For arbitrary nonnegative satellite weights x, maximum independent-set weight is

    alpha_x(G)=max_v [x_v + sum_(isolates w in U_v) x_w
                    + sum_(bicliques L,R in U_v) max(x(L),x(R))]. (1)

An independent set containing v consists of v and an independent set in U_v.
On a complete bipartite component it chooses one whole shore; nonnegative weights
permit inclusion of all isolates. Conversely every set on the right is independent.
Every nonempty independent set has an anchor v. An optimum can be taken nonempty
even when every weight is zero. This proves both directions of (1), including ties.

Since complements of vertex covers are independent sets,

    tau(x)=sum_v x_v-alpha_x(G).                              (2)

This is EXACTLY the inventory value used throughout the frozen theorem, not an
approximation or a new Lyapunov assumption. The representation is a finite max-plus
circuit: all anchor records together contain O(m^2) vertex occurrences. Scanning
all anti-neighborhoods, BFS adjacency work and complete cross-pair checks costs
O(m^3) elementary graph operations after the frozen raw forbidden-pattern test.
The raw graph test itself costs O(m^5) with the direct 4-/5-subset implementation.
Weighted evaluation takes O(m^2) additions/comparisons on integers of bit length
at most input weight bits plus O(log m), hence polynomial binary bit complexity.
No 2^m cover-mask enumeration occurs.

## 2. Witnesses and adverse-edge queries without all optimal covers

Choose an anchor attaining (1), include all its anti-neighborhood isolates and an
attaining shore in every biclique. This gives an optimal independent set. If needed,
greedily extend it to maximality; any newly addable vertex has zero weight, since
otherwise optimality would be contradicted. Its complementary structural cover
is inclusion-minimal and attains tau. This earns a concrete witness in polynomial
time even with zero-weight ties.

For an enabled edge ij, so x_i,x_j>0, set their weights to zero, leaving the graph
and compiled circuit unchanged. Then

    some optimal minimal cover contains i and j
       iff alpha_(x with x_i=x_j=0)(G)=alpha_x(G).             (3)

Setting those weights to zero computes the same optimum as deleting i,j: remove
any zero-weight endpoints from an independent set without changing its weight.
Equality is precisely existence of an original optimum avoiding both endpoints.
Extend that optimum to a maximal independent set. Neither positive-weight endpoint
can be added, because that would improve its original objective. Its complementary
minimal optimal cover contains both. The reverse implication is immediate.
The enabled-edge qualification matters for a claim about minimal covers; inactive
zero-product edges do not contribute to generator bounds.

Thus all bad active hubs used in the proof can be queried by O(|E|) evaluations of
the SAME acquired circuit, with no all-covers or weighted-optimization oracle.
These queries are not required to evaluate W itself; they expose exact receiving
of the proof's state-dependent mechanism. The pointwise proof still correctly
quantifies over all optimal covers and retains every tie.

## 3. Whole certificate semantics and costs

`cover_circuit.py` imports only the frozen raw parser, scalar helpers and rational
profile evaluator from `frozen_cover_source/cover_seed.py`. It does not call that
module's cover enumeration or numerical constructor. Its quantitative routine
reconstructs the same profile/constants, replacing the cover list by this circuit.
The frozen profile formulas and subsequent Foster proof apply verbatim via (2).

`qualitative(raw)` now returns the acquired polynomial-size circuit as part of its
finite structural receipt. It still does not materialize a requested-t profile.
`numerical(raw,t,max_profile_steps=...)` pays K-1 backwards steps and J-1 head
compensations, retaining their exact rational values, circuit, and factored bound.
A profile budget refusal remains `UNKNOWN_NUMERICAL_BUDGET` WITH the qualitative
conclusion. Unsupported raw structure remains stability UNKNOWN.

Only GRAPH inventory acquisition/evaluation is claimed polynomial. The rational
profile's length/bit growth, q, N_*, or complete numerical certificate acquisition
can still be enormous relative to binary input rates. Powers and exception sets
remain factored/unexpanded. No hostile-input service admission, small practical
constant or polynomial-size expanded numerical moment bound is claimed. Scaled
LW/t^N evaluation uses degree-two raw propensities, the exact circuit and rational
tail/head evaluation, with polynomial work in the already-materialized certificate
and binary count input; actual W=t^N h may have exponentially larger output.

Same-implementation `receive_*` routines are author self-checks, not independent
receivers. Trusted internal helper arguments are not externally certified objects.
The imported prototype's process-level decimal conversion guard setting is retained
and explicit. This is not a security-hardened service.

## 4. Limits and provenance

All frozen mathematical conclusions and qualifications are unchanged: exact raw
one-port binary hub architecture, all positive rates, arbitrary fixed t>1; not
general weak reversibility or arbitrary one-port conservative stability. The sharp
triangle+isolate/P4+isolate near-cone obstruction and ordinary detailed-balance wins
remain. No negative graph receipt establishes instability.

This is an ordinary neighborhood decomposition and weighted independent-set
construction, not a new algorithm claim. Its contribution here is removing an
unnecessary acquisition oracle/cost from the exact CTMC certificate representation.
The prior source-access failure remains disclosed and quarantined in the frozen
scope note. No source transfer, upload, publication or operational action occurred.
