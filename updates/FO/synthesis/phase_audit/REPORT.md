# Cold audit: phase-selective retained GaAs rewriting

**Audit status:** independent algebra and source audit completed. The physical operation remains an unvalidated hypothesis. This audit produced no physical experiment, atomistic calculation, independently reviewed result, novelty result, or industrial comparison.

## Decision

The incoming complete-melting calculation is correct inside its narrow model. At \(T_0=298.15\) K, equal-molar patches, fixed GaAs composition, equilibrium melting, no heat exchange during dose partition, and actual net deposited thermal doses \(Q(1\pm C)\), one patch can fully melt while the other remains strictly below onset only when
\[
C > C_* = \frac{L}{2H_s+L}=0.44849\ldots.
\]
That means a hot-to-cold **specific deposited-energy** ratio above 2.6264. This is not a universal no-go for partial interfacial melting, nonthermal transitions, sustained heating, unequal geometries, or local bond rearrangement. It also says nothing about successful recrystallization or retained polarity selection.

The bulk impulsive-melting path does not merit scale-up on the evidence in hand. Its decisive gate is a same-specimen measurement of phase-odd **local net heat** under the intended fluence, cap, temperature, and geometry. If that contrast is below the model's threshold, stop that bulk full-melt route. The strongest next physical experiment is a small, mapped, phase-reversal test of retained motion or bond rearrangement at a nearly flat boundary, with structure, composition, and thermal controls. First fix the optical geometry: ideal bulk QUIC population control is exactly zero for normal-incidence (001) illumination with purely in-plane fields. This geometry restriction is not a no-go for oblique-polarization, interface, CASH, or other mechanisms.

The most relevant acquisition template among the current capital gates is N789's same-specimen phase-, basis-, energy/angle-, and dose-resolved retained-event curve. N789's Te mechanism is not evidence for GaAs. N783 adds the right discipline around surviving carriers, retained rewards, and full costs, but its hBN repair chain is a separate chemistry. N814's gate concerns net work returned to a reusable bus at fixed saleable product and is not the relevant first gate for this laser-writing hypothesis. All three capability gates remain open.

## Reconstructed thermodynamic bound

