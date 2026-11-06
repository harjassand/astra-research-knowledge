CERTIFIED MODEL-FAMILY INFERENCE
Complete mathematical construction and runnable nonlinear-network operation
6 November 2026

WHAT IS DELIVERED

The chosen question is: how can finite information about an unknown
scientific law yield sharp, certified consequences for all models still
consistent with that information, including explicit models attaining
the bounds?

GENERAL_THEOREM.txt resolves that question for finite-horizon dynamics
driven by a stationary unknown potential with supplied global curvature
bounds. It gives a complete deterministic algorithm, explicit compatible
potential witnesses, controlled numerical error and charged algebraic
computation. It also constructs approximately optimal robust interventions
over a compact polynomially described design family.

COOPERATIVE_INFERENCE.txt resolves a stronger efficient specialization:
two explicit stationary constitutive models attain all componentwise
forecast bounds in a cooperative nonlinear network. An exact rational
contraction test also enables unique-equilibrium, sharp equilibrium-range
and all-future task certificates. This operation is implemented end to end.

These are model-conditional mathematical consequences. The general
real-algebraic optimizer is specified using accepted algorithms but was
not implemented or run here. The reference code does not claim to be a
universal inference system, a practical replacement for physical model
qualification, an independently audited theorem, or a P versus NP result.
The civilisation-scale consequence target is not declared achieved.

MAIN COMPUTED CONSEQUENCES

1. A whole scalar nonlinear-law family has the exact sharp x(1) interval
   [(32/27)exp(-3), 2^(-1/3)exp(-1)]. Rational integration certifies its
   endpoints; the task remains uncertain because the laws are uncertain.

2. A 16-node periodic nonlinear network has certified mean state at t=1
   in approximately [0.4826266579,0.5857462734], over all local laws and
   initial states in the stated input family.

3. A 64-node periodic nonlinear network has a certified equilibrium mean
   in approximately [0.2159911380,0.4163411458]. The two endpoint model
   computations have exact residual error radii below 2^-48.

4. For that 64-node family and the supplied initial box, EVERY compatible
   model satisfies mean x(t)<=0.4586856651...<1/2 for EVERY t>=8. This uses
   an explicitly computed contraction rate, not an unconstructed limit
   predictor. Exact rational bounds are in DERIVED_CONSEQUENCES.json.

All examples are synthetic mathematical inputs. No physical observations
were obtained. Decimals are display only; JSON strings contain exact
rational values. Mathematical proofs establish the general statements;
finite test passes are implementation checks and never a universal proof.

HOW TO RUN

Python 3.10 or newer and the standard library are sufficient. No external
solver, network access, package installation, worker or new infrastructure
is required for the network operation.

From this directory:

  python3 verify.py

This regenerates the mathematical fixtures and exact certificate files.
The tests check finite interpolation, explicit failure witnesses, shared
potential constraints, whole-law scalar forecasts, 16-node transients,
64-node equilibria, the derived all-future consequence, weighted
contraction, and rejection of corrupted numerical certificates.

To run a standalone inference and then check it against its original input:

  python3 infer.py solve EXAMPLE_TRANSIENT_INPUT.json OUTPUT_TRANSIENT.json
  python3 infer.py verify EXAMPLE_TRANSIENT_INPUT.json OUTPUT_TRANSIENT.json

  python3 infer.py solve EXAMPLE_EQUILIBRIUM_INPUT.json OUTPUT_EQUILIBRIUM.json
  python3 infer.py verify EXAMPLE_EQUILIBRIUM_INPUT.json OUTPUT_EQUILIBRIUM.json

The included EXAMPLE_*_OUTPUT.json files are completed runs. Exact replay
was also run with python -O; certificate checks do not disappear when
Python assertions are disabled. verify.py itself is a normal test runner
and should be run without -O.

CLI INPUT SCHEMA

All rational numbers should be strings such as "3/4", "-2" or "0".
Use sparse rows: each matrix row is a list of [column_index,coefficient].
An example one-node family is:

{
  "mode": "transient",
  "rows": [[]],
  "laws": [{"slopes": ["1","3"],
            "samples": [["0","0","0"],["1","2","2"]]}],
  "forcing": ["0"],
  "initial_box": [["1","1"]],
  "horizon": "1",
  "endpoint_error": "1/1024",
  "nonnegative_readout": ["1"]
}

For equilibrium mode omit initial_box and horizon. It requires the
comparison-matrix contraction condition described in the report; the
solver constructs any needed positive diagonal scaling. If that condition
is not certified, it raises a descriptive error, with no claim that the
actual nonlinear family lacks equilibria. Finite-time inference remains
available for any well-formed cooperative-family input.

At least one interval sample per local law is required. All off-diagonal
matrix coefficients must be nonnegative. Laws form an independent product
family and obey the global slope bounds on the entire real line. The
default nonnegative readout is the mean. endpoint_error bounds the outer
endpoint excess for every coordinate and this readout, not the total
model-uncertainty width. Exact input inconsistency is reported separately.
The CLI currently takes constant forcing; the mathematical construction
also specifies how to handle a finite supplied forcing-switch schedule.

FILES AND THEIR STATUS

GENERAL_THEOREM.txt       Complete general proof, algorithm and costs.
COOPERATIVE_INFERENCE.txt Complete network operation, proofs and deductions.
SOURCES_AND_PROVENANCE.txt Source pins, adopted conditions and predecessor credit.
CHECKPOINT.json           Preserved predecessor identities and result scope.
interpolation.py          Exact rational completion/interpolant evaluation.
algebraic_problem.py      Builds/evaluates shared-potential polynomial constraints.
network.py                Envelopes, integration, equilibria, scaling and checkers.
infer.py                  Standalone inference and certificate verification CLI.
verify.py                 Reproducible synthetic checks and source-model fixtures.
RESULTS.json              Exact bounds, costs and outcome of the producer checks.
GENERAL_POLYNOMIAL_FIXTURE.json Quadratic constraints; optimization NOT executed.
SCALAR_TRAJECTORY_CERTIFICATES.json Complete two-model scalar numerical traces.
NETWORK_TRAJECTORY_CERTIFICATES.json Complete 16-node numerical traces.
EQUILIBRIUM_CERTIFICATES.json Exact 64-node endpoint residual certificates.
WEIGHTED_CONTRACTION_CERTIFICATE.json A matrix scaling and equilibrium certificate.
DERIVED_CONSEQUENCES.json The exact all-future mean-state conclusion.
EXAMPLE_*_INPUT.json      Standalone 16-node/64-node operation inputs.
EXAMPLE_*_OUTPUT.json     Completed results for those inputs.
VERIFICATION_RECEIPT.json Final replay outcomes and mathematical scope checks.
MANIFEST.json            File hashes for this preserved package.

The previous mechanical-compiler and SAT archives remain unchanged. Their
identities/hashes are recorded in CHECKPOINT.json; they are not duplicated
or silently revised in this archive. N1226's effective-construction
approach is explicitly credited in the new source ledger as well as its
geometric architecture. The SAT question remains inactive and unresolved,
not declared impossible.
