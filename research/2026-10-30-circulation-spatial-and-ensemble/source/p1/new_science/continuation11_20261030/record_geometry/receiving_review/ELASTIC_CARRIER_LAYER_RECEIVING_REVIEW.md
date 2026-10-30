# Actual receiving review: elastic carrier density law

30 October 2026. Existing Astra P1 / record_geometry role.
No root file was edited; no new agent or numerical fixture was used.

## Received versions and decision

Original: ELASTIC_CARRIER_LAYER_AND_DENSITY_LAW.md, SHA256

7f3ecd1fcc7ac70b451fe10a206fd0df17d0bc679dbd90e7f85bc307ea31606a

Binding correction: ELASTIC_LAYER_CORRECTIONS.md, SHA256

b8b8dcf06013b559b558499aa1428117f22c83516add9440a16e211bc18ca72e

Both exact inputs are snapshotted beside this receipt. The earlier role
RESULT and MANIFEST were also preserved before any update.

**Accepted as original plus binding correction**, at the stated ideal
mechanical/source interface and at the corrected finite-force interface.
The preparation-to-joint-density bridge is sound. The original
continuous-time mesh wording and the unqualified finite-force bounds
needed corrections; root preserved the original and supplied both.
No further load-bearing error was found in the scoped review.

No forthcoming tracking, interpolation, work, controller-readout or native
path-LDP theorem has been assumed.

## 1. Local unread jitter supplies the initial ceiling

For one row, orthogonal projection of uniform coordinates in [-w,w]^N onto
the mean-zero hyperplane has density at most sqrt(N)(2w)^(1-N).
The normal fiber length is at most 2w sqrt(N), with Euclidean induced
hyperplane measure. With w=c_0/sqrt(kappa), gap deviations are at most 2w.
The uniform upper bound on V'' near one gives U_row<=C N.

Strong convexity and det'(L_N)=N^2 give

\[
Z_{\rm row}\le (2\pi/\kappa)^{(N-1)/2}/N.
\]

The positional density ratio is therefore at most

\[
N^{-1/2}\left[\frac{\sqrt{2\pi}}{2c_0}\right]^{N-1}e^{CN}.
\]

The kappa powers cancel. The projected Gaussian velocity and neutral
coordinates have precisely the relative reference factors. Across N rows,
the ceiling is exp(C N^2). Initial correlation of the center coordinate
with the projected jitter does not invalidate the marginal relative bound.

This is an actual preparation law, not an implication of invariance.
Exact point placement, or conditioning on a record of every continuous
jitter, can be singular and is not covered.

## 2. Nonlinear local geometry and autonomous relative dynamics

For the displayed spring, finite relative energy confines every gap to
(0,2). The convex domain is bounded after removing translation.
Endpoint divergence prevents a finite-energy conservative trajectory from
crossing or stretching a link beyond this range.

Translation invariance cancels internal forces in the actual collective
equations. The uniform command disappears from the projected equations
even if it depends on records correlated with relative coordinates.
Conservative transport preserves relative energy and volume. During the
bath the positional/velocity Hamiltonian flow and the orthogonal
neutral/source rotation preserve the product reference. The fresh
collective Gaussian source is independent of its relative components.

Thus the previously received untuned response applies at the explicitly
common-within-row parameter interface. Arbitrary particlewise response
mismatch is properly excluded. For the broader homogeneous row potential
class, the ordinary smoothness needed for the conservative flow is
understood. Cyclic row symmetry implies E_Pi u=0 without requiring V to
be even.

The finite-force sublevel estimates in the correction concern the explicit
potential. For a different unknown convex endpoint-divergent potential,
an upper bound near one does not supply a quantitative force or derivative
envelope at every energy sublevel. Such an envelope would be an additional
physical premise. This does not obstruct the broader ideal density result.

## 3. Joint concentration and the corrected continuous-time argument

