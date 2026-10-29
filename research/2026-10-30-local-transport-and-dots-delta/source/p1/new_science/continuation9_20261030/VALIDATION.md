# Proof receipt and executed validation

30 October 2026. Population-model checks and actual internal reviews. These
are not device measurements, an acquired confidence event, or an end-to-end
precision/cost budget. The code is a check on independently assembled models;
the mathematical claims rely on the saved proofs and their stated interfaces.

## Executed root program

From the archive root, run:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 new_science/continuation9_20261030/check_local_transport_law.py
```

The program was executed successfully under Python 3.12.14, NumPy 2.3.5 and
SciPy 1.17.0. Its actual output is `LOCAL_TRANSPORT_LAW_CHECK.json`.

| Check | Actual result | What it establishes |
|---|---|---|
| Full state-space port versus eliminated hidden impedance | Maximum norm discrepancy 3.893778881690102e-9 | Agreement of two separately assembled linear response calculations, including noncommuting unknown local friction and two hidden relaxation fields |
| Full driven noise versus fluctuation-dissipation spectrum | Maximum discrepancy 1.7039230894432783e-15 | The independent controller bath is correctly included; native resistor noise alone would not be the same calculation |
| Full thermal covariance identity | Maximum residual 8.881784197001252e-16 | The supplied finite Markov realization preserves the claimed Gaussian covariance |
| Exact protected counter and its noise | Drift residual at most 5.551115123125783e-17; noise residual zero | Actual native current and controller update have the stated pathwise relation in these models |
| Finite-band receiver | Largest actual-error/proved-bound ratio 0.10430578968502696 | The sampled response lies below the analytic bound for the two independently assembled noncommuting cases |
| Two-ring density mode | Errors 0.0049754957014589785, 0.0020284869926691707, 0.001448701342585655 at N=16,64,256 | Finite-size response is consistent with the proved limit; finite-size cross-ring response is not called zero |
| Common integrated-current covariance | Errors 0.023351527049248127, 0.0031156450133962422, 0.002316818894222205 | Exact matrix-exponential covariance agrees with the claimed limiting common channel; no simulated sample confidence is inferred |
| Finite-size DC load response | Maximum formula discrepancy 2.220446049250313e-16 | Checks the conservative-loss denominator and both ring currents |
| Nonlinear marked events | 30 forward/reverse pairs; maximum balance/energy discrepancy 4.440892098500626e-16 | Only the local marked detailed-balance calculation, not a nonlinear hydrodynamic or action receiver |

The response discrepancy near 4e-9 occurs at low frequencies near conserved
directions; it is not reported as machine precision. The finite-band examples
use small physical observation bands, with maxima about 5.86e-5 and 2.68e-5.
Long observation time and any actual noise/actuation cost remain real. No
practical acceleration follows from these checks.

## Complementary runnable constructions

- `physical_mechanism/check_wave_counter.py` and its saved JSON check the
  independent reciprocal-wave construction, finite mode covariance, poles,
  protected current and conservative-loss identities. Its validation file
  retains the failed complex-pole calculation outside the valid neighborhood.
- `record_geometry/check_finite_pulse_lc.py` and `FINITE_PULSE_LC_CHECK.json`
  check the finite-duration orthogonal transport/rotation program, exact
  counter, thermal covariance and low-mode Schur coefficient. The actual
  sequence uses isolation, synchronized finite-duration operations and fresh
  auxiliaries. It is a different supplier from an unknown native resistor.

No extra tests were added to duplicate an analytic proof or enlarge a fixture.
The mobility/action counterexample is symbolic and needs no numerical example
to establish its strict positive gap.

## Actual review record

Exact reviewed inputs, hashes, snapshots and reviews are retained, rather
than reconstructed from verdicts:

- Root independently received `physical_mechanism/RECIPROCAL_WAVE_COUNTER.md`
  together with `CONSERVATIVE_LOSS_EXTENSION.md`; the receipt is in
  `receiving_review/WAVE_COUNTER_RECEIVING_REVIEW.md`.
- The physical-mechanism role accepted the root signed-ladder theorem at
  `42b5d5537a2f357a05a8b1ff55d292414e23c84d50d99bf50d3527073afc3ce2`.
  Its review reconstructs the corrector, Gaussian whole-path step, full joint
  rate, force normalization and work interface. See its `receiving_review`.
- The same role accepted the finite-duration LC program at
  `49acbebb439b5eaa2305ee273239101316261d4875be45015f188f8a744b8cf2`.
- The record-geometry role received the passive-law proof and required an
  explicit out-of-band measurement premise and a positive wave-speed lower
  bound. The original plus `LOCAL_PASSIVE_LAW_REALIZATION_CORRECTION.md`
  are accepted together. Its RLC resonance counterexample is preserved.
- The same role received the causal-response proof and its fixed-geometry,
  bounded-gain and response-difference addendum. The original plus
  `CAUSAL_RESPONSE_INTERFACE_CLARIFICATION.md` are accepted together.
- The nonlinear partial construction and mobility selection calculation have
  their actual receiving receipts in `record_geometry`. Their acceptance is
  restricted to the claims made; it does not fill the missing nonlinear limit.

The full snapshot manifest pins all final artifacts, including later receipts
and corrections. Older accepted work and its review provenance remain unchanged.
