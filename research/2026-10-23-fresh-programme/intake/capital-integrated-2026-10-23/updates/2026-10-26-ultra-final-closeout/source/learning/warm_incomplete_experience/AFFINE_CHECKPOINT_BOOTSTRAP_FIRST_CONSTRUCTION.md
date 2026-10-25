# Acquired affine checkpoints make later experiments cheaper

26 October 2026. Owned first construction, written before new peer exposure.
This is a new use of the preserved quadratic-comparison acquisition argument,
motivated by the distinction between a requested-label inverse, resampling a
known witness, and generating both experimental addresses. No new source,
target, simulator, fixture, or observation is used here. The older files and
their measured failures remain unchanged.

## 1. Question and legal interface

Can acquired procedures expose small successive preparation problems even
when the entire learned system has a large nonlinear core? A representation
should change the experiments one can afford while acquisition is still in
progress, rather than only compress a completed source model.

Use the exact legal interface from the earlier comparison bootstrap. The
native domain is V=F_2^n. An unknown quadratic permutation Q:V->V determines

    C(x,z)=1{Q(x)<lex Q(z)}.

The learner receives n, the quadratic-permutation promise, exact chosen-pair
comparisons, native XOR/bit arithmetic, and actual fresh fair bits. It receives
no Q coefficients, output labels, hidden input basis, latent block partition,
checkpoint locations, or conditional sampler. Chosen native addresses and
every comparison, bit, code evaluation, linear solve, and failed proposal are
paid. This deterministic finite mathematical oracle does not include an
unacquired physical reset, noisy comparator, or free experimental settling.

The preserved PROOF.md and QUOTIENT_PREPARATION_SUPPLEMENT.md under
work/portfolio_20261024/learning_opportunity/ give comparison-to-label
acquisition once learned-prefix fibres can be sampled. Their computed
global-core and quotient-deficit costs can remain exponential after many
small nonlinear blocks have already been fully learned. The operation below
uses an earlier learned AFFINE FIBRE and the witness at which a new weak
label is requested. It need not solve a requested prefix label from scratch.

The source class remains supplied. The useful checkpoint structure is not:
it is computed from acquired coordinate programs, and may never offer a
small gap. A competent same-information structured retainer may adopt this
operation; no exclusive learning advantage or historical novelty is claimed.

## 2. The acquired period space

For the already acquired prefix h_t=(Q_1,...,Q_t), define

    B_i(x,v)=Q_i(x+v)+Q_i(x)+Q_i(v)+Q_i(0),
    L_t=intersection_(i<=t) rad B_i,
    A_t(v)=h_t(v)+h_t(0) on L_t,
    N_t=ker(A_t:L_t->F_2^t).                              (1)

All these are computed from the acquired quadratic ANFs. The polar matrices
are explicit alternating binary matrices. Find their common kernel, evaluate
the prefix on its basis, then take the kernel of that linear response map.
The response map is linear on L_t because all polar terms vanish there.
Dense Gaussian elimination and ANF evaluations suffice; naively performing
them for all n stages costs O(n^5) bit operations, with O(n^3) stored acquired
coefficients and checkpoint bases. No polynomial-identity oracle is used.

**Period lemma.** N_t is exactly the space of native translations preserving
the whole prefix at EVERY input:

    v in N_t <=> h_t(x+v)=h_t(x) for every x.             (2)

Indeed the difference is B_i(x,v)+Q_i(v)+Q_i(0). If it is identically zero,
setting x=0 kills the constant term, and the remaining bilinear dependence
forces v into every polar radical. Conversely (1) kills both terms. Hence
N_(t+1) is contained in N_t. Set N_0=V.

Every coset x+N_t lies in the prefix fibre through x. Bijectivity of Q makes
every true t-prefix fibre have exactly 2^(n-t) points. Consequently

    dim N_t <= n-t.                                      (3)

