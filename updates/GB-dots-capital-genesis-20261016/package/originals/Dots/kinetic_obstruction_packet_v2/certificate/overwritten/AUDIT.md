# Independent exact audit: static products with target overwritten to one

## Verdict

**PASS.** A NEW certificate, separate from the native-boundary dual, excludes all positive static product shapes with a single exponential time prefactor and fixed success payoff one:

    g(t,n)=exp(lambda(1-t))*product_i h_i(n_i) on continuation states;
    g(t,target)=1; g(t,overflow)=0.

The factors may be arbitrary positive 163-entry profiles at each site. There are no low-count restrictions, interpolation assumptions, factor bounds, or gauge assumptions. Every all-state backward supercaloric envelope in this class satisfies

    g(0,(50,...,50)) > 1-3*10^-22.

The direct dual proof uses lambda>=0. The negative-lambda reduction below extends the conclusion to any real lambda. No claim is made here about arbitrary time multipliers or genuinely time-dependent factor shapes.

This floor concerns candidate UPPER ENVELOPES, not the actual eight-site hitting probability.

## Independent reconstruction and exact results

Input certificate:

    certificate/overwritten/overwritten_product_exact_dual.json
    SHA256 a25a198fc0b699cbf8663daae13c8ecfe73eb1c45964fab44c43aedfdee32ce7

Independent audit files:

    certificate/overwritten/check.py
    certificate/overwritten/result.json

Replay with Python using the checker path above. The standard-library-only verifier directly enumerates actual reactions and diffusion on the geometrically reconstructed open 2-by-4 grid. It reads exact rational weights, not rounded optimizer output, and never executes producer code.

It verifies 325 distinct retained continuation states with positive rational weights. Two rows have target-entering jumps and two have overflow jumps. It checks all 326 orbit-coordinate identities exactly, then expands every row under the four explicitly verified grid automorphisms and independently checks all 1304 arbitrary-site-coordinate identities. All surviving coefficients are zero. This directly removes any need to assume orbit-symmetric factors.

The independently recomputed mass and overflow charge satisfy

    M = 0.722721676961630673402302497137396302625511345... <1,
    K = 2.66677749549462170665434730972405083475784117...e-22
      <3/10^22.

These inequalities and the matching producer fraction strings are verified exactly; decimals are descriptive only.

## The changed target row is essential

Let Phi(x)=sum_i log h_i(x_i). At t approaching the deadline one, the target-entry ratio tends to exp(-Phi(x)), because the target payoff is fixed at one. Accordingly define

    qhat_x(phi)
      = sum_{x->y continuation} rate(x,y)[Phi(y)-Phi(x)]
          - sum_{x->target} rate(x,target)*Phi(x).

Overflow transitions contribute ZERO derivative and the constant negative killing rate -k(x). The checker implements these three cases separately. In particular it does NOT reuse the native row Phi(target)-Phi(x).

Taking t upwards to one in the finite-state supercaloric inequality is valid for fixed finite profiles and a single finite lambda. Then exp(z)>=1+z yields

    qhat_x(phi)-lambda <= k(x).

The exact expanded dual identity is

    sum_i phi_i(50)+sum_x pi_x qhat_x(phi)=0.

Multiplication of the necessary inequalities by positive pi_x and summation gives

    log g(0,(50,...,50))
      =sum_i phi_i(50)+lambda
      >=(1-M)lambda-K.

For lambda>=0, M<1 makes this at least -K. The strict rational K<3*10^-22 and exp(z)>=1+z give the claimed strict floor. No boundary log value remains, so no hidden low-factor sign condition is required.

## Negative-lambda reduction

If lambda<0, define a new static shape V'(n)=exp(lambda)V(n), distributing the constant scaling into any one factor (or equally into all eight), and set lambda'=0. Keep target payoff one and overflow payoff zero. Then the new initial value equals the old initial value.

For every continuation state, the new generator ratio equals the old generator ratio at t=0: continuation-to-continuation ratios are unchanged, the fixed-target ratio becomes exp(-lambda)/V(x), and overflow remains zero. The old t=0 supercaloric inequality implies this ratio is <=lambda<0. Thus the new lambda'=0 function is itself a valid static supercaloric upper envelope with the same initial value. If the original inequality is stated only for t>0, continuity gives the same limiting conclusion. Terminal positivity and the fixed target boundary remain valid.

The lambda>=0 obstruction therefore applies to this transformed envelope, proving the same floor for the original negative-lambda candidate. This uses only a SINGLE exponential time prefactor and static shapes; it is not an assertion about arbitrary time dependence.

## Scope and relation to earlier results

This certificate closes the static target-overwrite escape left open by the prior native-product certificate. It does so with different rows and a different exact identity. The earlier native audit's limitation was correct and has not been silently removed from that proof.

The result covers arbitrary static site factors, including non-flat low profiles and unrestricted logarithmic magnitudes. It does not exclude time-dependent local factor shapes, pair/cluster factors, sums of products, tensor trains or other non-product representations. The actual rare probability and an affordable certified interior solve remain unacquired.

This is a finite exact certificate on the actual supplied eight-site benchmark, with same-team independent reconstruction. It is not external review, historical priority clearance, or evidence of algorithmic advantage.
