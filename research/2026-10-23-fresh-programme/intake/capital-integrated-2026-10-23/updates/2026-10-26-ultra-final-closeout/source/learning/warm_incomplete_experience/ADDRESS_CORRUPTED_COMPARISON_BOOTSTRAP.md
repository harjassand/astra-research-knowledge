# Acquiring closed procedures despite fixed corrupt native addresses

26 October 2026. Owned continuation of the conditional affine-frame
bootstrap. No new source, target, simulation, fixture, or observation.
The robustness question was chosen before root supplied the direct-vote
improvement. The initial owned event-union argument allowed a corrupt mass
at most 2^(-17) while retaining the original sorting median. Root then
supplied direct511 voting and its much stronger Beta-threshold bound;
that bound is independently reconstructed below. The owner's additional
operation is the short-fibre WIN CENSUS, which avoids a contaminated-fibre
union bound and works even with inconsistent/adaptive bad comparisons.
For the initial event-union calculation, a long-fibre median label fails
with probability at most the clean quantile bound plus512epsilon, and a
short-fibre label with probability at most64epsilon. At epsilon<=2^(-17)
the seven-corner error remains below1/4. This valid but weaker calculation
is retained; it is superseded by (6), not promoted as the strongest method.

## 1. Changed observation contract, stated literally

Keep an unknown quadratic permutation Q:F_2^n->F_2^n, native chosen addresses
and actual fair bits, but do NOT assume every comparison is correct.
There is a fixed unknown set B with native uniform mass at most epsilon.
Whenever both submitted endpoints lie outside B, the answer equals the
lexicographic comparison of Q. Every comparison touching B can be arbitrary,
inconsistent with a total order, and adaptive to the full past and the
currently submitted inputs.

B and Q are fixed before the learner's fresh tapes. Allowing B to be chosen
after seeing a fresh address would defeat the argument: a small evolving
set could contain every queried point. A numerical upper bound epsilon
is a source-contract premise, not acquired by these comparisons. No
per-fibre accuracy, pointwise query-noise bound, independent noise, latent
sampler, label access, or supplied conditional frame is given.

The object to recover is the underlying Q and its closed procedures, NOT
an exact representation of arbitrary answers at corrupt endpoints. If the
actual oracle is a total order with arbitrarily reranked points in B, its
literal rank bits need not be Q's bits even outside B. That distinction
must not be erased in an after-expiry interpretation.

The difficulty is that some selected prefix fibres can be ENTIRELY bad.
A proof requiring each conditional fibre to have small corruption would
assume a stronger observation contract than the one above.

## 2. The endpoint-marginal accounting that survives conditioning

Condition the ideal analysis on a correct acquired Q prefix h_t. Its exact
witness sampler is either the global-checkpoint or the stronger conditional
affine-frame sampler. For a fresh uniformly distributed request X, sample
Z uniformly from the true prefix fibre of X. Then Z itself has the native
uniform marginal. More precisely, write

    N=2^(n-t),
    delta_y=|B intersect h_t^-1(y)|/N.

Every prefix is equally likely and

    E_y delta_y=epsilon_actual<=epsilon.                 (1)

The seven nonempty additive-cube requests used to correct an arbitrary
desired next-coordinate value each have this uniform marginal, conditional
on the history BEFORE that trial's fresh cube offsets. They need not be
independent of one another or remain uniform after intermediate vertices
and replies are revealed. The rank-dependent error envelopes below hold
for every within-trial past; averaging each envelope over its marginal
at trial start is sufficient for the seven-vertex union bound. This is
the actual reason an accurate global statement can
survive conditional preparation. It does not make any particular fibre
accurate or hide its rejection/preparation cost.

## 3. Long fibres: direct comparison majority and a sharp averaged bound

For odd K and N above a short-fibre cutoff, draw K fresh same-prefix points
Z_l and label the requested x by the majority of C(Z_l,x). For a correct
total order this is identically comparison with their sample median: the
median lies below x iff more than half the sample lies below x. No sorting
of the K points is necessary. Under corruption the direct-vote procedure
is its own explicitly defined algorithm, not a possibly inconsistent sort.

