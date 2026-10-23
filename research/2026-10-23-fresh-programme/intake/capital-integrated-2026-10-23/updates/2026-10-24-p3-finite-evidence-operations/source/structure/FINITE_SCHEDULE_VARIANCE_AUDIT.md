# Finite-schedule variance from an acquired correlation program

## Finding

The proposed operation is correct. A uniform absolute error for all finite
open-loop correlations gives the same absolute error for the second moment
of any finite time average. The weighted-program subword recurrence evaluates
that second-moment approximation in O(n d^2) arithmetic operations. A paid
mean interval then gives a variance interval, and Chebyshev gives a finite-run
confidence statement without a global mixing bound.

The useful claim is **reusable finite-schedule second-moment/variance
certification under the acquisition and preparation contract**. It does not
by itself make an inaccessible equilibrium mean newly answerable. Independent
stationary starts are already IID samples for that same mean; they belong in
the strongest baseline. Historical novelty and practical advantage remain
UNKNOWN. This note is a theorem and scope audit, not a benchmark.

## 1. Exact identity and error propagation

Let X_0 have distribution pi and let fixed actions a_1,...,a_(n-1) choose
Markov transitions P_a, each preserving pi. Write

\[
Y_n=\frac1n\sum_{i=0}^{n-1} f(X_i),\qquad
\mu=\pi(f),\qquad |f|\le1.
\]

For i<j, the Markov property and the stationary marginal at time i give

\[
E[f(X_i)f(X_j)]=C(a_{i+1}\cdots a_j),\qquad
C(w)=\langle f,P_wf\rangle_\pi.
\]

Consequently,

\[
E[Y_n^2]=\frac{nC(\varnothing)+
2\sum_{0\le i<j\le n-1}C(a_{i+1}\cdots a_j)}{n^2}.
\tag{1}
\]

Only common stationary marginals and the Markov/open-loop contract are
needed for this identity. Reversibility is needed by the existing correlation
acquisition construction, not additionally by this composition step. The
inhomogeneous process need not have a shift-invariant joint law.

Suppose one data event gives |C(w)-Q(w)|<=eps for every finite word. Replace
each C in (1) by Q to obtain S_Q. The coefficients are nonnegative and sum
to [n+2 binom(n,2)]/n^2=1, hence

\[
|E[Y_n^2]-S_Q|\le\varepsilon.
\tag{2}
\]

A sharper retained diagonal bound |C(empty)-Q(empty)|<=delta_0 gives

\[
|E[Y_n^2]-S_Q|\le\delta_0/n+(n-1)\varepsilon/n.
\]

The n=1 boundary is simply E[f(X_0)^2]=C(empty). An average with n=0
is undefined and must be rejected. Repeated subwords enter with their
actual multiplicities.

## 2. Weighted-program evaluation

Suppose Q(w)=L M_w R with program dimension D=2d. Start a row u=0 and
scalar s=0. For each action a_k in chronological order perform

\[
u\leftarrow(u+L)M_{a_k},\qquad s\leftarrow s+uR.
\]

Induction gives
u_k=sum_(h=1)^k L M_(a_h)...M_(a_k). Thus the final s is the sum of Q
over every nonempty contiguous subword, exactly the off-diagonal sum in
(1). Return

\[
S_Q=[nLR+2s]/n^2.
\]

This uses O(n D^2) arithmetic and O(D) working storage in addition to the
stored action matrices. Exact arithmetic bit growth, construction, fitting,
metric search, and acquisition are separate charged costs. A retaining
program with the same evidence can execute this recurrence identically.

## 3. Mean uncertainty and an honest confidence statement

Let the same joint data event also give mu in [m_-,m_+] contained in [-1,1].
Set

\[
v_- = \min_{m\in[m_-,m_+]}m^2,\qquad
v_+ = \max_{m\in[m_-,m_+]}m^2.
\]

The minimum is zero if the interval crosses zero; otherwise it is the
smaller endpoint square. Clip the second-moment interval from (2) to [0,1],
calling it [s_-,s_+]. Then

\[
\operatorname{Var}(Y_n)\in
\left[\max(0,s_- - v_+),\;s_+-v_-\right].
\tag{3}
\]

The upper endpoint can also be intersected with a retained upper bound for
Var_pi(f), since Jensen gives Var(Y_n)<=Var_pi(f). Inconsistent intervals
should be rejected. No separate estimate of mu is required if a structural
symmetry already warrants mu=0. Such a warrant must be stated.

