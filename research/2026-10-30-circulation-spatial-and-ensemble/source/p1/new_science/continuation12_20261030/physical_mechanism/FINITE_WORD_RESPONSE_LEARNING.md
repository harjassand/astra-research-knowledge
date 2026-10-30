# Ordinary finite-word response learning without hidden-force reconstruction

30 October 2026. Existing Astra P1 complementary physical-mechanism role.
This is a constructive ordinary comparator, not a new fluctuation-response
principle. The physical target is to choose a finite pulse schedule that
improves an endpoint readout of an unknown nonlinear thermal material.
No microscopic state is copied, reversed, reconstructed or restarted inside
an episode. All previous work is preserved.

## 1. The actual task and interface

Fix a device, including any frozen fabrication parameters. Its complete
microscopic state is X; only Y(X) is read. A warranted preparation supplies
the same probability law mu before each training episode, conditional on
the complete retained past D. The preparation can be slow and expensive.
Stationarity alone does not supply it. An alternative dependent-data
implementation needs its own mixing, regeneration or concentration contract.

There are n chronological physical stages. Stage k has a supplied finite
duration, actual kernel P_(k,h), and a real control h in a neighborhood of
zero. Its clock, switching and sensing protocol are part of that kernel.
There is no fictitious zero-time intervention or arbitrary hidden reset.
Each P_(k,0) preserves mu, and

\[
 \mu_{k,h}(dx)=
 \frac{\exp[h B_k(Y(x))]}{\mu(\exp[hB_k])}\,\mu(dx),
 \qquad \mu_{k,h}P_{k,h}=\mu_{k,h}.                 \tag{1}
\]

The bounded conjugate feature B_k is known and physically readable,
|B_k| <= b. The control h is dimensionless. For an ordinary thermal
energy port it means the energy change -k_B T h B_k. The microscopic
potential and the kinetic response to h can be unknown. Different stages
can be different, noncommuting operations.

Assume the actual kernels and stationary family are differentiable strongly
enough to differentiate their action on the bounded functions below.
A finite state generator with smooth bounded rates is one sufficient
supplier. An overdamped diffusion with potential U_0(x)-k_B T h B_k(Y(x))
and an actual fluctuation-dissipation-consistent mobility is another, with
its usual well-posedness and differentiation hypotheses. Arbitrary sharp
labels need a real compatible bias operation; their readout alone does not
manufacture that operation.

Let F(Y) be a bounded endpoint loss, |F| <= f. The objective is

\[
 J(h_1,\ldots,h_n)
  =\mu P_{1,h_1}\cdots P_{n,h_n}F.                 \tag{2}
\]

Its training and deployment initial law is mu. The unperturbed stages all
preserve that law, even though they may retain arbitrarily long hidden
memory. Reversibility is permitted but unnecessary for Sections 2--6.

## 2. Exact ordinary estimator of every pulse derivative

Differentiate (1) at h=0. With P_k=P_(k,0), the derivative of the stationary
law has density B_k-mu B_k, so

\[
 \mu P'_k=\mu B_k(I-P_k).                           \tag{3}
\]

Here mu B_k denotes the signed measure with density B_k; the centering
constant cancels because mu P_k=mu. Since the prefix in (2) preserves mu,

\[
 g_k:=\partial_{h_k}J(0)
 =\mu B_k(I-P_k)P_{k+1}\cdots P_n F.               \tag{4}
\]

Execute one baseline episode

\[
 X_0\sim\mu,\qquad X_k\sim P_k(X_{k-1},\cdot),
 \qquad k=1,\ldots,n.
\]

Read the declared visible features at the actual stage boundaries and form

\[
 Z_k=
 F(Y(X_n))\,[B_k(Y(X_k))-B_k(Y(X_{k-1}))].          \tag{5}
\]

Then E Z_k=g_k. The first term has expectation mu B_k P_(k+1)...P_n F,
because X_k has law mu. The second has expectation
mu B_k P_k...P_n F. This proves the claim without a sample of two futures
from the same microscopic state. The chronological episode itself is the
experiment.

The same record supplies all k and any declared collection of endpoint
losses F_l. There is no small-nudge denominator. Unknown derivatives of
the kinetic prefactors cancel from this first-order, stationary-start,
endpoint-average identity. This cancellation does not identify those
derivatives or show that they are physically absent.

