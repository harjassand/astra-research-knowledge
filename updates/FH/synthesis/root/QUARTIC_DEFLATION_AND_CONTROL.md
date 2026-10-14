# Background deflation: an exact limit obstruction and a controlled alternative

14 October 2026. Integration-derived mathematics, separately from the incoming
rigidity manuscript. External correctness and historical novelty remain UNKNOWN.
Generalized inverses, Schur complements, residual identities and coercivity are
established methods; their general principles are not claimed as new here.

## 1. The exact interface supplied by nullspace closure

For a homogeneous planar quartic F that is rank-one convex, let X be a centered
law with finite fourth moment and E det X=0. Write

    C=E[vec X vec X^T], H=E D²F(X), b=E DF(X), c=E F(X).

The incoming one-indefinite-quadric theorem proves H>=0 and b in ran H, even
without rotational invariance. Hence the complete affine-background minimum is

    J(F,X)=inf_B E[F(B+X)-F(B)]=c−(1/2)b^T H†b.             (1)

Compatible gradients are a special case. Their singular-face Jensen theorem
proves J>=0 when H is singular in the full nine-coefficient invariant cone.
It does not prove that (1) is continuous near that face. The following actual
smooth gradient construction shows why a continuity argument would be invalid.

## 2. A fixed polyconvex quartic with discontinuous optimized gap

Use normalized averages on the square torus [0,2pi]². Put

    phi0=(sin x cos y, −cos x sin y),
    psi=(−sin(2x)/4, −sin(2y)/4), chi=(sin y,sin x),
    X_e=D(phi0+e psi+e² chi), 0<e<=1.

These are genuine compatible gradients with a common finite Fourier support.
They converge to X0 in every C^k norm and are uniformly bounded in L∞. Writing
a=cos x cos y and s=sin x sin y gives

    X0=[[a,−s],[s,−a]],
    q0=det X0=−[cos(2x)+cos(2y)]/2,
    E q0²=1/4, tr X_e=e q0, E det X_e=0.

Take the fixed quartic F(A)=(det A)². It is polyconvex and quasiconvex. This
example therefore cannot be a quasiconvexity counterexample. In row-major
coordinates, its covariance is exactly

    C_e=[[1/4+e²/8, 0, 0, −1/4],
         [0, 1/4+e⁴/2, −1/4, 0],
         [0, −1/4, 1/4+e⁴/2, 0],
         [−1/4, 0, 0, 1/4+e²/8]].

Its eigenvalues are e²/8, 1/2+e²/8, e⁴/2 and 1/2+e⁴/2. Thus C_e has rank four
for every e>0, whereas C0 has rank two. If K is the invertible symmetric matrix
sending vec X to grad(det)(X), determinant balance gives H_e=2 K C_e K.
Consequently H_e is positive definite for every e>0 and singular at zero.

For the background B_e=−I/e, determinant polarization gives

    det(B_e+X_e)=e^-2−q0+det X_e.

Its mean is det B_e, so the determinant-square Jensen gap is exactly

    E[(det X_e−q0)²]=e²/32+9e⁴/64+e⁸/4.                   (2)

In particular J(F,X_e) tends to zero by positivity and (2). At e=0, however,
the cubic vector is zero by Fourier orthogonality, and c0=1/4. Formula (1)
therefore gives J(F,X0)=1/4. The optimized Jensen gap is not lower semicontinuous
at this singular face, despite smooth convergence and bounded fields.

Direct exact elimination strengthens the comparison:

    J(F,X_e)=e²/32+9e⁴/64+e^10/[4(e²+4)] for e>0.          (3)

The unique minimizing background has diagonal entries

    −(2e⁵+e²+4)/[e(e²+4)], (2e⁵−e²−4)/[e(e²+4)],

and zero off-diagonal entries. It escapes to infinity. This identifies the
missing compactness: moment convergence and exact nullspace closure do not
bound the background that achieves the minimum. It is not caused by increasing
bandwidth, concentrating gradients or a failed numerical optimizer.

The e²Dchi term is important. Omitting it gives rank C=rank H=3 for e>0 for
this fixed F, so that variant alone would not demonstrate a positive-definite
to singular transition. The complete construction above does.

## 3. A strictly quasiconvex varying-integrand version

