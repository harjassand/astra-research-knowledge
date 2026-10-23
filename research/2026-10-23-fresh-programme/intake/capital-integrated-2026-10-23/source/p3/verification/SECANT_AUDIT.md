# Independent audit of the cubic secant compiler

**Status:** the proposed scalar inequalities and vector induction are valid under the stated assumptions. Exact rational tests found no counterexample to the correct construction. They did expose a factor-seven failure from using the previous time's reachable radius, and a failure from inward rounding. This is a mathematical and implementation audit, not evidence of practical superiority or novelty. Novelty remains **UNKNOWN**.

## Contract and indexing

Let

\[
x_{s+1}=\rho x_s+\kappa(Ax_s)^{\circ3}+\sigma(2u_s-\mathbf1),
\qquad S(u)=\sum_{s=1}^T b_s^\top x_s,
\]

where \(A\ge0\) is row stochastic, \(\rho,\kappa,\sigma\ge0\), \(\rho+\kappa+\sigma\le1\), and \(b_s\ge0\) componentwise. The initial state is common to the two trajectories and is zero in the tests. Pair two trajectories whose inputs differ only in bit \((t,j)\), from zero to one. All other innovations, including future innovations, are identical. Then the map is order preserving, and

\[
\delta_{t+1}=x_{t+1}^{(1)}-x_{t+1}^{(0)}=2\sigma e_j,
\qquad \delta_s\ge0.
\]

For \(x_0=0\), define

\[
M_0=0,\qquad M_{s+1}=\rho M_s+\kappa M_s^3+\sigma.
\]

Induction gives \(\|x_s\|_\infty\le M_s\le1\). Propagation from \(x_s\) to \(x_{s+1}\) uses **\(M_s\)**. In particular, a bit at input time \(t\) first changes \(x_{t+1}\); its first subsequent nonlinear propagation uses \(M_{t+1}\), not \(M_t\).

## Sharp scalar envelopes

For \(-M\le b\le a\le M\), put \(z=a-b\) and \(m=(a+b)/2\). Then \(0\le z\le2M\), \(|m|\le M-z/2\), and

\[
a^3-b^3=3zm^2+z^3/4.
\]

Consequently

\[
L(z)=z^3/4\ \le\ a^3-b^3\ \le\ H_M(z)=3M^2z-3Mz^2+z^3.
\]

Both bounds are sharp: the lower is attained at \((a,b)=(z/2,-z/2)\); the upper at \((M,M-z)\). Their derivatives are

\[
L'(z)=3z^2/4\ge0,\qquad H_M'(z)=3(M-z)^2\ge0.
\]

Thus both have monotone polynomial extensions beyond their physical interval. Only the interval \([0,2M]\) is needed for sharpness and the tighter-than-derivative comparison.

## Vector induction and score intervals

Because \(A\ge0\), \(A\delta_s^-\le A\delta_s\le A\delta_s^+\). Row stochasticity places both \(Ax_s^{(0)}\) and \(Ax_s^{(1)}\) in \([-M_s,M_s]^d\). Applying the scalar inequalities componentwise and using monotonicity gives

\[
\begin{aligned}
\delta_{s+1}^-&=\rho\delta_s^-+\kappa L(A\delta_s^-),\\
\delta_{s+1}^+&=\rho\delta_s^++\kappa H_{M_s}(A\delta_s^+),
\end{aligned}
\qquad
\delta_{t+1}^- =\delta_{t+1}^+=2\sigma e_j.
\]

These enclose the actual difference at every later time. Cubes and all polynomials here act componentwise. No column-stochasticity or symmetry of \(A\) is needed. A nonnegative row-substochastic matrix also suffices for the same cube argument.

The exact upper sequence stays in its physical interval: if \(\delta_s^+\le2M_s\mathbf1\), then

\[
\delta_{s+1}^+\le2(\rho M_s+\kappa M_s^3)\mathbf1\le2M_{s+1}\mathbf1.
\]

With \(M_s=1\), the same induction gives \(\delta_s^+\le2\mathbf1\). Since \(b_s\ge0\), valid bit-score bounds are

\[
\sum_{s=t+1}^T b_s^\top\delta_s^-
\ \le\ S(u^{(1)})-S(u^{(0)})\ \le\
\sum_{s=t+1}^T b_s^\top\delta_s^+.
\]

The compiler is deterministic; it does not require a probability law for the innovations. A subsequent product-measure importance-sampling theorem separately requires its product-law assumptions. Signed entries of \(b_s\) require interval sign selection, rather than these two unmodified sums.

