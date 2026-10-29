# Root review of additional consequential uses

29 October 2026. Ordinary mathematical review, not external acceptance or
empirical validation. This note records newly checked uses; it does not
routinely re-audit preserved predecessor results.

## Finite-window Wasserstein and unbounded observables

Reviewed physical_frontier/BOUNDED_FORCE_WASSERSTEIN_UPGRADE.md at SHA256
d23e011984ca60c42154f18be876e8d9556ec8e232d70efdd2e037d396478721.

The proof is valid. The stationary momentum estimate begins with bounded
increasing truncations of the OU mild formula. Exponentially shrinking p_0
tends to zero in probability without a moment assumption; Slutsky and then
monotone convergence establish all stationary moments. No hidden initial
integrability is assumed to prove integrability.

The integration-by-parts bound on the OU stochastic convolution gives
sup|p|<=|p_0|+A/gamma+2sqrt(2gamma tau)sup|W|. The displayed Doob estimate
therefore supplies uniform finite-window high moments at the exact source
parameters. It applies to the same Gibbs competitors.

For d_0=min(1,d_infinity), Kantorovich--Rubinstein duality agrees with the
stated bounded-Lipschitz convention: center a Lipschitz test at a base point.
A coupling of small d_0 cost has small probability of distance greater than
one. The r-th distance moment is at most 2^r M under every coupling, so
Holder on that exceptional event gives exactly

    W_p^p <=d_BL+(2^r M)^(p/r) d_BL^(1-p/r),  r>p>=1.

The SAME Gibbs competitor sequence therefore works for every fixed finite
W_p. The consequence bounds for fixed Lipschitz and uniformly polynomial-
sensitive functionals follow by coupling and the already proved moments.
These are finite physical windows. They do not justify integrating survival
probabilities over infinite time without a separate time-tail argument.

## Native phase and exact dynamical challenge

Read the full original phase construction, paired-reference note and the
exact dynamical score, together with
alternative_frontier/RELATIONAL_PAIRING_AND_DYNAMIC_INFORMATION_INDEPENDENT_REVIEW.md.
The dynamic proof's reviewed original SHA256 is
5ffae82b10e325024a47b980e4bb4e92078f32fb8e44e554b0c49b7253e2602f.
It is preserved under reviewed_versions/.

The root check confirms f'=n cos(z)v and the Ito formula with no missing
quadratic-variation term from z, which has finite variation. The ratio
f'^2/(1-f^2)=n^2v^2 holds outside a zero-occupation-time set. Hence the
record-derived score is a common measurable C1-path statistic and its
two drift means are plus/minus A h r(c)/c. The score moment/TV inequality
gives the saved constant exactly. It is an ideal exact-path observation,
not a finite-noise algorithm.

The relational product H conjugate(Z)=exp(i phi) is pointwise. It removes
the need to estimate an ensemble covariance only because the known SO(2)
source relation is supplied. It does not infer an arbitrary hidden map.
One actual simultaneous quadrature pair suffices with the stated error
balls; separate exact marginal laws do not supply the relation.

The timing correction is necessary: the free stationary Gaussian increment
law is valid at fixed/independent acquisition times. A velocity-selected
stopping time changes its conditional mean. Root incorporated this correction
and the scalar tangent exception. The single-potential reflection claim is
now explicitly restricted to the receiver/scalar-force record, excluding a
separately reported driver velocity. The original baseline translation
ambiguity still holds even when driver velocity is reported.

The two-probe mean requires its finite receiver factor
1-exp(-gamma h). At u=A/n its sufficient sample count grows quadratically;
under only an upper bound on u it can grow faster. The rigorous quadratic
lower bound concerns independent STATIC Gibbs readouts. The exact dynamic
challenge prevents promoting it to a universal bounded-force acquisition
ceiling.

## Review limits

The operational-forgetting and adaptive-orientation complementary notes
retain their authors' ordinary proofs and their expressly limited review
status. They are not load-bearing premises of the new native equilibrium/
intervention closure. The alternative quantum-reference branch also remains
separate. No review of one branch is transferred to a different physical
interface or a later theorem without a new argument.

## Quantitative native position regularity and force information

Reviewed causal_frontier/QUANTITATIVE_POSITION_REGULARITY_AND_FORCE_NORMS.md
at SHA256 31e42b9ea25d784e3cf0c9c0ac30a230675e64ad272b088e4dda2145fa1bdd9e.
The complete ordinary argument is valid at its stated stationary class.

The weak Duhamel formula has a plus force term; the density convolution
formula has minus divergence. Its near-zero L1 integrability follows from
a_s=O(s), v_s of order s^3 and ||grad G_v||_1=O(v^-1/2), leaving s^-1/2.
The stationary momentum cutoff justifies the generator differentiation.
Vector force-weighted pushforward measures have total variation at most A.

The Gaussian Hessian bound uses E|Z(Z.e)-e|^2=d+1, which is correct.
Extending the min(L s^-1/2,H r s^-2) integral to infinity and splitting at
(H r/L)^(2/3) gives exactly 3L^(2/3)H^(1/3)r^(1/3). Thus the source has
a uniform L1 translation modulus without requiring a density floor.

For a fitted Gibbs candidate, L1 smoothing of the difference costs
||grad eta||_1 e/delta, by coupling and the L1 kernel derivative. Combining
source 1/3 regularity with the Gibbs L1 gradient bound gives e^(1/4).
This use is stronger than an arbitrary weak-to-TV inference and is justified
by the native regularity just proved.

The identity (F-G)m=R+tau grad(n-m)+F(m-n) is exact. Division occurs only
by the Gibbs candidate m, whose floor and logarithmic gradient are known.
In particular div(phi/m) has bound c_G^-1(d+A/tau); it does not require
an extra factor d on the logarithmic-gradient term. This validates C_R,C_N
and the initial phase-space TV formula.

