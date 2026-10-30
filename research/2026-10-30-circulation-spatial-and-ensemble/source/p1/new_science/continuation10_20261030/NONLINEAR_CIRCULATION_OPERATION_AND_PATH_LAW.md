# A physical operation on circulation histories which preserves the bulk density law

30 October 2026. Central construction developed by Astra P1 root. This is a
theoretical apparatus and path-law theorem, not a manufactured device or a
priority certificate. The existing complementary roles supplied independent
carrier mechanisms, the delayed tracking proof, and strong ordinary feedback
comparators. Their inputs and reviews are preserved separately.

## 1. Consequence and physical task

An interacting conductor can have its macroscopic circulation history changed
by real added carrier motion while its entire macroscopic density history,
including rare density histories, remains unchanged. The operation need not
learn the native generator. It can implement a prescribed nonlinear function
of accumulated circulation, as well as a linear current projection.

The measured object is a composite conductor: a native lane and an isolated
auxiliary lane on each of a fixed number q of circular circuits of length N.
Both lanes and all their charges are present in the zero-drive reference and
in controlled deployment. Their total charge density and total current are
the physical observables. The native branch current itself is unchanged.
The auxiliary lane supplies additional flow; no current is renamed.

The scale separation is

\[
1\ll R_N\ll N,\qquad T_{\rm phys}=N^2T.                 \tag{1}
\]

R_N auxiliary carriers have vanishing empirical mass R_N/N. Repeated actual
winding nevertheless lets them transport order N^2 charge-distance during
the observation interval. This distinction between conserved mass and
accumulated transport is the mechanism. Feedback is ordinary current-error
feedback, used here through a different physical port.

The operation is active and directional: the sensor reads the native current,
and the drive acts on auxiliary carriers. A passive transformer, a constraint
on native currents, and this operation have different response, noise and
work laws.

## 2. Actual native interface

Let B(s)=(B_1(s),...,B_q(s)) count total signed native displacement in physical
time s. Each coordinate is a sum over all native bond counts, not merely one
cut count. Assume in the actual deployment filtration

\[
B(s)=\int_0^s b_u\,du+M(s),\qquad |b_u|\le C_0,         \tag{2}
\]

with jump sizes bounded by a constant and total conditional jump intensity
at most C_1N. The vector dimension q is fixed. Conditional exponential
martingale bounds follow from this actual bounded-jump interface. The native
state may contain persistent hidden variables and memory. No finite predictive
representation, mixing bound or known rate matrix is needed. Sensing and
auxiliary forcing must leave this native path law unchanged. Uncontrolled
measurement backaction is not this interface.

A concrete supplier is homogeneous exclusion on each ring: an occupied site
hops to an empty nearest neighbour at unknown fixed rate D_a in a warranted
interval [D_-,D_+]. The total unforced drift is identically zero, because it
is D_a times sum_i(eta_i-eta_(i+1)). A bounded field F_a(s,x)/N multiplying
right/left rates by exp(plus or minus F_a/(2N)) adds only bounded total drift.
The common unknown rate may vary causally if it still multiplies the complete
ring generator at each instant; this supplies (2), but not automatically the
exclusion action in Section 8. Arbitrary heterogeneous reciprocal bond rates
do not imply (2). Their total instantaneous drift can be O(N). The ordinary
stationary-reversible comparator supplies a different, broader equilibrium
class with a different proof; it is not substituted for (2) here.

## 3. The operation to be executed

Choose a fixed map

\[
\phi:[0,T]\times\mathbb R^q\to\mathbb R^q,
\qquad \phi(0,0)=0,                                    \tag{3}
\]

C^1 in time and C^2 in its vector argument, with uniformly bounded first and
second derivatives. Bounds may instead hold on a warranted exponentially
tight domain if its failure is accounted for.

The actual program includes an evaluator for this particular phi with finite
latency and a certified counter error. An arbitrary abstract smooth function
is not thereby granted as a computable operation. Rational linear maps,
phi(h)=h/(1+h^2), and phi(h)=h^2/(1+h^2) in one coordinate are explicit finite
arithmetic examples with bounded derivatives. Evaluation to O(1/N) absolute
accuracy uses O(log N) precision bits and polynomial-in-log-N arithmetic;
the scaled target error is O(N). Electronics and reliability remain paid.

