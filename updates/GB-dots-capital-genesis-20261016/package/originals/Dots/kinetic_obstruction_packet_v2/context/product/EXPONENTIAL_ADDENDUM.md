# Stronger obstruction: independently certified initial value >0.99998

This addendum supplements and preserves `AUDIT.md` and its independent >0.26 proof. All actual-instance definitions, retained counts 0 through 162, first overflow at 163, and sparse-state reduction remain unchanged.

## Verdict and independent computation

The strengthened claim is valid. For each degree d in {2,3}, positive functions H_d on {15,...,163} solve exactly

    b(n)[H_d(n+1)-H_d(n)]
      + mu_d(n)[H_d(n-1)-H_d(n)] + 15 H_d(n) = 0,
      16 <= n <= 162,
    H_d(15)=H_d(163)=1,
    mu_d(n)=a(n)+d*8.2207*n.

The newly written `check_exponential.py` uses exact rational SHOOTING RECURRENCES, rather than the constructor's tridiagonal elimination. Write H(n)=alpha(n)z+beta(n), start H(15)=1 and H(16)=z, propagate the displayed recurrence, then impose H(163)=1. The script checks that the coefficient determining z is nonzero. It independently verifies all 294 equations, both boundary values for each degree, and H_d(n)>1 at all 294 interior entries.

It certifies exactly

    H_2(50)<12,
    H_3(50)<3.

Descriptive values are 11.773731983345723521455717441734063 and 2.7274274632445486652200535514624714. These decimal displays are not certificates.

The shorter exact Taylor certificate independently obtained is

    sum_(k=0)^21 15^k/k!
      = 247222312764106429 / 79867346944
      > 3,000,000.

Since all omitted terms are positive, e^15>3,000,000. No floating exponential or residual tolerance is used.

## Sign, positivity and first-exit proof

Let Y be the same scalar chain and sigma its FIRST exit to either 15 or 163. Both boundary values of H are one. Positivity is crucial for using the equation with +15: existence of an arbitrary signed solution would not certify an exponential moment.

A positive solution must in fact be at least one everywhere. If a global minimum below one occurred at an interior n, then L_d H(n)>=0, while (L_d+15)H(n)>0, contradicting the equation. Interior values equal to the global minimum one are likewise impossible. Our arithmetic directly verifies the stronger H>1 interior condition as well.

For each fixed finite t,

    Z_t = exp(15*(t wedge sigma)) H(Y_(t wedge sigma))

is a true martingale. Its drift vanishes before sigma by the equation and it is constant afterward. On each bounded time interval it is bounded because the state space and H are finite. Thus E_50[Z_1]=H(50). On {sigma>1}, Z_1>=e^15, so DIRECTLY

    P_50(sigma>1) <= H(50)/e^15.

This direct finite-time argument avoids any need to assume exponential integrability in advance. It also shows sigma is almost surely finite by the analogous bound at t -> infinity. Fatou then gives E[e^(15 sigma)]<=H(50), if desired, but that stronger statement is not needed for the certificate.

Consequently

    P_50(sigma>1)<4*10^-6 for d=2,
    P_50(sigma>1)<1*10^-6 for d=3.

The existing independent exact harmonic calculations certify upper-first-exit probability <10^-20 for each degree. Decomposing deadline failure into the deadline exit tail and possible upper-first exit yields

    q_2(1,50)>1-4*10^-6-10^-20,
    q_3(1,50)>1-1*10^-6-10^-20.

These are deadline FIRST-HIT probabilities for the scalar loss-only comparison, not endpoint occupancies or actual eight-site probability lower bounds.

For four vertices of each degree, the prior exact sparse-state argument gives

    v(0,(50,...,50)) >= q_2(1,50)^4 q_3(1,50)^4
      > (1-4*10^-6-10^-20)^4 (1-10^-6-10^-20)^4
      > 49999/50000 = 0.99998.

The last comparison is checked using rational arithmetic. Its left side is approximately 0.9999800001659992599219223970300426930014; its positive margin above 0.99998 is approximately 1.65999259921922e-10. A first-order union bound alone would lose the strict comparison after subtracting overflow; the exact product retains the needed positive higher-order terms.

## Exact-boundary normalization broadens the applicable class

Suppose a positive product g(t,n)=product_i f_i(t,n_i) is defined by that SAME factorization throughout the retained box, including all target states, and g(t,n)=1 for every n with all counts <=15.

Fix t. Set c_i(t)=f_i(t,0). Evaluating at the all-zero state gives product_i c_i(t)=1. Evaluating at a target state with only coordinate i changed from zero to any k<=15, then dividing the two positive products, gives

    f_i(t,k)=c_i(t), every k<=15.

Define w_i(t,k)=f_i(t,k)/c_i(t). Then each w_i equals one at all low counts and product_i w_i=g IDENTICALLY. Differentiating the identity introduces no extra term: sum_i c_i'(t)/c_i(t)=0 follows from product_i c_i=1. The normalized low factors have zero time derivatives. Hence the entire obstruction applies without originally assuming the individual low factor values were one.

An additional positive global time prefactor does not evade this normalization if the resulting globally factorized g still equals one at every target state; it can be absorbed into one factor, and exact boundary normalization cancels it.

What remains outside this theorem:

- Boundary SLACK, where globally factorized g is only >=1 on target, need not normalize without changing g or its supercaloric inequality.
- An envelope defined as a product only on continuation states, with a separately overwritten target boundary, is not globally factorized on the retained box. The sparse-state argument can change at first target entrance, so it needs separate analysis.
- Non-product, pairwise/cluster, sum-of-products and general compressed representations remain unexcluded.

The stronger theorem remains an obstruction to this envelope representation, not a small certified actual hitting probability, efficient interior solve, or rare-event sampling improvement.

## Reproduction and provenance

Run `python check_exponential.py` in this directory; `exponential_result.json` records the successful exact checks. The earlier `check.py` and `result.json` independently certify the sparse-state reduction and overflow estimates used here. The source-pin limitation stated in `AUDIT.md` remains unchanged. This is same-team independent reconstruction, not external review.
