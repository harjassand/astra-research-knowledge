# A finite-duration local LC program with the ordinary heat density action

30 October 2026. Complementary constructive result, awaiting independent receiving review. The reciprocal LC/wave counter is the ordinary construction developed by the existing physical-mechanism role in `RECIPROCAL_WAVE_COUNTER.md`. This file supplies a different actual bath interface: finite-duration local Gaussian rotations, a declared isolation schedule, and a direct discrete-cycle receiver. It does not infer that interface from an unknown native resistor or from equilibrium weights.

## 1. Outcome and the paid change of interface

There is a local, finite-duration Gaussian program on a harmonic ring whose physical density and current have, on time N^2 T:

- ordinary nonflat heat relaxation with an explicitly determined diffusivity D;
- the full ordinary Gaussian heat **density-path** rate function at speed N;
- superexponentially vanishing harmonic current, uniformly over the whole horizon;
- no white driving force in the program and no event-responsive global bit.

The actual bath consists of fresh, independently prepared scalar Gaussian auxiliaries and local rotations of fixed duration. During each bath pulse the native transport port and wave interconnection are isolated. A predetermined periodic schedule coordinates these local operations. Isolation, timing, pulse fidelity, auxiliary preparation, retirement of used auxiliaries, and the visible initializer are real supplied resources. In particular, this is a stronger control port than passive access to arbitrary unknown reciprocal kinetic coefficients.

The variables are signed harmonic density and circuit/mechanical amplitudes. They are not exclusion occupations. The result does not supply the nonlinear particle construction or a force port not included in the schedule.

## 2. Actual schedule, physical current, and equilibrium

Let `(Bv)_i=v_(i-1)-v_i` on the N-site ring. Fix positive h,b,a,tau, independently of N, and write P=h+b for the physical period. Put

    g_N^2 = 1/log(N+1)                                     (1)

for sufficiently large N. The finitely many smaller sizes can use any fixed positive tap below the bounds used below.

Each cycle has two operations.

**Transport, duration h.** Run the actual lossless nearest-neighbor equations

    dx=Bv dt,
    dq=(g_N v-a B^T p)dt,
    dp=a Bq dt,
    tau dv=-(B^T x+g_N q)dt.                               (2)

Measure the physical current as `dJ=v dt` throughout this operation.

**Local bath pulses, duration b.** Isolate the port in (2), so x,q,p are held fixed and physical `dJ=0`. At each site, couple `u_i=sqrt(tau)v_i` to its own fresh, independently prepared scalar `r_i~N(0,1)` and perform

    du_i/dt=Omega r_i,       dr_i/dt=-Omega u_i,
    Omega=pi/(2b).                                         (3)

At the end, `u_i'=r_i(old)` and `r_i'=-u_i(old)`. Retire the used reservoir coordinate. The body has exactly received an independent Gaussian u_i. The reservoir carrying the old u_i is not reset for free.

All rotations act on disjoint local pairs and have fixed frequency Omega. The coefficients in (2) have bounded local norm: a and tau are fixed and g_N is bounded. Currents are continuous inside each transport segment. They are switched off during isolation; **the output is the actual gated current**, not v integrated through a closed port. All displacement during every transport segment is counted. The ideal abrupt change of a coupling at a stage boundary can be replaced by a fixed smooth envelope: use h as its integrated Hamiltonian duration and P as the resulting total physical period. No overlap between the transport and bath generators is inferred.

Every operation preserves

    mu_N = N_{sum x=0}(0,I) x N(0,I)_q x N(0,I)_p
           x N(0,tau^(-1)I)_v.                            (4)

For (2) this follows from skewness in energy coordinates `(x,q,p,sqrt(tau)v)`; for (3) it follows from orthogonal rotation with a fresh unit Gaussian. The body marginal is (4) at every phase when it starts there. The phase is part of the specified program; time-homogeneous reversibility is not claimed.

The initializer used for the nonflat theorem is an actual deterministic profile x_N^0 with zero sum, converging to a smooth rho_0 and satisfying `||x_N^0||^2<=C N`, together with independent thermal q,p,v from (4). This is a supplied conditional preparation, not postselection on a fully retained microscopic thermal sample. Alternatively all q,p can be initialized at zero, with the same result below; the proof notes the changed covariance term. In both cases the first velocity Gaussian draw is paid.

## 3. Exact current counter, including the bath interval

During (2), summation of the q equation gives `d sum q=g_N d sum J`. During (3), both quantities are fixed. Hence every actual path satisfies

    J_tot(t)=g_N^(-1) sum_i[q_i(t)-q_i(0)].                  (5)