Assume the joint acquisition event has probability at least 1-delta, with
both correlation and mean uncertainty charged. A finite schedule and n may
be selected after seeing the acquisition data. The target trajectory must
then be freshly prepared from pi **conditionally on those data and the
selected schedule**. If U is the valid nonnegative upper endpoint in (3),
then for alpha>0 the interval

\[
[Y_n-\sqrt{U/\alpha},\;Y_n+\sqrt{U/\alpha}]
\]

covers mu with probability at least 1-delta-alpha. Handle U=0 directly:
the target average equals mu almost surely on the good event. For a fixed
t>0, the corresponding conditional failure bound is min(1,U/t^2).
There is no new union bound over selected schedules or finite horizons.
Selecting a schedule from intermediate observations of the target run is
outside this claim.

Conditional preparation is essential, not a technical convention. On two
states with uniform pi and f(x)=x, let P_rho be the symmetric transition
with diagonal (1+rho)/2. For 0<rho<1 it is an irreducible reversible
continuous-time pulse. If a reused training endpoint X_0 selects P_rho_h
when X_0=1 and P_rho_l when X_0=0, then

\[
E[(X_0+X_1)/2]=1/2+(\rho_h-\rho_l)/8.
\]

Every candidate action preserves pi, but the selected run is biased unless
the two rho values agree. An unconditional stationary endpoint is therefore
insufficient when it also drives the choice of schedule.

## 4. Two precision obstructions

**A fixed correlation certificate has a floor.** Equation (2) gives an
additive eps variance uncertainty. It does not automatically shrink as
n grows. A Chebyshev target P(|Y_n-mu|>t)<=alpha needs the certified variance
upper bound <=alpha t^2. In particular, a hoped-for t of order n^(-1/2)
requires variance uncertainty of order 1/n. The previously proved hidden
slow-tail obstruction explains why this limitation cannot simply be
removed by declaring asymptotic variance or mixing.

**Raw nonzero means conflict with strict coefficient contraction.** In the
existing uniform construction, r<1 implies Q(a^N) tends to zero, including
its first-order correction channel. For an ergodic source C(a^N) tends to
mu^2. Therefore an all-word raw-correlation bound must have eps>=mu^2.
Subtracting mu^2 only after computing (3) does not remove that certificate
floor. General noncentered observables need a paid/known centering step or
an explicit invariant constant channel with contraction restricted to the
centered part. The already exposed centered witnesses are unaffected.

### Precise centering and constant-channel scope

If mu is exactly known, choose s>=1+|mu| and use the bounded centered
observable g=(f-mu)/s. Then

\[
\pi(g)=0,\quad |g|\le1,\quad
C_f(w)=\mu^2+s^2C_g(w),\quad
\operatorname{Var}(Y_{n,f})=s^2E[Y_{n,g}^2].
\]

Apply the strict-contraction certificate to g. Carry the known constant
mu^2 in a separate exact channel whose action is the scalar 1. The full
augmented program is not strictly contractive; it does not need to be.
The exact constant contribution cancels in the variance, while the
centered program contributes at most s^2 eps_g uncertainty. This repair
requires the known mean to be a real warrant, with any numerical/readout
precision charged. Merely appending a constant feature and submitting the
entire augmented action to an r<1 check would fail as expected.

If only a numerical center c is known, let s>=1+|c| and g_c=(f-c)/s.
Even on a valid event |mu-c|<=rho, its actual mean is (mu-c)/s, not zero.
The exact relations are

\[
C_{g_c}(w)=\frac{C_f(w)-2c\mu+c^2}{s^2},\qquad
\operatorname{Var}(Y_{n,f})=
s^2E[Y_{n,g_c}^2]-(\mu-c)^2.
\]

An unchanged strictly contractive correlation program for g_c must still
have eps_g>=((mu-c)/s)^2 in an ergodic source. The mean event bounds this
remaining invariant component by rho^2/s^2; it does not annihilate it.
Subtracting the estimated c^2, or subtracting a mean interval only after
the old raw-correlation certificate is formed, does not create an exactly
centered source. A verifier that instead treats the exact unknown mean as
a shared nuisance parameter would need to carry that dependence explicitly.

There is an obtainable exact alternative under the already assumed
**independent stationary reset** interface. Take two independent copies
and define

\[
F(x,x')=\frac{f(x)-f(x')}{2},\qquad
\widetilde P_a=P_a\otimes P_a.
\]

