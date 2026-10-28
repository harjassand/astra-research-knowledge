# Exact observation from persistent proxy samples

Status: derived mathematical construction/obstructions and executed exact finite
checks. The new general proofs await independent substantive review. Historical
priority and practical advantage are UNKNOWN. The completed N1073 source audit
remains sufficient at its actual accepted version and scope.

## Source and task contract

The source pin is `e1e2272165c8548326c31bb11817c28f871d21e9`. Its current catalog
contains 1762 records. N1073's complete governing `PROOF.md` (14519 bytes,
SHA256 `33007e1215fd91118e35be36b07b50ea3096b936b3c33c8e519b058d50ad4eb9`)
and completed `SEQUENTIAL_REVIEW.md` were read and retained unchanged. Exact
source routes/hashes are in `SOURCE_MANIFEST.json`. A packet is navigation;
this extension relies on the governing proof, not its card's authority alone.

N1073 assumes finite rational column-stochastic K,L; an already-classical X;
one fresh private Z~L(.|X); and an optional charged raw-X disclosure. It
characterizes a substochastic no-read U with UL<=K and the known queried
residual. Its adaptive result preserves the controller's Y record and finite
cq reference. Z, raw values, flags, costs, private randomness and memory remain
private. It neither manufactures a coherent-input measurement nor acquires a
physical source/calibration.

The new task holds one classical X persistent while the module gets several
fresh iid cheap records and delays one K output. All cheap service calls,
preparation, reset, calibration, entropy, arithmetic, storage and latency are
charged. The persistent iid stream is a supplied resource, equally available
to ordinary methods. Initial private randomness is independent of current X;
no free cached raw X, true-channel descriptor or parameter side channel is
supplied. A raw callback discloses X only.

Output equality below means equality of Y, or Y with an untouched cq reference,
after private registers are discarded. It does not preserve the joint law of
(Y,Z,flags,count). Even a call count independent of X can reveal information
when combined with Y, because the conditional output law can depend on count.

## 1. Known-channel block operation and ordinary method

