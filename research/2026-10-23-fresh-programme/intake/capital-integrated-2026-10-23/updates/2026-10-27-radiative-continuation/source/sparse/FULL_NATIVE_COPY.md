## ASTRA — Spatiotemporal radiation echo: a simpler exact construction

New result: The five-mode radiation-echo Hamiltonian can be reduced to a four-mode active system with substantially simpler controls, while retaining exact finite-time state transfer and complete cancellation of radiation at the final time.

The reduction exploits mirror symmetry between the two outer emitters. Their antisymmetric combination never becomes populated, so only the symmetric outer mode, central emitter and two storage modes are needed.

The resulting internal Hamiltonian is

\\[ H\_{\mathrm{int}}(t)=\mu I_4+ \begin{pmatrix} 0&0&C\_{ao}&C\_{ac}\\\ 0&0&C\_{bo}&C\_{bc}\\\ C\_{ao}&C\_{bo}&0&J\_{oc}\\\ C\_{ac}&C\_{bc}&J\_{oc}&\Delta_c \end{pmatrix}. \\]

All controls are real. The network has no direct storage-to-storage coupling.

For the same positive-frequency continuum and exact source trajectory as the preceding research, the independently executed full Schrödinger calculation gives:

| Property                                        | Result                   |
| ----------------------------------------------- | ------------------------ |
| Complete state-transfer error                   | \\(5.42\times10^{-11}\\) |
| Final radiation amplitude norm                  | \\(2.65\times10^{-14}\\) |
| Maximum storage–emitter hopping                 | \\(1.027B\\)             |
| Maximum additional emitter coupling or detuning | \\(1.76\times10^{-4}B\\) |
| Minimum sampled internal Schur margin           | \\(5.04B\\)              |

The exact final radiation cancellation follows analytically from the delayed-source equations; the nonzero residuals are numerical.

More importantly, I derived a continuous-time positivity bound, independent of any time grid:

\\[ \boxed{ H\_{\mathrm{int}}(t)-W^\dagger\omega^{-1}W \succeq1.46B\\,I \quad\text{for every }t. } \\]

This preserves the positive, gapless continuum Hamiltonian while eliminating several controls from the earlier construction.

## 2. Two fundamental control obstructions

The construction also reveals where simpler interfaces fail.

Stationary reciprocal transfer. For a time-independent, time-reversal-symmetric Hamiltonian, exact transfer between orthogonal localized states implies

\\[ U(2T)|a\rangle=e^{2i\phi}|a\rangle. \\]

The spectral theorem then forces the initial state's energy measure onto a discrete arithmetic set. Therefore:

\\[ \boxed{\text{Exact stationary reciprocal transfer cannot involve a genuine continuous radiative spectral component.}} \\]

A purely bound or dark subspace escapes the theorem, as does nonreciprocal propagation or time-dependent control.

This is consistent with recent passive giant-atom transfer research, which exploits engineered propagation and, in an important ideal construction, chiral coupling.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://journals.aps.org\&sz=32)

PRX Quantum

+1



Fixed hopping with onsite-only control. The prescribed smooth radiation echo cannot be realized using permanently fixed storage–emitter hoppings and only variable onsite energies. Its required zero initial emitter derivative would force those storage connections to vanish permanently.

Within the exact four-mode, real-carrier construction, I also proved why all five hopping connections and the central emitter detuning are needed for this particular trajectory. This is not a universal minimum-control theorem.

## 3. Moving-window radiation and a stronger-coupling test

A useful additional identity emerged:

\\[ \boxed{ \\|\xi(t)\\|\le2\sqrt2\\,\alpha\tau\\|v\\|\_2. } \\]

The transient radiation is determined entirely by two adjacent temporal windows of width \\(\tau\\). The complete earlier emission history cancels from the radiation amplitude.

I increased the physical continuum coupling while retaining the same source geometry.

At \\(\eta=0.60\\), the executed model gives a peak transient radiation probability of approximately 2.91%, complete final radiation cancellation and a positive sampled Schur margin of \\(2.43B\\). At \\(\eta=0.80\\), the sampled Schur margin becomes negative.

The latter is a decisive warning: exact final radiation cancellation does not itself guarantee a stable all-particle Hamiltonian. The stronger-coupling examples have not received the continuous-time positivity certificate established for the original weaker coupling.

## 4. A new four-emitter opportunity

The most consequential unresolved issue is physical locality. In the three-emitter echo, the first and last nonzero radiation sources must both occur at the middle emitter.

I proved a more general support-order theorem: in any finite, exactly terminally dark bidirectional emitter array, neither spatially outermost emitter can be the first or last source to radiate.

For four emitters, the restriction can be evaded. I constructed two exact source-null generators whose combination starts emission at emitter 2 and finishes at emitter 3. The executed Fourier cancellation residual is below \\(7.7\times10^{-16}\\).

This is a new source construction, not yet a physical state-transfer Hamiltonian. Its importance is that it identifies the smallest geometry in which source and destination can occupy distinct interior emitter positions. The next difficult step is realizing those histories through genuinely local controls, without an internal bypass.

## 5. Finite-control implementation

The four-mode Hamiltonian was also tested with piecewise-constant controls rather than continuously varying waveforms.

| Equal-duration control steps | Full state-vector error |
| ---------------------------- | ----------------------- |
| 32                           | 0.402%                  |
| 64                           | 0.101%                  |
| 128                          | 0.0251%                 |
| 256                          | 0.00629%                |

These are exact unitary propagations of the discretized finite-band Hamiltonian. They are numerical diagnostics, not certified hardware tolerances.

## Saved research

The full derivation includes the constructive inverse-control theorem, analytic positivity proof, stationary reciprocal no-go, geometry theorem, moving-window identity and explicit failures.

Complete proof and scientific findings

The executed checks are preserved as full Hamiltonian and state-transfer code, continuous-time certificate, finite-pulse simulation, and four-emitter source construction, with four-emitter results.

Scientific judgment: The strongest generalizable result is the distinction between stationary radiative transfer, time-delayed source cancellation, and dynamically realizable local controls. The four-mode mechanism is now constructive and stable, but it still permits internal connections that bypass the radiation channel. A true spatially separated, waveguide-mediated transfer with a restricted local control graph remains unproved. That is the stronger target than further optimizing the existing echo's fidelity.