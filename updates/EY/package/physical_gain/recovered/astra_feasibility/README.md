# ASTRA Natural Sciences: physical feasibility of kinetic electrical gain

**Research date:** 13 October 2026.  
**Status:** Source-linked physical hypothesis and executed feasibility calculations. No new material was synthesized, no field-dependent rate or dielectric gain was measured, and no first-principles electronic-structure calculation was performed. No exceptional technological advantage or historical priority is established.

## Outcome and branch decision

The original chemical-fuel capacitive chemomotor remains a thermodynamically consistent conditional model. This investigation did **not** identify a chemical interface jointly qualified for its charge coupling, barrier response, kinetic bandwidth and electrical isolation. Its high-efficiency numerical examples are not promoted to device predictions.

Instead of continuing to optimize those examples, the investigation pivoted to a concrete, optically maintained candidate: **negative dielectric absorption from Marcus-inverted charge recombination in CdS quantum-dot–alizarin complexes**. Light, not chemical fuel, supplies this candidate's energy. The measured charge-transfer mechanism provides a stronger material foothold, but net electrical gain is unmeasured.

The physical proposition is that an electric field which stabilizes a charge-separated dipole can accelerate its inverted-region recombination. The field therefore removes the very dipoles that would normally reinforce it. Delayed population depletion can supply negative electrical absorption. This is distinct from asserting that an ordinary adsorption pulse or negative imaginary capacitance produces power.

The chief new results are coupled electrostatic/kinetic constraints, a continuum estimate of terminal dipole, a rotational-loss condition, a two-component correction to the material response, and a noise-to-gain restriction. These are scoped derivations and calculations, not experimental discoveries.

## Evidence separation

**Established in external experiments:** the existence of the CdS–alizarin charge-transfer system; recombination in the Marcus-inverted regime; its pump-probe kinetics; the reported source fit and geometry. The primary article is S1 and the supplementary tables are S2.

**Calculated here:** differentiation of the source's vibronic rate fit; a dielectric-sphere effective-mass charge-centroid model; coupled reaction/electrical linear response; orientation losses; static-mixture sensitivity to the reported biexponential decay; noise, parasitic-loss and pump budgets.

**Still unacquired:** the field derivative of formation and recombination in one fixed device; charge-difference density and terminal dipole; the persistence of the charge-dipole orientation; dielectric and mobile-carrier loss under continuous illumination; host-dependent rate changes; photostability; complete power conversion.

**Not established:** a chemically fueled real interface, whole-device negative real admittance, an autonomous oscillator, a useful energy generator, an independently validated new operating principle, or a civilization-level advance.

## 1. Preserve the chemical model, but close its independent-parameter loophole

The predecessor used states 0 and 1, E1-E0=-qV, with two chemically opposed reversible channels. Its small-signal reaction capacitance was

\[
C_r=\frac{nq^2}{4k_BT}\left[1-\gamma\tanh\left(\frac{\Delta\mu}{4k_BT}\right)\right].
\]

A passive RC load becomes locally unstable only when

\[
-C_r>C_0+(G_L+G_\ell)/\lambda_{\rm kin}.
\]

Local instability does not alone prove a stable nonlinear oscillation. The predecessor's energy balance is retained; nothing here permits extracting energy from a lone equilibrium bath.

A physically motivated source of the unusual barrier response is nonadiabatic Marcus transfer. Write D=Delta_mu/2, t=kBT, reorganization energy Lambda, and electronic prefactor K. Symmetric chemical forward rates can be constructed as

\[
a_+(V)=K\exp[-(\Lambda-D-qV)^2/(4\Lambda t)],
\qquad
b_+(V)=K\exp[-(\Lambda-D+qV)^2/(4\Lambda t)].
\]

Reverse rates are fixed by detailed balance, not supplied independently. Comparing with the prior model gives

\[
\boxed{\gamma=D/\Lambda},\qquad
\boxed{k=K\exp[-(D-\Lambda)^2/(4\Lambda k_BT)]}.
\]

Thus increasing inversion also suppresses the rate. At strong chemical driving and fixed K, geometry and Lambda, the gain-bandwidth factor is proportional to

\[
\frac{D-\Lambda}{\Lambda}
\exp[-(D-\Lambda)^2/(4\Lambda k_BT)].
\]

