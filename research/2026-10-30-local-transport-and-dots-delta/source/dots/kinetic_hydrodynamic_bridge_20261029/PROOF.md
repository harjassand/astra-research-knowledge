# Nonlinear hydrodynamic resummation before spatial kinetic branching

Private constructive investigation, 29 October 2026. Status: exact toy-model
algebra and exact reference-law construction; floating diagnostics; the full
Boltzmann residual/cost bridge is OPEN. No novelty or physical capability claim.

## Selected opening and full-success contract

The selected opening after rejecting boundary thermodynamic tomography is a
query-directed kinetic simulator which does not reconstruct the entire prior
space-time field and does not pay exponentially for elapsed collision time.
Full success for spatial nonlinear Boltzmann dynamics, with conserved fluid
modes and usable finite accuracy, would create a qualitatively different way
to predict transport and design nonequilibrium matter. It is not achieved here.

Input would be an actual collision model and source evaluator/sampler, spatial
geometry, boundary conditions and quantitative source class. Output would be a
positive prescribed observation/sample or certified observable at arbitrary
finite time; all source reads, primitives, precision and preprocessing must be
charged. A supplied evolving Maxwellian, local moments or exact fluid trajectory
would already supply the hard part and is forbidden as an uncharged premise.

The early construction below selects a precise missing operation: resum the
nonlinear conserved dynamics before attempting subcritical kinetic genealogies.
Merely improving a linear spectral gap is insufficient. A conventional exact
Burgers receiver demonstrates that a nonlinear reference need not be a free
oracle; transferring it to the kinetic equation remains genuinely unfinished.

## 1. Actual Astra machinery and the spatial obstruction

At pinned revision 95c99ce592a48d4505dd4bfcc0925d7ebad0efdd, N1286 uses an actual
nonradial hard-sphere collision model, weighted source deviation at most 1e-4,
and a controlled absolute row <=199/200 times collision frequency. Its bounded
branching query has expected nodes <=400 uniformly in elapsed time. The exact
source was read in full, including native sampling and the large Bernoulli-factory
cost. Its positive continuous output pays explicit clipping bias. Its 128-output
timing lost to an equally informed ordinary lineage method. Its new independent
whole review and finite-bit/physical qualifications remain unacquired.

The control subtracts FIVE MOMENTS that remain zero during HOMOGENEOUS dynamics.
In a spatial equation, global zero moments do not make each position's moments
zero. For example, f0(x,v)=M(v)[1+epsilon cos(kx)] has zero global mass error but
nonzero local density. Its initial collision term is exactly zero. Applying the
homogeneous local zero-moment control generally adds a false O(epsilon) collision
term. Tracking x in the existing tree does not fix this error.

Subtracting global invariants instead cannot directly cancel the collision's
spatial delta kernel. Spatial LVDSMC and micro-macro methods already track local
fluid variables; they are stronger incumbents than generic unstable particle
simulation. Query-directed nonlinear branching paths also predate this work.

## 2. Exact three-velocity test model

Take velocities v=(-1,0,1), with densities f=(f_-,f_0,f_+) and periodic space:

    partial_t f + V partial_x f = q (f_0^2-f_- f_+),
    q=(1,-2,1), V=diag(-1,0,1).                         (1)

It has local mass and momentum conservation, positivity, and a detailed-balance
collision entropy. It is a TEST COLLISION MODEL, not literal monatomic 3D hard
spheres and not a justified replacement of their five-invariant physics.
The uniform equilibrium is f*=(1,1,1)/3.

Use orthonormal basis

    e_r=(1,1,1)/sqrt(3),
    e_j=(-1,0,1)/sqrt(2),
    e_z=(1,-2,1)/sqrt(6),
    f-f*=r e_r+j e_j+z e_z.

Set c=sqrt(2/3), b=1/sqrt(3). Then

    r_t = -c j_x,
    j_t = -c r_x-b z_x,
    z_t = -b j_x-2z + sqrt(6)[j^2/2-sqrt(2)r z+z^2/2]. (2)

Every quadratic forcing is in the kinetic z direction. Thus no conservation
condition was discarded merely to manufacture the obstruction.

The exact Fourier linear matrix is

    A(k) = [ 0      -i c k       0 ]
           [ -i c k    0      -i b k ]
           [ 0      -i b k      -2 ].                  (3)

Its characteristic polynomial is

    lambda^3+2lambda^2+k^2 lambda+(4/3)k^2.             (4)

The acoustic eigenvalues satisfy

    lambda_+/-(k)=+/- i c k-k^2/12+O(k^3),
    lambda_fast(k)=-2+k^2/6+O(k^4).                    (5)

The linear equilibrium gap is therefore O(k^2), not a fixed collision gap.

## 3. Conservation helps, but does not remove nonlinear resonance

For kinetic forcing e_z=(0,0,1), the exact resolvent is

 (lambda I-A(k))^{-1}e_z =
   [ -sqrt(2) k^2,
     -sqrt(3) i k lambda,
     2k^2+3lambda^2 ]
   /[3lambda^3+6lambda^2+3k^2 lambda+4k^2].             (6)

