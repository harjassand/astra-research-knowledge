# Force contrast to current-contact cooperative permission

29 October 2026. Independent construction; no apparatus, material qualification,
growth experiment or practical advantage is claimed. Mechanical logic,
magnetic docking, signal-passing assembly and proofreading are established.
Priority of this particular compiler is UNKNOWN.

## 1. Actual input contract

A recognition contact exerts generalized force on sensor stroke q=ell*x.
Warrant throughout the ENTIRE stroke and admitted pose, including backaction
and bounded disturbances: an intended contact has F/F0>=g, an unintended
contact has F/F0<=b, and all forces lie in [fmin,fmax], where 0<=b<g.
Forces may depend on x and time. One calibration gap does not warrant this.
Other faces, remote parts, friction and permission-linkage loads are included.

There is a separate CONTACT-OWNERSHIP interlock: a channel admits a new owner
only after reset; while permission can pass, the partner and admitted pose are
fixed; withdrawal removes permission BEFORE partner/pose can change. This is
break-before-make and reset-before-new-owner. Pins, sliders and blocking bolts
are possible implementations, not an acquired apparatus. Section 4 proves
that force discrimination alone does not supply this interface.

## 2. Explicit finite-time force discriminator

Set c=(g+b)/2, e=(g-b)/3, beta=c/e, E0=e*F0*ell, and use spring potential

U_s(x)=E0*(x^4/4-x^2/2+beta*x).

With drag zeta*dq/dt the force balance is
zeta*ell^2*dx/dt=E0*(h+x-x^3), h=(F/F0-c)/e.
Dimensionless time s=t*E0/(zeta*ell^2). For constant force the total potential
is U_s-F*ell*x; for x-dependent force use the differential force balance.
Good contacts have h>=3/2, bad contacts h<=-3/2. With no contact h=-beta<=-3/2,
so the bit resets instead of retaining a match indefinitely.

Choose integer X>=1 with X^3-X>=max(|(fmin-c)/e|,|(fmax-c)/e|).
The interval [-X,X] is forward invariant, even for measurable adversarial
forces in the bands. On [-X,1], x^3-x has maximum 2/(3*sqrt(3))<2/5.
Thus good force reaches x=1 from any initial state within

tau=10*(X+1)/11

dimensionless time: velocity before crossing is >=3/2-2/5=11/10. Reflection
gives the same time to x=-1 under bad/no contact. Once good, x>=1 is invariant;
once bad, x<=-1 is invariant. A bad contact admitted from x<=-1 NEVER qualifies.
The time bound is completeness, not a hidden timer: x=1 clears a blocking
slider, and x=-1 admits a new owner. Actual clearances and linkage loads remain
fabrication/force-contract requirements.

## 3. Self-timed cooperative compiler

Each of two designated inputs has four protocol states:

* RESET: permission blocked; no owner; admission blocked until x<=-1.
* DOCKED: one partner held in an admitted pose; permission blocked until x>=1.
* QUALIFIED: x>=1; same owner and pose; permission can pass.
* WITHDRAWING: permission blocked BEFORE owner/pose change; no-contact reset
  to x<=-1, then RESET.

A series blocking mechanism requires both sliders to clear before a commitment
bolt travels. This specifies its kinematic contract, not its acquired friction,
latch work, load capacity or manufacturability. There is no threshold on a sum
of magnetic scores. Contacts can arrive at different times, but both current
owners must remain present and locked at commitment.

Theorem: under Sections 1-2 and the ownership contract, every commitment has
two CURRENT intended contacts. Two intended contacts that remain owned both
qualify within tau after the later admission, unless another linkage blocks.
The statement holds for all force histories in the bands, without independence.

Proof: each owner begins at x<=-1; a bad owner's left half-line is invariant,
so it never qualifies. Withdrawal order excludes stale qualifications. Both
permissions are required for commitment. The latency is Section 2. QED.

For seeded directed growth, additionally mask output permission until a part
commits, initialize only the seed as verified, and require two verified
neighbors at commitment. Induction on commit events gives a proof DAG rooted
at the seed; unseeded blanks cannot activate themselves. This is ordinary
signal-passing growth semantics, not a physical implementation of masking or
a new universality result. Glue alphabet, seed/program information, species,
feedstock, available sites, transport and orientation remain explicit resources.
Arbitrary shapes and self-reproduction do not follow.

## 4. Finite-history failure without ownership

