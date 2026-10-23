# Frozen calculation contract: vanishing fixed screening

Owner: Astra PRO3. Scientific date: 2026-10-22 (Australia/Brisbane).
Written before the principal certificate calculations. These are mathematical
diagnostics and finite certificates, not empirical discovery or an application
benchmark. The closed fixed-positive-eta theorem is accepted received capital.

## Decision before calculation

Determine whether a screen that is fixed during each run, but decreases across
requested accuracies, can preserve uniform proposal-start accuracy. A complete
dimension-free bound plus an admitted adverse family is the acceptance rule.
A failed density estimate alone is not a lower bound. A lower family must have
positive pi,q, the certified forward KL budget, symmetric stochastic fixed Q,
and the actual two-factor local acceptance. All later paths must be retained.

The main expected result is a uniform finite bound obtained by summing the
original first-hit submeasures with an interpolation exponent independent of
time. Its proof, not plotted numerical agreement, determines acceptance.
Independent challenge is assigned to this particular new bound. A distinct
contributor constructs an actual adverse path and checks its probabilities.

## Principal computations frozen here

1. Implement the full finite upper certificate in logarithmic coordinates for
   K=1, alpha=1/2. Retain every term, even when the certificate is vacuous.
   Proof choices: h=0.01; a=0.95 times its admissible endpoint; R=n/(log n)^4.
   Evaluate log n in {100, 1000, 10000, 100000, 1000000}, with eta=1/2 and
   eta=min(1, lambda loglog n/log n), lambda in {0.5,1,2,4,8}.
2. Compute Lambda_* and the separately constructed path variational constant
   at (K,alpha)=(1,1/2), using 80-decimal arithmetic. Do not call either a
   proved exact critical threshold.
3. For epsilon in {0.05,0.02,0.01,0.005,0.002,0.001}, eta(epsilon)=
   min(1,d epsilon log(1/epsilon)), d in {0.25,1,4,16}, find the first
   log-time allowed by this particular finite certificate by a bracketed
   deterministic search. Report epsilon log-time, all controlling terms,
   and any infinite or failed bracket. This is an upper certificate, not
   the actual minimax time and not a claim of practical speedup.
4. Match the same forward-KL certificate against an ordinary pure-IMH
   truncation bound, including its error budget and global-step count.
   Do not compare a sufficient hybrid time to a measured IMH lower bound.

The support-growing path diagnostics are assigned separately and must preserve
their own exact selections, numerical precision, code and measured runtime.
No holdout is meaningful for a deterministic theorem or its identity checks.
These computations cannot certify a new population KL bound from samples.

## Access and resources

q is sampleable/evaluable; Q is fixed, symmetric, sampleable and target
independent. Only ratios of unnormalized positive target values are needed.
K is a supplied population bound. Screening h,R and W used in the proof are
not queries performed by the sampler. The normalized tables in finite
counterexample code are available to the verifier, not quietly supplied to the
sampler; complete table access would permit direct sampling.

One lazy hybrid step stays with probability 1/2, makes a global q proposal
with probability alpha/2, and makes a Q proposal with probability beta/2.
The local first screen uses q alone. An uncached target value is needed only
after that screen passes. Count initialization, all proposals, q evaluations,
acceptance uniforms, target evaluations and cache memory. Full caching is
allowed to both algorithms. Each run keeps eta,Q,alpha fixed.

No GPU, purchases, outreach, intervention, biological or galaxy data search,
or empirical performance claim is part of this experiment.
