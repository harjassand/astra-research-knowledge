# Independent finite-LO / finite-counter bus receiver audit

**Decision: ACCEPT the qualified declared finite optical instrument and exact grid, not an acquired detector.** The two qualifications below are controlling. The ideal-quadrature warm-apparatus theorem is not inherited. No new cancellation principle, hardware feasibility or architectural advantage is established.

Audit directory: `finite_lo_independent_audit_20261031_2307UTC`.
Original nine-file manifest SHA-256: `4c72c3356d10c4e4a3e2b8cc77663875efcf94b049a1822767174b2057fea321`.
Main proof SHA-256: `644b172cf3c5e0cf5269400f5afa479ca5acac18cd225c4e88baf344228ee923`.
Root candidate SHA-256: `1afefa1ad8bffd4f9a922e7a562ac0c8a437ccaca61ab2b049e8fcfd59f3581b`.
Controlling addendum SHA-256: `5b7d67e92e6030a6ed46673562bc796012469a5d6c5922997a4b7f1e9bbea8c0`.
Accepted qualified binding SHA-256: `3d9d17b547d4f090e154f544df8cb13b54ff3316fdc4312df984e946fca41968`.

All nine original files were byte/length authenticated before copying and rechecked unchanged at completion. The imported accepted bus certifier and certificate match their original bytes; the accepted gate's six-file manifest and controlling qualified binding `3ea9c10a2626b8f0d99edf89f662a3378d50ca8729a03b23003fb98a47f72a86` were also reverified. This is a new receiver audit, not inherited approval of a different measurement instrument.

## 1. Qualifications found and independently accepted

### End-to-end correction precision

The frozen table commands are rounded numerical approximations to the exact wrapped angle. A physical actuator tolerance of 1e-6 radians **relative only to the rounded command** does not by itself justify the grid's 4e-6 complete-error term. The table error must also be counted.

The controlling addendum correctly makes 1e-6 the **end-to-end per-qubit angle tolerance against the exact ideal wrapped correction**, including table computation. Its sufficient split, table error <=1e-8 plus actuator error <=0.99e-6, is sound. Actual certified maximum table errors are much smaller: below **4.982e-10** radians across the grid; at LO4, **4.6964324012e-10**. If actuator error were instead 1e-6 relative to the command, LO4 would need an extra at most **1.8785729605e-9** complete-error charge using the exact table bound, or the addendum's conservative **4e-8**. The original grid is accepted under the end-to-end specification, not by dropping this term. All rounded commands have ample margin within the stated pi/(2 tau_Z) strength envelope even with the admitted error.

### Detector misassignment is not arbitrary optical-instrument error

The 2 epsilon_num statement is accepted for classical mislabeling after the declared number measurement, or an explicitly received bad-event CP coupling whose probability is uniform on the admitted data/reference family. It is not established by a Fock-state confusion matrix alone.

An independent counterexample confirms this distinction: rotate a two-number-state measurement basis by an angle with sin^2(angle)=1e-4. Each number eigenstate is misclassified with probability 1e-4, but on a coherent superposition the measurement-channel trace-distance lower bound is approximately **0.019999**, not <=0.0002. Coherent POVM errors can therefore scale as the square root of a calibration misclassification probability. The controlling addendum correctly retains the supplied 0.001 as a *complete-operation* allowance rather than deriving it from such a confusion matrix.

## 2. Exact finite optical instrument

Appending a finite coherent LO, balanced mixing and measuring both number outcomes gives precisely the stated diagonal Kraus amplitudes. With real signal bA and imaginary LO iL, the phases of the two output amplitudes are `pi/2-atan(bA/L)` and its negative. For b=-2,0,2, `atan(bA/L)=b atan(2A/L)/2` exactly. Consequently the count-difference correction is a product of two local Z rotations. The unobservable count-dependent global phase does not affect any data/reference channel.

After correction each conditional amplitude is positive. Summing the two independent exponential series gives the Hellinger kernel

`exp[-(sqrt(n_LO+b^2 S)-sqrt(n_LO+c^2 S))^2/2]`.

Thus the +/-2 coherence is preserved by the collected receiver, but the zero-to-extreme coherence loses a factor v<1 at finite nonzero signal and finite LO. This is real remaining B^2 information, not an omitted phase or a hidden infinite-LO approximation. The LO resource is a finite **mean** photon number, not a hard maximum photon count.

