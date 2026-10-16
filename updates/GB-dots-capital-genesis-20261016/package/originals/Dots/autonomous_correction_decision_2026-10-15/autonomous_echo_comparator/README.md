# Independent audit: missing controlled-memory baseline

## Decision

A physical-qubit spin-echo comparator is constructively available from the **documented optical control graph**. There is no apparent selection-rule obstruction requiring new RF hardware. What is absent is its executed, calibrated, interleaved performance measurement under the same noise, timing, and reporting conventions. The acquired source data cannot rank AQEC against this comparator. Conversely, an ideal echo calculation cannot show that the real comparator beats AQEC.

This is a bounded scientific audit, not a reanalysis asserting an experimental winner. No author outreach, author-code execution, spending, or changes to the acquired evaluator were performed.

## 1. Exact candidate pulse sequence

Let a = |D5/2,m=-1/2>, b = |D5/2,m=+1/2>, and s = |S1/2,m=-1/2>. The v1 Methods, “State preparation and detection,” explicitly use sequential resonant 729 nm drives on s↔a and s↔b to prepare the best physical qubit. Both edges therefore exist on the apparatus. The same article describes phase-coherent optical control. This supports synthesis of the following operation, rather than evidence that it was executed as an echo.

Define R_sj(π,φ)=exp[-iπ(e^{iφ}|s><j|+e^{-iφ}|j><s|)/2]. Use chronological pulses A=R_sa(π,0), B=R_sb(π,0), A=R_sa(π,0). In the basis (a,b,s), their product is

    C = A B A = [[0,-1,0],[-1,0,0],[0,0,-1]].

Thus C restricted to the D qubit is exactly -X; s receives -1. It is not merely a population swap with an untracked relative phase. C²=I in all three levels. For constant edge phases φa and φb, the two transfers are a→-exp[i(φa-φb)]b and b→-exp[-i(φa-φb)]a, a known equatorial π rotation. Phase drifts between the first and last A require explicit calibration; they are not automatically global. Initially empty s is empty again after ideal C, but is populated during C and cannot be ignored in a finite-pulse analysis.

Suggested comparator A: idle–C–idle with equal idle times. The zero-noise target is -X, not I. Either compare process tomography to that known target (equivalently use a declared Pauli frame) or physically undo C and count its duration/error. A phase-frame adjustment that only implements Z is not a physical X undo.

Suggested comparator B, preferable for identity-process accounting: idle L, C, idle 2L, C, idle L. With calibrated composite duration c, total storage wall time T=4L+2c, hence L=(T-2c)/4≥0. Composite centers are at T/4 and 3T/4; the ideal net operation is I. This is a two-refocusing-pulse CPMG-type memory sequence implemented by **six optical π pulses**. In the instantaneous limit its signed idle exposure sums to zero. It is a proposal, not a sequence reported in Li's data.

### Timing that may and may not be counted

One C costs exactly two a-edge π pulses and one b-edge π pulse: c=2t_a+t_b+g, where g is the total necessary within-composite switching/settling time. Two C cost four a-edge and two b-edge π pulses plus the corresponding switching times. These are exact operation counts and conditional timing identities.

V1 reports 20 μs π times for the two pulses preparing the **auxiliary unencoded qubit** (Fig. S1b), then separately identifies the physical-qubit edges (Fig. S1c). It does not unambiguously calibrate both latter edges to 20 μs. Consequently c=60 μs, or six pulses=120 μs, is only an explicitly stipulated equal-speed, zero-switching estimate, not a measured comparator duration or a demonstrated upper bound. Nor should the stated 20 μs **inter-ion addressing** switching time be charged automatically to each same-ion optical-frequency change.

For comparison, v1 gives 620 μs entropy conversion, 90 μs cooling, and 20 μs addressing switching, but the revised archive has t_ms=0.015+3.2255N (ambient) and 0.015+0.7405N (injected). Those storage axes must remain authoritative; the detailed revised pulse schedule has not been reconciled. No total energy, throughput, laser-on-time equivalence, or “same budget” is established merely by these numbers. A credible resource comparison reports wall time, pulse/time/energy budgets, number of ions, reset requirements, and endpoint costs separately. Unused control allowance should not be filled with gratuitous error-inducing pulses.

## 2. What the noise description establishes

V1 Methods “Magnetic field fluctuation” describes Gaussian sampled currents, changing shot-to-shot and updated every 100 ms, with field standard deviation about 16 nT and a stated 10 Hz cutoff. The physical-qubit Gaussian-like decay alone does not identify the temporal correlation process. Update synchronization to state preparation, coil response/filter, correlations between draws, actual waveform, intra-shot update times, and noise during pulses are missing.

