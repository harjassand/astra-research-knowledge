# Physical-learning priority check

24 October 2026. Bounded primary-source check of the frozen one-copy oscillatory-nudge / synchronous local-correlation proposal. This is a mechanism-priority note, not a novelty clearance.

## Finding

The proposed local rule is already conventional at the algorithmic level. No source in this bounded check reports a bench experiment that combines one reciprocal resistor network, sinusoidal teacher-error injection, local squared-edge-voltage lock-in, and physically retained conductance updates. But the key operation and its local gradient identity are in the established Frequency Propagation work, and a 2026 Lock-in Equilibrium Propagation paper explicitly derives a one-copy continuous cosine probe with local synchronous Hebbian demodulation. Therefore the broad “new single-copy oscillatory physical-learning rule” claim should be retired. What remains unacquired is a particular resistor-level circuit implementation and its complete-cycle error, noise, latency, and energy accounting.

## Direct predecessor already supplied by the parent

Anisetti, Kandala, Scellier, and Schwarz, “Frequency Propagation: Multi-mechanism Learning in Nonlinear Physical Networks,” *Neural Computation* 36(4), 596–620 (2024), [DOI](https://doi.org/10.1162/neco_a_01648), [author manuscript](https://arxiv.org/abs/2208.08862).

For reciprocal resistive networks with energy containing

\[
E(\theta,x,v)=E_{\rm input}+E_{\rm nonlinear}+
\sum_{(j,k)}\tfrac12\theta_{jk}(v_j-v_k)^2,
\]

the paper injects an output-boundary current \(i(t)=\gamma\sin(\omega t)\,\partial C/\partial v(v,y)\), and defines nodewise DC and sine coefficients \(a_j=T^{-1}\int_0^T v_j(t)dt\) and \(b_j=2T^{-1}\int_0^T v_j(t)\sin(\omega t)dt\). Its local update is

\[
\Delta\theta_{jk}=-\alpha(b_j-b_k)(a_j-a_k)
=-\alpha\gamma\,\partial\mathcal L/\partial\theta_{jk}+O(\gamma^3).
\]

For an edge waveform \(v_e(t)=a_e+b_e\sin(\omega t)+O(\gamma^2)\), this is precisely the same cross-correlation as square-and-lock-in detection:

\[
\langle v_e(t)^2\sin(\omega t)\rangle_T=a_e b_e+O(\gamma^3).
\]

Thus using a local squarer and reference mixer instead of separately extracting and multiplying the two Fourier coefficients changes the detector implementation, not the learning signal. The paper assumes the network relaxes much faster than the probe period (\(\tau_{\rm relax}\ll T\)); it also requires observation over at least a period, conductance control, and synchronized phase reference for the sinusoidal coefficient. It presents the method as a candidate for in-situ realization, not as a measured conductance-training experiment.

## Three bounded source checks

1. Tammali and Olin-Ammentorp, [“Lock-in EP: An In-Situ Training Algorithm for Oscillatory Hardware”](https://arxiv.org/abs/2610.07283), arXiv:2610.07283 (5 October 2026). The paper continuously varies the output-cost nudge as \(\beta(t)=\varepsilon\cos(\omega_p t)\), then synchronously demodulates a local inter-layer Hebbian product. Its stated rule is \(\partial\mathcal L/\partial W_\ell=-2\langle\operatorname{Re}(z_\ell z_{\ell-1}^H)\cos(\omega_pt)\rangle_T/\varepsilon+O(\varepsilon^2)+O((\omega_p/\kappa)^2)\). This is the closest direct one-copy/lock-in interface, though its local observable is phase alignment, not squared resistor voltage. Assumptions include symmetric feedback, a stable non-degenerate free equilibrium, small probe staying in one basin, warm-up longer than the relaxation time, integer probe periods, and the adiabatic regime \(\omega_p\ll\kappa\). The reported Fashion-MNIST (784–256–64) accuracy and impairment-recovery results are software simulations; weights are updated by an outer SGD loop. The authors say experimental proof, physical realization of the global probe, and energy characterization remain open. It does not show conductance programming or physical acquisition.

2. Kim et al., [“Perturbative Contrastive Physical Learning”](https://arxiv.org/abs/2606.09756), arXiv:2606.09756 (8 June 2026). This paper explicitly names Frequency Propagation as a sinusoidally driven, frequency-demodulated contrast method, and presents it as a special case of its broader perturb-and-contrast framework. Its Mode B examples use a finite-difference Jacobian and externally computed pseudoinverse/Gauss–Newton update. The spring and continuous-variable optical examples are model-level demonstrations in the paper: the optical example specifies a four-mode Gaussian circuit, x-quadrature readout, finite-difference probes, classical post-processing, clipping, and an idealized beam-splitter multiplier/updater. I found no bench device readout or retained physical parameter update in the report. The framework therefore strengthens the conceptual-priority result, but does not close the acquisition gap for an autonomous resistor network.

3. Dillavou et al., [“Demonstration of Decentralized, Physics-Driven Learning”](https://doi.org/10.1103/PhysRevApplied.18.014040), *Physical Review Applied* 18, 014040 (2022), [author manuscript](https://arxiv.org/abs/2108.00275). This is the closest decisive real learning circuit in this bounded set. It physically trained a 16-edge variable-resistor network using a paired free and clamped copy; digital variable resistors had 128 states. Each edge’s integrated comparator compared the two local voltage-drop magnitudes and applied the same signed resistance step to both copies. The underlying rule is a voltage-square contrast, \(\Delta R_i\propto R_i^{-2}([\Delta V_i^C]^2-[\Delta V_i^F]^2)\), but the implemented circuit approximates it by the sign of \(|\Delta V_i^C|-|\Delta V_i^F|\), not an analog square/mixer. The supervisor supplies the clamped output \(V_C^O=\eta V_D+(1-\eta)V_F^O\); hence the free-output measurement/teacher construction remains boundary-side work. Measured comparison noise dominates for voltage differences below roughly 0.01 V; the apparatus limited update examples to 3–5 Hz. Resistor settings persist and were not reset between tasks; a later inference phase freezes the learning degrees of freedom. The paper describes clamping as higher-power than free operation and deliberately biases drift away from high-power solutions, but gives no full-cycle energy or energy-per-update accounting.

## Boundary for the frozen proposal

The square/mixer identity is mathematically the same local coefficient product used by Frequency Propagation, and Lock-in EP confirms the one-copy periodic-nudge/lock-in pattern in another physical model. The physical discriminator is therefore acquisition engineering: whether one reciprocal resistor network plus actual local squarer/mixer/integrator cells, an output-error driver, calibration/hold circuitry, and realistic settling/noise can retain useful conductance changes at a total cost that beats an equally resourced conventional learner. The existing coupled-learning apparatus proves real physical adaptation but relies on two simultaneous copies and a comparator-sign rule. None of these sources establishes an energy advantage or the proposed one-copy circuit’s measured operation. No absence-based novelty conclusion is made.
