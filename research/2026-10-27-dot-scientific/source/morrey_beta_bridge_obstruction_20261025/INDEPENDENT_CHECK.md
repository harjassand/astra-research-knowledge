# Independent audit: beta-elliptope bridge obstruction

25 October 2026. This verifies an obstruction to the specified interpolation and certain transitions between its marginals. It makes no claim to solve the full Morrey problem or to exclude a null stress from the origin to the actual cosine law.

## Verdict

The supplied moments and the continuous-martingale no-go are correct. The endpoint need not be included in the original time domain: bounded martingale convergence supplies it, and the beta laws have the required actual-cosine weak limit.

There is also an explicit globally defined convex scalar separator. Its composition with the determinant minus a linear functional is globally rank-one convex on the full space of 2-by-2 matrices, not merely on the three-dimensional symmetric subspace. A bounded-slope version proves that **no finite PSD, measurewise J-null stress can carry the marginal at t=99/100 to the endpoint marginal**, even if its spatial support was not assumed compact.

## 1. Independent exact moment calculation

Let eta>0 and t=1/(eta+1). Under the normalized density F^(eta-1) on the open correlation elliptope,

    F=1-u^2-v^2-w^2+2uvw,

the change of variables

    w=uv+sqrt((1-u^2)(1-v^2)) R

gives independent u,v,R with densities proportional to

    (1-u^2)^(eta-1/2), (1-v^2)^(eta-1/2), (1-R^2)^(eta-1).

This follows directly from F=(1-u^2)(1-v^2)(1-R^2) and the Jacobian sqrt((1-u^2)(1-v^2)). In particular,

    E u^2=t/2,
    E u^4=3t^2/[4(1+t)],
    E R^2=t/(2-t).

Coordinate sign changes with product +1 preserve the joint law. Consequently a monomial can have nonzero expectation only when its three exponents have the same parity. Permutations also preserve the law. The conditional representation then gives

    E u^2 v^2=t^2/4,
    E uvw=t^2/4,
    E u^3 v w=E u^4 v^2=3t^3/[8(1+t)],

    T := E u^2 v^2 w^2
       =(E u^4)^2 + (E[u^2(1-u^2)])^2 E R^2
       =t^3(1+4t)/[8(1+t)^2].

For q=uv+uw+vw, s=u+v+w, and H=q-s, expansion and the parity rule yield

    E q=E s=0,
    E q^2=3t^2/4,
    E qs=3t^2/4,
    E s^2=3t/2,

    E q^3=6T,
    E q^2 s=9t^3/[4(1+t)],
    E qs^2=3t^2/2,
    E s^3=3t^2/2.

Thus, independently of a symbolic package,

    E H=0,
    M2(t):=E H^2=3t(2-t)/4,
    M3(t):=E H^3=3t^2(4-t^2)/[4(1+t)^2].

In eta coordinates these are

    M2=3(2eta+1)/[4(eta+1)^2],
    M3=3(2eta+1)(2eta+3)/[4(eta+1)^2(eta+2)^2].

An independent exact SymPy monomial expansion also reproduces these expressions. The derivative facts are

    M2(1)=3/4, M2'(1)=0,
    M3(1)=9/16, M3'(1)=3/16.

## 2. Endpoint identification

As t increases to 1 (eta decreases to 0), u and v tend to independent arcsine variables. Also R^2 has Beta(1/2,eta) distribution, so R tends to an independent fair sign taking values -1,+1. The continuous conditional formula therefore identifies the weak limit.

If x,y are independent uniform phases, conditional on (cos x,cos y), the product of the signs of sin x and sin y is a fair independent sign. Hence

    (u,v,w) in the limit has law (cos x,cos y,cos(x+y)).

All variables lie in the compact cube, so all the displayed polynomial moments converge as well.

## 3. Martingale obstruction, including an open terminal time

Put J=(ee^T-I)/2, e=(1,1,1), so q(z)=z^T Jz and D^2H=2J. Suppose Z_t is a continuous martingale with these marginals and

    J:d<Z>_t=0

pathwise as a signed measure in time. Ito's formula gives

    dH(Z_t)=grad H(Z_t) dot dZ_t.

At every deterministic time Z_t lies in [-1,1]^3 almost surely. A countable dense-time argument and continuity put its whole path in that cube. Therefore H(Z_t) is a bounded local martingale, hence a true uniformly integrable martingale. For example |H|<=6 follows from the cube bound below.

If the process is originally defined only for t<1, the coordinatewise bounded-martingale convergence theorem gives Z_1=lim_(t up to 1) Z_t almost surely and in every finite L^p. Its law is the weak limit identified above; H(Z_t) also converges to H(Z_1). This extends the martingale to the terminal time. No Markov property or absolute continuity of the bracket is used.

Write X=H(Z_t), Y=H(Z_1). The martingale identity implies

    E(Y-X)^2=M2(1)-M2(t)=3(1-t)^2/4.

The exact identity

    y^3-x^3-3x^2(y-x)=(y-x)^2(y+2x)