Its maximum occurs at D-Lambda=sqrt(2 Lambda kBT). This is a restricted design relation, not a general impossibility theorem for chemical networks. Real vibrational channels can strongly modify this classical estimate, as they do in the chosen material.

Terminal charge and capacitance likewise cannot be independently assigned. Let psi_w be the electrostatic potential created by a unit terminal voltage in the actual device geometry. Then

\[
\Delta q=-\int\Delta\rho(\mathbf r)\psi_w(\mathbf r)\,d^3r,
\]

up to terminal sign convention. For a one-dimensional layered dielectric,

\[
c_A=\left[\int dz/\epsilon(z)\right]^{-1},\qquad
q=e c_A\int_{z_e}^{z_h}dz/\epsilon(z).
\]

The same boundary-value problem determines both. Adsorption charge measured in a different geometry is not automatically this q.

## 2. Concrete material and the change of energy source

S1 reports CdS quantum dots with surface-bound alizarin in hexane, including an approximately 4.1-nm-diameter sample labeled QD-450. Under 600-nm excitation of the alizarin, electron transfer creates a charge-separated pair which predominantly recombines to the ground state. Excitation of the dot at 400 nm accesses a different, triplet-producing pathway. These are not interchangeable reset reactions.

The source describes a multistate sequence, not a two-state chemical fuel cycle:

\[
G\xrightarrow{\text{light}}X\xrightarrow{k_{\rm inj}}C\xrightarrow{k_{\rm rec}}G,
\]

with other relaxation, spin and trapping channels requiring separate accounting. The reduced two-state formation rate R is legitimate only after acquiring or eliminating X. If eta=k_inj/(k_inj+k_loss), then R approximately equals W eta, and

\[
\partial_E\ln R=\partial_E\ln W
 +(1-\eta)(\partial_E\ln k_{\rm inj}-\partial_E\ln k_{\rm loss}).
\]

Even fast charge formation is not proof that R is independent of electric field.

The supplementary data (S2, Tables 1 and 2) give a recombination driving magnitude about 1.51 eV for QD-450 and **two recombination components: 0.996 ns^-1 at 44% amplitude and 0.219 ns^-1 at 56%**. The reported arithmetic average, 0.561 ns^-1, cannot be used indiscriminately as the continuous-pump relaxation rate.

A biexponential fit does not uniquely distinguish static subpopulations from internal multistate dynamics. Our two-component calculation is explicitly a sensitivity analysis using the static-subpopulation interpretation. A measured generator or complete response function is required for a definitive prediction.

## 3. Source-linked barrier response, including molecular vibrations

The source fits its scaled rates using a Marcus–Levich–Jortner form,

\[
k(D)\propto\sum_{w\ge0}e^{-S}\frac{S^w}{w!}
\exp\left[-\frac{(\lambda_s+w\hbar\omega_v-D)^2}{4\lambda_s k_BT}\right],
\]

with lambda_s=0.15 eV, hbar omega_v=0.186 eV and S=2.7 (S1). These are fit parameters, not separately verified constants for a future device.

Differentiating that fit at D=1.51 eV and a chosen evaluation temperature 298.15 K gives

\[
a=-\partial_D\ln k\simeq5.98\ {\rm eV}^{-1}.
\]

Varying D over 1.41–1.61 eV gives approximately 4.37–6.59 eV^-1 within the same fixed-parameter fit. This does not include parameter covariance or uncertainty from transferring between samples.

**Critical unclosed transfer:** the published energetic trend is not a measured electric-field derivative of one fixed interface. Changes in electronic coupling, reorganization, optical pumping, surface structure or vibrational channels may invalidate the substitution partial_E ln k = a mu_z. That derivative must be measured or computed under the actual device boundary conditions.

If the substitution is valid, D(E)=D0-mu_z E, so stabilization of C decreases D and speeds its inverted recombination. A field-dependent pump must be included through

\[
a_{\rm eff}\mu_z=\partial_E\ln k-\partial_E\ln R.
\]

For immobile isotropically oriented dipoles of magnitude mu, number density rho, p=R/(R+k), and lambda=R+k, the scoped population susceptibility is

