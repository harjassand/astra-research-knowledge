# The identical J residue becomes #P-hard when 3 divides the field degree

This independently audits the root's stronger fixed-residue reduction.
All calculations below use F_8=F_2[alpha]/(alpha^3+alpha+1), d=3,
A=F_8[t]/t^2, and lambda_2=Tr_[F_8/F_2]([t]).

Let p(a_1,...,a_N) be any Boolean cubic and require N to be even and at
least two. An unused Boolean input supplies this parity at known factor
two if needed. Set r=N+1, b=2r+1=2N+3, and

    J_r=sum_(i=1)^r(X_i^3+X_iY_i^2+Y_i^3+Z X_iY_i).

The input to the target counter is the homogeneous cubic H=J_r+tG,
with G defined below and with no extra binary quadratic.

## 1. All residue critical rays are acquired explicitly

At Z=1 the transverse critical equations are

    X_i^2+Y_i^2+Y_i=0,       Y_i^2+X_i=0.

Hence X_i=Y_i^2 and Y_i^4+Y_i^2+Y_i=0. The four solutions in F_8 are

    Y_i=a_i alpha+b_i alpha^2,        a_i,b_i in F_2.

They are all the roots because the displayed polynomial has degree four
and derivative one. The infinity matrix has invertible blocks
[[1,1],[0,1]], so the only affine critical vector with Z=0 is the origin.

At a transverse critical point, the ordinary homogeneous Euler identity
gives J_r=sum_i X_iY_i=sum_i Y_i^3. Directly,

    (a alpha+b alpha^2)^3=a alpha+b alpha^2+(a+b+ab).

Since 1,alpha,alpha^2 are independent, the projective critical condition
is exactly

    sum_i a_i=0,        sum_i b_i=0,        sum_i a_i b_i=0.

There are no extension-field or multiplicity assumptions in this step.

## 2. The source Boolean coordinates are ordinary field-linear forms

There is an explicit extractor, so no Boolean projection is assumed:

    L_i(X_i,Y_i)=alpha^2 X_i+alpha^4 Y_i.

On the four transverse critical points it equals a_i. Indeed its values
on (X,Y)=(alpha^2,alpha) and (alpha^4,alpha^2) are respectively one and
zero, and the map is binary-linear. Likewise
alpha X_i+alpha^2 Y_i extracts b_i, although the reduction does not need it.

Write p as its multilinear ANF. Define G by replacing each a_i with L_i,
for 1<=i<=N, and homogenizing every monomial to ordinary degree three
with Z. In particular a constant term becomes that constant times Z^3.
Then G is an ordinary homogeneous cubic in the original ring variables,
independent of the last pair and all b coordinates at the critical rays,
and G(v)=p(a_1,...,a_N) belongs to F_2 when Z(v)=1.

Every source cubic monomial expands into at most eight target monomials.
The description has O(N+L_p) constant-size field coefficients when L_p
is the source ANF length. No representation oracle or compression is used.

## 3. Exact multiplicities of the b coordinates

The first parity equation fixes a_r=sum_(i=1)^N a_i. Thus the first N
a-bits freely parametrize all even-parity a vectors of length r. Because
r is odd, such a vector can never be the all-ones vector.

For a=0, the b constraints reduce to one parity equation and have
2^(r-1)=2^N solutions. For a nonzero, a and the all-ones vector are
independent, so the two b equations have 2^(r-2)=2^(N-1) solutions.
If Z_p=sum_a(-1)^p(a) and s_0=(-1)^p(0), the weighted critical-ray sum is

    W=2^(N-1)(Z_p+s_0).

Setting p=0 gives the unweighted number

    N_crit=2^(N-1)(2^N+1).

The odd-r assumption is essential for this exact formula: if r were even,
the all-ones a vector would create a second exceptional fiber.

## 4. Highest-digit orthogonality proves the complete ring count

Write an arbitrary ring input as v+t w with v,w in F_8^b. Since t^2=0,

    [t] H(v+t w)=grad J_r(v) dot w+G(v).

Summing over w gives 8^b when grad J_r(v)=0 and zero otherwise. At v=0,
G(v)=0, including when the source p has a constant term. Every nonzero
critical residue vector is uniquely z times one of the critical chart
vectors, for z in F_8*. Homogeneity gives G(zv)=z^3 p(a).

Cubing permutes F_8*, because gcd(3,7)=1. Its radial character sum is
seven for p(a)=0 and minus one for p(a)=1. Equivalently it is
3+4(-1)^p(a). Therefore the exact signed ring count is

    Z_A=8^(2N+3)[1+3 N_crit+4*2^(N-1)(Z_p+s_0)].

This proof does not depend on a choice of Hensel center or lift. If the
stationary algorithm is used instead, its unique transverse lift has
critical value tG(v), because grad J_r(v)=0 makes the first-order change
in J_r vanish. Thus the lifted computation gives the identical formula.
Any invertible binary affine disguise preserves the count.

Recover the source count by the exact arithmetic expression

    Z_p=(Z_A/8^(2N+3)-1-3 N_crit)/(4*2^(N-1))-s_0.

The original target input count is n=6b=12N+18. All output integers have
O(n) bits. The full binary centroid is A: the residue third form is the
radical-free contact form Z wedge Omega, and arbitrary higher nilpotent
deformations retain the chain centroid by the companion audit.

## 5. Hardness source and exact scope

Boolean cubic signed counting is #P-hard by Boolean gate arithmetization.
Use input and uniquely determined internal-wire variables, and one binary
multiplier for each quadratic gate equation and the output-one equation.
The sum of multiplier times equation has degree at most three. Its signed
sum is exactly 2^(number of equations) times the number of accepting circuit
inputs. Adding an unused variable if necessary gives even N. Since zero
counts and signed counts determine one another by Z=2*#zeros-2^N, the
reduction also applies to exact zero counting.

Thus #P-hardness holds inside this exact J_r residue family at fixed d=3
and e=2, with arbitrary higher cubic coefficients, no quotient noise,
invertible infinity matrix, and the full chain centroid. It establishes a
substantive boundary to removing the 3-not-dividing-d qualification from
the one-ray/all-depth theorem while keeping arbitrary higher deformations.
The field degree here is intrinsic to the acquired full centroid: its
semisimple quotient is F_8 and its radical has square zero. It cannot be
changed to a field degree coprime to three by relabeling a chain-ring
presentation. A finite field extension containing F_8 also has degree
divisible by three, so that extension does not enter the one-ray range.

The same derivation extends to odd multiples of three for d, replacing
the radial factor by (q/2-1)+(q/2)(-1)^p. The displayed F_8 formula must
not be transferred unchanged to even d: cubing is then not a permutation.
No extension beyond fixed d=3 is needed for the hardness theorem.
