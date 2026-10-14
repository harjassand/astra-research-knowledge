# Physically obtainable pivot: resonance-check, dark park, then emit

**Status.** This is an independent literature-based operation audit and a new analytic calculation, not a device experiment. The strongest physically demonstrated pivot screened here is a T-center resonance-check sequence followed by a genuinely dark hold and a later probe/output attempt. It can replace blind frequency redraw with observed, conditional state preparation. It does **not** demonstrate that a state-dependent correlated reset repairs the 9801 rate-selectivity gate, and it does not demonstrate pairwise indistinguishable output or a network-level speedup. In the selected study, the 110 MHz linewidth and the 1.5 ms retention evidence were obtained at different laser powers and different conditional linewidths.

## Comparator screen and selection

Three demonstrated material/operation paths were screened before selecting one operation.

| Candidate | What the primary study measured | Why it is or is not the selected operation |
|---|---|---|
| Above-band charge reset in p-i-n T-center waveguides | Across 46 emitters, median PLE linewidth changed from 1.99 GHz to 0.57(11) GHz (3.5-fold); selected best line 128(22) MHz; coherent Rabi oscillations with 20(2) ns coherence. The reset charge configuration was stable for 4–100 microseconds in one delay series. | Strong unheralded reset prior, but not a frequency-selective pair-alignment protocol. The probe repolarizes the environment; the observed field recovery has a 7.5(2) microsecond time constant and is only about halfway to steady state by the 20-microsecond measurement endpoint. No pair output was tested. This is not an Astra novelty. ([arXiv:2608.15993v1](https://arxiv.org/html/2608.15993v1)) |
| **Resonance-check → dark park → probe/output** | On one cavity-coupled T-center, a photon click during a check at the desired frequency conditions later PLE to 110(10) MHz at the lowest check/probe powers; the probe-pulse click rate is 6× the unconditioned PLE rate. A separate dark-hold series reports no significant broadening to 1.5 ms at a 1.2(1) GHz conditional line. | **Selected.** It is a real, state-aware measurement/intervention that avoids pretending an emitter is protected while illuminated: a detected photon heralds the state, after which the lasers are off. Its retention is empirical. However, the narrowest and longest-retained regimes have not been joined in one matched run, and the study did not measure two-emitter interference or a useful entangled output. ([arXiv:2504.09908v2](https://arxiv.org/html/2504.09908v2), §§ I.2, SVI–SVII) |
| Al2O3 surface passivation | An 11 nm layer was reported as the best tested thickness; four same-emitter comparisons averaged a 32% narrowing, with a maximum of 57%. | Persistent material improvement without repeated heralding overhead is a relevant conventional route. It is a separate preprint/material setup, not a matched control against either selected RC-PLE or AB reset. ([arXiv:2608.09904v2](https://arxiv.org/abs/2608.09904v2)) |

I selected the resonance-check operation because it provides the strongest demonstrated combination of *target selection* and *measured retention*, rather than because it has established end-to-end advantage. The above-band reset is an unheralded environment-reset method, but its successful linewidth result is not a state-selective reset transition matrix. Surface treatment is a strong low-per-shot-cost comparator, not a same-device baseline.

## Exact answer to the 9801 gate

Let `O` denote an emitter outside a target spectral interval and `T` an emitter inside it. Suppose attempts occur with state-dependent rates `r_o` and `r_i`, and the conditional probabilities of switching states on an attempt are

- `a = Pr(O → T | an outside-state attempt)`;
- `b = Pr(T → O | a target-state attempt)`.

For a two-state continuous-time Markov model with these constant conditional hazards, target occupancy `p(t)` obeys

\[
\dot p = r_o a(1-p)-r_i b p,
\qquad
p_\infty=\frac{r_o a}{r_o a+r_i b}.
\]

Therefore the necessary and sufficient rate condition for `p∞ ≥ p*` in this model is

\[
\frac{r_o}{r_i}\geq\frac{p^*}{1-p^*}\frac{b}{a}.
\]

For an iid redraw into a target window with probability `q=0.01`, `a=q` and `b=1-q`. Taking `p*=0.99` gives

\[
\frac{r_o}{r_i}\geq\frac{0.99}{0.01}\frac{0.99}{0.01}=9801.
\]

This is exact algebra for the stated model, not an experimental rate measurement. If microscopic reset events are correlated but their state-conditioned transition rows remain `a=q`, `b=1-q`, those correlations do not lower the required 9801 rate ratio; with equal attempt rates they leave single-emitter occupancy at `q`. Correlations between two emitters may change joint success probabilities, but cannot be credited as single-emitter gate repair without measuring their joint law and marginals.

At equal attempt rates, state-dependent transitions repair the gate only if `a/b ≥ 99`. If the incoming transition remains `a=0.01`, then `b ≤ 1/9900`: the target state must survive at least `9899/9900 = 99.9899%` of such attempts. With zero observed exits, at least 29,657 independent target-state attempts are needed for the one-sided 95% binomial upper bound to reach that failure probability. This count assumes iid trials; repeated cycles on the same evolving emitter require clustered uncertainty and history controls. No cited study reports `a` and `b` for reset from both initialized states, much less a pairwise correlated reset kernel meeting this threshold. The exact calculation and its assumptions are in [`derive_gate.py`](derive_gate.py).

Thus, **the investigated RC-PLE operation bypasses rather than repairs the 9801 reset gate**. It observes a photon that certifies alignment, pays for that heralding attempt, and then parks the configuration in the dark. The cited work offers no evidence that an above-band reset causes the required state-conditioned asymmetry. The separate charge-reset result measures average linewidth after reset, which is not an estimate of `a`, `b`, or the 9801 ratio.

## What the selected operation actually did

The RC-PLE study excites T-center II at a chosen check frequency until a photon is detected. That click heralds resonance with the check laser. A target-frequency probe pulse follows after delay `τ`; the authors scan the probe to estimate the conditional line. At 0.4 K, their lowest-power values were `P_check=0.016 P_sat`, `P_probe=0.008 P_sat`, and the measured conditioned linewidth was 110(10) MHz—35-fold narrower than the raw PLE line of 3.8(0.1) GHz. The detected photon probability per probe pulse rose sixfold versus ordinary PLE. These are measured conditional-spectrum and relative probe-count results, not a two-emitter Hong–Ou–Mandel result or an entanglement rate.

The hold-time evidence comes from a separate series on the same T-center II at 0.27 K. To raise the count rate, the check and probe powers were increased to 0.19 and 0.11 `P_sat`. The conditional line then started at 1.2(1) GHz, and no statistically significant broadening was observed through 1.5 ms of dark wait; 200–500 MHz broadening appeared around 2.5–3.0 ms. **The 110 MHz linewidth has not been demonstrated at that 1.5 ms hold.** The retention claim is directly measured in the specified higher-power regime, so this report does not invoke a protected dark state as an assumption. The operation is dark during the park; illumination during a hold is a different intervention.

A different T-center check-probe study reports no dark-wait spectral diffusion through 3 ms, using the conditional click rate as a stability proxy. This is independent support for dark storage as a real effect, but it is a different measurement/device condition and still does not join the 110 MHz low-power line to the 1.5 ms RC-PLE regime above. ([arXiv:2504.08898v2](https://arxiv.org/html/2504.08898v2), check-probe results)

This distinction matters because the primary off-resonant perturbation study reports spectral diffusion even when the perturb laser is detuned by −5.1 or +5.95 GHz, chosen to avoid exciting the heralded T-center and sitting inside the 17.9 GHz cavity linewidth. In a sequence of 200 ns perturb pulses separated by 2.5 microseconds, the conditional line broadened from 1.16 to 2.98 GHz between zero and nine perturb pulses. The effect tracked the resonant perturbation trend, consistent with nearby charge-environment reconfiguration rather than T-center excitation being the dominant cause. So “optically dark emitter” is not sufficient if the environment is still exposed to off-resonant light. Conversely, the empirical dark-hold result supports a laser-off park for the measured interval. ([arXiv:2504.08898v2](https://arxiv.org/html/2504.08898v2), perturbation results and discussion)

The independent above-band reset study is also informative about noise, duration, and work. It uses a 640 nm pulse train in 220 nm SOI p-i-n waveguides at 15 mK. The authors infer a median charge-noise field spread `σ_E=25.3 kV/m` (16–84% range 18.7–33.1 kV/m), with its absolute scale carrying a bulk-Stark calibration systematic. The unattenuated reset pulse is 39 ns at 0.33 mW incident at the device, or 12.87 pJ per pulse; the five-pulse time-resolved recovery sequence therefore injects 64.35 pJ of reset-light energy at the device before adding the 300 ns, 100 microW PLE probe (30 pJ incident) and readout. Those are optical pulse energies at the device, not electrical wall-plug or refrigerator energy. The authors report a 4–100 microsecond dark stability window for the reset state, while resonant probing repolarizes the environment; in one emitter the field recovery time constant was 7.5(2) microseconds and the field reached only about half its final value by the 20 microsecond observation limit. The reset narrowed across an emitter cohort but did not establish stable mutual resonance or usable multi-emitter photons. ([arXiv:2608.15993v1](https://arxiv.org/html/2608.15993v1), §§ 4, 6–7)

## Work, reliability, and the matched conventional baseline

The strongest same-emitter baseline is conventional PLE on T-center II: 3.8(0.1) GHz raw width versus 110(10) MHz after the low-power check. The measured 6× increase is a relative probability per probe pulse, not an absolute per-attempt herald probability or a complete time/energy budget. The RC experiment reports `P_sat=1.3(0.1) µW` and a 100 ns check pulse. Applying its 0.016 setting and the reported 50% grating coupling gives an estimated 1.04 fJ incident on the device per check pulse; the 0.008 probe corresponds to 0.52 fJ. These estimates exclude laser wall power, collection losses, SNSPD/detection efficiency, refrigerator load, and all failed check pulses. The check is repeated until a click, so an absolute acquisition cost cannot be recovered without the detector/excitation probability and cycle timing. The low-power setting also lacks the pulse repetition-to-output and spin-error data needed to call the 6× figure an end-to-end usable-photon rate.

The published parallel preparation model can be scoped for a two-emitter comparison. It assumes independent emitters and geometric check attempts, with per-check success

\[
p_{\rm check}=\eta_{SD}\eta_{det}\eta_{exc},
\]

where `ηSD=Γhom/Γraw`. The paper's derivation assumes unit excitation efficiency for its ideal π-pulse; it notes that imperfect excitation multiplies the success factor. Its low-power holeburning width is 64(3) MHz, from which the authors estimate `Γhom≈32 MHz` as half the holeburning width. Using that estimate with `Γraw=3.8 GHz` and low-power RC width 0.11 GHz gives `ηSD≈0.008421` and a linewidth gain `g=Γraw/ΓRC≈34.545`. For two independent emitters the expected parallel number of check rounds is

\[
E[T]=E[\max(X_1,X_2)]=\frac{2}{p}-\frac{1}{2p-p^2},
\]

and the paper's modeled speedup is `g²/(1+E[T])`. Under those central values, model speedup exceeds one only when the unmeasured product `ηdet ηexc` is at least about 0.149. At 0.10 the reconstructed speedup is about 0.67; at 0.20 it is about 1.34. This is a reproduction of a model form with measured linewidth inputs and **unknown** detection/excitation inputs, not a measured speedup. The paper's model does not include an observed pairwise output, non-independent emitter drift, detector dead time, spin-flip error during checks, total prep latency, or wall-plug and cryogenic costs.

Reliability is therefore established at only the conditional PLE/readout level: a check click predicts a narrow subsequent probe spectrum in its measured window, and separate dark holding preserves a broader conditioned line for 1.5 ms. The experiment does not report the unconditional probability that two emitters jointly produce an interfering output photon within that window, so network success and scaling remain unknown. At larger `N`, the authors' independent-emitter model predicts `E[T]` grows logarithmically while the linewidth-gain numerator grows exponentially; that asymptotic model statement should not be read as a measured scaling law for coupled devices.

## Decisive experiment and failure criteria

The smallest experiment that could validate this pivot is a same-device, two-emitter, blinded/interleaved comparison on a platform where both emitters have calibrated check probabilities and output channels.

1. Map the no-check PLE line, homogeneous linewidth, saturation power, detector efficiency, excitation probability, spin state, and pulse-cycle timing for both emitters. Keep the source's actual temperature and optical-power calibration explicit. Retain all candidates and failures rather than selecting only unusually narrow lines.
2. Randomize repeated runs among (i) conventional PLE, (ii) the published low-power resonance-check sequence at 0.016/0.008 `P_sat`, (iii) the higher-power check condition used for retention, (iv) check followed by the laser-off hold and target output pulse, (v) an otherwise identical off-resonant perturb control near ±5 GHz, and (vi) an optical-dose-matched timing control. Record click/no-click, every pulse, elapsed cycle time, detector dead time, emitted and detected output, and all calibration uncertainty.
3. Measure conditional linewidth and output-photon spectrum at several delays through 1.5 ms for both the low-power 110 MHz condition and the high-power 1.2 GHz condition. This directly tests the missing regime crossing. The dark condition must be literally laser-off; off-resonant perturb is a separate control, not a substitute for darkness.
4. For a useful-output claim, interfere the two accepted output photons and report the indistinguishability/HOM visibility, heralded pair probability per wall-clock and per excitation attempt, rejected-run count, and spin/charge readout errors. Compare to conventional PLE with the same emitter pair, elapsed time, optical energy at the sample, detector and cryostat boundaries, and target output requirement.
5. If testing the reset-repair hypothesis separately, initialize the same emitters both inside and outside the target interval, apply the identical candidate reset, and estimate the transition matrix `(a,b)` with a readout-backaction calibration and emitter-clustered confidence intervals. At equal rates the measured gate condition is `a/b≥99`. A null exit count alone is not enough unless the independent-event assumption is justified; with iid trials and `a=0.01`, the 95% one-sided target is at least 29,657 target-conditioned reset events without an exit.

**Pass criterion for the selected operation:** in the same setup and at the same check/probe powers, the target frequency remains within the predeclared acceptance bandwidth across the required hold, and the paired emitted photons achieve a predeclared interference threshold while the complete attempt and energy costs beat the matched PLE baseline. Failure to retain the 110 MHz condition through the required delay, or failure to improve useful pair yield after counting all check attempts, rejects the claimed advantage. A positive state-conditioned transition ratio would be a separate finding; it cannot be inferred from RC-PLE retention.

## Scope and novelty limit

Resonance-check spectroscopy and dark storage are existing published T-center methods. The result here is the comparison and exact gate audit, not a new optical reset, protected-state mechanism, detector, or experimental observation. The low-power linewidth and higher-power retention are separate measurements; photon-count gain is not paired entanglement; surface passivation and AB reset are prior comparators; input, acquisition, and system-energy costs are incomplete. A defensible conclusion is therefore: **a real, experimentally grounded route exists to avoid the iid redraw gate by conditioning on a detected target-frequency event and then holding in the measured dark window, but present evidence does not establish retained 110 MHz pair output, 9801-gate repair, or an end-to-end advantage.**
