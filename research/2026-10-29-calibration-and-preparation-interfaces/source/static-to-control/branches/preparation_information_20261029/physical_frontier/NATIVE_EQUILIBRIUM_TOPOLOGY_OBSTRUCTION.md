# Vanishing heat need not approach a native equilibrium model in full-path TV

29 October 2026. Independent construction responding to the root question
whether an abstract reversible surrogate must remain in the same calibrated
underdamped thermal source class. This is a theorem with an explicit
stationary mechanical source, not merely a failure to control one proof.

## 1. Claim and observation scope

Fix two position coordinates on the torus of period 2pi, unit masses,
thermal temperature theta>0, damping rate gamma>0, and a force-amplitude
ceiling K. Observe the entire continuous position path on a fixed interval
[0,tau], tau>0. Because positions are continuously differentiable and their
derivative is momentum, this ideal record determines the full phase-space
path. It carries unlimited timing/position resolution; a fixed sampled
grid is a weaker interface.

There are smooth position-only forces F_n of uniformly bounded amplitude
A<=K, with the same calibrated bath and all momenta thermalized at gamma,
such that:

1. Their stationary physical entropy-production rates sigma_n tend to zero.
2. Their full phase-space path laws remain a uniformly positive TV distance
   from EVERY stationary equilibrium model with the same masses, bath,
   torus and position-only force bound K.

The derivative of F_n grows with n. Thus bounded force amplitude and a
fixed thermalization rate do not supply native-equilibrium closure in
full-path total variation. This does not contradict an abstract
Theta-reversible surrogate theorem: a surrogate can leave the
position-only-force class. It does not establish separation at fixed
finite observation bandwidth.

## 2. The stationary source

For integer n>=1 let

    dq_1=p_1 dt,       dp_1=-gamma p_1 dt + sqrt(2gamma theta)dW_1,
    dq_2=p_2 dt,       dp_2=A sin(n q_1)dt-gamma p_2dt
                                      +sqrt(2gamma theta)dW_2. (1)

Positions are periodic. All forces are velocity independent; physical
reversal is (q,p)->(q,-p), with no odd external parameter. The applied
force is the bounded divergence-free shear

    F_n(q)=(0,A sin(n q_1)).                               (2)

A two-sided stationary construction is explicit. Take p_1 stationary OU
and q_1 its integral modulo 2pi with an independent Haar phase. Let Z_2 be
an independent stationary OU process of variance theta and set

    R_n(t)=A integral_0^infinity exp(-gamma s)
                                      sin(n q_1(t-s)) ds,
    p_2(t)=Z_2(t)+R_n(t).                                 (3)

Take q_2 as the integral of p_2 modulo 2pi with an independent Haar phase.
Then q=(q_1,q_2) has the uniform distribution on the torus at every time.
The variables q_1,p_1 have their free equilibrium joint law; q_2 is uniform
independently of the other coordinates at each fixed time. The stationary
law is smooth and positive by the nondegenerate momentum noise and
kinematic coupling. In all cases |R_n|<=r_0:=A/gamma.

## 3. Exact physical dissipation and its vanishing limit

The covariance of the forcing is

    C_n(t)=E[sin(nq_1(t))sin(nq_1(0))]
      = (1/2) exp{-[n² theta/gamma²]
                              [gamma t-1+exp(-gamma t)]}. (4)

Proof: the integrated stationary OU displacement is Gaussian with variance
2theta[gamma t-1+exp(-gamma t)]/gamma². Averaging the independent uniform
phase converts the sine product to half the cosine of this displacement.

The independently driven thermal part Z_2 contributes no excess kinetic
energy. Using (3) and stationarity,

    E R_n² = (A²/gamma) integral_0^infinity exp(-gamma t) C_n(t) dt.

Hence the stationary heat entropy-production rate is exactly

    sigma_n = gamma/theta [E p_1²+E p_2²-2theta]
      = [A²/(2theta)] integral_0^infinity exp(-gamma t)
        exp{-[n² theta/gamma²][gamma t-1+exp(-gamma t)]} dt. (5)

