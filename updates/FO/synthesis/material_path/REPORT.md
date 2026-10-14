# GaAs post-growth polarity rewriting: materials and process-path audit

**Date:** 15 October 2026  
**Scope:** Retained, phase-selected GaAs polarity/APB rewriting; primary process comparators and adjacent laser pathways.  
**Status:** Feasibility screen with conditional thermodynamic arithmetic. No new physical response or retained phase-selected structure was experimentally demonstrated here.

## Decision

The proposed operation is physically conceivable only if the illuminated boundary separates variants with the required opposite phase-odd response and the resulting excitation biases an irreversible boundary transition. Neither condition has been demonstrated on the proposed GaAs-on-Si material. The strongest available optical result is a roughly 2% phase-dependent **carrier-density modulation** in a different, 650 nm (111) GaAs specimen. It is not a measurement of phase-dependent deposited heat, APB mobility, or a retained polarity change.

The concrete target geometry chosen for comparison is the published on-axis 300 mm Si(001) substrate with a 400 nm GaAs film. With a 20 nm Al2O3 cap and a 650 °C, 7.5 min Ar furnace anneal, its measured surface APB line density falls from 0.10 to 0.014 μm⁻¹. That is a 86% reduction (7.14-fold) without phase selection. The remaining domains show a nonzero plateau, while depth profiles after at least 650 °C for 10 min show nearly undetectable APBs through most—but not all—of the film. This is a strong retained-material comparator.

For normally incident, co-propagating fields on a (001) zincblende surface, the direct bulk third-rank interference contraction is zero: the allowed cubic components are xyz permutations, while both fields have only in-plane x/y components. A p-polarized oblique-incidence or otherwise z-polarized geometry could avoid this tensor zero, but the local carrier and absorbed-energy contrast must be measured under the actual cap, substrate, fluence, and temperature. The proposed normal-incidence transfer from the (111) optical experiment does not qualify.

**Disposition:** Do not treat phase-selective retained APB rewriting as an available GaAs operation or build a processing architecture around it. Preserve it as a specimen-scale hypothesis whose first decisive endpoint is signed, retained boundary displacement that reverses under φ→φ+π, with structural and composition checks. Bulk melt-and-regrow is especially poorly supported. A more concrete, already demonstrated GaAs operation is laser-assisted defect/electrical-property recovery in bulk LEC GaAs under arsenic-pressure control; it has a matched thermal-only comparator but is established prior art, slow, and not a polarity-writing substitute.

## Exact target and strongest competitors

### Chosen material geometry: GaAs-on-Si(001) with post-growth anneal

Barrett et al. grew 200 nm GaAs below 550 °C followed by 200 nm at 600–650 °C on nominally on-axis 300 mm Si(001). Specimens came from one wafer. They deposited 20 nm ALD Al2O3 at 200 °C, annealed ex situ in Ar, then stripped the cap in 49% HF for 30 s. For the matched 650 °C, 7.5 min furnace condition, the surface line density measured after selective etch and SEM/ImageJ fell from 0.10 to 0.014 μm⁻¹. More than 90% of counted surface domains were eliminated, not every domain. The density plateau corresponded to about one to two domains in an approximately 200 μm² SEM field. The source reports that at ≥650 °C for ≥10 min, density was nearly undetectable through most of the film; it also cautions that bulk and surface kinetics differ.

The authors infer curvature-driven self-annihilation: boundaries move toward their centers of curvature. Surface density followed the Allen–Cahn (t^{-1/2}) dependence, with a reported 3.8 eV activation energy for surface APB motion. This mechanism is already enough to explain unsigned domain shrinkage. A phase-write result must therefore show a **phase-reversible signed drift**, not simply a smaller domain after heating.

This process is the strongest direct competitor for an APB-density claim. Known process burdens include MOCVD epitaxy, 20 nm ALD cap deposition, a 7.5 min dwell plus unreported heat-up/cool-down, Ar handling, and post-anneal concentrated-HF cap removal. The selective chemical etch and SEM are destructive evaluation steps. Wafer-level yield, ramp/cool time, energy, cost, composition retention and device benefit were not reported, so they remain unknown.

