# Sharp negative generators: coercivity reductions and a closed concentration subroute

15 October 2026. Worker `sharp_boundary_coercivity`. New internal deductions
from the pinned universal certificate. External review, formal verification
and historical originality are UNKNOWN. Source files and the worktree are
read only throughout this investigation.

**Main storage question remains unresolved.** No positive constant for every
affine background and every compatible perturbation is proved here, and no
zero-margin sequence is constructed. The results below do prove strict
Jensen positivity, a quantitative rank-one-valued bound, and a nonconstructive
positive bound for all critical homogeneous angular profiles. The last result
rules out the proposed angular-zero logarithmic concentration mechanism.

## 1. Exact question and inherited premise

For each fixed real `r < -2`, write

```
A = [[a,b],[c,d]], u=a²+c², v=b²+d², j=ad-bc,
H=((a-d)²+(b+c)²)²,
alpha=3r/[8(r+2)], beta=r(r-1)/6,
J(A)=alpha H+beta u²+j²+r u j.
```

The desired constant is `gamma_r>0`, independent of the constant matrix B,
the domain, and the compatible perturbation, such that

```
integral [J(B+Dphi)-J(B)] >= gamma_r integral |Dphi|⁴.       (TARGET)
```

The intended domains are compactly supported smooth perturbations in R²,
bounded Lipschitz `W0^(1,4)` perturbations, and the periodic analogues. The
affine linear term integrates to zero in each class.

The inherited universal certificate proves all-background QC and gives the
fixed positive diffusion

```
L = d1 partial_xx+d2 partial_yy,
d1=(2r+1)/(r-1), d2=-3/(r-1).
```

With `psi_t=exp(tL)phi`, `A_t=B+Dpsi_t`,
`z=(psi1,xx,psi1,xy,psi1,yy,psi2,xx,psi2,xy,psi2,yy)` and
`Z=(a,b,c,d) tensor z`, its corrected heat density is

```
D_r(A,z)=Z^T C_r S_r C_r^T Z,       S_r positive definite. (1)
```

It equals the weighted heat Hessian plus the pullback of a globally exact
quadratic two-form. Thus the relative energy obeys

```
E'(t)=-integral D_r(A_t,D²psi_t),  E(infinity)=0.           (2)
```

The JSON SHA-256 is
`f45149312e694f6080a179b77d322aceabf0d7c2a55ed60c5e102037e55f6ee7`.
The original portable verifier was copied byte for byte into this worker
directory and run with the original JSON as a read-only input. The new
`EXACT_REDUCTIONS.py` separately checks the kernel rows and polynomial
reductions used below. Neither replay certifies the analytic arguments or
historical novelty.

## 2. A quantitative lemma excludes all rank-one-valued countersequences

**Lemma.** Suppose F is a homogeneous quartic polynomial, rank-one convex,
and `F(R)>0` for a given nonzero rank-one matrix R. For every matrix B,

```
F(B+R)-F(B)-DF(B):R >= F(R)/3.                            (3)
```

**Proof.** The scalar polynomial

```
g(t)=F(B+tR)=a t⁴+b t³+c t²+d t+e
```

is convex on the entire real line and has `a=F(R)>0`. Consequently
`g''(t)=12a t²+6b t+2c>=0` for every real t. Its discriminant gives
`c>=3b²/(8a)`. Hence

```
g(1)-g(0)-g'(0) = a+b+c
 >= a+b+3b²/(8a)
 = a/3+3(b+4a/3)²/(8a) >= a/3.
```

This proves (3). No compatibility or limiting acoustic argument is used.

For `R=x tensor xi`, `det R=0` and

```
J(R)=|x|⁴[alpha |xi|⁴+beta xi1⁴] >= alpha |R|⁴.
```

Both alpha and beta are positive. Thus, whenever `rank(Dphi)<=1` almost
everywhere, (3) applies pointwise with `R=Dphi` and gives

```
integral [J(B+Dphi)-J(B)] >= (alpha/3) integral |Dphi|⁴,
alpha/3 = 1/8-1/[4(r+2)] > 1/8.                           (4)
```