\[
\chi_{\rm pop}(s)=
-\frac{\rho\mu^2}{3}p(1-p)a_{\rm eff}\frac{\lambda}{s+\lambda}.
\]

Here chi=P/E has units F/m. The reaction admittance is (A/d) s chi; ordinary dielectric and conduction losses must still be added. If a_eff>0, this component has negative real admittance. **A negative component does not establish negative total device absorption.**

For a general linearized kinetic generator L, stationary state p0, and b=(partial_V L)p0, the corresponding expression is

\[
Y(s)=Y_{\rm passive}(s)+sN\mathbf q^T(sI-L)^{-1}\mathbf b
\]

on the probability-zero subspace. This is the required replacement when multiple states, populations or traps are resolvable.

## 4. Terminal dipole from a shared electrostatic geometry

`coupling_model.py` solves a scoped effective-mass problem, rather than inserting an electron-scale terminal charge.

A spherical dot of radius r0 is embedded in a uniform host. An external localized hole lies at radius rh on its polar axis; an electron is confined to the dot and is attracted toward the hole. The source supplies the approximate dot size and an effective electron mass 0.2m0 in its supplementary model. Core/host dielectric constants and the actual hole centroid are NOT acquired material data here.

For dielectric constants epsilon_c and epsilon_h, the uniform-field factor inside the sphere is

\[
L=3\epsilon_h/(\epsilon_c+2\epsilon_h),
\qquad
\kappa=(\epsilon_c-\epsilon_h)/(\epsilon_c+2\epsilon_h).
\]

The same dielectric boundary problem gives the terminal dipole

\[
\boxed{\mu_{\rm eff}/e
=r_h-\kappa r_0^3/r_h^2-L\langle z_e\rangle.}
\]

The external hole's screened potential inside the dot is expanded as

\[
\Phi_h=\frac{e}{4\pi\epsilon_0}
\sum_{l\ge0}\frac{2l+1}{l\epsilon_c+(l+1)\epsilon_h}
\frac{r^l}{r_h^{l+1}}P_l(\cos\theta).
\]

We solve H=-hbar² nabla²/(2m*)-e Phi_h with a hard spherical boundary using partial waves and radial finite differences. This estimates the charge centroid; it does **not** calculate the recombination matrix element. In particular, a hard wall sets the surface wavefunction to zero, so it cannot be used to validate a finite tunneling rate. The source's actual finite barrier, approximately 2.84 eV, and atomistic interface must be restored for such a joint electronic-structure calculation.

For radius 2.05 nm, epsilon_c=9, epsilon_h=2 and a hole centroid 0.30 nm beyond the surface, the executed estimate is:

- electron displacement toward the hole: 0.1082 nm;
- effective terminal dipole: 1.4601 e nm;
- corresponding terminal charge in a 1-micrometre uniform gap: 0.0014601 e, **not** an electron-scale terminal charge.

Varying the assumed core dielectric constant over 5,9,12 and the hole offset over 0,0.15,0.30 nm yields 0.725–1.722 e nm. This is a sensitivity range, not a confidence interval or experimentally bounded dipole.

Checks include a zero-hole parity control, the infinite-well eigenvalue, mesh/angular refinement, and a finite-field energy derivative matching the terminal weighting-field expectation. Omitted effects include electron self-image energy, finite-barrier leakage, ligand hybridization, anisotropy and polaron relaxation. No density-functional calculation was run.

For a volume-filled capacitor at fixed number density, q=mu_z/d, N=rho A d and C0=epsilon A/d. Thus the response-to-capacitance ratio is independent of d in this simple limit. Reducing the gap is not a free gain multiplier.

The illustrative mixture's background real permittivity is calculated from the same assumed core/host constants and dot volume fraction via dilute Maxwell–Garnett theory, rather than independently assigned. The resulting 1-mM dot concentration corresponds to approximately 2.17% core volume fraction and epsilon_eff=2.071. Ligands, interfaces, losses and non-dilute correlations require measurement.

## 5. Rotation can erase the gain

Allow the charge dipole to reorient with first-rank relaxation rate b=1/tau_r. In the scoped angular model, the ground state has zero dipole, both states have the same rotational diffusion, and pumping is isotropic and field independent. Let mC and mG be first orientational moments. Then

