# Limited comparison with existing machinery

This is a scoped primary-source comparison, not exhaustive priority clearance.

The operator distribution with transform \(e^{iA(t)}\), its interpretation through all linear marginals, Weyl-ordered moments, compact support, and Gaussian convolution as a plotting regularization are established ingredients in [Schwonnek and Werner, The Wigner distribution of n arbitrary observables](https://arxiv.org/html/1802.08342), Sections II.2-II.4 and III.1. The endpoint proofs inherit those ingredients. Their all-space scalar-convolution positivity estimate is an additional argument; it does not follow from plotting a smoothed function. Anderson's older calculus is a further antecedent, [The Weyl functional calculus](https://doi.org/10.1016/0022-1236(69)90013-5). The full 1969 article was not acquired here.

The appendix of [Pomatto, Strack and Tamuz, Stochastic Dominance Under Independent Noise](https://www.its.caltech.edu/~lpomatto/stochastic_dominance.pdf) states and proves a result attributed to Ruzsa-Szekely and Mattner: a scalar signed probability-mass-one measure can be convolved to positivity while preserving any prescribed finite moment order, or all ordinary moments. Its proof includes a geometric convolution series. [Mattner's author-hosted paper](https://www.math.uni-trier.de/~mattner/Papers/cumu2FinalVersion.pdf), Section 3.1, also discusses characteristic-function quotients and these antecedents.

The distinction needed here can be checked directly. For
\[
 \tau=(1-c)\sum_{k\ge0}c^k\pi^{*k},\qquad0<c<1,
\]
its moment-generating series is
\[
 m_\tau(g)=(1-c)\sum_{k\ge0}\bigl(c\,m_\pi(g)\bigr)^k.
\]
It diverges whenever \(c\,m_\pi(g)\ge1\). For a nontrivial scalar probability measure \(\pi\), some tilt direction eventually has this property. Preserving all ordinary moments by this geometric construction therefore does not yield the all-exponential radial-tail theorem. This observation is an elementary calculation, not a claim that all prior convolution methods have been excluded.

The endpoint proof's specific improvement over the supplied manuscript is the exact evaluation of analytic remainder coefficients followed by two endpoint simplex integrations in Duhamel's formula. The sharp constant-offset addendum additionally keeps the quadratic term, exploits commutation in the radial direction, and uses the full transverse Clifford moment block for necessity. Those precise statements require their own historical search before any novelty claim.
