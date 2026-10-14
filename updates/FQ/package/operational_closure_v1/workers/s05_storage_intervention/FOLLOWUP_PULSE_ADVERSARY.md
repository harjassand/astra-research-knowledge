# Adversarial audit of the opposite-order NV pulse contrast

15 October 2026. This audits [`s09_joint_quantum/REPORT.md`](../s09_joint_quantum/REPORT.md) without altering it. **Verdict:** the amplitude contrast is a valid way to reject responses linear in commanded pulse amplitude under matched initial states. It is a generic nonlinear, history-dependent response statistic. A nonzero (K_r) does not identify Fe/Li2O contact blocking, an interfacial failure precursor, or a site-specific current partition. Existing bipolar-pulse nonlinear characterization and nonlinear electrochemical spectroscopy already claim the broader measurement class; embedded NVs supply genuinely local magnetic access, but ordinary operando NV readout with the *same four pulse arms* contains every datum needed to compute (K_r). A consequential decision beyond those incumbents is unproven. The most useful rescue is a narrowly defined, validated local *waveform susceptibility* assay, with a same-site crossover gate and an independent chemical/thermal test.

## What the algebra actually isolates

Let the two order means at pulse magnitude (U) produce (C(U)=\mathbb E[y_{+-}(U)-y_{-+}(U)]), and form (K_r=C(rU)-rC(U)). If the waveform shape and initial-state distribution are identical and the entire input-to-field map is linear, (C(rU)=rC(U)). That cancellation is correct, even for an unknown linear memory kernel. For a smooth polarity-symmetric protocol, however,

\[
C(U)=c_1U+c_3U^3+c_5U^5+\cdots,
\qquad K_r=(r^3-r)c_3U^3+(r^5-r)c_5U^5+\cdots.
\]

Thus two amplitudes remove a first-order term but do not isolate a unique third-order chemical mechanism, and at finite amplitudes do not isolate the cubic coefficient. The short-time Lie bracket in S09 is mathematically valid for its assumed dynamics, yet all smooth dissipative stateful mechanisms have vector fields and potentially nonzero brackets. The bracket is not a fingerprint for a hidden contact state. This is directly related to nonlinear electrochemical impedance and bipolar-pulse analysis, which have demonstrated charge-transfer, diffusion, OCV, hysteresis and amplifier contributions to nonlinear responses [Murbach et al. 2018; Kirk et al. 2023; Ernst et al. 2019; Li et al. 2024]. The (+/-) order and amplitude contrast may be a convenient *time-domain projection* of these effects, but not a new source of information compared with the complete pulse and NV time series.

## Exact same-output thermal countermodel

S09's toy model has a hidden even-in-current contact state (z): (\dot x=vu(1-z)), (\dot z=a u^2-bz), (y=kx). Starting from (z=0), its endpoint result is (K_r=2kva(r^3-r)U^3(1-e^{-b\tau})^2/b^2). The following **different physical model produces the identical formula, including the pulse-duration dependence and a persistent local-charge difference after the pulses**:

\[
\dot\theta=a_Tu^2-b\theta,\qquad
\dot x=vu(1-\beta\theta),\qquad y=kx.
\]

Here (\theta) is local temperature above baseline, (a_Tu^2) is Joule heat divided by heat capacity, (b^{-1}) is a cooling time, and temperature changes the fraction of total current entering the magnetic Fe-associated pathway relative to a parallel carbon/SEI/other pathway. Such a temperature dependence can arise from different kinetic activation energies; no contact blocking or damage state is postulated. The two orders have exactly the same ​\(u^2(t)\), so they share a rising temperature trajectory. They apply opposite current signs in opposite thermal order. Substitution gives

\[
C_T(U,\tau)=\frac{2kv\beta a_TU^3}{b^2}(1-e^{-b\tau})^2,
\quad K_{r,T}=(r^3-r)C_T(U,\tau).
\]

