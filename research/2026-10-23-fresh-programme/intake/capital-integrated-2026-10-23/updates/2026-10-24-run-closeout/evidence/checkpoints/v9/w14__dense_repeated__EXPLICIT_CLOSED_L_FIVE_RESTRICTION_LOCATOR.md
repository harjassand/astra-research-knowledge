# Explicit closed-threshold quadratic Avoid by five parity restrictions

Version 1, 23 October 2026. New continuation; fresh independent review is
PENDING. No wrapping peer or new worker has been assigned another task.
The strict-threshold proof1272c471 and all audited packets remain unchanged.
Historical priority, external correctness, ordinary-time advantage, and
practical value are UNKNOWN. Generic quadratic Avoid is NOT_ACHIEVED.

## 1. Exact statement and what is acquired

Let F:F2^n -> F2^(n+1) be an explicit circuit. For each coordinate j let P_j
be its square coordinate projection, and let g_j be the removed bit. Suppose
SOME actually enumerated P_j is quadratic and has

    H(P_j) <= L = 2^ceil(n/2).                                  (1)

All coordinate ranks and all fiber sizes are permitted. No H, successful
projection, fiber bound, structural cover, annihilator, Fourier table, or
advice is supplied. There is a NUMERICALLY SPECIFIED uniform deterministic
FP^NP locator, using the fixed degree D=5, which returns a missing output of
F under(1). Every success is sound for arbitrary circuits, and every input
has the same explicit clock/query caps. Numerical condition(1) is NOT being
recognized. No square-hole, exact-count, or full-profile guarantee follows.

A slightly stronger version ACTUALLY acquires a nonempty affine flat T of
codimension at most5 disjoint from the collision set of its successful
projection, returning a base and direction basis. Every y in T has AT MOST
ONE square preimage. T may contain square holes as well as singleton outputs.
This version exactly recognizes existence of such a flat for an individual
arbitrary circuit projection; it does not recognize(1).

The new spectral bridge covers the entire SIMPLE regime

    maxfiber(P)<=2, H(P)<=cL,

with the explicit degree d=4c^2+2c-1 for every positive integer c. The closed
threshold(1) combines c=1's degree5 bridge with the separate repeated-fiber
endpoint proof6d864d96, stated and checked separately in Section5 below.
The degree2 claim for every simple H=L input remains OPEN here: this argument
does not classify minimal twice-minimum Reed--Muller supports.

## 2. Normalization and a direct quadratic spectral estimate

For one square P put w(y)=|P^-1(y)|-1, C={w>0}, H=#{w=-1}, and

    W(a)=sum_y w(y)*(-1)^(a.y).

Use normalized Fourier coefficients hat h(a)=2^-n sum_y h(y)chi_a(y), and
||h||_A=sum_a |hat h(a)|. Thus W=2^n hat w and W(0)=0. At nonzero a,
W(a)=sum_x chi_a(P(x)) is a quadratic Gauss sum. Alternating polar rank is
even and at most2floor(n/2), so every nonzero W(a) has magnitude at least L.
This uses arbitrary coordinate ranks and does not require ternary Gauss
values. Parseval therefore gives

    ||w||_A =2^-n sum_a |W(a)|
             <=(L*2^n)^-1 sum_a W(a)^2
             =sum_y w(y)^2/L.                                (2)

If all fibers are at most two, w is0,+1,-1 and sum w^2=2H. Thus under H<=cL,

    ||w||_A<=2c.

The true collision indicator is b=(w^2+w)/2, a Boolean0/1 function. Fourier
norm is submultiplicative, so

    ||b||_A <= (||w||_A^2+||w||_A)/2 <= T=2c^2+c.              (3)

Its density p=E b is exactly H/2^n in this simple regime, and

    p<=c*2^-floor(n/2).

Equations(2)--(3) are analytic existence bounds only. The algorithm neither
evaluates b at arbitrary points nor counts fibers nor computes its Fourier
coefficients. They are used solely to prove a degree cap for actual NP
feature acquisition.

## 3. One-sided restriction lemma with explicit constants

Lemma. Let b:F2^n->{0,1} have density p<1/4 and ||b||_A<=T. If a positive
integer d satisfies

    T-d/2+d*p<1,                                              (4)