In particular, 100 ms zero-order hold is **not a hard 10 Hz low-pass white-noise process**. For independently sampled holds with random uniform offset it has triangular covariance and a sinc-squared spectrum with its first zero at 10 Hz but nonzero sidelobes above 10 Hz. Filtering the coil drive would modify that result. “Shot-to-shot” changes could instead imply that each short storage interval sees one nearly static draw. Those cases can look similar in Ramsey storage while giving different refocusing residuals. They must not be silently identified.

The AQEC cycle durations (about 3.2255 ms or 0.7405 ms) are much shorter than 100 ms. For short hold intervals entirely within a noise plateau, a perfectly instantaneous echo removes the static magnetic phase exactly; AQEC's repeated correction of first-order rotation is a different operation. This observation makes the baseline scientifically important; it does not quantify real echo performance.

## 3. Exact explicitly stipulated comparison model

Assume only for this section: β(t) is the angular-frequency splitting noise of the D qubit, H=β(t)Z/2, with independent Gaussian hold values β_k of mean zero and variance σ², each held for Δ=0.100 s. Pulses are instantaneous ideal inversions; there is no leakage, relaxation, SPAM, ambient noise, or optical control error. The conversion from 16 nT to σ would require the actual magnetic sensitivity and field-waveform calibration; no fitted σ is taken from the archive here.

For an update phase u (time from start to next update), and ideal toggling y(t)=±1, define a_k(u)=∫_[hold k intersect [0,T]] y(t)dt. Conditional on u the exact coherence is

    W(T|u) = exp[-σ² sum_k a_k(u)² / 2].

This formula also covers any number of updates and ideal DD flips. Unknown phase is not a probability distribution: if u is unknown, retain this conditional answer or optimize over u. If an independent **uniform** phase is additionally stipulated, Wbar=Δ^{-1}∫_0^Δ W(T|u)du. Do not assume this uniform law is observed.

For one instantaneous Hahn inversion at T/2 and 0≤T≤Δ, no update during storage gives W=1. An update at u∈(0,T) gives W=exp[-σ² min(u,T-u)²]. Therefore

    Wbar_H = 1 - T/Δ + sqrt(π)/(σΔ) erf(σT/2),
    Fχ,ideal = (1+Wbar_H)/2,

with continuous σ→0 limit Wbar_H=1. The second equality is solely the identity-frame process fidelity of this ideal trace-preserving pure-dephasing channel. It is neither the archive's normalized nor unnormalized tomography convention with leakage.

For small σT, Wbar_H=1-σ²T³/(12Δ)+O(σ⁴T⁵/Δ). For comparison, no-refocusing phase-averaged coherence is

    Wbar_R=(1-T/Δ)exp(-σ²T²/2)
           +(1/Δ)∫_0^T exp[-σ²(u²+(T-u)²)/2]du.

The ideal Hahn model implies Fχ≥1-T/(2Δ) under uniform update phase, irrespective of σ. At 15.5655 ms this is 0.9221725. This is **not** a bound on an experimentally executable finite-pulse comparator and must not be compared to AQEC points as a measured superiority claim. With arbitrary unknown/nonuniform phase even this uniform-phase bound is inapplicable.

At uniform phase the autocovariance is σ² max(1-|τ|/Δ,0), with two-sided angular-frequency PSD σ²Δ sinc²(ωΔ/2). But randomizing the grid offset produces a mixture of conditional Gaussian processes, not generally a jointly Gaussian process. Replacing the exact phase average of exponentials by the exponential of a phase-averaged variance is generally wrong. This is a useful protection against an unqualified universal Gaussian-noise fit.

`model.py` independently implements hold-cell integrals and the exact uniform-phase formula; `model_checks.txt` records analytic-vs-quadrature checks and the explicit swap-matrix verification. Its displayed σ=1000 rad/s is an illustrative input, not fitted or calibrated. It executes no deposited author code.

## 4. Finite pulses: exact formal response, unresolved inputs

The ideal toggling formula cannot simply set y=0 during the optical pulses. Population travels through s, and magnetic detuning does not commute with the driven optical Hamiltonian. Even a constant field can cause imperfect swaps and final leakage.

A complete stipulated three-level finite-pulse comparison model can instead use, in a consistent rotating frame,

    H_j(B)/hbar = B diag(μ_a,μ_b,μ_s)
                 + (Ω_j/2)(exp(iφ_j)|s><j|+h.c.) + D_j,

