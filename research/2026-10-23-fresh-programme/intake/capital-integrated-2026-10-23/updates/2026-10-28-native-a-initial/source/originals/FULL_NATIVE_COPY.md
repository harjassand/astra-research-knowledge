I developed a **replacement for the packet’s unstable coupled-source inverse, proved a quadratic full-law correction theorem, and implemented a value-only scalar instance with a rigorous TV bound**. The full high-dimensional, polylogarithmic-query theorem remains open.

The main advance is the general analytical mechanism. The scalar implementation establishes that its correction can be acquired and executed without a mean or derivative oracle on a concrete nonlinear source. An independent challenge also found a substantially simpler scalar competitor, which changes how the implementation should be assessed.

The complete proofs, code, frozen coefficients, exact calculations, and unchanged starting sources are preserved in [Astra_Gaussian_Correction_2026-10-27.zip](https://chatgpt.com/library?file_id=libfile_573f6ec0b4448191ae2258b45e14bd7d&account_id=personal).

## 1. The consequential construction: center the correction over the whole Gaussian source

The packet’s Newton route required a correction to have zero mean **conditional on one Gaussian seed**. That is stronger than necessary for preserving the unknown target mean. It also leaves the derivative in the other seed as a difficult perturbation.

I replaced that condition with **global centering through joint Gaussian divergence**.

For analysis, write

\[
X=h(G)+Z,\qquad \mu=\mathbb Eh(G),
\]

where \(G,Z\) are independent standard Gaussian vectors and \(h\) has Lipschitz constant \(\ell<1\). The packet already supplies the canonical Stein resolvent \(K\), satisfying

\[
\delta_GK=h-\mu,\qquad \|K\|_{\mathrm{op}}\le \ell.
\]

Here \(K\) remains an analytical field; the packet’s two-query factory acquires an unbiased action of it, not the entire field.

Set

\[
Q=(G,Z),\qquad B=[K(G),I].
\]

Then the rowwise Gaussian divergence satisfies

\[
\delta B=X-\mu.
\]

Define

\[
\tau=B(DX)^\top,\qquad R=\operatorname{sym}\tau-I.
\]

For this initialization,

\[
\tau=I+K(Dh)^\top,\qquad
\operatorname{sym}\tau\succeq (1-\ell^2)I.
\]

The new correction uses a symmetric matrix field \(S\):

\[
J=SB,\qquad u=\delta(SB).
\]

Because a Gaussian divergence has expectation zero, \(X+u\) preserves \(\mu\). The field \(S\) need not be positive; the resulting random vector is a positive probability-law construction because it is an ordinary pushforward.

### The full coupled inverse is coercive

More generally, suppose

\[
\delta B=X-\mu,\qquad
\operatorname{sym}\tau\succeq cI,\quad c>0,
\]

with \(B,\tau\) bounded in operator norm. On the closed divergence graph space, solve

\[
\mathbb E\!\left[\delta(SB)\cdot\delta(TB)\right]
+\mathbb E\langle S\tau,T\rangle_F
=
-\mathbb E\langle R,T\rangle_F
\tag{1}
\]

for every admissible symmetric test field \(T\).

The decisive energy identity is

\[
a(S,S)
=
\|\delta(SB)\|_2^2
+\mathbb E\operatorname{tr}\!\left(S^2\operatorname{sym}\tau\right)
\ge
\|u\|_2^2+c\|S\|_2^2.
\]

Thus the full equation has a variational inverse. With

\[
r=\|R\|_{L^2(F)},
\]

its bounds are

\[
\boxed{
\|S\|_2\le \frac r c,\qquad
\|u\|_2\le \frac r{2\sqrt c},\qquad
\|J\|_2\le \frac{\|B\|_{\mathrm{op},\infty}r}{c}.
}
\tag{2}
\]

Equation (1) is precisely the weak form of

\[
\operatorname{sym}\!\left[B(Du)^\top+J(DX)^\top\right]=-R.
\tag{3}
\]

**The source derivative is absorbed into the principal operator.** It is no longer being treated as a bounded, small perturbation on ordinary Gaussian \(L^2\).

This resolves a real analytical obstruction in the frozen construction. It does not acquire the variational solution from values for free.

## 2. The correction has a proved full-law bound

The next issue was whether this inverse actually improves the law when its full derivative is not controlled.

It does, after explicitly budgeted Gaussian smoothing.

Let \(W\) be fresh standard Gaussian and \(a>0\). Then

\[
\boxed{
\operatorname{TV}\!\left(
\mathcal L(X+u+aW),
N\!\left(\mu,(1+a^2)I\right)
\right)
\le
\min\{1,C(a,c)r^2\},
}
\tag{4}
\]

where

\[
C(a,c)=
\frac{\sqrt6}{2\sqrt c}
\left[\frac1a-\arctan\!\frac1a\right]
+
\frac{\sqrt2}{8ca^2}.
\]

The reserve \(aW\) is included in the target covariance.

### Why this is a full-law theorem

For an arbitrary Borel event \(A\), smooth its indicator with that reserve Gaussian. Let \(f\) solve the corresponding Gaussian Stein equation. Testing (1) with \(D^2f(X)\) gives the exact cancellation

\[
\mathbb EH(X)+\mathbb E[DH(X)\cdot u]
-\mathbb EH(\mu+Z)
=
\mathbb E\!\left[R:D^3f(X)[u]\right].
\tag{5}
\]

Taylor expansion in **output space**, together with uniform Gaussian derivative bounds, controls the remainder. Taking the supremum over every event \(A\) proves TV.

This argument requires no estimate of the full \(Du\). It also makes no inference from finite moment matching.

### The theorem charges actual randomization

Suppose an implemented correction \(\widehat u\) has

\[
\mathbb E[\widehat u\mid Q]=u.
\]

Let \(e\) be the \(L^2\) norm of the **full** linearized-equation residual of an approximate solve. The proof gives

\[
\operatorname{TV}
\le
C_2(a)e
+
C_3(a)r\|u\|_2
+
C_4(a)\mathbb E\|\widehat u\|^2,
\tag{6}
\]

with

\[
C_2=\frac{\log(1+a^{-2})}{\sqrt2},\quad
C_3=\sqrt6\left[\frac1a-\arctan\!\frac1a\right],\quad
C_4=\frac{\sqrt2}{2a^2}.
\]

A conditional bias \(b\) adds \(\|b\|_2/a\).

This is useful because it charges the extra effects of a randomized correction explicitly. Unbiasedness alone is insufficient. Likewise, a Galerkin residual that vanishes only on the fitted basis is insufficient: the omitted directions must also be bounded.

The complete proof and domain assumptions are in SMOOTHED_LAW_NEWTON_THEOREM.md[SMOOTHED_LAW_NEWTON_THEOREM.md](sandbox:/workspace/scratch/810b1ee40202/research/coercive_audit/SMOOTHED_LAW_NEWTON_THEOREM.md).

## 3. An actual four-value correction, without querying the mean

The ideal expression

\[
u=\delta(SB)=S(X-\mu)-\operatorname{div}_B S
\]

appears to require \(\mu\). That dependence can be removed by querying an independent source value \(h(G')\).

Conditionally on the original source \(Q\),

\[
-S\bigl(h(G')-\mu\bigr)
\]

has zero mean and covariance at most \(\ell^2SS^\top\). Its effect is therefore charged quadratically through the implemented-law bound.

In scalar output dimension, this gives a concrete finite program.

For an explicitly evaluable coefficient \(S(G,Z)\), use the packet’s exact two-value secant factory to obtain \(\widehat K(G)\), with

\[
\mathbb E[\widehat K(G)\mid G]=K(G),
\qquad |\widehat K(G)|\le\ell.
\]

Return

\[
\begin{aligned}
X&=h(G)+Z,\\
\widehat u
&=
S(G,Z)\,[h(G)-h(G')+Z]
-S_G(G,Z)\widehat K(G)-S_Z(G,Z),\\
Y&=X+\widehat u+aW.
\end{aligned}
\tag{7}
\]

This uses exactly:

- One value \(h(G)\).
- One independent value \(h(G')\).
- Two endpoint values for the secant.

There is no derivative of \(h\), mean, potential, or conditional-mean query. Derivatives of \(S\) are derivatives of the explicit stored coefficient function.

The actual conditional error satisfies

\[
\boxed{
\mathbb E[(\widehat u-u)^2\mid G,Z]
\le
\ell^2(S^2+S_G^2).
}
\tag{8}
\]

Thus

\[
\mathbb E\widehat u^2
\le
\|u\|_2^2+\ell^2\mathbb E(S^2+S_G^2),
\]

which can be inserted directly into (6).

**Constructing and certifying \(S\) remains a separate cost.** Four runtime queries do not mean that an appropriate coefficient field has been acquired in four queries.

### Executed acquisition and a rigorous nonlinear fixture

I implemented a learner for

\[
h(x)=\frac7{20}\cos x
\]

that received only source values and the Lipschitz bound. It fitted a total-degree-ten Hermite polynomial \(S(G,Z)\), using all 66 basis elements.

The acquisition used **73,776 source-value queries**. Its training identities removed \(h'\) by integration by parts. The coefficients were frozen as exact dyadic rationals before the analytical truth evaluator ran.

For the ideal exact-real four-query program using those coefficients, the resulting certificate is

\[
\boxed{
\operatorname{TV}\!\left(
\mathcal L(Y),
N\!\left(\frac7{20}e^{-1/2},\,2\right)
\right)
<
\frac{331}{1{,}000{,}000}.
}
\tag{9}
\]

The certificate includes the actual randomized secant and independent mean replacement.

| Certified quantity | Upper bound, displayed numerically |
|---|---:|
| Full equation residual \(\|E\|_2\) | \(0.00101904438553\) |
| Initial Stein residual \(\|R\|_2\) | \(0.0323046347222\) |
| Ideal correction \(\|u\|_2\) | \(0.0157520218617\) |
| Additional stochastic variance | \(0.0000691824615907\) |
| Actual correction second moment | \(0.000317308654323\) |
| Residual contribution from omitted Hermite terms | \(<6.204\times10^{-18}\) |

These bounds come from exact rational polynomial calculations, Gaussian Hermite orthogonality, and an analytical \(L^8\) bound on the infinite tail. The final rational inequality is checked exactly. This is not a certificate obtained from output moments or KS tests. See EXACT_GALERKIN_CERTIFICATE.txt[EXACT_GALERKIN_CERTIFICATE.txt](sandbox:/workspace/scratch/810b1ee40202/research/coercive_audit/EXACT_GALERKIN_CERTIFICATE.txt).

The retained floating execution generated 100,000 outputs using exactly 400,000 runtime calls, or 473,776 calls including calibration. Training arithmetic is \(O(2304\cdot66^2+66^3)\); each output evaluates a 66-term polynomial and makes four source calls. The exact verifier performs additional rational arithmetic.

The certificate concerns the specified exact-real program. The floating outputs are execution checks; a finite-bit TV claim would require the commonly rounded target and a numerical-error budget.

The verifier also uses the known cosine fixture. **This is not yet a generic data-only certificate for arbitrary unknown \(C^{1,1}\) sources.** On the explicitly known cosine family, the analytic mean is an immediate conventional alternative.

## 4. A stronger scalar alternative changed the assessment

The independent challenge found a simpler scalar channel that needs **no fitted \(S\)**.

For any scalar globally \(\ell\)-Lipschitz source, query four independent values

\[
V_i=h(G_i),\qquad i=0,1,2,3,
\]

and define

\[
\widehat v=\frac{(V_1-V_2)^2}{2},
\qquad
\widehat m_3=(V_1-V_2)^2(V_1-V_3).
\]

With independent standard Gaussians \(Z,W\), return

\[
\boxed{
Y=
V_0+
\left(1-\frac{\widehat v}{2}\right)Z
-\frac{\widehat m_3}{6}(Z^2-1)
+aW.
}
\tag{10}
\]

This is a positive pushforward on every execution, including when the random coefficient of \(Z\) is negative. It uses four values, six scalar Gaussian draws, and constant arithmetic and storage.

Its full-law bound is

\[
\boxed{
\operatorname{TV}\!\left(
\mathcal L(Y),N(\mu,1+a^2)
\right)
\le
\frac{19D_4}{24(1+a^2)^2}\ell^4
+
\frac{\phi(1)}{a^2}
\left(\frac34\ell^4+\frac83\ell^6\right),
}
\tag{11}
\]

clipped at one, where

\[
D_4=\frac12\|\phi^{(4)}\|_1
=1.40030015041\ldots
\le\sqrt6.
\]

For \(a=1/2\),

\[
\operatorname{TV}
\le
1.4353975831\,\ell^4+
2.58102106154\,\ell^6.
\]

For example, \(\ell=0.1\) gives a bound below \(1.462\times10^{-4}\), with four queries and no calibration.

The proof retains the random coefficients throughout. Gaussian integration by parts cancels the variance and third-cumulant contributions, while uniform Taylor remainders control every smoothed event. The actual correction satisfies

\[
\mathbb EU^2
\le \frac34\ell^4+\frac83\ell^6,
\]

so its randomization is paid.

I am treating this as an **ordinary transported-cumulant comparator**, without a historical novelty claim. It demonstrates why expensive scalar fitting should not be defended as the main computational achievement. Its guarantee concerns a small Lipschitz-to-noise ratio; it does not give arbitrary-accuracy polylogarithmic sampling at a fixed ratio.

The proof and executed counting-oracle check are preserved in UNIVERSAL_FOUR_VALUE_SCALAR_COMPARATOR.md[UNIVERSAL_FOUR_VALUE_SCALAR_COMPARATOR.md](sandbox:/workspace/scratch/810b1ee40202/research/gaussian_challenge/UNIVERSAL_FOUR_VALUE_SCALAR_COMPARATOR.md).

Across the fitted, explicit-coefficient, and universal scalar experiments, the counted synthetic source runs used 1,427,552 calls, including the development replay. A separate null-seed implementation check added four calls. These are mathematical-oracle experiments, not physical observations.

## 5. Two decisive obstructions keep the high-dimensional claim honest

### The old conditional inverse is genuinely unstable

Take the legitimate affine source and exactly Gaussian output

\[
X=\alpha G+\beta Z,
\qquad \alpha^2+\beta^2=1.
\]

If corrections are restricted to \(u=\delta_ZJ\), the full scalar linearization becomes

\[
\mathcal LJ
=
\beta(N_Z+2)J+\alpha\delta_Z\partial_GJ.
\]

For the norm-one residual

\[
R_N=\frac{\operatorname{He}_N(G)}{\sqrt{N!}},
\]

the inverse obeys

\[
\boxed{
\|J_N\|_2
\ge
\frac{\beta^{-N-1}}{(N+1)(N+2)}.
}
\tag{12}
\]

The exact Hermite recurrence was checked with rational arithmetic through degree 128. For \(\alpha=0.6,\beta=0.8\), the inverse norm is approximately \(3.8\times10^3\) at degree 64 and \(1.5\times10^9\) at degree 128.

Thus a degree-uniform \(L^2\) inverse—or one with any fixed finite Sobolev loss—is false on that entire residual class.

This is an obstruction to the proposed inverse interface. It is not a lower bound for N687: affine means are available from \(g(0)\), and arbitrary Hermite residuals need not arise in an actual generated Newton sequence.

### Scalar moment correction has a large vector variance cost

A direct vector version estimates covariance by

\[
\widehat V=\frac{\Delta\Delta^\top}{2}.
\]

Its Gaussian correction has second moment

\[
\mathbb E\|\widehat VZ/2\|^2
=
\frac{\mathbb E\|\Delta\|^4}{16}.
\]

Already for the conservative affine field \(g(x)=\ell x\), this equals

\[
\boxed{\frac{\ell^4d(d+2)}4.}
\tag{13}
\]

So the straightforward implemented correction pays a quadratic dimension factor. This is a limitation of that estimator and proof interface, not a target lower bound or a TV conclusion from covariance.

There is also a genuine nonlinear geometric obstruction to simply rotating the joint inverse into affine coordinates. A smooth compactly supported conservative construction gives horizontal fields

\[
V_i=\partial_{Z_i}+K_i\cdot\nabla_G
\]

whose bracket is locally

\[
[V_1,V_2]
=
\eta^2(y\partial_x-x\partial_y).
\]

It is nonzero and outside their horizontal span at \((1,0)\). The source can be scaled to have arbitrarily small Lipschitz constant. The coupled geometry therefore needs an actual argument; a variable version of the affine rotation does not suffice.

## 6. The predictive-count alternative also yielded a useful distinction

I examined the second interface rather than assuming the Gaussian route must win.

An explicit rank-two classical CP family has observable core

\[
H=\begin{pmatrix}1&1\\0&q\end{pmatrix}.
\]

Its inverse norm grows like \(1/q\), while its exact physical norm in observable coordinates is

\[
\|x\|_Q=|x_0-x_1|+|x_1|
\le 3\|x\|_\infty,
\]

independently of \(q\).

Thus inverse-core norm inflation can be artificial. Nevertheless, learning a parameter accessible only after entering the rare state requires

\[
\Omega\!\left(
\frac{\log(1/\alpha)}{q\varepsilon^2}
\right)
\]

primitive calls for a guarantee on every normalized reachable input. A better norm cannot supply observations of an unvisited mode.

For the actual reset state, an occupation-sensitive coupling gives a nonvacuous whole-transcript guarantee. In the constructed family, 5,000 reset-and-trigger trials with zero successes, 99% confidence, and per-call abort probability \(0.1\) give an all-policy bound of approximately

\[
0.0082174,
\]

while the rare-state read parameter remains entirely unlearned. The normalized rare-state bound remains \(0.9\).

This positive result assumes the explicit two-state topology and the stated stopping-clock contract. A conventional controlled Markov/HMM learner with the same topology can reproduce it. The general unknown-CP problem still needs an acquired positive observable geometry. The complete argument is in RARE_MODE_CONFIDENCE_THEOREM.txt[RARE_MODE_CONFIDENCE_THEOREM.txt](sandbox:/workspace/scratch/810b1ee40202/research/predictive_work/RARE_MODE_CONFIDENCE_THEOREM.txt).

## 7. Comparison and the exact remaining obligation

The primary-source check found substantial established machinery around this construction. Courtade–Fathi–Pananjady already use coercive variational methods to construct Stein kernels; Fathi constructs positive symmetric kernels through moment maps; Detommaso and colleagues develop functional Stein variational Newton methods and Galerkin implementations. The contribution here should therefore be assessed as the **specific joint-divergence inverse, its weak full-law cancellation, and its charged acquisition interface**, not as the invention of variational Stein methods. Historical novelty has not been established. [arxiv.org](https://arxiv.org/pdf/1703.07707?utm_source=chatgpt.com)

The strongest computational comparisons remain the packet’s fixed-positive-exponent compiler under its actual proof status, bounded-input FORS with its tail and center-acquisition costs, and Gaussian-cloud correction. FORS already supplies polylogarithmic accuracy dependence under suitable light-tailed stochastic-query assumptions; those assumptions cannot be replaced silently by a dimension-free norm bound for \(g(G)\). [arxiv.org](https://arxiv.org/html/2602.14342v2?utm_source=chatgpt.com)

The main unresolved issue is now precise:

\[
r\le\sqrt d\,\ell^2
\quad\Longrightarrow\quad
\text{the current general one-step bound is }O(d\ell^4).
\]

The inverse constants are dimension-free, but the discrepancy being squared is the **total Frobenius discrepancy**. The proof also does not yet show that the corrected vector retains a bounded, coercive Stein representation that can be reused.

**The next scientific obligation is to acquire a reusable high-dimensional correction from legal source values whose full equation residual and actual correction variance contract at the required dimension scale, then prove stable iteration with an every-execution polylogarithmic query cap.** All coefficient acquisition, adaptive source dependence, arithmetic, storage, precision, and stopping tails must be included.

The work establishes an analytical inverse and full-law correction mechanism, an executed acquisition-to-law pipeline on a nonlinear fixture, and exact failures of tempting shortcuts. It does not yet establish the civilisation-scale computational capability sought by the case.