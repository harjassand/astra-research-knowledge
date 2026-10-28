# Independent substantive review: local C1,1 convex representative

**Disposition: ACCEPTED at its stated mathematical scope.**

Reviewed the whole of
`../../parent/regularity_positive/PROOF.md` and `exact_constants.py`, and
independently read the CW1,1 definition and Theorem 2.4 with its proof in
Azagra--Le Gruyer--Mudarra,
https://arxiv.org/html/1706.02235v4#S2.Thmtheorem4 . The source theorem is
the established extension result; no new extension theorem is being credited.
The accepted rational support inequality is an input. This review reconstructs
the analytic jet comparison rather than re-auditing that earlier certificate.

## Exact continuum estimates

For a monomial of degree n, its gradient norm is bounded by
n|A|^(n-1), and its Hessian operator norm by n(n-1)|A|^(n-2): each can be
viewed as the derivative of a product of n coordinate linear functionals,
each of norm one. Consequently the coefficient-l1 bounds used for F and p
are valid in the Frobenius/Euclidean norms, without an omitted dimension
factor.

For k=p/|A|^4, literal differentiation gives

    Dk=Dp/|A|^4-4p A/|A|^6,
    |k|<=P|A|^2,       |Dk|<=10P|A|.

At zero, |k(A)|/|A| tends to zero, so its derivative exists and is zero.
The derivative bound away from zero tends to zero, proving k is C1 on all
of R4. This justifies segment integration even for segments through zero.

The planar cofactor map is linear and an isometry; its derivative has
operator norm one. Hence the first four components of

    G(mA)=(DF(A)-k(A)cofA,k(A))

have derivative norm at most (12C+11P)|A|^2, and the last component has
derivative norm at most 10P|A|. With U=12C+11P, V=10P, d=|B-A| and
r=max(|A|,|B|)<=R, segment integration therefore yields

    |G(mB)-G(mA)|^2 <= (U^2 r^4+V^2 r^2)d^2
                        <= (U^2 R^2+V^2)r^2 d^2.       (1)

The exact planar determinant identity makes the jet remainder precisely

    f(mB)-f(mA)-G(mA):(mB-mA)
        =B_F(A,B-A)-k(A)det(B-A).

There is no neglected first-order cofactor term. The earlier accepted bound
is at least delta(|A|^2 d^2+d^4) with delta=1/2400000, because its quartic
coefficient 1/1600000 is larger than delta. Since r^2<=2(|A|^2+d^2), this
remainder is at least delta r^2 d^2/2. Combining with (1) proves CW1,1
with exactly

    M_R=(U^2 R^2+V^2)/delta.

The estimates hold for every ordered pair A,B in the entire closed ball,
including A=0, B=0, and A=B. No sampling or unstated compatibility of the
graph parameterization is involved. The map m is injective.

## Source conclusion and finiteness

Theorem 2.4 applies to an arbitrary subset of a Hilbert space and the
specified CW1,1 jet. The proposed infimum of quadratics followed by convex
envelope is exactly its formula. Thus g_R is globally finite, convex, C1,1,
and has gradient Lipschitz constant at most M_R. It matches both f and G
on E_R, not merely their function values.

One can also see finiteness directly here: E_R and its jet values are
bounded, so the infimum of the quadratic functions is finite and bounded
below; the CW premise supplies its affine minorants. The convex envelope
therefore cannot collapse to minus infinity.

## Independent exact constants

The companion replay independently expands the literal accepted F and p,
without importing the producer's code, and obtains

    C=2535570311/2500000000,
    P=1976430361/156250000,
    U=94569646817/625000000,
    V=1976430361/15625000,
    M_1=45580383762312788235267/488281250000.

These agree with the producer's recorded constants. The finite replay
does not prove the Whitney theorem or replace the continuum estimates
above.

## Limits retained

For each finite R, the extension represents F for every |A|<=R. It need
not represent F outside that ball. No compatibility between different R,
small evaluation cost, finite neural representation, physical realization,
or world priority follows. The source formula has a continuum infimum and
convexification cost. These limitations are accurately retained in the
producer's proof. Together with the separately reviewed no-C2 theorem,
this gives the claimed C1,1 versus C2 local regularity separation.
