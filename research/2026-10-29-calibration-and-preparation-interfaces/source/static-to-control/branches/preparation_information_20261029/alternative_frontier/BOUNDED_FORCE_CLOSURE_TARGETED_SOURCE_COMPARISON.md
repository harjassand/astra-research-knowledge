# Targeted comparison: bounded-force kinetic equilibrium closure

29 October 2026. Independent source check by
producer-workspace/different_consequential_opening. This is a focused comparison with
primary results actually inspected, not a historical-priority determination
or a full literature survey.

## Target and conclusion

Target: BOUNDED_FORCE_FINITE_RESOLUTION_EQUILIBRIUM.md,
SHA256 2bd8c75a5e1371b39b7ed346b10fb75810d5387012744888d7aa2b0730f8050f.

The target fixes the torus, bath, time horizon, and position-force ceiling.
Vanishing physical entropy production implies subsequential setwise path
convergence to a same-bath Gibbs model with bounded measurable gradient;
smooth Gibbs competitors then approximate every fixed declared observation
channel in the stated class. Full-path source-to-equilibrium TV convergence
is expressly excluded.

**A directly relevant conventional kinetic stability theorem was found.**
It already supplies WHOLE-SEQUENCE weak native-path convergence for ANY common
initial probability law, after a straightforward negative-Besov embedding.
There is no fourth-moment restriction in the strongest applicable proposition.
It does not state the
target thermodynamic or finite-resolution conclusion. Accordingly, the weak
generator closure should be presented as compatible with established kinetic
stability theory, not as an unavailable conventional capability. The root
compact-occupation proof remains a self-contained, narrower route.

No inspected primary section states the complete small-physical-entropy,
same-bath Gibbs closure and setwise/fixed-record theorem. That is a bounded
retrieval result; priority of that combined statement remains unresolved.

## 1. Printed path-stability result

