# Merged harmonic trap: bounded PA comparison

This addendum recomputes only the previously declared 396.5 MHz photoassociation model and the four known p-wave lines for a cold singlet and the lowest triplet spatial state in one harmonic trap. It does not establish the behavior of an arbitrary-orbital cooling cycle. Sources, molecular conventions and incomplete-spectrum qualifications remain those in `PA_AUDIT.md`.

## 1. The Gaussian contact, recalculated

For an isotropic harmonic orbital with l=sqrt(hbar/(m omega)),

\[
\int|\phi|^4d^3r=\frac1{(2\pi)^{3/2}l^3},\qquad
\Gamma=4\sqrt{\frac2\pi}\,\omega\frac{\ell_{\rm opt}}l.
\]

The coefficient is 3.191538. The old two-well Wannier calculation gave a coefficient about 0.177% smaller. At the same desired Gamma, the merged Gaussian therefore needs about 0.177% less PA intensity. The following values use the convenient explicit choice Gamma/omega=0.01, slightly above the old two-well value 0.00978684.

Using omega/(2pi)=100 kHz, the 396.5 MHz theoretical molecular line with optical length per intensity 840 a0/(W/cm²), and the same zero-field pi-light hyperfine calculation gives:

| Quantity | Recalculated value |
|---|---:|
| Harmonic length l | 24.3123 nm |
| Pair loss rate Gamma | 6283.185/s |
| Optical length | 1.439542 a0 |
| PA intensity | 1.713741 mW/cm² |
| Omega_D/Gamma_m, inferred weak molecular model | 0.0618984 |
| Per-atom Rayleigh rate | 0.164054/s |
| Per-atom Raman rate | 0.101308/s |
| Pair Raman hazard per Gamma exposure | 3.22475×10⁻⁵ |
| Pair total atomic-photon hazard per Gamma exposure | 8.44674×10⁻⁵ |

The harmonic trap removes the previous requirement for a stationary 119 nm two-well tunneling profile. It supplies no proof that merging, cooling, splitting or the actual trap source is spin-transparent.

## 2. Direct cold-singlet absorption uses log(1/q)

If a cold singlet remains in the admitted orbital and has constant useful pair-loss rate Gamma, its survival is q=exp(−Gamma T). Thus Gamma T=log(1/q), rather than the earlier sufficient charge-star exposure 12.5 log[9/(7q)]. This is an actual change of model, not an optimization claim about the old theorem.

For q=10⁻⁶, the direct cold absorption time is 2.198807 ms and Gamma T=13.815511. It gives pair Raman hazard 4.45515×10⁻⁴ and total atomic-photon hazard 1.16696×10⁻³. Elastic Rayleigh scattering is spin-scalar under the ideal angular-momentum assumptions; recoil and band changes still cost resources.

Cold singlet survival q is not the complete measurement-instrument error. Residual branch coherence, any physical molecule/atom return, replacement and the surviving triplet channel must be included separately.

## 3. On-site s+p restores the p-wave contact weight

The lowest antisymmetric harmonic spatial state has the geometry factor F_geom=1. The old separated-site value was 2.4620×10⁻⁴. Applying the same conservative positive-matrix trace bounds to the same four molecular lines gives:

| Theoretical p-line binding | Loss/Gamma upper bound | Absolute shift/(hbar Gamma) upper bound |
|---|---:|---:|
| 279 MHz | 1.59867×10⁻⁶ | 5.16055×10⁻⁴ |
| 355 MHz | 3.32134×10⁻⁶ | 3.78670×10⁻⁴ |
| 383 MHz | 2.69167×10⁻⁵ | 9.98284×10⁻⁴ |
| 416 MHz | 2.86327×10⁻⁵ | 1.53389×10⁻³ |
| Sum | 6.04694×10⁻⁵ | 3.42690×10⁻³ |

The coherent shift is the larger issue after this change. A measured total loss rate does not qualify that shift as scalar on the triplet.

### Remove scalar phases before charging logical disturbance

Each isolated molecular line contributes a signed positive matrix to the effective Hamiltonian. If its trace/norm upper bound is h_m, its spectrum lies in an interval of length at most h_m. Subtracting the midpoint of that interval times the identity gives a norm bound h_m/2. Summing these scalar centers is allowed: a global phase is irrelevant.

Thus the known-four-line globally centered Hamiltonian satisfies the sufficient estimate

\[
\inf_{c\in\mathbb R}
\frac{\|H_{p,\rm known}/\hbar-cI\|}{\Gamma}
\le1.71345\times10^{-3}.
\]

This bound does not identify the actual anisotropic component. A complete matrix might show further cancellation or a larger harmless spin-scalar orbital action. Neither is presumed here. No RF correction, polarization averaging or molecular spin transparency is supplied.

## 4. Complete cold-window budgets within the four-line diagnostic

| Cold singlet survival q | Loss time | Pair Raman hazard | Known p-loss hazard bound | Centered coherent phase-norm bound |
|---|---:|---:|---:|---:|
| 10⁻² | 0.73294 ms | 1.48505×10⁻⁴ | 2.78472×10⁻⁴ | 0.00789073 |
| 10⁻³ | 1.09940 ms | 2.22758×10⁻⁴ | 4.17708×10⁻⁴ | 0.0118361 |
| 10⁻⁶ | 2.19881 ms | 4.45515×10⁻⁴ | 8.35415×10⁻⁴ | 0.0236722 |
| 10⁻⁹ | 3.29821 ms | 6.68273×10⁻⁴ | 1.25312×10⁻³ | 0.0355083 |

The last column also gives a sufficient upper bound on the coherent channel's half-diamond distance, by global phase adjustment and Duhamel's inequality. Without centering, the corresponding raw phase-norm budgets are twice as large. These are conservative upper bounds, not lower bounds or observed errors. Loss hazards are likewise upper budgets within the specified weak, isolated-line model.

## 5. What this comparison settles

Direct cold-singlet absorption substantially reduces required exposure. Losing the separated-triplet overlap suppression makes the coherent molecular correction the largest quantified budget in this restricted comparison. Already at q=10⁻⁶, the known-line centered bound is approximately 2.4%, while the known p-loss and atomic Raman hazards are each below 0.1%.

This does not prove a 2.4% irreducible error or establish a device window. The four-line sum omits molecular states and uses low-energy optical-volume data in place of a finite trapped Franck–Condon calculation. Theoretical and measured line positions must not be mixed. The usable escape fraction is still unqualified.

Most importantly, the values apply to a cold singlet and the lowest p-wave triplet orbital. Cooling from arbitrary orbitals needs an energy-dependent bound on the actual Franck–Condon matrices and the integrated cooling/PA exposure. State-independent scalar cooling does not make the PA source spin-transparent. The central missing join remains the full molecular operator acting on the admitted spin and orbital domain.

Executable preservation: `pa_merged_checks.py` writes `pa_merged_results.json` and reuses the source parameters in `pa_checks.py`. These are ordinary floating-point model calculations, without certified enclosures.
