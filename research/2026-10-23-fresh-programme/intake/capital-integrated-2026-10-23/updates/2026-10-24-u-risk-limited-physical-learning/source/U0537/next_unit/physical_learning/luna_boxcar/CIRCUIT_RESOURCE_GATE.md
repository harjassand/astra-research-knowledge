# One standard-parts cell for reciprocal phasor-square learning

## Bounded result

The finite-frequency identity can be implemented with ordinary analog
multipliers, a digitally programmable resistor and a small I/Q controller.
For one edge, the calculation below returns the analytic loss gradient to
about $2.1\times10^{-14}$ relative error and one 10-bit conductance step
lowers the example loss. This is an executable circuit model, not a built
device result.

The construction does acquire an edge-local correlation from the physical
network. It does not show an advantage over ordinary local gradient sensing
plus numerical updates: the teacher measures the boundary error and computes
its complex conjugate, the controller stores plus/minus I/Q lock-in values per
edge, subtracts them and chooses a conductance code, and the same weight sees
three separate network epochs per example. The exact identity is a physically
realizable adjoint-gradient measurement, not evidence of faster or lower-energy
learning.

## Cell and boundary circuit

Use one trainable 100 k\(\Omega\) AD5292 digital rheostat in series between a
sinusoidal input source and one output node. Connect a 100 k\(\Omega\) load and
1 nF capacitor from the output node to ground. This is a reciprocal one-node
RC network. At the carrier frequency \(f=1\) kHz its output-node admittance is

\[
Y=g+g_0+i\omega C,
\qquad y=\frac{g V_{\rm in}}{Y},
\qquad v_e=V_{\rm in}-y.
\]

The task uses peak phasors \(V_{\rm in}=10\) V and \(y^*=6-i\) V, with loss
\(L=|y-y^*|^2/2\). A high-input-impedance differential buffer senses the
trainable edge voltage so the measurement circuit does not become a material
part of the edge conductance. The buffer transfer and all input capacitance
still require calibration.

The boundary teacher has three ordinary steps. It measures free-run output
I/Q, subtracts the programmed target phasor, and holds \(e=y-y^*\). A
controller conjugates the stored phasor by reversing the sign of its Q
component. A DAC and output transconductance stage inject the two probe
currents

\[
I_\pm=\pm\epsilon g_T e^*,
\]

at the output node, where \(g_T\) is an explicit calibrated teacher
transconductance, treated as real at the carrier in the equations below. Its
amplitude and phase must be measured; any driver phase lag must be included in
the injected phasor. The teacher holds the error measured in the free epoch
through both probes; it must not recalculate the error from the probe-perturbed
outputs. If it does, the boundary source becomes a feedback network and the
identity below changes. The error is therefore measured from the actual
network, not supplied as an adjoint oracle, but I/Q acquisition, conjugation,
sample-and-hold and output-current generation are charged electronics.

For a reciprocal linear AC network \(H=Y^{-1}=H^T\), let \(w_e\) be the
local edge-voltage response to the held output-error current. The two states
are \(v_{e,\pm}=v_e\pm\epsilon w_e\). Their complex phasor squares obey the
finite-difference identity

\[
\frac{v_{e,+}^2-v_{e,-}^2}{4\epsilon}=v_e w_e,
\qquad
\frac{\partial L}{\partial g_e}=-\frac{1}{g_T}\Re(v_e w_e)
=-\frac{1}{4\epsilon g_T}\Re(v_{e,+}^2-v_{e,-}^2).
\]

Here \(w_e\) includes the factor \(g_T\). No small-\(\epsilon\) approximation
is used in this identity: it is exact for a linear network so long as the
measured probes are symmetric and the weights are held fixed during the three
epochs. Finite frequency is also allowed; the complex network response must
settle to the same periodic state in each epoch.

The local detector first forms the actual instantaneous square of the edge
waveform, then extracts its **complex 2\(\omega\) component**. With the peak
phasor convention

\[
v_e(t)=\Re(\tilde v_e e^{i\omega t}),\qquad
v_e(t)^2=\frac{|\tilde v_e|^2}{2}
+\frac12\Re(\tilde v_e^2e^{i2\omega t}).
\]

