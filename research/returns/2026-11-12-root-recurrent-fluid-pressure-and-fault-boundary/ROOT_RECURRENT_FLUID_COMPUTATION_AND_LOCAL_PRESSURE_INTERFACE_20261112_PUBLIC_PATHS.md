Recurrent fluid computation and the missing local architecture

1. Scope and accepted input

The complete streaming return P2_STREAMING_UI_COPIED_FULL_FINAL_20261112.md
constructs the full issued finite-horizon compiler relative to the accepted
quantitative backend. Its new source-insertion propagator bounds hold on
both L2 and H1. In a directional filter the live-source L2 error tends to
zero with the hold length while its H1 envelope is independent of that
length; a separately chosen genuinely unforced smoothing tail, still with
input present, closes the H1 endpoint. Natural cubic and final-readout
windows have explicit decaying source errors. Actual-input routing,
two-frequency storage and exact clock composition therefore now apply to
live input. Only the complete final is available here; expanded activity
and helper contents are unavailable and are not silently imported.

The following consequences use these accepted uniform actual-input
services. They are deductions with the imported backend as a premise.
No linked proof archive
or held original is opened.

2. Infinite duration is not automatically a new scientific problem

Fix a finite code capacity q and a finite recurrent Boolean update
circuit C. Suppose the actual incoming magnetic register is in a small
neighborhood of a Boolean corner. A known nonzero mean carrier H1=1
is an explicit subcase of the accepted input class. It removes a parity
restriction on logical polynomials: replace a monomial v^alpha by
v^alpha H1^e, where e in{0,1} makes its total degree odd. On H1=1 its
value is unchanged. Velocity readouts are made even by the analogous
one-carrier parity lift. The physical mean is not observed or created.
If the compiler normalizes by M, H1=M*h1 and the known factor M is
charged in its coefficient envelope.

For Boolean values 0,1 use AND(x,y)=xy, NOT(x)=1-x and the restoring
polynomial R(x)=3x^2-2x^3. On a radius-r neighborhood of either bit,
|R(x)-bit|<=3r^2+2r^3 and |R'(x)|<=6r(1+r).
For a two-input AND, raw logical error is <=2r+r^2<=3r. With
r=1/64, restoring the raw gate gives error at most
9r^2(3+6r)<r/2. NOT has raw error r and a stronger bound.
Fresh physical errors and carrier errors can be chosen below a fixed
fraction of the remaining margin. The physical router returns a fresh
absolute H1 endpoint error relative to the ACTUAL incoming features;
this is the reason historical microscopic gains are not multiplied.

Refresh all live registers often enough inside the finite update circuit
that every physical input is in its fixed code neighborhood. The number
of services and their precision are polynomial in the circuit size and
q. They are independent of how many times this SAME update circuit is
later repeated. With an explicit visibility gamma, all raw code values
and H1 norms have polynomial envelopes in q,gamma^-1 and the code band.
There is no promise of q order-one normalized Fourier coordinates in an
H1 ball too small to contain them.

Use one fixed physical period, with the live input acting throughout.
The known temporal features for that period are actual integrals of
unknown measurable port amplitudes. A finite input-bit promise must
include a fixed distance from a decision boundary. A fixed polynomial
approximation to a Boolean decision on the two promised intervals,
followed by restoration, has constant degree at a fixed decision margin.
Its input contribution during gates is covered by the earned live
service; it is not deleted or called small rough noise.

For every fixed capacity/circuit there is consequently a positive
disturbance budget eta_C and a fixed repeatable force word. At each
period endpoint the logical corner is the correct recurrent update and
the actual state is back in a common H1 neighborhood. The same local
quantitative guarantees apply on every next period for all admitted
coefficient histories. Induction supplies arbitrary-duration strong
continuation and, with the same actual forcing and disturbances,
weak--strong uniqueness on the concatenated intervals. The tolerance
eta_C, code band and per-period force do not shrink with the number of
periods. Work over J periods is at most J times the common per-period
bound, and the emitted waveform can be a finite periodic description.

