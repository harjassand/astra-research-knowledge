# Exact fault-event admission under a fixed local controller

29 October 2026. This package gives an exact noise-conversion operation and
a separate obstruction to an unrepaired clock compiler. It does **not**
establish the missing charged-error memory theorem for the programme's
nominal thermal controller.

## 1. What is fixed and what is unknown

Let the system have finite-dimensional local cells. A catalogue of allowed
error supports has bounded diameter, bounded cardinality and bounded
incidence, all independent of system size. A support can be enlarged to a
known containing cell block; no unknown generator need be estimated. The
nominal local controller, any additional noise deliberately engineered below,
the input encoder and the final receiver are selected before the error.

For the explicit Pauli construction, a catalogue block X contains q_X qubits,
d_X=2^{q_X}, and an unknown time-independent Hermitian term H_X has
||H_X|| <= e_X. Its identity coefficient is immaterial. Additional local
unitary-jump noise can have arbitrary unknown nonnegative rates, with a
specified local total-rate budget. In particular those rates need not obey
detailed balance with any stabilizer Hamiltonian. Such noise is unital;
that fact must not be confused with thermal balance.

Every assertion about an autonomous memory below is conditional on an
explicit **physical-time** fault-event threshold of that controller. Neither
a synchronous threshold, nor a positive average update velocity, supplies
that premise.

## 2. Completing the square: exact coherent-to-unitary-jump admission

Write D_L(rho)=L rho L^dagger-{L^dagger L,rho}/2. For a Hermitian Pauli P,
real h and a positive number l, put

    J=l P+i h I,       r=l+h^2/l,
    U=J/sqrt(l^2+h^2).

Then J^dagger J=(l^2+h^2)I and U is unitary. Literal expansion gives

    (1/l) D_J = l(Ad_P-id)-i h[P,.]
              = r(Ad_U-id).                                  (1)

This is the standard Lindblad gauge freedom in a useful normalization.
There is no weak-noise expansion in (1). Adding it to any other generator,
whether commuting with it or not, gives exactly the same complete
generator and hence the same semigroup on every input and for every time.

Expand H_X=sum_{P!=I} h_{X,P}P. Pauli orthogonality gives

    sum_P h_{X,P}^2 = Tr[(H_X-Tr(H_X)I/d_X)^2]/d_X <= e_X^2.

Before H_X is known, engineer the **fixed** ballast

    B_X=l_X sum_{P!=I}(Ad_P-id).

Then B_X-i[H_X,.] is a sum of unitary-jump generators on X, of total rate

    r_X=(d_X^2-1)l_X+sum_P h_{X,P}^2/l_X
       <=(d_X^2-1)l_X+e_X^2/l_X.                            (2)

The optimal common l_X for this bound is e_X/sqrt(d_X^2-1), giving
r_X <= 2sqrt(d_X^2-1)e_X. If all supplied e_X are rational, the convenient
rational l_X=e_X/d_X gives r_X < 2d_X e_X. Blocks with e_X=0 need no ballast.
The first minimax constant is exact **within this Pauli completion
strategy**. For unequal ballast rates l_P, the adversary can take
H=e_X P at a minimum-rate Pauli. Its rate is sum_P l_P+e_X^2/min_P l_P,
minimized by the equal choice above. This is not an optimality statement
over all physical randomization or control mechanisms.

The physical device implements B_X, not the unknown U in (1). The latter is
only an exact representation of its actual unknown perturbed generator.
No estimation, adaptive cancellation, external timing, syndrome measurement,
retained record, infinitely fast dephasing or reset of a newly introduced
register is used by this conversion. The price is a deliberately increased
local noise rate. It can be very unfavorable when q_X is large.

That physical change is essential. A pure nontrivial Hamiltonian generator
cannot be written r(Phi-id) with finite r and Phi CPTP. In an eigenbasis,
two unequal eigenvalues E_a,E_b give a principal 2-by-2 Choi minor of
Phi=id-i[H,.]/r equal to -(E_a-E_b)^2/r^2<0. The successful conversion is
not simply a new unraveling of the unmodified coherent dynamics.

If a site x belongs to several catalogue blocks, the correct admitted local
fault budget is the sum over those blocks, for example

    p_loc <= max_x sum_{X containing x}
             [(d_X^2-1)l_X+e_X^2/l_X+nu_X],                (3)

where nu_X pays the additional unknown unitary-jump rates. A global
sum of all rates is not a size-independent local threshold parameter.
Overlap and noncommutation do not change the exact generator identity.

