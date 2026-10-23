# Amended construction: finite-carrier reciprocal adjoint acquisition

The original continuously nudged, one-copy squared-voltage lock-in mechanism
is conventional Frequency Propagation (Anisetti et al., arXiv:2208.08862;
Neural Computation 36, 596–620, 2024). Its basic learning-rule novelty is
retired. This is a subsequent construction using ordinary complex adjoint
network physics. It changes the teacher from continuous error feedback to a
sampled-and-held free-output error and explicitly adds three settled epochs.
It is not the same original protocol or a newly claimed learning principle.
It also changes the objective to the network's complex response at its actual
carrier frequency. It does not recover the original DC inference gradient
using an arbitrarily fast modulation probe, and is not a speedup comparison
against a DC trainer on an unchanged task.

Let a grounded passive linear RC network have real symmetric A(g)>0 and
C>=0, with fixed current input phasor b, angular frequency omega, and

    H=(A+i omega C)^(-1), v=H b,
    e=P v-y, L(g)=0.5 e^H e.

Trainable edge e has grounded incidence vector be and dA/dg_e=be be^T. The
ordinary derivative is

    dL/dg_e = -Re[(be^T lambda)* (be^T v)],
    lambda=H^H P^T e.

Reciprocity makes H symmetric, so H^H=H*. With an explicit output-teacher
transconductance kappa_T (siemens), inject kappa_T P^T e* at the same carrier
frequency through the same physical network. Its response w=H kappa_T P^T e*
satisfies w*=kappa_T lambda. Consequently

    dL/dg_e = -Re[v_e w_e]/kappa_T.

Neither H nor a supplied internal adjoint is used by the update operation.
The teacher does require measured free output I/Q values, the target and a
phase-conjugating current driver. This is physical forward/adjoint measurement,
not free passive computation.

An exact finite-probe linear implementation uses three epochs at fixed g:

1. Measure the free output at b and hold e=Pv-y.
2. Apply b+epsilon kappa_T P^T e*; locally measure squared-voltage 2omega
   coefficient Qplus=Re[(v_e+epsilon w_e)^2].
3. Apply b-epsilon kappa_T P^T e*; similarly measure Qminus.

Then -(Qplus-Qminus)/(4 epsilon kappa_T) is exactly the conductance gradient
for this linear model, for every nonzero finite epsilon. In each epoch,
q(t)=Re[z exp(i omega t)] has Q=4<q(t)^2 cos(2 omega t)>=Re(z^2). Ordinary DC
squared-voltage readout gives |z|^2/2 and is the wrong complex product. The
two probe phases must hold the sampled free error; continuously substituting
the perturbed output changes the circuit and invalidates this cancellation.
Conductances are held during probing and updated only afterward.

Fixed replay fixture, normalized units (not fitted device data): two free
nodes with shunts g1=1, g2=2 and link g12=0.5, C=diag(0.25,1), b=(1,0),
omega=4, P=(0,1), target y=0.1-0.05i, kappa_T=1, epsilon=0.2. One projected
gradient update uses eta=1 and bounds 0.1<=g_e<=4. Map to illustrative physical
units with G*=1 mS, C*=1 microfarad and V*=1 V: g_e=G* times normalized g,
C=C* times normalized C, b=G*V* times normalized b, and carrier frequency
omega G*/C* (about 637 Hz). This scaling is a layout target for ordinary
active electronics, not a validated component choice or cost advantage.

The desired acquired operation is finite-frequency calibration/learning of
the actual reciprocal network without identifying all its internal A,C.
Its price is boundary I/Q sensing, an explicit phase-conjugate current
teacher, free-error sample/hold, local 2omega square/lock-in detection, a
stored local contrast, three settling/integration epochs and conductance
programming/retention. Settling time and noise still matter; a fast carrier
does not imply arbitrarily fast or low-energy learning. Local active cells
must be compared with ordinary two-phase physical adjoint, numerical adjoint
and existing coupled-learning electronics at the same retained task error.

Scope is linear reciprocal networks with fixed capacitors. Nonreciprocal
couplings lose H^T=H; nonlinear/time-periodic operating Jacobians require a
different adjoint operation. No bench implementation, new priority, or
practical advantage follows from a simulated three-epoch replay.

## Replay and conventional comparison

`phasor_acquisition.py` executes the frozen virtual operation. The local
2omega measurements recover the three exact gradients to about 2e-17 absolute
arithmetic error and agree with an independent finite-difference check. One
programming step lowers loss from 0.0053879310 to 0.0053799109 (0.1489%). This
is one valid update, not evidence of task convergence or general learning.
At the illustrative physical scaling, 32 periods per epoch give 0.151 s for
three update epochs and another 0.0503 s to verify the retained free-output
loss. Mesh-only steady integration is 34.1 microjoule, or 45.4 microjoule with
verification; settling, active sensing/teacher, clocks, programming/retention
and reset are explicitly excluded, not assigned zero cost.

A directly relevant acquired ancestor is [Pai et al., Science 380, 398–404
(2023)](https://doi.org/10.1126/science.ade8450). It measures photonic adjoint
gradients and sum/difference power contrasts; analog update logic was tested
on one phase shifter. The larger classification experiment used camera tap
monitoring, off-chip nonlinearities and digital updates. This is strong prior
for the general interference/contrast operation, without establishing a fully
autonomous local trainer or a complete energy advantage for this RC variant.

The standard-parts resource worker specified a separate one-edge, 1 kHz
AD5292/AD633 cell. It is not this two-node replay and its costs must not be
spliced into an actual measured device claim. Three AD633s alone draw about
0.36 W typical under the chosen supply, before teacher/program/clock costs;
the raw contrast is sub-millivolt, requiring calibration and drift control.
AD5292 training can change volatile settings while powered, but its permanent
state uses a 20-commit nonvolatile memory budget. This is a limited retention
resource, not unlimited reusable learned material. Those component choices
are one constructive circuit specification, not a universal lower bound on
physical learning. No measured update accuracy, device resource win or new
learning-rule priority has been established in this unit.