where μ values are angular magnetic sensitivities, Ω_j and phase are the calibrated drive, and D_j includes drive detunings/light shifts. On each intersection of a constant-noise cell and a square control segment, U_r(B)=exp[-i H_r(B) duration_r/hbar]. Ordered multiplication of **all** idle and pulse segments, splitting any pulse at a noise update, gives U(B_1,...,B_n,u). Shaped pulses require a time-ordered exponential rather than the square-pulse replacement. The exact finite-pulse ensemble map is

    E(ρ)=∫ p(u)du ∫ product_k Normal(B_k;0,σ_B²)dB_k
                  U(B,u) ρ U(B,u)†.

With logical input/output embedding P and ideal qubit target V, its no-renormalization entanglement/process fidelity contribution is E[|Tr(V† P† U P)|²]/4. Leakage remains outside the logical output; postselecting or renormalizing P†UP would change the task. A decay/scattering model requires additional Kraus/Lindblad dynamics, not this unitary integral alone.

This expression is exact for the stated finite-pulse model, but cannot be numerically identified from the archive: Ω_a, Ω_b, switching, pulse envelopes on these edges, optical-phase/laser-noise correlations, AC Stark shifts, error correlations, leakage, and update phase are not supplied as a comparator calibration. Using the QEC pulse error budget as the echo-pulse error model would be unjustified. The S-state excursion additionally makes global optical pumping during the proposed composite dangerous; a memory-only comparator can keep such pumping off. It is not automatically compatible with concurrent dissipative tasks elsewhere.

## 5. Did the acquired experiment already refocus?

No Hahn/spin-echo/DD/refocusing sequence is described in the acquired v1 text or identified in the archive README or source-data labels. The comparison labels are physical, uncorrected logical, and repetitive AQEC. Readout phase compensation for the recovery-induced AC Stark shift is documented, but is not a mid-storage refocusing pulse. This is a bounded negative finding, not proof that undocumented laboratory operations never occurred.

V1 also says ambient data were retained when pre/post magnetic calibrations differed by less than 0.9 nT. This is a calibration-based dataset selection rule distinct from syndrome postselection. **It cannot be attributed to the June 2026 archive without revised methods.** A new matched experiment should report any such selection and apply a declared identical rule across arms.

## 6. Primary-source precedent, without performance transplantation

- Hrmo et al., Nature Communications 14, 2242 (2023), https://www.nature.com/articles/s41467-023-37375-2 : experimentally implements generalized spin-echo permutations using resonant 729 nm π pulses through S/D levels of 40Ca+. This supports optical permutation/refocusing control as established practice, not the fidelity of the proposed Li comparator. It is a gate experiment, not Li's matched memory trial.
- Manovitz et al., PRX Quantum 3, 010347 (2022), https://doi.org/10.1103/PRXQuantum.3.010347 : uses RF-driven D5/2 m↔−m inversions and a four-echo CPMG sequence while qubits are hidden during measurement. This is strontium with explicitly provided RF control; it is not evidence that Li has that RF control. The optical three-pulse construction above avoids importing it.
- Metropolitan-scale ion-photon entanglement via a quantum network node with hybrid multiplexing enhancements (published December 2025; volume 17, 697, 2026), https://www.nature.com/articles/s41467-025-67311-5 : explicitly includes a midpoint spin echo in D5/2 memory coherence measurements. This is corroborating later context, not prior art relative to Li's April 2025 v1 and not a matched benchmark. Its postselected network-storage performance cannot be imported into deterministic Li process fidelity.

Primary Li source: https://arxiv.org/html/2504.16746v1 . Acquired archive: https://doi.org/10.5281/zenodo.20768851 . Local evidence inspected: evaluator README, captured v1 HTML, archive README, Fig4b source rows and file inventory. Author simulation was not run or imported.

## 7. Decisive next measurement and stopping condition

A minimally decisive dataset interleaves physical idle, physical optical echo (one inversion with declared frame or two inversions returning I), and AQEC at identical wall times and injected waveform realizations. Calibrate and publish the three-pulse composite channel at zero and injected noise, including leakage, duration, switching, and optical phases. Preserve all four tomography inputs, raw counts, unconditional results, normalization prescription, and timestamps relative to the noise updates. Use the same ambient-selection rule, if any, and predeclare a useful-fidelity criterion. A modest DD scan can follow with calibrated pulse budgets; it should not be silently optimized on the same test shots.

