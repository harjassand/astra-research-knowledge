# Reconstruction of the autonomous sweep memory argument

16 October 2026, Australia Brisbane. This reconstruction separates deductions
from the two published probability imports. Its conclusion is an internal
mathematical assessment; external correctness and historical priority require
separate scrutiny. The initial saved proof is pinned in SOURCE_SNAPSHOT.json.

## Exact mathematical target

For some fixed integer b and positive epsilon, A, c, and all sufficiently large
M, put L=bM and n=6L^4. The 4D cubical toric code has six logical qubits. Encode
an arbitrary logical density operator, with any external reference, in its exact
code space. On each primal and dual vertex run the specified rate-kappa sweep:
if all incoming syndrome edges are absent, pair the nonempty even set of
outgoing edges in a fixed order and toggle its one or two positively based
faces. Otherwise do nothing. Use syndrome-conditioned Pauli Lindblad jumps for
these actions and independent single-face Pauli births at rates lambda_P.

When max(lambda_X+lambda_Y,lambda_Z+lambda_Y) <= epsilon*kappa, the target is one
fixed ideal final recovery Dec_L satisfying, simultaneously for all T>=0,

    || Dec_L exp(T L_total) Enc_L - Id ||_diamond
       <= min(2, A L^4 (1+kappa*T) exp(-c*L)).

All rates, supports and Hilbert space dimensions per cell are fixed independently
of L. The quantifier is a compatible family L=bM. The decoder and perfect code
initialization are supplied mathematical operations. Auxiliary envelopes and
time slabs are analytical variables, absent from the storage device.

## 1 Quantum reduction

For every physical Pauli label E and any code-reference state rho_0, write
rho_E=(P_E tensor I) rho_0 (P_E^dagger tensor I). A joint stabilizer function
f(S) has a scalar value f(s_E) on both sides of rho_E. Therefore for J=Q f(S),
where Q is a fixed Pauli string,

    D[J](rho_E)=|f(s_E)|^2 (rho_(E+Q)-rho_E).

The finite classical forward equation on Pauli labels, with these rates, gives
an exact solution of the quantum master equation for every rho_0. Uniqueness
of the finite-dimensional equation proves equality. The rates do not depend
on logical amplitudes or the reference. Linear dependence of the rho_E is
irrelevant to constructing this solution.

For the canonical generator, seven mutually exclusive active patterns per
vertex give a rate-kappa proposal clock with null proposals allowed. A Y mark
changes both CSS labels simultaneously. Each marginal sector has independent
face proposals at its summed rate, but the sector processes are correlated.

If decoded residual labels on a set of histories are stabilizers, the recovered
channel on that set is exactly Id. For the complementary probability q, the
channel is (1-q)Id+q*Psi for a Pauli channel Psi, hence its unhalved diamond
distance is at most 2q. This is uniform over references, rather than an inference
from fidelity for a few codewords. The classical bad-history estimate remains
an independent obligation.

## 2 Pathwise support domination

In either sector use an infected-vertex bit eta. At a common vertex clock v,
every right-hand side uses the pre-event state:

    eta'_v = eta_v AND (OR_i eta_(v-e_i)),
    eta'_(v+e_i+e_j) = eta_(v+e_i+e_j)
                      OR (eta_v AND eta_(v+e_i) AND eta_(v+e_j)).

A face birth sets its four corners to one. These are monotone maps. An incoming
syndrome edge supplies an occupied predecessor, so the envelope cannot remove
the physical vertex incorrectly. Without incoming edges, parity makes the
outgoing degree even and the complete sweep removes its incident defects.
Every new opposite corner of a written face has the three occupied old source
vertices used by the envelope. All other actual support persists in eta.
This proves eventwise inclusion for arbitrary continual fault histories.

Each tracked output can read at most 29 event/input pairs (35 is conservative).
One dependency step moves at most one fine infinity-norm unit. Reading only
old inputs forbids using the same clock mark twice in a zero-time cascade.

Healthy halfspaces x_i>=0 are invariant. The healthy halfspace sum_i x_i<=-b
is also invariant. Above the latter, a vertex becomes permanently healthy
after all four predecessors have permanently cleared and its next own ring.
The certificate DAG is finite for each target. Revealing independent vertex
Poisson streams in increasing height makes the residual services independent
Exp(kappa); these are certificate delays, not an assertion about actual
state-dependent clearance times. A directed path of H services has exponential
moment 2^H at kappa/2, and there are at most 4^H directed paths. This gives
a conservative clearance tail 2*8^H*exp(-kappa*t/2).

## 3 Uniform local forcing

Set s=1, C>10 log(8), R>=ceil(280 e C)+10 and Delta=Cb/kappa. Coarse cells
have side b. Healthy bits zeta indicate completely eta-free cells. Let A_i
be all coarse offsets of infinity norm <=R with ith coordinate >=0, and A_5
those with coordinate sum <=-1. Define

    phi(zeta)=OR_(j=1,...,5) AND_(a in A_j) zeta_a.

For a finite zero island of phi, the four coordinate maxima cannot increase,
whereas minimum coordinate sum increases by at least one each round. Finite
support is preserved, so the island disappears. This directly proves the
attractive-eroder hypothesis; isolated microscopic erosion alone would not.

Use one state-independent flag B for each target/slab, containing:

1. Any face proposal meeting the radius-(R+2) primitive guard.
2. Failure of the lower-height certificate by the slab endpoint, defined using
   only marks in the slab, with unfinished services assigned infinity.
3. Any strictly time-ordered m-clock dependency chain ending at a target at any
   time in the slab, m=floor(Rb/2).

