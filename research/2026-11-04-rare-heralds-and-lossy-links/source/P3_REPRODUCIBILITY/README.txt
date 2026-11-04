LOSSY FIXED MEASUREMENT PORT: REPRODUCIBILITY PACKET
4 November 2026

Scope
-----
This packet accompanies the construction of a quantum communication link from
a fixed driven-dephasing source H=Omega X/2, L=sqrt(gamma) Z, with vacuum input,
coherent collection efficiency eta, no source feedback during an emission
window, and the original source discarded afterward. Alice prepares a Bell
pair between the disposable source and a retained local memory. This is an
entanglement-generation protocol followed by purification and teleportation;
it is not direct recovery of an already inaccessible unknown source input.

The analytic all-drive-ratio theorem uses a transition-selective temporal mode
and a finite passive ladder receiver. The proof is in the accompanying answer.
all_ratio_bounds_and_purification.py reproduces conservative constants,
explicit receiver dimensions, and the complete five-qubit purification
weight enumerators and expected resource costs. It uses only Python's
standard library. Its evaluations illustrate proven inequalities; they do
not interval-verify every real parameter.

The separately certified finite-cavity instance uses Omega=1, T=pi,
gamma=0.005/pi, cavity linewidth 20, collection efficiency 0.01, coupling
G=1/sqrt(40*pi), and a single receiving qubit with coupling
R=-i sqrt(0.2) sigma_minus and H_B=Z_B/2. All output fields are traced out.
The constant local filters are specified in
constant_cavity_receiver_certificate.py. A local phase of
0.09745901407420347 radians aligns the returned Bell coherence.

Run
---
Dependencies: Python 3.10 or later, NumPy, SciPy.

    OPENBLAS_NUM_THREADS=1 python constant_cavity_interval_audit.py
    python all_ratio_bounds_and_purification.py

The first command audits every sparse generator coefficient using directed
50-digit Decimal intervals and a Machin-formula enclosure of pi. It executes
a 4096-step, degree-16 Taylor evolution and bounds Taylor error, binary64
roundoff, coefficient error, initial-state representation, final arithmetic,
and the analytically bounded Fock cutoff. Expected certified bounds:

    unnormalized output trace-norm error < 4.1370e-10
    success > 5.0000221e-6
    conditional Bell fidelity > 0.8942083

constant_cavity_certificate_result.json records the executed result. Small
last-digit variation in central floating-point results is possible across
platforms. The certificate assumes standard IEEE binary64 operations and
the stated operation-count model; it is not a formally verified arithmetic
library. The exact cavity plus vacuum transmission-line Hamiltonian is the
physical model being certified. This is not experimental data and does
not certify all microscopic corrections of a fabricated circuit.

The Fock cutoff is analytic, not convergence-only. If N cavity levels are
retained and alpha=2G/kappa, the common-dilation bound is

    ||E-E_N||_diamond <= 2 G T sqrt(N) alpha^(N-1)/sqrt((N-1)!).

At N=6 the bound is below 7.081e-12. It follows from the factorial moments
M_m=<(a^dagger)^m a^m> <= alpha^(2m). These estimates include arbitrary
initial source-reference entanglement and all downstream receiver operations.

linear_loss_receiver_check.py is included because it supplies small matrix
primitives imported by the cavity code. Its optional main program runs an
earlier smooth single-qubit Markov receiver at a fast fixed drive ratio.
Those adaptive-ODE results are consistency checks, not the validated
finite-cavity certificate. The all-ratio theorem does not rely on that ODE.

Purification accepts matching local syndromes, not both zero syndromes. For
Bell error e, u=1-e, x=e/3, its acceptance is
u^5+30*x^3*u^2+15*x^4*u+18*x^5 and its output error is
(30*x^3*u^2+18*x^5)/acceptance. Two rounds applied to the finite-cavity lower
fidelity yield error < 6.94e-9 under ideal local operations and require fewer
than 8.81 million source windows on average. Preparation, reset, gate time,
classical propagation, memory errors, and measurement errors must be added
as specified in the accompanying answer; no real-time hardware advantage
over a purpose-built network is claimed.

Exact primary sources and prior scope
------------------------------------
Coles and Piani, coherent measurement transfer, Proposition 1:
https://arxiv.org/abs/1305.3442
Yang, Huelga and Plenio, continuous decoder, Eq. (32) and initial condition:
https://arxiv.org/html/2209.08777v3
Nurdin, James and Yamamoto, tunable causal single-photon absorption:
https://arxiv.org/abs/1609.05643
Gough and James, series product, Definition 5.3 and Theorem 5.5:
https://pure.aber.ac.uk/ws/portalfiles/portal/142164/GJ%20Series%20Final.pdf
Didier, Bourassa and Blais, modulated longitudinal cavity coupling, Eq. (2)
and Supplement S1-S6, including rotating-wave assumptions:
https://arxiv.org/abs/1504.04002
Potts et al., source-controlled sideband exchange alternative:
https://arxiv.org/html/2407.02024v4
Cabrillo et al., weak-excitation single-photon remote entanglement:
https://arxiv.org/abs/quant-ph/9810013
Cirac et al., source-shaped photonic quantum state transfer:
https://arxiv.org/abs/quant-ph/9611017
Bennett et al., entanglement purification and hashing, Section 3.2.3:
https://arxiv.org/abs/quant-ph/9604024
Mueller-Hermes, Reeb and Wolf, two-way transposition strong converse, IV.C:
https://arxiv.org/abs/1502.05630
Siddhu, lossless complementary-channel positivity:
https://arxiv.org/abs/2003.10367
Singh and Datta, dimension criterion, Corollary 3.5:
https://arxiv.org/html/2105.06327v2

The new assertions are derived in the accompanying answer. These sources
do not themselves state the combined all-loss, all-nonzero-drive,
finite-causal-receiver theorem or the particular finite-cavity certificate.
Historical priority for that complete combination has not been established.
