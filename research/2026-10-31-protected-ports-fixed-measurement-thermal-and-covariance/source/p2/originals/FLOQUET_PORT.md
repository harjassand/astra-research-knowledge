# Cold-port filtering during the driven STAR operation

This calculation tests whether the proposed passive cold port causes charge escape while the STAR is driven. It uses all twenty states in the N=4, S=0 Hubbard sector. The computation oscillator, the root positive-capacitance model's counterterm, loading ramps and finite-coupling error bounds are absent. It is a component calculation within the stated Floquet weak-coupling bath model.

## Method and physical convention

Use the driven STAR point

\[
 U=1,\quad t=.1,\quad b=.005,\quad \epsilon_0=.4,
 \quad \omega_d=.05,
 \quad t_{12}(t)=\sqrt{t^2+b\cos\omega_dt}.
\]

The remaining two hopping amplitudes stay at t. A midpoint propagator is constructed over one period. A complex unitary Schur decomposition is performed separately in the two conserved outer-swap parity spaces. This avoids an arbitrary mixing of the degenerate logical branches in the zero-drive check. The two active modes are selected by their overlaps with the corresponding instantaneous low singlet states at the initial drive phase.

Let U(T)u_j=exp(-iq_jT)u_j, psi_j(t)=U(t)u_j and phi_j(t)=exp(iq_jt)psi_j(t). For the central density n_c-1, define

\[
 A_{ij}(t)=\langle\phi_i(t)|(n_c-1)|\phi_j(t)\rangle
 =e^{i(q_j-q_i)t}\langle\psi_i(t)|(n_c-1)|\psi_j(t)\rangle,
\]

\[
 A_{ij,m}={1\over T}\int_0^T A_{ij}(t)e^{-im\omega_dt}\,dt.
\]

The energy emitted to the bath in a transition j to i through harmonic m is

\[
 \nu_{ijm}=q_j-q_i-m\omega_d.
\]

The explicit drive-harmonic term is essential: a quasienergy chosen in one zone is not by itself a physical emitted energy. The static limit checks this sign convention. Floquet bath treatments of this form are established machinery; see Kohler, Dittrich and Hänggi, *Floquet-Markov description of the parametrically driven, dissipative harmonic quantum oscillator*, https://arxiv.org/abs/quant-ph/9809088. Its discussion also makes clear that degenerate transition frequencies require the corresponding nonsecular terms to be retained in a full master equation.

The root spectral function is used directly from `renewal_filter.py`:

\[
 S(\nu)={\nu\over1-e^{-\beta\nu}}R(\nu),\qquad \beta=200,
\]

with the continuous thermal limit at zero frequency. The two dimensionless impedance ratios are

\[
 R_{\rm RC}(\nu)={1\over1+(\nu/.8)^2},
\]

\[
 R_{\rm RLC}(\nu)={1\over1+Q^2(\nu/\omega_0-\omega_0/\nu)^2},
 \quad Q=1,\quad\omega_0=.8.
\]

The overall coupling is eta=.000200272. The RLC zero-frequency ratio is zero. These are the same cold-port parameters used for renewal in the root calculation; no separate tiny gate-noise constant is assigned.

In the weak-coupling transition model,

\[
 W_{i\leftarrow j}=\eta\sum_m|A_{ij,m}|^2S(\nu_{ijm}).
\]

Summing i outside the two selected active modes gives their escape rates. The diagonal logical dephasing rate is

\[
 \Gamma_{\rm diag}={\eta\over2}\sum_m
 |A_{00,m}-A_{11,m}|^2S(-m\omega_d).
\]

All resolved FFT harmonics are included. The integration grid runs from 512 to 1024 to 2048 midpoint samples. Harmonic-tail contributions beyond absolute index 32, 64 and 128 are preserved in the result file.

## Results at the supplied gate duration

For T_gate=102459/U, the 2048-step results are:

| Bath spectrum | Diagonal dephasing action | Escape action, first branch | Escape action, second branch |
|---|---:|---:|---:|
| RC | 1.9361770e-5 | 1.23669e-17 | about 1.5e-24 |
| RLC | 7.7648700e-8 | 2.09400e-21 | about 3.4e-26 |

The second-branch escape numbers are dominated by numerical noise. They should not be quoted as resolved physical rates. The first-branch RLC rate per unit eta is 1.01869e-22, 1.02013e-22 and 1.02048e-22 on the three grids. Its absolute-index-greater-than-64 tail is about 1.19e-28 per unit eta, well below the resolved contribution. The RC first-branch rate is about 6.02684e-19 per unit eta. The logical transition rates between the two parity branches vanish analytically because central density preserves that parity; numerical output retains their floating-point residuals.

The RLC spectrum therefore suppresses the projected driven dephasing by about a factor of 249 in this component model, while the fully resolved driven charge-escape channel is negligible at the displayed point. The active drive does not uncover a large bath-assisted charge transition that negates the spectral-filtering gain in this calculation.

Escape means departure from the two selected active Floquet modes. It is not automatically irreversible destruction of the larger symmetry-protected logical subsystem: some escaped charge states can retain encoded information. Conversely, their different active response can invalidate the qualified gate, so ignoring these transitions would also be unjustified. The calculation supplies the relevant event rates without identifying every departure with a complete logical failure.

## Static consistency and numerical floor

With b=0 the rates can be computed directly from the static eigenstates and their true energy differences. At beta=5, where thermal upward rates are large enough to resolve, the Floquet calculation agrees with this independent expression:

| Spectrum | Direct static escape rate per unit eta | Largest absolute Floquet difference |
|---|---:|---:|
| RC | 8.47670305235e-4 | 1.89e-15 |
| RLC | 1.26932955153e-3 | 2.82e-15 |

At beta=200 the true static upward rates are about 5.1e-60 for RC and 7.5e-60 for RLC. The sampled Floquet calculation instead reaches a floor around 1e-27. This check is why the tiny second-branch driven escape values are reported only as numerical-floor estimates. There are no certified rounding enclosures.

The active Schur residual is below 5e-12 at the largest grid. The low-mode overlaps reproduce the earlier periodic-density calculation. The resulting diagonal dephasing action includes the full resolved harmonic sequence and agrees with the root short-harmonic estimate.

## What remains outside this calculation

The root filter has passed a stronger check than comparing only low-frequency noise or diagonal expectation values: actual off-diagonal transitions of the periodically driven Hubbard system have been included. It still relies on an equilibrium bath, weak coupling, the stated spectral density and the appropriate Floquet secular treatment. A complete retained-memory channel must treat any resonant transition degeneracies consistently and bound the approximation at finite coupling.

The oscillator supplying the computation force is not present. Attaching it changes the periodic modes and introduces conditional motion, finite-energy requirements, its own loss, and the capacitance counterterm. Ramps, source preparation, readout, detector renewal, symmetry mismatch and the full interaction incident sum must still fit the physical duration/error region. The present rates do not certify a combined device or a computation threshold.

Executable preservation:

- `star_floquet_port.py`: full periodic-mode transition and dephasing calculation.
- `star_floquet_port_results.json`: convergence, harmonic tails and static consistency output.
- `star_floquet_force.py`: includes `force(..., return_waveform=True)` for direct access to the sampled density difference, branch samples and midpoint phases.