Reset bias is insufficient. Take two sensors x'=h+x-x^3, initially both -1.
Alternate with period p=1/100000: first half h1=3,h2=-3/2; second half swap.
There are NEVER two good inputs, yet both sliders exceed 1 at s=6.

Proof without floating simulation: both sensors stay in [-2,2]. Mean drive is
3/4. Let y'=3/4+y-y^3,y(0)=-1. On [-1,11/10] velocity is >=3/4-2/5=7/20,
so y(6)>=11/10; the upper endpoint cannot be crossed downward. The zero-mean
forcing primitive Pi has |Pi|<=a=9p/8=9/800000. Set zi=xi-Pi. Nonlinearity
f=x-x^3 has global one-sided Lipschitz constant 1. On segments from zi to xi,
|f'|<12 because |xi|<=2 and a<1/100. Scalar comparison gives

|zi-y|<=12*a*(exp(s)-1).

At s=6 an integer number of periods gives Pi=0. Since exp(6)<3^6=729,
xi(6)>=11/10-12*(9/800000)*728>1. The elementary exp(1)<3 follows from the
Taylor series/geometric tail. All remaining bounds are rational.
Fast switching is not claimed to occur in the experiment. This refutes a
GENERAL transfer omitting contact history/ownership. A warranted bandwidth
or slew limit could replace an interlock; it is another acquired input.

## 5. The calibrated soft-face input remains conditional

Nisser et al. arXiv:2208.03799v1 demonstrate coded soft-magnetic cube faces
and fit weaker repulsion with a 0.09 FORCE factor. In a same-overlap surrogate,
attractive force at raw correlation k is 0.455+0.545*k. At k=0 a wrong face
still attracts. One mate plus three such faces scores 2.365 versus two mates'
2: a monotone scalar-force threshold cannot implement the desired rule. This
is neither a bond-energy calculation nor an actual multi-face capture counter.

Per-face discrimination could use the raw wrong-correlation ceiling 0.36:
the surrogate upper is 0.6512, below a unit mate. An ILLUSTRATIVE additional
full-stroke error budget 0.05 gives g=0.95,b=0.7012. The consumer compiles these
numbers, not an acquired force profile. The experiment's one-gap calibration
does NOT establish all-stroke/pose/dynamic bounds, reset/ownership or masking.
No assembly accuracy follows from this example.

## 6. Full normal-force transfer for fixed hard-dipole faces

Two parallel faces carry fixed normal point dipoles s_i*m on square-grid
sites of pitch l, s_i in{0,+1,-1}, w active sites. As in root's separately
owned energy bridge use C=mu0/(4pi), with the facing-normal sign absorbed.
For lateral separation r and plane gap h,

E_pair=C*m^2*s_i*t_j*(r^2-2*h^2)/(r^2+h^2)^(5/2).

The normal attractive force (positive toward decreasing h) is its h derivative:

F_pair=3*C*m^2*s_i*t_j*h*(2*h^2-3*r^2)/(r^2+h^2)^(7/2).

Aligned equal GLOBAL moments give 6*C*m^2/h^4. Differentiation is essential:
an energy error bound need not bound its force derivative. For noncoincident
grid pairs, |F_pair|<=9*C*m^2*h/r^5. A max-norm shell j has 8j points at
r>=j*l; sum j^-4<=1+1/16+integral_2^infty x^-4 dx=53/48<10/9. Therefore
the total absolute fringe force divided by F_peak(h)=6*C*w*m^2/h^4 is at most
(40/3)*(h/l)^5. Finite apertures only remove terms from this absolute bound.

If admitted small pose error moves EVERY pixel by <=a*h, with a<=1/4, the
nonzero grid separations shrink by at most factor 1-a*h/l. Thus

epsF=(40/3)*(h/l)^5/(1-a*h/l)^5.

A formerly coincident pair has relative force
fF(u)=(1-3*u^2/2)/(1+u^2)^(7/2), u<=a. Bernoulli gives
1-5*a^2<=fF(u)<=1. General signed codes can lose cancellation under rotation;
a safe per-face score error is E=5*a^2+epsF. Intended registered overlap 1
and wrong signed correlation <=rho therefore give good force >=F_peak*(1-E)
and bad force <=F_peak*(rho+E), using ALL pair interactions.

For sensor stroke h/h0 in[1-s,1+s], evaluate epsF at h/l=(1+s)*h0/l and
require |delta_i|<=a*h throughout. In units F0=F_peak(h0), uniform bands are

