# Matched energy trial: positive scalar receiving plan and derivation

Status: NEW author construction, not an accepted numerical receiver. The
reviewed retained-clock package remains unchanged. Floating diagnostics test
the conservative formulas below, not their finite-bit implementation.

## 1. Actual input and task, no different physical fixture

Retain the original full reversible Langevin model F(y,z)=v(y)U(z),
v=1+kappa(1-y^2)^2, basins y<=-1/2 and y>=1/2, and once-only exact FULL Gibbs|A.
The refined parser will reuse the actual positive even quartic/isotropic or
diagonal constant-SPD model grammar. Such quartics consist precisely of pure
terms d_i z_i^4 and pair terms g_ij z_i^2 z_j^2. All d_i>0 and g_ij>=0.
No energy-coordinate Markov closure is assumed. The same raw 513D path-coupling
20 and unit-mobility program is the intended first consumer, not a new dimension.

The actual diagonal mobility entries mu_i and coefficients are now needed for
accuracy, not only their lower coercivity/mobility bounds. Receive exactly

 c_j=12 mu_j d_j+2 sum_{i:ij edge}mu_i g_ij,
 H=sum_j c_j^2, dmin=min_i d_i, alpha=m/4.

The full raw program is read and checked; constructing all c_j, H, their exact
rational bit growth and roots is paid. For the existing path fixture the c_j
are 52 at two endpoints and 92 at 510 interior vertices, so H=4322048.
Arbitrarily large couplings/mobility can make this refined certificate fail.
The earlier broad angular-uniform theorem remains valid separately.

## 2. Complete primal cost, geometric coarea only

Let v*=1+kappa, phi(y)=v*-v(y)=kappa(2y^2-y^4), b=1/2,
dphi=phi(b)=7kappa/16, and t=beta v* u with u=U(z).
For y>=0 define

 f(t,y)=exp[-t phi(y)/v*], J(t)=int_0^b f(t,y)dy,
 A0=int_0^y f, Aphi=int_0^y phi f,
 B0=int_y^b f, Bphi=int_y^b phi f,
 D(t,y)=A0 Bphi-Aphi B0.

D is the positive double integral of (phi(s)-phi(r))f(t,r)f(t,s),
0<=r<=y<=s<=b. Consequently D>=0 and D decreases with t. The frozen-fiber
trial is h_u(y)=B0/(2J), extended by symmetry and by constant basin values.
Direct differentiation gives

 |partial_u h_u(y)|=beta D(t,y)/(2J(t)^2).               (1)

The signed trial psi=2h_u-1 is odd, |psi|<=1 and equals the basin signs. The
coarea/divergence identity supplied separately by the root gives

 E_shell[grad U^T M grad U|U=u]
 <=sqrt(H)u^(3/2)/[(alpha+1/2)sqrt(dmin)].

This is a geometric shell average, not an acquired angular mixing law. Let
G_alpha be Gamma(alpha,rate1), an exactly known scalar reference density.
The complete Dirichlet cost C=E(h_u,h_u) obeys

 beta v*^alpha C <= P := P_f+P_z,
 P_f=E_G[1/(2J(t))],
 P_z=K E_G[t^(3/2) int_-b^b D(t,|y|)^2/(4J(t)^4)
                             *exp(t phi(y)/v*)dy],
 K=sqrt(beta H/(dmin v*^3))/(alpha+1/2).                (2)

Every beta and v* factor is retained. The transverse term is not discarded.
Unknown angular partition factors cancel by homogeneity/coarea, not sampling.

## 3. Rigorous finite positive-grid upper for P_f and P_z

