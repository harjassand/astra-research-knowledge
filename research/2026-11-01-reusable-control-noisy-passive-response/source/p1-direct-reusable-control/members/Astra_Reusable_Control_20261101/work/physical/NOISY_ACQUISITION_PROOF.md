# Finite noisy acquisition of a positive rational response law

1 November 2026. New construction in this investigation. This is an ordinary proof
of a finite acquisition guarantee under a warranted source class. It is not a
claim of a measured apparatus, historical priority, or a new linear-programming
algorithm. The new step is a quantitative diameter bound for the positive
rational outer family already proposed in Astra N1152.

## 1. Consequence and source contract

The task is to acquire, using finitely many noisy scalar experiments, a record
that subsequently bounds the response to **every** nonnegative combination of
the n actuators with a fixed total dose. Future commands may be chosen after
seeing the record. The microscopic state dimension, small individual couplings,
and spectral gaps are not supplied to the learner.

The warranted fixed source is

    F(u) = g^T P (I + P B P)^(-1) P g,
    P = diag(sqrt(u)), B >= 0,
    u_i >= 0, sum_i u_i <= delta,
    |g_i| <= G, B_ii <= kappa.

There are n finite controls, but B may have arisen as a Gram matrix in a much
larger or infinite coercive hidden Hilbert space. Only this finite-control
response law and the stated bounds are used. General chemistry does not
automatically have this source law. Actual scalar native readings may include a
shared baseline; the acquired intervals below must already account for its
calibration or for subtraction of a zero-command reading. All setting,
settling, drift, reset, receiver, and numerical errors remain charged.

Put L=delta G^2 and q=delta kappa. The cases delta=0 or G=0 are trivial because
F=0. Henceforth L>0. Normalize x=u/delta and f(x)=F(delta x)/L. The command set is

    X = {x >= 0 : sum_i x_i <= 1},       0 <= f(x) <= 1.

We assume rational outward specifications for q,L and rational observed
intervals; upper bounds may replace exact physical specifications throughout.
Neither g nor B is an acquired input.

## 2. Reused, revision-bound ingredients

Only prior Astra sources at Git revision

    51ce47ce39f976517d60e2f87bbe280b651f6056

are used. The two decisive complete proofs were read and retained alongside this
note:

1. `research/2026-10-29-control-acquisition-and-matrix-formulas/source/p1-dark/selection/inference_determinant_tail_theorem.md`,
   SHA-256 `07c78b79cf150dce546666654259f443c1b38e4337f5e40bf26397dc1206bf4d`.
   N1152, Sections 2--4 and 7: the determinant ratio, positive coefficient boxes,
   one-sided rational truncation, and proposed polyhedral outer family. Its
   existing review is scoped to that corrected theorem; this new diameter result
   is a separate proof.
2. `research/2026-10-29-control-acquisition-and-matrix-formulas/source/p1-dark/theory/SIMPLEX_LAW_ACQUISITION.md`,
   SHA-256 `279325cf5c9c90b8146c1bd3ea5e97485882aa1200d7b39f05ecdabc5212cf4f`.
   N1150, Sections 1--2: unisolvent degree-k simplex lattice and its
   dimension-independent norming constant. Sections 4--5 supply the strong
   Chebyshev and positive Bernstein comparators.

The resulting positive rational representation is

    f(x) = N(x)/D(x),
    D(x) = sum_S d_S x_S,       d_empty=1,
    N(x) = sum_{S nonempty} b_S x_S,
    0 <= d_S <= q^s,
    0 <= b_S <= s^2 q^(s-1),   s=|S|>=1,
    x_S = product_{i in S} x_i.

These are normalized coefficients: d_S here is delta^s times the original
denominator coefficient and b_S is delta^s/L times the original numerator
coefficient. They are finite even at dark g_i and singular B. At q=0 the s=1
numerator bound is interpreted as 1, and all higher coefficients vanish.