Choosing \(\beta a_T=a\) makes *all four post-pulse NV field means' order/amplitude contrast* match S09's toy result for every (U, r, \tau) in the model. Because \(\dot x=0\) at zero current, extending the zero-current NV-read delay does not distinguish these two models. A nonmagnetic-electrode sham also fails: the thermal alternative depends on Fe-associated magnetic current partition and vanishes without Fe. An optical-only heating sham at zero current fails for the same reason; the false positive needs the heat–current interaction. This is a structural identifiability obstruction for the proposed readout, not evidence that thermal coupling has the required magnitude in the proposed specimen.

The thermal alternative is physically serious in this exact apparatus. The embedded-NV primary study says focused laser light heated some electrode locations, uses the NV zero-field splitting as a temperature indicator, and notes that current generates Joule heat [Liu et al. 2024]. The paper's carbon/Fe3O4/PVDF electrode has heterogeneous local conductive paths, and its different NV positions sampled markedly different surroundings. The Fe3O4/Li bulk-magnetometry study used a 3 T field specifically to suppress low-field anisotropy/interparticle-coupling ambiguity in its Fe-particle magnetic interpretation [Li et al. 2021]; Liu's local NV readout used about 89 G. This does not prove a low-field artifact, but it means a fixed-bias local stray-field change cannot be assumed proportional to a unique Fe surface-charge change. Measuring the NV's own temperature helps but does not certify the temperature of each reactive Fe/electrolyte contact around it.

## A thermal-independent nonlinear incumbent can also make cubic (K_r)

Even an isothermal experiment can produce the same leading response through routine nonlinear current partition. Consider two reversible parallel local paths with common overpotential \(\eta\):

\[
j_F=g_F\eta+h_F\eta^3+O(\eta^5),\quad
j_P=g_P\eta+h_P\eta^3+O(\eta^5),\quad u=j_F+j_P.
\]

An odd cubic term is ordinary for a symmetric Butler–Volmer expansion; asymmetric kinetics and concentration dependence create further terms. Invert the total-current relation with (G=g_F+g_P). Then

\[
j_F=\frac{g_F}{G}u+
\frac{h_Fg_P-g_Fh_P}{G^4}u^3+O(u^5)
  =c_1u+c_3u^3+O(u^5).
\]

If a local reversible magnetic/ionic state relaxes as \(\dot q=-bq+j_F\) and NV output is (y=kq), exact two-pulse integration to cubic order gives

\[
C(U,\tau)=-\frac{2k(c_1U+c_3U^3)}{b}(1-e^{-b\tau})^2+O(U^5),
\quad K_r=-\frac{2kc_3(r^3-r)U^3}{b}(1-e^{-b\tau})^2+O(U^5).
\]

This matches S09's cubic amplitude and pulse-duration signature by choosing the physically unconstrained path coefficients. It requires no even-in-current gate (z). A long rest would attenuate this specific (q) model, unlike the thermal model above, but finite-delay measurements alone can be matched, and persistence cannot rule out the thermal model. The calculation is an analytic counterexample, not a fitted specimen or a claim that these path coefficients occur in Fe3O4. The primary NLEIS literature explicitly observes and models nonlinear charge transfer, OCV and diffusion, and the 2024 bipolar-pulsing study measures nonlinear voltage/hysteresis from thousands of pulses in commercial cells; these are credible incumbents for the *type* of signal.

## The proposed location map is not identified by sacrificial lanes

S09 proposes four randomized arms on separate, matched microelectrode lanes because exact resetting of a potentially damaged Fe/Li2O site is not guaranteed. This identifies \(\mathbb E[Y_s]\) for each arm (s\) over a population of lanes, assuming randomization and no interference. It does **not** identify the individual potential-outcome difference (Y_j(+,-)-Y_j(-,+)) for the same buried Fe/NV/contact network (j). Its headline “map of locations where order changes the local magnetic state” is therefore too strong unless each exact location can be measured in a verified reversible within-site crossover. Nominally corresponding image coordinates on two fabricated lanes are different microstructures and different NV-to-Fe distances. Liu et al. observed that some NV diamonds were likely near active material and others near binder/carbon, so this is not a merely statistical nicety.

The proposed lanes also share an optical/thermal environment and, as phrased, one Li half-cell. If they share electrolyte/counter-electrode, a pulse in one lane can alter neighboring ionic concentration, potential and heat; electrical addressability does not guarantee independent potential outcomes. The experiment needs either separately sealed microcells or a measured cross-talk bound with one lane pulsed and the others electrically idle. Otherwise random assignment of four arms within one common electrolyte is not an independent randomized trial. A site-specific claim and a population-average claim should be kept distinct throughout.

