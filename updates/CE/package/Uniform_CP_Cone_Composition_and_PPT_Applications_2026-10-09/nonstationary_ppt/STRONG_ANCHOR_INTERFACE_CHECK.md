# Strong anchor normalization and positive expansion

9 October 2026, 22:25 UTC. Targeted derivation check for the dependency used by UNRESTRICTED_PPT_WORD_THEOREM.md. This is not an independent broad review or a claim of external certification. The preceding proof records are preserved unchanged.

## Rectangular product input

Davidson–Marcoux–Radjavi, Transitive Spaces of Operators, arXiv:0706.2449, Theorem 4.9, was re-opened directly at https://arxiv.org/html/0706.2449 . For K subset M_(m,n) and L subset M_(n,p), with transitivity degrees k and l, their product span has degree min(k+l,m,p). There is no identity or common-space hypothesis.

In the application, each nonzero filter A_j factors through its rank as B_j C_j, with B_j injective and C_j surjective. Hence C_j S_j B_(j−1) is transitive whenever the seed Kraus span S_j is transitive. Starting with a transitive rectangular prefix, each next space increases its transitivity degree by one unless an endpoint dimension is reached. At that point the prefix is the full rectangular matrix space: its annihilator contains no nonzero matrix of any possible rank. A full rectangular prefix stays full after multiplication by another transitive space, because every rank-one output matrix is A(xz*) with Ax prescribed. Thus d seed occurrences give the full final square matrix space, even if intervening ranks oscillate.

## Compactness after gap normalization

For every nonzero CP internal gap C set c=tr J(C)>0 and C'=C/c. The normalized maps C' form the compact positive-Choi trace-one slice. In particular the zero map is excluded, while rank-deficient maps remain included. For seeds in a fixed compact strictly output-positive family, the filtered d-seed product has positive-definite Choi matrix at EVERY point of this compact parameter space: choose a nonzero Kraus matrix from each gap and use the full-span argument above. The continuous minimum Choi eigenvalue therefore has a strictly positive minimum eta. A finite maximum beta gives

 eta D <=_CP V <=_CP beta D,       D(X)=tr(X)I.

All removed positive scalars multiply the whole word and do not affect EB membership. Gaps between d-seed chunks need no normalization at all. A zero gap makes the containing word zero.

## Positive expansion with arbitrary gaps

Let T=V_t C_(t−1) V_(t−1) ... C_1 V_1, t>=2, and V_j=eta D+R_j. Put z=1−eta/beta. Since V_j<=_CP beta D,

 0<=_CP R_j<=_CP z V_j.

The all-R expansion term R is CP and satisfies R<=_CP z^t T by repeated positivity of composition. Every other expansion term is EB because it contains D. Their sum is F=T−R, with no subtraction used to infer a property of an individual term.

Write H=C_(t−1)V_(t−1)...V_2 C_1 and w=tr H(I). The positive expansion terms choosing eta D at the final output endpoint sum to

 F_left=eta D H V_1.

They are among the terms defining F. Furthermore

 F_left−eta^2 w D=eta D H (V_1−eta D)

is EB. Thus F>=_EB eta^2 w D. The comparison at the two endpoints also gives T<=_CP beta^2 w D. Consequently

 ||J(R)||_F <= tr J(R) <= z^t beta^2 w d^2.

Using the conservative separable-ball radius 1/d^2 around J(D)=I tensor I, the sum eta^2 w D+R is EB whenever

 z^t beta^2 d^4 <= eta^2.

Then T=(F−eta^2wD)+(eta^2wD+R) is a sum of EB maps. If w=0, H=0 and T=0. If eta=beta, every chunk is eta D. Otherwise 0<z<1 and such a finite t exists.

This verifies the arbitrary-gap interface used in the unrestricted dimension induction. No trace or unital assumption on the gaps, and no inverse gap singular value, enters the constants.
