# FJ physical alternative: acoustic pressure signaling instead of a neutral-liquid/electron port

**Status:** source-derived engineering proposal plus a bounded calculation from published electrokinetic measurements. No liquid-loaded acoustic device was fabricated or tested here. The selected acoustic composition is an experimentally grounded alternative for narrowband pressure *signals*; it is not a demonstrated steady-flow isolator or energy-transfer machine. Historical priority for the exact fluid-terminated composition remains unknown.

## Decision

The incoming physical source identifies the right bottleneck in its proposed neutral-liquid architecture: the required steady, reciprocal, zero-bias liquid-motion/electronic-current coefficient has not been measured for a complete neutral-liquid transducer. A stronger alternative for **directional pressure signaling** is to put an already demonstrated time-modulated acoustic isolator between conventional sealed pressure transducers. This removes the disputed liquid/electron interface. It also changes the operation: it sends a narrowband AC signal, not mean flow or steady hydraulic work.

The strongest experimental anchor found in this pass is Chen et al.'s three-resonator synthetic-magnetism coupler: it reports a forward transmission coefficient of 0.85 and 45 dB reverse isolation near 1.568 kHz. The authors realize the couplings using microphones, loudspeakers, amplifiers and relays, with a 55 Hz modulation offset; the experiment is airborne sound, not liquid acoustics. It therefore establishes an active acoustic signal router, not a passive wet interconnect. The full active electrical power, output noise spectrum and liquid-loaded transfer have not been reported in the evidence reviewed here.

The candidate use is a one-way, narrowband pressure-command link between two separately sealed liquid modules. An impermeable piezoelectric or compliant diaphragm terminates each liquid port; the dry acoustic core carries the signal between them. It could be useful where a pressure disturbance must be sent to a receiver without a shared liquid line. The receiver's pressure and volume flow must still be measured together to show work on a load. At present the operation is a plausible integration of known components, not an established new capability. It loses to an ordinary pump for fluid transport, and no advantage against direct electronic control for a pressure signal has been shown. The acoustic route's useful niche is unproven.

The more direct alternative for DC flow-to-current conversion is electrokinetics. It is experimentally obtainable and removes the “neutral liquid” requirement, but the strongest directly relevant data show very low conversion and pressure-limited scaling. A conditional calculation using a measured colloid-plug transport fit gives $\chi=9.375\times10^{-3}$ and $Z=\chi/(1-\chi)\approx9.464\times10^{-3}$, a single-converter maximum efficiency of about 0.235%, and—only for the incoming source's grounded three-terminal quasistatic topology—an identical-pair directional work-transfer ceiling of $1.39\times10^{-6}$ of source hydraulic power. This is a modeled ceiling from fitted coefficients, not an assembled-device measurement. The source paper did not directly measure both reciprocal cross-responses on the same plug.

## Mechanism and physical boundary

Use three resonant cavities (A,B,C). Cavities (A) and (C) are degenerate at angular frequency \(\omega_0\); cavity (B) is detuned by the modulation frequency \(\Omega=\omega_B-\omega_0\). There is a static (A\leftrightarrow C) path and two phase-programmed time-dependent paths:

\[
k_{AB}(t)=\Delta k\cos(\Omega t+\phi_1),\qquad
k_{BC}(t)=\Delta k\cos(\Omega t+\phi_2).
\]

At the operating frequency, the indirect path visits the (+1) Floquet sideband in (B) and returns to \(\omega_0\) at (C\). The two paths have a loop phase. In a reduced path description,

\[
t_{A\to C}=t_s+t_d e^{i\Phi},\qquad
t_{C\to A}=t_s+t_d e^{-i\Phi}.
\]

The reverse direction conjugates the dynamically accumulated phase. With equal path magnitudes and the relative phase chosen for destructive interference in reverse, one direction cancels while the other adds. Chen et al. give the ideal conditions \(\Delta\phi=\pi/2\) and \(k_{AC}^2=\Delta k^2/4\). Cascaded sideband conversion returns the transmitted signal to its original carrier frequency.