## Equal-budget competitors and decision value

The strongest same-information competitor is **the identical embedded-NV apparatus, four pulse arms, all raw ODMR spectra, current/voltage/temperature histories, and the same samples and measurement time**, analyzed as an ordinary operando NV transient with a flexible nonlinear response model. It can calculate (K_r) from those raw means exactly. If (D) denotes all acquired data and (K_r=f(D)), then the best decision based on (D) has no worse achievable expected loss than the best decision based on (K_r). The extra computation is negligible beside optical acquisition and cell fabrication but must be recorded. Thus (K_r) may be a robust predeclared statistic or simplification, yet it cannot give information inaccessible to the equal-access NV incumbent.

A lower-cost competitor uses the same four bipolar current arms, terminal voltage/current/temperature and, where feasible, electrode-resolved voltage, analyzed by established pulse/NLEIS methods. Ernst et al. already used opposite-polarity current pulses of increasing magnitude to measure current–overpotential nonlinearity, and Li et al. characterized nonlinear OCV/hysteresis with bipolar pulses. This electrical competitor will miss genuinely local *magnetic* Fe behavior; the point of embedded NV must be a decision that requires that spatial magnetic variable, not generic detection of nonlinearity. A fair trial should allow the electrical competitor an equal specimen/energy/time budget, and allow the equal-access NV comparator its exact data. Standard low-amplitude linear EIS or a no-sensor CCCV policy is too weak.

The only immediately supported scientific output of a positive (K_r) is: “at this calibrated magnetic site or site population, the two charge-balanced pulse orders give a field response whose amplitude scaling is not linear.” It says nothing by itself about Fe oxidation state, irreversible damage, contact blockage, preferred future waveform, or extra recoverable capacity. One *potentially* useful downstream decision is to choose which pulse order minimizes subsequent site-level Fe conversion mismatch or fade, but that predictive relation has to be shown prospectively. If the thermal twin predicts the same outcome, it is still a possible empirical predictor but no unique new mechanism; if an equal-data NV model performs as well, there is no independent operational advantage.

## Narrow rescue and decisive test

First establish pulse-level reversible resetting in the exact formed Fe/Li2O voltage window. Bulk Li et al. report highly reversible capacitive-like magnetization there, which makes this plausible, but their result does not prove exact reset for an embedded NV site's local structure or heat. On *one registered NV/Fe site*, alternate all four arms in randomized crossover order, separated by an independently checked return of full ODMR spectrum, electrode potential, temperature and local chemical proxy to baseline. If crossover cannot be validated, report only population-average (K_r), not a site map. Use independent electrolyte compartments or bound cross-lane interference experimentally. Record actual current integrals, voltage, cell energy, optical/microwave dose, full multi-orientation ODMR spectra and elapsed scan time; this source demonstrated minute-scale site tracking, not the required pulse-resolution floor.

The mechanism-discriminating intervention is a **thermal factorial on the Fe cell itself**. At fixed electrochemical pulses, alter heat removal or apply calibrated external heating so that the local thermal trajectory is measured and changed; repeat under an isothermal clamp if feasible. Require a joint fit to Fe-site NV thermometry plus a contact-proximate independent thermometer, with uncertainty for the temperature difference between sensor and reactive interface. A nonmagnetic sham or optical-only sham is insufficient. Vary magnetic bias within the calibrated NV range and corroborate the Fe phase/valence/charge state independently on matched sacrificial sites; this checks low-field magnetization/geometry explanations. Test multiple amplitudes and pulse lengths so a cubic small-signal region and higher-order terms can be separated. Any claimed chemical assignment needs the independent chemical result, not a field fit alone.