In particular,

    n sigma_n -> A² sqrt(pi)/(2 sqrt(2) theta^(3/2)).       (6)

One proof rescales t=s/n and uses the Taylor expansion at zero together
with an integrable dominating Gaussian for t<=1/gamma. For the remaining
tail, u-1+exp(-u)>=u/e for u>=1. More explicitly,

    integral in (5) <= sqrt(pi e/(2n²theta))
                + exp[-1-n²theta/(e gamma²)]
                    /[gamma+n²theta/(e gamma)].           (7)

This proves vanishing dissipation without an asymptotic approximation.
The odd-sector thermal rate remains gamma. Neither a slow thermostat nor
an unobserved odd degree of freedom is being introduced.

## 4. Every native equilibrium comparator has a fixed path-KL separation

In this source class a stationary zero-entropy model must have a Gibbs
law with centered Maxwell momenta and a conservative force

    G(q)=-grad U(q), |G(q)|<=K,
    rho_G(q,p)=Z_G^{-1}exp[-U(q)/theta] M_theta(p).         (8)

The characterization follows from the irreversible-current square: zero
entropy forces the momentum conditional density to be Maxwellian; the
stationary kinetic equation then forces G to be the corresponding
position log-density gradient. Conversely every such Gibbs source is an
equilibrium model under (q,p)->(q,-p).

Let P_n and Q_G denote stationary full-path laws over [0,tau]. Girsanov
with the same nondegenerate momentum diffusion gives

    D(P_n||Q_G)=D(rho_n||rho_G)
             +(tau/(4gamma theta)) E_{rho_n}|F_n(q)-G(q)|². (9)

The source position marginal is uniform. Periodic integration by parts
and div F_n=0 give integral F_n dot grad U=0. Consequently

    E_{rho_n}|F_n-G|²
       = A²/2 + uniform_average |G|² >= A²/2,

and therefore

    D(P_n||Q_G) >= d_0:=A²tau/(8gamma theta)>0.           (10)

KL separation alone would be insufficient to establish TV separation.
The next step supplies the necessary uniform likelihood-integrability
control; it is part of the theorem.

## 5. Uniform TV separation, with an explicit constant

The torus geodesic diameter is pi sqrt(2). For |G|<=K,

    |log[rho_G(q,p)/(uniform_q M_theta(p))]|
                                <= c_q:=K pi sqrt(2)/theta.

Conditional on q_1,p_1, the source p_2 is a mixture of Gaussians with
variance theta and means R_n in [-r_0,r_0]. Thus

    |log[rho_n/(uniform_q M_theta)]|
                      <= r_0|p_2|/theta+r_0²/(2theta).

Set

    c_0=c_q+r_0²/(2theta),  c_1=r_0/theta,
    C_init=2c_0²+2c_1²(theta+r_0²),
    B_force=A+K,
    C=3[C_init+B_force² tau/(2gamma theta)
                          +B_force^4 tau²/(16gamma²theta²)]. (11)

Then E_{P_n}[log(dP_n/dQ_G)]²<=C for every n and comparator G.
Indeed initial log-density ratios have the bound C_init. The dynamic
log-likelihood under P_n is a martingale of second moment at most
B_force²tau/(2gamma theta), plus a nonnegative drift bounded by
B_force²tau/(4gamma theta). Applying (a+b+c)²<=3(a²+b²+c²) proves (11).

The following elementary information inequality completes the argument.
For r=dP/dQ, delta=TV(P,Q), and E_P(log r)_+²<=C,

    D(P||Q) <= delta + sqrt(C delta).                     (12)

Proof: use D=E_Q[r log r-r+1]. On r<1 the integrand is at most 1-r.
On r>=1 it is at most (r-1)log r. Cauchy--Schwarz bounds the latter
integral by sqrt[E_Q(r-1)_+ * E_Q((r-1)_+(log r)²)]
<=sqrt(delta E_P(log r)_+²). Each signed variation has mass delta.

