# Rare-current law control with unchanged ordinary histories, and noncommuting force limits

30 October 2026. Root consequence of the nonlinear circulation operation.
The ordinary current-governor role supplied the decisive rare-arming
alternative before this consequence was chosen. The theorem below uses
robust sign feedback and does not require calibrated native or auxiliary
mobilities. It is an architecture result at the actual carrier, sensing and
force interfaces, not a new feedback algorithm or a thermodynamic loophole.

## 1. What becomes separately controllable

For the composite conductor in `NONLINEAR_CIRCULATION_OPERATION_AND_PATH_LAW.md`,
an N-dependent controller can simultaneously:

1. preserve its zero-drive ordinary physical trajectory law in total variation
   up to a probability decreasing faster than every inverse polynomial;
2. preserve the complete macroscopic native density-path law, including its
   large deviations;
3. change the speed-N macroscopic circulation-history rate by the physical map
   T_phi, including a nonlinear map or complete cancellation;
4. use vanishing expected carrier-drive work on the unforced deployment,
   while retaining the real continuously running apparatus costs.

These statements concern distinct limits. In particular the curvature of the
limiting large-deviation action need not recover central-limit noise for this
singular controller sequence. A weak-load response can also have different
limits depending on whether system size or force is taken first. The system
is active, retains memory, and is not a passive equilibrium conductor.

## 2. Precise premises and one-time arming

Use a fixed number of native rings with B(s) a bounded-jump martingale of
total activity O(N) in the actual unforced deployment. This property is
pointwise for homogeneous symmetric exclusion, so the initial density profile
need not be flat, equilibrated or newly reset. A hidden class or old record
is allowed when this same future martingale interface holds conditionally.

Use the independent physical carriers with actual rates
c_l exp(plus or minus F/2), c_-<=c_l<=c_+, and independent primitive randomness
from the isolated native system. Unknown fixed c_l suffice. Their exact
zero-force setting makes each auxiliary total a martingale with activity
O(R_N). No auxiliary positional equilibrium is needed. All initial counts
are zero by defining an observation interval, not by resetting physical
positions or discarding an old retained record.

For the finite-duration interacting supplier, replace its true current by
the martingale correction in its exact cell only in the proof. Gaussian
momentum/end-period bounds supply the same concentration. Its fresh sources,
initial momentum and synchronized switching remain actual preparations.

Let phi(t,0)=0 for all t, with the smoothness/evaluator conditions of the main
theorem. Choose

\[
b_N=N^{3/2}\log(2+N),\quad K_N=R_Na_N\to\infty,
\quad a_N\to0,\quad R_N=o(N),\quad K_Nd_N=o(N^2).       \tag{1}
\]

Keep the drive exactly off until a received timestamped error E_a=A_a-Z_a
exceeds b_N in some lane. Each lane can arm separately, or all may arm at
the first such event. Arming is permanent. After it, use the actual delayed
sign servo of the main theorem. Measurement/evaluation error must be o(b_N),
with a whole-horizon superexponential failure bound. This is stronger than
the o(N^2) precision sufficient for the macroscopic theorem alone.

For a clean digital schedule take d_N=O(N log N). Bounded skew and local
buffer/adder resources are given in the separate counter note. Commands and
true carrier motion are retained. There is no trigger-conditioned hidden
initializer and no revelation of a future noise seed.

## 3. Arming is rare, without a microscopic mixing hypothesis

Couple the controlled apparatus to the same zero-drive composite conductor,
including the same initial state, old record, carrier noise, sensors and
clock schedule. The latter may run the same target computation as a shadow
program. Until arming their applied operations and physical histories agree.
This is a proof coupling of two laws, not physical copying of an unknown state.

For a bounded-jump martingale with activity at most C N,

\[
\Pr\{\sup_{s\le N^2T}|B(s)|>x\}
\le C\exp[-c x^2/(N^3+x)].                            \tag{2}
\]

The same bound holds for zero-force A with N^3 replaced by R_NN^2.
Since phi(t,0)=0 and its derivative is bounded,

\[
|Z_N(s)|\le C|B(s)|.                                 \tag{3}
\]

