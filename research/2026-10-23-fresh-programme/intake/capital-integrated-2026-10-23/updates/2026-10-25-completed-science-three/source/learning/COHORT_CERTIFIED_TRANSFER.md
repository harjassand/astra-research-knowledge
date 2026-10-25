# A learned function family from incomplete, expiring sources

New operation: certify a whole reusable function family by sequential tests
of actually acquired basis programs, while each real basis source is still
available. The sources may then expire. Their true functions need not be
polynomials. A paid native local-correction experiment acquires new near-family
tasks robustly, instead of trusting fragile raw anchor values.

The core certificate is a common small error region for ALL linear
combinations of the actual source functions and their learned programs. It
does not require a supplied true feature envelope or whole-source recovery.
It does not assert that arbitrary future tasks belong to this learned family.
No new source, callback, fixture or benchmark is run in this note.

## 1. Chosen program language and genuinely acquired programs

Use native X=F_p^n, exact field outputs and a fixed source during each episode.
Choose a bounded polynomial program language P_(<=D), with p>2(D+1). D is
a compiler choice, not a claim that real sources are polynomials. Its native
monomial dimension is M=binom(n+D,D); construction/evaluation/field arithmetic
and any known-feature catalogue search are paid.

Acquire candidate programs G_i through actual source observations and a
declared fitter/compiler. The earlier retained-composition and graph-family
fitters are possible proposal mechanisms, but their useful coverage is not
granted. Each G_i must be fixed before its own fresh validation samples.
Select programs linearly independent as NATIVE polynomials, using paid
known-coefficient or actual known-program evaluation rank tests. Stop after
r independent programs; the policy caps r and all computation. Let f_i be
the actual corresponding source functions. We never acquire their whole
function tables or assume f_i in P_(<=D). Selection may depend on past
episodes, including their validation outcomes.

After selecting G_i, and before source f_i expires, perform q new uniform
native tests of G_i against f_i. Abort this cohort certificate on the first
mismatch. A failed source cannot be silently dropped followed by an
unbudgeted restart. Repeated cohort attempts require their own summable
confidence allocations, and all failed fits/tests remain paid.

## 2. One cohort certificate rather than unobserved global realizability

For each selected pair let

    e_i = Pr_x[f_i(x)!=G_i(x)],  x uniform in X.

Choose eta>0 and q>=ln(1/delta)/eta, using the SAME q per selected source.
For fixed candidates, conditional probability of q matching is (1-e_i)^q.
This remains true with adaptive candidates because their own samples are
fresh. Let C_i be the event that all guards through i match, and define

    Z_i = 1_(C_i) exp(q sum_(j<=i) e_j).

Condition on the whole history just before source i's guards. Then

    E[Z_i | history] <= Z_(i-1) exp(q e_i)(1-e_i)^q
                     <= Z_(i-1).

Known-program acquisition between guard blocks does not change the previous
product. Thus this is a nonnegative supermartingale; bounded cohort stopping
is allowed. Markov/optional stopping gives

    Pr[C_r AND sum_i e_i>eta] <= exp(-q eta) <= delta.       (1)

No individual e_i is estimated or silently replaced by eta/r. The validation
cost is r q actual source values, plus actual program evaluation/randomness.
This is an aggregate zero-failure test, not a conditional-on-return guarantee
without a lower bound on the return probability.

Let E=union_i{x:f_i(x)!=G_i(x)}. On the good certificate event nu(E)<=eta.
For EVERY c in F_p^r, including coefficients chosen after seeing the whole
history,

    f_c=sum_i c_i f_i,  P_c=sum_i c_i G_i

agree outside the SAME E. This gives uniform family-wide disagreement
<=eta without enumerating or separately testing p^r tasks. The actual basis
source functions, not their full descriptions, define the family.

The known polynomial family has minimum relative distance
rho>=1-D/p>1/2. If eta<rho and the G_i are independent, the actual f_i are
also independent: a nonzero coefficient relation among f_i would make its
nonzero P_c supported only on E, contradicting the polynomial distance.
Thus, within certificate confidence, a real r-dimensional actual function
family has been identified through partial observations, despite possible
nonpolynomial exceptional behavior. This certifies the selected family's
dimension; it does not certify global rank exhaustion of unseen tasks.

### Tolerant aggregate certificate with nontrivial return power

The zero-failure version can return infrequently when basis errors are real.
There is a tolerant alternative with the SAME order r/eta validation cost.
Take exactly q fresh tests per selected source, retain the total mismatch
count S, and let V=q sum_i e_i be the predictable total mean. For every real
lambda the process

    exp(lambda S - (exp(lambda)-1)V)

is a nonnegative supermartingale, because
1+e_i(exp(lambda)-1)<=exp(e_i(exp(lambda)-1)) for each fresh test.
Sources/candidates can still be chosen using all prior outcomes. Accept the
cohort when S<=q eta/2. With lambda=-ln2, on V>q eta and S<=q eta/2 the
exponent is at least (1-ln2)q eta/2>=q eta/8. Thus

    Pr[cohort accepted AND sum_i e_i>eta] <= exp(-q eta/8).