The wave term transports local stored information, so `x-Bq/g_N` is not conserved. Thus the earlier frozen-profile local-counter failure is absent.

Under the thermal initializer, any linear path functional has covariance at most its stationary counterpart after conditioning x(0). In particular each `sum q` has variance at most N, and the current difference has variance at most `4N/g_N^2`. The mean harmonic current is zero in this homogeneous program: the initial x has zero mean and only the zero Fourier mode could drive it.

Within each transport stage, the zero mode is just a two-coordinate harmonic rotation of q_0 and u_0. Its maximum is bounded by the sum of the two starting amplitudes. During a bath it is fixed. A Gaussian tail bound and a union over at most `1+N^2 T/P` stages therefore give, with numerical constants c,C_T,

    P(sup_(t<=T) |J_tot(N^2 t)| > epsilon N^2)
       <= C_T(1+N^2) exp[-c epsilon^2 g_N^2 N^3].           (6)

The same estimate, up to constants, holds with zero q,p initialization; conditional covariance only decreases. Equation (1) implies

    lim_(N->infty) N^(-1) log P(sup |J_tot|/N^2>epsilon)
       = -infinity.                                       (7)

No equilibrium preparation by the later reuse theorem, no typical-current argument, and no finite-TV transfer of finite-action probabilities is used.

## 4. Exact cycle matrix

Fix a nonzero Fourier wave number k and let

    beta=2 sin(k/2),       ell=beta^2.

A fixed unitary phase change on x and p makes the incidence symbol beta real. In coordinates `(x,q,p,u)`, the transport matrix is the real skew matrix

    K(beta,g) = [[0,       0,       0, beta/sqrt(tau)],
                 [0,       0, -a beta, g/sqrt(tau)],
                 [0,  a beta,       0,              0],
                 [-beta/sqrt(tau), -g/sqrt(tau), 0, 0]].    (8)

Let `U=exp(h K)`, let C be its upper-left 3 by 3 block, and f its upper-right column. At the successive starts of transport, the retained state S=(x,q,p) obeys exactly

    S_(n+1)=C S_n+f xi_n,       xi_n~N(0,1) independent,
    C C^*+f f^*=I_3,            ||C||<=1.                  (9)

This is the actual program, not a discretization error estimate for a white-noise equation. Real conjugate Fourier modes are paired in the usual way. Native particle histories are not being replaced by a signed projected law.

Writing `Theta=diag(1,1,-1)`, momentum reversal of (8) gives

    C^*=Theta C Theta.                                    (10)

These contraction and reversal identities are useful for controlling every omitted mode, including a slowly relaxing auxiliary one.

## 5. The finite cell's exact low-wave-number response

At beta=0, x and p are fixed, while the q,u pair rotates through `theta=g h/sqrt(tau)`. Consequently

    C(0,g)=diag(1,cos(theta),1).                            (11)

To compute the order-beta^2 response on the two retained slow coordinates x,p, hold them fixed to zeroth order over a cell. The q,u equations are

    q'=gamma u+F_q,        u'=-gamma q+F_u,
    gamma=g/sqrt(tau),
    F_q=-a beta p,         F_u=-beta x/sqrt(tau),            (12)

with u(0)=0 for the mean response, and with the periodic condition q(h)=q(0). Direct solution gives

    q(0)=F_u/gamma+(F_q/gamma)cot(theta/2),
    integral_0^h u dt=-F_q h/gamma,
    integral_0^h q dt=F_u h/gamma+2 F_q/gamma^2.             (13)

The condition `1-cos(theta)>0` is satisfied for all sufficiently small positive g. Substitution into x'=beta u/sqrt(tau) and p'=a beta q yields the exact second-order Schur coefficient

    M_g = [[0,          a h/g],
           [-a h/g, -2 a^2 tau/g^2]].                     (14)

For clarity, (14) is also obtained algebraically by partitioning C into slow indices `(x,p)` and the single q index:

    C_ss + C_sq (1-C_qq)^(-1) C_qs
       = I_2+beta^2 M_g+O_g(beta^4).                      (15)

The two decay coefficients are

    D_+/- (g) = (a^2 tau/g^2)
          [1 +/- sqrt(1-g^2 h^2/(a^2 tau^2))].             (16)

Thus

    D_-(g)=h^2/(2tau)+O(g^2),
    D_+(g)=2a^2tau/g^2+O(1).                              (17)

The small coupling has not removed all auxiliary modes. It separates one fast diffusive auxiliary branch from the physical density branch.