g=(1+s)^(-4)*(1-E),  b=(1-s)^(-4)*(rho+E).

If g>b>=0 these feed Section 2 directly. The consumer uses rational
rho=9/25,a=1/20,h0/l=1/10,s=1/100 and proves positive contrast. This is an
ALL-PATTERN theorem conditioned on fixed moments, grid-code correlation and
pose promises, not an acquired palette or tolerance. It does not fit the soft
material in Section 5. Other faces, remote bodies, tilt and constitutive errors
need separate force budgets. Root's energy bridge is credited for the model;
the derivative/full-stroke force bound here is independently derived.

If the sensor moves the actual plane gap by q=ell*x, its stroke promise also
requires X*ell<=s*h0. A wider stroke cannot silently be used to raise E0.

## 7. Resources, noise and consequence

The operation needs a biased quartic spring over stroke 2*X*ell, warranted
drag zeta, two clearances, contact ownership, series permission, and an output
mask/latch. Good/reset latency is <=tau*zeta*ell^2/E0. Without ell,zeta and a
force profile this is not seconds. Increasing ell increases stored/dissipated
energy and the required uniform force interval simultaneously. Friction,
recocking, magnetic separation, transport and output-latch work are charged.
For a time-varying force parameter in the constant-force potential model,
|x|<=X gives external work <=X*ell*total_variation(F) in absolute value.
This is not a free energy source or a full work bound for x-dependent fields.

If each of M verification/ownership episodes violates its entire contract
with conditional probability <=delta, any invalid commitment has probability
<=M*delta by union bound. M includes failed encounters, collisions and resets;
final product size cannot replace M. No Gaussian effective temperature,
independent errors or unlimited lifetime follows from a fluid-agitated source.
A process-level delta and M, rather than a mean force, are acquisition costs.

An equally informed MCU/Hall/force-sensor controller can use the identical
per-face classification, ownership handshake and permission logic. No hardware
cost advantage over that controller is proved. The result changes a MODEL
operation: quantified force contrast can be compiled into self-timed local
two-contact permission, and the indispensable history interface is exposed.
It does not yet change what a manufacturing system can demonstrably do.

## 8. Main replacement: a JOINT commitment coordinate

Replace two separately remembered recognition bits by ONE physical commitment
coordinate driven only by TWO designated input faces. Their approach
coordinates share q1=q2=ell*x, so generalized work is (F1+F2)*ell*dx. Output
faces transfer loads to the frame, not this coordinate. This mechanical role
separation is an additional design contract, not a consequence of coded faces.
Friction, lever losses, other loads and field errors belong in the force bands.
The coordinate itself advances the two-contact capture mechanism; it is not
a readout whose later signal addresses a separately delayed latch.

Legal means two intended inputs; illegal means at most one. Absence has zero
force and counts as bad. Put L=2*g, I=fmax+b, G=L-I. If G>0 choose
c2=(L+I)/2,e2=G/3,beta2=c2/e2,E2=e2*F0*ell. The same biased quartic spring gives

dx/ds=((F1+F2)/F0-c2)/e2+x-x^3, s=t*E2/(zeta*ell^2).

Legal loading gives drive >=3/2; illegal loading gives drive <=-3/2.
Choose X with X^3-X>=max(|(2*fmin-c2)/e2|,|(2*fmax-c2)/e2|).
Then [-X,X] is invariant and any continuously legal pair reaches x=1 from
any state in dimensionless time <=10*(X+1)/11.

NO-STALE-TRIGGER THEOREM. On ANY interval of illegal loading, x<=1 is forward
invariant, independent of earlier history. Earlier correct encounters which
did not complete therefore cannot combine with later incorrect encounters to
finish. This includes arbitrarily fast alternation of the two one-match
arrangements. At x=1 illegal velocity is <=-3/2. With continuous force near a
first upward crossing of x=1, drive there must be nonnegative; hence such a
crossing cannot have an illegal pair. This is a dynamical barrier from an
explicit potential, not a freely granted force-threshold oracle or timer.

The coordinate x itself completes commitment at its geometric engagement
position. An additional delayed actuator would need a current-contact guard.
Discontinuous collision models must specify the ordering of a contact change
exactly coincident with crossing. After commitment, ordinary ownership of the
formed bond and a specified release/reset remain necessary. Replacing a
partner inside a closed latch is not defined as a new assembly event.
Inputs must remain in admitted registered poses through the stroke, or their
force bands must hold over ALL accessible poses. Neither capture/registration
nor this joint mechanism is supplied by the existing magnetic source.

