# Same exponential response, different predictive initialization

## Scope

This is a fixed-deadline indistinguishability theorem and its exact attainable
uncertainty radius. It does not challenge the accepted bridge, which assumes
actual first-order dissipative hidden branches. Conservative dilation and the
importance of preparation are established theory. The result below makes the
finite-access ambiguity and its constants explicit.

The visible potential is mu x^2/2, mu>0. A calibrated local drag is one. Controls
apply additive force, or a nonnegative moving trap during preparation. They
cannot directly change the hidden generator. The future query is a prescribed
untrapped additive-force program. Preparation can use arbitrary causal control,
classical feedback, and force/position measurements.

## 1. A fixed passive conservative bath

For a>0 and B>0, use the positive spectral measure on omega>=0

    dnu = [2Ba/(pi(a^2+omega^2))] domega.

It has total mass B. Let r_omega be hidden strain and p_omega its conjugate
coordinate. In a mild sense set

    xdot = -mu x - integral r_omega dnu + f,
    rdot_omega = xdot - omega p_omega,
    pdot_omega = omega r_omega.

The nonnegative storage

    E = mu x^2/2 + (1/2) integral (r_omega^2+p_omega^2) dnu

obeys Edot=f xdot-xdot^2. Truncation and mild limits extend this identity as an
energy inequality to all finite-energy states. No finite spectral-moment bound
is required. The hidden dynamics is conservative.

Eliminating it gives

    xdot + mu x + K*xdot = f+g,
    K(t) = integral cos(omega t) dnu = B exp(-at), t>=0,
    g(t) = integral [u(omega)cos(omega t)+v(omega)sin(omega t)] dnu,

where u=-r(0), v=p(0). Initial hidden energy is

    E_bath = (1/2) integral (u^2+v^2) dnu.

The zero-state response is exactly that of a single dissipative Maxwell mode.
It does not determine the allowed hidden initial-force histories.

## 2. Exact force-history energy

Use Fourier transform ghat(omega)=integral_R exp(-i omega t)g(t)dt, and write
r(omega)=2Ba/[pi(a^2+omega^2)] for the spectral density. For real g in H^1(R), put

    u = Re(ghat)/(pi r),       v = -Im(ghat)/(pi r).

