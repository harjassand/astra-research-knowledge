# Receiving review: selective two-ring transport coupling

30 October 2026. Reviewer: the existing physical-mechanism role. Actual-file review of the local signed-ladder construction, its density and current path receiver, and its physical force port. No additional fixtures or agents were used.

## Reviewed input and decision

Source: `continuation9_20261030/SELECTIVE_TRANSPORT_COUPLING_AND_ACTION.md`.

SHA256: `42b5d5537a2f357a05a8b1ff55d292414e23c84d50d99bf50d3527073afc3ce2`.

The exact input is preserved as `SELECTIVE_TRANSPORT_COUPLING_REVIEWED_42b5d5537a2f.md`, with its path, byte count, and hash in `SELECTIVE_TRANSPORT_REVIEW_INPUT.json`.

**Decision: accept the stated homogeneous-within-each-ring, conditionally Gaussian theorem and its actual supplied force ports.** I found no correction required. In particular, unknown unequal positive constants r_1 and r_2 do not invalidate the independent-density receiver, the common Brownian variance, or the forced-rate normalization. The input does not establish unchanged density histories for spatially heterogeneous resistance, non-Gaussian hidden kinetics, arbitrary retained initial records, or a finite-amplitude apparatus.

The claims of independent density histories are macroscopic path and large-deviation claims in the stated weak Sobolev topology. They are not equality or independence of the two microscopic density processes at finite N.

## 1. The local controller and proof-only corrector

The signed ladder has

\[
A^*A=\begin{pmatrix}L+I&I\\I&L+I\end{pmatrix},
\qquad L=B_N^*B_N.
\]

In the common/difference ring basis this is diag(L+2I,L). Its only kernel is the spatially constant difference vector h_N, and B annihilates that vector. Thus

\[
FA=BA^\dagger A=B,
\qquad F=B A^\dagger.
\]

For a spatial Fourier eigenvalue ell, the squared singular values of F on the two nonzero sectors are ell/(ell+2) and 1. At ell=0 the density map vanishes. Hence \(\|F\|\le1\), including the potentially singular long-wave sector. Also

\[
FAA^*F^*=(FA)(FA)^*=BB^*.
\]

This is precisely the identity needed for the loss estimate; no estimate of \(\|A^\dagger\|\) alone would suffice. F is used only to prove the receiver. The actual controller remains the bounded-range A and A* interconnection, with the local conservative loss AA* and its declared matched bath.

Multiplying the native equation by B and substituting F times the p equation reproduces source equation (8), with the stated signs and factors. Commutation of R with B is used here and is valid because each ring has a spatially constant resistance. The proof would not establish the same equation with scalar heat resolvents for arbitrary spatial disorder.

## 2. The additive-functional estimate and density comparison

For a normalized density Fourier vector f, let w=F*f. Then

\[
\|w\|\le1,
\qquad \gamma w^*AA^*w=\gamma\ell.
\]

Under the complete stationary Gaussian law, the symmetric part of the generator sends \(h=\langle w,p\rangle\) to \(-\langle\gamma AA^*w,p\rangle\). The forward and stationary adjoint-backward martingales sum to twice the integral of this latter quantity. Each martingale has second moment \(2t\gamma\ell\), so Cauchy--Schwarz gives exactly

\[
\operatorname{Var}\!\left(\int_0^t\langle\gamma AA^*w,p_s\rangle ds\right)
\le2t\gamma\ell.
\]

No mixing time, irreducibility of the conserved p sector, or physical adjoint operation is being assumed. The directions in ker A* decouple from this calculation. Conditioning the stationary process on the specified initial visible density reduces the covariance of each linear path functional; the nonzero deterministic mean must be treated separately, as the source does.

The native velocity endpoint has centered variance of order ell, the auxiliary endpoint of order kappa, and the loss integral and controller martingale each of order kappa times t ell. This gives the stated uniform-in-time second-moment bound

\[
C_T[\ell+\kappa(1+N^2\ell)]
\]

at physical times at most N^2T. The scalar Volterra resolvent has integral norm at most one, so it changes only the constant. This is a supremum of second moments; the source correctly obtains a path statement later rather than treating it as an expected supremum bound.

For the mean, the energy inequality bounds the loss integral by

\[
\frac{g}{\sqrt N}
\left(\int_0^{N^2T}p^*\gamma AA^*p\,dt\right)^{1/2}
\left(N^2T\gamma\ell\right)^{1/2}
\le C_TgN\sqrt\ell.
\]