The DC response is bounded: (-A)^(-1)e_z=(-sqrt(2)/4,0,1/2).
It would nevertheless be wrong to infer a bounded absolute time-response norm.
The acoustic projection of e_z is O(k), while its decay time is O(k^-2).
Expansion of the two acoustic projectors gives

    integral_0^infinity ||exp(t A(k))e_z||_2 dt
                  = (2sqrt(3)+o(1))/|k|.              (7)

Reason: the fast term integrates to O(1). The two asymptotically orthogonal
acoustic components have combined norm |k|/(2sqrt(3)) times
exp(-k^2 t/12), up to a relative o(1) on scaled positive-time intervals.
Analytic eigenvalue/projector perturbation and an exponential tail envelope
justify the limit after setting s=k^2 t. Their integral is 2sqrt(3)/|k|.

The finite quadrature probe approaches this limit, but its k=.01 run emits a
roundoff warning and its reported error is retained. The asymptotic derivation,
not that quadrature, is the argument for (7).

More decisively, the actual quadratic term resonates. Let r(k) be the right-going
acoustic eigenvector normalized by its r coordinate=1, with eigenvalue
lambda(k)=-i c k-k^2/12+O(k^3). Then

    r(k)=(1,1,-i k/(2sqrt(3)))+O(k^2).

For the complex one-mode initial datum e^{ikx}r(k), the second-order coefficient
at spatial mode 2k is exactly

    h_2(t) = [exp(2lambda(k)t)I-exp(A(2k)t)]
             [2lambda(k)I-A(2k)]^{-1} e_z B(r(k)),
    B(r)=sqrt(6)[j^2/2-sqrt(2)r z+z^2/2].              (8)

At t_k=6 log(2)/k^2,

    ||h_2(t_k)||_2 = (3/4+o(1))/|k|.                  (9)

For verification of the constant: B(r)=sqrt(6)/2+O(k);
the resonant projector at 2k sends e_z to
(-i k/(2sqrt(3)))(1,1,0)+O(k^2). The difference in real exponents is k^2/6,
and the two scaled decays at t_k are 1/2 and 1/4. Thus the norm is
(|k|/2)*(6/k^2)*(1/4)=3/(4|k|).

Real sinusoidal sources contain the conjugate mode and the corresponding
Fourier amplitude factor; the same inverse-k scaling persists. This is a
coefficient of the actual nonlinear equation, not solely a loose operator norm.
An absolute perturbative genealogy around linear kinetics therefore encounters
a delta/k barrier. This is NOT an impossibility theorem for all kinetic solvers.

The spectral execution gives k||h_2||=.750367 at k=.1, .7500398 at .03,
.75000424 at .01 and .750000336 at .003. No interval certification is claimed.

## 4. Constructive nonlinear resummation, not a fluid oracle

For a weak right-going mode, eliminate the fast kinetic variable to second order:

    z=(sqrt(6)/4)j^2-(b/2)j_x + higher terms.

Projecting onto u=(r+j)/2, with the left-going mode zero to first order, gives

    u_t+c u_x+gamma u u_x=nu u_xx,
    gamma=sqrt(2)/4, nu=1/12.                         (10)

This Burgers equation reproduces EXACTLY the coefficient 3/(4k) in (9).
It resums the resonant effect rather than declaring it small. Its use as an
approximation of the full kinetic equation is separate from its exact solution.

For u0(x)=delta cos(kx), put

    y=k(x-ct), T=nu k^2 t, A=gamma delta/(2nu k).

Cole-Hopf gives

    Z(y,T)=int_0^{2pi} K_T(theta-y) exp[-A sin theta] dtheta,
    u/k=-(2nu/gamma) partial_y log Z,                 (11)

where K_T is the circle heat kernel of variance 2T. This is established
Cole-Hopf machinery, not a newly discovered linearization.

Define a POSITIVE normalized law

    pi_(A,y,T)(dtheta) proportional
              K_T(theta-y) exp[-A sin theta]dtheta.    (12)

A von Mises proposal with concentration A and center -pi/2 has density
proportional to exp[-A sin theta]. Accept using K_T(theta-y)/K_T(0).
The circle heat kernel is maximal at zero, as follows directly from its positive
Fourier coefficients. For fixed T>0 its minimum is positive. Hence expected
proposals are <=K_T(0)/min K_T, independently of A, k and elapsed t when T is
fixed. An explicit positive minimum lower bound is
exp[-pi^2/(4T)]/sqrt(4pi T) from the nearest wrapped Gaussian term. A corresponding
upper bound is its positive Gaussian sum at zero. The constants can be large
when T is small; no uniform all-T claim is made.