This is the finite-word form of equilibrium fluctuation-response theory.
Dembo--Deuschel's general Markov theorem directly supplies the central
principle: preservation of the tilted invariant law fixes the equilibrium
linear response, without requiring reversibility. Baiesi--Maes--Wynants
write the corresponding finite-window endpoint-correlation formula
explicitly. Exact primary links and read scopes are in PRIMARY_SOURCES.md.
The ordinary identity must not be promoted to a new physical adjoint law.

## 3. A finite acquired certificate and its resource ledger

For m independently prepared episodes, or episodes with the same conditional
law given the complete past, average (5). Since |Z_k| <= 2bf,

\[
 {\Pr}\{\max_{k\le n,\,l\le p}
  |\widehat g_{lk}-g_{lk}|>\epsilon\}
 \le 2np\exp[-m\epsilon^2/(8b^2f^2)].              \tag{6}
\]

Thus m >= 8b^2f^2 epsilon^(-2) log(2np/delta) suffices for a simultaneous
coordinate certificate of confidence 1-delta. Correlations between the
coordinates in the same episode do not invalidate the union bound.
There is no hidden-state dimension or hidden spectral gap in (6).

The experiment nevertheless uses:

* m warranted initial preparations, not m free equilibrium samples;
* mn actual stage calls and m times the complete physical word duration;
* the needed visible boundary readings, their reliability and reaction;
* storage or streaming accumulation for the requested features/outputs;
* calibrated input units, finite-duration clocks, switching and later
  parameter updates; and
* fresh physical noise and a conditional device law consistent across
  the episodes.

A long baseline record is not m independent episodes merely because it has
m disjoint windows. A frozen hidden variable is an immediate obstruction
to that substitution. One old specimen also does not resample a population
of fabrication classes. A per-device conditional statement and a new
population-preparation statement are different experiments.

Bounded sensor errors can be charged directly. If every B reading errs
by at most e_B and F by at most e_F, the error in (5) is at most
2 f e_B+2 b e_F+2 e_B e_F. A claim of unbiased separate readings is not
enough when their product uses shared sensor noise; the actual joint
instrument must justify it. No generic noninvasive reader is inferred.

## 4. An actual control consequence, including finite amplitudes

Let U be any declared set of pulse directions satisfying ||u||_1 <= A,
with an ordinary finite-dimensional optimizer available. Choose

\[
 \widehat u\in\arg\min_{u\in U}\widehat g\cdot u.
\]

On (6),

\[
 g\cdot\widehat u-\inf_{u\in U}g\cdot u
 \le 2A\epsilon.                                  \tag{7}
\]

This globally certifies the best first-order endpoint improvement in the
declared direction set. It is a useful transient control problem, not
training a hidden-state model.

For a certified descent direction, put

\[
 d=-\widehat g\cdot\widehat u-A\epsilon>0.           \tag{8}
\]

Then g dot u_hat <= -d. Differentiability gives, for all sufficiently
small positive lambda,

\[
 J(\lambda\widehat u)-J(0)
 \le-\tfrac34 d\lambda.                            \tag{9}
\]

The threshold in (9) is not supplied by static equilibrium weights.
A competent ordinary controller can instead validate a real finite step.
Try lambda_j=2^(-j), paying actual preparations and complete controlled
words for independent baseline and candidate endpoint-loss samples.
Estimate their difference Delta_j with an all-round confidence radius
d lambda_j/8, allocating failure probabilities summably, e.g.
delta_j=6 delta_val/[pi^2(j+1)^2].
Accept when

\[
 \widehat\Delta_j+d\lambda_j/8
 <-d\lambda_j/4.                                  \tag{10}
\]

At acceptance, the actual finite pulse program has mean loss at least
d lambda_j/4 lower than the unperturbed word. For a fixed differentiable
source satisfying (8), (9) implies eventual acceptance on the simultaneous
confidence event. There is no source-independent bound on the number of
halvings or samples without a real remainder/modulus contract. At stage j
the ordinary bounded-data sample requirement is of order
f^2/(d^2 lambda_j^2) times the confidence logarithm.

This is a complete, implementable improvement procedure at the supplied
baseline and control interfaces. It uses physical validation rather than
pretending that the linear response predicts a finite change exactly.
The selected direction is fixed before its fresh validation samples.

For several endpoint readouts, (6) similarly learns a small-signal response
matrix. A conventional constrained least-squares controller can design a
waveform to fit an output target. The finite physical action still needs
the remainder contract or actual validation above.

## 5. What happens to the horizon

If the same B is conjugate to every stage and a constant h is applied,
the sample for the derivative in that constant direction telescopes:

\[
 \sum_{k=1}^n Z_k
 =F(Y(X_n))[B(Y(X_n))-B(Y(X_0))].                   \tag{11}
\]