Every flag uses only fresh primitives in a deterministic radius-(R+3) coarse
guard. The third flag excludes arbitrary exterior input and exterior births.
The first two ensure the forced halfspace configurations clear the target.
Thus a single good flag gives zeta_(z,n+1)>=phi(zeta_n shifted z) for ALL initial
configurations and exterior histories.

The marginal bound is

    delta <= 2b^4 exp((5 log(8)-C/2)b)
             + b^4 (35 kappa Delta)^m/m!
             + 6 sigma ((2R+5)b+3)^4 Delta.

Repeated clock locations are permitted in the middle term: the factorial
moment measure counts distinct ordered arrivals and supplies m!, without
requiring independent arrivals at different steps. The terminal time is
already arbitrary throughout the slab. The birth guard uses its full side
length; an older expression 6(2Rb+3)^4 is insufficient and is not used.

Fix C,R first, and hence phi, connectivity k=4R+4, and the dependence radius.
Choose a sufficiently small iid-death tolerance p_* from HT. Choose a primitive
delta_* from LSS for that fixed dependence radius. Increase the fixed b until
each clock term is <=delta_*/3, then take

    sigma/kappa <= delta_*/(18 C b ((2R+5)b+3)^4).

This is strictly positive and independent of L,T. The order avoids letting
the dependence range grow while invoking a fixed domination tolerance.

## 4 Precisely stated published imports

LSS, Domination by product measures, Annals of Probability 25 (1997), 71-95,
DOI 10.1214/aop/1024404279: for fixed finite dependence range on Z^d, bad fields
with sufficiently small uniform marginals are dominated by iid bad bits of
arbitrarily small prescribed density. Here disjoint guards generate independent
sigma fields, a stronger condition than pairwise independence. Slabs have
independent increments, so domination couplings can be chosen independently
between slabs. This is used on infinite space only.

HT, Kinetically constrained models out of equilibrium, arXiv:2212.08437v2,
Section 2.4 and Corollary 9.5: for every fixed positive Euclidean spacetime
connectivity radius and every attractive eroder, sufficiently rare iid deaths
give exponential diameter tails for the anchored zero component of the upper
invariant spacetime trajectory. Couple its initial state below all ones and
use identical future deaths. This yields inclusion of the ENTIRE cold zero
history in the stationary zero history; individual-time stochastic ordering
alone would not establish this path event.

HT is checked directly in the current source. Original full-text access to LSS
is separately tracked in clusters/; its named standard theorem is an explicit
import. Neither source is being credited with a periodic-boundary theorem.

## 5 Stopped finite torus replay

Run native B-driven theta from all ones on the coarse torus. Reveal zero
vertices in chronological layers and a fixed order within each layer. Stop at
the first insertion p producing a k-connected spacetime component of diameter
at least ell=M/128. Every previously existing component had diameter <ell and
meets p within k. The entire new component is therefore within ell+k of p.

A nonforced zero has a zero parent in EVERY DNF forcing set. Every such parent
lies in an older revealed layer within k, and hence in that same component.
Its necessary zero ancestry closes inside the component and ends at forced
deaths, since layer zero is healthy.

For EACH deterministic prospective anchor, copy all primitives from a fixed
spatial coordinate patch of radius ell+k+R+4 through its time layer; extend
independently elsewhere. For sufficiently large M this is injective and
preserves all offsets. The copied primitives have their unconditioned ordinary
product law. No conditional law at a random first anchor is used. Induction
replays the closed zero witness in infinite theta; additional outside zeros
only help. Infinite-space domination and HT bound the anchored witness, and
a union over N M^4 deterministic anchors gives

    P(first coarse escape through layer N) <= C_1 N M^4 exp(-c_1 M).

The diameter can safely be replaced by anchor-to-point distance ell/2, changing
only c_1. All-time torus stationarity is neither claimed nor needed.

## 6 Continuous times and historical homology

At any time in slab n, an occupied target on a good flag traces to an occupied
initial cell within coarse radius R. A bad flag forces theta_(z,n+1)=0 even
if its actual defect disappears before that endpoint. Thus the whole occupied
slab is covered by N_R({theta_n=0}) union {theta_(n+1)=0}.
Representatives of adjacent fine vertices are within Euclidean spacetime
distance <4R+4. A physical component of diameter L/32 forces a coarse component
of diameter at least M/32-2R-1>ell for sufficiently large M. This covers
transient defects and pre-jump limits.

Fill each syndrome component of diameter <rho=L/8 deterministically inside its
uniquely lifted coordinate box; use a fixed global fallback otherwise. For a
single physical event F in a unit cube, with every pre-event component smaller
than r=L/32, all affected old/new components and their fillings lie in a common
embedded box of side <=2r+1<rho. Unaffected fillings cancel. The closed chain

    F + D(s) + D(s+boundary(F))

is supported in that contractible box, hence is a stabilizer boundary. This
also covers splitting, merging, cancellation, and a bounded closed part of F.
Induction preserves [E+D(boundary(E))] for the ENTIRE accumulated error E;
vanished syndrome history is never discarded.

Take N=ceil(T/Delta)+1, union the two CSS bounds without assuming sector
independence, and multiply by two for diamond norm. Absorb fixed b,C and the
conversion M=L/b into A,c. This yields the exact target under the imports.

## What is indispensable

The code, sweep action, stabilizer algebra, LSS, HT and cubical chain contraction
are inherited mathematics. The model-specific contributions requiring external
review are the exact envelope, uniform primitive forcing with its parameter
order, fixed-anchor stopped replay, and whole-slab plus historical-homology
composition. A direct multi-Pauli trajectory calculation is necessary to avoid
invoking a narrower single-qubit theorem. Whether these contributions are
historically new is a literature question, not a consequence of this deduction.
