# Unknown heterogeneous conservative loss: the same density path receiver

30 October 2026. Extension of `RECIPROCAL_WAVE_COUNTER.md`. The native coefficient remains a homogeneous unknown scalar `R=rI`. The auxiliary coefficients `Gamma_i` may now be arbitrary frozen unknown values in `[0,gamma_+]`, with the actual conservative force/noise connection of equation (1) in that file. This is not an extension to arbitrary native R preserving the same heat equation.

The exact invariant law, native-current identity, native response, passive spectrum bound and rare-current result in the main file already hold for these coefficients. The remaining issue is whole density paths and initial transients when Fourier modes of the auxiliary loss do not diagonalize. The following argument closes it without assuming a homogeneous Gamma or learning it.

## 1. Exact corrected visible equation

Write `K=B Gamma B^*` and `L=BB^*`. Combining the actual native velocity and auxiliary momentum equations gives

\[
r\,dx=-Lx\,dt-\tau\,d(Bv)-(g/a)dp-(g/a)Kp\,dt
+\sqrt{2r}B\,dW+(g/a)\sqrt2 B\sqrt\Gamma\,dV.                 \tag{1}
\]

No hidden operation is eliminated in this identity. In particular it retains both initial-to-final momentum terms and the accumulated conservative-loss term.

Let f be a normalized nonzero density Fourier vector, so `Lf=ell f` and `||f||=1`. Let `X_f=<f,x>`. Couple a conventional native overdamped density mode to the same mathematical W by

\[
dy_f=-(\ell/r)y_fdt+\sqrt{2/r}\langle B^*f,dW\rangle,
\qquad y_f(0)=X_f(0).                                       \tag{2}
\]

This is a proof coupling between supplied laws, not an experiment branching one microscopic specimen. The exact difference obeys

\[
X_f(t)-y_f(t)+\frac\ell r\int_0^t[X_f(s)-y_f(s)]ds=E_f(t),     \tag{3}
\]

where

\[
\begin{aligned}
E_f(t)={}&-\frac\tau r\langle B^*f,v_t-v_0\rangle
-\frac g{ar}\langle f,p_t-p_0\rangle\\
&-\frac g{ar}\int_0^t\langle Kf,p_s\rangle ds
+\frac g{ar}\sqrt2\int_0^t\langle B^*f,\sqrt\Gamma\,dV_s\rangle.
\end{aligned}                                                \tag{4}
\]

## 2. The conservative-loss integral is small without mixing

Under the actual stationary Gaussian law, take `h=<f,p>` and let S be the symmetric part of the full generator. Then

\[
Sh=-\langle Kf,p\rangle,
\qquad \mathcal D(h)=\langle f,Kf\rangle
\le\gamma_+\ell.                                            \tag{5}
\]

For the forward martingale `M_t=h_t-h_0-int_0^t Lh`, and the corresponding backward martingale under the stationary adjoint process,

\[
2\int_0^t\langle Kf,p_s\rangle ds=M_t+\widehat M_t.
\]

Both martingales have expected squared modulus `2t D(h)` (apply the real and imaginary identities if f is complex). Therefore

\[
\mathbb E\left|\int_0^t\langle Kf,p_s\rangle ds\right|^2
\le2t\langle f,Kf\rangle.                                    \tag{6}
\]

This is the usual forward/backward energy estimate, used with the actual full generator. It requires stationarity but neither ergodicity nor a spectral gap. The adjoint here is a mathematical time-reversal proof device; no physical adjoint experiment is being asserted.

For deterministic visible initialization and independent thermal auxiliaries, the centered covariance of this linear path functional is no greater than its stationary value, by Gaussian conditioning. Thus (6) also bounds its centered fluctuations in that initialization.

The two endpoint terms in (4) have variances bounded by constants times ell and kappa, respectively. The final auxiliary martingale has variance at most `C kappa t gamma_+ ell`. Combining these with (6), for a fixed macroscopic Fourier index k and `t<=N^2T`, gives

\[
\sup_{t\le N^2T}\mathbb E|E_f(t)-\mathbb E E_f(t)|^2
\le C_T[\ell+\kappa(1+k^2)].                                 \tag{7}
\]