### Uniformity when the coupling tends to zero

The following elementary finite-matrix estimate is enough; its bounds are deliberately loose. For fixed h,a,tau there are positive c,C,g_0 such that, for `0<g<g_0` and `0<|beta|<=c g^8`, C has a simple real density eigenvalue

    lambda_s = 1-beta^2 D_-(g)+O(beta^4 g^(-12)),            (18)

and a right eigenvector w with w_x=1 satisfying

    ||w-e_x|| <= C(g+|beta|g^(-6)).                        (19)

To see the bounds without assuming uniform eigenvalue separation at g=0, expand the analytic matrix C in beta. The slow-slow and q-q blocks are even in beta and the two off-diagonal blocks are odd. The q gap is `1-cos(theta)>=c g^2`. Eliminate q in a disk `|lambda-1|<=C beta^2/g^2`; its resolvent is at most C/g^2. After dividing the two-dimensional Schur equation by beta^2, the coefficient is M_g with remainder bounded by `C beta^2/g^6`. The eigenvalues of M_g have separation of order g^(-2), and its eigenvectors can be normalized as `(1,O(g))` and `(O(g),1)`, with uniformly bounded condition number. The elementary implicit-function estimate therefore identifies the density root, with an error smaller than the deliberately enlarged bound in (18). Back substitution gives a q component at most `C |beta|/g^2`; the change of the slow two-vector is at most `C beta^2/g^4`. These imply (19). The restriction `|beta|<=c g^8` makes each resolvent expansion and remainder absorption uniform.

By (10), a normalized left eigenvector is `Theta w/(w^*Theta w)`. Its distance from e_x has the same bound, and the denominator is `1+O(g^2+beta^2 g^(-12))`. Let Pi_s be the spectral projection. Since it commutes with the contraction C,

    |e_x^* C^n (I-Pi_s)e_x|
      =|e_x^*(I-Pi_s) C^n (I-Pi_s)e_x|
      <= C(g^2+beta^2 g^(-12)),       n>=0.                (20)

This controls every other power and initial transient without separately bounding their potentially close poles. Equations (17)-(20), and the elementary uniform comparison of two decaying exponentials, give for any fixed macroscopic Fourier label m

    sup_(n>=0) |(C^n)_(xx)-exp[-(h^2/(2tau))ell n]|
      ->0,             k=2pi m/N, g=g_N.                  (21)

Here `g_N^2=1/log(N+1)` makes every fixed power of 1/g_N negligible compared with N. In particular, the error in (18), multiplied by N^2, vanishes. Equation (21) is not claimed uniformly over microscopic Fourier wave numbers.

## 6. Exact mean and covariance receiver on physical time

The physical cycle has length P=h+b. Its limiting heat coefficient is therefore

    D=h^2/[2tau(h+b)].                                    (22)

This includes the time spent isolating and thermalizing the current coordinate. Ignoring that time would give the wrong diffusivity.

For deterministic visible initialization and independent thermal q,p, Gaussian conditioning and (9) give, for n>=m,

    E x_n=(C^n)_(xx) x_0,
    Cov(x_n,x_m)=(C^(n-m))_(xx)
                 -(C^n)_(xx) (C^m)_(xx)^*.                (23)

If q,p also start at zero, replace the last product by

    e_x^* C^n C^{*m} e_x.                                 (24)

The latter has the same limit: the right and left density eigenvectors approach e_x, and C remains a contraction. Thus, for the centered fluctuation mode, (21)-(24) converge to

    exp[-D(2pi m)^2 |t-s|]
      -exp[-D(2pi m)^2(t+s)].                              (25)

The whole process is Gaussian because all schedules and linear maps are deterministic and all fresh inputs are Gaussian. This fact is essential. Poisson-time Gaussian resets generally have the same linear first-moment equation and stationary covariance but a non-Gaussian multi-time law; that different operation cannot inherit this receiver from covariance alone.

Mean convergence for a general smooth initial profile follows by a Fourier-tail approximation and energy contraction. The actual finite-duration motion within a cycle does not change the limit. For a fixed Fourier label, x can change during transport only through a coefficient beta times bounded-norm energy coordinates, over a fixed physical duration. Its mean microscopic-cycle change is O(1/N), and its fluctuation-mode variance is O(1/N^2). The bath phase leaves x fixed.

## 7. Path control and the Gaussian large-deviation step

The empirical density is

    rho_N(t)=N^(-1) sum_i x_i(N^2 t) delta_(i/N),
    Y_N=sqrt(N)(rho_N-E rho_N).                            (26)