The covariance inequality of Brascamp--Lieb applies on the mean-zero
space. The actual primary source cited by root was checked:
[Carlen, Cordero-Erausquin and Lieb, arXiv:1106.0709, Eq. (1.3)](
https://arxiv.org/pdf/1106.0709). Under every linear tilt, the Hessian
still dominates kappa times the block cycle Laplacian. Integrating the
variance bound along that tilt gives the displayed sub-Gaussian proxy.
Convex barrier approximation supplies the bounded-gap domain version.

The independent Gaussian representation of exp(eta ||u||^2) then gives
the determinant bound. With eta=c kappa/N^2, its largest covariance
eigenvalue is uniformly below the singularity. The log determinant is
O(1) per row because the inverse cycle eigenvalues sum to O(N^2), hence
O(N) for all N rows. In particular the proof gives the stronger event

\[
P\{\|u(s)\|>\epsilon N^2\}
\le \exp[C_1N^2+C_2N-c\epsilon^2\kappa N^2].                 \tag{R1}
\]

The deterministic density error is at most C/N+||u||/N^2, uniformly in
all row translations C_y. Thus the joint volume exponent is correct.
A union of only row-speed concentration bounds would not have been enough.

For the time extension, convex dilation about the minimizer gives
Z((1-alpha)U)<=(1-alpha)^(-d)Z(U), with d=N(N-1).
The two Gaussian relative factors contribute another
(1-alpha)^(-d). The energy exponential moment is therefore
exp(C_alpha N^2), uniformly in stiffness. The preparation ceiling changes
only the volume-order constant.

Within each cell, relative energy plus the fresh source's energy is
conserved. Reference preservation at cell starts, followed by a union over
O(N^2) cells, proves the supremum-energy estimate at height C N^2 log N.
It is not necessary or appropriate to add all source energies over the
whole observation horizon.

The original mesh sentence invoked only the weaker density event.
That would not itself rule out density cancellations between rows that
later translations remove. The binding correction now uses (R1) at the
mesh times. Off the energy event,

\[
\|v\|\le C N\sqrt{\log N},\qquad
\frac{\|u(s)-u(s_j)\|}{N^2}\le C\frac{\sqrt{\log N}}N
\]

over a bounded physical interval. This proves the uniform time result
without assuming a collective-speed or collective-force bound.
The repair is complete.

## 4. Exact current identity and the deferred interpolation premise

For f of zero horizontal mean and partial_x psi=f, the actual chain rule
at every bead gives

\[
\langle Y_N(t),f\rangle
=\langle\rho_N^{aux}(t)-\rho_N^{aux}(0),\psi\rangle.
\]

The N^{-3} current and N^{-2} density normalizations agree, and the sign
matches integrated continuity. For s>3, unit H^s tests and their horizontal
primitives have uniformly bounded first derivatives. The density-path
estimate therefore controls the zero-horizontal-mean current component.

The horizontal mean available in this file is the row-atomic field with
weights A_y/N^2. To replace it by a step field, one sufficient separate
premise is exponential tightness of

\[
\sup_{t\le T}\frac1N\sum_y|A_y(N^2t)/N^2|.
\]

The interpolation error is then C/N times this quantity. The original
explicitly defers the necessary norm control to tracking. This receipt
does not certify that later result or infer the needed control from
negative-Sobolev tightness alone.

## 5. The finite-force correction is substantive and correct

The original allowed arbitrary kappa_N -> infinity but stated clearance
c kappa/H_* and force C H_*^2/kappa on a link energy sublevel.
Those expressions fail, for example, at kappa=N^4 and H_*=C N^2 log N.
For E=kappa V(1+z), exact algebra gives

\[
z^2=\frac{2E}{\kappa+2E},\qquad
\kappa|V'(1+z)|=
\sqrt{2\kappa E}\,(1+2E/\kappa)^{3/2}.                       \tag{R2}
\]

A link carrying a fixed fraction of H_* can have force of order
sqrt(kappa H_*), much larger than the original expression. The row
constraint does not prevent this example: compensate its displacement
among the remaining links.

The correction's valid all-regime bounds are

\[
1-|z|\ge\frac{\kappa}{2(\kappa+2H_*)},
\quad
\kappa|V'|\le\sqrt{2\kappa H_*}(1+2H_*/\kappa)^{3/2},
\quad
\kappa V''\le4\kappa(1+2H_*/\kappa)^3.
\]

For the selected kappa=log(N+2), H_*=C N^2 log N, the force range is
O(N^4 log N), the derivative range O(N^6 log N), and a unit-mass local
frequency bound is O(N^3 sqrt(log N)), up to bounded lattice-degree
constants. These match the correction. The simpler original expressions
hold in this selected slow-growth regime.

Coupling an actual smooth finite-force continuation to the ideal dynamics
until first exit is valid, provided the continuation agrees throughout
the declared sublevel and has specified post-exit dynamics. The exit
probability is superexponential at volume speed. Geometry after the
counted failure is not certified by merely retaining particle labels.

## 6. Conditional records and resource scope

The proof is pointwise in each fixed supplied potential/response array
with uniform constants. Retained old records are compatible when the
conditional local preparation ceiling and complete future source and
generator interfaces are preserved. Revealing exact initial jitters
need not preserve them. Uniform feedback's cancellation does not repair
a missing conditional initial law or future source.

The resource scope is material: N^2 actual charges and links, N^2 initial
positions at precision kappa^{-1/2}, increasing force/derivative range,
thermal sources and retirement, isolation, and readout/command distribution.
There are O(N^4) fresh thermal coordinates over physical time N^2 at the
declared fixed-period interface. Their work is not part of the tangential
drive-work identity.

The corrected preparation and density-law proof is received. The growing
rare-tail bandwidth is essential to its finite-force realization; the
near-equilibrium frequency alone is not an adequate apparatus certificate.

