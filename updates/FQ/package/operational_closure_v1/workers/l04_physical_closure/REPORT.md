# L04 — Physical closure audit of amplitude-cancelled NV pulse-order magnetometry

15 October 2026, Australia/Brisbane. **Finding: the proposed $K_r$ is a useful linearity-rejection contrast, but it is not specific to interfacial current partition or a new physical operation.** A general nonlinear electrochemical response and an exactly linear electrode with nonlinear NV transduction both give nonzero $K_r$. Battery NLEIS already measures higher-order electrochemical response; its raw-data comparator can compute this contrast and use the rest of the same records. No $K_r$ experiment, physical control result, or candidate-specific output is present in the inspected workspace. Advantage and novelty remain **UNKNOWN**.

## Scope and evidence boundary

I read the assigned [S09 report](../s09_joint_quantum/REPORT.md), including its proposed sequence, model, acquisition plan, and explicit statement that no laboratory data were produced. I also read the campaign [brief](../../BRIEF.md). The conclusions below are my independent analytic audit; they do not alter S09's derivation or turn its symbolic receipt into an experiment.

The physical affordance is established at a narrower level. Liu et al. embedded micrometre-scale NV-bearing diamond particles in Fe3O4 composite electrodes and measured local magnetic changes during battery discharge. Their paper reports multiple NV-orientation resonances, uses fitted ODMR dips to estimate field, notes that NV levels also respond to temperature and stress, and observes laser heating at some locations. It documents heterogeneous histories at selected sensor locations. This supports the sensor–electrode interaction and the need for thermal and spectral controls. It does not test order-reversed pulses, $K_r$, local reversible charge partition, or a consequential control decision. [Liu et al., *Device* 2, 100521 (2024)](https://doi.org/10.1016/j.device.2024.100521).

There is also direct prior art for the strongest competing diagnostic. Murbach, Hu, and Schwartz report full-frequency second-harmonic nonlinear electrochemical impedance spectroscopy on commercial LiNMC|C cells; they vary modulation amplitude, state of charge, and state of health, and report sensitivity to early degradation even when capacity loss is below 1%. [Murbach et al., *J. Electrochem. Soc.* 165, A2758 (2018)](https://doi.org/10.1149/2.0711811jes). Ernst et al. separately acquire charge- and discharge-direction nonlinear response, current-pulse pairs with relaxation, higher harmonics, and electrode-resolved measurements; their paper discusses third-harmonic response and identifies nonlinear charge transfer and diffusion as plausible sources, while marking some mechanistic attribution as tentative. [Ernst et al., *Frontiers in Energy Research* 7:151 (2019)](https://doi.org/10.3389/fenrg.2019.00151). Liebhart et al. explicitly extend frequency response to a Volterra model and apply nonlinear impedance measurements to pouch cells under controlled temperature, state of charge, and compression. [Liebhart et al., *J. Power Sources* 480, 228673 (2020)](https://doi.org/10.1016/j.jpowsour.2020.228673). These papers concern different cell materials and outputs; they do not establish the proposed Fe3O4/Li NV result. They do establish that amplitude-dependent and higher-order cell response is a standard competitor, not a special signature of the proposed hidden gate.

An NV-specific competitor is equally important. The embedded-battery paper itself fits a spectrum containing several orientation-dependent dips. A 2026 primary study of NV nanodiamond ensembles reports that overlapping resonances from random axes distort the line shape and break the linear frequency-to-field map under conventional Lorentzian fitting; model-assisted regression reduced reported RMSE under the same acquisition conditions. This is not evidence that the exact embedded sensor has a cubic error, but it confirms that the field-extraction map must be calibrated and that fitted “field” can inherit nonlinear spectral bias. [Gao et al., *Optics Express* 34 (2026)](https://doi.org/10.1364/OE.589141).

## Exact meaning of the contrast

Write the $+U,-U$ waveform as $u(t)=Up(t)$. For identical pulse shapes and duration, the $-U,+U$ waveform is exactly $-Up(t)$. Suppose the measured output admits a Volterra expansion about a fixed initial state:

\[
y[U p]=y_0+\sum_{n\ge 1} U^n a_n[p].
\]

Here $a_n[p]$ is the $n$-th order memory-kernel functional evaluated on the fixed pulse shape, not necessarily a static polynomial coefficient. Because the second waveform is the negative of the first,

\[
C(U)=y[Up]-y[-Up]=2(Ua_1+U^3a_3+U^5a_5+\cdots),
\]

and therefore

\[
K_r(U)=C(rU)-rC(U)=2\sum_{\substack{n\ge3\\n\text{ odd}}}(r^n-r)U^n a_n.
\]

This cancellation is exact for the degree-one response, including an arbitrary linear relaxation kernel. It retains the entire odd nonlinear response above degree one. At small amplitude, the cubic term may dominate if the system is analytic and the coefficient is nonzero; at finite amplitude, fifth and higher odd terms also contribute. Even-order terms vanish from this particular sign-reversal contrast. Thus $K_r\ne0$ says “the measured order contrast is not purely degree one under these matching assumptions.” It does not identify which part of the cell or sensor caused the nonlinearity.

An exact cubic Volterra competitor makes this limit explicit. Let an effective local magnetic state obey

\[
\dot x=-b x+a_1u+a_3u^3,\qquad y=kx,
\]

with $b>0$, fixed initial state $x_0=0$, and readout linear in the state. This is a first-order relaxation channel driven by a cubic current response; it is a canonical third-order input-output model for nonlinear electrochemical response, not a claim that one specific microscopic reaction follows this exact law. Set $\rho=e^{-b\tau}$. Integrating each constant pulse exactly gives

\[
y_{+-}(U)=-\frac{k}{b}(1-\rho)^2(a_1U+a_3U^3),\quad
y_{-+}(U)=+\frac{k}{b}(1-\rho)^2(a_1U+a_3U^3),
\]

so

\[
C(U)=-\frac{2k}{b}(1-\rho)^2(a_1U+a_3U^3),\quad
K_r(U)=-\frac{2k}{b}(1-\rho)^2a_3(r^3-r)U^3.
\]

This produces exactly the proposed cubic scaling, with no hidden even-in-current gate state $z$. The physical literature above shows that real lithium-ion cells exhibit nonlinear charge-transfer, diffusion, and higher-harmonic responses. The matching here is mathematical; it is not evidence that the Fe3O4/Li electrode has a nonzero $a_3$.

## Exact sensor and initial-state countermodels

**Linear specimen, nonlinear NV readout.** Let the specimen's local magnetic field (x) be linear in the applied waveform:

\[
\dot x=-b x+c u,\qquad x(0)=0,
\]

and let the reported ODMR-derived field be $y=G(x)=x+\lambda x^3$. With $\alpha=c(1-e^{-b\tau})^2/b$, the two final true fields are $x_{+-}=-\alpha U$ and $x_{-+}=+\alpha U$. Hence

\[
C(U)=-2\alpha U-2\lambda\alpha^3U^3,\qquad
K_r(U)=-2\lambda\alpha^3(r^3-r)U^3.
\]

The electrode and field dynamics are linear; all nonzero $K_r$ comes from the sensor/readout map. $G$ is an exact countermodel, not a claim about the calibrated sensor's actual error curve. Its plausibility as a control target follows from the documented line-shape, orientation, temperature, and fit sensitivities in the NV literature. A full-spectrum fit and external-coil calibration across the exact field, temperature, optical-power, and microwave-power range are needed to bound this term. A nearby reference NV alone cannot prove a linear local transfer function.

**Linear specimen, amplitude-correlated initial-state imbalance.** Retain the linear state equation \(\dot x=-b x+c u\), but allow different sacrificial lane groups to start at initial means \(\mu_{+-}(U)\) and \(\mu_{-+}(U)\). With \(\rho=e^{-b\tau}\), and after subtracting each lane's own start measurement, the contrast is

\[
C(U)=-2\alpha U+(\rho^2-1)\Delta\mu(U),\quad
\Delta\mu(U)=\mu_{+-}(U)-\mu_{-+}(U).
\]

The residual initial state decays during the two-pulse pair, so baseline subtraction does not make different initial states identical. Consequently,

\[
K_r(U)=(\rho^2-1)\{\Delta\mu(rU)-r\Delta\mu(U)\}.
\]

For the exact imbalance \(\Delta\mu(U)=dU^3\), a wholly linear plant yields \(K_r=(\rho^2-1)d(r^3-r)U^3\). Randomized blocked assignment makes this artifact mean-zero under an exchangeable initial-state law, but finite groups can still have imbalance; systematic SOC, formation, temperature, location, or assignment drift can make it worse. The experiment therefore needs independent sacrificial lanes, pre-pulse spectra, blocked randomization on measured baseline features, and time-matched no-current drift controls. A repeated pulse on one lane is not a replacement unless reset and history equivalence are demonstrated.

## Strongest comparator and decision boundary

The closest physical comparator is a standard NLEIS/Volterra analysis of the same applied current and measured voltage, with a regularized low-order model selected on development lanes and frozen before held-out lanes. For the proposed sensor output, the comparator should also receive the same raw ODMR spectra and fit them with a calibrated full NV Hamiltonian / ensemble model, rather than receiving only S09's scalar $K_r$. It should receive the same pre-pulse baseline, temperature, optical and microwave settings, reference-channel records, lane metadata, and any permitted post-pulse chemistry. The report's own strongest quantum comparator—ordinary operando NV spectra with optimized current pulses—is then a strict same-information comparator: it can calculate $K_r$ after seeing the raw data and can also use all remaining spectral and electrochemical information. A deterministic contrast cannot contain more information than the record from which it is calculated.

This does not make $K_r$ useless. It may be a convenient prespecified null test that rejects the linear-response explanation with a compact scalar. Its burden is to show a reliable, decision-relevant benefit against nonlinear electrochemical and NV analyses that see the same acquisition. A positive $K_r$, a cubic amplitude law, or a short-time $\tau^2$ law alone cannot distinguish reversible diffusion, Butler–Volmer response, magnetic reorientation, heating, sensor transfer error, and the proposed interfacial storage mechanism. Chemical identity requires a separately calibrated chemical observation.

## One decisive lab design with matched raw data and costs

Use at least two independently fabricated batches of formed Fe3O4/Li microcells with multiple electrically isolated sacrificial lanes under a shared, characterized optical and thermal environment. Pre-register the SOC window, pulse shape, $U,rU$, and at least three pulse durations. Randomize the four order-by-amplitude conditions across lanes within blocks matched on pre-pulse ODMR spectra, location, SOC, and temperature. Read full spectra before and after each pulse pair at the same zero-current rest delay. Include time-matched no-current lanes, nonmagnetic-electrode shams, no-NV lanes to measure inclusion-induced kinetics, and a calibrated external coil applying the same field waveforms to embedded NV sensors without an active electrochemical response. Record raw spectra, current, voltage, temperature, optical/microwave settings and energy, coil field, and location registration. Measure actual cell energy $\int VI\,dt$; commanded net charge cancellation does not make dissipated energy zero.

Freeze three analyses before the holdout: (1) the S09 $K_r$ statistic; (2) a low-order Volterra/NLEIS fit to current, voltage, temperature, and ODMR output; and (3) a conventional NV spectral estimator and pulse-based predictor. All receive the identical raw files and measured baselines. On independent sacrificial lanes, use registered local chemical/structural analysis after the pulse pair to measure whether any field contrast corresponds to changed Fe state or morphology; then test predictions on held-out cells cycled under predeclared schedules. The primary score is the held-out location-level chemistry or fade decision fixed before data collection, with calibration and prediction error reported. The claim passes only if $K_r$ improves that decision over the frozen same-data competitors and shams while its effect survives the coil-only NV calibration, initial-state blocks, thermal controls, and sensor-inclusion control. A contrast explained by the sensor transfer curve or by the Volterra/current–voltage model closes the candidate's claimed distinctiveness.

Charge every arm for formation and fabrication of matched lanes; NV diamond placement and its perturbation; cell and reference-electrode materials; potentiostat and leads; laser, microwave, magnet, temperature control, optical integration, and full-spectrum acquisition; calibration coils and standards; each pulse's cell energy; sacrificial replicates and reset assays; destructive chemical analysis; failed lanes; operator and instrument time; analysis compute; and any later cycling needed for the decision outcome. Because every frozen analysis gets the same raw acquisition, these physical acquisition costs are shared and charged identically; any different analysis or calibration cost is added to its arm. No such costs or measured sensitivity are currently acquired for the proposed arrangement.

## Status

No lab data, instrument receipt, physical control, or battery-control outcome was found in the assigned campaign material. The literature establishes (i) embedded NV detection of local magnetic evolution in Fe3O4 electrodes and (ii) experimental nonlinear battery response measured by NLEIS/Volterra methods. The exact S09 pulse-order statistic has not been observed in that literature as inspected here. Its historical novelty is **UNKNOWN**. The only current candidate-specific result is an analytic prediction; it does not establish physical access beyond existing embedded-NV sensing, a local chemical assignment, improved battery control, a total-cost advantage, or a new quantum capability.

## Primary sources inspected

1. Liu et al., “Operando quantum sensing captures the nanoscale electrochemical evolution in batteries,” *Device* 2, 100521 (2024), [DOI and primary full text](https://doi.org/10.1016/j.device.2024.100521). Inspected the abstract, NV and temperature discussion, multi-orientation spectrum fitting, local magnetic trajectories, laser-heating caveat, and methods.
2. Murbach, Hu, and Schwartz, “Nonlinear Electrochemical Impedance Spectroscopy of Lithium-Ion Batteries: Experimental Approach, Analysis, and Initial Findings,” *J. Electrochem. Soc.* 165, A2758–A2765 (2018), [DOI and publisher page](https://doi.org/10.1149/2.0711811jes). Inspected the abstract and experimental-method description for full-frequency second-harmonic spectra, amplitude variation, SOC/SoH comparison, and early-degradation sensitivity.
3. Ernst et al., “Capturing the Current-Overpotential Nonlinearity of Lithium-Ion Batteries by Nonlinear Electrochemical Impedance Spectroscopy (NLEIS) in Charge and Discharge Direction,” *Frontiers in Energy Research* 7:151 (2019), [primary full text](https://doi.org/10.3389/fenrg.2019.00151). Inspected theory, pulse-pair/NLEIS procedures, harmonics, experimental parameters, conclusions, and data-availability statement.
4. Liebhart, Satzke, Komsiyska, and Endisch, “Application of nonlinear impedance spectroscopy for the diagnosis of lithium-ion battery cells under various operating conditions,” *J. Power Sources* 480, 228673 (2020), [DOI](https://doi.org/10.1016/j.jpowsour.2020.228673). Inspected the publisher result/abstract description of the Volterra extension and controlled pouch-cell experiments; not the full article.
5. Gao et al., “Accurate magnetic field estimation in fiber-coupled nanodiamond NV ensembles using model-assisted regression,” *Optics Express* 34 (2026), [DOI and primary metadata/abstract](https://doi.org/10.1364/OE.589141). Inspected the primary abstract describing resonance-overlap distortions, nonlinearity of the frequency-to-field map, systematic errors, and same-acquisition RMSE comparison. Its fiber-coupled geometry is not the embedded battery geometry.