Finally preregister a *held-out decision*: from a low-dose (K_r) assay, predict either which of two subsequently applied waveform orders reduces site-specific irreversible Fe/Li2O change or which sites will exhibit excess fade after a fixed stress protocol. Compare blinded predictions and full acquisition-inclusive costs with (i) the same-data NV transient/model competitor and (ii) the equal-budget electrical bipolar/NLEIS competitor. If same-site crossover fails, thermal/low-field confounds fully explain (K_r), or (K_r) adds no held-out decision value over the same-data NV model, the proposed operation is a useful contrast at most. If all gates pass, the result would establish a task-specific local susceptibility/prediction protocol. It still would not establish a quantum advantage or priority for the general nonlinear pulse method.

## Primary evidence actually inspected

* [Liu et al., *Operando quantum sensing captures the nanoscale electrochemical evolution in batteries*, Device 2, 100521 (2024)](https://www.iop.cas.cn/xwzx/kydt/202409/P020240924528848148977.pdf): inspected experimental procedures, pages 3–7. Embedded micrometre-scale NV diamond in Fe3O4/carbon/PVDF; approximately 89 G bias; local magnetic maps at selected diamonds; laser-heating caveat; NV temperature sensitivity; different diamonds near active material versus carbon/binder; no pulse-order data or readout-noise bound for this proposed sequence.
* [Li et al., *Extra storage capacity in transition metal oxide lithium-ion batteries revealed by in situ magnetometry*, Nature Materials 20, 76–83 (2021)](https://ciqm.harvard.edu/uploads/2/3/3/4/23349210/li2021.pdf): inspected pages 1–6 and methods. Reported formed Fe/Li2O low-voltage capacitive-like reversible magnetic response. They measured at high field (3 T) to suppress anisotropy/interparticle-coupling alternatives to their magnetic interpretation. This does not calibrate an 89 G local NV field into charge or prove local pulse reset.
* [Murbach, Hu and Schwartz, *Nonlinear Electrochemical Impedance Spectroscopy of Lithium-Ion Batteries: Experimental Approach, Analysis, and Initial Findings*, J. Electrochem. Soc. 165 A2758 (2018)](https://doi.org/10.1149/2.0711811jes): inspected publisher full-text excerpts on measured higher harmonics, Butler–Volmer expansion and galvanostat distortion checks. It provides experimentally grounded generic nonlinear-process and instrument competitors, not Fe-site NV data.
* [Kirk et al., *Nonlinear Electrochemical Impedance Spectroscopy for Lithium-Ion Battery Model Parameterization*, J. Electrochem. Soc. 170 010514 (2023)](https://doi.org/10.1149/1945-7111/acada7): inspected publisher abstract/model summary. Their primary study identifies charge transfer, OCV and nonlinear diffusion contributions to measured NLEIS data; this does not by itself predict (K_r) on Fe/Li2O.
* [Ernst et al., *Capturing the Current-Overpotential Nonlinearity of Lithium-Ion Batteries by NLEIS in Charge and Discharge Direction*, Front. Energy Res. 7, 151 (2019)](https://doi.org/10.3389/fenrg.2019.00151): inspected primary methods: opposite-polarity current pulses, relaxation, rising amplitude and voltage measurements to measure nonlinear overpotential. They do not report this embedded-NV four-arm contrast.
* [Li, Berecibar and Preindl, *Nonlinear Characterization of Lithium-Ion Batteries With Bipolar Pulsing*, IEEE Trans. Ind. Electron. 71, 12983–12990 (2024)](https://doi.org/10.1109/TIE.2024.3352159): inspected [author-hosted full PDF](https://mplab.ee.columbia.edu/sites/mplab.ee.columbia.edu/files/content/Publications/Li-Berecibar-Preindl_2024_Nonlinear_Characterization_of_Lithium-Ion_Batteries_With_Bipolar_Pulsing.pdf), abstract, model and experiment sections. It measured nonlinear voltage/OCV/hysteresis with bipolar pulses in 11 nickel-based commercial cells. It is broad pulse prior art, not the same Fe/NV specimen or exact (K_r).

**Provenance:** all countermodels, potential-outcome argument, and comparator logic are analytic reasoning here. No pulse experiment or material measurement was run. These arguments refute unique interpretation and the individual-site map under sacrificial-lane assignment; they do not prove that a measured (K_r) must be thermal, that NV sensing is useless, or that the exact four-arm statistic lacks historical novelty.