Combining (10)--(12), uniformly in n and G,

    TV(P_n,Q_G) >= delta_0
      := 4 d_0²/[sqrt(C+4d_0)+sqrt(C)]² >0.               (13)

For the simple normalization A=gamma=theta=K=tau=1, one may use the
uniform rational statements sigma_n<2/n and TV(P_n,Q_G)>1/12000.
Indeed pi<22/7 and sqrt(2)<3/2 give C<18045/98<185, d_0=1/8, and exactly
185/12000<(1/8-1/12000)^2. These deliberately conservative constants
make the qualitative separation fully explicit.

Because continuous q paths determine p paths, the same lower bound holds
for the ideal complete continuous position record, although q is even
under physical reversal. This is a separation from native equilibrium
sources, not from all abstract time-reversible stochastic processes.

## 6. What the counterexample teaches

The force oscillates over position scale 1/n. Its filtered contribution to
kinetic energy vanishes, so heat vanishes. Full-bandwidth phase-space data
can nevertheless detect the force in the noisy momentum increments. A
conservative force cannot imitate the divergence-free shear over the
uniformly visited torus, and the amplitude ceiling prevents likelihood
differences from being confined to arbitrarily violent rare events.

At every finite n this is an ordinary smooth underdamped source with
positive dissipation. There is no infinite physical speed or exact zero-
heat driven source. The limiting distinction requires increasing spatial
and temporal resolution. No claim of an acquired laboratory record or
uniform-cost discriminator is made.

The observation topology is load bearing. The Girsanov discrimination
uses the full path. The accumulated forcing becomes small after temporal
integration, so ordinary weak path or fixed-resolution approximation can
behave differently. One may not transfer the TV obstruction to a finite
grid without another construction.

## 7. A positive native bridge under force compactness

The missing topology step can be supplied without a uniform mixing rate
or an initial-law KL estimate. Kinematic noise regularization is enough.

**Theorem.** Fix dimension d, a connected position torus, unit mass,
gamma>0, theta>0, a force bound K and a Lipschitz bound L. Let F range over
position-only fields with ||F||_infinity<=K and Lip(F)<=L. Use the ordinary
stationary underdamped source, with no odd external fields. Let P_F^tau
be its full stationary path law on a fixed finite interval. Let E_{K,L}
be the path laws in this class with conservative periodic forces. Then

    sigma(F_j)->0 implies dist_TV(P_Fj^tau,E_{K,L})->0.   (14)

In particular there exists a class-dependent modulus omega(s)->0 such
that dist_TV(P_F^tau,E_{K,L})<=omega(sigma(F)). The proof establishes the
existence of this modulus, not an effective value or an acquisition cost.
Any fixed measurable readout contracts the distance, so the conclusion
also holds for its observed path law.

### Step A: compact forces and tight stationary states

Arzela--Ascoli gives a uniformly convergent subsequence F_j->F with the
same K and L bounds. The stationary variation-of-constants formula for
momentum is a stationary Gaussian OU convolution plus a force convolution
bounded in norm by K/gamma. Thus stationary momentum moments of every
fixed order are uniformly bounded. Positions lie on the compact torus,
so stationary measures rho_j are tight. Choose rho_j weakly convergent
to rho.

For fixed initial state and finite time, synchronous SDE coupling and
Gronwall give convergence under uniform convergence of F_j. On compact
initial sets it is uniform. Stationarity and tightness therefore imply
that rho is stationary for F. This step does not use quantitative mixing.

### Step B: vanishing heat identifies a Gibbs limit

The native Gaussian bath identity and Gaussian logarithmic Sobolev
inequality imply

    D(rho_j || (rho_j)_q M_theta) <= sigma(F_j)/(2gamma). (15)

This is conditional momentum information, not entropy to an assumed full
Gibbs position law. Hence rho_j is TV-close to its own position marginal
times Maxwell momenta. Its weak limit has the form rho=nu(q) M_theta(p).

