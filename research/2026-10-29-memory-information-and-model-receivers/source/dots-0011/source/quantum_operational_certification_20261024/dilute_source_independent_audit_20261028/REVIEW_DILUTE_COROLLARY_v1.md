# Independent review: dilute-source inner distillation corollary

2026-10-28. Reviewer: construct_noisy_code_boundaries. Governing candidate: `../fixed_defect_schur_orbit_decoder_20261028/DILUTE_SOURCE_COROLLARY_v1.md`. This reviews the new rate/dimension/probability bridge, relying on separately received orbit access and weighted soft-polar moment results. It is not an independent hardware or historical-priority claim.

## Entropy, probability and dimension

Partial trace contracts trace distance, so the marginal distance to the promised pure component is at most delta. The finite-dimensional entropy-continuity function f_b gives the first entropy loss. On the Schur typical event the spectral total variation is at most u/2, giving the second loss. For sufficiently large k both arguments lie in the required monotonicity range; the written c/k<=1/2 and u<=1 already suffice for b>=2.

At sorted nonnegative spectrum p, every Schur monomial weight is majorized by the highest weight mu. Its value is at most p^mu, with zero entries handled by continuity. The number of monomials with multiplicity equals the Weyl dimension, at most (k+1)^{b(b-1)/2}. The Specht dimension upper bound is 2^{kH(mu/k)}. Thus the stated Schur probability bound follows with relative entropy in natural units. There are at most (k+1)^{b-1} diagrams, and natural-log Pinsker is D(q||p)>=||q-p||_1^2/2. Their sum gives exactly b0=(b-1)(b+2)/2 and epsilon/6 with the supplied u_k.

For an explicit lower-bound proof, append zeros so mu has b parts. The hook formula gives

 d_mu = k! prod_{i<j}(mu_i-mu_j+j-i) / prod_i(mu_i+b-i)!.

Discarding its positive integer numerator factors and bounding the extra factorial factors yields d_mu >= multinomial(k;mu)/(k+b)^{b(b-1)/2}. Sequential binomial factorization, together with binomial(n,t)>=2^{n h2(t/n)}/(n+1), gives multinomial>=2^{kH(mu/k)}/(k+1)^{b-1}. Combining proves the stated hook lower bound. The two entropy losses and logarithmic overhead are o(k), whereas kDelta is linear, so a finite uniform k threshold exists.

An independent exact-integer hook executable checks 9,343 partitions across b=2,...,5 and k=1,...,30. It also finds an illustrative valid parameter point b=2,c=1,R=.25,Delta=.25,epsilon=.1,j=4,k=8356. This is not practical: log2(alpha0) is about104.23.

## Environmental cutoff and Alice code fit

The received binomial domination applies to an eigenbasis expansion of the iid state, not a supplied eigenbasis or measurement. Factorial-moment Markov gives Pr(X>=j+1)<=c^{j+1}/(j+1)!, uniformly over the promised sources. Fixed c and epsilon make j fixed. The orthogonal component need not be otherwise identified.

For nonzero selected error space, Frobenius reciprocity gives a common S_(k-j) prefix alpha. The occurrence in the restriction of mu gives d_mu<=L d_alpha by induction; occurrence in lambda gives d_alpha<=d_lambda. Therefore D<=L d_lambda. Since M0=L^3 and 6A0/epsilon>1, the Bob dimension threshold implies d_lambda>=K. A sector failing Alice's code-fit test while passing Bob's dimension test has no selected mass and is already in environmental bad mass.

## Complete blocks and finite budgets

For each local-sector/environment-sector branch of the actual source purification, the reduced Alice Specht operator is scalar: the tensor-power purification is invariant under simultaneous permutations, sector projectors commute with those permutations, and tracing the other registers leaves an operator commuting with irreducible rho_lambda. Schur's lemma therefore makes the residual block's relative weight exactly its rank divided by d_lambda, independently of the random code unitary. This is the needed justification for q<K/d_lambda; an arbitrary non-invariant branch would not justify that assertion. Each complete block has weight K/d_lambda. No exponentially many block labels need be compiled as separate dense matrices.

The received moment beta is nonnegative and <=KN/D-K/d_lambda. Complete-block contribution is at most (1-q)A0 beta; weakening to A0 beta and adding q gives <=A0 KN/D. This validates the residual cancellation. N=0 contributes no selected mass; d=1/K=1 trivial-output cases must retain the earlier scope conventions. The physical coefficient weights must stay independent of the code seed, as required in the received mean review.

The filter remainder uses the conservative uniform 2alpha epsilon_f bound, not an exact-Haar first moment applied to an approximate ensemble. The chosen epsilon_f and eta therefore allocate epsilon/6 each. The norm for eta is the unhalved diamond norm of the two-copy twirling map; other moment norms cannot be substituted without conversion factors. Because log K=O(k) and log M0,log alpha0=O(j log k), inverse precision has polynomial logarithm. Polynomial synthesis follows from the separately reviewed logarithmic-precision design interface, not from inverse-tolerance algorithms.

The final implementation allowance must be for the whole adaptive LOCC channel (or a full purified circuit with its classical registers), uniformly over outcomes and random seeds. Polynomial worst-case gate count, branchwise reversible arithmetic, and gate-level error telescoping can supply it. No postselected-block matrix error alone supplies this allowance. Fixed local dimensions imply polynomially many local diagrams; actual Schur transforms, encoder/inverse, outcome routing and messages are charged separately. Six losses then sum to epsilon.

## One-way output convention

Alice may replace her own output on her own rejection and send that flag forward. Bob may locally replace his output on a bad mu, absent selected support, or local decoder failure. Bob cannot require Alice to overwrite her output based on his private mu without backward communication. A fixed joint failure state is unnecessary: any resulting normalized joint state has Bell infidelity at most1. The candidate's phrase about a fixed failure state requires this explicit local-only interpretation. Alice's encoder and code size K must not depend on Bob's private sector; Bob receives Alice's sector, seed and block label and performs the sector-dependent decoder locally.

## Scope

Accepted consequence, once the local-only failure convention is explicit: fixed target error and fixed source parameters yield an efficient one-way ideal-gate dilute-source inner distillation protocol at the stated payload, without source/environment tomography. This is a triangular-array promise delta_k<=c/k, not a fixed positive-noise source theorem. Growing j or shrinking error can destroy uniform polynomiality. High polynomial exponents, large constants, calibrated physical gate noise, conventional-protocol comparisons and experimental promise acquisition remain unestablished. Outer amplification/CSS coding is outside this review.
