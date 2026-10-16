# Checked corollaries of the exact radius formula

These are algebraic consequences of the established radius identification. Historical novelty is not asserted, especially for information-radius additivity.

## Negative-noise symmetric channels and exclusion

For T_lambda=lambda I+(1−lambda)J/m, every stochastic parameter −1/(m−1)<lambda<1 has strictly positive entries. Permutation symmetry and convexity permit a constant optimal center. Writing a=lambda+(1−lambda)/m and b=(1−lambda)/m gives

    C(T_lambda)=1−m²/[1/a+(m−1)/b]
               =lambda²(m−1)/[1+(m−2)lambda].

This derivation covers negative lambda, unlike the previous positive-lambda spectral Jensen argument. At lambda=−1/(m−1), each output row has a zero entry, J is empty, and the exact zero-support theorem gives C=1. At lambda=1, the identity channel likewise has C=1. At lambda=0, C=0.

The ORDINARY input-unrestricted classical chi-square coefficient is

    eta_ord(T_lambda)=m lambda²/[2+(m−2)lambda]

on the full stochastic interval. This is verified in Gu–Polyanskiy, Non-linear Log-Sobolev Inequalities for the Potts Semigroup and Applications to Reconstruction Problems, Appendix A, Proposition 40, Eq. (231). The proof explicitly treats lambda<0 on printed p.814 and confirms the full interval after Eq. (257) on printed p.816. Primary author PDF: https://people.lids.mit.edu/yp/homepage/data/nlsi_potts.pdf . The ordinary exclusion endpoint is 1/(m−1).

For the strictly positive approximation lambda=−(1−delta)/(m−1), 0<delta<1,

    C=(1−delta)²/[1+(m−2)delta],
    eta_ord=m(1−delta)²/[(m−1)(m+(m−2)delta)],
    C/eta_ord=(m−1)(m+(m−2)delta)/[m(1+(m−2)delta)].

Taking delta=o(1/m), for example delta=1/m², gives C→1 and C/eta_ord~m−1. By OPERATIONAL_CLASSICAL_THEOREM.md these compare exact complete versus ordinary binary-MMSE erasure thresholds, with arbitrary quantum side information allowed in the complete problem. They do not assert a growing absolute Bayes-risk advantage or any capacity comparison. The strict operational witnesses can involve very small binary perturbations.

## Parallel product composition

Let h(T)=1−C(T), and, when h>0, let K(T)=1/h(T)=min_w max_i Σ_y w_y²/T_yi. For strictly positive T,S:

- Product normalized centers give K(T⊗S)<=K(T)K(S), since the quadratic objective factors on each product input column.
- Product optimal dual priors give h(T⊗S)<=h(T)h(S), since each reciprocal row sum and the total row sum factor. This yields the reverse inequality for K.

Therefore exactly

    C(T⊗S)=1−(1−C(T))(1−C(S)).

The same statement follows with zero entries using the common-support definition: the common output support of the product is J_T×J_S; an empty factor support makes h=0, while otherwise both preceding constructions remain valid on the common supports. For k identical parallel copies, C(T^⊗k)=1−(1−C(T))^k.

This concerns the complete conditional-excess coefficient and its erasure-comparison threshold. It should not be described as fixed-prior chi-square tensorization, nor as a statement about independent restricted encodings. The optimized input encoding and reference may be joint across all channel uses.

## Bounded binary loss obstructs a dimension-independent absolute advantage

Let U be the uniform-replacement measurement channel on the same m-input/m-output alphabet. For every stochastic lambda,

    ||T_lambda−U||_diamond = 2|lambda|(1−1/m).                 (A)

Here the diamond norm is the trace norm without a factor 1/2. An elementary proof covers arbitrary ancillary dimensions and arbitrary, even non-Hermitian, test operators X. If X_ii are its diagonal input blocks, the output difference is block diagonal with y-block Σ_i a_yi X_ii, where a_yi=lambda(delta_yi−1/m). Hence

    ||((T_lambda−U)⊗id)(X)||_1
      <= Σ_yi |a_yi| ||X_ii||_1
      <= max_i Σ_y|a_yi| · Σ_i||X_ii||_1
      <= 2|lambda|(1−1/m)||X||_1.

The last inequality uses trace-norm contractivity of block pinching (an average of unitary conjugations). A basis-state input attains the column l1 norm, proving equality in (A).

Now consider ANY binary label ensemble x∈{−1,1}, arbitrary prior, arbitrary input/reference states, and arbitrary finite quantum reference. For squared loss, every reported estimate can be clipped to [−1,1] without increasing its pointwise loss. Thus the loss is in [0,4]. For a fixed measurement-estimator and the joint label/output/reference state, its risk is Tr(Lρ) for a loss operator 0<=L<=4I. Since the difference of two normalized states has trace zero,

    |Tr L(ρ−σ)| <= 4 · (1/2)||ρ−σ||_1.

Apply (A) to the joint label/reference ensemble. The risk of every clipped estimator changes by at most 4|lambda|(1−1/m). Taking infima over estimators on both sides preserves the same bound:

    |MMSE(T_lambda)−MMSE(U)| <= 4|lambda|(1−1/m).              (B)

E_q can reproduce U by ignoring its classical outcome, generating an independent uniform symbol, and retaining the reference. Therefore MMSE(E_q)<=MMSE(U), and

    MMSE(E_q)−MMSE(T_lambda)
      <= min{1, 4|lambda|(1−1/m)}.                            (C)

The extra bound 1 follows because the constant prior-mean estimator has risk Var(x)<=1 and risks are nonnegative. No equal-prior or equal-reference-marginal assumption is needed.

At the exclusion channel lambda=−1/(m−1), (C) becomes min{1,4/m}. For its strictly positive delta approximation it becomes min{1,4(1−delta)/m}. Thus the unbounded complete/ordinary erasure-threshold ratio DOES NOT furnish a dimension-independent absolute binary-MMSE advantage. In this family every absolute advantage vanishes as m→∞, regardless of reference dimension. This is a rigorous practical limitation, not a numerical optimizer failure.

`../checks/verify_bounded_loss.py` checks the exact rational column distance and simple binary Bayes risks for several alphabet sizes. These sanity checks supplement, rather than replace, the all-reference proof above.
