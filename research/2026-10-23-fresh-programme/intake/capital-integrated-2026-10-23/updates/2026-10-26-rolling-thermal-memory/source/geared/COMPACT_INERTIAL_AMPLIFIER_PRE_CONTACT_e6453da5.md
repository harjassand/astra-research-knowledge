# The quantum locking cost of a compact inertial amplifier

25 October 2026. Owned continuation from the finite-band harmonic frontier.
The physical question is what a passive lever/transformer pays when port
motion and translating mass fail to bound its response inertia. The new
representation is a FINITE-radius rotating body with a finite periodic
helical registry, rather than a massless rigid constraint. This exposes a
quantum shortcut that a linearized ideal inerter omits. The response result
below has an exact attaining family; the open-contact heat projection is
separate and is not supplied by a band-curvature calculation.

The root's abstract PSD counterexample and earlier MOTION_AMPLIFICATION.md
are preserved. They establish why geometry is a real alternative to the
positive-scalar maximum principle. They do not acquire its material
constraint. This note chooses that actual interface rather than another
linear algebra example.

## 1. A passive canonical model with its physical inertia exposed

There are two axial terminal blocks and a balanced rotor whose center is
attached to the left block. Put Y=u_R-u_L. The rotor has actual mass m_r,
radius at most R_r and moment I<=m_r R_r^2. Include its translating mass,
housing and bearings in the left block. If the right translating mass is
chosen equal to the COMPLETE left translating mass, the common coordinate
U=(u_R+u_L)/2 has mass M_tot and the bare relative kinetic mass is
B_0=M_tot/4. More generally the actual two translating mass groups give
their ordinary reduced mass B_0. The balanced rotor adds no translation/
rotation cross term. Every mass is positive and counted.

Let phi be the rotor's COMPACT angle, phi=phi+2pi, and let g>0 be its
helical phase advance per unit relative travel. The finite periodic-lock
Hamiltonian for the relative sector is

    H=p_Y^2/(2B_0)+L_phi^2/(2I)+V(phi-gY),             (1)
    L_phi=-i hbar partial_phi,  V(psi+2pi)=V(psi),
    0<=V<=U_bar<infinity.

The common translation is free and can be added back. Each fixed smooth
bounded V defines a self-adjoint canonical Hamiltonian on R x S^1. It is
positive and time independent. A screw/flywheel or helical magnetic
registry motivates phi-gY; the pitch is p=2pi/g. Equation(1) does NOT grant
an ideal rolling constraint, a zero-mass shaft or an acquired tooth/contact
potential. A literal material implementation must supply that potential
profile, pitch and its finite-force bandwidth in the counted apparatus.

An IDEAL constraint phi=gY mod2pi would give relative inertia

    B=B_0+I g^2.                                      (2)

Although the rotor's Cartesian material positions remain within R_r, its
angle can wind. An all-Cartesian-displacement cap therefore does not bound
(2). This is the precise compact-motion escape from a long translating
proof mass. The question is whether a FINITE lock actually yields B.

## 2. Exact reduction to a flux-sensitive rotor, not a harmonic truncation

Use psi=phi-gY and Fourier transform the remaining helical translation.
Its conserved momentum is P=p_Y+gL_phi. The exact fiber Hamiltonian is

    H(P)=P^2/(2B)+(L_phi-hbar q(P))^2/(2I_perp)+V(psi),
    I_perp=B_0 I/B,
    q(P)=g I P/(hbar B).                              (3)

In particular the NORMAL recoil scale is

    E_R=hbar^2/(2I_perp)=hbar^2 B/(2B_0 I).            (4)

No angle has been unwrapped and no high rotor state was discarded. Let
epsilon(q) be the lowest eigenvalue of the periodic operator
E_R(-i partial_psi-q)^2+V(psi). Its zero-flux ground state psi_0 is real,
strictly positive and nondegenerate. The lowest helical dispersion is

    E_0(P)=P^2/(2B)+epsilon(q(P)).                     (5)

Define the measurable low-band inertia by E_0''(0)=1/B_eff. This is an
exact band response. Equating it to an entire open-contact finite-frequency
susceptibility would require additional preparation/projection estimates.

## 3. An exact ground-density formula for the actually reflected inertia

Normalize int_0^(2pi) psi_0^2=1 and define the one-dimensional phase stiffness

    f=(2pi)^2/[int psi_0^2 int psi_0^-2],  0<f<=1.      (6)