Fix a fibre y and a GOOD requested x, of clean suffix rank r in
{0,...,N-1}. Put p_x=r/N. At every fresh Z_l, conditional on the entire
past, the comparison success probability lies between

    max(0,p_x-delta_y) and min(1,p_x+delta_y).            (2)

Only a bad sampled endpoint can change a clean comparison. Arbitrary
adaptive answers there do not invalidate these conditional bounds.

Binomial stochastic domination follows by recursive fresh-uniform coupling:
a sequence of Bernoulli variables whose conditional success probabilities
are at most a has its sum dominated by Bin(K,a); use the analogous lower
domination. These uniforms are proof-only, not an extra learner oracle.
Thus lower-half ranks have error at most the majority tail at p_x+delta_y;
upper-half ranks have error at most the opposite tail at p_x-delta_y.

Represent both tails with a common median U_* of K iid Uniform[0,1]
variables. For a fixed U_*=u, the number of lower-half ranks that may err,
divided by N, is at most

    (1/2-u+delta_y)_+.

The corresponding upper-half count is at most

    (u+delta_y-1/2)_+ +1/N.

The first bound uses ceil(N(u-delta_y)) as the first possible integer rank;
the second is the monotone grid bound on ranks below N(u+delta_y).
The two positive parts sum to at most |u-1/2|+2delta_y.
Charge bad requested x by an additional delta_y and average U_*. Its
symmetric Beta((K+1)/2,(K+1)/2) law has mean1/2 and variance1/[4(K+2)].
Cauchy--Schwarz therefore gives the fibre-average bound

    e_y <= 1/(2 sqrt(K+2)) +1/N +3delta_y.              (3)

The bound holds conditional on earlier history even for adaptive corrupt
answers: domination uses the same bounds (2) for every possible past.
Averaging (3) uses (1) ONCE. In particular there is no multiplication of
epsilon by K and no density amplification by an inverse prefix mass.

## 4. Short fibres: a deterministic win census replaces sorting

For short N, obtain the entire fibre by the same paid, known-N, capped
uniform collection as in the original acquisition. The source is not
asked to enumerate its inputs. Once the complete list is available, make
ONE comparison C(z,x) against every other listed point z, recognizing
self equality locally. Label x by

    1{number of reported wins >=N/2}.                   (4)

This takes N-1 comparisons, rather than sorting the fibre. It is exact
without corruption. It requires no transitivity of the corrupted answers.
The literal implementation first checks that the N-point distinct list
contains the requested x, and returns UNKNOWN if it does not. That check
is automatic on the true-prefix branch, but is needed when a wrong learned
model has an incorrect fibre-cardinality premise; it also preserves the
N-1 comparison ceiling on every branch.

Here is its robust bound. Let b=|B intersect fibre|. For a good x, its win
count differs from its clean suffix rank r by at most b, deterministically:
every good-good comparison is right, and there are only b bad other
endpoints. A lower-half good x can therefore be mislabeled only when

    N/2-b <=r<N/2,

and an upper-half good x only when

    N/2<=r<N/2+b.

There are at most 2b such rank positions. Add at most b errors from bad
requested points. Hence, even if the actual bad answers are chosen
adversarially after the list and x are known,

    e_y <=3b/N=3delta_y,   and globally e<=3epsilon.     (5)

Using the mass of ALL contaminated short fibres instead would give an
unnecessary N epsilon loss. Census cancels that dependence by bounding
rank perturbation inside each fibre. It still pays for collecting every
short-fibre point and all comparisons in (4).

## 5. A concrete end-to-end noise allowance

Take K=511 and census for N<=64; every other N is at least128. From (3)
and (5), at every acquisition stage the uniform-request average weak-label
error is at most

    e <=1/(2 sqrt(513))+1/128+3epsilon.                 (6)

If epsilon<=1/1024, seven cube vertices have combined error below1/4.
For an elementary rational check, sqrt(513)>22, and

    7e < 7/44+7/128+21/1024
       =2639/11264 <1/4.                              (7)

No independence of the seven vertices is needed. For every desired native
x, a third additive difference of the true quadratic Q_(t+1) vanishes, so
its value is the XOR of those seven true values. Replace them with the
weak labels. Equations (6)--(7) give conditional error below1/4 for each
correction trial, for arbitrary desired x, including x in B.