With lambda=ln2, on V<=q eta/4 and S>q eta/2 the exponent is at least
(ln2/2-1/4)q eta>=q eta/12. Hence

    Pr[cohort rejected AND sum_i e_i<=eta/4] <= exp(-q eta/12).

For q>= (12/eta)ln(1/min(delta,zeta_0)), the bad-cohort certificate probability
is <=delta, and a cohort whose total actual basis risk is <=eta/4 returns
except with probability zeta_0. These are joint-event bounds; if that risk
condition itself is random, do not substitute a conditional-on-selection
power claim without accounting for its failure probability.

The protocol may abort once its accumulated count exceeds q eta/2; it does
not drop a mismatching source and reuse the old confidence allocation. This
supplies genuine return power under a stated approximation condition while
preserving source expiration and full cost accounting. The remaining
transfer sections can use either valid cohort certificate.

## 3. A revealing coverage failure of raw anchor transfer

Average closeness to a learned family does not make a fixed anchor profile
robust. With one constant basis G_1=f_1=1, let a future f equal1 everywhere
except at the chosen anchor, where f=0. It is only 1/|X| away from the learned
family, but raw anchor fitting returns the zero function and has risk
1-1/|X|. The fresh guard rejects it; its coverage nevertheless collapses.
This is a counterexample, not a new favorable benchmark. We therefore need
an actual robustness operation before making a near-family transfer claim.

## 4. Native correction at a requested point, with all calls paid

Suppose a new actual source f has some (unknown) c satisfying

    Pr[f!=f_c] <= tau.

By the cohort certificate, Pr[f!=P_c]<=beta=eta+tau. This is a conditional
coverage property, not an oracle telling the learner c or tau. Fix

    beta <= 1/[8(D+1)].

At ANY requested native x, choose v uniformly from F_p^n and query

    f(x+j v),  j=1,...,D+1.

These are D+1 PAID native source values. Each queried point is uniform,
because j is nonzero mod p. Regardless of dependence within the line,
probability any point is in the error set is at most (D+1)beta<=1/8. If all
are good, degree-D interpolation in j, evaluated at j=0, returns P_c(x).
The D+1 interpolation weights can be computed once with exact paid field
arithmetic; no derivative, feature inverse, extension-field query, noiseless
reset or latent task sampler is provided.

Repeat for an odd number L of fresh independent directions and return the
most frequent field value. At least 7/8 of line estimates are correct in
expectation, with independent direction tapes, so majority failure is at most

    exp(-9L/32).

The true source f is a fixed function; this is not an assumption of fresh
readout noise or an attempt to erase persistent source corruption.

## 5. Acquire a near-family task after old source expiration

From the known G_i programs, compute r native points z_1,...,z_r whose
r-by-r evaluation matrix A is nonsingular. This is an actual known-feature
rank search/interpolation calculation, with caps and explicit cost; it is
not an evaluator frame or a hidden-coordinate oracle. In particular the
points may be chosen AFTER the old sources have expired, since only their
known G_i programs are evaluated. Their actual old f_i values are not needed.

Apply the preceding correction procedure to the CURRENT source f at each
z_l. For

    L odd and L >= (32/9) ln(r/zeta),

all r corrected values equal A c with probability at least1-zeta. Solve
for c and compile P_c=sum c_i G_i. The source cost is at most

    r(D+1)L native values,

plus sampling, coordinate edits, field interpolation, A construction/solve
and compiled-program evaluation. Duplicated same-target points may be cached;
the bound does not grant them free before they are observed. The new program
has risk at most beta on this successful near-family branch. If two different
polynomials were within beta of f, their mutual distance would be <=2beta,
contradicting rho; the corrected polynomial is therefore unambiguous.

This acquires coefficients in the learned r-dimensional family. Generic
degree-D reconstruction would require its M-dimensional fitting procedure;
the earlier acquisition of G_i and its real validation/computation must be
included before calling the r-versus-M change an amortized benefit. No
exclusive advantage over a competent common-evidence code/multitask learner
is asserted.

## 6. Open-world soundness and actual coverage power