Its amplitude is bounded by 2bf at every horizon. Only two feature
readings are needed for this single direction. A long physical time is
still a long experiment; there is no claim of free time or relaxation.

For a predetermined waveform u,

\[
 \sum_{k=1}^n u_k(B_k^{\rm time}-B_{k-1}^{\rm time})
 =u_nB_n^{\rm time}-u_1B_0^{\rm time}
   +\sum_{k=1}^{n-1}(u_k-u_{k+1})B_k^{\rm time},    \tag{12}
\]

where B_k^time=B(Y(X_k)). The absolute response sample is at most

\[
 bf\big(|u_n|+|u_1|+\sum_{k=1}^{n-1}|u_{k+1}-u_k|\big). \tag{13}
\]

Thus bounded-variation waveforms have a statistical bound governed by
their variation rather than the number of fine clock cells. Rapidly
alternating controls can have variation proportional to n. This is the
ordinary entropy-flux/integration-by-parts form of FDT, not a new
elimination of all horizon costs.

An additive expected loss sum_r a_r F_r(X_r) also works: for pulse k,
replace F(X_n) in (5) by sum_(r>=k) a_r F_r(X_r), with the appropriate
bound on that sum. This covers time-integrated expected state loss.
An arbitrary joint path loss is not covered; Section 7 gives an exact
failure already for a two-time product.

## 6. Concrete nonlinear physical supplier

On a compact configuration space, let an unknown interacting potential
U_0(x) and positive reciprocal mobility M_k(x,h) define the actual
overdamped generator

\[
 L_{k,h}f
 =\mu_{k,h}^{-1}\nabla\cdot
       (\mu_{k,h}M_k(x,h)\nabla f),                 \tag{14}
\]

with reflecting conormal or periodic boundaries. The supplied port adds
-hB_k to the dimensionless energy; the sensor reads B_k and F, which may
depend only on a small subset of coordinates. Execute stage k for its
actual finite time tau_k: P_(k,h)=exp(tau_k L_(k,h)).
The unknown mobilities and potential can be nonlinear and can couple the
visible and hidden coordinates. They need not be fitted.

Equation (14) is a mathematical family of actual thermal controls, not an
apparatus proof that every nonlinear material exposes those controls.
The known conjugate potential, physical thermal coupling, initialization
and readout have to exist. Noninvasive readout and temperature calibration
cannot be deduced from stationarity. If a stage changes a barrier or
thermal environment as well, its extra actuation costs remain.

For ideal prescribed conjugate-energy switching the source work is
-k_B T integral B dh. For isolated pulses started and ended at zero, its
absolute switching contribution is bounded by
2 k_B T b lambda ||u||_1. This counts that energy port only, not the cost
of preparing equilibria, waiting, reading, storing or modifying hidden
kinetic barriers. A small control-work bound does not price the learner.

## 7. Exact boundary: endpoint means hide kinetic information

The following two-state family is enough. X is +1 or -1 and

\[
 q_h(x,-x)=c(h)e^{-hx},\qquad c(h)>0,\quad
 \mu_h(x)=e^{hx}/(2\cosh h).                        \tag{15}
\]

Every member is reversible for the same specified Gibbs family. Take
X_0 uniform and observe at time t. Put r(h)=2c(h)cosh h. Direct solution
of the two-state forward equation gives

\[
 E_hX_t=\tanh h\,[1-e^{-r(h)t}],                    \tag{16}
\]
\[
 E_h[X_0X_t]=e^{-r(h)t}.                           \tag{17}
\]

Sources with the same c(0) have identical complete baseline path laws
and identical static biased equilibria for every h. Nevertheless,

\[
 \left.\partial_hE_hX_t\right|_0=1-e^{-2c(0)t},
 \qquad
 \left.\partial_hE_h[X_0X_t]\right|_0
   =-2c'(0)t e^{-2c(0)t},                         \tag{18}
\]
\[
 \left.\partial_h^2E_hX_t\right|_0
   =4c'(0)t e^{-2c(0)t}.                          \tag{19}
\]

The first derivative of the endpoint mean is precisely the ordinary
FDT value. The full two-time record and the second-order endpoint
response retain the unknown kinetic derivative. This is not a failure
of FDT; those are different questions.

For an old retained record X_0=x, the endpoint derivative is

\[
 1-e^{-2c(0)t}-2x c'(0)t e^{-2c(0)t}.              \tag{20}
\]

