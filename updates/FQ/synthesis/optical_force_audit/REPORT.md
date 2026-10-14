# Independent optical-force audit

15 October 2026. Source repository pin `00631610750c708263d5cf6d812ebbb8edc77335`. Incoming file and capital provenance are in `receipt.json`; full mathematics is in `DERIVATIONS.md`; reproducible arithmetic is in `calculate.py` and `results.json`.

**Disposition:** The transparent prescribed-field two-color pressure is internally consistent, but no same-regime GaAs retained-writing capability is established. Four exact conditional restrictions sharpen N821's existing acquisition boundary. They reject particular implementations and transfers, not all possible phase-directed structural control. Historical originality, actual hot coupling/loss/mobility, and useful retained-output advantage remain **UNKNOWN**.

## The reconstructed operation

The source proposes an externally phase-locked `omega/2omega` drive acting on verified inversion-related GaAs variants, followed by signed APB movement and a useful polarity pattern retained after light and annealing cease. In its local transparent scalar limit,

\[
f_s=-s\frac{\epsilon_0\chi_{\rm eff}^{(2)}}4E_1^2E_2\cos\Phi,
\qquad p_\Phi=\frac{\epsilon_0\chi_{\rm eff}^{(2)}}2E_1^2E_2\cos\Phi.
\]

Here `E1,E2` are peak **internal** fields. `chi_eff=100 pm/V`, `n=3.3` and equal fields are illustrative source normalizations. At `E=10^8 V/m` they give 442.7 Pa and 4.38 GW/cm² per color. The source's `10^-7` duty fraction gives average pressure `4.43e-5 Pa` only for its fixed-temperature linear-mobility law. Neither that mobility nor the hot susceptibility was acquired. The existing N821 normal-incidence (001) bulk-tensor null remains decisive for that geometry; oblique, cavity or waveguide geometries require their own actual tensor/mode overlap.

## 1. Spatial averaging turns the scalar pressure into a wall-overlap law

For a rectangular rigid wall, tangent dimensions `L1,L2`, normal position `X`, and relative wavevector `q`,

\[
F_X/A=p_0\prod_j\operatorname{sinc}(q_{tj}L_j/2)
\cos(\Phi+q_nX+\mathbf q_t\!\cdot\!\mathbf r_c).
\]

An integer beat length along a uniform lossless tangent dimension cancels the net force **at every phase**. If mismatch lies along the travel direction, fixed phase instead produces a periodic potential with exactly zero work per beat. Static isothermal gradient motion approaches a potential minimum; it does not supply indefinitely directed pressure.

