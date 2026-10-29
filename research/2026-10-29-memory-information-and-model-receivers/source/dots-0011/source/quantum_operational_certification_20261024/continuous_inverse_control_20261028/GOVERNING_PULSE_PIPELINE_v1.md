# Continuous learned inverse control, with complete noisy code boundaries

28 October 2026. Author finite-model construction, pending independent review. This successor preserves the received/under-review clock and boundary sources unchanged. It replaces a previously ideal per-use learned inverse by executed bounded-speed single-qubit Hamiltonian pulses, and changes the native-phase background convention explicitly. It is not a hardware measurement or a proof about arbitrary uncontrolled environments.

## Why this obligation matters

The frame estimator previously returned a saved SU(2) matrix W, and the native model simply applied W† exactly. Statistical accuracy of W does not establish the accuracy or cost of implementing W†. Repeating that missing operation T times can dominate an otherwise protected channel. Here each saved W† becomes three explicit controlled pulses and their full duration and noise are paid.

## Classical compiler and pulse interface

For each site, remove an irrelevant determinant phase from the saved two-by-two unitary U=W†. Write U=Rz(a) Ry(b) Rz(c), where b=2 atan2(|U10|,|U00|), a=arg U10−arg U00, c=−arg U10−arg U00. The executable order is z(c), y(b), z(a). The source checks the compiled product against U up to global phase; the saved matrices here are away from the vanishing-entry singular chart. A general compiler would add the corresponding zero-entry branches rather than divide by those entries.

A pulse of angle theta on axis j lasts d=|theta|/Omega+s, with Omega=pi and switching allowance s=.2 reference units. During its entire interval the declared Hamiltonian is

H = [(1+epsilon) theta sigma_j + eta X]/(2d).

Thus nominal rotation speed is bounded by Omega. The switching allowance is included in the rectangular-pulse interval; it is not a separate zero-drive dead-time model. The multiplicative angle error epsilon and unwanted X rotation eta are declared physical parameters, not inferred from the learned frame. There is no instantaneous ideal rotation in this local pulse channel.

Independent Markovian Z dephasing acts simultaneously. In Bloch coordinates, the exact generator is cross(v)/d + diag(−lambda,−lambda,0), where v=(1+epsilon)theta e_j+eta e_x. Matrix exponentiation of this real three-by-three generator gives the full pulse map. This is the exact finite-dimensional solution of the declared Hamiltonian/Lindblad model, evaluated in floating arithmetic. It does not claim validity for an unknown bath with memory or a time-dependent, misidentified generator.

All five sites run in three synchronized layers. Layer k lasts the largest of the five actual pulse durations. Sites finishing sooner undergo dephasing for the remaining layer time. Hence even data not under active drive pay the same layer clock. The full fitted angles and actual durations are retained in the output.

## Native-source phase is a distinct effective model

Each compulsory native source use lasts one reference unit. Its supplied discrete CPTP map is followed by one unit of independent background dephasing. This is an explicitly declared sequential effective channel: it is NOT derived as simultaneous native-Hamiltonian-plus-dephasing evolution. The microscopic native generator remains unknown. A laboratory implementation would need to validate this effective phase or replace it with its measured composite action. The exact continuous-time claim applies only to the controlled pulse segments above.

The old model had a two-unit native/inverse phase with no background. The new phase lasts 1+sum(max_site pulse_duration_k), includes native-background composition and padded pulse-background exposure, and so must not be presented as unchanged earlier performance. In the zero-background, zero-control-error limit its native+inverse CPTP matrices agree with the earlier ideal-inverse model.

## Complete pipeline and resources

The source composes the explicit noisy encoder and actual noisy terminal syndrome decoder from `noisy_code_boundaries_20261028/boundary_channel_v2.py`. Four local preparations, 30 Clifford gates, four syndrome measurements, feedback and conditional output correction cost72 units. The bulk uses the actual clocked flagged EC map, retains physical syndrome leakage, and performs a full EC after every r native uses. At T uses the elapsed time is

72 + T*[1+sum_k max_i d_ik] + 201*(T/r).

The same five native carrier exposures per use and inherited frame-calibration charge remain. Pulse controls require a known single-qubit X/Y/Z control interface, bounded-angle command precision and the explicit error model; unknown-noise preservation does not imply unknown or uncalibrated control hardware can be ignored. Initial unknown-input injection is not made fault tolerant by this compiler.

A strong conventional strategy with the same saved frames, code and hardware can execute exactly this pipeline. The construction removes a previously omitted control operation; it establishes no new optimizer/code advantage. A comparison to one-carrier controls must use this changed clock and source model, and may grant them stronger ideal controls. No such numerical comparator result is silently inherited here.

## Evidence type

`pulse_pipeline_v1.py` compiles the saved matrices, checks zero-error equivalence and evaluates complete physical-output channels for epsilon=0,.001,.01, with eta=.001, native horizon32, cadence2 and background rate .03/201. These are deterministic finite-model calculations. They do not acquire a new environment model, perform fresh hardware calibration, or certify floating coefficients with interval arithmetic. Ordinary physical-qubit input/output testing can subsequently certify the composed channel under trusted/calibrated external SPAM; earlier ideal-logical holdouts cannot be reused for these changed maps.
