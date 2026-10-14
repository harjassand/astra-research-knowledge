# S09 follow-up — what the pulse-order NV contrast can and cannot close

15 October 2026, Australia/Brisbane. This tightens [REPORT.md](REPORT.md). **Status: exact algebra and one symbolic countermodel check completed; no pulse/NV/chemical experiment completed.** The operational claim is conditional and narrow: an embedded NV field sensor may make a *specific nonlinear pulse-order contraction* available at a buried Fe3O4/Li interface. The contraction is not a chemical label, a damage forecast, an information advantage over its own raw traces, or a quantum speedup. Its value must be earned by same-electrode chemical validation and a resource-matched nonlinear incumbent.

## Exact cancellation, with the required timing and reset

Choose one galvanostatic template $p(t)=+1$ for $0\leq t<\tau$, $p(t)=-1$ for $\tau\leq t<2\tau$, and $p(t)=0$ thereafter. Its negative, $-p$, is the reversed order. All four arms start at the *same clock phase* after the same formation, target state of charge, open-circuit hold, baseline NV spectrum, and calibration; all are read at the same $T=2\tau+h$, after the same zero-current delay $h$. The acquisition windows, optical/microwave duty, bias field and active/reference sampling order are identical. The amplitudes are $a\in\{1,-1,r,-r\}$, with input **actual measured current** $u_a(t)=aU p(t)$, not merely a command sent to a current source. The $rU$ arms generally carry a greater ohmic burden, but neither dissipated nor net cell energy can be inferred from zero net charge; both are measured and charged to the protocol rather than silently matched by changing the waveform.

Let $Y_T[u]$ be the *noiseless or conditional-mean* map from actual current history to the active-minus-reference, after-minus-before NV field estimate at time $T$. This includes specimen dynamics, optical spin readout, spectral fitting and reference subtraction. Individual photon and specimen-noise realizations need not cancel; their contrast has zero expectation under the hypothesis below. Suppose on the tested domain this full mean map is affine,

\[
Y_T[u]=b_T+L_Tu,
\]

where $L_T$ is **any** linear functional of the input waveform. It may represent arbitrary memory, a spatially heterogeneous linear state-space system, a time-varying instrument *with the same scheduled coefficients in all four arms*, and non-convolutional relaxation. No known response kernel, spectral gap, diagonalization, stationarity or single time constant is assumed. Arm-to-arm drift that changes $L_T$ is a violation, not a canceled nuisance. Then

\[
C(U)=Y_T[Up]-Y_T[-Up]=2U L_Tp,
\quad
K_r(U)=C(rU)-rC(U)=2rU L_Tp-2rU L_Tp=0.
\]

The same proof holds pointwise for an entire trace $Y_t$ at matched times $t$. An active-minus-reference subtraction merely changes $L_T$ if both channels are affine. A nonzero raw $C(U)$ is allowed under a completely linear system; only $K_r$ is the exact affine null. If the true current clips, its rise time changes with amplitude, the initial physical state changes, or the optical fitting map saturates, the hypothesis $Y_T[u]=b_T+L_Tu$ for one common $L_T$ is false and this theorem says nothing about the chemical origin of $K_r$.

Exact within-site resetting is not guaranteed in a conversion electrode. Let $j$ label a lane/site and let $Y_j(a)$ denote its *potential* outcome after one assigned arm from its specified baseline. The individual contrast $K_j=Y_j(r)-Y_j(-r)-rY_j(1)+rY_j(-1)$ cannot be observed by one first exposure on $j$. If sites are randomly assigned to four arms in a predeclared block, the arm-mean estimator is unbiased (over assignment) for the **finite-population mean** $\bar K=J^{-1}\sum_j K_j$, even if each site has its own affine $b_j,L_j$; under sitewise affine behavior $\bar K=0$. Heterogeneity makes the finite estimator noisy. This population result is not a site-resolved $K_j$ map. A site-resolved prospective marker requires repeat exposures after an independently validated restoration gate; otherwise the study may claim only a block-level effect. The initial report's phrase “map of locations” is therefore conditional on this gate.