Then epsilon''(0)=2E_R f. A short derivation is worth retaining. At small
flux, the first derivative of the ground vector is purely imaginary, so
write its phase correction as psi_0 exp(iq chi). The exact second-order
ground-energy minimization is

    epsilon''(0)/2=E_R inf_(periodic real chi)
                         int psi_0^2(chi'-1)^2.

Stationarity gives psi_0^2(chi'-1)=constant. Periodicity fixes the constant
to -2pi/int psi_0^-2 and yields (6). Real amplitude changes start at order
q^2 and their contribution cancels by ground-state stationarity. This is
the standard one-dimensional phase-twist/Leggett functional, derived here
for the actual single-rotor fiber. Cauchy-Schwarz gives f<=1; positivity on
the compact circle gives f>0 for every finite smooth lock.

Using (3)-(6) gives the exact interpolation

    1/B_eff=f/B_0+(1-f)/B,
    B_eff/B=1/[1+(R-1)f], R=B/B_0.                    (7)

For no lock f=1 and B_eff=B_0, even if the formal geometric gain is huge.
The ideal constrained value B requires the periodic flux dispersion to
be suppressed to order1/R. Merely small local angle fluctuations or a
finite normal-mode gap is not that condition. A finite-order harmonic
expansion loses the winding effect altogether.

## 4. A rigorous necessary barrier law for ANY finite periodic lock

Shift the minimum of V to0 and let U_bar=max V. The zero-flux ground
energy lies in[0,U_bar]. Put a=psi_0'/psi_0, a smooth periodic function.
At each maximum or minimum of a, its Riccati equation gives

    a^2=(V-epsilon(0))/E_R<=U_bar/E_R.

Thus |a|<=sqrt(U_bar/E_R) everywhere. The shorter arc between the maximum
and minimum of psi_0 has length at most pi, so

    max psi_0/min psi_0<=exp(pi sqrt(U_bar/E_R)),
    f>=exp(-2pi sqrt(U_bar/E_R)).                     (8)

To obtain a fixed fraction c in(0,1) of the ideal inertia, (7) requires
f<=(1-c)/(c(R-1)). Therefore every such periodic potential obeys

    U_bar >= E_R/(4pi^2)
             log_+^2[c(R-1)/(1-c)].                   (9)

This is a finite canonical theorem, not a WKB estimate. A fixed finite
barrier and bounded E_R^-1 cannot produce arbitrarily large low-band
inertial amplification. For fixed B_0,I and g->infinity, E_R grows as g^2;
indeed U_bar/E_R->0 for fixed U_bar. The normalized ground state tends
uniformly to the free rotor, f->1, and B_eff->B_0. Geometry alone then
LOSES its supposed low-energy gain rather than approaching an inerter.

The last limit follows directly from regular perturbation of the isolated
free-rotor eigenvalue at dimensionless potential norm U_bar/E_R->0. No
large-angular-momentum tail or two-level projection is postulated.

## 5. A scaling-optimal explicit passive lock: exact, no Mathieu asymptotics

There is also a constructive sufficient family at the SAME barrier order.
For b>0 choose the positive two-harmonic potential

    V_b(psi)=E_R[b^2 sin^2 psi+b(1-cos psi)]
            =E_R[(b^2/2)(1-cos2psi)+b(1-cos psi)].      (10)

Its exact ground state and energy at zero flux are

    psi_b=exp(b cos psi)/sqrt(2pi I_0(2b)),
    epsilon_b(0)=E_R b,                               (11)

as direct substitution shows. The positive no-node eigenfunction is the
ground state. Its complete phase stiffness is therefore

    f_b=I_0(2b)^-2.                                  (12)

For b>=1, the interval |psi|<=1/sqrt(b), with
cos psi>=1-psi^2/2, gives

    exp(2b-1)/(pi sqrt b)<=I_0(2b)<=exp(2b),
    exp(-4b)<=f_b<=pi^2 e^2 b exp(-4b).               (13)

Also0<=V_b<=E_R(b^2+2b). For any fixed epsilon>0 take
b=(1/4+epsilon)log R when R is large. Then (R-1)f_b->0,

    B_eff/B ->1,
    U_bar=O(E_R log^2 R).                              (14)

Together (9),(14) prove that E_R log^2 R is the OPTIMAL ORDER of a bounded
periodic locking barrier for near-ideal ground-band inertial amplification.
No semiclassical bandwidth formula, fitted Kerr spectrum or numerical
flattening result is needed. This is the actual positive construction,
not merely an obstruction to a cosine guess.

## 6. What the resources become in a cold-contact application

The already proved harmonic response envelope requires participating
relative inertia of order1/theta for a fixed deficit at fixed port motion
and bounded translating mass. This is a TARGET for an implementation,
not an automatic heat theorem for (1). If B is chosen of that order and
c is fixed, (9) gives two distinct ways of paying for the target:

* At fixed finite I and radius, g^2 is order1/theta, the pitch shrinks as
  sqrt(theta), E_R is order1/theta, and the lock barrier must be at least
  order theta^-1 log^2(1/theta). The family (10) attains that barrier order.
* At fixed g, one can instead grow I as1/theta. With fixed rotor mass its
  radius must grow at least as theta^-1/2. E_R then tends to a positive
  constant, while the necessary/sufficient barrier order is log^2(1/theta).

The second option is an equally informed ordinary large-flywheel alternative;
it moves the resource into extent rather than deleting it. Compound gear
trains can move costs into element count, mass, stiffness and contact
preparation. This single-stage theorem is not a universal lower bound on
every topology or a claim that the first option is an optimal apparatus.

A literal finite lever with bounded angular travel instead pays macroscopic
length and its complete bending/longitudinal spectrum. Hard stops or a
topologically fixed no-slip constraint change the configuration space and
are NOT refuted by the periodic-lock theorem. Their finite material/contact
realization remains another physical resource to acquire.

## 7. Force, material, preparation and coupling bandwidth are not free

In (1), the maximum terminal locking force is g||V'|| and its curvature
is g^2||V''||. A C^2 periodic potential obeys

    U_bar<=pi||V'||,
    U_bar<=(pi^2/2)||V''||.

Hence (9) also gives necessary force/stiffness capacities. For fixed I and
large g they grow at least as g^3 log^2 g and g^4 log^2 g respectively,
up to the fixed dimensional constants. The explicit construction (10)
has ||V_b'||<=E_R(b^2+b), ||V_b''||<=E_R(2b^2+b), so it pays those same
orders. A fixed finite force/stiffness interface does not realize the
arbitrarily large compact gain.

If the entire locking barrier is stored in a LINEAR elastic active volume
with modulus E, density rho, maximum allowed strain e_max and mass m_act,
its declared elastic-energy budget is at most E e_max^2 m_act/(2rho).
Using that as a finite U_bar cap makes (9) an explicit gain limit. Neither
mass nor E/rho ALONE supplies this cap without a strain/feature/material
model. Magnetic, chemical or hard-contact barriers need their own actual
energy and geometry accounting; they are not covered by that elastic formula.

The design (10) has exact positive reference ground energy E_R b with the
potential minimum set to0. At fixed g and P=0, an ideal adiabatic ramp from
V=0 to V_b stores that amount of normal-sector energy. This is not a
per-use heat debit or a lower bound on every assembly process. Preparing
the low band, its entangled helical phase profile and an actual momentum
window has nonzero apparatus/time/error requirements. A large gap above
the finite lead band does not let those leads cool that mode for free.

The full rotor-plus-terminal-plus-leads Hamiltonian is defined without a
truncation, but we have NOT yet bounded its low-frequency open response
uniformly under the heat-operating retuning. Band curvature alone does
not prove its heat deficit, its total Y covariance, finite reset time or
absence of other material modes. Those are the next physical gates, not
assumptions hidden inside the word 'inerter'.

## 8. Conventional ancestry and why it matters here

Smith2002 introduced the ungrounded two-terminal inerter with stored
relative kinetic energy, using rack/pinion/gears and a flywheel. Its
finite travel, neglected gear masses and large internal motion are explicit
modeling boundaries. That is the strongest classical operation comparator,
not a newly named component. Source:
https://www-control.eng.cam.ac.uk/foswiki/pub/Main/MalcolmSmith/cued_control_859.pdf .

Koch et al., arXiv:cond-mat/0703002v2, SecIIA-B Eqs2.1-2.7 and the rotor
discussion, is a direct primary for the same periodic quantum rotor,
flux sensitivity and winding/phase-slip physics. I read those governing
pages directly. The paper explicitly explains why any finite-order local
harmonic expansion misses the compact-boundary charge dispersion. Its
cosine/WKB asymptotic is not needed to prove (9)-(14). Source:
https://arxiv.org/pdf/cond-mat/0703002 . The phase-stiffness functional (6)
is conventional one-dimensional twist physics; no novelty claim attaches
to the formula or to the canonical rotor. The owned consequence is the
explicit, scaling-optimal locking-resource construction for the proposed
compact mechanical response escape, with its open-contact gate retained.