there is a nonempty affine flat of codimension at most d on which b=0.

Proof. Write s=1-2b. Its constant coefficient is1-2p, every nonconstant
coefficient has magnitude at most2p, and therefore the constant is strictly
largest. Moreover

    ||s||_A=1+2||b||_A-4p<=1+2T-4p.                          (5)

If b is nonzero then it is not constant, since p<1/4. Let beta be a largest
nonconstant coefficient of s. Restrict to the parity coset on which
chi_beta=sign(hat s(beta)). The constant coefficient becomes
1-2p+|hat s(beta)|, so the restricted collision density decreases, remains
at most p, and the constant coefficient remains strictly largest.

Shpilka--Tal--Volk's main restriction lemma gives a Fourier-norm reduction
at least the previous largest coefficient, hence at least1-2p, on THIS same
coset. This is their Lemma3.1 with alpha=0, not a claim that a merely
existential monochromatic coset is necessarily the zero one. Each chosen
parity is nonzero in the current quotient, so the affine coset is nonempty
and codimension increases by one. If b becomes zero sooner, stop.

After t restrictions, if still nonzero, write p_t<=p for its density. By(5),

    ||s_t||_A<=1+2T-4p-t*(1-2p),
    ||b_t||_A=(||s_t||_A-1+4p_t)/2
              <=T-t/2+(t-2)*p+2p_t
              <=T-t/2+t*p.                                  (6)

At t=d equation(4) would make ||b_t||_A<1, impossible for a nonzero Boolean
indicator because ||h||_infinity<=||h||_A. Thus it became zero within d
steps. If the current dimension becomes zero earlier, its density bound
already forces b=0. This proves the lemma.

Primary source, read directly: Amir Shpilka, Avishay Tal, Ben lee Volk,
On the Structure of Boolean Functions with Small Spectral Norm,
arXiv1304.0371v2 (22 May2013), Lemma3.1 and its proof, Sections3.1--3.2:
https://arxiv.org/html/1304.0371v2 . The saving side and preservation of the
largest coefficient are also discussed in Section1.4, crediting the
independent Tsang et al. refinement. This is CLASSICAL Fourier restriction
machinery; only its exact one-sided acquisition application is developed
here. We do not silently apply a0/1 theorem with an uncharged sign conversion.

Retained primary PDF: primary/Shpilka_Tal_Volk_1304_0371v2.pdf,
SHA2568d1df8814ffdde75a6d9cf34535248cf4833ab7c35c735c71d13f0792fd0038a;
text SHA2564583ca3d71763f7a942c7ba4eff52b9c5fa695b0f85fa627aed0cb50aea7c3ea.

## 4. Fully numerical simple-fiber theorem, all dimensions

For c=1, T=3. At n>=8, p<=1/16 and

    T-5/2+5p<=1/2+5/16=13/16<1.

Thus the collision set misses a nonempty codimension-at-most-five affine
flat. For n<=7, |C|=H<=L<=16. Any set of at most16 points has a nonempty
codimension-at-most-five affine flat in its complement: choose y outside
C, choose five independent random LINEAR forms (independence is not needed),
and use the coset through y. For each z in C, the probability that all five
forms vanish on z+y is2^-5, so a union bound is at most16/32<1. Some choice
misses C. Its normal rank can be smaller than five, which is allowed.
The phrase 'independent random forms' refers to independent samples, not
an assumed linearly independent five-tuple in small n. A y outside C exists
since every square map has |C|<=2^(n-1). Empty C gives the whole cube.
The n=0 case directly flips the single output bit.

Hence EVERY simple square quadratic with H<=L has an actual noncollision
flat of codimension at most5, in ALL dimensions. No enormous finite fallback
or unextracted Cohen constant occurs.

