# A third future is an operation; finite randomization is an alternative

29 October 2026. Complementary interface analysis, ordinary proofs. This note
does not assume a microscopic reset, hidden contraction, bath reversal or
state-cloning instrument is available.

## 1. What a reversible stationary record supplies

For a stationary reversible Markov state X_0, the past and future are
conditionally independent given X_0. After the correct physical parity is
applied, both are future experiments from the same present state. If the two
reported experiments have conditional mean functions a(X_0),b(X_0), their
paired stationary record acquires E[a(X_0)b(X_0)]. This supplies a bilinear Gram
form, assuming the reports and reversal are the stated physical operations.

The ordinary stationary record does not thereby acquire
E[a(X_0)b(X_0)c(X_0)] for three independently evolved future experiments.
Three time windows on one trajectory are not three independent futures from
the same X_0. Past and future give two sides; cutting more windows does not
restore the state at the center. The present visible label can be a third
emission, but it may be constant on a hidden fiber and fail to resolve it.

A complete output-law ambiguity pair supplies a decisive abstract test: every
common randomized postprocessing of its stationary output, including recorded
time reversal, subsampling, simulated stitching, data-dependent feature fitting,
or noise added only AFTER observation, has the same law on the pair. None can
produce a distinguishing physical three-future statistic. This is immediate
from equality of measures and common-kernel contraction, not a sample limit.

## 2. Why a momentum flip is not hidden-state restoration

The native Langevin equation has dissipative drift and a realized thermal noise
history. Reversing the observed momentum at the end of a segment and evolving
with fresh thermal noise gives another stochastic segment, not a return to the
initial full microscopic state. Even when its equilibrium distribution is
correct, equality of marginal preparation laws is weaker than returning to
the same latent state needed for conditional three-view moments.

Exact microscopic Hamiltonian reversal of system AND bath, or exact state
checkpoint/restore in a simulator, can warrant a return-and-branch protocol.
These are additional operations with their own state coverage and precision.
A bath-noise playback protocol must also account for dissipative terms and all
hidden forces; recording only the observed momentum cannot supply them.
Classical cloning is not forbidden in principle. Its availability must be
constructed or warranted for the admitted source class.

## 3. Finite known randomized commands need no hidden-state restoration

There is a distinct exact route when intervention trials are allowed. Consider
an arbitrary hidden-state physical process, initialized from the same full law
each run. At stages i=0,...,m-1, observe report history h_i and draw an applied
command a_i from a KNOWN kernel beta_i(.|h_i), using independent apparatus
randomness. The hidden physical transition and sensing law given the actual
command are otherwise arbitrary and unchanged across policies.

For a target policy pi_i(.|h_i) absolutely continuous with respect to beta_i,
define on the actual jointly recorded reports and commands

    L_pi = product_i [ d pi_i(.|h_i)/d beta_i(.|h_i) ](a_i).

Then, for every bounded transcript consequence f,

    E_pi f = E_beta[f L_pi].                                  (1)

Proof: write the full hidden trajectory law as initial law times alternating
sensor/physical kernels and action kernels. Changing policy replaces only the
known action factors. Their likelihood ratio depends on recorded history and
commands, so it survives integration over every hidden state. This remains true
for feedback, hidden memory and arbitrary non-Markovian visible dynamics.
If physical action selection also depends on hidden information, the known
factorization fails; merely estimating beta from visible frequencies does not
repair that confounding.

For L commands with uniform beta_i, a deterministic target has L_pi equal to
L^m on matching action sequences and zero otherwise. E_beta L_pi^2=L^m.
Thus ordinary importance sampling has variance at most L^m/N for |f|<=1,
and a median-of-means bound uses
N=O(L^m epsilon^-2 log(1/delta)) independent reference trials for a fixed
query. If beta_i(a|h)>=b, the second moment is at most b^-m. This is a sufficient
and sometimes attained importance-sampling cost, not a universal lower bound.

The finite operation has a real acquisition contract: m commanded actions per
trial, their amplitude/duration calibration, a genuinely independent preparation
for each trial or separately justified dependence control, synchronized reports,
randomization probabilities and the desired controller's actual information
interface. If L is a power of two, exactly log2 L independent fair bits suffice
per action. Other rational probabilities can use a finite bit source with a
specified approximation/overflow treatment. No infinite-precision Brownian
command is needed for (1).

These trials are controlled physical experiments, not more passive samples.
The estimator is standard randomized-policy importance sampling. It can be
much less efficient than executing a selected controller directly or acquiring
a structurally justified reduced model. Its role is to provide an honest
constructive substitute for unavailable microscopic branching, with its actual
cost exposed.

## 4. Scientific choice indicated by the comparison

A three-future acquisition could reveal multiplication of hidden predictive
functions and enable a reusable physical realization; a recorded-noise or
randomized-command acquisition directly identifies the controlled consequence
family without that realization. The first targets a compact explanatory model;
the second targets broad causal coverage at potentially exponential reuse cost.
They are different physical interfaces. Neither follows from equilibrium,
passive reversibility, small stored memory, or a fitted visible record alone.