### Conditional consequence

Suppose a particular fixed controller and encoder/receiver have an all-input
memory estimate f(n,t,p) for **every** local unitary-jump perturbation in the
support catalogue with local intensity <=p. Then that same estimate applies
to the controller plus the fixed ballast above under every unknown H_X
satisfying the supplied bounds and additional unitary-jump noise whenever
(3)<=p. It follows by equality of generators; there is no t||Delta L|| term.

This consequence is a genuine admission reduction, not a new autonomous
threshold theorem. In particular this package does not replace the unknown
physical-time threshold by the synchronous QCA statement of a prior paper.

## 3. Arbitrary local Markovian errors: CPTP event admission

The unnormalized Choi convention is

    J(E)=sum_ab |a><b| tensor E(|a><b|).

For the completely depolarizing channel T(rho)=Tr(rho)I/d,
J(T)=I_{d^2}/d. Let E be any local Hermiticity-preserving, trace-annihilating
linear map with ||J(E)|| <= k/d. Then

    Phi=T+E/k                                               (4)

is CPTP, since its Choi matrix is positive and its output partial trace is I.
Consequently

    k(T-id)+E = k(Phi-id)                                   (5)

exactly. This works even for signed perturbations of nominal jump terms,
provided the actual full generator is physical. E need not separately be
a Lindblad generator. It is local, and so is Phi.

A directly usable sufficient bound for

    E=-i[H,.]+sum_j D_{L_j}

is ||J(E)|| <=2d(||H||+sum_j||L_j||^2). Indeed the Hamiltonian Choi matrix
is the difference of |H>><<I| and its adjoint, while a dissipator has Choi
|L>><<L| minus the two half anticommutator rank-one matrices. Use
||I||_F=sqrt(d), ||H||_F<=sqrt(d)||H||, and similarly for L and L^dagger L.
Thus the fixed choice

    k=2d^2(e+g),   ||H||<=e,   sum_j||L_j||^2<=g             (6)

suffices. A sharper acquired local Choi bound can replace (6), but is not
needed for the unknown-error theorem. The support-size factor is paid.

Equation (5) is a state-independent rate-k Poisson process of arbitrary
CPTP fault events. The maps can be unknown; their construction or oracle
access is not needed by the nominal controller. Conditional event maps may
be realized by fresh local Stinespring environments for analysis. This is
not a claim that their Kraus-resolved records have state-independent rates.
Only the trace-preserving coarse event has that property.

### Open-class normal form and the remaining threshold target

Fix any family L0_n, encoders Enc_n and receivers Dec_n and a bounded
support catalogue. Suppose the family has a specified all-input memory
bound for **every** local CPTP-event perturbation

    sum_X k_X(Phi_X-id),
    max_v sum_{X containing v} k_X <=p0,                    (7)

with arbitrary unknown Phi_X. Choose fixed k_X before the unknown error
so that sum k_X satisfies (7), and define

    Lnom_n=L0_n+sum_X k_X(T_X-id).

For every local trace-annihilating Hermiticity-preserving E_X satisfying
||J(E_X)||<=k_X/d_X, the actual generator Lnom_n+sum E_X obeys exactly the
same memory bound, with the same Enc_n and Dec_n. This follows from (4)--(5)
and does not assume that E_X preserves any Gibbs state, syndrome block or
logical module. It admits unknown nonunital error and even small signed
changes of a nominal jump term. The complete positivity needed for the
actual dynamics follows from its displayed CPTP-event representation.

Conversely each local CPTP event of intensity k has
||J(k(Phi-id))||<=2dk, since both Choi matrices have positive trace d.
Thus a genuine threshold against all sufficiently small local generator
perturbations necessarily includes a CPTP-event threshold. Up to this
fixed, paid depolarizing change of controller and support-dimension
constants, **rare arbitrary local CPTP events are a sufficient and
necessary test class for this Markovian robustness question**.

This is an exact normal-form reduction, not a syndrome Markov reduction.
The state conditioned on a fault-event history remains fully quantum and
can have arbitrary syndrome coherences. Only the coarse event labels are
Poisson. A proof for sector-separable Pauli processes cannot therefore be
substituted for (7). The reduction says where the restoring-history work
must be done; it does not claim that the original nominal thermal
controller or a raw autonomous clock already satisfies (7).

### Exact class boundary

