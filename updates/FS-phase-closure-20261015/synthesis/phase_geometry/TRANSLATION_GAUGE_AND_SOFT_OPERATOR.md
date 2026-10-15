# Translation-gauge blowup and the nonlocal mixed-phase operator

Date: 15 October 2026. Worker: phase_geometry.

Status: internal analytic derivation, externally unreviewed. Historical novelty
UNKNOWN. The final soft-potential formula is an exact reduction, not a sign
theorem. No full quasiconvexity theorem or negative compatible test is claimed.

## 1. Exact projective coordinates in a large target translation

Let Omega be a bounded connected Lipschitz planar domain. Let
`u=(a,b)` be `C^1` on its closure. Let F be a rank-one-convex homogeneous
quartic with positive minimum rank-one value `mu_F>0`.

For `R>2||a||_infinity+1` set

    w_R = (R+a,b),    n_R = w_R/|w_R|,
    beta_R = b/(R+a).

Every map with this prescribed direction and the same boundary amplitude can
be written exactly as

    v_R(h) = (R+a+h, b+beta_R h),
    h|boundary=0,    R+a+h>=0.                           (1.1)

Indeed, `v_R(h)=(1+h/(R+a))*w_R`. The positivity constraint is precisely the
nonnegative-amplitude constraint. Its energy is

    E_R(h) = integral F(Du+e_1 tensor grad h
                         +e_2 tensor grad(beta_R h)).    (1.2)

On bounded subsets of `W_0^(1,4)(Omega)`,

    beta_R -> 0 in W^(1,infinity),
    E_R(h)-E_infinity(h) -> 0 uniformly,
    E_infinity(h) = integral F(Du+e_1 tensor grad h).      (1.3)

The uniformity follows from `||beta_R||_(W1,infinity)=O(1/R)`, the Sobolev
embedding into L-infinity in two dimensions, and quartic polynomial growth.
The limiting functional is ordinary convex minimization of one output
component while the other output component is frozen.

In the phase variables of the incoming note,

    R theta_R -> b in C^1,
    |w_R|-R -> a in C^1,
    |w_R| Dn_R -> e_2 tensor grad b.

Thus the small phase gradient is multiplied by an amplitude of order R. It
retains an arbitrary transverse output gradient. No small coupling follows.

## 2. The fixed fourth-mass constraint leaves a mean constraint

The incoming replacement fixes the actual translated fourth mass. In (1.1)
the condition is

    integral |v_R(h)|^4 = integral |w_R|^4.              (2.1)

Put `t_R=R+a` and `q_R=(1+beta_R^2)^2`. Its difference is exactly

    integral q_R(4t_R^3 h+6t_R^2 h^2+4t_R h^3+h^4)=0.   (2.2)

For h in any bounded W1,4 set, divide by `4R^3` to obtain

    integral h = O(1/R).                                (2.3)

The limit therefore retains `integral h=0`; dropping this condition would
silently change the supplied fixed-mass operation.

Conversely, take any `h in W_0^(1,4)` with integral zero. Fix a nonnegative
smooth compactly supported psi with integral one. There is a scalar
`c_R=O(1/R)` such that `h_R=h+c_R psi` satisfies (2.1) exactly. To see this,
the mass residual at c=0 is O(R^2), while its derivative in c is

    4 integral q_R (R+a+h+c psi)^3 psi = 4R^3+O(R^2)

uniformly for small c. The intermediate value theorem gives the correction;
strict monotonicity there gives uniqueness of this small root. Since h is
bounded in dimension two, positivity in (1.1) holds for sufficiently large R.
Moreover, `h_R -> h` strongly in W1,4.

## 3. The complete constrained variational limit

Let m_R be the infimum of E_R subject to (1.1) and (2.1). Then

    lim_(R->infinity) m_R
      = min { E_infinity(h): h in W_0^(1,4), integral h=0 }. (3.1)

The minimum on the right exists. This statement concerns an exact variational
limit, not just a formal Taylor expansion.