The kinetic block reduction to position frequencies 2^(3j) is valid because
F-G is independent of momentum. A projected fixed smooth anisotropic cutoff
has bounded position L1 kernel and C1 size O(2^(3(d+1)j)). Splitting the
dyadic SUPREMUM, not a frequency sum, gives exponent beta/[3(d+1)] and no
endpoint logarithm. Fixed bath-coordinate changes affect constants only.
This estimate is not being transferred to arbitrary momentum-dependent
unknown baseline forces.

## The stronger source density floor

Reviewed physical_frontier/QUANTITATIVE_STATIC_FORCE_BALANCE.md at SHA256
a4e577ce8e27db9a167d6e82184452c038917e560ff2e444315839175a7665fa.
The root independently checked its new terminal-position bridge, not just
the already reviewed all-set bound.

Conditioning the Gaussian stochastic integral Y_t on its endpoint produces
Brownian drift K(t-s)(r-Y_s)/V_(t-s). Its residual covariance and mean are
the stated Gaussian conditional formulas. Concavity gives
V_v>=v K(v)^2/3, so the expected bridge drift is integrable, including the
terminal singularity. Its integral is bounded by
|r|J_t/V_t+2sqrt(3dt).

Smooth F(q_s) has pathwise finite variation on a finite continuous kinetic
path. The stochastic integral therefore has the common integration-by-parts
version under free and conditioned laws. Under the bridge its innovation
integral has zero mean and its finite drift term is controlled solely by A.
Conditional Jensen gives the endpoint likelihood lower bound. Choosing a
nearest torus winding restricts |r| to the torus diameter independently of
the initial momentum. Disintegration establishes the density floor almost
everywhere. Stationarity then gives the same floor for the position marginal.

This floor has no claimed regeneration of momentum or controller memory.
The smoothed Boltzmann construction and scale correction yield the improved
static exponent 1/(2d+4) with their explicit potentially large constants.
The learned-candidate force theorem above does not need this source floor.

## Quantitative transition and full-path bounds

Read the complete independent review/strengthening at SHA256
905142e9aaa4dca0f7ce77efe65a0322064e6ede6bfb7304a75db7692900ef66,
which reviews the root original 363af8817b0106ad7410107ace7ce14d1bbdab83aed616a9f0036157b1a88cf2.
Root also inspected the exact primary product and Schauder statements.

The safe weighted proof uses L_infinity -> C_B^0 in the correct direction.
The stronger endpoint extraction smooths to C_B^(1/8), avoiding the false
reverse embedding at regularity zero. Its source beta integral has powers
3/16 and 3/4, leaving h^(1/16). The feedback term uses free L_infinity
contraction and the weighted w bound, leaving h^(3/8). Both constants and
the common Borel-control limiting argument are sound. The resulting
uniform-mesh path power eta^(8/23), with its Brownian logarithm, follows.

These are quantitative theorems in fixed analytic constants. The absence
of instantiated numeric Schauder/product/cutoff constants remains an actual
operational limitation, not a missing hidden-physics assumption. The fixed
numerical LP fixture is not an acquisition of a low-entropy native source.

## Finite constrained position selection

Root read the complete ordinary proof in alternative_frontier/
FINITE_POSITION_SELECTION_BRIDGE.md at SHA256
2ca60f0d01c51a6e7e636c032d28a74c4eaa0a54ed18c87abb9bb4ff7ec7f90d.
The ratio-constrained transport LP, McShane extension, mollification and
static error inequalities are valid. The dyadic multinomial bound charges
dimension and true cross-trial independence. Inner rational coefficient
loss is bounded by an explicit mixture with uniform, so saturation is not
silently treated as robust. The source's finite arithmetic execution is
its own checked certificate, not a new native experiment or dynamic solver.

## Snapshot history composition and finite entropy-upper acquisition

Root read the complete final snapshot proof, SHA256
82f03e795b525e7f7fbe64a9d1fea37d28c4d1f1a0ffd94ea113a50ee84d849a,
including Section 7's use of the completed stronger transition bound.
Augmented-state kernel contraction is valid for arbitrary standard-Borel
reports and measurable history-selected branch controls. The transition
bound is uniform in start time, state and branch field, so the same candidate
works before the program choice. Subdivision needs at most m+T/h0 pieces;
each costs at most C_imp eta. Arbitrarily short report-chosen gaps are covered.
Path-triggered timestamps or accumulated between-snapshot records are not.

The initial condition is a JOINT physical-state/history bound. A shared
calibration record plus genuinely fresh baseline service permits the stated
conditional population bound; an unreset correlated source does not. The
finite-record TV guarantee is not full continuous-path TV.

Root also read FINITE_PHYSICAL_ENTROPY_UPPER_ACQUISITION.md at SHA256
335a6a3d43257e33344ef94540cab0eba88f0edabaafb198873b7d1ebae9882b.
The clipped-component identity for capped energy is exact. The capped-energy
map is globally 2sqrt(R)-Lipschitz, so finite-range momentum calibration is
sufficient without approximating arbitrarily large p. The fourth-moment
bound, block Chebyshev probability 1/4, odd-block Hoeffding failure exp(-k/8),
and tail bias C4/(4R) all check. Uniform metrology errors may be correlated;
they are charged on their own event, not counted as independent samples.

The source energy identity is used only in its native stationary domain.
Bath uncertainty must be maximized over its calibrated interval. A successful
mean estimate does not promise that the resulting entropy upper bound is small.
The proof supplies a finite acquisition contract, with no executed source assay.

