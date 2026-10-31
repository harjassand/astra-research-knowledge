# Independent extension: raw-current resistor-network record

2026-11-01. Same exact LP-dual and derivative/concavity proof as
`control_certificate_review.md`. No proof or data was weakened to meet a
numerical target.

## Inputs and isolation

The checker was extended with `--data` and `--output`. On this run it read
only these files and the existing normalized public specifications/task menu:

* `../control/network_results/scalar_records.json`;
* `../control/network_results/dual_certificates.json`;
* `../control/network_results/raw_current_records.json`.

It did not load the hidden network, B,g, determinant coefficients, the
known-source optimization diagnostics, or the demonstration's report. It
did not run an optimizer. The revised demonstration was also inspected:
its network B,g generate the raw current record and diagnostics; they do
not enter IntervalLearner, its proposal, or its certificate routines.

## Raw-to-normalized interval transfer

All 84 settings were checked exactly. The record supplies physical scale
L=1/4, measured zero-dose current Rhat_0 and radius e0=1/8000000. Every
measured Rhat_i has the same radius ei. The normalized records obey exactly

    y_i=(Rhat_i-Rhat_0)/L,
    eta_i >= (ei+e0)/L = 1/1000000.

The zero-dose command is one of the 84 settings; its raw value and radius
match the shared reference, and its normalized value is exactly zero. No
additional baseline assay was silently introduced. The triangle bound is
valid with arbitrary correlation from the shared baseline. This verifies
the interval transport conditional on the specified raw error bounds; it
does not infer calibration validity from the observed numbers themselves.

## Exact certificate verdict and target failure

All 32 exact dual certificates and all four derivative/regret calculations
are valid. The normalized regrets are:

| Task | Exact certificate displayed as decimal | Initial 2e-5 target |
|---|---:|---|
| All controls | 2.1901794413051278e-5 | Missed |
| Changed prices | 2.8157768589753130e-5 | Missed |
| Actuator 2 unavailable | 1.0774361251274800e-5 | Met |
| Half budget | 9.1904411486352050e-6 | Met |

The receipt stores exact fractions. Certificate validity and target
achievement are separate: `verdict=PASS` and
`all_requested_2e_minus_5_targets_met=false`. The checker initially stopped
at its old target assertion; it was amended to report the unchanged exact
bounds and the missed target, not to change the data, estimator, error bars,
or proof. No new source queries or parameter tuning followed this finding.

Multiplying each normalized objective, including its specified price term,
by physical scale L=1/4 multiplies each regret by 1/4. This is a unit change,
not attainment of the originally requested normalized 2e-5 target.

Receipt: `independent_network_control_validation.json`.
Reproduce with:

    python validate_control_certificates.py \
      --data ../control/network_results \
      --output independent_network_control_validation.json

As before, r=n=3 and k=6 exercise a full-degree rational model and local
global-regret certificates. They do not demonstrate cheap high-dimensional
factorial truncation, uniformly tiny whole-simplex error, a physical device,
historical originality, or an advantage over equally informed ordinary fits.
