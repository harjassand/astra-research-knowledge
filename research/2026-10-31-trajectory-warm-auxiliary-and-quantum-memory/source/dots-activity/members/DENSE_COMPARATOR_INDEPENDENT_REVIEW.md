# Independent narrow review: dense exponential and CPTP repair comparator
31 October 2026. Reviewer: independent internal mathematical review.

## Scope and binding
PASS for Section 3 of graded_reservoir_comparison_20261031/PRIMARY_COMPARISON_AND_CONSEQUENCE.md, source SHA-256 9909bb26470ee7755d6172ebbe8fc456d0e47139486f15f0c0ab3f6ed62218a2. I read the actual Section 3 and surrounding scope statements and verified the source hash. This is not an independent verification of every literature comparison in the other sections.

The accepted claim is polynomial work in the FULL finite Hilbert dimension d and input/precision lengths, with logarithmic dependence on the generator action bound Bt. It is not efficient succinct access to an exponentially large matrix. All matrix acquisition and input-dependent preprocessing remain paid.

## Scaling and squaring
For the exact channel powers E_j, ||E_j||_diamond=1. If X_j differs by e_j, submultiplicativity gives
||X_j^2-E_j^2||_diamond<=2e_j+e_j^2.
Thus 1+e_s<=(1+delta_0)^(2^s) without arithmetic rounding. Choosing s with Bt/2^s<=1 and delta_0=O(epsilon/2^s) gives final O(epsilon) error.

On the scaled argument, the exponential Taylor remainder is at most e/(k+1)!, so the displayed conservative k=O(log(1/delta_0)+1) suffices. Entrywise/dense-matrix errors convert to diamond errors with dimension-polynomial factors. Squaring-roundoff errors can be assigned weighted budgets of order epsilon/2^(s-j). Intermediate map norms remain bounded; there is no exp(Bt) precision loss.

Accordingly s=O(log(2+Bt)) dense squarings and polynomial arithmetic/guard precision suffice. Input coefficient and acquisition lengths must still be counted, as stated.

## Explicit CPTP repair
Use the unnormalized Choi convention with channel partial trace I and trace d. If the approximate exponential has diamond error eta, its Hermitian Choi approximation is within d eta in trace norm of the true Choi matrix J.

Taking its positive part K gives ||K-J||_1<=2d eta. Let R=Tr_output K. Then ||R-I||_infinity<=2d eta. For eta<1/(4d), R is uniformly bounded away from zero. Conjugating K by I tensor R^(-1/2), with tensor ordering adjusted to the chosen Choi convention, yields an exactly positive Choi matrix with partial trace I.

The correction changes the Choi matrix by O(d^2 eta), conservatively, and hence changes the channel by a dimension-polynomial multiple of eta. Requesting a more accurate initial exponential absorbs this factor.

The ONLY inverse square root is of the marginal R, which has a certified gap near one. Small Choi eigenvalues do not require inverse-eigenvalue postselection or an eigenvector-gap oracle. Positive-matrix square roots have the usual square-root error modulus, so one pays a squared accuracy tolerance in the preceding arithmetic. Certified dense spectral or matrix-square-root arithmetic suffices with polynomial dimension and precision-bit costs.

The repaired Choi matrix defines a dense Stinespring isometry. Approximate classical construction and ordinary unitary synthesis can be budgeted to give a nearby actual unitary circuit, whose induced channel is exactly CPTP. This does not require intermediate scaling/squaring matrices themselves to be CP.

## Consequence and exclusions
Prescribed controls may be inserted between these compiled JOINT system-reservoir channels while retaining the reservoir. The channel construction supports arbitrary reference-entangled inputs; it is not merely a fitted single-state trajectory. Thus dense exponentiation is a valid strong ordinary comparator for modest full dimension.

The costs can be prohibitive when d is exponential in the succinct register description. The statement does not prove that all competing compressed methods enumerate d, nor does it remove acquisition queries or ordinary dense synthesis costs. It establishes that logarithmic microscopic-rate dependence by itself is not a small-system novelty or advantage claim.

No new solver, implementation, practical crossover or literature-priority claim is accepted by this narrow review.
