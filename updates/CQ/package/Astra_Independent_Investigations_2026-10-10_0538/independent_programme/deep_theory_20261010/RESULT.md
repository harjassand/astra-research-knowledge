# Closed investigation: stationary transport for directed triangles

Date: 2026-10-10. Status: **the proposed mechanism failed**. No Caccetta–Häggkvist bound was improved, and no foundational breakthrough or priority claim is made.

The investigation kept the actual uniform 0/1 row condition after its initial spectral probes. The decisive result is a fully explicit, strongly connected, triangle-free, 52-outregular graph on 160 vertices for which

    E_pi[d^-(v) + s(v)] = 104 - 2493/485524 < 2r,

where pi is the stationary distribution of the uniform random walk and s(v) counts vertices reachable in exactly two steps but not in zero or one step. Thus even a proposed repair that charges stationary indegree surplus against deficient second neighborhoods is false. Two separate exact implementations verified the construction.

This is a counterexample to the attempted intermediate inequality, **not** to Caccetta–Häggkvist. Here 160 > 3*52, so the original conjecture is respected.

## 1. Actual target and proposed mechanism

The directed-triangle case of Caccetta–Häggkvist asks whether a finite oriented triangle-free graph with minimum outdegree r must have n >= 3r+1. One may delete excess outgoing arcs to make every row of the adjacency matrix A have exactly r ones. Passing to a sink strongly connected component retains this property and cannot create short cycles.

Let P=A/r and let pi be its positive stationary distribution. For each vertex v, write

- I(v) = its incoming neighbors;
- S(v) = its outgoing neighbors, with |S(v)|=r;
- T(v) = (union of S(u) over u in S(v)) minus S(v) and v;
- s(v)=|T(v)|.

In a triangle-free oriented graph, {v}, I(v), S(v), and T(v) are pairwise disjoint. Consequently

    d^-(v) + s(v) <= n-r-1.                      (1)

The proposed route sought to average a reverse-step entropy gain and a forward two-step expansion under the same pi.

### A valid component: reverse-step entropy

The reversed transition is P*(v,u)=pi(u) A(u,v)/(r pi(v)). In a stationary chain,

    sum_v pi(v) H(P*(v,.)) = H(X_0|X_1) = H(X_1|X_0) = log r.

The middle equality follows because X_0 and X_1 have the same distribution. Since the reverse row has d^-(v) possible predecessors,

    sum_v pi(v) log d^-(v) >= log r,

and Jensen gives

    E_pi d^- >= r.                              (2)

This proof is valid; it does not imply anything comparable for exact second neighborhoods. Entropy monotonicity for P^2 concerns the union of first and second neighborhoods, so it cannot discard transitive two-step paths remaining in S(v).

### The missing charging step, written exactly

Let t(v) be the number of arcs induced by S(v). Let h(v) be the number of absent arcs from S(v) to T(v). Every arc leaving S(v) ends in S(v) or T(v); there are exactly r^2 such arcs. Hence

    r^2 = t(v) + r s(v) - h(v),
    r(s(v)-r) = h(v)-t(v).                       (3)

A stationary mass transport from transitive wedges to missing S-to-T arcs would need E_pi h >= E_pi t. The 64-vertex example below proves that the required transport capacity is actually insufficient. Allowing payment from the valid indegree surplus (2) still fails on 160 vertices. This is a falsified acquisition step, not an unproved conjecture being presented as a mechanism.

## 2. The internal 16-vertex graph H

Use disjoint sets A, B, C, D of sizes 4, 3, 4, 4 and one additional vertex u. Include all arcs

    A -> B -> C -> D -> A.

Inside A, include a directed 4-cycle. Also include the four arcs u -> A. Include no other arcs.

Every vertex has outdegree 4:

- an A vertex has one internal successor and three successors in B;
- a B, C, D, or u vertex has four successors in the next indicated block.

H has no digons or directed triangles. Any cycle involving different A/B/C/D blocks needs at least four block changes; the only internal cycle is the 4-cycle in A; u is a source. H itself need not be strongly connected, which is harmless because the full construction is strongly connected.

The exact indegrees and exact second-neighborhood sizes, constant on each named group, are:

    group       size       indegree       exact second size
    A             4             6                  5
    B             3             4                  4
    C             4             3                  4
    D             4             4                  3
    u             1             0                  3