For a chosen truncation degree r>=1 let rho=min(r,n). The true truncated pair
N_r,D_r uses |S|<=rho and has D_r>=1. Define

    A_r(q) = sum_{j=0}^rho q^j/j!,
    e_r(q) = 0                         if rho=n,
             [q^rho/rho!]/A_r(q)       if rho<n.

Then simultaneously on X,

    0 <= f(x) - N_r(x)/D_r(x) <= e_r(q).               (1)

The actual-dose version is

    0 <= f(x)-N_r(x)/D_r(x)
       <= s_x H_rho(q s_x),   s_x=sum_i x_i,          (2)

with zero right side when rho=n. These are inherited accepted truncation
statements, not assumptions about an arbitrary candidate coefficient pair.

## 3. The finite experimental protocol

Choose a lattice degree k>=1, independently of r. For each nonnegative integer
vector alpha=(alpha_0,...,alpha_n) with sum alpha_i=k, set

    x_alpha=(alpha_1,...,alpha_n)/k.

Acquire simultaneous interval bounds

    f(x_alpha) in [y_alpha-xi_alpha, y_alpha+xi_alpha],
    0 <= xi_alpha <= xi.

There are M=binom(n+k,k) commands and each has at most k nonzero actuators.
The interval event may be deterministic; independence of node errors is not a
mathematical premise. If statistical intervals are used, all conclusions hold
on their simultaneous coverage event. Node selection is fixed in this theorem.

Construct the following rational polytope P_r of candidate coefficient pairs
(N,D). Retain only square-free monomials with |S|<=rho. Impose d_empty=1,
n_empty=0, the nonnegative boxes in Section 2, and, at each acquired node,

    (y_alpha-xi_alpha-e_alpha) D(x_alpha) <= N(x_alpha)
                                             <= (y_alpha+xi_alpha) D(x_alpha),

where either e_alpha=e_r(q) or the sharper actual-dose bound (2) is used. All
constraints are linear in the coefficient arrays. The true truncated pair is
feasible by (1), so P_r is nonempty on the interval event. It is closed and
bounded. All candidates have D(x)>=1 on the entire domain.

The feasible pair need not be a physical Gram source. No assertion of positivity,
concavity, or source realizability beyond the stated coefficient constraints is
silently made. This relaxation is the reason an ordinary LP can implement it.

At a later command x, compute

    lo(x) = min_{(N,D) in P_r} N(x)/D(x),
    hi(x) = max_{(N,D) in P_r} N(x)/D(x).

Then the acquired response interval is

    f(x) in [lo(x), hi(x)+e_x] intersect [0,1].        (3)

The true f_r is in the feasible family. Equation (1) proves (3) directly. The
uniform diameter theorem below guarantees that these intervals become narrow
from this explicit finite experimental design. Neither coefficient
identification nor a chosen adaptive query heuristic is required.

## 4. A coefficientwise cross-product bound

Define the exact rational nonnegative number

    B_(r,k)(q) = sum_{1<=a<=rho, 0<=b<=rho, a+b>k}
                    a q^(a+b-1)/[(a-1)! b!].         (4)

At q=0 use ordinary polynomial continuity; the only potentially nonzero product
has total degree one and contributes nothing when k>=1. Thus B=0 at q=0.
If k>=2rho the sum is empty, so B=0 exactly.

For any candidate pair in P_r and any fixed x in X, its homogeneous degree-a
numerator obeys

    N_a(x) <= a^2 q^(a-1) sum_{|S|=a} x_S
           <= a q^(a-1)/(a-1)!,                     (5)

because the elementary symmetric polynomial is at most (sum x_i)^a/a!<=1/a!.
Likewise D_b(x)<=q^b/b!. This applies to every relaxed candidate, using only its
boxes. Consequently

    1 <= D(x) <= A_r(q).                             (6)

For two candidate pairs (N,D) and (N',D'), write

    H = N D' - N' D,
    H = H_low + H_high,

where H_low retains total degrees <=k and H_high retains degrees >k. Each
positive product ND' or N'D has a tail at x bounded by (4), using (5) degree by
degree. Since both tails are in [0,B], their difference satisfies

    |H_high(x)| <= B_(r,k)(q).                       (7)

