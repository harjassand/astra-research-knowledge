# Port assumptions can be replaced by a measured task-error certificate

2026-10-15. Base b7cada92d2eb304578be5ed974f1e44b10a89928.
Internal mathematical construction and synthetic checks only. No laboratory
data, historical novelty, independent proof review or practical advantage
is claimed. Full proofs are in PROOFS.md; executable checks and their exact
receipts are in check.py and check_results.json.

## Result and useful capability

The incoming port construction does not acquire its premise that every
nonreciprocal coupling lies on known accessible ports. An alternative is to
acquire an error certificate for the actual control task. Fix the computed
adjoint candidate before validation; inject independent random combinations
of the acquired control tangent forces; measure the objective's scalar
response. These physical dot-product discrepancies estimate the norm of
the candidate's task error. They can certify all later chosen first-order
directions in that force span on one probability event, while hidden
couplings outside the ports remain present.

This removes the need to certify global nonreciprocity support for a
sufficiently accurate candidate. It does not manufacture an accurate
candidate if the pilot is wrong. Directly measuring an unresolved proposed
direction is the immediate repair, and is cheaper for a single decision.
The operation is an application of established adjoint dot-product testing
and independent random-sketch cross-validation to an explicitly costed
physical interface.

## Reconstructed source and its exact obstruction

At one fixed loaded linear operating point, Ax=b and the objective
derivative is c. The true adjoint is lambda=A^{-T}c. With accessible port
matrix P, acquire Y=A^{-1}P, z=A^{-1}c and H=P^T Y. The incoming formula is

    alpha = H^{-1} P^T z
    beta  = H^{-1}(H^T-H) alpha
    lambda_hat = z + Y beta.

For A=R+PKP^T with R symmetric and H invertible, this equals the adjoint.
Full interior reconstruction is unnecessary. The source's experimental
objective-trace reanalysis concerns a reciprocal physical-adjoint baseline;
it does not validate this nonreciprocal extension.

The exact pair A±=I±e2 e4^T, b=e1, c=e2, P=[e3,e5] has identical full
responses to every prescribed source. For a conductance change p vv^T,
v=e1-e4, the objectives are J±(p)=∓p/(1+2p). Their initial gradients have
opposite signs despite uniformly positive symmetric parts. Thus even
complete state readout of the prescribed profiles cannot certify the
support premise or choose this action.

## Exact target equivalence and hidden-defect bound

Let Q have orthonormal columns spanning the acquired control tangent-force
space T. For a direction d, the force is f_d=b'_d-A'_d x and the derivative
is F'_d+f_d^T lambda. Only Q^T lambda is needed. Exact task equivalence is

    Q^T(lambda_hat-A^{-T}c)=0.

One proposed force f can instead be evaluated by one forward injection f
and the scalar measurement c^T A^{-1}f. This comparator has the same
additional directional access as the random audit.

There is an exact residual identity even when the port hypothesis fails.
Set D=H^{-T}-H^{-1}, M=A+PDP^T and E=A^T-M. The same port algebra gives
M lambda_hat=c, and hence

    lambda-lambda_hat = -A^{-T} E lambda_hat,
    f^T(lambda-lambda_hat) = -(A^{-1}f)^T E lambda_hat.

Thus a task can be correct while substantial hidden nonreciprocity is
task-dark. If acquired coercivity A_s >= mI and the objective-specific
residual bound ||E lambda_hat|| <= tau are available, every force error is
at most ||f|| tau/m. A global bound ||E|| <= epsilon is sufficient but
stronger than necessary. Those residual/coercivity bounds are additional
acquisitions, not consequences of the original profiles. A source-work
measurement can bound ||lambda_hat|| without full interior readout; its
injection, readout and coercivity assumptions are stated in PROOFS.md.

## Physically implementable probabilistic audit

Fix A, c, Q and a_hat=Q^T lambda_hat from pilot data before validation.
Write g=a_hat-Q^T A^{-T}c in R^r. Draw independent standard Gaussian xi_i,
i=1,...,q, and inject

    u_i=Q xi_i/L_i,       L_i=max(1,||xi_i||/Amax).

Known extra per-channel scaling is allowed. Undo the scaling after measuring
m_i=c^T A^{-1}u_i:

    D_i=L_i(a_hat^T xi_i/L_i-m_i)=xi_i^T g.

