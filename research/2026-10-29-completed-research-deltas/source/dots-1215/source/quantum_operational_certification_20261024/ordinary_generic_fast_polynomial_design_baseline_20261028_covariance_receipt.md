# Independent receiving audit: generic fast polynomial-design baseline

**RECEIVED, with the stated k^6 dimension price and paid retained-frame contract.** 28 October 2026.

Source: `ordinary_generic_fast_polynomial_design_baseline_20261028.md`, SHA-256
`74e7ff7ee4a02b2b7096602cecc7eec6583aa34e318cebfe66d558b396bb0f84`.

This is an independent mathematical review of the full construction, supplemented by physical-action covariance and finite-conditioning checks distinct from the author's design simulations. No source correction was requested by this reviewer. The separately received frame/compiler, finite full-decoder SDP and known-channel synthesis are imports, not newly implemented here.

## 1. Explicit conditioning and the apparent circularity

The decoder anchors are feasible and affinely spanning. For m=d_C their uniform covariance has lower eigenvalue at least1/(33m^2): if y_j=z_0+z_j/4, then ||z||^2<=33m[z_0^2+sum y_j^2]. The ten encoder anchors are explicitly invertible; their stated1/4000 covariance bound is conservative. Dividing by u<=19 and taking the product design therefore proves the source's lambda_* lower bound without a source-state condition number.

Put R=(B^2/tau)/lambda_*. Every covariance is at most(B^2/tau)I. Before at most T_max updates, retained initial mass gives

    V >= lambda_*(1-1/D)^T_max I.

Since T_max<=D log_2 R+2 and(1-1/D)^D>=1/4, this is at least lambda_*/(4R^2), stronger than the displayed lambda_*/(4R^4). The oracle is therefore justified inductively throughout all potentially reachable iterations. Each certified update then multiplies the determinant by more than2, so the determinant cap prohibits an additional iteration beyond the declared horizon. This is not a circular assumption that the algorithm first terminates and therefore its earlier oracle was valid.

LDL pivots lie between lambda_low and Lambda. Moreover r_i V r_i^T=d_i gives ||r_i||^2<=Lambda/lambda_low, so the chosen M is conservative. Consequently both the z interval and the reciprocal mesh have polynomial MAGNITUDE in k and1/tau, not merely polynomial bit descriptions of exponentially many grid points. Fixing x,z makes the fractional-quadratic variational bracket affine in C. A feasible decoder SDP lower witness, with the stated finite gap/rounding budget, therefore certifies the leverage update or the10D^2 stop bound. No decoder net is hidden in this oracle.

## 2. Stratified covariance, coordinate medians and all-action coverage

For n_i=ceil(n pi_i), exact independent bit variances give

    Cov(theta_batch)
      <=V^-1 [sum_i pi_i a_i a_i^T/u_i] V^-1/n
      =V^-1/n.

This holds conditionally on the prior good history at each fixed mathematical common frame U. It does not assume fresh independent physical frames. The whitening phi=L^T theta has coordinate variances at most1/(n d_i). Median amplification across independent batches is valid coordinatewise even though coordinates within a batch are correlated. The simultaneous coordinate event implies

    (theta_med-theta)^T V(theta_med-theta)<=16D/n.

Combining this with the leverage bound proves uniform prediction error over ALL continuous decoders in K_s and all listed encoders. The median need not be unbiased. Subsequent rational rounding contributes at most tau/64, and hence the stated1/16 sqrt(tau u) radius is valid. Every support ceiling is counted.

## 3. Affine envelope and finite first-failure argument

The update u_new=2qhat+2tau remains affine, which is essential for the SDP oracle. With c=1/16,

    3c^2+2c sqrt(32)=0.718825531...<3/4.

Thus on the prior good event the proposed envelope is bounded below by q+1.281...tau and above by3q+2.719...tau. The declared range checks have ample strict slack. On a bad history they may abort; if they accept, positivity and the global bound19 still suffice for the finite design/arithmetic caps. The statistical statement uses conditional first failure, not an unsupported assumption that q<=u on every possible history. Rounding envelope coefficients at every stage prevents uncontrolled recursive bit growth.

The SDP body has a supplied strict center and all new decoders are rounded inward. Known row/feature bounds, the covariance eigenvalue floor and the finite objective coefficients suffice for polynomial precision. This review does not infer polynomial runtime merely from an abstract exact-real optimization oracle.

## 4. Selection and operational comparator

The clipped square root is used only in the selection proof, not to alter the affine design weights. A tau-optimal final affine minimization adds at most sqrt(tau), giving sqrt(q_selected)<=sqrt(q_*)+5sqrt(tau). Young's inequality gives the stated relative/additive bound. The original full-CPTP comparator is recovered by the explicitly paid interior mixture and encoder net; fixed-decoder quadratic stationarity, rather than smoothness of the optimized risk, justifies the net debit.

At s,h^2<=epsilon/256 and tau<=gamma epsilon/2^15, the computed ideal additive coefficient is below0.020371epsilon, hence belowepsilon/16. The bad-history beta and whole interactive control/frame/payload loss debit fit comfortably within the claimed expected Bell-loss budget. Only the expected one-payload statement is received; no posterior guarantee for every exposed learner record or free reset/reuse of the frame follows.

With D=10(3k^2+1), L_*=10D^2 and n=O(D L_*/tau), the charged pilot cap is O_tilde(k^6/(gamma epsilon)). The polynomial scalar grid may have very large fixed exponents and constants, but its size is polynomial. The separately received explicit online compiler is paid in the FULL horizon, k, log ambient dimension and precision, including growing memory and all adaptive known-decoder controls. The construction is available equally to the strongest informed conventional learner.

## 5. Independent evidence and received boundary

The companion check uses actual physical decoder anchors and quaternion-unitary/replacer source families. It verifies24 additional physical feature identities, six full stratified covariance matrices and their LDL-whitened bounds,20 closed determinant/conditioning cases,12 exact binomial median tails and the envelope/comparator constants. The maximal physical feature residual is3.34e-16; the largest observed normalized covariance eigenvalue is0.291<1. These are finite algebra/conditioning diagnostics, not execution of the enormous conservative source cap, a full SDP software implementation, a fresh compiler proof or hardware.

This receives a GENERIC ordinary-input inverse-accuracy learner with polynomial processing at a k^6 dimension rate. It does NOT receive the desired k^2 rate, practical speedup, new quantum advantage, learned positive Choi completion, or a free unknown-source optimization oracle. The older k^4/exponential-menu baseline and the new k^6/polynomial-processing baseline have different resource tradeoffs; neither should be mislabeled as the rank-squared target.