Set Y_e=D(phi0+e psi) and F_e=q²+e⁴|A|⁴. Then F_e is uniformly quasiconvex for
each fixed e>0, with Jensen gap at least e⁴ E|Dphi|⁴/3. Its averaged Hessian is

    H_e=2 K C_e K+e⁴[8C_e+4(tr C_e)I]>0.

Here C_e has rank three. The norm term alone supplies strict positivity.
At B_e=−I/e, the total gap is exactly

    e²(5e⁶+40e⁴+209e²+258)/64,                            (4)

which also tends to zero while the limiting optimized gap is 1/4.

F_e is outside the incoming exceptional class for every e>0. If it equalled
gamma q²+|alpha x_C+beta y_C|⁴, its rank-one restriction would imply
|alpha|=|beta|=e and Re(alpha conjugate(beta))=0. Thus the fourth power would be
e⁴(u+v±2q)², whose nonzero orientation term ±4e⁴q(u+v) cannot be canceled by
gamma q². This is a nonuniformity example across varying coefficients, not a
counterexample for one fixed nonexceptional quartic and not negative energy.

## 4. An explicit compact background range under strict rank-one coercivity

There is a positive replacement when a quantitative hypothesis is available.
Suppose F−delta|A|⁴ is rank-one convex, delta>0, and m2=E|X|²>0,
m4=E|X|⁴<infinity. Applying the one-quadric averaged-Hessian theorem to this
residual quartic yields

    H_F >= delta[8C+4m2 I] >=4delta m2 I.                   (5)

Let K_F be the l1 norm of F's coefficients in the fixed 35-monomial row-major
basis. Since |DF(X)|<=4K_F |X|³ and E|X|³<=sqrt(m2 m4),

    |b|<=4K_F sqrt(m2 m4),
    |B*|=|H_F^-1b| <= (K_F/delta)sqrt(m4/m2).              (6)

Thus a known strict rank-one-convexity margin and moment bound make affine-
background search compact, even for quartics without rotational invariance.
The coefficient norm is coordinate dependent and is not silently replaced by
the invariant nine-coefficient norm. Computing or certifying delta is a real
operation. Equations (5)-(6) do not bound Fourier support, all possible gradient
laws or the limit delta→0. They do not solve Morrey's problem.

## 5. A source-complete residual test for the remaining scalar obstruction

The source-aware response identity in N798 transfers after nullspace closure
has supplied its exact range hypothesis. Work on ran H. Assume a symmetric
minorant C0 with 0<C0<=H on that space and ker C0=ker H. For any trial v, let
r=b−Hv and G0=2b^Tv−v^THv. Completing the square gives

    b^TH†b=G0+r^TH†r,
    G0 <=b^TH†b<=G0+r^TC0†r.

Consequently

    c−(G0+r^TC0†r)/2 <= J(F,X) <= c−G0/2.                 (7)

The upper is the actual background trial B=−v. The lower is rigorous by inverse
order on the common range. Without b in ran H, the affine infimum could be
minus infinity; without a valid range/coercivity minorant, the upper response
bound is not justified. The incoming theorem closes the first obligation,
not the second. A nonnegative lower in (7) certifies this particular gradient
law for every background. Quasiconvexity still requires such control for every
compatible law, with justified acquisition and precision.

This is a precise composition of two established variational mechanisms. It
does not invent Schur complementation or make a dense inverse/free coercivity
oracle available. The fixed-dimensional moment objects and exact Fourier
examples are executable; a universal completion remains open.

## 6. Evidence and attribution

`near_face_deflation.py` independently reconstructs all fields as Laurent
polynomials, takes exact zero Fourier coefficients, checks covariance/ranks,
the complete optimized expression (3), strict variant (4) and a singular-range
residual example. The independent critic reconstructs the trial formulas and
ranks separately; its delta review checks (3) and (5)-(7).

The general operator viewpoint has prior art, including Anderson and Trapp,
*Shorted Operators II*, SIAM J. Appl. Math.28(1),60–71 (1975), DOI
10.1137/0128007. Its primary publisher abstract/metadata were accessed, not its
full proof. The derivations here are self-contained. No novelty of generalized
Schur complements, singular inverse behavior or residual bounds is asserted;
priority of this explicit compatible-gradient realization is unresolved.
