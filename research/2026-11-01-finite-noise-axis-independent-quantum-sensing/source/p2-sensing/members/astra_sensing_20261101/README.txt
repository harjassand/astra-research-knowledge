ASTRA FRESH INVESTIGATION — 1 NOVEMBER 2026
Quantum sensing without calibrating the noise axis

MAIN RESULT
===========
In the specified model, an unknown transverse noise direction need not be
estimated to obtain quantum-enhanced frequency sensing. Let noise events take the
sensor into and back out of a parity error sector. Equal successive unknown flips
cancel. A finite meter observes how long the system occupies those sectors, and
feedback changes the scalar noise rate so useful signed signal exposure grows
linearly with time.

The construction includes sensor noise during finite two-body interactions,
measurement, readout, reset and feedback latency. The actual final statistic
removes the unknown static axis for every signal frequency. At the controlled
working point it has classical Fisher information C T^2 with explicit C>0.
A multiscale interval estimator promotes this to inverse-total-sensing-time
high-confidence frequency accuracy if a physical Z counterdrive preserves the
admitted noise and measurement model. The estimator needs only coarse gain bounds.

STRONGEST IMPLEMENTATION TRADE
=============================
Two routes are proved. A constant-hardware reference coherently erases logical
information from each meter using one finite controlled-Z before erroneous
classical readout. An alternative removes that entangling eraser entirely:
use the first noisy report for feedback, retain and repeatedly QND-read the
decoupled meter, and apply the known logical Pauli correction only to the final
classical output sign after its record is accurately decoded.

The latter route needs O(log(M/alpha)) concurrent meter/readout capacity and
O(M log(M/alpha)) total report work for M cycles. Its critical premise is stable
meter Z populations during repeated readout, or an independently supplied protected
classical record. A perfect first measurement is not assumed; actual terminal
meter discard supplies the latent classical representation.

WHAT IS ESTABLISHED HERE
=======================
* Exact fixed-rate nuisance obstruction and a conventional strategy attaining its
  limiting coefficient, even when event flags are accessible.
* Exact cancellation of static unknown jump phases on returned error trajectories,
  including unknown inputs and untouched reference correlations.
* An explicit finite two-body meter, exact four-state transfer matrix and positive
  signed-exposure rate with finite latency and constant report errors.
* A two-setting local Pauli readout that needs no perfect final parity herald.
* A constructive global frequency interval algorithm, with actual acquisition,
  counterdrive assumptions, confidence bounds and sensor-time cost.
* An optional delayed-frame implementation and its read-work/hardware costs.
* A cyclic higher-dimensional generalization, stopping-time bounds, useful failures,
  full-cost conventional comparisons, and a logical-fault operating-window bound.

WHAT REMAINS CONDITIONAL
=======================
Native rate control must preserve one shared static transverse noise axis and the
signal Hamiltonian. The reference qubit must remain coherent. Active meter
population errors, generic logical phase faults, reference-drive errors and
uncontrolled axis drift remain harmful. Repeated readout does not itself protect
unstable meter populations. No fault-tolerance threshold or hardware performance
advantage is proved. Historical novelty remains unestablished.

FAIR COMPARISON
===============
Known-noise HNLS QEC already gives quadratic information with suitable controls.
Even with unknown axis, two-rate ordinary QEC plus retained counts and joint
inference also gives local quadratic information. Subsystem, autonomous and
fault-tolerant sensing have strong established constructions. The candidate
contribution is a concrete finite interaction/observation architecture that removes
axis inference and sensor recovery pulses, together with its exact costed consumer.
It is not a claim that all prior sensing methods lacked Heisenberg scaling.

ILLUSTRATIVE EXACT-MODEL INSTANCE
================================
gamma_low=1, gamma_high=4, active time=.1, deadtime=.1,
classical report error=.1, meter action lambda*tau=pi/2.
The derived gain is v=.1962121845, even occupancy=.5931497427,
and information coefficient C=.01354505081. Achieved information is 555.3426
at total time 200 and 54314.8569 at time 2000. Units are normalized to gamma_low.
These are computed model values, not measured device results.

MAP OF FILES
============
PROOF.txt: primary construction and synthesis, including costs and limitations.
SOURCES.txt: primary research comparisons and exact Astra source revision/scope.
research_feedback_sensor.py: full finite-controller likelihood, exact derivatives,
  operating-window examples and scientific figure generation.
finite_controller_results.json, finite_controller_scaling.png: reproducible outputs.
verification_results.json: final executions of the independent check programs.
supplements/: complementary proofs, rejected openings and their useful results.

REPRODUCE
=========
Python3, NumPy, SciPy and Matplotlib are needed. No network is needed.
From this directory:
    python research_feedback_sensor.py --output reproduced
    python checks/verify_sensing_two_body_meter.py
    python checks/verify_sensing_interval.py
    python checks/check_sensing_nuisance.py
    python checks/count_echo_complement.py

The full three-qubit Liouvillian is checked independently against the reduced
transfer matrix for populations and logical coherences. Deferred classical-frame
processing is also compared directly to coherent erasure. Additional checks cover
100 stationary parameter sets, finite-interval instruments, exact Kraus identities,
cyclic operators and the explicit robust conventional code. These checks are
evidence for the derivation, not experimental data or proof of historical priority.

SOURCE CUTOFF
=============
This is a fresh investigation. The physical question was selected from primary
research before selective Astra retrieval. Astra was pinned to Git revision
6cecc51aafd33e74ec0d7b806e6673f5e16336a2. No predecessor conversation was reloaded.
The source terminal-readout identity is used under its actual discard and QND
conditions. Other scoped source achievements were not promoted into an assumed
hardware platform, general fault-tolerance theorem or free perfect syndrome oracle.
