# Finite thermal cooling and robust warm quantum processing

Research dossier, 7 November 2026, Brisbane. Research only; no public release commissioned.

**Strongest result achieved.** At the supplied code/dense-descent hypotheses, finite thermal collisions and a direct fault expansion give exponentially reliable warm storage and compatible gate processing under fixed local imperfections, including coherent errors coupled to the same retained environment. The required local accuracy is fixed independently of code size and duration. No exponentially accurate global Markov simulation is needed.

This closes the proposed local-imperfection bridge for a specified powered architecture. It does not establish affordable scalable quantum computation or a new computational regime. The cooling schedule is measurement-free active correction; a matched active controller can run the identical operation. Useful constants, Euclidean geometry, a finite recyclable refrigerator, general noisy ports and full-cost advantage remain open.

The complete operation established below is a restricted hybrid service with encoded noisy input, isolated fault-tolerant staging, short noisy transfers, warm storage/compatible gates, physical encoded recovery and encoded output. Its staging assumptions remain explicit. The older exact microscopic three-body clock and its bath/noisy-loading contract remain distinct.

## Governing capital and proof dependencies

Use [the previous dossier](PROTECTED_QUANTUM_PROCESSING_RESEARCH_DOSSIER.md), SHA256 `b94faadf5e396a54566414b0889bb45286080a47512701f032795c8e10fb8c00`, and [the previous service theorem](../work/protected-quantum-processing-20261107/principal/THERMAL_SERVICE_THEOREM.md), SHA256 `bb4e12ae7cc82ed68f94d4b162f6c9a85e08671fd88b805a510ee47058666b40`. This dossier uses its audited two-sector local energy/global low-energy repair, fixed canonical full-module correctability, bounded-depth native gates, positive CP/TNI repair and restricted encoded-port construction at their exact scopes. It replaces the ideal whole-memory GKSL cooling primitive. It does not prove a new code family or retroactively change another thermal-memory model.

All local spectral projectors include their full read neighborhoods. Every future-accessed reset output must be retained or rigorously excluded. Incoming DATA/gauge/bath/reference correlations are allowed; unused future source blocks stay outside the arbitrary old bath until delivery. Bounded degree is not bounded-density three-dimensional geometry. Arbitrary unbounded bosonic memory couplings do not satisfy the complete local norm premise merely by being weak.

The complete essential proof is given next; subsequent sections supply sources, operation, costs, counterexamples and status.

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

with fixed slack. All statements hold for n>=n0, chosen so every fixed local-support term fits within that strict distance slack. This is the established two-sector low-energy repair contract;
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


## 8. Explicit finite thermal source, including its waiting Hamiltonian

For a target energy gap Delta>0, let two source spins have

    H_pair=Delta*(n_1+n_2)+h*(sigma_+ tensor sigma_-+
                              sigma_- tensor sigma_+),
    0<|h|<Delta.

The energies/eigenstates are 0 on |00>, 2Delta on |11>, and Delta±h on the two
single-excitation Bell states. For any fixed beta>0 take the actual Gibbs state

    omega_pair=exp(-beta H_pair)/Z,
    Z=1+2 exp(-beta Delta)cosh(beta h)+exp(-2beta Delta).

Every pair is stationary under its **nonzero** waiting interaction for every
delivery time. A bank with Hamiltonian sum_j H_pair,j has product Gibbs state
tensor_j omega_pair,j. Therefore distinct unused pairs remain independent of one
another and of the incoming payload/old memory bath, provided there is no other
coupling before delivery.

There is an exact positive decomposition

    omega_pair=(1-p_bad)|00><00|+p_bad omega_bad,
    p_bad=[2 exp(-beta Delta)cosh(beta h)+exp(-2beta Delta)]/Z
         <=3 exp[-beta*(Delta-|h|)].

The fresh-block bad flags are genuinely independent. They retain *all* token--
partner correlations inside omega_bad. This is better than asserting only a
thermal marginal. A preparation difference from the ground-pair reference has
diamond norm at most 2*p_bad and constant two-spin support, and can be inserted
directly in the full-swap round expansion. Choosing fixed h with |h|<=Delta/2 and
fixed sufficiently large beta*Delta makes this a small fixed local budget.

The delivered token marginal has excitation probability

    q_token=[exp(-2beta Delta)+exp(-beta Delta)cosh(beta h)]/Z.

It is not generally the uncoupled Gibbs state with gap Delta. That equality is
unnecessary for the direct cooling theorem, which only needs the small positive
fresh-block fault weight above. If an exact detailed-balance sampler were desired,
the difference would matter and could not be omitted.

To deliver, ramp h(t) to zero. All Hamiltonians Delta*N+h(t)V commute, so the
state remains exactly omega_pair during an arbitrary-duration ideal ramp. The
token and partner may remain correlated; keep the partner in the actual output
environment or exclude it permanently from future accesses. The decoupling work
for this equilibrium state is

    W_decouple=-h Tr(V omega_pair)
       =2h exp(-beta Delta)sinh(beta h)/Z>=0.

All routing, finite ramp duration, switching/control error, token temperature and
source spacing are paid. The bound is a **reserve/fuel** construction; it does not
recycle a spin or prove an indefinitely reusable refrigerator. K rounds use O(nK)
source spins and O(nK) delivery operations. For exponential K the entire finite
reserve is exponential in n, just as its total consumption time is exponential.
Peak O(n) active source space requires a replenished flow and charges that flow.

Fixed local preparation precision can also suffice: if independent prepared pair states obey ||tildeomega_j-omega_j||1<=epsilon_src, and each private waiting CPTP map fixes omega_j with all its waiting-environment outputs permanently excluded from future access, contractivity gives the same per-delivery error at every waiting time. Independent private waiting preserves the product source law, and the signed budget per pair is <=2p_bad+epsilon_src. If a waiting reservoir returns, reduced fixed-point invariance alone does not supply this joint bound; the full source law must be earned separately.