This includes scalar-target perturbations and one-dimensional laminates.
An affine rank-one contact therefore cannot be a counterexample to TARGET.
A failure must use genuinely rank-two gradients on a positive share of the
fourth-power energy.

## 3. Eight exact kernel equations give qualitative rigidity

Put

```
X(A)=(a-d,b+c),
Y(A)=(-3b+(2r+1)c,(2r+1)a+3d).
```

Eight entries of `ell=C_r^T Z`, verified directly from the original JSON,
are, with zero-based entry numbers,

```
ell0 = Y1 z0/(2r+1),  ell3 = Y1 z3/(2r+1),
ell6 = Y2 z0/3,       ell9 = Y2 z3/3,
ell2 = X2 z2,         ell5 = X2 z5,
ell8 = -X1 z2,        ell11 = -X1 z5.                     (5)
```

All denominators are nonzero for `r<-2`. Since S is positive definite,
`D_r(A,D²psi)=0` implies

```
X(Dpsi) psi_yy=0,      Y(Dpsi) psi_xx=0,                 (6)
```

with componentwise vector multiplication understood. These are necessary
kernel equations; the full kernel has additional equations which are not
needed in the following rigidity argument.

**Analytic rigidity.** Let psi be real analytic on the whole plane and
satisfy the full zero-density relation, hence (6). Suppose either

1. `psi(x)=Bx+eta(x)` with eta Schwartz; or
2. `|psi(x)|<=C(1+|x|^(1/2))`.

Then `Deta=0` in case 1, and `Dpsi=0` in case 2.

To see this, if X is not identically zero, one of its analytic components
is nonzero on an open set. Equation (6) makes `psi_yy=0` there. Analytic
continuation gives `psi_yy=0` everywhere. Similarly, if Y is not identically
zero, then `psi_xx=0` everywhere. If both X and Y are nonidentically zero,
these two identities make psi an affine map plus a vector multiple of xy;
the asserted decay or sublinear growth removes the nonconstant part in the
relevant case.

If `X(Dpsi)` vanishes identically, psi satisfies the ordinary planar
Cauchy-Riemann equations. Its components are harmonic. In case 1, decay
first forces `X(B)=0`, and eta is a Schwartz harmonic function, hence zero.
In case 2, the interior gradient estimate for entire harmonic functions,
`|Dpsi(x0)|<=C R^(-1) sup_(B_R(x0))|psi|`, tends to zero as R tends to
infinity because the growth is of order R^(1/2).

If `Y(Dpsi)` vanishes identically, put `k=-(2r+1)/3>1`. The equations are

```
psi2,y=k psi1,x,       psi2,x=-psi1,y/k.
```

Cross differentiation gives, for each component,

```
k² psi_xx+psi_yy=0.                                      (7)
```

This is a uniformly elliptic equation for this fixed r. A linear change of
coordinates reduces it to the harmonic case, giving the same conclusion.
This covers all cases and proves the rigidity statement.

The same argument on a rectangular torus, after subtracting Bx, forces a
zero-density periodic perturbation to be constant. Analytic continuation,
periodicity, and the elliptic equations suffice; no decay at spatial infinity
is needed there.

## 4. Strict Jensen positivity for each individual perturbation

**Theorem.** For each fixed `r<-2`, each B, and each nonzero gradient
`Dphi` in the compact smooth or bounded-Lipschitz `W0^(1,4)` class,

```
integral [J(B+Dphi)-J(B)] > 0.                            (8)
```

The periodic statement holds when the periodic gradient is nonzero.

**Proof.** The zero extension of a `W0^(1,4)` perturbation is compactly
supported. For every positive heat time its convolution is real analytic
and Schwartz. If the initial gap were zero, (2), nonnegativity of the
density, and the zero infinite-time limit would force the density to vanish
at every positive time. Analytic rigidity from §3 then makes every heat
gradient zero. Heat convolution is injective on these data: its Fourier
multiplier is everywhere nonzero, so local distributional inversion shows
that a zero heat gradient had zero initial gradient. This contradicts the
hypothesis. Periodic heat and the torus rigidity argument give the periodic
version.

