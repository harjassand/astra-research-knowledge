# Solver-enabling structure acquisition: candidate, proof, and rejected novelty claims

Internal research note, 31 October 2026. This is a complementary investigation, not a claim of a foundational breakthrough.

## Prize

Acquire an operation or geometry that enables exact global optimization over exponentially many configurations in every future task, including arbitrary dense interaction graphs. Recovering an individual sparse graph is not the target.

## Algebraic tractability route and a governing obstruction

A natural target is a polymorphism of a shared finite constraint language. A suitable polymorphism certifies tractability for all future instances over the language, independent of interaction-graph treewidth. However, discovering the algebra is a separate computation and can be harder than exploiting it.

Primary sources:

- Chen and Larose, *Asking the metaquestions in constraint tractability*, arXiv:1604.00932v2 (2017), https://arxiv.org/abs/1604.00932 . Their metaquestion framework directly covers discovering tractability polymorphisms; relevant metaquestions are NP-complete.
- Bodirsky and Weiss, *The Complexity of Finding Coset-Generating Polymorphisms and the Promise Metaproblem*, ICALP 2026, https://drops.dagstuhl.de/storage/00lipics/lipics-vol374-icalp2026/html/LIPIcs.ICALP.2026.169/LIPIcs.ICALP.2026.169.html . Deciding whether a finite relational structure admits a heap polymorphism (x,y,z) -> xy^{-1}z is NP-complete. This decision result must not be conflated with impossibility of uniformly solving the promised tractable CSP. The paper explicitly says the latter remains open for heaps. Under an abelian-heap promise, affine integer programming supplies a uniform polynomial algorithm without first finding that group operation; it can be used to construct a weaker sufficient Maltsev operation.
- Idziak et al., *Tractability and Learnability Arising from Algebras with Few Subpowers*, SIAM J. Comput. 39(7), 2010. https://www.math.uwaterloo.ca/~rdwillar/documents/Publications/KedgeTractability.pdf . Direct antecedent for combining learnability and algebraically induced tractability.

Conclusion: a claim that the learner discovers a suitable algebra cannot use existence of that algebra as if it were an acquisition algorithm. It may be better to acquire an executable sufficient reduction than to identify the latent generative algebra exactly.

## Constructive fallback: acquire hidden product-chain optimization geometry

Let X = product_i D_i with n >= 2 and finite explicitly labelled domains D_i, |D_i| = q_i >= 2. Unknown total orders on each D_i define a product lattice. Let F:X -> R be a calibration energy promised submodular in that lattice. The learner receives exact value-query access to F, and may set all coordinates of each query; this is stronger access than passive data. Fix an arbitrary baseline z and labelled anchor pair (a_i,b_i) in every coordinate.

Define the mixed difference at the baseline slice:

    Delta_ij(a,b;c,d)
      = F(z[i=a,j=c]) + F(z[i=b,j=d])
        - F(z[i=a,j=d]) - F(z[i=b,j=c]).

For a <_i b and c <_j d, submodularity gives Delta_ij <= 0. Reversing exactly one ordered pair reverses its sign.

Assumption A (exposure): The graph G whose edges have nonzero anchor mixed difference Delta_ij(a_i,b_i;a_j,b_j) is connected. For every such edge {i,j}, the score

    h_ij(x) = F(z[i=x,j=b_j]) - F(z[i=x,j=a_j])

is injective on D_i, and h_ji is injective on D_j. This assumption is a genuine calibration requirement. It is not inferred from a finite successful transcript. Strict submodularity on each relevant two-coordinate slice suffices.

### Theorem

Under Assumption A, the learner acquires all coordinate orders up to simultaneous reversal using O(n^2 + sum_i q_i) exact value queries, O(n^2 + sum_i q_i log q_i) arithmetic/comparison work, and O(n + sum_i q_i) retained representation after the acquisition transcript is discarded. The learner can subsequently apply ordinary submodular minimization to every value-oracle task on X promised to share those orders, including tasks with arbitrary higher-order dense interactions. Acquisition has not recovered F itself.

### Proof

Let s_i=+1 if a_i precedes b_i, otherwise -1. Every observed nonzero anchor edge satisfies sign(Delta_ij)=-s_i s_j. Select a spanning tree of G and fix an arbitrary sign at its root. Propagating s_j=-sign(Delta_ij)s_i determines all signs up to one common flip, by connectedness. Because the true signs satisfy every edge, cycles are consistent.

