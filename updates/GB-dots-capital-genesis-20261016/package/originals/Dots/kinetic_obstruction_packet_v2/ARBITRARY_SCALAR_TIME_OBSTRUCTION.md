# Arbitrary common time dependence cannot rescue a static spatial product

This is a further consequence of the exact actual-boundary occupation certificate. It is a bound on a certificate class, NOT a bound on the physical hitting probability. No historical novelty is asserted for the ingredients.

## Statement

On the actual capped eight-site model, let a candidate upper envelope on continuation states be

    g(t,n)=a(t) h(n),   h(n)=product_i h_i(n_i)>0,

with arbitrary static positive site-specific factors, a positive differentiable common scalar a(t) for0<=t<1, a nonnegative finite terminal limit, target payoff exactly1, and overflow payoff0. Require the actual supercaloric inequality at every continuation state and time.

Then its initial value is strictly greater than1/4. The factors may have arbitrary low-count and high-count shapes; the common scalar may have arbitrary permitted time dependence. Genuinely time-varying SPATIAL profiles, pair factors and sums of products remain unexcluded.

The stronger near-one floor for a SINGLE EXPONENTIAL prefactor remains a separate result. Arbitrary scalar schedules have only the weaker floor proved here.

## Exact certificate inputs

Use the expanded actual-state weights from overwritten_product_exact_dual.json, averaged over the four exact graph automorphisms when treating arbitrary site-specific factors. The independent full1304-coordinate identity is

    F(initial)+sum_s pi_s qhat_s(F)=0,

for every additive F(n)=sum_i phi_i(n_i). The total occupation W=sum pi is approximately .72272167696, and the overflow charge K=sum pi_s k_s is below3e-22. The exact comparisons needed here are W<8/11 and K<1/1000.

Let kappa_s be the total target-entry rate. Applying the identity to the constant additive function F=1 proves

    H=sum_s pi_s kappa_s=1.

This target-flux identity must be verified from the actual target-entry rows; it is not inferred from a rounded numerical total.

## Summed differential inequality

Put F=log h and F0=F(initial). Define constants

    A=sum_s pi_s kappa_s exp(-F(s)),
    B=sum_{s->y continuation} pi_s rate(s,y)[exp(F(y)-F(s))-1] -H-K.

Multiplying each supercaloric inequality by pi_s/h(s) and summing gives

    W a'(t)+B a(t)+A <=0.

Integrating with the positive factor exp(Bt/W), and using a(1)>=0, gives

    a(0)>=A integral_0^(1/W) exp(Bu) du.

This formula includes B=0 by its integral form and works for either sign of B. A limiting endpoint argument gives the same conclusion when differentiability is only imposed before the deadline.

## Eliminate all unknown spatial profiles

Write z=sum_s pi_s kappa_s F(s)-F0. Since target-flux weights are nonnegative and sum to1, Jensen gives

    A exp(F0)>=exp(-z).

The exact additive balance and exp(x)>=1+x give B>=z-1-K. The integral is increasing in B. Consequently

    g(0,initial)>= integral_0^(1/W) exp[(u-1)z-u(1+K)] du.

Since W<8/11, the integration domain includes [5/8,11/8]. On that interval the mean of u is1 and its length is3/4. Jensen, or symmetry of the exponential around u=1, therefore gives

    g(0,initial)>=(3/4) exp[-(1+K)].

Finally e<=8/3+(1/24)/(1-1/5)=87/32, and K<1/1000 gives e^K<1000/999. Their product is strictly below3. Thus g(0,initial)>1/4, as claimed.

The more precise integral over a centered interval of half-width1/W-1 would give a stronger constant. It is unnecessary for the operational conclusion: optimizing only a common time multiplier cannot obtain a rare-event upper bound of order1e-8 from static spatial product factors.