There is no extra factor two in (7). This is a bound on the difference of two
nonnegative numbers in the same interval.

## 5. Finite-noise whole-law diameter theorem

Let

    C_k = binom(2k-1,k),
    Delta_(r,k) = C_k A_r(q)^2 (2xi+e_r(q))
                           + (C_k+1) B_(r,k)(q).    (8)

**Theorem.** On the simultaneous node-coverage event, every two feasible
candidate ratios satisfy

    sup_{x in X} |N(x)/D(x)-N'(x)/D'(x)|
           <= Delta_(r,k).                          (9)

The intervals (3) have simultaneous width at most

    min{1, Delta_(r,k)+e_r(q)}.                     (10)

Multiply by L to restore the physical response units. Future adaptive choice
of x does not need a new union bound: the same deterministic event implies
(9) at every x.

**Proof.** At an acquired node every feasible ratio lies in the common interval

    [y_alpha-xi_alpha-e_alpha, y_alpha+xi_alpha].

Therefore the gap between any two is at most 2xi+e_r, not 2xi+2e_r. Multiplying
by the two denominators and using (6) gives

    |H(x_alpha)| <= A_r(q)^2 (2xi+e_r).              (11)

Equation (7) gives

    |H_low(x_alpha)| <= A_r(q)^2(2xi+e_r)+B.         (12)

The polynomial H_low has total degree at most k. The N1150 lattice cardinal
functions are

    L_alpha(x) = product_{i=0}^n binom(k lambda_i,alpha_i),
    lambda_0=1-sum x_i, lambda_i=x_i.

They reproduce H_low and satisfy sum_alpha |L_alpha(x)|<=C_k. For completeness,
absolute falling-factorial coefficients are bounded by rising-factorial ones;
the product of generating functions is (1-z)^(-sum_i k lambda_i)=(1-z)^(-k),
whose degree-k coefficient is binom(2k-1,k). Thus (12) gives

    |H_low(x)| <= C_k[A_r(q)^2(2xi+e_r)+B].          (13)

Add (7), then divide by D(x)D'(x)>=1. This proves (9). Taking the supremum and
infimum over feasible pairs bounds hi-lo; (3) adds one one-sided tail. This
proves (10). All zero-degree, dark-coupling, and singular-source cases are
already included. QED.

Two useful specializations are:

* Exact cross interpolation: k>=2rho gives B=0. For rho=n it learns the exact
  finite-control rational law to bounded noise, with no truncation allowance.
* Smaller experimental lattice: r=k<n. The products may have degree 2k, but
  the charged positive tail in (4) permits degree-k experimental acquisition.
  This is the main effective-degree form.

One can improve the displayed sufficient bound in a particular run by retaining
actual node errors, actual-dose e_alpha, candidate denominators, and the exact
finite coefficient tails. Those improvements are optional; no claim of
optimality is attached to (8).

## 6. Why this converges for every fixed finite q

Take r=k<n. Then A_k(q)<=exp(q), e_k(q)<=q^k/k!, and the finite tail (4) is
bounded by the corresponding infinite positive series:

    B_(k,k)(q) <= sum_{j>=k}(2q)^j/j!
                              + q sum_{j>=k-1}(2q)^j/j!.               (14)

The generating series behind (14) is t(1+qt)exp(2qt). For k>=4q and k>=1,
geometric domination of successive series terms yields, with boundary equalities
interpreted conservatively,

    B_(k,k)(q) <= (k+2)(2q)^k/k!.                    (15)

Indeed the first sum is at most 2(2q)^k/k! and the second is at most
2q(2q)^(k-1)/(k-1)!; their sum is (k+2)(2q)^k/k!.

Since C_k<=4^k, the zero-noise contribution in (10) tends to zero factorially.
For fixed q>0 and target normalized width tau decreasing to zero, one can choose

    k = (1+o(1)) log(1/tau)/log log(1/tau),

then choose xi<=tau/[4 C_k A_k(q)^2], making the noise contribution at most
tau/2 and increasing k until the remaining terms are at most tau/2. Thus

    xi = tau^(1+o(1))        for fixed q,
    M = binom(n+k,k).