Write h_N(t)=B(N^2t)/N^2. At one held timestamp s define the desired real
auxiliary displacement

\[
Z_N(s)=N^2[\phi(s/N^2,B(s)/N^2)-B(s)/N^2].             \tag{4}
\]

If A_a(s) is actual auxiliary displacement, servo a measures

\[
E_a(s)=A_a(s)-Z_{N,a}(s).                              \tag{5}
\]

It applies an inward force according to a delayed sign of E_a, allowing a
small deadband. Each servo may have a different unknown mobility, particle
number and noise strength. No matching or common-noise assumption is used.
For the two-circuit arithmetic common-current projection,

\[
\phi(h)=((h_1+h_2)/2,(h_1+h_2)/2),                    \tag{6}
\]

the errors are E_1=A_1+(B_1-B_2)/2 and E_2=A_2-(B_1-B_2)/2. This needs
separate native and auxiliary counts, an actual sensing requirement.

## 4. Two real carrier suppliers

### 4.1 Bounded-rate independent carriers

One implementation places each of R_N charges on its own N-cell track. A
supplied noninteracting shared lane is another option. At carrier l's current
location the actual two intensities are

\[
c_l(s,\mathcal H_s)e^{F_a(s)/2},\quad
c_l(s,\mathcal H_s)e^{-F_a(s)/2},\quad
0<c_-\le c_l\le c_+.                                  \tag{7}
\]

The same prefactor multiplies both outgoing directions. These are conditional
intensities including hidden history, not conclusions from equilibrium
weights. Unknown fixed track clocks are a simple supplier. Generic reciprocal
edge conductances need not satisfy (7).

With F_a=-a_N sign(delayed E_a), inward drift is between
2c_-R_N sinh(a_N/2) and 2c_+R_N sinh(a_N/2), with activity O(R_N). No clock
estimate is needed. Separate tracks cost O(NR_N) physical cells. A generic
shared exclusion lane fails: one clustered block has only two active edges
and loses capacity proportional to R_N.

### 4.2 Finite-duration interacting mechanical carriers

`record_geometry/FINITE_DURATION_INTERACTING_CARRIER_PORT.md` constructs a
force/displacement interface retaining unknown translation-invariant relative
interactions U. Charged positions X_l, velocities V_l and neutral coordinates
Y_l obey, during transport for h=pi/(2g),

\[
\dot X_l=V_l,\quad \dot V_l=-\partial_lU-gY_l+F,
\quad \dot Y_l=gV_l.                                  \tag{8}
\]

During a finite bath interval b, only the V--Y coupling is disconnected;
particles continue moving under -partial U+F. Each Y is quarter-rotated with
a fresh unread standard Gaussian coordinate at frequency pi/(2b). All motion
is counted. Summed relative forces cancel because sum_l partial_l U=0.
With P=sum_l V_l, Y_k=sum_l Y_l at a period start, p=pi/(2g)+b and beta=2/g+b,

\[
P_{k+1}=-Y_k+R_NF_k(1/g+b),\qquad
\Delta A_k+\Delta P_k/g=-\beta Y_k+R_N\beta^2F_k/2.     \tag{9}
\]

Y_k is fresh N(0,R_N) conditional on information selecting F_k and must not
be exposed before that choice. Initial momentum needs a warranted tail,
supplied for example by Gaussian velocity preparation. The momentum
correction is analytic; the detector still measures A. Its endpoints and
within-period motion have explicit Gaussian maximum bounds. Unknown relative
interactions need not be learned or mixed.

This is a finite-response mechanical supplier, not an inferred white-noise
force. It needs isolation, the displayed switching, O(R_NN^2) fresh neutral
preparations and retirements, synchronized operations, force generation and
sensing. Bounded frequency is not a hard amplitude bound: Gaussians have
unbounded support. Approximate pulses and local sensing of the interacting
particles need the actual error and relative-energy contracts in the supplier
and counter notes. A center-of-mass identity alone does not bound every
unobserved relative velocity.

