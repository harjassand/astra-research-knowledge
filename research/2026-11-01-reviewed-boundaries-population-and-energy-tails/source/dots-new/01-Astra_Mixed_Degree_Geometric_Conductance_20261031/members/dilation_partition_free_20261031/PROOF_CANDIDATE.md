# Geometric partition cancellation without homogeneous energy

Status: NEW construction, not independently reviewed. Earlier accepted homogeneous,
mobility-family and finite-Jensen source freezes are unchanged.

## 1. Actual model and acquired structural premise

Let s(y)=1+kappa(1-y^2)^2, kappa>0, and F(y,z)=U(s(y)z), z in R^m, m>=1.
The energy U is a finite sum U=sum_(d in D) U_d of nonnegative homogeneous
polynomials, of even degrees2<=d<=p, where p=max D. At least one component has
an acquired coercivity bound U_d>=a||z||^d, a>0. Thus U need NOT be homogeneous.
A concrete sufficient raw grammar below combines a positive quadratic form with
nonnegative pure/mixed quartics and admits nonconvex energies.

Use either the actual isotropic process, or the precisely declared UNIVERSAL
family with any finite constant SPD transverse M, unit longitudinal mobility,
zero cross covariance and matching drift/noise:

  dy=-partial_y F dt+sqrt(2/beta)dW_y,
  dz=-M grad_z F dt+sqrt(2M/beta)dW_z.

The task is equilibrium full-fiber capacity/mass between y<=-1/2 and y>=1/2.
No actual physical membership, arbitrary-start hitting time, angular mixing or
projected Markov description is inferred. An input potential does not by itself
authenticate a particular kinetic matrix/interface.

Precisely, mu=exp(-beta F)dy dz/Z and
cap_mu,M(A,B)=inf_h beta^(-1) int[(partial_y h)^2+grad_z h^T M grad_z h]dmu,
over the weighted H1 affine class h=0 on A and h=1 on B. Truncation to [0,1]
does not increase energy. Smooth/local H1 approximation and Fubini extend the
one-dimensional slice Cauchy inequality below to this class. This definition is
an equilibrium conductance, not a general expected first-passage time.

## 2. Exact geometric cancellation, not energy homogeneity

For every beta>0 let Z_beta=int exp[-beta U(x)]dx. A change of spatial variables
x=s(y)z gives EXACTLY

  int exp[-beta U(s(y)z)]dz = s(y)^(-m) Z_beta.

Hence q(y)=s(y)^(-m), independently of beta and all coefficients of U. There is no
claim that Z_beta factorizes as a power of beta: for mixed degrees it generally
does not. Its entire unknown value cancels from the marginal and rate ratio.
Geometric cancellation holds for any integrable U, but the lower bound below
requires additional structure. The companion counterexample shows this is real.

Set Q=int_R q, MA=int_(1/2)^infinity q, R0=int_-1/2^1/2 s^m,
k_free=1/(beta MA R0). The scalar Dirichlet trial is always the full upper bound.

## 3. Fixed-fiber Cauchy plus Jensen without a Gamma identity

Put s0=s(0)=1+kappa, F0(z)=U(s0 z),
Z0=int exp(-beta F0)dz=s0^(-m)Z_beta, and let rho0 be the normalized density
exp(-beta F0)/Z0. For each fixed z, weighted one-dimensional Cauchy gives

  cap_M >= (1/(beta Z)) int [int_slab exp(beta F(y,z))dy]^(-1)dz.

Write S(z)=int_slab exp[beta(F(y,z)-F0(z))]dy. Then the last integral is
Z0 E_rho0[1/S]. The factor beta in this expectation is ESSENTIAL. Jensen gives
E[1/S]>=1/E[S]. No density or partition constant is sampled/evaluated in execution.

On the slab, r=s(y)/s0 lies in(0,1]. For each d<=p, concavity of t^(d/p) gives

  2-r^d >= (2-r^p)^(d/p).

Since U_d>=0, termwise comparison yields

  2U(s0 z)-U(s(y)z)
    >= U(s0*(2-r^p)^(1/p)*z).

Consequently

  E_rho0 exp[beta(F(y,z)-F0(z))]
    = Z0^(-1) int exp[-beta(2F0-F_y)]dz
    <= (2-r^p)^(-m/p),

where the unknown Z_beta cancels AGAIN by a spatial dilation. Tonelli applies to
these positive integrands. The bound is finite throughout the compact slab.
Jensen is legitimate; S>0, and the parallel integral is finite since
R_z>=exp(beta U(s_min z)) when U is radially nondecreasing, with slab length1.
The stated positive components earn that monotonicity and coercivity.

Define ONE additional scalar resistance

  R_plus=int_slab [s0^(2p)/(2s0^p-s(y)^p)]^(m/p)dy.

As Z mu(A)=Z_beta MA and Z0=s0^(-m)Z_beta, all factors give the finite sandwich

  1/(beta MA R_plus) <= cap_M(A,B)/mu(A) <=1/(beta MA R0).   (G)

No Gamma identity/integral or homogeneous-energy approximation is used. Both
inequalities are uniform over the declared fixed transverse SPD family: the
lower discards its nonnegative energy and the scalar upper has none.

## 4. The organizing condition: radial p-concavity

The comparison really uses concavity of t->U(t^(1/p)x) for every x. Then
U(r x)+U((2-r^p)^(1/p)x)<=2U(x), because the two scalar arguments average to1.
Nonnegative homogeneous components of degrees<=p provide a directly acquirable
sufficient certificate of this radial concavity. This is weaker than homogeneous
energy, but is not an oracle for arbitrary polynomial positivity or shape.

