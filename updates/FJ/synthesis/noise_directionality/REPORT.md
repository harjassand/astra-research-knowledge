# FJ noise and directionality: a work-limited readout, not a noiseless channel

## Finding

The proposed passive hydraulic composition can have a genuinely one-way
*mean* pressure-to-flow response. At common temperature, however, eliminating
the electrical variables does not eliminate their equilibrium fluctuations.
The reduced hydraulic noise is fixed by the Hermitian (dissipative) part of the
same effective response. For exact one-way transfer, passivity gives a
pointwise-in-frequency gain bound and an ideal matched-filter work bound:

\[
H_{12}=0\quad\Longrightarrow\quad
|H_{21}|^2\le4\operatorname{Re}H_{11}\operatorname{Re}H_{22},
\qquad
\mathrm{SNR}^2\le\frac{2W_{\rm in}}{k_BT}.
\]

The proof includes the cross-correlated noise of each reciprocal wet
converter and the Johnson noise of every dissipative hidden electrical contact
and load. A noiseless Hall/gyrator component is possible only as
nonreciprocal-but-bidirectional transfer (equal forward/reverse magnitude).
Suppressing reverse response while retaining forward gain requires a
dissipative Hermitian component, and FDT assigns that component thermal noise.

For the source's particular grounded three-contact chiral circuit, when the
receiver also extracts power through its maximum-power hydraulic load, the
signal and acquisition work satisfy

\[
\mathrm{SNR}^2=\frac{P_{\rm out}\tau}{k_BT}
=\frac{\eta W_{\rm in}}{k_BT},
\qquad
\eta\le\frac14\eta_c(Z_1)\eta_c(Z_2)\le\frac14.
\]

Thus a loaded SNR of 5 requires at least 100 kBT input work even at
the source-topology's best possible 25% efficiency. With the source's
theoretical Z estimates conditionally applied to *both* wet interfaces,
the corresponding conditional upper efficiencies are about
\(2.499\times10^{-9}\) for Z=4\times10^{-4} and 0.07617 for Z=11.
If either theoretical Z applied independently to both wet converters and its
topology bound were saturated, the loaded-SNR-5 pressure-work floors at 300 K
would be 4.14e-11 J and 1.36e-18 J, respectively. These are arithmetic
consequences of unmeasured theoretical inputs, not device predictions, and
exclude pumps, calibration, readout, field generation, temperature control,
reset, and other acquisition costs.

The conclusion is not that directional control is impossible. It is that the
candidate cannot deliver an equilibrium-information shortcut: back-pressure
response can be suppressed, but an output signal still requires input work,
and the associated thermal covariance and measurement noise remain. Whether
the surviving directionality is useful for chemical isolation or stationary
interfaces is an engineering question not settled by this calculation.

## Reconstructed incoming model

The incoming physical source defines hydraulic/electrical fluxes
\((Q_i,I_i)\), conjugate efforts \((p_i,V_i)\), and power entering wet
converter (i) as (p_iQ_i+V_iI_i). At fixed temperature/gate and with no
local magnetic field its measured near-equilibrium law is

\[
\binom{Q_i}{I_i}=\begin{pmatrix}K_i&C_i\\C_i&G_i\end{pmatrix}
\binom{p_i}{V_i},\quad C_i^2\le K_iG_i.
\]

The source requires acquiring both equal reciprocal cross-responses,
\(\partial I_i/\partial p_i=\partial Q_i/\partial V_i=C_i\). For diagonal
heterogeneous (K,C,G) and dry electrical admittance (Y(B,\omega)), its
KCL sign convention (I=-YV) gives

\[
Q=Hp,\qquad H=K-C(G+Y)^{-1}C.
\]

Its reported exact-chiral DC model is
\(H=\begin{psmallmatrix}\kappa_1&0\\b&\kappa_2\end{psmallmatrix}\),
with \(\kappa_i=K_i-C_i^2/(G_i+g)\) and
\(b=|C_1C_2|g/[(G_1+g)(G_2+g)]\). The source reports a maximum-load
efficiency \(b^2/(4\kappa_1\kappa_2)\), bounded by
\(\frac14\eta_c(Z_1)\eta_c(Z_2)\) after optimizing electrical matching.
These source equations are producer claims preserved in
`work/FJ-sources/physical_PASTED_SOURCE.txt`; they are not physical
measurements. The source itself says the complete neutral-liquid reciprocal
work-conversion interface and assembled operation have not been demonstrated.

## Noise after eliminating the hidden electrical variables