## 5. Causal tracking of the nonlinear target

Set K_N=R_Na_N and require

\[
a_N\to0,\quad K_N\to\infty,\quad R_N/N\to0,
\quad K_Nd_N=o(N^2),\quad d_N=o(N^2).                  \tag{10}
\]

d_N bounds every used timestamp's age, including sampling, communication,
evaluation, force ramp and startup. R_N=N^(2/3), a_N=N^(-1/3) allows
d_N=O(N log N). No instantaneous global transform is used. The whole-horizon
count/evaluation error is at most eta_N=o(N^2), outside probability p_N with

\[
\limsup_NN^{-1}\log p_N=-\infty.                      \tag{11}
\]

`record_geometry/LOCAL_COUNTER_COMMUNICATION_AND_SOURCE_SCOPE.md` gives a
local finite-bandwidth implementation contract. All coordinates of (4) refer
to a common timestamp within a paid skew bound. Summing local readings taken
at O(N)-different times is not warranted by a bound on simultaneous total
drift. Fixed calibration or detector failure probability does not give (11).
One may instead state a conditional theorem after establishing the interface.

**Target lemma.** Z_N has bounded jumps, drift O(1), and conditional jump
intensity O(N), uniformly over allowed native hidden dynamics.

**Proof.** A jump delta B has size O(1). Taylor expansion gives

\[
\Delta Z_N=(D_h\phi-I)\Delta B+O(|\Delta B|^2/N^2).    \tag{12}
\]

The first term has bounded jumps and drift (D_h phi-I)b. Summing the remainder
at intensity O(N) gives drift O(1/N). Time dependence contributes bounded
partial_t phi; target N^2 cancels the physical/macroscopic time conversion.
Compensation of the complete jumps yields the noise bound. QED.

Apply `record_geometry/DELAYED_CARRIER_QUEUE_BOUND.md` to A_a-Z_a, or its
momentum-corrected version for (9). The target lemma supplies the bounded
disturbance. Either carrier port supplies inward drift of order K_N and
total noise of order N. Its proof bounds delayed-window martingale excursions
and then upcrossings under inward drift. It stops at failures, without
conditioning a martingale on a future good record. For every epsilon>0,

\[
\limsup_N\frac1N\log\Pr\{\max_a\sup_{s\le N^2T}
|E_a(s)|>\epsilon N^2\}=-\infty.                      \tag{13}
\]

An initially unarmed controller can start at an o(N^2) trigger if startup is
included in d_N and its overshoot is superexponentially o(N^2). A version
with vanishing mean carrier work is in the companion root force-limit note.

## 6. Conservation supplies the complete spatial path

For a discrete native lane use

\[
\rho_N(t)=N^{-1}\sum_i\eta_i(N^2t)\delta_{i/N},\qquad
W_N(t,x)=J_i(N^2t)/N\quad (i/N<x<(i+1)/N).             \tag{14}
\]

This current has mean B(N^2t)/N^2 and obeys exact distributional continuity:

\[
\partial_xW_N(t)=-(\rho_N(t)-\rho_N(0)).               \tag{15}
\]

Use the same embedding for auxiliary lattice carriers. For mechanical ones,

\[
\langle Y_N(t),f\rangle=N^{-2}\sum_l\int_0^{N^2t}
f(X_l(s)/N)\,dX_l(s).                                 \tag{16}
\]

Its mean is A(N^2t)/N^2 and it satisfies (15) with auxiliary density nu_N.
Uniformly at every time,

\[
\|\nu_N(t)\|_{\rm TV}=R_N/N.                          \tag{17}
\]

For mean-zero f choose its periodic primitive psi. Conservation gives

\[
|\langle Y_N(t)-\overline Y_N(t)dx,f\rangle|
=|\langle\nu_N(t)-\nu_N(0),\psi\rangle|
\le2(R_N/N)\|\psi\|_\infty.                           \tag{18}
\]

Thus the nonconstant part of the entire accumulated auxiliary current tends
to zero uniformly in time in H^(-s), s>3/2, at deterministic rate C_sR_N/N.
Nonuniform auxiliary positions and arbitrarily many windings are allowed.
No equilibrium or independence is needed for (17)--(18).

