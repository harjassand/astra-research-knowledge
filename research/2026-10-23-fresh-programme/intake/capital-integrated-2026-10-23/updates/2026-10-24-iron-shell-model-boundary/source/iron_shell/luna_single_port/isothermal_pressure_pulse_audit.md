# Fe-shell pressure-pulse audit

**Status:** the proposed pressure pulse is a testable operating perturbation, not an identified shell-opening mechanism. A fixed ideal-gas H2O/H2 ratio protects one reaction-affinity difference; it does not hold the reacting material or reactor in the same state.

## Frozen candidate and question

The pre-existing hypothesis proposes an isothermal total-pressure pulse at fixed nominal H2O/H2 partial-pressure ratio, intended to change pressure gradients across a reduced iron shell, refresh product-layer gas, or open cracks while leaving the ideal redox affinity unchanged. The target discrimination is whether any rate or final-porosity change is caused by mechanical reopening, rather than ordinary gas chemistry, transport, or a changed reduction history.

## What the ideal thermodynamics actually fixes

For the local wüstite-to-iron step

\[
\mathrm{FeO(s)+H_2(g)\rightleftharpoons Fe(s)+H_2O(g)},
\]

write dimensionless activities using a standard fugacity f°:

\[
Q=\frac{f_{H_2O}/f^\circ}{f_{H_2}/f^\circ}\,\frac{a_{Fe}}{a_{FeO}},\qquad
\Delta_rG=RT\ln(Q/K(T)).
\]

If both solids are pure phases with unit activity and the gases are ideal, f_i = p_i, hence Q = p_H2O/p_H2. At fixed temperature, scaling both reactive partial pressures by a common factor lambda leaves this one reaction quotient and affinity unchanged. The same ratio also fixes the ideal-gas oxygen potential because mu_H2O - mu_H2 is ratio-dependent.

That cancellation is narrow. If both partial pressures double, each individual gas chemical potential changes by RT ln 2: about 6.18 kJ mol⁻¹ at 800 °C. Other equilibria and surface coverages can therefore move while the FeO/Fe quotient stays fixed. For dilute dissolved hydrogen, Sieverts scaling predicts c_H proportional to sqrt(f_H2), so doubling f_H2 changes the equilibrium concentration by a factor sqrt(2), and quadrupling it doubles it. This is a regime-limited model prediction, not a claim that a porous product shell reaches equilibrium during a short pulse.

“Raise total pressure at fixed ratio” also leaves the actuator underspecified:

* **Compress or pressurize a fixed-composition H2/H2O/inert mixture:** p_H2 and p_H2O both rise. The ideal redox affinity is fixed, but absolute reactive-gas activities, adsorption, and hydrogen uptake change.
* **Add inert gas while holding p_H2 and p_H2O fixed:** the ideal reactive-gas chemical potentials and quotient stay fixed. This better isolates a total-pressure/mechanical perturbation, although gas transport, fugacity coefficients, and flow-controller behavior still need matching.

For a real mixture, f_i = phi_i y_i P, so the gas part of Q is (phi_H2O/phi_H2)(y_H2O/y_H2); fixed composition ratio alone does not guarantee fixed fugacity ratio if the fugacity-coefficient ratio changes with pressure. Real wustite is nonstoichiometric, and a pellet may contain Fe/FeO/Fe3O4 fronts with evolving solid activities. Finally, a fixed feed ratio does not fix the local ratio at a reacting interface: H2 is consumed and H2O generated inside the pore network.

## Strongest conventional null

An observed rate transient at fixed nominal ratio has several nonmechanical explanations:

1. **Surface reaction and coverage.** Scaling absolute p_H2 changes hydrogen adsorption/dissociation and surface coverage; p_H2O changes product inhibition/oxidizing coverage. McKewan's primary report states that an earlier magnetite-pellet study found rate proportional to hydrogen partial pressure up to 1 atm while maintaining a constant water-vapor/hydrogen ratio; its own high-pressure experiments found rate increasing with pressure then saturating, and attributed the trend to hydrogen coverage. This is a direct warning that constant ratio does not imply rate invariance. The pressure-rate result is not a test of this pulse or evidence of mechanical shell opening. [McKewan, Reduction Kinetics of Magnetite in Hydrogen at High Pressures](https://www.onetunnel.org/documents/iron-and-steel-division-reduction-kinetics-of-magnetite-in-hydrogen-at-high-pressures).
2. **Hydrogen in the product iron.** In the dilute equilibrium regime, \(\tfrac12H_2(g)\rightleftharpoons[H]_{Fe}\) gives Sieverts scaling \(c_H=K_S\sqrt{f_{H_2}/f^\circ}\). Uptake, diffusion, trapping, and release can lag the gas pulse and change the mass signal or interfacial kinetics without shell fracture. Hill and Johnson measured hydrogen concentrations in iron over hydrogen pressures up to 136 atm and reported pressure/temperature dependence; those data establish a real state variable but do not quantify uptake in a fresh porous reduction shell at the proposed waveform. [Hill & Johnson, *The Solubility of Hydrogen in Alpha Iron*](https://onetunnel.org/documents/institute-of-metals-division-the-solubility-of-hydrogen-in-alpha-iron).
3. **Gas transport and hydrodynamics.** Total pressure changes gas density and, in the dilute-gas regime, binary diffusivity (approximately \(D\propto1/P\)). The resulting flux and residence-time change depend on whether the rig controls molar flow, actual volumetric flow, or superficial velocity. It can alter delivery of H2, removal of H2O, and local reaction-front composition. No universal sign follows without the flow boundary conditions.
4. **Thermal and instrument transients.** Compression/decompression changes gas temperature before the solid and furnace can re-equilibrate; line dead volume, pressure regulators, and gas switching can generate short composition/flow excursions. “Isothermal” must be measured at the sample on the pulse timescale, not inferred from the furnace setpoint.
5. **Ordinary reaction-history changes.** A persistent rate or porosity change can follow a different Fe/FeO/Fe\(_3\)O\(_4\) fraction, reduction degree, iron sintering, pore coarsening or sealing, or water redistribution. The morphology benefit could close transport paths as readily as it opens them. A post-pulse improvement alone does not identify mechanical cracking.

These nulls are especially strong if the pressure pulse scales reactive partial pressures. If reactive partial pressures are held fixed by inert backfill, the chemical-coverage null is reduced, but transport/hydrodynamic and mechanical loading remain entangled.

## “Trapped water pressure” needs a physical state and a sign

Let p_pore(t) denote pore-gas pressure inside the product shell and p_bulk(t) the surrounding pressure. The mechanical driver is a spatial stress field associated with a lag or difference such as delta_p(t) = p_pore(t) - p_bulk(t), together with shell geometry and constitutive properties, not the common-mode value of reactor pressure by itself. In an open, equilibrated pore network, p_pore is approximately p_bulk, so a slow uniform pressure change supplies little persistent differential load. A fast external pressure rise initially gives p_bulk > p_pore (compressive loading); a fast release can instead leave p_pore > p_bulk (outward loading). Which sign can crack, buckle, compact, or seal a given shell cannot be inferred without its geometry and strength.

The relevant lag depends on pulse duration versus gas equilibration through the actual product layer; a first scale is t_D approximately L^2/D_eff, with pore permeability/compressibility also entering. Without measured L, D_eff, permeability, and pulse waveform, no pressure-gradient magnitude follows. At a fast pulse, ordinary reactive-gas transport changes occur at the same time as any mechanical lag.

Water must also be assigned a phase and location. If it is pore vapor, its local partial pressure follows gas inventory, reaction production, temperature, and leakage; it is not automatically the external pressure step. If it is adsorbed, capillary-condensed, liquid-included, or otherwise isolated, its chemical potential and pressure are not set by the external H2O/H2 ratio alone. Establish local temperature and whether condensation is possible before using “trapped water pressure” as a mechanism. A pressure pulse does not itself demonstrate that such an inventory exists or that it is coupled to a crack.

## Minimal discriminating comparison

A meaningful test should compare matched samples at the same starting phase fractions and reduction degree, then keep sample temperature, feed ratio, pulse duration, and actual flow boundary condition measured. At minimum, separate (i) a pressure waveform that scales reactive partial pressures at fixed mixture composition from (ii) inert backfill that raises total pressure while holding p_H2 and p_H2O fixed. Include a no-pulse run with the same cumulative H2/H2O exposure and an optimized conventional temperature/flow profile as the equally informed incumbent.

Measure both gas-side conversion (time-resolved H2/H2O balance) and solid state (Fe\(^0\)/FeO/Fe\(_3\)O\(_4\) fractions, total oxygen removal, and before/after crack connectivity or porosity); record sample temperature and pressure at the particle/bed scale. A pressure response without an independently resolved pore/shell deformation or newly connected crack path remains compatible with chemistry and transport. A persistent response is persuasive for mechanics only if it survives matching final phase fractions and reduction degree and correlates with the independently measured structural change. Merely recovering the baseline rate after a pulse is not sufficient either: that can be a reversible adsorption, hydrogen-uptake, or flow transient.

## Conditional constructive candidate: a shallow Fe/FeO excursion

The pressure pulse remains a null hypothesis. A more chemically specified alternative is to oxidize a deliberately shallow part of the metallic product shell to wüstite and then reduce it again. The volume and interface changes during Fe-to-FeO and FeO-to-Fe may create connected cracks, but they may instead compact or seal the shell; that is the unknown to test, not a promised outcome.

For a simple Fe–O system, make the excursion only where wüstite is a stable phase (roughly above 570 °C) and choose the H2O/H2 ratio in the phase-selective window

\[
r_{Fe/FeO}(T)<r=p_{H_2O}/p_{H_2}<r_{FeO/Fe_3O_4}(T).
\]

Here the lower boundary favors oxidation of Fe to FeO, while staying below the upper boundary is intended to avoid advancing the shell to Fe3O4. These are conditional equilibrium boundaries, not universal setpoints: real ore has nonstoichiometric wüstite, gangue, and mixed phases. First map the phase/oxygen-uptake response of the actual ore or pellet at its chosen temperature and reduction degree, then choose a ratio and bounded oxygen dose that produce measurable FeO without magnetite growth. If that selective window does not appear in the actual material, stop; the operation is not defined by the pure-FeO diagram alone.

The candidate operation is: reduce the representative pellet to a specified metallic-shell state; hold temperature; apply a short H2^18O/H2 pulse at the calibrated Fe/FeO-selective ratio; use net solid-oxygen increase corroborated by bulk Fe-valence/phase change only as a net-inventory controller, not as a bound on the depth or amount of a shallow oxide skin; then return to a reducing ratio below the Fe/FeO boundary and re-reduce. A depth-limited excursion requires an independently calibrated growth/depth map or spatially resolved phase/valence/isotope geometry in the actual shell. Raw isotope uptake, bulk TG, and bulk Fe valence alone cannot ensure that the cycle stayed shallow or that no internal phase cycling occurred. The useful outcome is not uptake itself: it is an increase in connected shell porosity and in subsequent original-ore oxygen removal or reduction rate at matched final Fe/FeO/Fe3O4 fractions, reduction degree, total time, heat, and gas cost versus an optimized conventional thermal/flow profile.

The decisive readouts are (i) time-resolved H2, H2^16O, and H2^18O in the effluent, with a complete gas/solid oxygen ledger; (ii) spatially resolved phase/valence/isotope geometry sufficient to calibrate oxide-skin growth and depth in the actual shell, plus bulk Fe^0/Fe2+/Fe3+ before and after; and (iii) before/after connected pore/crack structure. Include a no-redox inert pressure/flow sham, a sub-threshold isotope-exposure sham, and the optimized conventional-profile incumbent. If the labelled water changes isotopologue output but Fe valence and total solid oxygen do not change, that is compatible with isotope exchange, not demonstrated Fe oxidation/reduction. If a spatially verified FeO excursion closes pores or gives no rate/connected-path advantage at matched cost, the constructive mechanism fails.

Bulk cancellation counterledger, with the same oxygen isotope for clarity:

\[
q\,\mathrm{Fe}_{outer}+q\,\mathrm{H_2^{16}O}\to q\,\mathrm{Fe^{16}O}_{outer}+q\,\mathrm{H_2},\qquad
q\,\mathrm{Fe^{16}O}_{core}+q\,\mathrm{H_2}\to q\,\mathrm{Fe}_{core}+q\,\mathrm{H_2^{16}O}.
\]

Adding these concurrent legs gives zero net H2/H2O, zero net solid-oxygen change (+q−q=0), and zero net metallic-Fe change (−q+q=0), while the outer Fe oxidizes and core FeO reduces. With H2^18O dosing, the outer reaction can put oxygen-18 into the skin while reduction of core FeO releases oxygen-16 as H2^16O. Thus bulk TG and bulk Fe-valence endpoints do not upper-bound oxide-skin depth or gross phase cycling; isotope-exchange profiles are also nonunique without spatial phase/isotope information.

## Exact oxygen and hydrogen ledger for the excursion

For an ideal excursion of q mol of metallic Fe, the balanced unlabeled legs are

\[
q\,\mathrm{Fe}+q\,\mathrm{H_2O}\to q\,\mathrm{FeO}+q\,\mathrm{H_2},\qquad
q\,\mathrm{FeO}+q\,\mathrm{H_2}\to q\,\mathrm{Fe}+q\,\mathrm{H_2O}.
\]

The leg-by-leg ledger is:

| Leg | Solid change | Gas in | Gas out |
|---|---|---|---|
| Steam oxidation | q Fe -> q FeO; solid O increases by q mol | q mol H2O | q mol H2 |
| Re-reduction | q FeO -> q Fe; solid O decreases by q mol | q mol H2 | q mol H2O |
| Closed cycle | no net Fe or O change | zero net only with ideal recovery/routing | zero net only with ideal recovery/routing |

Without capturing/reusing oxidation-produced H2, the reduction leg still needs q mol H2; without recovering the reduction-produced H2O, the oxidation leg still needs q mol steam. Even with ideal recycle, the reactor processes q mol in each direction, spends time and switching/compression work, and must handle the opposite reaction heat in each leg. Any finite-rate cycle has losses; no extra net oxygen removal from the original ore follows from this excursion. The relevant comparison remains final metallic-iron fraction and original-ore oxygen removal at matched total heat/time/gas cost versus the optimized conventional profile.

For the ideal labelled ledger, the two steps are

\[
q\,\mathrm{Fe}+q\,\mathrm{H_2^{18}O}\to q\,\mathrm{Fe^{18}O}+q\,\mathrm{H_2},\qquad
q\,\mathrm{Fe^{18}O}+q\,\mathrm{H_2}\to q\,\mathrm{Fe}+q\,\mathrm{H_2^{18}O}.
\]

The isotope ledger must close separately from the total-oxygen ledger, but closure still gives a bulk net balance, not a spatial profile:

\[
N_{18,\mathrm{in}}=N_{18,\mathrm{effluent}}+\Delta N_{18,\mathrm{solid}}+N_{18,\mathrm{other}},\qquad
N_{O,\mathrm{initial}}+N_{O,\mathrm{in}}=N_{O,\mathrm{effluent}}+N_{O,\mathrm{solid,final}}+N_{O,\mathrm{other}}.
\]

In the ideal labeled excursion the imposed dose is q mol of oxygen-18, and the reducing leg returns that q mol as H2-18O. When the cycle closes, it has zero net oxygen uptake; the underlying ore-reduction ledger remains N_O mol of original oxygen removed per N_O mol H2 consumed if all original oxide oxygen exits as water. In a real pellet, isotope exchange can move oxygen-18 into oxide and release original oxygen-16 without the intended Fe-valence excursion. Furthermore, concurrent outer Fe oxidation and core FeO reduction can cancel in both bulk oxygen and bulk Fe-valence records. Therefore isotope uptake/release plus bulk TG/valence alone cannot establish a shallow q-dose: pair the closed bulk balance with spatially resolved isotope and phase/valence geometry. Also report any oxygen-18 retained in solids or lost to other products rather than forcing the ideal closure.

The cycle's H2 balance is similarly conditional. If the oxidation outlet q mol H2 is captured at usable purity/pressure and reused in the re-reduction, the two ideal legs cancel net H2 makeup. If that stream is vented, diluted, or mixed with steam so it cannot be reused, the reducing leg still requires q mol H2 supply. Even perfect recycle does not erase gross throughput: the oxidation consumes q mol steam and produces q mol H2; re-reduction consumes q mol H2 and produces q mol steam. Recovering and routing both streams, managing opposite reaction heats, and achieving a finite-rate excursion have time, separation, compression, and heat-management costs. It is not extra net ore oxygen removal for free.

**Decision:** treat fixed-ratio pressure pulsing as a confounded operating perturbation, not evidence of mechanical shell reopening. The distinct shallow Fe/FeO excursion is a conditional mechanism candidate only: it requires an actual-ore phase-selective window above the wüstite stability temperature, verified isotope/oxygen and valence balances, and a matched-cost connected-porosity benefit. Neither operation is validated here.