For the illustrative soft-face bands g=.95,b=.7012,fmax=1.05,fmin=-.14,
L=1.9,I=1.7512,G=.1488>0,e2=.0496 and X=4 suffices. Latency <=50/11.
Section 6 supplies another conditional hard-dipole family with a larger gap.
If four faces all load the coordinate, Section 5's obstruction returns.
Mechanically isolating two input roles avoids it. Directed input/output tile
semantics are established; this construction pays a force-to-commit link and
its history barrier, not a new universality principle or acquired apparatus.

## 9. Finite inertia is a decisive additional interface

The exact current-loading theorem uses an OVERDAMPED first-order coordinate.
The experiment does not acquire that sensor law. A nonzero-mass second-order
replacement need not preserve its barrier: if x<1 and velocity v>0 under
previously legal force, switch to illegal loading just before crossing. On a
compact local state/force region, acceleration has a finite absolute bound A.
For switching distance d<v^2/(2*A), x crosses 1 before stopping. A sufficiently
fast CONTINUOUS force change preserves this with reduced margin. Making an
oscillator 'highly damped' therefore does not supply an exact instantaneous
current-contact theorem for arbitrary histories. Force-band calibration alone
does not acquire the necessary contact/kinetic condition.

An exact example is x(0)=99/100,v(0)=1,x''=h+x-x^3,h=-3/2. On
x in[99/100,101/100], acceleration is in[-2,0]. At t=1/50,
x(t)>=99/100+t-t^2=1.0096, unless it crossed earlier. Velocity remains
positive until crossing. The consumer checks these rational bounds. This is
not asserted as a state observed in the apparatus; it refutes a general
first-order-to-inertial transfer.

A real design must acquire a finite-bandwidth contact law, kinetic/clearance
receiver, or direct mechanical owner/pose interlock. The joint coordinate
reduces stale-bit requirements but does not eliminate physical capture and
timing. Agitation can inject kinetic energy and must be included, rather than
named an effective temperature without a process model. This is the hardest
unpaid manufacturing interface in this route.

## 10. Equally informed ordinary operation: preloaded LINEAR spring

The quartic is unnecessary. For the SAME gap G=L-I>0, engagement travel ell,
choose preload P=(I+G/3)*F0 and spring k=G*F0/(3*ell). A linear spring
compressed by d0=P/k, with reset stop q=0, has approach law

zeta*dq/dt=F1+F2-P-k*q, 0<=q<=ell.

Legal loading advances at speed >=G*F0/(3*zeta); illegal loading has velocity
<=-G*F0/(3*zeta) at all q>=0. Engagement takes <=3*zeta*ell/(G*F0). The SAME
no-stale-trigger barrier holds without nonlinear spring or classifier bits.
The stop is an explicit component. Added spring energy over the stroke is
(I+G/2)*F0*ell. PRELOADED energy is P^2/(2*k), equivalently
3*(I+G/3)^2*F0*ell/(2*G); precompression d0/ell=3*I/G+1. Stiffness, energy,
friction and reset are charged. A nominal F0=.16N,ell=5um yields a finite
illustrative spring spec, not a qualified material or full-stroke force.

The ordinary linear operation dominates the quartic proposal at this scope:
same input/pose/isolation/first-order premises, simpler device. Finite inertia
defeats exact current-contact transfer in the same way as Section 9. The
surviving result is a general compiler and missing-physics contract, not a new
assembly principle or demonstrated manufacturing advantage.

The sharper worst-case write time is (zeta/k)*log(2): at the weakest legal
force the equilibrium is 2*ell, so q=2*ell*(1-exp(-k*t/zeta)). Under the
strongest illegal force the equilibrium is -ell; resetting from ell to 0
takes the SAME time. Scalar comparison covers all histories in those bands.
A symmetric magnetic gap interval h/h0 in[1-s,1+s] allows linear engagement
stroke ell<=2*s*h0, rather than the larger quartic stroke requirement.

For nominal per-face bounds g0,b0,fmax0 and independent-sign adversarial force
error <=nu*F0 on EACH input, the robust gap is
G=2*g0-fmax0-b0-4*nu. Thus the soft surrogate's nominal gap .3488 permits
nu<.0872; the .05 compilation is a force-error budget, not a measured noise
level. Pose/model/backaction errors consume that SAME budget rather than
separate free allowances. This finite-noise statement requires no IID model.