The special phase linearity is not true for additional general B eigenvalues. Nor does it apply to arbitrary displaced warm/nonclassical signal states: their count amplitudes are not the stipulated coherent amplitudes. An independent two-mode quantum beam-splitter evolution, using the Fock-space unitary rather than replacing it by classical amplitude algebra, reproduced the vacuum kernel. Replacing the initial signal vacuum by one photon changed the corrected kernel by Frobenius norm **0.217604** in the same diagnostic setup. This is a finite-cutoff diagnostic supporting the explicit noninheritance boundary; the analytic coherent-state sums provide the actual theorem.

## 3. Unequal efficiencies and all lost modes

For constant, real, mode-independent attenuation in the two output arms, the observed count phases are unchanged. The observed magnitude kernel depends on the average efficiency through S=eta_bar A0^2 and n_LO=eta_bar L0^2. Direct overlap of both unobserved coherent fields gives real lost-signal distinguishability `(1-eta_bar)A0^2` and imaginary phase

`+ A0 L0 (eta_plus-eta_minus)(b-c)/2`.

The stated negative local-B correction cancels this phase with the correct sign. Independent checks included unequal .4/.9 efficiency, a completely lost arm, .999/.997, and the historical .274/.354 pair. The largest numerical kernel discrepancy was below 1.4e-15.

This receiving does not cover mode-dependent attenuation, arbitrary optical phase shifts, drifting imbalance, dark counts, detector backaction or nonvacuum loss ports. Their actual instruments are additional inputs. The numerical grid uses equal .999 efficiency; unequal-efficiency phase calibration is not silently assumed paid by that grid. The inherited filter's unobserved signal modes and endpoint storage are already included in ell. LO loss introduces no additional real signal distinguishability beyond the received overlap, but unequal loss introduces the calibrated phase above.

## 4. Complete error and minimax scope

The corrected three-sector kernel has adjacent t=exp(-2ell)v and extreme d=exp(-8ell). It is a positive correlation matrix. The previously reviewed weighted-Schur/eigenvalue argument therefore applies unchanged with w=1-t and q=1-d: the exact diamond distance is q when q>=2w and `4w^2/(4w-q)` otherwise. Multiplicity of the zero eigenspace does not alter it. Independent explicit maximizing inputs attain the formula, and arbitrary-reference checks obey it.

The old lost-extreme-pair Bell-negativity lower bound applies even after adding an independent LO and arbitrary accessible-field/data processing. Hence the ideal unbounded-count finite-LO receiver is minimax when its actual interval-certified condition `2t>=1+d` holds. In this grid that condition holds at LO13 and LO16, not LO4. Their **finite-cap** implementation has the additional overflow receiving term and is not claimed to attain that ideal-counter minimax. At zero inaccessible energy the finite-LO receiver retains nonzero B^2 information and generally does not implement perfect erasure.

## 5. Finite count cap and uniform CP receiving

Conditioned on a B eigenbranch, the two counts are independent Poisson variables with total mean `n_LO+b^2 S`, including unequal constant efficiencies after using the observed parameters. On any data/reference input, the overflow effect is diagonal in B and its probability is bounded by the extreme-branch tail at `lambda_max=n_LO+4S`.

The root falling-factorial bound is valid. The sharper certificate bound is also valid: after the first tail term at M+1 the term ratios are at most lambda_max/(M+2)<1, giving the displayed geometric sum. Exact dyadic intervals enclose it; clipping an upper bound at one is safe.

For the declared number instrument with arbitrary trace-preserving fallback only on overflow, the ideal and fallback bad-outcome maps are CP with diamond norms at most p_over each. Thus their difference is at most **2 p_over**, including arbitrary references. No square-root probability penalty or postselection normalization is needed. With total cap20 there are 231 resolved low-total pairs and one coarse overflow alternative; only 41 distinct local correction commands are needed. The construction need not physically resolve arbitrarily high counts to define this finite-outcome instrument.

However, actual correctness of those finite low-count effects and detector recovery is a supplied service. The overflow theorem does not receive arbitrary unmodeled detector behavior or error accumulation in later service calls. For LO4, direct quantum beam-splitter count enumeration gave extreme-branch overflow about **6.93909e-9**, below the certified geometric upper **6.9562642729e-9**.

## 6. Control, timing, bucket detectors and release

The new budget correctly removes the old ideal-homodyne ADC and Gaussian-saturation terms. It uses the inherited finite filter capture, adds one time unit of number readout/decision latency, and retains finite local-Z correction time. The continuing gamma D[Z_j] terms commute with this diagonal operation and are charged over the longer duration. Local phase commands are actual corrections, not a free frame before noncommuting gates. The 0.001 other-error allowance is still explicitly supplied and must cover all additional stated preparation, calibration and instrument errors.

