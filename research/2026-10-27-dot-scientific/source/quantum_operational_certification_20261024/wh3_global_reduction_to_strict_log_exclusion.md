# A sufficient operator-log exclusion for the FULL unrestricted target

2026-10-25. Root derivation. The operator-log premise below is UNPROVED. This note proves its full-target receiving consequence; it does not assert that the premise holds.

## Sufficient finite-dimensional lemma L

For every pair of faithful positive matrices A,B with equal trace and A<9B, and every0<p<1/4, the matrix

F_p(A,B)=2log(pA+(1-p)B)-log A-log B

is NOT positive definite.

This is weaker than claiming F_p>=0 forces A=B. No invalid exponentiation of operator inequalities is used. A generic counterexample to L would reject this sufficient route, not refute the WH3 target, since the application additionally has B=E(A).

## Target and regularization

Let N=W3 tensor id_R and E(rho)=I3/3 tensor rho_R. Define the homogeneous defect

Delta_N(rho)=D(rho||E rho)-2D(N rho||E rho)
=2S(N rho)-S(rho)-S(rho_R)-(Tr rho)log3

for normalized rho, with the obvious homogeneous interpretation elsewhere. The target is Delta_N>=0 in every finite reference dimension.

Suppose a counterexample exists. Define N_t=(1-t)E+tN. Entropy continuity implies that the same finite-dimensional state remains a strict counterexample for some t<1 sufficiently close to1. N_t is unital, trace-preserving, CP, self-adjoint, fixes E, and

N_t^2=(t²/4)id+(1-t²/4)E.

## A negative global minimizer is faithful on its actual reference support

In the given finite reference dimension, Delta_(N_t) is continuous on the compact state space and has a negative minimum. Choose a minimizing rho and restrict R to the support of rho_R. This restriction changes no nonzero eigenvalues or entropies, and the minimizer is still minimizing among all states on that smaller space. Now sigma=E rho is faithful.

N_t rho>=(1-t)sigma>0. If rho had a nonzero kernel, mix it toward sigma:

rho_epsilon=(1-epsilon)rho+epsilon sigma.

Its reference marginal is EXACTLY unchanged. Opening the input kernel raises S(rho_epsilon) by c epsilon log(1/epsilon)+O(epsilon), c=Tr(P_ker rho sigma)>0, while output entropy is smooth because N_t rho is faithful. Therefore Delta_(N_t)(rho_epsilon)<Delta_(N_t)(rho) for small positive epsilon, a contradiction. Hence rho is faithful as well.

## Full stationarity and operator Jensen

At this interior trace-one minimizer, differentiation gives

log rho-2N_t(log N_t rho)+log sigma=lambda I.

The derivative of the reference term is log sigma because E is a self-adjoint conditional expectation. Euler homogeneity gives lambda=Delta_(N_t)(rho)<0.

Operator Jensen for the unital CP map N_t yields

N_t(log N_t rho)<=log(N_t² rho).

Thus, with p=t²/4,

2log(p rho+(1-p)sigma)-log rho-log sigma>=-lambda I>0.

Finally, the complete index bound is rho<=9E rho. For a positive3x3 block matrix rho=(rho_ij) and a block vector(v_i), positivity gives |<v_i,rho_ij v_j>|<=sqrt(<v_i,rho_ii v_i><v_j,rho_jj v_j>); scalar Cauchy–Schwarz and rho_ii<=rho_R then give <v,rho v><=3 sum_i<v_i,rho_R v_i>=<v,9E rho v>. It is STRICT for faithful rho: write rho=epsilon I+X with X>=0 and apply the non-strict bound to X, obtaining9E rho-rho>=8epsilon I>0. Therefore A=rho,B=sigma meet all premises of L, contradicting it.

This proves: lemma L implies the FULL unrestricted WH3 half-relative-entropy contraction in every finite reference dimension. The regularized channel, rather than an assumed catalogue of boundary equality states, removes the singular-output obstruction.

## Exact remaining issue

L is not proved here. The commuting case follows directly from scalar ratios: for p<1/4, a positive diagonal entry of F_p at a ratio r>1 requires r>((1-p)/p)^2>9, incompatible with the cap; equal traces force some r>=1. Noncommuting log sums cannot be treated as scalar ratios. Neither trace-only tests, ordinary exponentiation, finite numerical probes, nor the proved local cap-boundary perturbation exclusion establish L.

The stronger source-compatible premise restricting B to I3/3 tensor Tr_A A could suffice even if the generic matrix lemma fails. No claim of equivalence, historical novelty, or completed conjecture follows from this reduction.
