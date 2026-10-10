# Strict output positivity survives arbitrary filters strongly enough for finite EB

9 October 2026. Complete proof candidate for a genuinely larger anchor class than positive-definite Choi matrices. This result does not require PPT. It still does not settle arbitrary nonstationary PPT words near non-strictly-positive boundaries. No priority or external-certification claim is made.

## Theorem

Let K be a compact set of completely positive maps M_d -> M_d, every member strictly output-positive:

 Phi(X)>0 for every X>=0, X!=0.

Then there is a finite N(K) such that every word containing N(K) arbitrary factors from K, with arbitrary completely positive maps inserted between them, is EB. No trace preservation, unitality, invertibility of the filters, or PPT assumption is needed.

In particular, a fixed strictly output-positive CP seed has a finite uniform filtered-word EB index even when its Choi matrix is singular.

The proof has two parts. A new-to-this-programme rectangular Kraus-space application upgrades d such seed occurrences to uniformly positive-definite Choi matrices. The already-recorded faithful-word expansion then supplies EB. The latter expansion is not claimed as a new result.

## 1. Rectangular transitivity and saturation

A matrix space S subset M_(b,a) is transitive if Sx=C^b for every nonzero x in C^a. A CP map is strictly output-positive exactly when its Kraus span is transitive.

The primary input is Davidson–Marcoux–Radjavi, Transitive Spaces of Operators, arXiv:0706.2449v1, Theorem 4.9: product spans of k- and l-transitive rectangular spaces are min(k+l, the endpoint dimensions)-transitive. Source: https://arxiv.org/html/0706.2449 . The theorem was inspected directly in the preceding continuation.

A full rectangular matrix space remains full when multiplied on the left by a transitive space:

 span S M_(r,d)=M_(s,d),     S subset M_(s,r) transitive.       (1)

Indeed fix nonzero x in C^r. Every rank-one y z* can be written as A(x z*) with A in S satisfying Ax=y.

Consequently, a chain of d transitive rectangular spaces, with both endpoint dimensions d and every intermediate dimension at most d, has full product span M_d. Before saturation, transitivity increases by at least one at every step. If a smaller intermediate dimension caps that degree, the accumulated product is already a full rectangular space, and (1) preserves fullness thereafter. Otherwise degree d is reached by the last step.

## 2. Arbitrary singular single-Kraus filters

Let Phi_1,...,Phi_d be strictly output-positive CP maps on M_d, with transitive Kraus spans S_1,...,S_d. Let A_1,...,A_(d-1) be arbitrary nonzero matrices; they may be singular.

Factor each A_j=B_j C_j through its rank r_j, where B_j:C^(r_j)->C^d is injective and C_j:C^d->C^(r_j) is surjective. The Kraus span of the filtered word is

 span S_d A_(d-1) S_(d-1) ... A_1 S_1.

This is the product span of the following d rectangular spaces:

 C_1 S_1,
 C_j S_j B_(j-1)                  (2<=j<=d-1),
 S_d B_(d-1).

Every listed space is transitive. An injective input factor takes a nonzero vector to a nonzero vector; S_j then spans all of C^d; a surjective output factor spans its entire target. Section 1 therefore makes the final product span all of M_d.

Thus

 J(Phi_d Ad_(A_(d-1)) Phi_(d-1) ... Ad_(A_1) Phi_1)>0.  (2)

The square maps and filters are interleaved in the displayed order; its Kraus span is the fully written product above.

For d=1 the assertion is immediate.

## 3. Arbitrary CP filters and a uniform Choi margin

Let C_1,...,C_(d-1) be nonzero CP maps. Choose one nonzero Kraus matrix from each C_j. The expansion of the filtered word contains the corresponding positive CP branch from (2), whose Choi matrix is positive definite. The whole Choi matrix is therefore positive definite.