This is a supremum of second moments, not an unproved bound on the expected path supremum. That distinction causes no gap: tightness comes independently from the actual passive current spectrum in the main proof.

Solving the scalar Volterra equation (3) gives

\[
X_f(t)-y_f(t)=E_f(t)-\frac\ell r
\int_0^t e^{-\ell(t-s)/r}E_f(s)ds.
\]

The convolution kernel has L1 norm at most one. Hence the centered difference has the same bound (7), up to a factor four. This proves convergence of all joint finite-dimensional density distributions to the standard native OU field for arbitrary Gamma in the given class. It explicitly controls the retained initial momenta.

## 3. Nonflat means and full paths

For a deterministic visible profile of energy at most CN, the unforced deterministic mean energy decreases. In particular

\[
\int_0^\infty \bar p_s^TK\bar p_sds\le CN.
\]

Test (4) with the empirical-density vector `phi=f/sqrt(N)`. The native endpoint term is `O(sqrt(ell))`, the auxiliary endpoint term is `O(g)`, and Cauchy--Schwarz gives

\[
\left|g\int_0^{N^2T}\langle K\phi,\bar p_s\rangle ds\right|
\le g\sqrt{CN}\sqrt{N^2T\langle\phi,K\phi\rangle}
\le C_T g|k|.                                                \tag{8}
\]

All these terms vanish for fixed k when `kappa_N ->0`. Thus the mean obeys the same nonflat heat limit, not merely the stationary zero profile.

The full native matrix impedance remains passive, giving `S_v<=2R^(-1)` and therefore the same Sobolev/time increment bound as in the main file. It applies to the centered process after conditioning. The controlled and reference density paths are tight in `C([0,T],H^(-p))`, for any p>3/2. Their coupled finite-dimensional difference tends to zero by (7). Consequently the coupled centered difference converges to zero in this whole path space, and the controlled density converges to the ordinary OU field with its actual initial condition. Smooth nonflat mean profiles follow by the same energy/tightness argument and Fourier-tail approximation.

## 4. The rare-history transfer is genuinely stronger than a CLT

The coupled centered path difference is Gaussian. A sequence of Gaussian random elements converging weakly to zero has converging norm moments, by the common Fernique bound for a tight Gaussian family. Its weak variance

\[
\sigma_N^2=\sup_{\|\Lambda\|\le1}\operatorname{Var}\Lambda(X_N-y_N)
\]

therefore tends to zero, as does its expected norm. Borell's inequality implies, for every delta>0,

\[
\frac1N\log\mathbb P\bigl(\|X_N-y_N\|>\delta\sqrt N\bigr)
\longrightarrow-\infty.                                    \tag{9}
\]

Here X_N,y_N denote the centered fluctuation-field embeddings. After dividing them by sqrt(N), (9) is exponential equivalence of the **macroscopic density paths** at speed N. The nonflat deterministic mean difference tends to zero and introduces no random tail.

Exact native continuity reconstructs every nonconstant integrated-current mode from the density path. The remaining constant current is superexponentially zero under `kappa_N N^2 -> infinity` by the actual current bound in the main file. Therefore its joint action (31), with zero harmonic current, extends to arbitrary frozen bounded conservative Gamma. The initial profile and complete current topology stay as stated there. This does not include the entire bath record or conditioning on future controller noise.

The required scales remain only `kappa_N ->0` and `kappa_N N^2 ->infinity`. Known or unknown bounded local conservative loss does not need a vanishing precision budget. Grounded auxiliary loss is still excluded by the distinct failure already proved, and arbitrary heterogeneous native R still requires the true metric-projected receiver.

## 5. Scope and provenance

The invariant law, positive-real impedance and current counting are inherited from the actual equations of the main file. The forward/backward martingale identity is established reversible-energy machinery, not a new theorem being claimed. The constructive addition is its use to close the heterogeneous conservative-loss receiver, including its actual initial momenta and Gaussian rare-history transfer. No new fixture or physical experiment is used to replace that proof.
