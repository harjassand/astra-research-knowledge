# Exact handoff — 15 October 2026

## State

The flagship mission is **not demonstrated**. Preserve the positive measurement normalization and verified countermodels; do not count this as a new scientific capability or a historical-priority result.

Completed: one real cell's EIS input; positive-RC plus series L/C model; exact inductance-canceling mass; full-half-line compactification; four checked continuum duals; four exact-feasible positive models; six checked sparse-protocol duals; NNLS internal comparator; local unit checks and offline replay.

Not completed: full upstream data checksum verification; complete pulse/current trace acquisition; finite-amplitude voltage validation; calibrated measurement uncertainty; nonlinear model-error bounds; other-cell tests; full hybrid-drt or Stieltjes incumbent execution; matched total acquisition comparison; independent proof/code review; novelty clearance.

## Exact central state

- Data: data/cell_001_eis.csv, first row of the three upstream EIS CSVs, 70 frequencies.
- Main conditional data interface: 58 points, 0.01 through 904.7 Hz; epsilon=0.1 mOhm per real/imaginary component.
- Full-band necessary minimum error from real-part monotonicity: 0.515 mOhm. The rejected full-band model must not disappear from future summaries.
- Positive mass: Re Z(0.01 Hz) - Im Z(0.01 Hz) + 0.01 Im Z(1 Hz); upper mass 71.4268 mOhm under the stated error box.
- Compactified mode: s=(2*pi*0.01*tau)/(1+2*pi*0.01*tau). Both endpoints are included. They encode ohmic and ideal capacitive limits.
- Q_10 checked outer interval: use the exact rational values in results/continuum_certificates.json; safe outward display [62.1849,62.7360] mOhm.
- Q_1000 safe outward display: [100.4125,529.1050] mOhm.
- Two exact-feasible positive models give Q_1000 approximately 100.769677 and 528.747375 mOhm. Their separation is a genuine ambiguity of the stated EIS-only interface.
- Three six-frequency protocols are in results/probe_protocols.json. Their final six dual bounds are in results/probe_protocol_certificates.json. No mass repair or extra low-frequency inputs are used in those sparse-protocol bounds.

## Replay

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python code/reproduce.py
```

The results are contingent on the model, the transcribed input, interval-library correctness, and the declared deterministic error budget. Source collection/experimental time is not included in runtime.json.

## Specific continuation constraint

Do not infer finite-amplitude voltage safety from these linear-response certificates. Do not infer a universal acquisition lower bound from the three tested frequency sets. Do not compare the new code only with plain NNLS and call that a strongest-method win. Do not withhold existing pulse or pseudo-open-circuit information from incumbents to manufacture an advantage.

The decisive continuation is a genuinely improved nonlinear, target-specific measurement/information operation with a matched physical validation budget. Further relaxation-grid compression or a longer positivity manuscript, alone, does not pass that gate.