This is strict positivity for each fixed perturbation. It does not give a
uniform lower bound on a normalized sequence of perturbations, and it is
not an assertion of the standard quantitative strong-quasiconvexity
condition.

## 5. The critical homogeneous angular infimum is positive

Let `h in W^(1,4)(S1;R²)` be periodic and define, with its continuous
representative,

```
phi(rho,theta)=rho^(1/2)h(theta),   phi(0)=0,
A_h(theta)=(h(theta)/2 | h'(theta)) (e_r(theta) | e_theta(theta))^T.
```

Then `Dphi=rho^(-1/2) A_h` and

```
|A_h|²=|h|²/4+|h'|².
I_r(h)=integral_0^(2pi) J(A_h(theta)) dtheta,
N(h)=integral_0^(2pi) |A_h(theta)|⁴ dtheta.                (9)
```

**Theorem.** For every fixed real `r<-2` there is a positive, possibly
nonexplicit number `delta_r` such that

```
I_r(h) >= delta_r N(h) for every such periodic h.          (10)
```

No value of delta_r and no uniformity in r are claimed.

### 5.1 An exact heat identity for smooth angular data

Initially suppose h is smooth. Its homogeneous phi has sublinear growth,
so Gaussian convolution is defined although phi is not compactly supported.
Let `psi_t=exp(tL)phi`. Heat scaling gives

```
psi_t(x)=t^(1/4) psi_1(x/sqrt(t)),
Dpsi_t(x)=t^(-1/4) Dpsi_1(x/sqrt(t)).                     (11)
```

At large radius R, local small-time heat expansion on an annulus gives

```
Dpsi_1(R e_r(theta))
 = R^(-1/2)[A_h(theta)+O(R^(-2))],
D²psi_1=O(R^(-3/2)).                                    (12)
```

The errors and needed angular derivatives are uniform in theta for this
fixed smooth h. The nonsmooth origin contributes only an exponentially
small Gaussian tail in this far-field expansion.

Set `E_R(t)=integral_(|x|<R) J(Dpsi_t)`. Quartic homogeneity and (11) give
`E_R(t)=E_(R/sqrt(t))(1)`. Differentiating this identity in the radius,
then using (12), yields

```
lim_(R->infinity) E_R'(t)=-I_r(h)/(2t).                  (13)
```

Integration by parts in the ball, followed by the exact two-form correction,
gives the other expression for this derivative. All boundary terms vanish:
the heat flux is of size `|A|³|DA|=O(R^(-3))` and the cubic primitive
pullback has the same size, whereas the circle length is O(R). The corrected
density is `O(R^(-4))`, hence integrable at infinity. It is smooth at the
origin for positive t. Thus

```
I_r(h)=2t integral_R² D_r(Dpsi_t,D²psi_t),
in particular I_r(h)=2 integral_R² D_r(Dpsi_1,D²psi_1).   (14)
```

This is an exact identity. It uses ordinary radial scaling, which commutes
with every fixed constant anisotropic diffusion through (11); full right
rotational invariance of J is not needed.

### 5.2 No nonzero angular profile has zero energy

Equation (14) gives nonnegativity. If its left side is zero, the positive
Gram density is zero everywhere at time 1. The analytic heat field has
the sublinear growth required in §3, so its gradient vanishes. Heat
injectivity on tempered distributions then implies that the initial phi
has zero gradient. More explicitly, the nonvanishing Gaussian Fourier
multiplier makes the initial Fourier transform supported at frequency zero;
the initial map is therefore a polynomial. Homogeneity of degree 1/2
forces that polynomial to be zero. Hence h is zero.

For general `h in W^(1,4)(S1)`, approximate strongly by smooth periodic h_n.
The angular energies and N(h_n) converge by quartic continuity. The
homogeneous maps have a common `C(1+|x|^(1/2))` growth bound, and their
positive-time heat fields and derivatives converge on compact sets by
Gaussian convolution. Fatou applied to the nonnegative densities in (14)
therefore gives

```
I_r(h) >= 2 integral_R² D_r(D exp(L)phi,D² exp(L)phi).     (15)
```

Consequently `I_r(h)>=0`, and equality again forces h=0 by analytic rigidity
and heat injectivity. The one-sided extension (15) is sufficient here; an
unproved equality for rough angular data is not required.

