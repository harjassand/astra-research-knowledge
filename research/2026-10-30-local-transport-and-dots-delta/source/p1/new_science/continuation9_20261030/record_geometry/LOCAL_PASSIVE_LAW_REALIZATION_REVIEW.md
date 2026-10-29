# Receiving review: local passive realization of an unknown transport law

Existing record-geometry role. This is an actual-file mathematical review, not a review of a proposal or an apparatus validation. No root input was edited. No additional numerical fixture was needed for the two corrections below.

## Reviewed inputs and disposition

The original root file is `../LOCAL_PASSIVE_LAW_REALIZATION.md`, SHA-256

`946ecd0eb2463bfa88bb1b27f0062bc1feca1eb679c49430af8fbf5cfae59148`.

Its exact bytes are preserved as `LOCAL_PASSIVE_LAW_REALIZATION_REVIEWED_946ecd0eb246.md`.

The receiving correction is `../LOCAL_PASSIVE_LAW_REALIZATION_CORRECTION.md`, SHA-256

`db9576980955f626d66fb8430cd85ed9e4ed3ec37c1bb66c4ee48a9b5d34f2cc`.

Its exact bytes are preserved as `LOCAL_PASSIVE_LAW_REALIZATION_CORRECTION_REVIEWED_db9576980955.md`.

**Accepted together, at the stated stationary Gaussian port and finite-observation interface.** The matrix Schur estimate, passive controller elimination, thermal spectrum identity, and Gaussian KL calculation check out. The original file alone needs the correction's explicit out-of-band supplier for a leaking measurement filter and its fixed-positive-wave-speed qualification for the scaling corollary. Neither correction changes the central finite-band operator estimate.

## 1. The operator ordering and finite-band estimate

Let `Z=R+K/(i omega)+C_kappa`, with `K=B* H B`, `P=proj ker A`, and `Q=I-P`. The premise `BP=0` gives `KP=PK=0`; therefore the off-diagonal blocks of Z are exactly those of R. No commutativity between R and P is required.

The elimination of the controller is correct for rectangular A. On an eigenvector of `L=A* A` with eigenvalue ell, it gives

\[
c_\ell(z)=\kappa\frac{z+\gamma\ell}{z^2+\gamma z\ell+a^2\ell}.
\]

The expression for its nonnegative real part in equation (7) follows directly. The P block is `kappa/z`; the controller has no Q-P mixing. The covariance and dimensions of the supplied conserving noise `sqrt(2T gamma) A dV` agree with the `gamma AA*` damping in p.

For the band in (10), `a^2 ell-omega^2 >= a^2 ell/2`. Thus

\[
\|C_Q\|\le\frac{2\kappa}{a^2}
\left(\gamma+\frac{\Omega}{\lambda}\right)=d.
\]

The Neumann bound for `H_P=PRP+kappa/(i omega)` is `||H_P^{-1}||<=2 Omega/kappa=e`.

The potentially delicate non-Hermitian Schur step is valid. For `p=-H_P^{-1}R_PQ q`, the P component of `Z(q,p)` vanishes. Hence

\[
\Re(q^*Sq)=\Re((q,p)^*Z(q,p))
\ge r_-(\|q\|^2+\|p\|^2).
\]

This proves `||S^{-1}||<=1/r_-` directly; it does not require treating the Schur correction as a small perturbation. The two off-diagonal inverse blocks retain their ordered products `-S^{-1}R_QP H_P^{-1}` and `-H_P^{-1}R_PQ S^{-1}`. Their norms, and the additional ordered product in the P-P inverse block, give exactly the four terms summed in (11)-(12).

The constrained target is consequently the restricted native impedance. The static positive-resistance formula

\[
D-DU(U^*DU)^{-1}U^*D
\]

is correct. It generally differs from `QDQ`; the proof does not replace the native metric by a Euclidean one.

## 2. Response, thermal noise, and stability scope

With the supplied independent Gaussian thermal baths and their actual stationary initialization, the controller's force spectrum is `2T Re C_kappa`. The matrix identity has the correct order:

\[
Y(Z+Z^*)Y^*=Y+Y^*,\qquad
S_v=2T\Re Y.
\]

Indeed `YZY*=Y*` and `YZ*Y*=Y`. The same calculation on Q yields the ideal spectrum. Neither reciprocity of the unknown R nor a finite-dimensional realization of its hidden memory is needed for this identity.

The estimate proves invertibility and coercivity in the certified band. It is not, by itself, a theorem that every abstract passive boundary-value matrix has a well-defined globally stationary causal realization. The root text separately supplies the actual causal port, stationary initializer, and absence of a visible undamped current mode. Those are load-bearing premises and are retained in this acceptance.

In particular, independent thermal q and p marginals alone do not manufacture the complete stationary history of a colored native bath after interconnection. A warranted complete joint stationary law, or a valid physical preparation establishing it, is needed for the stationary convolution and spectrum statements. The file already states that conditional future bath law and initial-law interface. Its explicit separation of stationary forcing from an unpaid finite-time transient is appropriate.

The exact path identity for `P J` follows by applying P to the q equation. With the stated equilibrium q covariance, Cauchy-Schwarz gives the printed `4T/kappa` endpoint variance bound. A whole-horizon supremum needs an additional path estimate, as the file says.

