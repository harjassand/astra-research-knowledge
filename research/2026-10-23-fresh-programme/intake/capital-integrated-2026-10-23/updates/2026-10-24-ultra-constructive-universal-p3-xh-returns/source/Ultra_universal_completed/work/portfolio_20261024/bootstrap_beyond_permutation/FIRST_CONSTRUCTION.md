# Owned first construction: acquire an experiment that resets behaviour

24 October 2026. Saved before support-agent exposure. This is a new question and representation, independent of the quadratic-permutation representation. The earlier proof and quotient supplement remain unchanged and retain their distinct execution scopes.

## Limitation and representation

Learning an unknown controlled system repeatedly requires a reproducible preparation. An external reset may be expensive, while the raw available controls do not include any reset word. Can measured input/output behaviour be used to *construct a cheaper reset intervention*, enabling subsequent system learning under repeatable preparation without a hidden-state model or latent reset oracle?

Represent the object by **controlled experiment probabilities and their finite-dimensional continuation space**, not by a supplied latent state. A physical run starts from a costly reproducible initializer rho0; a raw control word w is executed; a finite visible test t returns a bounded outcome. The scalar probability h(wt) is acquired by repeated actual executions. The learner may concatenate words, randomize among them and observe outcomes; it is not given hidden transition matrices, state labels, coordinates, reset controls or an equilibrium sampler. Initializer, full word durations, each readout, randomness, fitting, verification and runtime are paid.

First exact mathematical contract: a finite-dimensional controlled linear observable process with a supplied dimension bound m and exact scalar experiment-probability oracle, plus unit-cost symbolic concatenation only as notation (actual word lengths are charged). Exact probability access is an idealized interface; finite-sample/noisy acquisition needs its own robust theorem. A finite known test/preparation length budget is supplied; finding a sufficiently conditioned span within it is acquisition work, and may fail. A small representation is not assumed free.

## Independent construction

Let B=(b1,...,br) be acquired preparation words and T=(t1,...,tr) acquired test words. Let H_ij=h(bi tj) be nonsingular. For every raw control word u, let H_u,ij=h(bi u tj). The matrix

    M_u = H^{-1} H_u

acts on the row of test probabilities x(w)=(h(w t1),...,h(w tr)) by x(wu)=x(w)M_u, since H_u=H M_u, provided B,T span the process's reachable/observable rank. This is observable-operator system identification; its ingredients are established. Span completeness must be justified from a correct rank bound or a finite distinguishing-test contract; an invertible finite H alone does not prove it.

The proposed acquired operation is a finite randomized word library W. Choose nonnegative lambda_u summing to one such that

    S=sum_(u in W) lambda_u M_u

has rank one and preserves the normalization functional c (x c=1 for every physical predictive state). Equivalently S=c v for a row v with v c=1. Executing one freshly selected actual word u has predictive expectation xS=v for *every* reachable normalized x, so it is a reset of all future visible behaviour. The hidden state need not be reset or even identifiable; its surviving differences are experimentally irrelevant to the legal continuation interface.

For a specified desired v, feasibility and minimum average actuation cost are finite linear programs. If any such stochastic reset exists in the library hull, Caratheodory gives a finite support of at most r^2+1 words; the true affine dimension may improve this. If the target v is not fixed, S=c v is still linear in lambda and v. The physical controller needs only the sampled word, not signed state combinations. Negative observable-operator coefficients are legal internal coordinates, but lambda must be nonnegative.

This is stronger than a single deterministic reset word: if the legal raw controls permute a finite hidden orbit transitively, no word resets the hidden state, yet a suitable randomized mixture can make the same predictive output law from every initial state. Its word count/duration and random bits remain paid. Group averaging is known; the candidate claim is acquisition and certification from measured continuation operators, including cases where hidden states, group and reset mixture are not supplied.

After acquiring this reset, subsequent experiments can begin by executing it rather than the expensive external initializer. Its new initial predictive state v may differ from rho0; the next learning task must be defined from v. This is a real new preparation intervention derived from acquired behaviour, not a claim that observations alone change physical controllability. If the original task requires rho0 specifically, the LP must set v=x(rho0); otherwise the substitution is invalid.

## What must be resolved now

The central constructive questions are not answered by saying 'use a PSR'. They are: how to acquire/validate the finite continuation span without a latent feature oracle; how to build and certify a **uniform** reset from noisy scalar experiments; whether its total paid acquisition plus repeated operation costs beat repeated external initialization or strongest conventional control/system-ID methods; and which obstruction remains when no positive reset exists.

A load-bearing possible extension is a robust finite-basis certificate. If the model has an acquired *positive reachability enclosure* K containing every normalized reachable predictive state, then a fitted reset S with sup_(x in K)||xS−v||_test<=epsilon gives a true uniform behavioural preparation error. Such an enclosure is not free: it must be induced/verified by raw controlled operations, and a signed span alone is insufficient. A bad unbounded coordinate norm can make tiny fitted residuals worthless. The independent support checks will attack exactly this bridge and closest synchronization/active-learning comparators.

Exact small examples or an LP solver are not sufficient to establish a new capability. The target is an all-size operation with a defensible acquisition interface and finite-error preparation guarantee. Historical priority, physical implementation and civilisation-level consequence remain unknown.
