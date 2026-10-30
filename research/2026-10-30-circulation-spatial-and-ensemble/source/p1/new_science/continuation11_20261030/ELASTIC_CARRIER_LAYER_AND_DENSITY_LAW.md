# Elastic carriers: density concentration without dilution

30 October 2026. Root's central mechanical construction. This is a theoretical
apparatus with specified operations, not a certificate for an uncharacterized
belt. The spatial tracking and work notes are separate parts of the result.

## 1. Actual architecture

Add N isolated horizontal circular trains to an N by N native material.
Each train has N unit charges on a circle of circumference N. Both reference
and deployment contain them. Their total empirical mass is **one**, and the
complete measured density is native density plus this physical density.

Write X_{y,l}=l+C_y+u_{y,l}, sum_l u_{y,l}=0, X_{y,l+N}=X_{y,l}+N.
The actual neighbor gaps are g_{y,l}=1+u_{y,l+1}-u_{y,l}. Supply

\[
 U_N=\kappa_N\sum_{y,l}V(g_{y,l}),\quad \kappa_N\to\infty,
 \qquad V(1+z)=\frac{z^2}{2(1-z^2)},\quad |z|<1.                 \tag{1}
\]

Here V''(1+z)=(1+3z^2)/(1-z^2)^3>=1. Gaps remain in (0,2) at finite
energy, so these are spatially local links, not merely adjacent labels.
An unrestricted harmonic chain would not supply that geometric conclusion.
More generally, unknown homogeneous row potentials are allowed with
V(1)=V'(1)=0, V''>=1, endpoint divergence, and a uniform upper bound on V''
near one. Row choices may differ. The ideal singular link and its finite
force approximation are distinguished in Section 7.

## 2. Finite-duration carrier response

Use the preserved untuned partial-thermal cell, now with N carriers per row.
During transport of duration h,

\[
 \dot X_l=V_l,\quad\dot V_l=-\partial_lU_N-g_yY_l+F_y,
 \quad\dot Y_l=g_yV_l.                                      \tag{2}
\]

During a bath interval b, disconnect only V--Y; charges continue moving under
their relative forces and F_y. Rotate each Y with a fresh unread standard
Gaussian through angle psi_y; retire the other output. Every displacement in
both intervals counts. Forces are selected before fresh sources are exposed.

Use common h,b so p=h+b is known. Actual fixed unknown g_y,r_y=cos(psi_y)
are common within each row and satisfy the preserved compact positive-response
bounds: 0<theta_-<=g_yh<=theta_+<pi, g bounded above/below, |r_y|<=r_*<1.
Arbitrary particlewise mismatch is not covered.

Let A_y=sum_l[X_{y,l}(s)-X_{y,l}(0)], z_y=(sum_lV_l,sum_lY_l).
Translation invariance cancels every relative force. The earlier exact cell
and its proof therefore give

\[
 z_{y,k+1}=M_yz_{y,k}+Nd_yF_{y,k}+\sqrt N n_y\zeta_{y,k},
\quad \Delta A_{y,k}+k_y^T\Delta z_{y,k}
 =N\mu_y F_{y,k}+\sqrt N\sigma_y\zeta_{y,k},                  \tag{3}
\]

with actual fresh standard Gaussian zeta, sigma_y^2=2mu_y,
0<mu_-<=mu_y<=mu_+, bounded k_y, and ||M_y^j||<=C r_0^j, r_0<1.
Explicitly mu_y=(1-r_y)[2/g_y+b cot(g_yh/2)]^2/[2(1+r_y)].
The controller reads A_y and never learns or implements the analytic k_y.
The true work is sum_y integral F_y dA_y, not corrected-current work.

## 3. Autonomous relative law

Project (2) onto the rowwise mean-zero spaces. F_y disappears. The scalar
Gaussian source in (3) is independent of the mean-zero source components.
Each conservative segment preserves relative energy and volume. Partial
thermal rotation preserves its Gaussian marginal. Thus all phases preserve

