# Actual receiving review: metered finite cell and joint spatial error

30 October 2026. Existing Astra P1 record-geometry role. No new agent,
branch, fixture, or experimental acquisition was used. Root's input was
read and reconstructed; its original bytes were not changed.

## Exact reviewed input and decision

Input: new_science/continuation11_20261030/METERED_FINITE_CELL_AND_SPATIAL_ERROR.md

SHA256:
dc141155fe9933e9a7c2cd475ec01aa7d2f02ac251ebcd6188fd61a0d391a655

Exact local snapshot:
METERED_FINITE_CELL_AND_SPATIAL_ERROR_REVIEWED_dc141155fe99.md

**Receive the finite-cell construction, joint-error tracking receiver, and
native-marginal composition at their stated actual-operation interfaces.**
The joint spatial norm and separate large scalar cap threshold repair the
previously unattainable maximum-row error requirement. I found no
load-bearing counterexample to those claims.

There is one harmless aggregate-normalization typo in the FDT derivation,
specified below. There is also a necessary distinction between the tracking
and work precision requirements: uniformly vanishing deterministic error
suffices for tracking, while the asserted order-N² carrier-work bound needs
the earlier O(1/K_N) deterministic error rate. Root independently identified
and undertook to bind this latter clarification. The original input is
received with those explicit qualifications, not as a claim about an
uncharacterized final pointer reader.

## 1. Actual cell, reaction, and stable response

The extension identity is consistent throughout both physical intervals:
R=g_N X-U and dot U=P give dot R=g_N V-P. The reciprocal terms cancel
in the declared energy. In particular -g_N R V cancels +g_N R V,
-R P cancels +P R, and the bath terms -Omega P zeta and +Omega zeta P
cancel. Translation invariance gives sum_l partial_l U_N=0. Thus the
aggregate four-dimensional equation is exactly linear even though the
relative material remains nonlinear. Every charged displacement during
transport and bath contributes to A.

At g=0, transport sends (R,P) to (-P,R). At the stated bath point,

\[
R_{\rm out}=(R_{\rm in}+\zeta_{\rm in})/2-P_{\rm in}/\sqrt2,
\qquad
P_{\rm out}=(R_{\rm in}-\zeta_{\rm in})/\sqrt2.
\]

Composing these maps gives the displayed probe block

\[
\begin{pmatrix}-1/\sqrt2&-1/2\\0&-1/\sqrt2\end{pmatrix}.
\]

Its stability, the compact positive-response old-cell class, and finite
dimensional continuity provide a common spectral-radius margin for all
sufficiently small g and a small open design neighborhood. A resolvent
circle outside that common spectrum then gives the uniform power bound
used by the proof. No unmeasured particlewise kinetic matching beyond the
declared common-within-row supplier has been inserted.

The corrected-current identity follows directly by substituting
(I-M_g)^T k_g=l_g. The mathematical corrector is never read, subtracted
from counted physical charge, or used in the actual governor.

### FDT normalization correction

For the standardized aggregate z/sqrt(N), include every initial, fresh,
and retired Gaussian variable. The zero-force map is orthogonal. With
constant physical force, its input is sqrt(N) F. The exact energy identity
therefore gives Var_0 A_m=2 partial_F E_F A_m. This is a finite-time identity
for the actual aggregate in its stated Gaussian reference law.

For A_m as defined in the input, the subsequent asymptotic displays must be

\[
\operatorname{Var}_0 A_m=N m\|\sigma_g\|^2+O(N),\qquad
\partial_F E_F A_m=N m\mu_g+O(N).
\]

The original text omits the common factor N in both expressions. Equivalently
one can explicitly use the single-carrier normalization there. The factor
cancels, so the conclusion \|\sigma_g\|^2=2\mu_g and all subsequent equations
are unchanged. Stable endpoint covariances and the geometric sum of their
correlations with the accumulated fresh noise justify the O(N) terms.

## 2. Relative density and actual preparation

Uniform row forcing drops out of the projected relative subsystem. The
additional neutral Gaussian coordinates preserve the product relative
Gibbs invariant law, while local positional jitter has the already reviewed
exp(CN²) preparation ceiling. The previous Brascamp--Lieb norm event and
energy-mesh continuation therefore remain applicable with a constant
increase in the number of energy coordinates.

For the aggregate Gaussian assertions, the supplied initial extension and
momentum variables are the actual independent per-carrier Gaussians
(and their projected relative parts have the stated Gaussian law).
Specifying only centered relative variables would leave the aggregate
initial law unspecified. The explicit local placement U_l(0)=g_NX_l(0)-R_l(0)
is compatible with this preparation, but is a real correlated placement,
not a consequence of invariance.

The elastic proof's existing finite-force and rare-energy restrictions
remain binding. No new claim of bounded pointer range, free source
preparation, or inexpensive material response follows from adding the meter.

## 3. The two error geometries are correct

Under capped adapted forcing write the aggregate state as an unforced
Gaussian reference plus its actual forced convolution. At g=0 the forced
(V,Z) block does not feed (R,P). Uniform stability and parameter smoothness
give an O(g) summable cross-response kernel for small g. Thus the forced
aggregate R contribution is bounded pathwise by C N g a_N.

At a held time, the Gaussian part of the normalized meter error has
covariance at most

\[
\frac{C N}{g_N^2N^4}I_N=\frac{C}{NH_N}I_N,
\]

where endpoint correlations are allowed. The remaining forced envelope is
C a_N/N per row. A Gaussian norm bound and a union over polynomially many
held times give the stated

\[
\exp[CN-c\varepsilon^2N^2H_N]
\]

joint spatial tail, up to the polynomial factor. At the force-cap scale
D_N=N^{3/4}/K_N, the scalar exponent is