Call t an AFFINE CHECKPOINT precisely when the COMPUTED dimension equals
n-t. Under the correct-prefix and permutation promises, the inclusion and
cardinality give the much stronger fact

    h_t^-1(h_t(x))=x+N_t for every native witness x.        (4)

No fibre enumeration or latent coordinate recovery is needed to certify
this implication within the model. It is not recognition of arbitrary
source orders. A wrong learned prefix can pass the dimension test. A
computed dimension greater than n-t can trigger UNKNOWN, but passing that
test cannot remove the acquisition confidence allowance.

There is always a checkpoint at 0. There is one at n because a translation
preserving an injective complete Q must be zero. Write ALL true checkpoints

    0=tau_0<tau_1<...<tau_k=n,
    g(Q)=max_j(tau_j-tau_(j-1)).                          (5)

This is an a posteriori complexity parameter, not input to the learner. No
invariance under arbitrary reordering/mixing of output significance is
asserted. Invertible affine native input changes do preserve (2)--(5).

## 3. Exact witness-conditioned preparation between checkpoints

At current learned stage t<n, let tau be the last checkpoint at or before
t. A weak-label request supplies its own actual native point x. Compute
h_t(x) from acquired programs. Repeat with a fresh fair-bit tape:

1. Choose V uniformly in N_tau using its acquired basis, and put Z=x+V.
2. Accept exactly when the acquired coordinates tau+1,...,t at Z match
   those at x. Otherwise pay the proposal and repeat.

By (4), Z is uniform in the entire earlier prefix fibre. Both relevant
fibres have known sizes, so on correct prefixes acceptance is EXACTLY

    2^(n-t)/2^(n-tau)=2^(-(t-tau)).                       (6)

The accepted input is exactly uniform in h_t^-1(h_t(x)). Different calls
are independent conditional on their requested witness and the correct
fixed acquired prefix when their bit tapes are independent. The seed uses
n-tau bits per PROPOSAL, not n-t bits per successful draw; the rejected
bits and code evaluations are charged. Expected proposals per draw are
2^(t-tau), with polynomial work and memory per proposal. Since tau is the
last true checkpoint, t-tau<=g(Q)-1.

This improves a very specific interface. Knowing h_t(x) as a label and
knowing an actual x are computationally different. The median/correction
bootstrap already has x at every request, including all its randomly
offset vertices. This mechanism therefore requires no new observation or
input-access contract. It uses the same information that the earlier
label-indexed sampler left unused.

It would be invalid to replace (4) by just a nontrivial period space. If
dim N_tau<n-tau, a single translation orbit may be only one part of a true
fibre. Sampling that orbit need not supply an averaged next-bit label.
There is no generic efficient way here to find all the other orbits. The
equality in the checkpoint test is load-bearing.

## 4. Closing the comparison acquisition loop, with finite caps

For completeness, the statistical reduction being reused is explicit. Let
D_n=1+n+binom(n,2). Given a correct prefix sampler, take K=511 independent
uniform same-prefix points and compare the requested x against their
sample median. In a fibre of size N>=128, the resulting threshold label
has uniform-input average error at most

    e_N <= 1/(2 sqrt(513))+1/N,
    7 e_N < 1/4.                                         (7)

The finite-grid bound comes from coupling discrete sample ranks with floors
of N times continuous uniforms. For N<=64, collect the entire known-size
fibre and sort it to obtain the exact midpoint label; the collection cost
is paid below. A third additive difference kills every quadratic, so the
requested next bit is the XOR of its seven nonempty random-offset cube
vertices. Each vertex is marginally uniform on V, although the seven need
not be independent. Equation (7) and a union bound make one corrected
bit wrong with probability below 1/4. Fresh offsets and median tapes give
independent correction trials when the previous coordinates are correct.
An odd R-fold majority has error at most exp(-R/8).

