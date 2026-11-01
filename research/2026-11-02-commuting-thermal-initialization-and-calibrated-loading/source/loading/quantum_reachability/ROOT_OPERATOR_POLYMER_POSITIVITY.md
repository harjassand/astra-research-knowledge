# Root candidate: operator-polymer positivity of a quantum inverse-noise state

1 November2026. New proposed supporting mechanism. NOT an efficient preparation algorithm, not a completed loader. Independent review required.

## A. Finite matrix-gas zero-free lemma
Let finitely many polymer operators A_gamma be Hermitian, with [A_gamma,A_eta]=0 whenever gamma and eta are compatible. Define the matrix gas
 Z(S)=sum_{compatible Gamma subset S} product_{gamma in Gamma} A_gamma,
including identity for empty Gamma. Suppose positive mu_gamma satisfy
 ||A_gamma|| product_{eta in N[gamma]}(1+mu_eta) <= mu_gamma,
where N[gamma] is the closed incompatibility neighborhood (including self).

Claim: every Z(S) is invertible and
 ||Z(S)^(-1) Z(S\{gamma})|| <=1+mu_gamma.
Proof by induction on |S|. Write B=S\{gamma}, C=B\N(gamma). The exact deletion identity is Z(S)=Z(B)+A_gamma Z(C). Compatibility gives [A_gamma,Z(C)]=0. Thus
 Z(S)=Z(B)[I+Z(B)^(-1)Z(C)A_gamma].
Deleting the neighbors of gamma successively telescopes Z(B)^(-1)Z(C) into ordered products of smaller inverse-deletion ratios. Its norm is at most product_{eta in B∩N(gamma)}(1+mu_eta). The displayed closed-neighborhood condition bounds the perturbation in brackets by mu_gamma/(1+mu_gamma)<1. Neumann inversion proves the claim. No commutation among incompatible operators is needed.

Scale all A_gamma by a common real t∈[0,1]. The same bound applies, every Z_t(S) is Hermitian and invertible, and Z_0(S)=I. Eigenvalues cannot cross zero, so Z_1(S)>0. The argument is finite-dimensional and uniform in total volume once rooted activity bounds establish the local condition.

## B. Application candidate: weakly noncommuting Gibbs state plus independent Pauli noise
Let H_ref be a sum of commuting bounded finite-range terms (the actual code H0 plus bounded onsite bath terms). Let V=sum_a V_a be bounded-degree weak local Hermitian perturbations. Fix finite beta and finitely many bounded-support physical Pauli conjugations P_i(.)P_i, with bounded patch overlap. The actual target is the FULL joint Gibbs operator G=exp[-beta(H_ref+V)], including the bath. Independent noise acts only on the accessible chosen memory spins.

The relative operator U=exp(beta H_ref/2) G exp(beta H_ref/2) has a Duhamel connected-component expansion. Since H_ref terms commute, imaginary-time conjugation of each V_a enlarges its support only by reference terms touching its original support, with norm amplification bounded independently of volume. Grouping all words with a fixed distinct perturbation-label set gives an operator activity for each connected component. Disjoint components commute/factor, each component is Hermitian by time reversal/dagger symmetry of the centered expansion, and norm is bounded by a^{|gamma|}, with a=exp(beta epsilon exp(c beta))-1.

This exact identification, especially individual Hermiticity and component factorization, must be checked against the actual centered-Duhamel expression; it is not inferred solely from positivity of U.

For Pauli noise factor C_i=(1-q_i)id+q_i Ad(P_i), q_i<1/2, set r_i=q_i/(1-q_i). Omitting the positive global prefactor, the inverse-noise relative operator is
 K=sum_{F subset labels} (-1)^|F| product_{i in F}r_i B_F U B_F†,
 B_F=exp(beta H_ref/2) P_F exp(-beta H_ref/2).
For an individual label B_i is supported on its bounded enlarged reference patch and ||B_i||²<=exp(beta B), with B a local energy-change bound. Products satisfy B_F=product_i B_i up to irrelevant Pauli phase. Their conjugation superoperators commute, as the original Pauli conjugations do.

Build a joint graph of perturbation labels a and noise labels i, joining overlapping enlarged patches. For each fixed connected union of selected V labels and selected noise labels, first decompose its V-only subgraph into connected components, multiply their mutually commuting Duhamel activities, then conjugate by the selected B_i and multiply the real signed noise coefficient. This is proposed to be the joint operator activity. It is Hermitian, supported on the joint patch, and bounded by
 a^(number V labels) [max_i r_i exp(beta B)]^(number noise labels).
Disconnected joint components commute and factor; therefore K is precisely a Hermitian matrix polymer gas on the joint graph.

If this component identification is correct, bounded-degree rooted counting and Part A give K>0 for sufficiently small fixed epsilon and q, uniformly in total memory/bath volume. Hence C^(-1)(rho_actual) is a POSITIVE normalized quantum state, not merely a signed formal operator. Trace preservation of C^(-1) gives normalization automatically. The temperature/noise constraint is charged; no uniform beta→infinity tolerance follows.

## C. Crucial missing operation
Even if positivity passes, it does not prepare the preimage or the actual joint Gibbs state. An exponential-cost nonunitary filter, access to inaccessible bath spins, or a target-dependent Gibbs oracle would not close the physical-loading obstacle. Efficient preparation and logical-input preservation under the subsequent noise are separate required constructions. Generic inverse noise does not automatically commute with logical overwrite; quantum coherences remove the simple classical-prefix syndrome argument unless its exact replacement is earned.

This candidate is meant to test whether positivity itself is an essential obstruction in the actual near-commuting quantum region. It must not be presented as an operational memory advantage or as a novel general cluster-expansion method.