### Strongest comparator for a chosen polarity pattern

Granger et al. demonstrate that deliberate orientation patterns can already be made and used. Their OP-GaAs/AlGaAs flow starts with a 2 in [001] wafer carrying a MOVPE stop layer and ~100 nm GaAs layer; wafer bonding to an oppositely oriented [001] wafer, etching to the stop, stop removal, photolithographic patterning, and etching create the orientation-patterned template. MBE then regrows 2.5 μm Al0.5Ga0.5As, 1.5 μm Al0.3Ga0.7As cladding, and 14 μm OP-GaAs. A second lithography/etch defines 7 μm ribs. Their demonstrated waveguide uses an 85 μm quasi-phase-matching period and alternates [001]/[00-1] polarity; a 14.5 mm chip produced 3.9–9.3 μm continuum with 2 mW total output (including residual pump) and an estimated 1 mW in the continuum.

This is an established, functioning route to a chosen polarity pattern, not correction of an already grown defective film. It is a strong comparator for any claim that the laser operation uniquely makes a selected pattern. Full process yield, cost, cycle time and wafer-scale uniformity were not quantified in that paper.

## Do the target APBs have the needed polarity relation?

There is primary evidence that some GaAs APD pairs are polarity-reversed. Morizane et al. report reversed 〈111〉 polarity axes in adjoining GaAs domains on Ge, observed on (100)/(110) specimens. Rasmussen et al. show rigid-body translation across {110} GaAs APBs and explain how absolute polarity can be identified from a bright-field image. These sources make polarity-based coupling structurally possible; they do not establish the polarity/susceptibility sign of every boundary in Barrett's specific GaAs/Si wafer.

A practical prerequisite is to identify on the actual target specimen which APBs separate true inversion-related variants. Then measure the *signed* phase-sensitive nonlinear response and the population-control tensor projection across those same domains. Intensity-only SHG, an APB label, or a bulk-average carrier signal is insufficient. Even where inversion symmetry guarantees opposite signs of inversion-odd response, the domain-resolved absorption and transition kernel remain specimen- and geometry-dependent.

For ideal bulk zincblende GaAs, the relevant third-rank tensor has xyz permutations. Under normal incidence on (001), (E_z=0) for both co-propagating optical colours and all available components lie along x/y, so the xyz contraction vanishes. The Fraser experiment instead deliberately used a (111) sample and reports a specific nonzero (111) projection of χxyz for polarization along [011]. An oblique mixed-polarization geometry can supply z field, but it must be calibrated on the capped 400 nm Si-supported film; reflections, absorption and the cap change the local fields.

## Thermal selectivity test: what the measured optical contrast does and does not buy

For equal molar patches starting at (T_0), suppose the **actual net deposited thermal energies** are (Q(1+C_Q)) and (Q(1-C_Q)), with negligible heat exchange during an impulsive step, fixed composition, and equilibrium melting. Let (H_s) be the sensible enthalpy from (T_0) to the GaAs melting point, and (L) its fusion enthalpy. Full melting of the hot patch while the protected one stays below melt onset requires

\[
Q(1+C_Q)\ge H_s+L,\qquad Q(1-C_Q)<H_s.
\]

A nonempty dose interval therefore requires

\[
C_Q>\frac{L}{2H_s+L}.
\]

Yamaguchi et al. measured a GaAs melting point of (1514\pm1\) K and fusion enthalpy (106.72\pm0.20\) kJ mol⁻¹. Their GaAs(s) heat-content fit, valid from 800 to 1514 K and referenced to 298.15 K, gives (H_s=65.6166) kJ mol⁻¹ at room-temperature start (fit error reported as 100 J mol⁻¹). The calculated threshold is **(C_Q>0.4485)**, equivalent at the boundary to a hot/cold deposited-energy ratio of 2.63. Under this particular model, the threshold rises to 0.6449 at 1000 K and 0.8884 at 1400 K; preheating does not help complete selective melting because it removes the protected patch's sensible-heat margin while leaving the hot patch's latent-heat requirement.