Proof of equicoercivity. Write the matrix in (1.2) as

    Q_R+C_R,
    Q_R = (1,beta_R) tensor grad h,
    C_R = Du+e_2 tensor h grad beta_R.

Q_R is rank one and `F(Q_R)>=mu_F |grad h|^4`. Quartic growth and Young's
inequality give

    F(Q_R+C_R) >= (mu_F/2)|grad h|^4-C_F |C_R|^4.

Poincare's inequality and `||grad beta_R||_infinity=O(1/R)` allow the h term in
C_R to be absorbed for all sufficiently large R. Thus, independently of the
mass constraint,

    E_R(h) >= (mu_F/4)||grad h||_4^4-C(u,F,Omega).        (3.2)

The competitor h=0 bounds m_R above. Minimizing sequences are therefore
bounded in W1,4. Their weak limits have boundary zero, and (2.3) gives mean
zero. The term `grad(beta_R h)` tends strongly to zero in L4. The remaining
integrand in (1.3) is convex in grad h, by rank-one convexity, and so is weakly
lower semicontinuous. This proves the liminf bound. The exact recovery
correction in Section 2 proves the matching limsup bound.

The quartic rank-one Bregman bound in the incoming source gives strict
convexity of the limiting functional modulo constants; zero boundary removes
the constants. Hence its minimizer is unique. The result remains valid after
rotating the target translation direction; then the output component
perpendicular to that translation is frozen in the limit.

At an affine input u=Bx, the limiting minimizer is h=0 because the linear term
integrates to zero and rank-one convexity gives a nonnegative scalar remainder.
At a non-affine input, the limiting problem is a mean-constrained scalar row
problem for the actual frozen other component. This does not establish any
comparison with `|Omega|F(B)` for arbitrary frozen components.

This is the precise limitation of trying to exploit target-translation gauge:
the apparent small-phase regime contains the full unsolved vectorial
interaction after the necessary rescaling.

## 4. The reduced second variation is a nonlocal Schur complement

At a constant background B, define the acoustic matrix

    Q_B(xi)_(alpha,beta)
      = D^2 F(B)[e_alpha tensor xi,e_beta tensor xi].      (4.1)

Rank-one convexity gives `Q_B(xi)>=0`. In the translation-gauge limit the radial
variable is the first output component a and the phase variable is the second
component b. For a periodic Fourier mode with `Q_11>0`, exact quadratic
minimization over the radial component gives

    Q_reduced(xi) = Q_22-Q_21 Q_11^(-1) Q_12.             (4.2)

This is nonnegative because Q is PSD. For Dirichlet data the corresponding
operator, when the first scalar block is coercive, is

    L_reduced = L_22-L_21 L_11^(-1) L_12,
    L_alpha,beta = -div(C_alpha,beta grad).

It is a nonlocal operator: eliminating the radial block subtracts a positive
coupling term. Positivity of the phase block alone does not control this
subtraction. If Q_11 vanishes, PSD also forces Q_12=0; one must use the actual
zero block or an appropriate pseudoinverse, not divide by zero.

The fixed-mass mean constraint affects the zero Fourier mode, not (4.2) for
nonzero modes. The familiar positivity of constant-coefficient rank-one-convex
quadratic forms follows from this acoustic decomposition; it does not control
the nonlinear reduced phase value.

## 5. The exact soft mixed-phase operator for retained G at B=I

Use the source integrand

    G(A) = 3(u+v-2j)^2+(35/24)u^2+j^2-(5/2)ju,
    u=A_11^2+A_21^2, v=A_12^2+A_22^2, j=det A.

The source packet supplies its full rank-one-convexity certificate; no angular
sampling is substituted for that premise. Direct differentiation at I gives

    D^2G(I), in row-major matrix coordinates,
      = [[9/2,0,0,-7/2],
         [0,0,1/2,0],
         [0,1/2,5/6,0],
         [-7/2,0,0,2]].