Interpolate each next coordinate at 0, e_i, and e_i+e_j. The D_n resulting
values determine its quadratic ANF. Newly acquired ANFs give the new N_t
and checkpoint test, and therefore the next experimental procedure. The
previous flag is never supplied in advance.

Here is a literal all-branch finite version. Choose rational allowances
delta_a, eta_1, eta_2>0, whose sum is at most delta. Let ceil_log2 be paid
integer ceiling of a base-two logarithm, and take R to be the least odd
integer at least

    8 ceil_log2(n D_n/delta_a).

There are at most L=7 n D_n R weak-label requests. At a short fibre of
KNOWN size N<=64, stop its collection after

    J_N=N ceil_log2(N L/eta_2)

accepted preparation calls unless all N distinct inputs have appeared.
On a correct prefix its failure probability is at most
N exp(-J_N/N)<=eta_2/L. It is UNKNOWN, not partial enumeration, on a cap.
Set

    M=L max(511,J_64),
    S=ceil_log2(M/eta_1).

M bounds every requested conditional preparation. At stage t with last
ACQUIRED checkpoint tau, cap that preparation at

    B_t=2^(t-tau) S                                      (8)

proposals, returning UNKNOWN if none passes. On correct prefixes (6)
bounds this failure by exp(-S)<=eta_1/M. A global bit/work/memory cap may
also be supplied by the user, in which case exceeding it returns UNKNOWN.
No loop can hang because an erroneous prefix creates an empty filter.

Couple the implementation to an ideal uncapped run that uses the true
prefix at every stage on the same tapes. They agree until their first
coordinate error or collection/preparation timeout. The n D_n independent
value-request bounds, short-collection bounds, and proposal bounds give

    P[correct completion and every cap respected]
        >=1-delta_a-eta_1-eta_2 >=1-delta.                (9)

This is not a conditional-on-return confidence claim and does not condition
future trials on their own good randomness. On (9), the total known-code
work is bounded, for example, by

    O(n^5 + M 2^(g(Q)-1) S n^3),                         (10)

plus source comparison work. The code factor n^3 is a conservative dense
prefix evaluation bound. Fresh bits are at most

    3n*nD_nR + M 2^(g(Q)-1) S n,

and acquired storage and live collection/linear-algebra state are polynomial
in n and logarithmic confidence parameters. No exponential core catalogue
is stored. The same comparison count as the fresh-median original proof
applies:

    at most 32,200 n D_n R exact source comparisons.      (11)

Sorting at most 511 objects uses at most 4,599 comparisons, plus one
threshold comparison, and each correction uses seven such labels.

Critically, (10) is a simultaneous correct-prefix/high-probability runtime
bound. On a wrong learned prefix the checkpoint sequence may be different
and can have a gap as large as n. Thus the capped learner has an all-branch
2^n poly(n,log(1/delta)) upper bound, not an unconditional expected FPT
bound in the TRUE g(Q). The earlier caution about mistaken acquired core
parameters remains in force. Fair bits are an actual external interface;
a fixed PRNG replay is not whole-lifetime independence.

## 5. Once acquired, the same checkpoints give a closed inverse

After correct acquisition, the comparator may expire. The checkpoint spaces
are nested and have dimensions n-tau_j. Compute a direct complement U_j
of N_(tau_j) in N_(tau_(j-1)), of dimension
d_j=tau_j-tau_(j-1)<=g(Q). These are acquired native binary matrices.

To invert an arbitrary COMPLETE requested output y, start with x=0. At
stage j, the current x already matches y through tau_(j-1). Enumerate the
2^d_j native additions U_j a, and choose the one whose acquired program
matches the next d_j output bits. The earlier prefix is unchanged. There
is EXACTLY ONE successful a: the earlier fibre is x+N_(tau_(j-1)), its
N_(tau_j) cosets are in bijection with all next-checkpoint extensions, and
the additions U_j a represent those cosets exactly once. Update x and
continue. At the final checkpoint the fibre is a singleton, so x=Q^-1(y).