If (C_Q=0.02) were hypothetically a true thermal contrast, the protected-patch inequality permits a supremum of only 2.51% melted fraction before the protected patch reaches melt onset. That value is a conditional calculation, **not** a conversion of Fraser's carrier measurement. The missing quantity remains the actual phase-dependent deposited thermal energy (C_Q) in the intended processing regime; none of the sources measured it for the target film. This is not a no-go for sustained heating, boundary-local rearrangement, nonthermal transitions, or partial melt/seeded regrowth. Those paths need their own measured transition and retention kernels.

The 2% optical result belongs to a separate specimen and operating regime: Fraser et al. used undoped 650 nm bulk GaAs (111) bonded to sapphire, at 295 K, with overlapped 120 fs 1550/775 nm pulses at 250 kHz and peak incident irradiances 9 GW cm⁻² and 150 MW cm⁻². Their measured carrier modulation amplitude was about 2%, with peak carrier concentration about 10¹⁸ cm⁻³. They also measured phase-dependent 775 nm transmission, and analyze direct interference plus energy exchange between colours. That is evidence for coherent control of carriers/absorption in that sample, not a phase-selective structural operation. They did not measure boundary movement, melt depth, retained polarity or post-drive composition.

## Thermal and laser routes are not interchangeable

| Primary experiment | Its actual sample and regime | Measured output | Limit on transfer |
|---|---|---|---|
| Barrett et al. (2019) | 300 mm Si(001), 400 nm GaAs, 20 nm ALD Al2O3 cap, 650 °C/7.5 min Ar furnace | Retained APB-density reduction 0.10→0.014 μm⁻¹; curvature-linked shrinkage | Strong direct comparator; no phase-selected drift |
| Fraser et al. (1999) | 650 nm bulk GaAs (111)/sapphire, 295 K, 120 fs, 1550/775 nm | ~2% carrier-density modulation; optical transmission change | Not the target cut, film, cap, high-fluence thermal contrast or retained structure |
| Sokolowski-Tinten et al. (1998) | Bare polished single-crystal GaAs (100), 620 nm, 100 fs, fresh spot per shot; reported threshold 150 mJ cm⁻² | Transient reflectivity interpreted as nonthermal melting above threshold; thermal melt below threshold develops on ~100 ps scale | Confirms an ultrafast structural pathway but no recovered polarity or post-pulse retention; cannot set a capped-film threshold |
| Rys et al. (1990) | Si/Se-implanted GaAs under Si3N4 cap; ~10 ns, 308 nm XeCl or 728 nm dye pulses; fluence range 0.06–0.9 J cm⁻² | Carrier activation and melt dynamics; cap-damage thresholds 0.34 J cm⁻² (308 nm) and 0.12 J cm⁻² (728 nm) | Shows cap survival is a separate gate. Different dopant profile, wavelength and pulse duration; do not transfer thresholds |
| Xu et al. (2024) | GaAs laser-processed with 800 nm, 100 fs, 1 kHz pulses; pulse energies discussed from 1 to 300 μJ, pressure varied | Low-energy near-bulk As:Ga; decomposition and composition change at higher energies; at 150 μJ surface relief reached ~4 μm and depth-profile alteration extended to ~9 μm | Clear material-loss/stoichiometry failure mode, but this is a separate material/environment and was used for surface activation, not polarity writing |
| Ruda et al. (1992) | 5×5 mm nominally undoped LEC GaAs chips in sealed quartz with As charge; 700 °C/10 h; concurrent 532 nm, 10 ns, 10 Hz at ~0.07±0.01 J cm⁻², controlled As pressure | EL2 recovery/resistivity and etch-pit density; laser-assisted recovery exceeded matched thermal-only recovery in selected conditions | A real adjacent defect-control operation; not a phase-selective or shorter-cycle APB process |

