# Result: finite acquired positive corrections; full target remains open

Constructed and executed a value-only nonlinear Gaussian-mean sampler for **every** globally L-Lipschitz conservative g=grad F, F in C^{1,1}, including nonconvex fields. It uses the legal whole-vector values, Gaussian seeds and arithmetic; no mean, derivative, potential, matrix or conditional-expectation oracle is supplied. This is an intermediate construction, not the requested polylogarithmic capability.

The four-query operation is an unbiased bounded **covariance action** J(v), E[J(v)|v]=Cov(g(G))v and ||J(v)||<=L²||v||. It composes two inherited R22 secant actions at a shared Gaussian heat center, then averages the Brownian time. This covariance formula is proved rather than inferred from moments of numerical samples.

With r=L/sigma, n independent source values, k fresh actions on retained Gaussian Z, and a fresh final Gaussian reserve, the actual positive map

    Y=gbar_n+(sigma/sqrt(2))Z-Jbar(Z)/(sqrt(2)sigma n)
        +(sigma/sqrt(2))W

has exactly preserved mean and the proved full-law bound

    TV(Y,N(Eg(G),sigma²I))
       <= r² sqrt(d)/n^(3/2)+r⁴ sqrt(d)/(2n²)+r⁴ d/(2n²k).

Its query cap is **n+4k on every execution**, with O((n+k)d) arithmetic and O(d) streaming storage. An explicit deterministic schedule gives O_r(d^(1/3)epsilon^(-2/3)) queries. THEOREM.md gives the complete law argument, including nonlinear-action randomization, weak C^{1,1} regularity and exact-real/rounded-target scope.

A stronger ordinary variant stratifies action times. It keeps the same general bound and query cap. Its covariance integrand is Loewner monotone, giving a dimension-independent pathwise time-quadrature bound L²/k. On the sine family, shared-time variance falls from O(k^-1) to O(k^-3); at k=8 the exact variance reduction is 48.57. This is not a TV or runtime speedup factor.

A second executed correction uses fresh eight-query Sigma² words. It cancels the deterministic covariance-squared residual, has cap n+4k+8ell, and has a proved implemented full-law remainder (SECOND_ORDER.md). The first-action randomization and averaged Stein fluctuation remain, so its general dimension exponent does not improve.

The failure analysis is discriminating. For the genuine smooth conservative family g_i(x)=sin(x_i):

- The independent-time first correction has TV error tending to one whenever n+4k=o(d^(1/3)); this matches its upper exponent at fixed accuracy.
- The stratified first correction has TV error tending to one whenever n+4k=o(d^(1/4)). Its proved general upper exponent remains 1/3, so a gap remains for this variant.

These are lower bounds for the exact specified first-correction architectures, not for N687 or all value-query algorithms. They use an actual-law shell coupling, not covariance alone. They do not cover the second correction.

Execution evidence includes pathwise affine-action errors below 1.3e-14; a noncommuting-Hessian covariance-action check with all nine entries within 0.624 estimated standard errors; exact affine query counts and covariance formulas; same-query ordinary-average/first-correction comparisons; and actual high-dimensional secant shell tests. At d=262144,n=8,k=1, candidate/target shell-event frequencies were 0.6445/0.0391 over 256 runs. Numerical frequencies and moments are diagnostics; the proofs provide the full-law claims. All scripts, seeds and data are retained.

The ordinary independent-average baseline has sufficient O_r(sqrt(d)/epsilon) queries. The frozen R16 arbitrary-fixed-positive-exponent proof candidate is asymptotically stronger in d under its recorded audit status; cloud/FORS competitors retain their actual contracts. Thus this is not a best-known asymptotic compiler or a demonstrated practical speedup. Equal-query first correction remains competitive with the second correction in the executed example. Test families with analytically easy means cannot establish oracle advantage over all family-specific methods.

The main worker chose the mechanism, constructed the sampler/code and integrated the proofs. One same-settings helper independently reconstructed the law bound, supplied the first shell counterexample, and audited the strengthened stratification and second correction. No grandchildren were used. Inherited secant actions, Brownian covariance, Stein smoothing, binomial expansion and stratification are prior capital/standard methods. Priority of this assembly and the restricted obstructions is UNKNOWN; no external novelty search was performed.

The hardest remaining obligation is an acquired **positive reusable full-law update** that removes or squares the implemented randomization and source-dependent Stein defect with constant branching or a genuinely subcritical capped forest. The current corrected output has not been given a fresh conservative Lipschitz source contract; iterating this theorem on it would be unjustified. More binomial terms alone do not remove the first randomization term. This is the precise next attack, while the requested poly(log d,log(1/epsilon)) query target remains NOT_ACHIEVED.
