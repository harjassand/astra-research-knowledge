# Exact native-family obstructions

All statements below were derived in this investigation. No claim of historical originality is made.

## 1. Isotropic simplex: exact cost of ordinary random chords

Let \(N=n+1\), let \(H=\{z\in\mathbb R^N:\sum_i z_i=0\}\), and let \(P\) be uniform on \(\Delta_N=\{p_i\geq0,\sum_i p_i=1\}\). Set

\[
X=\sqrt{N(N+1)}\left(P-N^{-1}{\bf1}\right).
\]

Then \(X\) is isotropic on the \(n\)-dimensional Euclidean space \(H\), since \(\operatorname{Cov}P=[N(N+1)]^{-1}P_H\).

Fix a unit \(u\in H\), put \(A=\sum_i(u_i)_+=\sum_i(-u_i)_+=\|u\|_1/2\), and use the unscaled simplex coordinates. Distances along \(u\) to the two endpoints of the chord through \(P\) are

\[
T_+=\min_{u_i<0}\frac{P_i}{-u_i},\qquad T_-=\min_{u_i>0}\frac{P_i}{u_i}.
\]

Uniform simplex volume scales as the \(n\)-th power of its total slack, so for \(s,t\geq0\),

\[
\mathbb P(T_+\geq s,T_-\geq t)=(1-A(s+t))_+^n.
\]

For \(n\geq2\), differentiation gives joint density \(n(n-1)A^2(1-A(s+t))^{n-2}\) on \(s,t>0,s+t<1/A\). Hence with \(L=T_++T_-\),

\[
\mathbb E L^k=n(n-1)A^2\int_0^{1/A}\ell^{k+1}(1-A\ell)^{n-2}\,d\ell
=\frac{(k+1)!n!}{(n+k)!A^k}.
\]

In particular \(\mathbb E L^2=6/[N(N+1)A^2]\). The \(n=1\) case has deterministic \(L=1/A\) and the same second-moment formula. After isotropic scaling, the conditional line-coordinate variance is the squared chord length divided by 12, yielding the exact identity

\[
\mathbb E_X s_u^2(P_{u^\perp}X)=\frac1{2A^2}=\frac2{\|u\|_1^2}.
\tag{1}
\]

Let \(P_{HR}\) be ordinary uniform-direction, uniform-chord heat bath. Its Dirichlet form is \(\mathcal E_{HR}(f)=\mathbb E_u\mathbb E_Y\operatorname{Var}(f\mid Y)\). For \(f=a\cdot X\), (1) gives

\[
\mathcal E_{HR}(a\cdot X)=\mathbb E_u\frac{2(a\cdot u)^2}{\|u\|_1^2}
=\frac{2|a|^2}{n}\mathbb E_u\|u\|_1^{-2}.
\tag{2}
\]

The final equality follows because the matrix inside the expectation is invariant under every coordinate permutation; its restriction to \(H\) is scalar, and its trace determines that scalar.

The lower bound \(\|u\|_1^2\leq N\) gives \(\mathbb E\|u\|_1^{-2}\geq1/N\). Interpolation gives \(\|u\|_2^3\leq\|u\|_1\|u\|_4^2\), hence \(\|u\|_1^{-2}\leq\sum_i u_i^4\). A uniform unit vector on \(H\) has

\[
\mathbb E\sum_i u_i^4=\frac{3n}{N(n+2)}.
\]

Since \(\operatorname{Var}(a\cdot X)=|a|^2\), every nonzero affine test has the same Rayleigh quotient \(r_n\), with

\[
\frac2{n(n+1)}\leq r_n\leq\frac6{(n+1)(n+2)}.
\tag{3}
\]

Thus the spectral gap is at most \(O(n^{-2})\). Isotropic covariance alone cannot imply an \(\Omega(n^{-1})\) gap for ordinary random-direction chord refresh. Choosing simplex-adapted edge directions would be a different operation and would require its own general construction and analysis.

