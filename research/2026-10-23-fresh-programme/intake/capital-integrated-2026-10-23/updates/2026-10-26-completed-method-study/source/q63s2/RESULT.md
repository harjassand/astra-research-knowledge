# Stage2 result: dynamic stress, physical-noise limits and conditional calibration

The original reconstruction survives as an exact-data mathematical operation,
but its proposed scalable physical use does not. This second stage closes the
transient-drive escape under explicit readout assumptions, checks a more
physical quasistatic noise model, and constructs a stronger conditional
self-calibration mechanism. **The mission-scale scientific advance remains
not achieved.** No device, physical performance or historical priority is
claimed. Stage1's 16 preserved files are unchanged by SHA-256 comparison.

## Most consequential stress: can dynamics overcome deep attenuation?

The strongest practical competing mechanism is to select a frequency, send a
carefully shaped pulse, or vary positive shunts during the experiment. A small
steady signal alone would not rule out any of these.

I proved a stronger result over the full declared finite model. Let two
networks differ by one added positive leak, with fixed positive capacities.
For every signed input and every nonnegative time-varying shunt schedule, the
fault-response kernel is pointwise dominated by the unloaded kernel. Therefore

    ||output_difference||_2 <= unloaded_DC_difference * ||input||_2.

The unloaded system attains this induced gain in the long, low-frequency limit.
For a finite sampled horizon, ordinary singular-value decomposition gives the
optimal input over all signed waveforms, and no positive shunt schedule can
increase that optimum. This uses established positive-systems theory, not an
invented generic control principle: see
[Rantzer, Theorem 3](https://arxiv.org/html/1203.0047v3).
The fault-cascade and time-varying comparison are derived in
[PROOF_STAGE2.md](PROOF_STAGE2.md).

With parameter-independent external white readout noise, the same bound limits
the relative entropy of even an adaptive experiment. It retains the
exponential depth cost of the stage1 leaky-path family. The budget is
**integral input squared over time**; actual dissipated energy and complete
source/reset costs are separate and have not been measured. This is not a
universal thermodynamic no-go statement.

## Genuinely withheld execution and conventional optimum

The stage2 seeds were unused in stage1 and fixed before execution. All 25 new
networks are retained: cycles, complete bipartite graphs, ladders, two-clique
bridges and deeper paths, at n=6,10,14,18,24, with heterogeneous weights,
capacities and leaks. This includes graph families absent from the stage1
test set. The proof supplies generality; the numerical checks test its
implementation.

* **16,200 load-frequency pairs** gave no gain beyond unloaded DC.
* **32 time-varying schedules** on four finite-horizon fixtures were compared
  with the ordinary *optimal* unloaded SVD input, using identical input norm
  and observation horizon. Their best gain ratios were 0.630, 0.100, 0.170
  and 0.000112. These ratios are finite tests, not general bounds.
* On the n=18 path, the unloaded DC difference was 4.57e-18 and the optimal
  finite-horizon gain was 2.74e-18. Optimizing the input did not produce a
  hidden high-frequency amplification.

See [frequency_noise_stress.csv](frequency_noise_stress.csv),
[transient_stress.csv](transient_stress.csv),
[withheld_networks.json](withheld_networks.json) and
[transient_data.json](transient_data.json).
The executable [stress_and_completion.py](stress_and_completion.py) constructs
the conventional optimum explicitly; it does not compare only with a weak
constant-pulse baseline.

## Attack on the readout-noise assumption

Stage1's exact statistical dominance required configuration-independent noise.
That assumption cannot be silently transferred to real thermal/electrical
noise. I proved a separate all-configuration result for independent
quasistatic Gaussian readings with variance a+nu*port_resistance. Both absolute
and relative fault signals decrease under positive shunt loading, so both
directions of one-reading Gaussian KL divergence also decrease. This includes
a fixed detector floor, an ideal low-frequency equilibrium noise term, or
both. It gives an adaptive KL bound, not an unsupported unequal-variance
Blackwell claim. There were 600 numerical configuration/noise-model checks.

[Nyquist's primary paper](https://doi.org/10.1103/PhysRev.32.110) motivates the
resistance-dependent noise term. It does not justify independent readings at
arbitrary bandwidth. A supplementary complex spectral-noise diagnostic on the
same 25 fixtures also found its best tested information at unloaded DC, to
roundoff. That grid is **not a proof** for all colored noise, thermal gradients,
configuration-dependent process noise or spectral acquisition strategies.
See [spectral_noise_diagnostic.csv](spectral_noise_diagnostic.csv). These remain
explicit limits of the physical inference, rather than hidden assumptions.

## Stronger positive construction: capacities can anchor unknown load gains

The stage1 calibration obstruction jointly rescaled conductances, capacities
and actuator gains. A stronger representation breaks it if the node capacity
matrix C is independently known. This is additional physical information,
not an inferred property of an unknown specimen.

With unknown positive shunt gains H=diag(1,h_1,...), write

    B(s) = H^(-1/2) (K+s C) H^(-1/2).

The stage1 algorithm recovers B at each of two distinct positive **real
Laplace points** s_1,s_2. Their difference is diagonal, with entries
(s_2-s_1) C_i/h_i. Thus the gains h_i and the entire physical conductance
matrix K follow exactly. This uses n(n+1) scalar response values and needs
neither known topology nor generic eigenvalues. It is a complete governing
construction in the declared class. It is not a claim about two ordinary
sinusoidal measurements or free access to internal sensors.

**15/15 exact rational cases recovered both K and every gain entry exactly.**
The proof is Proposition C in PROOF_STAGE2.md; data are in
[exact_self_calibration.csv](exact_self_calibration.csv).
If capacities are also unknown, only the ratios C_i/h_i are acquired and the
stage1 ambiguity remains. Known capacities are a calibration resource, not
acquisition of physical semantics without an anchor.

I also supplied a finite-pulse acquisition: a known rectangular input and an
exponentially weighted output integral estimate each real Laplace response.
The omitted tail has a rigorous bound using only the known port capacity,
pulse and Laplace parameter. Its external white-readout variance and repeated
cycle cost are explicit. Sixteen finite-duration calculations satisfied the
tail bound, but only four direct reconstructions remained in the physical
class. Increasing observation time does not make readout variance vanish.
See [finite_pulse_acquisition.py](finite_pulse_acquisition.py) and
[finite_pulse_acquisition.csv](finite_pulse_acquisition.csv).

## Strong ordinary method and the positive construction's failure

The same-information incumbent jointly fits all nonnegative edge conductances,
leaks and positive load gains, with known C, an analytic Jacobian and eight
starts. It receives the same commands and the same two-point observations,
no true topology or parameters. Selection uses the observed residual alone.
Thirty-two new load/Laplace combinations are withheld for prediction scoring.

| Observation noise sd / baseline | Direct self-calibration | Ordinary joint fit |
|---|---|---|
| 0 | 4/4 physically valid; K errors 1.5e-12 to 1.3e-11 | 4/4 physical; K errors 9.1e-12 to 3.7e-9 |
| 1e-7 | 0/4 physical: one rejection, three nonphysical matrices | K errors 4.2e-5 to 0.00369 |
| 1e-4 | 0/4 physical: four rejections | K errors 0.0647 to 7.51 |

At the larger noise level the conventional method's port prediction errors
were only 0.000281 to 0.000503 while its physical parameter errors could be
huge. That is evidence of ill-conditioned internal inference, not validation
of the recovered network. The new formula does not defeat this ordinary
incumbent on noisy data. Full results and raw evidence are
[self_calibration_comparison.csv](self_calibration_comparison.csv) and
[self_calibration_data.json](self_calibration_data.json).

A physical experiment may retain its entire output waveform and fit it
directly; a competent incumbent should be allowed to do so. The two-statistic
comparison measures inversion on identical summaries and establishes no
advantage over a full-history physical estimator. Conversely, an ordinary fit
succeeding on a potentially new acquisition design does not logically erase
that design. Priority of this exact finite calibration design is unresolved.
The limiting findings are its noise sensitivity, additional calibration
resource and absence of a demonstrated useful physical implementation.

## Established result and remaining obstacle

Established: exact finite single-port reconstruction; a proof that transient,
frequency and positive time-varying shunt control cannot rescue the deep fault
under the stated input/readout model; a quasistatic resistance-dependent-noise
extension; and exact joint gain/network calibration when capacities are known.
Numerical failures, invalid reconstructions and poor incumbent parameter
estimates are retained. All data are synthetic.

Not established: historical novelty of the combined finite designs; a useful
new detector or internal actuator; a uniform stable inverse; a general result
for all physical noise and energy conventions; or a practical acquisition
advantage over conventional methods. The missing operation is still calibrated
access that avoids or removes hidden loss without installing comparably
powerful interior instrumentation. Known capacity standards solve one gauge
but do not provide this operation or its precision.

Numerical execution emitted NumPy/SciPy matmul divide/overflow/invalid warnings.
Saved operators were finite and passed their inequalities. I additionally
cross-checked eight matrix exponentials against an independent nonnegative
uniformization series using a separate arithmetic path: maximum entry
difference 6.72e-15. The warning's runtime cause was not diagnosed. This audit
is retained in [numerical_audit.csv](numerical_audit.csv), not concealed.
The governing conclusions rely on the proofs, not that runtime's warnings.

New primary evidence and its scope are in [SOURCES_STAGE2.md](SOURCES_STAGE2.md).
The research history and rejected interpretations are in
[RESEARCH_NOTES.md](RESEARCH_NOTES.md).

Reproduce from stage2:

    /usr/local/bin/python3 -B stress_and_completion.py
    /usr/local/bin/python3 -B physical_noise_and_audit.py
    /usr/local/bin/python3 -B finite_pulse_acquisition.py

The first script verifies the preserved stage1 hash inventory. No sibling,
evaluator, assignment key or programme chat was inspected; no delegation,
external write, publication, equipment operation or paid service was used.
