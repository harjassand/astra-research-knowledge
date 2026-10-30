# Finite-birth expansion of the true tail-return operator
Status: new unreviewed construction. It is a possible way to replace per-phase scalar first-up estimates by finite matrix certificates. No general recurrence theorem is asserted.

## Earned setting
Use an actual residual s preserved by conservative motion and clearing, with each competing birth changing s by at most J. Let N measure conservative size and clearing decrease N. Above a FIXED finite head N<=H, every conservative fiber reaches clearing. Assume the finite-fiber bound and resource gap from POLYLOG_CAP_FINITE_FIBER_EXTENSION.md. Stop at the actual cap N<=L(s)=(log s)^p and at a fixed low-s threshold. The previously derived estimates imply, uniformly at every tail restart,

    P(any birth before returning to the head or exiting the cap)
        <= s^(-g+o(1)),       g=q-a>0.

The zero-birth route preserves s exactly. It consists of finite conservative killed blocks followed by clearings, decreasing N until the head. Its phase-valued return distribution is actual, not a frozen stationary average.

## Weighted expansion by the number of rare births
Let phi(s)=Gamma(s+1)^alpha exp[(log s)^(1+p/2)] with alpha J<g. Its one-birth upward weight ratio is at most s^(alpha J+o(1)). Stop at head return, cap exit, or the low-s threshold, giving zero terminal value at the latter two exits. The positive first-birth renewal operator therefore has weighted norm at most

    epsilon(s)=s^(-(g-alpha J)+o(1)).

Choosing the threshold large makes its supremum less than 1/2. The full weighted head-return kernel is bounded in weighted sup norm by 2. Expand it by 0,1,...,K-1 births. For fixed K, the residual before those births differs from its initial value by at most KJ. The first K rare-birth factors are therefore each evaluated at s+O(K), and the remaining continuation has norm at most2. The remainder obeys

    ||R-R_{<K}||_phi <= s^(-K(g-alpha J)+o(1)).              (1)

For every fixed D>=0 the SAME proof and exponent hold in the heavier weight psi(s)=(1+s)^D phi(s), because its fixed-jump ratio changes only by 1+O(1/s). This upgrade is essential for terminal profiles growing as s^D: the terminal residual after an unbounded number of births is not bounded by its initial value.

This is an absolute weighted-return bound; it does not assume that the tail is invariant or already recurrent. The same renewal construction can include stopped running costs, using the earned absorption-time bounds.

## Why each fixed truncation is genuinely finite algebra
Starting from a head-to-tail jump, the initial N is bounded. Before the Kth birth, N increases by at most K times the bounded birth increment. Thus all conservative fibers appearing in R_{<K} belong to a fixed finite set, independent of the moving cap once s is large. Their exact killed resolvents and exit kernels are finite matrix inverses. For the present residual family, physical resource counts on each fixed fiber are affine in s (B=s+g_N). Under this representation hypothesis, the mass-action entries are rational functions of s (with fixed shifts); arbitrary bounded-jump residual coordinates alone do not ensure rational dependence. multiplying the FACTORIAL part of the weight ratio across the bounded total residual shift yields algebraic expressions with Puiseux expansions at infinity for rational alpha (not necessarily rational functions of s^(1/q)). The subexponential tilt ratio is an additional explicit analytic factor, not a rational-Puiseux function. It must be retained exactly or bounded to sufficient order (including logarithmic factors); it may not be dropped when its error exceeds the claimed negative margin. No infinite matrix or phase-space mixing estimate enters these finite coefficients.

## Finite-head certificate, not an automatic sign theorem
The actual head generator plus its true tail-return kernel defines a finite-phase nonlocal return operator in s. Replace the tail kernel by its <K-birth expansion and compute a positive rational-Puiseux profile v_j(s). If its strict negative certificate has margin at least s^(-m)phi(s), while max_j v_j(s)<=C s^D and the phi-weighted head-to-tail entrance operator is bounded by C s^Q (INCLUDING the actual ratio phi(s+ell)/phi(s) at each entrance jump), then use (1) in the weight psi=(1+s)^D phi, not merely phi. Its initial bound is s^D phi(s), and after multiplying by this weighted entrance bound s^Q it absorbs the omitted true return forcing whenever

    K(g-alpha J)>D+Q+m.

The certificate must also include the finite-time running cost and actual head shifts; these are finite algebra at fixed K. This gives an explicit verification obligation rather than assuming a favorable finite-corner barrier.

This mechanism has not yet been instantiated on the enlarged mixed-complex family. There is no claim that increasing K must eventually find a certificate. An all-zero leading operator, or a nonnegative true return mode, remains an obstruction. In particular weak reversibility alone has not here been shown to force the required finite-head sign.

## Further global interface obligation
A head certificate is not by itself the global Foster function. Its actual tail extension must retain a controlled polynomial-in-s profile relative to phi, and its incoming cap collar must satisfy the quantitative factorial separation already isolated in the cap theorem. If those fail, the construction stops; neither a killed boundary nor a truncation may be silently treated as a physical reflecting boundary.