This is a driven Floquet system. The modulation waveform, microphone/speaker loops, amplifiers, relay drive, source signal and dissipative losses all belong in the energy boundary:

\[
P_{\rm acoustic,in}+P_{\rm modulation}+P_{\rm electrical,control}
=P_{\rm acoustic,out}+P_{\rm loss}+\frac{dE_{\rm stored}}{dt}.
\]

The modulation may exchange work with the signal even when the final carrier frequency is unchanged. The reported isolation ratio is not an efficiency. The candidate does not create mean flow at zero signal or transmit fluid molecules.

For a liquid-terminated version, let the measured port variables be pressure (p_i(t)) and volume flow (Q_i(t)). Useful receiver power is

\[
\overline P_{\rm receiver}=\frac{1}{T}\int_0^T p_2(t)Q_2(t)\,dt,
\]

not pressure amplitude alone. An AC pressure signal can produce oscillatory volume displacement; its cycle-average work is zero unless it is phase-matched to a dissipative or active load. Rectification or nonlinear streaming would be a separate mechanism and must not be silently counted as output of this linear coupler.

## What is experimentally demonstrated

The primary acoustic article reports the following parameters and implementation:

| Quantity | Reported value / implementation | Scope |
|---|---:|---|
| $A,C$ resonance | $f_A=1568$ Hz | Air-filled acoustic cavities |
| $B$ resonance | $f_B=1623$ Hz | Detuning / coupling modulation $\Omega/2\pi=55$ Hz |
| Intrinsic loss | $\gamma/2\pi=4.5$ Hz | Single-cavity fitted loss; roughly 9 Hz full linewidth under the paper's CMT convention |
| Three-cavity measured coupling | $\Delta k=7.5$ Hz, $k_{AC}=3$ Hz | One experimental operating point; ideal model match is $k_{AC}=\Delta k/2=3.75$ Hz |
| Directionality | 45 dB isolation; forward transmission coefficient 0.85 | Measured in airborne sound, around the tuned carrier |
| Coupling hardware | Microphones, speakers, signal amplification, DC-powered electronics, and DPDT relay switching | Active synthesized coupling; the article does not provide a full wall-plug energy budget |

The 45 dB isolation means reverse/forward transmission-amplitude ratio $10^{-45/20}=5.62\times10^{-3}$. For equal normalized port impedance this corresponds to a reverse/forward transmitted-power ratio of $3.16\times10^{-5}$. The forward coefficient 0.85 is not a wall-plug efficiency; if it is interpreted as a matched-port amplitude coefficient, its corresponding signal-power fraction is $0.85^2\approx0.72$, before the modulator and control power are charged.

The fitted single-cavity resonance gives a narrow operating window: $Q\approx f_A/(2\gamma/2\pi)=1568/9\approx174$, using the usual CMT half-width convention. The 55 Hz modulation offset is not a 55 Hz data bandwidth. The measured nonreciprocity is near one carrier; a broadband liquid-pressure transfer was not shown.

## Why it is not a DC replacement

The path removes the need to know the neutral liquid's electronic cross-coefficient by using conventional pressure-to-electrical and electrical-to-pressure transducers at the wet boundaries. That substitution introduces two new boundaries and a powered controller. With piezoelectric diaphragms, the sealed liquid ports can remain chemically isolated, but their fluid loading changes the transducer and cavity responses. At room temperature the characteristic acoustic impedance is $Z_a=\rho c$: water is about $1.5\times10^6$ Pa·s/m and air about $4\times10^2$ Pa·s/m, a mismatch of order $3.5\times10^3$. A diaphragm can transform impedance, but matching loss, resonance shift and acoustic leakage must be measured. A dry air core behind two diaphragms preserves the demonstrated core but makes both wet/dry transitions decisive. A fully liquid-filled version would be a different resonator design.

