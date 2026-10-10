# Paired phase encoding through an uncalibrated detector

## Status

**Closed as a transformative-invention candidate.** The exact identity and finite
certificate below are valid under their assumptions. However, ratio-to-phase
conversion, ideal sinusoidal nonlinearity cancellation, and reversed-channel
phase comparison all have close explicit antecedents. Extending the statement
to arbitrary time-equivariant periodic dynamics does not establish an exceptional
new practical capability. A small synthetic check is retained, without a
hardware or originality claim.

## Native measurement model

The unknown scalar x is positive and constant during a measurement pair. Two
calibrated controls create inputs to the *same* detector:

z_+(theta) = (lambda_0 + b cos(theta)) x + a(1+sin(theta)),
z_-(theta) = (lambda_0 + b cos(theta)) x + a(1-sin(theta)),

where a,b>0 and b <= lambda_0 <= 1-b. Thus attenuation remains in [0,1], and
the additive pilot is nonnegative. A constant unmodulated background can be
absorbed into the common DC value. Units come from the pilot amplitude a;
this is not measurement without any standards or calibrated actuation.

The putative optical capability is intensity measurement through an unknown,
nonlinear, delayed detector, using a controllable attenuator and added reference
light. The construction does not by itself validate a practical attenuator,
reference source, optical mixing path, switching bandwidth, or stable scene.
It cannot be applied to a generic chemical state just by naming a dilution and
a spike: intervening on all nuisance components changes the measurement model.

## Exact identity, including nonlinear detector memory

Set c=lambda_0 x+a, R=sqrt((b x)^2+a^2), and
phi=atan(a/(b x)) in (0,pi/2). Then

z_+(theta)=c+R cos(theta-phi),
z_-(theta)=c+R cos(theta+phi).

Assume the detector is time-translation equivariant and has a unique settled
2pi-periodic response g(theta) to c+R cos(theta). The two settled outputs are
therefore g(theta-phi) and g(theta+phi), even if the detector is nonlinear and
has memory. Define the first Fourier coefficient by

Y = (1/(2pi)) integral_0^(2pi) y(theta) exp(-i theta) dtheta.

If H is the coefficient of g, then

Y_+ = exp(-i phi) H,
Y_- = exp(+i phi) H.

When H is nonzero,

arg(Y_- conjugate(Y_+)) = 2 phi in (0,pi),
x = (a/b) cot(phi).

This follows directly by shifting the integration variable. Unknown gain,
static response curve, dynamic phase lag, and common DC response cancel. The
hypotheses exclude drift between scans, nonunique steady responses, uncharged
transients, and loss of the informative harmonic. Mere time invariance does not
guarantee a unique T-periodic response: subharmonic or chaotic outputs require
separate treatment.

For a memoryless increasing nonconstant response, the fundamental is positive
relative to the input phase. For arbitrary memory or nonmonotone response, it
may vanish. The method must refuse a numerically uninformative measurement.

## A finite-data conditional certificate

For each settled output assume an independently justified bound

|y(theta)-y_center| <= M,
TV(y; one period) <= V.

With N equally spaced phase samples, the centered complex Fourier average
has deterministic quadrature error at most

eta_quad = (V + 2pi M)/N.

Proof: the variation of (y-y_center) exp(-i theta) is at most V+2pi M. On each
partition interval the difference between its integral average and the sampled
value is bounded by the variation on that interval. Summing and normalizing
proves the displayed bound. This explicitly charges aliasing; arbitrary bounded
waveforms alone provide no finite deterministic quadrature guarantee.

Add independently valid bounds for bounded measurement noise, residual
settling, digital accumulation, and device drift. For example, a pointwise
noise/settling bound nu adds at most nu to eta. Finite phase timestamps also
need a quantified rule: one actual sample inside each quadrature cell still
obeys the tagged-quadrature bound, and a reference-angle error at most delta
adds at most M delta when forming the complex weight. Imperfect *input*
waveforms are a different issue and do not follow from this clock statement.

Suppose resulting disks satisfy

|Yhat_+ - Y_+| <= eta_+,
|Yhat_- - Y_-| <= eta_-,
eta_+ < |Yhat_+| and eta_- < |Yhat_-|.

Then define

phihat = 0.5 arg(Yhat_- conjugate(Yhat_+)),
e_phi = 0.5 [arcsin(eta_-/|Yhat_-|) + arcsin(eta_+/|Yhat_+|)].

On the correct physical branch, phi lies in the resulting interval intersected
with (0,pi/2). If its endpoints are phi_low,phi_high, the concentration/intensity
interval is

[(a/b) cot(phi_high), (a/b) cot(phi_low)].