Put rho^tot=rho+nu, W^tot=W+Y and define

\[
\mathcal T_\phi(\rho,W)(t)=
(\rho(t),W(t)+[\phi(t,\overline W(t))-\overline W(t)]dx).
                                                               \tag{19}
\]

Use the joint Skorokhod path space with negative-Sobolev spatial coordinates.
Uniform-in-time estimates dominate its metric. On bounded sets the weak
measure topology agrees with this use. The mean functional and the map (19)
are continuous for the joint Skorokhod topology.

**Whole-path operation theorem.** Under the actual interfaces above,
(rho^tot_N,W^tot_N) is exponentially equivalent at speed N to
T_phi(rho_N,W_N). More strongly, the auxiliary record is retained:

\[
(\rho_N^{\rm tot},W_N^{\rm tot},Y_N)\simeq_{\exp,N}
(\rho_N,W_N+[\phi(t,h_N)-h_N]dx,[\phi(t,h_N)-h_N]dx).
                                                               \tag{20}
\]

Exponential equivalence means every fixed positive path-metric discrepancy
has probability whose log divided by N tends to minus infinity.

**Proof.** The density difference is (17), the centered current difference is
(18), and the constant current difference is E_a(N^2t)/N^2 from (13).
All bounds hold simultaneously for the whole horizon. QED.

The customary atomic-edge current and (14) give the same exclusion LDP.
In one dimension conservation bounds W_N minus its mean by a fixed constant
when native empirical mass is at most one. Replacing edge samples by edge
averages changes a test pairing by at most
C_s(1+sup_t|h_N(t)|)/N. The bounded drift/activity interface makes an excursion
|h_N|>cN superexponentially rare at speed N. Hence the embeddings are
exponentially equivalent. This also justifies the usual weak-current and
negative-Sobolev formulations on the exponentially tight sets used here.

## 7. Non-Gaussian law and retained records

If the actual native pair has a good speed-N LDP with rate I in this compatible
path geometry, contraction and (20) give

\[
I_\phi(\rho,W^{\rm out})=
\inf\{I(\rho,W):\mathcal T_\phi(\rho,W)=(\rho,W^{\rm out})\}.
                                                               \tag{21}
\]

This is a pushforward supplied by a physical operation, not restriction of
the native action to a constraint surface or a Gaussian approximation to an
interacting law. No native LDP follows from (2) alone; (20) precedes that input.
Minimizing (21) over output current gives exactly the native density-path
rate, since every native current has an output and density is unchanged.

The joint rate with Y retained comes from the full map (20). It does not
discard the background component, because

\[
W^{\rm native}=W^{\rm out}-Y.                         \tag{22}
\]

Thus no controller information or dissipation is erased by the displayed
marginal contraction. Old records can be unchanged coordinates if the actual
conditional interfaces and joint native law are warranted. Uniform tracking
bounds survive mixtures; one conditional exclusion action is not the action
of an arbitrary hidden-rate mixture.

The theorem does not identify fine detector logs with a projected hypothetical
apparatus in total variation. It concerns the macroscopic physical paths
shown. Rare arming provides a different coupling of controlled and zero-drive
finite-N records on histories where their actual operations coincide.

## 8. Explicit nonlinear exclusion action for the common-current operation

For two independent homogeneous exclusion backgrounds with fixed unknown D_a
and bounded smooth weak fields F_a/N, the native dynamic action is

\[
I(\rho,j)=I_{\rm init}(\rho(0))+\frac14\sum_{a=1}^2
\int_0^Tdt\int_0^1dx\,
\frac{[j_a+D_a\partial_x\rho_a-D_a\chi(\rho_a)F_a]^2}
{D_a\chi(\rho_a)},\quad \chi(r)=r(1-r),               \tag{23}
\]

on continuity, using right/left rates D_a exp(plus or minus F_a/(2N)).
For a deterministic associated profile I_init is zero on that profile and
infinite elsewhere. The literal calculation below assumes densities bounded
away from zero and one; degenerate densities use the standard lower
semicontinuous extension. Bertini et al., `math/0512394`, prove the unforced
empirical-current LDP; their rate-1/2 convention is changed by time scaling.
A smooth weak field supplies the displayed term by its actual jump likelihood
tilt. This is not the different, unfinished round9 particle-field apparatus.

