# Addendum: information per actual death probability

24 October 2026. Adversarial check of the proposed actual-death refinement. This is an addendum to `INFORMATION_FRONTIER_AUDIT.md`; it uses no simulations.

## Adaptive and stopped-law derivation

Under a reference parameter θ, let `J_i` indicate that attempt (i) is reached and made, `B_i` indicate that this exposure survives, and `p_i=exp(-kappa a_i^s)`. The amplitude is predictable at the time of attempt. Conditional on the pre-exposure history and (a_i), survival is independent of θ and the Gaussian noise. Hence

`E_theta[J_i B_i a_i^s] = E_theta[J_i p_i a_i^s]`.

Since (x e^{-x}\le 1-e^{-x}) for (x\ge0),

`kappa E_theta[J_i B_i a_i^s] <= E_theta[J_i(1-p_i)]`.

The latter expectation is exactly the probability that death occurs at attempt (i). These events are disjoint, so summing over all attempts gives

`E_theta[sum_i J_i B_i a_i^s] <= rho_theta/kappa`,

where `rho_theta=P_theta(death)`. This remains valid for adaptive actions and stopping: each summand is conditioned only on the pre-attempt history, and monotone convergence handles an unbounded stopping time when the sums are finite. A fatal exposure is included in the death event but has `B_i=0`, so it contributes risk and no Gaussian information.

Let (q=2r/s). If (s>2r), then (q<1); apply Holder to the probability-times-successful-attempt measure, whose total mass is `E_theta[C]` for (C=\sum_i J_iB_i):

`E_theta[E_obs] <= min{ E_theta[C],
                         (E_theta[C])^(1-q) (rho_theta/kappa)^q }`,

where `E_obs=sum_i J_i B_i a_i^(2r)`. If `s<=2r`, `a^(2r)<=a^s` and `E_theta[E_obs]<=rho_theta/kappa`. These are reference-law inequalities; a uniform risk guarantee requires substituting `sup_theta rho_theta` (or another uniform upper bound), because adaptive readouts can make the action distribution, and thus death probability, depend on theta.

The full stopped-law KL identity from the prior audit is exactly

`KL(P_theta || P_theta') = ((theta-theta')^2/(2 sigma^2)) E_theta[E_obs]`.

Thus the death-based information frontier is valid for arbitrary adaptive controls and data-dependent stopping, with no survivor-conditioned Gaussian approximation. If a two-point confidence test requires expected observed information `E_need=2 sigma^2 kl(1-alpha||alpha)/Delta^2`, then for (s>2r)

`E_theta[C] >= E_need^(1/(1-q)) (kappa/rho_theta)^(q/(1-q))`.

Attempt count (M) equals (C) plus at most one fatal attempt, so `E[M]=E[C]+rho_theta` under this interface. A cap on expected or pathwise attempts therefore yields the same `epsilon^(-2s/(s-2r))` duration exponent. For (s\le2r), fixed `rho_theta` caps observed information and blocks arbitrarily precise estimation. This strengthens the earlier hazard-sum formulation by expressing the budget directly in actual fatal probability.

## Constant-amplitude check and notation distinction

For a fixed amplitude (a), write (h=\kappa a^s), (p=e^{-h}), and run for at most (N) attempts. Then

`rho = 1-p^N`, `E[C] = p rho/(1-p)`,

`E[sum_i J_i B_i a_i^s] = (rho/kappa) h/(e^h-1)`,

`E[E_obs] = rho kappa^(-q) h^q/(e^h-1)`.

The expression `(rho/kappa) h/(e^h-1)` is the expected *successful hazard-dose sum* `sum B_i a_i^s`, not the Gaussian information dose unless (s=2r). As `h` tends to zero, successful hazard dose tends to `rho/kappa`. For (s>2r), information dose instead scales as `rho kappa^(-q) h^(q-1)` and grows as the control gets weaker, at the cost of a diverging number of attempts. This distinction prevents an ambiguous “dose saturation” phrase from being mistaken for information saturation.

For a completion-and-confidence guarantee (1-\delta), constant amplitude gives exact joint success `(1-rho)(1-alpha)`. Choose `alpha<delta` and `rho=(delta-alpha)/(1-alpha)`, so the joint success is exactly `1-delta`; equivalently the planned hazard is `h_plan=-log(1-rho)=log((1-alpha)/(1-delta))`. Substituting this (h_{plan}) for (h) in the prior duration formula gives the same exact confidence and duration scaling, while charging directly in death probability.

## Finite control limits under the death budget

If every nonzero amplitude is at least (a_*>0), then for (s>2r),

`E_theta[E_obs] <= rho_theta/(kappa a_*^(s-2r))`.

For (s\le2r), the ceiling is already `rho_theta/kappa`. Thus the actual-death formulation does not remove the finite-resolution obstruction. If the augmented contract has a per-attempt fatality floor (q_0>0), then

`rho_theta = sum_i E_theta[J_i(1-p_i)] >= q_0 E_theta[M]`,

so `E_theta[E_obs] <= E_theta[C] <= rho_theta/q_0`. A fixed death-probability cap then bounds the number of useful readings as well as information.

## Design boundary

The expected-death inequality and Holder bound hold conditionally after every history, so adaptively selecting amplitudes cannot evade the order frontier. For (s>2r), equal (a_i^s) remains the Holder-optimal allocation at fixed successful-count budget and successful hazard dose; the constant-amplitude policy has the matching small-(h) behavior at fixed ρ. A competent finite-sample design should still optimize the exact censored likelihood, completion probability, control/readout costs, and the required uniform risk criterion. No dominance claim follows from matching this frontier.
