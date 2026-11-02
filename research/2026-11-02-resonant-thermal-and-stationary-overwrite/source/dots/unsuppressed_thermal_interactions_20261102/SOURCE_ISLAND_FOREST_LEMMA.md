# Abstract source-island forest lemma: sufficient hypotheses and counting

This is the explicit combinatorial operation following `CONNECTED_SOURCE_CONSTRUCTION.md`. It isolates the dictionary assumptions needed to apply it to the native compiler. Constants below are deliberately padded. This does not assert the actual generic-V dictionary satisfies the hypotheses without inspection.

## 1. Objects and hypotheses

Let X be a bounded-degree graph of clock/support sites. A source island I has a nonempty finite support C(I) subset X, a trajectory/pin label, and a complex measure z(dI). Collections of islands must have pairwise disjoint supports. Overlap is encoded by setting the joint moment to zero.

For any finite collection S of labeled islands, suppose its scalar-normalized reference moment has the EXACT form

`M(S) = M_base(S) exp{ integral_E w(dT) [product_(I in S) B_I(T)-1] }`.

Require:

(A) `|M_base(S)|<=1`, M_base(empty)=1, and M_base factorizes across disconnected induced components of the graph joining I,J when their support sets are within graph distance two. These facts are established by the positive-nonwinding-singleton Poisson extraction, provided the source dictionary is exact.

(B) `|B_I(T)|<=1` and `B_I(T)=1` unless C(I) intersects an influence set K(T) subset X. (Deletion of a source clock is B_I=0.)

(C) Residual events obey the weighted local absolute bound

`L_* := sup_(x in X) integral_(T: x in K(T)) |w|(dT) exp[(log 3 + 3)|K(T)|] < infinity`.

There may be arbitrary event arity and complex signs. In the intended model K(T) is the closed neighborhood of the rod-cluster support, so |K(T)|<=D n(T). This norm is paid by the strengthened per-rod KP weight and is O(beta J0), with parameter-dependent constants explicitly charged.

(D) Let d_2 bound the number of sites in a distance-two neighborhood. Define a stability-inflated source measure

`z_*(dI)=|z|(dI) exp[(d_2 log 3 + 2 L_*) |C(I)|]`.

Assume its rooted support norm obeys

`rho := sup_x integral_(I: x in C(I)) z_*(dI) exp[|C(I)|]`

` <= min{1/4, 1/[32(1+d_2+L_*)]}`.

All integrals can first be finite discrete sums, then extended by absolute convergence. For a countable unbounded label set, apply the estimates uniformly to finite truncations.

## 2. Exact connected expansion

Expand M_base into its cumulant blocks, using partition Möbius inversion. The dependency-graph tree inequality bounds a block B by `2^(|B|-1)` times the sum of trees on the distance-two overlap graph of B (a larger universal tree constant can instead be absorbed into d_2).

Möbius-invert the residual logarithm:

`U_A = integral_E w(dT) product_(I in A)[B_I(T)-1]`.

Then expand `exp(U_A)=1+f_A`. The logarithm of the source generating function selects exactly those configurations whose union of base cumulant blocks and residual hyperedges is connected. This follows from the ordinary labeled exponential formula, before any absolute-value estimate.

## 3. Stability extraction without exp(exp L)

For a fixed compatible collection S, put u_A=|U_A|. Each residual event T can affect at most |K(T)| islands, since their supports are disjoint and each affected island occupies a distinct site of K(T). Thus

`sum_(nonempty A subset S) u_A`

` <= integral |w|(dT) [3^(number of affected islands)-1]`

` <= sum_(I in S) sum_(x in C(I)) integral_(T:x in K(T)) |w|(dT) 3^|K(T)|`

` <= L_* sum_(I in S) |C(I)|`.

Also `1+|f_A|<=exp(u_A)`. Therefore the residual graph sum has stability cost at most `exp[L_* sum_I |C(I)|]`. It does not have cost exp(sum |f_A|).

The base-block tree majorant can be enlarged to a graph sum with edge weight 2 on the distance-two overlap graph. For a compatible collection its number of edges is at most `(d_2/2) sum_I |C(I)|`. Its nonselected-edge cost is bounded by `3^(number of edges)`, already paid by z_*.

## 4. Exploration hyperforest and row estimates

