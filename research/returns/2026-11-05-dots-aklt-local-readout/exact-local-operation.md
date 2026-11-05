# Exact local sampling, physical observable and complete cost scope

The [local theorem](package/square_aklt_local_sampler_20261105/LOCAL_SAMPLING_THEOREM.md), [primitive proofs](package/square_aklt_local_sampler_20261105/PRIMITIVE_PROOFS.md), [query-local physical operation](package/square_aklt_local_sampler_20261105/QUERY_LOCAL_PHYSICAL_OPERATION.md), and [physical observable audit](package/independent_audit/PHYSICAL_CORRELATOR_AUDIT.md) give the construction behind the [reported correlation](README.md).

## Routed loop measure and all-length control

A loop is an unoriented cyclically routed edge-simple closed square-lattice trail. Vertices may be visited twice, and the routing records the pairing at a four-valent vertex. Its activity is `w_gamma=3^(1-L_gamma)(3/5)^r_gamma`. Distinct loops sharing an edge are incompatible; otherwise their pair factor is `(3/5)^c` for c shared vertices. The scalar partition function is the identity/trace component of the AKLT boundary Gram operator, not that full operator.

The [raw contraction theorem](package/square_aklt_operator_bridge_20261105/RAW_LOOP_CONTRACTION_THEOREM.md) includes identical-loop self-exclusion and bounds the exponentially length-weighted kernel below 0.996411. The stronger [short-tail theorem](package/square_aklt_operator_bridge_20261105/SHORT_TAIL_GREEN_THEOREM.md) gives type-weighted contraction at most 0.907806 at the actual parameter point, with short-type weights at least 0.711122124 and weight 1 for loops of length at least 14. These are all-length statements, not a catalog truncation. The planar/open-box scope does not silently cover physical periodic winding loops.

## A finite-query oracle with no enclosing physical box

For any finite nonempty vertex query K, the local birth proposal rate is

```text
lambda_local |K|,
lambda_local=66455976045001/166988328468480<0.397967791.
```

Null proposals are included. A killed Doob transform of a rational Green supersolution on a memory-six trail automaton and auxiliary 16x16 torus proposes arbitrary-length routes. This torus is a proposal majorant, not a periodic physical boundary. Actual closure, no repeated physical edge and optional open-box membership are checked in true lattice coordinates. A final rational contact correction pays for forgotten self-contacts.

A loop meeting K has exactly 2k_K rooted oriented encodings, counting cyclic visits rather than distinct vertices. The rate factor 3/2 and final 1/k_K correction give exactly w_gamma. The independently checked 4x4 enumeration includes 793 loop types and 21,288 encodings, including crossings and revisits. Enumeration checks the implementation locally; telescoping/counting and all-length bounds support the full theorem.

## Shared ancestors belong to one marked Poisson process

Every loop type has Poisson births and exponential mean-one lifetimes. Each overlapping pair of cylinders has one conflict mark, reused whenever the same pair is encountered. Query all candidate cylinders alive at time0 and meeting K, then explore their older marked parents and clean oldest first.

After earlier child queries, the unrevealed cylinders remain conditionally Poisson outside the seed region, with intensity multiplied by the relevant earlier-child delta factors. Fresh parents are sampled from that residual intensity; existing atoms and cached pair marks are reused. Rejected fresh candidates are auxiliary thinning proposals, not newly exposed atoms. Different births with the same geometric loop remain distinct cylinders. Independently redrawing a separate parent cloud for each child would not implement this law.

Symbolic exponential times use lazy uniform bits and rational logarithm enclosures. Shared atoms cancel before comparisons; refinement continues until strict separation. Almost-sure finite clans and comparisons give almost-sure termination without time, loop or ancestor cutoffs. Each fresh sample call is a new independent joint marginal; adaptive extension of an already returned infinite configuration is not implemented.

## Resource theorem and its limits

For fixed finite K, independently checked bounds give expected retained clan length below 34.481635|K|, retained cylinders below 6.539013|K|, birth-oracle calls including nulls below 14.120548|K|, and attempted loop-walk steps below 171.505|K|. No enclosing physical volume enters these counts. Query size and coordinate bit length still cost work.

The [discovery-forest resource proof](package/independent_audit/LOCAL_RESOURCE_PROOF.md) gives a joint exponential moment for retained type weight A and all proposals P:

```text
E exp(10^-8 A+10^-8 P)<=exp(0.000002039 |K|).
```

It pays for history scans, known pairs and rejected proposals, without assuming the merging ancestor DAG is an independent branching tree. The [lazy-time proof](package/independent_audit/LAZY_TIME_COST_PROOF.md) additionally pays exact-time refinement, symbolic/rational arithmetic and the Poisson primitive. The unbounded random source-path query is covered too, giving qualitative finite expected arithmetic for a complete physical attempt.

These statements are not linear bit complexity, a useful small universal bit-operation constant, a deterministic runtime or a bounded-memory theorem. Scans can be quadratic in realized clan size and canonicalization pays path-length costs. The mathematical algorithm has no finite deterministic worst-case runtime. Published timings are observations rather than latency guarantees.

## Physical pair and secondary observables

The [thermodynamic join](package/square_aklt_local_sampler_20261105/THERMODYNAMIC_PAIR_JOIN.md) uses a finite sampled path and its finite ancestor clan under a common infinite Poisson construction. Every sufficiently large open box eventually contains them, identifying the virtual-identity-boundary pair limit. Perfect normalization does not reconstruct every boundary coefficient, and additive accuracy does not make exponentially small distant correlations easy at relative accuracy.

The [quadrupole audit](package/square_aklt_quantum_observable_audit_20261105/OBSERVABLE_AUDIT.md) and [uniform bound](package/square_aklt_quantum_observable_audit_20261105/quadrupole_uniform_bound.json) preserve additional local loop-incidence observables and fluctuation bounds. Equal-time correlation sums are not Kubo/static susceptibility. None of these operations is quantum-state preparation, a spectral-gap proof, arbitrary-boundary uniqueness or continuous O(3)-spin sampling.