The endpoint means have the stated orders. Thus the mean empirical difference vanishes for every fixed continuum Fourier label under precisely kappa going to zero; no stronger upper window such as kappa much smaller than N inverse is hidden in this argument.

## 3. Whole-path Gaussian exponential equivalence is justified

The complete native admittance has positive-real impedance with Hermitian part at least R. Including the auxiliary bath in the fluctuation-dissipation calculation is essential: the spectrum is \(2\operatorname{Re}Y\), not just the filtered native resistor noise. The matrix inequality

\[
2\operatorname{Re}Y\le2R^{-1}\le(2/r_-)I
\]

holds without commuting R with the ladder impedance. It gives the stated density increment bound. Together with Gaussian higher moments and Fourier weights, this supplies path tightness in C([0,T],H^{-s}), s greater than 3/2. Conditional initial covariance is smaller, while deterministic means are controlled by the energy and Fourier-tail estimates.

The actual and reference processes are coupled through the same mathematical native Brownian motion, with the actual auxiliary bath retained. Marginal tightness gives joint tightness; the corrected finite-mode second moments make every subsequential difference identically zero. The centered difference therefore converges to zero as a Gaussian random element of the path space.

For completeness, weak convergence to zero of a tight Gaussian sequence gives a uniform Fernique bound. Uniform integrability then makes both its expected norm and its second norm moment vanish. Its weak variance is bounded by the latter. Borell's inequality at a threshold of order sqrt(N) consequently yields a logarithmic probability divided by N tending to minus infinity. Adding a deterministically vanishing empirical mean difference does not change exponential equivalence. This closes the step from the fixed-mode comparison to the full macroscopic path claim.

The reference density noises are independent because the two native W blocks are independent. Consequently the two limiting heat fields and their density actions are independent even though the actual finite-N controller couples them.

## 4. Harmonic impedance and Brownian normalization

On spatially constant modes, the ladder eigenvalues are 2 for the common channel and 0 for the protected difference channel. Eliminating q,p gives

\[
c_2(\omega)=\kappa\frac{i\omega+2\gamma}
{2a^2-\omega^2+2i\gamma\omega},
\]

whereas the difference-channel impedance is \(\kappa/(i\omega)\). Native resistance in that basis has diagonal rbar and off-diagonal rdiff. Thus source equation (14) retains the unknown mismatch rather than discarding it.

At \(\omega=\Omega/N^2\), fixed nonzero Omega, the protected impedance diverges because N^2 kappa tends to infinity, while c_2 tends to zero because kappa tends to zero. The inverse therefore tends to diag(1/rbar,0). The uniform positive-real bound permits dominated convergence against the integrated-current spectral kernels, whose products are integrable both at zero and infinity.

The normalization is correct. Each total ring current is sqrt(N) times the integrated normalized harmonic velocity. Transforming back from the unit common vector gives the limiting covariance matrix

\[
\frac{2}{r_1+r_2}
\begin{pmatrix}1&1\\1&1\end{pmatrix}\min(t,s).
\]

Hence each ring receives the same Brownian motion with variance coefficient \(2/(r_1+r_2)\), as claimed. The spatial harmonic block is independent of all nonzero Fourier blocks under the actual Gaussian initialization and translation-invariant dynamics. This makes the common Brownian mode independent of both density fields, not merely uncorrelated at one time.

The increment spectrum supplies a uniform linear variance bound, and Gaussian fourth moments give continuous-path tightness. No uniform approximation of the harmonic impedance over all physical frequencies is needed.

## 5. The selected-current counter is strong enough for the action

Since A h_N=0, the exact counter is

\[
J_{1,\rm tot}-J_{2,\rm tot}
=\frac{\sqrt{2N}}g\,[h_N^*q(t)-h_N^*q(0)].
\]

Its variance is bounded by 8N/kappa. The passive increment bound and Gaussian metric entropy give the stated expected supremum, with logarithm \(\log(2+N^2\kappa)\). The ratio of this expected supremum to N^2 vanishes. Borell's exponent for an order-N^2 excess is of order kappa N^3; after division by speed N it diverges exactly when N^2 kappa tends to infinity. Therefore the equality of harmonic currents holds at the whole-path large-deviation scale. It is stronger than a final-time or typical-current statement.

