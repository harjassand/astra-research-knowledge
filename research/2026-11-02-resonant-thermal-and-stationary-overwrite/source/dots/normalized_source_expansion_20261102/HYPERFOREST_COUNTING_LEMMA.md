# Explicit connected-hypergraph counting after Poisson saturation

2026-11-02. This closes a combinatorial sublemma, conditional on the bounded dependency-graph base cumulant bound and the uniform residual hyperedge majorants in `unsuppressed_thermal_interactions_20261102/CONNECTED_SOURCE_CONSTRUCTION.md`. It does not verify the generic source-molecule dictionary.

Let V be a finite set of possible source sites. A source set S has activity at most q^|S|. Suppose:

1. Base cumulants satisfy `|kappa_base(B)| <= sum_{trees T on G0[B]} c^(|B|-1)` for nonempty B, including singleton bound 1. G0 has maximum degree Δ.
2. Residual hyperedges |A|>=2 have nonnegative, trajectory-uniform majorants u_A and `|exp(U_A)-1| <= exp(u_A)-1`.
3. Residual singleton factors cost at most exp(l1) per source.
4. For some a>=log 2, `sup_i sum_{A contains i} u_A (1+exp(a))^(|A|-1) <= l2`.

The same conclusion holds in infinite volume by a uniform finite-volume majorant.

## Graph stability extraction

Expanding base moments into cumulant partitions and replacing every block by its tree majorant gives exactly a sum over forests of G0[S], with edge weight c. Enlarge the forest sum to all graphs, retaining the requirement that graph plus chosen residual hyperedges connects S. This is an upper bound because all terms are nonnegative.

The resulting graph/hypergraph sum equals

`(1+c)^(|E(G0[S])|) exp(sum_{A subset S, |A|>=2}u_A)`

multiplied by the probability that an independent random hypergraph is connected. Its pair-edge probabilities are c/(1+c), and residual hyperedge probabilities are 1-exp(-u_A)<=u_A. The prefactor is at most

`exp{[Δ log(1+c)/2 + l2]|S|}`.

Include singleton factors and set

`q_eff = q exp[l1+l2+Δ log(1+c)/2]`.

## Trimming exploration witnesses

Explore any connected selected hypergraph from a prescribed root. Each discovery edge A adds a nonempty set N of newly reached vertices; choose one already reached parent i in A. Replace A by B={i} union N. All vertices of A outside B have already been reached and need not be retained in the witness. The discovery edges, with these trimmings, form a rooted hypertree covering S.

Use a deterministic parent/exploration convention to obtain a witness; union bound over all witnesses is valid. Original selected edges are distinct, so their probabilities multiply. Dropping the distinctness restriction in the majorant only adds nonnegative terms.

For each trimmed residual edge B use the effective weight

`v_B = sum_{A contains B} u_A`.

Pair edges of G0 have weight at most 1. Summing the possible original edges and all trimming choices gives

`sup_i sum_{B contains i, |B|>=2} v_B exp[a(|B|-1)]`

` <= sup_i sum_{A contains i} u_A [(1+exp(a))^(|A|-1)-1] <= l2`.

The rooted label i is fixed; no hidden factor |A| is needed. Allowing multiple parent choices is already covered by counting all rooted hypertrees. A deterministic actual exploration chooses just one of them.

## Rooted recursion and explicit sufficient radius

Let T_i be the total majorant of rooted hypertrees at i, with vertex factor q_eff. Allow arbitrary distinct-label violations and repeated branch choices to overcount. The standard unordered-branch exponential bound gives

`T_i <= q_eff exp[ sum_{j:ij in G0} T_j + sum_{B contains i, |B|>=2} v_B product_{j in B\{i}} T_j ]`.

This is understood as a domination by the smallest nonnegative formal solution. If all T_j<=t<=1, the exponent is at most `(Δ+l2)t`: every hyperedge has at least one child and the unweighted v-row is <=l2. Therefore the explicit choice

`q_eff <= (1/2) exp[-(Δ+l2)/2]`

makes t=1/2 a supersolution. Monotone iteration from zero is bounded by it. The sum of connected absolute weights rooted at a site is consequently finite, uniformly in |V|.

Equivalently a sufficient source activity is

`q <= (1/2) exp[-l1-(3/2)l2-(Δ/2)(1+log(1+c))]`.

This conservative radius has only exp[O(Δ+l1+l2)] loss. In the intended application l1,l2=O_{D,kappa}(βJ0), Δ=O(D²), and there is NO exp(βJ0K) loss. Spare per-source or spatial weights can be included by replacing q with its weighted version before applying the inequality.

## Limits

The proof requires pointwise, trajectory-independent u_A with the displayed GLOBAL row bound, not merely a row bound after an incompatible source-dependent averaging. Such u_A can be formed from the absolute native residual cluster measure, the support-incidence indicator, and |B_i-1|<=2 in the distinct-clock setting. The weighted native KP cost must be paid first.

For source molecules, vertex activities and degrees become size-dependent. One must repeat the rooted recursion with molecule charge and native-clock incidence; this note does not silently identify a molecule with a single clock.