These statements exclude neither a thin boundary nor measured standing/cavity modes with an appropriate overlap. They also do not make every patch of a flexible wall stationary. In fact, the cold 22 °C dispersion example gives overlap magnitude 0.99738 across 400 nm at 2.3/1.15 µm and 0.99996 at 4.6/2.3 µm. Thus **no thickness-cancellation rejection of the 400 nm assay is claimed**. Its hot optical overlap still needs measurement; the relevant primary fit measured temperatures only through 95 °C. [Skauli et al.](https://doi.org/10.1063/1.1621740).

An adaptive phase ramp can translate this periodic potential. In the freely moving, linear-mobility model, locked motion at speed `v` requires `|v|<M p_max`. This is a concrete conditional mechanism mutation, with control and energy costs, not an acquired repair operation or a historical novelty claim.

## 2. Hot gap narrowing opens loss channels omitted by a one-beam screen

Panish–Casey's primary absorption measurements cover 300–973 K. Their published GaAs gap fit gives `Eg(650 °C)≈1.11790 eV`. Within that fit:

| Requirement for an `omega/2omega` pair at 650 °C | Necessary fundamental wavelength |
|---|---:|
| SH one-photon / pump two-photon transition below the direct gap | `>2.218 µm` |
| Mixed-color two-photon transition below the direct gap | `>3.327 µm` |
| All interband one- and two-photon channels below the direct gap | `>4.436 µm` |
| SH three-photon transition also below the direct gap | `>6.655 µm` |

These are energetic screens, not predictions of an absorption rate. [Panish and Casey](https://doi.org/10.1063/1.1657024).

The cold 1.8/0.9 µm cavity precedent's harmonic crosses the fitted gap around 152 °C. It cannot carry its “below-gap harmonic” premise into a 650 °C anneal. At 2.3/1.15 µm the harmonic is only 39.8 meV below the fitted hot gap, while harmonic 2PA and mixed-color 2PA remain open. Counting only the fundamental's cold 3PA cannot qualify the two-beam thermal state. Nondegenerate two-photon absorption is directly demonstrated in GaAs, but its coefficient in the actual hot capped film is unmeasured here. [Buckley et al.](https://doi.org/10.1021/ph500054u), [Apiratikul and Murphy](https://photonics.umd.edu/pubs/ja-30/).

Longer wavelengths are a possible experiment choice, not a free loss exemption: free-carrier, defect, higher-order and thermal absorption, hot nonlinear coupling, mode confinement and source cost remain coupled.

## 3. A rooted wall can bow while its APB root remains

With fixed substrate root, free film top, thickness `d`, uniform pressure `p` and isotropic wall tension `gamma`, the exact graph-equilibrium displacement is

\[
X_{\rm top}=\frac{pd^2/\gamma}{1+\sqrt{1-(pd/\gamma)^2}}
\simeq pd^2/(2\gamma),\quad |p|d<\gamma.
\]

Holding the root fixed precludes complete through-film erasure of that root. Exceeding the graph-equilibrium threshold does not by itself prove depinning or a legal interface reconstruction.

Using the published **static DFT** `gamma110=28 meV/Å²≈0.449 J/m²` merely as a normalization gives 0.079 nm top bow for the source's 443 Pa in a 400 nm film, or 2.13 nm for its 11.95 kPa example. These are not measured hot displacements. The same model says a cylindrical selected-polarity island can reverse its radius drift only if `p_max>gamma/R`; the middle source pressure and static normalization give `Rc≈1.01 mm`. A flat unrooted wall can avoid these restrictions. The actual hot orientation stiffness, root state, pinning and wall mobility must be measured together. [Rubel and Baranovskii, Table 1](https://www.mdpi.com/1422-0067/10/12/5104).

## 4. Self-generated SHG cannot supply its own polarity reference

For the source Hamiltonian, `Na+2Nb` is exactly conserved by lossless three-wave mixing. Force and conversion occupy real and imaginary quadratures, so zero instantaneous conversion does not mean zero force or sustained free work. In a cavity with no independently injected harmonic, global inversion sends `g -> -g` and `beta -> -beta`, leaving the mechanical force invariant. This symmetry persists with pump depletion when the remaining optical/material laws respect the same inversion. A separate phase-locked harmonic seed provides the missing reference; the source already supplies one. This result rules out an unseeded cavity substitution, not the source's seeded operation.

Nonlinear optical force/torque is not itself new physics: force sensing of nonlinear polarization is experimentally established, and a published theory treats torque transferred through nonlinear scattering. Neither demonstrates internal GaAs APB rewriting. [Schumacher et al.](https://doi.org/10.1073/pnas.2003945117), [Toftul et al.](https://doi.org/10.1103/PhysRevLett.130.243802).

## Precise missing experiment and stop rule

Use one structurally and polarity-mapped, composition-protected GaAs specimen at the intended annealing temperature, with a nonzero tensor geometry and a mapped accessible boundary exit/annihilation path. A rooted and a released/exit-connected boundary must not be treated as equivalent. Acquire complex signed nonlinear response, local two-color fields/phase through the thickness, both-color and mixed absorption, carrier history, temperature/strain, and wall pinning/kinetics in this same state. Infer the predicted generalized force from that independently calibrated interaction, rather than fitting it to the desired final displacement.

Then randomize phase-reversed, quadrature, phase-incoherent, single-color and matched measured thermal/carrier controls across comparable initial boundaries. A moving-phase implementation additionally needs positive/negative ramp and stationary-phase controls. Record signed boundary trajectories and the final three-dimensional polarity/defect/composition map after drive removal at a declared retention horizon; check a guard region for buried roots, relocated damage and material loss. Require the chosen polarity to occupy the declared useful volume and pass an application-relevant functional assay. An optical signal or surface disappearance alone fails the endpoint.

Reject the specified operating point if its acquired force-overlap/pinning bounds or `integral M(T,n,X,...) p(t) dt` upper bound cannot reach the declared displacement, or if the apparent selection is explained by measured heat/carriers/material loss. Compare successful retained output against optimized dark annealing and template bonding/regrowth, including source wall energy, both colors, phase stabilization, preparation, cap/ambient, heating/cooling, readout, reset if relevant, throughput and yield. No favorable unknown parameter is inserted to pass this gate.

`calculate.py` passed independent numerical cycle/overlap integration, static-force work, complex-amplitude conservation/parity, and exact elastica checks. These validate the specified internal algebra and arithmetic only. No N821 physical or review gate is closed.
