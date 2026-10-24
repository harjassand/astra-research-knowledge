# Multimode gate for the scalar phonon optimum

## Transport ledger

The scalar optimum is an ideal, one-branch Landauer result at \(\theta=k_BT/(\hbar\omega_0)=1/2\), with \(u=\omega/\omega_0\) and \(g(u)=(u/\sinh u)^2\). Its normalized conductances are

\[
J_* = 1.133319342823405,\qquad J_{\rm rigid}=1.440176577374174,
\qquad \Delta J=0.306857234550769.
\]

The physical multiplier is \(k_B\omega_0/(2\pi)\). The unrestricted ballistic acoustic-channel integral is \(J_Q=\int_0^\infty g(u)\,du=\pi^2/6\), so one ideal transmitted acoustic mode contributes \(G_Q=\pi^2k_B^2T/(3h)\). The scalar decrement is only \(\Delta J/J_Q=0.1865468\) of one thermal-conductance quantum. As \(T\to0\) at fixed cell frequencies, both scalar designs recover the same gapless-channel quantum and the decrement tends to zero.

A slender free elastic beam has four low-frequency acoustic branches: one longitudinal, one torsional, and two flexural. Thus a real beam does not implement the scalar count. For a matched beam control where only the longitudinal channel changes and the other three transmissions are unchanged, write their combined normalized Landauer contribution as \(B\). Then

\[
J_{\rm control}=J_{\rm rigid}+B,\quad J_{\rm device}=J_*+B,
\quad \eta_{\rm total}=\frac{\Delta J}{J_{\rm rigid}+B}.
\]

Illustrative limits, not a beam prediction:

- If the three bypass branches each have the same finite rigid-reference contribution, \(B=3J_{\rm rigid}\), the total reduction is 5.327%.
- If each is an ideal unbounded acoustic channel, \(B=3J_Q\), the total reduction is 4.813%.

The \(J_Q\) example is a clean low-energy channel reference, not an upper bound on a finite beam's \(B\) if additional optical branches enter the thermal window.

In either matched comparison the absolute change remains \(\Delta J\); the other polarizations dilute the percentage. Additional parasitic paths present only in the resonator device are different: if their normalized excess contribution is \(L\), the net advantage is \(\Delta J-L\), so it vanishes at \(L\ge0.306857\). Three equal bypass leaks must each carry less than \(\Delta J/(3J_Q)=6.218\%\) of a full acoustic-channel integral to meet that one-channel-reference budget. The real test quantity is always

\[
J=\int_0^\infty g(u)\,\mathrm{Tr}[t(u)^\dagger t(u)]\,du,
\]

including mode conversion and every propagating lead mode. It is not valid to infer total heat flow from an axial mode measurement alone.

At 50 mK, choosing \(\theta=1/2\) requires \(f_0=\omega_0/(2\pi)=k_BT/(\pi\hbar)\simeq2.08\) GHz. The scalar branch has acoustic passband \(0\)–2.08 GHz, stopband 2.08–4.17 GHz, and optical passband 4.17–8.88 GHz; the rigid reference ends at 4.44 GHz. This is a design frequency conversion, not evidence that a proposed beam has those bands. The ideal one-channel decrement would be about \(8.83\) fW/K at 50 mK before contact losses.

## Concrete cryogenic test platform and its boundary

