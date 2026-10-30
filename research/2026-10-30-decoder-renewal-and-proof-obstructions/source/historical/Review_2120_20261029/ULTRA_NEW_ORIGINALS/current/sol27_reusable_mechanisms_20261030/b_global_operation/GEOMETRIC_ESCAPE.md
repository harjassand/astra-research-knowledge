# The scalar geometric escape and a paid nonlinear conjugacy

B, 30 October 2026. Two complementary constructions distinguish a real
escape from the linearization barrier from a renamed old QC proof. The
first classifies the infinitesimal rank-one-image-preserving scalar speed;
the second explicitly exports a known heat proof by inverse deformation.
Neither is presented as a new solution of the unrestricted QC problem.

## 1. Rank-one image dimension is different from a fixed image curve

Consider u_t=a(Du) Delta u, where a is scalar and its pullback
(v,p)->a(v tensor p) is C1 for v,p!=0; C1 coefficients away from zero
are a sufficient, stronger hypothesis.
At a local rank-one map u=gamma(g), with gamma'!=0 and grad g!=0, write

    v=gamma'(g), w=gamma''(g), p=grad g,
    f=a(v tensor p) Delta g, h=a(v tensor p)|p|^2.

Then u_t=v f+w h. Differentiation gives the exact determinant identity

    (det Du)_t=det(v,w) [g_x h_y-g_y h_x].                          (1)

