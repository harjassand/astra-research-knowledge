# Confidence amplification gives an expected-runtime checkpoint guarantee

26 October 2026. Root consequence of
AFFINE_CHECKPOINT_BOOTSTRAP_FIRST_CONSTRUCTION.md. Independent whole
reconstruction pending. This is a standard tail-amplification argument,
not a new comparator oracle, observation, source experiment or novelty claim.

## 1. Use the actual all-branch cap

The checkpoint learner takes an error allowance epsilon. Its stated caps
and ideal-run coupling give, for the TRUE promised quadratic permutation Q,
an event E_epsilon with

    Pr(E_epsilon)>=1-epsilon,
    correct completion on E_epsilon,
    W<=P(n,log(1/epsilon)) 2^{g(Q)} on E_epsilon.       (1)

Here W is total bit/known-code/source-comparison work, and P is a fixed
polynomial that includes the source's R,M,S, collections, interpolation and
linear algebra. One can increase P to absorb all constant factors and
ceilings. The true checkpoint-gap parameter g(Q) is NOT supplied.

On EVERY branch, including erroneous learned prefixes, the same literal
algorithm has

    W<=P(n,log(1/epsilon)) 2^n.                        (2)

Indeed each proposal budget is2^{t-tau}S<=2^n S, every collection and
majority is capped, there are polynomially many requests, and all live
matrices and ANF evaluations have polynomial dimension. A detected invalid
dimension, empty filter, failed collection or exhausted cap returns UNKNOWN.
An undetected incorrect acquired model can still return a wrong answer;
the argument does not relabel such a branch as a certificate.

## 2. A wrapper that needs no knowledge of g

For requested failure allowance0<delta<1, execute that SAME learner at

    epsilon=delta 2^{-n},

splitting epsilon across the source's three error budgets, e.g. epsilon/3
each. This rational allowance is constructed by an n-bit denominator
shift; its representation and arithmetic costs are polynomial. Then

    log(1/epsilon)=n log2+log(1/delta).

Let P_*=P(n,n log2+log(1/delta)), enlarged if needed for the wrapper's own
arithmetic. The event in(1) still gives actual correct completion with
probability at least1-delta2^{-n}, hence at least1-delta. Crucially (2)
gives an expectation bound without conditioning away the bad branch:

    E[W]
      =E[W 1_E]+E[W 1_{E^c}]
      <=P_*2^{g(Q)} +delta2^{-n} P_*2^n
      =P_*[2^{g(Q)}+delta].                           (3)

The same reasoning applies separately to paid fair bits and known-code
evaluations using their literal all-branch bounds. Source comparisons are
already polynomial in n and log(1/epsilon), so they remain polynomial.
Storage remains polynomial on every branch. At g<=3, this yields a
bounded-error polynomial expected-work acquisition procedure on the full
affinely hidden block family, with the acquired inverse/sampler thereafter
costing polynomial work times2^g per operation on the correct branch.

No invocation of g, checkpoint catalogue, hidden block labels, inverse
oracle or new source values is added by the wrapper. The stronger
confidence is paid through more independent correction trials, larger
finite collection/proposal caps, comparisons and random bits.

## 3. What this does and does not improve

The original fixed-confidence theorem had only a simultaneous good-event
FPT work bound; its complement could contribute epsilon2^n to expectation.
The explicit wrapper suppresses exactly that contribution. It gives a
BOUNDED-ERROR expected-runtime guarantee. It is not a Las Vegas algorithm,
an all-branch FPT bound, or an unconditional guarantee outside the promised
quadratic-permutation/comparator/native-bits interface. The worst-case
runtime remains finite exponential, and an external smaller resource cap
can still force UNKNOWN even on otherwise correct tapes.

The same-information retaining or affine-flag method can adopt the
checkpoint compiler AND this wrapper. No algorithmic lower bound or
exclusive advantage is inferred. The earlier failed scalar-economy claims
and absent historical guards for the separate six-source experiment remain
unchanged. This is a stronger complexity consequence of the new acquired
operation, with its actual confidence resources paid.