More generally put T=2c^2+c, d=2T-1 and q=ceil(log2(4cT)). If n>=2q,
p<=1/(4T), so T-d/2+dp<=1-1/(4T)<1. The restriction lemma gives codim<=d.
If n<2q, the elementary inequality4cT<=2^(2T-1) gives q<=d: use T>=3c,
4cT<=(4/3)T^2<=2^(2T-1) for integer T>=3, the last inequality following by
induction from T=3. For the LOW-DEGREE annihilator version, the small-n
conclusion is immediate: d>=q>=ceil(n/2), so the degree-d monomial space has dimension
strictly larger than2^(n-1)>=|C|. Thus a nonzero degree-d annihilator exists.
The general-c claim in Section1 is this annihilator claim. The stronger
codimension-d flat statement for general c is asserted here only in the
large-n branch; no unjustified factorization of an arbitrary small-n kernel
polynomial is used. For c=1 the preceding16-point argument proves the actual
codimension-five flat in every dimension.

## 5. Repeated fibers at the exact endpoint: separate dependency

The prior strict theorem1272 proves a two-flat collision cover for all H<L.
For H=L and some fiber>=3, the proposed frozen endpoint proof
EXPLICIT_AT_L_REPEATED_FIBER_EXTENSION.md,
SHA2566d864d9602d53632e6882b28cee21bc39e127524a00ed0c2441e4357eee81ae2,
establishes the same proper two-flat cover for n>=8. Its independent review
is PENDING; this dependency is not promoted by the earlier strict audit.

For completeness, its precise argument is: a Gauss amplitude2L saturates
triangle inequality and confines C to one hyperplane. Otherwise W is0,+/-L;
the repeated fiber makes the odd support U have weight strictly below2L.
Classical strict Kasami--Tokura forms apply to U. Aggregate w by aff U;
positive idempotence and W59's coupling give |U|<=L+L2^-h for quotient rank h.
Minimum U confines C to an affine flat. Nonminimum h>0 forces h=1,
|U|=1.5L and whole hull dimension<=K+3<n. For h=0 all defects lie in aff U.
If that hull is full, the TypeA support consists of two K-flats, up to their
intersection; its weight is2L-2 in even n and2L-4 in odd n. The exact excess
2H-|U|=2sum_(w>0)floor(w/2) permits at most one or two positive-even outlier
points. Enlarge one K-flat by those points. Its union with the other flat
has size at most5L<2^n for n>=8. One affine separator per flat gives a
nonempty codimension-at-most-two noncollision flat. The TypeB hull bound
K+2<n excludes that case from a full hull. All even positive outliers are
charged; C is NOT silently assumed contained in odd support.

For n<=7, repeated fibers also have |C|<=H<=16, so the same finite-set union
bound gives a codimension-at-most-five flat. Thus, conditional only on the
fully written endpoint derivation being correct, ALL quadratic square maps
with H<=L have such a flat. No claim is made that the exact repeated endpoint
has an exhibited all-size actual realization. The proof remains meaningful
without inferring such realizability.

## 6. Actual ordinary-NP acquisition and complete costs

Let M_5=sum_(i=0)^min(5,n)binom(n,i). Acquire E_5, the complete F2 span of
degree-at-most-five monomial evaluation vectors of collision OUTPUTS, using
actual INPUT pairs u!=v with P(u)=P(v) and v_5(P(u)) outside the current span.
Each YES is self-reduced using2n prefix bits, then contributes an independent
row. Keep its original source point y as well as the reduced row basis.
At most M_5 YES stages occur; full rank aborts before further work. A terminal
ordinary NO certifies completeness. All M_5 slots and the full padded
M_5-by-M_5 field are physically encoded from the first query.

For a missing word alone, a nonzero kernel polynomial is actually obtained
by P linear algebra. Set to1 an inclusion-minimal supported monomial and
set all other variables to0; that point evaluates to1. It is therefore a
noncollision output. Ordinary NP preimage existence, followed by n prefix
decisions at YES, gives either an empty square fiber or its unique preimage.
Apply the CLASSICAL append/flip operation to g. This returns a rectangular
hole. Chung et al. TR23-193 revision1 Definition2.4/Theorem3.1 is explicitly
credited; the operation itself is not new.

For the actual FLAT output, ask a further ordinary NP relation for FIVE
affine forms ell_1,...,ell_5 whose Boolean product is nonzero and annihilates
E_5. Guess5(n+1) coefficient bits. Nonzero product is a P consistency test
for ell_i(y)=1, all i. Since the saved source evaluation vectors span E_5,
orthogonality is equivalently the P check

    product_i ell_i(y_j)=0 for every saved source point y_j.   (7)