Terms containing f or gamma''' cancel. Consequently normal curve motion
does not itself destroy rank-one image DIMENSION: it is allowed if its
normal velocity depends only on the curve parameter g. Keeping the SAME
fixed curve would be a stronger and inappropriate requirement here.

## 2. Tangency classification on every nonzero rank-one gradient

Suppose (1) vanishes for EVERY curve/scalar local jet. Choose det(v,w)!=0.
For fixed v, the Hessian of g is arbitrary. The terms depending on it are

    -p2 h_(p1) g_xx
    +(p1 h_(p1)-p2 h_(p2))g_xy
    +p1 h_(p2)g_yy.

Since p!=0, all three coefficients vanish only when D_p h=0. Thus

    a(v tensor p)|p|^2=c(v),                                      (2)

independent of nonzero p. Factorization invariance under
(v,p)->(s v,p/s) gives c(sv)=s^-2 c(v). If a is invariant under output
rotations, c is radial; hence for one constant c0,

    a(A)=c0/|A|^2 on EVERY nonzero rank-one A.                      (3)

Conversely (3) makes h=c0/|gamma'|^2 depend on g alone, so it gives the
claimed infinitesimal tangency. This is a complete local-jet equivalence,
not a theorem of global PDE existence or invariant-manifold regularity.

For a>=0, either c0>0 and this speed is singular as A->0, or c0=0 and
the speed vanishes on all rank-one gradients. The latter makes every
periodic rank-one-image map stationary, so it cannot converge them all to
constants. For example u=(cos x,sin x) has nonzero rank-one Du everywhere.
There is therefore no bounded continuous-at-zero, output-isotropic scalar
diffusion which is tangent to every rank-one image and also smooths all
such periodic maps to constants.

For the pure nonnegative energy integral(det Du)^2, exact monotonicity
from zero-energy rank-one data would REQUIRE rank-one preservation as
long as a sufficiently smooth solution exists. This observation is used
only to explain the geometry of the operation. It does not transfer the
tangency requirement to det^2+epsilon|Du|^4 or prove those energies QC.

## 3. An actual established geometric speed hits the singular branch

[Andrews--Carapetis, arXiv1609.08317v1](https://arxiv.org/html/1609.08317),
Theorem1, proves global smooth existence, preservation of diffeomorphisms
and convergence to a harmonic affine map for flat-torus diffeomorphisms
under a(A)=1/(|A|^2+2|det A|). Its boundary value at rank-one A is EXACTLY
1/|A|^2, consistent with the rank-one tangency classification (3).
This is a controlling positive predecessor,
not a proposed new flow. Its domain excludes the singular zero-gradient
state and has its own derivative lower bounds; it does not contradict
LINEARIZATION_BARRIER.

For the literal boundary speed c0/|A|^2 a conditional factorized evolution
can be written

    gamma_t=c0 gamma''/|gamma'|^2,
    g_t=c0 Delta g/(|gamma'(g)|^2 |grad g|^2).

Whenever these factors are smooth and noncritical, the chain rule gives
u=gamma(t,g(t,x)) solving the scalar flow and retaining rank-one image.
This exhibits the parameterization cancellation. It supplies no solution
through critical points, global periodic real-valued submersion, or QC
dissipation theorem. Andrews--Carapetis pays its DIFFERENT invertible
torus-map regime by an actual tensor maximum principle.

## 4. First positive attempt: inverse-heat conjugacy

Let F be any known componentwise-heat-dissipated energy in2x2, with its
actual global certificate/monotonicity already supplied. Fix a constant
matrix C and an invertible mean matrix M with sym M>=mu I>0. On the
source torus let

    v0(y)=M y+phi(y),
    sum_(k!=0) |k| |phi_hat(k)| <B<mu.

All norms of vector Fourier coefficients are Euclidean. Smooth phi, or
an explicitly acquired Wiener tail, pays this condition; merely knowing
pointwise values does not. Set v(t)=M y+exp(t Delta)phi. Its derivative
perturbation has operator norm<=B for all t. Thus v is globally strongly
monotone and proper on its universal cover, hence a global diffeomorphism
between the two flat tori, with singular values in
[mu-B,||M||+B]. It converges smoothly to an affine map.

Its inverse u=v^-1 is an actual globally defined nonlinear evolution:

    u_t=sum_(i,j) [A^-1 A^-T]_(ij) u_ij, A=Du.                    (4)

The inverse-function second-derivative identity proves (4). It is
uniformly parabolic on this acquired invariant derivative domain; its
coefficient becomes singular at A=0, outside that domain. No general
preservation of diffeomorphisms by ordinary heat was assumed: the paid
Wiener/strong-monotonicity condition is what ensures it here.

Define the rationally transformed energy, when F is polynomial,

    W_C(A)=det A F(A^-1-C), A in GL+(2).                           (5)

Change of variables gives the EXACT normalized energy identity

    mean_target W_C(Du(t))=(det M)^-1 mean_source F(Dv(t)-C).        (6)

It therefore decreases under (4) and tends to W_C(M^-1). This is a usable
nonlinear flow export for a supplied heat proof, with an explicit input
derivative regime and no new angular-primitive selection problem.

## 5. The export genuinely contains non-polyconvex energies

As a symbolic family use the already-proved
[Bruno--Pasqualotto energy](https://arxiv.org/html/2608.06367)

    F_gamma(B)=|B|^4-2gamma |B|^2 det B,
    1<gamma<=2/sqrt(3).

Choose t>0 with t^2<(gamma-1)/(gamma+1), s>max(1,t), and D=diag(1,-1).
The four source deviations I,-I,tD,-tD have weights

    lambda_+=lambda_-=t^2/[2(1+t^2)],
    lambda_D+=lambda_D-=1/[2(1+t^2)].

Their mean and mean determinant both vanish, while their mean energy is

    4t^2[(1-gamma)+(1+gamma)t^2]/(1+t^2)<0.                       (7)

Translate by sI, producing SPD matrices B_i=sI+deviation_i with mean
B0=sI and mean det B_i=det B0. Invert and reweight:

    A_i=B_i^-1, mu_i=lambda_i det B_i/det B0.

Then sum mu_i A_i=B0^-1 and sum mu_i det A_i=det B0^-1, since cofactor
is linear in2x2. For W_(gamma,s)(A)=det A F_gamma(A^-1-sI), its mean
energy at these same-minor atoms is (7)/det B0<0=W_(gamma,s)(B0^-1).
Thus the WHOLE parameterized family is non-polyconvex even on SPD
gradients, and is covered by the nonlinear export (6) on its admitted
map class. These atoms are a polyconvexity witness, not a realizable
gradient law or a non-QC assertion.

For orientation and exact arithmetic, gamma=17/16,t=1/8,s=2 yields target
atoms I/3,I,diag(8/17,8/15),diag(8/15,8/17), with weights
9/520,1/520,255/520,255/520. The minor means are I/2 and1/4, and the
energy mean is -31/66560. This is an analytic evaluation of (7), not a
new numerical source/flow run or a practical test case.

## 6. Strong ordinary collision: this is NOT a new QC capability

The map W->det A W(A^-1) is the classical SHIELD transform. Invariance
of rank-one convexity, SMOOTH-TEST quasiconvexity and polyconvexity is already a known
theorem; see Voss--Martin--Ghiba--Neff,
[JNS2022, discussion of Shield](https://link.springer.com/article/10.1007/s00332-022-09827-4),
whose Lemma6.2 explicitly states C_c-infinity quasiconvexity and credits
Ball1977 Theorem2.6. Here all transformed QC claims use that exact scope:
smooth compact perturbations with everywhere positive determinant, whose
proper universal-cover maps are global diffeomorphisms. No extension to
arbitrary Sobolev maps/homeomorphisms is claimed. Translating F and
applying this ordinary transform already proves that smooth-test QC of
(5) on its proper GL+ variation domain. Formula(6) does not discover a stronger static energy
class than that equally informed ordinary construction.

Accordingly the inverse-flow attempt is retained as an honest positive
coordinate/convergence compiler and is RETIRED as a new QC opening. Its
purpose here is to demonstrate a real singular/restricted-domain escape,
not to disguise the source certificate as a newly acquired one. No
assertion is made that the resulting W lacks every constant-flow proof.

Likewise u_t=div DF(Du) automatically dissipates ANY differentiable F.
Its principal part vanishes at zero for a quartic, so the new barrier
does not forbid it. But global smooth convergence to the affine state,
absence of non-affine traps and all-base behavior remain UNSUPPLIED.
Energy descent or a ground-energy lower bound is not that missing theorem.

The meaningful narrowed research gate is now a degenerate/singular,
nonlocal or enlarged-state flow with BOTH a globally controlled domain
and a new dissipated-energy/convergence theorem. Existing geometric
diffeomorphism convergence alone does not supply monotonicity of the
desired non-PC energy; existing variational descent alone does not
supply convergence. Neither missing operation is silently imported.