The initially proposed product tau_Delta tensor tau_Delta is also stationary,
because it is a function of N=n1+n2 and [N,V]=0. It is a valid explicitly prepared
state, but is not the interacting Gibbs state exp(-beta H_pair)/Z at h!=0. The
genuine Gibbs version above avoids that terminology issue.

**Load-bearing noise boundary.** Future source pairs must remain private until
delivery. The arbitrary old retained bath B in the memory theorem must not have
unbudgeted access to unused reserve pairs. Otherwise long waiting can correlate
the future tokens, and correct marginal temperatures do not prevent a common
logical fault. Additional nonequilibrium, cross-pair, calibration or bank noise
needs a delivered-block bound or an explicit fresh reset before delivery. A
private waiting channel that exactly fixes omega_pair can be allowed, but its
fixed-point property and independence have to be proved for the actual model.

This establishes a finite, interacting, genuinely thermal, stationary source at
its exact Hamiltonian/initial-state/isolation premises. It is not a robustness
theorem for every perturbation of an unmonitored thermal bank, a practical
refrigerator, or a favorable resource comparison.

There is one exact additional noise class: arbitrary fluctuations Delta(t)N+h(t)V leave the nominal omega_pair invariant because N and V commute. Even correlated classical amplitude fluctuations across pairs create no state correlations when every conditional evolution fixes every pair. Energy-changing or cross-pair errors are not covered by this observation. Thus this finite source is a fully specified restrictive model, not a universal refrigerator robustness claim.

## 9. Complete restricted input–processing–recovery operation

For the service accounting let K_tot=K_hold+k_entry+sum_g k_restore,g count EVERY cooling sweep, including admission and gate restoration. Core sweep formulas use K for any total number of sweeps; service error/time/resources use K_tot. Fixed restoring counts do not disappear from the ledger.

### 9.1 Primitives and the actual interfaces

Use the previously verified [encoded-port proof](../work/protected-quantum-processing-20261107/challenges/quantum_ports_closure.md) and [coherent decoder addendum](../work/protected-quantum-processing-20261107/challenges/quantum_ports_coherent_decoder_addendum.md). Their code and decoder are the same DATA code and canonical frame used above. No incompatible readout code is substituted.

The extra physical staging processor has independent circuit-stochastic noisy quantum gates, preparation, measurement and idle locations with parameter p below the specified threshold. It is isolated from the retained memory bath during its long circuits. Its classical computation is noiseless as in the imported CFG construction. Computational input/output ports are already encoded. Parallel matched short SWAP links connect staging to the original memory cells; the actual memory Hamiltonian, its noise and every switching/link error stay in the integrated local pulse budget. The memory bath stays on its original hardware throughout and may remain correlated with the payload after capture.

The service is the following actual sequence:

1. Receive an unknown encoded state, possibly entangled with an arbitrary reference and correlated with its computational gauge.
2. Run the fault-tolerant encoder E_n in isolated staging, then its physical output interfaces. The interfaces have a positive supported-fault mixture, not merely a small immediate decoded error.
3. Perform the short noisy parallel WRITE SWAP. Sparse interface faults plus low-order link faults put the payload into the fixed warm canonical module. Old memory/bath correlations remain auxiliary; no bath is silently replaced.
4. Apply entry cooling, then K finite cooling sweeps and G supplied bounded-depth code-preserving gates, each followed by the fixed restoring number of sweeps. All source deliveries and controls are charged.
5. At the chosen final capture cutoff, perform the short noisy capture SWAP into staging and turn the links off. Further memory-bath evolution is on the reference side of the isolated staging circuit.
6. Run the physical-to-computational interfaces and the fault-tolerant COHERENT promised recovery/unencoder D_n. Return an encoded quantum output, which can be consumed by further fault-tolerant processing.

The ordinary coherent writer has waiting-inclusive size S_E=O(n^3); the coherent decoder can conservatively be implemented with S_D=O(n^4), including history/waiting. The decoder scans the supplied local energy tables, performs a decreasing move, and repeats at most O(n) times before the Clifford unencoder. Its extension outside the promise is fixed arbitrarily with a uniform cap. Common-span correctability, not separate stochastic error corrections, handles the canonical memory error, capture error and interface error together. For a combined representative E and final syndrome sigma, weight(E_sigma^dagger E)<d_n makes it a stabilizer up to scalar, proving recovery on arbitrary coherent error spans and bath/reference coefficients.

### 9.2 Quantitative complete-channel contract

