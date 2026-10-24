# Static compliance, equilibrium motion, and thermal transmission: bounded primary-source check

Scope: compare the proposed bulk one-link passband/conductance constraint at fixed internal centre-of-mass (CM) compliance against established response and transport sum rules. This is a source-scope check, not a novelty or priority determination.

## The closest established response identity

For a retarded scalar susceptibility \(\chi_Y(\omega)\) of a coordinate \(Y\), analyticity and the usual decay at high frequency give the zero-frequency Kramers–Kronig relation

\[
C_Y=\operatorname{Re}\chi_Y(0)=\frac{2}{\pi}\int_0^\infty \frac{\operatorname{Im}\chi_Y(\omega)}{\omega}\,d\omega,
\]

with sign adjusted if the Fourier convention defines the dissipative part oppositely. The fluctuation–dissipation theorem relates the equilibrium coordinate-noise spectrum to that same dissipative susceptibility. In the classical harmonic Gibbs ensemble this reduces to \(\operatorname{Var}(Y)=k_BT C_Y\); for a quantum harmonic system, each normal mode instead contributes \(\hbar\coth(\hbar\omega/2k_BT)/(2\omega)\), which is at least \(k_BT/\omega^2\). These are standard one-port response/compliance statements, not transport bounds.

The primary basis is Callen and Welton, “Irreversibility and Generalized Noise,” *Phys. Rev.* 83, 34 (1951), DOI [10.1103/PhysRev.83.34](https://doi.org/10.1103/PhysRev.83.34). Their theorem relates generalized resistance to equilibrium generalized-force fluctuations in linear dissipative systems, with Brownian motion, electromagnetic noise and gas-pressure fluctuations as examples. The official APS record and a public scan were inspected; the scan is [here](https://123.physics.ucdavis.edu/week_3_files/callen_irreversibility_and_noise_1951.pdf). Kubo’s primary paper, “Statistical-Mechanical Theory of Irreversible Processes. I,” *J. Phys. Soc. Jpn.* 12, 570 (1957), DOI [10.1143/JPSJ.12.570](https://doi.org/10.1143/JPSJ.12.570), explicitly develops response/correlation relations and discusses sum rules. A public 17-page scan at [this host](https://staff.ulsu.ru/moliver/ref/kubo/kubo57.pdf) was acquired by the native reader as a PDF but exposed no line-extracted body; the scope statement is verifiable from its indexed text and the JPSJ primary record.

Applied to the local CM-relative coordinate \(Y\) in the current optimal-network result, the proven static value \(C_Y=1/k_*\) therefore fixes a weighted integral of its own response spectrum. It also gives the stated equilibrium variance floor. It does not identify that response spectral measure with the bulk passband indicator \(\chi(\omega)\): the former is weighted by the squared participation of \(Y\) in modes and by \(1/\omega\), while the latter counts propagating bulk channels with the Landauer thermal weight.

## Harmonic Landauer transport is a distinct observable

Dhar and Roy, “Heat Transport in Harmonic Lattices,” *J. Stat. Phys.* 125, 801–820 (2006), DOI [10.1007/s10955-006-9235-3](https://doi.org/10.1007/s10955-006-9235-3), provide the sharpest same-paper connection between fluctuations and transport. The acquired primary arXiv text has the reservoir-noise FDT in Eq. (3.5), the reservoir-dressed retarded Green function in Eq. (3.7), and the heat current in Eq. (4.2):

\[
J=\int_{-\infty}^{\infty}d\omega\;\operatorname{Tr}\!\left[G_W^+\Gamma_LG_W^-\Gamma_R\right]\frac{\hbar\omega}{\pi}[f(\omega,T_L)-f(\omega,T_R)].
\]

Eq. (4.2) is a lead/contact-coupled Green-function trace, while equilibrium position correlations are separately calculated in Sec. 4 and Appendix B. The authors explicitly say the formalism generalizes to more than two reservoirs (Sec. 2). Thus this paper connects bath noise to the driven lattice and computes both transport and correlations, but does not turn a chosen internal static compliance into a lower bound on bulk Landauer conductance.

Das and Dhar, “Landauer formula for phonon heat conduction: relation between energy transmittance and transmission coefficient,” arXiv:1204.5595, give the more explicit transmission interface. Their Eq. (1) is the Bose-weighted Landauer current; Eq. (6) gives \(\mathcal T(\omega)=4\operatorname{Tr}[G_+\Gamma_LG_-\Gamma_R]\), and Eq. (7) reduces it to \(4\Gamma_L\Gamma_R|G^+_{1N}|^2\) for their single-channel 1D chain. The full text states that the NEGF expression keeps its form for arbitrary reservoir geometries, while its interpretation in terms of plane-wave channels becomes more involved (Introduction, lines 24–25). This is the relevant warning for multiple links/channels: the observable is a matrix transmission, not a scalar local compliance. Primary text: [arXiv:1204.5595](https://arxiv.org/abs/1204.5595).

There is also a genuine, but different, causal thermal sum rule. Shastry, “A Sum Rule for Thermal Conductivity and Dynamical Thermal Transport Coefficients in Condensed Matter—I,” arXiv:cond-mat/0508711, Eq. (21), derives

\[
\int_0^\infty \operatorname{Re}\kappa(\omega)d\omega
=\frac{\pi}{2\hbar T\mathcal L}\langle\Theta^{xx}\rangle,
\]

with \(\Theta^{xx}\) defined by a long-wavelength commutator of heat current and energy density (Eqs. (10)–(13)); it also works out a 1D harmonic lattice example (Eqs. (55)–(56)). This is a frequency-integrated *linear-response thermal conductivity* rule, whose operator is a heat-current/energy-transport object. It is not the Bose-weighted ballistic passband-count objective and it is not the static compliance of an internal displacement. Full primary text: [arXiv:cond-mat/0508711](https://arxiv.org/abs/cond-mat/0508711), especially Eqs. (10)–(13), (21), and (55)–(56).

## What Foster and Bode–Fano cover

Foster’s primary “A Reactance Theorem,” *Bell System Technical Journal* 3, 259–267 (1924), DOI [10.1002/j.1538-7305.1924.tb01358.x](https://doi.org/10.1002/j.1538-7305.1924.tb01358.x), states that a finite lossless one-port has alternating resonance/antiresonance frequencies and can be synthesized from resonant branches; the paper notes the proof’s mechanical small-oscillation analogy. The publisher abstract was read (lines 57–59); the full article was not acquired. This is relevant to positive rational driving-point response and the star-network realization, but says nothing about a Bose-weighted bulk conductance optimum.

Fano’s primary “Theoretical Limitations on the Broadband Matching of Arbitrary Impedances,” *J. Franklin Inst.* 249, 57–83 (1950), DOI [10.1016/0016-0032(50)90006-8](https://doi.org/10.1016/0016-0032(50)90006-8), scopes its integral constraints to the logarithm of a matching network’s reflection coefficient for a prescribed load impedance. Its official abstract was read; the full article was not. Such bounds are a useful analogy for causal bandwidth tradeoffs, but their matched-load/reflection observable is not a periodic bulk passband count. No Bode–Fano result inspected here subsumes the proposed question.

## Comparison to the one-link and multi-link questions

The currently owned one-link theorem uses the special Bloch pencil

\[
D(q)=D_0+4K\sin^2(q/2)vv^{\mathsf T}.
\]

That rank-one structure supplies the exact full-spectrum moments and interlacing used in its Bose-dual proof. The exact optimal CM compliance \(C_Y=1/k_*\) is an additional consequence of the optimizer’s fixed bright two-dimensional subspace. The classical FDT/Kramers–Kronig relation is consistent with this compliance result, but does not independently give the bulk indicator moments, the sign pattern of the Bose dual, or the global one-resonator minimizer. Those stronger conclusions require the one-link spectral structure and the theorem’s fixed \(M,K,m_0\) resource contract; they are not a standard direct corollary of compliance/FDT.

For multiple identical parallel links between the same pair of neighboring-cell coordinates, the springs simply sum to a single effective \(K\), so the rank-one premise is unchanged. For distinct intercell connection patterns, the Bloch matrix is generally of the form \(D(q)=A_0+A_1e^{iq}+A_1^{\mathsf T}e^{-iq}\) (and can have higher harmonics for longer-range links), with matrix-valued bright subspaces. A single scalar \(w^{\mathsf T}D(q)^+w\) cannot in general determine its determinant or all channel transmissions; \(\partial_qD(q)\) is not generally a semidefinite rank-one update. The Landauer trace still applies, but the scalar rank-one trace/log-determinant moment proof does not transfer without new hypotheses and a new derivation.

**Bounded conclusion:** the standard response literature gives a causal integral identity for the internal compliance and the equilibrium fluctuation floor; standard harmonic transport literature gives a separate Landauer matrix-trace expression; thermal-conductivity sum rules and Foster/Fano network bounds constrain other observables. No inspected primary source directly derives a bulk one-link Landauer passband/conductance lower bound from prescribed internal-CM static compliance. This is a bounded “no direct match found,” not a priority or novelty claim.

## Version clarification for Shastry

The equation numbers above were copied from the unversioned arXiv HTML capture I read; I did not establish its e-print version. The current v6 primary text uses Eq. (18) for the integrated thermal-conductivity sum rule and Eqs. (49)–(50) for the harmonic example (parent independently checked v6). The previously recorded Eqs. (21), (55)–(56) refer to the capture's numbering and should not be carried forward as v6 references. The observable and scope distinction above is unchanged. Cite the [v6 primary text](https://arxiv.org/abs/cond-mat/0508711v6) with v6 numbering when exact equation numbers matter.
