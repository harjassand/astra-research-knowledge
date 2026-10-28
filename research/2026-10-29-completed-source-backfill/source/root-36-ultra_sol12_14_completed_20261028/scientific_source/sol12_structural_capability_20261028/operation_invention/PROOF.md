# Conditional trace readout without a pose estimate

This is a finite calculation and a conditional measurement construction. It does not acquire the constitutive law, bandwidth, field accuracy, trajectory sensor, or particle admission premises of the powder certificate. Generic intermodulation and Fourier demodulation are established methods. No historical priority or practical advantage is claimed.

## 1. Target and existing inputs

The desired new action is a covered measurement of electric-polarizability trace divided by mass on one moving, rotating conductor, without reconstructing its pose at every sign exposure. This quantity could feed the existing conditional closed-void receiver in current Astra technology T-powder-closed-void.

The governing source is research_account.tex, lines 70–183, pinned to public repository revision 8d51d60762b3ee28c10aaaa56e1b92da119dc1cc. Its scalar trace fields, fixed-configuration four-sign projection, and positive-exposure obstruction are existing inputs. They are not results of this work. Source acquisition and hashes are in sources/powder_source_receipts.json.

In the source's instantaneous free-space affine-field model,
\[
 E_{\rm ext}(x,t)=e(t)+G(t)x,\qquad G=G^T,\quad \operatorname{tr}G=0,
\]
and integration over the complete charge distribution gives
\[
 F(t)=q e(t)+G(t)p(t).
 \tag{1}
\]
For a fixed configuration, linear electrostatics gives
\[
 p(t)=p_q(t)+\alpha(t)e(t)+B(t):G(t).
 \tag{2}
\]
Here the time arguments allow prescribed translation and rotation. Treating(2) as instantaneous during that motion is an explicit input promise, not a consequence of a static electrostatic theorem. Retardation, conductivity memory, magnetic forces, finite-electrode images, and motion-induced constitutive changes have not been bounded.

Let d=e_x be the measured direction. Use the three symmetric trace-free matrices
\[
 G_1=\begin{pmatrix}1&0&0\\0&-1&0\\0&0&0\end{pmatrix},\quad
 G_2=\begin{pmatrix}0&1&0\\1&0&0\\0&0&0\end{pmatrix},\quad
 G_3=\begin{pmatrix}0&0&1\\0&0&0\\1&0&0\end{pmatrix}.
 \tag{3}
\]
These are exactly the gradients of the source's three harmonic quadratic potentials. They obey G_j d=e_j, so
\[
 d^TG_j\alpha e_j=\alpha_{jj},\qquad
 \sum_{j=1}^3d^TG_j\alpha e_j=\operatorname{tr}\alpha.
 \tag{4}
\]
Only this scalar readout is asserted; transverse force is present.

## 2. A common difference frequency

Take an observation interval of length T. Let all frequencies below denote integer cycles per T. Apply
\[
 e(t)=E_a\sum_{j=1}^3e_j\cos(2\pi u_jt/T),\qquad
 G(t)=g_a\sum_{j=1}^3G_j\cos(2\pi v_jt/T),
 \tag{5}
\]
where u_j=v_j+\Omega and
\[
 (v_1,v_2,v_3)=(101,173,257),\quad
 (u_1,u_2,u_3)=(118,190,274),\quad \Omega=17.
 \tag{6}
\]

Assume every scalar coefficient in p_q, alpha and B is T-periodic with Fourier support in [-B_0,B_0], B_0=9. Assume additionally
\[
 \alpha(t)=R(t)\alpha_0R(t)^T,\qquad
 A=\operatorname{tr}\alpha_0
 \tag{7}
\]
for an unknown orthogonal R(t). The receiver does not need R(t).

Expanding(1)–(2), all contributions belong to the following carrier classes, before coefficient sidebands are added:

| Force contribution | Carrier frequencies |
|---|---|
| q e | +/-u_i |
| G p_q | +/-v_i |
| G alpha e | +/-u_i +/-v_j |
| G(B:G) | +/-v_i +/-v_j |

