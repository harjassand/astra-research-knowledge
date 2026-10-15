# ASTRA ULTRA — Foundational Capability Genesis, second investigation

15 October 2026, Australia/Brisbane. **Mission: NOT_ACHIEVED.** The strongest
surviving contribution is an internally complete general convolution criterion,
with an explicit dependent scalar kernel that defeats every product and every
Gaussian alternative for the same exact positivity task. No new experimentally
qualified physical operation, exceptional foundational significance, historical
priority, or complete-resource technological advantage was established.

The three supplied pasted texts were read and copied with exact provenance.
No missing research package or audit was sought or used as a premise. The
earlier phase-clock campaign is preserved separately and was not restarted.

## Strongest mathematical operation

Let T be a compactly supported finite-order Hermitian d-by-d matrix-valued
distribution on R^m, with total mass T(1)=I. A distribution here permits signed
densities and derivatives of delta masses. Define its real Laplace transform

    L_T(g)=<T(y), exp(g·y)>,       g in R^m.

The internally proved criterion is:

    L_T(g) is positive definite for every real g
    iff some scalar probability noise with every exponential moment
        makes T*noise a positive matrix distribution.

Whenever this is possible, the noise can be a single smooth radial strictly
log-concave density p. The result T*p is then positive definite at every
point, normalized to I, and has every exponential moment, as do its derivatives.
The noise depends on T. This is pointwise matrix positivity of L_T(g), not
Bochner positive-definiteness of a function on a group. Semidefinite transforms
with zeros do not suffice for normalized mass I. The proof also treats singular
matrix masses using a constant-kernel condition, and general Banach cones with
an interior normalization under its stated norm-distribution hypotheses.

The construction retains the positive exponential tangent L_T(grad V(x)) and
expands only the local curvature remainder of p=exp(-V)/Z. Unlike the supplied
quantum-tuple result, it assumes no exponential lower bound on the Laplace
positivity margin. An explicit sequence of smooth slope transitions makes
curvature decay fast enough relative to the worst margin on each gradient
ball, while the slope still diverges. Thus p has every exponential moment.
The necessity proof uses compact cutoffs and works even for probability noise
without a density; positive output forces strict transform positivity.

The difference in hypotheses is real. A compact smooth signed scalar kernel
is constructed whose real Laplace transform is everywhere positive but has
valleys below exp[-exp(r_n²)] along an explicit sequence. Any positive
regularization forces noise cumulant growth at least exp(r_n²)-O(r_n).
Consequently no density bounded in both tails by C exp[-c|x|log|x|], for any
c>0, can regularize it. The adaptive all-exponential-moment construction still
does. This is an analytic example, not a numerically resolved tiny valley.

Evidence: [full proof](workers/mathematical_invention/PROOF.md),
[producer report](workers/mathematical_invention/REPORT.md), and
[independent construction](workers/laplace_consequences/REPORT.txt).
The latter uses a different sum-of-square-root potentials and an independent
compact signed-measure product for the no-exponential-margin example.
Root reconstructed the slow-slope/finite-jet proof, cutoff necessity,
full-complex Paley–Wiener bound, and tail-class separation. These are internal
analytic proofs, not external review or formal verification.

## A fully explicit consequence with a global margin

Consider Qp=p+partial_x² partial_y²p, whose real Laplace symbol is the
strictly positive scalar SOS polynomial 1+g_x²g_y². Put

    rho=sqrt(1+(x²+y²)/25),
    p(x,y)=Z^(-1) exp[-5 rho log rho].

Then p is smooth, radial and strictly log-concave, and

    Qp >= 0.1832635445963654... p > 0   everywhere,
    integral Qp = integral p = 1.

The global inequality is proved by bounding five negative derivative terms,
not inferred from a grid. Qp preserves both coordinate marginals and the
covariance of p, while E_Qp[X²Y²]=E_p[X²Y²]+4. This is a concrete operation
on dependence invisible to those lower-order descriptions.

Every strictly positive C² product density with every exponential moment
fails to make Qp even nonnegative. At a point where g''<0, a putative product
f(x)g(y) would force f''<=Kf globally; cutoff integration against exp(tx)
then gives (K-t²)M_f(t)>=0, a contradiction. Every nondegenerate Gaussian,
including arbitrary correlation and translation, fails too. Thus merely
adding correlations through a Gaussian does not supply this operation.