There is no clipping or rejection of the Gaussian samples. Suppose acquired
instrument/error bounds give ||D_hat-D|| <= epsilon_D simultaneously. Let
t be the lower delta quantile of chi-square_q. Then

    ||g|| <= U := (||D_hat||+epsilon_D)/sqrt(t)

with confidence at least 1-delta, less the measurement-bound failure
probability. Noise may be correlated, adversarial or depend on xi; the
separate joint bound, rather than a Gaussian noise model, handles it.
Every force f=Qv, including one chosen after seeing the audit, then satisfies

    c^T A^{-1}f in [a_hat^T v-U||v||, a_hat^T v+U||v||].

No action-count union bound is needed for that norm event. Add explicit
F'_d, uncertain force construction and their errors separately. A finite
list of pilot-fixed candidates can share the same profiles, using delta/P
for P candidates. New data-dependent candidates need fresh validation or
a justified simultaneous procedure.

This is a fixed-plant frequentist guarantee. It is not deterministic
closure of every plant selected after the random probes. It applies at
the current operating point, and does not turn a positive local derivative
into an unqualified finite-action improvement. Finite steps need actual
resolvent/curvature bounds or direct action verification.

## Amplitude, precision and interface costs

If each unscaled scalar discrepancy is bounded by epsilon0, one must use
epsilon_D=epsilon0 sqrt(sum_i L_i^2). In expectation

    r/Amax^2 <= E L_i^2 <= 1+r/Amax^2.

At fixed q/confidence, the measurement contribution to U therefore scales
approximately as epsilon0 sqrt(r)/Amax. Small profile count does not mean
dimension-independent precision or energy. Without capping, expected
total squared source amplitude is qr. With capped injections and
independent repeats of sub-Gaussian variance proxy sigma^2, a sufficient
repeat count for measurement contribution at most eta is

    n >= 2 sigma^2 log(2q/delta_m) sum_i L_i^2 / (eta^2 t).

This is the certificate's sufficient cost, not a lower bound for an easy
single action. Settled source work can be bounded using acquired coercivity;
drivers, sensor integration, thermal/electrical settling and reset remain
separate physical costs.

Starting with the incoming pilot, the ideal profile total is k+2+q:
one baseline, k port profiles, one objective-source profile and q validation
profiles. Pilot sensing must still supply the rows needed for the control
forces/candidate. Each validation profile requires the objective scalar
readout, with all physical sensors/multipliers needed to realize it.
Synthesizing the candidate field physically, if desired, costs another
profile; the digital task certificate itself does not require that synthesis.

Required additional access is signed source injection on the control-force
support, not merely on the original k asymmetric ports. Having voltage
sensors at those vertices does not supply current drivers there. The drivers
must be permanently loaded or equivalently calibrated so every profile sees
the same A. Balanced plus/minus perturbations can double q profiles. Source
mismatch, sensor gain/offset, drift, finite-amplitude nonlinearity and
uncertain c or tangent forces need acquired joint error budgets. Small
current error alone does not bound its consequence without a transfer bound.
Euclidean source norms refer to declared calibrated units; a physical
energy or hardware budget must be mapped to those units.

## Completion can follow the decision geometry

Exact direct probes on a force-coordinate subspace U determine g_U. Given
an acquired norm bound ||g||<=eta, let
rho=sqrt(eta^2-||g_U||^2). The exact vector-ball interval for a force v is

    a_hat^T v-v_U^T g_U ± rho ||v_Uperp||.

It is attained by parallel/antiparallel remaining error. With noisy direct
probes, optimize over their joint slabs/ellipsoid intersected with the norm
ball; do not substitute a noisy point projection into this formula. Extra
device structure can narrow this information class.

If the interval does not separate a decision, measure a critical force
directly and audit only the unresolved subspace when useful. Fresh random
stages with summable failure allowances retain the conditional guarantee.
This is task-restricted active linear design, not a new optimization
algorithm. One native tangent probe settles one proposed first-order
direction in the noiseless setting; the random operation is potentially
useful when many subsequent directions share a coarse accuracy certificate.

## Unknown low rank still hides support

Even bounded, uniformly coercive plants can hide a target direction.
Let V contain all queried source profiles and c. Choose unit d in Vperp,
c_hat=c/||c|| and 0<a<=1. The rank-two family

    A±=I±a c_hat d^T,       A±^{-1}=I∓a c_hat d^T

has identical complete responses on V, symmetric-part minimum 1-a/2>=1/2,
and operator/inverse norm at most 1+a. But

    c^T A±^{-1} f = c^T f ∓ a||c|| d^T f.