This is an upper bound, not an optimal-information law. For fixed n, the exact
choice r=n,k=2n is also available and eventually preferable. When q grows, the
constants grow as well; an O(q+log(1/tau)) degree suffices from the displayed
bounds, and no uniform statement independent of q is claimed.

For q=0 the source is affine, r=k=1 suffices, A=1 and B=e=0. Formula (10) then
gives width at most 2xi, with n+1 experiments. This is the expected benign
boundary and requires no limit argument or division by q.

## 7. Finite arithmetic and costs

In normalized coordinates all input coefficients in the design are rational.
Monomials at a node have denominator dividing k^rho. Box coefficients q^s and
s^2 q^(s-1), the tail e_r, A_r and B_(r,k) all admit exact rational evaluation.
No eigenvalue computation, Poisson random variable, or transcendental number is
needed to execute the theorem. Equations (14)--(15) are only asymptotic bounds;
use the exact finite sum (4) for a concrete budget.

There are V=2[sum_{s=0}^rho binom(n,s)-1] free coefficient variables, M data
constraints on each side, and box constraints. A node has support at most
min(n,k), so each data row has at most twice sum_{s=0}^rho
binom(min(n,k),s) nonzero monomial positions (with impossible binomial terms
zero). The exact LP may still be large. Standard rational LP algorithms have
time polynomial in this explicitly charged input size and its bit length;
the combinatorial experimental cost has not disappeared.

For a future rational command x, linear-fractional optimization in (3) reduces
to ordinary LP. Set t=1/D(x), z=t theta, where theta is the coefficient vector
including its fixed constant. Impose D_z(x)=1, d_empty,z=t and the original
linear/box constraints homogenized by t. The objective is N_z(x). The bound
1<=D(x)<=A_r(q) gives 1/A_r(q)<=t<=1. The transformed feasible set is compact;
exact rational primal/dual certificates or correctly directed numerical
enclosures provide endpoints. A binary64 optimizer's bare answer is not an
exact certificate. Because the original rational polytope is nonempty, it has
rational feasible points even if the underlying physical coefficients are
irrational.

Commands: M=binom(n+k,k). Requested nonzero setting writes total
n binom(n+k-1,k-1); clearing pays the same unless a different physical protocol
is earned. Every command pays preparation, settling, exposure, detection, and
reset. Repeated measurements and calibration add to these costs. Actuation
resolution must be included in the given node interval, using a warranted
sensitivity bound; repeated averaging does not eliminate a systematic error.

If, as a separate sensor model, repeated dimensionless measurements have
independent sigma-sub-Gaussian noise, t_rep >= 2 sigma^2 xi^(-2)
log(2M/alpha) repeats at each node give simultaneous error xi with probability
at least 1-alpha. This produces total observations M*t_rep. At fixed q the
per-node precision cost is tau^(-2-o(1)) up to logarithms. Arbitrary physical
noise is not assumed to be sub-Gaussian, independent, or reducible by repeats.

## 8. What changes and what remains conventional

N1152 already supplies the determinant representation, positive truncation, and
LP outer family. This note supplies a specific finite noisy experiment set and
a proved whole-family diameter bound. N1150's simplex norming estimate is the
second essential Astra ingredient. The mechanism is to approximate the
**cross-multiplied discrepancy of two feasible responses**, where positive
coefficient tails have factorial control, rather than to reconstruct weak
microscopic couplings or interpolate the response itself blindly.

The conventional positive Bernstein receiver has noise gain one and bias at
most q/k in normalized units. It can be much preferable at modest accuracy or
with an irreducible sensor error floor. The same lattice's Chebyshev comparator
has an explicit sufficient geometric-decay regime q<16/9. The present rational
diameter construction converges at every fixed finite q and uses asymptotically
smaller degree than the proved Bernstein bias bound when precision increases.
These are comparisons of proved sufficient guarantees, not lower bounds on
either best polynomial approximation or every possible conventional learner.

