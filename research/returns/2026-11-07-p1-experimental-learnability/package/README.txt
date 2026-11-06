EXPERIMENTAL LEARNABILITY
7 November 2026, Australia/Brisbane

Read RESULT.txt for the complete question, three theorems/constructions,
proofs, scientific consequences, exact observation interfaces and costs.

The principal operation now includes experiment acquisition design: it
computes the best achievable worst-case task accuracy to any prescribed
tolerance, constructs a finite programme approaching that accuracy, and
returns compatible models witnessing the irreducible information limit.
This general result uses a convex, finitely presented bounded-curvature
potential family and positive native measurement error. It is a proved
THG/Euler/CAD construction, not an executed general CAD implementation.

A separate theorem proves constant-accuracy uncomputability of learnability
for two programme-presented, polynomial-time evaluable quadratics. The
forward models remain uniformly strongly convex and contracting. Their
representation and nonconvex two-model prior differ explicitly from the
general positive theorem's inputs.

EXECUTED SOFTWARE

Python 3 standard library only; no package installation or solver required.
From this directory run:

  python3 run.py

This builds and verifies the finite-budget design certificate and finite
controls for the bounded model evaluator. To replay the saved certificate:

  python3 run.py --check-only

The checks also work under python3 -O; scientific checks use explicit
exceptions rather than assertions disabled by optimization.

Files:
  experiments.py                  exact finite-budget minimax construction
  programme_models.py             bounded TM/forward-model evaluators
  run.py                          complete fixture and certificate replay
  EXPERIMENT_INPUT.json            model, channel, catalogue and budget
  EXPERIMENT_CERTIFICATE.json      all posterior states/actions/responses
  FIXED_SCHEDULES.json             all 21 fixed schedule values
  OPTIMAL_POLICY.json             optimal adaptive action selection
  VERIFICATION.json               executed checks and measured work record
  PROGRAMME_MODEL_CHECKS.json      finite controls; not an undecidability test
  SOURCES.txt                     credited primary/Astra sources and scope

Exact fixture results:
  no measurements: 1/3 worst-case equilibrium error
  one best measurement: 5/32
  two best fixed measurements: 5/48
  at most two adaptive measurements: 1/12
  unlimited finite programmes with refinable precision on [0,1]: 1/32

The adaptive result checks 2,011 distinct states and 3,836 response edges.
An attained worst transcript leaves equilibria 13/16 and 47/48 compatible
with the same complete history. Every scientific guarantee is conditional
on the declared global secant bounds and bounded-error direct observation
channel. No physical acquisition was performed.

The preceding Certified_model_family_inference_2026-11-06.zip is included
unchanged in this package. It supplies the accepted inference
algorithm, its implemented network operation, attribution and the chain
to all earlier archives. The general CAD algorithm and executed network
software retain their distinct status. No predecessor is declared
superseded, solved beyond its scope, or impossible by these results.

The new mathematics and software have producer-side derivations and
checks. They have not received independent peer review or complete formal
verification. No historical-priority or civilisation-scale impact claim
is made. No additional worker, infrastructure or scientific peer transfer
was used for this continuation.