Under the actual zero-drive law the arming event is therefore contained in
a fixed number of native/auxiliary maximal excursions of size c b_N, plus
the observation-error event. Thus

\[
\Pr\{\mathrm{arm}\}\le C_T e^{-c_T\log^2(2+N)}+p_N.   \tag{4}
\]

The native unforced interface is all that is used here. An arbitrary reversible
stationary background can use the stronger ordinary comparator's forward/
backward and tilted-generator arguments, but an initial density ceiling
exp(CN) alone does not preserve the low arming probability for that larger
class. Do not promote that different premise to the present claim.

## 4. The nonlinear macroscopic operation still executes

Before arming, every received error is below b_N plus its certified readout
error. Over an unobserved window d_N, the target source has bounded drift
and noise O(N), by the main theorem's Taylor lemma. Hence for each fixed
epsilon>0 the probability of an unobserved excursion epsilon N^2 is bounded
by a polynomial factor times

\[
\exp[-c_\epsilon N^4/(Nd_N+N^2)],                     \tag{5}
\]

which is superexponential at speed N for d_N=O(N log N). One need not show
that the activation error is itself O(b_N) with a superexponential bound;
o(N^2) with that probability is sufficient. This avoids an unnecessarily
strong overshoot premise.

Once a true macroscopic error exceeds epsilon N^2/2 on the good delayed-window
event, the trigger has already been observed and the controller is armed.
Every contributing sample then has the same sign. Its inward drift is of
order K_N, overwhelming the bounded source drift. The stopped upcrossing
argument in the queue lemma applies unchanged. Add (5) and sensor failures.
For every epsilon>0,

\[
\limsup_NN^{-1}\log\Pr\{\sup_{s\le N^2T}|E(s)|>
\epsilon N^2\}=-\infty.                              \tag{6}
\]

This proof is carried out in the actual filtration and stops at failures.
It never treats the native law after a rare trigger as an equilibrium law.
Consequently the complete nonlinear path-map and LDP of the main theorem
apply to the armed controller as well.

The estimates (2)--(6) also allow bounded weak native loads in the tracking
theorem. Under a load the native total has drift O(1) and arming may be typical;
then (4) and its low-work consequence do not apply.

## 5. Ordinary records remain statistically unchanged

Let P_N^phi and P_N^0 be the laws of common physical path/measurement records
for the armed and zero-drive deployments. Include actual native and auxiliary
paths, delayed reads, timing and applied-force logs on the same record space.
The fixed protocol setting is a condition of the comparison, not a random
data field claimed to be equal. The coupling agrees up to the first arm, so

\[
\|P_N^\phi-P_N^0\|_{\rm TV}
\le\Pr\{\mathrm{arm}\}
\le C_Te^{-c_T\log^2(2+N)}+p_N.                       \tag{7}
\]

Every finite-N record statistic, including an N-dependent rescaling, inherits
this bound. In particular every valid central-limit distribution of the
zero-drive composite remains valid for the controlled composite. Polynomially
many independent passive trials still have vanishing distinguishing power:
their product-law total variation is at most the number of trials times (7).
This is a statement about these deployments, not an impossibility of active
system identification. A sustained force probe or inspection of the controller
program supplies different information and can distinguish them.

For the harmonic current, the unbiased auxiliary variance is O(R_NN^2).
After division by the native central-limit scale N^(3/2), it vanishes when
R_N/N->0. Hence the native harmonic-current central limit is also preserved.
The analogous uncentered native *density* fluctuation statement needs extra
care: R_N/N may exceed N^(-1/2). Equation (7) compares the same composite
reference, which already contains its auxiliary mass. It does not silently
remove that mass at a finer fluctuation scale.

At the same time, a nonzero protected macroscopic circulation has a finite
cost in the native exclusion action, but superexponentially small probability
under phi=0. For a flat native density m and current j, its native dynamic
cost is T j^2/[4D m(1-m)], finite for finite j. The controlled circulation is
concentrated at zero at speed N. This is compatible with (7): an exponentially
rare event may contribute much less than the already small total-variation
bound. The controller changes the tails by acting before the scale N^2 is
reached, while its trigger lies far above the scale N^(3/2).

