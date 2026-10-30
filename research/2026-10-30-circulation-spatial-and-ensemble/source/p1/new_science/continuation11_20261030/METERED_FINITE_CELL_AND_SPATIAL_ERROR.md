# A metered finite thermal cell and the spatial error it actually needs

30 October 2026. Root's constructive receiver after the complementary role
proposed a passive displacement follower. This changes the measurement
architecture and the precision contract. Read with the main elastic-layer,
joint tracking and work notes and their binding corrections. The original
reviewed versions remain unchanged. Final pointer readers, communication
and force delivery are still physical supplier obligations.

## 1. A moving pointer is different from a leaky counter

For each actual charged carrier position X, supply a neutral displacement
pointer U through a local no-slip transformer of known ratio g_N. Its
extension is R=g_N X-U and its velocity is P. The pointer retains actual
unwrapped displacement, not merely phase modulo one revolution. The local
spring stores R²/2, its inertia stores P²/2, and the native carrier receives
the reciprocal force -g_N R. No dense spatial transformer is used.

The required small ratio, absence of slip, pointer range, compliance,
initial placement and final reading are resources. A periodic phase sensor
without a winding record does not implement this coordinate. One may use
a local belt/gear or a corresponding flux-coordinate transducer, but its
actual force/flow and noise relations must be the ones below.

## 2. Actual finite-duration metered carrier cell

Augment the existing elastic train by R,P,U per carrier. Denote the old
neutral coordinate by Z and its unknown within-row coupling by omega_y.
The actual uniform force is F_y. During the transport interval h,

\[
\begin{aligned}
 \dot X_l&=V_l,&
 \dot V_l&=-\partial_lU_N-\omega_y Z_l-g_NR_l+F_y,\\
 \dot Z_l&=\omega_y V_l,&
 \dot R_l&=g_NV_l-P_l,\qquad
 \dot P_l=R_l,\qquad \dot U_l=P_l.                         \tag{1}
\end{aligned}
\]

During the finite bath interval b, disconnect V--Z but continue all charged
and pointer motion. Introduce independent fresh unread standard Gaussians
xi_l,zeta_l and evolve

\[
\begin{aligned}
 \dot X_l&=V_l,&
 \dot V_l&=-\partial_lU_N-g_NR_l+F_y,\\
 \dot R_l&=g_NV_l-P_l,&
 \dot P_l&=R_l-\Omega\zeta_l,\qquad
 \dot\zeta_l=\Omega P_l,\qquad \dot U_l=P_l,\\
 \dot Z_l&=-\beta_y\xi_l,& \dot\xi_l&=\beta_y Z_l.           \tag{2}
\end{aligned}
\]

Retire the two bath outputs after this interval. They are not observed to
select an earlier command. Joint freshness is required across all carriers,
rows and periods. Every displacement in both intervals counts. There is no
clutch that stops U while its momentum continues moving, and no instantaneous
thermal reset. Switching these local couplings and supplying/retiring bath
coordinates remain paid operations.

At F=0 every segment conserves
U_N+sum(V²+Z²+R²+P²+xi²+zeta²)/2 and phase-space volume.
With force, its exact power input is F sum_l V_l. This supplies the genuine
force/displacement interface and includes the pointer reaction.

## 3. A stable unknown-response supplier exists

For the aggregate state z_y=sum_l(V_l,Z_l,R_l,P_l), translation invariance
cancels every relative material force. One full cell therefore has the exact
linear form

\[
 z_{k+1}=M_gz_k+Nd_gF_k+\sqrt N B_g\zeta_k,\qquad
 \Delta A_k=l_g^Tz_k+Nc_gF_k+\sqrt N o_g^T\zeta_k,            \tag{3}
\]

where zeta_k is now a two-component fresh standard Gaussian. These matrices
are obtained by the two declared finite matrix exponentials; the runnable
check gives them without fitting hidden response. Gaussian invariance gives
M_g M_g^T+B_g B_g^T=I.

An exact stable design point is h=pi/2, b=pi/(2 sqrt(2)), Omega=1. At g=0
the old (V,Z) cell is the preserved untuned supplier. The probe (R,P) block
is explicitly

\[
 M_{probe}=
 \begin{pmatrix}-1/\sqrt2&-1/2\\0&-1/\sqrt2\end{pmatrix}.    \tag{4}
\]

Its spectral radius is 1/sqrt(2). Choose omega and r_y=cos(beta_y b) in
the earlier fixed compact positive-response/stability class. Compactness
and continuity give g_*>0 and uniform constants C,r_*<1 for all
0<=g<=g_*: ||M_g^j||<=C r_*^j. There is also an open neighborhood of the
displayed h,b,Omega with the same conclusion. Exact quarter-period tuning
of a fabricated probe is not required; its actual parameters must lie in
that warranted neighborhood. Arbitrary carrierwise mismatch is not covered.