For a periodic or zero-boundary perturbation `phi=(a,b)`, the determinant
null identity gives exactly

    integral D^2G(I)[Dphi,Dphi]
      = integral [(9/2)(a_x-(2/3)b_y)^2+(5/6)b_x^2].      (5.1)

Pointwise, the right-hand integrand exceeds the quadratic form by `det Dphi`.
The acoustic matrix and determinant are

    Q(p,q) = [[(9/2)p^2,-3pq],
              [-3pq,(5/6)p^2+2q^2]],
    det Q = (15/4)p^4.                                  (5.2)

Eliminating the radial row gives

    Q_reduced(p,q) = (5/6)p^2,  p!=0,
                  = 2q^2,      p=0.                     (5.3)

The minimizing amplitude coefficient for `p!=0` is
`a_hat=(2/3)(q/p)b_hat`. The discontinuity between the two cases reflects
the singular first-row block; it is not a contradiction of rank-one convexity.

For example,

    a_N=(2N/3) sin(x+Ny),   b_N=sin(x+Ny)

has normalized quadratic action exactly `5/12` for every integer N, although
its transverse derivatives are unbounded with N. Thus there is no uniform
transverse coercivity for the reduced operator at this acoustic boundary.
The positive quartic rank-one value `mu_G=3` does not imply a strictly positive
quadratic acoustic margin at every nonzero background.

This is a concrete obstacle to a phase argument that requires uniform
ellipticity of the amplitude inverse or uniform phase-gradient coercivity.
It also identifies a nonlocal mixed-phase representation worth retaining.

## 6. A compatible potential chart that kills the leading square

Enforce the soft relation by a scalar periodic potential v:

    a=(2/3)v_y,    b=v_x.

Then `a_x=(2/3)b_y` exactly, and (5.1) reduces to `(5/6) integral v_xx^2`.
Write `p=v_xx`, `q=v_xy`, `r=v_yy`. The compatible gradient is

    I+s Dphi = [[1+(2s/3)q,(2s/3)r],
                [sp,1+sq]].

Exact expansion gives

    G(I+sDphi)-G(I)
      = -(5/18)s q
        +(s^2/12)(5p^2+4pr-4q^2)
        -(5s^3/162)q(9p^2+4q^2)
        +s^4 K(p,q,r),                                 (6.1)

where

    1944 K = 8667p^4+18792p^3r+576p^2q^2+16416p^2r^2
             +1440pq^2r+6912pr^3+56q^4+576q^2r^2+1152r^4.

For periodic v, `integral q=0` and `integral pr=integral q^2`; hence the full
compatible energy difference is exactly

    (5s^2/12) integral p^2
      -(5s^3/162) integral q(9p^2+4q^2)
      +s^4 integral K(p,q,r).                            (6.2)

This formula keeps the genuinely resonant cubic term. There is no assumption
that it cancels under arbitrary-frequency mixing. Its independence from r is
an exact algebraic cancellation, potentially useful in anisotropic estimates.

The quartic K is not pointwise nonnegative: `K(1,0,-3/2)=-1/24`. Those values
are unconstrained Hessian jets, rather than a periodic Hessian witness. It is
therefore invalid to discard K, or to infer a negative compatible integral
from its negative pointwise value.

A universal sign theorem for (6.2), or an explicit negative periodic v with
rigorous integration, remains open in this worker's state. This is a specific
next obligation, rather than an asserted new solution by renaming a minimum.

## 7. Source boundaries

The direction-density perspective and the quartic Bregman constant are from
the immutable incoming `sources/phase_density/PHASE_DENSITY_COMPATIBILITY.md`.
The G formula is equation (6.1) there. The N830 finite-jet/linear-selector
obstructions are consistent with this nonlocal operator; no forbidden local
storage is being asserted. N819's one-frequency storage is not promoted to
the resonant potential identity (6.2).

The Schur-complement calculation and the translation limit are derived here
from elementary differentiation, scalar convexity, and compactness. These
ingredients are standard; historical novelty of these applications is UNKNOWN.
All exact finite algebra is checked by `verify_phase_geometry.py` separately
from the analytic arguments.