The obvious observable delta E_pi[cos theta] suffers cancellation when A is
large. Instead differentiate the HEAT KERNEL:

    u/k=(2nu/gamma) E_pi[ K_T'(theta-y)/K_T(theta-y) ]. (13)

The ratio is a bounded known function on the compact circle at fixed T>0.
Therefore (13) has a bounded natural-scale estimator and concentration schedule
independent of delta/k. There is no hidden evolving fluid field, signed output
law or unnormalized clipping in this operation. A deterministic quadrature of
the same known integral is an equally informed, often stronger, alternative.

### Executed receiver

At T=log(2)/2, y=.25 and A=.1,1,10,100,1000,10000, 20,000 accepted samples were
compared with ordinary centered adaptive quadrature. At A=10000:

* score estimate u/k=1.23802727, standard error .00004810;
* ordinary adaptive quadrature=1.23810511;
* same accepted samples but naive initial-data observable=1.77784564,
  standard error .33349758.

219040 proposals were generated in batches for 20000 retained samples; unused
accepted values in the final batch are charged in this count. Total Python time
including the quadrature was about .13s in this run. The program uses numpy's
von Mises generator and truncated wrapped Gaussian sums, not certified exact
fair-bit arithmetic. Ideal exact rejection follows from (11)-(13); finite-bit
implementation and numerical bounds are not certified by floating agreement.
There is no speed claim over deterministic quadrature.

## 5. Full kinetic comparison: the missing bridge is visible

kinetic_compare.py uses exact LOCAL collision flow plus spectral transport in
Strang splitting. For physical mass rho=f_-+f0+f_+, momentum j=f_+-f_-, and
g=f_-+f_+, the collision ODE is

    g'=1.5 g^2-4rho g+2rho^2+.5j^2.

Set d=sqrt(4rho^2-3j^2), g_low=(4rho-d)/3, R=2d/3 and h=g-g_low. The exact step is

    h(t)=h(0)e^(-dt)/[1-h(0)(1-e^(-dt))/R].           (14)

This preserves rho and j and the physical local collision positivity domain.
Spectral interpolation itself is not globally positivity preserving, but all
executed component minima remained above .270; this is observed, not a general
positivity certificate. No continuum or time-discretization error bound follows
from the numerical result.

The initial source is on the exact RIGHT SIMPLE-WAVE curve of the equilibrium
Euler flux g_eq(rho,j)=(4rho-sqrt(4rho^2-3j^2))/3, rather than an arbitrary
mixture of both acoustic branches. Its scalar density parameter is
rho=1+sqrt(3)delta cos(kx). The momentum curve is acquired from the known
analytic ODE dj/drho=lambda_+(rho,j), integrated numerically in the comparator.
This construction and all initial fields are given to both methods.

At delta=.05 and k=.03, t=6 log 2/k^2≈4621, the Burgers replacement has about
4.15% relative L2 density error. Halving the kinetic time step .2→.1 leaves that
error almost unchanged. The maximum absolute discrepancy normalized by k is
about .0974. The 512-cell kinetic run costs about four seconds in this executor.

A subsequent theory-motivated attempt replaced the zero-momentum sound speed
by the exact equilibrium speed at the source's known conserved mean momentum.
It WORSENED the discrepancy to about 5.8%, not improved it. This failed variant
is retained separately. At k=.01 and t≈41589 its error is likewise about 5.8%,
with normalized maximum discrepancy .240. It is not silently adopted as a repair.

These are not tiny stochastic errors: they expose finite-amplitude characteristic
coupling, left-going corrections and long-time phase that the one-way quadratic
reference does not certify. Substituting (13) into the existing hard-sphere tree
would therefore simulate a different law unless these residuals are paid.

## 6. Where new theory would actually be needed

For a known reference F, write f=F+g. The exact equation is

    (partial_t+v.grad_x)g = L_F g+Q(g,g)-R_F,
    R_F=(partial_t+v.grad_x)F-Q(F,F).                  (15)

This identity does not solve the problem. A usable reference must be computable
at queried points with charged precision, preserve the actual conserved fields,
and supply a certificate on the causal inverse of the LINEARIZATION ABOUT THE
NONLINEAR REFERENCE. A generic linearized gap, an empirical close plot, or a
small local residual cannot be substituted for that inverse.

The desired next result is a subcritical bounded residual representation with a
source threshold not collapsing as the spatial wavelength grows. The exact
resonance shows why a reference that only carries linear fluid modes cannot have
that property. The positive Burgers receiver shows a constructive way nonlinear
modes can be supplied instead of assumed, but the toy kinetic comparison proves
that this is not yet enough. Generic a posteriori Gronwall estimates can grow
like exp(constant delta/k); an actual nonlinear stability mechanism is required.

For three-dimensional hard spheres, all five fluid invariants, transverse modes,
boundaries and shock/rare-event regimes must be handled. Nothing in this record
establishes that capability or an advantage over spatial LVDSMC, micro-macro
asymptotic-preserving solvers, deterministic kinetic solvers or existing nonlinear
backward Monte Carlo. The broad target remains consequential, but this branch is
an evidence-driven opening with a constructed component and a precise unclosed
bridge, not a civilization-changing result or a novelty-cleared theorem.