## 3. Required correction: a leaking filter needs an out-of-band supplier

The in-band hypotheses (2) do not imply equation (18) when `A_out>0`. The coefficient `4T/r_-` in that equation requires the extra global-coercivity alternative explicitly stated in Section 5, or another warranted bound on the actual out-of-band spectral difference. This is not just a technical issue concerning very high frequencies.

Here is an analytic passive counterexample to the unqualified extrapolation. Embed a scalar P current into a two-current system with `A=(0,1)`, `B=0`, and a positive constant resistance on the Q current. On P choose

\[
R_P(z)=\delta+\frac{r_0}{1+\tau z}+\mathcal L z,
\qquad
\mathcal L=\frac{r_0\tau}{1+\omega_0^2\tau^2}
             +\frac{\kappa}{\omega_0^2},
\]

where all parameters are positive and `omega_0` lies outside the measured band. This is a causal positive-real impedance. At `omega_0`, the imaginary part of `R_P(i omega)+kappa/(i omega)` cancels exactly, and

\[
\Re Y_P(i\omega_0)
=\frac{1}{\delta+r_0/(1+\omega_0^2\tau^2)}.
\]

For example fix `Omega=1/10`, `tau=10`, `r_0=kappa=a=lambda=1`, take `omega_0>=1`, and let `0<delta<=0.01`. The in-band real-part bound `r_-=1/2` and norm bound `r_+=1.2` hold uniformly, and both conditions (10) hold. As `omega_0` grows and delta decreases, the outside-band current spectrum becomes arbitrarily large. The ideal P current is zero. A normalized observation filter concentrated near that outside resonance violates the proposed fixed outside-band coefficient. Strictly positive delta makes the passive closed-loop scalar realization damped; the example does not rely on an excluded visible undamped mode.

The root correction gives precisely the needed repair:

\[
\delta_\Sigma\le 2T\Delta A_{\rm in}
+\int_{\rm outside}\|F(\omega)\|_{\rm op}^2
 E_{\rm out}(\omega)\,\frac{d\omega}{2\pi},
\]

with an actually warranted envelope `E_out`, or `A_out=0`. Under global coercivity, the printed constant `4T/r_-` follows because each admittance has norm at most `1/r_-`. The correction explicitly notes the spectral leakage of a real finite-duration filter and does not infer an envelope from a finite calibration grid. **This correction is accepted.**

## 4. Required correction: the asymptotic wave speed is positive uniformly

The core formulas (10)-(12) remain valid for every positive a. However, the subsequent assertion `Delta=O(sqrt(lambda))` for `Omega=O(lambda)` and `kappa~sqrt(lambda)` requires a fixed a, or a uniform positive lower bound on a, in addition to uniform resistance bounds and bounded gamma.

For example, take `a^2=lambda`, `Omega=c lambda` with `0<c<1/sqrt(2)`, `kappa=sqrt(lambda)`, and `gamma=0`. The conditions (10) still hold for small lambda, but

\[
d=2c/\sqrt\lambda,
\]

which does not vanish. A controller Q mode with eigenvalue lambda then has impedance of order `lambda^{-1/2}` at this frequency, so even the intended convergence need not occur. A mere upper bound on a is insufficient.

The root correction explicitly fixes this quantifier and directs a varying-a family back to the full estimates (10)-(11). **This correction is accepted.**

## 5. Finite-record law and retained information

After a valid covariance error has been supplied, the Gaussian KL direction and constants in (19) are correct. If the ideal measured covariance is `Sigma_*>=sigma^2 I`, write

\[
E=\Sigma_*^{-1/2}(\Sigma-\Sigma_*)\Sigma_*^{-1/2}.
\]

Then `||E||<=a_0`, and the actual-to-ideal covariance contribution is
`(1/2) sum_j [u_j-log(1+u_j)]`. For `|u_j|<=a_0<1`, this is at most `d a_0^2/[4(1-a_0)]`; the mean contribution is bounded by `||delta_mu||^2/(2 sigma^2)`. Pinsker gives the stated TV estimate.

This is the law of the supplied finite linear measurement vector with its actual independent sensor noise. It is not an estimate for noiseless full trajectories. If a nontrivial P component is observed without noise, the ideal component is identically zero while the actual finite-kappa thermal Gaussian component can have nonzero variance. Their laws are then singular, despite small in-band operator error. The root text correctly uses this as a possibility, not as an assertion about every filter or a zero-temperature experiment.

Conditional application with a retained old record is valid when every conditional port, preparation, and future source law satisfies the same hypotheses. Integrating those conditional TV bounds preserves that same old record. Conditioning on a record that reveals future noise or changes the conditional source law cannot be justified merely by the unconditional spectrum. Arbitrary feedback is not covered by this open-loop receiver. The original text already preserves these qualifications.

## Final receiving status

The two exact reviewed files together supply a valid conditional finite-band response/noise theorem and a finite-precision Gaussian measurement receiver. The out-of-band and fixed-a corrections are substantive and incorporated by the separately preserved addendum. No new claim is made here about acquisition of all-frequency port bounds, nonlinear hidden dynamics, arbitrary adaptive records, a manufactured apparatus, or historical priority.
