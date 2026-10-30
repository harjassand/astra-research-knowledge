# Weighted incidence replaces the unweighted noise-overlap degree
2026-10-30. Addendum to frozen CP_NOISE_CAVITY_AND_MIXED_BAD_BOX_V1.md (33a89f263fc79d87309f9649886fe9091db25e1353e315708469d91ace8d21ea). Candidate; independent review pending.

The V1 proof uses a bounded degree D only to count the partitions of restoration labels into generator-derivative blocks. A weighted induction removes that assumption. Keep local nominal hardware and its witness packing, but allow topology-free bounded-body perturbation supports with the same per-site incident norm budget.

Let K bound the number of simultaneous witness patches a physical perturbation support can meet. This follows from bounded support cardinality q and bounded patch incidence per physical site; the sites in Z need not be geometrically adjacent. For each nonempty derivative-label set A define the uniform integrated bound

    nu_A = 2^|A| integral sum_(Z meets every patch in A) ||N_Z(u)||_cb du,

where A's windows must all be active at u. This vanishes for |A|>K. For every fixed label i, swapping the sums gives

    sum_(A contains i) nu_A
      <= 2 * 3^(K-1) integral_(window i)
                    sum_(Z meets S_i)||N_Z(u)||_cb du
      <= Q := 2 * 3^(K-1) v eta T.                       (1)

The combinatorial factor is exact as an upper bound: for a support meeting k<=K patches, sum_(A subset those patches, i in A)2^|A|=2*3^(k-1).

Let

    W(R)=sum_(pi a partition of R) product_(A in pi) nu_A,
    W(empty)=1.

For Q<=1 set x=Q^(1/K). Induct on |R|, choosing one i in R and its partition block A:

    W(R)=sum_(A subset R, i in A) nu_A W(R\A)
        <= x^|R| sum_(A contains i)nu_A x^(-|A|)
        <= x^|R| Q x^(-K)
        = x^|R|.                                        (2)

The Q=0 case follows directly. The ordered mixed-Duhamel integrals are bounded by exactly this partition sum, while the unchanged service witness argument retains p^|S|. Therefore V1's conclusion sharpens to

    ||B_F||_diamond <= [p + Q^(1/K)]^|F|.                 (3)

This bound has no unweighted noise-interaction-degree requirement. All physical support changes in a cavity still shrink Z, and the reset/hardware premise remains ONSITE dissipators. It does not broaden the separate unfinished asynchronous-QCA correctness theorem, prove a stronger preparation/output interface, or make this norm candidate independently accepted.