The matched terms i=j in G alpha e have low-frequency part
\[
 \frac{E_ag_a}{2}\sum_j\alpha_{jj}(t)
          \cos(2\pi\Omega t/T)
 =\frac{E_ag_a A}{2}\cos(2\pi\Omega t/T).
 \tag{8}
\]
All other carriers in the table are at distance at least 17 from +Omega. The coefficient bandwidth 9 cannot move them onto the target. Also 2Omega=34>9, excluding a negative-target sideband in the more general componentwise calculation.

Consequently the complex Fourier coefficient and trace receiver are exactly
\[
 \widehat F_x(\Omega)
 =\frac1T\int_0^T F_x(t)e^{-2\pi i\Omega t/T}\,dt
 =\frac{E_ag_a A}{4},\qquad
 \widehat A=\frac4{E_ag_a}\widehat F_x(\Omega)=A.
 \tag{9}
\]
The proof is Fourier support plus(4); it uses no estimate of pose. Prescribed rotation through several turns is permitted when its coefficients meet the stated finite support.

For N equally spaced samples over the entire period, the same formula is exact whenever no carrier plus coefficient sideband aliases modulo N to the target. The stronger simple guard N>2(maximum carrier+B_0) suffices and holds for N=4096.

For the acceleration observable, divide(1) by the fixed particle mass m. The identical receiver returns A/m directly from center-of-mass acceleration; a separate mass measurement is not needed for that ratio. Acquiring that acceleration from an optical trajectory is a separate inverse problem.

## 3. The executed finite instance

The code uses alpha_0=diag(1,2,4), with true trace 7, and rotation by three full turns during T about the axis (1,2,3). It includes all terms in (1)–(2):

- nonzero charge q=.3;
- a rotating permanent dipole, including q times prescribed position;
- an arbitrary rotating rank-three gradient-response tensor;
- the translation-induced tensor contribution alpha_ij times position_k;
- simultaneous excitation of all six carrier channels.

The prescribed position contains frequencies 1 and 2. The rotating rank-three tensor has support at most 9; the translation contribution has support at most 8. Thus the declared support is verified algebraically for this supplied instance.

The result is 7.000000000000002 with imaginary residual below 1.6e-14. The code is a force-level response calculation with prescribed kinematics. The position and rotation are not solutions of the generated force and torque. It is not a free-flight, trapping, sensor, electrode, or self-consistent electromechanical simulation.

## 4. An equally informed ordinary method

Ordinary least squares on columns 1, cos(2pi Omega t/T), sin(2pi Omega t/T) yields the same target coefficient. A complete real FFT also gives it. On the coherent grid these are the same linear statistic, including after the supplied Gaussian noise is added.

With independent force-sample noise of variance sigma_F^2, the real trace receiver has
\[
 \operatorname{sd}(\Re\widehat A)
 =\frac{\sqrt{8/N}\,\sigma_F}{E_ag_a}.
 \tag{10}
\]
The ordinary least-squares receiver has exactly the same variance. The toy noise sigma_F=.02 produces a trace standard deviation .0008838835. This noise level is an input, not an acquired instrument capability.

The shortest discriminating test therefore supports a conditional pose-independent encoding, but gives no statistical or computational acquisition advantage over ordinary simultaneous multitone regression on the same data. Demodulation needs O(N) work at a single target; the ordinary method can use that same sufficient statistic.

## 5. Three controls that delimit the construction

**Material dispersion.** The three carrier tensors must coincide closely enough to justify(7). Merely matching their individual traces is insufficient. With a fixed orientation, choose
\[
 \alpha_1=\operatorname{diag}(6,.5,.5),\quad
 \alpha_2=\operatorname{diag}(.5,6,.5),\quad
 \alpha_3=\operatorname{diag}(.5,.5,6).
\]
Every trace is 7, but (9) reads 18. In a frequency-domain extension, the target is the sum of the three relevant diagonal components at their respective carrier frequencies.

