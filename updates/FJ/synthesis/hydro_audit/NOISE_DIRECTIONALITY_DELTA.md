# Independent delta audit: equilibrium noise, directionality, and loaded readout

## Scope and result

This is a separate audit of work/FJ-noise-directionality/DERIVATION.md and its NumPy checker. I did not import or execute that checker, and I did not edit the frozen source, that worker's files, or the initial FJ-hydro-audit packet.

The core identities are algebraically correct when read with the stated conditions: linear passive response, a single common bath temperature, complete inclusion of every dissipative terminal's equilibrium noise, classical low-frequency FDT, and the stated two-sided angular-frequency PSD convention. The unilateral gain determinant and its frequency-integrated source-work bound then follow. The max-power loaded-flow equality also follows exactly for the memoryless DC model when the passive load is at the same temperature and its Johnson pressure noise is included.

I found no counterexample to those conditional claims. Several scope qualifications matter:

- A finite-duration rectangular pressure pulse contains arbitrarily high frequencies. The D9 time-average equality is exact for its ideal white-noise, memoryless DC circuit, but it is not automatically an equality for a real bandwidth-limited hydraulic system. Use a band-limited waveform and the full \(H(\omega)\), load, and measurement transfer functions for a physical finite-time prediction.
- The Lyapunov calculation in D7 proves that the Gibbs covariance is invariant. It proves convergence to that covariance only with additional stability/ergodicity conditions; a lossless passive gyrator is a simple counterexample to convergence.
- FDT alone gives second moments. The matched-filter SNR and \(D_{\rm KL}=\mathrm{SNR}^2/2\) statements additionally need the specified equal-covariance Gaussian hypotheses. A non-Gaussian thermal/mesoscopic detector requires its likelihood, not just its PSD.
- The single-temperature FDT cannot be reused for unequal-temperature wet interfaces, Hall contacts, wiring, or loads. At multiple temperatures the noise is bath weighted, and thermal gradients are resources.
- D9 treats the hydraulic load as an external noisy element and adds its noise to the device's \(\xi\). If a termination is instead included inside a complete external \(H\), its noise belongs in that complete FDT once, not a second time.

## Re-derivation of the Schur-eliminated FDT

