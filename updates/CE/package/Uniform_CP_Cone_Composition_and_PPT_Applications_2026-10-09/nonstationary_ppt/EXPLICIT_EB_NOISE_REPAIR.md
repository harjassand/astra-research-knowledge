# Explicit separable-noise repair and exponential EB domination

9 October 2026. New complete strengthening of the approximation candidate. This removes the semialgebraic error-bound step from EXPONENTIAL_APPROXIMATE_PPT_WORDS.md and gives a positive, separable-noise repair. The earlier route remains valid and preserved. The present derivation is not covered by the old focused reviews. No priority or external-certification claim is made.

## 1. Inputs and constants

Fix d>=2 and put r=d-1. Use the explicit constant c_d=1−1/(8d) proved in GAUSSIAN_PPT_CONCURRENCE_GAP.md. PAIR_ROTATION_CONCURRENCE_GAP.md independently supplies the weaker 1−1/(4d^2) bound. Sections 1 and 4 of EXPONENTIAL_APPROXIMATE_PPT_WORDS.md give the exact qubit filter covariance and its contraction consequence. The earlier compactness proof remains independently preserved, but no non-numerical constant is now required for this approximation rate.

For a length-m word S of CPTP, 2-copositive maps and every isometry V:C^2->C^d, the normalized state

 rho_V=(id_2 tensor S Ad_V)(omega_2)

satisfies

 dist_F(rho_V,Sep_(2,d))<=delta_m,
 delta_m=sqrt(2)c_d^m.                                 (1)

Here omega_2 is the normalized Bell projector. This is the concurrence-to-distance estimate already proved there. No Schmidt-number conjecture is assumed.

Define the depolarizing channel D_d(X)=tr(X)I_d/d and

 b_d=1/(4d^2),
 p_m=delta_m/(b_d+delta_m),
 beta_m=1-p_m=1/(1+4sqrt(2)d^2 c_d^m).                 (2)

The values are explicit and deliberately conservative. No sharpness claim is made.

## 2. Elementary rectangular separable ball

The Frobenius ball of radius b_d around

 omega_0=I_2/2 tensor I_d/d

consists of separable positive operators when restricted to Hermitian perturbations of that size. A short proof supplies the stated constant.

Choose real Hilbert–Schmidt orthonormal Hermitian bases {H_a} of M_2 and {G_b} of M_d. Each basis element has operator norm at most one. For either sign,

 I_2 tensor I_d +/- H_a tensor G_b

is separable: average the two appropriate products (I_2+/-H_a) tensor (I_d+/-G_b), whose factors are positive. A Hermitian Z has 4d^2 real product-basis coefficients, so their absolute sum is at most 2d||Z||_F. Consequently I_2 tensor I_d+Z is separable if ||Z||_F<=1/(2d), by a convex combination of these signed separable operators and the identity. Dividing by 2d proves b_d=1/(4d^2).

No optimal separable-ball result is required.

## 3. A direct 2-EB repair

Set

 S_tilde=beta_m S+p_m D_d.                              (3)

We prove S_tilde is 2-entanglement breaking and CPTP.

For each V, choose a separable density matrix sigma_V with

 ||rho_V-sigma_V||_F<=delta_m.

Such a minimizer exists by compactness. Since depolarization sends the embedded Bell state to omega_0,

 (id_2 tensor S_tilde Ad_V)(omega_2)
 =beta_m sigma_V+[p_m omega_0+beta_m(rho_V-sigma_V)].    (4)

The bracket is separable by Section 2, because

 beta_m delta_m=p_m b_d.

Both summands in (4) are therefore separable. Their traces add to one.

It remains to check that these particular inputs test 2-EB. Every pure vector psi on C^2 tensor C^d can be written

 psi=(A tensor V)|Omega_2>,

where V is an isometry and A is a 2-by-2 matrix, including singular A. The qubit filter A commutes with the local channel. Thus the output of S_tilde on |psi><psi| is a local filter of (4) and is separable. Convexity covers arbitrary positive inputs. This proves genuine 2-EB, not merely small distance to the 2-EB set.

This argument is also a linear error bound in this setting: a uniform separability defect delta on the embedded Bell test states is repaired by at most delta/(b_d+delta) depolarizing admixture. No Lojasiewicz inequality, convex-roof continuity theorem, or dimension-recursive approximation is needed in the repaired step.

## 4. A positive EB dominator after d-1 blocks