At the demonstrated 1.568 kHz carrier, the wavelength in water is about 0.95 m. A compact liquid implementation cannot simply copy the air-cavity geometry; compliant or Helmholtz-type resonators and the diaphragm's mass/compliance would set the modes. This is a concrete engineering barrier rather than evidence of impossibility.

The signal chain is already active: microphones detect cavity pressure, an amplifier drives speakers, and relays switch coupling sign at the detuning rate. For an instrument that already has pressure sensors and actuators, ordinary electronic feedback can command the downstream pressure without adding a resonant acoustic core. The coupler's demonstrated advantage is high reverse isolation in a resonant acoustic network, not a demonstrated lower-energy or lower-latency controller.

## Direct electrokinetic comparator and bounded calculation

Pingulkar, Ayela and Salmon tested an aqueous 0.1 mM NaCl electrolyte through a 2 cm packed-colloid plug in a 0.5 mm-radius tube. They report hydraulic resistance $R_h\approx1$ bar·min/µL, fitted streaming-current coefficient $S_{str}\approx25$ nA/bar, and internal electrical resistance $R_C=25\pm5$ MΩ. At a 5 MΩ external load, their directly measured conversion efficiency was about 0.14%; the plug generated about 0.09 µW at 6 bar. A shorter 3 mm plug with nine-times-lower hydraulic resistance gave about 0.18% at its matched load. In the pervaporation configuration, five PDMS leaves produced about 0.18 nW at 0.14% efficiency. Cavitation repeatedly appeared when leaf pressure approached zero; this limited the demonstrated surface-area scaling.

Using their central fitted values as a local linear two-port estimate:

\[
K=R_h^{-1}=1.67\times10^{-16}\;\mathrm{m^3\,Pa^{-1}s^{-1}},\quad
G=R_C^{-1}=4.0\times10^{-8}\;\mathrm S,
\]
\[
C=S_{str}=\frac{25\times10^{-9}\;\mathrm{A/bar}}{10^5\;\mathrm{Pa/bar}}
=2.5\times10^{-13}\;\mathrm{A/Pa},\quad
\chi=\frac{C^2}{KG}=9.375\times10^{-3},\qquad
Z=\frac{\chi}{1-\chi}=9.464\times10^{-3}.
\]

For the single-converter expression \(\eta_c=(\sqrt{1+Z}-1)/(\sqrt{1+Z}+1)\), this gives \(\eta_c\approx2.355\times10^{-3}\). The incoming source's contact-inclusive grounded three-terminal topology then gives, for two identical ports,

\[
\eta_{\rm pair}\le\tfrac14\eta_c^2\approx1.39\times10^{-6}
=0.000139\%.
\]

Varying only the paper's stated $R_C=20$–$30$ MΩ fit range gives $\eta_{\rm pair}\lesssim0.89$–$2.00$ ppm. This calculation is conditional: $S_{str}$ and $R_C$ are fitted from the loaded streaming-potential model, the paper does not independently measure the reverse electro-osmotic coefficient on that same plug, the reported $R_h$ and $S_{str}$ have no full uncertainty in the text, and the bound applies only to the stated source topology. It is not a universal electrokinetic or acoustic limit.

This route is more direct than the acoustic route for sustained DC operation and gives measurable paired engineering parameters, but it requires mobile ions and sacrifices most input work to losses. It does not meet the neutral-liquid requirement and is not an attractive bulk-energy transfer mechanism. It is the right fallback only where electrolytes are acceptable and the objective is sensing or small electrical output rather than fluidic work transfer.

## Strongest relevant control comparator

For moving a real sample, a piezoelectric micro-diaphragm pump is a more relevant comparator than a resonant signal coupler. Bußmann et al. measured a pump with passive spring valves that transports cell solution: at the reported single-stroke setting, one stroke used about 2 mJ and transported about 10 µL, an actuator-only cost of roughly 0.2 J/mL before driver electronics. The device transported a 500 µL cell sample in under 10 s; a 30 Hz characterization gave an extrapolated blocking pressure near 70 kPa. Leakage at 50 kPa was under 30 µL/min before sample handling, while one of six pumps rose to 260 µL/min after fibers were found in its valves. The hybrid waveform produced a similar cell impact to sinusoidal actuation while retaining rectangular-waveform fluidic performance; it left about 7.3 percentage points fewer intact Jurkat cells and 4.6 fewer K-562 cells than controls. Long-term cell activity was not measured. These are measurable tradeoffs of a direct flow controller. It is a moving-valve solution and shares the fluid path, but it supplies mean flow and quantified load performance that the acoustic candidate does not.

