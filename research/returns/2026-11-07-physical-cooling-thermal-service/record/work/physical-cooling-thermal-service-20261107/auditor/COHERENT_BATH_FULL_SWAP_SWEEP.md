# Full-swap cooling rounds with a retained coherent bath

Constructive challenge and proof, 7 November 2026. This is a follow-up to the
immutable independent initial `../initial/auditor.md`. After that initial was
frozen, I read the principal's frozen initial and exchanged the finite-depth
Stinespring/pull-through proposal with the principal. This note audits and closes
that proposal **at the explicit local-noise and fresh-token hypotheses below**.
It does not claim a reusable finite-bath reset theorem.

## 1. Formal input and conclusion

Let the augmented DATA stabilizer family have n qubits, distance d_n>=delta*n,
and a nonnegative commuting integer syndrome energy U=sum_v u_v. Every u_v has
bounded body, norm and incidence. Let D_E bound the sum of norms of terms touching
one DATA qubit. A w-supported DATA operator changes energy support by at most
D_E*w. For every syndrome with U<u_c*n, fix once a canonical Pauli E_sigma of
weight at most C0*U(sigma). The physical frame is

    W(|psi>_L tensor |sigma>_G)=E_sigma Enc|psi>.

Assume at least kappa*U strictly decreasing labels at each such syndrome, from an
O(n) catalog of bounded-support Paulis with bounded full read-support incidence.
Every lowering step changes integer U by at least one. Let D bound the absolute
energy change of a catalog move. Take u_c small enough that

    2*C0*u_c<delta

with fixed slack. This is the established two-sector low-energy repair contract;
global soundness alone is not substituted for it.

There are fixed positive constants a,q_eff,c_anc,c_reset and a constant-duration
finite-depth physical cooling round, using fresh qubit modes of gaps in
{J,2J,...,JD}, such that the following holds. Let u_s<u_c satisfy the strict
canonical-distance margins in Section 5. Define P_s=1_(U<=u_s*n). Let the complete
actual round, retaining the same old perturbation bath B and optionally all
outgoing ancillas A_out, be Gamma. Suppose its integrated local perturbation and
fresh-reset errors have a support-counting expansion with budget mu*n as derived
in Section 4. If alpha>0 satisfies

    D_E*q_eff*alpha<a*u_s,
    C0*(2-a)*u_s+q_eff*alpha<delta,
    e*mu<alpha,

then Gamma on the **entire** P_s logical/gauge/bath module has a CP/TNI comparison

    id_L tensor C: (G_s,B) -> (G_s,B,A_out)

with complete error at most 2*delta_round, where

    delta_round=sum_(r>floor(alpha*n)) (mu*n)^r/r!
       <=[(e*mu*n)/(floor(alpha*n)+1)]^(floor(alpha*n)+1)
             /(1-mu*n/(floor(alpha*n)+2)).                (1)

The right side decays exponentially for fixed e*mu<alpha. This is a comparison
of maps with the **same actual accessible bath**, not a replacement bath state.
All logical/gauge/bath/reference correlations are allowed. The CP/TNI output is
again P_s-supported, so the comparison composes for K rounds with error bounded
by 2*K*delta_round before the conservative logical lost-mass conversion.

The actual physical round has no projection, decoder or artificial reinitialization
of DATA. P_s and the CP/TNI comparison are proof devices. It uses finite-duration
driven local collisions and replenished finite-temperature modes. It is powered
measurement-free correction, not an autonomous passive Hamiltonian memory.

## 2. Exact ground collision and deterministic energy contraction

For a Hermitian catalog Pauli P_a and positive energy change d, put

    B_(a,d)=P_a Pi_(a,-d).

B is the *lowering* partial isometry. Thus B^dagger=P_a Pi_(a,+d),
[JU,B]=-Jd B, B^dagger B=Pi_(a,-d), and BB^dagger=Pi_(a,+d). Let a fresh ancilla
have H_a=Jd |1><1| and set

    V_(a,d)=B tensor |1><0|+B^dagger tensor |0><1|.

It is Hermitian and commutes with H_0=JU+sum_a H_a. At angle pi/2 the ancilla |0>
branch sends every lowering-source syndrome to its lowered partner and leaves
every other syndrome unchanged. Its reduced DATA channel has Kraus operators

    K0=I-Pi_(a,-d),       K1=-i B.

The full isometry retains the branch label in the outgoing ancilla. Phases can
depend on syndrome and are retained in the gauge map. No logical phase is dropped.

