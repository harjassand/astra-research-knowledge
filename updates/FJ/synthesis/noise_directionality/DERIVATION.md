# Equilibrium-noise and work bound for one-way hydraulic readout

## Result and scope

For a stable, linear, passive two-port at one temperature T, write the
hydraulic response at angular frequency ω as

\[
Q(\omega)=H(\omega;B)p(\omega)+\xi(\omega),
\qquad
H_s=\tfrac12(H+H^\dagger)\succeq0.
\]

Use the two-sided angular-frequency convention
\(\langle\xi(\omega)\xi(\omega')^\dagger\rangle
=2\pi\delta(\omega-\omega')S_\xi(\omega)\). In the classical equilibrium
band, the fluctuation-dissipation theorem is

\[
S_\xi(\omega)=2k_BT H_s(\omega)=k_BT(H+H^\dagger).
\tag{D1}
\]

If the response is exactly unilateral at a frequency, `H12=0`, passivity
forces

\[
|H_{21}|^2\le 4\,\operatorname{Re}H_{11}\,\operatorname{Re}H_{22}.
\tag{D2}
\]

For imperfect directionality, passivity instead requires
`|H12+conj(H21)|^2 <= 4 Re(H11) Re(H22)`. If a measured reverse-leakage
bound gives `|H12| <= rho |H21|` with rho<1, the triangle inequality yields
`|H21|^2 <= 4 Re(H11) Re(H22)/(1-rho)^2`. The 16:1 response ratio in the
finite-reverse numerical circuit corresponds to rho=1/16; the ideal-chiral
bound is recovered as rho tends to zero. A pure gyrator has rho=1 and opposite
phase, so it is correctly outside this one-way estimate.

Thus a lossless gyrator can carry a nonzero signal without thermal noise, but
its two transmission magnitudes are equal; a *one-way* response has a
dissipative symmetric component and the corresponding FDT noise. For a known
pressure waveform `p1=lambda u`, `p2=0`, ideal output-flow measurement,
and Gaussian equilibrium noise, the matched-filter squared SNR obeys

\[
\mathrm{SNR}^2
=\lambda^2\int\frac{|H_{21}u|^2}{2k_BT\operatorname{Re}H_{22}}\,
\frac{d\omega}{2\pi}
\le \frac{2W_{\rm in}}{k_BT},
\quad
W_{\rm in}=\lambda^2\int\operatorname{Re}H_{11}|u|^2\,
\frac{d\omega}{2\pi}.
\tag{D3}
\]

For (D3), the waveform spectrum is supported in a band where `H12=0`, the
device begins in equilibrium, and the work integral includes the complete
response/ringdown so no energy remains stored at the end. If unidirectionality
is only approximate, retain `(H12+conj(H21))/2` in the Hermitian-part
determinant instead of applying (D2).

For equal-covariance Gaussian signal/no-signal hypotheses, their KL divergence
is `SNR^2/2`, so this particular detection problem satisfies
\(D_{\rm KL}\le W_{\rm in}/k_BT\). This is a source-work bound for the
specified linear Gaussian detection task. It is not a universal Landauer bound
for arbitrary coding, active sensors, nonequilibrium baths, or measurement
apparatuses.

## Eliminating the electrical ports without deleting their noise

Use the incoming source's quasistatic reciprocal wet-interface law, with
diagonal matrices (K,C,G):

\[
Q=Kp+CV+\eta_Q,\qquad
I=Cp+GV+\eta_I.
\]

The local reciprocal wet noise has the classical equilibrium covariance

\[
S_{(\eta_Q,\eta_I)}=2k_BT
\begin{pmatrix}K&C\\C&G\end{pmatrix},
\qquad C_i^2\le K_iG_i.
\tag{D4}
\]

Let the passive dry electrical network have admittance (Y(\omega;B)), and
let its Norton noise be (\eta_Y). KCL is
\(I+YV+\eta_Y=0\). Define (A=G+Y). Then

\[
V=-A^{-1}(Cp+\eta_I+\eta_Y),\qquad
H=K-CA^{-1}C,
\]

and the *reduced noise* is

\[
\xi=\eta_Q-CA^{-1}(\eta_I+\eta_Y).
\tag{D5}
\]

For a common temperature, the dry network noise is
\(S_{\eta_Y}=2k_BT Y_s\), where (Y_s=(Y+Y^\dagger)/2\). The wet and dry
noise sources are independent, but the wet ηQ and ηI are correlated as in
(D4). Since (G+Y_s=(A+A^\dagger)/2), direct expansion gives

\[
\begin{aligned}
\frac{S_{\xi}}{2k_BT}
&=K+CA^{-1}(G+Y_s)A^{-\dagger}C
  -CA^{-\dagger}C-CA^{-1}C\\
&=K-\tfrac12C(A^{-1}+A^{-\dagger})C
=\tfrac12(H+H^\dagger).
\end{aligned}
\tag{D6}
\]

This is the explicit Schur-elimination form of (D1). It requires the Johnson
noise of all dissipative electrical contacts/loads and the cross-noise of each
reciprocal wet converter. Eliminating a hidden contact from the *mean* circuit
while setting its thermal source to zero generally violates (D6). A grounded
third contact is a physical bath/terminal when it has finite conductance.

For a general dynamic passive network, (D1) applies directly to its complete
external hydraulic admittance (H(\omega;B)), including fluid inertia,
compliance, electrical capacitance, contact impedance, and any passive
termination retained inside the boundary. The noise is frequency dependent
through the Hermitian part of (H); no DC transfer coefficient determines
bandwidth by itself. Onsager-Casimir symmetry gives
\(H(\omega;B)^T=H(\omega;-B)\), whereas the same-field noise uses
\(H+H^\dagger\). Consequently (S(B)=S(-B)^T); in general one must not
replace the same-field Hermitian part by an ordinary transpose-symmetric
response.

## One-way passivity and the SNR/work inequality

When (H_{12}=0), the Hermitian part has the form

\[
H_s=\begin{pmatrix}
\operatorname{Re}H_{11}&H_{21}^*/2\\
H_{21}/2&\operatorname{Re}H_{22}
\end{pmatrix}.
\]

Its positive-semidefinite determinant proves (D2). From (D1), the output-flow
noise spectrum is `S22=2 k_B T Re(H22)`. A known input waveform at port 1 has
mean output `H21 p1`. In stationary Gaussian noise,
the ideal matched-filter SNR is the signal norm in the inverse-noise metric,
which is the integral in (D3). Substitution of (D2) gives

\[
\mathrm{SNR}^2
\le \lambda^2\int\frac{4\operatorname{Re}H_{11}\operatorname{Re}H_{22}
|u|^2}{2k_BT\operatorname{Re}H_{22}}\frac{d\omega}{2\pi}
=\frac{2W_{\rm in}}{k_BT}.
\]

For exact one-way response, (D1) also gives the nonzero equilibrium cross-noise
`S12=k_B T conj(H21)` even though the reverse *mean response* is zero. This is
the noise correlation between ports that a deterministic Schur complement
alone would miss.

If \(\operatorname{Re}H_{22}=0\), (D2) also forces (H_{21}=0), so there is
no zero-noise finite-gain exception. A general lossless gyrator instead has
\(H_{21}=-H_{12}^*\): it can be noiseless, but it is not a one-way isolator.

The constant matrix
\(H=\begin{psmallmatrix}1&0\\2&1\end{psmallmatrix}\) is an equality witness:
\(H_s=\begin{psmallmatrix}1&1\\1&1\end{psmallmatrix}\succeq0\). It is an
abstract passive one-way two-port and establishes sharpness of (D2)-(D3) for
the broad passive class. It is **not** claimed realizable by the incoming
wet-plus-grounded-Hall topology.

## Thermal backaction and dynamic bandwidth

For pressure storage (S\succ0), consider the thermal Langevin model

\[
S\dot p=-Hp+\xi,\qquad
\langle\xi(t)\xi(t')^T\rangle=2k_BT H_s\delta(t-t').
\tag{D7}
\]

The candidate equilibrium covariance \(\Sigma=k_BT S^{-1}\) solves the
Lyapunov equation because

\[
S^{-1}H\Sigma+\Sigma H^TS^{-1}
=2k_BT S^{-1}H_sS^{-1}.
\]

Thus nonreciprocity changes lagged correlations but not the equal-time Gibbs
covariance. With (S=I), (H=\begin{psmallmatrix}1&0\\1.8&1\end{psmallmatrix}),
and (k_BT=1), the equilibrium pressure covariance is (I), while the lag
covariance is (e^{-Ht}) and is asymmetric. The exact OU simulation in the
script checks this prediction; the finite-sample covariance is a numerical
diagnostic, not proof of the theorem.

In the source's ideal chiral electrical model with (g_-=0), (H_{12}(\omega)
=0) remains exact after adding terminal shunt capacitances. But
\(H_{21}(\omega)=-C_1C_2g_+/[(G_1+g_++i\omega c_1)(G_2+g_++i\omega c_2)]\)
in the chosen orientation, so its magnitude falls as (\omega^{-2}) at high
frequency. The hydraulic noise remains governed by (H_s(\omega)); capacitance
does not remove wet or contact dissipation. The numerical sweep uses normalized
parameters and establishes only this model-level bandwidth/noise tradeoff.

## Loaded actuation and acquisition cost

For the ideal DC unilateral matrix
\(H=\begin{psmallmatrix}a&0\\b&d\end{psmallmatrix}\), drive constant pressure
\(p_1=p\) for time \(\tau\), and connect a passive load resistance (R) at
port 2. Its thermal pressure noise has spectrum (2k_BTR), so the load-flow
signal and noise spectrum are

\[
\bar Q_2=\frac{bp}{1+dR},\qquad
S_{Q_2Q_2}=\frac{2k_BTd}{1+dR}.
\tag{D8}
\]

For a time-average over τ, \(\mathrm{SNR}^2=\tau b^2p^2/[2k_BTd(1+dR)]\).
The source work is \(W_{\rm in}=a p^2\tau\). The maximum-power load
\(R=1/d\) receives \(P_{\rm out}=b^2p^2/(4d)\), and its conversion
efficiency is \(\eta=b^2/(4ad)\). At that load,

\[
\mathrm{SNR}^2=\frac{P_{\rm out}\tau}{k_BT}
=\frac{\eta W_{\rm in}}{k_BT},
\qquad
W_{\rm in}=\frac{k_BT\,\mathrm{SNR}^2}{\eta}.
\tag{D9}
\]

Equation (D9) includes the thermal noise of the hydraulic load as well as the
reduced-network noise. It assumes an ideal flow measurement and excludes
pump/source overhead, calibration, transducer acquisition, instrument noise,
readout electronics, reset, and any auxiliary energy needed to create the
magnetic bias or temperature conditions.

For the incoming source's *specific* two-wet-interface, grounded three-contact
chiral topology, its definitions give

\[
\eta=\frac{b^2}{4\kappa_1\kappa_2}
\le \tfrac14\eta_c(Z_1)\eta_c(Z_2)\le\tfrac14,
\quad
\eta_c(Z)=\frac{\sqrt{1+Z}-1}{\sqrt{1+Z}+1}.
\tag{D10}
\]

The algebra is: with (t_i=g/G_i),
\[
\frac{b^2}{\kappa_1\kappa_2}
=\prod_i\frac{\chi_it_i}{(1+t_i)(1+t_i-\chi_i)},
\quad \chi_i=\frac{C_i^2}{K_iG_i},
\]
and each factor is maximized at (t_i=\sqrt{1-\chi_i}), where it equals
\(\eta_c(Z_i)\) for \(Z_i=\chi_i/(1-\chi_i)\). The general passive
bound (D2) permits (\eta\le1); (D10)'s 25% limit is specific to this
contact-inclusive topology and its two reciprocal converters.

Using the source report's theoretical estimates only as conditional inputs,
identical wet-interface (Z=4\times10^{-4}) gives
\(\eta\le2.4990\times10^{-9}\), while identical (Z=11) gives
\(\eta\le0.07617\). For an ideal loaded-flow SNR of 5 at 300 K, those
conditional bounds correspond to (W_{\rm in}\ge4.14\times10^{-11}\,\mathrm J\)
and (W_{\rm in}\ge1.36\times10^{-18}\,\mathrm J\), respectively. These
numbers inherit the source's unmeasured theoretical (Z) estimates; they are
not predicted performance of an acquired device. Actual measurement noise and
all auxiliary work can only increase the required total resource in the
specified experiment.

## Scope and failure modes

1. (C_i^2\le K_iG_i), the measured full (Y(\omega;B)), and equal bath
   temperatures are hypotheses. An observed cross-current alone does not
   establish the reciprocal voltage-to-flow coefficient.
2. If the dry circuit, wet interfaces, hidden contacts, and loads are not at one
   temperature, the noise is a temperature-weighted sum of bath contributions;
   a single-temperature FDT does not apply. Any thermal gradient or active
   bias is an additional resource to be measured and charged.
3. The script uses low-frequency classical FDT. At quantum frequencies, replace
   (2k_BT) in the symmetrized spectrum by
   \(\hbar\omega\coth[\hbar\omega/(2k_BT)]\); zero-point noise and measurement
   quadrature conventions then matter.
4. This derivation establishes neither the existence nor useful size of the
   neutral-liquid reciprocal transducer, nor historical novelty of the
   proposed physical composition.
