# Independent scoped review: weighted incidence for mixed signed box norms
2026-10-30. Reviewer: `challenge_live_busy_energy`.

**PASS**, with the explicit Q<=1 hypothesis, for `WEIGHTED_INCIDENT_PARTITION_ADDENDUM.md`, SHA-256 `76c217f5ebc3611670abda4a852db92716b10006c5742c819b9351cc95ba9e8a` (copied alongside this receipt).

This extends only the norm-locality part of the already reviewed CP-cavity/mixed-box theorem, SHA `33a89f263fc79d87309f9649886fe9091db25e1353e315708469d91ace8d21ea`. The prior conditional receipt SHA `7161a260a9eba75a1af661e85e2c50ebd939d9a3c05610e35235d4a67f449e4c` is unchanged. The nominal onsite-only dissipator, valid service witness, complete physical cut, retained-bath regularity, compatible counter instrument and weighted CP contraction premises are retained. No asynchronous semantic correctness claim is added.

## 1. What changes
Noise supports may now join arbitrary distant sites, with fixed body size q and the SAME per-site incident joint-cb norm budget. The fixed nominal witness patches still have volume at most v and bounded incidence kappa: each physical site belongs to at most kappa simultaneous patches. Therefore any noise support meets at most K=q kappa simultaneous patches, independent of how many other terms or distant partners exist.

The unweighted overlap degree D can be arbitrarily large and is no longer used. Nominal finite-range hardware and its buffered witness packing number P remain fixed; this is not a global-total-budget replacement for the per-site hypothesis.

## 2. Weighted derivative bounds and exact row-sum estimate
For each nonempty restoration-label set A, the unchanged mixed-Duhamel proof bounds its derivative insertion by

    nu_A=2^{|A|} integral sum_{Z meeting every A patch}||N_Z(u)||_cb du.

All A windows must be active at u. This uniform bound is independent of the restoration parameters and of which other patches are kept cut. It vanishes for |A|>K. Additional cavity projections have norm at most one and shrink physical support, so they cannot invalidate the bound.

Fix a label i. At a particular time, a support Z touching k<=K active patches and touching i contributes the factor

    sum_{A subset touched(Z), i in A}2^{|A|}=2*3^{k-1}.

Tonelli is legitimate for these nonnegative norms. The per-site budget on S_i then gives

    sum_{A containing i}nu_A
      <=2*3^{K-1} integral_(window i)sum_{Z meeting S_i}||N_Z||_cb
      <=Q=2*3^{K-1}v eta T.                       (1)

No fixed partner graph, degree or independence assumption enters (1). For finite lattices the incident norm budget also gives the absolute convergence required for arbitrary decompositions.

## 3. Partition induction and its essential smallness condition
For finite restoration set R define

    W(R)=sum_(partitions pi of R) product_(A in pi)nu_A,
    W(empty)=1.

Choose i in R and its unique block in a partition. The exact recurrence is

    W(R)=sum_{A subset R, i in A}nu_A W(R\A).

For 0<Q<=1 set x=Q^{1/K}<=1. Induction, |A|<=K, and (1) give

    W(R)<=x^{|R|}sum_{A containing i}nu_A x^{-|A|}
         <=x^{|R|}Q x^{-K}=x^{|R|}.

For Q=0, every nonempty nu_A vanishes and the conclusion follows directly. The Q<=1 condition is load-bearing: for K=2, two singleton weights both equal to Q=2 give W=4, whereas Q^{2/K}=2. The induction cannot be used unchanged above one.

The original ordered derivative integrals are bounded by W(R): set partitions record the generator-derivative blocks, and their time orderings partition the associated time cube. There is no missing factorial. The cavity factor E_S still makes every derivative act outside all retained service witnesses, so the original factor p^{|S|} survives with no extra conversion per insertion. Hence

    ||D_R H_S||_diamond<=p^{|S|}Q^{|R|/K}.

The already proved Boolean identity now gives

    ||B_F||_diamond<=[p+Q^{1/K}]^{|F|}.             (2)

Choose hardware/witnesses first, fixed T long enough for p, and eta afterward so Q<=1 and (2)'s strength is below the desired fixed bound. No threshold constants are claimed practical.

## 4. Diagnostic and scope
`check_weighted_partitions.py` exhaustively evaluates all subset recurrences for four dense finite hypergraphs (up to 10 labels and 385 derivative hyperedges), including Q=1. Every weighted bound passes. Its explicit Q>1 counterexample confirms the stated restriction. This is a combinatorial diagnostic, not a service or threshold simulation.

This addendum removes the NOISE interaction-degree assumption only. It does not remove witness-patch incidence, nominal packing, the true instrument condition or the service-witness contract. It establishes topology-free bounded-body signed-box norm locality under the per-site joint norm budget; good-box semantic QCA correctness and generic-payload hardware service remain separate modules.