This is externally clocked, fixed-capacity recurrent computation. It
does not imply a capacity-independent physical noise threshold or a
fixed spatial resolution. Its force, band and eta_C^-1 may all grow
polynomially in q. It does not prove stability under unbounded thermal
kicks. Indefinite repetition at this actual scope follows from the displayed
restoration and uniform actual-input contracts.

A related corollary holds for a supplied contractive state update
F:[-1,1]^q x input ->[-1,1]^q with Lipschitz constant <=1-kappa in the
state argument. Per-step logical error <=delta gives
E_j<= (1-kappa)^j E_0+delta/kappa. A margin in the state cube and
delta<=epsilon*kappa/4 make the physical budget independent of duration.
This composes an EXPLICIT supplied finite update; qualitative fading-
memory universality does not provide a polynomial-size approximation to
an arbitrary unknown filter or acquire its coefficients.

3. A uniform-in-volume pressure estimate for a possible local layout

Consider the physical three-torus of side L, L=a*M, with cells separated
by a fixed spacing a. Write B=H+b with constant H. For incompressible
fields the pressure generated by the nonlinear term satisfies
-Delta p=partial_i partial_j(u_i u_j-b_i b_j), up to a convention on sign.
The terms linear in constant H vanish after the double divergence since
div b=0. Let G_L be the mean-zero periodic Green function. The pressure
GRADIENT uses three derivatives of G_L, not the two derivatives of the
Leray projector applied to an arbitrary force.

Away from zero,
|D^3 G_L(x)|<=C[dist_L(x,0)^(-4)+L^(-4)].
Indeed, the Euclidean singularity is C/|x|; its third derivatives have
order |x|^-4. The remainder is smooth on the unit torus away from zero,
and G_L(x)=L^-1 G_1(x/L) gives the stated L^-4 remainder.

Suppose a stress S_j is supported in a fixed-size active region in each
cell, with ||S_j||L1<=E, and active regions in different cells are
separated by spacing a>=4 times their diameter. At a point in one active
region, the pressure gradient from all OTHER cells is at most
C E a^-4 sum_(j!=0)|j|^-4 + C E M^3 L^-4 <= C' E a^-4.
The lattice sum converges in dimension3: the r-th shell has O(r^2)
sites and sum r^2/r^4 is finite. The periodic remainder is
M^3/L^4=1/(a^4 M)<=a^-4. These constants are independent of M.
Integrating over a fixed physical gate duration retains a constant
per-cell bound. This estimate applies to the stated actual stress norm
assumption; it does not derive that norm or prove a local gate.

There is a genuine distinction for naive force cutoffs. Leray projection
of a general compact force uses D^2G_L, of order |x|^-3; its absolute
lattice sum grows logarithmically with M. Localize a vector potential
and take curl instead of simply multiplying a solenoidal force by a
cutoff if a divergence-free compact force is needed. This avoids that
particular artificial long-range forcing tail. It does not eliminate
the actual pressure coupling or supply a shield around the fluid.

Uniformly local L1 stress bounds can also be used with a partition of
unity in place of exactly disjoint stresses. The near-cell contribution
must be treated by local energy and smoothing, not by evaluating a
singular kernel at zero. Diffusion and induction leakage, buffer renewal,
and propagation of arbitrary off-code errors remain physical work.

4. What is missing for a scalable material processor

A spatial lattice of fixed-size codelets, driven by ONE fixed spatially
periodic and temporally periodic ordinary force, could in principle
implement a fixed universal cellular update. Programme and data would
be initial local magnetic states, not a computation-dependent force
script. The alphabet, local gate truth table, clock period, particle/
field resolution, noise tolerance and force per physical volume would
all be fixed BEFORE capacity and duration grow. Larger devices would
pay more volume and total energy, rather than narrower pulses or
smaller error budgets at every site.

The accepted global Fourier compiler does not yet provide this. It
reuses a capacity-dependent common code bank, changes its geometry as
capacity grows and has no size-independent local actuator theorem.
Its twelve fundamental modes on a unit torus cannot simply be declared
to act independently inside every subvolume. A localization argument
must build genuine neighboring-cell transfer, renew its buffers, pay
nonlinear pressure/induction leakage and prove a uniform local basin
of attraction under rough disturbances. The estimate in3 removes one
naive volume divergence but leaves all of those central operations.