The [Yamaguchi, Itagaki and Yazawa (1989) GaAs fit](https://doi.org/10.2320/jinstmet1952.53.8_764) gives the solid heat content relative to \(298.15\) K, in J/mol,
\[
H(T)-H(298.15)=47.3T+3.99\times10^{-3}T^2+2.40\times10^5/T-1.53\times10^4.
\]
For \(T_m=1514\) K, it gives \(H_s=65{,}616.5825\) J/mol from room temperature to melt onset. The source reports \(T_m=1514\pm1\) K and \(L=106.72\pm0.20\) kJ/mol. Thus complete melting from room temperature requires:

- sensible heat: \(65.617\) kJ/mol;
- latent heat: \(106.720\) kJ/mol;
- total: \(172.337\) kJ/mol, or \(1.19145\) MJ/kg and \(1.78614\) eV per GaAs formula unit.

Using the \(5.32\) g/cm³ density used in the cited laser-decomposition study, that total is about \(6.3385\) kJ/cm³. These are equilibrium enthalpy conversions, not a pulse-fluence specification: absorbed depth, reflectance, carrier escape, heat transport, cap chemistry, and non-equilibrium transitions are not included.

For equal-molar patches, write \(q_h=Q(1+C)\) and \(q_c=Q(1-C)\), in J/mol. Full melting and strict protection require
\[
Q\ge\frac{H_s+L}{1+C},\qquad Q<\frac{H_s}{1-C}.
\]
The interval is nonempty exactly when
\[
(H_s+L)(1-C)<H_s(1+C),
\]
equivalently \(C(2H_s+L)>L\). At equality the endpoints coincide, and the strict cold-patch inequality makes the interval empty. At room temperature \(C_*=0.4484916\), and the threshold dose ratio is
\[
\frac{q_h}{q_c}=\frac{1+C_*}{1-C_*}=1+\frac{L}{H_s}=2.6264181.
\]

The incoming code's preheating values reproduce: \(C_*=0.57019\) at 800 K, \(0.64486\) at 1000 K, \(0.74555\) at 1200 K, \(0.88837\) at 1400 K, and \(0.98470\) at 1500 K. Preheating close to \(T_m\) removes the sensible-heat buffer while leaving fusion enthalpy, so this particular contrast requirement rises toward one.

For partial melting, if fraction \(f\) of the hot patch's moles melt while the cold patch remains below onset, then
\[
Q(1+C)\ge H_s+fL,\qquad Q(1-C)<H_s,
\]
so for \(C>0\)
\[
f<\frac{2CH_s}{(1-C)L},\qquad
\sup f=\min\!\left(1,\frac{2CH_s}{(1-C)L}\right).
\]
When the right-hand ratio is below one, the supremum is not attained because protection is strict. At room temperature, inserting hypothetical \(C=0.02,0.064,0.14\) gives suprema 0.02510, 0.08408, 0.20018. Those values are not measurements of heat contrast or molten fraction. They bound only this equal-patch, equilibrium, impulsive model; boundary-local melting and partial melt/regrowth can fall outside its spatial assumptions.

### Source uncertainty

Yamaguchi et al.'s Table 1 gives a GaAs solid heat-content error of ±100 J/mol over 800–1514 K, while Table 2 gives ±0.20 kJ/mol for fusion heat and ±1 K for \(T_m\). The paper does not give the error convention or fit-coefficient covariance in the accessed text. At \(T_m\), the fit derivative is \(C_p\simeq59.28\) J mol\(^{-1}\) K\(^{-1}\). If the listed ± values are provisionally treated as hard, independent magnitudes and the 1 K term is linearized, a room-temperature sensitivity envelope is approximately \(C_*\in[0.44743,0.44956]\). This is a sensitivity calculation, not a confidence interval; its upper \(T_m\) endpoint is 1 K beyond the tabulated solid-fit range. For preheated initial states, the uncertainty of \(H(T_m)-H(T_0)\) cannot be certified without covariance information. The nominal arithmetic is robust to this thermochemical uncertainty; the physical assumptions dominate.

## What the bound does and does not say

The model's \(C\) must be the phase-resolved difference in **net thermal energy per mole (or per formula-unit volume)** after optical and carrier energy exchange is accounted for. It is not automatically the carrier-generation modulation, incident-field modulation, transmitted-power modulation, or whole-patch energy difference. Under the ideal direct one-/two-photon interference model, phase-odd absorption and carrier generation are coupled; in a real capped sample, cascaded conversion, reflection, depth-dependent fields, carrier escape, damage, and delayed electron–phonon transfer can separate carrier count from retained lattice heat. Measure both colours' reflected and transmitted power, spatial absorption, carrier density, and delayed lattice temperature under the actual operating condition.

Equal patch amounts matter only if \(C\) is computed from equal-mass specific doses as the source does. A simple exact countermodel illustrates why total-patch joules are the wrong variable for unequal patches: set \(H_s=L=1\), hot and cold patch amounts \(n_h=1/4,n_c=1\), and give each patch total energy \(3/5\). Total-energy contrast is zero, but specific doses are \(12/5\) and \(3/5\); the first exceeds the hot full-melt requirement \(H_s+L=2\), and the second stays below \(H_s=1\). With uniform illumination and identical local response, total absorbed energy would ordinarily scale with amount; this countermodel is a warning against misdefining contrast, not a prediction of the GaAs process.

### Exact countermodels to an overbroad no-go

**Sustained heating with cooling.** Let equal lumped patches obey
\[
C_{\rm th}\dot T_\pm=P(1\pm C)-G(T_\pm-T_b)
\]
with equal conductance \(G\), and let \(\Delta=T_m-T_b>0\). Choose \(P=G\Delta\). For every \(0<C<1\), the cold steady temperature is \(T_m-C\Delta<T_m\), while the hot side has positive power \(G\Delta C\) available at \(T_m\). Once hot material reaches onset, a finite latent heat \(nL\) can be supplied in time \(t_L=nL/(G\Delta C)\), under the stated lumped assumptions. For \(C=0.02\), this normalized latent-heating time is 50 times \(nL/(G\Delta)\), not infinite. This exactly defeats a universal impossibility claim based on the impulsive threshold; it also makes the cost diverge like \(1/C\) as \(C\downarrow0\), and says nothing about correct regrowth. Inter-patch heat flow, temperature-dependent properties, and changing geometry would need a better model.

**Geometry can fake selection.** At \(C=0\), two equal patches with different thermal conductances \(G_h<G_c\) can satisfy \(G_h\Delta<P<G_c\Delta\): the weakly cooled patch reaches melt onset while the other stays below it. That is not phase selection. It shows why cap, substrate contact, boundary density, and illumination asymmetries must be measured and why switching \(\phi\) to \(\phi+\pi\) must switch the selected domain in a counterbalanced same-specimen test.

**Nonthermal and boundary-local routes.** The accessible abstract of [Sokolowski-Tinten et al. (1998)](https://doi.org/10.1103/PhysRevB.58.R11805) reports nonthermal melting within a few hundred femtoseconds above a distinct high-fluence threshold, and thermal melting on an approximately 100 ps timescale below that threshold. This confirms that equilibrium enthalpy is not a universal description, but it does not show phase-selected or retained polarity rewriting. A phase-reversible interfacial-bond transition or boundary-rate bias is another escape from the complete-bulk-melt calculation; its transition kernel and retained output remain unmeasured. Curvature-driven shrinkage or increased mobility alone is not proof of chosen-polarity control.

## Optical contrast, fluence, and geometry

Fraser et al. experimentally demonstrated phase-dependent carrier generation and net optical absorption in bulk GaAs using 1550/775 nm, approximately 120 fs pulses at 295 K ([1999 paper](https://doi.org/10.1103/PhysRevLett.83.4192)). Their (111)-oriented, 650 nm sample showed about 2% carrier-density modulation; the paper's 6.4% value at 1550 nm and 14% nearer the band gap are theoretical limits under their susceptibility model, not measured local thermal contrasts. The paper explicitly includes phase-dependent energy transfer and absorption. Stevens et al. later measured phase-dependent carrier/spin signals in a (110) GaAs/AlGaAs quantum-well structure with a 500 nm AlGaAs preamplifier ([2005 paper](https://doi.org/10.1063/1.1879079)); their experiment supports CASH-dominated carrier control in that stack, while “nearly 100%” is a proposed design prospect, not the measured result.

The Fraser experiment used peak incident irradiances around 9 GW/cm² at 1550 nm and 150 MW/cm² at 775 nm. For Gaussian 120 fs FWHM pulses, these correspond approximately to incident fluences of 1.149 mJ/cm² and 0.0192 mJ/cm². As a deliberately generous uniform-depth comparison, complete-melt enthalpy for a 650 nm GaAs layer is about 0.412 J/cm². Even if all incident two-colour energy were absorbed uniformly in that layer, it would be about 0.284% of that equilibrium enthalpy. This estimate assumes a Gaussian pulse, uniform 650 nm absorption depth, room-temperature density, and no nanoscale hotspot; it is not a claim about the original experiment's heat deposition. It shows why high peak irradiance does not supply a high-fluence-to-melting measurement. The 1999/2005 coefficients cannot be extrapolated through high carrier density, elevated temperature, cap-dependent propagation, nonlinear absorption, plasma/damage, or phase change. Conversely, low-fluence \(C\) does not upper-bound \(C\) at a different fluence. The contrast must be measured in the regime where a structural event is attempted.

There is also a hard ideal-bulk geometry check. For zinc-blende \(T_d\) symmetry the QUIC density-control tensor has its independent component \(j_{abc}\) with \(a,b,c\) the three distinct cubic axes \([100],[010],[001]\), or permutations. At normal incidence on (001), both optical fields are transverse and lie in the x-y plane; every contraction \(j_{ijk}E^\omega_iE^\omega_jE^{2\omega}_k\) is therefore zero in that ideal bulk model. The 1999 (111) and 2005 (110) geometries do not establish a nonzero coefficient for normal-incidence (001). Oblique p-polarization, interfaces, finite numerical aperture, or a distinct CASH/surface channel may alter the field projection; each needs its own acquired same-specimen response. A common external converter alone does not discriminate two domains with identical subsequent linear response. Ordinary antiphase translation also need not reverse \(\chi^{(2)}\); first identify inversion-related twins and verify opposite nonlinear phase, not just intensity SHG.

## Cap, stoichiometry, timescale, and spatial smoothing

The thermochemistry source used high-purity GaAs specimens sealed under vacuum in quartz ampoules and held in a platinum crucible to reduce oxidation and volatility. That is a calorimetry preparation, not evidence that an unspecified laser cap preserves the composition of a thin film at melt or ablation conditions. A recent primary femtosecond GaAs decomposition study ([2024 paper](https://doi.org/10.37188/lam.2024.026)) reports substantial depth-dependent As:Ga changes, rippled morphology, and a layer fault under its 800 nm high-pulse-energy conditions. It is not the proposed two-colour/capped setup, so it establishes a failure mode to assay, not a direct prediction. The exact cap material, thickness, atmosphere/pressure, optical constants, thermal boundary conductance, As chemical potential, and before/after material inventory are missing.

Thermal APB annealing is a useful comparator but not a matched test of this proposal. [Barrett et al. (2019)](https://doi.org/10.1007/s10853-019-03353-7) used a 20 nm Al2O3 cap and Ar ambient on GaAs-on-Si(001); at 650 °C (923 K), a 7.5 minute anneal reduced surface APB density from 0.10 to about 0.014 µm\(^{-1}\), with an order-of-magnitude decrease reached in under 10 minutes at ≥650 °C. Residual domains remained. This is sub-melting annealing, with migration attributed to vacancy-assisted Ga diffusion and curvature reduction, not phase-selected polarity advance. Orientation-patterned GaAs for nonlinear optics also already exists: [Granger et al. (2023)](https://doi.org/10.1038/s41377-023-01299-9) describe opposite [001]/[00-1] domains prepared through wafer bonding, lithographic patterning, and epitaxial regrowth. A new route would need matched whole-process advantage over such established patterning and annealing, not merely domain motion.

Relevant scales differ sharply. The source optical pulses are about 100–120 fs; Fraser probes carriers after roughly 0.2 ps, Stevens after roughly 3 ps. The 1998 GaAs melting study places thermal melting near 100 ps below its nonthermal threshold. Using the \(0.2\)–\(0.4\) cm²/s diffusivity quoted in the 2024 laser study only as a scale estimate, \(\sqrt{\alpha t}\) is 1.4–2 nm at 100 fs, 45–63 nm at 100 ps, and 4.5–6.3 µm at 1 µs. The common diffusion-length convention \(2\sqrt{\alpha t}\) is twice these values. The 2024 paper estimates microsecond relaxation for a roughly 5 µm modified depth. Neither estimate determines the response of a capped boundary; carrier transport, phase fronts, latent heat, and interface resistance are additional.

The source's linear thin-film model is dimensionally consistent:
\[
C_a\partial_tT=\kappa d\nabla^2T-G(T-T_b)+P_0[1+C\cos(kx)].
\]
Here \(C_a\) is J m\(^{-2}\) K\(^{-1}\), \(\kappa d\) is W K\(^{-1}\), \(G\) is W m\(^{-2}\) K\(^{-1}\), and \(k\) is m\(^{-1}\). At steady state, \(T_{\rm mean}-T_b=P_0/G\) and
\[
\frac{\delta T}{T_{\rm mean}-T_b}=\frac{C}{1+(k\ell_T)^2},\qquad \ell_T=\sqrt{\kappa d/G}.
\]
Reducing \(G\) lowers the power needed for a given mean temperature but enlarges \(\ell_T\), suppressing fine spatial temperature contrast when \(k\ell_T\gg1\). For fixed mean excess \(\Delta T\), the phase-odd temperature amplitude is \(C\Delta T/[1+(k\ell_T)^2]\). No measured \(\kappa,G\), high-temperature optical response, or melting dynamics are supplied; this steady linear result is a tradeoff, not a melting model.

## Acquisition decision and gate comparison

| Capital gate | Current open obligation | Fit to this question |
|---|---|---|
| N783 / G-FB-N783-CAPABILITY | Acquire a specific reaction, retained outgoing excitation, branching/loss/damage/energy; validate a full configuration-level kernel or reward potential; compare terminal retained benefit with matched controls. | Useful discipline for separating excitation and retained reward, but its hBN repair-chain chemistry and carrier survival are not supplied by GaAs. |
| N789 / G-FC-N789-CAPABILITY | Same-specimen phase-, basis-, energy/angle-, and dose-resolved retained-event curve; independently calibrated joint atomic/electronic trajectory, covariance, uncertainty; null-scope/control/retention/comparator/cost accounting. | Closest acquisition template for a phase-driven retained-event claim. Its Te recoil hypothesis and data do not transfer to GaAs. |
| N814 / G-FL-N814-CAPABILITY | Measure chemistry-compatible net work return to a reusable bus at fixed saleable product, jointly with state, loss, loading, return, reset, heat, throughput, and conditioning costs. | Not the right first gate for this route; applies only if a net work-return process is claimed. |

Recommended sequence:

1. Freeze the intended twin type, cap, temperature, orientation, incidence, polarizations, fluence, patch dimensions, and retention horizon. The normal-incidence (001) ideal QUIC null must be addressed before a high-power structural run.
2. On one mapped specimen, measure phase-dependent carriers and the local energy balance (both colours, reflected/transmitted light, converted light, carrier escape, delayed lattice temperature). Determine the actual \(C_{\rm heat}\) and its uncertainty at the target fluence. If bulk impulsive full melting is the proposed route, require the measured lower confidence bound to exceed the relevant thermochemical threshold before proceeding.
3. Only then test retained output: phase \(\phi\) versus \(\phi+\pi\) at matched individual-colour fluences and counterbalanced order, plus randomized phase, non-overlap, single-colour, and matched-temperature histories. Map the boundary before/after with phase-sensitive polarity identification; measure displacement, defects, As:Ga/material inventory, cap damage, and retention after cooldown. Use a nearly flat boundary to null curvature bias and independent regions/specimens to avoid treating pulses as independent samples.
4. Compare energy and elapsed time per retained-good area/volume, including laser wall energy, conversion/stabilization, cap/specimen preparation, preheat/cooling, readout/feedback, failed yield, and material loss, against a declared APB-anneal and/or template-growth baseline.

A phase-odd optical/carrier signal alone fails the retained-output gate. Apparent boundary motion caused by curvature, asymmetric heat sinking, ablation, or composition loss also fails. On current evidence the worth-pursuing result is one bounded falsification/acquisition experiment for a boundary-local phase-reversible response—not a bulk-melt production claim.

## Reproduction and audit boundary

The source's calculate_bounds.py was copied before execution into source-copy/; its generated JSON matched the received results.json byte-for-byte (SHA-256 9937e83d… in the source receipt). checks/rederive_audit.py independently recomputes the thermochemical rows, proves the dose-window endpoint collapse at equality, constructs an exact partial-melt witness, and checks exact sustained-cooling and unequal-patch countermodels. These are arithmetic/algebra checks only. They validate no physical response, transfer coefficient, high-fluence behavior, retained transition, or technological advantage.

Local capital status and source access are pinned in READ_LEDGER.md; all incoming source copies and this audit's files are listed by hash and size in MANIFEST.json.
