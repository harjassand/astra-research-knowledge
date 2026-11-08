# Two-body first-discovery proof of the full-noise spatial response

> Release-copy note: this historical proof/review snapshot has presentation-only edits recorded in SOURCE_PROVENANCE.json. Mathematical content is unchanged. Current status and superseded steps are identified in START_HERE.md and DEPENDENCY_MAP.md at the package root.

8 November 2026. This is the explicit repair of the multi-site-target issue found during independent review. It replaces the source-dependent language claim in WORD_LIFT_LEMMA.md for the actual nearest-neighbor, at-most-two-body model. Higher-arity interactions are not covered by this proof.

## 1. Setup

Let the physical interaction graph have maximum vertex degree at most Delta. Group all Hamiltonian contributions on a given two-site edge into one Hermitian H_e, and on each site into an on-site term. Every grouped term has operator norm at most h in every classical-label assignment. The K labels are central coefficients, not physical vertices. Retain D=sum_i gamma(E_i-Id) on every physical qubit.

Choose q targets S_i inside buffers B_i. The buffers are vertex-disjoint and no Hamiltonian edge connects two different buffers. Every physical Hamiltonian factor controlled by selected label i is contained in S_i. Put R_*=V minus the union of buffers. The initial operator M is supported in R_* and independent of all labels. Its true support may be much smaller than R_*.

Let Q(X)=2^{-K}sum_sigma(-1)^{K-|sigma|}X(sigma). The desired mixed finite difference is 2^K Q. A word with no factor carrying one selected label is killed by Q.

## 2. First-discovery tree of a Hamiltonian word

Consider an ordered word in on-site and two-site Hamiltonian commutator letters. Initialize the visited vertices to all of R_*. Process the factors in chronological order:

- If a factor has no visited endpoint, declare the word geometrically null. Indeed it is disjoint from the initial support and all preceding factor supports, so its commutator evaluates to zero.
- If an on-site factor is visited, or both endpoints of an edge are visited, do not change the tree.
- Otherwise, an edge has exactly one visited and one unvisited endpoint. Record this occurrence as the discovery of its new endpoint, whose parent is the old endpoint. Mark the new endpoint visited.

Contract R_* to a single root. Recorded discovery edges form a rooted tree, with a unique path to every discovered vertex. For each target S_i, stop its target record at the first discovery of any vertex in S_i. If there is no such event, the word contains no factor carrying that selected label, and Q kills it.

For a word visiting every target, retain the discovery-tree path from the root to that first target vertex. Write it as

    v_i,0 -- e_i,1 -- v_i,1 -- ... -- e_i,l_i -- v_i,l_i,

where v_i,0 is in R_*, the remaining vertices are in B_i, and only the final vertex is in S_i. The path is self-avoiding. A root-to-target path cannot travel through a different buffer: entering the exterior again would terminate its ancestry at the root. Thus retained paths for different targets have disjoint physical edge factors and disjoint nonroot vertices.

The irreducible skeleton is the chronological shuffle of all retained discovery-edge occurrences. It preserves each path's edge order. Return paths and repeated uses after discovery remain in the word; they are not discarded.

## 3. Exact allowed intervals, including the whole target

At a stage where k_i of path i's edges have occurred, define its forbidden set by

    F_i(k_i) = S_i union {v_i,k_i+1,...,v_i,l_i},  if k_i<l_i;
    F_i(l_i) = empty.

The full forbidden set is the union over unfinished targets. An interval Hamiltonian letter is allowed exactly when its physical support avoids this full set. Crucially, the ENTIRE multi-site S_i stays forbidden before the designated first arrival, not only the endpoint of the chosen path.

### Necessity

Take a geometrically non-null word and its retained discovery paths. Before the designated discovery of any retained path vertex, no earlier factor can touch that vertex: the first such non-null edge would discover it with a different recorded parent. Before the designated target event, no earlier factor can touch any site of S_i, because that would be an earlier target visit. Therefore every nonskeleton factor lies in the allowed alphabet of its interval.

The skeleton occurrences themselves are unique: they are the first-discovery occurrences of the specified vertices. Cutting the word at those occurrences gives a unique interval decomposition.

### Sufficiency

Conversely, choose self-avoiding paths as above, a shuffle preserving their internal orders, and arbitrary allowed interval words. Suppose the resulting Hamiltonian word is not geometrically null. Immediately before its next designated skeleton edge, all prior vertices on that path are visited. Its new endpoint is unvisited, since every earlier interval avoided all still-undiscovered retained vertices, and skeleton edges of other buffers cannot visit it. Hence that edge uniquely discovers the designated endpoint from its designated parent.

Before the final path edge, every interval avoided the whole S_i and no earlier path vertex belonged to S_i. That final edge therefore gives the actual first target visit. Induction over the skeleton establishes that the word's first-discovery paths and skeleton are exactly the ones prescribed.

Thus every non-null word visiting all targets appears exactly once in this free-interval expansion. Extra interval words may be geometrically null; they evaluate to zero. Words with no visit to a selected target are killed by Q. No matrix cancellation or final-support property is used in this bijection.

## 4. Full local noise lifts the bijection exactly