## 2. A ball hides nonlinear block-refresh slowness from all linear tests

Let \(n=2m\), and let \((X,Y)\in\mathbb R^m\times\mathbb R^m\) be uniform in a ball of radius \(R\). Refresh exactly one of the two blocks conditionally, each with probability 1/2. Denote the transition operator by \(P\).

Every linear function has \(P\ell=\ell/2\), so its Rayleigh quotient is \(1/2\). This remains true after isotropic scaling \(R^2=n+2\).

Put \(A=|X|^2/R^2\), \(B=|Y|^2/R^2\). Their joint density is proportional to \(a^{m/2-1}b^{m/2-1}\) on \(a,b\geq0,a+b\leq1\); equivalently \((A,B,1-A-B)\) has Dirichlet parameters \((m/2,m/2,1)\). Therefore

\[
\mathbb E[A\mid B]=r(1-B),\quad \mathbb E[B\mid A]=r(1-A),\quad r=\frac m{m+2}.
\]

For the centered quadratic \(f=A-B\), direct calculation gives

\[
Pf=\frac12\{r-(r+1)B+(r+1)A-r\}=\frac{m+1}{m+2}f.
\]

Its Rayleigh quotient is \(1/(m+2)\), so the spectral gap is at most this. The ratio between this nonlinear quotient and the linear quotient tends to zero as \(m\to\infty\), on the most elementary convex body. Any proposed proof based solely on first-chaos/covariance normalization of a higher-rank refresh fails this test.

This does not disprove the rank-one normalized-chord conjecture. It proves that its affine identity cannot substitute for nonlinear analysis.

## 3. Inverse-chord-square clocks have infinite stationary mean rate

Take the uniform measure on the square \((-1,1)^2\), and fix any line direction not parallel to an edge. Near a corner, lines orthogonal-coordinate distance \(r>0\) from the extreme supporting line cut chords of length \(\ell(r)=c(u)r\), until the next combinatorial change. The projected marginal density is \(\ell(r)/4\). Conditional variance is \(s^2(r)=\ell(r)^2/12\).

The stationary average of the proposed refresh rate \(s^{-2}\), in this corner interval, is therefore

\[
\int_0^\varepsilon \frac{12}{\ell(r)^2}\frac{\ell(r)}4\,dr
=\frac3{c(u)}\int_0^\varepsilon\frac{dr}{r}=\infty.
\]

For uniform directions the exceptional edge-parallel directions have measure zero, so Tonelli gives infinite mean rate after direction averaging too. Affine rescaling to an isotropic square does not change divergence.

This does **not** prove that the mathematical Dirichlet form is ill-defined: for Lipschitz \(f\), the quotient \(\operatorname{Var}(f\mid Y)/s^2(Y)\) is bounded by its directional Lipschitz constant squared. Nor does infinite mean rate alone prove pathwise explosion. It does prove that an asserted finite expected number of exact conditional-refresh events per unit stationary time is false. An efficient simulation theorem would need a different finite-cost realization or a truncation argument with an explicit convergence and cost analysis.

## 4. A natural log-concave Stein metric separates matrix means from pathwise norms

Let \(E_i\) be independent rate-one exponentials and \(X_i=E_i-1\). This product measure is isotropic and log-concave. Integration by parts proves that

\[
\tau(X)=\operatorname{diag}(E_1,\ldots,E_n)
\]

is a positive Stein kernel: \(\mathbb E[X_i f(X)]=\mathbb E[E_i\partial_i f(X)]\). In particular

\[
\mathbb E\tau=I,\qquad \mathbb E\tau^2=2I.
\]

But exponential order statistics give, with \(H_n=\sum_{k=1}^n k^{-1}\) and \(H_n^{(2)}=\sum_{k=1}^n k^{-2}\),