The DC term \(|\tilde v_e|^2/2\) is not the gradient signal. A band-pass and
gain stage at 2\(\omega\), followed by cosine and sine lock-ins, yields I/Q
estimates of \(\tilde v_e^2\). At this fixture's nominal edge voltage, a
2\(\omega\) amplitude of about 1.05 V can be given gain 8 before mixing; this
keeps the peak below 8.5 V while lifting the +/− lock-in difference from
about 0.7 mV to about 5.5 mV. The two estimates from the + and − probes are
held, digitally subtracted, and scaled by the known \(\epsilon\) and \(g_T\).
Using only a DC square detector would lose the phase information and generally
give the wrong gradient for this complex RC state.

## Concrete component count and interface costs

For each trainable edge, the proposed cell contains:

- one AD5292BRUZ-100, used in rheostat mode, for the actual edge conductance;
- three AD633 multipliers: one squares the buffered edge voltage, and two
  multiply its 2\(\omega\) component by the common cosine and sine references;
- one high-impedance differential edge buffer, a shared 2\(\omega\) band-pass,
  two low-pass/integrator channels with hold capacitors, and mux taps to a
  shared dual-channel ADC;
- a local 1 \(\mu\)F AD5292 EXT_CAP capacitor, edge calibration constants,
  and a serial update connection to the controller.

The AD633 transfer is \(W=(X_1-X_2)(Y_1-Y_2)/10\,\mathrm V+Z\). The three
multiplier packages are 8-lead SOICs; their package outline alone occupies
about 93 mm² of board footprint before pads and spacing. An AD5292 is one
14-lead TSSOP. The 100 k\(\Omega\) version has 1024 taps and a specified ±1%
end-to-end resistance tolerance in resistor-performance mode; the calculation
uses its ideal tap law only. Including this package, a high-Z buffer, op-amps
for the I/Q filters/holds, passive filter and integration components, and
routing, a first-placement allowance of roughly 20 × 20 mm (4 cm²) per
trainable edge is reasonable but is not a PCB layout. The core scales as three
multiplier packages and one programmable resistor per edge, so a network with \(E\) trainable edges requires at least
\(3E\) multipliers, \(E\) rheostats, and \(O(E)\) local filters, holds and
interconnect.

At ±15 V rails, each AD633 is specified at 4 mA typical and 6 mA maximum
quiescent current; budgeting both rails gives about 0.12 W typical or 0.18 W
maximum per multiplier. Thus the three multipliers alone use approximately
0.36 W typical, up to 0.54 W by this conservative rail-power calculation,
per adjustable edge. This omits the buffer, op-amp, ADC, controller, DAC,
clock, output driver and the AC network. The multiplier bandwidth is 1 MHz;
the chosen carrier is 1 kHz and the lock-in reference is 2 kHz, far inside
that limit. The AD633's specified output offset is ±5 mV typical and ±50 mV
maximum, while the example's unamplified +/− lock-in difference is below
1 mV. A calibrated zero, differential phase-pairing and drift/noise check are
therefore part of the operation, not optional refinements. These AD633
package, bandwidth, noise, offset and supply values are from the [manufacturer
datasheet](https://www.analog.com/media/en/technical-documentation/data-sheets/AD633.pdf).

The boundary and controller are shared across edges but not free. They need
an input source, target-phasor storage, one synchronized output ADC channel
for digital I/Q measurement, an ADC/DAC path for the teacher current, a
calibrated voltage-to-current driver, a master carrier and 2\(\omega\)
reference, reference fanout, phase calibration, a clock, integrator reset/hold
control, and enough memory to hold
each edge's two + and two − I/Q lock-in scalars (one complex-square result for
each probe).
The current source must synthesize \(\epsilon g_T e^*\) with the required
complex phase; a scalar DC error amplifier is insufficient. For a large mesh,
the common reference fanout and output-current injection layout need explicit
stability and crosstalk checks.

## One finite-carrier check