## 6. Expected force work and the work distribution

For the hop supplier, actual drive work in units k_BT is

\[
W_{\rm drive}=\sum_l\int F_l(s)\,dA_l(s).             \tag{8}
\]

Predictable compensation gives

\[
\mathbb E W_{\rm drive}
=\mathbb E\int\sum_l 2c_l F_l\sinh(F_l/2)\,ds.
                                                               \tag{9}
\]

This is nonnegative and at most C R_N a_N^2 per unit time while armed. It is
zero before arming. Therefore

\[
0\le\mathbb E W_{\rm drive}
\le C_T N^2 R_Na_N^2
[e^{-c_T\log^2(2+N)}+p_N]=o(N^{-p})\quad\forall p>0.   \tag{10}
\]

The prefactor is polynomial because R_N<N and a_N<=1 eventually. Unknown
prefactors require no inference for this bound. Equation (8) is force work;
equating it to total bath heat would additionally require the complete
internal-energy and local-detailed-balance specification. For homogeneous
constant track clocks that specification is explicit in the ordinary note.
Stochastic work need not be positive on every realization.

For the finite-duration mechanical supplier, actual work is F Delta A, not
F(Delta A+Delta P/g). The separately derived full-block-delay identity is

\[
\mathbb E W=RL(\beta^2/2)\sum_m\mathbb EF_m^2
-\frac{R(1/g+b)}{2g}\left[
\sum_m\mathbb E(F_m-F_{m-1})^2+\mathbb EF_{M-1}^2\right].
                                                               \tag{11}
\]

It retains momentum/switching correlations. For aligned blocks of L cells,
one-block-delayed force choices, and F_-1=F_0=0, its lower quadratic coefficient
is nonnegative and its upper bound yields (10) with a constant mobility.
The exact synchronized cell is not interchangeable with a spatially staggered
approximate pulse without an error calculation. Its O(R_NN^2) thermal
preparations continue even while the force is off.

The expected work conclusion is not a uniform bound on each rare history.
For calibrated homogeneous hop clocks c, the convex function

\[
H_R(u)=2u\operatorname{arsinh}(u/(2cR))
\tag{12}
\]

gives, for every causal controller at that affinity-only port,

\[
\mathbb EW_{\rm drive}\ge tH_R(\mathbb EA(t)/t).
                                                               \tag{13}
\]

A sustained O(1) mean correction over t=N^2T costs Omega(N^2/R_N). Constant
affinity attains the mean-work lower bound. An analogous leading bound holds
for the finite-duration carrier under its declared block schedule. These
are loaded-deployment bounds. Conditioning an equilibrium martingale on a
future rare trajectory does not justify applying (13) conditionally without
a separate argument.

The controller continually pays acquisition, timing, storage, local
communication and drive availability. No claim of vanishing total apparatus
energy, free reliability, or practical efficiency follows from (10).

## 7. Explicit noncommuting weak-force and large-system limits

This is a concrete physical consequence beyond a passive current constraint.
Use one homogeneous exclusion ring with n_N particles,
n_N/N->m in (0,1), fixed unknown D>0, and its uniform canonical initial law.
Use the independent homogeneous auxiliary tracks, independent initial state
and clocks, and the armed controller phi=0. The controller does not receive
the force parameter. Let an external per-step field F/N act on the native
lane through rates D exp(plus or minus F/(2N)). The force port is specified:
it acts on that lane, while the auxiliary lane receives its own control force.
Both actual currents are measured in the composite total C_N=B+A.

Define

\[
\mathcal J_N(F)=N^{-2}\mathbb E_F C_N(N^2T),\qquad
\chi_N=\frac{n_N(N-n_N)}{N(N-1)}\to m(1-m).            \tag{14}
\]

**Fixed macroscopic load.** For each fixed finite F the native aggregate
drift is bounded. The queue theorem cancels C_N/N^2 superexponentially.
Its bounded jump intensities give polynomial moments, so Cauchy--Schwarz
on a bad event plus an arbitrary epsilon on its complement proves uniform
integrability sufficient for

\[
\lim_{N\to\infty}\mathcal J_N(F)=0\qquad\forall F.
                                                               \tag{15}
\]