Choosing d along the unqueried part of f attains half-width
a||c|| dist(f,V). A deterministic adaptive exact algorithm has the same
obstruction along its identity-response transcript. Thus unknown low
nonreciprocity rank does not acquire its orientation or support, even
with uniform conditioning bounds. This is a bounded active linear class,
not a claim that arbitrary directed couplings are resistor-only devices.
It is distinct from, and weaker than, the parent's unrestricted
unbounded-completion theorem.

## Strong comparators and capital transfer

The relevant existing operations are:

* [Claerbout's adjoint dot-product test](https://sep.stanford.edu/data/media/public/docs/gem/ajt/paper_html/node19.html):
  random vector inner products are an established adjoint consistency check.
* [Ward, Compressed Sensing with Cross Validation](https://arxiv.org/abs/0803.1845):
  independent sketches estimate residual norms of fixed candidates;
  the independence requirement is essential. Our chi-square form gives
  an exact Gaussian confidence factor and explicitly charges physical
  normalization and measurement error.
* [Fiez et al., Sequential Experimental Design for Transductive Linear Bandits](https://arxiv.org/abs/1906.08399):
  directional information should be purchased for the decision set;
  a full gradient is not automatically optimal.
* [Bösch et al., Unifying Physical Backpropagation](https://arxiv.org/abs/2608.11585):
  general same-hardware physical backpropagation and random-direction
  Taylor gradient checks are existing baselines. Their assumptions and
  access must be matched rather than treating a reciprocal baseline as
  the strongest alternative.
* [McCaughan et al., Multiplexed gradient descent](https://arxiv.org/abs/2303.03986):
  multiplexed perturbation-based physical training is a further
  random-direction baseline.
* [Spall's SPSA](https://www.jhuapl.edu/SPSA/Pages/):
  two objective measurements can form one simultaneous-perturbation gradient
  estimate, with noise, bias and iteration costs. A full adjoint should be
  compared against the resulting decisions, not just coordinate differences.

With equal injection/readout access, direct tangent evaluation dominates
for one chosen local direction. For a finite decision set, compare
decision-focused sequential direct probes, randomized finite-action trials
and SPSA/random-direction optimization, including pilots, resets, source
amplitudes, precision, settling and held-out updates. Neither a q-profile
certificate nor a full gradient establishes a practical advantage.

N820's calibrated target-row-span theorem and the current FS decision-fiber
criterion remain exact deterministic standards. The audit changes the
quantifier to fixed-plant probabilistic task accuracy with new directional
access; it does not evade them. N841's joint-response and detector gates
transfer as acquisition requirements, not numerical circuit bounds.
PR90's native stochastic lower bound has a different interface/model and
does not imply a circuit lower bound. The frozen late audit recorded its
then-open state; a fresh read-only GitHub receipt now records PR90 as merged.

## Checks, decisive next test and unresolved gate

The checker reconstructs the incoming counterexample symbolically, verifies
the stable rank-two pair exactly, and tests the port/defect identities on
48 synthetic matrices. Maximum exact-port and defect-identity errors are
1.59e-15 and 2.28e-15. All stated numerical assertions passed.

A synthetic rank-32 audit with q=16, source cap 1 and assumed scalar error
1e-4 has true task error .04 and upper bound .0577454. A candidate direction
with predicted gain .4 receives lower first-order gain .342255; actual
synthetic gain is .395636. Total capped squared source amplitude is 16,
versus 534.102 unscaled. One direct tangent query is cheaper for this one
decision. A 6000-draw diagnostic has coverage .9475 around theoretical .95;
it is neither a proof nor laboratory noise calibration. The separate
rank sweep exhibits the expected square-root precision penalty.

Highest-value next test: a controlled low-voltage linear network with
permanently attached mixed current drivers on the actual control-force
support and a calibrated hidden directed coupler outside the advertised
ports. Freeze the pilot candidate, run capped independent audit profiles
under a separately acquired joint error allowance, then measure held-out
directions and actual bounded conductance updates. Include hidden
task-visible and task-dark couplings. Compare optimized direct tangent and
randomized finite-action policies with identical native access, elapsed
time, source/readout work, reset and precision budgets. Report acceptance,
rejection and all failed decision separations.

The strongest missing physical premise is a calibrated, same-operator
directional injection/measurement interface with a credible simultaneous
error allowance at the required amplitude and precision. This investigation
derives a conditional operation and its costs; it has not acquired that
interface or demonstrated a device benefit.
