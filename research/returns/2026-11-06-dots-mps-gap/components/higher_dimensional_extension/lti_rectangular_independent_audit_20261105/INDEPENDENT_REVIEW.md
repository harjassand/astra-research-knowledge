# Independent adversarial review: rectangular strict-product LTI completeness

2026-11-05. Internal mathematical review, not external/formal verification or a novelty determination.

## Verdict and exact scope

I found no remaining algebraic gap in the revised `lti_2d_product_extension_20261105/PROOF_CANDIDATE.md` with SHA256

    a2a3e72ab2b0a35fe72281ffdfee6711c1f270592e64792ffb87ff469f7d036f.

The reviewed claim is for a fixed spatial dimension p, one translate per lattice site of a positive interaction on the **full cube** K=[0,R-1]^p, and the strict local product bound cQ_K<=h<=MQ_K. The hierarchy uses the centered window Lambda_L=(A_L-A_L)+K, full opposite-face marginal equalities, energy normalization Tr rho h_0=1, and the half-sum of all nonzero displacement anticommutators. It is not a statement about an unspecified 2D SDP implementation or generic PEPS.

Within this scope the O(1/L) surface/volume comparison checks. The proof's direct bound on positive far-pair moments is essential; a generic norm/triangle bound would not give this rate in arbitrary dimension.

The revised one-site-translation-covariant finite-depth-circuit extension also checks for its explicitly enlarged target window and unchanged displacement set. Fixed-period blocking has been excluded and is not part of this verdict.

## 1. Domain and normalization audit

The window is genuinely centered: each h_0 and h_z for z in D_L fits, including displacements with mixed signs. If x,y lie in A_L, translating the pair (h_x,h_y) to (h_0,h_(y-x)) stays in the rectangle along a coordinate-by-coordinate path. Full opposite-face marginal equality therefore supplies every needed pair moment. One-site marginal invariance alone would not suffice.

The two signs satisfy b_z=b_(-z) by translating and using the symmetry of the anticommutator. In the torus sum of q_L, each retained unordered pair occurs twice before the factor 1/2 and once afterwards. At sufficiently large torus size there are no wrap aliases. Because L>=R, every overlapping pair is retained. All omitted pairs have disjoint physical supports and their anticommutators are positive.

The revised proof obtains gamma_L<=Delta_N directly: translation-average a first excited torus state, restrict to the window, and divide by its local energy Delta_N/N^p. Its normalized objective is at most Delta_N. This avoids any reliance on unproved primal attainment when obtaining the uniform near-optimal objective bound.

The normalized identity is strictly positive and satisfies all full-LTI equalities. The core second-moment bound supplies v>=-C_0/L, so the minimum SDP is feasible, finite, and strictly feasible in its PSD cone. Standard finite-dimensional Slater duality then gives the equal, attained local-coboundary maximization value. Redundant face equalities do not invalidate strict cone feasibility. The face-equality multipliers are precisely finite-support translation differences, so their periodic sums vanish. No trace compactness or dual optimizer was assumed.

## 2. Core moments and the objective budget

For every feasible rho,

    a=Tr rho h_0^2<=M,
    b_z>=-2M,
    b_z>=0 for ||z||_infinity>=R.

The last assertion uses disjoint support, not positivity of products of arbitrary positive matrices. There are only J=((2R-1)^p-1)/2 potentially negative displacement classes. Hence

    B(v):=sum_(disjoint classes) b_z <=v+2MJ.

Near minimizers have bounded v because gamma_L<=R^p M. This bounds the entire positive far-pair budget. It is the step that prevents surface-squared moments from invalidating the rate.

For the anchor cube A_L, the exact number of unordered pairs at displacement class z is product_j(L-|z_j|). The coefficient deficit for the finitely many overlap classes is at most p(R-1)L^(p-1). Subtracting the exact expansion from L^p v therefore gives the stated core second-moment bound. No operator inequality H_core^2<=H_total^2 is used.

## 3. Boundary covering, pair counting, and noncommutativity

For a full cubical support, clamping the crossing anchor y into A_L produces an anchor a(y) such that

    (K+y) intersect U is contained in K+a(y).

Vacuum compression then gives B_y<=MQ_T<=(M/c)h_(a(y)). This is the point where the full-cube assumption matters. Arbitrary sparse supports can leave a physical core corner uncovered; the draft correctly excludes that extension rather than silently asserting the same cover.

For the core/boundary cross term, ||x-a(y)||_infinity>=R makes h_x disjoint from both B_y and its dominating h_(a(y)). Positivity can safely be multiplied on these disjoint tensor factors. A fixed displacement class contributes at most two x values per crossing y, giving the 2s multiplicity. Nearby noncommuting pairs are handled by

    {A,B}<=A^2+B^2<=M(A+B),

before any unsafe product domination. Their number is at most s(2R-1)^p.

For boundary/boundary products, separation of the **assigned** anchors by at least 3R implies separation of the original anchors by at least R+2, because clamping moves each coordinate by at most R-1. Thus the original interactions are disjoint as required. Compression factors only in this far class. Assigned interior supports are also disjoint, so B_y B_z<=kappa^2 h_(a(y))h_(a(z)) is a legitimate tensor-factor inequality.