The executable model uses AD5292 code 683 under its ideal tap law (wiper
resistance omitted), giving \(R_e=66.699\) k\(\Omega\) and
\(g=14.9927\) \(\mu\)S. The load is \(g_0=10\) \(\mu\)S,
\(C=1\) nF and \(f=1\) kHz, so \(\omega C/(g+g_0)=0.2514\): the state is
not treated as an adiabatic DC response. At the selected input and target,

\[
y=5.6422-1.4185i\;\mathrm V,\quad
e=-0.3578-0.4185i\;\mathrm V,\quad
v_e=4.3578+1.4185i\;\mathrm V.
\]

With \(g_T=10\) \(\mu\)S and \(\epsilon=0.1\), the held conjugate error
produces a signed teacher-probe current of magnitude 0.55 \(\mu\)A peak.
The complex-square difference is
\(0.27424-0.27958i\;\mathrm V^2\). The two AD633 lock-ins return an
unamplified difference of
\(0.6856-0.6989i\;\mathrm{mV}\), after the known \(1/400\) scale factor.
Applying the calibrated scale gives
\(\partial L/\partial g=-68{,}560.52\;\mathrm{V^2/S}\), matching the
direct analytic derivative to relative error \(2.1\times10^{-14}\) in the
ideal arithmetic check.

The update is quantized rather than an ideal continuous memory law. One
descent step from AD5292 code 683 to 682 raises ideal conductance to
15.0147 \(\mu\)S and lowers this one-example loss from 0.15156 to 0.15006.
The RDAC code can be changed serially during powered training; writing the
final setting to its one-time-programmable nonvolatile memory consumes one of
20 permanent-write opportunities. If the final value is not committed there,
power cycling restores the previously committed setting. The actual mapping
from code to conductance must be calibrated including wiper resistance,
resistor tolerance, terminal parasitics and update glitch. The tap count,
tolerance, SPI control and 20-time-programmable memory behavior are specified
in the [AD5291/AD5292 datasheet](https://www.analog.com/media/en/technical-documentation/data-sheets/ad5291_5292.pdf).

At the model's 1 kHz, the output-node RC settling constant is about 40 \(\mu\)s
and 5\(\tau\) is 0.20 ms. Averaging 100 carrier cycles per free, + and − epoch
sets the nominal update time at about 0.30 s per training example, before ADC
and SPI time. Each example must also reset the lock-in capacitors, resample the
free-run output after the previous conductance update, and wait for the next
periodic response before its probes. All edges can acquire in parallel, but
the analog circuitry scales linearly with edge count. The passive example network itself consumes
only about 0.33 mW of real AC power; the three local multipliers' estimated
quiescent power is hundreds of milliwatts per edge. At a 0.30 s update, that
is roughly 0.11 J per edge in multiplier quiescent power alone, versus about
0.10 mJ dissipated in the passive network across the three epochs. The circuit
therefore does not present a low-energy win in this fixture.

The reproducible arithmetic is in [`cell_check.py`](cell_check.py), with
machine-readable values in [`cell_check.json`](cell_check.json). It verifies
the complex-square identity and the one-code loss decrease; it does not model
AD633 noise, frequency-dependent phase error, AD5292 wiper resistance,
op-amp settling, board crosstalk or a learned multi-example task.

## Comparison and kill gate

The strongest useful comparator is numerical adjoint/backpropagation on the
same measured network, plus conventional two-phase or hardware-in-the-loop
updates. Those approaches already obtain a local derivative from calibrated
network parameters or paired perturbation measurements. The present cell's
potential distinction is that reciprocal physical response supplies the
adjoint-shaped voltage field without a separately programmed internal
adjoint voltage source. Its cost is three physical epochs, a held I/Q teacher,
three multiplier ICs per edge, local phase-sensitive sensing and a quantized
state update. This one-edge fixture is too small to establish any scaling,
latency, robustness, energy or generalization advantage.

The operation fails its present resource gate if the +/− complex-square
difference cannot be separated from multiplier offset/drift, if measured
edge loading or phase lag changes the sign, if teacher I/Q error is stale by
the time probes run, or if a full network requires more local electronics and
calibration than the numerical/two-phase comparator. No general learning
claim follows from this circuit identity.

