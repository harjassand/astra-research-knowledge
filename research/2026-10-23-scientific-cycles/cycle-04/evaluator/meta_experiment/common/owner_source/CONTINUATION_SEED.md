# PRO3 continuation seed: vanishing-screen robustness

Scientific date: 2026-10-22, Australia/Brisbane. Owner: Astra PRO3.
This is the latest scientific state in this return and supersedes the old
fixed-eta question in the unchanged Cycle2 archive. Max owns integration;
the evaluator owns research-system assessment. The scientific mission continues.

## Exact family

Finite labelled spaces, strictly positive pi,q, fixed K>0 and alpha in (0,1),
D(pi||q)<=K, beta=1-alpha, fixed symmetric stochastic target-independent Q.
G is proposal-q independence MH. L_eta uses the two reciprocal acceptance
factors stated in VANISHING_SCREEN_THEOREM.md, and
C_eta=(I+alpha G+beta L_eta)/2 starts from q. The normalizer is unavailable;
ratios, q/Q proposals, all target queries and full caching are counted.
No empirical KL inference or whole-target-table restriction is invented.
Eta may be selected from a requested deterministic horizon or error, but is
fixed during every individual trajectory. Q and mixture weights stay fixed.

## Accepted received capital

Both all-positive-fixed-eta proofs are accepted once without repair, within
the finite class. Every fixed eta>0 has log(n)R_eta(n)->K and
epsilon logT_eta(epsilon)->K. The old low-eta gap is closed. Preserve the
conjugation and telescoping proofs, their blind reviews, methods, failures
and cost records. No novelty or prompt-tactic superiority follows.

## New established result

Let eta_n in (0,1] be deterministic across runs. Then

    R_{eta_n}(n)->0 iff eta_n log n->infinity.

The new principal upper proof retains the received moment exponent and
affine reset. For each first-hit submeasure nu_j, interpolate its geometric
mass bound with its moment bound, giving a summable total of Lp norms
independent of eta. Smooth each nu_j at its own remaining horizon, rather
than transporting all entries to a growing burn-in. Equal-mass anchor
cancellation preserves every return path. The full finite inequality is
Theorem A in VANISHING_SCREEN_THEOREM.md, independently source-reviewed.

Put kappa0=-log(1-alpha exp(-K)/2) and

    Lambda_*=1+log(1+beta/2)/kappa0.

If liminf eta_n log n/loglog n>Lambda_*, then log n R_{eta_n}(n)->K.
This is sufficient, not sharp. The eta-independent two-state Q=I family
supplies the K lower.

The actual three-state capture family proves convergence necessity and the
bounded/critical-u crossover. A growing symmetric path proves more. Put
d_*=2alpha exp(-K)/beta; chi=1 if d_*>=1, otherwise solve uniquely
d_*=chi(1-chi)^((1-chi)/chi). If

    eta_n log n/loglog n->lambda in (0,1/chi),

then log n R_{eta_n}(n)->infinity. At K=1,alpha=1/2,
chi=0.91870999842712..., 1/chi=1.08848276573897..., whereas
Lambda_*=3.31290271377331.... The exact example lambda=27/25=1.08
is certified by 321^27<25^27*16^25. A universal sharp multiplier one
is therefore falsified. The full lower construction was independently
developed and then directly accepted by the principal.

## Accuracy and cost formulation

Choose eta(epsilon) before the run, hold it fixed, and let
d_epsilon=eta(epsilon)/[epsilon log(1/epsilon)]. For d_epsilon->d>0 finite,

    max(K,1/(d chi)) <= liminf epsilon log T
       <=limsup epsilon log T <=max(K,Lambda_*/d).

For d_epsilon->infinity the exact coefficient is K. For d_epsilon->0
it diverges to infinity. A finite d>Lambda_*/K also gives coefficient K.
These are direct fixed-kernel-per-error statements, not an inversion of
a possibly nonmonotone diagonal risk.

Pure IMH already has coefficient K. At K=1,alpha=1/2,d=1 the lower
coefficient 1.08848... is strictly worse than pure IMH. No speedup follows.
Weakening eta raises local acceptance and first-screen passage, so it does
not itself save uncached target evaluations. No precision/runtime uniformity
over arbitrary input ratios is proved.

## Precise next owned question

Determine the sharp finite-d coefficient or its existence in this diagonal
accuracy regime. Start by representing transport before the first safe hit
as a killed positive operator, preserving its actual global-escape mass,
and compare its optimal weighted-norm exponent with the admitted path
variational exponent chi. The concrete bottleneck is whether the affine
norm growth bound and a uniform killing rate can be coupled sharply, rather
than interpolated separately. A complete upper must retain all returns and
support uniformity. A stronger lower must supply actual target-independent
symmetric Q, positive probabilities, KL slack and relative capture/retention.

This is the selected next scientific step, not a claim it has been executed.
No background computation remains running. Do not repeat the fixed-eta,
joint-KL, prefix or candidate-only stopping questions. Do not start an
application search to justify the sampler.

## Source and status

Main proof: VANISHING_SCREEN_THEOREM.md; lower: reviews/vanishing_lower_proof.md.
Source-bound upper review: reviews/vanishing_transport_source_binding.md.
Principal lower acceptance: LOWER_ACCEPTANCE.md. Full information/cost
contract: EXPERIMENT_CONTRACT.md and NUMERICS.md. Actual calculations and
failed attempts are included. Read README.md for portable verification.
Internal correctness, historical originality, implementation efficiency,
physical significance, private delivery and Max integration are distinct.