## Tightening and what it does not imply

For \(0\le z\le2M\),

\[
L(z)\ge0,\qquad H_M(z)\le3M^2z\le3z\quad(M\le1).
\]

Induction therefore shows that the exact secant lower bound is no smaller than the derivative lower recursion \(\rho\delta^-\), and the secant upper is no larger than the derivative upper recursion \((\rho I+3\kappa A)\delta^+\). The reachable-cube upper is no larger than the uniform-cube upper. For the latter claim, use

\[
\partial_M H_M(z)=3z(2M-z)\ge0\quad\text{when }0\le z\le2M,
\]

followed by monotonicity in \(z\). These are interval inclusions, not claims that every corresponding proposal has smaller actual sampling variance. The earlier observed failure of practical superiority against the linear proposal is not overturned by this audit.

Contraction \(\rho+3\kappa<1\) is **not necessary** for the enclosure proof. It is useful for accumulated roundoff bounds and decay of the impulse. One executed fixture deliberately has \(\rho+3\kappa=11/10\).

## Derivative-critical harmonic bound

The follow-up critical construction also passes the audit. Set \(\rho=\kappa=1/4\), \(\sigma=1/2\), so that the global derivative bound is one. In the scalar case \(A=1\), the uniform-cube upper impulse recursion is

\[
d_0=1,\qquad d_{n+1}=g(d_n)=d_n-\tfrac34d_n^2+\tfrac14d_n^3.
\]

For \(0<d\le1\), \(0<g(d)\le d(1-d/2)\le d\). Hence

\[
\frac1{d_{n+1}}-\frac1{d_n}
\ge \frac1{2(1-d_n/2)}\ge\frac12,
\qquad d_n\le\frac2{n+2}.
\]

If \(N\) is the number of affected score terms, including the immediate impulse, then

\[
\sum_{n=0}^{N-1}d_n\le2\sum_{k=2}^{N+1}\frac1k
=2(H_{N+1}-1).
\]

For a general nonnegative row-stochastic \(A\), put \(m_n=\|\delta_n^+\|_\infty\). Monotonicity yields \(m_{n+1}\le g(m_n)\), and \(m_0=1\), so the same bound holds. For constant nonnegative \(b\), the bit-score upper bound is at most \(2\|b\|_1(H_{N+1}-1)\). It can be loose in a high-dimensional local system because it replaces a localized impulse by its maximum in every coordinate. This establishes a logarithmic upper bound on the cumulative certified sensitivity where the corresponding scalar derivative recursion gives \(N\). It does not prove that the actual score difference grows logarithmically or that an importance estimator has bounded variance as \(T\) grows.

At derivative criticality the uniform geometric roundoff formula cannot be used. A simulator with a certified per-step local error \(\eta\), clipped to the invariant cube, has state error at most \(t\eta\) at time \(t\), for exact initial state. The resulting constant-\(b\) score error is at most \(\eta\|b\|_1T(T+1)/2\), before adding objective arithmetic errors.

Likewise, a grid-rounded upper secant sequence need not obey the unrounded harmonic bound. Its accumulated additive rounding error can be bounded by \((n+1)h\), or the independently proved analytic harmonic upper bound can itself be used with a valid numerical enclosure. The executed eight-bit example becomes constant at \(9/128\), exceeding \(2/(n+2)\) first at \(n=27\); at \(n=512\), the unrounded bound is \(1/257\). The rounded sequence remains a valid upper enclosure. The invalid claim would be to ascribe the unrounded asymptotic decay to that sequence without accounting for rounding.

## Finite precision and computation

Unrounded exact rational cubics can grow denominator bit lengths by a factor of three at each iteration. Their mathematical existence is not a polynomial-bit implementation claim.

A direct finite-grid implementation is valid: use grid \(h=2^{-B}\), evaluate each update exactly from the rational grid inputs, round lower endpoints down, and upper endpoints up. Round the initial impulse in the same directions. Clip lower endpoints at zero. Upper endpoints may be clipped at an independently proved cap such as two or \(2\widehat M_s\). Propagate \(\widehat M_s\) with upward rounding, and cap it at one using the proved global invariant. Then \(M_s\le\widehat M_s\le1\). For actual \(z\le2M_s\), increasing the radius from \(M_s\) to \(\widehat M_s\) increases \(H_M(z)\), and monotonicity in \(z\) completes the rounded upper induction.