Fixed-capacity copying, arithmetic, live source handling and restoration
are actual starting capital. A bounded-degree universal cellular rule
has a constant-size local Boolean truth circuit; its ideal restoration
margin can therefore be fixed once. The physical challenge is realizing
that SAME local rule in the full coupled field at every site and every
cycle with fixed local resources. No differentially programmed local
actuator, magnetic gate, ideal wall, position measurement or independent
cell simulator is supplied.

The deterministic bounded-disturbance target is distinct from a thermal
fault-tolerance theorem with rare unbounded kicks. A later thermal claim
would have to pay the probability of logical failure through duration J,
the resulting spatial redundancy, and energy/noise statistics. Robust
code neighborhoods alone do not establish that stronger claim.

5. A full obstruction to an overly strong local fault contract

There is a universal obstruction if one adds arbitrary coherent bounded
body-force errors while requiring a capacity-independent local energy
bound forever in a connected unanchored fluid. This gives a full negative for that precise conjunction.

Normalize Fourier coefficients by volume. For wavevector
k=(0,2pi/L,0), a spatially a-periodic prescribed drive has no coefficient
at k when M>1. Put h_u=A e1 sin(2pi x2/L), h_B=0, with a positive A
small enough that its L2 norm in every cell is below any proposed fixed
local tolerance. It is mean-zero and divergence-free. If the proposed
uniform local H1 bound is C_*, then the normalized velocity coefficient
is bounded by a constant C and each normalized stress coefficient by
C^2, uniformly in L. Its forced real quadrature obeys
 d U_k/dt >= A/2-C|k|C^2-C nu_+ |k|^2.
For sufficiently large L the right side is >=A/4. Integrating contradicts
the asserted bound on U_k after time O(C/A). The same argument applies
to a coherent additive magnetic body error through its curl-form
nonlinearity. It uses momentum/flux balance and finite energy density,
not failure of one control or one spatial cutoff.

Thus a scalable physical fault model must account for momentum/flux
sources, supports and noise statistics. It cannot include arbitrary
macroscopic coherent forcing for free while asserting bounded energy
density. This is a full negative for that precise conjunction, not for
the completed unit-volume compiler, centered local thermal-like noise,
a supported material, or scalable computation generally.

In particular, a physically meaningful next question can use independent
local Poisson fault clocks with conditionally centered bounded
solenoidal kicks. They supply a fixed positive local noise floor and
arbitrarily severe finite clusters, but not the forbidden persistent
macroscopic drift. Correctness must then be probabilistic over all
events through the requested duration; one finite unprotected memory
cannot promise no thermal fault forever. Redundancy, seed preparation,
all rare-path energy/work and failure probability are charged. A native
continuum threshold under those conditions is NOT a consequence of the
fixed-capacity deterministic corollary in2 or the pressure bound in3.

6. Primary comparisons actually read

Grigoryeva--Ortega1712.00754v1 Theorems4.3/4.7 and Corollary4.5 give
qualitative universal approximation of fading-memory filters by specified
state-affine/reservoir families. They do not provide an efficient general
filter-acquisition algorithm or this local continuum implementation.
https://arxiv.org/pdf/1712.00754v1

Vakulenko1511.02047v1 Definition3.1/Theorem3.2 and Sections2--4 construct
finite-dimensional vector-field realization for a two-dimensional
Marangoni/heat-source model by a tailored spectral gap and attracting
manifold. The heat source, domain/Prandtl parameters and model differ;
orbital hyperbolic realization is not a uniform resource, timed-I/O or
rough-fault local MHD theorem.
https://arxiv.org/pdf/1511.02047v1

The earlier actually read Cardona2111.03559v1 retains its finite-tape
steady-Euler orbit scope and construction-specific severe costs.
The newer2508.11990v2 reader failed on the first governing follow-up;
only its exposed introduction was seen and no governing learning result
is imported here. No held source, linked proof or alternate recovery is
used by the deductions above.