In particular the uniform average second-neighborhood size is 63/16 < 4. The mean indegree is 4, as always. This non-Eulerian block is the source of the obstruction.

## 3. Dense, row-regular outer substitution

For an integer q>=1, let F_q have N=3q+1 vertices modulo N, with arcs i -> i+j for j=1,...,q. F_q is q-inregular and q-outregular, strongly connected, and triangle-free: a sum of two or three allowed positive jumps is positive and strictly less than N, so it cannot return to its start. Each vertex has exactly q exact second neighbors, at displacements q+1,...,2q.

Replace every vertex of F_q by one copy of H. For each outer arc, add every arc from the first H copy to the second. Denote the result by G_q. Then

    n_q=16(3q+1),       r_q=16q+4.

Every row contains exactly r_q ones. G_q is strongly connected because external complete arcs allow travel through the outer strongly connected graph and entry into any desired vertex of a block. A directed triangle entirely inside one block would be a triangle of H; a triangle using three blocks would project to one in F_q; a triangle using exactly two blocks would require an outer digon. None is possible.

For a vertex corresponding to x in H,

    d^-_G(x)=16q+d^-_H(x),
    s_G(x)=16q+s_H(x).                            (4)

The second identity can be checked by separating internal two-step walks from those that use an outer arc. Outer one-step blocks are excluded from the exact second neighborhood; the q outer exact-second blocks contribute all 16q vertices.

### Correct stationary normalization

Outer translation symmetry gives each H copy stationary mass 1/N. Let sigma be the conditional distribution inside an H copy, and put R=16q+4. Its exact equation is

    R sigma = q*1 + H^T sigma.                    (5)

The external inflow into **each internal vertex is q/R**, not 1/R. In particular sigma(u)=q/R. A transient exploratory substitution of 1/R for this quantity at q>1 was rejected because the masses failed to sum to one. No reported counterexample uses that erroneous normalization.

Since every row of H sums to 4, (5) gives sum sigma=16q/(R-4)=1. The full stationary probability of (outer vertex i, internal vertex x) is sigma(x)/N.

Let a,b,c,d,z denote total sigma masses of A,B,C,D,{u}. Equation (5) becomes

    R a=4q+a+4d+4z,
    R b=3q+3a,
    R c=4q+4b,
    R d=4q+4c,
    R z=q.

Using the group counts above,

    E_pi(s_G-r_q)       = a-d-z,
    E_pi(d^-_G-r_q)     = 2a-c-4z,
    E_pi(d^-_G+s_G-2r_q)= 3a-c-d-5z.              (6)

Solving these exact equations gives the joint gap

    -(256q^4 - 464q^3 - 568q^2 - 193q - 24)
    / [4(4q+1)(256q^3+240q^2+84q+13)].            (7)

The checker independently solves all 16 vertex equations and then verifies stationarity on every coordinate of the full graph. It does not rely only on these five aggregate equations.

### First failure: stationary second-neighborhood expansion

At q=1, n=64 and r=20. Equations (5)-(6) give

    E_pi s = 20 - 29/1186,
    E_pi d^- = 20 + 1283/11860.

Thus E_pi s>=r is false even with all the actual required assumptions: 0/1 adjacency, equal row degree, strong connectivity, and no directed triangles. The stronger joint inequality still holds in this example, with surplus 993/11860. It was therefore tested separately rather than being declared repaired.

### Decisive failure: the joint stationary repair

The joint gap is positive at q=2 (383/19134), but negative at q=3. Now n=160 and r=52. The five masses are

    a=2422/9337,
    b=7023/37348,
    c=9159/37348,
    d=121203/485524,
    z=3/52.

They sum exactly to one. The exact expectations are

    E_pi d^- = 52 + 20777/485524,
    E_pi s   = 52 - 895/18674
             = 52 - 23270/485524,
    E_pi(d^-+s) = 104 - 2493/485524.

This defeats the proposed use of (2) to pay the deficit in (3). The required net transport capacity, multiplied by r, is short by 2493/9337.

### Narrow amplification consequence

Replace each vertex of G_3 by t independent twins and each arc by all t^2 corresponding arcs. The resulting graph remains strongly connected, oriented, triangle-free, and rt-outregular. Every indegree and exact second count is multiplied by t; the mass of each clone is its old vertex mass divided by t. Hence its joint gap is

    -t*2493/485524.