An endpoint at zero gives no finite upper bound. If calibrated a and b have
interval uncertainty, replace the lower factor by a_low/b_high and the upper
factor by a_high/b_low. A branch crossing or a disk containing zero requires
refusal or additional measurements, not an invented point answer.

For a static monotone map into [0,1], centered M=1/2 and V<=2 are valid. A
positive unit-mass LTI convolution, including a causal low-pass cascade and
fixed delay, preserves these range/variation bounds. They do not automatically
hold for every nonlinear dynamic detector covered by the exact identity.

## Critical end-to-end limitations

1. **The paired waveforms must be actual phase shifts, not merely nominally so.**
   A small mismatch in analog actuator shape, gain, or timing need not induce
   a small output error for an arbitrary unknown nonlinear detector. A validated
   incremental-stability bound could convert input mismatch to output error,
   but cannot be assumed free. One can construct time-equivariant systems with
   amplitude-dependent delay that magnify tiny amplitude mismatch arbitrarily.
2. **Settling is part of acquisition.** There is no uniform settling-time bound
   for an otherwise arbitrary unknown stable detector. Observing similar cycles
   is a useful diagnostic but is not a rigorous bound on hidden slow state.
3. **The first harmonic needs usable magnitude.** Suppression or saturation can
   force arbitrarily many samples or complete refusal. Pilot/signal imbalance
   makes the cotangent inversion poorly conditioned near branch endpoints.
4. **x and detector behavior must remain stable across the pair.** Output drift
   that mimics a phase shift is indistinguishable without additional assumptions.
5. **Controls and data are physical resources.** Each result requires two settled
   scans, N output samples per scan, a calibrated additive pilot, calibrated
   modulation depth b, and phase-coherent waveform generation. O(N) digital
   postprocessing is cheap; it is not the dominant unproved engineering task.

## Small arithmetic check

`check_phase_identity.py` tests 12 combinations: four positive x values and
three unknown-response fixtures (sigmoid, clipped affine, and threshold), each
followed by a common second-order low-pass response and pure delay. A 65536-point
reference grid generates the synthetic periodic traces; 4096 samples per scan
are retained, with bounded noise of magnitude 0.0002. The calculation takes
under a second on one native CPU thread.

Maximum observed relative error was 0.0001643. All displayed conservative
intervals contained the true x; the widest was about 44.5% of x because of poor
pilot balance. The interval calculation includes an explicit 0.0001 allowance
for reference-grid simulation. That allowance is not a formal FFT rounding or
truncation proof. These are reproducible arithmetic sanity checks, not formal
numerical certificates or experiments on sensors. No inference about practical
speed, accuracy, or advantage over established instruments is supported.

## Direct prior boundary

- **M. Katsura (2015), “Nonlinearity error reduction in signal ratiometry by
  ratio-to-phase conversion,” Measurement Science and Technology 26, 125011.**
  https://doi.org/10.1088/0957-0233/26/12/125011
  Author manuscript: https://ir.library.osaka-u.ac.jp/repo/ouka/all/54384/MST_26_125011.pdf
  Section 2.2 already describes ideal harmonic removal yielding a sinusoid whose
  phase is unaffected by the detector's static nonlinearity, and exact ratio
  recovery in that ideal case. Figure 5/Eq.7 exchanges input signals between
  channels and uses their phase difference. Section 2.3 emphasizes the
  difficulty of realizing the ideal filter, then treats finite harmonic
  cancellation. Thus neither ideal continuous-wave cancellation nor paired
  phase comparison is new here. The general time-equivariant-memory statement
  above is not claimed to appear verbatim in that paper.
- **US patent 4,453,225 (1984), “Counteracting the effect of phase shift changes
  between two quantities in extracting their ratio.”**
  https://patents.justia.com/patent/4453225
  The publication explicitly reverses the order of signal portions so leading
  and lagging contributions cancel phase-shift effects. This is an additional
  prior architecture, not evidence of this precise arbitrary-dynamics theorem.
- **Midgley and Gatford (1990), known addition-dilution titration potentiometry.**
  https://doi.org/10.1016/0026-265X(90)90048-A
  Already uses spiking followed by dilution to restore the original response,
  with matrix matching required. The earlier derivative-ratio idea in this
  investigation is not a new invention merely because it avoids fitting h.
- **Bussgang (1952), amplitude-distorted Gaussian crosscorrelations.**
  https://dspace.mit.edu/entities/publication/b7c1301f-be07-4a37-8f9f-617b80813b86
  An older baseline for nonlinear-response cancellation via symmetry and
  correlation. The deterministic circular-phase construction here does not
  require Gaussian probes, but symmetry-based cancellation is longstanding.

The search was targeted and not an exhaustive patent or novelty analysis. The
close positive collisions are already sufficient to withhold an originality
or transformative-capability claim. The candidate is closed at this scope.
