# An obtainable stationary-preparation interface for the pulse certificate

## Decision

**Exact preparation can be supplied algorithmically for a substantive,
explicit class of finite attractive spin simulators.** Monotone coupling
from the past (CFTP) supplies independent Gibbs starts without a normalizer.
Known Gibbs updates also supply the common invariant measure and actual
adjoint controls. This closes the logical interface for that class.

It does not establish a cost advantage. The same explicit factors give every
competitor full simulated states, exact state copying, conditional sampling,
and coupling bounds. Perfect preparation may itself be expensive. The
appropriate scoped application is reusable finite-budget variance prediction
for schedules of complete Gibbs sweeps, for observables such as bounded
magnetization or energy density. This is a computational statistical-mechanics
task, not a certificate for the physical dynamics of an unknown material.

No new fixture, numerical experiment, implementation, or empirical advantage
claim is made here.

## 1. A finite-bit input class

Let G=(V,E) be an explicitly supplied finite graph with N vertices and
bounded maximum degree Delta. Use binary spins x_i in {0,1} and rational
factors lambda_i>0 and theta_ij>=1, all with finite encoded bit length:

\[
\pi(x)=Z^{-1}\prod_i\lambda_i^{x_i}
\prod_{\{i,j\}\in E}\theta_{ij}^{x_ix_j}.
\tag{1}
\]

This is an attractive lattice gas, equivalently a ferromagnetic Ising model
with fields. It has 2^N configurations; the factorization is the input,
not a supplied table of 2^N equilibrium probabilities. Rational factors
define the exact target in this contract. Rounding parameters of another
physical model would introduce an additional model error and is not silently
covered by exact simulation of (1).

The conditional probability at site i is

\[
p_i(x_{\partial i})=
\frac{\lambda_i\prod_{j\sim i}\theta_{ij}^{x_j}}
{1+\lambda_i\prod_{j\sim i}\theta_{ij}^{x_j}}.
\tag{2}
\]

It is rational, lies strictly between zero and one, and increases with
every neighboring spin. The partition function cancels. The heat-bath
operator K_i replaces spin i according to (2) and fixes the others.
As conditional expectation under pi, K_i is a self-adjoint contraction
on L2(pi) and preserves pi. These facts follow from the explicit factors;
they are not learnt from the correlation experiments.

For a fully finite-bit construction, compute all 2^(degree(i)) local
conditional probabilities at each site. Let D_i be the least common
multiple of their denominators. Store the integer thresholds D_i p_i(s).
Draw K uniformly from {0,...,D_i-1} and set x_i=1 exactly when
K<D_i p_i(s). Using the same K for different states gives the monotone
coupling. Fair-bit rejection sampling generates the integer exactly.

This charges O(sum_i 2^(degree(i))) conditional entries, their rational
arithmetic, all least-common-multiple and threshold work, and their storage.
The bit length of D_i can reach the sum of the denominator bit lengths.
Bounded degree makes this a finite local preprocessing route; it is not
free input and should not be generalized to unbounded degree without
charging its exponential dependence. A lazy-bit comparison alternative
can avoid these tables, but all precision work must then be counted.

## 2. Exact CFTP preparation and why it terminates

Use the reference preparation kernel K=N^(-1) sum_i K_i. Its random map
first draws a site uniformly and then the exact integer for that site's
conditional rule. Every map preserves the coordinatewise order. Run the
all-zero and all-one configurations through the same maps from time -T
to the fixed endpoint 0. Equality at time 0 certifies that every possible
starting configuration has the same image. Double T until this occurs,
preserving all previously drawn maps at their original time indices.

This is the monotone Propp–Wilson construction [1]; Fill's primary paper
gives its precise algorithm and distinguishes it from stopping at forward
first coalescence [2, §5.2]. The following proof makes the input contract
explicit. Let Phi_T be the composition of the T maps ending at time zero,
and let tau be the first lookback length for which Phi_T is constant.
For any fixed T, applying Phi_T to an independent pi-distributed state
still has distribution pi. On {tau<=T}, that image is the eventual CFTP
output Z. Therefore

\[
d_{TV}(\mathcal L(Z),\pi)\le P(\tau>T)\longrightarrow0.
\]

Almost-sure termination follows here without assuming a useful mixing
bound. Define b_i=1-max_s p_i(s)>0. In a block of N reference updates,
the event that sites 1,...,N are selected in that order and every shared
integer forces its site to zero has probability

\[
\beta=N^{-N}\prod_{i=1}^N b_i>0.
\]