Normalize every filter by tr J(C_j)=1; positive scalar factors do not affect EB. This normalized set of CP maps is compact and contains no zero map. The seeds range over compact K. The family

 V=Phi_d C_(d-1) Phi_(d-1) ... C_1 Phi_1

is consequently compact, and every member has J(V)>0. There are common finite constants eta,beta with

 0<eta<=beta,
 eta D<=_CP V<=_CP beta D,       D(X)=tr(X)I.             (3)

No lower bound on a filter's rank or smallest nonzero singular value is required. Rank-one filters are harmless; in that case the surrounding transitive seed spaces already produce a full product Kraus span.

If any filter in the original word is zero, the word is zero and hence EB, so excluding it during normalization loses nothing.

## 4. Faithful chunks with arbitrary CP maps between them

Take t chunks V_1,...,V_t satisfying (3), with arbitrary CP maps C_j between chunks. Put

 T=V_t C_(t-1) V_(t-1) ... C_1 V_1,
 R_j=V_j-eta D,
 z=1-eta/beta.

The remainder obtained by choosing every R_j satisfies

 R_t C_(t-1) ... C_1 R_1 <=_CP z^t T.

All other positive expansion terms contain D and are EB. Let H denote the middle CP composition in T=V_t H V_1, and w=tr H(I). Grouping the expansion terms with eta D at the left endpoint gives an EB part F satisfying

 F>=_EB eta^2 w D,
 T<=_CP beta^2 w D.

The remaining CP remainder has Frobenius Choi norm at most z^t beta^2 w d^2. The separable ball of radius 1/d^2 around I tensor I proves T EB whenever

 z^t beta^2 d^4 <= eta^2.                               (4)

Choose finite t>=2 satisfying (4). The cases eta=beta or w=0 are immediate. This is exactly the existing faithful-word argument, allowing independently varying chunks and arbitrary CP maps between them.

## 5. Counting seed occurrences

Divide any word of d t seed occurrences into t consecutive groups of d occurrences. Normalize only the filters internal to each group, pulling out their positive scalar factors. The groups satisfy (3); the filters between groups remain arbitrary CP maps. Section 4 gives EB.

Therefore one may take N(K)=d t. All later words are EB because additional CP pre- or postcomposition preserves EB.

## Scope and relation to the unrestricted gate

- Positive-definite Choi matrices are not assumed. Strict positivity on ordinary positive inputs is enough, through transitive Kraus spaces.
- This settles the filtered-seed question for Choi-singular seeds that are strictly output-positive. It also supplies uniform arbitrary-filter anchors for compact strictly-positive families.
- A PPT seed may fail strict output positivity even with faithful input and output marginals. Such seeds are outside this theorem.
- A family approaching the non-strict boundary need not retain the uniform eta in (3); no dimension-only EB bound for all PPT words follows by merely taking a limit of the constants.
- Every product here is serial composition, not a tensor power.

## Strong-anchor corollary for unrestricted PPT words

For fixed d and epsilon>0, let K_epsilon be the compact set of CPTP maps satisfying Phi(rho)>=epsilon I for every density matrix rho. The theorem supplies a finite H(d,epsilon) such that any CP word containing H(d,epsilon) factors from K_epsilon is EB, with arbitrary CP maps between them. In particular the anchors may be different PPT maps; neither the intervening maps nor their grouped products need be bistochastic.

This closes the many-strong-anchor branch of the unrestricted nonstationary problem. It does not close the branch where all tagged strict-positivity margins become arbitrarily small.

## Bounded numerical check

verify_filtered_transitive_bridge.py and filtered_transitive_bridge_verification.json contain 24 d=4 tests based on the published transitive space in DMR Example 2.2. They include different unitarily transformed seeds, ranks 1 through 4 for the filters, and nonzero singular values as small as 10^(-9). Every four-seed word had full Choi rank; the smallest observed lambda_min/lambda_max was about 0.02018. These seeds need not be PPT, consistent with the theorem's scope. The computation checks examples and is not the universal proof.
