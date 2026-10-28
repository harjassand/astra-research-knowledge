# Scoped review: finite-transcript support and zero-count confidence

28 October 2026. This review covers only the new support obstruction, its
A_e/B_e binary-receiver application, and the zero-success statistical rule
in `POSITIVE_RESIDUAL_INTERFACE.md`. It does not reopen the scalar compiler
reviews or audit the proposed LCU implementation and gate accounting.

Reviewed source SHA256:
`42aed699d6dd5c9c8a4d7ba52f3c834592396fedb6ff8d7598741b9547c3082e`.
The A_e/B_e definition was read from `THEORY.md` at SHA256
`b28b016d2fc6ac85d2a1ed7abc9c4cf984c9f2d3edcef35ecacde0d580f53818`.

## Finding

The support theorem and the binary-receiver application are valid. The
zero-success rule is a valid frequentist false-certificate bound under its
fixed-operation independent-trial contract. It is not a posterior guarantee
conditional on acceptance. Mutual absolute continuity is more than the
support proof needs: the direction P1 restricted to each finite transcript
is absolutely continuous with respect to P0 suffices.

## 1. Precise stopping formulation and proof

Fix one algorithm, with the same source-independent random seed U under both
sources. Let F_n contain U, the first n query choices and their observations;
queries are chosen measurably from the previous transcript. Let T be a
stopping time, finite almost surely under both sources, and Z>=0 an
F_T-measurable output. Assume P1|F_n << P0|F_n for every finite n.

If E0 Z=0, nonnegativity implies P0(Z>0)=0. For positive integers n,k,

    A_nk={T<=n, Z>1/k}

belongs to F_n and has P0 probability zero. Absolute continuity gives
P1(A_nk)=0. The union over n,k is {T<infinity,Z>0}. Almost-sure finiteness
under P1 therefore implies Z=0 P1-almost surely, contradicting E1 Z>0.

No finite expectation of T, deterministic sample cap, bounded output,
uniform integrability or uniform likelihood-ratio bound is needed. The
algorithm may have an arbitrarily long finite run. The expectation can be
understood in the extended nonnegative sense. The statement is about one
common observation-only algorithm, not a procedure supplied with the source
label. Declaring a value after an infinite transcript is outside its scope.

## 2. Adaptive arbitrary-length binary words satisfy the premise

For the declared 0<e<=1/2,

    A_e=[[1-e,e],[e,1-e]], B_e=(1-e)I, b=e1, Tmodel=1-e.

Both are positive contractions. Their residuals are

    (A_e-(1-e)I)b=e e2,   (B_e-(1-e)I)b=0,

so their squared norms are e² and zero. Their finite-length responses are

    f_A(k)=[1+(1-2e)^k]/2, f_B(k)=(1-e)^k,

with the empty-word response treated as one. The receiver's Bernoulli
probabilities q(k)=1/4+f(k)/2 lie in [1/4,3/4] under both sources. The same
bounds hold for each binary outcome's probability.

Conditional on U and any fixed finite outcome history, the algorithm chooses
the same next finite word under both sources. Each one-step likelihood ratio
then lies between 1/3 and 3. The joint likelihood ratio of n observations
lies between 3^-n and 3^n, including adaptive query choices. Integration over
the common random seed preserves mutual absolute continuity. No upper bound
on the chosen finite word lengths is required. A finite number of finite
words also uses a finite total number of primitive operations on that run,
although its expectation can be unbounded.

Apply the theorem with P0 the B_e receiver and P1 the A_e receiver. This
rules out any almost-surely terminating nonnegative unbiased residual
estimator with respective expectations 0 and e², and any exact Bernoulli
residual flag with probability zero versus a positive probability. For the
LCU normalization in the source note, that positive probability is
 e²/(2-e)² when x=1. Its exact value is not needed for the impossibility.

## 3. The zero-success statement is a different statistical claim

Suppose a fixed, correctly normalized positive detector has iid Bernoulli
success probability p=||D_i x||²/C², with known C>0. For fixed N and
0<delta<1,

    P_p(no successes)=(1-p)^N<=exp(-Np).

Therefore the procedure that reports

    ||D_i x||² <= C² log(1/delta)/N

only after zero successes has false-certificate probability at most delta.
The exact binomial upper endpoint C²(1-delta^(1/N)) is slightly tighter;
the displayed logarithmic bound is conservative. If C=0, the residual is
algebraically zero and the ratio p is unnecessary.

The quantifier is

    P_p(report a false bound) <= delta,