The preimage multiplicity bound P=(2R-1)^p is conservative. It gives at most 2Ps unordered boundary pairs per displacement class. The near-pair bound T=P(6R-1)^p is likewise conservative; including diagonals or counting ordered pairs only enlarges the stated estimates. I found no missing factor that changes their constants or scaling.

The collar N>=L+3R is sufficient to embed the entire touched coordinate box injectively. Opposite-face boundary interactions do not unexpectedly overlap across the periodic seam.

Finally, dropping H_out in the second moment is justified through H_out nu^(1/2)=0 and ||H_N nu^(1/2)||_HS^2. It does not require H_out to annihilate H_A nu^(1/2), which generally would be false.

## 4. A genuine counterexample to an invalid shortcut, not to this proof

I explicitly tested the tempting identity

    vacuum_compression(h_y h_z) = B_y B_z

for nearby crossing interactions. It fails on the supplied generic complex 2x2 interaction. On a normalized one-particle core state at L=2, a boundary pair has compression-factorization discrepancy about 0.0033857329273892.

Thus a proof that applied this identity indiscriminately would be wrong. The reviewed draft deliberately classifies these pairs as near and bounds their original anticommutator before compression, so this counterexample does not apply to its argument.

## 5. Completion, GNS, and finite-depth transport

The cross and seam-square estimates are O(s)[B(v)+constant], with s=O(L^(p-1)). The denominator is at least L^p. Taking a near-minimizing sequence with uniformly bounded v therefore yields the claimed O(1/L) comparison for every sufficiently large N, without normalizing away a potentially large trace.

Restriction of larger-window feasible states preserves full LTI. New displacement-shell terms are disjoint for the allowed levels, so gamma_L is monotone. The all-large-N comparison and certified periodic upper bound squeeze the periodic limit without assuming it exists first.

For the product GNS representation, vacuum padding embeds every finite positive rho_U as a finite-rank, trace-class finite-excitation operator. Every range vector and its image under H have finite support, so the H and H^2 moments used in the argument are well defined. The commuting block vacuum-complement lower bound yields a unique vacuum and a strictly positive GNS gap on the dense local domain. The standard local form-core variational principle supplies the reverse comparison. One can justify the core directly: each nested local commutator adds only a bounded number of sites along an interaction sequence, giving the usual factorial analytic-vector bound for finite-range bounded interactions in any fixed spatial dimension. No higher-dimensional MPS transfer assumption is involved.

For the circuit extension, alpha maps the full source algebra on Lambda_L into the target algebra on Lambda'_L. Pulling a positive target functional back through this unital *-homomorphism gives a positive source functional. Translation covariance preserves every source LTI equality; energy and objective are identical because q'_L=alpha(q_L). Thus gamma'_L>=gamma_L. Taking L>=R+2w includes every possible overlapping target displacement, ensuring target soundness. This exact fixed-displacement/window construction avoids an unproved level-shift rule.

GNS equivalence here is the canonical unitary between the ground-state representations related by alpha. It need not mean a single infinite product of gates is an operator in the original vacuum representation. The stated compatible periodic circuit realizations provide the finite-torus spectral equivalence separately.

## 6. Independent finite checks

`check_geometry_and_moments.py` imports no constructor code. It reads only the explicitly supplied interaction matrix, SHA256

    b0742f1398d77b94f502e1e2c6313b5e9aa061e7d6fed5123c9af99fbd05b1bc.

It independently verifies:

- clamping covers, multiplicities, core pair coefficients, far original-support separation, near-pair counts and boundary counts in five cases through p=3, including 33,457 far unordered boundary pairs in the p=3 test;
- full-LTI two-particle Dicke marginals at L=2,3,4, with exact partial-trace hypergeometric weights and complete enumeration of every output of the local h;
- the core, cross and seam-square inequalities, including nonzero total disjoint moment budgets 3.20958 and 4.36277 in the L=3,4 cases;
- a nearby compression-factorization counterexample described above.

The Dicke states are permutation-invariant and hence satisfy the full rectangular LTI condition, not merely one-site invariance. Their reduced core states include the vacuum and all permitted particle sectors. No output excitation truncation is made, despite sparse storage. These states are not asserted to be SDP minimizers. For some tests their objective exceeds the near-optimal cutoff, so the tests correctly use the actual B(v) in inequalities (5) and (7), not the near-minimizer-only uniform B_*.

Results are in `results.json`. Floating tests corroborate the exact proof; they do not establish a universal theorem, certified optimum, or priority.

## 7. Remaining boundaries

- No result is established here for arbitrary sparse supports with the same boundary map, general injective PEPS, intrinsic topological order, or arbitrary fixed-period circuits after blocking.
- The finite-depth class is an explicitly trivial-circuit phase, even when its ground state is entangled and its translated interactions do not commute.
- Positive gap existence is elementary for the strict local product assumption. The possible contribution is exact-value completeness of the precisely defined hierarchy, not discovery of a new gapped phase or a new best numerical gap.
- The Hilbert-space/SDP size is exponential in the number of sites in the enlarged window. No efficient algorithm or practical performance advantage follows from this audit.
- This is internal independent reasoning and testing, not formalization, peer review, or proof of novelty.