The tests use exact `Fraction` arithmetic followed by directed rounding to eight fractional bits. They do not assume that ordinary floating evaluation followed by one `nextafter` encloses a polynomial; such an implementation would need an error bound or interval arithmetic. Logistic functions, exponentials, accumulated objective sums, and the final variance-certificate evaluation need their own numerical treatment.

For a uniform cube and \(\lambda=\rho+3\kappa<1\), each envelope map has infinity-norm Lipschitz constant at most \(\lambda\) on the invariant cube. Grid error of at most \(h\) per update, including the initial rounding, accumulates to at most \(h/(1-\lambda)\) per component. This bound concerns the compiler's endpoints; it does not bound unaccounted simulator or estimator arithmetic.

The generic all-bit forward compiler requires \(O(dT^2(\operatorname{nnz}(A)+d))\) arithmetic operations. For time-homogeneous dynamics, a uniform cube, and constant \(b\), one impulse sequence per site can be reused across all remaining horizons, yielding \(O(dT(\operatorname{nnz}(A)+d))\). Spatial translation symmetry can permit further reuse. The absolute-time reachable radius generally prevents horizon-only reuse. These are operation counts; coefficient bit lengths, directed-rounding work, preprocessing, and the actually used symmetry must also be charged. No runtime comparison was conducted here.

## Executed adversarial checks

`check_secant.py` was written before its single recorded execution. The two-site case had previously been exposed in the derivative-compiler audit; the other two cases were chosen for this audit. All cases are exploratory fixtures, not independent confirmation or a representative performance benchmark.

The exact-rational run checked 1,683 scalar endpoint pairs, 96 adjacent monotonicity pairs, and sharp attaining endpoints. It exhaustively checked three dynamical fixtures:

| Fixture | Dimensions | Steps | Paths | Paired bit changes | Component enclosures |
|---|---:|---:|---:|---:|---:|
| Symmetric two-site | 2 | 4 | 256 | 1,024 | 5,120 |
| Asymmetric row-stochastic three-site | 3 | 3 | 512 | 2,304 | 13,824 |
| Noncontractive, invariant cube | 2 | 3 | 64 | 192 | 768 |
| Total | | | 832 | 3,520 | 19,712 |

Every exact and rounded enclosure held; derivative dominance, reachable-cube dominance, and positively weighted time-dependent score bounds held. The process recorded **0.355011209998338 seconds** using `time.perf_counter`; this is only an execution receipt for a small check, not a performance claim. No model-token or monetary usage receipt was exposed for this bounded work.

Two invalid variants have explicit counterexamples:

1. **Wrong radius index.** Let \(\rho=1/2,\kappa=1/20,\sigma=9/20\), and \(A=\begin{pmatrix}3/4&1/4\\1/4&3/4\end{pmatrix}\). Flip the first bit at input time zero and keep the second bit one. At state time one the pair is \((-\sigma,\sigma)\) and \((\sigma,\sigma)\). The next-step second-coordinate gap is exactly \(5103/1280000\). Using \(M_0=0\) in that propagation produces the false upper bound \(729/1280000\), seven times too small. The correctly indexed \(M_1=9/20\) attains the exact upper gap.
2. **Inward rounding.** Rounding the actual impulse \(2\sigma=9/10\) down to an alleged eight-bit upper endpoint gives \(115/128<9/10\), failing before any propagation.

The separately written `check_secant_critical.py` ran once after the critical extension was proposed. It checked eight exact-rational stages of the scalar recursion and a three-site asymmetric recursion, their cumulative harmonic bounds, and the reciprocal increment. It also checked the eight-bit rounded scalar recursion through 512 stages and identified the plateau described above. Its recorded `time.perf_counter` duration was **0.02284076799696777 seconds**. This follow-up was an adversarial check, not part of a previously held-out performance comparison.

## Reproduction and continuation

Run `python p3_work/verification/check_secant.py`. The complete machine-readable receipt is `secant_audit_results.json`. The source, output, and this audit are in `/workspace/scratch/8b3a6d33b6cf/p3_work/verification/`.

Run `python p3_work/verification/check_secant_critical.py` for the derivative-critical check; its receipt is `secant_critical_results.json` in the same directory.

The remaining empirical question is whether the tighter certified intervals produce a useful complete acquisition-and-inference process against equally informed baselines after all compilation and precision costs are counted. This audit does not resolve it. The parent's main implementation and already frozen evaluation should answer that question; no new allocation, worker, external contact, or Ultra request was made for this follow-up.
