# Working proof: real-torus Abel conditioning and physical Toda reconstruction

**Status.** The uniform Abel differential bound in §2 has been independently
checked by the mathematical reviewer. The general signs/indexing of the physical
decoder in §3 and the norming-weight/Gram bounds in §4 have also been independently
checked; a symbolic three-site check is additional evidence, not their proof.
The receipt is `LAX_DECODER_FRONTIER.md`. No certified approximate Jacobian-arithmetic algorithm,
raw-to-spectral acquisition theorem, or full fast-forwarding theorem is claimed.
The precise open obligation is §5. This file is ordinary working science, not a
publication or a claim of priority for classical inverse-spectral formulas.

## 1. Scientific system, exact data, and elementary bounds

Use the positive periodic Toda lattice with N>=3, indices modulo N:

    a_i' = a_i(b_(i+1)−b_i),
    b_i' = 2(a_i²−a_(i−1)²),        a_i>0.

Its two elementary conserved quantities are

    H = sum_i (b_i²/2+a_i²),       C=product_i a_i >0.

Their derivatives vanish by direct telescoping. In particular, for every real
time on the solution,

    |b_i| <= sqrt(2H),  a_i <= sqrt(H),
    a_i >= a_* := C/H^((N−1)/2).

Thus the solution stays in a compact subset of the positive phase space, and
these bounds prevent finite-time blowup and any a_i from approaching zero.
The constants are computable from the actual initial data, not promised.

The associated periodic Jacobi equation is

    a_(i−1) psi_(i−1)+b_i psi_i+a_i psi_(i+1)=lambda psi_i.

Its transfer matrices and monodromy, with this exact indexing, are

    T_i(lambda)=[[(lambda−b_i)/a_i, −a_(i−1)/a_i],[1,0]],
    M(lambda)=T_N ... T_1,     det M=1,
    p(lambda)=C tr M(lambda), F(lambda)=p(lambda)²−4C².

Here p is monic of degree N. The spectral curve is y²=F(lambda), and its two
Floquet multipliers are kappa=(p±y)/(2C). The spectrum and C are conserved by
the classical Toda Lax evolution. We do not claim to have acquired this Lax
representation from arbitrary raw equations in this file.

For §§2–4 first assume the computed F has 2N distinct real roots
E_0<...<E_(2N−1). Section 1a below gives the independently reviewed exact
closed-gap reduction; no perturbation of initial data is needed.
Set g=N−1, choose M>=1 bounding all |E_l| and the norm of the finite principal
Jacobi matrices below, and let Delta in (0,1] be any lower bound on distinct
root separation. For example M=4 max(1,H) is conservative by the row-sum bound.

If the initial a,b are rational of binary length B, p and F can be computed by
polynomial multiplication/transfer recurrence with coefficient bit lengths
polynomial in N,B. This is not a generic small-circuit height claim. Clear
denominators to get an integer polynomial F_int of degree d=2N and leading
coefficient A. Since its nonzero discriminant is an integer,

    1 <= |disc(F_int)|
       <= |A|^(2d−2) delta_min² (2M)^(d(d−1)−2).

Consequently the explicit, possibly very pessimistic bound

    Delta = min(1, |A|^(−(d−1)) (2M)^(−(d(d−1)/2−1)))

is valid. In particular log(1/Delta), log M and log(1/a_*) are polynomial in
the rational input size. Their *values* need not be polynomially bounded.

## 1a. Exact closed-gap normalization and the translation vector

This extension was independently verified after the original review. Receipt:
`audit/CLOSED_GAP_TODA_REVIEW.md`; four exact rational regressions and a generic
symbolic sign check are in `audit/closed_gap_toda_replay.py/.json`. It is classical
periodic-Jacobi normalization, explicitly described in Teschl, Remark 7.6:
https://www.mat.univie.ac.at/~gerald/ftp/book-jac/jacop.pdf .