\[
\dot m_C=-(k+b)m_C+R m_G+\frac{\mu p}{3}(b\beta-ka)E,
\]
\[
\dot m_G=k m_C-(R+b)m_G+\frac{\mu p}{3}kaE,
\qquad \beta=(k_BT)^{-1}.
\]

Eliminating the moments gives

\[
\chi(s)=\frac{\rho\mu^2p}{3}
\frac{b\beta[1+R/(s+b)]-ka}{s+R+k+b}.
\]

For L=R+k+b,

\[
\operatorname{Re}[i\omega\chi(i\omega)]
=\frac{\rho\mu^2p}{3}
\frac{\omega^2\{(b\beta-ka)(b^2+\omega^2)+b\beta R(b+L)\}}
{(b^2+\omega^2)(L^2+\omega^2)}.
\]

Within this model, a necessary and sufficient condition for some frequency with negative reaction-plus-rotation absorption is

\[
\boxed{\tau_r>1/(ka k_BT).}
\]

It does not ensure that the negative band lies in a physically valid frequency range or that other losses are overcome. With the source two-component rates and the fitted a, the individual thresholds are approximately **6.5 ns and 29.7 ns**, stricter than the earlier single-average estimate of about 12 ns.

A constructive proposed control is a viscous nonpolar host. Hardy's original NBS measurements give n-hexadecane viscosity 3.0594 mPa s at 25 C for the tabulated 99.22%-purity composite sample (S3). A rigid 2.05-nm sphere then has the Stokes–Einstein–Debye estimate

\[
\tau_r=4\pi\eta r_0^3/(k_BT)\simeq80.5\ \mathrm{ns}.
\]

This is an independently specified way to slow physical rotation, **not** proof of persistent charge orientation. A hole hopping between surface ligands can erase the dipole without rotating the dot. Permanent ground-state dipoles, slip, ligand motion and anisotropic pumping also change the model. Furthermore, the published charge-transfer rates were acquired in hexane, not this proposed host. Solvent transfer requires remeasurement of kinetics, energetic response, dispersion stability and RF losses.

## 6. Source-linked measurement budget—not a generator prediction

`source_constrained_budget.py` retains the two measured decay components as a conditional static mixture. It uses the continuum nominal dipole, the computed 80.5-ns rigid-sphere reorientation estimate, a 100 by 100 micrometre electrode area, a 1-micrometre active gap, 1 mM dot density and 1% total charge-separated occupation. These geometry/concentration/occupation choices are assay design targets, not measured properties.

At equal pump rate per dot, the two occupations are 0.00338 and 0.01520. Their kinetic corners are approximately 159 and 35.4 MHz. The effective weak-pump rate is 0.333 ns^-1, not the amplitude-average 0.561 ns^-1.

At 90 MHz the executed conditional budget is:

| Quantity | Calculation |
|---|---:|
| Ideal mixture capacitance | 0.183 pF |
| Immobile reaction real admittance | -8.10 nS |
| Reaction plus modeled rotation real admittance | -5.43 nS |
| Maximum additional loss tangent, if no other losses | 5.24e-5 |
| 10-mV-peak probe's extra in-phase current | 54.3 pA |
| Incremental RF work supplied to that probe | 0.272 pW |
| Minimum productive absorbed 600-nm pump | 6.67 mW |
| Minimum absorbed pump per geometric area | 66.7 W/cm² |
| Ideal resonator Q required at 90 MHz, no parasitic capacitance | about 19,100 |
| Phase-resolution target for 20% signal precision | about 1.05e-5 rad |

The minimum absorbed pump assumes one productive absorbed photon per cycle. Incident pump, incomplete charge yield and auxiliary power can be higher. This table is **not** a claim that the material has adequate dielectric loss, breakdown reliability, photostability or optical absorption.

At 90 MHz, reorientation-time controls in the same model give +8.21 nS at 12 ns, +2.13 nS at 20 ns, -2.82 nS at 40 ns and -5.42 nS at 80 ns. A measured host change cannot be interpreted using these numbers until its rates and field slopes have also been remeasured.

The RC self-oscillation criterion from the predecessor is not met by this weak response. A passive resonator would have to satisfy its own measured total-loss threshold; its quality factor is not assumed available. Parasitic capacitance and dielectric loss can make the quoted ideal threshold much harder.