Fresh random offsets and conditional preparations give that bound after
EVERY past history. Bounded-martingale Hoeffding therefore bounds R-trial
majority error by exp(-R/8); independent noise is not assumed. If the
source is a fixed deterministic corrupted order, ordinary independent-
trial Hoeffding also suffices. The martingale statement covers the more
general explicit contract from Section1.

Interpolate D_n=1+n+binom(n,2) requested values for each of the n true
coordinates. Use the same first-error coupling, short-fibre collection
caps, proposal caps, dimension guards, and UNKNOWN rules as
CONDITIONAL_AFFINE_FRAME_BOOTSTRAP.md. On true acquired prefixes the
sampler and its balance are EXACT; all corruption occurs in the observed
comparisons, already accounted for by (6).

Choose R and the three allocations delta_a,eta_1,eta_2 as in that note.
The ideal-run calculation followed by the first-error/timeout union bound
gives

    Pr[correct complete underlying Q, every cap respected]
        >=1-delta_a-eta_1-eta_2.                        (8)

This is neither recognition of the corruption promise nor confidence
conditional on a particular returned artifact. Incorrect models remain
possible within the stated allowance. Once the correct underlying Q has
been acquired, however, the closed evaluation/inverse/fibre procedures
are exact forever without any further source calls or errors from B.
This is the after-expiry capability at stake, rather than an indefinitely
callable noisy-source alias.

## 6. Paid resources and the stronger retaining baseline

Every weak label now costs at most511 comparisons: long fibres use511
votes; the short census uses at most63. The full acquisition ceiling is

    3577 n D_n R logical comparisons.                  (9)

This is an unexecuted theorem/algorithm bound. It is not the measured cost
of the old sorting-based code. Native address generation, source latency,
counts, majority/interpolation work, frame construction, all rejected
proposals, random bits, collection failures, and acquired program memory
remain paid. In particular the old finite full-sort wins and their real
costs remain unchanged by this improved mathematical ceiling.

The conditional preparation work is still
poly(n,log(1/delta))2^g_cond(Q) on the simultaneous correct/capped event.
Every branch is finitely capped by poly*2^n. Running at the internal
allowance delta 2^(-n), exactly as in the root wrapper, gives expected
known-code/bit work poly(n,n+log(1/delta))(2^g_cond(Q)+delta).
The corruption mass epsilon is not suppressed by this amplification;
it must satisfy (7) to supply a one-trial correction advantage at all.

A same-evidence retaining learner can use every one of these operations,
including direct votes, short census, and conditional native frames.
Robust ranking, stochastic domination, self-correction, and martingale
confidence are established ancestry, not claimed new primitives. The
specific contribution being investigated is the closed acquisition of
cheap exact conditional experiment programs despite arbitrarily bad
selected fibres, with no per-fibre accuracy oracle. The supplied low-degree
latent model and native address-noise budget remain substantial premises;
historical priority and universal learning advantage are not established.

No existing six-source fit acquires an absent old-class guard from this
prospective theorem. It also supplies no related-future target guarantee.
The recovered source-derived procedures, their actual construction cost,
and the tasks they can support are kept distinct.

## 7. General constant-noise form, with the tolerance cost exposed

The same calculation permits any fixed epsilon<1/84. Put

    alpha=1/28-3epsilon>0.

Choose a power-of-two short cutoff N_0>=4/alpha and odd
K>=4/alpha^2, using explicit integer ceilings. Census every N<=N_0.
For all longer fibres, (3) gives

    e <=3epsilon +alpha/4+alpha/4
       =1/28-alpha/2 <1/28,

where 1/(2sqrt(K+2))<=alpha/4 and 1/N<=alpha/4.
Thus the seven-corner correction still has error below1/4. Each weak
label costs at most max(K,N_0-1) comparisons, and collections use
J_(N_0)=N_0 ceil_log2(N_0 L/eta_2) accepted preparations. All those costs,
bits and list memory must be substituted into the finite caps.

This is polynomial in 1/alpha, not necessarily polynomial in the encoded
bit length of an epsilon chosen arbitrarily close to1/84. It is a
sufficient tolerance bound from this proof, not an optimal breakdown
threshold or a lower bound on other robust learners. The concrete choice
epsilon<=1/1024 above avoids a parameter-dependent large cutoff and is
already a complete fixed-constant construction.
