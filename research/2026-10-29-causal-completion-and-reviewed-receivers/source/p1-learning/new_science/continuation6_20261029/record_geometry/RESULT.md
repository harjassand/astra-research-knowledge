# Continuation6 complementary result: ordinary learning already reaches untested useful control

**Verdict:** an ordinary behavioral route is sufficient under an explicit LTI port and observable-lag interface. It uses one continuing specimen, visible input–output data and no hidden-state reset. The actual controlled waveform is new. Its finite precision and conditioning costs can be certified directly. This is a strong comparator, not a new foundational mechanism.

`TASK_DIRECTED_BEHAVIORAL_CONTROL.md` contains a complete exact synthesis proof, a square-data perturbation certificate, cost-improvement and confidence transfers, explicit physical costs, and the hidden-delay obstruction. `PRIMARY_PREDECESSORS.md` distinguishes what was read and which sensing assumptions each predecessor actually uses.

## Concrete executed result

One synthetic two-temperature specimen, with only its first temperature observed, supplies 40 input–output samples at binary input amplitudes. The exact order/lag is warranted as two; the readout error is bounded by the imposed metrology budget \(10^{-6}\). Ten measured trajectory columns define a certified predictor. The learned six-call control is rounded to the actual declared grid of denominator 65536. Every chosen amplitude is absent from the calibration record.

All numerical claims below were checked with exact rational arithmetic; floating-point QR only selected measured columns.

- Zero-input baseline task cost: **0.48063305378713406**.
- New waveform actual task cost: **0.053130256879652005**.
- Guaranteed cost reduction from the visible-data certificate: **0.4121036470381547**.
- Actual cost reduction in the known verification fixture: **0.42750279690748205**.
- Guaranteed maximum future output error: **0.004072447980390399**.
- Actual maximum future output error: **0.0000016430909407106985**.
- Calibration calls/readings: **40/40**; subsequent physical calls: **6**; hidden resets: **0**.

This is a deterministic synthetic calculation with bounded sensor errors, not measured apparatus data or a claim that the stated metrological precision is inexpensive. Sensor accuracy, exact grid actuation and validity of the linear port law are explicit premises. Frozen device dependence is permitted only when the same specimen is calibrated and used and the premises hold for it.

## What the experiment cannot establish

For any calibration budget \(N\), the stable scattering-passive delay ports \(y_t=\pm\rho u_{t-L}\), \(L>N\), have identical complete calibration histories even for adaptive excitation. They require opposite controls for a later target, giving worst-case squared task error at least \(a^2\) when a sign-informed controller attains zero. Their hidden realizations are finite and nilpotent. Thus a small observed Hankel rank does not certify a short hidden memory or justify arbitrary extrapolation. The task deadline in this obstruction includes the delayed response.

The established positive result and this obstruction jointly sharpen selection: the missing research contribution is a physical source of task-relevant completeness or a different useful control principle robust to hidden alternatives. Learning only a task-relevant response, using a persistent input–output record, or synthesizing a new waveform is already established on the conventional interface.

## Files

- `TASK_DIRECTED_BEHAVIORAL_CONTROL.md`: theorem, proof, finite-error receiver, physical resource accounting and obstruction.
- `PRIMARY_PREDECESSORS.md`: focused primary-source comparison.
- `check_behavioral_control.py`: exact rational fixture, visible-only designer, independent hidden-model verification and passive-delay checks.
- `BEHAVIORAL_CONTROL_SYNTHETIC_READOUTS.json`: all 40 observed readouts, inputs, imposed sensor errors and the executed waveform, saved as rational strings.
- `BEHAVIORAL_CONTROL_CHECKS.json`: compact check results and explicit limitations.
- `MANIFEST.json`: hashes of the completed artifacts.

No extra agents, producer exports, apparatus, or external transfers were used. All earlier continuation files are preserved.
