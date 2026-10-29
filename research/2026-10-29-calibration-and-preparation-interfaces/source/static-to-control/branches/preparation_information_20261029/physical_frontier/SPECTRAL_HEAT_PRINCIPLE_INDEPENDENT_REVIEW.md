# Independent review: heat norm, force norm and native explanations

29 October 2026. Reviewed the root's proposed periodic shear generalization
as supplied in its task message, together with the explicit stationary
source established in NATIVE_EQUILIBRIUM_TOPOLOGY_OBSTRUCTION.md. This is
an ordinary mathematical review of that proposal, not a claim to have
read a later root manuscript version.

## 1. Verdict and conventions

The proposed Fourier identity, negative-half-order norm interpretation,
exact band-limit constant, regularity interpolation and optimal exponent
all check under the stated stationary mechanical interface. The two-sided
kernel bounds also hold with c=exp(-3/2) and upper constant 5.

Use theta for temperature and T for observation duration to avoid a
collision between those two resources. Positions have period 2pi, masses
are one and damping rate is gamma. For real bounded periodic f,

    fhat_m=(1/(2pi)) integral_0^{2pi} f(x) exp(-imx) dx,
    ||f||²=(1/(2pi)) integral |f|² = sum_m |fhat_m|².

The source is F(q)=(0,f(q_1)), with q_1,p_1 an autonomous equilibrium
kinetic Langevin process and q_2,p_2 driven transversely. No odd external
field, hidden parity relabeling or changed bath is used. The zero Fourier
mode is allowed and corresponds to winding work on the torus.

## 2. Independent derivation of the exact identity

Uniform initial phase gives

    C_f(t)=E[f(q_1(t))f(q_1(0))]
     =sum_m |fhat_m|² exp{-m²theta/gamma²
                                  [gamma t-1+exp(-gamma t)]}. (1)

This is the uncentered correlation. Removing the mean would incorrectly
delete the physical work done by a constant transverse force. The factor
of one half for a sine is already accounted for by its two Fourier
coefficients; there is no extra factor in (1).

The transverse stationary momentum is an independent thermal OU
component plus

    R(t)=integral_0^infinity exp(-gamma s) f(q_1(t-s)) ds.

Fubini and stationary correlation give

    E R²=(1/gamma) integral_0^infinity exp(-gamma t) C_f(t) dt.

Hence thermal entropy production is

    sigma[f]=(1/theta) sum_m |fhat_m|² I_m,
    I_m=integral_0^infinity exp(-gamma t)
             exp{-m²theta/gamma²[gamma t-1+exp(-gamma t)]}dt. (2)

Bounded f makes the force convolution bounded and justifies these
interchanges. The Fourier series can be handled first for trigonometric
polynomials and then by L2 convergence: stationarity controls each
filtered mean-square error, and the positive coefficient sum is bounded
by ||f||²/gamma. This passage does not require pointwise Fourier-series
convergence.

For m=0, I_0=1/gamma. For |m| increasing, I_m decreases strictly.
With a=|m|sqrt(theta)/gamma and u=gamma t,

    I_m=J(a)/gamma,
    J(a)=integral_0^infinity exp[-u-a²h(u)]du,
    h(u)=u-1+exp(-u).                                    (3)

As a tends to infinity, rescaling u=z/a gives

    J(a)~sqrt(pi/2)/a,
    I_m~sqrt(pi/2)/[|m|sqrt(theta)].                      (4)

The Gaussian domination on u<=1 and exponential tail on u>=1 used in the
single-mode proof justify the limit. The next formal expansion agrees
with the earlier control: I_m=sqrt(pi/2)/(|m|sqrt(theta))
-2gamma/(3m²theta)+O(|m|^-3). Only the leading asymptotic is needed.

## 3. Explicit global kernel bounds

Let c=exp(-3/2). Then for all a>=0,

    c/(1+a) <= J(a) <= 5/(1+a).                         (5)

Lower bound: restrict u to [0,1/(1+a)]. Since h(u)<=u²/2,
u+a²h(u)<=1+1/2, so the integrand is at least c over an
interval of length 1/(1+a).

Upper bound: J(a)<=1 always. Thus a<=2 is covered by
J(a)<=3/(1+a). For a>=2, use h(u)>=u²/(2e) on [0,1]
and h(u)>=u/e on [1,infinity), obtaining

    J(a)<=sqrt(pi e/2)/a
                 +exp[-1-a²/e]/[1+a²/e].

The tail is at most 1/a²<=1/(2a). Also sqrt(pi e/2)<5/2.
Therefore J(a)<3/a<5/(1+a) when a>=2. The constants are
intentionally nonoptimal but valid uniformly through the crossover.

Restoring physical units,

    c/[gamma+|m|sqrt(theta)] <= I_m
                         <=5/[gamma+|m|sqrt(theta)].     (6)

## 4. Exact native equilibrium explanation cost

Let G=-grad U be any bounded periodic conservative position-only force
with the same bath and torus. The stationary source position marginal
is uniform, so periodic gradient orthogonality gives

    uniform_average |F-G|²=||f||²+uniform_average |G|².

The same-bath stationary path KL rate is consequently minimized exactly
by the free equilibrium G=0, and its optimum is

    K_native[f]=||f||²/(4gamma theta).                    (7)

This is an asymptotic path-likelihood rate. It is not a second physical
entropy-production formula. Finite-window KL also has a nonnegative
initial preparation term, so one cannot identify its exact optimum with
T times (7) without addressing that term. The earlier bounded-force TV
argument supplies a separate finite-window consequence.

The source force need not be identified to state the existence theorem.
If f is actually supplied, direct Fourier evaluation and ordinary
Girsanov regression already exploit the same information; no computational
or acquisition advantage is obtained merely by naming the two norms.

