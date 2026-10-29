# Independent lazy-law, support and full-cost reconstruction

30 October 2026. This challenges the sample-only supplier proposed in
root_predictive/SAMPLE_TEACHER.md and T's next operation. It is separate from the
frozen VALUE-oracle review. The construction is mathematical; no new source case,
simulation, learner or solver is run here. The primary ordinary predecessor is
Liu--Moitra2411.07536v1, Section 4.1, Claim 4.1, Lemma 4.6 and Remark 4.7.
That source explicitly supplies consistent empirical trees, exact sample/PDF
access to the acquired perturbed law and lazy implementation. Those mechanisms
are not claimed new. The support restriction and KL composition must still be
paid at their actual asymmetric P/Q interface.

## 1. The probability space is a fixed teacher, not a changing estimate

Let Q be one fixed law on [O]^T. At every positive-Q prefix h, associate a
conceptual independent batch of m conditional-Q draws. Its first-token counts
define e_h. These batches are independent of all P trajectories, holdout data,
compiler feature randomness and the uniforms used to sample the acquired law.
This finite conceptual product probability space is used only in the proof.
The algorithm exposes a batch once, when its node is first needed, and memoizes
it. No exponential table or random-bit tape is materialized.

For 0<rho<=1/(10O), define the active row

    qbar_h(o)=(e_h(o)+rho)/(1+O rho).

An initially active path becomes permanently uniform after taking any edge with
zero count. Its status at a specified prefix is determined by the unique
root-to-prefix path and the cached batches there. It is not redrawn when a
different query revisits that prefix. For each fixed complete conceptual table,
these rules define ONE full-support probability law Qbar.

At an active node h, its positive Q probability has already been certified by
the path: every preceding edge had a positive observed count. A positive count
cannot occur for a zero-probability Q token under exact conditional draws. The
empty prefix starts positive. Thus a new conditional-Q batch is always queried
at a positive-Q prefix. If an arbitrary queried history includes an impossible
Q edge, its count must be zero, so evaluation switches to uniform BEFORE reaching
that unsupported prefix. No test of whether an unknown positive real is zero
is needed. This remains true when the queried history came from P, from the
global uniform component, or from an arbitrary density query.

Each newly exposed row must use fresh source draws. Reusing fragments of an
ancestor's future samples as if they were independent descendant batches is not
part of this construction. The source may supply a whole future rather than a
next token; extracting its first token is valid but all returned symbols and
service time are charged.

## 2. Uniform accuracy needs no exponential acquisition

There are fewer than O^T prefixes of length below T and at most O^(T+1) token
coordinates. A sufficient exact integer batch bound is

    m >= ceil(((T+1)ceil_log2(O)+ceil_log2(2/beta))/(2 rho^2)).

Since ceil_log2(z)>=log(z) for z>=1, ordinary coordinate Hoeffding plus a union
bound gives, with probability at least 1-beta,

    |e_h(o)-Q(o|h)|<=rho

at every conceptual positive-Q node. The batch size depends on the LOGARITHM of
the number of conceptual nodes. The number of batches actually acquired depends
only on visited nodes. These are different resources; neither is being charged
as the other. Adaptive visits are justified by the deferred independent batches.

Conditioning on the entire fixed table, the compiler still samples the exact R
law using separate token uniforms. Its feature draws are not the empirical
batches which defined R. The accepted VALUE theorem may therefore be applied
conditionally to that fixed R. Its success bound can then be averaged over the
table's good event. Conditioning on good table accuracy does not introduce a
new independence premise for P or for the compiler's independent uniforms.

## 3. Native KL transfer, including the bad paths

On the all-node event, let G be the strings which never take a zero-count edge.
Every active numerator e_h(o)+rho is at least Q(o|h), so on G,

    Qbar(x)>=Q(x)/(1+O rho)^T.

Under Q, the first zero-count transition has conditional mass at most O rho at
any active node. Union over the T possible first-loss times gives

    Q(G^c)<=T O rho.

For R=(1-alpha)Qbar+alpha Uniform with 0<alpha<=1/4, put
B0=T log O+log(1/alpha). If d=D(P||Q)<infinity, Pinsker gives
P(G^c)<=TO rho+sqrt(d/2). Exactly,

    D(P||R)=d+E_P log(Q/R).

