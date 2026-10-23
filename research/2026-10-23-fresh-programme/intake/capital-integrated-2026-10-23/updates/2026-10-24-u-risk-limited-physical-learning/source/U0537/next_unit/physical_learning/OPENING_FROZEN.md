# Independent opening: acquired local learning in a reciprocal physical network

24 October 2026, frozen before mechanism-specific primary-source comparison.

Missing operation: train a real, reciprocal resistor/conductance network from
boundary input/target examples without an externally computed Jacobian, a
supplied internal gradient oracle, or an ideal material law that already
contains the desired update. The operation must actually change and retain
conductances, with the input/output teacher, internal local circuitry and
reset/hold work visible. This is distinct from a matrix-query learner or
mere fitting of a simulation.

Proposed central mechanism: one physical network receives its ordinary input
and a small sinusoidally modulated output-error current at frequency Omega.
In the slow-drive limit the response is v_e(t)=v_e,free + epsilon v_e,adj cos
Omega t. A local squared-voltage detector followed by synchronous weighting
with the same cosine extracts

    <cos(Omega t) v_e(t)^2> = epsilon v_e,free v_e,adj.

For a reciprocal network and the correctly signed teacher-current boundary,
the product is the conductance derivative of the output loss. A local
integrator can therefore update a controllable conductance from this measured
correlation. This identity is only the starting mechanism: finite electrical
settling, teacher feedback, detector noise, integration bias and update-rate
separation can defeat the claimed operation.

Concrete prospective interface: standard voltage-controlled conductances or
switched resistor cells plus a local analog squarer/mixer/integrator at each
trainable edge; measured output voltages and an explicit error-current
injection circuit; a common clock and sample/hold phase; fixed conductance
bounds and retained settings. These active local cells are not a free
passive material. Their power, area, initialization, calibration and state
retention are charged. A material-only law cannot silently replace them.

The first bounded construction should use a fully specified linear reciprocal
network and one input/output training task, with one finite-amplitude,
finite-frequency acquired update and the actual loss decrease (or failure)
computed. It must include the hardware teacher gain and the fact that the
teacher itself sees the modulated output. A programmed independent adjoint
voltage source would be a supplied oracle and is not allowed as acquisition.

Strong incumbents: ordinary numerical adjoint/backpropagation on the same known
network, hardware-in-the-loop calibration, two-phase/single-copy equilibrium
propagation, and two-copy coupled learning with local contrastive voltage
updates. The correlation mechanism may already be conventional; no new
learning rule, analog advantage, or intelligence capability is presumed.

Full cycle/resource discriminator: count all boundary measurements, output
feedback currents, local squared-voltage sensing and phase integration,
conductance programming/holding, time to settle and integrate, clock work,
driver bias/rail power, training examples, and final held-task error. Compare
at identical target error/retained settings and noise/latency assumptions,
not just arithmetic operations or ideal Joule power in the resistor mesh.
No hardware purchase, laboratory action, outreach or disclosure is authorized.

Kill gates: a direct conventional implementation already supplies the same
operation; the proposed local circuit merely hides internal gradient sensing
or an unavailable multiplier/material law; teacher feedback changes the
quantity being learned; finite-frequency response loses reciprocity/gradient
sign; or the same-resource conventional method wins. A correct gradient
identity alone does not establish an acquired physical learning capability.