Now allow arbitrary D_i letters in the word and erase them before constructing the discovery tree. Each D_i preserves every physical support subspace and introduces no classical-label dependence. Therefore a disconnected-prefix null word still evaluates to zero after any D insertions; an untouched target still leaves its label absent.

For every other word, its skeleton Hamiltonian occurrences are uniquely located after erasure and at uniquely corresponding positions before erasure. Every D letter belongs to one and only one interval. Conversely arbitrary D letters may be inserted in every interval. No D letter is commuted past a Hamiltonian factor.

The free interval alphabet is consequently ALL physical D_i, plus the allowed Hamiltonian letters for that stage. Summing each interval gives the propagator generated by full D and the corresponding allowed Hamiltonian subset. The Taylor coefficients agree word by word: at total word length n each contribution has T^n/n!. Summing interval lengths is precisely the ordered-simplex/Duhamel identity. Finite-dimensional absolute convergence legitimizes this reorganization.

Hence Q exp(TL)M equals the sum over path families and skeleton shuffles of their ordered integrals, with the full-noise allowed-subset propagator between every pair of skeleton insertions.

## 5. Hypercontractivity and paths

Choose p(t)=1+(p_0-1)exp(2gamma t), or cap this schedule at the requested p_1. Every interval's full-noise physical semigroup is hypercontractive between its endpoint exponents. On the normalized direct-sum algebra, the undamped K labels cost at most 2^{K(1/p_before-1/p_after)}. These factors telescope. Each commutator insertion costs at most 2||H_e|| in its current exponent.

The normalized Fourier average Q is a Schatten-p contraction from the direct sum to the physical algebra. Recovering the Boolean finite difference costs 2^K. The initial label-independent norm equals the physical norm.

For a path family with lengths l_i and total l, the number of order-preserving shuffles is l!/product_i l_i!. Each ordered simplex has volume T^l/l!. Consequently the summed bound factorizes into one physical path sum per target:

    ||Delta_all Phi_T(M)||_(p_1,tau)
      <= 2^{K(1+1/p_0-1/p_1)} ||M||_(p_0,tau)
         product_i sum_(paths Gamma_i) (2T)^|Gamma_i|/|Gamma_i|!
                                            product_(e in Gamma_i)||H_e||.

This holds whenever p_1-1 <= (p_0-1)exp(2gamma T).

## 6. Explicit physical path count

Let the root-to-target distance be at least r. Each path first enters B_i through its inner vertex boundary and ends at its first S_i vertex, necessarily on the target boundary. Count backwards from the final vertex in boundary S_i: at most Delta^l length-l walks start at each such endpoint. Therefore the number of retained paths is at most |boundary S_i| Delta^l, and hence at most |boundary B_i||boundary S_i| Delta^l when a target is reachable. No extra branching factor is omitted. For the square nearest-neighbor model Delta=5 safely dominates the four possible physical edges.

Put x=2h Delta T. For x<r, the elementary exponential Markov bound gives

    sum_(l>=r) x^l/l! <= inf_(alpha>1) alpha^(-r) exp(alpha x)
                      <= (e x/r)^r.

Thus each physical path sum is bounded by

    |boundary B_i||boundary S_i| (2e h Delta T/r)^r.

The candidate's delta=2 max_i |boundary B_i||boundary S_i| (2e h Delta T/r)^r is conservative. All earlier packing constants and the scalar sufficient condition therefore remain valid under this repaired two-body proof.

## 7. Tests and scope

check_first_discovery.py checks the exact word-language rule, without evaluating matrices, on 655,516 exhaustive/random words from a multi-site target graph with alternative paths/cycles and two separated multi-site buffers. Every geometrically causal word is either correctly absent for an unvisited target or occurs in exactly its recorded path family. The old target-omitting rule fails the explicit word 02,24,01,13 for target {3,4} and designated path 01,13. The corrected rule excludes that incorrect assignment.

The independent reviewer's physical 2-by-4 example gives a distinct nonzero Taylor-coefficient discrepancy for the literal old rule. Those checks explain why the repair is necessary. The general proof is Sections 2–4, not the finite tests.

The method of resumming reducible words into full propagators and the physical path counting are established techniques; compare McDonough et al., arXiv:2502.02652v2. This document supplies the explicit target-inclusive two-body construction needed here rather than asserting a literal import of the source's multi-site formula. No priority claim is made.

This fixes one analytic operation. It does not remove the exp(O(r^2 m)) activity-evaluation cost, supply a uniform all-time sampler, establish a practical speedup, or prove the same language rule for higher-arity interactions.

## 8. Physical-probe corollary for the finite-patch dependency

The same first-discovery identity also applies with the final observation map equal to a product of q normalized physical commutators, (1/2)^q product_i ad_(O_i), with ||O_i||<=1 and support O_i contained in S_i. A word that never visits one target is killed by its physical probe; disconnected words are zero as before. The final map is a contraction in every Schatten norm. There are no classical labels in this corollary.

Consequently the two-body simultaneous nested-commutator estimate used by the earlier finite-patch lemma follows directly from the repaired identity and the same physical path count. This closes the analogous multi-site-target proof dependency for the present two-body application. It does not validate the source's literal interval alphabet unchanged, or claim a proof for arbitrary higher-arity interactions.