and E[Y-X | F_t]=0 give, with |X|,|Y|<=6,

    |M3(1)-M3(t)| <=18 E(Y-X)^2
                        =27(1-t)^2/2.

But

    M3(1)-M3(t)=3(1-t)/16+O((1-t)^2).

The linear left side cannot satisfy the quadratic bound as t increases to 1. This proves the no-go. The nullity assumption is local/measurewise, not merely zero total expected contraction of the bracket.

## 4. Explicit global separator

The polynomial H is affine in each cube coordinate separately. Its extrema on the cube are therefore attained at vertices. Their values are -2,0,6, giving

    -2<=H<=6 on [-1,1]^3.

Define the following scalar function on the entire real line:

    psi(x) = -108x-144,                                  x<=-3;
             8(x+3)^3-108(x+3)+180,              -3<=x<=-2;
             18x^2-x^3,                          -2<=x<=6;
             108x-216,                                   x>=6.

It is C^2 at all three junctions. Its second derivatives, in the same order, are

    0; 48(x+3); 36-6x; 0,

all nonnegative. Thus psi is globally convex, with |psi'|<=108 and at most linear growth. On the whole support of every marginal,

    psi(H)=18H^2-H^3.

Let P(t)=E psi(H(Z_t))=18M2(t)-M3(t). Then

    P'(1)=-3/16<0,

and the exact rational gap is

    P(1)-P(99/100)=-942849/1584040000<0.

More generally,

    P(1)-P(t)
      =3(t-1)(68t^3+68t^2-63t-69)/[16(t+1)^2].

This violates scalar convex order for H, providing a finite-pair witness rather than only an asymptotic argument. If a strictly interior pair is wanted, one also has

    P(399/400)-P(199/200)
      =-1653596680783/7227312184960000<0.

### Extension to the full matrix space

For the physical map

    B(u,v,w)=[[u+w,w],[w,v+w]],

define on all real 2-by-2 matrices

    h(A)=det A-tr A+(A12+A21)/2,
    G(A)=psi(h(A)).

Then h(B(z))=H(z). On any rank-one line A+rD, det(A+rD) is affine in r because det D=0. Thus h is affine along that line and G is convex along it. This proves global rank-one convexity. In fact G is polyconvex, because it is a convex function of the affine expression in (A,det A). No unsupported global extension from the symmetric subspace is being assumed.

Equivalently g(z)=psi(H(z)) is globally convex on each q-null line in coefficient space.

## 5. Direct exclusion of a finite transition stress

Suppose T is a finite symmetric PSD matrix-valued measure on R^3 satisfying

    J:T=0 as a scalar measure,
    integral D^2 f:dT = integral f d(mu_1-mu_(99/100))

for every compactly supported smooth f. A positive constant multiplying either side does not affect the argument.

With g=psi composed with H, the chain rule gives

    D^2g=psi''(H) grad H tensor grad H +2psi'(H)J.

Hence positivity and measurewise nullity imply

    D^2g:dT=psi''(H) (grad H)^T dT grad H >=0.

The possibly unbounded Hessian causes no gap. Choose nonnegative smooth cutoffs chi_R equal to 1 on the radius-R ball and zero outside the radius-2R ball. Since psi has bounded slope,

    |g(z)|<=C(1+|z|^2),
    |grad g(z)|<=C(1+|z|).

Apply the stress identity to chi_R g. (The identity extends from C_c^infinity to C_c^2 by local C^2 approximation.) Its Hessian is chi_R D^2g plus cutoff terms. On their supporting annulus, those terms have norm bounded uniformly in R, since |grad chi_R|=O(1/R), |D^2 chi_R|=O(1/R^2), and the two growth bounds hold. Their integrals tend to zero because tr T is a finite measure. The main term is nonnegative for every R. For R large enough the right side is exactly

    P(1)-P(99/100)<0.

Letting R tend to infinity is a contradiction. Thus the finite-stress exclusion requires neither compact support of T nor unproved integrability of the full Hessian against T.

The same argument excludes the displayed strictly interior pair. It also explains why the global bounded-slope extension is preferable to citing the cubic polynomial alone.

## 6. Scope and cautions

- The proposed family cannot be the marginals of a continuous martingale with determinant-null bracket, regardless of a singular or regular time clock.
- Some terminal transitions in this family are impossible even as finite positive J-null stresses, and even in the broader rank-one-convex order.
- The result does not exclude all intermediates, every martingale route, or a finite positive J-null stress from delta_0 to the actual cosine law. The separator expectation at the endpoint is P(1)=207/16>0, whereas psi(H(0))=0, so this witness is consistent with that unresolved origin-to-endpoint direction.
- The result depends on the specified correlated actual-cosine endpoint. No independent-coordinate replacement, numerical scan, simulation, external search, or historical-originality assertion was used.

## Verification provenance

The conditional beta formula and target claims were supplied by the parent task. The moment calculation in section 1 was derived afresh; an exact SymPy expansion independently checked it and all rational gaps. The physical matrix map was checked against the local `STEIN_CAP_OBSTRUCTION.md` work product. All proofs and the global separator above were explicitly rechecked in this audit.
