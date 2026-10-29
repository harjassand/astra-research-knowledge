# A finite-rate local inertial Hodge thermostat

30 October 2026. Constructive conventional comparator within the existing Astra P1 role. This is a harmonic, signed-density model. It solves useful nonflat relaxation plus exact cycle-current exclusion with local runtime interactions and finite-rate independent bath calls. It does not solve the subsequently strengthened objective of preserving the ordinary heat path law and its density large deviations.

## 1. Complete supplied operation

On the N-site ring, let `(Bp)_i=p_(i-1)-p_i`, `L=BB^T`, and `H=1^perp`. The actual state is

    x in H, p in H, y in R^N.

The measured density is x. Its complete physical bond current is

    dJ=p dt,                 dx=B dJ.                         (1)

Between bath calls the apparatus follows the local deterministic equations

    dx=Bp dt,
    dp=-B^T(x+y) dt,
    dy=Bp dt.                                                (2)

At a call at vertex i, replace only `y_i` by a fresh centered Gaussian of variance theta. Neither x nor p jumps. The call intensity is an unknown frozen value `lambda_i(h)` satisfying known bounds

    0 < lambda_- <= lambda_i(h) <= lambda_+ < infinity.        (3)

The hidden parameter h can have an arbitrary nonmixing distribution, and may be correlated with a retained old record. Every conclusion below is uniform pointwise in h. The calls and their fresh draws have the stated conditional law after that record. A rate that depends arbitrarily on the evolving visible state is not included merely because it obeys (3).

This is an actual auxiliary-coordinate heat-bath operation, not an assertion that equilibrium weights supply its kinetic implementation. A call acts at one vertex. The continuous dynamics uses only incident coordinates. Its Hamiltonian matrix has norm at most `sqrt(2)||B||<=2sqrt(2)`, independently of N. There are at most `N lambda_+ t` expected calls in physical time t. No event-wide bit update, global broadcast, or white shared force is used. Gaussian draws and instantaneous local reset events are supplied ideal operations; a hard maximum force, minimum inter-event spacing, or finite duration for a reset is not proved by the finite intensity bound.

The physical current p is continuous, and is continuously differentiable between calls. A bath call changes its subsequent acceleration locally. Thus this version also avoids impulsive density-current kicks.

## 2. Exact current geometry and actual initialization

All supplied changes of p lie in `im B^T=H`. Hence the local initializer `p(0)=0` guarantees

    sum_i p_i(t)=0,          sum_i J_i(t)=0                    (4)

for every path and every actual time. One may also set `y(0)=0`; no prepared long-range Gaussian memory is required for (4) or the relaxation theorem below. An arbitrary nonflat deterministic x(0) in H is allowed.

More generally, on a connected bounded-degree graph use x in the zero-sum vertex space, p in `im B^T`, and y in the full vertex space, with the same equations and vertex resets. Then p and J have zero projection onto every graph cycle, pathwise. Equivalently,

    J(t)=B^dagger [x(t)-x(0)]                                (5)

where `B^dagger` maps zero-sum vertex vectors to their unique gradient edge current. Formula (5) counts all physical current from (1), not a gauge-redefined current. The proof and constants below are written for the ring; the same proof replaces the bounds 2 and 4 by the graph incidence and Laplacian norms.

A general initial cycle component of p persists and gives ballistic cycle current. It cannot be discarded by calling it hidden memory. Preparing the zero component is therefore an actual initialization condition, supplied here by local zeroing.

## 3. Stationary law and its symmetry

For every fixed h the exact stationary law is

    mu = N_H(0,theta I) x N_H(0,theta I) x N(0,theta I).       (6)

The deterministic field (2) is skew and conserves `|x|^2+|p|^2+|y|^2`. It preserves the indicated subspaces. Each individual coordinate heat bath preserves its Gaussian factor. This proves invariance without knowing any lambda_i.

With momentum reversal `(x,p,y)->(x,-p,y)`, the Hamiltonian part changes sign and the heat baths are self-adjoint and unchanged. Thus the system has the ordinary generalized detailed balance of an inertial thermostat. Its generator is not self-adjoint without momentum reversal. In particular, it does not fall under the earlier purely reversible bounded-counter relaxation obstruction.

The graph version has a nonlocal stationary covariance for gradient p. That covariance is a stationary result, not a free prepared initializer: starting p=y=0 is allowed, and the theorem below charges the time and calls that create the stationary correlations.

## 4. Uniform finite-system contraction despite unknown reciprocal rates

Couple two actual copies using the same call times and the same Gaussian refresh draw at each call. Their difference `(X,P,Y)` obeys (2) between calls, and at a call at i its coordinate Y_i is set to zero. No microscopic cloning is proposed: this is a mathematical coupling used to compare probability laws.

Put

    E=|X|^2+|P|^2+|Y|^2,
    F=X^T B P,                 G=Y^T B P,
    V=E+epsilon F-2epsilon G.                                (7)

Let `Lambda=diag(lambda_i)` and choose

    epsilon=min{1/6, lambda_-/(20+4lambda_+^2)},
    c_*=min{epsilon/2,lambda_-/8},
    ell_N=4sin^2(pi/N),        r_N=(2c_*/3)ell_N.             (8)

Then `E/2 <= V <= 3E/2`. Direct application of the coupled generator gives

    L E = -Y^T Lambda Y,
    L F = P^T B^TB P-X^T L X-X^T L Y,
    L G = P^T B^TB P-Y^T L X-Y^T L Y-Y^T Lambda BP.          (9)

Consequently

    L V = -Y^T Lambda Y-epsilon P^T B^TB P-epsilon X^T L X
          +epsilon X^T L Y+2epsilon Y^T L Y
          +2epsilon Y^T Lambda BP.                         (10)