The polynomials p−2C and p+2C are characteristic polynomials of the real symmetric
periodic and antiperiodic N-site Jacobi matrices. Each eigenspace has dimension at
most two by the second-order recurrence. Hence every root of F is simple or
double. At a double root the monodromy is +I or −I, respectively, so the root is
a fixed (simple) root of the full finite-Jacobi Dirichlet polynomial G, with
Floquet multiplier kappa=+1 or−1. Exact rational polynomial arithmetic computes

    K=gcd(F,F') monic,   Ftilde=F/K²,   Rrad=F/K=K Ftilde,
    G=K Gactive,         g'=N−1−deg K.

Both Ftilde and Rrad are squarefree, and K,Ftilde are coprime. The normalized
curve ytilde²=Ftilde has genus g'. Its active divisor has one point on each open
gap; closed nodes are retained only in the full-state decoder. For all separation
bounds needed by that full decoder use the radical Rrad, not Ftilde alone: the
fixed closed nodes still occur in G. The integer-discriminant argument in §1
applies to Rrad. The reduced Abel bound uses its active branch roots.

The flow sign can be checked without assuming a Dubrovin formula. If J_fin is
the finite (N−1)-site principal Jacobi matrix and B_fin has superdiagonal a_i
and subdiagonal −a_i, its derivative is

    J_fin'=[B_fin,J_fin]+diag(−2a_N²,0,...,0,+2a_(N−1)²).

Hellmann–Feynman and §3's normalization S_j give

    mu_j'=2 a_N²(kappa_j²−1)/S_j
          =−2 C(kappa_j−kappa_j^−1)/G'(mu_j)
          =−2 y_j/G'(mu_j).

For active points set ytilde_j=y_j/K(mu_j), preserving the actual SIGN of K.
Then G'(mu_j)=K(mu_j) Gactive'(mu_j), so exactly

    mu_j'=−2 ytilde_j/Gactive'(mu_j).

Replacing K by |K| is wrong and reverses some oval velocities; the regression
suite includes a rational example exhibiting this sign trap. For reduced
holomorphic differentials x^(ell−1) dx/ytilde, polynomial Lagrange interpolation
therefore gives the exact Abel velocity

    d/dt sum_j integral^P_j x^(ell−1) dx/ytilde
       =−2 sum_j mu_j^(ell−1)/Gactive'(mu_j)
       =−2 delta_(ell,g'),       ell=1,...,g'.

Thus the continuous-time translation vector is (0,...,0,−2), with no period or
velocity oracle assumed. For g'=0 the positive isospectral component is a point.
The full decoder in §3 still uses G=K Gactive and includes the fixed closed
nodes with kappa=±1, determined by gcd(K,p∓2C). It must NOT discard these nodes
when reconstructing the (N−1)-site Jacobi matrix.

## 2. Uniform Abel differential: branch endpoints do not force a singular chart

The real physical Dirichlet divisor has one point on each gap oval, with

    mu_j in [E_(2j−1),E_(2j)],       j=1,...,g.

This is a standard inverse-spectral description of the positive isospectral
torus. The global identification with a component of the real Jacobian is a
classical imported fact; the following quantitative differential bound is proved
directly and does not assume a favorable target divisor.

Write alpha_j=E_(2j−1), beta_j=E_(2j), c_j=(alpha_j+beta_j)/2,
r_j=(beta_j−alpha_j)/2, and use a genuine circle coordinate, including sheet:

    mu_j=c_j+r_j cos(theta_j),
    y_j=r_j sin(theta_j) sqrt(|product_(l notin {2j−1,2j})(mu_j−E_l)|).

The excluded product is negative on this gap. Therefore y_j²=F(mu_j), and

    dmu_j/y_j = −dtheta_j /
      sqrt(|product_(l notin {2j−1,2j})(mu_j−E_l)|).

This identity extends smoothly across theta_j=0,pi; dividing by y in the
lambda coordinate alone would incorrectly suggest a singularity at the edges.

Use the unnormalized holomorphic differentials
omega_k=lambda^(k−1) dlambda/y, k=1,...,g. In a local Abel lift,

    J_kj = partial A_k/partial theta_j = −mu_j^(k−1) w_j,
    w_j=|product_excluded(mu_j−E_l)|^(−1/2).

Each of the 2g excluded factors lies between Delta and 2M in absolute value,
so (2M)^(−g) <= w_j <= Delta^(−g). Different mu_j lie in different gap intervals,
separated by an intervening band of width at least Delta. Let
V_kj=mu_j^(k−1). Lagrange interpolation writes the jth cardinal polynomial as

    product_(l!=j)(lambda−mu_l) / product_(l!=j)(mu_j−mu_l).

Every numerator coefficient is at most (1+M)^(g−1) in absolute value, and the
denominator is at least Delta^(g−1). Thus every entry of V^−1 is bounded by
((1+M)/Delta)^(g−1), giving

    ||J^−1||_2 <= g (2M)^g ((1+M)/Delta)^(g−1).                 (A)

This is uniform over the **entire physical gap torus**, not just a generic open
chart. A corresponding upper bound is

    ||J||_2 <= g max(1,M^(g−1)) Delta^(−g).

The logarithms of both bounds are polynomial in N,B. This closes a target
nonspeciality/conditioning gap for the unnormalized Abel map on this component.
It does NOT alone give a polynomial-time algorithm for global inversion, group
arithmetic, period computation, or original-state evaluation.

## 3. Explicit physical decoder from Dirichlet points and Floquet sheets

Take the Dirichlet solution psi_0=0, psi_1=1. Then

    psi_N(lambda)=G(lambda)/(a_1 ... a_(N−1)),
    G(lambda)=product_(j=1)^g(lambda−mu_j).

At lambda=mu_j, psi_N=0 and the multiplier of this solution is

    kappa_j=psi_(N+1)(mu_j),
    a_(N−1) psi_(N−1)(mu_j)=−a_N kappa_j.

The discrete Lagrange identity, obtained by differentiating the recurrence in
lambda and telescoping, gives

    S_j:=sum_(i=1)^(N−1) psi_i(mu_j)²
        =a_(N−1) psi_(N−1)(mu_j) psi_N'(mu_j)
        =−a_N² kappa_j G'(mu_j)/C.

The spectral weights for the first coordinate of the finite (N−1)-site principal
Jacobi matrix are W_j=1/S_j>0 and sum_j W_j=1. Hence

    a_N² = −C sum_j 1/(kappa_j G'(mu_j)),                     (B)
    W_j = −C/(a_N² kappa_j G'(mu_j)).                        (C)

Every summand in (B) is positive on the physical spectral data, so the sum does
not conceal cancellation. The kappa_j are obtained from the signed curve points
as (p(mu_j)+y_j)/(2C). When this branch is small, evaluate equivalently
2C/(p(mu_j)−y_j), using kappa_j*kappa_j^other=1.

The finite Jacobi matrix is then recovered from its eigenvalues mu_j and positive
weights W_j by the classical Stieltjes/Lanczos orthogonal-polynomial algorithm.
It returns b_1,...,b_(N−1) and a_1,...,a_(N−2)>0. Finally,

    b_N = (sum_i b_i invariant) − sum_j mu_j,
    a_(N−1) = C/(a_N product_(i=1)^(N−2) a_i).

The invariant sum_i b_i is minus the next-to-leading coefficient of p. Thus all
original a,b are recovered from actual spectral curve/divisor data and sheets,
not merely conserved eigenvalues. Branch signs, positivity and recurrence
normalization are part of the decoder contract.

This is a classical inverse-spectral mechanism, not a claimed new formula.
An appropriate explicit comparator is Andrea–Berry, *Continued fractions and
periodic Jacobi matrices* (1992), DOI 10.1016/0024-3795(92)90008-X. The independent
review checked this derivation rather than assuming it from the citation.

## 4. Why this decoder has a derived polynomial-log condition bound

Let J_fin be the g-site finite Jacobi matrix above, with ||J_fin||<=M and all
off-diagonal entries >=a_*. For an eigenvector normalized by psi_1=1,

    psi_(k+1)(mu)=P_k(mu)/(a_1...a_k),

where P_k is the monic characteristic polynomial of the k-site leading principal
matrix. All its roots are in [−M,M], so |P_k(mu)|<=(2M)^k. Therefore

    W_j >= [g (2M/a_*)^(2(g−1))]^−1.                        (D)

This lower bound follows from the actual Toda energy/product invariants and
needs no separate norming-weight promise.

The moment Gram matrix for degrees 0,...,g−1 is

    H_mom=V diag(W_j) V^T,
    lambda_min(H_mom) >= min W_j / ||V^−1||_2².              (E)

Equations (A),(D),(E) give polynomial bounds on the logarithms of the condition
numbers of the finite Stieltjes/Cholesky reconstruction. The square-root steps
for a_i are also separated from zero by a_*. The final product/quotient decoder
has denominators bounded using the same a_*.

For the spectral-to-weight stage, G'(mu_j) is a product of g−1 separated factors.
The values of p and p' on [−M,M] are bounded from its coefficient height; since
kappa and 1/kappa are the roots of z²−(p/C)z+1, their magnitudes are bounded above
and below by reciprocal quantities of polynomial logarithmic size. The signed
angle representation in §2 bounds derivatives of y without division by sin(theta)
at band edges. Thus (B),(C), evaluated with the stable reciprocal branch, have
derivative/precision bounds of the form exp(poly(N,B)).

These estimates support a required working precision poly(N,B,log(1/epsilon))
for this physical inverse map. A complete numerical-algorithm theorem must still
specify certified routines and error composition; the current draft is a
conditioning derivation, not an executable end-to-end certified implementation.

## 5. Exact open bridge—do not replace it with a conditioning promise

Local inverse Abel evaluation followed by repeated Jacobian doubling is already
classical: Couveignes–Edixhoven §3 and Mascot's numerical Abel–Jacobi inversion.
Their arithmetic operation count is not an automatic full-state accuracy result.
The modular-curve theorem's direct torus accuracy is explicitly distinguished
from divisor accuracy. Sources:

- https://arxiv.org/abs/1205.5896
- https://arxiv.org/abs/1211.1635
- https://arxiv.org/abs/math/0409209 (Khuri-Makdisi group arithmetic)

The unresolved step here is a **certified approximate group-arithmetic route**
whose intermediate Riemann–Roch/subspace/rank computations have precision and
work polynomial in the actual Toda input size and requested error, even when
chosen divisor representations collide or cross their exceptional loci.
Final-target nonspeciality and physical decoder conditioning do not by themselves
bound these internal computations. Exact finite-field operation counts do not
settle approximate complex arithmetic. An exponential-dimensional theta/projective
embedding is not a free workaround.

Also still required for a full compiler: acquire the spectral representation
from raw equations; compute needed periods or avoid them legitimately; certify
global arithmetic branches and numerical error composition; and compare to
equally informed classical Toda inverse-spectral algorithms. Section 1a now
verifies the translation vector and handles exact closed gaps, but does not
settle the approximate group-arithmetic obligation. No claim of superiority or full polynomial-time fast-forwarding is
made before these obligations are met.
