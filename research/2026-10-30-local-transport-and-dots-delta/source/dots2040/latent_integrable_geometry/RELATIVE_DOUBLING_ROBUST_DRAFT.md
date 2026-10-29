# Working draft: robust relative doubling without a pivot promise

**Status (2026-10-29).** Proposed quantitative adaptation of classical
Brill–Noether / Couveignes–Edixhoven approximate divisor arithmetic. This is
NOT an accepted full arithmetic theorem, an implementation receipt, or a new
integrability formula. The norm and local-zero lemmas below are elementary
proofs submitted to independent review. Global root bookkeeping, the complex
inverse collar, and a full bit-complexity audit remain obligations.

Companion: `PERIODIC_TODA_CONDITIONING_BRIDGE.md` proves the physical Abel
Jacobian and inverse-spectral condition bounds. Its acceptance scope does not
extend automatically to this file.

## 1. Exact relative operation in a small explicit section space

Let C: y²=F(x), F monic squarefree of degree 2g+2 with real roots in [−M,M],
minimum separation Delta>0. Let I=∞_++∞_−. A physical divisor D contains one
point on each real gap oval. Fix a physical D0. Relative doubling seeks the
unique physical E satisfying E~2D−D0. This is the usual Jacobian group law with
origin D0, not a new time-doubling identity.

Put S=2D+iota(D0), degree 3g, where iota(x,y)=(x,−y). The vector space

    L(2g I) = {f=A(x)+y B(x): deg A<=2g, deg B<=g−1}

has dimension 3g+1. A nonzero f vanishing at S has section-zero divisor

    Z(f)=S+T,     deg Z(f)=4g, deg T=g,
    T~2g I−S~iota(E).

Zeros here include infinity with the multiplicities of the section of O(2g I),
even if the rational function has fewer actual poles. Physical nonspeciality
implies dim L(2g I−S)=1. This exact statement does NOT imply a safe pivot for the
naive evaluation matrix: repeated points require jets; near-coincident rows can
be arbitrarily close even though the represented divisor problem is nonspecial.

## 2. A quantitative algebraic norm lemma (no pivot involved)

Normalize max coefficient |(A,B)|=1. Write R=A²−F B², degree<=D=4g, and
r=||R||_1. R is nonzero because squarefree F is not a rational-function square.
At every branch root E_l,

    |A(E_l)|²=|R(E_l)|<=r M_+^(4g),   M_+=max(1,M).

Interpolate A at any 2g+1 distinct branch roots. Lagrange numerator coefficients
are bounded by (1+M)^(2g), denominator by Delta^(−2g). Consequently

    ||A||_infty <= K_A sqrt(r),
    K_A=(2g+1) ((1+M)/Delta)^(2g) M_+^(2g).

Thus ||A²−R||_1 <= K_C r, where K_C=(2g+1)² K_A²+1. On |z|=L=2M+1,
|F(z)|>=1 and

    |B(z)|²=|(A²−R)(z)/F(z)|<=K_C r L^(4g).

Cauchy's coefficient bound gives ||B||_infty<=sqrt(K_C)L^(2g)sqrt(r).
Normalization therefore forces

    ||R||_1 >= eta := min(K_A^(−2), K_C^(−1)L^(−4g)).

The deliberately loose bound has log(1/eta)=poly(g,log M,log(1/Delta)). It
handles complex coefficients and leading-coefficient cancellation. No promise
about an evaluation minor or a norm-polynomial leading coefficient is used.

## 3. Same-sheet residual-to-zero lemma

Elementary analytic statement: h is holomorphic on the unit disk, |h|<=U,
and some Taylor coefficient c_k, k<=K, satisfies |c_k|>=u>0. If h has no zero in
|z|<rho<=1, Harnack applied to log(U/|h|) on that disk and Cauchy on rho/2 give

    u <= (2/rho)^K U^(2/3) |h(0)|^(1/3).

Therefore

    |h(0)| < u³ U^(−2) (rho/2)^(3K)

forces an actual zero in the SAME analytic curve chart. A strict upper bound
U can be enlarged to avoid the constant/harmonic boundary case.

For h=A+yB on controlled hyperelliptic charts, the algebraic norm lemma provides
such a nonzero low Taylor coefficient with K=O(g) and polynomial-log U,u:

* Ordinary chart: x=x0+s z, with s bounded below by exp(−poly) and the disk
  avoiding all branch roots. Both h and h*=A−yB are analytic and bounded.
  Their product is R(x0+s z), a degree-D polynomial. Inverting the affine
  substitution bounds its coefficient norm below by eta times exp(−poly).
  If all h coefficients through D were tiny, the product coefficients would
  all be tiny, contradiction. Hence K<=D.
* Branch chart: x=E+s² z² and y=s z sqrt(F_E(E+s²z²)), F_E=F/(x−E).
  Choose s²<=Delta/4. After centering at the input point within this chart,
  h*h* is a degree-2D polynomial with a similarly bounded coefficient norm.
  Hence K<=2D. This includes branch-edge inputs without dividing by y.

A finite atlas with these quantitative scales covers the compact real ovals.
The full constants and centering margins must be written in the final proof;
no exponential-in-1/Delta atlas enumeration is needed (only the branch charts
and the chart centered at each of the O(g) requested input points).

Alternative independently suggested proof: continue an inverse branch of the
proper meromorphic map f from f(P) to0. Homogeneous polynomial root perturbation
for (A−z)²−FB² confines the x-coordinate to a cluster of O(g) nearby roots; the
quadratic relation y²=F(x) gives same-sheet proximity by continuity. The local
analytic lemma above avoids needing this alternative's projective root matching.

## 4. Proposed robust operation and what must be proved

1. Replace the two copies of each D point and the iota(D0) point by three
   nearby, separated points on the same oval. Choose angle displacements
   <=O(epsilon) and mutual angle separation >=epsilon, including collisions
   and branch edges. Three points per oval suffice; this perturbation has a
   directly bounded Abel error by the companion file's uniform derivative.
2. Evaluate the 3g-by-(3g+1) section-basis matrix at those distinct points and
   round each entry to q binary digits. Compute ANY exact rational nonzero
   kernel vector of the rounded matrix, normalized by its maximum coefficient.
   Fraction-free elimination has polynomial bit complexity in g,q. No rank
   lower bound or stable kernel-vector approximation is requested.
3. The resulting real rational f has small residual at each input. The lemma
   in §3, with radius below one quarter of their separation, forces 3g DISTINCT
   nearby actual section zeros. Choose and remove one corresponding zero for
   each input, preserving multiplicity. Small residual is not by itself proof
   of exact interpolation, and the zero-selection matching is load-bearing.
4. Compute the complete section-zero divisor using the rational polynomial
   R=A²−F B², exact common factors of A,B, and algebraic root isolation. Account
   for both sheets and zeros at infinity, not just x-roots. Remove those 3g
   zeros and retain T of degree g. Its divisor class has the desired relative
   arithmetic value up to a directly bounded Abel error.
5. The target iota(E) is uniformly nonspecial. The companion's uniform inverse
   Jacobian plus explicit analytic second-derivative bounds should give a
   complex inverse collar of radius exp(−poly). If the error lies in that
   collar, T is the unique effective degree-g representative there and must
   lie near iota(E), since a nonspecial degree-g class has only one effective
   representative globally. Identify one point per gap, project its local
   signed-angle coordinate to the real oval, and charge that projection error.

Important: rounding real coefficients need NOT preserve real zeros near a
multiple zero. The complex collar/projection in step5 cannot be omitted merely
because the initial data and matrix are real. Likewise final physical
conditioning does not by itself certify steps3–4.

## 5. Precision accounting and comparator

For each call, arrange direct Abel/torus error at most delta. The residual-zero
exponent O(g) costs q=poly(g,log M,log(1/Delta),log(1/delta)), not a favorable
pivot. Polynomial root computation adds polynomial work/precision in that q.
If m doublings are performed, direct group error satisfies e_(j+1)<=2e_j+delta.
Thus taking delta<=epsilon·2^(−m)/polycondition makes the total physical error
<=epsilon. The O(g) Hölder exponent is paid afresh per call; composing coordinate
Hölder estimates naively would incorrectly require g^m bits.

This direct-error strategy is classical in Couveignes–Edixhoven, book §12.8–12.9;
related local Abel inversion plus repeated doubling is explicit in Mascot.
The proposed contribution here, if proved, is only a uniform quantitative
transfer to the physically conditioned real hyperelliptic family, with no
auxiliary genericity promises. It is not a speedup over the equally informed
classical integrability algorithm that uses exactly these techniques.

Still open in this draft: the complete explicit atlas/collar constants; certified
root/sheet/infinity/multiplicity bookkeeping and actual tests; complete rational
bit-growth accounting; acquisition from raw equations. There is no full
fast-forwarding claim.