### 5.3 Compactness upgrades angular strictness to an angular margin

Suppose (10) were false. By homogeneity, choose `N(h_n)=1` and
`I_r(h_n)->0`. Formula (9) bounds h_n in `W^(1,4)(S1)`. Pass to a subsequence
with h_n converging uniformly to h and h_n' converging weakly in L4 to h'.

For each theta and each fixed h, the integrand

```
v -> J(h tensor e_r/2+v tensor e_theta)
```

is convex in the two-vector v, because differences are rank-one matrices.
Its integral is a continuous convex functional of v in L4, hence weakly
lower semicontinuous. Replacing h_n by h in that integrand changes the
integral by at most

```
C_r ||h_n-h||_infinity
    integral (|h_n|+|h|+|h_n'|)³ ->0.
```

Therefore `I_r(h)<=liminf I_r(h_n)=0`. Section 5.2 forces h=0, so h_n tends
uniformly to zero.

Now apply the pointwise rank-one Bregman lemma (3) with
`B=h_n tensor e_r/2`, `R=h_n' tensor e_theta`. Since `J(B)>=0` for rank-one B,

```
I_r(h_n) >= (alpha/3) integral |h_n'|⁴
             -C_r ||h_n||_infinity³ integral |h_n'|.     (16)
```

The last term tends to zero. The assumed energy limit then forces
`h_n'->0` strongly in L4. Together with uniform convergence of h_n to zero,
this contradicts `N(h_n)=1`. Thus delta_r is strictly positive. This
argument proves existence, not a numerical value or a computable enclosure.

### 5.4 Consequence for logarithmic annular concentration

A smooth inner and outer radial cutoff of the degree-1/2 homogeneous map
on an annulus `exp(-T)<rho<1` has

```
integral J(Dphi_T)=T I_r(h)+O(N(h)),
integral |Dphi_T|⁴=T N(h)+O(N(h)).                        (17)
```

The transition constants are independent of T and uniformly bounded when
N(h)=1: the radial cutoff differentiates h, and (9) controls both h and h'.
The inner transition cost is scale invariant at degree 1/2. Thus (10)
prevents a zero ratio from this construction at B=0 even if the angular
profile varies with T. The same conclusion holds at any fixed B: its
quadratic and cubic cross terms have uniformly bounded integrals because
`rho^(-1/2)` is radially L2 and L3 at the origin. No assertion is made here
for an affine background B_T growing with T. The lower bound applies to
this critical homogeneous mechanism, not to arbitrary two-dimensional
concentration or general multiscale gradients.

## 6. Exact reduction of the remaining all-affine question

For any compatible zero-mean gradient q, quartic polarization gives

```
K(q)=integral J(q),
L(q)=integral DJ(q),
M(q)=(1/2) integral D²J(q),
integral[J(B+q)-J(B)] = B^T M(q) B+L(q)^T B+K(q).        (18)
```

The vectorization order of B is row-major. All-background QC implies that
M(q) is PSD and L(q) is in its range; otherwise the right side is negative
for some B. Consequently its exact minimum over all affine backgrounds is

```
K(q)-(1/4)L(q)^T M(q)^+ L(q),                            (19)
```

where `+` is the Moore-Penrose inverse. TARGET is exactly the assertion
that (19) is at least `gamma_r integral |q|⁴` for every compatible q.

At B=I, if `q=[[p,q],[w,z]]`, the integrated quadratic term simplifies to

```
integral [((r+1)p+z)²+r(r+2)w²/3].                        (20)
```

The discarded term is exactly `(r+2) integral det(Dphi)=0`. On a torus
its exact kernel has `phi2,x=0` and `phi2,y=-(r+1)phi1,x`, forcing phi2
constant and phi1 to depend only on y. The cubic term is zero on this
kernel. This agrees with the rank-one lower bound in §2. Nearly axial soft
waves and general nonlinear rank-two gradients still require a quantitative
estimate; (20) alone does not provide one.

## 7. Numerical checks and their limited interpretation