Color the graph of **full** update/read neighborhoods; its degree is uniformly
bounded. Each color is a set of disjoint neighborhoods. Apply a pi/2 exchange to
all modules in each color, then move to the next color. The number of colors is a
fixed constant. All ancillas are distinct. This defines a constant-depth unitary
W0 on DATA and all round ancillas; the abstract reference initializes them in |0>.
This ground initialization is an analytical comparison, not a physical zero-
temperature resource claimed for the actual implementation.

Let R0 bound the number of lowering predicates whose value can change when one
catalog move is applied. It is a fixed constant from bounded read incidence. Mark
the >=kappa*U_start labels active at the beginning of a sweep. Every marked label
either performs a lowering step when visited, or has been invalidated by an
earlier successful move. Charge the latter to the first such move. Each successful
move is charged at most R0 invalidations and its own successful visit. If S is the
number of successes, then

    kappa*U_start<=(R0+1)*S.

No ground collision raises energy. Therefore, with

    a=min(1/2,kappa/(R0+1)),       theta=1-a,

the deterministic final syndrome f(sigma) obeys

    U(f(sigma))<=theta*U(sigma).                            (2)

This is a statement about every syndrome, not an averaged drift. At the completed
ground sweep, the full isometry maps each syndrome to one final syndrome plus
outgoing ancilla labels. On arbitrary coherent input it extends linearly, retaining
all syndrome off-diagonals.

Throughout the ideal ground trajectory, every DATA energy component is at most
U_start: a partial exchange only superposes the original energy with a lower one.
For neighboring source/target syndromes, canonical neutrality follows from

    wt(E_tau^dagger P_a E_sigma)
       <=C0*U(tau)+C0*U(sigma)+wt(P_a)<d_n.

The zero-syndrome Pauli in this inequality is a stabilizer up to a scalar. Hence
every ideal ground partial/full collision acts as identity on L on the full safe
module, including arbitrary ancilla/bath/reference coefficients. The isometry
W0 initialized in ground ancillas therefore has the form

    W0 W_in = (id_L tensor w0) W_in                        (3)

in the canonical output frame, and its DATA output energy is at most theta times
its input energy. The possibly O(n) total number of corrections does not create
a hidden logical Pauli: neutrality is established at every local transition.

## 3. Finite temperature and exact finite cones

The actual fresh ancilla state is its Gibbs state at fixed beta>0,

    tau_d=(1-q_d)|0><0|+q_d|1><1|,
    q_d=(1+exp(beta Jd))^(-1)<=exp(-beta J).

An excited input ancilla is the local input operation X_a on the ideal ground
ancilla. Exactly,

    Prep_tau=Prep_0+q_d(Ad_X-id) Prep_0.                   (4)

The difference has diamond norm at most 2*q_d and is supported on one ancilla.
The independent product of the actual thermal inputs has a coefficient-counting
expansion obtained by multiplying (4). No positivity of the signed difference is
asserted; the complete actual preparation is CPTP.

The ideal unitary includes its actual finite collision durations and H_0. Every
exchange V_(a,d) commutes with H_0, so the free H_0 evolution can be moved to one
end of the ideal circuit. Since the terms of JU commute, conjugating a local
operator by exp(-itJU) involves only the energy terms that originally failed to
commute with it. Terms commuting with that operator continue to commute after
all these conjugations because the Hamiltonian terms commute with each other.
Thus the propagated support is contained in the union of the finitely many
originally incident energy-term supports, independently of t. Ancilla free phases
do not spread support.

Combining this bounded enlargement with the fixed circuit depth gives a uniform
q_eff: every q-local operator on DATA/round ancillas, pulled through any ideal
suffix, has DATA support at most q_eff. Its ancilla support is also bounded. This
includes all projector/read neighborhoods and all physical pulse cones. It is
false for a generic noncommuting always-on Hamiltonian without an additional
Lieb-Robinson/tail analysis. Exact resonance and the commuting H_0 are load-bearing.
Small mismatch is allowed only as part of the charged perturbation budget.

## 4. Arbitrary retained-bath errors: complete signed expansion

Retain one actual bath B. Its bath-only propagators are the actual normal CPTP
maps and need not be inverted. Between physical reset/collision operations let
the actual joint generator equal the ideal system control plus the actual
bath-only generator plus normal HP local terms N_Z(t), supported on at most q
DATA/active-ancilla cells and arbitrary B. Require

    N_Z^*(I)=0,
    integral_round sum_Z ||N_Z^*(t)||_cb dt<=mu_cont*n.

The complete actual evolution is CPTP with the requisite common-domain and
integrability properties. Bounded finite GKSL or Hamiltonian models satisfy this
directly. This is a local **full joint** norm premise; small reduced DATA error is
not a substitute. No fixed bath-partner graph or bath/gauge product state is used.

