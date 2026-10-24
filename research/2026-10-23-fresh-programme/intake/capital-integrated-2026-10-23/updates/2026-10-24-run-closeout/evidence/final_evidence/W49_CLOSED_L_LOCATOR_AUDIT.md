# Independent audit of the closed-L quadratic collision locator

24 October 2026. Reviewer: W49. This is a new cold analytic reconstruction,
with an independent stdlib exact-arithmetic diagnostic. No producer code was
imported or executed. The producer's numerical replay and previous reviews
are not mathematical premises. No descendant or other worker was assigned.

## A1. Exact targets and separate verdicts

The frozen sources read in full are:

* W14 `dense_repeated/EXPLICIT_CLOSED_L_FIVE_RESTRICTION_LOCATOR.md`, SHA256
  `79d8032dbf31e76dd5951444135677851f73d6c8dcb09f99d91f05e2df32fc43`.
* Its repeated-fiber endpoint dependency,
  `EXPLICIT_AT_L_REPEATED_FIBER_EXTENSION.md`, SHA256
  `6d864d9602d53632e6882b28cee21bc39e127524a00ed0c2441e4357eee81ae2`.
* Its strict-interval dependency,
  `EXPLICIT_SUB_L_RECTANGULAR_ANNIHILATOR.md`, SHA256
  `1272c471eaa0a4947358c01140795440f3f1f077c5feaba6fac5aefdfaad9dde`.

The paths are under
`work/workers/w14_complexity_invention/dense_repeated/`.

**Simple-fiber spectral/restriction verdict:** no blocking defect found.
The selected STV restriction is specifically the side increasing the
positive constant bias. Iteration forces the collision indicator to be
ZERO. An unspecified monochromatic restriction would not suffice.

**Repeated-fiber H=L verdict:** no blocking defect found in the full
reconstruction below. The argument applies classical binary Reed--Muller
forms to the odd support, and does not apply a simple signed-trade theorem
to repeated multiplicities. The endpoint nonnegative quotient and the
positive-even outlier count both check.

**Strict H<L dependency:** reconstructed separately below; no blocking
defect found. Its structural range is n>=6; the main five-restriction source
uses its own finite-set argument for all n<=7.

**Combined closed-threshold theorem and acquisition:** internally accepted
at these exact hashes, with the classical KT/minimum-word facts stated
below as explicit imported theorems. This is an internal mathematical
audit, not external certification, historical novelty or practical speed.
No mandatory repair of the three frozen mathematical theorems was found.
The original 1970 KT full text was not retrieved; the exact forms were
checked in the accessible primary mathematical paper that explicitly
states them. This source-access limit is preserved, not hidden.

The additive-slack and fresh-chi continuations were not used or reviewed.

## A2. Model, signs and quadratic Walsh lattice

For a square map P:F2^n -> F2^n, let k(y)=#P^{-1}(y), w=k-1 and C={w>0}.
Then w is integer valued, w>=-1, and

    sum_y w(y)=0,
    H=#{w=-1}=sum_{w>0}w,
    sum_y |w(y)|=2H.

Put K=ceil(n/2), L=2^K, and W(a)=sum_y w(y)(-1)^{a.y}. At a=0, W=0.
At a!=0 the contribution of the constant -1 vanishes, so W(a) is exactly
the Gauss sum of the quadratic Boolean function a.P.

For completeness, if q is any Boolean quadratic and B its alternating
polar form of rank r, square its Gauss sum and set the two summation
arguments to x and x+h. The sum over x vanishes unless h is in rad B.
On that radical, q(h)+q(0) is linear. Therefore the squared Gauss sum is
either zero or 2^n*2^(n-r). The even rank satisfies r<=2floor(n/2).
Thus every nonzero W(a) has absolute value 2^(n-r/2), at least L and an
integer multiple of L. Arbitrary affine terms and arbitrary coordinate
ranks are included. Nothing requires all nonzero amplitudes to equal L.