Then |F|<=1 and its mean under pi tensor pi is exactly zero without knowing
mu. The product actions remain common-stationary reversible contractions.
For every word,

\[
C_F(w)=\frac{C_f(w)-\mu^2}{2},\qquad
\operatorname{Var}(Y_{n,f})=2E[Y_{n,F}^2].
\tag{4}
\]

The first identity follows by expanding the four products; the two cross-copy
expectations are mu^2 by independence. Each C_F measurement is obtainable
from two independently prepared endpoint traces with the same pulse word:
multiply their initial f-value difference by their final f-value difference
and divide by four. Sequential independent runs suffice; no hidden-state
cloning or knowledge of pi is introduced beyond the existing reset warrant.
Disjoint pairs give independent bounded observations for ordinary confidence
accounting. Existing individually retained endpoint traces can be paired if
their preparation independence is already warranted; scalar correlation
intervals alone are not a substitute for those observations.

Applying the existing certificate to F gives a variance approximation with
error at most 2 eps_F, and no separately estimated mean is needed. Acquisition
uses two stationary preparations and two pulse executions per paired trial.
This is elementary covariance symmetrization, not a novelty claim. The direct
paired-target-run comparator below uses exactly the same access. The repair
removes only the unknown global constant component: unresolved slow modes,
other invariant components, and the finite residual-error floor remain.

These distinctions affect usefulness, not the validity of the root's
generic finite-variance formula when its stated global error bound is valid.
No further source fixture or implementation check is required to establish
that scope correction.

## 5. Strong baselines and scientific use

**Use the paid starts.** If the acquisition protocol obtains K independent
stationary preparations and observes f at their starts, those K observations
are already IID pi samples for the same mu. Their average has variance
Var_pi(f)/K. Discarding them when comparing downstream mean inference would
hide information already purchased. Cheap independent stationary preparation
can remove the original reason for using MCMC. A useful application therefore
has to price preparation, readout, and updates, or identify a different
target such as reusable protocol variance prediction.

**Direct finite-schedule calibration needs no gap either.** With the same
stationary reset access, obtain independent target averages Y,Y' and set
Z=(Y-Y')^2/2. Then Z is in [0,2] and E Z=Var(Y), without estimating mu.
For m independent pairs, the one-sided Hoeffding upper bound is

\[
\operatorname{Var}(Y)\le \bar Z+
\sqrt{2\log(1/\delta)/m}
\]

with confidence at least 1-delta. It costs 2m prepared target runs. It can
be expensive for long protocols or many changed schedules, but it is a
strong complete acquisition-and-inference comparator. For a second-moment
target alone, Y^2 in [0,1] is an even simpler direct estimator.

**Moment bounds should optimize this finite objective directly.** For a
single reversible action and a centered observable, the variance is the
spectral integral of

\[
p_n(x)=n^{-2}\left[n+2\sum_{k=1}^{n-1}(n-k)x^k\right].
\]

The retained moment intervals define a classical finite moment optimization
problem for this polynomial. Such a method can be stronger than summing
separate uniform correlation bounds. For multiple actions, joint
noncommutative moment constraints provide a more expensive equally informed
alternative. The corrected-center terms are themselves affine functions
of the shared retained data, so combining them before interval evaluation
can also improve the simple eps envelope.

Relevant established primary methods include Paulin's stationary variance
and Bernstein bounds [1], Gyori–Paulin's finite-sample MCMC confidence
analysis and parameter estimation [2], and Berg–Song's moment-constrained
autocovariance estimation [3]. These sources do not establish the particular
all-schedule acquisition result here; they prevent mistaking covariance
summation, Chebyshev inference, or spectral moment structure for new
principles. The present reuse is conditional and scientifically meaningful,
but any practical advantage remains to be demonstrated against the complete
comparators above.

## Primary sources read for this audit

1. D. Paulin, *Concentration inequalities for Markov chains by Marton
   couplings and spectral methods*, corrected arXiv v5, §§3.2 and 5.2.
   https://arxiv.org/pdf/1212.2015
2. B. Gyori and D. Paulin, *Non-asymptotic confidence intervals for MCMC in
   practice*, abstract and §2.2.
   https://arxiv.org/pdf/1212.2016
3. S. Berg and H. Song, *Efficient shape-constrained inference for the
   autocovariance sequence from a reversible Markov chain*, §§1–2.
   https://arxiv.org/html/2207.12705v3

No new numerical fixture or empirical comparison was run for this note.