Use `C([0,T],H^(-s))`, for example any s>3/2, for the density path. Finite-duration currents make the actual density path continuous.

Here are the estimates needed beyond finite-dimensional covariance convergence.

First, at a fixed Fourier label, decompose the linear observable e_x using the left density eigenvector. Under the stationary Gaussian reference, the eigenvector component has increment variance proportional to `1-lambda_s^r` over r cycles; the residual has variance at most its squared norm times four. Therefore, on the macroscopic clock,

    E |Yhat_N(m,t)-Yhat_N(m,u)|^2
      <= C_m[|t-u|+g_N^2+N^(-2)g_N^(-12)]                 (27)

at cycle times. Conditioning the initial state only reduces increment covariances. The finite-duration within-cycle difference has variance O_m(N^(-2)). Taking Gaussian tails and a union over O(N^4) pairs of cycle times proves the exponential temporal modulus: for every fixed finite Fourier projection and epsilon>0, the speed-N logarithmic probability of a density modulus exceeding epsilon tends to minus infinity as the macroscopic time mesh tends to zero. The floor in (27) tends to zero before that mesh limit. It is not being used as a finite-N Kolmogorov modulus.

Second, at a cycle start the full normalized body covariance is bounded by identity, and its deterministic mean energy is bounded by C N. The same bounds hold during the exact orthogonal transport and bath operations, including the active fresh reservoir. For high Fourier labels, the weighted norm of all four coordinates bounds that of x throughout a transport segment because each Fourier block evolves orthogonally. The Gaussian Hilbert-norm tail, followed by a union over O(N^2) segments, gives for any fixed epsilon and large Fourier cutoff K

    limsup_N N^(-1) log P(sup_t ||P_(>K)(rho_N-E rho_N)||_(H^-s)
                             >epsilon)
       <=-c epsilon^2 K^(2s).                              (28)

The expected tail norm vanishes as N increases at fixed K. The deterministic mean tail is bounded by C K^(-s) by its energy bound. The usual discrete Fourier alias sums converge for s>1/2. These estimates prove exponential tightness in the stated continuous-path topology and exponentially good finite-mode/time-grid approximations. Within a finite-duration pulse the relevant fixed-mode path is generated by a fixed-dimensional bounded-frequency linear map, so a bounded collection of Gaussian coordinate tails controls its supremum; no uncounted microscopic time grid or white-noise limit is needed.

The finite-dimensional normalized log moment-generating functions of rho_N now converge, by (23)-(25), to those of the small-noise heat Gaussian. Their quadratic Legendre transforms and the exponentially good finite approximations identify the complete path rate. Equivalently, identify the Cameron--Martin image of

    dY=D partial_x^2 Y dt+sqrt(2D) partial_x dW,
    Y(0)=0.                                               (29)

The density rate is

    I_dens(rho)=(1/(4D)) integral_0^T
                  ||partial_t rho-D partial_x^2 rho||_(Hdot^-1)^2 dt,
    rho(0)=rho_0, sum/mass fixed,                           (30)

with the weak controlled-PDE interpretation, and infinity if no square-integrable control realizes the path. This is the full rate, not only its value on smooth histories. Exponential tightness supplies goodness. The mean path is the ordinary nonflat heat solution.

## 8. Joint native-current action

Set

    W_N(t)=N^(-2) sum_i J_i(N^2t) delta_(i/N).               (31)

Exact native continuity gives, for each resolved nonzero Fourier mode,

    rhohat_N(t)-rhohat_N(0)=N b_k What_N(t),                (32)

with the fixed incidence orientation. On `|m|<=N/2`, the nonzero inverse multipliers are bounded by C/|m| and converge to the continuum inverse derivative. The density exponential compactness and these multiplier bounds identify the nonconstant current as a continuous inverse-gradient image of the density change in a weak Sobolev path topology. The constant mode is superexponentially zero by (7).

Consequently the joint density/integrated-current LDP is

    I(rho,j)=(1/(4D)) integral_0^T integral_0^1
                          (j+D partial_x rho)^2 dx dt,    (33)

on

    partial_t rho+partial_x j=0,
    rho(0)=rho_0,
    integral_0^1 j(t,x) dx=0 for almost every t,             (34)

and infinity otherwise. The observed current path is `W(t)=integral_0^t j(s)ds`. A finite-action pair is the weak PDE image of an L2 control; smoothness is not imposed by definition. The ordinary Gaussian heat model minimizes over its harmonic current at zero, since its mobility is spatially constant. Thus (33) retains that model's entire contracted density action while excluding its nonzero harmonic histories.