## 7. Noise, leakage and energy exclude easy technological claims

For independent immobile two-state units, the one-sided current-noise spectral density is

\[
S_I(\omega)=4N\langle q^2\rangle p(1-p)
\frac{\lambda\omega^2}{\lambda^2+\omega^2}.
\]

Comparing it with the population gain gives

\[
\boxed{\frac{S_I}{4|\operatorname{Re}Y_{\rm pop}|}=\frac1a.}
\]

This remains true for a static mixture with the same a in each component. The corresponding noise-to-gain temperature ratio 1/(kB a) is approximately 1940 K for the selected source-fit point. This is neither the sample temperature nor a complete amplifier added-noise temperature. Rotation and other losses/noise are not included in that simple ratio. Nevertheless, increasing site count or charge coupling cannot remove this noise penalty within the independent-site model.

At a single-component kinetic corner, mobile-carrier dissipation imposes another coupled constraint. If fraction f_escape creates carriers of lifetime tau_f and RF mobility sum M,

\[
\sigma_{\rm mobile}\simeq e\rho p k f_{\rm escape}\tau_f M.
\]

The ideal population gain has magnitude rho mu² p k a/6, so it requires

\[
f_{\rm escape}\tau_f M<\mu^2 a/(6e)
\]

before other losses. Blocking the electrodes does not eliminate dissipation by carriers moving inside the layer. Values for this product in the proposed interface are unacquired.

For the same single-component weak-probe limit,

\[
P_{\rm RF}/P_{\rm abs,min}=a(\mu E_{\rm peak})^2/(12h\nu).
\]

This is a local small-signal budget, not a universal maximum conversion efficiency. The full balance must include incident/absorbed/reflected optical power, useful electrical output, heat, luminescence and changes in stored energy. Continuous recycling also requires measuring the accumulated photochemical damage, not extrapolating a pump-probe transient to an indefinitely stable generator.

## 8. Decisive experiment and rejection conditions

**Stage A: establish the material response without claiming gain.** Reproduce the reference chemistry, acquire the complete charge-transfer dynamics, and measure the field derivatives of both formation and recombination in the same cell. The terminal charge-difference dipole must be obtained from a boundary-consistent calculation or measurement. An isotropic ensemble can cancel a naive first-order optical lifetime shift; an oriented sample is one option, but the following temporal separation provides a different calibration route.

**Post-formation voltage marking.** Create charge pairs with a weak optical pulse at zero field. Wait until their formation is substantially complete, then impose matched small positive and negative voltage steps. Subtract the corresponding dark electrical-step response and acquire the slower charge-displacement transient together with optical population decay. Applying the field only after formation removes the pump's field dependence from that segment of the experiment. This is a proposed calibration technique, not an asserted novel established method.

For one component, with surviving occupation p0 at the step and an initially isotropic dipole distribution, our angular model predicts

\[
\frac{Q_{\rm pop}(t)}{V}=
\frac{A\rho\mu^2p_0}{3d}
\frac{b\beta-ka}{b}
\left(e^{-kt}-e^{-(k+b)t}\right).
\]

In the immobile limit this becomes

\[
\frac{Q_{\rm pop}(t)}{V}=
-\frac{A\rho\mu^2p_0}{3d}\,ka\,t e^{-kt}.
\]

The characteristic delayed negative displacement is the proposed signature. Prompt electronic polarization, state-dependent polarizability, rotational torque and the actual formation/step impulse response must still be fitted or independently acquired. A second sequence with the voltage already present during formation can constrain the formation term; the difference should not be replaced with an assumed field-independent pump.

`pulse_calibration.py` executes the two-component version. For the same conditional continuum/host/geometry inputs as the final budget, 1% initially created pairs and an idealized 0.30-ns wait, it predicts approximately 85% survival to the voltage step. Per applied volt, the negative population charge peaks at **-7.27 attocoulombs around 1.52 ns**, and its initial current is approximately **-15.2 nA**. One volt across the assumed micrometre gap gives a small kinetic expansion parameter about 0.0087. These are instrument-design numbers, not measured signals or a breakdown certification.