Equally informed rational system identification, semialgebraic fitting, and
positive rational set-membership methods can adopt the Astra determinant and
norming ingredients. The LP is ordinary. A strong physical-source-constrained
nonlinear fit may use fewer parameters, and specialized apparatus knowledge may
make direct identification or direct control far cheaper. The theorem does not
prove a practical or exclusive speedup over those routes.

More specifically, the following primary predecessors were checked during this
investigation:

* O. Salazar Celis, A. Cuyt, B. Verdonk, *Rational approximation of vertical
  segments*, Numerical Algorithms 45 (2007), 375--388,
  DOI https://doi.org/10.1007/s11075-007-9077-3. Its full author-hosted text
  https://medialibrary.uantwerpen.be/oldcontent/container2652/files/papers/SaCe_Cu_ea_rat_07.pdf
  expressly treats multivariate interval data and linearizes positive-denominator
  ratio inequalities. Thus noisy rational fitting through linear inequalities is
  not a new result of this investigation.
* A. Cuyt, X. Yang, *A practical error formula for multivariate rational
  interpolation and approximation*, Numerical Algorithms 55 (2010), 233--243,
  DOI https://doi.org/10.1007/s11075-010-9380-2. The full author-hosted text
  https://medialibrary.uantwerpen.be/oldcontent/container2652/files/papers/Cu_Ya_pra_10.pdf
  derives multivariate rational interpolation error by applying polynomial error
  formulas to a denominator-multiplied discrepancy, including interval data.
  The general multiplication-and-interpolation strategy is therefore also
  established. Here the source-specific positive tail gives an explicit
  uniform all-candidate bound without unknown high derivatives or small
  denominator singular values.
* A. P. Austin, M. Krishnamoorthy, S. Leyffer, S. Mrenna, J. Mueller, H. Schulz,
  *Practical algorithms for multivariate rational approximation*, Computer
  Physics Communications 261 (2021), 107663,
  DOI https://doi.org/10.1016/j.cpc.2020.107663. The publisher's primary preview
  and author-repository text describe linear-algebra and constrained
  approximation routes, including domain-wide pole exclusion through a
  semi-infinite optimization. This is a strong ordinary competitor. Its
  methods can adopt the particular nonnegative coefficient representation here.
* A. Charnes, W. W. Cooper, *Programming with linear fractional functionals*,
  Naval Research Logistics Quarterly 9 (1962), 181--186,
  DOI https://doi.org/10.1002/nav.3800090303. The ratio-to-LP transformation in
  Section 7 is classical linear-fractional programming.

These sources rule out broad priority claims about rational identification,
interval fitting, or polynomial error reduction. The precise additional
statement established here is (8)--(10), using the pinned source's determinant
structure and whole-simplex norming to close its stated finite-noisy
acquisition gap. A broader literature-clearance claim has not been established.

It also does not solve downstream global optimization for an arbitrary relaxed
rational function. The target source is concave, but a relaxed coefficient pair
need not be. A consumer must pay for its finite action menu, use the actual
source's convex optimization structure with appropriate error control, or
provide a separate global certificate. Accurate prediction alone is not a free
planning oracle.

## 9. Scope, failure modes, and honest interpretation

The result is an information-acquisition theorem with an executable ordinary LP
receiver. Its potential consequence is reusable control of an unknown passive
response under sparse experiments, including dense future commands and dark
latent paths. The warranted model and total effective dose q carry the
structure. No biological, catalytic, or hardware model is validated by this
algebra alone.

Nonempty fit does not validate the source class. Empty fit signals inconsistency
among the physical model, intervals, calibration, and data but does not identify
which failed. Fixed nonvanishing noise eventually blocks arbitrary precision,
and an infinite kappa makes this theorem unavailable. The number of physical
controls remains in binomial acquisition and LP sizes. The sufficient constants
may be much too expensive for practical use. Their magnitude is not a physical
lower bound or an invitation to label a cheap model-fitting calculation a device
breakthrough.

The decisive new mathematical object is the finite, noisy, reusable response
enclosure and its explicitly paid cost. Historical originality and useful
physical advantage remain separate questions.