The construction and bounds were independently reconstructed. Symbolic
differentiation and a 151,601-point grid checked the formulas; the grid is
diagnostic. An initial rounded constant and intermediate floating overflow
were corrected before freeze and recorded. [Explicit proof](root/EXPLICIT_DEPENDENT_KERNEL.md)
and [calculus receipt](root/DEPENDENT_KERNEL_CHECK.json).

## Closest mathematics and the remaining consequence

Positive convolution multipliers are established mathematics. The accessible
Katkova–Vishnyakova 2001 theorem already obtains a nonnegative scalar
convolution from strict bilateral Laplace positivity for a compact-interval
input positive at both endpoints, without a quantitative global transform
margin. Its multiplier is one-sided and atomic. The proposed smooth compact
examples have zero support-boundary values, and the current target additionally
specifies radial strict log-concavity, arbitrary dimension, matrix/cone values
and strict all-space output. These differences do not establish priority.

Diamond–Essén, *Functions with non-negative convolutions* (1978), is a decisive
older predecessor. Its publication was verified, but its exact theorem text
could not be retrieved through the accessible publisher routes. **Historical
novelty is UNKNOWN.** Poincaré–Pólya–Handelman coefficient/multiplier results
and matrix polynomial positivity certificates are additional close precedents.
[Exact comparison and access limits](workers/laplace_literature/PRIMARY_COMPARISON.md).

The mathematical consequence is an exact existence criterion and new-to-this-
investigation constructions for positive representations of signed distributions
and constant-coefficient differential operations. It does not decide positivity
of an arbitrary symbol, give an efficient kernel compiler, optimize variance,
stabilize deconvolution, or establish a computational speedup. Thresholds may
be enormous and require supplied lower margins on entire real gradient balls.
The next proof with operational consequence would turn specified computable
margin/seminorm bounds into finite-precision, finite-cost constructions with
useful noise and sampling bounds. Exact comparison with Diamond–Essén is
required before making a priority claim; specialist proof review is open.

## An obtainable qubit format that loses to its incumbent

For a radial positive qubit kernel M(x)=u(r)I+v(r)n·sigma, root and the Capital
constructor obtained a direct compiler: sample r with density 4pi r²u(r),
measure a uniformly random spin direction once, and classically flip the
resulting direction with mean v/u. This avoids estimating a Fourier transform
from many copies. The gamma kernel in the pasted input was reconstructed;
its existence was supplied, not newly invented here.

The entire operation is state-independent classical postprocessing of the
existing covariant spin POVM. That incumbent statistically dominates its
output for every state-inference decision. Hence the compiler supplies the
requested exact projection-law format without an information-acquisition
advantage under the same random-axis interface. Its raw coordinate second
moment is about 8.639917, versus 3 for the ordinary covariant 3n estimator or
random-Pauli shadows on the maximally mixed state. Radius quadrature and ideal
continuous rotations are not certified finite-precision hardware.

A separate analytic bound shows exact all-linear scalar noise must have
coordinate variance at least 2+64/(27pi^4), exceeding the ordinary unbiased
covariant value 2. This is a nonoptimal constraint on this exact output format,
not a universal estimator/sample-complexity lower bound.
[Compiler and comparator proof](root/PAULI_OPERATION_AND_VARIANCE.md).

## Scalar acquisition: exact generic recovery, decisive collective failure

An independent investigator derived a scalar-only calibration schedule for
f(u)=c^T(A+P diag(u)P^T)^(-1)b. With fixed real linear apparatus, calibrated
independent additive rank-one controls, permissible values and nonvanishing
algebraic separation conditions, (3m²-m+4)/2 scalar configurations recover
the future diagonal-control response map. Singletons identify local terms,
pairs leave two directed choices, and triples align them. A weighted-transpose
ambiguity remains but predicts all permitted actions identically.

The exact theorem is generic, with no uniform noise tolerance. At m=32 its
1,522-query initial four-level synthetic reconstruction had median held-out RMS
error about 1.8e-12; absolute noise 1e-4 raised it to about .547. A separately
executed ternary {0,1,2} schedule gave noiseless median error 3.27e-12 and about
.684 at noise 1e-4. Failed real-root estimates were counted. Exact weak-anchor examples invalidate a uniform
robustness claim. A stronger directed-cycle pair agrees under EVERY intervention
on fewer than all m controls while retaining a constant-size collective
response difference with polynomial matrix conditioning. At m=32 two collective
actions are ranked oppositely. One full-support experiment separates the pair;
no exponential experiment lower bound is claimed. Its O(m) control amplitudes
and O(m²) total conductance are charged.