\[
 \Pi_N(du\,dv\,dy)\propto
 e^{-U_N(u)-\|v\|^2/2-\|y\|^2/2}\,du\,dv\,dy.              \tag{4}
\]

Uniform feedback does not enter this relative motion, even when its records
are correlated with relative coordinates. This is not a claim that the
controlled collective state is Gaussian.

## 4. Local preparation suffices; global Gibbs preparation is not assumed

At each nominal location l prepare an independent unread eta_{y,l} uniform
on [-w_N,w_N], w_N=c_0/sqrt(kappa_N), with fixed sufficiently small c_0.
Set X_{y,l}(0)=l+eta_{y,l}; prepare independent standard Gaussian V_l,Y_l.
These are explicit local positioning and thermal initial-law premises.

For u_y=eta_y-mean eta_y, its hyperplane density is at most
sqrt(N)(2w_N)^(1-N): orthogonal projection integrates over an interval of
length at most 2w_N sqrt(N). Initial gaps are near one, and U_y<=C N.
With L_N the cycle Laplacian, U_y>=kappa_N u_y^T L_N u_y/2 and

\[
 Z_{y,N}\le (2\pi/\kappa_N)^{(N-1)/2}/N,                    \tag{5}
\]

because det'(L_N)=N^2. The powers of kappa_N cancel against the preparation
density. Consequently the complete initial relative law satisfies

\[
 d\nu_N/d\Pi_N\le e^{C N^2}.                               \tag{6}
\]

Every relative transition preserves this ceiling. No mixing estimate is
needed. A conditional theorem with old records requires the same conditional
freshness; conditioning on a record of every exact eta would not satisfy (6).
Initialization has not been bootstrapped from invariance.

This costs N^2 placements at spatial precision kappa_N^(-1/2) and N^2
velocity/neutral preparations. In a harmonic comparison, changing fixed
stiffness to kappa_N raises equilibrium free energy by order N^2 log kappa_N.
The extra relative entropy in (6) is at most C N^2. These statements do not
supply an uncharged finite-time preparation protocol.

## 5. Joint volume-speed concentration of the entire density path

Define rho_aux=N^(-2)sum_{y,l}delta_(X_{y,l}/N mod1,y/N). Compare each
bead with the equally spaced row l+C_y. Shifted grid quadrature and
Cauchy--Schwarz give the deterministic bounded-Lipschitz estimate

\[
 d_{BL}(\rho_N^{aux},dxdy)\le C/N+N^{-3}\sum|u_{y,l}|
 \le C/N+\|u\|_2/N^2.                                     \tag{7}
\]

Cyclic symmetry implies E_Pi u=0. The Hessian is at least kappa_N times the
block cycle Laplacian. Brascamp--Lieb applied to every linear tilt and then
integrated twice proves

\[
 E_{\Pi_N}e^{v\cdot u}\le e^{v^TC_Nv/2},\qquad
 C_N=\kappa_N^{-1}\operatorname{diag}(L_N^+,\ldots,L_N^+).
                                                               \tag{8}
\]

The convex bounded-gap domain follows by convex barrier approximation.
Using an independent standard Gaussian G to represent exp(eta||u||^2),

\[
 E_{\Pi_N}e^{\eta\|u\|^2}\le\det(I-2\eta C_N)^{-1/2}.       \tag{9}
\]

Take eta=c kappa_N/N^2 with sufficiently small c. The eigenvalues of L_N
are 4 sin^2(pi j/N). Per row the log determinant in (9) is O(1), because
sum_{j=1}^{N-1}[4sin^2(pi j/N)]^(-1)=O(N^2). There are N rows. Equations
(6)--(9), at every deterministic physical time, yield

\[
 P\{d_{BL}(\rho_N^{aux},1)>\epsilon\}
 \le\exp[C_1N^2+C_2N-c\epsilon^2\kappa_NN^2].                \tag{10}
\]

This is a joint estimate. It is superexponential at speed N^2 as
kappa_N->infinity; a union of row-speed estimates would not establish it.

