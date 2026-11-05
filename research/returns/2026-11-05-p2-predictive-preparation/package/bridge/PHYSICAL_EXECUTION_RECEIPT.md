# Physical execution receipt

The machine-readable receipt is physical_execution_receipt.json. It binds the unchanged acquired table and executed source program by SHA-256. Full source details are in SOURCE_EXECUTION_NOTES.md.

## Executed operations

A single retained 26-state passive oscillator source is observed through a finite first-order position sensor and 102 finite position boxes. Every box is converted to a 20-bit ADC value. Calibration and deployment use separate selected windows and separately initialized instruments; the source is never reset. A permanent spring supplies the input through its center. There is no plant release.

The initial state is fixed before the clock draws. The nominal source uses passive fixed-center idle. Independent reproducible PRNG streams emulate the private choices; a physical entropy source was not executed.

## Finite hardware and memory bill

Observed mass, local drag and permanent stiffness are each one. The energy bounds supply peak reactions for our known fixture: calibration trap force at most 2 and damper force at most 1; deployment trap force below 1.983216 and damper force below 1.183216. No bound on hidden force peaks, hidden bandwidth or hidden relaxation is inferred. The plant must actually obey its supplied LTI storage law over the operating range.

The calibration amplitude is 1 and ramp duration .02. Center speed is at most 93.75 and acceleration at most 14433.757. Center travel through ramp and return is 2; absolute moving-center work is bounded by 4 in normalized units. The query amplitude is .8 with rise duration .05, center speed 30 and acceleration below 1847.521. Its final off-ramp lasts .02 after the forecast and is included in total time and energy.

The exact derivative constants are checked in physical/universal_actuator_checks.py. For k_h=R'/h, ||k_h'||_1=15/(4h) and ||k_h''||_1=40 sqrt(3)/(3h^2). Thus the acceleration notation in the physical closure is correct. A single quintic ramp instead uses max|R''|=10 sqrt(3)/3.

The actual schedule lasts 37154.426896 normalized time units; the worst declared duration is 50390.748704. The .01 postread latency lies inside the deployment readiness window. Waveform and bin-duration resolution is 1e-8; absolute report/slot uncertainty is separately 1e-6. Counter width is finite. Accuracy over the physical schedule remains a calibration contract, rather than following merely from counter resolution.

The sensor time constant is 1e-5, with .0002 clearing before each baseline. ADC range is [-2,2]. The 102 raw ADC outputs contain 2040 payload bits. The learned table has 101 nodes. The exact fraction payload, JSON size, random bits and timer bits are recorded in the machine-readable receipt.

Streaming acquisition needs one baseline, the finite node array, counters and a stored control program. Reliable classical arithmetic, memory protection, clock state and controller execution are supplied hardware contracts. Their energy consumption and fault rates are not inferred from the logical bit count; a nonzero hardware-failure budget must be added to the conditional success event.

## Calibration and error account

Each position box has deterministic allowance 1e-4, covering finite sensor response, calibration, ADC, integration and duration normalization. White-readout density is 1e-10. Force discrepancy is at most 1e-5; selected-window meter backaction is at most 1e-6. The post-calibration energy upper bound including those allowances is below .450174 and is rounded to .5 for deployment readiness.

The table carries response error .0562185, readiness error .04070011 and separate deployment delivery error .000008. The readiness term includes baseline-only backaction and does not duplicate later delivery error. Conditional joint success is at least .951998 under the stated quiet, noise, ADC and reliable-controller contracts.

## Imperfect off mode and repeated use

For a common private-index-independent time-varying off force bounded by xi_0,

    failure <= 2 E D/(N delta^2) + xi_0^2 D^2/delta^2.

The executed contract uses passive fixed-center idle. A nonzero time-varying specification requires a new allocation of N, energy, sensor range, and on-minus-off delivery error. Increasing the wait alone does not remove the second term.

A fixed unknown off-center force f_0 is better handled by shifted storage:

    Esharp = E-f_0 x+f_0^2/(2mu) >= 0.

It obeys Esharpdot <= -v^2 during that constant off mode. A sufficient initial bound is

    Esharp_initial <= E_initial+|f_0||x_initial|+f_0^2/(2mu)
                   <= (sqrt(E_initial)+|f_0|/sqrt(2mu))^2.

This shifted bound must be supplied or obtained from the displayed known bounds; it is not estimated from a quiet-looking trace. Incremental inputs relative to that fixed center have the same response S and the same energy update. The measured baseline absorbs the offset. This corollary does not cover time-varying drift or a disturbance responding to the private index.

After every actual query and return ramp, update the energy ledger by one quarter of the actual squared-force integral, then run fresh readiness for the changed state. Numerical counterfactuals reuse the table. Source evolution during physical computation and any nonzero idle force remain in the time/energy budget.

## Evidence limit

Source, sensor and cumulative-box ODEs were floating numerical integrations. Long waits used floating matrix exponentials. The sampled diagnostics do not prove the uniform theorem. Exact rational encoding and the separate compiler verification concern emitted numerical objects. No laboratory plant, physical entropy source, physical protection system, or full worst-case perturbation experiment was executed.