That block is a constant map. Independent blocks yield

\[
P(\tau>mN)\le(1-\beta)^m,\qquad E\tau\le N/\beta.
\tag{3}
\]

This is a termination proof, not an affordability claim: beta can be tiny.
Independent random-map streams for independently completed calls give
IID pi-distributed configurations. Fresh pulse randomness is independent
of preparation and of training, giving the conditional stationary-start
contract needed for subsequently selected target schedules.

The coalescence test concerns the reference sampler and its known order;
it is not arbitrary recognition of an unknown model's state space or a
learned proof of physical equilibrium.

## 3. Preparation cost and stopping semantics

If tau is the minimal successful lookback, the final doubled horizon
T_* is less than 2 tau. The sum of replayed horizons is less than 4 tau.
Updating both bounds at every replay step therefore uses fewer than
8 tau single-configuration conditional updates. Count those failed
shorter lookbacks: they are work, not discarded setup.

An explicit implementation stores up to T_* random-map symbols, each with
its site and integer draw, plus two N-bit configurations and the local
conditional tables. Store/replay includes all random bits or an explicitly
declared pseudorandom approximation; an unqualified seed is not a proof
of mathematically independent fair bits. Exact integer rejection costs
expected fewer than twice its bit width per draw. Actual bit arithmetic,
memory, random generation, and observable evaluation remain charged.

**Use a prescribed number of completed independent CFTP calls.** Pause and
resume a call while preserving its maps. Do not discard a slow call and
restart until a fast one succeeds: CFTP output and runtime need not be
independent, so such censoring can bias the retained states [2]. A resource
cap can return UNKNOWN/no completed acquisition. It cannot silently turn
the selected fast completions into the IID data assumed by Hoeffding.
Fill's interruptible perfect sampler is an established alternative when
that stopping contract is essential; its own transitions and rejection
costs must be included [2].

For K acquired pulse protocols, let m_w be the independently prepared
trials for protocol w, C_prep the random preparation work, C_pulse(w) its
charged update work, and C_f the readout work. A raw endpoint acquisition
has cost of the form

\[
C_{\rm local\ tables}+
\sum_w\sum_{r=1}^{m_w}
\bigl(C_{{\rm prep},w,r}+C_{\rm pulse}(w)+2C_f\bigr),
\tag{4}
\]

