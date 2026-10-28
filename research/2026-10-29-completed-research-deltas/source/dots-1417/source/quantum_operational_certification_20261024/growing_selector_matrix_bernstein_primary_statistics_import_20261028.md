# Independent primary import: bounded matrix Bernstein for actual selector records

28 October 2026. **PASS.** No source calls, sampled outcomes, RNG draws or changes to received artifacts.

## Primary theorem actually inspected

I independently retrieved and read [Joel A. Tropp, *User-friendly tail bounds for sums of random matrices*, arXiv:1004.4389v6](https://arxiv.org/pdf/1004.4389v6), Theorem6.1(ii), printed pages21--22 (PDF pages20--21). The theorem requires independent self-adjoint summands X_k, zero means and an almost-sure upper-eigenvalue bound R. Its variance parameter is the norm of sum_k E X_k^2. For t>=0 it bounds the largest-eigenvalue tail by

    d exp[-t^2/(2 sigma^2+(2/3)R t)].

An operator-norm bound requires applying this result to BOTH X_k and -X_k. The primary text explicitly warns that the two one-sided R parameters need not coincide; here one common norm bound supplies both. No martingale or heavy-tail extension is invoked. The versioned PDF text and formula were inspected; the web screenshot tool reported that PDF screenshots were unsupported, so no visual-page inspection is claimed.

## Application derived for the actual ordinary estimator

Use the frozen base's canonical rational BINOMIAL C, actual input x=Cz/||Cz||, one Bernoulli y, and recorded Y=y s T with s=||Cz||^2. Conditional on a good PREVIOUS history, F=E Y=CAC lies in[0,I], s<=1/tau, and within the batch all source resets/design choices are independent. Set

    S_m=m^2(m+3)/4, R_m=m(m+1), 0<tau<=1.

For every z, T(z)^2 is positive. Since0<=s(z^T Fz)<=1/tau,

    E Y^2=E[s(z^T Fz)T(z)^2]
          <=(1/tau)E T(z)^2=(S_m/tau)I.

No commutation between F and T is used. Centering gives

    0<=E(Y-F)^2=E Y^2-F^2<=(S_m/tau)I.

Also ||T||=m(m+1)/2 and ||F||<=1, so

    ||Y-F||<=m(m+1)/(2tau)+1<=R_m/tau.

The last inequality uses tau<=1 and m>=1. For N observations, the primary theorem has dimension d=m, variance at most N S_m/tau, bound R_m/tau and threshold N delta. Applying both signs and summing their tail bounds gives

    Pr(||Fhat-F||>delta)
      <=2m exp[-N delta^2/(2S_m/tau+(2/3)R_m delta/tau)].

Thus the dimension advantage comes from the matrix operator variance of this SAME acquired Y, not from replacing its physical observations by an oracle.

For at most H estimates, define P_m=2S_m+R_m and

    L=ceil log2(4mH/beta),
    N=ceil[P_m L/(tau delta^2)], 0<delta<=1.

The denominator coefficient is at most P_m, so the exponent is at least L. Since e>2, each failure is at most2m*2^(-L)<=beta/(2H). This is valid conditionally on each pre-batch good history. A first-failure union over adaptive stages costs at most beta/2; it does not require unconditional independence of envelopes. The rational sample mean replaces the base medoid only in the separate refinement, not retrospectively in the frozen base.

Finite synthesis and capped random-sampler deviations remain in the one whole-process operational discrepancy. They are not uncharged biases in the ideal mean identity. Failure histories retain a fixed resource cap and a safe physical fallback.

## Scope and independent deterministic support

`growing_selector_matrix_bernstein_statistics_check_20261028.py/.json` separately checks exact canonical-C operator variance, both-sign centered norm bounds and rational stage/cap arithmetic. Its prescribed finite matrix cases are not source samples and do not prove Tropp's theorem. This primary import is independent of the forthcoming full-refinement main/statistics receipts, avoiding a dependency cycle.
