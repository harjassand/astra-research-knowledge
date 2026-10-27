## ASTRA Pro3 — A band-selective experiment compiler

The new construction changes the physical intervention sequence rather than simply waiting longer for another impulse response.

For a positive relaxation spectrum \\(\mu\\), the scientific task is to bound the total weight of slow modes:

\\[ W\_{7/8}=\mu([7/8,1)). \\]

Instead of one impulse followed by a long wait, the learner uses a short sequence of positive and negative pulses. The final boundary reaction measures a polynomial of the unknown relaxation spectrum.

The experiment is designed from the previously acquired four moments. A uniform-spectrum model is used only to propose an intervention; the final certificate does not assume that this model is correct.

### Executed result

Single lag-16 impulse

# 0.004995

Certified upper bound on slow-band mass

Three shaped pulses

# 0.000552

Certified upper bound, same final readout time

The shaped intervention gives a 9.06× tighter certificate on the executed continuum-spectrum source. Both experiments require two new scalar boundary-reaction readings, finish at time step 17 and use the same total absolute intervention dose of \\(1/5\\).

The additional cost is three active pulse commands instead of one. The certificate includes an absolute raw-reaction sensor-error allowance of \\(10^{-8}\\), propagated through the nonlinear reciprocal readout using exact rational interval arithmetic.

### A shorter experiment for the same decision

A separate task required only certification that slow-band mass was below 0.01.

| Experiment                | Latest measurement | Additional readings | Pulse commands | Certified upper bound |
| ------------------------- | ------------------ | ------------------- | -------------- | --------------------- |
| Single lag-16 pulse       | Step 17            | 2                   | 1              | 0.004995              |
| Shaped lag-7 intervention | Step 8             | 2                   | 5              | 0.008298              |

The shaped experiment satisfies the same decision threshold nine time steps earlier, at the cost of more intervention commands. Both results retain the earlier eight acquisition readings in their total history.

These are conditional software-source results, not guarantees that the same improvement holds for every compatible physical source.

### Stronger result: the same filter works with nonnegative physical inputs

The signed polynomial can be implemented even when the physical apparatus cannot apply negative inputs.

The procedure separates the positive and negative polynomial coefficients into two different nonnegative intervention histories, then subtracts their transformed boundary readings. No extra scalar readouts or total dose are required.

The executed nonnegative-input version achieved:

| Latest response time | Certified slow-band upper bound |
| -------------------- | ------------------------------- |
| Step 8               | 0.008298                        |
| Step 9               | 0.005083                        |
| Step 17              | 0.000552                        |

Both trials use nonnegative inputs, and their combined dose remains \\(1/5\\).

This also revealed an important causal benefit. An adjacent-pulse interaction that produced a false admission in the original signed-pulse experiment is never activated by the separated nonnegative histories. The corrected architecture therefore avoids that particular failure without another sensor.

It is not universally immune to nonlinear memory. A different delayed interaction can still deceive it; I constructed and executed such a counterexample. That limitation motivates explicit intervention-interaction testing rather than treating a successful spectral filter as evidence of linearity.

### Further result: learning the measurement operation with minimal sensor access

I proved that the two nonnegative histories are measurement-count optimal for exactly acquiring the selected signed polynomial functional, assuming the original four moments are retained.

One nonnegative scalar reaction cannot determine that functional for every compatible source. I constructed two strictly positive continuous spectra that produce identical original moments and an identical additional scalar reading, but different values for the desired functional.

Two properly encoded nonnegative histories are sufficient. The lower bound concerns exact acquisition of this functional, not every possible method of certifying a slow-band threshold.

### Causal falsification and repair

The executed experiments also established a substantial limitation on reliable learning.

A hidden delayed intervention interaction caused the differential sensor to report a slow-band upper bound of 0.006006, apparently satisfying the requested 0.01 threshold. The true source contained slow-band mass 0.077922.

Three additional factorial readings detected the interaction. Correcting the task-specific response restored the sound interval

\\[ [0.077625,\ 0.078246]. \\]

A separate between-run drift attack gave another false-safe bound of 0.004507. A four-reading interleaved protocol cancelled the affine drift and correctly certified a lower bound of approximately 0.077860.

There is also a fundamental limit: under finite raw-sensor error, two stable positive spectra can have slow-band masses of zero and one while remaining indistinguishable through every bounded-dose experiment within a fixed finite horizon. Better filtering alone cannot guarantee universally reliable classification exactly at the spectral threshold.

### New questions answered from the same acquisition

After retaining the one shaped spectral reading, the learner answered four subsequently specified spectral-tail questions without further source measurements.

| New slow-mode threshold | Certified upper bound |
| ----------------------- | --------------------- |
| 7/8                     | 0.00055154            |
| 15/16                   | 0.00011809            |
| 31/32                   | 0.00005896            |
| 63/64                   | 0.00004230            |

The calculation uses the known polynomial response and its certified uncertainty, not fresh source access.

### Scientific status and saved work

All 11 executable programmes passed isolated replay, reproducing 12 JSON results files byte-for-byte. An independent exact-arithmetic verifier completed 84 checks, and the 29-file archive passed integrity verification.

Complete mathematical proofs and findings

Experiment synthesis, nonnegative implementation, exact query lower bound, sensor-noise guarantees, causal falsification and information limits.

Reproducible research bundle

Actual executable source, native Schur dependency, measured results, independent verification, clean replay and SHA-256 manifest.

Assessment: The useful development is a task-directed experimental compiler that changes how an unknown causal source is interrogated, rather than merely fitting its previously measured responses. It can trade intervention count against waiting time, reuse the resulting evidence for unforeseen questions, and actively challenge causal assumptions that would otherwise produce misleading conclusions.

Its polynomial-moment and coded-excitation ingredients have classical antecedents.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://webspace.maths.qmul.ac.uk\&sz=32)

webspace.maths.qmul.ac.uk

+1

&#x20;There is no established historical priority, physical device or advantage over an equally informed conventional identification algorithm.



The strongest remaining foundational problem is a causally warranted, noise-robust observation interface that can discover useful spectral and nonlinear-memory structure without taking linear positive-response dynamics as a supplied premise.