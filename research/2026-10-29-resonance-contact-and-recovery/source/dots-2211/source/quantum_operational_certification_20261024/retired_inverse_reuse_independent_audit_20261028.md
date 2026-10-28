# Independent receiving: retired-record finite inverse reuse

28 October 2026. Reviewer `producer-workspace/review_effect_only_acquisition`. **PASS at the separately bound source version.** This receives a finite complete-process upper bound and a specified GHZ-workload lower bound, not a universal quantum-computing lower bound. The author source is unchanged.

## Same learned program and complete feedback

The residual channel is R_t=Ad_exp(i t Z/2). Its generator L=i[Z,.]/2 has diamond norm at most one by the two multiplication bounds; L^2 has norm at most one by submultiplicativity. In a J-slot composition, differentiating twice produces J same-slot terms and J(J-1) ordered distinct-slot terms. The intervening actual maps at the same t remain CPTP contractions. Therefore the second derivative bound J^2 is valid with coherent source memory and reference, and with fixed adaptive instruments represented by ordinary CPTP maps on classical registers. Their actual memory trajectories need not equal the reference trajectory.

The controller/source maps must not themselves depend on the private program except through the declared recovery slots. Fixed-theta program independence from the initial service state/source is substantive. If a decision rule reads the estimator, or training memory leaks it, this derivative decomposition would not describe the compared process.

At a grid angle, conjugation symmetry of the estimator induces a symmetric principal residual angle. Splitting antipodal mass between +pi and -pi leaves the physical rotation CHANNEL unchanged, including under reuse, and makes E[t]=0. Banach-space Taylor remainder has norm <=J^2 t^2/2; the extra half-distance factor gives J^2 E[t^2]/4. Since t^2<=pi^2 sin^2(t/2) on [-pi,pi], the stated coefficient follows. This cancellation occurs after genuine record retirement and cannot replace an average of conditional trace norms.

For a continuous angle, replace only the TRAINING law by its nearest grid law while keeping actual service maps and controller fixed. A mixture of the same physical process maps costs at most the law's TV. Next change the deterministic residual rotation by 2Delta at every slot: half-diamond cost per slot is <=|Delta|. This proves the sqrt(N)+J grid debit even when the actual native service maps depend on the fixed true theta. They are held unchanged in this mathematical comparison, not silently replaced by another world's service dynamics.

The rational finite K rule, contrast-dependent sufficient horizon, full-protocol implementation debit and finite arithmetic limitations are inherited correctly. J independent calibration banks yield a sum of per-slot bounds only if the future bank is still independent of all prior service activity; joint initial independence and unused private programs provide this premise. The stated total-call quadratic scaling follows, without treating reuse of one bank as independent resampling.

## Fixed-workload lower bound, including arbitrary collective decoders

The GHZ encoder fixes a two-dimensional code subspace on which J simultaneous phase rotations act as V_(Jtheta). Composing any collective final CPTP decoder with this isometric code embedding gives a general qubit CPTP map. Thus reducing to D_y does not omit a possible collective decoder. Changing the encoder or introducing interleaved echoes is explicitly a different workload.

The normalized Choi matrix of D is positive with trace one. Logical entanglement fidelity after V_(Jtheta) is its overlap with the normalized Choi vector of the inverse unitary, with the standard transpose placement harmless for these diagonal phase rotations. The sum of the two target rank-one projectors has largest eigenvalue 1+|cos(2Jdelta)|. Hence the stated sum-infidelity inequality holds for arbitrary CPTP D, not only unitary fits.

Entanglement infidelity is linear in the decoder. Integrating against the overlap of actual calibration laws therefore directly lower-bounds the record-DISCARDED mean channel's infidelity. This does not reuse the invalid expected-trace-norm transfer excluded by the previous lower bound. Measuring the Bell projector lower-bounds half trace distance by infidelity, and the diamond supremum includes this Bell input.

For N>=1 and integer J>=1, delta=1/[4max(J,sqrt N)] gives TV<=1/2 and Jdelta<=1/4. From 1-cos(2Jdelta)=2sin^2(Jdelta)>=8J^2delta^2/pi^2, the final minimax constant is min(1,J^2/N)/(8pi^2). The two angles may be supplied to the learner; this is not a search-complexity bound. For requested error below the saturation constant it implies the stated Omega(J^2/epsilon) horizon. It matches J and epsilon dependence of the upper theorem on the noiseless subfamily, not its contrast dependence or hardware costs.

## Independent checks and simulation audit

`retired_reuse_complete_feedback_independent_check_20261028.py` propagates retained physical, source-memory and reference registers through random joint native unitaries, nonunitary memory operations and the SAME phase error in every slot. Twenty-five J/t cases check the symmetric Taylor bounds. A separate 480 general-CPTP Choi checks and 20 finite parameter cases verify projector and minimax constants numerically. These stress checks are not the proof.

I copied the author's simulation program to a separate temporary path and reran its exact seed without changing the original outputs. All four stored complex-sum arrays and the entire JSON matched exactly. It individually generates 5,242,880 ordinary finite-root Born outcomes across 8,192 independent banks. Each bank is reused for all scored J values; those scores are not separate acquisitions. Stored NPZ contains summary S arrays, while the seed/program reconstruct raw outcomes. `retired_reuse_author_replay_independent_20261028.json` records this audit. Floating synthesis/readout is simulated, not a confidence-certified finite-control implementation or hardware.

No unresolved load-bearing gap found at the stated scope. Historical novelty, generic encoding optimality, coherent multi-query calibration bounds, correlated training/service memory and physical fault-tolerance remain outside acceptance.