Hence an unconditional stationary certificate is not a certificate
conditional on every old record. The same calculation with initial
mean m_0 replaces x by m_0 and shows the nonstationary-start obstruction.
With c(h)=c_0+a sin(Lh), 0<a<c_0 fixed, all rates remain bounded on a
fixed control interval while |c'(0)|=aL is unbounded. A finite hidden
rate ceiling therefore does not supply a uniform linear-response radius.

Even absolute bounded-variable estimation does not cure vanishing
signals. In (15) with c(0)=epsilon and B=F=X, the constant-field sample
is 1-X_0X_t, equal to 2 only if the endpoints differ. Its mean is
R_t=1-exp(-2 epsilon t), variance 2R_t-R_t^2.
For epsilon t small, constant relative precision requires order
1/(epsilon t) independently prepared episodes, hence order 1/epsilon
native elapsed-time budget. Choosing a longer t changes the allocation,
not the physical slow-mode burden.

## 8. Static equilibrium training is an even stronger ordinary comparator

If actual preparations are available for
mu_theta proportional to exp[-U_0-sum_j theta_j V_j], with known
readable V_j, then for a theta-independent bounded cost C,

\[
 \partial_{\theta_j}\mu_\theta C
 =-\operatorname{Cov}_{\mu_\theta}(C,V_j).          \tag{21}
\]

Two independent actual equilibrium preparations X,X' give the unbiased
sample

\[
 -\tfrac12[C(X)-C(X')][V_j(X)-V_j(X')].             \tag{22}
\]

The ordinary Gibbs-score route supplies all coordinates without a
dynamic adjoint, a nudging port for C, hidden-force knowledge, or a
finite-difference denominator. It pays the preparations and local
feature readings. It need not be available when the derivatives of the
physical energy controls cannot be read.

Equilibrium propagation is a powerful alternative when the loss can be
physically nudged. In an equilibrium Markov system, apply a small
energy nudge +hC from mu_theta and observe V_j at finite time t. Its
first-order response is

\[
 R_j(t)=-\operatorname{Cov}(C,V_j)
             +\operatorname{Cov}(C(X_0),V_j(X_t)). \tag{23}
\]

The last term is the actual finite-relaxation bias. It need not vanish
when hidden classes are frozen. For a reversible continuous semigroup,
its magnitude is at most

\[
 \sqrt{\langle C_c,P_tC_c\rangle\,
             \langle V_{j,c},P_tV_{j,c}\rangle},   \tag{24}
\]

because P_t=P_(t/2)^*P_(t/2). This gives an ordinary visible-correlation
route to certifying a finite-time EqProp bias, with actual mean and
correlation acquisition costs. It does not certify hidden ensemble
equality or arbitrary later interventions.

Known control-energy derivatives are not a universal requirement of all
ordinary physical learning. Agnostic EqProp already uses floating
parameter coordinates, one homeostatic control per parameter and a real
loss-nudging energy. It obtains a gradient step without explicitly
calculating those derivatives. Its supplied relaxation/minimization,
clamping and homeostatic ports are substantially stronger than merely
being handed a reversible thermal operation. We do not remove those
costs when comparing it.

Finally, if the target is moment fitting rather than an arbitrary
nonconvex task, the ordinary objective
log Z(theta)-theta dot m_star for
mu_theta proportional to exp[theta dot B]mu_0
has gradient mu_theta B-m_star and Hessian Cov_theta(B).
An equilibrium sampler plus conventional stochastic convex optimization
already learns the closest attainable moment target. The unknown base
potential is unnecessary. Actual preparation at each theta, conditioning
of the covariance and reachability of the requested moments remain.

## 9. Retained-record and deployment scope

All confidence statements can be conditioned on a fixed complete prior
D if the declared preparation and Markov/control contracts hold under
that conditioning. They cannot be extended by subsequently conditioning
on one of the path readings used in the estimator. Section 7 proves why.

An adaptive input program whose earlier choices depend on observed
states usually destroys the stationary-prefix identity in (3)--(5).
One can use an ordinary score estimator if the full likelihood derivative
is supplied, or actual randomized selector scores when only the
controller probabilities are varied. Those are legitimate stronger
comparators, with their variance, horizon, exploration and record costs.
Neither unknown Gibbs weights nor physical reciprocity supplies the
missing hidden transition score by itself.

The result is an actual ordinary capability: acquire and use a complete
finite small-signal endpoint response matrix of an unknown nonlinear
material, and validate a real improved pulse program. It is not a
complete-record learner, full-state preparation certificate, universal
nonlinear controller, hardware demonstration or speedup claim.