After stability extraction, view each residual hyperedge as selected with probability `1-exp(-u_A)<=u_A`. Any connected realization admits a deterministic exploration rooted at the marked island: whenever an edge/hyperedge first meets the explored set, it adds its previously unseen vertices; discard edges adding none. This yields a bipartite exploration forest whose hyperedge nodes may have several new island children.

This operation has two important features:

- no effective hyperedge is required to have bounded arity;
- a hyperedge bringing k new islands pays their k source measures. Extra choices of already-seen versus new children can be bounded by the available exponential cardinality weight, rather than by an arity factorial.

Suppose inductively that the rooted mass of a child island is at most `z_*(dI) exp[|C(I)|]`, so its mass hitting any fixed site is at most rho.

For base edges, a parent island I sees child supports meeting its distance-two neighborhood. Their total mass is at most `d_2 rho |C(I)|`, up to the already-padded fixed tree-edge constant.

For a residual event T affecting a parent I, summing nonempty sets of child islands meeting K(T), with their measure and response bound |B-1|<=2, costs at most

`exp[2 rho |K(T)|]-1`.

This is an upper bound: it drops disjointness and any requirement that all old hyperedge vertices already be present. With rho<=1/4,

`exp[2rho k]-1 <= 2rho k exp(k/2)`.

The factor k and all exploration subset choices are dominated by the exponential spare in definition (C). Integrating over T, and marking one parent site in C(I), bounds the residual child budget by a padded

`8 rho L_* |C(I)|`.

Together the total branch budget is at most

`16 rho (d_2+L_*+1)|C(I)| <= |C(I)|/2`.

Unordered branches exponentiate with their usual 1/k! factor. Therefore the rooted-forest recursion preserves the inductive bound `z_* exp(|C|)`, with strict slack under (D). Start with finite-height forests and pass monotonically to arbitrary height. This establishes absolute summability of the connected source majorant and a finite per-site rooted norm.

The exact numerical factor 32 is not sharp; if the selected dependency-graph tree convention has a larger universal constant, increase 32 and the fixed d_2 coefficient together. No factor depends exponentially on beta*M0.

## 5. Construction of source islands from local insertions

An exact generic-V application can use the following unique grouping, provided its dictionary has the required locality:

- vertices are individual V insertions, including their local Pauli/matrix-unit/bath labels and ordered times;
- join two vertices if their complete affected support sets overlap (clock pins, syndrome-changing clocks, shared data sites, and shared bath sites all count);
- take connected components as source islands;
- keep all insertion labels/times inside each island, and assign every occupied clock to that island once.

Different islands then have disjoint complete supports. Every clock's scalar nonwinding pressure is canceled once per occupied column, not once per V insertion. Local multi-clock source terms are internal island bonds, not discarded constraints.

For an island with m insertions and at most b_c m affected clock/support sites, its bare absolute measure can be bounded using full-column traces, local decomposition l1 norms, and its ordered-time simplex. A standard rooted tree enumeration of overlapping local insertion supports gives an island root norm controlled by a geometric series in

`q_micro = beta*v * C_dictionary * K^(b_c) * exp[beta(J0+delta_beta)b_c]`.

The local overlap count, source-filling spatial weights, and e^(constant*m) connected-set enumeration must be included in C_dictionary (or displayed separately). Repeated insertions are allowed; the time simplex/indistinguishable-label factorial cancels the factorial tree-label growth in the usual way.

Inserting the stability factor from (D), a sufficient admission has the form

`beta*v * C_dictionary * K^(b_c)
 * exp{ b_c[ beta(J0+delta_beta)+C d_2+C L_*+1] }
 * C(1+d_2+L_*) << 1`.

Because L_*=O(beta J0), this is the desired exp(O(beta J0)) source cost, with no exp(beta J0 K) self-energy charge. It is polynomial in K only if b_c and the dictionary l1 overhead are held fixed; generic dressed clock perturbations can have b_c=O(K).

## 6. Scope of the result

The connected combinatorial operation is now explicit: positive singleton extraction -> bounded dependency-graph base cumulants -> residual hyperedges -> stability extraction -> exploration hyperforest. It does not use the invalid implication from moment bounds alone to cumulant convergence.

The remaining application-specific obligation is to verify the exact source dictionary and its complete affected-support definition, including bath traces and syndrome seams. If those objects satisfy (A)–(D) and the displayed insertion-root measure bound, this lemma gives connected-source convergence. The lemma is not evidence that an uninspected dictionary automatically satisfies them.
