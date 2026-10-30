# Graph-transfer scope and primary comparison

30 October 2026. Structural calculation for the proposed global class, with BOTH seed channels positive as required by PARAMETRIC_TRANSFER_GLOBAL_SCOPE_CORRECTION.

There are k residual types including a, plus D and physical B: k+2 species. The fast complexes are the k complexes X_i+D, plus 2a and 2D, all translated by the common a0 A+qB seed; the two additional connector complexes are 0 and A+B. Thus there are k+4 complexes and one linkage class. Fast conversions span dimension k-1, and a+D->2a adds one independent direction, giving fast rank k on the N-conserving hyperplane. The connector vectors project onto (N,B) as (1,1) and (m-1,q-1); their determinant is q-m>0. Total rank is k+2 and deficiency is one.

This is therefore a structured deficiency-one acquisition class, not arbitrary growing-deficiency networks. That limitation matters when describing its scope.

Complex balance is not automatic. Let k1 be 2a->a+D, k5 be 2a->2D, k6 be 2D->a+D, and k2 be a+D->2a. At every non-a type+D complex, complex balance forces the corresponding conversion balance; summing the conversion flows then forces the a+D conversion part to balance too. The 2D and a+D balance equations consequently require respectively

    d/a=sqrt(k5/k6),     d/a=(k1+k5)/k2.

These are incompatible for generic rates (all four rates equal to one give 1 versus 2). This excludes the direct complex-balanced product-Poisson route at those rates; it does NOT exclude other conventional recurrence theorems or decompositions.

Primary check: the official abstract of [Anderson–Cappelletti–Kim, *Stochastically modeled weakly reversible reaction networks with a single linkage class*](https://arxiv.org/abs/1904.08967) explicitly gives binary systems and a pure multiple-of-each-species complex as additional assumptions, and uses an n-step embedded-chain technique. The full physical connector graph here is not binary and lacks pure complexes for the hidden types. This headline theorem therefore does not directly certify the proposed class. This is not an exhaustive literature or novelty conclusion.

A fresh attempt to open the primary decomposition article at https://pmc.ncbi.nlm.nih.gov/articles/PMC8187217/ returned a browser CAPTCHA. Its full theorem was not inspected in that attempt and is not used as evidence for or against closure. No CAPTCHA bypass, denied Wisconsin PDF retry, upload, or outreach was performed. The earlier project 'in preparation' claim and planar/bimolecular preprint comparisons remain subject to their recorded scope limitations.