Let k_g solve (I-M_g)^T k_g=l_g and put
mu_g=c_g+k_g^Td_g, sigma_g^T=o_g^T+k_g^TB_g. Then

\[
 \Delta A_k+k_g^T\Delta z_k=N\mu_g F_k+\sqrt N\sigma_g^T\zeta_k.
                                                               \tag{5}
\]

All coefficients are uniformly bounded; mu_g stays positive by continuity
from the untuned g=0 supplier. The controller does not know k_g or mu_g.

For completeness, sigma_g^T sigma_g=2mu_g. Under zero force, include all
fresh and retired Gaussian coordinates over m complete cells. Their total
linear map is orthogonal. A constant force adds a deterministic vector d_m;
energy balance for every initial vector implies that the displacement's
linear coefficient is d_m^T times that orthogonal map, and its quadratic
force coefficient is ||d_m||²/2. Thus Var_0 A_m=2 (d/dF) E_F A_m exactly.
Uniform state stability and (5) give Var_0 A_m=m||sigma_g||²+O(1) and
(d/dF)E_F A_m=m mu_g+O(1), proving the identity. This argument is for the
free aggregate, where relative forces have canceled; it does not replace
the nonlinear relative dynamics with harmonic material dynamics.

The earlier retained-state work calculation is dimension-independent.
With full-block-old forces and L complete cells, replace its two-dimensional
state by this four-dimensional state. The old-state correlation is still
retained and suppressed by ||M_g^L||. Hence the main O(N²+NK_N) mean
carrier-force work theorem continues to hold under the received error
moments below. No extra powered cancellation actuator has been introduced.

## 4. The density proof survives the meter

The rowwise relative subsystem is autonomous because the applied force is
uniform. Its invariant density is proportional to

\[
 \exp[-U_N(u)-\tfrac12(\|v\|²+\|z\|²+\|r\|²+\|p\|²)].      \tag{6}
\]

Prepare the same local positional jitter and Gaussian velocities as before,
and independent Gaussian relative extensions and pointer momenta. Initial
pointer placement realizes U_l(0)=g_N X_l(0)-R_l(0); this correlated placement
is an actual initializer, not an inferred free copying operation. The warm
density ceiling exp(CN²) and the Brascamp--Lieb norm bound are unchanged in
order. The added Gaussian energy coordinates preserve the time-mesh energy
bound. Thus the complete charged auxiliary density is still exponentially
equivalent to the uniform background at speed N². Neutral pointer mass and
its apparatus occupy real space but are not relabeled as native charge.

## 5. Internal pointer accuracy has joint spatial geometry

At a held timestamp, use actual changes of U, including its initial reading:

\[
 \widehat A_y={1\over g_N}\sum_l[U_{y,l}(s)-U_{y,l}(0)]
 =A_y-{1\over g_N}\sum_l[R_{y,l}(s)-R_{y,l}(0)].             \tag{7}
\]

Set g_N²=H_N/N², H_N->infinity and H_N=o(N). Under the unforced reference,
the aggregate R_y has Gaussian covariance N and different rows have joint
product sources. Under any capped force, stable linear response contributes
at most C N g_N a_N to that aggregate: its response from the forced (V,Z)
block to the (R,P) block is O(g_N), uniformly in the compact class. Therefore
the normalized error eta_y=(widehat A_y-A_y)/N² has a deterministic envelope
C a_N/N plus a Gaussian vector with covariance operator at most C/(NH_N).
Initial and later endpoint noises need not be independent; Cauchy--Schwarz
on their marginal Gaussian exponential moments supplies this bound.

On polynomially many held timestamps, for every fixed epsilon>0,

\[
 \Pr\{\max_m\|\eta_m\|_2/\sqrt N>\epsilon\}
 \le\operatorname{poly}(N)\exp[CN-c\epsilon²N²H_N],           \tag{8}
\]

after the vanishing forced envelope. Extra independent bounded-variance
Gaussian or uniformly sub-Gaussian positional reader errors have the same
scaling if their actual joint covariance and conditional supplier justify
it. This last statement is a reader contract, not a claim that looking at
the pointer has no physical backaction. Correlated common-mode reader noise
can destroy (8).

With D_N=N a_N/K_N and a_N=N^(-1/4), scalar tails also give

\[
 \Pr\{\max_{y,m}|\eta_{y,m}|>D_N/8\}
 \le\operatorname{poly}(N)
                  \exp[-c N^{5/2}H_N/K_N²].                 \tag{9}
\]