`DERIVATION.md` gives the complete algebra. In brief, with wet noise
\((\eta_Q,\eta_I)\) having equilibrium covariance proportional to
\(\begin{psmallmatrix}K&C\\C&G\end{psmallmatrix}\), dry-network noise
\(\eta_Y\) proportional to \(Y_s=(Y+Y^\dagger)/2\), and
\(A=G+Y\), KCL gives

\[
\xi=\eta_Q-CA^{-1}(\eta_I+\eta_Y).
\]

Direct covariance propagation then yields

\[
\frac{S_\xi}{2k_BT}
=K+CA^{-1}(G+Y_s)A^{-\dagger}C
-CA^{-1}C-CA^{-\dagger}C
=\tfrac12(H+H^\dagger).
\]

This remains true for heterogeneous wet interfaces and complex frequency
response, provided the full network is passive and all dissipative parts are
at the same temperature. Eliminating a grounded contact or wiring impedance
from the mean equations while omitting its noise gives the wrong output noise.
For unequal bath temperatures the noise becomes a bath-weighted sum and the
single-temperature FDT does not apply; any temperature gradient or active bias
must be treated as a resource.

For exact one-way response, the equilibrium cross-spectrum is still
`S12=k_B T conj(H21)`; zero reverse response does not mean independent or
noise-free ports.

At each frequency, exact directionality `H12=0` makes
\(H_s=\begin{psmallmatrix}\mathrm{Re}H_{11}&H_{21}^*/2\\
H_{21}/2&\mathrm{Re}H_{22}\end{psmallmatrix}\). Its PSD determinant gives the
gain bound. The matched-filter calculation is frequency resolved, so it
accounts for dynamic bandwidth rather than extrapolating the DC result:

\[
\mathrm{SNR}^2=
\int\frac{|H_{21}(\omega)p_1(\omega)|^2}
{2k_BT\,\mathrm{Re}H_{22}(\omega)}\frac{d\omega}{2\pi}
\le\frac2{k_BT}\int\mathrm{Re}H_{11}|p_1|^2\frac{d\omega}{2\pi}.
\]

With finite reverse leakage, the exact condition is
`|H12+conj(H21)|^2 <= 4 Re(H11) Re(H22)`. If the measured magnitude ratio
satisfies `|H12| <= rho |H21|` for rho<1, then the same work bound holds with
factor `2/(1-rho)^2`. The 16:1 controlled circuit has rho=1/16, giving
factor 2.276 instead of 2; its exact-chiral sweep has rho=0.

The bound is sharp for an abstract passive one-way two-port with
\(H=\begin{psmallmatrix}1&0\\2&1\end{psmallmatrix}\), whose Hermitian part is
positive semidefinite and rank one. That equality witness is not the proposed
wet-plus-grounded-Hall topology. A separate exact OU model confirms that
one-way drift changes lagged pressure correlations while leaving the
equilibrium equal-time covariance at its Gibbs value.

## Controlled calculations

The owned script `noise_directionality_audit.py` independently propagates the
primitive wet and dry noise sources through the electrical Schur complement.
The reported dimensionless heterogeneous wet parameters are
`K=diag(1.8,2.1)`, `C=diag(0.55,0.60)`, and `G=diag(0.9,1.1)`. A passive
three-terminal forward/backward network with `g+=0.8,g-=0.05` has directional ratio
\(|H_{21}/H_{12}|=16\) across the six frequency points tested. The maximum
FDT covariance residual after dividing out `2 k_B T` was
\(4.45\times10^{-16}\), and the minimum eigenvalue of `H_s` was 1.6192;
there was no passivity violation. These tests validate the stated matrix model,
not a fabricated component.

With `g-=0` and shunt capacitances `diag(0.4,0.7)`,
\(H_{12}(\omega)=0\) at the five tested points, while \(|H_{21}|\) decays at
high frequency: normalized \(|H_{21}|\) drops from 0.08173 at zero frequency
to 9.42e-5 at \(\omega=100\). The capacitors store energy but do not remove wet/hall
dissipation or its equilibrium noise. An exact-discrete OU simulation
(seed 20261014; 100,000 post-burn-in samples) gave pressure covariance
\(\begin{psmallmatrix}1.0148&-0.0138\\-0.0138&1.0000\end{psmallmatrix}\)
against target `I`, and a nonzero asymmetric one-step lag covariance
\(C_{21}-C_{12}=-0.0856\). This is a finite simulation receipt only.