Published input: Christandl–Müller-Hermes–Wolf, arXiv:1807.01266v2, Theorem II.1, https://arxiv.org/html/1807.01266v2 . A serial product of r=d-1 independently varying CP 2-EB maps on M_d is EB. This known theorem is credited, not claimed here.

Take an n-word T of CPTP, 2-copositive maps, with n>=r. Put m=floor(n/r), divide r m of its factors into r consecutive length-m blocks S_1,...,S_r, and leave any remaining factors in an exterior CPTP segment L. Thus

 T=L S_r ... S_1.

Repair each S_j by (3), using the same beta_m,p_m. Then

 E=L (beta_m S_r+p_m D_d) ... (beta_m S_1+p_m D_d)

is EB and CPTP by the published theorem.

Expand this expression as a sum of positive CP words. The term containing no D_d is q_n T, where

 q_n=beta_m^r=(1+4sqrt(2)d^2 c_d^m)^(-r).               (5)

Every other term contains a depolarizing channel and is EB. Consequently

 E=q_n T+F,                    E,F are EB CP,
 E*(I)=I,                      F*(I)=(1-q_n)I.          (6)

Thus E does more than CP-dominate q_n T: its positive remainder F is itself EB. Equations (5)–(6) are an explicit separable-noise repair of the entire word.

In particular

 ||T-E||_diamond<=2(1-q_n)
 <=8sqrt(2)(d-1)d^2 c_d^floor(n/(d-1)).                 (7)

For the last estimate use 1-(1+x)^(-r)<=r x. The quantity is also bounded by 2. With c_d=1−1/(8d), this is a fully explicit ordinary exponential bound. In particular, for 0<eta<2, it suffices to take

 n >= (d−1) ceil[8d log(8sqrt(2)(d−1)d^2/eta)]          (7a)

to make the error at most eta. This is O(d^2 log(d/eta)). The inequality is a conservative mathematical guarantee; no claim is made that the resulting length is near optimal. For n<d−1 the trivial error bound 2 applies.

## 5. Arbitrary CP words and positive joint inputs

For a word T of arbitrary CP, 2-copositive maps, let H=T*(I). POSTSELECTION_ROBUST_EB_APPROXIMATION.md, Section 2, proves the exact factorization

 T=S Ad_(sqrt(H)),

where S is a word of the same length in CPTP, 2-copositive maps. The direct support-completed formula handles singular H without taking an inverse on its kernel.

Apply (6) to S and precompose the resulting maps by Ad_(sqrt(H)). There are EB CP maps E,F satisfying

 E=q_n T+F,
 E*(I)=H,                       F*(I)=(1-q_n)H.         (8)

For every finite reference R and every positive joint input X,

 ||(id_R tensor (T-E))(X)||_1
 <=2(1-q_n) tr[(id_R tensor T)(X)].                     (9)

Indeed T-E=(1-q_n)T-F, and the two positive output terms have the same trace (1-q_n)tr[(id_R tensor T)(X)]. Triangle inequality gives (9).

If the success probability p is nonzero, define the normalized actual output rho, the normalized E-output sigma, and the normalized F-output nu. Then sigma and nu are separable and

 sigma=q_n rho+(1-q_n)nu.                              (10)

So a fraction 1-q_n of explicitly separable noise suffices to make every conditioned output separable, uniformly over the input and reference. In the usual convention where one mixes rho with t times a normalized separable state and divides by 1+t, this supplies the upper bound

 t<=(1-q_n)/q_n=(1+4sqrt(2)d^2 c_d^m)^(d-1)-1.          (11)

Equation (10), rather than terminology for an entanglement measure, is the precise assertion.

## 6. Meaning and limits

This strengthens the postselection-robust trace-distance statement by exhibiting a positive EB remainder with exactly controlled effect. Finite classical-outcome instruments can be treated branchwise as in POSTSELECTION_ROBUST_EB_APPROXIMATION.md. If branches have different lengths at least n, lower a branch's q to the common q_n by mixing its EB E-map with any effect-matched EB channel; the effect and EB-noise form remain valid. Alternatively apply the n-step bound and absorb exterior CP factors.

The fixed transmitted dimension, absence of bypassing noiseless quantum memory, and CP/2-copositivity of every counted branch remain essential. This is not a general quantum-network impossibility theorem. The channel-level repair is explicit. An efficient measure-and-prepare decomposition or optimality of the rate is not asserted.

A positive EB dominator with q_n arbitrarily close to one does not imply T is itself EB. Full-rank entangled states can approach a separable boundary with arbitrarily small required separable-noise dilution. The exact finite-word gate remains separate.
