# Full WH3 bound for every flat-marginal and modular-commuting input

2026-10-25. Exact entropy-duality receiver of the all-projector theorem. This does not use monotonicity under discarding quantum memory.

## 1. Every flat reference marginal is safe

Let rho_AR be any finite-dimensional state, with physical A=C3, whose reference marginal is flat on its support:

rho_R=Pi_R/r.

Purify rho_AR to a pure state psi_ARE. Apply the antisymmetric Stinespring isometry of W3, obtaining a pure state Omega_BCRE. Both channels A->B and A->C are W3 up to a fixed unitary. Consequently

I(B:C|R)_Omega
=2S((W3 tensor id_R)(rho_AR))-S(rho_AR)-S(rho_R)
=Delta_N(rho_AR)+log3.

Purity gives exact conditional-mutual-information duality I(B:C|R)=I(B:C|E). Thus

Delta_N(rho_AR)=Delta_N(rho_AE).                          (1)

This same physical identity is already established in wh3_rank_two_qubit_reference_mi_theorem.md, Section 3; no partial trace is claimed to improve the deficit.

The nonzero spectrum of rho_AE is exactly the spectrum of rho_R, hence rho_AE is a normalized rank-r projection. The all-projector input theorem applies to it, with arbitrary E dimension. Equation (1) therefore proves

Delta_N(rho_AR)>=0

for EVERY state with flat reference marginal, with no restriction on its global rank or global spectrum.

## 2. Every state commuting with its own reference marginal is safe

More generally suppose

[rho_AR,I_A tensor rho_R]=0.

Let the distinct positive spectral values of rho_R be lambda_j on orthogonal reference subspaces R_j of dimensions r_j. The commutation assumption gives the actual block decomposition

rho_AR=direct_sum_j p_j rho_j, p_j=lambda_j r_j,
Tr_A rho_j=I_(R_j)/r_j.

Every rho_j has a flat reference marginal, so Section 1 applies. Since N and E act trivially on the classical reference block label, the homogeneous entropy deficit is exactly additive:

Delta_N(rho_AR)=sum_j p_j Delta_N(rho_j)>=0.              (2)

The classical flag entropy cancels with coefficients 2-1-1. Thus this is a proved arbitrary-spectrum, arbitrary-rank class of the unrestricted physical target, not merely an invariant 1+8 family. Quantum correlations inside degenerate marginal eigenspaces are unrestricted.

## 3. Exact obstruction to removing the commutation condition by pinching

The spectral pinching of rho_R is a physical operation but need not improve Delta. Here is an exact source-compatible example with NONFLAT marginal and with the pinching uniquely determined by its distinct eigenvalues.

Let A=R=C3, let |phi>=(|00>+|11>)/sqrt2 and Phi2=|phi><phi|. Set

sigma=(1/2)[(3/5)Phi2+(2/5)|22><22|]+I9/18,
H=|phi><22|+|22><phi|.

Sigma is faithful, with minimum eigenvalue1/18. Both partial traces of H vanish, and

sigma_R=diag(19/60,19/60,11/30).

Its canonical reference spectral pinching has blocks span{|0>,|1>} and span{|2>}. It preserves sigma and annihilates H. Therefore rho_t=sigma+tH has the same nonflat reference marginal, and its canonical marginal pinching is sigma for every sufficiently small t.

The input BKM metric is exact. H connects eigenvectors of sigma with eigenvalues a=16/45 and b=23/90, whose difference is1/10. Hence

g_sigma(H)=2 log(a/b)/(a-b)=20log(32/23).

At the output, NH has two disjoint off-diagonal pairs, each of amplitude1/(2sqrt2), joining baseline eigenvalues c=7/45 and d=47/360. Since c-d=1/40, the two pairs give

g_(N sigma)(NH)=20log(56/47).

Therefore

2g_(N sigma)(NH)-g_sigma(H)
=20log[(56/47)^2(23/32)]
=20log(2254/2209)>0.                                    (3)

All signs in (3) are exact rational-log comparisons. No numerical optimization, limiting regularization or unproved error bound enters.

Because the marginal is constant along rho_t, the second derivative of Delta is g_input-2g_output. Thus, for sufficiently small nonzero t,

Delta_N(rho_t)<Delta_N(sigma).

The first derivative vanishes by the phase symmetry that sends H to -H while preserving sigma and channel entropy. Positivity of rho_t follows, for example, from |t|<1/18 since ||H||=1.

This example rejects the assertion that canonical marginal pinching can reduce the general problem to (2) for free. It does not violate the full entropy target: the safe block baseline has a positive margin, and (3) does not establish that the coherence cost can exhaust it.

## Scope

Any still-possible counterexample must fail to commute with its own reference marginal (and, by the same purity duality, evade the corresponding proved class on the complementary reference). The missing global construction must retain both the established block margin and the actual inter-marginal coherence cost. No information or entropy is discarded for free.