For each i choose an incident edge {i,j}. If a_j precedes b_j, then for x preceding y in D_i,

    h_ij(y)-h_ij(x)=Delta_ij(x,y;a_j,b_j) <= 0.

Injectivity makes this inequality strict. Thus h_ij is strictly decreasing in the true order; if the anchor order in coordinate j is reversed, it is strictly increasing. Evaluate h_ij once for each label x, using two F queries per label, and sort by its values in the direction fixed by the synchronized orientation of j. This recovers the order of D_i. The arbitrary common sign flip reverses every recovered coordinate order simultaneously. A simultaneous order reversal exchanges meet and join and hence preserves submodularity.

Testing all anchor pairs uses at most 4 binomial(n,2) F queries (caching may reduce this); the score stage uses at most 2 sum_i q_i. Graph construction, tree propagation and scalar sorting establish the stated bounds. The retained object is the ordered list of domain labels for each coordinate.

An arbitrary future task promised submodular on the same product of chains is now an ordinary finite distributive-lattice submodular minimization instance. Its cost is the cost of that established solver on a lattice with sum_i(q_i-1) join-irreducibles, plus the value-oracle evaluation cost. This is a polynomial-time reduction, not a new minimization algorithm.

### Noise and precision

If every mixed difference used for synchronization and every pairwise score gap needed for ordering has magnitude at least gamma, deterministic query error at most eta < gamma/4 preserves mixed-difference signs; score differences involve four scalar values and need the same bound. With independent sigma-sub-Gaussian evaluation noise, averaging O(sigma^2 gamma^{-2} log(Q/delta)) replicates per queried value yields success probability at least 1-delta across Q distinct queried values, up to explicit standard tail constants. Unknown gamma needs sequential confidence intervals and can have unbounded cost when the margin vanishes. Exact minimization under later noisy value queries is a separate problem.

### Failure modes

1. A modular calibration F contains no coupling information; its anchor graph is empty and no relative geometry is learned.
2. Local mixed differences may be zero at the chosen slice and nonzero elsewhere. The proof cannot replace the exposure assumption by global submodularity alone.
3. Finite samples cannot certify that all unseen contexts or future tasks share submodularity. This theorem is conditional on the family promise.
4. Arbitrary extra constraints on future tasks can restore NP-hardness; the promise includes that the feasible restriction is supported by the chosen ordinary submodular solver.
5. The acquisition oracle permits arbitrary setting of coordinates. Passive observations do not provide it automatically.

## Novelty judgment: reject as a major original result

The construction is a useful small oracle bridge, but its core belongs to an established line:

- Nakashima, Yamauchi, Kijima and Yamashita, *Finding Submodularity Hidden in Symmetric Difference*, arXiv:1712.08721v3 (2019), https://arxiv.org/abs/1712.08721 . The binary version has O(n) oracle acquisition under strict submodularity and exponential acquisition in general. This is a very close antecedent, not merely a competitor.
- Green and Cohen, *Domain permutation reduction for constraint satisfaction problems*, Artificial Intelligence 172 (2008), 1094-1118, https://doi.org/10.1016/j.artint.2007.12.001 . Domain permutations revealing a tractable language are established.
- Helaoui, Naanaa and Ayeb, *Domain permutation reduction for Valued CSPs*, Soft 2011. Permuted-submodular binary valued constraints are explicitly studied. Available workshop proceedings: https://cs.fit.edu/~msilaghi/pages/papers/CP2011_SoftWorkshop_Schedule.pdf . The acquired score construction also resembles classical permuted-Monge recognition.
- Cechlarova and Szabo, *On the Monge property of matrices*, Discrete Mathematics 81 (1990), 123-128, https://doi.org/10.1016/0012-365X(90)90143-6 . Recognition of hidden row/column permutations enabling Monge optimization is established.

No advantage over a conventional learner implementing these same acquisition operations has been demonstrated. Do not headline this as a new computational boundary or theory of intelligence.

## Useful further warning about universal-learning fallbacks

Goldreich and Ron's author page, https://www.wisdom.weizmann.ac.il/~oded/p_ul.html , explicitly corrects the published claim of simultaneous time/sample optimality. Their universal learner's proved statement is time optimality up to the relevant description-dependent factor; simultaneous sample optimality is false. Thus universal enumeration cannot be used to erase both acquisition time and information costs.