Fresh-reset implementation errors, when included, are local HP map differences
Delta_j with complete norms epsilon_j, with support on the actual reset cell and
any explicitly retained B. They must compare the **full map on all future-accessed
degrees of freedom**, not just reset marginals. A fresh no-return reservoir reset
provides a channel on that cell extended by identity on old B; Merkli's fixed-size
result can bound this channel after the new outgoing reservoir is physically
excluded from future accesses. A reused bath needs its own joint theorem.

Add bounded local calibration errors, clock/switching errors and waiting noise to
these actual budgets. Uniform small coherent calibration is allowed; an
occasional n-body global clock failure needs its own all-subset/tail law and is
not made local by calling the clock classical.

Let

    mu=mu_cont+(1/n)sum_j epsilon_j
               +(2/n)sum_(thermal ancillas a) q_(d_a)
               +other declared local signed budgets.      (5)

For O(n) ancillas/resets and fixed local imperfections this is a fixed constant.
The coefficientwise product of all discrete differences and the continuous
Duhamel series is bounded by exp(z*mu*n). Therefore the total order-r part
Gamma_r has

    ||Gamma_r||_diamond<=(mu*n)^r/r!.                      (6)

These norms include B and arbitrary inert references. A thermal-input difference
counts as one local insertion; a local reset difference counts as one; a
Liouvillian insertion has local DATA/ancilla legs on both bra and ket. The
necessary finite local Pauli expansion does not introduce an uncharged bath
Kraus-coefficient sum: the complete norm controls the coefficient map, while
the Pauli expansion is used only to prove exact support and factorization.

Push ideal *system/ancilla* unitaries to the right of each error insertion, using
their suffix conjugations. Bath-only maps commute with these unitaries and remain
complete contractions in their original order. A term with r insertions is a
linear combination of system/ancilla left/right operators acting after W0 whose
DATA support is at most q_eff*r on each leg. This is the same algebraic operation
as in the established finite-pulse proof, now using the full collision
Stinespring rather than a purported inverse of a cooling channel. No bath map,
cooling channel or nonunitary reduced update is inverted.

## 5. Operator support and full logical factorization of every low order

Take arbitrary input operator matrix units in the full canonical module
L tensor G_s tensor B, including off-diagonal sigma/sigma' and arbitrary bath
coefficients. Append ideal ground ancillas in the reference expansion. By (2)-(3)
the ideal ground isometry has DATA energy at most theta*u_s*n and is identity on
L on every such matrix unit.

For r<=m=floor(alpha*n), every Pauli coefficient of an output error leg has weight
w<=q_eff*r, and its output energy support is at most

    theta*u_s*n+D_E*q_eff*r<=u_s*n.                       (7)

This proves a **spectral support inclusion** on both bra and ket, hence on
arbitrary coherent inputs. It does not infer coherent correctability from a
classical probability distribution. If eta is the output syndrome and f(sigma)
the corresponding ideal ground-sweep output syndrome, then

    wt(E_eta^dagger P E_f(sigma))
       <=C0*u_s*n+C0*theta*u_s*n+q_eff*r<d_n.             (8)

It has zero syndrome and is therefore a stabilizer up to scalar. Consequently
each such Pauli coefficient acts identically on L. Ancilla and bath coefficients
are untouched by this statement and can be arbitrary, correlated and coherent.
Equation (8) establishes the full input/output module factorization

    Gamma_<=m=id_L tensor C_signed,                       (9)

with output supported by P_s. This is strictly stronger than testing one encoded
state or one gauge sector. C_signed need not be positive. No claim of its
positivity is made.

The subtle possibility of an actual trajectory leaving a basin and returning is
irrelevant to this low-order **algebraic** proof: the whole imperfect history is
equivalent to a bounded-support output error after a logically neutral ground
sweep. The high-order histories are charged by the tail (1). We have not used an
unjustified projected drift observable during partial collisions.

## 6. Positive repair on the same environment

Work in the fixed canonical frames, with P_s=I_L tensor P_(G_s). Restrict the input
module to G_s. Set

    C(theta)=Tr_L[P_s Gamma(I_L/d_L tensor theta)P_s].      (10)

Gamma is the actual CPTP round, with the actual B and actual outgoing ancillas.
Thus C is CP/TNI, maps to G_s and keeps that same B. Applying the complete
contractions in (10) to (9) and using ||Gamma-Gamma_<=m||<=delta_round gives

    ||C-C_signed||_diamond<=delta_round,
    ||Gamma-id_L tensor C||_diamond<=2*delta_round.        (11)

