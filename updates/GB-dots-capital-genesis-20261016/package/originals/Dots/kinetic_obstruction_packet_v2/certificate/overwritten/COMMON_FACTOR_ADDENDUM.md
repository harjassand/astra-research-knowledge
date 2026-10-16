# Independent audit: arbitrary common scalar time factor

## Verdict

**PASS, with the strengthened strict floor 1/4.** The SAME exact overwritten-target dual proves that any upper envelope of the form

    g(t,x)=a(t)*V(x),  V(x)=product_i h_i(x_i)>0 on continuation states,
    g(t,target)=1, g(t,overflow)=0,

with arbitrary positive differentiable common scalar a(t), fixed positive site factors, and nonnegative terminal limit a(1), must satisfy

    g(0,(50,...,50)) > 1/4.

Ordinary continuity to the endpoints and sufficient regularity for the pointwise backward inequality are understood; absolute continuity with the inequality almost everywhere also suffices. This is weaker numerically than the near-one floor for a single exponential prefactor, but it covers arbitrary common scalar time dependence. It does NOT cover genuinely time-dependent relative spatial profiles h_i(t,n).

The conclusion also applies to native-boundary envelopes of this form that majorize one on target: overwriting their target values by one only decreases the continuation generator, producing an admissible envelope with the same continuation values and initial value.

## Independent exact checks

The separate `check_common_factor.py` rebuilds all actual jumps from the same frozen overwritten dual input and re-verifies all 326 orbit identities and all 1304 site-specific identities after graph-automorphism expansion. It additionally computes the target-entry flux directly and certifies

    H=sum_x pi_x*kappa(x)=1 exactly;
    0<W=sum_x pi_x<8/11;
    0<K=sum_x pi_x*k(x)<3*10^-22<1/1000.

Here kappa is the total target-entry rate and k is the total overflow rate. This is independent of the shortcut that obtains H=1 by testing the linear coefficient identity on a constant total log function.

Replay:

    python certificate/overwritten/check_common_factor.py

Receipt: `common_factor_result.json`. Input hash remains a25a198fc0b699cbf8663daae13c8ecfe73eb1c45964fab44c43aedfdee32ce7. All comparisons use exact fractions; no new optimization or floating probability estimate is involved.

## Summed differential inequality

Write F(x)=log V(x), F0=F(initial). Use the expanded site-specific weights. Define the finite constants

    A=sum_x pi_x*kappa(x)*exp(-F(x)) >0,
    B=sum_{x->y continuation} pi_x*r(x,y)*(exp(F(y)-F(x))-1)-H-K.

Dividing each supercaloric inequality by V(x), rather than by a(t)V(x), and summing gives exactly

    W*a'(t)+B*a(t)+A <=0.

This correctly retains the target contribution as the CONSTANT A: target payoff is one, not a(t). Overflow contributes -K*a(t). There is no missing target derivative.

Multiplying by exp(B*t/W), integrating to time one, and using a(1)>=0 gives

    a(0) >= (A/W)*integral_0^1 exp(B*t/W) dt
           = A*integral_0^(1/W) exp(B*u) du.

The integrating factor is positive for every sign of B, so no stability sign or exponential-moment assumption is needed. The terminal contribution has nonnegative sign and may be discarded. Equivalently, the integrating-factor expression plus its explicit source integral has nonpositive derivative, which proves the same inequality directly under differentiability.

## Exact balance and Jensen

Let

    T=sum_x pi_x*kappa(x)*F(x), z=T-F0.

The already verified coefficient identity states

    F0 + sum_{continuation jumps} pi_x*r(x,y)*(F(y)-F(x)) - T =0.

Thus the linear continuation increment sum is z. The elementary exp(v)>=1+v bound gives B>=z-1-K. Since H=1, target fluxes pi_x*kappa(x) form a probability distribution, and Jensen gives

    A*exp(F0) >= exp(F0-T)=exp(-z).

Both estimates may be used inside the integral because u>=0. Therefore

    g(0,initial)
      >= integral_0^(1/W) exp[(u-1)z-u(1+K)] du.

No closure of spatial dynamics, factor independence, or actual hitting-probability lower bound has been asserted.

## Uniform lower bound and exact exponential estimate

The verified W<8/11 implies 1/W>11/8. Restrict the positive integral to [5/8,11/8], whose length is 3/4 and whose mean is one. Writing u=1+v and applying Jensen to the symmetric uniform interval gives

    g(0,initial)
      > exp(-(1+K))*integral_(-3/8)^(3/8) exp(v*(z-1-K)) dv
      >= (3/4)*exp(-(1+K)).

The first inequality is strict because the original integration interval includes additional positive-length intervals with positive integrand. The centered Jensen bound holds for EVERY real z.

For the final constant, the exponential power series gives

    e <= sum_(j=0)^3 1/j! + (1/24)/(1-1/5)
      = 87/32.

The remaining factorial tail is bounded geometrically since each successive denominator after 4! is at least five. Also, for 0<=K<1/1000,

    exp(K) <= 1/(1-K) <1000/999.

The checker verifies the rational comparison (87/32)*(1000/999)<3. Hence exp(1+K)<3 and

    g(0,initial) > (3/4)/3 =1/4.

The proof uses the conservative rational floor, not a decimal approximation to the sharper expression.

## Limits

This closes arbitrary COMMON scalar time dependence for a fixed product shape, with fixed success payoff one (and, by decreasing boundary values, native target majorization). Time-dependent local profiles, pair/cluster factors, sums of products and tensor representations remain outside the theorem. The true rare probability, a useful inside majorant and practical solver advantage remain unestablished.