Apply the stationary equation of the limiting source to the test function
phi(q)p_i. Since Maxwell momentum has mean zero and covariance theta I,

    theta integral partial_i phi dnu + integral F_i phi dnu=0,
    equivalently partial_i nu = (F_i/theta) nu             (16)

as distributions. This already forces a positive Gibbs density. A direct
regularity argument avoids assuming it in advance: convolve nu with a
strictly positive smooth torus approximate identity. The resulting
densities nu_epsilon satisfy

    |grad nu_epsilon| <= (K/theta) nu_epsilon.

Their normalized log densities are uniformly Lipschitz and uniformly
bounded above and below on the connected compact torus. A subsequence
converges uniformly to a positive density nu. Convolution in (16), using
continuity of F, gives grad nu=(F/theta)nu. Therefore

    F=theta grad log nu = -grad U,
    U=-theta log nu,

and the limit is a native equilibrium model within the same force class.

### Step C: a kinetic-noise smoothing lemma in total variation

For any Lipschitz force F and fixed t>0, its transition kernel K_t^F(z,.)
is locally Lipschitz in z for TV distance. This can be proved directly
by a deterministic bridge and Girsanov, without a global contraction.

For two nearby initial states z,z', choose a cubic vector function eta_q
with eta_q(0)=q-q', eta_q'(0)=p-p', eta_q(t)=eta_q'(t)=0, and set
eta_p=eta_q'. If Y follows the source from z', X=Y+eta starts at z and
has the correct position equation. Its momentum drift differs from the
desired source at X by

    u_s=F(X_q-eta_q)-F(X_q)+gamma eta_p+eta_p'.

Thus |u_s|<=L|eta_q|+gamma|eta_p|+|eta_p'|. The squared integral is bounded
by C_t(L,gamma)|z-z'|². Girsanov and Pinsker control endpoint TV by a
constant times |z-z'|, since X_t=Y_t. The noise covariance is the same
2gamma theta I throughout. A local torus lift handles the position
coordinates, and compact initial sets have uniform continuity constants.

It follows that for weakly convergent tight measures mu_j->mu,

    TV(mu_j K_t^F, mu K_t^F)->0.                          (17)

For completeness, approximate K_t^F on a compact set by finitely many
kernel values using its TV continuity. Choose the partition boundaries
to have mu-measure zero; weak convergence handles the finite mixture
weights. Tightness controls the complement. This proves (17).

### Step D: stationary and full-path TV continuity

For two forces with uniform difference delta_F, Girsanov with the same
initial state gives, uniformly over that state,

    TV(K_t^{F_j}(z,.),K_t^F(z,.))
                     <= delta_F sqrt[t/(8gamma theta)]. (18)

Stationarity, (17) and (18) imply

    TV(rho_j,rho)
      <= sup_z TV(K_t^{F_j}(z,.),K_t^F(z,.))
                       + TV(rho_j K_t^F,rho K_t^F) ->0.

The same Girsanov inequality holds for full conditional paths, so

    TV(P_Fj^tau,P_F^tau)
       <= TV(rho_j,rho)
                      + ||F_j-F||_infinity sqrt[tau/(8gamma theta)]
       ->0.                                             (19)

Since the limit F is conservative, every sequence with vanishing sigma
has a subsequence approaching E_{K,L} in full-path TV. A contradiction
argument proves (14) and the existence of omega. No supplied global
hidden contraction, stationary preparation time, or uniform statistical
sample bound has been used or acquired.

### What the regularity premise buys

The shear family has bounded amplitude but Lipschitz constant nA, so it
escapes this compact class. Equations (13) and (14) therefore give a
genuine boundary: local thermalization controls reversal ambiguity, while
spatial force regularity is a separate resource for an equilibrium
explanation that retains the calibrated mechanical interface in
full-path TV. This does not show that a Lipschitz bound is the unique
possible repair; finite observation bandwidth or another compactness
condition can change the question. Neither bound is acquired merely by
fitting a coarse record.
