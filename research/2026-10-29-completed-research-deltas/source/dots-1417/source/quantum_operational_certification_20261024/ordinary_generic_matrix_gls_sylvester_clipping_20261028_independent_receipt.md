# Independent audit of Sylvester transformed clipped matrix GLS

**RECEIVED with the scoped generic O-tilde(k^4/(gamma epsilon)) ordinary-source price, O-tilde(k^2) matrix-bank count, and paid collective-receiver/common-frame contract.** 28 October 2026. No blocking defect was found in the stated mathematical composition or its deterministic source ledger.

This receipt binds `ordinary_generic_matrix_gls_sylvester_clipping_20261028.md`, SHA-256 `9454b204df34d302bf315bfe20afddc6ea5f109a8205bbd20f61b4de22c22c21`. The reviewer did not write or edit that manuscript. The author supplied the proposed mechanism for independent checking; preliminary audit findings were returned before this source-bound review. The local physical query and causal-frame/compiler results are separately received imports, not newly implemented or reproved here.

The checked imports are the received matrix-GLS manuscript `a331566da59a07b7d9b679e4516368866fd38df20e44cff4f87f8496332d52ea`, its cap companion `23a7d41b408007eb11c5616129cb2bc5253ba3bd44e92538659d2382cda3072c`, and the local finite directional-MSE theorem `483a8507c4ca0dfef510c888a2fc755e84b653bcee81a0329830d152b9ed3968`.

## 1 Full second moments give both transformed matrix variances

The GLS transfer must start from the complete real-Hilbert-Schmidt second moment about the true parameter, not just a centered covariance. The imported weighted bias contraction and the corrected zeta restriction give precisely this bound. With E=Y_x-T_x, block leverage then gives E[vec(E)vec(E)^T]<=alpha K(U_x), alpha=101L/n. The nonzero bias remains included throughout the following argument.

If U<=Ubar, K(U)<=K(Ubar) as operators on the real Hermitian space, because their quadratic-form difference is Tr((Ubar-U)O^2)>=0. For a fixed complex vector v, each quantity ||DeltaZ v||^2 or ||DeltaZ* v||^2 is a positive real quadratic form in the Hermitian coefficients of E. Consequently full second-moment domination transfers to both matrix moments. No Gaussian comparison of tails is used.

In the eigenbasis of Ubar, the reference real-Hermitian Gaussian has diagonal variance alpha lambda_i and E|E_ij|^2=alpha(lambda_i+lambda_j)/2. This includes i=j correctly. For B=sqrt(Ubar), independent real-Hermitian coordinates give the exact reference formulas

    E DeltaZ DeltaZ* = diag_i[(alpha/2) sum_j lambda_i/(lambda_i+lambda_j)],
    E DeltaZ* DeltaZ = diag_j[(alpha/2) sum_i lambda_i/(lambda_i+lambda_j)].

Each is at most alpha d I/2. If B=sqrt(Ubar) W for a unitary W, then Z_B=W* Z_sqrt: the first moment matrix is unitarily conjugated and the second unchanged. Thus the manuscript's nonsymmetric rational factor does not lose either bound. This is the substantive dimension improvement over coefficientwise robust aggregation.

The reconstruction is exact: for R=S_Ubar^-1(T), Z=B*R implies BZ+Z*B*=Ubar R+R Ubar=T. Positivity of the Sylvester inverse follows from its exponential-integral representation. Hence 0<=T<=Ubar implies 0<=R<=I/2 and ||Z||<=||B||/2<4. There is no inverse of an unknown state or unknown eigenspace.

## 2 Clipping supplies its own boundedness before concentration

Functional calculus gives -X^2/t<=clip_t(X)-X<=X^2/t and clip_t(X)^2<=X^2. Therefore E X^2<=vI implies clipping bias at most v/t and centered variance at most vI. The variance identity is E(Y-EY)^2=EY^2-(EY)^2; no commutation is required. Since ||Y||<=t, the centered range is at most 2t.