Use uniform rational t_i=L+i h_t, i=0,...,N_t, T=t_N, and y_j=j h_y on[0,b].
All formulas here will be evaluated outward. Write a=t/v*. On a y cell[l,r],
phi and phi' increase and phi'' decreases but remains positive. Since

 f''=[a^2(phi')^2-a phi'']f,
 (phi f)''=[phi''-2a(phi')^2+phi(a^2(phi')^2-a phi'')]f,

valid absolute second-derivative ceilings are

 F2=f(t,l)[a^2 phi'(r)^2+a phi''(l)],
 G2=f(t,l)[phi''(l)+2a phi'(r)^2
                 +phi(r)(a^2 phi'(r)^2+a phi''(l))].

The cell trapezoid +/- h_y^3 F2/12 encloses int f, and the analogous G2
encloses int phi f. Clamp lower endpoints at zero. Independently sum these
positive cell intervals from the left AND from the right. Do not obtain a
tiny right tail by subtracting a prefix from a rounded total.

For t in[t_i,t_(i+1)] and y in[y_j,y_(j+1)], monotonicity of positive primitive
integrals and of D in t gives the cell upper

 D <= D_ij := max(0,
 A0_hi(t_i,y_(j+1))*Bphi_hi(t_i,y_j)
 -Aphi_lo(t_i,y_j)*B0_lo(t_i,y_(j+1))).                 (3)

The entire right side uses left/right integrals at t_i, not a sign-indefinite
numerical derivative. J(t)>=J_lo(t_(i+1)), and
exp(t phi(y)/v*)<=1/f_lo(t_(i+1),y_(j+1)). A positive lower denominator must
actually be resolved; otherwise return UNKNOWN.

Let W_i be an outward interval for exact Gamma probability of[t_i,t_(i+1)].
Then safe finite-window bounds are

 P_f(window) <= sum_i W_i_hi/[2 J_lo(t_(i+1))],
 P_z(window) <= K_hi sum_i W_i_hi*t_(i+1)^(3/2)
    *2h_y sum_j D_ij^2/[4J_lo(t_(i+1))^4
                              f_lo(t_(i+1),y_(j+1))].  (4)

Integer alpha permits exact finite-sum Gamma survival evaluation:
S_alpha(t)=exp(-t) sum_{k=0}^{alpha-1}t^k/k!,
W_i=S_alpha(t_i)-S_alpha(t_(i+1)). Outward subtraction and nonnegativity are
mandatory. No numerical quadrature error is assigned to a floating Gamma CDF.

## 4. Cheap optional LOWER J: positive Taylor, not an asymptotic remainder

Put a0=2kappa/v*, gamma=v*/(4kappa), X=b^2 a0 t. The exact transform is

 2J(t)=(a0 t)^(-1/2) int_|x|<=sqrt(X)
                   exp(-x^2) exp(gamma x^4/t) dx.

Because the exponential's Taylor coefficients are nonnegative, for ANY finite
K0>=0 the integral is at least the sum of its first K0+1 terms. Each finite
Gaussian moment is Gamma(2k+1/2)-Gamma(2k+1/2,X). The incomplete upper tail has
the elementary ceiling

 Gamma(s,X) <= exp(-X) X^(s-1)/[1-max(s-1,0)/X]         (5)

when the denominator is positive. For s<=1 use denominator1, not the stronger
but generally unjustified 1-(s-1)/X. For s>1, (5) follows by bounding the
logarithmic decay derivative below by 1-(s-1)/X on[X,infinity]. If unavailable,
the full moment is itself a valid tail upper bound, producing a zero lower
moment. Positive-part lower moments are therefore always safe.

Take the maximum of this analytic J lower and the trapezoid J lower. Full
half-integer Gamma values are rational multiples of sqrt(pi); a finite ordinary
Machin/alternating-series pi enclosure and outward roots will be paid.
**No upper Taylor remainder is needed** for this use: only a lower J is used to
upper-bound (2). In particular, a short positive Taylor polynomial is not
treated as an accurate asymptotic expansion without a direction of inequality.

## 5. Full scalar tails are separate, explicit and paid

For all t>=0 choose |y|<=b/sqrt(1+t). There
t phi(y)/v*<=kappa/(2v*)<1/2. Since exp(-1/2)>1/2,

 2J(t)>=1/[2sqrt(1+t)], hence 1/(2J(t))<=2(1+t).

Thus P_f outside[L,T] is at most twice the corresponding Gamma mass plus
twice its first truncated moment. Integer-Gamma shapes alpha and alpha+1
evaluate those quantities exactly with outward arithmetic.

The simple covariance bound |partial_u h|<=beta*dphi/4 gives a tail ceiling
for P_z. Put r=1-dphi/v*=v(b)/v*>0. Since t^(3/2)<=(t+t^2)/2,

 P_z(tails) <= K*dphi^2/32 *sum_{k=1,2}
   (alpha)_k r^(-alpha-k)
   [ P(Gamma(alpha+k,1)<rL)+P(Gamma(alpha+k,1)>rT) ].    (6)

This includes the full longitudinal slab (length1). No angular tail law or
transverse partition estimate is supplied free. All lower-tail cancellation,
upper-tail truncation and large r^(-alpha-k) prefactors are paid together.
The diagnostic choice L=32,T=400 at alpha128,kappa1 has tiny received-formula
tail prices, but those FLOAT displays are not an exact tail certificate.

## 6. Shifted dual and actual clock reference

Choose a_bar=v*(1-1/(2alpha)) only after checking a_bar in[v(b),v*]. The separate
shifted-well theorem constructs an actual current, with

 R_a=int_S[a_bar^2/(2a_bar-v(y))]^alpha dy,
 B_f<=beta[M^2 R_a+2E_rest].

E_rest is the independently earned old well ceiling, not omitted because it is
small. The separate odd-slab current gives B_r<=beta/4(1+kappa/8)^(-alpha),
for r=psi-(1_A-1_B). Then Q_psi<=(sqrt(B_f)+sqrt(B_r))^2.

Let P_hi be the complete outward bound from (4)--(6), including raw K.
Cu=P_hi/(beta v*^alpha) is a rational upper on the full trial energy. Acquire
Ml<=M<=Mh. One simple declared reference flip rate is lambda_star=Cu/Ml.
N=int psi^2 w>=2M>=2Ml and E(psi)<=4Cu give, for k=2lambda_star,

 E_spectral[K_global/k]<=1,
 E_spectral[k/K_global]<=Cu Bpsi_hi/Ml^2 =1+epsilon.    (7)

The actual capacity is at most Cu, so its stationary full-transition intensity
is at most2Cu/Ztot<=lambda_star. Thus the SAME received sampled-path and
hysteretic-count mechanism applies to this new earned trial with no extra
midpoint-rate discrepancy. The mass/current overestimate is instead explicitly
paid in epsilon. All well/source quantities must be evaluated using actual
upper/lower masses in the displayed safe directions.

For conditioning, use R_a/v*^alpha and Bpsi/(beta Ml^2 v*^alpha). The decisive
primal/dual product is dimensionless: the exponentially large reference R and
v*^alpha cancel, rather than being estimated by rare crossing simulation.
The physical rate still includes v*^-alpha and Ml, which must be output exactly
within declared bit/digit budgets. No physical time or initialization is erased.

## 7. Execution plan and limits

Uniform t-grid f(t_i,y_j) values can be advanced by multiplication with the
fixed positive ratio exp[-h_t phi(y_j)/v*]. Only the seed and ratio require
exponentials for each y point; outward interval multiplication accumulates its
actual rounding width. An underresolved positive lower value is UNKNOWN, not
replaced by a floating seed. Gamma finite sums are separate and fully paid.
Two consecutive rows and positive prefix/suffix arrays suffice: no million-
element hidden-state or angular basis is acquired.

The expensive operations remain O(N_t N_y+alpha N_t), with finite bit length,
roots, elementary exponential tails and explicit raw input costs. This is an
ordinary deterministic interval construction, not a new quadrature oracle.
The initial FLOAT conservative-formula diagnostic with analytic J, 1024x256
gives slab excess about0.003039 and ideal-rate ten-record bound about0.09174;
2048x256 gives about0.002666 and0.08570. Well/mass/rate/input/finite-bit prices
must still fit the actual 10% request. Failed grids and work exhaustion must
be preserved. The current accepted 15%/45% service remains the fallback.

This U-dependent trial does not inherit arbitrary scalar-trial-neutral
processing. Baseline B=0 is the present target. A drift preserving U could be
an independently earned later subclass, not an automatic parser promotion.