The unchanged native mean is
2D N chi_N sinh(F/(2N)) N^2T, so B/N^2 tends D m(1-m)FT.
The added carriers perform the real cancellation and incur loaded work.

**Infinitesimal force at finite N.** The canonical native initial law is
independent of F. At F=0, the path score for the native likelihood is exactly
B/(2N). The derivative of the total escape rate vanishes pointwise because
sum_i(eta_i-eta_(i+1))=0. Conditional on a complete native path, the auxiliary
controller law has no explicit F-dependence. Thus

\[
\mathcal J'_N(0)=\frac{\mathbb E_0[C_N B]}{2N^3}.
                                                               \tag{16}
\]

Differentiation is legitimate at each finite N: all hop intensities are
bounded on compact force intervals and count moments have exponential bounds.
The controller's threshold discontinuity is a path functional, not an
F-dependent switching formula, so it contributes no extra score term.

Couple A to the zero-drive A^0 as in (7). They agree off the arming event.
Poisson domination bounds all needed moments of A,A^0,B by powers of N.
Holder's inequality and the superpolynomial arming bound imply

\[
N^{-3}|\mathbb E_0[(A-A^0)B]|\to0.                    \tag{17}
\]

Independence gives E[A^0 B]=0. Native B is a martingale, and stationarity
gives E B^2=2D N chi_N N^2T. Hence

\[
\boxed{\lim_{N\to\infty}\mathcal J'_N(0)
=D m(1-m)T>0,
\qquad
\left.\frac{d}{dF}\lim_{N\to\infty}\mathcal J_N(F)
\right|_{F=0}=0.}                                    \tag{18}
\]

This is an order-of-limits result, not violation of finite-system response
theory. The trigger creates a shrinking force boundary layer. Indeed, if
|F_N|=o(log N/sqrt(N)), the deterministic native displacement is o(b_N),
and the same martingale argument keeps arming superpolynomially rare.
A fixed nonzero F ultimately falls outside that layer. The field F/N is
weak per microscopic step even then; the diffusive horizon lets it accumulate
a finite macroscopic displacement.

At zero force the native harmonic current obeys the Gaussian martingale
central limit with variance 2D m(1-m)T. One can check the bracket without a
mixing assumption: the instantaneous canonical activity has variance O(N);
stationarity and Jensen bound its N^-3 integrated-bracket variance by O(1/N).
Bounded rescaled jumps vanish. The zero-drive auxiliary contribution is
O(sqrt(R_N/N)) at this scale, and (7) transfers the same limit to C_N.
Thus this nonzero central-limit noise coexists with (15) and the degenerate
speed-N circulation rate. Passive FDT reasoning cannot be applied across
these different singular limits.

The force could instead be coupled to both lanes at a separately specified
physical port; then its auxiliary contribution and path score must also be
included. The background-only score (16) is not silently used for that
different experiment.

## 8. Information, failures and scientific scope

The operation preserves macroscopic density histories by conservation and
isolation, not by claiming small total relative entropy forces equal rare
laws. Equation (7) shows directly why ordinary passive samples can miss the
changed tails. A sustained active probe detects the different response;
there is no general obstacle to a well-informed conventional learner.

The claims use an actual zero-force setting, an intermediate trigger,
bounded native activity, a true additional carrier lane and a delayed
directional control channel. A reciprocal passive capacitor acting on all
carriers would alter the native density dynamics. A fixed total-loop voltage
does not provide the necessary auxiliary capacity. An unpriced ideal sensor
or a discarded timing record would change the resource comparison.

The direct predecessors remain Brandes's current governor (2010), its
experimental sampled implementation (Wagner et al. 2017), interacting-channel
feedback (Brandes 2015), and established large-deviation/control machinery.
The ordinary role's rare-arming construction materially changed the root's
target. The potential foundational gain is a physical separation of bulk
histories, ordinary circulation fluctuations, rare-current laws, and
macroscopic weak-load response at explicitly different scales. The proof
does not establish historical priority, an apparatus, or a total-cost
advantage. It identifies a stronger capability for an apparatus to realize
and exposes which acquisition and active resources are responsible.
