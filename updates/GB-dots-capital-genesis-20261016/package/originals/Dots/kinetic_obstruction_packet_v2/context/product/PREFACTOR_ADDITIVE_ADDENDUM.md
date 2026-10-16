# Audit of static exponential-prefactor and additive-drift extensions

Both additional obstructions are valid under their stated static, flat-low assumptions. This is a separate addendum; it does not alter the earlier proofs. `check_prefactor.py` independently reconstructs the mean-exit functions by exact rational shooting recurrences, unlike the constructor's tridiagonal elimination. Its execution receipt is `prefactor_result.json`.

## Static exponential prefactor

For g(t,n)=exp(lambda(1-t))*product_i h_i(n_i), lambda>=0 and h_i(k)=1 at k<=15, the native target boundary is exp(lambda(1-t)). At a sparse state, division by this positive prefactor gives (L_d-lambda)h_i<=0, with scalar boundary h_i(15)=1 and killed overflow h_i(163)=0. A globally supercaloric envelope therefore satisfies that STATIC generator inequality.

If the target payoff is instead overwritten to one, the same inequality follows by taking t upwards to one. At sparse count 16, the target contribution after division is exp(-lambda(1-t)), which converges to one. Other rows already have the ordinary static form. This limiting argument is legitimate because the shape is fixed and all finite rates and factors are finite; no arbitrary time-dependent factor version follows.

For sigma the scalar first exit to 15 or 163, discounted optional sampling gives

    h_i(50) >= E[e^(-lambda sigma) 1{lower exit}].

Indeed, apply the generator inequality to e^(-lambda(t wedge sigma))h_i(Y_(t wedge sigma)); discard the nonnegative unfinished-path term and let t grow. This uses a static necessary inequality valid for arbitrary stopping durations. It is NOT a substitution of eventual hitting probability for the original deadline-one probability.

Writing P_d=P(lower exit) and m_d=E[sigma|lower exit], conditional Jensen gives

    h_i(50) >= P_d exp(-lambda m_d).

Thus g(0,(50,...,50)) >= P_2^4 P_3^4 exp(lambda(1-4m_2-4m_3)).

The independent script checks both endpoint values zero, all 294 positive interior values and all 294 exact equations L_d T_d=-1. Finite-state stopped Dynkin identifies T_d with E sigma: positivity first bounds E(sigma wedge t), proving integrability; boundedness of T and almost-sure exit then permits passage to the limit. The verified values satisfy

    T_2(50)=0.0969567304267... <1/10,
    T_3(50)=0.0586348291312... <3/50.

The script separately reconstructs the exact scale ratios and verifies upper-first-exit probabilities less than 10^-25. Consequently it checks exactly

    4*(1/10)/P_2 + 4*(3/50)/P_3 <13/20,
    P_2^4 P_3^4 >1-8/10^25.

Since m_d<=T_d(50)/P_d, the claimed strict bound follows for every lambda>=0:

    g(0,(50,...,50)) > (1-8*10^-25) exp(7*lambda/20).

At lambda=0 strictness comes from the probability-product bound; for positive lambda both exponent and product bounds apply. The finite-deadline envelope requirement has not been weakened.

## Static additive drift repair

For a positive static flat-low product V, killed at overflow, suppose QV<=K with K>=0 on all continuation states. Sparse reduction gives L_d h_i<=K. Stopping at sigma wedge 1 yields

    q_d <= E[h_i(Y_(sigma wedge 1))] <= h_i(50)+K.

Here the first inequality follows because successful exit contributes one and all other contributions are nonnegative. The expected time charge is at most K. Thus, with q=999995/1000000 strictly below both previously certified q_d,

    V(50,...,50)+K >= K+max(q-K,0)^8.

For K>=q, this exceeds .34. For K<q, put x=q-K. Convexity of x^8, or Young's inequality, gives for r=3/4

    x <= 7r/8 + x^8/(8r^7) <= 21/32+x^8,

because the exact rational 8r^7 is greater than one. Therefore the bound is at least q-21/32=0.343745>0.34. The independent script checks these rational comparisons. This is a lower bound on the standard candidate certificate V(initial)+K, not a probability lower bound.

## Scope

These results exclude static flat-low shape repairs of the two specified forms. They do not exclude genuinely time-dependent slack factors, non-flat low factors under slack, pair/cluster factors, sums of products, or tensor trains. The static prefactor theorem also covers target overwrite to one; this does not generalize to every boundary-overridden product. No useful compressed interior probability certificate or algorithmic advantage has been acquired. Prior source-pin limitations remain as recorded in `AUDIT.md`.
