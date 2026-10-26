# Q95 stage 1: finite interrogation cannot certify the absence of arbitrarily slow relaxation

**The construction is complete, but the intended universal material-characterization capability was not achieved.** The result is a governing theorem, an exact conditional testing operation, and a reproducible numerical comparison. Scientific priority of the derived theorem has not been established. No new material, detector, or experimentally demonstrated capability is claimed.

## Initial question and available operations

Can short, safe mechanical experiments certify a passive material's equilibrium stiffness or eventual flow, without first assuming a finite relaxation model or an upper bound on its memory? Such an operation would support accelerated screening of materials for long-life engineering.

The demonstrated available operations are conventional strain-controlled relaxation and broadband mechanical interrogation, positive-spectrum inference, and temperature-shifted master-curve acquisition in compatible materials. These already have strong incumbents: [nonnegative-spectrum recovery](https://doi.org/10.3390/polym15163464), [optimal Gaussian model-discrimination design](https://doi.org/10.3390/e21040351), and [BOTTS](https://doi.org/10.1039/D4SM00798K). The first proposed passive-continuation route also overlaps directly with [Brown and Grabovsky's established extrapolation theory](https://arxiv.org/html/2401.15178v1).

The missing operation is independently excluding slower modes outside the observed window. A well-fitted or stable finite spectrum does not perform that exclusion.

## Actual claim constructed

For known binary causal linear systems with an entrywise nonnegative response-contrast matrix, independent common Gaussian readout noise, and a fixed peak-input bound, a constant maximum input can **simulate the complete observation/action record of every bounded randomized feedback policy** through a parameter-independent stochastic map. This gives an exact comparison for every decision loss, not a selected score advantage.

The physical instantiation compares a permanent spring of modulus A with a Maxwell element of the same instantaneous modulus and viscosity A/lambda. Both are passive. Their stress contrast under strain u is a positive causal filter:

\[
\delta y(t)=A\lambda\int_0^t e^{-\lambda(t-s)}u(s)ds.
\]

An ordinary step saturates its pointwise envelope AU(1-exp(-lambda t)). The exact optimum classification error, allowing all bounded feedback probes, is

\[
p_*(\lambda,T)=\Phi\!\left[-\frac{AU}{2\sigma}
\sqrt{\int_0^T(1-e^{-\lambda t})^2dt}\right].
\]

Here dY=stress dt+sigma dW defines the readout model. The complete finite-bin and continuous proofs are in `PROOF.md`.

A general consequence follows for all nonnegative relaxation spectra with known instantaneous modulus A but no rate floor. If g denotes equilibrium modulus, then for every finite horizon, finite peak strain and positive detector noise,

\[
\inf_{\text{bounded causal policy},\widehat g}
\sup_{\substack{G(t)=g+\int e^{-\lambda t}d\mu(\lambda)\\
g\ge0,\ \mu\ge0,\ g+\mu((0,\infty))=A}}
\mathbb E_G(\widehat g-g)^2=A^2/4.
\]

The upper bound is the ordinary estimate A/2 without using data. The lower bound uses an arbitrarily slow Maxwell element whose finite observation law approaches that of the permanent spring while its equilibrium modulus remains zero. Thus no representation learner, waveform optimizer or adaptive controller can improve this *uniform* equilibrium-stiffness risk in the stated class. This does not deny useful inference for particular materials or with additional justified structure.

This is the new-to-this-trial scientific statement. Its general degradation mechanism is established comparison-of-experiments theory, and an [explicit adaptive-collapse antecedent](https://arxiv.org/html/2608.22905v1#S2) was found. The constitutive application and exact minimax corollary are derived here; they are not asserted to be new to science merely because an exact title match was absent.

## A positive operation, with its hypothesis exposed

If a separate source establishes that every ambiguous relaxation rate is at least ell>0 and the ambiguous spectral mass is A, the least-favorable material is the single Maxwell mode at ell. A step followed by one matched-filter threshold is exactly minimax optimal across **every** nonnegative spectrum supported above ell, including continuous spectra and any number of components. Its worst-case error is the same p*(ell,T). The proof supplies both the attaining test and the lower bound against all bounded feedback policies.

This is an implementable conditional inference operation. It does not acquire ell, and a fitted minimum rate cannot be substituted for the independent physical premise.

## Executed comparison and stress results

The actual ordinary comparator is the globally optimal step and Gaussian likelihood-ratio test with the same horizon, peak strain, noise density and readouts. It may use the full known pair information. Arbitrary feedback cannot outperform it under the theorem's hypotheses. Simple waveforms are diagnostic alternatives; they are not weak substitutes for the incumbent.

All values below are dimensionless theoretical or simulated results. A numerical strain bound of one means one unit of an independently validated linear-range strain bound, not a physical claim of 100% linear strain.

* All **65,536** saturated 16-bin waveforms were enumerated at lambda=0.2, T=1. The maximum contrast energy was **0.0114966840891**, equal to the ordinary step. Both constant signs attain it. The theorem extends the comparison beyond these vertices and this discretization.
* At lambda=0.1, T=1, noise density 0.02, with 512 readout bins, the exact step error was **0.0821542**. Ramp, sine, chirp and alternating-block errors were respectively **0.293282**, **0.318551**, **0.432231**, and **0.465346**. The table records input exposure, work, dissipation and final stored energy, rather than treating waveform cost as free evidence of an advantage.
* The same bounded feedback policy was simulated directly and by the step-observation simulator, **30,000 trials each**. Errors were **0.2679 ± 0.0050** and **0.26423 ± 0.00499** (Monte Carlo 95% halfwidths). The optimum ordinary step error for those parameters was **0.141725**. The stochastic diagnostic supports the implementation; the proof establishes exact simulation of its law.
* A **1,000-spectrum** mixture check obeyed the exact least-favorable-spectrum error bound. The boundary single mode attains the bound; broad mixtures are easier. Finite examples are not the proof for all spectra.
* For lambda=0.001, T=1 and noise density 0.02, even the continuous-readout optimum error was **0.494244**. The two candidates have equilibrium moduli **1 and 0**. Reaching 5% error requires **23.6443** time units. This correctly permits white-noise averaging to beat waiting a full relaxation time of 1,000, while preserving the unbounded duration as lambda decreases.
* A necessary-hypothesis stress test used two ordinary passive RC filters with a sign-changing impulse contrast. At T=60, the bounded sinusoid gave **39.3186 times** the step's squared output contrast. Passivity alone therefore does not imply the theorem.

The Maxwell passivity ledger closes to 3.5e-15 in the executed check. Explicit causal matrices agree with an independent state recurrence. The final run completed with warnings promoted to errors. Initial matrix-product warnings and their implementation correction are preserved in `RESEARCH_NOTES.md`.

## Consequence, cost and unresolved operation

The adaptive-waveform bridge is decisively blocked **within the defined scalar, linear, common-Gaussian-noise experiment class**. This has broader scope than a failed fixture: a single passive hidden component defeats uniform certification across the entire spectral class. The exact conditional optimum also identifies what information would change the conclusion.

Temperature acceleration was examined as a stronger bridge. Even granting a known compatible finite maximum speedup leaves the same obstruction with a rescaled hidden rate. Compatibility cannot be assumed universally; [thermorheological complexity](https://doi.org/10.1002/polc.5070350106) is an established limitation. Existing successful accelerated rheometry retains its actual regime and value.

The remaining physical operation is a source-supported exclusion of slower hidden modes, or a compatible additional measurement/actuation channel that bypasses the contrast bound. Neither was constructed. The result does not cover nonlinear activation, additional detectors, model-dependent fluctuation noise, or a different physical observable. A new primitive would need its own evidence and matched resource comparison.

The experiment model grants initial equilibration, free computation and ideal strain control. It counts peak strain, duration, readout count/noise, strain-squared exposure, and model-specific mechanical work/dissipation. It does not provide a measured preparation, reset, thermal-cycle or apparatus-calibration cost. No physical speedup is claimed, so these omitted physical costs are not hidden in a reported capability gain. No civilisation-changing advance is asserted.

## Reproduce and inspect

Run `/usr/local/bin/python3 -W error experiment.py` in this directory. It writes `results.json`, `RUN_OUTPUT.txt`, `waveform_comparison.csv`, `detection_duration.csv`, and `research_figure.png`/`.pdf`. The seed and runtime versions are recorded. The code makes no network calls. `SOURCES.md` records exact primary URLs and what was inspected; `RESEARCH_NOTES.md` preserves the substantive pivots and unresolved operation.
