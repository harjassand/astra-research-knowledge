# Retained oscillator source: executed acquisition and readiness

## Files and learner boundary

The executable is acquired_response_source.py. Its learner output is acquired_step_response.json. The predictor receives only this finite response table, baseline, declared bounds and resources. It does not consume retained_source_diagnostics.json or source_trace_diagnostic.json. The former contains microscopic source parameters and diagnostic ground truth; the latter contains a sampled physical trajectory for later comparison.

The source has one observed mass/velocity coordinate with M=Gamma=k=1 and twelve hidden two-dimensional skew/damped mode blocks. Its energy is half the squared full state norm. The coupling blocks are exact transposes with opposite sign in the observed and hidden equations, so the continuous energy identity is

    Edot = f v - v^2 - sum_j d_j ||z_j||^2.

One dark undamped pair is decoupled from the port; its stored energy remains. The other rates and couplings are not given to the learner.

The initial source state is generated once with total numerical energy 0.2, before the distinct calibration and deployment clock draws. The physical state is retained through the positive probe, off-ramp, second waiting interval, query and final off-ramp. Only the sensor/integrator is initialized twice.

## Exact emitted contract

- Response error: 112437/2000000 = 0.0562185.
- Deployment baseline: -1191/131072 = -0.00908660888671875.
- Readiness error: 4070011/100000000 = 0.04070011.
- Forecast force/backaction error, separate from readiness: 1/125000 = 0.000008.
- Horizon, local damping, permanent stiffness, observed mass: all one.

The response error includes:

    .02 quiet background + .02 finite ramp + .005 finite box
    + .01 interpolation + .0002 deterministic meter difference
    + .001 simultaneous noise + .000002 report timing
    + .0000165 calibrated force/backaction.

The step Lipschitz constant two is conservative for this known mass/energy fixture. The one-dimensional storage proof actually permits a tighter nominal constant, but the executed contract does not rely on that improvement.

Readiness includes .04 quiet drift, .0001 deterministic baseline allowance, .0006 noise and 1.1e-7 baseline-only backaction. The last term safely exceeds 2*1e-6*sqrt((.0002+.005+2e-6)/2), so finite slot guards are covered. Forecast force error 1e-5 plus meter backaction 1e-6 over horizon one costs less than the separate 8e-6 allowance.

The calibration 16.5e-6 force/backaction term exceeds

    (2*1e-6 + 1e-5 + 1e-6)*sqrt(1.030202/2).

These robust nonzero error allowances are not all sampled as physical perturbations in the nominal source run.

## Finite measurement and timing

There are 101 calibration position boxes (one baseline and 100 signal boxes) and one deployment baseline box. Every recorded mean is simulated through an actual first-order sensor with time constant 1e-5, initialized only at the selected window and allowed to clear for .0002 before the baseline. The source itself is never reset.

Each sensor box gets a white-readout Gaussian draw with variance density 1e-10 divided by box duration .005, then a fixed 2e-6 calibration offset and an actual 20-bit ADC rounding over[-2,2]. All 102 raw ADC values lie in range. The exact rational learner reports are differences of these finite ADC outputs; they are not exact physical position values.

The deterministic 1e-4 per-box budget covers sensor lag/transient, finite integration, calibration, ADC quantization and duration normalization. Source position/velocity bounds during acquisition are at most one from the rounded energy bound. Sensor lag 1e-5, the cleared transient, ADC half-step below 2e-6, and nominal calibration offset 2e-6 fit well below that budget. Deployment uses energy bound .7 and the corresponding velocity bound.

Absolute slot/report timestamp uncertainty is 1e-6. Within-program waveform and box-duration normalization use a separately paid 1e-8 time precision. For the largest calibration waveform slope 93.75 this produces force error below 1e-6, leaving room within the 1e-5 complete force-delivery allowance for other tracking/gain/rounding errors. A single absolute timestamp tolerance must not be misread as permission for uncharged normalization or waveform errors.

Private physical entropy was not executed. The numerical illustration uses separate reproducible PRNG streams for source, calibration clock, deployment clock, calibration readout and deployment readout. The theorem requires the stated fresh private randomness.

## Actual clock bill and energy

The calibration slot is 1.030202; N_cal=32768 and the realized index is 30458. The deployment slot is 1.015202; N_dep=16384 and the realized index is 5688. The latter slot includes sensor clearing, baseline, a fixed .01 postread latency, the entire forecast and clock guards.

- Actual calibration wait: 31377.892516 normalized time units.
- Actual deployment wait: 5774.468976.
- Actual entire protocol including final return: 37154.426896.
- Worst declared duration: 50390.748704.
- Private random-bit requirement: 15+14 bits.

The complete nominal calibration ramp/hold/off squared-force integral is computed exactly in the program. Adding the allowed force/backaction errors gives energy at most 0.450173334 after calibration, safely rounded upward to 0.5 for the next initialization.

Numerical actual energies:

- Initial: 0.2.
- After complete calibration pulse: 0.280010353501.
- Before selected deployment window: 0.0808444643212.
- After deployment and off-ramp: 0.204547607191.

Hidden energy before deployment is 0.0808034031827. The dark pair retains approximately 0.0122509799369 throughout. This illustrates retained hidden storage; it is not used to prove the general theorem.

The permanent center has finite range, speed and acceleration. The calibration amplitude 1 and ramp .02 require center speed 93.75 and acceleration at most 14433.7568. Its reaction-force bound is 2, travel 2 and absolute moving-center work bound 4 in normalized units. The query 4/5 has ramp 1/20, speed 30 and acceleration below 1847.521. Its reaction bound under energy .7 is 1.983215957. Holding-center apparatus power is an additional real hardware cost.

## Numerical evidence limits

The physical source and finite sensor/integral ODE were computed with floating Radau integration; long free waits used a floating matrix exponential. This is not an interval-validated physical-source enclosure. The table is exact rational data, and the root predictor separately verifies its finite numerical operation.

The source fixture reports a sampled table discrepancy 0.00368991001736 against its microscopic zero-state response, and sampled deployment free-motion variation 0.000445391052. Neither diagnostic establishes the uniform contract. The acquisition proof and its declared meter/energy events supply that contract.

The run took about 12.4 seconds in the recorded environment, while its physical schedule lasts tens of thousands of normalized time units. Calibration Radau work used 47060 right-hand-side evaluations; deployment used 47126. These computation times are simulation costs, distinct from the physical protocol and from the later finite predictor's execution costs.

The fixed future input is preprogrammed as a 4/5 quintic rise starting at forecast time zero, with rise duration 1/20, followed by a hold through the horizon. Its final off-ramp occurs after the forecast and is charged in the source energy/time ledger. An optimizer-dependent force would require the planner's additional finite computation and execution contract; it is not claimed to have been applied in this source run.