A published low-temperature platform provides a literal starting geometry: two suspended 100-nm SiN membranes with heaters and thermometers, joined by one or two catenoid-shaped SiN waveguides. Tavakoli et al. measure down to 50 mK, use forward/reversed heat-flow protocols, sever one of two links to check additivity, and separately measure the supporting-beam path. They count four acoustic channels per wire and report that the measured conductance remains well below the four-quantum ideal because transmission/contact coupling is nonideal. This is exactly why the finite contract must retain lead contacts, support beams, all four modes, and calibration controls; the scalar 21.3% cannot be reported as a device-level reduction without that accounting. [Tavakoli et al., *Nature Communications* 9, 4287 (2018)](https://www.nature.com/articles/s41467-018-06791-0).

The same experiment quotes a representative wire conductance of order \(10^{-14}\,\mathrm{W/K}\) at 100 mK, while one ideal channel quantum there is about \(9.46\times10^{-14}\,\mathrm{W/K}\). The scalar model's ideal decrement at that temperature is \(0.18655G_Q\simeq1.77\times10^{-14}\,\mathrm{W/K}\), larger than that representative measured total. This rules out transplanting the ideal decrement unchanged to that contact-limited device: the decrement must be recomputed from its actual channel transmissions, and for a pure suppression it cannot exceed the matched baseline conductance. The comparison alone does not determine experimental resolution for a smaller differential effect.

A proposed *unconstructed route* is a short periodic resonator section in the narrow central part of that type of link, with a symmetric three-dimensional cell: a centered compliant axial paddle for the longitudinal branch; paired side paddles along both cross-section axes for the two flexural branches; and offset, torsion-compliant masses for the torsional branch. Tune those sub-resonators around the thermal window and preserve mirror symmetries where possible. A 3-D elastic FEM/Bloch calculation must supply all four acoustic bands, optical bands, and polarization-conversion scattering before fabrication; no scalar optimum or resource bound transfers automatically to this composite cell. A companion link could use the same host, total resonator masses, intercell axial stiffness, contact tapers, and supports, but stiff-lock the paddles to the spine. The comparison would be matched only on declared mass/stiffness and measured geometry; the changed transverse spectrum must be included in the measured full transmission rather than assumed away. This route is not an achieved interface or measured design.

There is direct mechanical precedent for the components, though not yet for this cryogenic thermal integration. Park and Jeon fabricated a three-cell tapered beam whose thickness/width-varying unit cells suppress flexural transmission in a measured gap; they report −35 to −10 dB over 3.6–237.9 Hz. Chuang et al. experimentally extract torsional and bending response separately with two symmetric fiber-Bragg-grating sensors, using their difference to cancel bending and their sum to recover it. Arretche and Matlack demonstrate a radial torsional filter using locally resonant inclusions and radially varied thickness/impedance. These demonstrate polarization-aware beam design/readout methods, not performance at GHz or in a dilution refrigerator. [Park & Jeon (2021)](https://doi.org/10.1016/j.jsv.2021.115977); [Chuang et al. (2020)](https://doi.org/10.1016/j.jsv.2019.115004); [Arretche & Matlack (2022)](https://doi.org/10.1016/j.jsv.2022.117305).

A second practical geometry precedent is the NIST GaN-pillar/suspended-Si membrane experiment: grown nanopillars create many local resonances coupled to membrane heat-carrying phonons; the authors measured up to 21% lower thermal conductivity with unchanged power factor. It is a multi-mode, device-scale room-temperature result, not a cryogenic ballistic test and not a fixed-total-mass/fixed-\(K\) comparison. It supports the physical plausibility of resonator-to-membrane coupling, not the scalar theorem's device consequence. [Spann et al., *Advanced Materials* 35 (2023)](https://www.nist.gov/publications/semiconductor-thermal-and-electrical-properties-decoupled-localized-phonon-resonances).

## Decision gate

Do not market the scalar number as a four-mode beam result. A useful next gate would be a paired, cryogenic measurement of full two-terminal conductance versus temperature for the resonator and stiff-locked links, plus polarization-resolved driven transfer functions to diagnose the four modes. Calibrate contacts and the parallel support path on-chip; compare the measured \(J(T)\) to the complete FEM scattering matrix. A positive full-device result requires the total measured weighted decrement to exceed the uncertainty and any unmatched shunt leakage. The available cryogenic literature also flags that ballistic length-independence does not ensure unit transmission: contact and reservoir coupling can dominate. [Rego & Kirczenow, *PRL* 81, 232 (1998)](https://doi.org/10.1103/PhysRevLett.81.232) gives the ideal single-mode quantum, while [Schwab et al., *Nature* 404, 974–977 (2000)](https://www.nature.com/articles/35010065) measured it in suspended structures; neither validates this resonator link.
