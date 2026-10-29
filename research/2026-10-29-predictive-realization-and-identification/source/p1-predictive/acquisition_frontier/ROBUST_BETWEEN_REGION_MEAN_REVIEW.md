# Scoped proof and independent review: between-region uncertainty

29 October 2026. This verifies the root's new rowwise uncertainty certificate and the frozen between-region and positive-realization consumers. It does not re-audit the native acquisition confidence event or the universal realization theorem, which have separate completed reviews. No observations are redrawn and no producer implementation is imported.

## 1. The quadratic comparison does not transfer to bilinear means

After regional elimination the mean is T=(c_C+a^T h)/mu_C, Kh=b, with c_C>=0, a>=0, b>=0, mu_C>0. Generally a differs from the full live-region load b. Loewner order alone does not give coordinatewise or bilinear order for K^-1b.

Exact counterexample: two live states have ground conductance 1 each and live edge c in [1,2]. Set b=(1,2). Then

    K(c)=[[1+c,-c],[-c,1+c]],
    h(c)=((1+3c)/(1+2c),(2+3c)/(1+2c)).

Although K(1)<=K(c)<=K(2) in quadratic-form order, h_0 rises from 4/3 to 7/5. Choosing a=(1,0) disproves using the larger-edge inverse as a lower bound on this mean. It is already a reversible three-state conductance model without hidden states.

## 2. The proposed exact row certificate is sound

Write (Kx)_i=g_i x_i+sum_j c_ij(x_i-x_j), with acquired nonnegative intervals gL<=g<=gU and cL<=c<=cU. For x>=0 the exact minimum row is

    Fmin_i(x)=gL_i x_i
      +sum_j [cL_ij(x_i-x_j) if x_i>=x_j,
              cU_ij(x_i-x_j) otherwise].

The maximum row Fmax uses gU and the opposite edge endpoints. Every compatible true K obeys Fmin(x)<=Kx<=Fmax(x). If nonnegative candidate vectors u,l satisfy

    Fmin(u)>=bU,     Fmax(l)<=bL,                 (1)

then Ku>=b and Kl<=b. The true grounded K is a nonsingular M-matrix, whose inverse is entrywise nonnegative. Therefore l<=K^-1b<=u.

Opposite rows may select different values for the same undirected edge. They form a rectangular row relaxation, which need not be reversible or jointly attainable. This does not invalidate (1): the inequalities are verified against every true row separately. It can widen the result. In the example above, the rectangular bounds are l=(5/4,3/2), u=(3/2,7/4), whereas the symmetric-edge family has h_0 in [4/3,7/5], h_1 in [8/5,5/3].

Policy iteration only proposes l,u. Their exact signs and row inequalities are sufficient for release; apparent floating convergence is not. A sufficient existence condition is that the strictly positive lower-edge graph connects each live state to a positive lower ground rate. Uniformizing all policies at a common upper rate yields a uniform positive chance of absorption along fixed lower-positive paths within at most n steps. Thus all row policies are proper with bounded expected reward, and conventional Bellman equations have finite solutions. If the rectangular relaxation includes a nonabsorbing policy, the certificate can fail despite every compatible symmetric source being proper. Such failure concerns this relaxation, not necessarily missing information.

## 3. Shared positive mass sharpens the ratio

For a source union C, the root uses a=b_C and mu_C=sum_i a_i. After bounding h by l,u and c_C by cL,cU, a stronger ordinary calculation optimizes

    f(a)=(c+sum_i a_i h_i)/sum_i a_i

over a positive box aL<=a<=aU, retaining the same a in numerator and denominator. For fixed other coordinates, the derivative has the sign of h_i-f(a); hence an optimum exists at a box vertex. At a minimizing vertex, upper weights can occur for lower h values and lower weights for higher h values. Otherwise the derivative signs contradict optimality, except at irrelevant ties. Thus sorting h increasingly, starting with all lower weights, and successively switching a prefix to upper weights visits a minimizing vertex. Descending order similarly visits a maximizing vertex. Checking m+1 prefixes costs O(m log m), rather than enumerating 2^m vertices.

This statement holds for any fixed c and positive denominators; here c>=0 and h>=0 come from the physical problem. Using cL for the minimum and cU for the maximum is justified by monotonicity in c. All correlations with K, b and the original acquisition remain inside the common confidence event; the outer optimization is conservative. When C is the entire surviving region union, intersecting the earlier independently valid quadratic interval is sound.

## 4. Actual independent checks

`review_between_region_record.py` reads only the frozen public certificates for its consumer reconstruction. It imports neither producer nor consumer. It checks:

- all six target-vector pairs, all 36 exact row inequalities and the positive lower-graph grounding;
- every fractional-box vertex for each of the 12 ordered disjoint nonempty source/target unions (168 vertex evaluations in total), then exact equality with the sorted-threshold outputs after the documented quadratic intersections;
- the exact outward maximum factor bound 1.557794 and inherited confidence event 3/5000;
- all 12 true means by an independent rational reconstruction and full killed solve of the private 18-state conductance geometry, performed after deterministic consumer checks;
- the public 12-state representative's generator signs, zero row sums, weighted detailed balance, coefficient selection, full block Schur record, regional residence terms and all 12 prepared means;
- exact containment of both the private original means and prepared representative means in the released intervals, and the reported numerator/denominator bit counts.

The full block check solves the leaf/interior block directly rather than trusting the producer's specialized reconstruction assertions. The private original geometry is used only for diagnostic validation; it does not enter the released consumer or representative. The scope is the two frozen executions and their new algebraic uses, not external proof review or physical experimentation.

## 5. Strong conventional sources

Krak, *Hitting Times for Continuous-Time Imprecise-Markov Chains*, UAI/PMLR 180 (2022), https://proceedings.mlr.press/v180/krak22a/krak22a.pdf , develops lower/upper hitting-time equations for uncertain rates. Section 3.3 requires compact convex row-separable sets and lower reachability, relevant to interpreting the present relaxation.

Sangalli and Krak, *Lower and Upper Expected Hitting Times for Weighted Imprecise Markov Chains*, arXiv:2603.16665v1 (17 March 2026), https://arxiv.org/html/2603.16665v1 , extends the framework to positive weights and adapts existing fixed-point algorithms. Section 4 explicitly requires separately specified rows. This current primary preprint is an antecedent/comparator, not claimed accepted external review.

The robust M-matrix/Bellman consumer and sorted linear-fractional optimization are conventional tools. The larger programme's addition is the acquired, reusable physical information representation to which those tools are applied.
