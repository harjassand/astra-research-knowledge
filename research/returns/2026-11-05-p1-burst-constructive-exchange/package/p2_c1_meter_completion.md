# Completed smooth finite-meter bridge for the original sine-arm intervention

## Result

The box-switch idealization has been removed. The same original-family intervention now uses continuous differentiable pointer couplings with explicit finite amplitude and slew. The source-force pulses were already C1. A new directed interval certificate establishes the complete sine-arm feasibility conditions uniformly for every normalized stiffness \(0\le k\le1/4\), retaining \(\eta=1/2\).

For each of the eight consecutive pointer windows of length \(1/8\), the coupling rises from zero to one over \(1/64\), stays at one for \(3/32\), and falls to zero over \(1/64\). On a rising edge with normalized local time \(v\in[0,1]\),
\[
g(v)=3v^2-2v^3.
\]
The falling edge uses its complement. The coupling and its first derivative match at every join. Its peak is one, its maximum slew is \(96\) in the normalized time convention, and its area per pointer is \(7/64\). These are explicit requirements on the coupling actuator. This is a bounded-slew C1 pulse, not a claim of strict Fourier band limitation.

All canonical pointer dynamics and source backaction remain included: \(H_{\rm int}=g(t)xP\), \(\dot Q=P/m+g(t)x\), and the source receives \(-g(t)P\). Initial pointer variances remain \(\operatorname{Var}Q=10^{-6}\), \(\operatorname{Var}P=10^{-2}\), mass100. The Langevin source bath remains active throughout. Source stiffness is never changed, and the hidden constant force is not identified.

## Exact ramp operation

This calculation does not discretize a smooth waveform and infer a continuum claim from sample points. An edge with physical duration \(L\) uses local time \(v=t/L\). Introduce integral states
\[
J_0'=x,\quad J_1'=J_0,\quad J_2'=J_1,\quad J_3'=J_2,
\]
all initially zero, and deterministic input states \(P,vP,v^2P,v^3P,F\). The complete deterministic state
\[
(x,p,J_0,J_1,J_2,J_3,P,vP,v^2P,v^3P,F)
\]
obeys a constant linear equation in \(v\). Its transition is an exact 11 by 11 matrix exponential. Repeated integration by parts gives the rising-edge pointer increment
\[
\int_0^L g(t/L)x(t)dt=L(J_0-6J_2+12J_3),
\]
and the falling-edge increment \(L(6J_2-12J_3)\). These identities hold pathwise for the source trajectory. The six dynamic states carrying thermostat noise yield their exact covariance through a 12 by 12 Van Loan exponential. Thus the smooth meter is reduced exactly to the same observation, endpoint-gain and covariance matrices used in the sine-arm theorem.

The constrained momentum cancellation, two-readout position correction with zero initial-position gain, independent tilted-Gaussian dither, and finite force pulses are unchanged. The original endpoint identity remains
\[
\mathcal L(A,p_T,x_T,Z,R)=\tfrac12 q_A(p_T)\,\mathcal L(x_T,Z,R),
\qquad q_A(p)=G_{\sigma^2}(p)[1+A\eta\sin(p/\sigma)].
\]

## Uniform certificate

The 100-piece directed interval computation at 40 decimal digits gives
\[
V/\sigma^2\le0.542831310263894,\qquad
\alpha=\tfrac12e^{V/[2(\sigma^2-V)]}\le0.905327082396364<1,
\]
and the determinant of the two-readout position correction is everywhere below \(-0.118702839995102\). The certificate defines a piecewise-rational candidate momentum predictor, corrected to satisfy its three initial-gain constraints exactly. It does not require interval inversion of the full correlated observation covariance.

The constrained-optimal point fixtures have \(V/\sigma^2=0.428724\) at \(k=0\) and \(0.427372\) at \(k=1/4\), with tilted-dither amplitude about0.728. Their normalized expected source-force action for \(D_0=1\) ranges from13,324 to23,324. Those point-action numbers describe the constrained-optimal fixtures; the uniform certificate uses its own explicit candidate predictor. The latter has finite bounded action on the compact stiffness interval because all inverses have certified nonzero denominators and its position displacement has exactly zero initial-position gain. No energy optimum or calibrated numerical uniform action bound is asserted.

An independent full19-state time-varying ODE, including the canonical pointers and their initial noises, agrees with the lifted exact formulas at \(k=0.1\): maximum covariance discrepancy below \(2.6\times10^{-11}\), gain discrepancy below \(10^{-15}\). Directed intervals provide the continuum result; this independent ODE calculation checks the different representation. There were zero hardware trials.

## Scope still paid

The nominal1.1/γ window is the specified coupling-plus-force schedule. It assumes the completed pointer observation is available when the source-force window begins. Real readout and control latency must be accommodated causally, not merely added to a calendar after fixing the endpoint covariance. One valid design strategy is to reserve an initial idle subinterval inside the final0.1/γ prediction window and run the two force pulses only after the result becomes available. This keeps the same total source-noise prediction horizon but increases actuator action; any continuing pointer free drift or added readout noise must be included in the observation matrices and checked again. The present certificate does not supply an ADC latency or precision specification for a laboratory device.

Initial pointer preparation, actual cold-reservoir availability, finite sensor range, metrology/calibration acquisition and drift, finite arithmetic, dither generation, pointer isolation/reset and reuse remain as stated in the main note. Finite-slew control is now a proved model ingredient; those other resources are not silently supplied by the proof. The calibration model and bounded moment assumptions determine campaign accuracy, while a real calibration experiment determines calibration time. The exact channel identity applies for an arbitrary initial classical law and old reference within the affine constant-force plant class. It is not a universal nonlinear apparatus theorem.

## Files and reproduction

- `p2_c1_direct_sine_arm.py`: C1 fixture and interval-certificate driver.
- `p2_c1_direct_sine_arm.json`: constrained-optimal point fixtures and action.
- `p2_c1_direct_sine_arm_interval.json`: complete100-piece interval certificate.
- `p2_slew_direct_sine_arm.py`: exact ramp operations and shared proof calculation.
- `p2_smooth_meter_validation.py` and `.json`: independent full-state validation.

Run `python3 p2_c1_direct_sine_arm.py`, `python3 p2_c1_direct_sine_arm.py --interval --pieces 100`, and `python3 p2_smooth_meter_validation.py` in this directory. The continuous piecewise-linear alternative is also preserved with maximum slew64 and its own certificate; the C1 version supersedes it for the stronger smooth-control statement.