With normalized Fourier coefficients, Parseval gives

    ||w||_A = 2^-n sum_a |W(a)|
             <= (L*2^n)^-1 sum_a W(a)^2
             = L^-1 sum_y w(y)^2.                         (A2)

If all fibers have size <=2, w is in {-1,0,1}; then its positive and
negative supports both have size H. Hence ||w||_A<=2H/L. In this case ONLY,

    b=1_C=(w^2+w)/2

is the actual collision indicator. Multiplication becomes convolution of
normalized Fourier coefficients, so the triangle inequality gives

    ||b||_A <= (||w||_A^2+||w||_A)/2.

Consequently H<=cL implies ||b||_A<=T=2c^2+c and
p=E b=H/2^n<=c*2^-floor(n/2). In particular c=1 gives T=3.
Using this formula for repeated fibers would be invalid; the source does
not do that. These are existence estimates, not an algorithm with free
access to b, Fourier coefficients, H or the fiber counts.

## A3. The restriction side, including a direct reconstruction

Let b be any Boolean indicator, p<1/4, and s=1-2b. Its constant Fourier
coefficient a0=1-2p is positive; each nonconstant coefficient has magnitude
at most 2p. Thus the constant is strictly largest. If b is nonzero, s is
nonconstant. Let beta be an index of a largest nonconstant coefficient,
and take the nonempty coset chi_beta=epsilon, where epsilon is the sign
of that coefficient. In quotient coordinates the new constant is

    a0+|s_hat(beta)|,

so p'<=p. Since s remains +/-1 valued, its new nonconstant coefficients
are bounded by 2p' and its constant remains strictly largest. This
justifies repeating exactly the same rule in the current quotient.

The same-side saving is not an inference from an existence-only
monochromatic-subspace theorem. It is the explicit side in primary STV
Lemma 3.1, after setting its maximal index alpha=0. I checked the proof as
well. Here is an independent coefficient argument sufficient for its
weaker published saving. Pair coefficients at gamma and gamma+beta.
The identity s^2=1 implies that the signed products over all such unordered
pairs sum to zero. The pair {0,beta} has product a0*s_hat(beta).
The pairs with opposite sign after multiplication by epsilon therefore
have total absolute product at least a0*|s_hat(beta)|. Neither of their
entries is the coefficient at zero; both have magnitude <=|s_hat(beta)|.
Their sum of minimum magnitudes is consequently at least a0. Merging a
cancelling pair loses twice that minimum from the Fourier norm; even
discarding that factor gives a saving at least a0 on the selected side.
This proves precisely the bound needed here without changing the source's
constants or making a new optimal-codimension claim.

Using S=||s||_A, the exact sign conversion is

    S=1+2||b||_A-4p.

If t restrictions have been made without stopping, their previous
constants are at least 1-2p, where p denotes the INITIAL density. Thus

    S_t<=1+2T-4p-t(1-2p),
    ||b_t||_A=(S_t-1+4p_t)/2
               <=T-t/2+(t-2)p+2p_t
               <=T-t/2+tp.                               (A3)

If T-d/2+dp<1, b_t cannot still be nonzero at t=d: a nonzero indicator
has sup norm one and Fourier norm at least one. If the quotient reaches
dimension zero earlier, its density is 0 or 1, and p_t<=p<1/4 already
forces zero. Every parity selected before stopping is nonzero in the
current quotient, so the codimension rises by one and the flat stays
nonempty. The acquired existence statement is b|T=0, not b|T arbitrary
constant. The opposite sign generally increases p; the fresh exact
control below explicitly exhibits this failure.