Primary: Elena Issoglio, Stefano Pagliarani, Francesco Russo, Davide Trevisani,
[Degenerate McKean–Vlasov equations with drift in anisotropic negative Besov spaces,
arXiv:2401.09165v2](https://arxiv.org/html/2401.09165v2),
18 March 2026.

Actual read: §1.3 Assumption 1.1 and constant-matrix kinetic setup;
§4.2 Theorem 4.9, Corollary 4.11 and Lemma 4.12; §5.1 Definition 5.1,
Proposition 5.5 context, Lemmas 5.7–5.8 including tightness and limit-
identification proof, Theorem 5.11 statement, and Proposition 5.12 including
its complete disintegration/dominated-convergence proof.

Proposition 5.12 takes the drift assumptions of Lemma 5.8 and ANY common
initial probability law. It gives convergence of the WHOLE sequence of path
laws to the unique limiting martingale-problem solution. Lemma 5.8 is only
the finite-fourth-moment intermediate step. Proposition 5.12 disintegrates
over deterministic initial states, uses uniqueness from Theorem 5.11, and
integrates bounded continuous path observables by dominated convergence.
Their fixed linear matrix may include friction; the noise acts in velocity,
under the kinetic Hörmander condition. Theorem 4.9 supplies the backward-
equation stability used to pass the martingale identities.

This is a printed result about path laws, not merely a PDE regularity
analogy. It is stated on Euclidean space with a fixed initial law, and does
not assert equilibrium, stationary-preparation convergence or setwise
convergence. The nonlinear McKean–Vlasov part is unnecessary here.

## 2. Explicit specialization and the remaining deductions

The following is our specialization, not a quoted theorem.

Let F_j be uniformly bounded periodic position forces with
F_j weak-* -> F in L-infinity(T^d). Extend them periodically to Euclidean
position space and make them independent of momentum. For any negative
anisotropic Besov exponent -epsilon, a dyadic decomposition gives convergence
in that norm:

- Each fixed low-frequency block contains finitely many torus Fourier
  modes. Their coefficients converge by weak-* convergence, so that
  block converges uniformly.
- Uniform force bounds uniformly control every dyadic block before the
  weight. The negative weight bounds the tail by C A 2^(-epsilon K).
- First choose K large, then j large. Hence the full norm tends to zero.

The kinetic anisotropy changes the relation between spatial wave number and
dyadic index, but not this low-block/tail argument. Independence of momentum
means there is no noncompact momentum-translation obstruction. The original
bath can be put into the source's unit-noise form by a fixed linear scaling;
the matrix has momentum block -gamma I and the usual position/velocity
coupling. Thus the printed stability result applies directly to this bounded-
periodic-force sequence with any common initial probability law. Proposition
5.12 gives whole-sequence weak convergence, without a moment restriction.

The root theorem has changing stationary preparations. The literal statement
of Proposition 5.12 does not cover that change. The backward-equation proof can be
adapted using weakly convergent initial laws and uniform moments; alternatively
the root endpoint-smoothing and common-L2-density construction handles it
directly without importing this adaptation. A lift from the torus also needs
a consistent initial-coordinate convention, or one can formulate the same
periodic backward equations on the torus.

The remaining target ingredients are separate logical steps:

1. The calibrated physical entropy identity and conditional Maxwell Gaussian
   logarithmic Sobolev inequality force product form in the stationary limit.
2. The stationary generator identity then forces grad nu=F nu/tau, giving
   a positive Gibbs density and bounded-gradient potential.
3. Uniform L2 path likelihoods relative to one free reference upgrade
   identified subsequences to setwise convergence.
4. Smooth potential approximation and ordinary probability arguments give
   the stated fixed-record consequences.

The cited stability theorem neither acquires the bath identity nor identifies
a hidden force experimentally. It also does not supply a computable small-
entropy modulus or a physical intervention guarantee. The root theorem
appropriately keeps those obligations separate.

## 3. A second conventional route, less literal for this target

Primary: Zikai Chen, Zimo Hao, Xicheng Zhang,
[Kinetic SDEs with subcritical distributional drifts,
arXiv:2508.12234v1](https://arxiv.org/html/2508.12234v1).

Actual read: main-result setup; §4 hypotheses, Proposition 4.3, Lemma 4.5
and its uniform Krylov estimate; Lemma 4.8 and Theorem 4.9 proof through
the limiting martingale argument.

Their stated kinetic dimension is d>=2. Their decomposition permits a
distributional drift part and a linear-growth
part. Uniform negative-Hölder Krylov bounds control additive drift errors;
the existence proof identifies weak limits of regularized kinetic equations.
For the present bounded periodic forces, negative-norm convergence makes
those estimates a conventional alternative to the compact-occupation lemma.
This is an adaptation of the inspected argument, not a claim that their
printed theorem states arbitrary weak-* force stability or thermodynamic
equilibrium closure. The source establishes no competing entropy-to-fixed-
record conclusion in the sections read.

## 4. Thermodynamic ingredient and screened nonmatches

The earlier exact-zero equilibrium characterization for position-only forces
in Hao Ge, arXiv:1209.3081v3, §V.A, was already inspected and recorded in
TARGETED_NATIVE_THERMAL_SOURCE_COMPARISON.md. It should remain acknowledged
as an ingredient; no re-audit was performed here. It is an exact-zero result,
not the present uniform small-entropy topology statement.

Additional targeted searches concerned bounded measurable kinetic drift
stability, weak-* drift limits, small entropy production, Kramers equilibrium,
and Gibbs path closure. Choi–Song, arXiv:2510.06656v1, was inspected only
through its abstract and introductory setup: its nonlinear kinetic collision
model, physical boundary data and weak-solution compactness target differ.
An AHL kinetic regularity article (doi:10.5802/ahl.221) was encountered via its
primary indexed abstract but body access failed. A 2026 kinetic contractivity
article (doi:10.1007/s00208-026-03478-6) was screened only from its primary
indexed result. Neither unopened body is used to infer absence or novelty.

## Assessment to preserve

Known machinery is strong enough to recover native kinetic weak stability.
The useful content to assess in the root theorem is the complete physically
specified inference: all momenta thermalized by a fixed bath, only a force
amplitude cap, vanishing physical entropy, same-bath Gibbs closure, and the
distinction between each fixed acquired record and source-dependent exact
path tests. The independent source check found no printed theorem directly
subsuming that combined assertion in the selected reads. It has not
established historical novelty.

## Follow-up scope correction

Root identified Proposition 5.12 immediately after the previously inspected
Theorem 5.11. A targeted primary read confirmed its statement and proof, and
the comparison above now credits its strongest scope. The earlier comparison
stopped at Lemma 5.8 plus uniqueness, so it unnecessarily retained a moment
restriction and a subsequential formulation. The additional proposition
removes both for a common initial law. Changing stationary preparations,
setwise convergence and Gibbs/thermodynamic assembly remain separate.

This proposition assumes convergence of the drift in its stated anisotropic
norm. It is not, by itself, a printed assertion uniform over all bounded
Borel Markov interventions. No independent review of the new root controlled
theorem was performed in this source follow-up.