in addition to fitting, representation search, exact certificate checking,
and later target execution. Products f(X_0)f(X_T) lie in [-1,1]. A simple
simultaneous Hoeffding allocation of half-width eta_w uses
m_w>=2 eta_w^(-2) log(2K/delta). This is a sufficient count, not an optimum.
The mean-free two-copy observable F=(f-f')/2 uses two independent
preparations and two pulse executions per paired trial. Reuse of existing
traces is legitimate only when their independence and retained readouts
support that pairing.

## 4. Actual adjoints and a meaningful scheduling language

The current adjoint certificate permits complete systematic sweeps.
For a sweep A=K_(i_1)...K_(i_N), with every site included,

\[
A^*=K_{i_N}\cdots K_{i_1}.
\]

The actual reverse-order sweep is an executable Markov operation preserving
the same pi. Its availability is derived from the explicit heat-bath
operators. The forward and reverse acquisition data must both be charged;
one must not declare a forward sweep self-adjoint. Reversible random-scan
mixtures, their powers, and palindromic sweeps are alternative actions.

The scientific schedule language should use complete sweeps or suitable
full-system blocks. An alphabet of individual site updates contains words
that update one site forever, preserving functions of untouched sites.
For many observables the strict all-word contraction certificate is then
uninformative even though ordinary complete-sweep sampling is useful.
Selecting a scheduling language is a task restriction and must be stated.
Likewise an invertible deterministic action together with its inverse
contains identity words; no strictly decaying predictor can approximate
their nonzero correlation arbitrarily well. Neither issue is repaired by
perfect stationary preparation.

Within this schedule language, the target can be the finite variance of
the mean of bounded magnetization, normalized energy, or an event indicator
under a previously unqueried sequence of sweep orders. The certificate
concerns these algorithmic update protocols. Interpreting them as physical
time evolution would require a separate model warrant.

## 5. Baselines given the same source and controls

**Full simulated-state access and copying.** The CFTP implementation already
stores each N-spin configuration. A competitor may copy that full state
and run independent conditional futures, without enumerating 2^N states.
This supplies batched snapshot access for stochastic residual/Galerkin
methods, including the ResDMD interface [4]. It may also use explicit local
spin features, exact conditional expectations when available, control
variates, and the very same retained scalar correlation representation.
An artificial endpoint-only restriction on that competitor would be unfair.

**Coupling and influence bounds from the factors.** Compute the rational
influence

\[
c_{ij}=\max_{s,s'\text{ differing only at }j}
|p_i(s)-p_i(s')|
\]

from the same local tables. If alpha_col=max_j sum_i c_ij<1, common-update
coupling of the uniform reference chain satisfies

\[
E[H_{t+1}\mid X_t,Y_t]
\le[1-(1-\alpha_{\rm col})/N]H_t.
\]

Starting at the extremal configurations gives
P(tau>t)<=N exp(-(1-alpha_col)t/N), hence expected CFTP update work
O(N(1-alpha_col)^(-1) (1+log N)). This elementary bound counts reference
single-site updates, not sweeps. It is an instance of the established
influence-matrix methods, for which stronger weighted norms are available
[3]. The local arithmetic and matrix analysis are paid, just as for the
learned representation.

For complete sweeps, alpha_row=max_i sum_j c_ij<1 gives a direct
schedule-uniform contraction of the maximum disagreement probability:
after every site has been updated once, it is at most alpha_row times
its value before the sweep, for any order. Keeping the full influence
matrices can improve this bound and give observable-dependent covariance
and finite-variance bounds. Thus the regime with a simple polynomial
preparation guarantee already offers strong direct analytical competitors.

**Direct exact-start inference.** Each prepared state supplies an IID
observation for the same equilibrium mean. For a specified target schedule,
two independent target averages Y,Y' give
Z=(Y-Y')^2/2 in [0,2] with E Z=Var(Y). Direct concentration of Z yields a
finite-budget variance bound without identifying a global gap. Charge its
preparations, full target sweeps, and readouts; compare it with (4) across
the actual number of changed schedules. The paid starts and all retained
observations must be usable by both methods.

## 6. What this resolves and what it relocates

The interface is **obtainable** in the specified simulator class. No unknown
normalizer or arbitrary exact-equilibrium oracle is assumed. Monotonicity
and adjoint access are warranted from explicit finite local rules; exact
coalescence supplies the samples. The argument does not require learning
the 2^N-state transition matrix.

Its efficiency remains conditional. Outside a regime with sharp coupling
bounds, successful CFTP still certifies an exact sample, but the observed
and expected cost may be large. Replacing stationary preparation by CFTP
relocates that part of the difficulty to a charged, self-verifying
computation; it does not remove it. Inside an easy coupling regime, the
same information can make the strongest direct baseline very good.

A regeneration label alone would not close the same interface. A reset at
a regeneration time generally has its regeneration law, not pi. Stationary
sampling from regenerative cycles requires the appropriate equilibrium
occupation/length-bias construction and finite-cost access to it. Merely
observing a reset or return is insufficient.

The completed representation theorem therefore has a concrete algorithmic
front door, while **practical acquisition-and-inference advantage remains
UNKNOWN**. No physical preparation of an unknown system, class recognition
from black-box observations, or new perfect-sampling result is claimed.

## Sources and retrieval limits

1. J. Propp and D. Wilson, *Exact sampling with coupled Markov chains and
   applications to statistical mechanics* (1996). Publisher abstract and
   primary-paper metadata retrieved. The Berkeley full-paper PDF timed out;
   no claim of reading that full copy is made.
   https://doi.org/10.1002/(SICI)1098-2418(199608/09)9:1/2%3C223::AID-RSA14%3E3.0.CO;2-O
2. J. A. Fill, *An Interruptible Algorithm for Perfect Sampling via Markov
   Chains*. Author-hosted primary paper, especially §§4–6, read for the exact
   monotone transition contract, CFTP algorithm, and runtime-censoring issue.
   https://www.ams.jhu.edu/~fill/papers/algo1.pdf
3. M. Dyer, L. A. Goldberg, and M. Jerrum, *Matrix norms and rapid mixing
   for spin systems*, arXiv v3 / Annals of Applied Probability (2009),
   introduction, Lemma 17, Corollary 18, and systematic-scan discussion.
   https://arxiv.org/pdf/math/0702744
4. M. J. Colbrook, Q. Li, R. V. Raut, and A. Townsend, *Beyond expectations:
   Residual Dynamic Mode Decomposition and Variance for Stochastic Dynamical
   Systems*, v3, previously read §§3.2 and 4.2; primary abstract rechecked.
   https://arxiv.org/html/2308.10697v3