\[
\mathbb E\|\tau\|_{op}=H_n,\qquad
\mathbb E\|\tau^2\|_{op}=H_n^2+H_n^{(2)}.
\]

Proof: \(\max_i E_i\) is distributed as a sum of independent exponentials with rates \(1,2,\ldots,n\), so its mean and variance are \(H_n\) and \(H_n^{(2)}\). Consequently no universal constant converts \(\|\mathbb E\tau^2\|_{op}\) into \(\mathbb E\|\tau^2\|_{op}\), even for this canonical native family.

Even in dimension one, \(\int \tau(f')^2d\mu\leq C\int(f')^2d\mu\) is false uniformly: choose a smooth derivative supported where \(E\in[R,R+1]\); the quotient is at least \(R\). A weighted inequality cannot be unweighted by averaging the coefficient independently of the gradient.

## 5. Positive Stein identity alone is not a weighted spectral-gap theorem

For standard Gaussian \(Z\in\mathbb R^2\), put \(v(Z)=(Z_2,-Z_1)\) and \(\tau(Z)=v(Z)v(Z)^T\). Direct differentiation gives \(\operatorname{div}(\rho\tau)=-Z\rho\), where \(\rho\) is Gaussian density. Also \(\mathbb E\tau=I\).

For every smooth radial function \(f\), however, \(v\cdot\nabla f=0\), hence \(\int\nabla f^T\tau\nabla f\,d\gamma=0\), while nonconstant radial functions have positive variance. Thus the positive Stein identity and correct matrix mean do not themselves imply \(\operatorname{Var}f\leq\int\nabla f^T\tau\nabla f\).

For a strictly positive example, \(\tau_\varepsilon=\varepsilon I+(1-\varepsilon)vv^T\) is a positive-definite Stein kernel with mean \(I\). For \(f=|Z|^2\), its weighted Rayleigh quotient is \(2\varepsilon\). Any proof invoking a canonical moment-map kernel must use its additional structure explicitly, not merely the generic Stein identity.

## 6. Fiber centering has unbounded distortion already on a half-disk

Let \(K=\{(x,y): -1<x<1,-\sqrt{1-x^2}<y<0\}\). Its vertical-fiber midpoint is \(m(x)=-\tfrac12\sqrt{1-x^2}\). The measure-preserving centering map is \(T(x,y)=(x,y-m(x))\), taking \(K\) to an ellipse.

But \(m'(x)=x/[2\sqrt{1-x^2}]\) is unbounded, and

\[
DT=\begin{pmatrix}1&0\\-m'(x)&1\end{pmatrix}.
\]

Hence this map has no bounded pointwise metric distortion and no universal pullback comparison of all smooth Dirichlet energies; localized high-frequency tests detect the arbitrarily large singular value of \(DT\). Fixed nonsingular affine transformations before and after the map cannot remove the divergence. This refutes the free-cost transport argument, not every possible spectral monotonicity statement about symmetrization.

## 7. Trace-normalized entropy misses one bad coordinate

Let \(\mu_n\) be the product of one centered rate-one exponential and \(n-1\) standard Gaussians. It is isotropic and log-concave. Relative entropy to the standard Gaussian is

\[
D(\mu_n\|\gamma_n)=\tfrac12\log(2\pi)-\tfrac12,
\]

independent of \(n\). Nevertheless its Poincare constant is at least four. To see the lower bound, for an exponential variable \(E\) use \(f(E)=e^{\alpha E}\), \(0<\alpha<1/2\), for which

\[
\frac{\operatorname{Var} f}{\mathbb E(f')^2}=\frac1{(1-\alpha)^2}\longrightarrow4.
\]

Tensoring these tests with constants in the Gaussian coordinates preserves the quotient. Therefore a bound \(C_P(\mu_n)-1\leq C D(\mu_n\|\gamma_n)/n\) is false for every fixed \(C\). A trace-averaged non-Gaussianity budget cannot certify proximity of the worst spectral mode to its Gaussian value.