## 5. Sharp regularity interpolation and bandwidth bounds

Write w_m=gamma+|m|sqrt(theta). For s>0 suppose

    B_s:=sum_m w_m^(2s)|fhat_m|² <= R_s².

By (6), sum |fhat_m|²/w_m <= theta sigma/c. With
r=2s/(2s+1), Holder applied to

    |fhat_m|²=(|fhat_m|²/w_m)^r
                        (w_m^(2s)|fhat_m|²)^(1-r)

gives

    K_native[f] <= [1/(4gamma theta)]
           (theta sigma[f]/c)^(2s/(2s+1))
                            R_s^(2/(2s+1)).              (8)

The exponents and units are consistent. R_s is the square root of the
weighted squared budget; replacing it by B_s would change the displayed
power. At s=0 the statement reduces to an amplitude-energy ceiling and
provides no stability as sigma vanishes.

For f_n(x)=n^-s sin(nx), B_s stays bounded, whereas

    K_native[f_n] asymptotic to a positive constant times n^-2s,
    sigma[f_n] asymptotic to a positive constant times n^-(2s+1).

Thus no larger power of sigma can replace 2s/(2s+1) with a uniform
constant on that bounded-budget class. This shows sharpness of the
exponent, not of the numerical constant c.

If f is band limited to |m|<=N, monotonicity of I_m gives the exact
optimal inequality

    K_native[f] <= sigma[f]/(4gamma I_N).                 (9)

A real sine or cosine at N attains the rate ratio. The zero-mode case
N=0 gives K_native=sigma/4. Bandwidth or Sobolev budgets are physical
source restrictions or acquired force information; a coarse fitted path
does not by itself certify either one.

## 6. Reach and the known machinery

Equation (2) is a heat-weighted Green--Kubo calculation for a triangular
mechanical source. The high-frequency weighting makes sigma equivalent
to a squared H^{-1/2}-type norm, while native force-likelihood cost is an
L2 norm. This is exact for the declared shear family; it is not a universal
Sobolev law for arbitrary coupled underdamped systems.

The integrated-OU Fourier decorrelation kernel is already in Boi, Mazzino
and Muratore-Ginanneschi, *Eddy diffusivities of inertial particles in
random Gaussian flows*, arXiv:1611.02747, equations (8)--(9):
https://arxiv.org/pdf/1611.02747.
Their eddy-diffusivity observable uses that kernel with the carrier-flow
correlation. The present heat functional adds the transverse relaxation
weight exp(-gamma t). In fact an exponentially correlated carrier-flow
choice in their formula reproduces this weighted integral after parameter
conversion. The kernel and the general correlation-filtering mechanism
must not be presented as newly discovered here.

Hao Ge, *Time reversibility and nonequilibrium thermodynamics of
second-order stochastic processes*, arXiv:1209.3081, Sections III--V:
https://arxiv.org/pdf/1209.3081.
Its explicit examples and equations (13)--(15) already distinguish
time-reversible dynamics from the Maxwell reservoir condition, and it
identifies the simpler position-force setting where the relevant entropy
notions coincide. The abstract-versus-native distinction is therefore
not itself a new conceptual observation.

The particular additional statement under development is quantitative:
an exact mismatch between physical heat and best same-mechanical-class
path-likelihood cost, its native full-path obstruction, and the precise
spectral source information that repairs stability. Holder interpolation
and Fourier cutoffs are conventional mathematics. A bounded search did
not locate this combined theorem, but it cannot establish priority.

## 7. A general operator form suggested by the calculation

The same mechanism extends beyond a free horizontal driver, without
claiming a new correlation formula. Let X be any stationary equilibrium
underdamped driver, let f depend only on its positions, and add a transverse
cyclic position with momentum driven by f(X) and thermalized at rate gamma.
The driver remains autonomous. If its generator is L and its equilibrium
position law is nu, then

    sigma[f]=(1/theta) <f,(gamma-L)^-1 f>_rho.             (10)

The resolvent is bounded on L2 and the correlation representation proves
the identity. On reversal-even functions its compression is symmetric:
L*=Theta L Theta and Theta f=f imply this directly. It is positive since,
for u=(gamma-L)^-1 f,

    <f,u>=gamma||u||²-<Lu,u> >= gamma||u||².

For position-only forcing define the compressed positive operator

    H_gamma=P_position (gamma-L)^-1 P_position.

The best same-bath conservative explanation differs from the equilibrium
driver only by the added force. Integration in the cyclic transverse
coordinate again makes that force orthogonal to every periodic gradient,
even when nu is nonuniform. Hence its optimum likelihood rate is still
||f||²_nu/(4gamma theta).

Consequently a linear uniform comparison between native explanation cost
and heat on an allowed force subspace holds exactly when the compressed
operator has a positive spectral lower bound on that subspace. The free
driver diagonalizes H_gamma by Fourier modes and yields the explicit
negative-half-order law above. This operator observation does not acquire
the driver, its resolvent or a spectral lower bound. It is offered as a
further structural formulation for root to develop if useful.

## 8. Review receipt

Reviewed ordinary derivations: stationary correlation, exact entropy
normalization including the zero mode, kernel bounds, asymptotic scaling,
native KL-rate optimum, Holder powers, exact band-limit coefficient and
the optional operator extension. No new numerical experiment was needed.
Primary texts read directly: Boi et al. equations (8)--(9), and Ge's
reversibility/Maxwell distinction and governing entropy section.
Web source refs: turn650view0, turn651view0, turn650view1, turn651view1.
Searches also covered entropy production with shear/Fourier and negative
Sobolev terminology; absence of a retrieved collision is not priority.