Thus this particular proposed universal inequality cannot be repaired by an additive o(n) allowance over all such graphs. This is only a limitation of the stated stationary-average inequality, not an impossibility theorem for stationary methods or a new barrier for Caccetta–Häggkvist itself.

## 4. Earlier discarded simplifications

These are preserved to prevent reuse. They are not the central outcome.

### 4.1 Replacing minimum outdegree by spectral radius

Take four blocks of m vertices, each internally a transitive tournament, with all arcs from each block to the next cyclic block. This is triangle-free. Its adjacency spectral radius is

    rho=(2^(1/m)-1)^(-1),

because a block-symmetric positive eigenvector satisfies x_i=(1+1/rho)x_{i+1}, and its sum condition gives (1+1/rho)^m=2. Therefore rho/n tends to 1/(4 log 2)>1/3. The minimum outdegree is only m. This does not contradict CH; it refutes the attempted spectral-radius replacement.

### 4.2 Even uniform stationarity and quadratic energy are insufficient

On the same support, index internal positions i,j=0,...,m-1 and let D=11m-1. Set

    P_ij=6/D                            within a block if i<j,
    P_ij=(8m+2+6(i-j))/(mD)              into the next block,
    P_ij=0                              otherwise.

All entries on the support are positive, and direct summation shows every row and column sum is one. Thus pi is exactly uniform; there is no stationary skew to charge. Its squared Hilbert–Schmidt norm is

    ||P||_F^2=(32m+8)/(11m-1).

For m=12 this is 392/131=3-1/131. The support is strongly connected and has no directed cycles of length at most three. A nonnegative Markov kernel with invariant measure pi is a contraction in L2(pi), by conditional Jensen, so the example also has the contraction property. This refutes a lower bound of 3 based only on these weighted-kernel hypotheses. It does not have flat 0/1 rows, and does not refute an argument that genuinely uses that additional structure.

### 4.3 Choosing a maximum-stationary-mass vertex

A separately preserved 25-vertex, 6-outregular, strongly connected triangle-free graph has a unique maximum-pi vertex, numbered 5, with only five exact second neighbors. Its indegree is ten, so it is not a counterexample to a combined local inequality. Exact adjacency and the full rational stationary vector appear in `exact_maximum_pi_counterexample.json`.

## 5. Computation, reproducibility, and limitations

Run these from the workspace root:

    python independent_programme/deep_theory_20261010/verify_route_obstructions.py
    python independent_programme/deep_theory_20261010/verify_combined_counterexample.py

Both use exact rational arithmetic; SymPy is used only for finite linear algebra. The second script constructs the graphs directly, verifies the 0/1 row sums, every stationary coordinate, strong connectivity in both directions, all short-cycle exclusions, and all exact second-neighborhood counts. It writes full adjacency and full rational pi certificates for n=64 and n=160. An independent audit implementation and its full certificates are in `audit/`.

The earlier random and annealing scripts are retained, with outputs and deterministic seeds. They failed to find a violation of the stationary expansion claim. The subsequent structured construction falsified it. Those negative searches are not evidence for the false claim and must not be cited as validation.

No external paid computation, third-party contact, publication, repository push, or work on the user's computer was used.

## 6. Literature boundary and exact remaining status

Primary background checked:

- Hladky, Kral, Norin, *Counting flags in triangle-free digraphs*, arXiv:0908.2791v4: https://arxiv.org/abs/0908.2791 . The paper states the CH triangle target and proves the 0.3465 minimum-outdegree threshold using flag-algebra and inductive ingredients. No comparison here improves its bound.
- Sullivan, *A Summary of Results and Problems Related to the Caccetta–Haggkvist Conjecture* (AIM, 2006), Conjecture 6.15: https://aimath.org/WWN/caccetta/caccetta.pdf . It records the related unweighted Eulerian average second-neighborhood conjecture, attributed to Seymour/Jackson. This investigation's false stationary generalization must not be advertised as a newly established version of that question.

A search did not establish prior-art status for these precise counterexample formulas. Accordingly no novelty or priority claim is made.

The valid reverse-entropy lemma survives. Its proposed use to acquire sufficient second-neighborhood expansion does not: both the expansion claim and the explicit indegree-paid repair are false. There is no pending proof obligation for those false statements. A successful CH mechanism would need genuinely different additional structure or a different local-to-global certificate, rather than assuming either failed inequality. None has been acquired here. This branch is closed rather than promoted as a promising reduction.
