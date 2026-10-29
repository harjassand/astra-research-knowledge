# Faster bounded sign filter, without a source spectral-gap promise

28 October2026. Independently checked analytic variant. This adds an asymptotically faster standard-polynomial option; it does not supersede the explicit positive binomial filter or supply missing frame/block access.

Let alpha>=max(1,||M||),0<epsilon<1/2, and delta=1/(2alpha). Take a bounded real odd polynomial f with|f(x)|<=1 for|x|<=1 and|f(x)−1|<=epsilon on[delta,1]. No positivity of f on[0,delta] is required. Use the same success contraction and total failure-completed decoder as in the independently received governing lemma.

For0<=sigma<=1/2,

    1+sigma²−2sigma f(sigma/alpha)
      <=(1+sigma)²
      <=4(sigma²−1)².

The last inequality follows from1/(1−sigma)²<=4, including sigma=0. For1/2<=sigma<=alpha, approximation to1 gives

    1+sigma²−2sigma f(sigma/alpha)
      <=(sigma−1)²+2alpha epsilon
      <=(4/9)(sigma²−1)²+2alpha epsilon.

Functional calculus followed by positive weighted trace therefore yields

    1−F_e(D_f E_S) <= min(1,4b+2alpha epsilon).

The filter transition at delta is NOT a promise that the source has no smaller singular values. Those values, including exact zero, are paid through b rather than discarded or conditioned away.

Primary existence/construction: Gilyén et al., arXiv:1806.01838v1, Lemma25 (printed p26) states an efficiently computable bounded real odd sign approximant of degree O(delta^(−1) log(1/epsilon)); its stated domain[-2,2] includes the interval needed here. Therefore q=O(alpha log(1/epsilon)) suffices. Source: https://arxiv.org/pdf/1806.01838v1 . The same Corollary18 real-polynomial normalization and finite-precision caveats in QSVT_INTERFACE_ADDENDUM_v1.md apply. No particular coefficients or compiled phase sequence for this faster option were executed in this review.

Choosing epsilon proportional to a requested error allowance divided by alpha makes the query degree O(alpha log(alpha/error)). This improves the explicit binomial option's alpha² dependence while changing the defect coefficient from20/9 to4. Efficient polynomial alpha and actual access to M/alpha, inverse and projector controls remain indispensable. Approximate-success-block and full-circuit error allowances remain2tau and xi respectively, as previously proved.
