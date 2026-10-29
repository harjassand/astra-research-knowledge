# Whole review of conditional all-cold clock preparation

29 October 2026. Root independently read ALL_COLD.md, SCALED_LOCALITY.md,
FLOW_CIRCUIT.md and the vacuum-CP martingale in the frozen clock-stability
proof. The theorem is accepted at its stated ideal mathematical circuit
scope. This review is additional to the earlier polynomial-window review;
it does not change that frozen result.

The decisive checks were:

* The KMS similarity cancels its imaginary-time loss/coherent coefficients
  exactly to sech(t ad_K/4). Its positive time-average representation
  preserves the acquired form comparison between K and the defect count.
  Thus the baseline is uniformly coercive in the number of doubled-cell
  defects, rather than merely globally gapped.
* Negative-band filtering annihilates the true vacuum exactly. The fixed
  filter has an O(lambda) local difference from bare lowering operators,
  so vacuum-CP localization supplies G_minus comparable to N without a
  t lambda remainder. Both non-number-conserving terms and excited-clock
  sectors remain present.
* The spectral-flow bootstrap uses the stronger defect-count hypothesis.
  Its globally vacuum-annihilating difference admits the dimension-free
  CP martingale decomposition; polynomial ball-volume sums pay its form
  bound. It is not the false assertion that every uniformly gapped
  Hamiltonian is stable to arbitrary local perturbations.
* The scaled shell bookkeeping supplies a convolution constant independent
  of the scale, polynomial pair-norm/LR bounds, fixed moment orders and
  clipped real-time filtering. The separate parameter-flow velocity is
  small by an explicit additional epsilon times polynomial gate. Hence
  no exp(poly(t)) is hidden behind a locality constant. Exponential heating
  suppression beats these fixed polynomials for every real t above a
  computable threshold, not just on a finite grid.
* FLOW_CIRCUIT pays the native gapped-path spectral flow in operator norm
  through finite scalar quadrature, known-term LCU, native evolutions and
  path discretization. The bootstrap parent flow is proof-only. No parent
  ground-state, Gibbs-state or many-body eigenvalue oracle is implemented.
  The condition-number prefactor is logarithmically absorbed into the
  O(nt+log(1/epsilon)) update time, not left in an exponential runtime.

Accepted consequence: for a single sufficiently small fixed admitted
coupling and every t >= T0, the known-sign conditional FULL clock Gibbs
state has a polynomial(n,t,1/epsilon) coherent preparation circuit and
parent gap at least 1/16. The lambda_prod/T0 constants are not numerically
qualified for the literal native recipe. No actual quantum state was
prepared in this review. The correct source-syndrome marginal remains a
separate acquired operation. A finite-range autonomous reservoir, unknown
controller errors, practical advantage and historical novelty are not
consequences of this acceptance.

Reviewed packet's frozen ALL_COLD SHA256:
279489efa7940ebc4e9d55f6cec09320cb8bf12fb421332b892475755ab6cbe5.