The bounds

    X^T L Y <= (X^T L X+Y^T L Y)/2,
    2Y^T Lambda BP <= |BP|^2/2+2lambda_+^2 |Y|^2,
    ||L||<=4

and (8) imply

    L V <= -(lambda_-/2)|Y|^2
           -(epsilon/2)(P^T B^TB P+X^T L X)
        <= -c_* ell_N E <= -r_N V.                         (11)

Here both X and P have zero mean, while the full Y norm is directly damped. Thus

    E E(t) <= 3 exp(-r_N t) E E(0).                         (12)

The estimate is uniform over all unknown frozen h and needs no kinetic identification. In particular, for the actual full state S=(x,p,y),

    W_2^2(Law(S_t),mu)
       <=3 exp(-r_N t) W_2^2(Law(S_0),mu).                 (13)

The coupling also proves uniqueness of the stationary law in this fixed cycle sector and convergence from every finite-second-moment initializer. A nonflat density profile is not trapped in a conserved `x-Bz` sector.

For x(0)=x^0, p(0)=y(0)=0, an independent reference draw from (6) gives the explicit initial coupling cost

    E E(0)=|x^0|^2+theta(3N-2).                             (14)

When `|x^0|^2=O(N)`, fixed fractional mean-square equilibration takes O(N^2) physical time. Accuracy epsilon in the normalized state metric costs O(N^2 log(1/epsilon)) time and O(N^3 log(1/epsilon)) expected bath calls, with constants depending on the supplied rate bounds and theta. This is a resource statement, not a speedup assertion.

## 5. A genuine trajectory guarantee

The synchronous error energy E is constant between calls and decreases at every reset. It is therefore nonincreasing on each coupled path, even though V was needed for its expected contraction rate. At a burn-in time t,

    sup_(u>=0) |S_(t+u)-S^ref_(t+u)|^2 <= E(t).              (15)

Together with (12), this controls complete future state paths in a uniform Euclidean coupling metric. It does not assert total-variation closeness of the fine paths or of the clock log.

For currents measured from the common burn-in time, (5) further gives, on every finite or infinite future interval,

    sup_(u>=0) |[J_(t+u)-J_t]-[J^ref_(t+u)-J^ref_t]|^2
       <= (4/ell_N) E(t).                                  (16)

Thus a joint density/current trajectory objective can be supplied with an explicit metric and resource budget. No limit theorem is required for the exact harmonic-current exclusion (4).

If an old record chooses the initial law or the frozen h, apply (12)-(16) conditional on that record and average the actual initial coupling cost. The guarantee does not condition on future clock draws or a freshly exposed preparation log. A bad calibration event with fixed probability cannot silently support a rare-event claim.

## 6. Response port and strengthened-objective failure

A supplied fixed vertex potential phi can be applied locally by replacing the second equation of (2) with

    dp=-B^T(x-phi+y)dt.                                    (17)

The stationary density mean becomes `P_H phi`, with the same covariance and the same contraction proof after translation. This is an explicit nonuniform conservative response, uniform over the reciprocal bath rates. The force uses only endpoint potential differences.

An arbitrary nonconservative edge force is not automatically this port. If a cycle force f is simply added to dp, then its cycle component accelerates that component of p and destroys (4). Rejecting it by a Hodge projection would be an extra physical constraint operation, not an inference from this theorem. Thus the comparator does not establish suppressed circulating-load response at a matched arbitrary-force interface.

Even with uniform rates lambda, the density is not governed by the ordinary heat semigroup. For a Fourier mode of Laplacian eigenvalue ell, the mean generator has characteristic polynomial

    z^3+lambda z^2+2ell z+lambda ell.                       (18)

At small ell, two roots are

    z_+/- = +/- i sqrt(ell)-ell/(2lambda)+O(ell^(3/2)).       (19)

Density information is transported as a wave with a diffusive damping envelope. An O(N^2) relaxation bound therefore does not preserve the nonflat heat trajectory law or its rare histories. This is why the construction solves the first task but not root's strengthened target.

## 7. Apparatus and predecessor accounting

The operation supplies O(N) continuous auxiliary coordinates, local bounded-frequency linear couplings, independent finite-intensity bath calls, and fresh Gaussian readouts. A real finite range for every coordinate, finite-precision Gaussian sampler, reset duration, energy reservoir, and force/sensing transducer need their own implementation and error analysis. No such engineering is inherited merely from (2)-(3).

The central ingredients are conventional. Andersen's original thermostat introduces random-time heat-bath collisions and proves canonical invariance: H. C. Andersen, *Molecular dynamics simulations at constant pressure and/or temperature*, J. Chem. Phys. 72 (1980), 2384-2393, DOI 10.1063/1.439486. The actual scanned primary text's temperature-thermostat construction and invariance discussion were read at https://users.wfu.edu/natalie/f23phy711/lecturenote/HCAndersen.pdf (pages 1-2 of the six-page scan). Local momentum-preserving thermostats and stretch/momentum hydrodynamics are established; the primary model in S. Marchesani, *Hydrodynamic limit for a diffusive system with boundary conditions*, https://arxiv.org/abs/1903.08576, was read, including its explicit additional position noise and scaling. Its macroscopic theorem is not imported into (2). Laird-Leimkuhler, DOI 10.1103/PhysRevE.68.016704, is a primary antecedent for auxiliary Hamiltonian thermostat design; only its publisher abstract was read here. Lowe's momentum-conserving pair thermostat is also a close established construction, but its original full text was not retrieved in this pass.

The supplied equations, synchronous coupling and constants above make the ordinary alternative concrete at the task and resource interface. They are not a claim to a new thermodynamic principle or a replacement for the stronger heat/history objective.