The discarded comparison trace is positive and controlled by these same errors.
For an arbitrary correlated input rho_LGBR, its initial LR marginal minus the
id_L tensor C output marginal is positive: write the effect
I-C^*(I)>=0 and sandwich rho by its square root before tracing GB. Thus comparison
trace loss is not normalized away and introduces no hidden postselection bias.

The output is again in the exact same hard-support module. Composition of the
CP/TNI comparisons uses only complete contractions. K actual rounds are within
2*K*delta_round in complete norm of id_L tensor C_K...C_1. The conservative
half-trace logical preservation bound is at most 2*K*delta_round after including
the positive lost mass. This statement holds uniformly with a reference and for
the actual admitted writer state; immediate decoded writer error and actual
physical READ error add separately as in the capital.

## 7. Admission, gates, resets, clocks and resource consequences

**Admission.** The round theorem requires a positive hard-supported admitted
input at U<=u_s*n. It does not turn a first moment into that promise. The earlier
supported noisy writer yields a positive rare-bad-branch decomposition by choosing
its supported-fault cutoff to make D_E*b_W*zeta_W<u_s. If admission is instead
given by a coherent exponential-energy tail, the actual complete clipping loss
must be paid (in general a square root). Any initial warmer state can be treated
with a larger input threshold and the same inequalities
theta*u_in+D_E*q_eff*alpha<u_out<u_c; repeated rounds with a strict margin reduce
it to u_s. Logical accuracy of WRITE is independently required: the wrong logical
state can have zero energy.

**Gates.** A supplied bounded-depth code-preserving physical gate has the earlier
full input-correction/suffix-spread proof. Choose its input energy, output energy,
support tail and constant signed budget with strict margins, then follow by a
fixed number of cooling rounds. A selected CCZ family remains selected CCZ; this
does not establish a universal gate set or noisy bare I/O. The existing encoded
staging port theorem can be attached only at its exact isolated stochastic and
classical-processing premises. No new common-bath quantum-I/O threshold is claimed.

**Refresh.** The simplest fully finite model for a finite requested horizon is a
product thermal tape, with each finite-gap token used once and then permanently
excluded from future coupling. Ancillas can be physically reset by swapping with
fresh tape cells. The initial state of a noninteracting tape Hamiltonian is a
product Gibbs state. Its independence from the incoming logical payload/old B is
an explicit resource premise. Small local supply/clock errors are charged in
(5); correlated marginals alone are insufficient. A fresh reservoir thermalizer
can replace the tape only after its complete local reset/no-return contract is
established, and its input-cell waiting noise is charged. Nothing here proves
that a finite recycled bath stays fresh indefinitely.

**Timing.** Each full swap takes finite time pi/(2*g) at fixed finite coupling g.
The graph coloring gives a constant number of layers, hence constant round time,
at the charged bounded-incidence connectivity. The nominal H_0 remains on. All
resets, switches, calibration errors and idles belong in the budget. A bounded
fractional calibration error contributes a fixed integrated amount; shortening
the pulse is not an argument that it vanishes. A missed local module can be a
local fault. A single noisy global enable bit changing O(n) modules is not covered
unless it is protected or its all-subset/tail bound is proved.

**Costs and comparator.** Each round uses O(n) collision operations and fresh
thermal/reset opportunities, with possibly enormous fixed body, degree, control,
temperature and threshold constants. K rounds cost O(n*K) total control/reset
locations and bath throughput. A finite precharged tape uses O(n*K) physical
qubits; a replenished source may have O(n) active cells, but the source, flow,
factory work and discarded entropy are charged. Net heat cannot be read from the
number of operations; actual energy conservation and external work must be used.
Bounded degree is not a bounded-density 3D hardware layout. A matched active or
autonomous computer receives the same local controls, reset streams, protected
ports, routing and clocks. No complete-resource advantage has been demonstrated.

## 8. Audit verdict and limits

**PASS as a mathematical theorem at the premises in Sections 1-4.** The full
Stinespring pull-through closes the logical-basin issue without requiring
projections at intermediate times, a positive sparse decomposition of coherent
common-bath noise, or exponentially accurate global approximation of an ideal
Davies evolution. The only Markov approximation that may be used is an optional
fixed-size local reset estimate, whose complete no-return applicability must be
proved separately. Exact finite thermal tokens require no Markov approximation.

**Not established here:** a small-body/Euclidean implementation of the supplied
DATA code and full energy-read couplers; economical numerical constants; an
unbounded bosonic perturbation satisfying a bounded full-joint norm premise; a
single finite recyclable refrigerator; generic common-bath quantum-I/O; arbitrary
noisy bare endpoints; universal processing from selected CCZ; full-cost advantage;
experimental validation or historical priority. These limits do not negate the
proved finite-temperature/noisy finite-round capability at its explicit model.