This deterministic algorithm has at most sum_j 2^d_j<=n 2^g(Q) trials,
polynomial work per trial, polynomial space, and ZERO further comparisons.
It pays for every complete acquired program evaluation and complement
construction. It never assumes the unknown block inverse or the hidden
native frame. If the learned model was wrong, zero or multiple matches
can return UNKNOWN; a unique match is not an extra semantic certificate.

Every requested t-prefix label can subsequently be sampled exactly: append
n-t independent fair suffix bits and execute this closed inverse. This
uses exactly n-t random bits and poly(n)2^g(Q) known-code work per sample,
on the correct acquired branch. It is a different post-expiry interface
from the cheaper during-acquisition witness sampler, and both are proved.

## 6. All-size separation from the previous cost parameters

Use the already preserved three-bit F_8 cube

    C(a,b,c)=(a+b+c+bc, b+ab+ac, c+ab).

Its polar coefficient rows in pair order (ab,ac,bc) are
(0,0,1), (1,1,0), (1,0,0), which are independent. The common radical of
the first two is zero, as is that of all three. The map is a permutation
because z->z^3 permutes F_8, with gcd(3,7)=1. These are governing algebra
from the existing FIBRE_SAMPLER_AUDIT.md, not new source observations.

For n=3m, take m disjoint copies of C in significance order and apply an
arbitrary UNKNOWN invertible affine input hiding x->Ax+b. No latent block
labels, hidden frame, or checkpointer is supplied to the learner.

After each complete cube, the leading output tuple is bijective on the
corresponding latent coordinates and independent of the others. Its full
native fibres are exactly affine cosets of dimension n-3j. Hence every
3j is a true checkpoint and g(Q)<=3. The operation above has polynomial
acquisition and closed inverse cost on this whole all-size family, without
needing to infer its hidden three-dimensional block partition first.

In contrast, the global common-polar-radical parameter is b(Q)=n. At the
strict prefix t=n-1 the first two coordinates of the last cube already
have common polar radical zero, so L_t=0 and rank A_t=0. The earlier
quotient-deficit parameter is therefore kappa(Q)=n-1. Its declared generic
bound, and the earlier full-core table bound, are exponential here.
This is a separation of PROVED COST PARAMETERS, not a claim that an
equally informed conventional algorithm must incur those earlier costs.

No nonzero linear combination of the complete outputs is affine: the
independent three polar coefficients within each disjoint block cannot
cancel against another block, and invertible input congruence preserves
this fact. Thus the family is outside the earlier N780 complete scalar
triangular class, whose first significance coordinate is affine. On that
incumbent's overlap its much smaller comparison bound remains stronger.

Arbitrary mixing/reordering of OUTPUT significance can destroy these small
gaps; none is granted or recovered for free. The important positive claim
is the learned native checkpoint operation with data-computed g, not a
general polynomial-time learner for quadratic permutations or an autonomous
discovery of their model class.

## 7. Why this is a useful but restricted next operation

This closes an acquisition/deployment loop in which an expensive early
source can expire leaving exact closed evaluation, inversion, and experiment
procedures. Its central additional operation is using a paid learned period
space and a supplied REQUEST WITNESS, then recognizing when the entire
old fibre is that translation orbit. Once a nonlinear block is complete,
its information need not be rejected again in every later preparation.

Linear-structure theory, stabilizer chains, blocked comparison learning,
and the older affine-flag decoder are strong incumbent directions. The
exact same-source/bits/computation comparison must be checked against their
governing statements before any priority or broader advantage conclusion.
The new theorem does not confer a representation-free future-task promise,
remove unknown physical preparation costs, recognize the supplied class,
or rescue any previously defeated scalar/query-economy claim. No new finite
benchmark or source experiment is claimed. The meaningful mathematical
discriminator is the all-size g<=3 versus b=n and kappa=n-1 separation,
with the full acquisition and post-expiry costs paid.