For any strictly positive m-by-n K and known rational k-by-n L with distinct
columns, a finite iid block can simulate K exactly without raw X. Let C_r be
the confusion matrix of nearest-column classification of the empirical proxy
distribution, with deterministic ties. Put kappa=min K_yx and
Delta=min_{x!=x'}||L_x-L_x'||_infinity>0. If each classification error is <=d,
then ||C_r-I||_1<=eta=2d. For eta<1,

    ||C_r^-1-I||_1 <= eta/(1-eta).

Since ||K||_1=1, V=K C_r^-1 is nonnegative if eta/(1-eta)<kappa. Its columns
sum to one, and V C_r=K. Coordinate-wise Hoeffding plus a union bound gives
d<=2k exp(-r Delta^2/2); for example

    r >= (2/Delta^2) log(8k(1+kappa)/kappa)

suffices with slack. The executable `compile_by_classifier` instead accepts
the actual exact rational identity and positivity certificate. It enumerates
M=binomial(r+k-1,k-1) types, using O(Mnk) rational operations plus inversion
and O(Mk+n^2) words. Encodings grow with r and input bit length. Delta may be
exponentially small, and M is not polynomial uniformly in k. This is ordinary
classification and garbling, not a new complexity result. A joint-channel LP
may improve its repetition count with the identical supplied observations.

The exact source pair is

    L=[[2/3,1/6,1/6],[1/6,2/3,1/6],[1/6,1/6,2/3]],
    K=[[2/15,49/120,49/120],
       [13/30,71/240,71/240],
       [13/30,71/240,71/240]].

The retained one-record primal/dual gives q*=3/40; `verify.py` independently
checks feasibility and equal objectives. The unique ordinary one-record
postprocessor has first row (-1/20,1/2,1/2), excluding zero raw cost there.

With two records let c count those equal to zero. Choose output zero with
probabilities (13/25,17/100,0) at c=0,1,2; otherwise split outputs 1,2 equally.
Its output-zero law at p=L_0x is

    g(p)=13/25-(7/10)p+(9/50)p^2.

Direct substitution gives g(2/3)=2/15 and g(1/6)=49/120. Thus the entire K
channel is exact at all inputs with two cheap calls and no raw call. The
ordinary classifier construction independently yields

    C_2=[[8/9,11/36,11/36],[1/12,2/3,1/4],[1/36,1/36,4/9]],
    K C_2^-1=[[17/210,58/105,58/105],
               [193/420,47/210,47/210],
               [193/420,47/210,47/210]],

which is stochastic with the same acquisition counts. There is no special
advantage over this ordinary method. Both callbacks in `source_two_proxy_output`
are actual cheap calls; no raw callback has already been invoked behind a flag.

## 2. Open stationary uncertainty with a finite hard cheap budget

Let each actual column p_x range over a relatively open nonempty subset of the
simplex interior, with the true columns unknown to the module. Require exact K
for every allowed column. Allow arbitrary private randomization/adaptation,
at most B<infinity total cheap draws, and at most one raw disclosure. Any prior
calibration observations available to the protocol count in this total.

Write b_y=min_x K_yx and alpha=sum_y b_y. Every such protocol has raw
probability >=1-alpha at each input/channel. To prove this, presample B iid
records w and pad unused draws. Let A_yx(w) be the total conditional output
probability, and U_y(w) the probability of output y without raw disclosure.
The latter is independent of x, and 0<=U_y(w)<=A_yx(w). Average over each
multinomial type t. Exactness makes

    sum_|t|=B multinomial(B,t) p^t bar A_yxt = K_yx

on an open simplex subset. Polynomial identity and uniqueness of the degree-B
Bernstein basis force bar A_yxt=K_yx for every t. Hence bar U_yt<=b_y and
the total no-read mass is <=alpha at every p.

Ordinary common-part splitting attains the bound without cheap calls: emit y
with unnormalized mass b_y; otherwise disclose X and output from
(K_.x-b)/(1-alpha). Here alpha=29/40 and raw cost=11/40. The queried residual
is (0,1/2,1/2) at x=0 and (1,0,0) at x=1,2.

The theorem is a finite-hard-budget statement. It is not an unbounded-stopping
lower bound or a result for lower-dimensional parametric uncertainty. Requiring
UL_theta<=K at several channels does not alone build a robust implementation:
N1073's nominal queried residual requires the actual L_theta.

For illustration, perturb each source column by delta*(1,-1/2,-1/2). Channel
TV is |delta|. The two-record output TV is
|(-7/10+(9/25)L_0x)delta+(9/50)delta^2|. At delta=1/600 this is
(4597,6397,6397)/6000000. The unchanged nominal one-record runtime has TV
(2/5)|delta|. Exact rational checks include +/-1/600 and +/-1/60000.
The finite interpolation tests B=1..4 have ranks 3,6,10,15 inside radius 1/600;
these tests illustrate, rather than prove, the general polynomial argument.

## 3. Explicit stationary-uncertainty factory

For TV radius delta<=1/12, p=Pr(Z=0) lies in p<=1/4 at x=1,2 and p>=7/12 at
x=0. Define a known function on all p in [0,1]:

    f(p)=49/120                         if p<=1/4,
    f(p)=2/15                           if p>=7/12,
    f(p)=49/120-(11/40)S(3p-3/4)         otherwise,
    S(t)=10t^3-15t^4+6t^5.

An f(p) coin, with equal outputs 1,2 on tails, implements K throughout those
neighborhoods without identifying X. f is C^2 with Lipschitz second derivative
and range strictly in (0,1). This is an ordinary Bernoulli-factory operation.

Use M2=297/8 for |f''| and M3=891/2 for Lip(f''). These follow from
|S''|<=15, |S'''|<=60 and transition width 1/3. At square four-adic degrees put

    h_n(k)=f(k/n)-[(k/n)(1-k/n)/(2n)]f''(k/n),
    e_n=D/n^(3/2), D=3861/4=2(M2+M3),
    a_n=h_n-e_n, b_n=h_n+e_n.

For elevation n->4n, J~Hypergeom(4n,k,n), t=k/(4n), W=J/n-t. Then E W=0,
E W^2=3t(1-t)/(4n-1), E|W|<=1/(2sqrt(n)). The sampling-without-replacement
Hoeffding bound implies E|W|^3<n^(-3/2); its looser bound 2n^(-3/2) suffices.
Taylor remainder is <=M3 E|W|^3/6. The function t(1-t)f''(t) has Lipschitz
constant <=M2+M3/4. Substitution gives

    |E h_n(J)-h_4n(k)|
      <= [M2/32+M2/4+M3/16+M3/3] n^(-3/2)
      <= (M2+M3)n^(-3/2).

The exact remaining quadratic term is 3t(1-t)f''(t)/[8n(4n-1)], bounded by
M2/(32n^2). Since e_n-e_4n=(7/8)D n^(-3/2), the lower/upper coefficient
envelopes nest. At n0=1024, M2/(8n0)+e_n0<2/15, so all coefficients lie in
[0,1], and the bound decreases thereafter. Both polynomial envelopes converge
to f by Bernstein approximation and a vanishing correction.

At the first level, heads/tails/continue probabilities at count k are
(a_n(k),1-b_n(k),2e_n). On continuing to m=4n, they are

    [(h_m(k)-Elev(h_n)(k)+e_n-e_m)/(2e_n),
     (Elev(h_n)(k)-h_m(k)+e_n-e_m)/(2e_n), e_m/e_n].

Conditional elevation is hypergeometric. Induction gives the lower polynomial
as the probability of heads by each level and one minus the upper polynomial
as the probability of tails. Therefore the limiting heads probability is f
and stopping is almost sure. The continuation probabilities are constant at
every count: 2e_n0=3861/65536 initially and 1/8 thereafter. For
n_j=1024*4^j,

    Pr(N>n_j)=2D/n_j^(3/2),
    E N=n0+sum_j 3n_j Pr(N>n_j)=44351/32=1385.96875.

All coefficients are rational; integer rejection from independent unbiased
bits samples them exactly in finite expected random-bit cost. `factory.py`
implements this construction, with full exact hypergeometric sums.

## 4. Full-cost repair by lazy exact comparison

The full-sum implementation has a genuine defect: reached level n processes
Theta(n) integers of Theta(n) bits at interior frequencies, while level
probabilities decay as n^(-3/2). Its expected bit work diverges. Finite expected
cheap observations alone cannot justify promotion.

`factory_lazy.py` repairs this under a positive stationary plateau margin.
Predraw terminal degree independently, with probabilities 1-2e_n0 initially
and 2(e_m-e_n) at n=4m thereafter. Draw only that many cheap records and use
the conditional STOP heads coin

    q_n(k)=1/2+[h_n(k)-Elev(h_m)(k)]/[2(e_m-e_n)]

at later levels; initially use (h_n0(k)-e_n0)/(1-2e_n0). Telescoping of the
weighted heads polynomials proves the same exact f(p) law. This preserves the
degree distribution and expected cheap count. The predrawn degree remains a
private register; it is not appended to the ideal transcript.

If x=k/n lies on a plateau c, h_n(k)=c. Let g be its distance to the transition.
An elevated h_m coefficient differs from c only if J/m crosses the transition.
Consequently the one-sided hypergeometric Hoeffding bound gives

    |q_n(k)-1/2| <= R_m exp(-2m g^2),
    R_m=[11/40+M2/(8m)]/[2(e_m-e_n)].

No exponential-size rational denominator is needed. Set

    B=floor(2m g^2)-ceil(log2 R_m).

Since exp(-s)<=2^-floor(s), |q_n-1/2|<=2^-B. Compare an ideal uniform's bits
against the dyadic strip around 1/2 lazily. Away from that strip the answer is
known without an exact sum. On entering the strip, compute the exact q_n and
continue comparing against the SAME saved uniform prefix. Replacing that
uniform by a fresh coin on the strip would be incorrect. Exhaustive dyadic
prefix checks and a forced exact fallback exercise this detail in the code.

For the actual TV promise delta=1/600, every true p is at least
gamma=49/600 inside a plateau. At terminal degree n, the empirical count is
within gamma/2 of p except with probability <=2exp(-n gamma^2/2). On that
event its plateau distance is >=gamma/2. Thus a completely computable bound
on triggering any costly exact evaluation is

    T(n) <= min(1, 2*2^-floor(n gamma^2/2) + t(B_gamma(n))),
    B_gamma(n)=floor((n/4)gamma^2/2)-ceil(log2 R_(n/4)),
    t(B)=1 if B<2, and 2^(1-B) otherwise.

This decays exponentially up to a polynomial factor. For example the looser
bound T(n)<=min(1,4 n^(3/2)2^(-n gamma^2/8)) holds. Binomial coefficients in
the implementation use an explicit multiplicative recurrence: O(n) arithmetic
operations on O(n)-bit integers. Exact evaluation therefore has a conservative
polynomial bit-work upper bound (O(n^3) with schoolbook integer arithmetic
suffices). Prefix comparison and other rare work also have polynomial cost.

The expected complete work is bounded by a computable series of the form

    C0 E[N log^c N] + C1 sum_j Pr(N=n_j) T(n_j) n_j^d,

for fixed implementation constants c,d. The first term is finite under the
four-adic n^(-3/2) tail and the second is finite for EVERY fixed polynomial d
because T decays exponentially. This is a finite expected BIT-WORK guarantee
at positive margin, not merely an arithmetic-operation or sample guarantee.
Worst-case time/space remains unbounded. At the plateau boundary (zero margin)
the exact law and finite cheap mean survive, but this full-cost proof does not.

The code's 96 seeded diagnostic outputs used no exact elevated sums, including
a 65536-call terminal degree. They are finite PRNG diagnostics, not physical
data or proof of the ideal distribution/expectation. Exact algebra and the
analytic bound carry those general claims, pending independent audit.

## 5. Unknown stationary point versus actual nonstationarity

For any delta<1/4 the scalar intervals around 1/6 and 2/3 stay disjoint. A
rescaled smooth step with strictly positive buffers gives the same type of
zero-raw factory, with recomputed constants and positive-margin bit-cost proof.
Our fixed constants only cover delta<=1/12 and the full-cost guarantee above
uses the narrower actual delta=1/600 promise. At delta>=1/4 the FULL TV balls
for columns 0 and 1 intersect at (5/12,5/12,1/6). Identical cheap-stream laws
then force a common no-read subdistribution. Raw cost is >=TV(K_.0,K_.1)=11/40,
and ordinary common-part splitting attains it, even with unbounded sampling.

There is a stronger obstruction for exact robustness to arbitrarily small
NONSTATIONARY perturbations. Suppose exact K is required after independent
open perturbations of any finite prefix of draw laws, followed by the nominal
iid tail, and require almost-sure termination. For a fixed prefix length r,
pad/presample the prefix and let A_yx(w) be the eventual output law conditional
on its symbols w, including the nominal tail and possible raw disclosure.
A_yx(w) is independent of the prefix-law parameters. Exactness makes

    sum_w product_t p_t(w_t) A_yx(w)=K_yx

on an open product neighborhood. Uniqueness of this multi-affine polynomial
basis forces A_yx(w)=K_yx for every prefix w. Let U_y,r(w) be the conditional
probability of halting with output y, no raw, and at most r cheap calls. This
depends only on the prefix and X-independent private randomness, so is common
to every x. It is bounded by each A_yx(w), hence by min_x K_yx. Averaging gives
Pr(no raw and halt by r cheap calls)<=alpha. Monotone convergence under
almost-sure finite termination gives Pr(no raw)<=alpha, or raw>=11/40.

Any positive budget epsilon for sum_t TV(p_t,L_.x) contains such an open box for
each finite r: allocate perturbations smaller than epsilon/(2r), also inside
the positive simplex. Thus exact robustness to this arbitrarily tiny total
perturbation budget has sharp raw cost 11/40, even evaluated on the nominal
iid stream and even with unbounded stopping. The common-part baseline attains
it. This argument assumes no prefix-law/parameter side channel and accounts
for all cheap observations. It does not invalidate stationary unknown-point
Bernoulli factories. Exact rank checks for r=1,2,3 give 3,9,27 in a total TV
budget 1/600; the universal result is the proof, not those finite checks.

Target zeros also matter: with full-support source columns every finite word
has positive probability at every input. In a no-raw almost-surely finite
protocol, an output forbidden at one input cannot have positive probability at
another. In particular an identity target cannot avoid raw disclosure. The
positive K above avoids this support obstruction.

## 6. Strong ordinary approximate comparator and complete-resource scope

At delta=1/600, threshold the mean of m cheap zero-indicators at 5/12 and then
sample the corresponding known K column (merge inputs 1,2). The class gap is
1/4-delta=149/600. Even with predictable per-draw drift within those separated
intervals, conditional Hoeffding yields

    output TV <= (11/40) exp(-2m(149/600)^2).

102 calls certify TV<=1e-6 (bound 9.455010408690606e-7); the expression at 101
calls is 1.0696148162716992e-6. `verify_lazy.py` checks these using exact rational
upper/lower Taylor bounds for the exponential, not floating comparisons.
`source_approximate_output` implements the comparator. Its approximation
contract differs from exactness; it establishes no contradiction with the
exact nonstationarity obstruction and prevents overstating practical benefit.

For one output the nominal two-call operation beats the one-call service cost
only if c_X>(40/3)c_L before other costs. The robust exact factory's service-
only crossover against common-part splitting is c_X>(221755/44)c_L, about 5040
cheap calls per raw disclosure, plus all arithmetic/calibration/preparation
terms. No physical service or cost ratio was acquired. For many requested
outputs at one known-persistent X, ordinary one-read caching is also allowed;
one two-record block cannot simply be reused to produce independent K outputs.

## Primary prior and conclusion

[Nacu–Peres](https://arxiv.org/pdf/math/0309222) supplies the established
Bernstein-envelope factory framework. [Holtz–Nazarov–Peres](https://arxiv.org/pdf/0808.1936)
Theorem 8 relates smoothness to simulation rates. The explicit specialization
and lazy evaluation above use those ordinary ideas. [Hoeffding](https://www.cs.rpi.edu/academics/courses/spring06/random/hoefding.pdf)
supplies the concentration bounds, including sampling without replacement.
[Makur–Singh](https://arxiv.org/pdf/2309.08475) describes common-part/Doeblin
coupling. No novel general Bernoulli factory, new information source, or
complexity-class separation is claimed. A narrow search found no direct
nonstationary-prefix theorem, which is not evidence of historical priority.

Achieved: executable exact block and stationary-uncertainty operations; an
explicit finite expected complete-cost repair; exact calibration/drift/support
boundaries; and a competent approximate comparator. Physical calibration,
source acquisition, a complete-resource advantage, historical novelty, and the
civilisation-level discovery objective remain unestablished.