## Countermodels that survive the affine null

**Sensor saturation alone.** Give a perfectly linear physical plant a field $B_T[Up]=B_0+dU$ and $B_T[-Up]=B_0-dU$. If the fitted optical output is $F(B)$, then

\[
C(U)=F(B_0+dU)-F(B_0-dU)
=2F'(B_0)dU+\tfrac13F'''(B_0)d^3U^3+O(U^5),
\]

so $K_r(U)=\tfrac13(r^3-r)F'''(B_0)d^3U^3+O(U^5)$. For the explicit saturating map $F(B)=B/[1+(B/B_s)^2]$ at $B_0=0$, $K_r=-2(r^3-r)d^3U^3/B_s^2+O(U^5)$, although the specimen is strictly linear. The NV frequency *difference* suppresses common zero-field temperature shift only to the extent that the axial approximation and fitted lines remain valid; it does not establish linearity of the entire fitting chain. Inject calibrated coil fields at the relevant field offsets/amplitudes through the same optics, microwave settings and fitting code, including sham electrodes, and place the observed coil-induced $K_r$ and its uncertainty in the error budget. Record complete ODMR spectra, NV charge-state fraction, linewidth, contrast and orientation-dependent shifts; predeclare a readout-linearity range or abandon the chemical interpretation.

**Even-in-current heat with temperature-gated local current.** The initial report's exact two-state formula is *identically reproduced* by a thermal model. Take $\dot\theta=a u^2-b\theta$, $\dot x=v u(1-\alpha\theta)$, and $y=kx$, with common $\theta(0)=0$. Here $\theta$ is local excess temperature and $x$ is merely charge routed to a magnetic particle, with no damaged contact or interfacial storage state. Direct integration gives

\[
C(U,\tau)=2kv\alpha a U^3\frac{(1-e^{-b\tau})^2}{b^2},
\qquad K_r=(r^3-r)C(U,\tau).
\]

This is the same $U^3$ and $\tau$ law as the proposed hidden-contact toy model. An even-in-$u$ thermometer output $y=\beta\theta$ alone would have zero order contrast when $|u|$ is identical at all instants; the current-partition coupling is what makes heating order-sensitive.

**Pure ohmic heating can produce the same law at the readout.** A stronger countermodel needs no nonlinear charge partition at all. Let a reversible polarization $q$ obey $\dot q=-\lambda q+u$, $q(0)=0$. Let local resistance be $R(q)=R_0+\gamma q>0$ on the small tested range. Over a short pair for which cooling is negligible, $\dot\theta=a u^2R(q)$, and let the recorded field have a thermal coefficient $y=\beta\theta$ (for example, Fe susceptibility changes with temperature, or residual spectral-fit temperature error). For $p=+-$, $q_{-p}(t)=-q_p(t)$, and exact integration gives

\[
\int_0^{2\tau}q_p(t)\,dt
=U\frac{(1-e^{-\lambda\tau})^2}{\lambda^2},
\quad
C(U,\tau)=2\beta a\gamma U^3\frac{(1-e^{-\lambda\tau})^2}{\lambda^2},
\quad K_r=(r^3-r)C(U,\tau).
\]

The $R_0$ term cancels between orders, while the benign state-dependent ohmic term does not. This model exactly mimics the proposed cubic signature and pulse-width shape while reporting heat rather than local chemistry. The thermal, ohmic and sensor-saturation formulas passed the reproducible [SymPy checker](verify_followup.py); these are mathematical counterexamples, not fitted battery models. Finite cooling changes the known integral weight but does not restore chemical identifiability. Required controls are simultaneous actual $I(t),V(t)$ and $\int I(t)V(t)\,dt$, independent local thermometry (not only the NV line used for the magnetic estimate), optical-power titration and laser-off thermal-history shams where feasible, ambient-temperature blocks, and a microheater or optically induced temperature intervention spanning the measured $\theta(t)$ without the electrochemical pulse. An imperfect heat match limits the inference; a fitted $U^3$ law alone cannot pass the gate.

## The strongest nonlinear incumbent already targets this information

If the full map is analytic near the chosen baseline, write its causal Volterra expansion as $Y_T[u]=Y_T[0]+\sum_{n\ge1}H_{n,T}[u,\ldots,u]$, with $H_n$ symmetric $n$-linear forms including the usual $1/n!$ factor. For $p$ above,

\[
C(U)=2\sum_{n\ \mathrm{odd}}U^nH_n[p^{\otimes n}],
\qquad
K_r(U)=2\sum_{n\ge3,\ n\ \mathrm{odd}}(r^n-r)U^nH_n[p^{\otimes n}].
\]

Thus the weak-signal $K_r$ is **one projection of the cubic Volterra kernel**, with fifth and higher odd orders at finite amplitude. It cannot by itself reconstruct a kernel, separate sensor from specimen nonlinearity, or outperform a statistically optimal analysis of the same raw four-arm full trajectories. Nonanalytic hysteresis invalidates the cubic expansion but not the exact affine null. A third-order fit to optimized local NV transient trajectories, including their preparation and readout, is the nearest equally informed incumbent. Battery nonlinear impedance spectroscopy is also substantive prior art: [Murbach, Hu and Schwartz 2018](https://doi.org/10.1149/2.0711811jes) measured second-harmonic lithium-ion cell responses and early-aging sensitivity; [Kirk et al. 2023](https://eprints.soton.ac.uk/495667/1/Kirk_2023_J._Electrochem._Soc._170_010514.pdf) derived and fitted model-based nonlinear impedance contributions and validated time-domain voltage predictions; [a 2020 Volterra-based nonlinear impedance study](https://www.sciencedirect.com/science/article/abs/pii/S0378775320309770) explicitly used Volterra response functions for cell diagnosis. These are terminal electrical measurements, not buried local magnetic readouts, but they defeat any assertion that amplitude-cancelled nonlinearity itself is new.

Two matched comparisons are needed. **Same-data upper comparator:** hand the full $I,V,T$, ODMR spectra, active/reference traces and arm labels to an unrestricted prespecified nonlinear learner/Volterra fit. It can compute $K_r$, so $K_r$ cannot contain more information; a claimed gain can only be finite-sample regularization, interpretability, or measurement-design economy. **Equal-budget different-design comparator:** permit a team using the same NV microscope to optimize ordinary local magnetic transient probes, pulse patterns, integration times and nonlinear regression under exactly the same four-lane/sample count, total current throughput, peak voltage, pulse energy, optical/microwave dose, calibration and elapsed time. Add a terminal-only NLEIS/pulse $I,V,T$ comparator under its own fully counted hardware cost. Do not make EIS-only or a single relaxation fit the straw-man baseline. [Liu et al. 2024](https://www.iop.cas.cn/xwzx/kydt/202409/P020240924528848148977.pdf) established embedded NV magnetic readout during Fe3O4/Li discharge, not this pulse operation, chemical readout, or predictive superiority.

## A closed-loop, same-electrode decision test

**Access and reset gate.** Build independently addressable, registered Fe3O4 composite lanes with embedded active and remote-reference NVs, paired with geometrically matched undoped lanes. Establish a formed low-voltage window in which both amplitude levels, all four order arms and any repeated diagnostic return to the declared electrical and full-ODMR baseline after a fixed rest. Measure current waveform error, voltage compliance, temperature, local optical absorption, inter-lane electrical leakage and lane-to-lane dispersion. A reset claim needs predeclared tolerances for OCV, small-signal response, local spectrum and repeat-dose stability, plus a sham repetition check; these measurements reduce but cannot prove microscopic initial-state equality. If repeatability fails, run a four-arm *randomized first-exposure* population experiment and stop calling $K_r$ a same-site predictor.

**Chemical truth on the measured electrode.** In blocks of four sister lanes, randomize the arms, acquire full local NV trajectories at registered positions, wait the same $h$, and then quench/transfer **those very lanes** under controlled inert conditions for co-registered chemical analysis. Predefine a primary chemical target such as local Fe oxidation-state fraction from Fe K-edge micro-XANES in a fixed window around each sensor, with spatial Fe/Li2O morphology and surface chemistry as secondary outcomes. [A 2019 Fe3O4 cycling study](https://www.nature.com/articles/s41467-019-09931-2) used Fe K-edge XANES and in situ/ex situ TEM to connect lost Fe redox to internal Li2O passivation, establishing the relevance of these chemical endpoints; it did **not** demonstrate micro-XANES co-registration with embedded NVs. That registration, sufficient Fe signal, X-ray dose control and sample-transfer fidelity are experiment gates. Compute the same order/amplitude contrast on the chemical target and test whether block-level $K_r^{\rm NV}$ predicts its sign and size across independently fabricated blocks better than ordinary magnetic transient features and measured thermal/electrical histories. This tests chemical association, not prospective damage, because the diagnostic arms themselves may change the chemistry. If a proposed surface-storage state has no stable Fe-valence signature, the chemical target must be changed and locked **before** outcome collection; it cannot be relabeled after a null result.

**Prospective damage test only after the reset gate.** On a separate cohort, use randomized four-arm cycles at *each* registered site only if the above repeatability gate supports a nondamaging reset. Then apply the same fixed future stress schedule to all sites, blinded to $K_r$. The primary outcome is the change in co-registered Fe oxidation-state response to a standardized state-of-charge step before versus after that stress, with local loss of active Fe connectivity by post-mortem microscopy as a mechanistic check. Randomize diagnostic versus no-diagnostic sham sites to measure any harm caused by acquiring $K_r$. Hold out entire fabricated electrodes/batches when training a prediction rule; splitting neighboring NV pixels from one electrode across train and test would leak material history. If within-site reset is unavailable, a block-level randomized-potential-outcome study remains valid, but there is **no individual-site K-based prospective claim**.

**Decision rule and stop rule.** Freeze the endpoint, waveform, $r,U,\tau,h$, temperature and optical settings, block randomization, feature sets, model-selection procedure and paired held-out score before revealing chemistry. Give each predictor the same prediagnostic resource budget and common measured $I,V,T$. Compare $K_r$-only, ordinary local NV transient features, their combination, a nonlinear/Volterra fit of full local traces, and terminal electrical NLEIS/pulse features. Use a proper held-out error or log score for the chemical target and a confidence interval across *electrodes*, with cost and sensor-induced damage on a separate ledger. A useful $K_r$ result requires calibrated nonzero signal above coil/sham/thermal floors, chemical correspondence on the same electrode, and improvement over an optimized ordinary-transient design at equal total resource. If full same-data nonlinear analysis is equal or better, the defensible outcome is a compact estimator or useful pulse design, not new information access. If heat, saturation, irreversible reset failure, or diagnostic injury explains the effect, the proposed primitive fails its intended interpretation. Finally, test whether a $K_r$-guided subsequent pulse schedule reduces the preregistered chemical degradation/capacity loss versus a schedule chosen by the best incumbent, under equal delivered charge, energy, thermal dose and elapsed sensing time; without that randomized policy comparison, no control benefit has been shown.

The full experiment remains unperformed. No value of $K_r$, sensor noise, reset fidelity, chemical correlation, held-out score, decision benefit or historical priority has been measured or established. Source inspection scope: Liu et al. 2024 full primary PDF apparatus/results/methods; Murbach et al. 2018 online abstract and experimental-method excerpt; Kirk et al. 2023 indexed author-PDF abstract and model summary; the 2020 Volterra study's abstract; and the 2019 Fe3O4 study's online abstract and Fe-XANES result excerpt. The latter two were not independently inspected in full. These sources supply feasibility ingredients and comparators, not evidence that this operation works.