The cited bounded matrix Bernstein inequality was checked in the primary source, [Tropp, Theorem 6.1(ii)](https://tropp.caltech.edu/papers/Tro11-User-Friendly-preprint.pdf). Applying its two signs in dimension 2d gives the manuscript's probability prefactor 4d and the valid deviation sqrt(2vh/b)+4th/(3b). For the factor-two threshold interval, the total clipping-bias-plus-deviation coefficient is at most

    1+sqrt(2)+8/3 < 8.

Thus the published conservative constant 8 is safe. An independent sharper check gives exponent at least (24/19)h at deviation 4sqrt(vh/b), but the receipt does not replace the manuscript's constants or require that sharpening.

The current center is conditioned on before acquiring each fresh collection of whole GLS batches. For D=H(Z_*)-M, ||D||<=delta, the inequality (A+D)^2<=2A^2+2D^2 gives E X^2<=2(sigma^2+delta^2)I. The transformed batch's possible mean error has norm at most sigma by E H(DeltaZ)^2<=sigma^2I. This bias is explicitly added, not mistaken for clipping bias or discarded by centering.

With b=2^16 h, 8sqrt(2)/256<1/16. Thus the ideal next radius is below delta/16+17 sigma_bar/16. Adding the full sigma_bar/4 numerical allowance still lies inside delta/4+2sigma_bar. Fresh independent batches make this conditional calculation legitimate. Dependence among grid predictions from a common batch is harmless: the proof unions over their separate bad events and never asserts independence over x.

## 3 The scale schedule and all projector transfer close

The source choice n=ceil(2^28 dL/eta) gives sigma^2<=101 eta/2^29. Its dyadic sigma_bar satisfies sigma<=sigma_bar<=sqrt(2eta)/2048. Starting at radius 4 and applying delta_new=delta/4+2sigma_bar for ceil((13+floor(j/2))/2) rounds yields delta<=4sigma_bar, with slack.

For any unit v, exact reconstruction then gives

    |v*(T_tilde-T)v| <= 2||B*v|| ||(Zhat-Z_*)v||
                      <= 8 sigma_bar sqrt(v*Ubar v)
                      <= sqrt(eta v*U v)/128.

Entrywise rounding of each Hermitian grid matrix has operator error below eta/128 at the stated mesh. U>=eta I absorbs that absolute rounding error into the looser c=1/16 confidence bound. The event covers every output projector without a projector net.

The predetermined logarithm in h is more conservative than the required natural logarithm. Summing 4d exp(-h) over at most M J t_max conditional first-failure opportunities costs less than beta. Good histories satisfy the radius hypotheses; no claim about later radii after a first failure is needed. All histories retain deterministic operational caps.

## 4 Nonquadratic learned tables do not break GLS or the comparator

Only the physical T_x needs the ten-feature quadratic model. The block covariance V=sum pi_i F_i K(U_i)^-1 F_i^T and the anchor lower bound use the known values U_i and their certified spectral range. They do not use a polynomial representation of U. The determinant growth, support cap, inverse bound, and leverage-to-operator inequality therefore remain valid for arbitrary accepted tables.

Each fresh GLS batch still predicts the same true quadratic model at all grid points. Applying a separate nonlinear robust mean at each grid point need not return a single quadratic coefficient vector. That does not change the batch moment calculation. The next design again uses known table values, and the final decoder objective is affine in C at each fixed x. Classical processing of the polynomial-size grid is not an additional source bank at every x.

The Loewner-envelope induction uses only the simultaneous projector inequality, and so transfers unchanged. The final trace-k Cauchy-Schwarz argument also uses only that inequality and positive Tr C=k. For the original encoder comparator, the stationary quadratic is the true fixed-decoder risk, not the learned predictor. Thus its squared-chord discretization remains available. The newer direct-decoder corollary is not needed or silently imported.

Under the same received final-SDP/interior-repair interface and whole-process finite-control debit, the earlier root-risk proof supplies the claimed expected one-payload completed-loss comparison with the unrestricted full-CPTP optimum.

## 5 Rational factors and gap independent clipping are finite

The stated Cholesky backward error gives 0.9U<=L_ch L_ch*<=1.1U. Scaling by 11/10 yields 1.089U<=Ubar<=1.331U, a stronger sandwich than required. The known lower bound eta prevents small unknown pivots; certified rational Cholesky approximation has polynomial precision requirements. The exact Sylvester solve then has smallest singular value at least 2eta. Using Ubar=BB* consistently is important: there is no unbudgeted irrational-factor reconstruction error.

For off-diagonal Hermitian input X, spectral clipping remains in the same subspace because clipping is odd. It is also the unique Frobenius projection onto the Hermitian operator interval [-tI,tI]. Adding the off-diagonal constraint therefore does not change the projection. For objective (1/2)||Y-X||_F^2, strong convexity and the projection variational inequality turn objective gap e^2/2 into distance at most e. The point 0 is a known strict relative-interior point of the constraint set. The finite known-matrix convex optimization and rational feasible repair can consequently be carried out with polynomial accuracy/bit complexity; an unknown-source oracle or an empirical eigenvalue gap is unnecessary.

The average of b individually e-accurate clipping results is e-accurate, not b e-accurate. The two sigma_bar/8 budgets therefore pay all clipping and center-rounding error. The local all-history matrix bound, inherited V inverse bound, Sylvester conditioning, and predetermined clipping thresholds bound intermediate magnitudes on bad records as well. This receipt validates a finite constructive interface; it does not claim that a production SDP implementation was executed.

## 6 Every repeated bank and the common frame horizon are paid

The fixed-cap algebra transfers with the new n and the explicit multiplier b t_j. In particular m_i<=m_bar, sum_i m_i<=n+S_j(f+1), l_i<=m_i+L_zeta, and beta_i>=beta_bar. The displayed n0_bar consequently dominates every paid coarse-center bank. Thus N_j_bar bounds the full raw cost of all support settings, all batches and all inner rounds, before any design or measurement outcome is known. Q_bar counts repeated homogeneous matrix-query invocations separately. Unused horizon slots are padded as required by the same retained causal frame.

The fine contribution is O-tilde(d^3/eta_final). The support floors are of this same order, because S=O-tilde(d^2) and r<=d; they cannot be dropped in this improvement. Repeated coarse centers contribute O-tilde(d^4). With eta_final=Theta(gamma epsilon/k), d=2k, and gamma epsilon<=1, both are covered by O-tilde(k^4/(gamma epsilon)). All stage and inner-round multipliers are logarithmic. The distinct invocation cap remains O-tilde(k^2).

The paid common frame, purification memory, known receiver controls, final decoder synthesis and one payload remain inherited parts of the physical contract. This is not a count-only measurement model or a source-cost statement with free receiver resources.

## 7 Independent diagnostic evidence and limits

The accompanying `_independent_check.py`, `_independent_check.json`, and `_independent_replay.log` pass:

- 12 noncommuting envelope/factor covariance calculations, including eigenvalues at the eta floor and the manuscript's rational Cholesky scaling;
- 36 correlated, biased finite-support error laws with exact prescribed second moments, including strongly skewed rare-large atoms rather than assumed Gaussian tails;
- 324 spectral-clipping bias, full matrix-variance, range and off-diagonal-symmetry checks;
- 3 genuinely nonquadratic envelope-table block designs with 32 actual determinant updates and covariance/leverage checks;
- 18 exact dyadic contraction/precision schedules and 54 exact rational full-bank-cap checks, including local zeta restrictions, coarse-center counts and all-round multiplication.

Extremal reference spectra approach 0.9545 of the d/2 matrix-moment bound. The largest tested realized raw-bank sum is approximately 0.999999976 of its predetermined cap. These tests exercise the claimed inequalities; they are not empirical quantum-query sampling, a confidence-frequency simulation, a certified numerical SDP run, or hardware/compiled-circuit verification.

The received advance is this specific mathematical composition and source ledger. No generic k^2 source rate, quantum advantage over an equally informed conventional learner, new efficient Hayashi implementation, practical gate performance, or novelty/priority claim is established. The earlier received sources remain unchanged.