This experiment needs subnanosecond electrical/optical timing, GHz-scale transient readout or calibrated impulse-response recovery, repeated averaging, and matched references against a much larger ordinary capacitive step. The finite formation kernel and state-dependent instantaneous polarization cannot be omitted merely because the illustrative formula assumes a completed preparation.

**The voltage step is an external energy source. This transient would identify a kinetic response; it would not demonstrate autonomous electrical power.** The population charge returns to zero after reset. It must lead to a separate zero-DC, constant-pump gain prediction and test.

Measure charge-dipole persistence, not just whole-particle rotation. Repeat all relevant acquisition after changing host.

A field-induced change of coupling or pump rate which makes a_eff nonpositive rejects the proposed population-gain route for that specimen. Unknown dielectric and mobile-carrier losses remain rejection gates even if a_eff is positive.

**Stage B: whole-device small-signal power test.** Use a sealed, optically accessible microcapacitor with chemically compatible insulating electrode coatings and measured voltage division. Maintain constant optical pumping and zero DC electrical bias. Measure complex admittance over approximately 10–500 MHz. Spectroscopy-based parameters must predict the electrical response before fitting the gain trace.

The required observation is **negative real admittance of the complete device** after correcting measurement leads and calibration errors, with uncertainty below the negative margin. Subtracting the device's own positive dielectric loss to reveal a negative reaction component is NOT success. Neither a negative pump-induced change nor negative imaginary capacitance passes the gate.

The small illustrative budget calls for approximately nanosiemens real-admittance precision against roughly 0.1 mS capacitive susceptance. Open/short/load and dummy-cell calibrations, shielding, reference-plane control and an independent power-flow measurement are essential. Ordinary cable capacitance can exceed the sample capacitance and further tighten phase-systematic requirements.

**Stage C: independent energy-flow validation.** Confirm reflected RF power greater than incident RF power through a characterized passive matching network, or demonstrate increasing electrical energy in a passive resonator after the RF seed is removed while the optical pump remains constant. A slower decay than the dark case is not enough. Autonomous oscillation is a separate, higher loss-budget test.

Long flat-top illumination windows can test quasi-steady gain before long-term stability is established, provided the measurement is well inside the flat top, far longer than the kinetic relaxation, and not driven by the pump edges. A long-term power claim requires sustained operation and a full energy balance.

Controls include dark operation; a temperature-matched heater; bare dots, free alizarin and ligand controls; measured pump stability; electrode leakage; illumination of contact-only dummy structures; host changes with all kinetics reacquired; occupation dependence; dose-dependent damage; and persistence tests excluding discharge of initially stored energy. The 400-nm pathway is a different-state control, not a predicted simple sign inversion. Heating, photoconduction, traps and instrument feedback must be excluded as alternative causes.

Cadmium-containing nanomaterial containment, solvent compatibility, photochemical stability, optical access, interfacial insulation and waste handling are real fabrication requirements. No breakdown rating or catalyst lifetime is established here. The weak probe avoids requiring the predecessor's large nanogap fields, but does not remove photocharging and interfacial-failure risks.

## 9. Prior art, unique capability and limits

Chemical inductance and delayed electronic/ionic responses already have extensive prior art (S4). Programmable catalytic charging and energy exchange are also not new broad principles (S5,S6). Light-to-RF conversion and room-temperature maser amplification have already been demonstrated (S7,S8). The candidate is not entitled to those broad novelty claims.

Its narrow possible contribution is **electrical work from incoherent, localized, inverted recombination through displacement current, without harvesting the reaction carriers at contacts**. Whether this precise operating mechanism is historically new has not been established by an exhaustive literature/patent review.

The correct comparator after the pivot is an optical power source plus RF electronics, or an optically pumped maser—not a chemically fueled fuel cell. The optical budget and independent-population noise provide no current evidence of superior power conversion or low-noise amplification. Avoiding sustained ionic transport is a possible architectural distinction, not a demonstrated cost, lifetime or efficiency advantage.

A successful experiment would establish a scientifically useful kind of kinetic electrical activity. It would not by itself meet the civilization-enabling technology objective. The present recommendation is one bounded, preregistered gain experiment after derivative/loss acquisition, not a generator development or scale-up program.

## Reproducibility and verification scope

Run in this order:

```sh
python feasibility.py --output results
python coupling_model.py
python source_constrained_budget.py
python pulse_calibration.py
```