Thus the acoustic alternative only survives for a narrower requirement: transmit an AC pressure command across an impermeable boundary with high one-way signal isolation. If the requirement is DC flow, dosing, pressure generation or work recovery, use and optimize the actual pump/valve or an appropriate pressure exchanger. If the requirement is only a directionally isolated command, a direct electronic controller is the equal-information, lower-complexity baseline. No system-level advantage over either baseline is established.

## Noise, energy, preparation, bandwidth and scale

- **Noise:** 45 dB is reverse isolation, not signal-to-noise ratio. The acoustic paper gives no calibrated output noise spectral density or full controller-noise budget. The microphones, amplifier, speaker, relay switching, diaphragm thermal motion, pressure-sensor noise and electrical feedthrough must be measured. An equilibrium compliance $C_{ac}=dV/dp$ has thermal pressure variance $\langle p^2\rangle=k_BT/C_{ac}$ in the single-mode lumped model; the actual liquid-loaded compliance and bandwidth are unmeasured.
- **Energy:** the acoustic signal's input/output pressures are not the complete energy boundary. Measure source acoustic power, amplifier DC input, modulation/relay power, wet transducer driver power, receiver load work, and dissipated heat. Frequency preservation at the output does not imply zero work exchanged with the modulator. Electrokinetic measurements are explicit about a hydraulic input but remain at sub-percent conversion.
- **Preparation:** tune three resonances, set the 55 Hz detuning, calibrate both dynamic couplings and their relative phase, set the direct (A-C) path, then remeasure after attaching the fluid diaphragms. In the source experiment, the cavity resonances and coupling sign are adjusted, with relay-driven switching and microphone/speaker calibration. The wet adaptation adds diaphragm fabrication, sealing and pressure calibration.
- **Bandwidth:** expect a carrier-centered window on the order of the measured cavity linewidth (about 9 Hz full width in the source's fitted single-cavity convention), unless a new broader design is demonstrated. The modulation frequency is not the usable signal bandwidth. Off-resonance isolation, pressure-step response and low-frequency/steady transfer are not established.
- **Scaling and manufacture:** one resonant network requires matched cavities, active coupling electronics and phase calibration; adding channels adds resonators, modulation paths, cross-talk and control power. Chip-scale liquid resonators face the water/air impedance contrast and wavelength/compliance issues above. Reproducibility, sealing lifetime, fouling, drift, assembly yield and cleanability have no results here.
- **Mechanics:** the paper's “without relying on mechanical motion” means it avoids a biased bulk medium flow; it still uses microphones, speakers and switching hardware. The liquid module's piezo diaphragm also moves. Any no-moving-parts or reduced-maintenance claim would be false for this proposed integration unless separately redesigned and tested.

## Decisive bench test

Build two water-filled, hydraulically isolated channels, each ending at an impermeable diaphragm coupled to the (A) or (C) port of the three-cavity core. Keep the active acoustic core dry. Characterize the complete two-port response before assembly: (T_{CA}(f)=p_C/p_A), (T_{AC}(f)=p_A/p_C), the port impedances, diaphragm motion, electrical feedthrough, and all drive powers. Then repeat with a measured receiver resistance/compliance that allows (p_2(t)Q_2(t)) work to be integrated.

Pre-register a narrowband pass criterion at the retuned carrier: (i) forward normalized acoustic-power transmission at least 0.5; (ii) reverse isolation at least 30 dB after correcting both liquid ports to the same power normalization; (iii) carrier-frequency output after measuring all Floquet sidebands; (iv) receiver work follows the predicted load dependence; and (v) no common liquid, electrical leakage or unintended direct vibration path. Use source-paper-scale 45 dB and 0.85 only as stretch targets, not assumptions.

Controls: turn modulation off; sweep relative phase through $0,\pi/2,\pi$; set $k_{AC}=0$ and then tune it through the destructive-interference condition; reverse source and receiver; replace the modulated coupler with a reciprocal electrical/acoustic path; measure empty-port/electrical pickup; and compare against direct sensor-to-actuator feedback and a conventional pump on the same liquid load. Simultaneously integrate output work and every electrical input.

The proposal fails as a fluidic capability if isolation vanishes when the liquid diaphragms and receiver load are attached, if output pressure is only sensor pickup without receiver work, if matched-port directionality requires high modulation or amplifier power, if isolation is confined to a tolerance-infeasible resonance, or if direct feedback achieves the same task with lower complete energy and complexity. If it works but has no net DC flow, its evidence status remains “narrowband pressure signaling,” not “hydraulic isolator.”

## Novelty and pivot

The demonstrated physical principle—time-modulated acoustic nonreciprocity—is established prior art, and the exact microphone/amplifier/speaker coupling is an active signal-processing implementation. The proposed wet-boundary integration has not been shown here to add an operation that ordinary piezoelectric transduction and electronic control cannot provide. Historical priority for a liquid-terminated version was not exhaustively searched and remains UNKNOWN. Do not promote this as a new nonreciprocal force, a pump, a passive isolator, or an energy technology.

The useful pivot is to separate two experiments. For the original neutral-liquid idea, directly measure the steady paired coefficients $\partial I/\partial p|_V$ and $\partial Q/\partial V|_p$ before building the Hall assembly. For a pressure-signal application, run the sealed-diaphragm acoustic test above and charge all modulation power. If neither test beats its matched comparator, preserve the demonstrated acoustic and electrokinetic results as engineering baselines and close this alternative as no breakthrough.

## References

1. Z. Chen et al., “Sound non-reciprocity based on synthetic magnetism,” *Science Bulletin* 68 (2023), 2164–2169, DOI [10.1016/j.scib.2023.08.013](https://doi.org/10.1016/j.scib.2023.08.013); primary preprint [arXiv:2209.15192v1](https://arxiv.org/abs/2209.15192v1). Full 13-page preprint PDF and extracted text are in `primary/`.
2. H. Pingulkar, C. Ayela and J.-B. Salmon, “Pervaporation-driven electrokinetic energy harvesting using poly(dimethylsiloxane) microfluidic chips,” *Lab on a Chip* 24 (2024), 5328–5337, DOI [10.1039/D4LC00831F](https://doi.org/10.1039/D4LC00831F); [arXiv:2411.15226v1](https://arxiv.org/abs/2411.15226v1). Full 10-page preprint PDF and extracted text are in `primary/`.
3. A. Bußmann et al., “Microfluidic Cell Transport with Piezoelectric Micro Diaphragm Pumps,” *Micromachines* 12 (2021), 1459, DOI [10.3390/mi12121459](https://doi.org/10.3390/mi12121459). Full HTML copy is in `primary/`.
4. For the pressure-transducer impedance estimate, use $Z_a=\rho c$, IAPWS/NIST water-property formulations ([IAPWS R6-95](https://www.iapws.org/relguide/IAPWS-95.html), [NIST SRD 10](https://www.nist.gov/srd/nist-standard-reference-database-10)) and NASA standard-air values ([NASA Glenn](https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/air-properties-definitions/); sound-speed table [NASA technical note](https://ntrs.nasa.gov/api/citations/20160000818/downloads/20160000818.pdf)). Values are order-of-magnitude inputs at room conditions, not a measured diaphragm transfer.

The incoming FJ physical source remains preserved, unchanged, at `work/FJ-sources/physical_PASTED_SOURCE.txt`. The electrokinetic reconstruction and code are separate, explicitly derived artifacts under this directory.