Fourier inversion gives the requested g. Plancherel yields

    E_bath[g] = [1/(4Ba)] integral_R [g'^2+a^2 g^2] dt.          (1)

Conversely every finite-energy pair (u,v) gives this H^1 function and the same
norm. Because the density is strictly positive, the representation is unique
modulo null sets.

Translation of g preserves (1). Any smooth compactly supported force pulse can
therefore be delayed arbitrarily while retaining exactly the same energy.

## 3. Arbitrary causal local preparation does not reveal a future-only force

Fix a finite preparation deadline H. Choose opposite initial states whose old
forces are +g and -g, with g=0 on [0,H]. Use the same controller random bits and
the same meter noise in both experiments. Causality and uniqueness imply the
same visible path, trap force, additive control, every finite observation, and
every adaptive controller action throughout [0,H]. The common applied force
changes the driven bath contribution but does not reveal or erase the latent
initial-force difference.

This exact indistinguishability permits noiseless continuous observation. It
also rules out a deterministic causal stopping rule that terminates in finite
time on the zero-free-force record: take H to be that execution's stopping time,
then place the indistinguishable pulse immediately afterwards. A private
randomized stopping time has different quantifiers; its constructive escape is
proved in RANDOMIZED_PREDICTIVE_INITIALIZATION.md. A fixed deadline with a
randomized choice of preparation controls is still covered by the same pair.

## 4. Exact minimax future radius

For a force vanishing before H, introduce w by

    g'+a g = sqrt(2Ba) w,      g(H)=0.

For w in L2(H,infinity), (1) and integration by parts give

    E_bath = (1/2) integral_H^infinity w^2.                     (2)

Take w supported on [H,H+T] and continue g exponentially afterwards. The energy
of that continuation is already included in (2).

For the same future prescribed input, the deviation from the nominal g=0 path
has transfer function

    X(s)/W(s) = sqrt(2Ba)/[s^2+(a+mu+B)s+a mu].                  (3)

Write

    r_minus = ((a+mu+B)-sqrt((a+mu+B)^2-4a mu))/2,
    r_plus  = ((a+mu+B)+sqrt((a+mu+B)^2-4a mu))/2.

Both roots are positive and distinct for B>0. Its impulse response is

    h(t)=sqrt(2Ba)[exp(-r_minus t)-exp(-r_plus t)]/(r_plus-r_minus).

For hidden energy at most E, the exact L2-to-sup radius on [0,T] is

    R(E,T) = sqrt(2E) ||h||_L2(0,T).                            (4)

The upper bound is Cauchy--Schwarz at each time; the partial L2 norm of h increases
with time. Equality at T is attained by

    w(s)=sqrt(2E) h(T-s)/||h||_L2(0,T),   0<=s<=T.

The nominal response is the attainable center. The two opposite extremizers
have the same entire preparation record and future separation 2R at T. Any
forecast errs by at least R for one of them. For randomized forecasts, one of
the states has failure probability at least 1/2 at every strict error threshold
below R. The initial state is chosen before the random forecast seed.

More generally, states consistent with g=0 on [0,H] may have nonzero g at negative
times. That past part only uses additional energy in (1); it cannot increase
(4). Setting it to zero attains the bound. Thus (4) is the exact radius for the
zero-free-force record, not merely a lower bound from a special pair.

No H occurs in (4). A longer prescribed preparation interval cannot reduce this
worst-case radius. The center is a two-state linear ODE and is computationally
attainable. Finite numerical and drive errors can be added through the same
linear response, with their actual computation and actuator costs.

An explicit expression is

    ||h||_2^2 = [2Ba/(r_plus-r_minus)^2] *
       [(1-exp(-2r_minus T))/(2r_minus)
        +(1-exp(-2r_plus T))/(2r_plus)
        -2(1-exp(-(r_minus+r_plus)T))/(r_minus+r_plus)].          (5)

As T tends to zero, R ~ sqrt(4BaE/3) T^(3/2). As T tends to infinity,

    ||h||_2^2 -> B/[mu(a+mu+B)],
    R -> sqrt(2BE/[mu(a+mu+B)]).

These are worst-case energy-ball statements. They do not assign probability to
the extremizing states under a thermal equilibrium preparation.

### Known positive observed inertia

If the physical implementation requires an observed mass M>0, use

    M xddot + xdot + mu x + K*xdot = f+g.

The storage adds M xdot^2/2, while the hidden force-energy identity (1) is
unchanged. With the initial visible coordinate and velocity fixed at zero, the
same indistinguishable states now have transfer

    X/W = sqrt(2Ba)/[(s+a)(M s^2+s+mu)+Bs].

Its impulse response h_M gives the exact radius sqrt(2E)||h_M||_L2(0,T), attained
by the same reversed-impulse construction. The norm is computable from a
three-state controllability Gramian. Thus finite positive inertia does not
remove the obstruction. The explicit two-root formula (5) is specifically the
overdamped M=0 case.

## 5. Finite-mode approximants

The exact exponential kernel uses a continuum. Absence of a supplied finite
dimension or spectral cutoff prevents a uniform escape by replacing it with an
unknown finite bath at a nonzero metrology resolution.

Fix finite duration S and eps in (0,1). Truncate at omega=W and partition [0,W]
into cells of width at most Delta. Put a mode at each midpoint, with exact cell
mass b_j and mass-weighted averages u_j,v_j of the original initial state.
Jensen gives

    (1/2) sum_j b_j(u_j^2+v_j^2) <= E.

The omitted spectral mass obeys m_tail<=2Ba/(pi W). Uniformly for |t|<=S,

    |K_N(t)-K(t)| <= m_tail + BS Delta/2,
    |g_N(t)-g(t)| <= sqrt(2E m_tail)+sqrt(2EB)S Delta/2.         (6)

The second estimate uses Cauchy--Schwarz in the tail and the Lipschitz bound on
the sine/cosine vector inside each cell. Therefore W=O(a eps^(-2)) and
Delta=O(eps/S) give force error O(sqrt(2EB)eps), kernel error O(B eps), with

    N=O(aS eps^(-3))

finite modes. All frequencies and amplitudes can be rounded with additional
finite error. A bounded finite local-control program gives a finite continuity
bound from (6) to the measured averages. Select eps below its actual metrology
resolution or finite Gaussian exposure budget. This can be expensive; no
polynomial bound in every controller parameter is asserted.

## 6. Consequence and prior machinery

Even a perfectly known one-mode completely monotone response kernel does not
determine predictive initialization from an energy bound. An actual dissipative
Maxwell branch permits only a decaying-exponential free force. The conservative
realization above permits every H^1 free-force history charged by (1), including
delayed incoming pulses.

This is consistent with generalized Langevin theory, whose initial-state force
requires a preparation or stochastic law. It is also consistent with existing
conservative extension and well-preparedness theory. The derived endpoint here
is the finite-access ambiguity and exact attainable radius, rather than a claim
to have discovered conservative dilation or preparation dependence.

Primary comparisons:

- Figotin and Schenker, Hamiltonian structure for dispersive and dissipative
  dynamical systems, https://arxiv.org/abs/math-ph/0608003
- Mielke, Peletier and Zimmer, Deriving a GENERIC system from a Hamiltonian
  system, https://arxiv.org/html/2404.09284v2, especially well-preparedness.

## 7. Explicit local string realization

The oscillator dictionary has a direct local mechanical realization. Attach a
spring of stiffness B between the observed coordinate x and an endpoint y of a
lossless string. Let the string have positive tension T_s, mass per unit length
rho_s, wave speed c=sqrt(T_s/rho_s), and impedance

    Z=sqrt(T_s rho_s)=B/a.

Its transverse displacement u(xi,t), xi>=0 measured away from the endpoint,
satisfies u_tt=c^2 u_xixi and u(0,t)=y(t). Write

    u(xi,t)=phi(t-xi/c)+psi(t+xi/c),
    v_out=phi',       v_in=psi'.

At the endpoint,

    ydot=v_out+v_in,
    T_s u_xi(0,t)=Z(v_in-v_out)=Z(2v_in-ydot).

The latter is the string force on the endpoint. A massless endpoint force balance
therefore gives

    B(x-y)=Z(ydot-2v_in),
    ydot=a(x-y)+2v_in.                                        (7)

The massless endpoint is a declared ideal boundary element; a small finite
endpoint mass changes the rational transfer and must be included if present.
No limit of an infinitely strong applied control is used in (7).

For r=x-y, the observed-coordinate and spring equations are

    xdot=-mu x-Br+f,
    rdot=xdot-a r-2v_in.

With initial spring strain zero, eliminating r gives the exact same response
kernel K(t)=B exp(-at) and old force

    g(t)=2B integral_0^t exp(-a(t-s))v_in(s) ds,
    g'+ag=2B v_in.

Set w=sqrt(2Z)v_in. Since Z=B/a, this is exactly
g'+ag=sqrt(2Ba)w, with the same signs and normalization as (2)--(3).

### Local energy and its incoming/outgoing split

The string energy density is

    (rho_s/2)u_t^2+(T_s/2)u_xi^2
       =rho_s(v_out^2+v_in^2).

For a pure incoming initial wave, its total energy is

    E_in=Z integral_0^infinity v_in(s)^2 ds
        =(1/2) integral_0^infinity w(s)^2 ds.                  (8)

The endpoint power identity is

    B(x-y)ydot=Z(v_out^2-v_in^2).

Consequently

    d/dt[mu x^2/2+B(x-y)^2/2]
       =f xdot-xdot^2+Z v_in^2-Z v_out^2.

Adding the actual string field energy cancels the last two fluxes and gives
the full passive identity Edot=f xdot-xdot^2. Equation (8) is the actual stored
wave energy, not an abstract statistical noise allowance.

### Exact delayed input from a local initial wave packet

Take v_in supported in [H,H+T]. Define psi(s)=integral_0^s v_in(r)dr and use at
time zero

    u(xi,0)=psi(xi/c),
    u_t(xi,0)=v_in(xi/c),
    u_xi(xi,0)=v_in(xi/c)/c.

The string and endpoint are unperturbed near the source until the packet arrives.
The packet's initial velocity and strain occupy distances [cH,c(H+T)]. Its
displacement may have a constant plateau beyond the packet; that plateau has
zero field energy. Opposite signs give the indistinguishable pair.

Any permitted boundary preparation creates outgoing waves. The linear wave
equation lets outgoing and incoming waves cross without interaction, so boundary
controls cannot modify the incoming packet before it reaches the endpoint.
There is no direct access to the remote field. This earns the causal interface
in the negative theorem by finite propagation, rather than assuming an abstract
unobservable register.

The extremizer in Section 4 supplies an L2 packet and attains the exact radius.
If smooth finite-amplitude initial data are required, approximate that w in L2
by smooth compactly supported packets and rescale to the same energy bound.
The observed endpoint differs by at most ||h||_2 times the L2 approximation
error, so the sharp radius is approached arbitrarily closely. A simple explicit
nonoptimal smooth witness is

    v_in(t)=V0 sin^2(pi(t-H)/T),  H<=t<=H+T,
    V0=sqrt(8E/(3ZT)).

Its energy is exactly E. It has finite peak velocity V0, peak strain V0/c,
and derivative bounded by pi V0/T. It yields a strictly positive later visible
deviation because h and this pulse are positive inside their supports.

### Finite extent and costs

For a witness required only through H+T, use a finite string of length

    ell>c(H+T)

with a free far endpoint. The initial constant displacement plateau is compatible
with its zero-slope boundary condition. All initial velocity and strain fit
inside the line. The far endpoint has no initial motion; waves launched at the
source cannot return before 2ell/c>H+T. The finite line therefore gives the
same local record and future deviation on the relevant horizon. Its response
will have later reflections; it is not globally equal to the infinite-line
exponential kernel for all times.

The construction pays physical extent ell, total string mass rho_s ell, tension
T_s, spring B, and the packet's energy, amplitude and spatial resolution. For
fixed E,T,Z,c, increasing H enlarges the distance/extent but need not increase
packet amplitude or shorten its wavelength. Thus the delayed witness is not
obtained by an ever faster source control. If total hidden extent is supplied
as an upper bound, an experiment can in principle pay its propagation time;
the dimension/extent-independent fixed-deadline obstruction then no longer has
the same quantifiers.

An ideal nondispersive string is the declared continuum physical model. A real
finite-bandwidth line, finite chain, or finitely many normal modes must include
its calibrated dispersion/cutoff error. Smooth packet approximation and the
finite-energy finite-mode estimates (6) provide finite-horizon versions at any
specified nonzero metrology resolution, with paid extent and resolution.
No assertion of an exact unbounded-bandwidth laboratory string is made.