For (6), output currents have equal spatial means. Their native preimages are
(j_1+u(t),j_2-u(t)). Define

\[
a_a=j_a+D_a\partial_x\rho_a-D_a\chi(\rho_a)F_a,
\quad r_a=\int_0^1\frac{dx}{D_a\chi(\rho_a)},\quad
\ell_a=\int_0^1\frac{a_a\,dx}{D_a\chi(\rho_a)}.        \tag{24}
\]

The minimizing circulation is u_*=-(ell_1-ell_2)/(r_1+r_2), giving

\[
\boxed{I_{\rm out}=I_{\rm init}+\frac14\int_0^Tdt
\left[\sum_a\int_0^1\frac{a_a^2}{D_a\chi(\rho_a)}dx
-\frac{(\ell_1-\ell_2)^2}{r_1+r_2}\right].}            \tag{25}
\]

It is infinite if continuity, initial or common-current conditions fail.
The subtracted term comes from real additional flow and contraction over
untouched native histories. Passive native-current constraint instead retains
a restricted native action and generally changes the nonlinear density law.

For always-active linear control at a homogeneous profile, force response is
Q M and leading current noise is Q M Q. Here M is native mobility and Q the
arithmetic projection. Input forces still act on the background. A passive
two-sided transformer also transforms the force port. Armed control has a
further singular distinction: its ordinary central-limit noise stays native
even though its macroscopic rate is (25). The companion force-limit theorem
keeps these limits separate.

## 9. Resources and boundaries

The apparatus acquires native and auxiliary counts with synchronized
timestamps, stores counters and the target, evaluates phi, communicates and
drives real carriers. A local O(N log N)-delay network suffices; there is no
dense instantaneous transformer. The local counter note charges precision,
preparation, timing, communication, and the mechanical readout's energy
envelope rather than inferring these from a center-of-mass calculation.

The per-step force cap a_N tends to zero, but whole-loop affinity N a_N
generally grows. Fixed total-loop voltage gives capacity O(R_N/N) and is not
a supplier. Distributed drive or growing total-loop range is essential.
Sustained O(1) mean auxiliary flow over N^2 time costs order N^2/R_N at fixed
per-carrier mobility. Rare arming can make mean carrier-drive work vanish
unforced; sensors, clocks and thermal preparations still run. Neither is a
total-energy claim. Actual momentum/switching terms remain in mechanical work.

The earlier passive receiver's outside-band measurement qualification remains
intact. This theorem uses actual all-time counts and conditional noise bounds.
A detector characterized only in a finite frequency band does not supply
those counts, timestamps or the failure probability (11).

## 10. Predecessors and candidate addition

Current-error feedback is a direct predecessor: Brandes, PRL 105, 060602
(2010), https://arxiv.org/pdf/1005.0018. Sampled experimental control is Wagner
et al., Nature Nanotechnology 12, 218 (2017), https://arxiv.org/pdf/1602.05466.
Brandes, PRE 91, 052149 (2015), https://arxiv.org/pdf/1503.03672, treats
interacting channels and local signal propagation. Ordinary controllers can
consume the added-carrier port here; no new basic feedback algorithm is claimed.

Density's failure to determine divergence-free current is explicit in
Bertini et al., https://arxiv.org/pdf/math/0512394. Nemoto--Sasa, PRL 112,
090602 (2014), https://arxiv.org/pdf/1309.7200, precedes feedback construction
of rare-current ensembles by learned native rate changes. It is a strong
alternative, not evidence for novelty of an abstract change of measure.

The candidate addition is the conjunction: actual dilute carriers, finite
delayed local control with unknown bounded native kinetics, nonlinear
circulation-history transformation, and preservation of the full interacting
density-path law, with retained auxiliary records. This is an enabling
architecture theorem. Historical priority and practical advantage have not
been established. Broad spatial-network versions, manufactured-port errors,
and an acquired total resource budget remain separate tasks.
