# From a rational angular identity to full strong quasiconvexity

30 October 2026. Root's independent quantitative reconstruction for A's
original quartic. This supplies an analytical receiver for a LITERAL
polynomial identity/PSD certificate. It does not certify those premise
bytes, historical novelty or the target's non-polyconvexity by itself.
Those are separate source/certificate obligations being challenged by T.

Let F be the actual homogeneous quartic on2-by-2 matrices, A=(a,b,c,d)
in row order, T=|A|^2. Let alpha=P5(A)/T on A!=0, for a polynomial1-form
P5 homogeneous of degree5, extended by0 at0. Let omega=dalpha. For any
compatible second jet h=(u1_xx,u1_xy,u1_yy,u2_xx,u2_xy,u2_yy), put

 B1=(h0,h1,h3,h4), B2=(h1,h2,h4,h5),
 J(a,b,c,d)=(-c,-d,a,b),
 D=F''(A)[B1,B1]+F''(A)[B2,B2]
       +nu(F''(A)[B1,JB2]+F''(A)[B2,JB1]).

Assume the exact certificate proves

 T^2 [D+omega_A(B1,B2)]=z(A,h)^T Q z(A,h),
 Q>=I/2000, |nu|<1/1000,                              (1)

where z lists EACH degree3 monomial in the four A entries times EACH of
the six h entries, exactly once. These are the concrete symbolic premises,
not an optimization-status or finite-grid substitute.

## 1. The origin and the null integral

alpha is smooth off0 and homogeneous degree3. On the unit sphere all its
derivatives are bounded. Its derivatives of orders0,1,2 consequently scale
as |A|^3,|A|^2,|A| and extend continuously by0 at the origin. Successive
difference quotients show these are the actual derivatives there. Hence
alpha is C^2 globally, omega is C^1, homogeneous degree2, and its pullback
under every smooth periodic A is an exact2-form. Stokes gives

    integral omega_A(partial_x A,partial_y A)=0.

No third derivative at0, analytic extension or punctured-domain boundary
term is silently assumed. Smooth approximation of alpha also gives the
same pullback identity if desired.

## 2. A genuinely smoothing compatible-gradient flow

For arbitrary constant M and smooth periodic phi:T^2->R^2, evolve

    phi_t=Delta phi+2nu J2 phi_xy,
    J2=[[0,-1],[1,0]], A=M+Dphi.

On Fourier mode k its propagator is heat decay exp(-|k|^2 t) times a
real orthogonal rotation exp(-2nu kx ky J2 t). Thus the solution remains
smooth and periodic, A is always a compatible gradient, and A->M smoothly
as t->infinity. A scalar positive heat kernel is unnecessary. Normalizations
for a2pi-periodic torus only change the Fourier notation.

Integration by parts gives

    d/dt integral F(A)=-integral D.

The two cross terms have identical INTEGRALS, since each arises by
integrating DF(A).J partial_xy A along one of the two coordinates. No
pointwise identity of those cross terms is required. Adding the Stokes
integrand leaves this energy derivative unchanged.

## 3. Explicit coercivity and integration

Every multinomial coefficient in T^3 is at most6. Therefore
sum_(|beta|=3) A^(2beta)>=T^3/6. Equation(1) implies, including A=0 by
continuity,

 D+omega_A(B1,B2)>=T |h|^2/12000.

Because |DA|^2=|B1|^2+|B2|^2<=2|h|^2, the F energy gap is at least

    (1/24000) integral_0^infinity integral |A|^2 |DA|^2. (2)

For G(A)=|A|^4, ||G''(A)||<=12|A|^2. Its corresponding skew-flow dissipation
satisfies |D_G|<=12(1+|nu|)|A|^2|DA|^2 by Cauchy--Schwarz. The SAME flow
therefore gives

 integral G(M+Dphi)-G(M)
 <=12(1+|nu|) integral_0^infinity integral |A|^2|DA|^2.  (3)

Pointwise uniform convexity gives
G(M+v)-G(M)-DG(M).v>=|v|^4/3. For |v|=1 the minimum occurs at
M=-(1/3)v, with no perpendicular component; scaling proves the general
case. The linear term integrates to0 for periodic gradients. Combining
(2),(3) proves

 integral [F(M+Dphi)-F(M)]
 >= [864000(1+|nu|)]^-1 integral |Dphi|^4
 >= (1/900000) integral |Dphi|^4.                     (4)

The bounds themselves imply finiteness of the required integrals; one can
first integrate over finite time and then take the monotone bound/heat
limit. No contraction of the skew semigroup in L4 was used.

## 4. Full test class

For a smooth compactly supported variation on an arbitrary bounded open
domain, extend it by0 into a larger rectangular periodic cell. The outside
integrand and gradient variation vanish, so(4) gives the domain inequality.
Density then extends it to W0^(1,4) variations, since F has quartic growth
and Dphi converges in L4. This is full strong quasiconvexity of the FIXED F,
not a finite-mode, one-background or rank-one test.

Actual application still requires the exact target F, correct compatible
jet map and primitive signs, the full polynomial identity, the Gram lower
bound and the separate non-polyconvexity source. The nearby ordinary-PC
control is a different energy. A successful application is a mathematical
result, with no claimed material, device or civilisation-level capability.