For H_N=log(N+2), K_N=log log(N+e^e), this is super-volume. In contrast,
requiring every error to be <=C/K_N with super-volume failure would ask for
the insufficient row exponent NH_N/K_N². The original stronger uniform
readout contract should not be silently asserted for these physical probes.

## 6. Receiving tracking theorem with the attainable error

Use the actual full-block-old capped governor. Replace the old uniform
observation contract by (8), (9), together with deterministic evaluation,
timestamp and force-command errors tending uniformly to zero and with their
own warranted whole-protocol failure. The readout errors may be correlated
with native paths and with earlier commands; the proof never conditions
noise increments on future successful measurement.

Before first cap/fault the same exact recurrence applies. Its response to
eta is the diagonal convolution alpha_y g_{y,j} eta_{y,m-1-j}. The known
uniform positive-response class gives

\[
 \sum_{j\ge0}\max_y|\alpha_y g_{y,j}|\le C.                 \tag{10}
\]

Hence its entire spatial L2 response is bounded by C max_m||eta_m||_2.
The corrector's large Gaussian event is unchanged. The stopped target and
thermal martingales retain the original joint directional-net proof.
For any fixed requested error, first choose a sufficiently small fixed
threshold in (8); its failure is super-volume. This proves the same full-
time spatial tracking assertion. No vanishing per-row deterministic radius
with an unattainable probability is inserted.

For first cap, apply the scalar convolution bound at the large threshold
D_N, use (9), and use the already proved scalar native/thermal tail and
corrector event. The forcing remains globally capped even on a reader
failure. For work, each coordinate has E eta_y²<=C/(NH_N)+C a_N²/N².
The weighted Cauchy--Schwarz estimate
(sum_j w_j eta_j)² <= (sum_j|w_j|) sum_j|w_j| eta_j²
works even with temporal dependence. It adds at most C/(NH_N) to the
tracking second moment. For H_N>=K_N it does not exceed the previous
C/(NK_N) fluctuation term. Deterministic readout bias of order 1/K_N still
retains the earlier possible order-N² work contribution.

Equations (8)--(10) are the central precision change: the instrument is
judged at the joint spatial scale of the intended law, with a separate
large-deviation check for the actuator's cap. They also receive a native
passive follower's endpoint errors, subject to its actual source-law scope.

## 7. Composition with a perturbed native measurement architecture

The original main theorem leaves the native microscopic path unchanged.
A passive native follower instead changes that path law. The complementary
native-marginal likelihood comparison has its own scope: canonical
underdamped native dynamics, independent Gaussian probe initialization,
and a supplied passive follower. When its positive and negative density
moments satisfy
log E Z^(p_N)=o(p_NN²) and log E Z^(1-p_N)=o(p_NN²), p_N->infinity,
the native speed-N² LDP and super-volume events transfer. It does not
preserve every microscopic apparatus record or a CLT.

A careful receiving route avoids revealing probe states to a source
martingale proof that only conditions on native histories. Analyze an ideal
current governor as a measurable function of the native path and independent
auxiliary primitives. The native-marginal likelihood comparison extends
unchanged to those independent primitives. It therefore transfers the
ideal governor's super-volume tracking event. Then compare the real
pointer-driven governor on the same native path and auxiliary primitives.
Its extra observation error is controlled pathwise by (10).

In this comparison the difference of analytic current correctors is also
controlled: stable block states give
max||Delta c|| <= C K_N/N² (max||Delta e||+max||eta||)
before first cap. Since K_N/N²->0, this term is absorbed in the deterministic
convolution estimate. Use the large scalar threshold separately for first
cap. Thus native/probe correlations do not require conditional independent
readout noise, and no joint native-plus-probe likelihood is falsely claimed.

This composition still needs an actual native source receiver. One concrete
continuous family has fixed row labels, equal within-row friction and an
interaction invariant under independent translations of each row. Rowwise
internal forces then cancel; the native aggregate velocity is an OU process,
so its integrated current has the same bounded-memory martingale form used
by the tracking proof. Interactions among relative coordinates may be
unknown and nonharmonic. A native density/current LDP is a separate premise;
free row-confined Brownian carriers provide a simple example. Arbitrary
two-dimensional interactions, changing row identities, or all hidden jump
systems do not automatically supply this source. The earlier exclusion
example retains its declared readout interface instead.

The useful gain is a passive internal displacement memory and a proved
joint-error receiver. A full experimental instrument still needs the
macroscopic pointer reader, local message integrity, actual range and
gear-slip control, and the complete energy budget. No order-N² total
apparatus-work claim is made. The nonlinear spatial principle is thereby
given a stronger metering architecture without erasing the remaining
physical boundaries or the independent native-isolation result.
