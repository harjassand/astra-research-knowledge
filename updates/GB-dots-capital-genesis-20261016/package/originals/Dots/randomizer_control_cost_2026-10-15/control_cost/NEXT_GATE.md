# Exact next gate

## Mathematical gate

Freeze one bounded parent gadget and one fixed deterministic M-cell schedule. Supply its COMPLETE intended and actual dilation, including initial frame, every internal ramp, final inverse, private frame register, any syndrome/reset records, ambient joint coupling, and all physical supports/time windows. Choose one of two routes:

1. Certify the full causal CP decomposition R=(1-epsilon)R0+epsilon R1 with exact reference R0 and state-independent scalar weights. Demonstrate that it remains valid after arbitrary allowed prior histories and outside-parent faults. This is not expected for a generic coherent unitary error.
2. Certify H_actual=H_reference+sum_i R_i in one common frame, with each R_i depending only on its own private variables; bound the FULL joint residual action; and establish initial-frame conjugation covariance on the complete error support. Verify every deletion/interpolation used by the proof. For finite-width internal ramps, explicitly show U_control(t)=C_eta(t)g0, C_eta independent of initial g0, and exact endpoint inverse. Handle imperfect initial/final wrappers separately rather than recursively assuming perfect outer wrappers.

Then prove the zero-character memory support certificate on that exact full support, and insert the charged p and actual total tau into the recomputed whole-gadget contour budget. Stop if any controller term reads another selected seed, any uncharged bath map depends on private frames, any random schedule escapes its fixed reservation, or any zero-character residual acts nontrivially on memory.

## Experimental/model-identification gate

Ordinary randomized benchmarking or average gate infidelity cannot identify either full-process premise. The smallest useful empirical input is a specified finite-dimensional device/controller model with justified joint residual norm/action bounds (or a justified causal stochastic fault mechanism), together with waveform timing/support and an explicit privacy/record-access model. Check those bounds over all allowed initial bath/controller states or state the strictly weaker preparation scope.

Only after those inputs exist, evaluate the symbolic inequalities using measured/qualified values and actual pulse-width dependence. No numerical hardware parameter is assumed in this note. If only isolated reduced-channel calibration is available, report the remaining gap rather than converting it into the required CP probability or joint action.

## Bounded stopping condition

This research pass ends after the conditional algebra, independent audit, explicit obstructions and self-authored finite checks. It does not run author code, request hardware access, install software, contact researchers, or alter the previous canonical theorem packets.
