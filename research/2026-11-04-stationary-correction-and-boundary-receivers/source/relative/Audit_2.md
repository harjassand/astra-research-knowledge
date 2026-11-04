# Independent adversarial audit: weighted Pfaffian interfaces

Date: 2026-11-04.
Audited file: ../PROOF.md.
Audited SHA-256: c46f70d3ed6e5f4960bfb38fa1f5c3279eb4cecb3ad1c85b44d4820b67597b35.

## Verdict

No counterexample or substantive mathematical error found in the stated theorem. The relative-error interface, finite-sample product-field response algorithm, sequential signed-mass repair, and multi-block certificate are justified under their explicit promises. This is not a general contraction algorithm and not a proof of novelty or practical superiority. The positivity assumptions, isolated-data contract, and distinction between signed algebra and sampled surrogates are essential.

## 1. Weighted derivative bound survives the rare-event attack

A mixed derivative with respect to disjoint upper-triangular pair coordinates has absolute value equal to a normalized product of: uniform spins on the removed endpoints, and a sign-flipped genuine marginal on the remaining coordinates. Its total mass is exactly one. Shared-endpoint derivatives vanish.

For nonnegative W with nonnegative Fourier coefficients, its expectation in this derivative law is

sum over S avoiding removed endpoints of w_S chi_S m_S.

Odd moments vanish; even m_S are nonnegative. This expression is at most sum_S w_S m_S = Z, by removing sign flips and restoring omitted nonnegative terms. The left side is nonnegative because both W and the absolute derivative law are nonnegative. No lower bound on a particular assignment probability is used.

Taylor expansion is around the genuine C only. Every surviving monomial is a matching, hence the weighted absolute error is bounded by Z times the sum of products of absolute coordinate perturbations. Bounding this sum by exp(D)-1 is valid. No positivity of any interpolated matrix, Taylor intermediate, or reconstructed distribution is required.

The same-sign rare-event example is sound: for H of size r, W=product_{i in H}(1+x_i), Z=2^r P(all H are plus), and Z>=1 because its Fourier constant is one and all contributing moments are nonnegative. Thus P(event)>=2^-r. The known factor 2^-r introduces the exponentially small probability without an ill-conditioned normalization. Relative error in Z is exactly relative error in the event probability. This does not extend to a mixed-sign assignment.

More generally, every nonzero nonnegative W in the admitted Fourier cone has w_empty>0 and Z>=w_empty. The assumption Z>0 is therefore consistent, not a hidden numerical probability oracle.

## 2. The environment cone has the advertised closure, but not arbitrary evidence

Products of factors (1+a x_i x_j) and (1+t x_i), with a,t>=0, retain nonnegative Fourier coefficients because multiplication uses symmetric difference of index sets and never introduces a negative coefficient. Summing hidden spins discards all monomials with nonempty hidden support. Hard equalities are valid factors. Nonplanarity does not affect these algebraic statements.

However, ferromagnetic interactions alone are insufficient when external fields have opposing signs. The two-spin example W=(1+x_1)(1-x_2), correlation c=1-rho, has Z=rho; an absolute perturbation delta in c changes relative normalization by delta/rho. This is a genuine obstruction to extending the same condition number to arbitrary observations. A global sign change handles uniformly negative fields, not arbitrary local sign changes in a connected ferromagnetic environment.

Physical application requires the EXACT common-face Pfaffian and nonnegative-moment promises. Approximate emergence of Pfaffian correlations near criticality does not satisfy the theorem automatically: a separate weighted error budget for model mismatch would be necessary. Nor do equilibrium observations taken inside an unknown interacting environment automatically supply the isolated block law.

## 3. Normalization and sequential clipping are correct

Let r be the normalized signed weighted law, with total mass one. At any reached prefix a, its signed mass r(a) is positive. If child masses are r(a,-) and r(a,+), the sum of their positive parts is at least r(a)>0. Inductively, sampled prefix mass Q(a)<=r(a) on reached positive prefixes. Therefore

Q(a,b)=Q(a) r(a,b)_+ / sum_c r(a,c)_+ <= r(a,b)_+.

At full assignments, Q<=r_+. Since both Q and the target P_W have mass one, TV(Q,P_W) equals their positive excess mass, which is at most the positive excess mass of r-P_W. The latter is half its L1 norm. This proves the advertised bound without a per-prefix lower probability bound. Tiny or zero true conditional probabilities do not invalidate the argument.

This clipping argument applies AFTER forming the chosen environment's complete signed weighted prefix contractions. The proof does not license separately clipping each learned block in isolation and then treating those clipped blocks as interchangeable inputs to arbitrary environments. That is a different operation and needs a separate theorem. The current proof does not make that stronger claim; downstream summaries should not imply it.

## 4. Product-field identities and hard fields

The sign convention in F_A(z)=Pf(J-D_z A D_z), with one-based D_z, is correct. In the Pfaffian minor expansion, the signs from choosing the A minor are canceled by the alternating diagonal and the minus sign. Padding odd k with a zero A row/column and dummy z=1 preserves the polynomial. The two-spin case gives 1+A_12 z_1 z_2, confirming the convention directly.

The stated prefix expression follows by multiplying the prefix indicator factors and evaluating each fixed boundary field at its assigned spin. It remains valid for negative prefix values, t_i=0, and t_i=1. Mixed signs inside a computational prefix do NOT require a new statistical guarantee for a mixed-sign external environment; they are merely exact evaluations of the same signed polynomial. The global clipping theorem supplies the error bound.