The extra log ratio is at most TO rho+2alpha on G and at most B0 on all strings,
because Q<=1 and R>=alpha O^(-T). Hence

    D(P||R)<=d+TO rho+2alpha+(TO rho+sqrt(d/2))B0.

No negative KL contribution is discarded in this derivation. The last expression
is a deterministic bound for every table on its good event. It does not assert
uniform conditional closeness to P, or closeness of Qbar after a zero-count edge.
Those are not prerequisites of the accepted asymmetric compiler.

If d is infinite, this transfer is not used. Algorithms and candidate laws must
nevertheless be defined on that input; they may have a vacuous guarantee.

## 4. Exact acquired values do not estimate unknown tiny Q probabilities

Write rho=p/q as a positive rational. Every active row has the common integer
denominator m(q+Op), with numerator k_o q+mp. Each row is a rational probability
vector. At an inactive prefix its row is exactly uniform. For a prefix h of
length t, Qbar(h) is the product of its active-row factors followed, if necessary,
by a uniform tail. Its rational bit length is bounded by

    O(T[log m+bits(rho)+log O]).

The global mixture prefix probability is

    R(h)=(1-alpha)Qbar(h)+alpha O^(-t),

and the next-token row is exactly R(ho)/R(h). Both are exact rational arithmetic
on the acquired law. Even an arbitrarily precise requested interval for R does
not require additional source draws to estimate an unknown Q probability. It
requires only outward rounding of that exact rational result. Its time is
polynomial in the displayed bit bound and the requested number of rounding bits.

The teacher is not held in the returned model. R is a compilation-time service;
after the finite autoregressive candidate is frozen, its output program stores
only the finite arrays and deterministic inference rule from the accepted
compiler. The conceptual unvisited tree is not a secret post-compilation oracle.

## 5. Full original-Q draw, memory and random-bit bills

Let B be a deterministic cap on the accepted compiler's R row/value/conditional-
future queries, with every full-future request counted. A query can expose at
most T previously unvisited active nodes. Thus the total number of acquired
empirical rows is at most TB and the total number of original conditional-Q
future draws is at most mTB. If the interface returns full futures, returned
symbol count is at most mT^2B. Its actual source service cost is additional;
conditional reset is not a free physical operation.

The exposed counts need O(TB O log(m+1)) bits; prefix labels can be stored in a
trie with O(T^2B log O) conservative overhead. Exact rational cache arithmetic
has polynomial bit length in T, O, log m, bits(rho), bits(alpha) and the requested
precision. Repeated value queries at higher precision reuse rows and incur no
new statistical estimation cost. This is a whole-cycle bound, not a unit-cost
probability-value oracle supplied by assumption.

Exact rational categorical sampling can use uniform integer tickets and rejection
from a power-of-two range. Its acceptance is at least one half, so expected bit
work is polynomial in the rational denominator bit length. A finite number of
trials with a separate union budget yields the stated high-probability work cap.
The original Q source's own bit/physical work is not inferred from this argument.

## 6. Bad-candidate completion and law identity in selection

The fixed-tau compiler can be run without knowing d, using its synthetic
x^(-4096) promise only for analysis. All acquisition and geometry loops must have
their known work cap and an explicit uniform fallback. On an invalid-rank or
unresolved geometry input they return an actual law, not an invalid object.
Finite feature polytopes remain feasible through their uniform coefficient
vector regardless of the teacher-quality event. Token rows are normalized
nonnegative rationals; clamping actual signed marginals gives positive rational
output rows even if no negative-mass theorem applies to that candidate.

There is also a uniform lower bound, so a bad candidate does not conceal an
unbounded child division. For cached probability rows q_i and |alpha_i|<=C,

    sum_o |sum_i alpha_i q_i(o)| <= sum_i |alpha_i| <= SC.

Therefore its clamp denominator is at most SC+Ob and EVERY actual token has
probability at least b/(SC+Ob). Raw-reference coefficients are at most
C(SC+Ob)/b, still a fixed polynomial without an accuracy promise. Log/LP/FW
bit caps can use that larger bound. Equivalently the implementation may
deterministically fall back if its stronger good-event pi>=a check fails.
Neither option changes the good candidate's theorem.