Python 3.10+, NumPy 2.0+ and SciPy are required. Set OPENBLAS_NUM_THREADS=1 for the recorded small sparse calculations if desired.

The completed package contains **36 diagnostic groups: 17 kinetic/response checks, 7 continuum checks, 7 source-mixture checks and 5 pulse-calibration checks**. These include finite differences, matrix-resolvent comparisons, a time-domain response integration, selected detailed-balance/energy identities, mesh refinement and explicit passive controls. They are not 36 independent validations of the physical hypothesis. No laboratory work, atomistic electronic-structure computation, independent implementation audit or interval certification was performed.

The earlier `results/results.json` keeps the transparent single-average 1.5-eV instrument example used during development. The later **`results/source_constrained_results.json` supersedes it for the final material-linked budget**, using 1.51 eV, both decay components, computed continuum dipole, rotation and the coupled mixture permittivity. Keeping the earlier example does not endorse its immobile-average approximation as the material prediction.

The continuum model omits finite-barrier tunneling; the mixture model assumes a possible interpretation of biexponential data. Passing their internal checks does not close those physical modeling gaps.

## Research-capital use

Astra's task/evidence and technology entry material was read at revision `74c2843bd224c2975c6e46735b30ae7c927f948b`. The OpenAI mathematics repository entry was consulted selectively. No theorem from either repository is a load-bearing physical premise. Nothing was published back to either repository by this investigation.

## Primary references and access limitations

**S1.** Wang et al., *Marcus inverted region of charge transfer from low-dimensional semiconductor materials*, Nature Communications 12,6333 (2021). DOI 10.1038/s41467-021-26705-x. Full publisher HTML read. https://www.nature.com/articles/s41467-021-26705-x

**S2.** Supplementary Information to S1, particularly Tables 1–2 and Notes 2–5. PDF table pages 15–16 were inspected as images; the 600/400-nm pathway and modeling sections were read. https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41467-021-26705-x/MediaObjects/41467_2021_26705_MOESM1_ESM.pdf

**S3.** Robert C. Hardy, *Viscosity of n-Hexadecane*, Journal of Research of the National Bureau of Standards 61(5),433 (1958). Table 1 read from its page image. The 25-C 3.0594-cP value is the 99.22%-purity composite sample, not the separately discussed 99.94%-purity NBS standard at 20 C. https://nvlpubs.nist.gov/nistpubs/jres/61/jresv61n5p433_A1b.pdf

**S4.** Bisquert and Guerrero, *Chemical Inductor*, JACS 144(13),5996–6009 (2022). DOI 10.1021/jacs.2c00777. Primary abstract/metadata; no claim of exhaustive full-text priority clearance. https://pubmed.ncbi.nlm.nih.gov/35316040/

**S5.** Onn et al., *Platinum Graphene Catalytic Condenser for Millisecond Programmable Metal Surfaces*, JACS 144(48),22113–22127 (2022). DOI 10.1021/jacs.2c09481. Primary author-institution/publisher records. https://pubmed.ncbi.nlm.nih.gov/36383403/

**S6.** Abdelrahman and Dauenhauer, *Energy Flows in Static and Programmable Catalysts*, ACS Energy Letters (2023). DOI 10.1021/acsenergylett.3c00522. Inherited prior-art lead from predecessor; full publisher text remained inaccessible. This reference is not used to establish a particular new device result here.

**S7.** Day et al., *Room-Temperature Solid-State Maser Amplifier*, Physical Review X 14,041066 (2024). DOI 10.1103/PhysRevX.14.041066. Publisher abstract accessible. https://journals.aps.org/prx/abstract/10.1103/PhysRevX.14.041066

**S8.** *LED-pumped room-temperature solid-state maser*, Communications Engineering 4,122 (2025). DOI 10.1038/s44172-025-00455-w. Published comparator, not an alleged new ASTRA capability. https://www.nature.com/articles/s44172-025-00455-w

Recent catalytic-condenser, redox-transfer and RF developments were searched, including 2026 preprints. Inaccessible full texts and unrelated implementations were not treated as material qualification. Search coverage does not establish the absence of prior art. No third-party manuscripts or full source PDFs are redistributed in this package.