Primary comparison: [Shpilka--Tal--Volk, arXiv1304.0371v2](https://arxiv.org/html/1304.0371v2),
Lemma 3.1 and Section 1.4, supply the classical restriction mechanism and
its bias-preserving refinement. This audit does not attribute their
learning algorithm to the much weaker acquisition interface here.

## A4. All dimensions and the general-c qualification

For c=1, T=3. When n>=8, p<=1/16, and at d=5 the last bound in (A3) is

    3-5/2+5/16=13/16<1.

For 1<=n<=7, |C|<=H<=L<=16. Independently, any square map has
|C|<=2^(n-1), because each such output consumes at least two inputs. Pick
some y outside C for this existence proof. Sample five linear functionals
independently and take their common coset through y. For every z in C,
z+y!=0, so the probability all five constraints also admit z is 1/32.
The expected number of such z is at most 16/32<1. Some sampled tuple
therefore excludes all of C. The tuple need not be linearly independent:
its rank is at most five and its common coset through y is nonempty. This
works in dimensions less than five as well. This is not a free randomized
algorithm for finding y; acquisition is addressed in A9. For n=0, there
is one input and the sole output bit can simply be flipped.

For integer c>=1 let T=2c^2+c, d=2T-1 and q=ceil(log2(4cT)). When n>=2q,
p<=1/(4T), and the bound is 1-1/(4T)<1. In smaller n, the inequality
4cT<=2^(2T-1) implies q<=d. One proof uses T>=3c and
(4/3)T^2<=2^(2T-1) for integer T>=3, starting at T=3 and inducting.
Then n<2q implies d>=ceil(n/2), and

    sum_{i<=min(d,n)} binom(n,i)>2^(n-1)>=|C|.

Linear algebra therefore yields a nonzero degree-d annihilator. This
small-n general-c argument does NOT factor that annihilator into d affine
forms, and the source correctly does not claim a codimension-d flat from
it. The actual all-dimension flat result used by the main theorem is c=1.
If c is a variable input, the displayed acquisition costs are polynomial
in M_d, not claimed polynomial in n and log c. With c fixed the degree is
a specified constant. Capped arithmetic can read c and compute min(d,n)
without constructing a needlessly huge unbounded integer.

## A5. Imported classical low-weight facts and their scope

For the repeated/strict arguments put m=n-K. A nonzero Boolean function of
degree at most m has weight at least L; a minimum word is an affine K-flat
indicator. Between weights L and 2L the literal KT forms give:

1. Type A is the XOR of two K-flat indicators with common fixed factors.
   For 2<=mu<=m it has weight 2L-2^(K+1-mu) and hull dimension <=K+mu.
2. Type B has m-2 common affine coordinate factors and an even-rank
   quadratic factor with nu>=3 pairs. Its hull dimension is <=K+2;
   counting that quadratic gives weight 2L-2^(K+1-nu)>=7L/4.

These consequences were reconstructed from the literal forms, including
the first nonminimum weight gap 3L/2. The low-weight classification itself
is a classical imported theorem, not re-proved by this audit or the
finite controls. I read [Ghorbani--Kamali--Khosrovshahi--Krotov,
arXiv1810.02296v2](https://arxiv.org/html/1810.02296v2), Lemma 11 and its
parameters, and checked the minimum-word theorem and proof in [Leducq,
arXiv1001.2554](https://arxiv.org/html/1001.2554), Theorem 1. For q=2 the
latter's parallel-hyperplane description is precisely one affine flat.
KT's 1970 DOI is 10.1109/TIT.1970.1054545, as identified in the primary
paper's bibliography. Its original full text was not obtained through the
available retrieval route. The minimal-word predecessor is Delsarte,
Goethals and MacWilliams, 1970; Leducq provides a primary new proof.

Only binary support classification is used here. In particular the later
exclusion of Type B for simple signed trades is NOT imported: w may have
repeated positive multiplicities, and U is only its simple binary odd
support. Nor are strict KT forms used at weight exactly 2L.

## A6. Odd support, affine-origin quotient and positive idempotence

For both structural dependencies, W is divisible by L. Expand integer w
in the unique integer multilinear monomial basis. The coefficient on S is

    (-2)^|S| * 2^-n * sum_{a contains S} W(a).

It is even for |S|>n-K, because the total displayed power of two then
has exponent at least one. Reducing that integer expansion modulo two
proves that 1_U, U={w odd}, has Boolean degree <=m. All holes lie in U.
Mass balance gives the exact identity

    2H-|U|=2 sum_{w>0} floor(w/2).                         (A6)

Take O=aff U=b+V, translate b to the quotient origin, and sum w over each
V-coset to obtain p(t). Every negative entry is in O; hence p(t)>=0 for
t!=0, p(0)=-Pout and Pout<=H. Its Walsh coefficients are the restrictions
of W, with only the harmless signs caused by that affine origin, and

    W_p(a)=sum_{t!=0}p(t)(chi_a(t)-1)<=0.                  (A7)

In the ternary case W in {0,+/-L}, (A7) forces W_p in {0,-L}. Therefore
nu=delta_0+p/L has total mass one, is nonnegative whenever H<=L, and has
Fourier coefficients only zero or one. This includes the endpoint where
the preliminary lower bound on nu(0) is merely zero.

Here is the finite-group lemma used without assuming nu(0)>0. For a
probability with Fourier values zero or one, any character with expected
value one equals one at every support point. Those characters form a
subgroup D. All other Fourier coefficients vanish; inversion makes nu
the uniform distribution on D's annihilator T. In particular 0 belongs
to its support and, if h=dim T,

    nu(0)=2^-h>0,  Pout=L(1-2^-h).                        (A8)

For every quotient cell outside T the marginal is zero. Its entries are
nonnegative since it is not the base cell, so every such entry of w is
zero. All defect lies in the preimage of T; its affine hull has dimension
at most dim O+h. No uniformity within a cell was inferred.

All positive odd points are in O and consume at least one unit each of
the positive mass H-Pout there. Thus the sharper coupling is

    |U|=H+#{positive odd points}<=2H-Pout.                 (A9)

This also makes explicit why silently replacing C by a subset of U would
be wrong: positive even entries are outside the parity support.

If U is minimum, write U=B, an affine K-flat, and phi=w+1_B. It is
nonnegative and even, has mass L and has Walsh coefficients divisible by
L. Positivity bounds them by L, so phi/L is a probability with Fourier
coefficients in {0,+/-1}. Its modulus-one characters are constant on the
support, with consistent signs; translation by one support point reduces
this to the previous subgroup lemma. Hence phi=q1_A for an affine flat A.
The constant q=L/|A| is a positive EVEN integer, so q>=2 and dim A<=K-1.
Then w=q1_A-1_B has positive set EXACTLY A, including if A and B meet.
Thus C is contained in a proper affine flat. At H=L they are in fact
disjoint by counting B\A, but that extra observation is not required.

## A7. The strict H<L structural dependency

If H=0, P is bijective and C empty. If 0<H<L, |W|<=2H<2L and Walsh
divisibility gives the ternary case. By (A6), 0<|U|<=2H<2L, so A5 applies.
For a nonminimum U with h>=1, (A8)--(A9) would give

    3L/2<=|U|<=2H-L/2<3L/2,

a contradiction. The minimum case was handled above. Otherwise h=0 and
all defects lie in O. A proper O yields a linear collision annihilator.

If O is full and n>=6, K+2<n excludes Type B. In Type A, n<=K+mu and
mu<=m=n-K force mu=m. Its weight is 2L-2 for even n and 2L-4 for odd n.
Because H<=L-1, (A6) leaves respectively zero or at most two units of
excess. There are therefore zero or at most ONE positive even point
outside U. Every positive odd point is already in U. Write U=F1 triangle
F2 for the KT K-flats, and enlarge F1 by that possible point. The enlarged
flat has dimension <=K+1; together with F2 it has at most 3L<2^n points.
Choose z outside both. For each flat there is an affine functional zero
on it and one at z. Their product is a nonzero degree<=2 annihilator of C.
Moreover their common one-coset is a noncollision flat of codimension <=2.
This proves exactly the n>=6 range needed here; it does not attribute an
unproved small-n two-flat theorem to the strict source's finite fallback.

## A8. The repeated-fiber endpoint H=L

Here |W|<=2L. If |W(a)|=2L for any a, then a!=0 and equality in the
triangle inequality forces sign(w(y))=sigma*chi_a(y) at every defect.
All positive defects lie in one proper hyperplane, yielding a linear
annihilator and the opposite noncollision coset.

Otherwise W is ternary. A fiber of size >=3 means some positive w>=2,
so (A6) gives 0<|U|<2L. Thus exactly the strict classical low-weight
classification is now applicable, despite the repeated fibers. The
minimum case is already A6. For nonminimum U with h>=1, (A8)--(A9) give

    3L/2<=|U|<=L+L2^-h<=3L/2.

Every inequality is equality: h=1 and |U|=3L/2. By the literal forms this
is Type A with mu=2, since Type B's weight is at least 7L/4. Therefore
dim O<=K+2 and whole-defect hull dimension <=K+3<n for n>=8. A linear
annihilator again suffices. This is a dimension bound for the containing
flat, not a claim about the value distribution of w within it.

For h=0 every defect is in O. If O is proper we are done. If O is full,
Type B is impossible since K+2<n. Type A again has mu=m, so |U| is
2L-2 (even n) or 2L-4 (odd n). The budget (A6), now with H=L, permits
at most ONE or TWO positive-even points outside U, respectively. Large
positive odd entries consume budget but lie inside U already. Enlarge
one of the two KT K-flats by ALL such outliers. Its dimension is <=K+2;
the total cover has at most 5L<2^n points, with both flats proper for
n>=8. The same two affine separators produce a nonzero quadratic
annihilator and an actual nonempty codimension-at-most-two flat avoiding
C. No polynomial is assumed to factor merely from its degree; these
two factors come from the proved geometric cover.

For all n<=7, whether fibers are simple or repeated, |C|<=H<=16 and
A4 gives the required codimension-five flat directly. Combined with A3,
A7 and the H=0 case, this proves the main closed-threshold flat existence
for ALL square quadratic maps with H<=L, with no fiber-rank promise.
Existence of an all-size family realizing each abstract endpoint profile
is neither needed for this implication nor inferred from it.

The unresolved stronger degree-two SIMPLE endpoint remains outside this
argument: its odd support can have weight 2L and full hull, where the
strict KT classification above is unavailable. The degree-five STV bridge
bypasses that obligation; it does not resolve it by classifying that case.

## A9. Actual acquisition with one ordinary NP language

Let d=5 and M=sum_{i<=min(d,n)} binom(n,i). Use all squarefree monomials,
including the constant, and let v_d(y) be their evaluation vector. Start
with zero span E. At each feature stage ask whether there are INPUTS
u!=v such that P(u)=P(v) and v_d(P(u)) is outside E. Checking this is in
P once the 2n witness bits, explicit circuit and physically padded M-by-M
row field are supplied. An ordinary existential prefix query self-reduces
each YES in at most 2n further decisions. Keep the actual source point
P(u), as well as its independent reduced row.

Each YES raises rank by one. If rank becomes M, abort that projection:
then no nonzero degree<=d polynomial can annihilate all collisions, so
there is certainly no nonempty codimension-d flat avoiding them.
Otherwise a terminal ordinary NO means EVERY collision point's feature
is in E. This is complete acquisition through actual witnesses. Branching
on a NO answer of the NP oracle is allowed in a deterministic FP^NP
computation; no universal condition is silently put inside an NP verifier.
Completeness of E is not supplied as advice.

For the word-only route, obtain a nonzero coefficient vector R in the
orthogonal complement of E by GF2 elimination. To find a point with R=1,
take an inclusion-minimal monomial in its support, put precisely those
variables to one, and all others to zero. No other supported monomial is
a proper subset; larger or incomparable monomials evaluate to zero.
Thus R evaluates to one. If its point were a collision, its acquired
feature in E would instead give zero, a contradiction.

For the actual FLAT route, guess five affine functions ell_i. Their
Boolean product has degree <=5 after squarefree reduction. It is nonzero
if and only if the five equations ell_i(y)=1 are consistent, a deterministic
GF2 linear-algebra test. To test that this product annihilates E, it
suffices to evaluate it at the saved source points, because their feature
vectors span E. This is a polynomial verifier on a guessed 5(n+1)-bit
word. Explicit multiplication and row dot products give the same test.
The oracle is not asked to check all outputs or count collisions. A
prefix self-reduction extracts all factor bits. Solve the five equations
to return a base and direction basis; pad a smaller-codimension flat
with constant-one factors. Conversely every such nonempty flat has this
representation. A factor-query NO, or full feature rank, is therefore an
EXACT rejection of this geometric class for that arbitrary projection.
It is not a decision of H<=L or of quadraticity.

At any selected noncollision point y, ordinary NP preimage existence and
n-bit prefix extraction find its unique preimage if present. If absent,
either removed-bit extension is missing from F. If present, flip the
removed bit at that unique input. The resulting rectangular word cannot
be in the image. The output bit is inserted at its ORIGINAL coordinate j.
All n+1 projections are actually enumerated, and the successful one is
not supplied. The removed output bit g_j need not be quadratic. Indeed
the entire procedure is sound on arbitrary circuit inputs; only semantic
completeness uses a good quadratic projection with H<=L.

The append/flip mechanism is classical. I checked Definition 2.4 and the
proof of Theorem 3.1 in the retained primary Chung et al. TR23-193 revision
1, PDF SHA256
`28ee7a65f41ea0825aabfd1894d7119b9e19faa63ad620ae046605407279c4f2`.
The [official ECCC record](https://eccc.weizmann.ac.il/report/2023/193/)
identifies that revision. Direct remote revision-PDF retrieval timed out;
the locally retained primary text was read. No claim of a new append/flip
reduction is appropriate.

## A10. Query, serialization and outside-time accounting

At most M feature YES stages occur; with full-rank abort, even including a
terminal NO the feature decisions are bounded by (2n+1)M. Inversion uses
at most n+1 decisions, so the source's safe word-only cap is

    (2n+1)M+n+2.

For a flat, add one factor-existence decision and at most 5(n+1) prefix
decisions. Together with inversion this is below the stated safe cap

    (2n+1)M+6n+8.

Multiply by n+1 for all coordinate deletions, irrespective of the promise.
Every matrix has M physical rows and M columns from the FIRST query;
source-point and prefix fields are also physically bounded. Standard
GF2 span membership and the explicit circuit verifiers are polynomial in
their actual query lengths. Query bits are

    O(S_F+M^2+n^2),

and the generous outside-work cap

    O((n+1)(S_F+n+1)^4(M+1)^4)

dominates feature enumeration, all adaptive query serialization, exact
row elimination, point-list checks, factor processing and inversion.
For fixed d=5, M=O((n+1)^5), this is uniform FP^NP. Dense quadratic
F has S_F=O((n+1)^3); the displayed caps give O((n+1)^7) decisions and
O((n+1)^33) outside bit work. Oracle solving time is not a polynomial
ordinary-time bound. No numerical structural Cohen constant, count oracle,
Fourier table, random membership access to C or stronger promise oracle
is included. The five-restriction theorem is an explicit degree cap,
not an acquisition-free structural classifier.

## A11. The actual strict-class control at n=11

For P ignoring x0 and outputting (q(x1,...,x10),x1,...,x10), every image
fiber has size two. The image graph C has size 2^10; H=2^10 greatly
exceeds L=2^6. Its complement is the level h=1 of
h(y)=y0+sum_{i=1}^5 y_(2i-1)y_(2i).

The polar form has rank ten and one-dimensional radical span(e0), along
which h changes by one. A constant-h affine flat has isotropic direction
space W. If dim W>=6, its projection to the ten-dimensional symplectic
quotient forces W to contain the radical, since the quotient's isotropic
dimension is at most five. But translation by that radical vector changes
h, a contradiction. Thus every constant-h flat has dimension <=5, while
codimension <=5 in dimension eleven would require dimension >=6.
So the exact factor-class recognizer rejects this projection, although
the obvious quadratic h annihilates C and the word-only A2 class succeeds.
This is an easy actual separation of two acquisition classes, not hardness
of Avoid, not a claim that every coordinate projection fails, and not a
finite E5 acquisition replay performed in this audit.

## A12. Fresh diagnostics and what they do not establish

`check_walsh_locator_independent.py` uses Python integers/Fractions only,
with fixed RNG seed and no imports of sibling or producer implementations.
It passed:

* all 709 Boolean indicators on dimensions 0 through 4 with density <1/4,
  checking the selected restriction, exact saving, monotone bias, norm
  iteration, actual affine parametrization and final ZERO values;
* 60 abstract disjoint-three-flat controls in dimensions 8,9,10, with
  Fourier norm <=3 and density 3/64, again returning actual zero flats;
* 644 actual square quadratic maps through dimension eight, including all
  such maps in dimensions one and two, checking the Gauss-lattice,
  Parseval/norm bounds and every component Gauss sum directly;
* 52 small-map acquisitions using ONLY explicit existential INPUT-pair,
  prefix and preimage predicates, with 1,198 simulated ordinary decisions,
  actual feature rows, an extracted kernel point and a valid flipped
  rectangular missing word in every case;
* 2,000 exact integer-c constant checks, including the small-n feature
  dimension bound.

Across the Boolean controls, 804 restriction steps were checked. One
opposite-side witness starts at density 1/8 on eight points and becomes
1/4 on the wrong parity side, so preservation of the correct sign is a
meaningful tested distinction. Among the finite actual maps, 54 simple
and 52 repeated H=L endpoints occurred. No large-instance endpoint family
is inferred from that count. The abstract three-flat indicators are not
asserted to be quadratic collision profiles.

The diagnostic's truth-table backend is exponential, uses acquired
truth only as TEST DATA, and does not implement a polynomial-time ordinary
NP solver. The factor-search verifier and its all-input correctness are
proved in A9; this new replay does not claim a fresh full factor-NP solver
or the producer's Z3 run. Runtime was about 1.20 seconds and peak RSS was
21,954,560 host units (macOS bytes). These are finite execution costs, not
the theorem's oracle cost or an advantage over equally informed methods.
Raw data are in `INDEPENDENT_WALSH_LOCATOR_CHECKS.json`; the exact source
hash is embedded there. No tests substitute for STV, KT or A6--A10.

## A13. Boundaries and next falsifiers

The internally reconstructed result is a uniform specified-degree
FP^NP locator for a conditional quadratic near-square promise, with
an actually acquired codimension-five noncollision flat. The promise is
not recognized. Degree-two acquisition for the full simple endpoint is
still open in these sources. General quadratic Avoid, ordinary-time
efficiency, historical priority, external review and practical value
remain UNKNOWN or NOT_ACHIEVED as appropriate.

The decisive potential falsifiers were: a saving restricted to the wrong
side, failure of the positive endpoint quotient, an even-defect point
outside the claimed cover, assuming a kernel polynomial factors, or
putting a universal completeness test into the NP verifier. Each was
checked explicitly above; none produced a blocker at the frozen hashes.
No square-hole/count/full-fiber-profile guarantee, generic P-versus-NP
claim, physical operation, public disclosure or equipment experiment is
part of this audit.