The exact primary imports are Christandl–Fawzi–Goswami, [arXiv:2408.05260v3](https://arxiv.org/html/2408.05260v3), Lemma 40, equation (128), and Lemmas 41–42, equations (129)–(132). Their full computational-module circuit error is <=2 size(Phi)(cp)^ell, their input-interface good extension is logically identity with an auxiliary state, and their output-interface good part traces only gauge. Their positive bad-interface probabilities are O(cp). The prior proof derives the required complete reference-safe sparse-interface law from these lemmas directly. Theorem 53 alone is a weaker operational communication statement and is not cited as if it literally gave the present diamond theorem.

The resulting circuit contributions are

    WRITE: 2 S_E (cp)^ell,
    READ:  2(n+S_D)(cp)^ell.

For O(n) interfaces, positive all-subset intensity <=p_0^|A| gives discarded support weight <=exp[-n D_Ber(rho||p_0)+O(1)] for fixed rho>p_0. Short-link and gate high-order tails have the form (1). All cutoffs are chosen before the noise/source constants; additional cooling cannot overcome an implementation floor above the target cutoff. In the present hard-basin proof the successful comparison already has exact output support, so no repeated moment-filter loss is required.

With fixed strict margins and ell=O(n), a conservative bound is

    epsilon_total <=epsilon_input+epsilon_output
       +2(S_E+S_D+n)(cp)^ell
       +C_interface exp(-c_interface n)
       +C_link exp(-c_link n)
       +2K_tot delta_round+2G delta_gate+C_entry exp(-c_entry n).

Every term is uniform with an arbitrary reference. Encoded input/output errors are their actual supplied port errors. No final perfect bare decoder is a free physical operation.

### 9.3 Native gates, universal wrappers and the exact open boundary

The accepted two-sector construction retains its verified full code-preserving non-Clifford unitary. Its literal selected CCZ product acts on selected binary 1-components only when all unused binary components and complementary logical coordinates are initialized computational zero. Bitwise CNOT requires identical CSS codes. These are distinct gate conditions; their combination is not a proved universal native gate set.

Universal computation can be purchased with a separately verified active processing/conversion wrapper. This would use known fault-tolerance capabilities and must charge every extraction, conversion, active logical gate, restoration and reset. It earns no new universality or advantage by being attached to this memory.

Aharonov–Ben-Or's measurement-free computation is a powerful candidate for removing noiseless internal classical staging. Its Theorems 10–12 in [quant-ph/9906129](https://arxiv.org/abs/quant-ph/9906129) prove reliable classical-function computation without intermediate measurements/classical operations. Their Section 4.2 expressly permits garbage depending on basis input/output because only classical answers are required. Therefore those statements cannot be imported directly as coherent unknown-state quantum-port factorization. A rigorous replacement still needs sparse raw-measurement-to-classical-packet and packet-to-quantum-control boundary faults, with a complete correlated auxiliary contract. This check prevented an unjustified claim of a completely noisy universal service.

For bare input, an allowed independent dephasing fault before redundancy gives half-diamond floor >=1-(1-p)^k on k input qubits. A noisy final bare release has a corresponding endpoint floor. Protected encoded ports are a substantive operation, not typography around an ideal input.

## 10. Powered two-body implementation with a fixed accuracy budget

Dropping the physical JU term is mathematically legitimate. Retain U solely as a stabilizer-syndrome Lyapunov observable. The ideal reference sweep consists of fixed-patch unitaries U_a on at most q_* DATA-plus-source qubits, followed by discarding each source spin. Every U_a is now a *driven* gate rather than an energy-conserving thermal operation. The same ground-source contraction and finite-cone proof apply to these reference gates. The physical implementation may use one- and two-qubit driven Hamiltonians.

For an explicit conservative compilation bound, put D_*=2^q_*. QR decomposition uses at most D_*(D_*-1)/2 two-level rotations and D_* phases. Gray-code/multiple-control decompositions give an ancilla-free elementary-gate bound

    m_*(q_*) <=C q_*^3 4^q_*

over arbitrary one-qubit rotations and CNOT. Barenco et al., *Elementary gates for quantum computation*, Phys. Rev. A 52, 3457 (1995), DOI 10.1103/PhysRevA.52.3457 / arXiv:quant-ph/9503016, is the primary predecessor. This is deliberately loose; q_* is a fixed locality constant, so the cost is independent of N,K. Ancilla-free synthesis avoids adding uncharged pure work qubits.

If the hardware library is finite and approximately universal, compile each one-qubit rotation to operator error <=delta_syn/(4m_*). A standard Solovay--Kitaev bound supplies

    m_syn <=C_SK m_* log^c_SK(4m_*/delta_syn)

elementary gates, for a fixed inverse-closed universal library and fixed c_SK. Dawson--Nielsen, arXiv:quant-ph/0505030, is the appropriate primary algorithmic source. One must verify the exact library/universality hypotheses; an arbitrary pair of physical controls is not automatically universal. For a continuous rotation library this extra approximation is unnecessary.

Choose a fixed per-patch synthesis error delta_syn and per-microgate actual complete error delta_phys. For c_cat N catalogue gates, each entire sweep has a discrete insertion budget bounded by

    mu_sweep <=c_cat [delta_syn+m_syn delta_phys]
       +mu_src+mu_idle+mu_reset+mu_switch+mu_route.

Here mu_src is the thermal/source-state budget (2 n^(-1) sum q_d for simple qubits, or 2 n^(-1) sum p_bad for the pair source), separate from implementation reset errors. Choose that fixed quantity below the bridge's alpha/(8e) margin. All choices are independent of N,K. No whole-sweep diamond approximation is promised: its distance may be O(N delta_syn); only the local insertion budget is small. This is precisely why exponential global simulation accuracy is unnecessary. The bounded-depth schedule uses at most chi m_syn microgate layers, duration

    tau_sweep <=tau_source+chi m_syn tau_micro+tau_route.

The output cone constant depends on the fixed sequence of catalogue patches; each microgate fault remains inside its patch until that patch completes. A coarse q_*^(chi+O(1)) bound suffices, regardless of m_syn. Peak local drive is a fixed O(1/tau_micro); finite systematic calibration errors and timing jitter enter delta_phys or the integrated local-generator budget. A finite max drive and nonzero noise rate may fail the displayed inequality on real hardware; no useful numerical threshold is inferred.

The source spin can be a thermal qubit of a fixed gap Delta_src at the fixed ambient temperature, with p_src=(1+exp(beta Delta_src))^(-1) below the source-count threshold. It need not have a gap matched to U, because U is not physical energy in this powered representation. Any source preparation/disposal remains charged. Future source spins must be isolated from old B until their turn.

### Thermodynamic and capability accounting

The simplified device is measurement-free active quantum error correction with thermal polarized ancillas and time-dependent two-body drive. It is not a two-body passive self-correcting material, an equilibrium quantum memory or a zero-work refrigerator. Its finite source reserve is O(NK), source/reset/transport events O(NK), elementary control locations O(m_syn NK), and elapsed cooling time K tau_sweep. For smooth local pulses of norm <=Omega and total variation <=C_var Omega per pulse,

    |W_drive| <=C_var Omega m_syn c_cat N K

is a conservative system-Hamiltonian work bound. Actual controller/refrigerator inefficiency is not determined by that bound. Source reserve preparation, transport apparatus and cyclic renewal costs must not be renamed zero simply because U is diagnostic.

This representation closes a finite-body implementation theorem with fixed local accuracy. It does not enable a capability unavailable to the strongest matched active FT machine, which receives the same cooling spins, two-body controls, clock/drive, routing and ports. Hong--Guo--Lucas already construct measurement-free finite-depth Gibbs-sampling circuits in Section 4 and Appendix E of arXiv:2403.10599v3. The generic two-body compilation is established circuit synthesis. Any novelty claim must be confined to a separately established local-contraction/coherent-bath/compiler theorem, not to powered thermal-ancilla QEC itself.


## 11. Exact physical reset import and coherent-noise predecessors

Primary source: Merkli, *Dynamics of Open Quantum Systems II, Markovian
Approximation*, [arXiv:2105.00023v2](https://arxiv.org/html/2105.00023v2),
Theorem 1.1, Proposition 1.3, equations (1.26)–(1.28), (1.33)–(1.42),
(3.48)–(3.52), (3.63)–(3.70). The cached full PDF is SHA256
`8c00223487b6b8276f0502153ad028c8895c190a28151943d9b745d6aeef5017`.

Consider one qubit with `H_A=Delta |1><1| (the source energy basis is relabeled, so |0> is ground)`, `Delta>0`, `G=X`, and an independent
infinite-volume free boson reservoir with dispersion `omega(k)=|k|` in a thermal
state at a fixed positive temperature `T=1/beta`. Take the isotropic real form
factor

```
g(k)=g_rad(|k|),
g_rad(r)=r^3/(1+r^6) [2+e^(-r)].
```

All displayed hypotheses hold:

1. In equation (1.26) choose `p=q=3`, and `h(r)=2+e^(-r)`. Thus `p>2`, `q>2`.
   Every one of `h,h',...,h''''` is bounded on `(0,infinity)`, and its limit at
   zero is respectively `3,-1,1,-1,1`, all nonzero. The radial form factor is
   smooth for `r>0`. Its squared radial `L^2(R^3)` density behaves as `r^8` at
   zero and `r^(-4)` at infinity, both integrable. The usual field relative-bound
   integral `||g/sqrt(omega)||_2` is also finite (powers `r^7` and `r^(-5)`).
2. In the energy eigenbasis, `G_12=1` and `G_11=G_22=0`. The only distinct-energy
   transition gap is `Delta`. The FGR quantity in (1.28) is
   `4 pi g_rad(Delta)^2>0`.
3. With the paper's spectral density
   `S(omega)=(pi/2)omega^2 int_(S^2)|g(omega,Sigma)|^2 dSigma`,
   one has `S(omega)=2 pi^2 omega^2 g_rad(omega)^2`, so `S(Delta)>0`.
4. The level-shift blocks at Bohr frequencies `+/-Delta` are one-dimensional.
   The zero-frequency block has eigenvalues `0` and
   `2i S(Delta)coth(beta Delta/2)`, which are distinct. Hence the simplicity
   assumption holds. Its spectral projections are orthogonal, so the paper's
   projection condition number `kappa` is one. The Bohr-frequency separation is
   `g_Bohr=Delta`; the smallest nonzero decay rate and level-shift gap are fixed
   positive constants. The Lamb-shift principal-value integrals are finite
   under the verified form-factor assumptions.
5. The initial new boson reservoir is thermal and independent of the qubit plus
   all old references. The Hamiltonian is static during the reset dwell. These
   are operational assumptions, not consequences of an accurate ancilla marginal.

Theorem 1.1 therefore supplies, for `|lambda|<c0`, an all-time reduced-channel
estimate of order `C |lambda|^(1/4)`. Proposition 1.3 allows the sufficient
low-temperature bound `c0=c0' T^(76/3)` for this `p>-1/2` qubit case. These are
fixed-dimensional constants; there is no `2^n` many-body factor here. The paper
does not supply a turnkey numerical value of its absolute constants, so this
is an existence-level fixed-accuracy reset construction, not a numerical
hardware specification.

### Complete reset estimate and its precise operational scope

Let `V_t` be the actual reduced qubit channel, let `D_t` be the Davies channel,
and let `R_tau(X)=tau Tr X`. The state-uniform trace estimate extends to all
Hermitian trace-class operators by positive/negative decomposition, and then
to arbitrary operators by real/imaginary decomposition. The standard
fixed-input-dimension inequality `||T||diamond<=2||T||_(1->1)` gives the
conservative bound

```
||V_t-D_t||diamond <=4 C |lambda|^(1/4).           (2.1)
```

Use the generator (1.33), rather than copying a relaxation formula blindly.
Writing

```
r_beta = c_hat_beta(Delta)+c_hat_beta(-Delta)>0,
```

the population displacement from `tau` decays as `exp(-lambda^2 r_beta t)`;
off-diagonals decay as `exp(-lambda^2 r_beta t/2)` up to a unitary phase. A
direct qubit block estimate, uniform over every external reference, gives

```
||D_t-R_tau||diamond <=6 exp(-lambda^2 r_beta t/2). (2.2)
```

The constant six is deliberately conservative: the diagonal displacement
contributes at most four and the two off-diagonal blocks at most two, before
using the slower decay exponent. Thus

```
||V_t-R_tau||diamond
 <=4 C |lambda|^(1/4)+6 exp(-lambda^2 r_beta t/2).  (2.3)
```

For a fixed reset tolerance `epsilon_R>0`, it suffices to choose

```
0<|lambda|<min(c0,(epsilon_R/(8C))^4),
t_reset >= 2/(lambda^2 r_beta) log(12/epsilon_R).
```

Both are constants independent of memory size and runtime, albeit potentially
very poor ones. A finite set of target gaps `Delta in {J,...,JD}` can be handled
by taking the worst constants across that finite set.

There is a visible typographical issue in the primary source: equation (1.37)
prints a minus sign before the Gibbs population term. That would tend to a
negative population and contradicts its immediately preceding fixed-point
equation (1.36). The reset argument above instead derives the positive relaxation
from (1.33). This local typo does not invalidate the all-time approximation
theorem. No questionable printed rate convention is needed in (2.2).

The new outgoing boson bath may be correlated with the qubit and old references.
The complete reset estimate is valid for subsequent operations **only when that
outgoing reservoir is never accessed again**. Its trace is then the genuine
reduced channel in (2.3). One may not silently keep the outgoing reservoir in
the accessible common bath and use (2.3) as a joint reset estimate. The theorem
also cannot be restarted on the same disturbed reservoir for every cycle.
During reset the qubit must be disconnected from DATA except for charged local
disturbances, and the fresh reservoir must be independent of the old accessible
environment. Switching and waiting errors must be charged or supplied through
an explicit reset primitive. The boson field interaction has unbounded full
operator norm; it is not automatically one of the bounded joint `N_Z` noise terms
of the DATA theorem.

A fresh noninteracting finite Gibbs tape is cleaner for a completely finite
requested horizon. The principal/auditor true-Gibbs two-spin source-pair
construction can be used without any Markov approximation. Its `O(nK)` reserve,
private stationary waiting and permanent no-return after use remain charged.
The fixed-qubit Merkli construction is an optional source/reset implementation
with fresh reservoirs; it is not an economical recycled refrigerator theorem.

### Further exact coherent-threshold comparators

### Han–Zhao–Xu–Wang–Liu, 2609.20537v1

Primary source: [*Coherent error threshold for quantum LDPC codes*](https://arxiv.org/html/2609.20537v1),
17 September 2026; cached HTML SHA256
`dbacd5c15ba738560efe1a22a4722d29e1285f9fccb4e5c54093200ed87a2c98`.

The local coherent model is a depth-`D` circuit, `D` fixed, with disjoint gates
per layer on at most `r` qubits, generated by bounded operators of strength
`eta`. Supports need not be geometrically connected. It is followed by perfect
measurement of all stabilizer checks and a CPTP recovery. Theorem 1/rigorous
Theorem 14 gives optimal-recovery code-capacity suppression; Theorem 2/rigorous
Theorem 18 gives minimum-weight recovery. Informal bounds are respectively
`C sqrt(n)e^(-c d_n)` and `C_MW n e^(-c_MW d_n)` for `d_n=Omega(log n)` below
fixed thresholds.

The channel extension in Theorem 15 uses a depth-`D` tensor-product-per-layer
CPTP noise circuit with local strength `half||Phi_alpha-id||diamond<=p`.
With the paper's counting constant `chi`, it gives

```
q(p)=2 chi sqrt(2p),
epsilon_opt <=2 sqrt[D/(chi(1-q))] sqrt(n) q^(d_n/(2r)).
```

Theorem 19 supplies the corresponding minimum-weight channel threshold:
`rho_MW(p)=2^D chi_MW (2p)^(1/(2r))` and
`epsilon_MW<=2n rho_MW^d/[chi_MW(1-rho_MW)]`.

**Actual distinction:** these are strong general qLDPC coherent/channel
**code-capacity** theorems with ideal syndrome measurement and recovery.
The paper explicitly leaves noisy circuit-level extraction and persistent
non-Markovian noise as further problems. It does not implement the finite
temperature lowering sweep or establish its repeated warm-gauge invariant
module. Conversely the current compiler does not supersede the paper's much
broader `d=Omega(log n)` result. For our linear-distance code, the elementary
total-order tail already gives a coherent threshold with sufficiently small
constant total local strength; cluster resummation is not needed for that fact.
Claiming a new general coherent threshold here would be wrong.

### Terhal–Burkard, quant-ph/0402104v2

Primary source: [*Fault-Tolerant Quantum Computation For Local Non-Markovian Noise*](https://arxiv.org/html/quant-ph/0402104),
PRA 71, 012336 (2005), Theorem 1. The noise amplitude is gate time times half
the spectral width of the bounded local system-bath interaction. The displayed
threshold is `Delta_SB t0 <1/[e A_C(A_C-1)]` for their code/gadget assumptions,
with `N polylog(N/sqrt(epsilon))` noisy locations. Crucially their theorem
retains the stated “noninteracting qubits have noninteracting baths” assumption.
It is incorrect to attribute unrestricted common-bath scope to this particular
theorem without its later extensions. The paper explicitly supplies fresh
ancillas prepared offline. The fine-grained coherent fault-path argument is a
direct predecessor to the present norm expansion.

### Aharonov–Kitaev–Preskill, quant-ph/0510231v1

Primary source: [*Fault-tolerant quantum computation with long-range correlated noise*](https://arxiv.org/html/quant-ph/0510231),
PRL 96, 050504 (2006), equations (1)–(5), (22)–(25). The bath Hamiltonian is
arbitrary, while a two-body perturbation `H_SB=sum_(ij)H_ij` can act on each pair
of system qubits and the common bath. A sufficient local strength premise is

```
eta=t0 max_i sum_j ||H_ij|| <eta0.
```

The paper converts this to a standard non-Markovian fault amplitude
`epsilon=e^(1+1/(2e))sqrt(2eta)` and imports the accuracy-threshold machinery.
Algebraic spatial decay faster than `r^(-D)` makes this local sum finite in
dimension `D`. Its higher-body discussion yields the corresponding root-strength
scaling. Thus arbitrarily long quantum computation under a bounded common
coherent bath is established FT capital. The present logical-preservation
tail is not a new principle of non-Markovian fault tolerance.


## 12. Further primary physical-cooling and computation comparators

These are checked comparators, not extra hypotheses of the main proof.

### 12.1 Stronger correlated-initial-state resonance result

Merkli, [arXiv:2107.02515v2](https://arxiv.org/html/2107.02515v2), Theorem 2.2 and equations (2.31)–(2.38), extends the all-time approximation to a specified class of initially correlated states obtained by Kraus operations on the uncoupled equilibrium. The full-observable expansion has a correlation term decaying as `(1+t^3)^(-1)`; that term vanishes identically on system-only observables. The remainder is `O(|lambda|^(1/4))`, with constants depending on the initial correlation operation. This prevents the false assertion that resonance theory only allows product initial states. It still provides no uniform arbitrary-admitted-module bound under an arbitrary persistent computational workload. No blanket initial-correlation no-go is asserted.

### 12.2 Ong–Parameswaran–Placke–Hahn, PRA 114, 042445 (2026)

DOI [10.1103/25wc-17zy](https://doi.org/10.1103/25wc-17zy), [arXiv:2605.03011v2](https://arxiv.org/html/2605.03011v2), 22 October 2026. Theorem 1, equation (41), is a **fixed-point trace-error bound**, not a protected logical-channel theorem. Its cycle resets `n_B` ancillas to pure `|0>`; uses time-dependent Gaussian-filtered interactions; randomizes the final time by a Gaussian of scale `T0`; and averages over those random times. Its exact setup is equations (9)–(15).

Writing `t_J(epsilon)=J^2 tau_mix(epsilon)` for the rescaled mixing time of the reference channel K_LS in equation (24), the bound is

```
2epsilon + t_J n_B exp[beta^2/(4sigma^2)-T^2/(2sigma^2+4T0^2)]
 + J^2 t_J poly(n_B,beta/sigma,T/sigma,T/T0)
       exp[5beta^2/(2sigma^2)].
```

Transferring its mixing bound to the actual channel K also requires equation (25): tau_mix(epsilon/2)||K-K_LS||_(1->1)<=epsilon/2. Equation (77) displays the hidden size dependence: terms include `J^2 n_B beta T^6/(sigma^3 T0^4) exp[9beta^2/(4sigma^2)]`, `t_J J^2 n_B^2 exp[beta^2/(2sigma^2)]`, and `t_J J^2 n_B^2[1+beta T^6/(sigma^3 T0^4)] exp[5beta^2/(2sigma^2)]`. Appendix A Lemmas 1–2 supply fixed-point/mixing perturbation estimates. Theorem 2 bounds random-channel observable variance with channel-contraction/Jordan prefactor `C`, rather than a reference-uniform computation error.

Applicability verdict: the authors explicitly require `t_J=o(J^(-2))` to make the weak-coupling fixed-point error vanish and leave general validation of this scaling open (discussion after equation (42), Section VII). The expected total evolution time scaling (44) is `~O(T t_J^2/epsilon)`, suppressing other parameters. This is substantial physical-sampler machinery and a mandatory comparator, but an exponentially accurate unique Gibbs state is the wrong target for preserving arbitrary logical information. Our route instead proves basin drift at fixed physical precision.

### 12.3 Wang–Ding: finite coupling beyond Lindblad

[arXiv:2512.03457v4](https://arxiv.org/html/2512.03457v4), 19 September 2026, is stronger than saying all rigorous physical samplers require a vanishing coupling with precision. Theorem S2 (rigorous version of Theorem 1), equation (S21), allows a fixed sufficiently small `Gamma=O(1)` while widening the Gaussian filter. It assumes decay of `gamma` at infinity and integrable derivatives of `gamma` and `gamma e^(beta omega)`; its error has rescaled mixing time times `beta log(sigma)/sigma` times the retained multiplier A_gamma=||gamma_prime||_1+||(gamma exp(beta omega))_prime||_1, plus a Gaussian truncation tail. The microscopic algorithm uses a refreshed thermal ancilla, random bath frequency and random signed local coupling [equations (2)–(3)].

Theorem S10 requires `Gamma^2=O(lambda_gap)`, `sigma=~Omega(beta^2/lambda_gap)` and `T=~Omega(sigma)` to transfer a KMS gap to a mixing bound. Theorem 3's thermal end-to-end result has `Gamma=O(N^(-1/2))` and runtime `~O(poly(N) epsilon^(-2))` for its listed models. The fixed-point result's coupling can be independent of precision; its filter width still scales essentially like `beta t_mix A_gamma/epsilon` up to logarithms, at fixed other structural parameters; dropping A_gamma needs its uniform bound. Hence targeting global error `epsilon=e^(-c n)` through that bound incurs an exponential window. This says nothing negative about obtaining a basin moment bound by a more local argument; that is exactly the constructive route above.

### 12.4 Very recent parallel physical-sampler comparator

Ding–Li–Zhang, [arXiv:2611.03422v1](https://arxiv.org/html/2611.03422v1), submitted 2 November 2026, proves arbitrary-initial-state Gibbs preparation for bounded nearest-neighbour one-dimensional qudit chains at every fixed positive temperature. Theorem 1.1/Corollary 9.2 uses `(4^q-1)n` resettable thermal ancillas, randomized bath frequencies and randomized interaction duration, `alpha^2=c epsilon/n`, `T0=Theta(sqrt(log(n/epsilon)))`, and expected Hamiltonian evolution time `~O(n/epsilon)`. Theorem 9.1 explicitly bounds stationary-state bias by `C n alpha^2+C alpha^2 sqrt(n)/T0` and contracts weighted state differences by `1-kappa alpha^2`.

It is a particularly important current comparator: parallel ancillas and finite physical contacts themselves are not new. Its one-dimensional unique-thermalization aim and accuracy-dependent coupling do not supply a noise threshold for repeated non-Clifford processing in our nongeometric code. It also shows why it is too strong to claim that physical system-bath samplers are generically out of reach or lack end-to-end analysis.

### 12.5 Thermal computation and dissipative fault-tolerance precedents

* Rouze–Franca–Alhambra, [arXiv:2403.12691v3](https://arxiv.org/html/2403.12691v3), Theorem II.4, proves BQP-completeness of approximating local observables at outputs of efficiently simulable low-temperature Gibbs samplers, using inverse temperature polynomial in size. Corollary II.5 gives the corresponding classical hardness for fast-mixing observables. This is an established dissipative computation model, with different temperature and input/noise contracts; it is not this fixed-positive-temperature noisy quantum service. It rules out presenting thermal computation itself as a discovery.
* Dunnweber–Styliaris–Trivedi, [arXiv:2601.20818v3](https://arxiv.org/html/2601.20818v3), 25 September 2026, is a stronger autonomous universal comparator. The main theorem gives a 2D local translation-invariant discrete-time QCA, local correlated/non-Markovian fault strength below a nonzero threshold, suitable encoded initial states, `O(N polylog(ND/delta))` qudits and `O(D polylog(ND/delta))` time. Its current text explicitly leaves a formal continuous-time threshold extension for future work (main-text continuous-time discussion and outlook). Do not promote the continuous Lindbladian outline to the proved discrete-time threshold. Do not deny its actual autonomous universality or correlated-noise scope.
* Pastawski–Clemente–Cirac, [arXiv:1010.2901v2](https://arxiv.org/html/1010.2901v2), PRA 83, 012304 (2011), already develops engineered dissipative quantum memories, including local 4D toric-code protection and dissipative ancillary implementation. Broad autonomous correction and ancillary reservoir engineering predate this programme.
* Rojkov–Zapusek–Reiter, [arXiv:2507.12534v2](https://arxiv.org/html/2507.12534v2), introduces trickle-down dissipative correction operators shared across error subspaces, reducing operator counts and improving biased repetition-code performance. Its equations (4)–(7), numerical code sizes and physical effective-dynamics construction must be distinguished: polynomial count does not make the operators geometrically local, and their trapped-ion realization uses effective elimination with unwanted off-resonant transitions. This is a direct conceptual predecessor to descent-based dissipation.
* Scandi–Alhambra, [arXiv:2505.20064v2](https://arxiv.org/html/2505.20064v2), PRX 16, 011040 (2026), and Slezak et al., [arXiv:2601.16154v1](https://arxiv.org/html/2601.16154v1), were screened as microscopic KMS and physical-thermalization alternatives. The former gives time-linear absolute approximation error; the latter gives polynomial-time thermalization in specified high-temperature/weak/1D regimes. They are not imported to assert arbitrary-bath all-time processing. Their full versions are cached; no priority or general applicability claim is inferred from a title or abstract.


### 12.6 A stronger powered nonunital-noise comparator

Shtanko–Sharma, *Complexity of Local Quantum Circuits under Nonunital Noise*, [arXiv:2411.04819v1](https://arxiv.org/abs/2411.04819v1), already constructs measurement-free refrigeration/RESETs from contracting nonunital single-qubit noise and driven circuits. Lemma 7 constructs RESET, Theorem 4 supplies a measurement-free threshold wrapper, and formal Theorem 1 (equation 136) simulates local noiseless-circuit output at sufficiently weak noise with polarization dependence. Its local contracting channel/fixed-point contract and classical final readout are narrower than arbitrary retained-bath quantum I/O. Its exact overhead exponent is not imported here. This comparator further rules out presenting powered thermal-ancilla correction itself as a new capability. See the [exact synthesis/classical-interface audit](../work/physical-cooling-thermal-service-20261107/constructor/COMPILER_AND_CLASSICAL_IMPORT_AUDIT.md).

## 13. Full resources and capability comparison

For K_tot sweeps and G compatible bursts, DATA/current cooling workspace is O(n). Total source consumption and cooling/control contacts are O(nK_tot+nG), before paid ports. The powered two-body representation uses O(m_syn nK_tot) elementary locations and time K_tot tau_sweep; m_syn is a potentially enormous constant. Add routing, timing/ROM, code acquisition, factory switching, preparation, disposal, waiting, protected port blocks and their polynomial staging circuits.

The full physical duration is K_tot tau_sweep+G tau_gate+T_ports, including all source preparation/delivery waits assigned to those durations. A finite precharged bank has O(nK_tot) ACTUAL quantum hardware. For exponential K_tot it is exponential in DATA size. O(n) active source space requires an explicitly charged streaming factory; the finite reserve theorem does not construct an economical indefinitely operating refrigerator. The delivered-source law is not inferred from an unmonitored tape under arbitrary long nonequilibrium noise.

At admissible code lengths the error K exp(-cn) permits n >=(log K+log(1/epsilon)+O(1))/c for target epsilon. Claiming n=O(log(K/epsilon)) uniformly in every size additionally needs a sufficiently dense, effectively available code family. Ordinary fault tolerance already has polylogarithmic computation-size/accuracy overhead under its own noise contracts. For K exponential in n this is polynomial in n, and our polynomial ports must be compared accordingly.

Each energy-conserving collision transfers the opposite DATA energy change to its token. Absolute exchange is <=JD per contact; O(JD nK) is a gross bound, not net heat or refrigerator work. Under unforced nominal HOLD the total signed change of a bounded DATA Hamiltonian is O(n). Sustained cooling current needs compensating input energy. Gates, source-pair decoupling and powered controls do work; source acquisition/disposal and actual refrigerator efficiency are not determined by counting gates.

**Matched inclusion test.** Give the active comparison class the same reset/thermal stream, controls, graph, routing, calibration, timing and encoded ports. It contains a controller executing this identical schedule with the identical channel and resources. Thus this compiler alone cannot establish a strict advantage over that class. This is not a lower bound against future thermal architectures or a claim that a commercial machine is optimal. Removing measured syndrome feedback during HOLD is an operational feature, not a full-cycle advantage.

Hong–Guo–Lucas, [2403.10599v3](https://arxiv.org/html/2403.10599v3), Section 4 and Appendix E.2–E.4, is especially close: finite-depth measurement-free Gibbs sampling with resets and local control/Pauli-rate analysis is established. The defensible synthesis here is a deterministic energy-restoring block with full coherent module/positivity closure for the supplied code. Historical priority of that synthesis is not established.

The achieved capability is an explicit finite implementation of the warm service with fixed local precision. Removal of a dominant affordability obstacle, a favorable full-cost comparison, and a new consequential computational regime are **NOT ACHIEVED**.

## 14. Strongest obstructions and constructive repairs

### 14.1 Exact thermal marginals can cause an uncorrectable logical floor

Let L=P_1...P_w be a nontrivial logical Pauli. Supply ancillas in

    omega=(1-p)|0^w><0^w|+p|1^w><1^w|.

Each marginal is EXACTLY Gibbs for beta Delta=log((1-p)/p). Local controlled-P_j gates implement (1-p)id+p Ad_L. A logical Bell input gives half-diamond error p. Both branches have zero syndrome energy, and the channel fixes the syndrome Hamiltonian's Gibbs state. Exact marginal thermality, fixed points, low energy and local observables therefore do not certify logical preservation. A GHZ purification makes the same obstruction a bath correlation.

Repair: a fresh-block/full-joint source law or another sufficiently strong complete joint fault bound. The independent stationary pair bank is one finite paid realization. A shared recycled refrigerator must earn its own law.

### 14.2 State accuracy is not scalable channel accuracy

The Werner–Holevo channels Phi_±(X)=(Tr(X)I±X^T)/(D±1) differ by trace norm at most 4/(D+1) on every unentangled state. On a maximally entangled reference input their outputs lie in orthogonal symmetric/antisymmetric subspaces, giving diamond distance two. Constant-dimensional reset norm conversion is harmless; applying the same logic to an n-qubit memory can hide an exponential factor.

Repair: use Merkli only for checked constant-size reset modules, or use exact finite sources. A whole-memory reduced-state estimate is not a logical threshold theorem.

### 14.3 Failed shortcuts and their repairs

- A first energy moment permits a constant high-energy component. Warmer hard-supported admission is repaired by v_(j+1)>(1-a)v_j+D_E q_eff alpha, with strict distance/cutoff margins and a floor below u_s. Exponential-moment clipping instead pays its actual square-root loss.
- A channel can leave a logical basin and return to zero energy. The full Stinespring output-cone/canonical argument repairs this gap without intermediate projections.
- A small coherent error near a unitary need not be a positive mixture containing it; unitary Choi rank is one. The successful proof retains signed low orders and repairs positivity from the ACTUAL channel. Deliberate depolarization/Choi interior is an alternative, unnecessary here.
- Fixed additive all-time Markov accuracy does not imply exponentially small logical error. Low-order correctability plus a high-order tail is the repair; actual dynamics can remain globally far from nominal dynamics.
- One faulty global clock/program bit can trigger O(n) strong wrong gates with constant probability. Marginal rates do not satisfy the local joint norm law. A physical controller needs that law or a separately proved protected packet/schedule.
- Fixed depolarizing noise over exponential waiting heats unused source cells to I/2. The private stationary pair model handles a specific waiting problem; generic energy-changing/cross-pair contamination still needs refresh/per-use bounds.
- A discarded reset reservoir cannot be quietly allowed to return. Fresh no-return or a full future-accessible joint reset estimate repairs the inference. General recyclable refrigeration remains open.

## 15. Status, novelty and decisive next operations

| Statement | Status | Exact scope |
| --- | --- | --- |
| Finite collision and deterministic energy contraction | PROVED | Supplied integer energy, dense local descent and full support/incidence bounds. |
| Fixed-temperature coherent-bath warm service | PROVED at stated model | Finite cones, full CPTP dynamics, bounded complete local budgets and delivered-source law; same B retained. |
| CP/TNI comparison and exponential rounds | PROVED | Full canonical module; no normalization or bath/gauge product approximation. |
| Stationary interacting Gibbs pair reserve | PROVED | Private independent pairs and specified waiting dynamics; O(nK) finite hardware. Generic bank contamination excluded. |
| Specified boson-bath local reset | PROVED optional import | Checked fixed-qubit Merkli hypotheses; constant local accuracy; fresh reservoir/no-return, no finite-power/reuse theorem. |
| Two-body driven compilation | PROVED application | Fixed patch/library/precision, large constants and drive/source costs paid; U diagnostic, not passive energy. |
| Noisy encoded WRITE/READ | PROVED restricted transfer | Isolated stochastic staging, short actual links, encoded ports and CFG classical premise. |
| Selected non-Clifford processing | PROVED at earlier gate premises | Selected binary-component/zero-complement assumptions retained. |
| Fully noisy universal wrapper | CONDITIONAL / NOT CLOSED | Reference-safe quantum ports and protected classical boundary interfaces still needed. |
| Affordable full-cost gain | NOT ACHIEVED | Identical active implementation is matched; no favorable numerical threshold or layout estimate. |
| Historical first priority | UNKNOWN | Close predecessors verified; bounded Zenodo discovery does not clear all deposits. |

Thermal operations, measurement-free correction, coherent fault paths, Choi order, subsystem positive repair and fixed-patch synthesis are established ingredients. This dossier earns a specific composite bridge for the supplied dense-descent code, without renaming the ingredients as discoveries.

The decisive constructive targets are:

1. **Recyclable source with joint guarantees and finite power.** A spatially separated conveyor with quantitatively discarded modes, local mixing/decoupling and charged entropy/heat could earn a delivered-block fault law under back-action. Fixed-point fidelity alone cannot.
2. **Fully noisy coherent ports/control.** Protect classical packets, keep sparse raw boundary faults and prove a reference-safe quantum interface. Classical-output correctness does not establish it.
3. **Useful geometry and full-cost gain.** Instantiate tables, patch sizes, pulse counts, source coldness and layout, then compare with the strongest measurement-free/active qLDPC alternative on identical hardware. The finite compiler can have prohibitive constants.
4. **Native universal protected gates.** Verify code switching or teleportation/injection in the same low-energy canonical contract. Stable-duality algebra alone does not supply an addressed logical Hadamard.
5. **Unbounded physical baths.** Replace bounded full-joint norms by energy-constrained complete estimates with stable repeated-gate tails. Neither a reduced Markov approximation nor the current bounded-spin theorem closes this operation.

These remain mathematical tasks, not promises of a breakthrough.

## 16. Reproducible research record

The [record index](../work/physical-cooling-thermal-service-20261107/INDEX.md) links frozen initials, subsequent challenges, primary caches and exact source hashes, finite checks, and the recorded independence-timing limitation. The consolidated theorem uses the deterministic proof; the earlier mgf/relative-observable alternatives remain candidates in their original notes. Artifact hashes/checks do not establish scientific priority.