Sokolowski-Tinten's “nonthermal melt” is identified by ultrafast transient optical response and a carrier threshold near 10²² cm⁻³; it does not show retained polarity after the material recovers. Rys's nitride-cap thresholds are tied to its implant/cap/laser conditions. Xu's pulse-energy series includes a methods/results range discrepancy (methods state 10–300 μJ while results discuss 1–300 μJ); the report preserves that inconsistency. At 150 μJ and 0.15 MPa, Xu reports a strong As-rich surface after treatment; the same paper describes an HF clean and silver deposition for its intended surface-activation/SERS operation. Those data warn against treating surface decomposition as a retained rewrite. None of these incident energies/fluences are combined into one threshold because the samples, absorption, pulsewidth, wavelength, cap, ambient and intended endpoint differ.

### More concrete attainable GaAs operation if the polarity target is deprioritized

Ruda et al. studied nominally undoped, single-crystal LEC GaAs. The 5×5 mm samples were annealed in closed high-purity quartz ampoules with an elemental-As source in a controlled-temperature cold zone. After a 1000 °C/24 h treatment that erased EL2 and made the material conducting, they compared standard thermal re-annealing and concurrent laser-assisted annealing. At 700 °C for 10 h, arsenic-rich thermal-only treatment gave only partial EL2 recovery; adding 532 nm, 10 ns, 10 Hz laser pulses at about 0.07±0.01 J cm⁻² gave stronger recovery. Their text says the arsenic-rich 700 °C laser condition produced electrical/optical properties essentially matching an arsenic-rich 800 °C/10 h thermal treatment. Etch-pit density was minimized near stoichiometric conditions.

This has a concrete retained material/electronic endpoint and a matched thermal comparator. It could matter when bulk GaAs electrical compensation must be restored under a lower peak-temperature ceiling. The process still takes 10 h, uses an As-controlled sealed ampoule and laser delivery through a furnace viewport, and does not establish lower total energy, cost, improved yield, or wafer-scale throughput. It is published prior art; it cannot be presented as a new operation or as evidence for phase-selected polarity rewriting. The full article text was reviewed through an author-uploaded ResearchGate view; a local PDF download was unavailable, so the process details should be checked against the publisher copy before a new experiment is specified.

## Smallest decisive experiment for the original hypothesis

1. Use a structurally mapped, capped GaAs-on-Si(001) specimen close to the 400 nm target geometry. Identify a boundary between verified opposite-polarity domains and measure its signed nonlinear response. Reject boundaries whose relation is translation-only or whose phase-odd population tensor is not detected.
2. Choose an oblique mixed-polarization geometry with nonzero xyz projection. Measure local fields, phase-dependent carrier density, both-colour transmission/reflection, temperature history and absorbed energy under the actual cap and substrate. First do this below any measurable irreversible change.
3. On a nearly straight, pre-mapped boundary, compare phase φ and φ+π with matched per-colour fluences. Include randomized phase, nonoverlapping pulses, each single colour, and a thermal-history-matched control. Counterbalance order and use independently prepared regions/specimens.
4. After the drive and cooling, measure **signed boundary displacement**, polarity on both sides, composition/As loss, surface height/material inventory and new defect density. Recheck retention after a defined hold and thermal challenge. Use structural diffraction/TEM or an equivalent polarity-sensitive method; SHG intensity alone is not a structural endpoint.
5. A positive mechanism result must reverse the advancing polarity under the phase flip and survive after the field is removed, while measured heating, curvature relaxation, converted-light escape and material removal fail to explain the sign. Faster shrinkage at either phase, phase-dependent optical transmission alone, or disappearance by ablation is a failure for the stated operation.

The fair process comparison is the same 300 mm-class material and quality endpoint against Barrett's capped 650 °C furnace recipe, and against OP bonding/patterning/regrowth if the claimed output is a prescribed polarity pattern. Account for both-colour laser wall energy, frequency conversion, phase stabilization, scanning/alignment, cap/ambient control, thermal hold/cool, destructive verification, material loss and yield. Those costs and the actual sample area processed per hour are presently unknown.

