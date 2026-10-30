# Independent audit: entropy-separated sum and actual two-population corner exit

Reviewer: finite_phase_drift_challenge, 2026-10-30. Internal mathematical review. Reviewed ENTROPY_SUM_GLUES_ALL_COMPOSITIONS.md.

## Verdict

The sum construction earns one norm-like function with strict physical drift throughout the finite B-corner at all sufficiently large A+C, uniformly over ALL compositions. The entropy comparison, fixed exponential tilt, and polynomial error bounds pass. The stopped exit/forcing consequence is also valid; its finite-head proof should explicitly include the finite wrong-jump landing set and return-time bound, as detailed below. Outer B-feedback remains unproved.

## 1. Exponentially damped common phase certificate

Replacing the growing tilt by r^(alpha delta) exp(-d delta)2^|delta| changes only fixed positive edge constants. Downward factors still tend to zero; upward burdens still have exponent 2alpha delta; first-down return-path energy still gains at least delta in flux height. Thus every endpoint policy remains eventually Hurwitz for alpha<1/2. Policy-independent tree offsets are unchanged. The finite policy-maximization argument and eventual rational-Puiseux ordering still apply, with real coefficients containing the fixed exponential constants if necessary.

The actual forward W ratio includes exp(-d delta) exactly. The remaining Gamma and rational-vector shift errors are 1+O(1/r) and are absorbed by fixed inflation. This verifies the stated robust LW inequality on A/N≥epsilon1 without differentiating source coefficients or freezing the hidden composition.

## 2. Uniform entropy estimates, including population endpoints

For every fixed finite B set, the previously audited recursion gives

    V0≤F≤C(N+8)^(8alpha)V0

after absorbing finite B-factorials into constants. Thus log F=alpha log(A!C!)+O(log(N+1)) uniformly over 0≤A≤N, including A=0 or C=0.

The finitely many positive rational-Puiseux components of v_d have uniform polynomial upper and lower bounds. Integer beta offsets change Gamma(N+beta+1)/N! only by polynomial factors, and exp(-d beta) is a phase constant. Hence log W=alpha log(N!)-dN+O(log(N+1)) uniformly over the halo phases.

The uniform binomial entropy estimate log binom(N,A)=N H(A/N)+O(log(N+1)) is valid also at A=0,N. Therefore the claimed W/F comparison is uniform over ALL compositions.

Because H is strictly increasing on (0,1/2), there is a genuine positive gap between alpha H(epsilon1) and alpha H(epsilon0). The selected d gives uniform exponential SMALLNESS of W/F on A/N<epsilon1, and uniform exponential LARGENESS on epsilon0≤A/N≤1−epsilon0. The overlap and opposite endpoint need no dominance because both drifts are already negative there. No selector is differentiated.

## 3. Polynomial drift margins and global-in-corner sum estimate

At B<4, LF=-V0 and F/V0 is polynomial, giving LF≤-cN^(-D)F. At B≥4 in either extreme cone, the stronger cubic negative drift supplies the same weaker polynomial-margin form. Everywhere on the fixed halo, bounded reaction shifts and finite recursion give |LF|≤CN^D F.

For W, its negative drift is exp(-dr)Gamma(r+1)^alpha, while W differs by a positive polynomial/Puiseux factor, giving LW≤-cN^(-D)W on the comparability cone. Outside that cone, every connector rate is polynomially bounded in N, and every fixed count/phase ratio of W is polynomially bounded. Invisible fast conversions contribute EXACTLY zero. Hence |LW|≤CN^D W holds uniformly even where the projected coefficient lower bounds fail.

In the C-dominant bad-W cone, exponential smallness of W/F defeats the polynomial positive LW bound and leaves a fixed fraction of F's negative margin; U is comparable to F there. In the balanced bad-F cone, exponential largeness of W/F defeats the polynomial positive LF bound and leaves a fixed fraction of W's negative margin; U is comparable to W. In the remaining regions, add the two negative margins directly. Taking a common exponent and threshold proves LU≤-cN^(-D)U on every phase in J and every composition at large N.

All actual incoming target values needed by the primal generator lie in the exact halo. Extending W elsewhere positively is harmless for this LOCAL calculation, but establishes no drift outside J. Also U≥F≥V0, so U is norm-like on the strip and N^(-D)U tends uniformly to infinity as N→infinity.

## 4. Exit and finite-head argument without recurrence import

Kill the physical process on its first exit tau from J. Assign zero to the cemetery state for the preliminary nonexplosion test. The killed-generator drift is no larger than the physical LU, since positive exit target values are removed. The norm-like stopped Foster argument therefore proves nonexplosion before tau and finite expected hitting time of a sufficiently large finite head or exit, bounded by a constant times U(x).

To justify finite expected exit from the head without circularly assuming it, use the following explicit regeneration attempt. From each head state prescribe successive immigrations until leaving J, at most K+1 steps. The union P of all states on these finitely many paths is finite, and every prescribed channel has positive rate. The probability of completing the prescribed path before its first wrong jump is bounded below by a fixed p>0 over head states. Each attempt has uniformly finite mean duration; immigration ensures total holding rate at least one.

If an attempt fails, its first wrong jump lands in a finite set P' because P is finite and the reaction list has bounded finite jumps. From every state of P', the drift estimate bounds the mean time to return to the head or exit; the maximum of these finitely many bounds is finite. Thus successive attempts have uniform positive success probability and uniformly bounded mean duration, proving finite expected exit by a geometric-attempt argument. This uses actual reaction paths, not frozen phases or recurrence of the full network.

Only AFTER obtaining these finite head exit means, apply the strong Markov property at first head entry to bound expected head occupation uniformly over starting states. Stopped Dynkin, localization, and Fatou then give E_x U(X_tau)≤U(x)+C. Since the negative drift integrand is bounded below by a positive constant outside the head, the same argument gives E_x tau≤C'(U(x)+1). It also bounds occupation integrals of the displayed integrand outside the head.

Boundary data dominated by U consequently have finite nonnegative Dirichlet extensions, and running costs dominated by the earned occupation integrand have finite Poisson extensions. Neither construction replaces actual composition/phase excursions by an averaged law.

## Scope retained

The certificate is global in composition within a fixed finite B-corner, not global in all populations. Its outer halo values feed back into the generator outside J, and the present proof gives no inequality absorbing that feedback. No global recurrence, width-uniform constants, or efficient synthesis claim follows.

Reviewed source hash:
4b2c76b8e766e1fe96f8fdd6729b893f8d63b3bcc92cda04dc53bf156209b564  producer-workspace/ENTROPY_SUM_GLUES_ALL_COMPOSITIONS.md