The returned convex-inference procedure must be **deterministic**, with rational
LP tie-breaking and slack stopping rules. For example, interval first-order gaps
can use a stop threshold and a strictly smaller step threshold, so no equality
of a transcendental log needs to be decided. A fixed work cap and deterministic
feasible fallback also define the rule on every history. No cross-query solver
warm-start state or new random convex choices may silently change a candidate's
point probabilities. Then its pathwise rational product H(x), its sampler and
its Yatracos comparison all refer to exactly the same finite law.

This explicit law identity defeats the strongest possible implementation
objection to teacher-free model selection. It is a construction requirement,
not a claim about the existing floating T8 diagnostic. No new installed-library
or source execution is inferred.

### An explicit polynomial-bit rule across the whole horizon

This deterministic completion can be made literal without a growing algebraic
conditioning assumption. At EVERY projection start afresh at the known uniform
feasible coefficient vector. Let xi be its desired first-order tolerance. The
feature polytope lies in [-C,C]^S, has fixed rational cached constraints and
diameter at most 2C sqrt(S). Its objective Hessian operator norm is at most a
known polynomial, for example S^3/tau under the declared positive feature floor.
Take the rational segment-curvature upper bound

    Mcurv=1+4C^2 S^4/tau.

At an iterate, compute the log-gradient to componentwise error at most
xi/(8SC), rounding on a predetermined rational grid. Warranted log intervals
are evaluated at fixed precision and deterministically rounded; equality with
an irrational grid boundary need not be decided. An exact rational LP with
fixed lexicographic ties supplies a VERTEX v minimizing that rounded gradient.
The directional-gap error, uniformly for all feasible v, is at most xi/4.

If its rounded gap is at most 3xi/4, stop: the true full FW gap is at most xi.
Otherwise the true directional gap is at least xi/2. Use the FIXED rational step
eta=xi/(2Mcurv), rather than a high-precision gap-dependent step. Smoothness gives
objective decrease at least xi^2/(8Mcurv). The objective range is polynomially
bounded by the clipped-log bound, including the larger bad-reference bound
above. Thus a known fixed polynomial iteration count suffices independently of
the actual accuracy of the candidate.

All LP vertices have a fixed polynomial bit bound from the cached rational
constraint matrix (Cramer's rule after clearing denominators). The rounded
gradient only chooses among vertices; it cannot enlarge that vertex bit bound.
After I iterations, the exact convex-combination coefficient vector has

    O(I[vertex_bits+bits(eta)]+S)

conservative rational bit length. This bound is independent of the parent's
algebraic history. The parent vector enters only the reference-gradient
calculation and is then replaced by this newly initialized fixed-cap solve.
Consequently iterating through T tokens does not compose a bit-polynomial's
degree T times. Exact point likelihoods and rational categorical sampling have
a genuine polynomial bit port across the entire horizon. This is ordinary
finite convex arithmetic, not a new optimization or learning principle.

## 7. Failed objections and surviving scope

An exponentially large conceptual tree is not an exponentially large execution:
only its accuracy-union logarithm and visited empirical nodes are used. Adaptive
visits do not create a fresh teacher on each call because rows are fixed once.
Uniformly smoothing into an impossible original-Q prefix would be invalid; the
absorbing uniform rule prevents that query. A global uniform R component does
not undo support safety because R evaluation first traces the same support-safe
Qbar path. Tiny original Q values are not being estimated at exponential absolute
accuracy; exact acquired rational R values replace that task. Finally, candidate
selection uses fresh P holdout and the already frozen finite laws, so it neither
queries conditional P nor identifies a good candidate by its unknown KL value.

The operation still assumes a fixed Q and independent conditional sampling at
chosen positive-Q prefixes. It is not passive teacher data, an uncontrolled
language-model API, a physical reset device or efficient realization of a target
hidden state. Formal powers and the resulting misspecification modulus remain
astronomical and weak. The ordinary empirical-tree and finite-family selection
machinery receive full credit; historical priority and practical advantage are
not established here.