For an amplitude-damping generator E=g D_{|0><1|},
E(I)=g Z !=0. Adding any fixed unital ballast preserves this nonzero value.
Every sum of unitary-jump generators annihilates I. Therefore no unital
ballast can convert this error into a unitary-jump generator. The CPTP
events in (5) cannot be silently admitted to a theorem stated only for
unitary jumps.

This obstruction is also stable under the choice of a fixed nonunital
ballast: it cannot cancel E(I) for an entire class containing both zero
and a nonzero amplitude-damping generator. A nonunital fault threshold is
an actual further resource, not a choice of unraveling.

### Strong ordinary extension to every unital local error

Watrous's 2009 mixed-unitary theorem supplies a further exact admission
when E(I)=0. Let a>=d||J(E)||, so Phi_1=T+E/a is a unital channel by (4).
For d>=2, put p=1/(d^2-1). The theorem makes

    Phi=p Phi_1+(1-p)T =T+E/[a(d^2-1)]

mixed unitary. Thus with the **fixed** padding k=a(d^2-1), equation (5)
is a finite mixture of unitary Poisson jumps. A supplied upper bound on
||J(E)|| suffices to select a; the unknown error need not be acquired.
This covers arbitrary sufficiently bounded **unital** local generator
perturbations at an explicit, usually much worse, rate than the Pauli
Hamiltonian construction. Watrous's theorem is the controlling ordinary
result, rather than a new claim about mixed-unitary channels. Nonunital
errors remain excluded by the preceding exact obstruction.

## 4. Physical resources and what this changes

For q-qubit X, B_X is exactly d^2 l_X(T_X-id), since the full Pauli average
is T_X. One may specify it either as d^2-1 local unitary noise channels or
as one bounded-support depolarizing event. Its local support and rate are
fixed before the error; the number of terms per block and the required
constant local dimension are explicit. No thermal equilibrium or detailed
balance is imposed. An instrument realizing these engineered generators
and its own local errors remain physical acquisition obligations.

The new useful division is:

* Unknown energy-changing coherent terms can be admitted exactly into an
  already acquired unitary-event robustness theorem by paying a fixed
  local noise budget. Coherent cancellation between correction events is
  not then the central obstruction.
* Fully arbitrary unbalanced (including nonunital) Markovian terms can be
  admitted into an acquired **CPTP-event** theorem by Choi padding.
* Neither conversion constructs restoring histories. The companion clock
  theorem proves that a natural finite-state autonomization compiler can
  fail even for arbitrarily weak allowed reset faults.

No output here assumes the perturbed Gibbs state is stationary, uses a
finite-order Zeno effective rate, or adds a perfect-measurement fallback.

## 5. Ordinary antecedents and present disposition

The generator identity is an application of established Lindblad gauge
freedom; see Albert--Bradlyn--Fraas--Jiang, *Geometry and Response of
Lindbladians*, PRX6,041031 (2016), Appendix A Eq(A4).
Depolarizing channel interiors, Choi positivity, Poisson channel semigroups
and the deliberate use of additional noise are ordinary mathematical
tools. Duer--Hein--Cirac--Briegel, PRA72,052326 (2005), already studies
standardizing noise by randomization and increasing decoherence. Watrous,
QIC9,406--413 (2009), proves a mixed-unitary ball around the depolarizing
channel in the unital affine space. No new general identity, CP-ball,
randomization principle or world-priority claim is made.

Dünnweber--Styliaris--Trivedi2601.20818v1 is the strongest directly relevant
autonomous comparator acquired here. Its discrete-time local fault-path
model is stronger than Pauli noise. Its Section IV instead states local
unitary Poisson jumps. Section V explicitly leaves general nonunitary
Lindblad perturbations open. Equations(1)--(3) are useful at the literal
unitary-event boundary, but their continuous-time successful-update
admission still needs a size-uniform restoring-history argument. Lake
2510.08056v2 Sections IV.2.2--IV.2.3 explicitly distinguishes a positive
computation velocity from fault tolerance and pays reliable polylog-sized
classical registers in its proved threshold. Those promises are not our
fixed bounded-local noisy-controller theorem.

The charged autonomous memory target is **NOT_ACHIEVED** in this package.
The exact noise-admission primitive is complete and reusable; the clock
obstruction is a real negative result for its stated architecture. The
remaining worthwhile question is a fault-contained clock/history repair
mechanism with a full physical-time threshold, not a better finite-order
coherent-rate approximation.