\[
N H_N D_N^2=N^{5/2}H_N/K_N^2.
\]

Changing the displayed fraction D_N/8 to any smaller fixed fraction,
as needed for the convolution constants, only changes c. The exponent
at the much smaller maximum-row radius C/K_N would indeed be only
N H_N/K_N². It is correctly not used as a volume-speed error contract.

These calculations require actual joint initial and future source
covariances. Independent scalar marginals alone are insufficient. Actual
final-reader errors may be appended only with their declared conditional
joint tails, gain, timing, and backaction. An unknown multiplicative
transduction gain is not removed by the kinetic corrector.

## 4. Feedback filtration, stopping, and joint tracking

For fixed but unknown positive response coefficients, alpha_y is between
two constant multiples of K_N delta_N. The explicit delay response obeys

\[
\max_y|\alpha_y g_{y,j}|
\le C K_N\delta_N\exp[-cK_N\delta_N j].
\]

Summing proves equation (10). Hence the complete observation contribution
is bounded in the maximum-over-time spatial Euclidean norm by a constant
times the corresponding input norm. This bound is deterministic and does
not need temporal independence of the observed error.

The source and fresh-thermal martingales are stopped predictably. The
separate Gaussian-reference envelope is then used as a pathwise bound;
one never conditions a martingale law on future good measurement. A fixed
small joint-norm error threshold suffices for any fixed desired tracking
tolerance. The large scalar threshold handles first cap activation.
Uniformly capped forces keep the physical comparison defined even on
failure. The original within-block and continuous-time arguments then
apply to the four-coordinate cell.

Any actual command, including a sensor or evaluator error represented
inside that command, must be measurable with respect to the complete
record at the start of the previous block and held over the declared
complete cells. Selection merely before the current block is weaker:
it would allow correlation with the previous block's fresh thermal
innovation in the physical-work identity. A finite-duration final reader
must actually supply the stipulated held-record/latency contract.

## 5. Native marginal composition is properly separated

Let the ideal controller be the causal function of the native path and
independent auxiliary initial/bath primitives used in the proof. A
likelihood ratio that compares only native marginal paths extends to
this product by the same ratio. The supplied two-sided high moment bounds
therefore transfer the ideal tracking event and any independently supplied
native path LDP.

Couple the actual pointer-driven and ideal governors on that same native
path and the same auxiliary primitives. Their relative material dynamics
also agree because row forcing is uniform. Before the first relevant cap,

\[
\Delta z_k=N\sum_{i<k}M_g^{k-1-i}d_g\,\Delta F_i,\qquad
\Delta F=-\frac{K_N}{N}(\Delta e+\eta).
\]

Consequently

\[
\max\|\Delta c\|
\le\frac{CK_N}{N^2}
       \big(\max\|\Delta e\|+\max\|\eta\|\big).
\]

The current recurrence and the summable delay kernel bound then absorb
the corrector term for large N. This argument works in the joint spatial
norm and separately in a scalar row norm for the cap. It does not require
conditioning on probe trajectories to preserve a native martingale.
Native and probe correlations are allowed in the pathwise error input.

For the displayed reference source with equal within-row friction and
translation-invariant relative interactions, summing the native velocity
equation gives an OU row aggregate. Its integrated current is a Brownian
martingale plus a bounded-response endpoint corrector. Substituting this
representation and the bounded-derivative target yields the claimed
source receiver, subject to its initial velocity and load conditions.
This is a continuous displacement interface; it does not manufacture an
exclusion jump sensor or establish a native LDP for every unknown potential.
The separate explicit continuous-row receiver is being reviewed by the
physical-mechanism role, not certified by this receipt.

Retaining actual apparatus records is permitted. Conditioning on arbitrary
future probe records is a different assertion and does not inherit the
native marginal likelihood estimate. Conditional old-record assertions
still require the stated initial ceilings, genuinely fresh probe laws,
independent auxiliary primitives, fixed-class bounds and future dynamics
conditional on that old record.

## 6. Work scope and remaining physical obligations

The retained-state work derivation is dimension-independent. The fresh
noise sum in a held block has zero correlation with its full-block-old
force, the previous block's contribution is treated with that stronger
filtration, and the surviving old-state term is bounded by the uniformly
small M_g^L. Thus the four-coordinate supplier has the same signed
force-work estimate once the actual force second moments are supplied.

For the internal meter, the stated Gaussian-plus-envelope construction
does give E eta_y² <= C/(NH_N)+C a_N²/N². Weighted Cauchy--Schwarz handles
arbitrary time correlations of those errors. H_N>=K_N keeps this stochastic
contribution below the previous 1/(NK_N) term.

Tracking and work nevertheless have different deterministic precision
requirements. An additional normalized bias beta_N contributes order
N² K_N² beta_N² to the total work bound. beta_N=o(1) suffices for path
tracking but does not guarantee order-N² work; beta_N=O(1/K_N) does.
This also applies to timestamp, evaluator and actuator-command errors
included in the held force.

Likewise native-marginal LDP transfer alone is not a transfer theorem for
the sharper second moments used in a work estimate. If the native passive
follower is started only under a general exp(CN²) ceiling, its marginal
tail bound contains that ceiling; it does not by itself imply every
coordinate's canonical 1/(NH_N) error moment. A mean-work claim for that
composition must use its actual source/meter moment assumptions or a
separate energy/moment receiver. The new metered auxiliary cell's exact
Gaussian aggregate and its work proof are not affected by this distinction.

No new numerical fixture was run for this receipt. Root's subsequently
reported finite-cell calculations are population-model checks and were not
needed to reconstruct the governing proof. Final pointer readout,
distributed held records, actual clock synchronization, force uniformity,
component range, gain precision, calibration reliability, preparation and
the full apparatus energy budget remain the explicit supplier boundary.