For a smooth U, an equivalent differential sufficient certificate is

  p D U-D^2 U>=0, where D=x.grad_x,

because f(t)=U(t^(1/p)x) has
f''(t)=[D^2 U-p D U](t^(1/p)x)/(p^2 t^2). If U>=0 globally, such a concave
f on (0,infinity) cannot have a negative derivative: its supporting tangent
would eventually force a negative value. Thus D U>=0 also follows, earning the
radial monotonicity used in the Lyapunov proof. Coercivity/integrability is still
separately required. The receiver here uses only the cheap nonnegative-component
certificate; it is NOT a general global-polynomial-positivity solver.

For example, U(x)=x^2-x^4+x^6+x^8 has p8 certificate
8DU-D^2U=12x^2-16x^4+12x^6>=0 (the quadratic 12-16t+12t^2 is positive).
Also U>=3x^2/4+x^8 since their difference is x^2(x^2-1/2)^2. Negative coefficients
are not intrinsically forbidden by the organizing theorem, although this example
is outside the present executable mixed-quadratic/quartic finder.

Geometric partition cancellation alone does NOT imply(G). An arbitrary coercive
energy may have radial wells and violate the comparison. Do not discard the
component-sign/degree premise after recognizing a coordinate dilation.

## 5. Global process and tail, with all chain-rule factors

Let D(y,z)=z.grad_z F=sum_d d*s(y)^d U_d(z)>=0. In particular grad_z F is the
physical z derivative of U(s z), including its chain-rule factor s. Then
partial_y F=(s'/s)D.

For K=1+kappa and each fixed SPD M choose

  V_M=1+y^2+K z^T M^(-1)z.

Its generator satisfies

  L_M V_M=-2[y s'/s+K]D+2(1+Km)/beta <=2(1+Km)/beta,

because y s'>=-kappa and s>=1 imply y s'/s>=-kappa. Thus the bracket is>=1.
The stopped Lyapunov argument gives nonexplosion for each fixed finite M; no
uniform relaxation rate is asserted. Smoothness, finite Gibbs and the constant
block/FDT interface give the conservative reversible Dirichlet process.

For T>1,

  int_T^infinity q <= kappa^(-m)(1-T^-2)^(-2m)
                         * T^(1-4m)/(4m-1).              (T)

This tail is finite already for m>=1. Physical m, not polynomial degree or the
auxiliary exponent m/p, controls this tail. Its exact rational upper bound is
charged in the mass integral; no reflecting boundary at finite T is substituted.

## 6. Acquired raw aligned mixed quadratic/quartic consumer

The sufficient first grammar uses actual physical coordinate axes:

  U2=sum_i q_i z_i^2, q_i>0,
  U4=sum_i d_i z_i^4+sum_(i<j)J_ij z_i^2 z_j^2,
  d_i,J_ij>=0 (omitted entries are zero).

U2 alone acquires U>=q_min||z||^2. With nonzero U4 this is genuinely mixed energy.
Large positive mixed quartics may make the full U nonconvex; positivity of each
homogeneous component, not convexity or mixing, is the premise.

From the COMPLETE expanded raw F, the quadratic part has a unique absent aligned
y axis and positive pure quadratic coefficients on all other axes. For a degree-d
fiber monomial, the ratio of its y^2 coefficient to its y^0 coefficient is
-2d*kappa/(1+kappa). One quadratic monomial acquires t=kappa/(1+kappa) and then
kappa=t/(1-t). All components/signs/coercivity and the ENTIRE identity
F=U(s(y)z)=s(y)^2 U2(z)+s(y)^4 U4(z) must then be verified. The full degree can be20;
a Hessian or a few matching coefficients alone do not admit the model.

A generic rotation, non-diagonal quadratic form, negative component or arbitrary
SOS decomposition may return UNKNOWN under this sufficient finder. No useful
basis is assumed for free. Strong ordinary nullspace/positivity machinery gets
the same raw input if a later broader finder is compared.

The implementation receive_dilation.py scans and binds every exponent and exact
rational coefficient, derives the axis/parameter/components, and verifies the
entire identity. It allows U4=0 as the stronger ordinary quadratic comparator;
then p=2, rather than gratuitously paying the p4 comparison. With any nonzero U4,
p=4. The diagonal-positive U2 is deliberately sufficient, not a claim to recognize
every polynomial admitting such coordinates.

## 7. Exact scalar receiving and honest losses from the older theorem

q=s^-m and the old resistance integrand s^m are rational at rational y. For p4,
the extra integrand is the fourth root of a rational power; reducing m/p first
allows exact rational powers whenever divisible, and square/fourth roots otherwise.
All powers, integer divisions/roots, precision, tail and monotone quadrature are
paid. The extra integrand decreases on the half slab, since s decreases there.
It is >=s^m because s0^(2p)-s^p(2s0^p-s^p)=(s0^p-s^p)^2>=0.

Outward intervals [L_M,U_M],[L_0,U_0],[L_plus,U_plus] yield
[1/(beta U_M U_plus),1/(beta L_M L_0)]. A requested TOTAL width is checked exactly;
intrinsic comparison slack can cause UNKNOWN even with finer arithmetic.

The earlier exact angular-independent robust-mobility OPEN-range endpoint formula
does NOT carry over by changing filenames. For each mixed U the fixed-fiber lower
endpoint can depend on its energy mixture. Equation(G) gives a universal OUTER
bound, not equality of all parallel endpoints or exact actual rates. No inverse
mobility, actual model calibration, experimental claim or novelty is added.