The audit stops here because the missing object is an executed controlled-memory baseline or a complete comparator calibration, neither reconstructible from these aggregates. Feasible controls plus deliberately slow injected noise make this a substantial missing comparison, while finite-pulse and noise-waveform uncertainty prevent a verdict on which protocol wins.

## Appendix: exact finite-angle ideal recovery and temporal correlations

An independent four-level calculation verifies the finite-angle recovery factor supplied during this audit. Use m=(-3/2,-1/2,+1/2,+3/2),

    L0=(1/2,0,√3/2,0),       L1=(0,√3/2,0,1/2),
    E0=(-√3/2,0,1/2,0),      E1=(0,-1/2,0,√3/2),
    R0=|L0><L0|+|L1><L1|,
    R1=|L0><E0|+|L1><E1|.

The E vectors match the deposited simulation convention; a simultaneous sign reversal of both E vectors leaves the recovery channel unchanged. These are orthonormal code/error bases and R0†R0+R1†R1=I4. For Uθ=exp(−iθSz), the conditional ideal map ∑r Rr Uθ ρ Uθ† Rr† preserves both logical populations and multiplies ρ01=|L0><L1| by

    f(θ)=−exp(3iθ)/8 + 3exp(iθ)/4 + 3exp(−iθ)/8
        =cosθ(1+sin²θ/2) + i sin³θ/2.

One route to this identity is to write the diagonal logical Kraus amplitudes as A00=exp(3iθ/2)/4+3exp(−iθ/2)/4, A11=A00*, B00=(√3/4)[−exp(3iθ/2)+exp(−iθ/2)], B11=−B00*. Then f=A00²−B00². Its modulus satisfies |f|²=1−3sin⁴θ/4. Changing U's sign or using ρ10 conjugates f; there is no discrepancy of physical predictions.

At small θ, f=1+iθ³/2−3θ⁴/8+O(θ⁵). Thus the exact conditional recovery retains a cubic coherent phase as well as a quartic contraction; treating it as only an incoherent phase-flip probability discards information relevant to repeated correlated cycles.

For a fixed angle in every one of n ideal cycles, the coherence is f(θ)^n. If that fixed angle varies between shots, it is E[f(θ)^n]. For independent newly drawn angles every cycle, it is (E[f(θ)])^n. Neither can be substituted for the other on the basis of an averaged one-cycle process matrix. More generally it is E[∏j f(θ_j)], so the joint angle distribution is required. In particular, complete dissipation of the syndrome/motion after each ideal recovery does not reset an external persistent field realization.

For a stipulated zero-mean Gaussian angle with variance v, E[f]=(9/8)exp(−v/2)−(1/8)exp(−9v/2). The persistent-angle n-cycle answer is exactly obtained by expanding the finite Fourier polynomial f^n and replacing each exp(ikθ) with exp(−k²v/2). This is a conditional ideal-operation statement, not an identification of the real process. The ideal identity-process fidelity is [1+Re E(f^n)]/2; the corresponding qubit average state fidelity is [2+Re E(f^n)]/3. These conventions must not be conflated with each other or archive normalization/leakage handling.

The independent `check_ideal_recovery.py` evaluates the full 4×4 Kraus map, checks the factor and modulus on 401 angles, and verifies two fixed-angle cycles. `ideal_recovery_checks.json` reports maximum factor error 1.60×10⁻15. As a nonfitted illustration with angle standard deviation 0.4 rad and n=2, E[f²]=0.9537421813 whereas (E[f])²=0.9558227080. The example establishes noninterchangeability, not the size or direction of a universal experimental advantage.

Read-only inspection of deposited `Extended_data_Fig6.py` confirms the same L/E/R definitions, persistent detuning within each multi-cycle numerical trajectory, and an `exact_AQEC(n)` finite-sum Gaussian analytic expression (with additional preparation/recovery parameters). Its ideal-parameter coefficients −1/8, 3/4, 3/8 and Gaussian characteristic-function terms already encode this static-noise calculation. Its returned 2/3+coherence/3 convention is average fidelity, not Fχ. No novelty is claimed here, and the deposited script has neither been imported nor executed.

This appendix sharpens the original verdict without changing it: in the same purely static, idealized limit, a perfect physical inversion cancels magnetic phase, while finite-angle ideal recovery generally leaves the above residual. Actual optical pulse errors, finite recovery dynamics, and waveform correlations remain unmeasured for the proposed comparator; the ideal comparison does not establish a laboratory winner.