Nonzero current modes follow from exact native continuity. The inverse discrete-gradient multipliers are bounded by C/|m| on resolved modes, and converge to the continuum inverse. One sufficient joint topology is the product of density and integrated-current C([0,T],H^{-s}) spaces, s greater than 3/2. The harmonic part is a finite-dimensional continuous path. Gaussian path tightness and finite-dimensional quadratic cumulants then identify the joint good rate, including its degenerate direction.

Writing \(j_a=j_a^\perp+I\), the two density actions contribute the ordinary zero-mean current costs. The common Brownian channel contributes

\[
\frac{r_1+r_2}{4}\int I^2dt.
\]

All cross terms vanish because \(j_a^\perp\) and the spatial density derivative have zero average. This exactly reconstructs source equation (18) on its equal-mean-current constraint. The rate extends to the full weak L2-controlled PDE image. Contracting over I leaves the sum of the two independent ordinary density rates.

## 6. Actual force, transient, work, and rate normalization

The physical input \(f_{a,i}(s)=F_a(s/N^2)/N\) becomes \(F_a/\sqrt N\) in the normalized harmonic coordinates. The macroscopic current derivative is sqrt(N) times the harmonic velocity. These factors cancel, giving the scaled transfer matrix in the source with no missing N or sqrt(2).

All auxiliary harmonic means start at zero, so the causal zero-state response to a force extended by zero into the past is the actual mean response, including charging. For an L2 force on the observation interval, extend it by zero outside that interval when using Plancherel; the future extension cannot affect the earlier causal response. Uniform passivity and pointwise scaled admittance convergence prove L2 convergence to

\[
I_0=(F_1+F_2)/(r_1+r_2).
\]

The integrated means converge uniformly by Cauchy--Schwarz. Spatially uniform forces act only on the harmonic block, so neither density law is changed. Deterministic forcing leaves every covariance unchanged.

The forced common rate is therefore the correctly normalized shifted Brownian rate. Direct expansion confirms the constant that would be incorrectly retained by merely restricting the original forced native rate:

\[
\sum_a\frac{r_a}{4}(I-F_a/r_a)^2
=\frac{r_1+r_2}{4}(I-I_0)^2
+\sum_a\frac{F_a^2}{4r_a}
-\frac{(F_1+F_2)^2}{4(r_1+r_2)}.
\]

The actual rate has minimum zero. This is the expected normalization for a changed physical law, not an unnormalized conditioning weight.

The work scaling also checks: \(W_a/N=F_a J_{a,\rm tot}/N^2\) for constant F_a. The input, output and dissipated native-work limits follow. At finite-N DC, c_2(0)=kappa gamma/a^2, so each per-bond current is

\[
\frac{f_1+f_2}{r_1+r_2+2\kappa\gamma/a^2}.
\]

The stated lossless result and the conservative-loss correction both have the correct factors. These work statements concern the declared native force interface. They do not account for every apparatus preparation, compliance, or external support cost, and the source appropriately does not call them apparatus-inclusive efficiency.

## 7. Physical and conditional scope retained

The construction supplies a matched reciprocal tap, a local signed-ladder wave interconnection, structurally conservative auxiliary damping, independent matched native and auxiliary baths, and a complete actual conditional initializer. These are stronger ports than knowledge of equilibrium weights. Their support and locality are genuine: F and A dagger are absent from the apparatus.

The preparation can be a product thermal auxiliary law with deterministic nonflat visible density; no long-range initial covariance is required for this declared Markovian supplier. It is still a paid preparation. An old record correlated with auxiliary coordinates can destroy the conditional law. Conditioning on a warranted frozen pair r_1,r_2 is legitimate, whereas averaging unknown resistances does not preserve a single Gaussian law or a fixed conditional rate function.

The theorem uses a fixed positive inertial response and white voltage baths; it does not claim a hard frequency cutoff. Gaussian storage is unbounded, and weak g requires actual matched gain, compliance and precision. An error that changes the protected counter cannot be discarded merely because it is small at a typical scale. The finite-duration isolated-bath program is a different supplier and is not silently composed with this resistor interface.

Accepted scientific consequence: a local autonomous signed-ladder controller links two collective native transport channels, retains a common force-responsive and noisy work channel, and preserves both independent nonflat density actions at the Gaussian macroscopic objective. This is a substantive distinction from pointwise gearing or cutting the native rings. It does not assert a new basic LC principle, new tight-coupling thermodynamics, particle-system generality, or practical superiority.