Take Fourier transforms \(x(\omega)=\int x(t)e^{i\omega t}\,dt\) and define two-sided angular-frequency spectra by
\[
\langle x(\omega)y(\omega')^\dagger\rangle
=2\pi\delta(\omega-\omega')S_{xy}(\omega).
\]
For a single common classical temperature \(T\), FDT for a passive complete hydraulic admittance \(H\) is
\[
S_\xi=2k_BT H_s=k_BT(H+H^\dagger),\qquad
H_s=\frac{H+H^\dagger}{2}\succeq0.
\]
The factor is consistent with two-sided Johnson current noise \(2k_BT G\) for a conductance \(G\); the corresponding one-sided per-Hz value is \(4k_BT G\).

For the source's quasistatic wet law, add its local equilibrium noises:
\[
Q=Kp+CV+\eta_Q,\qquad I=Cp+GV+\eta_I,
\]
\[
S_{(\eta_Q,\eta_I)}
=2k_BT\begin{pmatrix}K&C\\C&G\end{pmatrix}.
\]
Let the dry terminal admittance be \(Y(\omega)\), with independent Norton noise \(\eta_Y\) at the same temperature and
\(S_{\eta_Y}=2k_BT Y_s\), \(Y_s=(Y+Y^\dagger)/2\). KCL is
\(I+YV+\eta_Y=0\). For \(A=G+Y\),
\[
H=K-CA^{-1}C,\qquad
\xi=\eta_Q-CA^{-1}(\eta_I+\eta_Y).
\]
Propagating the full primitive covariance, including the wet cross-covariance \(S_{\eta_Q\eta_I}=2k_BT C\), gives
\[
\begin{aligned}
\frac{S_\xi}{2k_BT}
&=K+CA^{-1}(G+Y_s)A^{-\dagger}C
  -CA^{-1}C-CA^{-\dagger}C\\
&=K-\frac12C(A^{-1}+A^{-\dagger})C
=\frac12(H+H^\dagger),
\end{aligned}
\]
because \(G+Y_s=(A+A^\dagger)/2\). This is the complete cancellation that the deterministic elimination alone would miss. It is valid for the independent-element decomposition above. Shared or correlated dissipative elements must instead be represented by their complete joint covariance; the total-equilibrium FDT remains the governing statement.

The exact identity is also easy to misuse across boundaries. If \(H\) is the device response before an external hydraulic load, use its FDT noise and add the load's independent thermal noise. If \(H\) is redefined to include that load, recompute the full response and do not add the same load noise again. Likewise a grounded electrical contact cannot be removed from the mean circuit while its Johnson source is silently deleted.

A complex dynamic \(H\) uses the Hermitian part, not an ordinary transpose-symmetric part. Onsager-Casimir reversal, when the relevant port parities and field-reversal hypotheses hold, is \(H(\omega;B)^T=H(\omega;-B)\); it implies \(S(B)=S(-B)^T\), not that \(S(B)\) is obtained by symmetrizing \(H(B)\) with a plain transpose.

## Directionality and waveform work

For a two-port, passivity gives \(H_s\succeq0\). Its determinant is
\[
\operatorname{Re}H_{11}\operatorname{Re}H_{22}
-\frac14|H_{12}+H_{21}^*|^2\ge0.
\]
Thus if \(H_{12}=0\) at a frequency,
\[
|H_{21}|^2\le4\operatorname{Re}H_{11}\operatorname{Re}H_{22}.
\]
If \(|H_{12}|\le\rho|H_{21}|\), \(0\le\rho<1\), the triangle inequality gives
\[
|H_{21}|^2\le
\frac{4\operatorname{Re}H_{11}\operatorname{Re}H_{22}}{(1-\rho)^2}.
\]
This is pointwise in frequency. A DC isolation measurement cannot be used for a waveform whose spectrum extends into a leaky band.

For a prescribed deterministic pressure \(p_1=\lambda u,\ p_2=0\), ideal flow readout at port 2, stationary Gaussian equilibrium noise, and signal-independent covariance, the two-sided matched-filter statistic is
\[
\mathrm{SNR}^2
=\lambda^2\int
\frac{|H_{21}u|^2}{2k_BT\operatorname{Re}H_{22}}
\frac{d\omega}{2\pi}.
\]
The expected source work is
\[
W_{\rm in}=\lambda^2\int\operatorname{Re}H_{11}|u|^2
\frac{d\omega}{2\pi}.
\]
If the support lies where \(H_{12}=0\), substitution of the determinant bound gives
\[
\mathrm{SNR}^2\le\frac{2W_{\rm in}}{k_BT}.
\]
Finite leakage changes the factor to \(2/(1-\rho)^2\). Work here is net pressure-flow work at the prescribed source port, with the complete response/ringdown included so the device has no uncounted residual stored energy. It does not include the pump, pressure actuator, field supply, temperature control, calibration, or readout. Any signal-bearing initial free energy, active feedback, or other powered port is outside this inequality unless its work is charged.

At exact one-way response the equilibrium cross spectrum is still
\[
S_{12}=k_BT H_{21}^*.
\]
So the ports' thermal fluctuations are correlated despite zero reverse mean response. If \(\operatorname{Re}H_{22}=0\), passivity also forces \(H_{21}=0\); there is no finite-gain, zero-noise exception. At frequencies where both vanish, interpret the matched-filter quotient by a limiting/pseudoinverse convention: that band carries no signal and contributes no information.

For equal-covariance Gaussian hypotheses, \(D_{\rm KL}=\mathrm{SNR}^2/2\). This is the KL divergence of this mean-shift observation model, not a general bound on arbitrary encodings, non-Gaussian likelihoods, active sensors, or nonequilibrium baths. The one-sided versus two-sided PSD convention only changes representation; using a one-sided PSD with the two-sided formula would introduce a factor-of-two error.

## Loaded maximum-power readout

For the memoryless DC unilateral device
\[
H=\begin{pmatrix}a&0\\b&d\end{pmatrix},\qquad a,d>0,
\]
drive \(p_1=p\) and connect a passive receiver resistance \(R\), at the same \(T\). Write its thermal pressure source as \(n_R\), independent of the device's reduced noise \(\xi_2\), with
\(S_{\xi_2}=2k_BT d\), \(S_{n_R}=2k_BT R\). The loaded port equations give
\[
Q_2=\frac{bp+\xi_2+d n_R}{1+dR},
\quad
\bar Q_2=\frac{bp}{1+dR},
\quad
S_{Q_2Q_2}=\frac{2k_BT d}{1+dR}.
\]
For a time average over \(\tau\) in this white-noise idealization,
\[
\mathrm{SNR}^2=\frac{\tau b^2p^2}{2k_BT d(1+dR)}.
\]
At \(R=1/d\), output power is \(P_{\rm out}=b^2p^2/(4d)\); source work is \(W_{\rm in}=ap^2\tau\); and \(\eta=P_{\rm out}/(ap^2)=b^2/(4ad)\). Therefore
\[
\mathrm{SNR}^2=\frac{P_{\rm out}\tau}{k_BT}
=\frac{\eta W_{\rm in}}{k_BT}.
\]
The load noise is essential for this equality. At another \(R\), the same SNR-to-work identity is generally false; with a cold/hot load it is also false in this form. A pressure source with finite impedance/noise or nonzero \(H_{12}\) changes the boundary equations. In a dynamic system, use the load's \(Z_L(\omega)\), its noise spectrum, the full \(H(\omega)\), and the actual observation filter rather than inserting DC \(a,b,d\).

### Exact source-topology loaded case

Choose two identical wet converters with \(K_i=G_i=1,\ C_i=3/5\), and the ideal chiral electrical link \(g_+=4/5,\ g_-=0\). Each has \(\chi=9/25,\ Z=9/16\), and \(t=g/G=4/5=\sqrt{1-\chi}\). Exact Schur elimination gives, after reversing the receiver port orientation,
\[
H=\begin{pmatrix}4/5&0\\4/45&4/5\end{pmatrix},
\quad R_*=5/4,\quad
\eta_*=\frac{(4/45)^2}{4(4/5)^2}=\frac1{324}.
\]
This saturates the source topology product bound since \(\eta_c=1/9\) for each converter.

Set \(k_BT=p=\tau=1\). Then
\[
\bar Q_2=2/45,\quad
S_{\xi_2}=8/5,\quad S_{n_R}=5/2,\quad
S_{Q_2Q_2}=
\frac{8/5+(4/5)^2(5/2)}{(1+1)^2}
=\frac45.
\]
The variance of the time-average is \(4/5\), so
\[
\mathrm{SNR}^2=\frac{(2/45)^2}{4/5}=\frac1{405}
=\frac{\eta_* W_{\rm in}}{k_BT}
=\frac{P_{\rm out}\tau}{k_BT},
\qquad W_{\rm in}=4/5,\quad P_{\rm out}=1/405.
\]
Every quantity is rational and the check is independent of the worker script. It verifies the algebra of an idealized source-topology circuit, not any fabricated wet interface.

The broader passivity/FDT SNR bound is sharp for the abstract one-way passive matrix
\[
H=\begin{pmatrix}1&0\\2&1\end{pmatrix},\quad
H_s=\begin{pmatrix}1&1\\1&1\end{pmatrix}.
\]
For \(p_1=1\), a unit observation interval, and \(k_BT=1\), the ideal unloaded output has mean 2 and white PSD 2; the time-average variance is 2, so SNR squared is 2, exactly \(2W_{\rm in}/k_BT\) with \(W_{\rm in}=1\). This sharp witness is not the source's grounded-Hall topology; its max-power-load efficiency is one, whereas that topology is bounded by 1/4.

## Independent heterogeneous dynamic example

At normalized \(\omega=1\), take
\[
K=\operatorname{diag}(2,3),\quad
C=\operatorname{diag}(1/2,1/3),\quad
G=\operatorname{diag}(1,2),
\]
and a passive grounded Hall terminal matrix with \(g_+=1/2,\ g_-=1/8\), shunted by \(i\omega\operatorname{diag}(1/3,1/5)\):
\[
Y=\begin{pmatrix}5/8+i/3&-1/8\\-1/2&5/8+i/5\end{pmatrix}.
\]
Both wet blocks are strictly passive: \(K_iG_i-C_i^2=(7/4,53/9)>0\). The dry Hermitian part is
\[
Y_s=\begin{pmatrix}5/8&-5/16\\-5/16&5/8\end{pmatrix},
\quad \det Y_s=75/256>0.
\]
Independent exact Gaussian-rational matrix arithmetic computes \(A=G+Y\), \(H=K-CA^{-1}C\), and propagates the full joint primitive covariance of \((\eta_Q,\eta_I,\eta_Y)\). It gives exact entrywise equality
\[
S_{\xi}/(2k_BT)=(H+H^\dagger)/2,
\]
a positive \(\det H_s=280658276/51287835\), and \(H_{21}/H_{12}=4=g_+/g_-\). Thus this example tests a genuinely complex frequency response, heterogeneous wet parameters, finite reverse leakage, the dry shunt's zero dissipative contribution, and the correlated reciprocal wet noise without importing worker code.

At the same frequency and with the same heterogeneous wet blocks, setting \(g_-=0\) gives an exact complex-frequency chiral check: \(H_{12}=0\), \(H_{21}=-13/629+4i/629\ne0\), and \(\det H_s=10474633/1924740>0\). Separately propagated primitive noise still equals \(H_s\) exactly. This verifies that the unilateral determinant applies to the dynamic response at that frequency, not merely to the DC example.

## Cold audit of the worker checker and derivation claims

The checker is structurally consistent with the derivation. Its transfer matrix for \(\xi=\eta_Q-CA^{-1}(\eta_I+\eta_Y)\) has the right dimensions and signs; it includes the \(Q/I\) wet cross covariance and dry \(Y_s\) term. Its 16:1 finite-reverse ratio follows from the grounded two-port Hall matrix's shared determinant. The ideal-chiral dynamic matrix stays triangular under diagonal capacitive shunts. The OU transition is exact for its chosen \(H=I+\) nilpotent shear; \(Q_{\rm step}=I-AA^T\) gives unit stationary covariance. The checker appropriately treats its Monte Carlo covariance as a receipt, not a proof.

The independent exact replay strengthens the checker: the Schur FDT equality and the loaded D9 arithmetic hold exactly for rational data. I found no missing factor of two under the stated two-sided angular convention.

The derivation must still keep its boundary conditions visible. Passivity alone does not imply a single-temperature noise law. For example, two uncoupled unit conductances at temperatures \(T_1=1\) and \(T_2=3\) have \(Y_s=I\) but noise \(2k_B\operatorname{diag}(1,3)\), which cannot be written as \(2k_BT Y_s\) for one scalar \(T\). Likewise, passivity with only semidefinite dissipation does not guarantee relaxation to a unique stationary distribution: \(H=\bigl(\begin{smallmatrix}0&g\\-g&0\end{smallmatrix}\bigr)\), \(S=I\), \(H_s=0\) is a noiseless lossless gyrator that rotates states but does not thermalize arbitrary initial conditions. The D7 covariance still solves its Lyapunov equation and is invariant, but uniqueness/convergence requires a stable, sufficiently dissipative/ergodic model.

The FDT statement is a standard consequence of generalized response/noise theory; for instance, [Callen and Welton](https://doi.org/10.1103/PhysRev.83.34) formulate generalized-force noise in terms of dissipation, and [Kubo](https://doi.org/10.1143/JPSJ.12.570) treats fluctuation-response relations for complex conductivity tensors. Nothing in this audit establishes new FDT prior art or physical novelty for the hydro-electronic composition.

## Exact-check receipt and limits

The accompanying noise_delta_checks.py contains standalone Fraction/Gaussian-rational arithmetic and no imports from work/FJ-noise-directionality or any other worker. It checks the exact source-topology loaded SNR case, the general SNR-bound equality witness, and a heterogeneous dynamic full-noise elimination. noise_delta_checks.out is its deterministic exact output.

No physical noise spectrum, temperature, wet device, Hall element, instrument, or energy boundary was acquired. The analysis confirms a conditional information/work theorem for passive common-temperature linear systems, not a noiseless channel or free hydraulic sensing.