The saved scripts search represented compatible Fourier gradients and
critical homogeneous angular maps. Trig quadrature uses more than four
times the largest represented frequency, so it integrates the represented
quartic polynomial exactly in exact arithmetic. Optimization and linear
algebra remain floating-point computations, and local optimization has no
global guarantee.

At r=-2.5, the affine-minimized two-dimensional Fourier searches returned
ratios approximately 1.02883 (K=2), 0.617273 (K=4), and 0.419397 (K=8).
An aspect ratio of 0.1 gave 1.19808 at K=2 and 0.777143 at K=4.
The degree-1/2 angular searches at K=12 returned approximately 0.127771
for r=-2.5, 0.100235 for r=-3, and 0.0976675 for r=-4.

These are candidate upper bounds on the respective infima, subject to
roundoff. They are not certified lower bounds. Some unconstrained optimizer
runs grew the coefficient scale and stopped with a small Euclidean gradient;
homogeneity makes that stopping criterion unreliable without a scale gauge.
The proofs in §§2–5 do not use any numerical result.

For the elementary radial profile `h=(cos theta,sin theta)`, the exact
angular ratio is

```
(59r³+299r²+572r+384)/[1200(r+2)].                        (21)
```

`EXACT_REDUCTIONS.py` checks this algebra. Equation (21) is an explicit
test-profile upper bound, not the angular minimum.

## 8. Classical comparisons and why they do not close TARGET

The inherited heat/exact-form method is due to
[Bruno and Pasqualotto](https://arxiv.org/html/2608.06367v1), §§2–3. Their
full left-and-right rotation theorem does not directly cover J: the present
right symmetry is only an elliptic quarter turn. This worker uses the
separate supplied anisotropic certificate.

The standard strong-quasiconvexity hypothesis used by
[Gmeineder and Kristensen](https://arxiv.org/pdf/2209.01613), equation (1.7)
and §6, subtracts a positive multiple of
`V_p(A)=(1+|A|²)^(p/2)-1` at a background. At p=4 this entails a quadratic
margin for small gradients. The exact acoustic contacts exclude that
hypothesis at the contact backgrounds. TARGET asks only for a pure fourth
power and is weaker. Coercivity/QC equivalences cannot supply their own
missing quantitative hypothesis.

The [Friesecke–James–Müller rigidity theorem](https://www.aem.umn.edu/~james/research/Publications_Files/PDF/73.pdf)
estimates the gradient distance from a single rotation using distance from
SO(n). Here the nonnegative quantity is a quadratic form in products of a
gradient and a second jet, and its zero relation has two elliptic strain
planes. The required metric and energy hypotheses are therefore not supplied
by that theorem. The exact analytic inclusion in §3 proves a qualitative
rigidity result; a suitable quantitative stability estimate remains missing.

The [Bañuelos–Janakiraman complex Beurling estimate](https://www.math.purdue.edu/~banuelos/Papers/Beur_Ahl.pdf)
controls the compatible gradient by its anti-conformal strain in L4. It
supports the inherited interior-margin corollary after subtracting epsilon H.
At the sharp boundary that subtraction fails rank-one convexity, so the
elliptic bound alone cannot produce the needed energy lower bound.

## 9. Exact remaining gate and N866 consequence

The all-affine pure fourth-order compatible margin is **UNRESOLVED**. The
following are not substitutes for it: strict Jensen positivity, positivity
of S on its reduced support, exclusion of rank-one-valued counterexamples,
or the positive homogeneous angular margin. A normalized sequence can still
in principle escape through genuinely two-dimensional oscillation,
concentration, affine-background growth, or combinations of those effects.

The receiving N866 horizon proof uses an actual constant gamma controlling
near-minimizer fourth-power gradient energy on arbitrary zero-end strip
loops. No such gamma is produced for sharp J here. N866 remains established
only for its particular certified G and specified effective endpoint data;
its same-G improved constant is unaffected. No sharp-J storage computability,
practical solver advantage, or executed storage value follows from this work.

A decisive continuation is either a quantitative version of §3 controlling
the residual (19) for all compatible q, or an explicit rank-two compatible
sequence making (19)/integral|q|⁴ tend to zero. Merely increasing a Fourier
cutoff would not resolve either claim.