A physical LO must have the right phase, temporal/spectral/polarization mode and observed mean; at .999 efficiency its input mean exceeds the observed mean by 1/.999. Optical/electronic response, readout-window discrimination, late photons, detector recovery, real control strength and duty cycle remain unpaid. The normalized time unit is not a conversion of a cited experiment's microsecond response into a feasible gate time.

I independently constructed the per-bin on/off POVMs `|0><0|` and `I-|0><0|`, applied one phase increment per click, and multiplied the actual bin channels. They reproduce the stated non-PNR kernel. Increasing bin count approaches the finite-LO PNR kernel, not an infinite-LO quadrature receiver. The 512/1024 stated budget distinction is supported in this stipulated model, but does not acquire equal-energy binning, rearming, a larger command implementation or the same latency in hardware. Mean photon count alone never certifies these services.

The original desired bus force is off at T; the optical processing and residual apparatus evolution are data independent except for the declared classical corrections. The accepted gate release condition therefore survives this receiver replacement after its additional latency. Residual physical interactions remain in the supplied complete-error bill. The arbitrary-warm ideal-quadrature release theorem is not being imported into finite coherent counting.

## 7. Exact numeric receiving and retained failures

Imported interval arithmetic, square roots, pi and exponentials remain byte-identical to the accepted certifier. The finite-LO extension uses valid interval-separated diamond branches, the valid Poisson majorant and alternating-series atan enclosures on its declared frontend domain. Exact rational wrapping and rounding enclose all 369 table entries. The frontend's atan argument restriction is computational, not a physical no-go outside the grid.

| observed LO mean | ideal count receiver diamond | total sufficient upper | <=0.01? |
|---:|---:|---:|:---:|
|1|0.0125332272|0.0165045014|No|
|2|0.0077239314|0.0116952055|No|
|3|0.0060141180|0.0099853923|Yes|
|4|0.0051635510|0.0091348390|Yes|
|6|0.0043649039|0.0083425171|Yes|
|7|0.0041646115|0.0081905296|Yes|
|8|0.0040319404|0.0083215553|Yes|
|13|0.0038419472|0.0745001725|No|
|16|0.0038419472|0.3697529431|No|

LO13/16 fail this **sufficient declared-service budget** because its overflow charge is large. An upper-bound failure is not a universal lower bound on every alternative overflow policy/instrument. No global optimization over hardware or measurement architectures was proved. LO3's narrow margin is not a recommendation. LO4's exact accepted total remains **0.009134838999948075** under the end-to-end control qualification.

Executed evidence:
- **487 author checks** passed. Exact `finite_lo_certificates.json` replayed byte-identically. One floating optimizer-log error changed from 6.94e-18 to zero, so the diagnostic log is not claimed byte-identical.
- `independent_finite_lo_audit.py`: **105 assertions**, including the genuine two-mode quantum BS, vacuum/nonvacuum comparison, reference-assisted overflow/channel tests, unequal-efficiency phase, exact attaining states, table margins and coherent-POVM counterexample.
- `independent_interval_bucket_audit.py`: **100 independent 130-digit interval checks**, **369 table checks**, actual Poisson-tail comparisons and five direct on/off-POVM comparisons. High precision and finite optical cutoffs are diagnostics, not alternative interval or infinite-mode proofs; the analytical arguments were separately reviewed.

## 8. Primary evidence and completion

[Thekkadath et al.](https://arxiv.org/html/1908.04765) is direct ordinary weak-field-homodyne precedent with balanced mixing and two number-resolving detectors. Its main text reports total efficiencies .274/.354 (the supplement gives .352 for the latter), distinct from intrinsic detector efficiency, and 10-microsecond acquisition windows. None supports the candidate's .999 system instrument. The candidate's average-.314 comparison is a stipulated constant-loss calculation, not a transplantation of that apparatus: its independent lost-pair lower bound is **0.35081589476013747**. It is not a universal lower bound for current or alternative hardware.

**Completed:** whole instrument/proof/cost review, authenticated dependencies, exact replays, independent adversarial diagnostics, two accepted controlling qualifications and this receipt. **Denied actions:** none. **Pending/uncertain:** actual low-loss force/collection/mode preparation, faithful finite-window high-efficiency number instrument, controller/readout/isolation services and broad architecture selection. No actual capability was acquired, and this audit does not authorize further fixture expansion. No equipment, outreach, purchases, publication, external/helper agents, source edits or denied-source retries occurred. No execution remains running.