Outside the near-family condition the correction routine can return an
incorrect candidate; do not mark it correct merely because the line votes
agree. Apply a NEW tolerant native guard against the real source. For a
chosen risk epsilon, accept only when q' independent mismatches have empirical
rate <=epsilon/2. If actual risk>epsilon, Chernoff bounds false acceptance by
exp(-q' epsilon/8). If risk<=epsilon/4, rejection probability is at most
exp(-q' epsilon/12). For example

    q' >= (12/epsilon) ln(1/min(delta',zeta'))

controls these by delta',zeta'. Every new source/attempt gets its own
conditional budget. Accuracy of accepted programs thus needs NO
near-family, polynomial-source or common-rank assumption. Coverage has a
real sufficient condition: beta<=min(epsilon/4,1/[8(D+1)]) implies return
probability at least1-zeta-zeta' on a good cohort certificate. There is no
such return guarantee for arbitrary unrelated tasks.

Long interactive reuse still needs the earlier finite-horizon, per-history
input-domination certificate, with deterministic beta_l caps in its TV
bound. Uniform risk over a function family is not certainty on every input
or a free guarantee over an unlimited adaptive lifetime.

## 7. Acquisition and boundaries kept visible

All G_i must actually be acquired. As a general fallback, if a source happens
to be beta_0-close to some degree-D polynomial with beta_0<=1/[8(D+1)],
the same native correction can be used at M known unisolvent nodes to fit
that polynomial. This costs M(D+1)L_0 source values, with L_0 chosen for
its M-node failure budget, plus full native interpolation arithmetic. It is
a conditional completeness route, not a supplied polynomial model or free
initial sampler. An acquired smaller feature catalogue can lower fitting
work; its construction/search must be counted. Sources with no suitable
program simply need not yield a certified cohort.

For a concrete sufficient cohort-completeness condition, if each selected
f_i is within eta/(4r) of its recovered polynomial and all those fits succeed,
their sum risk is <=eta/4; the tolerant cohort certificate then has the return
power just stated. Fit failures and all their source calls receive their own
budgets. This condition is not inferred before measurement or supplied as
an acquired capability; the independent tests remain the soundness gate.

Each source must last long enough for its own actual fitting and q guards.
A strict r+1-query episode generally cannot supply these arbitrary confidence
levels; the expired-task constraint theorem alone does not provide them.
After that finite episode, no old source persistence is used. Memory/code,
randomness and finite-field bit/precision costs remain additional to native
answer counts. No new observations or finite advantage experiment are claimed.

One explicit implementation bound: the total-degree Newton grid supplies M
native nodes; selecting the r learned-family pivot rows can use at most Mr
KNOWN-program evaluations and paid elimination. Precompute the D+1 line
interpolation weights in O(D^2) field work. Each line uses O(n(D+1)) native
coordinate arithmetic and O(D+1) weighted-sum work, in addition to its source
values. A^{-1} costs O(r^3) once; each target solve costs O(r^2). Uniform
directions consume rLn field draws per target, with actual fair-bit sampling
and any rejection/cap failures charged. All field values have log p bits;
bit arithmetic is additional to a field-operation model.

Parameters may be finite rationals. Replacing each natural logarithm above
by ceil(log2 of the same argument) gives a conservative integer-computable
budget; choose L to be the next odd integer. A uniform field draw can reject
b=ceil(log2 p) fair bits when their integer is >=p, with acceptance >=1/2.
Its expected bit cost is <=2b. A literal finite retry cap has its own paid
failure/UNKNOWN probability, union-bounded across all field draws. No fixed
PRNG replay is a certificate of independent randomness. The tolerant-cohort
constants use 2/3<=ln2<=3/4, obtained from the midpoint/trapezoid bounds for
the convex function 1/x on [1,2].

The retained program P_c can share the closed G_i library and store r new
coefficients. Its evaluation still costs the sum of the G_i evaluation costs
plus O(r) arithmetic, which can be expensive. Source-query reduction does
not imply scalar, derivative or total runtime improvement. The global
agreement-outside-E argument uses finite-field equality/Hamming error; a
real-valued small-L2-error version needs coefficient/conditioning control
and is not proved by this argument.

The operation removes true-H and full-old-source contracts for selective,
uniform-family approximation, and repairs near-family anchor fragility by
actual native experiments. It does not acquire a universally useful language
or prove that nature supplies related future tasks. Polynomial self-correction,
sequential risk tests and ordinary retaining/multitask learners are the
strong incumbents; their exact primary scope must be checked before making
any priority or comparative capability conclusion.

## 8. Primary comparison: primitives are established

Howard, Ramdas, McAuliffe and Sekhon's nonnegative-supermartingale framework
contains the sequential concentration machinery. I read Lemma1, its
Section6.1 optional-stopping proof and Section2.3's Chernoff application. Our
two cohort tests are elementary scalar specializations; there is no new
concentration theorem. [Primary paper](https://arxiv.org/html/1808.03204).

Gemmell and Sudan's *Highly Resilient Correctors for Polynomials* gives a
strictly stronger noise-tolerance incumbent when its larger-field condition
holds. I read Section3's random quadratic restriction, pairwise-independence
argument, reduction to univariate decoding and Theorem4. It corrects error
fractions approaching1/2 using Berlekamp-Welch and a field-size condition
depending on degree and error margin. Our D+1-line interpolation is a weaker,
explicit primitive with the stated small-corruption/field constants, not a
new self-corrector or noise-tolerance frontier.
[Author-hosted primary paper](https://people.csail.mit.edu/madhu/papers/1992/gemmell.pdf).

An equally informed learner can combine these known primitives with retained
feature fitting and the same actual source observations. The owned result is
the explicit expiring-source/common-error/near-family transfer operation and
its boundaries, not an algorithmic advantage over that adopter. No favorable
new source is manufactured to disguise the tie.
