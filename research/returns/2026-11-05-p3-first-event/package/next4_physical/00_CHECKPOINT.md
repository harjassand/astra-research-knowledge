# Physical branch checkpoint

Current corpus checked: fef3640a8b1dc5475674a006de417f652f3baf3c.

Selected candidate endpoint: exact active thermodynamic nonidentifiability at a single mechanical port, even with full continuous acquisition, bounded adaptive force protocols, known all-even microscopic reversal, and a controllable/observable two-coordinate system. This is a foundational endpoint rather than an unearned device.

Candidate family:
A=diag(1,3), c=(1,1)/sqrt(2), v=(1,-1)/sqrt(2).
Sigma_s=A^{-1}+s vv^T; D_s=(A Sigma_s+Sigma_s A)/2.
dX=(-A X+c u)dt+sqrt(2D_s)dW; Y=c^T X, stationary start.
All s in [0,4+2sqrt(5)) have identical complete Y covariance and collocated response:
C(t)=.5 exp(-|t|)+(1/6)exp(-3|t|), g(t)=.5(exp(-t)+exp(-3t)).
They satisfy exact observed equilibrium FDT at T=1.
Sigma_s c=A^{-1}c makes the full stationary Gaussian forcing process identical; consequently arbitrary causal well-posed port feedback gives identical controlled output records and work distributions.
Both state directions controllable/observable; no appended decoupled subsystem.
Orthogonally diagonalizing positive D_s realizes each as two independent thermal reservoirs coupled by a reciprocal harmonic potential.
Candidate stationary entropy production sigma_s=s^2/(1+2s-s^2/4), zero at s=0 and divergent as s approaches upper endpoint. Divergence uses temperature approaching zero; do NOT equate it with unbounded dissipated power.
At s=4, temperatures 5+-2sqrt(5) and sigma=16/5, fixed decay rates 1 and 3, already gives exact equilibrium/non-equilibrium ambiguity with strictly positive bounded temperatures.

Checking literature/corpus for priority and scope. N1225 already covers passive reversal ambiguity and generalized-equilibrium completions, but known all-even reversal and active equivalence may be distinct.
A complete hidden-coordinate reset to a known point would distinguish this family through transient covariance; it is an additional physical operation, not a free preparation. No claim it is acquired.

Original directories remain untouched. Proof and computational audit underway.


## Corpus-overlap correction (latest)

The current main corpus already contains `research/returns/2026-11-05-p2-tracial-acquisition/active-port-nonidentifiability.md`, whose exact arbitrary adaptive conjugate-force ambiguity, all-even reversal, fully controllable/observable realization, unbounded entropy range, and known-drift two-step span criterion overlap the main qualitative endpoint. Its full companion was retrieved. The common thermal-pulse return also supplies the additional noise intervention and finite-slew acquisition path. Therefore this branch MUST NOT be promoted as an independently new qualitative endpoint.

The remaining physical strengthening is a two-coordinate reciprocal two-bath realization with **fixed known unit mobility, fixed spring matrix, fixed output/force port**, no nonconservative drive, and fixed relaxation rates 1 and 3. Only the two reservoir temperatures vary. The old isothermal realization changes mobility and requires a hidden nonconservative force. Here the family is a Brownian heat conductor: its actual heat flux is J=s/sqrt(5); entropy is s^2/(1+2s-s^2/4). The equilibrium case s=0 and s=4 have identical controlled port laws although the latter has both bath temperatures within [0.5278,9.4722], fixed mechanical parameters, heat flux 1.7889 and entropy rate 3.2. The unlimited entropy limit approaches a zero-temperature bath and does NOT mean unlimited heat/energy flux.

I am finishing this as a rigorously scoped physical strengthening and prior-overlap audit, not a rival destination to root's rare-event sampler. The exact hidden thermal operation is established; harvesting its heat or identifying its bath temperatures requires another port/noise intervention. No actual hardware experiment or full positive acquisition pipeline is claimed.

## Final status: completed physical specialization; do not select as new endpoint

The full proof is now in `01_FIXED_MECHANICS_THERMAL_PORT.md`.
`audit.py` executed successfully; its exact and numerical checks are recorded in `audit_results.json`.
Copies of the two current Astra summaries and the original active-port proof companion are under `sources/`.

The broad arbitrary-adaptive-force obstruction is already in current Astra. The remaining increment is a two-coordinate reciprocal Brownian conductor with **the same spring matrix, same unit mobility, same bath directions, same mechanical force/observation port, and fixed rates 1 and 3** for all hypotheses. Only the two reservoir temperatures vary. At s=4 the temperatures are 5±2√5, heat current is 4/√5, and entropy production is 16/5, yet the full port transcript is exactly the equilibrium transcript.

The construction closes finite-force/slew work predictions as well: a smooth sine-squared cyclic force has Gaussian work N(m,2m), m≥0, for equilibrium and conductor alike. Symbolic identities and independent covariance/energy work integrals agree. No impulse experiment or acquisition inversion is assumed.

This does not deliver a new positive thermodynamic instrument or engine. A trusted full-state reset, second sensor, or calibrated thermal intervention breaks the equivalence; the latter operation already exists conditionally in Astra's thermal-pulse return. I recommend retaining this as an assumption/physical-model companion and choosing the parent's genuinely new constructive destination.