The source-topology arithmetic check uses the same normalized wet parameters
and ideal chirality. It gives load efficiency 0.0005389, below its
source-defined `Zi=chi_i/(1-chi_i)` bound 0.0005464. It is an algebra
fixture, not a material prediction. All values and checks are in
`noise_directionality_results.json`.

## Prior art and novelty boundary

- R. Q. Twiss, [“Nyquist's and Thevenin's Theorems Generalized for Nonreciprocal Linear Networks,” *J. Appl. Phys.* 26, 599–602 (1955)](https://doi.org/10.1063/1.1722048), gives the multiport nonreciprocal thermal-current covariance proportional to (Y+Y^\dagger), correlated port noise, and passive-realizability conditions. This is direct prior art for the core network FDT; the result here is not a new general noise theorem.
- H. B. Callen and T. A. Welton, [“Irreversibility and Generalized Noise,” *Phys. Rev.* 83, 34–40 (1951)](https://doi.org/10.1103/PhysRev.83.34), establish the generalized resistance/noise relation. R. Kubo, [“Statistical-Mechanical Theory of Irreversible Processes. I,” *J. Phys. Soc. Jpn.* 12, 570–586 (1957)](https://doi.org/10.1143/JPSJ.12.570), develops the response/correlation FDT including conductivity tensors.
- M. Büttiker, [“Scattering theory of thermal and excess noise in open conductors,” *Phys. Rev. Lett.* 65, 2901–2904 (1990)](https://doi.org/10.1103/PhysRevLett.65.2901), treats multiprobe equilibrium noise and the quantized Hall regime. L. Callegaro, M. Ortolano, and J. Schurr, [“Equilibrium noise correlations in quantum Hall effect devices as a test of a formula by Büttiker,” *EPL* 101, 50003 (2013)](https://doi.org/10.1209/0295-5075/101/50003), report an experimental test on nonreciprocal six-terminal quantum-Hall networks.
- B. Coquinot, L. Bocquet, and N. Kavokine, [“Hydroelectric energy conversion of waste flows through hydroelectronic drag,” arXiv:2403.20209v2](https://arxiv.org/html/2403.20209v2), provides the wet reciprocal transport matrix and the theoretical hydro-electronic figure-of-merit framework used by the incoming source. Its own paper says reciprocal current-induced flow (“quantum osmosis”) had not yet been observed in the cited context.

The Schur-eliminated hydraulic FDT, one-way PSD determinant, and source-work/SNR inequality are straightforward combinations of established multiport FDT and passivity. I did not establish historical priority for this hydro-electronic application. The particular remote neutral-liquid composition remains unvalidated and its novelty is UNKNOWN. The evidence supports a precise noise/work gate, not a new physical capability or technology claim.

## Decisive experiment and next gate

1. At one measured temperature, independently acquire each wet device's full
   complex \(K_i(\omega),C_i(\omega),G_i(\omega)\), both reciprocal cross
   directions, and its pressure/current cross-noise.
2. Acquire the dry network's full terminal (Y(B,\omega)), including ground,
   contacts, cable, and load terminations, with their temperatures. Predict
   both (H(B,\omega)) and (S_\xi(B,\omega)) before assembly.
3. With all baths equilibrated, test (S_\xi=k_BT(H+H^\dagger)), including
   off-diagonal cross spectra, and verify (S(B)=S(-B)^T). Test for parasitic
   pressure pickup, mechanical vibration, displacement current, and temperature
   gradients.
4. Drive a calibrated small pressure waveform, measure donor hydraulic work,
   receiver signal, receiver noise, and the full transfer function under an
   explicit passive load. Compare measured Fisher/SNR with (D3) and, at the
   maximum-power load, with (D9). Repeat on field reversal, reciprocal
   electrical substitute, open circuit, and donor/receiver interchange.
5. Add the real input/output instruments, pressure source, magnetic-field
   generation, temperature control/refrigeration, calibration, reset, and
   lifetime costs before claiming useful acquisition or work transfer.

The first go/no-go measurement is still the source's wet-interface contract:
the same steady, near-equilibrium cross coefficient must be observed in both
directions. A failure blocks this composition; it does not refute FDT or the
underlying hydro-electronic theory.

## Reproduction

Run from the task workspace with Python 3 and NumPy:

```bash
python3 work/FJ-noise-directionality/noise_directionality_audit.py
```

The script writes the deterministic JSON result beside itself. It uses no
source code archive, no sibling FJ worker output, no internet data at runtime,
and no physical acquisition. The exact source and capital read scope is in
`READ_LEDGER.md`.