This conclusion uses only the declared native output. Apparatus energy or charge transport in a different channel must be counted separately if it is part of an application's requested output.

## 9. Resources, conditioning, and exclusions

On physical time N^2 T there are `N floor(N^2 T/(h+b))`, up to the endpoint initialization, actual fresh Gaussian reservoir preparations and local bath rotations. There are O(N) live body coordinates and O(N) simultaneous reservoir slots, with no global state-dependent decision. Used reservoirs contain the retired velocities and require actual removal or later paid rethermalization. All counts are of physical operations, not retained bits.

The prescribed periodic phase must be supplied by synchronized local timers or an actual drive. Its initial preparation and later timing errors are not free. The proof treats the exact supplied schedule. A bounded maximum frequency is not a hard frequency cutoff, a finite bit representation, or a hard amplitude cap. Gaussian coordinates have unbounded support. At the rare-history objective, discarding fixed-probability saturation, preparation, or calibration failures is invalid. For example, a naive amplitude cutoff of order sqrt(log N) may be adequate for typical trajectories but is not automatically superexponentially harmless at speed N.

The port-isolation premise is substantive. Unknown native reciprocal friction, residual force, or hidden dynamics during the transport or bath pulse cannot simply be composed into (2)-(3). A Poisson Andersen replacement at unknown bounded local rates is an ordinary finite-rate alternative that preserves the same Gibbs law and the counter; its means match a corresponding damped LC system. Its full path is a Gaussian mixture, so its density rare-history theorem needs a different proof.

The stated receiver is homogeneous. It does not make an unknown heterogeneous current-metric projection equal to the density-preserving orthogonal projection. A force applied during the isolated stage or directly to a retired reservoir is a different force port. No suppression at unchanged circulating-load response, no device efficiency, and no practical superiority is asserted.

For an old retained record, require the stated initial law and complete future conditional pulse/auxiliary laws after that record. A conditional-on-calibration-coverage result can use the theorem at its warranted parameters. A fixed failure-probability mixture does not inherit the unconditional speed-N rate. Newly exposed reservoir or fine apparatus records are not part of the density/current action proved here.

## 10. Primary comparison and executable scope

The reciprocal LC architecture and the homogeneous continuous receiver are credited to the existing physical-mechanism role. Freitas--Delvenne--Esposito, *Stochastic and Quantum Thermodynamics of Driven RLC Networks*, PRX 10, 031005 (2020), https://arxiv.org/abs/1906.11233, is a direct primary construction for passive network state, topology, reciprocal response and thermal-noise accounting. Its introduction and graph/port construction were read here; the preceding role read the deeper thermodynamic sections. This file does not infer a fabricated transducer from a graph equation.

Andersen's original random-collision thermostat, DOI 10.1063/1.439486, is a direct predecessor for independent canonical refreshing. Its actual temperature-thermostat construction was read in the scanned primary source https://users.wfu.edu/natalie/f23phy711/lecturenote/HCAndersen.pdf. Replacing a Gaussian coordinate by a quarter-rotation with a fresh Gaussian oscillator is elementary harmonic-bath machinery. Hamiltonian/heat-bath splitting is also conventional. The finite schedule and its exact cell coefficient must carry the present receiver; no generic new thermalization or LC principle is claimed.

Duncan--Lelievre--Pavliotis, DOI 10.1007/s10955-016-1491-2, https://www.ma.imperial.ac.uk/~pavl/nonreversible.pdf, explicitly treats invariant-preserving antisymmetric drifts and lifted/Hamiltonian sampling. Its introduction and invariant-drift formula were read; it reinforces the boundary against claiming generic auxiliary-state or skew-motion novelty. Zhu--Zhu, *Kawasaki-type dynamics: Diffusion in the kinetic Gaussian model*, DOI 10.1103/PhysRevE.66.017102, https://arxiv.org/abs/cond-mat/0204156, is a direct conservative Gaussian redistribution predecessor read during the initial finite-rate attack. Its mean diffusion calculation is not this finite-duration path theorem.

`check_finite_pulse_lc.py` and `FINITE_PULSE_LC_CHECK.json` record the executed population check of orthogonality, exact Gaussian covariance balance, zero-mode current counting, the finite cell Schur coefficient, and low-mode mean/variance convergence. These checks resolve the finite-cell normalization and timing risk; they are not measured data, an acquisition budget, or an independent proof of the asymptotic LDP.