For the full time path, the invariant law has
E exp(alpha H_rel)<=exp(C_alpha N^2), alpha in (0,1). The position part
uses Z((1-alpha)U)<=(1-alpha)^(-d) Z(U), by convex dilation about the
minimizer; Gaussian velocity/neutral parts are explicit. Ceiling (6) changes
only the volume-order constant. Within a cell, relative energy plus the
fresh source energy is conserved. A union over O(N^2) cells gives

\[
 P\{\sup_{s\le N^2T}H_{rel}(s)>C N^2\log N\}
 \le\exp[-cN^2\log N+C' N^2+O(\log N)].                     \tag{11}
\]

Off this event ||v||<=C N sqrt(log N). During any bounded physical interval,
||u(s)-u(s_j)||/N^2<=C sqrt(log N)/N. Apply (10) at O(N^2) bounded-spaced
physical times. Therefore

\[
 \boxed{\limsup_N N^{-2}\log P\{\sup_{t\le T}
 d_{BL}(\rho_N^{aux}(N^2t),1)>\epsilon\}=-\infty.}           \tag{12}
\]

Fixed stiffness does not give this rare-event conclusion.

## 6. The nonconstant current is also controlled

The actual auxiliary current is

\[
 \langle Y_N(t),f\rangle=N^{-3}\sum_{y,l}\int_0^{N^2t}
 f(X_{y,l}(s)/N,y/N)\,dX_{y,l}(s).                          \tag{13}
\]

Its horizontal row mean is a_y=A_y/N^2. For f of zero horizontal mean,
choose its periodic x-primitive psi. The exact chain rule gives

\[
 \langle Y_N(t),f\rangle
 =\langle\rho_N^{aux}(t)-\rho_N^{aux}(0),\psi\rangle.          \tag{14}
\]

Equation (12) thus makes Y_N-a_N(y,t)e_x superexponentially negligible in
a negative Sobolev current geometry, for example H^(-s)(T^2), s>3. Unit
H^s tests and their horizontal primitives have bounded first derivatives.
The row-atom/step-field interpolation error is O(1/N) times the appropriate
norm of a_N; the joint tracking proof supplies its exponential tightness.
All these quantities use real positions, not the analytic corrector in (3).

## 7. Actual response and force limits

The stiffness grows. Near the minimum, relative frequency is order
sqrt(kappa_N) for unit masses. This bandwidth and the precision in Section 4
are paid resources. The ideal link (1) also has unbounded force at its
finite-extension endpoints. It is not a fixed-band material claim.

For a finite-force theoretical realization, match (1) on H_rel<=H_*=C N^2
log N and smoothly continue it outside. On that region each endpoint
clearance is at least c kappa_N/H_*, and |link force|<=C H_*^2/kappa_N.
Couple the actual continuation to the ideal dynamics until first exit.
Equation (11) bounds its probability at the required volume speed. The
continuation needs the stated, polynomially growing force range and the
corresponding growing derivative/response bound. A spring characterized
only near its minimum is not a supplier. Geometric links are bounded on the
coupled good histories; behavior after the counted failure is not declared
local by relabeling it.

The fresh sources, uniform tangential force, common within-row parameters,
finite switching and native isolation remain essential. Thermal preparation,
switching and readout work are not included in the carrier force work.

## Primary and preserved sources

The actual response uses round10 `UNTUNED_PARTIAL_THERMAL_CARRIER.md`
with its binding correction. No rare-arming or CLT conclusion is imported.
The established concentration inequality is given in Carlen,
Cordero-Erausquin and Lieb, https://arxiv.org/pdf/1106.0709, Eq. (1.3).
Elastic chains and fluctuation suppression have direct predecessors; see
Ikeda, https://arxiv.org/pdf/2309.03155, for a different noise-driven
ordering mechanism. The candidate addition is their physical composition
into spatial current-law control with a preserved bulk path law, not a new
basic belt, spring, thermostat or concentration inequality.