If a correctly admitted model provides a common tensor alpha(t) and componentwise carrier deviations satisfying ||alpha_j(t)-alpha(t)||_op<=eta_j, with the same support guards, the matched-term trace bias is at most sum_j eta_j. Constitutive memory and sidebands that violate that support must enter a separate target-coefficient error bound. Neither qualification is acquired here.

**Window leakage.** Keeping only .9970703125 of the period and using the naive Fourier average produces 6.995056681-.004057470i. The fully informed ordinary method is allowed the same declared frequency class and actual timestamps. Joint regression on 729 real columns has rank 729 and condition number 2.872681; it recovers 7 to approximately 1e-14. It is incorrect to force this comparator to use a biased truncated FFT.

**Unadmitted target-band force.** Adding .1 cos(2pi Omega t/T) to the measured force changes the receiver to 7.2. The one target coefficient alone cannot distinguish this nuisance from changed trace. Rotation-induced sidebands, coefficient variation, nonlinear response or finite-window tails at this frequency need measured bounds.

## 6. How a qualified residual would enter a receiver

Suppose an independent physical argument bounds the absolute real target-coefficient model error by epsilon_F, in force units, after all field, temporal, geometry and constitutive deviations. Then the deterministic trace error in(9) is at most
\[
 \frac{4\epsilon_F}{E_ag_a}.
 \tag{11}
\]
A one-sided trace/mass upper bound must add the corresponding acceleration residual, a covered random-error allowance, field amplitude/phase uncertainty, and transfer-function uncertainty. An exact periodic bandlimit is not automatically acquired by observing a smooth or apparently slow trajectory.

For a free particle, an acceleration harmonic of amplitude a_Omega has a particular displacement amplitude
\[
 x_\Omega=\frac{a_\Omega}{(2\pi\Omega/T)^2}.
 \tag{12}
\]
Unknown initial position/velocity, all other force harmonics, observation-window boundary terms and colored measurement noise must be included in a position-data regression. Equation(12) is not an achieved sensor precision or a justification for differentiating noisy positions for free.

## 7. Drive and physical costs

In the ideal field basis,
\[
 \langle|e|^2\rangle=\tfrac32 E_a^2,\qquad
 \langle\|G\|_F^2\rangle=3g_a^2.
 \tag{13}
\]
Relative to equal-time use of the three source fields with amplitudes E_0,g_0, matching both quadratic field budgets requires E_a=sqrt(2/3)E_0 and g_a=sqrt(2/3)g_0. The target force amplitude in(8) is then E_0g_0 A/3. Peak fields, slew, calibration and actual power are not specified by these quadratic norms.

The construction requires six calibrated carrier drives, known phase and timing, resolved signed motion or force data, sufficient sensor bandwidth and antialias filtering, and an admission rule for response/motion bandwidth. It does not eliminate charge/permanent terms physically; it separates their supplied Fourier support. The signed common beat has no desired DC trace force and needs a distinct actuator to sort.

No electrode solution beyond the ideal affine basis, conductivity/oxide model, gas/neighbor interaction bound, per-particle density or composition bound, reference void ground truth, useful acceptance yield, industrial tail coverage, or full-cycle energy/throughput budget was acquired.

## 8. Scope relative to primary methods

Intermodulation electrostatic force microscopy already mixes drives and uses resolved sidebands with calibrated transfer functions; see [Borgani et al., 2014](https://arxiv.org/html/1408.5285). Our construction specializes that familiar operation to the scalar Maxwell trace basis and a precise moving-coefficient contract. A focused primary-source screen is not a priority clearance.

The existing static perfect-conductor inequality, also discussed by [Colbrook and Sadeghi, 2026](https://arxiv.org/html/2608.20466v1), remains conditional on the relevant physical response. The separate FAILED_LOSS_BRIDGE.md proves why a finite-conductivity material-volume witness does not supply that missing enclosed-volume premise.
