# A four-g-query source preimage of the first smoothed Stein residual

This closes one concrete residual-action interface in CORE_THEOREM.md. It does not acquire the starting smoothed mean h_b(G) itself, and it does not establish an iterated compiler.

Let g be any globally L-Lipschitz conservative C^{1,1} field. Fix 0<b<1 and define the analysis fields

    h_b(y)=E g(by+sqrt(1-b²)Z),
    K_b(y)=integral_0^b E Dg(ty+sqrt(1-t²)Z)dt,
    Gamma_b=sym(K_b Dh_b).

Weak derivatives occur only in the analysis. All executed queries below are original g values. Let 0<kappa<1, a=sqrt(1-kappa²), and suppose for a declared beta<1,

    (kappa²/a²) * 2b²/(1-b²) <= beta.                 (1)

For the analysis program X=h_b(G)+aZ, its residual is Gamma_b-kappa²I. A matrix field R0 with

    P_a^G R0=Gamma_b-kappa²I                           (2)

has an exact bounded conditional action costing at most FOUR original g-value queries on every execution. No whole random matrix is produced or used in a square root.

## Construction

Draw T uniform on [0,b] using a Gaussian three-coordinate/radius ratio. Write t=T, c=(t,b)^T, and

    D=diag(1-t²,1-b²),
    N=D-(kappa²/a²) cc^T,
    delta²=(1-beta)(1-b²)/2.

The rank-one PSD test and (1) give N>=(1-beta)D>=2delta²I. Draw a correlated Gaussian pair (C1,C2) with scalar covariance N-delta²I acting identically on physical coordinates. This needs only a known 2-by-2 covariance square root and Gaussian vectors. Given acquired y,v, put

    c1=(t/a)y+C1,          c2=(b/a)y+C2.

Conditional on T,C1,C2, acquire two fresh bounded heat-Hessian actions with smoothing delta, using the frozen S4 chi_3 secant factory. Compose them in a fresh equiprobable order. Return

    A_R0(y;v)=b² J_Hdelta(c1) J_Hdelta(c2) v-kappa²v,   (3)

with the stated random order. Each heat action costs two g values, is conditionally unbiased, and obeys ||J(v)||<=L||v||. Hence

    E[A_R0(y;v)|y,v]=R0(y)v,
    ||A_R0(y;v)||<=(b²L²+kappa²)||v||                (4)

on every execution. The common C1,C2 are conditioned first, and the two secant calls then use independent fresh internal seeds. Thus their product has the required conditional mean despite the correlated centers. There is no independence assertion after feeding a word into an adaptively chosen new center.

## Proof of the source-preimage identity

The mean of (3) is the symmetrized derivative word at

    X1^0=(t/a)y+C1+delta Z1,
    X2^0=(b/a)y+C2+delta Z2,

where Z1,Z2 are independent fresh standard Gaussians. Its conditional residual input covariance is exactly N. Apply source smoothing y=aG+kappa W, with common W standard Gaussian. The centers become tG,bG and the added common covariance is (kappa²/a²)cc^T, restoring exactly D. Thus, conditional on G,T, the two resulting derivative points have independent residual Gaussian noises of variances 1-t² and 1-b². Averaging T and the random order gives

    b² sym{[E_T E Dg(TG+sqrt(1-T²)Z1)]
                                  [E Dg(bG+sqrt(1-b²)Z2)]}
      = sym(K_b Dh_b)=Gamma_b.

The constant -kappa²I is unchanged by P_a. This proves (2) while retaining the actual source common-noise correlation.

## The implemented correction and its cost

Substitute the action (3) for R0(Y)V in CORE_THEOREM.md's finite correction. The action's extra randomness is included, with

    E||Uhat||² <= pi²/(8a²) (b²L²+kappa²)² d.         (5)

Therefore its Gaussian-reserve randomization error has the full-TV upper bound phi(1) times (5) divided by tau². This is an actual four-g-query correction action, not a residual oracle assumption. It uses O(d) scalar/vector work around the four whole-vector calls; the two-by-two covariance is independent of physical d. Gaussian-and-real primitives match the original model, up to the same scalar-constant approximation convention as the frozen secant factory.

The uniform condition (1) is charged. As b tends to one it fails for fixed kappa. It supplies a finite first smoothed residual preimage, not arbitrary inverse heat flow. The corresponding h_b(G) in X is still an unacquired mean node: treating its value as free would conceal the starting mean acquisition problem. A finite value-only implementation of the joint starting program, control of subsequent nonlinear residual preimages and current-law inverses, source retention, target-noise allocation, and an every-execution polylog query cap remain open.

The useful next attack is to combine this negative-correlation Gaussian allocation with an acquired joint mean circuit or a subcritical correction forest. The construction avoids the exponential high-frequency preimage cost in its explicit smoothing regime. It does not establish that this regime can be maintained through the required recursive program.

The covariance construction extends exactly to an m-factor fixed-center word. For source coefficients t_i, start with D=diag(1-t_i²) and set N=D-(kappa²/a²)tt^T. A uniform positive heat reserve exists whenever (kappa²/a²)sum_i t_i²/(1-t_i²)<=beta<1. Conditional on a common Gaussian with the padded N covariance, m fresh secant actions acquire the word preimage with 2m original queries and norm bound L^m||v||. The covariance arithmetic is polynomial in m,d. This concerns fixed linear source centers and fresh word actions; it does not cover arbitrary adaptive centers or acquire a current-law nonlinear residual automatically.