Measured-model wave control, Virtual VNA and a 2026 read-once-determinant learner
are strong existing comparators. No matched physical/model-fitting win was
executed. The decisive experiment would calibrate an actual apparatus blindly
and compare held-out collective predictions at equal precision, switching,
settling, source/readout and reuse costs.
[Proof and obstructions](workers/scientific_operation/CONSTRUCTION_AND_PROOF.txt)
and [competitors/costs](workers/scientific_operation/COSTS_AND_COMPARATORS.txt).

## Physical sequences: stop at measured interfaces

The independent isotope route selected load/close/purge/harvest in one
experimentally studied Cu-ZIF-gis bed. The broad thermal gating cycle is
already published prior art. An additional purge that doubles isotope odds
while retaining 90% of captured D requires cumulative unwanted/desired escape
exposure ratio at least 7.5788. Existing uptake, single-gas diffusion and mixed
breakthrough results do not supply that fractional-release/receiver balance.
The next decisive measurement is a mass-balanced mixed-feed release curve on
the same bed, followed only if it passes by a complete-cycle energy/recovery
comparison. No further hypothetical pulse optimization is justified.

A room-temperature graphene capture/release alternative also stopped: separate
pure-isotope tests do not qualify mixture separation, and the reported surface
density stores at most 3.34 micrograms D per square metre per fill even granting
all-D occupation. Strong palladium thermal-cycling and quantum-sieve competitors
already deliver separation; no lower-cost isotope capability was established.
[Physical mechanism, competitors and decisive experiment](workers/physical_invention/REPORT.md).

An independent model challenger found a positive established precedent:
Tong et al.'s double-gated/twisted-bilayer graphene experiments use field and
carrier control to separate transport from hydrogenation and select the reacting
layer. Same-device layer/proton measurements make this evidence for attainable
selective control. Credit belongs to those authors. It supplies no battery
coefficients or new Astra operation; the bilayer also loses proton flux relative
to the earlier monolayer. The article's conflicting proton-XOR ratio statements
were retained with the conservative body value. This supports the user's
co-design hypothesis in a specific apparatus, without proving a universal
explanation. [Primary evidence and limits](workers/model_discovery/PHYSICAL_MODEL_CHALLENGE.md).

## Collaboration and resource scope

The initial allocation was three independent Sol Max construction leads plus
one Luna Max model challenger and one Luna Max Capital scout. Two targeted
workers then deepened the mathematical proof/consequences and predecessor
comparison; a Luna Max continuity worker prepared preservation. Eight distinct
workers participated in this investigation: four Sol Max and four Luna Max,
plus root. Continuing investigators owned their constructions.

Collaboration changed the result: an independent potential construction closed
the arbitrary-margin proof; root's scalar differential example became an
explicit all-point construction and a product/Gaussian impossibility theorem;
the Capital scout replaced Fourier reconstruction by a direct one-shot compiler
and strong existing comparator; physical qualification stopped two unsupported
separators; and low-order control calibration gave way to exact collective
countermodels. The allocation was productive in these concrete senses. It was
not a controlled test of swarm efficiency, and worker agreement is not external
validation.

Five copy-first selected scripts passed using three subprocess slots in
2.893 seconds of bounded script wall time; a separate ternary replay passed
in 2.478 seconds. This is not inference expenditure
or total research time. Model tokens, pure inference time, aggregate worker
compute, energy, monetary cost and network-transfer telemetry were unavailable.
No laboratory experiment, paid compute job, purchase or message to outside
people occurred. Primary papers were inspected; raw source files remain local.
[Resource ledger](RESOURCE_LEDGER.json) and [replay receipts](root/REPLAY_RECEIPTS.json).

Capital preservation starts from freshly fetched main
03b51f364080972740e2207aa2c3e1fa803c08eb, after PR92 merged during this run.
The earlier FT packet remains byte-identical. New results remain
source_derived_unreviewed, with separate proof/priority and capability gates.
Publication/integrity receipts will be separate from this frozen science report.