Thus the verifier needs no universal all-output test, threshold classifier,
counting, proper representation, or nested oracle. Alternatively it can
explicitly multiply five squarefree affine polynomials in M_5 slots and
test all row inner products. Verify in P that the source features span the
public E_5 if desired. There are at most M_5 source points, physically padded.
An affine flat of smaller codimension is represented by constant-one forms.
Prefix extraction costs at most5(n+1) additional decisions. Solve the five
equations to return T's actual base and direction basis. A NO is an exact
rejection of this codimension-five-flat class for the projection. An arbitrary
kernel polynomial is never assumed to split.

The safe SINGLE-projection caps are

    word only: (2n+1)M_5+n+2;
    word plus actual flat: (2n+1)M_5+6n+8.                    (8)

Trying all n+1 coordinate deletions pays the factor n+1 and actually restores
the removed bit at its original position. No unknown good projection is
received for free. On all inputs, query bits are

    O(S_F+M_5^2+n^2)=O(S_F+(n+1)^10),

and safe total outside bit work is

    O((n+1)(S_F+n+1)^4(M_5+1)^4).

For dense quadratic F with S_F=O((n+1)^3), this is O((n+1)^33); decisions
are O((n+1)^7). These conservative bounds include self-reduction, feature
enumeration, exact GF2 algebra, point lists, product checks and serialization.
One fixed ordinary NP decision language handles all tagged predicates.
No SAT solver running-time assumption or promise oracle is hidden. For an
input c, clip d to n before feature enumeration and pay its binary reading
cost; the general-c word-only theorem uses the same formulas with M_d.

## 7. Status and next falsifiers

The acquired codimension-five class is STRICT on actual quadratic maps.
For n=11 let P ignore input x0 and output

    (x1*x2+x3*x4+x5*x6+x7*x8+x9*x10, x1,...,x10).

Its collision set is exactly its quadratic image graph; all image fibers
have size two and H=2^10, whereas L=2^6. The complement is the1-level of
h(y)=y0+sum_(i=1)^5 y_(2i-1)y_(2i). Its polar rank is10, with radical
span(e0), and translation by e0 flips h. A constant-h affine flat has an
isotropic direction space. An isotropic space of dimension6 must contain
the radical (the nondegenerate quotient has maximal isotropic dimension5),
which would make h nonconstant. Therefore every constant-h flat has
dimension at most5, while codimension at most5 would require dimension6.
The factor acquisition correctly rejects this actual input. Ordinary A_2
still succeeds using the displayed quadratic graph relation. This is the
same matched easy obstruction as the earlier codimension-two control,
generalized to five; it is not Avoid hardness. No expensive actual complete
E_5 replay for this11-bit NO control is claimed here.

The primary restriction lemma is classical and numerically explicit. This
new bridge does not depend on the unextracted Cohen count, a supplied Fourier
table, membership access to C, or a free structural classifier. The complete
endpoint theorem still has the stated unreviewed repeated-case dependency.

Finite controls must independently check: Gauss-lattice norm bound(2), the
SAME saving side increasing positive bias, every strict inequality in(6),
actually acquired collision features, actually extracted factor coefficients,
every returned flat point, and the restored rectangular missing word. Dense
row padding is checked from the first decision. Truth tables used by a
finite oracle backend are diagnostic/backend data, not supplied learner
inputs. Such replays do not replace the all-size proof or establish novelty.

Companion finite replay:44 actual projections through n10,8,102 simulated
ordinary decisions,1,242 actual Z3 calls on the factor P-verifier, and13
actual all-coordinate runs with2,535 further decisions. It includes six
simple H=L cycle/conjugate controls and three actual repeated H=L controls
in small dimensions only. All final flat points and missing words are
checked against full truth.707 exact Boolean restriction controls and1,000
integer-c scalar checks pass.25 separate full-affine-hull, low-density
three-flat Boolean controls test the restriction lemma; their realization
as quadratic collision profiles is explicitly NOT ASSERTED. The old
exponential pair/preimage backend remains exponential. The new factor
backend solves only the fully specified P verifier on ACTUALLY acquired
points; its finite speed is not an all-size algorithmic bound.