The procedure supports arbitrarily strong encoded activities, including exact hard plus pins. It does not promise efficiency in the bit length of an unbounded real field when converting that field to an exponentially long explicit activity representation. This limitation is correctly stated.

## 5. Bit complexity and statistical accounting

Each empirical entry has denominator N. A Pfaffian term has degree at most floor(k/2) in those entries and degree at most k in the z variables. A common denominator using N^floor(k/2) and the product of query denominators has polynomial bit length. The number of matching terms contributes O(k log k) bits to coefficient height, not exponentially many bits. Prefix prefactors and rational conditional divisions preserve polynomial bit length, even if a prefix is numerically extremely small. Exact pivoted rational or fraction-free Pfaffian elimination therefore suffices.

The stated Hoeffding bound for variables in [-1,1] is valid. With m pair coordinates and h=epsilon/(32m), the union event gives D<=epsilon/32. For epsilon<=1, exp(D)-1<=epsilon/16, so the subsequent normalization and TV constants are conservative.

A reduced rational Bernoulli coin a/b can be drawn using ceil(log2 b) unbiased bits and rejection. Acceptance probability exceeds one half unless it is exactly one. Capping the number of trials at the stated R gives a union-bounded O(epsilon) perturbation over k choices. The fallback must be a positive signed child as specified. The given capped transition probability and its exact evaluation are correct; its numerator/denominator bit sizes grow by a polynomial factor R.

No exponential rare-event sample cost is hidden in these arithmetic steps. Physical mixing, independent snapshot acquisition, and calibration of the structural promise remain outside the iid data contract. The theorem is per learned output distribution, not jointly epsilon-close for an unlimited stream of samples.

## 6. Multi-block expansion is valid without intermediate positivity

Treat pair variables from all blocks as disjoint coordinates and expand once around the product of genuine block laws. A mixed derivative selects a matching in each involved block. Its absolute value is a product of normalized uniform/sign-flipped marginal laws. For a Fourier monomial of W, the expectation factorizes by block. If an intersection with a block is odd, its contribution is zero; otherwise all true block moments are nonnegative. The same deletion-of-signs argument bounds every weighted derivative norm by the ORIGINAL Z. Summing terms gives exp(sum_b D_b)-1.

This is stronger and safer than iterating a one-block theorem at perturbed signed environments, where the required positivity need not hold. The manuscript uses the correct simultaneous expansion.

The certificate does not supply polynomial-time contraction for general compact W. Prefix evaluation can remain difficult. Hard identifications are allowed only through explicit constraints on initially distinct boundary copies; normalizations are relative to the independent isolated laws. Passive samples do not determine additive bulk energy constants or the individual absolute block partition functions. These boundaries are correctly retained.

## 7. Independent exact checks

Independent exact rational computations, not the author's audit script, checked:
- 42 Pfaffian generating-polynomial identities for k=1 through 7, with mixed-sign rational matrices and mixed-sign z.
- 210 weighted prefix identities, including hard t_i=1 and zero fields.
- 100 nonnegative-Fourier environment tests for weighted stability and sequential clipping, with genuinely signed reconstructed distributions.

The signed test used four perfectly aligned unbiased spins, C_ij=1 above the diagonal, and A_12=9/10 with other upper entries unchanged. Its reconstructed law has minimum mass -1/80. For generated product-field/ferromagnetic-edge environments, exact arithmetic verified weighted error <= Z/10 (the stronger one-coordinate bound), normalization, Q<=r_+, and the claimed TV inequality. This perturbation is an algebraic stress test, not an assertion that this particular empirical matrix occurs from sampling the perfectly aligned law.

Finite checks supplement the analytic proof; they do not establish its generality or novelty. No code is included in this proof-only audit packet.

## 8. Strongest direct prior-method comparison

Common-face multipoint Pfaffian identities and boundary correlation parametrizations are established. Galashin and Pylyavskyy, https://arxiv.org/abs/1807.03282 , relate boundary correlations to the positive orthogonal Grassmannian. The exact known-parameter Pfaffian representation is not new.

Specified planar Ising models already admit Pfaffian-based correlation and sampling methods, including Thomas and Middleton, https://doi.org/10.1103/PhysRevE.87.043303 . Planar zero-field models with fields only on a common boundary can also be handled by introducing a ghost spin in that face: condition the ghost to plus, and the added edges implement the boundary fields while preserving planarity. Thus all-strength boundary response is not a new specified-model tractability class.

Learning planar Ising models from pair correlations is also established, e.g. Johnson et al. (2016), https://jmlr.org/papers/v17/15-579.html . That work fits an explicit planar graphical model; it is not, from the inspected abstract, the same hidden-bulk-independent uniform relative-response guarantee proved here.

The 2026 Pfaffian point-process sampler cited in the manuscript, https://arxiv.org/abs/2605.01202 , is an appropriate related algebraic comparator, not evidence by itself that arbitrary noisy signed kernels are physical point-process kernels. Likewise matchgate computation does not convert the abstract arbitrary-environment stability certificate into an efficient algorithm.

The potentially distinct contribution is the assembled finite-data, uniform weighted relative-error guarantee and signed-prefix repair under the stated promise. This audit did not establish priority for that guarantee. A defensible comparison must supply the same access model: unknown hidden bulk, known boundary ordering, iid isolated full-boundary samples, and rational boundary activities. No practical or civilisation-scale advantage follows from correctness alone.