not P_p(bound true | a certificate was reported)>=1-delta. For a fixed p
that exceeds the bound, every zero-success certificate is false conditional
on its being emitted; emission itself is a rare event. Calling it a
confidence certificate is standard, but the source note's phrase
"conditional certificate" should be read in this operational sense, not as
conditional-on-acceptance reliability.

A fixed target selected from earlier data is also valid if these are fresh
conditional iid detector trials. Multiple independently selected targets
need an appropriate joint failure allocation. Searching retrospectively
across many disjoint zero-success batches without such correction is not
covered. For completeness, one *all-zero prefix* monitored before the first
success retains the same error bound even with a stopping choice of N:
the false-report event implies a zero prefix past the deterministic crossing
n>log(1/delta)/p. This does not justify resetting the counter after successes
and searching indefinitely for a long all-zero run.

Thus the support obstruction does not preclude ordinary confidence intervals
or high-confidence approximate detection. Such procedures intentionally
allow a nonzero false-output probability, whereas the exact positive flag
must have probability exactly zero at the zero-residual source.

## 4. Nontrivial limitations and weakened-hypothesis counterexamples

### Same marginal support is insufficient

Let each source return two individually fair bits. Under P0, sample U fair
and return (U,U). Under P1 return (U,1-U). Every individual observation has
the same Bernoulli(1/2) marginal under both sources, but the two-observation
laws have disjoint supports. The finite procedure Z=1{Y1!=Y2} is nonnegative
with E0Z=0 and E1Z=1. The theorem needs finite **joint conditional transcript**
absolute continuity; matching supports of isolated marginals is insufficient.
The specified independent binary word receiver avoids this counterexample.

### The receiver restriction is material even for the same A_e/B_e pair

Fix known rational e and choose a long finite word for which the two response values
differ by g>0. Suppose instead of binary samples the receiver returns a
sound bounded-error scalar report with radius eta<g/2. The two possible
report supports are disjoint. A single long-word query identifies this
known pair exactly, after which private randomness can generate a Bernoulli
flag of probability 0 or e²/(2-e)² as appropriate. Thus an exact classical
flag can exist for a stronger or different scalar receiver. This violates
the support premise, not the theorem. For a concrete choice, e=1/4, k=20
and eta=1/100 give f_A>1/2 and f_B<1/100. The report supports are disjoint;
a threshold of 1/4 identifies the source, and the positive target flag has
known probability 1/49.

The binary example establishes that there is no universal ordinary
postprocessing reduction covering that receiver class. It does not prove
that every scalar receiver, or every restricted known source family, lacks
such a reduction. The existing deterministic interval interface and this
statistical receiver model must not be silently conflated.

### Infinite paths and signed outputs are genuine escape routes

For two distinct interior Bernoulli probabilities p0,p1, every finite iid
transcript law is equivalent. Nevertheless the infinite empirical-frequency
limit equals p0 or p1 almost surely, so its tail event distinguishes sources
exactly. It is not a finite-time output.

Nonnegativity is also essential. At k=2 in the declared pair,
q_A(2)-q_B(2)=e²/2. One binary observation Y gives the signed estimator

    Z=2[Y-q_B(2)],

with expectation zero under B_e and e² under A_e. Its negative outcomes are
precisely what the positive-estimator theorem excludes.

## 5. Primary-literature consistency

Nacu and Peres, *Fast simulation of new coins from old*, Annals of Applied
Probability 15 (2005), 93–115, define an exact coin simulation using an
almost-surely finite stopping time. Their introductory statement of the
Keane–O'Brien condition and their finite-prefix polynomial formulation are
consistent with the interior-support obstruction used here:

https://arxiv.org/pdf/math/0309222

Jacob and Thiéry, *On nonnegative unbiased estimators*, Annals of Statistics
43 (2015), 769–784, study the stronger generic sign-constrained estimator
problem and emphasize the importance of additional model-specific premises:

https://arxiv.org/pdf/1309.6473

The reviewed proof is a direct finite-transcript support argument. It does
not claim their full theorems as interchangeable with this adaptive-word
instrument, or claim a new general Bernoulli-factory impossibility result.

## Review scope

Completed: the ordinary measure-theoretic proof with explicit stopping
conditions, the adaptive binary-word absolute-continuity application, the
residual values, the zero-count frequentist interpretation, and the above
counterexamples. No new simulation is needed for these exact arguments.
The LCU implementation, its precise coherent errors and gate costs, and a
physical realization of an exact null detector are outside this review.