## Source citations

- Barrett et al., “Dissolution of antiphase domain boundaries in GaAs on Si(001) via post-growth annealing,” *J. Mater. Sci.* 54, 7028–7034 (2019), [DOI](https://doi.org/10.1007/s10853-019-03353-7), [full PDF](https://swamp.mse.ufl.edu/wp-content/uploads/sites/286/2020/06/Barrett2019.pdf).
- Granger et al., “GaAs-chip-based mid-infrared supercontinuum generation,” *Light: Science & Applications* 12, 252 (2023), [DOI](https://doi.org/10.1038/s41377-023-01299-9).
- Fraser et al., “Quantum Interference in Electron-Hole Generation in Noncentrosymmetric Semiconductors,” *Phys. Rev. Lett.* 83, 4192 (1999), [DOI](https://doi.org/10.1103/PhysRevLett.83.4192), [author PDF](https://www.physics.utoronto.ca/~vandriel/papers/fraser1.pdf).
- Sokolowski-Tinten et al., “Thermal and nonthermal melting of gallium arsenide after femtosecond laser excitation,” *Phys. Rev. B* 58, R11805 (1998), [DOI](https://doi.org/10.1103/PhysRevB.58.R11805), [full PDF](https://qcmd.mpsd.mpg.de/wp-content/uploads/2023/06/PhysRevB.58.R11805.pdf).
- Xu et al., “Semiconductor surface decomposition induced by femtosecond laser for silver deposition and SERS detection,” *Light: Advanced Manufacturing* 5, 26 (2024), [DOI](https://doi.org/10.37188/lam.2024.026).
- Ruda et al., “Control of EL2 concentration and dislocation density in liquid encapsulated Czochralski-grown GaAs using laser processing,” *J. Phys. D: Appl. Phys.* 25, 1538–1544 (1992), [DOI](https://doi.org/10.1088/0022-3727/25/10/023), [author-uploaded full-text view](https://www.researchgate.net/publication/230962995_Control_of_EL2_concentration_and_dislocation_density_in_liquid_encapsulated_Czochralski-grown_GaAs_using_laser_processing).
- Yamaguchi, Itagaki & Yazawa, “High Temperature Heat Content Measurements of the III-V Compounds,” *J. Japan Inst. Metals* 53, 764–770 (1989), [DOI](https://doi.org/10.2320/jinstmet1952.53.8_764), [full PDF](https://www.jstage.jst.go.jp/article/jinstmet1952/53/8/53_8_764/_pdf).
- Morizane, “Antiphase domain structures in GaP and GaAs epitaxial layers grown on Si and Ge,” *J. Crystal Growth* 38, 249–254 (1977), [DOI](https://doi.org/10.1016/0022-0248(77)90305-0). Abstract-only evidence used for polarity reversal in adjoining domains.
- Rasmussen, McKernan & Carter, “Rigid-body translation and bonding across {110} antiphase boundaries in GaAs,” *Phys. Rev. Lett.* 66, 2629 (1991), [DOI](https://doi.org/10.1103/PhysRevLett.66.2629). Abstract-only evidence used for polarity identification.
- Rys et al., “Pulsed laser annealing of GaAs implanted with Se and Si,” *Optical Engineering* 29, 329–338 (1990), [DOI](https://doi.org/10.1117/12.55603), [repository record and abstract](https://digitalcommons.unl.edu/electricalengineeringfacpub/592/). The full-text PDF endpoint was not retrieved.

## Reproduction and status boundary

Run `python3 work/FO-material-path/calculate_bounds.py` with Python 3. The script writes `results.json` using the published GaAs solid heat-content fit, fusion enthalpy and the stated equal-patch model. It also reproduces the arithmetic reduction in Barrett's measured line density. Assertions check dose-window existence on both sides of the derived threshold. These checks validate only the arithmetic/model implementation; they do not validate optical coupling, material properties of the target film, a processing threshold, retained structural response, cost, novelty, or technological benefit.
